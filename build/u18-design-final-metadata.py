from pathlib import Path
import json,copy,hashlib
from collections import Counter
O=Path('curriculum/proposals/unit18')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
inv=read(O/'inventory.json');outcomes=read(O/'outcomes.json');tasks=read(O/'task-plan.json')['tasks'];displays=read(O/'display-matrices.json')
lex=read('lexicon/entries.json');gram=read('curriculum/grammar.json')
old={'form':{f['form_id']:f for l in lex['lemmas'] for f in l['forms']},'sense':{s['sense_id']:s for l in lex['lemmas'] for s in l['senses']},'feature':{f['feature_id']:f for f in gram['features']}}
for k in ['productive_outcomes','recognition_outcomes','bounded_scope','study_sequence','teaching_order_rule']:inv[k]=copy.deepcopy(outcomes[k])
if isinstance(inv['bounded_scope'],list):inv['bounded_scope']={'explicit_limits':inv['bounded_scope']}
inv['bounded_scope'].update({'assessment_boundary':'All exact source hints and supplied forms, senses and whole constructions remain visible. Their independent recall is never assessed. A table cell establishes only its explicit morphology and stated lexical frame.','source_reading':'One complete226-word episode at175.18–177.2 with22 original notes and29 anchors. The subsequent Apollonius as Teacher is unassigned.','new_practice':outcomes['original_practice_counts'],'completion_claim':'The47 final numbered Cook items complete the canonical numbered exercise assignment crosswalk, not mastery of the entire reader, all prose, poetry or Old English.'})
inv['prior_requirements']={'baseline':'0eda27783a3830fbd10bebef3702e27c15ff837c','scope':'Only actual active ch01–ch17 records.'}
for k in ['form','sense','feature']:inv['prior_requirements'][k+'_ids']=sorted({rid for t in tasks for rid in t.get('required_'+k+'_ids',[])}&old[k].keys())
hints=read(O/'source-hint-inventory.json')
inv['source_task_crosswalk']={'exact_prompt_source':'sources/audits/unit18-source/exercises-prompts.json','tasks':[{'source_item_id':t['task_id'],'key_id':t['key_id'],'output_position_ids':[p['output_position_id'] for p in t['output_positions']],'source_control_ids':[r['reference_id'] for r in t.get('source_control_records',[])],'disposition':'assigned'} for t in tasks if t['task_id'].startswith('EX-')],'original_controls':hints['records'],'global_instructions':read('sources/audits/unit18-source/exercises-prompts.json')['instructions'],'unassigned_from_these_sets':[]}
examples=read(O/'composition-bindings.json')['examples'];compositions=read(O/'compositions.json');compositions['teaching_examples']=examples;compositions['new_compositions']=[];save(O/'compositions.json',compositions)
ids={r['teaching_id'] for r in inv['teaching_records']}
for e in examples:
 if e['teaching_id'] not in ids:inv['teaching_records'].append({'teaching_id':e['teaching_id'],'kind':'translated_new_example','example_id':e['example_id'],'sequence_id':e['sequence_id'],'text':e['text'],'translation':e['translation'],'teaching_point':e['teaching_point'],'form_ids':sorted({t['form_id'] for t in e['tokens']}),'sense_ids':sorted({t['sense_id'] for t in e['tokens']}),'feature_ids':e['feature_ids'],'origin_category':'new teaching material','knowledge_status':'previously_taught','lesson_placement':'Before the corresponding cumulative analysis or composition task.'})
catalog={}
for register in [lex,gram]:
 for eid,e in register.get('evidence_catalog',{}).items():
  assert eid not in catalog or catalog[eid]==e,eid
  catalog[eid]=copy.deepcopy(e)
for path in ['sources/audits/unit18-source/evidence-catalog.json','sources/audits/unit18-grammar/evidence-catalog.json','sources/audits/unit18-coordinator/evidence-catalog.json']:
 if not Path(path).exists():continue
 d=read(path)
 if 'primary_inspection_entries' in d:d={r['evidence_id']:{k:v for k,v in r.items() if k!='evidence_id'} for r in d['primary_inspection_entries']}
 elif 'evidence_catalog' in d:d=d['evidence_catalog']
 elif 'entries' in d and isinstance(d['entries'],list):d={r['evidence_id']:{k:v for k,v in r.items() if k!='evidence_id'} for r in d['entries']}
 elif 'records' in d and isinstance(d['records'],list):d={r['evidence_id']:{k:v for k,v in r.items() if k!='evidence_id'} for r in d['records']}
 if isinstance(d,list):d={r['evidence_id']:{k:v for k,v in r.items() if k!='evidence_id'} for r in d}
 for eid,e in d.items():
  if not isinstance(e,dict):continue
  assert eid not in catalog or catalog[eid]==e,('evidence collision',eid)
  catalog[eid]=copy.deepcopy(e)
inv['evidence_catalog']=catalog
inv['pre_key_review_exclusions']=sorted(set([p.as_posix() for folder in [O,Path('sources/audits/unit18-grammar'),Path('sources/audits/unit18-source'),Path('sources/audits/unit18-coordinator')] for p in folder.glob('*') if p.is_file() and (folder==O or p.name.startswith('author-only') or p.name.startswith('candidate-') or p.name.startswith('model-amendments') or p.name in ['REPORT.md','reconciliation.json','prompt-model-comparison.json'])]+['chapters/ch18/coverage.json','chapters/ch18/answer-key.md']))
inv['review_independence']={'models':'All selected OE models and target analyses are private preparation. A fresh reviewer receives learner tasks and visible support only, freezes actual solutions, then consults the model/key.','reading':'The source editor and coordinator translation witnesses remain independently preserved. This design supplies a separately prepared complete translation model from the actual Old English, without consulting their witness files.','scope':'This proposal validates identity/dependency closure. Fresh linguistic solving, full-paradigm evidence review and exported-page inspection remain coordinator gates.'}
inv['orthographic_identity_policy']='Preserve every existing stored form surface and analysis. Sentence-initial or contextual capitalization is recorded in literal/surface on the occurrence and compared after casefold only; no vowel length, dialect spelling or morphology is silently normalized. Hāl/hāl is this declared capitalization-only case.'
inv['record_counts_by_scope']={k:dict(Counter(r['knowledge_status'] for r in rows)) for k,rows in [('form',[r for l in inv['lemmas'] for r in l['forms']]),('sense',[r for l in inv['lemmas'] for r in l['senses']]),('feature',inv['features'])]}
inv['record_identity_counts']={k:{'reused_prior_IDs':len({r[k+'_id'] for r in rows}&old[k].keys()),'new_IDs':len({r[k+'_id'] for r in rows}-old[k].keys())} for k,rows in [('form',[r for l in inv['lemmas'] for r in l['forms']]),('sense',[r for l in inv['lemmas'] for r in l['senses']]),('feature',inv['features'])]}
inv['promotions']=[{'record_kind':k,'record_id':r[k+'_id'],'prior_scope':r.get('prior_scope'),'new_scope':r['knowledge_status'],'teaching_ids':r.get('teaching_ids',[])} for k,rows in [('form',[r for l in inv['lemmas'] for r in l['forms']]),('sense',[r for l in inv['lemmas'] for r in l['senses']]),('feature',inv['features'])] for r in rows if r[k+'_id'] in old[k] and r['knowledge_status'] in ['new_production','new_recognition']]
inv['counts'].update({'lemmas':len(inv['lemmas']),'forms':sum(len(l['forms']) for l in inv['lemmas']),'senses':sum(len(l['senses']) for l in inv['lemmas']),'features':len(inv['features']),'teaching_records':len(inv['teaching_records']),'tasks':len(tasks),'requested_output_positions':sum(len(t['output_positions']) for t in tasks),'source_words':226,'source_notes':22,'source_note_anchors':29,'source_controls':154,**displays['counts']})
inv['analysis_input_hashes'].update({p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['sources/audits/unit18-source','sources/audits/unit18-grammar'] for p in Path(folder).glob('*.json') if not p.name.startswith('author-only')})
inv['status']='reconciled_proposal_pending_final_validation'
save(O/'inventory.json',inv);print(json.dumps(inv['counts'],indent=2))
