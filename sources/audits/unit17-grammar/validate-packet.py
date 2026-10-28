"""Private packet reconciliation, not a linguistic truth certificate."""
import copy,hashlib,json,re,unicodedata
from pathlib import Path
O=Path(__file__).resolve().parent;ROOT=O.parents[2]
def read(p):return json.loads(p.read_text(encoding='utf8'))
def norm(s):return unicodedata.normalize('NFC',s).casefold()
def tokens(s):return re.findall(r'[A-Za-zĀ-žǢǣȲȳÆæÐðÞþ]+(?:-[A-Za-zĀ-žǢǣȲȳÆæÐðÞþ]+)*',s)
files=['candidate-models.json','candidate-verbal-bindings.json','reading-verbal-bindings.json','verbal-systems.json','senses-constructions-support.json','evidence-catalog.json','numeric-control-analysis.json']
D={n:read(O/n)for n in files};M=D['candidate-models.json'];V=D['candidate-verbal-bindings.json'];R=D['reading-verbal-bindings.json'];S=D['verbal-systems.json'];P=D['senses-constructions-support.json'];E=D['evidence-catalog.json']
prompts=read(ROOT/'sources/audits/unit17-source/exercises-prompts.json')['items']
reading=read(ROOT/'sources/audits/unit17-source/reading-source.json')['source_spans'][0]
L={x['lemma_id']:x for x in read(ROOT/'lexicon/entries.json')['lemmas']}
expected=[x['source_item_id']for x in prompts]
assert [r['source_item_id']for r in M['rows']]==expected==[r['source_item_id']for r in V['rows']]
assert len(expected)==82 and len(set(expected))==82
cells={};appearances=0
for system in S['systems']:
 assert system['scope'] and system['derivation_rules'] and system['evidence_refs']
 for c in system['cells']:
  appearances+=1
  if c['form_id']in cells:
   old=cells[c['form_id']];assert old['form']==c['form']and old['analysis']==c['analysis']
  cells[c['form_id']]=c
senses={x['sense_id']:x for x in P['sense_proposals']}
supports={x['feature_id']for x in P['whole_frame_support']}
rsupports={x['feature_id']for x in R['whole_frame_support']}
checks={'model_occurrences':0,'reading_occurrences':0,'actual_prior_form_records_preserved':0,'prior_senses_verified':0,'new_senses_verified':0}
def occurrence(v,t,allowed_supports,reading=False):
 assert t[v['token_position_one_based']-1]==v['surface'],v
 lemma=L.get(v['lemma_id'],{})
 old_forms={x['form_id']:x for x in lemma.get('forms',[])}
 old_senses={x['sense_id']:x for x in lemma.get('senses',[])}
 if v['form_knowledge_status']=='previously_taught':
  old=old_forms[v['form_id']];assert old.get('production_taught_in'),v
  assert norm(old['form'])==norm(v['surface']),v
  assert v['prior_form_record']==old,(v['surface'],'prior record changed')
  checks['actual_prior_form_records_preserved']+=1
 elif v['form_knowledge_status']=='new_production':
  assert v['form_id']in cells,v
  assert norm(cells[v['form_id']]['form'])==norm(v['surface']),v
 else:
  assert v['form_knowledge_status']=='supplied',v
  assert v.get('whole_frame_support_ids')or v.get('construction_support_ids')or v.get('source_hint_reference')or v.get('visible_reference'),v
 if v['sense_knowledge_status']=='previously_taught':
  assert old_senses[v['sense_id']].get('production_taught_in'),v
  checks['prior_senses_verified']+=1
 elif v['sense_knowledge_status']=='new_production':
  assert senses[v['sense_id']]['knowledge_status']=='new_production',v
  checks['new_senses_verified']+=1
 else:assert v['sense_knowledge_status']=='supplied',v
 assert v.get('current_context_analysis')and v.get('contextual_role_and_meaning'),v
 for sid in v.get('whole_frame_support_ids',[])+v.get('construction_support_ids',[]):assert sid in allowed_supports,sid
 checks['reading_occurrences'if reading else'model_occurrences']+=1
for model,row in zip(M['rows'],V['rows']):
 assert model['model']==row['model']
 t=tokens(model['model']);assert t==model['tokens']
 for sid in row['whole_frame_support_ids']:assert sid in supports
 for v in row['verbal_occurrences']:occurrence(v,t,supports)
rt=tokens(reading['learner_text']);assert len(rt)==252
for v in R['verbal_occurrences']:occurrence(v,rt,rsupports,True)
semantic_records=[]
for correction_path in sorted(O.glob('semantic-correction-*.json')):
 correction=read(correction_path)
 if correction['correction_id']=='U17G-SEMANTIC-CORRECTION-01':
  assert next(v for v in R['verbal_occurrences']if v['token_position_one_based']==71)==correction['after_occurrence']
  assert next(f for f in R['whole_frame_support']if f['feature_id']=='U17-RSUP-04')==correction['after_support']
  assert hashlib.sha256((O/'candidate-models.json').read_bytes()).hexdigest()==correction['preservation']['candidate_models_sha256']
  for name,digest in correction['preservation']['model_amendments_sha256'].items():assert hashlib.sha256((O/name).read_bytes()).hexdigest()==digest
 semantic_records.append({'path':str(correction_path.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(correction_path.read_bytes()).hexdigest()})
assert not V['unresolved_occurrence_routes']and not R['unresolved_routes']and not P['still_pending']
catalog={e['evidence_id']:e for e in E['primary_inspection_entries']};assert len(catalog)==len(E['primary_inspection_entries'])
images=0
for e in catalog.values():
 assert e['actually_inspected']
 if 'image_path'in e:
  assert hashlib.sha256((ROOT/e['image_path']).read_bytes()).hexdigest()==e['image_sha256'];images+=1
 for ref in e.get('component_evidence_ids',[]):assert ref in catalog
def evidence_refs(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k=='evidence_refs':
    for ref in v:
     if ref.startswith('U17G-'):assert ref in catalog,ref
   else:evidence_refs(v)
 elif isinstance(x,list):
  for v in x:evidence_refs(v)
for n,d in D.items():evidence_refs(d)
for r in M['rows']:
 r['stage']='frozen private contract candidate; not learner text or answer key'
 r['controls_checked']=True
 r['verbal_morphology_checked']=True
 r['verbal_sense_frames_checked']=True
 r['morphology_checked']=False
 r['sense_frames_checked']=False
 r['check_scope_note']='Exact prompt controls and the verbal analysis are checked against the cited images; complete nonverbal form/sense integration belongs to source/design/coordinator. The two broad false fields deliberately do not certify another worker’s integration.'
(O/'candidate-models.json').write_text(json.dumps(M,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
V['status']='Frozen205 ordered contextual verbal occurrences; source/form/sense routes validated, no unresolved verbal routes. Not a key or a claim that nonverbal integration is complete.'
(O/'candidate-verbal-bindings.json').write_text(json.dumps(V,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
receipt={'schema_version':1,'access':'author-only audit; excluded from blind reviewers','status':'passed','scope':'Structural reconciliation and source receipts; independent linguistic review still required after contract integration.','counts':{'cook_items':82,'reading_words':252,'systems':len(S['systems']),'display_appearances':appearances,'unique_display_form_ids':len(cells),'sense_proposals':len(P['sense_proposals']),'feature_records':len(P['features']),'exercise_whole_supports':len(supports),'reading_whole_supports':len(rsupports),'numeric_control_groups':len(D['numeric-control-analysis.json']['rows']),'primary_catalog_records':len(catalog),'individual_inspected_images':images,**checks},'unresolved_verbal_routes':[],'source_hashes':{str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest()for p in [ROOT/'sources/audits/unit17-source/exercises-prompts.json',ROOT/'sources/audits/unit17-source/reading-source.json']},'packet_hashes':{n:hashlib.sha256((O/n).read_bytes()).hexdigest()for n in files},'scope_limits':['No Beads writes; no active registers or earlier chapters edited.','All models are private proposed translations, excluded from blind review.','Exact dictionary hints remain visible reference positions, not independent-recall evidence.','Display appearances include two repeated base cells;436unique form identities.','Nonverbal integration and canonical contract remain coordinator/source/design responsibilities.']}
receipt['semantic_correction_records']=semantic_records
(O/'validation-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(receipt['counts'],ensure_ascii=False))
