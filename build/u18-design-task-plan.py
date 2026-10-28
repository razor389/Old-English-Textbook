from pathlib import Path
import copy
import hashlib
import json

OUT=Path('curriculum/proposals/unit18')
def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def dump(name,data):(OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lex=read('lexicon/entries.json'); gram=read('curriculum/grammar.json'); inv=read(OUT/'inventory.json')
forms={f['form_id']:f for l in lex['lemmas'] for f in l['forms']}
senses={s['sense_id']:s for l in lex['lemmas'] for s in l['senses']}
features={f['feature_id']:f for f in gram['features']}
for l in inv['lemmas']:
    forms.update({f['form_id']:f for f in l['forms']});senses.update({s['sense_id']:s for s in l['senses']})
features.update({f['feature_id']:f for f in inv['features']})
public={s['sequence_id']:copy.deepcopy(s) for s in read(OUT/'original-prior-bindings.json')['sequences']}
form_public=read(OUT/'form-input-bindings.json')['sequences']
public.update({s['sequence_id']:copy.deepcopy(s) for s in form_public})
private=read(OUT/'author-only-original-models.json')['models']+read(OUT/'author-only-form-models.json')['models']
models={m['output_position_id']:copy.deepcopy(m) for m in private}
private_sequences={m['output_position_id']:copy.deepcopy(m['output_sequence']) for m in private if m.get('output_sequence')}
private_sequences.update({s['output_position_id']:copy.deepcopy(s) for s in read(OUT/'author-only-form-bindings.json')['sequences']})

def knowledge(record):
    if record.get('production_taught_in'):return 'previously_taught'
    if record.get('recognition_taught_in'):return 'prior_recognition'
    return record.get('knowledge_status','unresolved')
def deps(seqs,kind):return sorted({t[kind+'_id'] for s in seqs for t in s['tokens']})
def finish_task(t):
    t['key_id']=t.get('key_id','KEY-'+t['task_id']);t['key_item_id']=t['key_id']
    t['output_positions']=t.pop('requested_outputs',t.get('output_positions',[]))
    t['task_type']=t.get('kind',t.get('task_type'));t['origin']='new_teaching_material'
    t['input_sequences']=[copy.deepcopy(public[sid]) for sid in t.get('input_sequence_ids',[]) if sid in public]
    for seq in t['input_sequences']:seq['owner_id']=t['task_id']
    outseqs=[]
    visible={tok['surface'].casefold() for s in t['input_sequences'] for tok in s['tokens']}
    visible_senses={tok['sense_id'] for s in t['input_sequences'] for tok in s['tokens']}
    reqfeat=set(t.get('feature_ids',t.get('required_feature_ids',[])))
    for s in t['input_sequences']:reqfeat.update(s.get('feature_ids',s.get('required_feature_ids',[])))
    for pos in t['output_positions']:
        oid=pos['output_position_id'];pos['output_id']=oid
        pos['kind']='translation' if pos['response_language']=='Old English' else 'explanation'
        if oid in private_sequences:
            seq=private_sequences[oid];seq['owner_id']=t['task_id'];seq['output_position_id']=oid;seq['kind']='author_only_output'
            for tok in seq['tokens']:
                if tok.get('assessment_role')!='visible_reference_position':
                    tok['assessment_role']='visible_reference_position' if tok['surface'].casefold() in visible else 'independent_production'
                tok['independent_recall_assessment']=tok['assessment_role']=='independent_production'
                tok['form_assessment_role']=tok['assessment_role']
                tok['sense_assessment_role']='visible_reference_position' if tok['sense_id'] in visible_senses or tok['assessment_role']=='visible_reference_position' else 'independent_production'
            outseqs.append(seq)
            pos['output_sequence_id']=seq['sequence_id']
            reqfeat.update(seq.get('feature_ids',seq.get('required_feature_ids',[])))
            for kind in ['form','sense']:
                pos['required_output_'+kind+'_ids']=deps([seq],kind)
                pos['tested_'+kind+'_ids']=sorted({tok[kind+'_id'] for tok in seq['tokens'] if tok[kind+'_assessment_role']=='independent_production'})
                pos['supplied_'+kind+'_ids']=sorted({tok[kind+'_id'] for tok in seq['tokens'] if tok[kind+'_assessment_role']=='visible_reference_position'})
            pos['reference_output_positions']=[tok['token_index'] for tok in seq['tokens'] if tok['assessment_role']=='visible_reference_position']
            pos['reference_sense_output_positions']=[tok['token_index'] for tok in seq['tokens'] if tok['sense_assessment_role']=='visible_reference_position']
        for kind in ['form','sense']:
            pos['required_input_'+kind+'_ids']=deps(t['input_sequences'],kind)
            pos['required_'+kind+'_ids']=sorted(set(pos.get('required_output_'+kind+'_ids',[]))|set(pos['required_input_'+kind+'_ids']))
            pos.setdefault('tested_'+kind+'_ids',[])
            pos.setdefault('supplied_'+kind+'_ids',[])
        pos['required_feature_ids']=sorted(reqfeat)
    t['required_feature_ids']=sorted(reqfeat)
    for kind,register in [('form',forms),('sense',senses)]:
        t['required_input_'+kind+'_ids']=deps(t['input_sequences'],kind)
        t['required_output_'+kind+'_ids']=deps(outseqs,kind)
        t['required_'+kind+'_ids']=sorted(set(t['required_input_'+kind+'_ids'])|set(t['required_output_'+kind+'_ids']))
        t['tested_'+kind+'_ids']=sorted({rid for p in t['output_positions'] for rid in p['tested_'+kind+'_ids']})
        t['supplied_'+kind+'_ids']=sorted({rid for p in t['output_positions'] for rid in p['supplied_'+kind+'_ids']}|{rid for rid in t['required_input_'+kind+'_ids'] if knowledge(register[rid])=='supplied'})
    t['supplied_feature_ids']=[fid for fid in t['required_feature_ids'] if fid in features and knowledge(features[fid])=='supplied']
    t['tested_feature_ids']=[fid for fid in t['required_feature_ids'] if fid in features and knowledge(features[fid]) in ['previously_taught','new_production','new_recognition','prior_recognition']]
    t['mode']='supported_reading_analysis' if t.get('source_span_id') else 'analysis_and_production' if t['task_id'].split('-')[-1].startswith(('A','F')) else 'independent_production'
    pending=[p['output_position_id'] for p in t['output_positions'] if p['response_language']=='Old English' and p['output_position_id'] not in private_sequences]
    if t.get('source_span_id') or t.get('source_task_refs'):t['dependency_status']='awaiting_exact_source_occurrence_join'
    elif pending:t['dependency_status']='awaiting_exact_verbal_or_reference_join'
    else:t['dependency_status']='closed'
    t['assessment_scope_note']='Visible source hints, given dictionary forms and copied input positions are reference responses. Their independent recall is not tested. Productive status of a lemma never substitutes for a form or sense record.'
    t['dependency_closure_basis']='Every selected input/output token is bound to an actual prior or proposed current form/sense; every requested output remains separately reviewable. Pending source tasks are not certified.'
    return t

seeds=read(OUT/'task-seed.json')['tasks']+read(OUT/'form-task-plan.json')['tasks']
tasks=[finish_task(copy.deepcopy(t)) for t in seeds]
tasks.sort(key=lambda t:(t.get('stage',2),0 if '-F' in t['task_id'] else 1,t['task_id']))
cook=read(OUT/'source-task-crosswalk.json')['cook_items']
for raw in cook:
    t=copy.deepcopy(raw);t['output_positions']=t.pop('requested_outputs');t['origin']='exact_source';t['mode']='English_to_Old_English_with_visible_source_hints'
    t['task_type']='source_translation';t['input_sequences']=[];t['input_sequence_ids']=[]
    for kind in ['form','sense','feature']:
        for scope in ['required','supplied','tested']:t[scope+'_'+kind+'_ids']=[]
    for kind in ['form','sense']:
        for scope in ['input','output']:t['required_'+scope+'_'+kind+'_ids']=[]
    t['dependency_status']='awaiting_exact_source_occurrence_join'
    tasks.append(t)

dump('task-plan.json',{'schema_version':1,'chapter':'ch18','status':'normalized_task_plan; source_occurrence_joins_pending','assignment_rule':'All47 Cook items and all13 newly composed tasks; no silent item omission or output collapse.','tasks':tasks,'counts':{'tasks':len(tasks),'requested_output_positions':sum(len(t['output_positions']) for t in tasks),'closed_tasks':sum(t['dependency_status']=='closed' for t in tasks)}})
dump('public-sequence-bindings.json',{'schema_version':1,'chapter':'ch18','status':'exact_prior_and_current_reference_inputs','sequences':[s for s in public.values() if s['kind']!='worked_example']})
dump('author-only-original-sequence-bindings.json',{'schema_version':1,'chapter':'ch18','visibility':'AUTHOR ONLY. Exclude from fresh blind review until solutions are frozen.','sequences':list(private_sequences.values())})
dump('author-only-output-models.json',{'schema_version':1,'chapter':'ch18','visibility':'AUTHOR ONLY. Exclude from fresh blind review until solutions are frozen.','models':list(models.values())})
examples=copy.deepcopy(read(OUT/'compositions.json')['examples'])
for e in examples:e.update(copy.deepcopy(public[e['sequence_id']]))
dump('composition-bindings.json',{'schema_version':1,'chapter':'ch18','examples':examples,'new_compositions':[],'status':'two_examples_bound_to_actual_prior_form_sense_and_feature_ids'})
print(json.dumps({'tasks':len(tasks),'outputs':sum(len(t['output_positions']) for t in tasks),'closed':sum(t['dependency_status']=='closed' for t in tasks),'public_sequences':len(public),'private_original_sequences':len(private_sequences),'models':len(models)},indent=2))
