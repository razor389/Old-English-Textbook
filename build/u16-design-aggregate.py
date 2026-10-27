import copy
import json
import re
import unicodedata
from collections import defaultdict,Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'curriculum/proposals/unit16'
def read(path,default=None):
    p=ROOT/path
    return json.loads(p.read_text(encoding='utf-8-sig')) if p.exists() else default
def save(name,data):
    (DEST/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

inv=read('curriculum/proposals/unit16/inventory.json')
baseline=read('lexicon/entries.json')['lemmas']
old_lemmas={l['lemma_id']:l for l in baseline}
old_forms={f['form_id']:(l,f) for l in baseline for f in l['forms']}
old_senses={s['sense_id']:(l,s) for l in baseline for s in l['senses']}
old_features={f['feature_id']:f for f in read('curriculum/grammar.json')['features']}
issues=[]

seed=read('curriculum/proposals/unit16/task-seed.json')['tasks']
form_tasks=read('curriculum/proposals/unit16/form-task-plan.json')['tasks']
tasks=copy.deepcopy(form_tasks+seed)
original_models=read('curriculum/proposals/unit16/author-only-form-models.json')['tasks']+read('curriculum/proposals/unit16/author-only-model-seed.json')['tasks']
output_sequences=read('curriculum/proposals/unit16/author-only-form-bindings.json')['sequences']+read('curriculum/proposals/unit16/author-only-sequence-bindings.json')['sequences']
public_sequences=read('curriculum/proposals/unit16/form-input-bindings.json')['sequences']+read('curriculum/proposals/unit16/public-sequence-bindings.json')['sequences']
cook_sequences=read('curriculum/proposals/unit16/author-only-cook-sequence-bindings.json')['sequences']
cook_models=read('sources/audits/unit16-grammar/author-only-cook-models.json')['items']
prompts=read('sources/audits/unit16-source/exercises-prompts.json')['items']
cook_model_by_id={m['source_item_id']:m for m in cook_models}
for p in prompts:
    tid=p['source_item_id'];m=cook_model_by_id[tid];oid=tid+'-O001'
    tasks.append({'task_id':tid,'source_item_id':tid,'source_locator':copy.deepcopy(p),'origin':'exact_source','prompt':p['prompt'],
        'task_type':'source_production','inputs':[],'required_feature_ids':[],
        'target_specification':'; '.join(m.get('grammar_targets',[])),
        'output_positions':[{'output_position_id':oid,'output_id':oid,'kind':'old_english_translation','label':'Complete original Cook item','response_language':'Old English'}],
        'local_support':[],'grading_obligations':{'essential_meaning':p['prompt'],'target':'; '.join(m.get('grammar_targets',[])),
            'defensible_alternatives':'Accept a grammatical alternative preserving every English clause and relationship; separately assess explicit Cook lexical, number, omission and order controls.',
            'source_prompt_integrity':'The source prompt is exact and complete; modern corrections and helps remain separate.'}})
    original_models.append({'task_id':tid,'outputs':[{'output_position_id':oid,'output_id':oid,'model':m['model'],
        'essential_meaning':p['prompt'],'target_compliance':'; '.join(m.get('grammar_targets',[])),
        'valid_alternatives':'See the explicit source amendments and supplied-frame notes. Grammaticality and compliance with each Cook control must be assessed separately.',
        'source_evidence_refs':m.get('source_evidence_refs',[])}]})

support_packets=[read(p,{}) for p in ['sources/audits/unit16-grammar/source-support.json','sources/audits/unit16-source/reading-support.json','sources/audits/unit16-source/exercise-support.json','sources/audits/unit16-source/exercises-dependencies.json']]
supports=[]
for packet in support_packets:
    for key in ('cook_support','supports','local_support'):
        if isinstance(packet.get(key),list):supports.extend(packet[key])
dependencies=[]
for path in ['sources/audits/unit16-grammar/exercises-verbal-dependencies.json','sources/audits/unit16-source/exercises-dependencies.json']:
    packet=read(path)
    if not packet:
        issues.append({'kind':'pending_dependency_packet','path':path});continue
    for key in ('items','dependencies','tasks'):
        if isinstance(packet.get(key),list):dependencies.extend(packet[key]);break

source=read('sources/audits/unit16-source/reading-source.json')['source_spans'][0]
reading=copy.deepcopy(source)
ledger=read('sources/audits/unit16-source/reading-token-ledger.json',{'tokens':[],'unresolved':['missing ledger']})
reading_tokens=[]
for n,t in enumerate(ledger['tokens'],1):
    token=copy.deepcopy(t)
    token['token_index_one_based']=n
    token.setdefault('source_surface',t.get('surface',''))
    token.setdefault('form',t.get('surface',''))
    token.setdefault('form_status',t.get('knowledge_status','unresolved'))
    token.setdefault('source_line_ids',[t['source_line_id']] if t.get('source_line_id') else [])
    reading_tokens.append(token)
reading['tokens']=reading_tokens
apparatus=read('sources/audits/unit16-source/reading-apparatus.json')
reading['original_notes']=copy.deepcopy(apparatus['notes'])
anchors=[]
for note in reading['original_notes']:
    nid=note['apparatus_id']
    note['display_id']=nid.replace('FB-U16-','P').replace('-N','N')
    for anchor in note.get('anchors',[]):
        anchors.append(dict(copy.deepcopy(anchor),apparatus_id=nid,display_id=note['display_id']))
reading['original_note_anchors']=anchors
reading_support=read('sources/audits/unit16-source/reading-support.json',{})
reading_constructions=read('sources/audits/unit16-source/reading-constructions.json',{})
reading['modern_support']=reading_support.get('reading_support',reading_support.get('supports',reading_support.get('items',[])))
reading['nominal_and_function_glossary']=reading_support.get('nominal_and_function_glossary',[])
reading['verbal_glossary']=read('sources/audits/unit16-grammar/reading-verbal-support.json',{}).get('items',[])
reading['latin_accessibility']=reading_support.get('latin_accessibility',{})
reading['construction_notes']=reading_constructions.get('constructions',reading_constructions.get('items',[]))
reading['original_apparatus_policy']='Keep all original notes verbatim and page-specific labels separate from modern English support. Original Latin parallels receive English sense support; no Latin analysis is assigned.'
if ledger.get('unresolved'):issues.append({'kind':'reading_ledger_unresolved','count':len(ledger['unresolved'])})

in_by_owner=defaultdict(list);out_by_owner=defaultdict(list)
for seq in public_sequences:in_by_owner[seq['owner_id']].append(seq)
for seq in output_sequences+cook_sequences:out_by_owner[seq['owner_id']].append(seq)
model_by_task={t['task_id']:t for t in original_models}
feature_map={f['feature_id']:f for f in inv['features']}
lemmas={l['lemma_id']:l for l in inv['lemmas']}

def import_prior(rid,kind):
    pool=old_forms if kind=='form' else old_senses
    if rid not in pool:
        issues.append({'kind':'missing_'+kind,'id':rid});return
    old_l,old=pool[rid];lid=old_l['lemma_id']
    if lid not in lemmas:
        lemmas[lid]={k:copy.deepcopy(v) for k,v in old_l.items() if k not in ('forms','senses')}
        lemmas[lid]['forms']=[];lemmas[lid]['senses']=[];lemmas[lid]['prior_lemma_present']=True
    key=kind+'_id';coll=lemmas[lid]['forms' if kind=='form' else 'senses']
    if any(x[key]==rid for x in coll):return
    record=copy.deepcopy(old)
    record['knowledge_status']='previously_taught' if old.get('production_taught_in') else 'prior_recognition' if old.get('recognition_taught_in') else 'supplied'
    record['prior_scope']={k:old.get(k) for k in ('production_taught_in','recognition_taught_in','supplied_in','coverage_contract')}
    record['teaching_ids']=['NEW-U16-PRIOR-RECALL']
    record['used_in_tasks']=[];record['assessed_in']=[]
    coll.append(record)

def refresh():
    return ({f['form_id']:(l,f) for l in lemmas.values() for f in l['forms']}, {s['sense_id']:(l,s) for l in lemmas.values() for s in l['senses']})
forms,senses=refresh()
all_sequences=public_sequences+output_sequences+cook_sequences+read('curriculum/proposals/unit16/composition-bindings.json')['sequences']
all_tokens=[t for s in all_sequences for t in s['tokens']]+reading_tokens
for token in all_tokens:
    if token.get('form_id') and token['form_id'] not in forms:import_prior(token['form_id'],'form')
    if token.get('sense_id') and token['sense_id'] not in senses:import_prior(token['sense_id'],'sense')
forms,senses=refresh()

def record_status(record):
    return record.get('knowledge_status','unresolved')
def ids_from(tokens,kind):
    return sorted({t[kind+'_id'] for t in tokens if t.get(kind+'_id')})
def support_bindings(tokens):
    result=[]
    for t in tokens:
        if t.get('form_id') not in forms or t.get('sense_id') not in senses:continue
        lid,f=forms[t['form_id']];sl,s=senses[t['sense_id']]
        if record_status(f) in ('supplied','prior_recognition','new_recognition') or record_status(s) in ('supplied','prior_recognition','new_recognition'):
            result.append({'lemma_id':lid['lemma_id'],'form_id':f['form_id'],'sense_id':s['sense_id'],'form':f['form'],
                'form_status':record_status(f),'sense_status':record_status(s),'gloss':s.get('contextual_gloss',s.get('gloss','')),
                'analysis':t.get('contextual_analysis',t.get('analysis',f['analysis'])),
                'evidence_refs':sorted(set(f.get('evidence_refs',[])+s.get('evidence_refs',[])))})
    return list({(x['form_id'],x['sense_id']):x for x in result}.values())

def plain_words(text):
    return [unicodedata.normalize('NFC',w.strip('.,;:!?‘’“”\"\'()[]')).casefold() for w in text.split()]

def scaffold_positions(task,sequence):
    words=plain_words(sequence['text']);position_supports=defaultdict(list)
    for support in task.get('local_support',[]):
        text=support.get('actual_supplied_text')
        if not text:continue
        cursor=0
        lexical_family=support.get('support_id','').startswith('U16-CSUP-')
        segments=re.split(r';|/|\.{3}|…',text) if lexical_family else re.split(r'\.{3}|…',text)
        for segment in segments:
            selected=plain_words(segment)
            if not selected:continue
            starts=[i for i in range(0 if lexical_family and '...' not in text else cursor,len(words)-len(selected)+1) if words[i:i+len(selected)]==selected]
            if not starts:
                if not lexical_family:issues.append({'kind':'supplied_frame_alignment','task_id':task['task_id'],'support_id':support.get('support_id'),'unmatched_segment':segment})
                continue
            start=starts[0];cursor=start+len(selected)
            for i in range(start+1,cursor+1):position_supports[i].append(support['support_id'])
    for t in sequence['tokens']:
        if t['form_id'] in task['supplied_form_ids'] or t['sense_id'] in task['supplied_sense_ids']:
            position_supports[t['token_index']].append('U16-HELP-'+task['task_id']+'-LEXICAL')
    return position_supports

def supplied_input_sequences(task):
    result=[]
    for support in task.get('local_support',[]):
        text=support.get('actual_supplied_text')
        if not text:continue
        sid=support['support_id']
        lexical_family=sid.startswith('U16-CSUP-')
        pieces=re.split(r';|/|\.{3}|…',text) if lexical_family else re.split(r'\.{3}|…',text)
        candidate_tasks=support.get('source_item_ids',[support.get('source_item_id',task['task_id'])])
        cursors=defaultdict(int)
        for number,piece in enumerate(pieces,1):
            piece=piece.strip();wanted=plain_words(piece)
            if not wanted:continue
            found=None
            for owner in candidate_tasks:
                for sequence in out_by_owner[owner]:
                    words=plain_words(sequence['text'])
                    start_min=cursors[owner] if '...' in text else 0
                    starts=[i for i in range(start_min,len(words)-len(wanted)+1) if words[i:i+len(wanted)]==wanted]
                    if starts:
                        start=starts[0];found=(sequence,start);cursors[owner]=start+len(wanted);break
                if found:break
            if not found:
                issues.append({'kind':'unbound_supplied_input','support_id':sid,'task_id':task['task_id'],'text':piece});continue
            source_seq,start=found
            bound=[]
            for pos,original in enumerate(source_seq['tokens'][start:start+len(wanted)],1):
                tok=copy.deepcopy(original);tok['source_model_token_index']=original['token_index'];tok['token_index']=pos
                tok['literal']=piece.split()[pos-1];tok['surface']=tok['literal'].strip('.,;:!?‘’“”\"\'()[]')
                tok['input_role']='supplied_scaffold_not_unaided_recall'
                bound.append(tok)
            result.append({'sequence_id':task['task_id']+'-'+sid+f'-INPUT-{number:02d}','owner_id':task['task_id'],'kind':'input',
                'text':piece,'tokens':bound,'support_id':sid,'source_model_sequence_id':source_seq['sequence_id'],
                'required_form_ids':ids_from(bound,'form'),'required_sense_ids':ids_from(bound,'sense'),
                'status':'exact_supplied_segments_bound'})
    return result

for task in tasks:
    tid=task['task_id'];task['key_id']=task.get('key_item_id','KEY-'+tid);task['key_item_id']=task['key_id']
    inputs=in_by_owner[tid];outputs=out_by_owner[tid]
    input_tokens=[t for s in inputs for t in s['tokens']]
    output_tokens=[t for s in outputs for t in s['tokens']]
    is_reading=tid.startswith('NEW-U16-R')
    if is_reading:
        input_tokens+=reading_tokens
        task['source_span_ids']=[reading['source_span_id']]
    feature_ids=set(task.get('required_feature_ids',[]))
    for dep in dependencies:
        if (dep.get('source_item_id') or dep.get('task_id'))!=tid:continue
        for key in ('feature_ids','required_feature_ids','grammar_feature_ids','new_productive_feature_ids','visible_supplied_feature_ids'):
            feature_ids.update(dep.get(key,[]))
        for prior in dep.get('prior_feature_dependencies',[]):
            feature_ids.add(prior['feature_id'])
        for frame in dep.get('lexical_frame_assignments',[]):
            if isinstance(frame,dict) and frame.get('feature_id'):feature_ids.add(frame['feature_id'])
            elif isinstance(frame,str) and frame in feature_map:feature_ids.add(frame)
        if dep.get('interpretation_and_control_audit'):
            task.setdefault('grading_obligations',{})['interpretation_and_control_audit']=dep['interpretation_and_control_audit']
            for target in model_by_task[tid]['outputs']:
                target['explanation']=dep['interpretation_and_control_audit']
        task.setdefault('source_control_strings',[]).extend(dep.get('source_control_strings',[]))
    if is_reading:
        for f in reading_constructions.get('features',[]):
            feature_ids.add(f['feature_id'])
        for note in reading['construction_notes']:
            if note.get('feature_id'):feature_ids.add(note['feature_id'])
            feature_ids.update(note.get('feature_ids',[]))
    for support in supports:
        assigned=support.get('source_item_id')==tid or tid in support.get('source_item_ids',support.get('task_ids',[]))
        if assigned:
            task.setdefault('local_support',[]).append(copy.deepcopy(support))
            if support.get('feature_id'):feature_ids.add(support['feature_id'])
            elif support.get('support_id','').startswith('U16-CSUP-'):feature_ids.add(support['support_id']+'-FRAME')
    if tid.startswith('EX-'):
        supplied_sequences=supplied_input_sequences(task)
        inputs+=supplied_sequences
        input_tokens += [t for s in supplied_sequences for t in s['tokens']]
    for token in output_tokens:
        # Lexical teaching records may name their separately bounded frame directly.
        if token['sense_id'] in senses:
            for teaching_id in senses[token['sense_id']][1].get('teaching_ids',[]):
                if teaching_id in feature_map:feature_ids.add(teaching_id)
    task['required_feature_ids']=sorted(feature_ids)
    task['input_sequences']=copy.deepcopy(inputs);task['input_sequence_ids']=[s['sequence_id'] for s in inputs]
    task['required_input_form_ids']=ids_from(input_tokens,'form');task['required_input_sense_ids']=ids_from(input_tokens,'sense')
    task['required_output_form_ids']=ids_from(output_tokens,'form');task['required_output_sense_ids']=ids_from(output_tokens,'sense')
    task['required_form_ids']=sorted(set(task['required_input_form_ids']+task['required_output_form_ids']))
    task['required_sense_ids']=sorted(set(task['required_input_sense_ids']+task['required_output_sense_ids']))
    supplied=support_bindings(input_tokens+output_tokens)
    # A supplied citation form does not supply every inflection of its sense;
    # a supplied contextual sense does not supply other uses of its form.
    nonproductive_statuses={'supplied','prior_recognition','new_recognition'}
    task['supplied_form_ids']=sorted({x['form_id'] for x in supplied if x['form_status'] in nonproductive_statuses})
    task['supplied_sense_ids']=sorted({x['sense_id'] for x in supplied if x['sense_status'] in nonproductive_statuses})
    if supplied:
        task.setdefault('local_support',[]).append({'support_id':'U16-HELP-'+tid+'-LEXICAL','type':'explicit_word_help',
            'title':'Forms and meanings supplied for this task','bindings':supplied,
            'text':'Print each bound form, its contextual grammatical role, and its English gloss before the task. These positions are scaffolded; independent recall is not assessed.',
            'evidence_refs':sorted({r for x in supplied for r in x['evidence_refs']})})
    task['scaffolded_output_positions']=[]
    independent_tokens=[]
    for sequence in outputs:
        covered=scaffold_positions(task,sequence)
        input_headword_ids={t['form_id'] for s in inputs if '-HEADWORD-' in s['sequence_id'] for t in s['tokens']}
        for token in sequence['tokens']:
            n=token['token_index']
            token.pop('support_ids',None)
            if n in covered:
                token['assessment_role']='supplied_position_not_unaided_recall'
                token['support_ids']=sorted(set(covered[n]))
                task['scaffolded_output_positions'].append({'sequence_id':sequence['sequence_id'],'output_position_id':sequence.get('output_position_id'),
                    'token_index':n,'form_id':token['form_id'],'sense_id':token['sense_id'],'support_ids':token['support_ids']})
            elif token['form_id'] in input_headword_ids:
                token['assessment_role']='given_dictionary_form_position_identification_not_unaided_recall'
            else:
                token['assessment_role']='independent_production'
                independent_tokens.append(token)
    task['tested_form_ids']=ids_from(independent_tokens,'form')
    task['tested_sense_ids']=ids_from(independent_tokens,'sense')
    task['assessment_scope_note']='Only output tokens marked independent_production assess unaided production. Exact supplied frames/words and answers identical to a given dictionary form retain their supplied/reference roles; all requested complete responses still have a specific model.'
    task['supplied_feature_ids']=[fid for fid in feature_ids if feature_map.get(fid,{}).get('knowledge_status')=='supplied']
    task['tested_feature_ids']=[fid for fid in feature_ids if fid not in task['supplied_feature_ids']]
    task['mode']='supported_reading_analysis' if is_reading else 'supported_production_translation' if tid.startswith('EX-') else 'form_production' if tid.startswith('NEW-U16-F') else 'composition' if tid.startswith('NEW-U16-C') else 'analysis_and_rewrite'
    task['dependency_status']='integration_pending'
    seq_by_output={s.get('output_position_id'):s for s in outputs}
    for pos in task['output_positions']:
        oid=pos['output_position_id'];seq=seq_by_output.get(oid)
        ptokens=seq['tokens'] if seq else input_tokens
        pos['required_form_ids']=ids_from(ptokens,'form');pos['required_sense_ids']=ids_from(ptokens,'sense')
        pos['required_feature_ids']=task['required_feature_ids']
        independent=[t for t in seq['tokens'] if t.get('assessment_role')=='independent_production'] if seq else []
        pos['tested_form_ids']=ids_from(independent,'form')
        pos['tested_sense_ids']=ids_from(independent,'sense')
        pos['scaffolded_token_positions']=[p['token_index'] for p in task['scaffolded_output_positions'] if p['output_position_id']==oid]
        pos['supplied_form_ids']=[fid for fid in pos['required_form_ids'] if fid in task['supplied_form_ids']]
        pos['supplied_sense_ids']=[sid for sid in pos['required_sense_ids'] if sid in task['supplied_sense_ids']]
        pos['required_output_form_ids']=ids_from(seq['tokens'],'form') if seq else []
        pos['required_output_sense_ids']=ids_from(seq['tokens'],'sense') if seq else []
        pos['required_input_form_ids']=task['required_input_form_ids']
        pos['required_input_sense_ids']=task['required_input_sense_ids']
        if oid not in {m['output_position_id'] for m in model_by_task[tid]['outputs']}:
            issues.append({'kind':'missing_output_model','task_id':tid,'output_position_id':oid})
    if tid.startswith('EX-') and (not outputs or len(output_tokens)!=len(outputs[0]['text'].split())):
        issues.append({'kind':'incomplete_cook_binding','task_id':tid})

for task in tasks:
    for fid in task['required_feature_ids']:
        if fid not in feature_map:
            if fid in old_features:
                f=copy.deepcopy(old_features[fid]);f['prior_scope']={k:f.get(k) for k in ('production_taught_in','recognition_taught_in','supplied_in','coverage_contract')}
                f['knowledge_status']='previously_taught' if f.get('production_taught_in') else 'prior_recognition' if f.get('recognition_taught_in') else 'supplied'
                f['teaching_ids']=['NEW-U16-PRIOR-RECALL'];f['used_in_tasks']=[];f['assessed_in']=[];feature_map[fid]=f
            else:issues.append({'kind':'missing_feature','id':fid,'task_id':task['task_id']})
    for kind,pool in [('form',forms),('sense',senses),('feature',feature_map)]:
        for rid in task['required_'+kind+'_ids']:
            if rid not in pool:continue
            rec=pool[rid][1] if kind!='feature' else pool[rid]
            rec.setdefault('used_in_tasks',[])
            if task['task_id'] not in rec['used_in_tasks']:rec['used_in_tasks'].append(task['task_id'])
            if rid in task.get('tested_'+kind+'_ids',[]):
                rec.setdefault('assessed_in',[])
                if task['task_id'] not in rec['assessed_in']:rec['assessed_in'].append(task['task_id'])

compositions=read('curriculum/proposals/unit16/composition-seed.json')
example_sequences={s['owner_id']:s for s in read('curriculum/proposals/unit16/composition-bindings.json')['sequences']}
for e in compositions['teaching_examples']:
    seq=example_sequences[e['example_id']]
    e['input_sequence']=seq;e['tokens']=copy.deepcopy(seq['tokens']);e['form_ids']=seq['required_form_ids'];e['sense_ids']=seq['required_sense_ids'];e['status']='exact_tokens_bound_pending_reconciliation'
    for fid in e['feature_ids']:
        if fid not in feature_map and fid in old_features:
            f=copy.deepcopy(old_features[fid]);f['knowledge_status']='previously_taught' if f.get('production_taught_in') else 'prior_recognition';f['teaching_ids']=['NEW-U16-PRIOR-RECALL'];feature_map[fid]=f
        elif fid not in feature_map:issues.append({'kind':'missing_example_feature','id':fid})

teaching={t['teaching_id']:t for t in inv['teaching_records']}
records=[('form',f) for l in lemmas.values() for f in l['forms']]+[('sense',s) for l in lemmas.values() for s in l['senses']]+[('feature',f) for f in feature_map.values()]
for kind,record in records:
    for tid in record.get('teaching_ids',[]):
        target=teaching.setdefault(tid,{'teaching_id':tid,'type':'prior_recall' if tid=='NEW-U16-PRIOR-RECALL' else 'explicit_teaching_record','form_ids':[],'sense_ids':[],'feature_ids':[],'evidence_refs':[]})
        target.setdefault(kind+'_ids',[]).append(record[kind+'_id']);target.setdefault('evidence_refs',[]).extend(record.get('evidence_refs',[]))
for e in compositions['teaching_examples']:
    teaching[e['example_id']]={'teaching_id':e['example_id'],'type':'translated_teaching_example','graded':False,'form_ids':e['form_ids'],'sense_ids':e['sense_ids'],'feature_ids':e['feature_ids'],
        'text':e['text'],'translation':e['translation'],'scope_note':e['pedagogical_purpose'],'evidence_refs':sorted({r for t in e['input_sequence']['tokens'] for r in forms[t['form_id']][1].get('evidence_refs',[])})}
for t in teaching.values():
    for key in ('form_ids','sense_ids','feature_ids','evidence_refs'):t[key]=sorted(set(t.get(key,[])))
    t.setdefault('title','Prior forms and bounded uses recalled for the current tasks' if t['teaching_id']=='NEW-U16-PRIOR-RECALL' else t['teaching_id'])

outcomes=read('curriculum/proposals/unit16/outcomes.json')
for key in ('productive_outcomes','recognition_outcomes','bounded_scope','study_sequence'):
    inv[key]=outcomes.get(key,[])
inv['readings']=[reading];inv['lemmas']=list(lemmas.values());inv['features']=list(feature_map.values());inv['teaching_records']=list(teaching.values())
inv['prior_requirements']={'baseline':'e1d94be','form_ids':sorted(fid for fid in forms if fid in old_forms),'sense_ids':sorted(sid for sid in senses if sid in old_senses),'feature_ids':sorted(fid for fid in feature_map if fid in old_features),
    'rule':'These references preserve exact prior form/sense identities and milestones. A prior recognition/supplied record is not promoted unless an explicit current teaching record does so.'}
inv['pre_key_review_exclusions']=['curriculum/proposals/unit16/author-only-*','sources/audits/unit16-grammar/author-only-cook-models.json','sources/audits/unit16-grammar/initial-independent-models.json','sources/audits/unit16-coordinator/*translation*','build/u16-design-*']
inv['new_material_examples']=compositions['teaching_examples'];inv['new_compositions']=[]
inv['source_task_crosswalk']=read('curriculum/proposals/unit16/source-task-crosswalk.json')
inv['teaching_order_rule']='Display morphology, basic uses, vocabulary senses and translated examples before independent output; print every supplied frame and lexical help beside its task. The full reading has its original notes and modern support before the reading tasks.'
inv['promotions']=[{'kind':kind,'id':r[kind+'_id'],'prior_scope':r.get('prior_scope'),'new_scope':r['knowledge_status'],'teaching_ids':r.get('teaching_ids',[])} for kind,r in records if r.get('prior_scope') and not r['prior_scope'].get('production_taught_in') and r.get('knowledge_status')=='new_production']
counts={'tasks':len(tasks),'cook_items':59,'original_tasks':len(tasks)-59,'requested_output_positions':sum(len(t['output_positions']) for t in tasks),
    'morphology_output_positions':sum(len(t['output_positions']) for t in form_tasks),'morphology_old_english_positions':sum(len(t['outputs']) for t in read('curriculum/proposals/unit16/author-only-form-models.json')['tasks'])-8,
    'morphology_single_form_positions':sum(p['kind']=='form' for t in form_tasks for p in t['output_positions']),
    'morphology_phrase_positions':sum(p['kind']=='old_english_translation' for t in form_tasks for p in t['output_positions']),
    'morphology_explanation_positions':sum(p['kind']=='explanation' for t in form_tasks for p in t['output_positions']),
    'morphology_form_tokens':sum(len(s['tokens']) for s in read('curriculum/proposals/unit16/author-only-form-bindings.json')['sequences']),
    'lemmas':len(lemmas),'forms':len(forms),'senses':len(senses),'features':len(feature_map),'paradigms':len(inv['paradigms']),
    'paradigm_cells':sum(len(p['cells']) for p in inv['paradigms']),'teaching_records':len(teaching),'source_words':444,'source_notes':54,'source_note_anchors':59,'examples':4,
    'cook_model_tokens':sum(len(s['tokens']) for s in cook_sequences),'original_oe_input_tokens':sum(len(s['tokens']) for s in public_sequences),
    'cook_scaffold_input_sequences':sum(len(t['input_sequences']) for t in tasks if t['task_id'].startswith('EX-')),
    'cook_scaffold_input_tokens':sum(len(s['tokens']) for t in tasks if t['task_id'].startswith('EX-') for s in t['input_sequences']),
    'original_oe_output_tokens':sum(len(s['tokens']) for s in output_sequences)}
inv['counts']=counts
missing_evidence=sorted({ref for _,r in records for ref in r.get('evidence_refs',[]) if ref not in inv['evidence_catalog']})
if missing_evidence:issues.append({'kind':'missing_evidence_refs','ids':missing_evidence})
for conflict in inv.get('unresolved_integration',{}).get('conflicts',[]):issues.append(conflict)
inv['unresolved_integration']={'issues':issues}
inv['status']='integration_candidate_not_sealed'
save('inventory.json',inv)
save('task-plan.json',{'schema_version':1,'chapter':'ch16','status':'integration_candidate_not_sealed','assignment_rule':'All59 exact Cook prompts plus17 original tasks; no omitted clauses or unrecorded deferrals.','tasks':tasks})
save('compositions.json',compositions)
save('author-only-output-models.json',{'schema_version':1,'chapter':'ch16','visibility':'author_only','tasks':original_models})
save('author-only-cook-sequence-bindings.json',{'schema_version':1,'chapter':'ch16','visibility':'author_only','status':'contextually_bound_with_scaffold_roles','sequences':cook_sequences})
save('author-only-original-sequence-bindings.json',{'schema_version':1,'chapter':'ch16','visibility':'author_only','sequences':output_sequences})
save('reading-token-bindings.json',{'schema_version':1,'chapter':'ch16','source_span_id':reading['source_span_id'],'tokens':reading_tokens,'status':ledger.get('status')})
save('validation.json',{'schema_version':1,'chapter':'ch16','status':'integration_candidate_not_sealed','counts':counts,'issues':issues})
print(json.dumps({'counts':counts,'issue_count':len(issues),'issue_kinds':dict(Counter(x.get('kind','conflict') for x in issues))},ensure_ascii=False))
