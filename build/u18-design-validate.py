from pathlib import Path
from collections import Counter
import hashlib
import json
import unicodedata

O=Path('curriculum/proposals/unit18');issues=[]
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def norm(s):return unicodedata.normalize('NFC',s.strip('.,;:!?“”‘’\"()')).casefold()
def check(ok,kind,**d):
    if not ok:issues.append({'kind':kind,**d})
def index(rows,k):
    out={}
    for r in rows:
        check(r[k] not in out,'duplicate_identity',key=k,identity=r[k]);out[r[k]]=r
    return out
inv=read(O/'inventory.json');plan=read(O/'task-plan.json');hints=read(O/'source-hint-inventory.json');displays=read(O/'display-matrices.json')
lex=read('lexicon/entries.json');gram=read('curriculum/grammar.json');source=read('sources/audits/unit18-source/exercises-prompts.json')
old={'form':{f['form_id']:f for l in lex['lemmas'] for f in l['forms']},'sense':{s['sense_id']:s for l in lex['lemmas'] for s in l['senses']},'feature':{f['feature_id']:f for f in gram['features']}}
new={'form':index([f for l in inv['lemmas'] for f in l['forms']],'form_id'),'sense':index([s for l in inv['lemmas'] for s in l['senses']],'sense_id'),'feature':index(inv['features'],'feature_id')}
reg={k:dict(old[k],**new[k]) for k in old}
owners={k:{r[k+'_id']:l['lemma_id'] for l in lex['lemmas']+inv['lemmas'] for r in l[field]} for k,field in [('form','forms'),('sense','senses')]}
teach=index(inv['teaching_records'],'teaching_id');ev=inv.get('evidence_catalog',{})
valid={'previously_taught','prior_recognition','new_production','new_recognition','supplied'}
def state(k,rid):
    if rid in new[k]:return new[k][rid].get('knowledge_status','unresolved')
    r=old[k].get(rid,{})
    return 'previously_taught' if r.get('production_taught_in') else 'prior_recognition' if r.get('recognition_taught_in') else 'supplied' if r.get('supplied_in') else 'unresolved'
for k,rows in new.items():
    for rid,r in rows.items():
        check(r.get('knowledge_status') in valid,'invalid_status',record_id=rid,status=r.get('knowledge_status'))
        check(bool(r.get('evidence_refs')),'missing_evidence',record_id=rid)
        check(bool(r.get('teaching_ids')),'missing_teaching',record_id=rid)
        for eid in r.get('evidence_refs',[]):check(eid in ev,'unknown_evidence',record_id=rid,evidence_id=eid)
        for tid in r.get('teaching_ids',[]):check(tid in teach,'unknown_teaching',record_id=rid,teaching_id=tid)
        if rid in old[k]:
            if k=='form':
                check(r['form']==old[k][rid]['form'],'prior_surface_changed',record_id=rid)
                check(r['analysis']==old[k][rid]['analysis'],'prior_analysis_changed',record_id=rid)
            if k=='sense':check(r['gloss']==old[k][rid]['gloss'],'prior_gloss_changed',record_id=rid)
            if k=='feature':check(r.get('description')==old[k][rid].get('description'),'prior_description_changed',record_id=rid)

def sequence(s,label):
    words=s.get('learner_text',s.get('text','')).split();ts=s.get('tokens',[])
    check(len(words)==len(ts),'sequence_token_count',sequence=label,words=len(words),tokens=len(ts))
    for i,(w,t) in enumerate(zip(words,ts),1):
        fid=t.get('form_id');sid=t.get('sense_id')
        check(fid in reg['form'],'missing_token_form',sequence=label,position=i,form_id=fid)
        check(sid in reg['sense'],'missing_token_sense',sequence=label,position=i,sense_id=sid)
        if fid in reg['form']:check(norm(w)==norm(reg['form'][fid]['form']),'token_surface',sequence=label,position=i,word=w,form_id=fid)
        if fid in reg['form'] and sid in reg['sense']:check(owners['form'][fid]==owners['sense'][sid]==t.get('lemma_id'),'token_owner',sequence=label,position=i,form_id=fid,sense_id=sid)

tasks=index(plan['tasks'],'task_id');prompts={r['source_item_id']:r['prompt'] for r in source['items']}
check(len(tasks)==60,'task_count',actual=len(tasks));check({k:t['prompt'] for k,t in tasks.items() if k.startswith('EX-')}==prompts,'exact_cook_prompt_crosswalk')
position_ids=[]
for tid,t in tasks.items():
    check(t.get('dependency_status')=='closed','open_task',task_id=tid,status=t.get('dependency_status'))
    position_ids.extend(p['output_position_id'] for p in t['output_positions'])
    for k in reg:
        required=set(t.get('required_'+k+'_ids',[]));tested=set(t.get('tested_'+k+'_ids',[]));supplied=set(t.get('supplied_'+k+'_ids',[]))
        check(tested|supplied<=required,'dependency_scope',task_id=tid,record_kind=k)
        for rid in required:check(state(k,rid) in valid,'unresolved_dependency',task_id=tid,record_kind=k,record_id=rid)
        for rid in tested:
            allowed={'previously_taught','new_production'}|({'new_recognition','prior_recognition'} if any(x in t['mode'] for x in ['analysis','reading','recognition','comprehension']) else set())
            check(state(k,rid) in allowed,'untaught_tested_record',task_id=tid,record_kind=k,record_id=rid,status=state(k,rid))
        for p in t['output_positions']:check(set(p.get('required_'+k+'_ids',[]))<=required,'output_scope',task_id=tid,output_id=p['output_position_id'],record_kind=k)
    for s in t.get('input_sequences',[]):sequence(s,s['sequence_id'])
    for p in t['output_positions']:
        for fld in ['target','essential_meaning','alternatives_policy','error_diagnosis']:check(bool(p.get(fld)),'missing_answer_requirement',output_id=p['output_position_id'],field=fld)
check(len(position_ids)==len(set(position_ids))==87,'output_crosswalk',total=len(position_ids),unique=len(set(position_ids)))
models=index(read(O/'author-only-output-models.json')['models'],'output_position_id')
check(set(models)==set(position_ids),'complete_private_response_contracts')
for oid,m in models.items():
    for field in ['model','target','essential_meaning','explanation','alternatives','error_diagnosis']:
        check(bool(m.get(field)),'missing_private_model_field',output_id=oid,field=field)

check(len(hints['records'])==154,'control_count',actual=len(hints['records']))
for r in hints['records']:
    check(prompts[r['task_id']][r['character_start_zero_based']:r['character_end_exclusive']]==r['literal_source_text'],'control_span',reference_id=r['reference_id'])
    check(r.get('dependency_status')=='bound','unbound_control',reference_id=r['reference_id'])
    check(r.get('independent_recall_assessment') is False,'hint_is_recall',reference_id=r['reference_id'])
    check(bool(r.get('explanatory_content')),'missing_control_explanation',reference_id=r['reference_id'])
for s in hints['sequences']:sequence(s,s['sequence_id'])
check(not hints.get('unresolved'),'hint_unresolved_list',items=hints.get('unresolved'))
check(sum(bool(t.get('source_instructions')) for t in tasks.values())==0,'global_instruction_crosswalk')

cook=read(O/'author-only-cook-sequence-bindings.json')
check(len(cook['sequences'])==47,'cook_model_count')
current_models={r['source_item_id']:r['model'] for r in read('sources/audits/unit18-grammar/candidate-models.json')['rows']}
check({s['owner_id']:s['text'] for s in cook['sequences']}==current_models,'current_independent_model_text_join')

for s in cook['sequences']:
    sequence(s,s['sequence_id']);t=tasks[s['owner_id']]
    for k in ['form','sense']:check({x.get(k+'_id') for x in s['tokens']}<=set(t['required_output_'+k+'_ids']),'model_missing_requirement',task_id=t['task_id'],record_kind=k)
    for x in s['tokens']:
        check(x.get('assessment_role') in ['visible_reference_position','independent_production'],'unclassified_output_position',task_id=t['task_id'],position=x['token_index'])
        if x.get('assessment_role')=='visible_reference_position':check(bool(x.get('reference_route_ids')),'reference_without_route',task_id=t['task_id'],position=x['token_index'])
        else:
            for k in ['form','sense']:check(state(k,x.get(k+'_id')) in ['previously_taught','new_production'],'untaught_independent_position',task_id=t['task_id'],position=x['token_index'],record_kind=k)
check(not cook.get('unresolved'),'cook_unresolved_list',items=cook.get('unresolved'))
orig=read(O/'author-only-original-sequence-bindings.json')
for s in orig['sequences']:sequence(s,s['sequence_id'])
for e in read(O/'compositions.json')['teaching_examples']:sequence(e,e['example_id'])

readings=inv.get('readings',[]);check(len(readings)==1,'reading_count')
if readings:
    r=readings[0];sequence(r,r['source_span_id']);original=read('sources/audits/unit18-source/reading-source.json')['source_spans'][0]
    check(r['learner_text']==original['learner_text'],'source_reading_changed');check(len(r['tokens'])==226,'reading_word_count')
    check(len(r['original_notes'])==22 and len(r['original_note_anchors'])==29,'reading_apparatus_count')
    # Coordinator's independent full-token readback identified this material case
    # distinction; Cook177 note2 explicitly refers the reflexive to184b.
    reflexive=r['tokens'][224]
    check(reflexive.get('form_id')=='ic-acc-pl','reading225_reflexive_accusative',form_id=reflexive.get('form_id'))

    support_index=index(r['local_support'],'support_id')
    for x in r['tokens']:
        check(set(x.get('support_route_ids',[]))<=set(support_index),'unknown_reading_support_route',position=x['token_index'])
        if state('form',x.get('form_id'))=='supplied' or state('sense',x.get('sense_id'))=='supplied':check(bool(x.get('support_route_ids')),'reading_supplied_without_help',position=x['token_index'])

cells={(p['paradigm_id'],c['cell_id']):c for p in inv['paradigms'] for c in p['cells']}
routes=displays['paradigm_cell_display_routes'];matrices=index(displays['matrices'],'matrix_id')
check(len(cells)==sum(len(p['cells']) for p in inv['paradigms']),'duplicate_logical_cell')
check(Counter((r['paradigm_id'],r['logical_cell_id']) for r in routes)==Counter(cells.keys()),'display_route_bijection')
for r in routes:
    m=matrices[r['matrix_id']];ri=r['row_index_zero_based'];ci=r['column_index_zero_based']
    check(m['rows'][ri][ci]==r['surface'] and m['cell_logical_ids'][ri][ci]==r['logical_cell_id'] and m['cell_form_ids'][ri][ci]==r['form_ids'],'literal_route_coordinates',route=[r['paradigm_id'],r['logical_cell_id']])
    check(bool(r['form_ids']) and all(fid in reg['form'] for fid in r['form_ids']),'display_record_missing',route=[r['paradigm_id'],r['logical_cell_id']])
for t in tasks.values():
    for p in t['output_positions']:
        if p['kind']=='form':check((p.get('paradigm_id'),p.get('cell_id')) in cells,'single_form_output_route',output_id=p['output_position_id'])
check(not inv.get('unresolved_integration'),'inventory_unresolved_list',items=inv.get('unresolved_integration'))
check(not plan.get('unresolved'),'task_plan_unresolved_list',items=plan.get('unresolved'))

formtasks=[t for t in tasks.values() if t['task_id'].startswith('NEW-U18-F')]
counts={'tasks':len(tasks),'cook_items':47,'original_tasks':len(tasks)-47,'requested_output_positions':len(position_ids),
    'morphology_output_positions':sum(len(t['output_positions']) for t in formtasks),'morphology_old_english_positions':sum(p['response_language']=='Old English' for t in formtasks for p in t['output_positions']),
    'morphology_single_form_positions':sum(p['kind']=='form' for t in tasks.values() for p in t['output_positions']),
    'morphology_explanation_positions':sum(p['response_language']=='English' for t in formtasks for p in t['output_positions']),
    'lemmas':len(inv['lemmas']),'forms':len(new['form']),'senses':len(new['sense']),'features':len(new['feature']),'paradigms':len(inv['paradigms']),'paradigm_cells':len(cells),'teaching_records':len(teach),
    'source_words':226,'source_notes':22,'source_note_anchors':29,'examples':2,'cook_model_tokens':sum(len(s['tokens']) for s in cook['sequences']),
    'source_controls':len(hints['records']),'hint_input_sequences':len(hints['sequences']),'hint_input_tokens':sum(len(s['tokens']) for s in hints['sequences']),
    'cook_scaffold_input_sequences':sum(len(t.get('input_sequences',[])) for t in tasks.values() if t['task_id'].startswith('EX-')),
    'original_oe_output_tokens':sum(len(s['tokens']) for s in orig['sequences']),**displays['counts']}
if not issues:
    inv['status']='proposal_ready_for_coordinator_reconciliation'
    displays['status']='complete_literal_display_proposal'
    for name,data in [('inventory.json',inv),('display-matrices.json',displays)]:
        (O/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
report={'schema_version':1,'chapter':'ch18','status':'pass' if not issues else 'fail','counts':counts,'issues':issues,
    'methods':['Actual seventeen-unit registers and coverage contracts read before proposals; historical archive grants no teaching credit.','Exact ordered token form/sense owner and surface checks for all inputs, outputs and source reading.','Every original hint/control has its exact visible span and explanatory route; supplied output positions have explicit non-recall support.','Every assigned logical paradigm cell has one literal display route. Existing surfaces, analyses, glosses and descriptions are preserved.','Every requested answer position retains its target, essential meaning, alternatives policy and useful error diagnosis, with one private model and explanation.','Selected model strings equal the independent grammar packet, and reading225 uses the accusative reflexive identity supported by Cook177 note2/184b.'],
    'scope_limit':'Structural dependency and evidence-identity validation; fresh independent learner solving, paradigm review and rendered-page review remain coordinator gates.',
    'input_hashes':{p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(O.glob('*.json')) if p.name!='validation.json'}}
(O/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'status':report['status'],'counts':counts,'issue_count':len(issues)},indent=2));print(json.dumps(issues[:30],ensure_ascii=False,indent=2))
raise SystemExit(bool(issues))
