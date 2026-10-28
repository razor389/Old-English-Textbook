import json,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
L={x['lemma_id']:x for x in json.loads((ROOT/'lexicon/entries.json').read_text(encoding='utf8'))['lemmas']}
D=json.loads((O/'candidate-verbal-bindings.json').read_text(encoding='utf8'))
P=json.loads((O/'senses-constructions-support.json').read_text(encoding='utf8'))
S={s['sense_id']:s for s in P['sense_proposals']}
new_by_lemma={}
for s in P['sense_proposals']:new_by_lemma.setdefault(s['lemma_id'],[]).append(s['sense_id'])
reuse={s['lemma_id']:s['sense_id']for s in P['prior_sense_reuse']}
special={('37-08','don'):'don-u17-fulfil',('40-03','secgan'):'secgan-u17-call',('40-03','geseon'):'geseon-u17-regard',('40-04','don'):'don-beneficiary',('40-08','onfon'):'onfon-u17-person',('41-02','healdan'):'healdan-u17-maintain',('41-03','wyrcean'):'wyrcean-work',('41-04','laedan'):'laedan-u17-carry',('40-07','hyngran'):'hyngran-u17-hungry-participle'}
special.update({('37-06','settan'):'settan-u17-establish',('39-01','settan'):'settan-u17-establish',('37-06','gewitan'):'gewitan-u17-decree-pass',('40-07','forlaetan'):'forlaetan-u17-let-go',('41-02','gefyllan'):'gefyllan-fill-source',('43-03','cleopian'):'cleopian-u16-cry',('43-16','slean'):'slean-kill',('42-08','settan'):'settan-1'})
support_map={'37-06':['U17-H-37-06'],'37-14':['U17-H-37-14'],'38-09':['U17-H-38-09'],'41-01':['U17-H-41-01'],'41-05':['U17-H-41-05'],'42-01':['U17-H-42-01'],'42-02':['U17-H-42-02-PART','U17-H-42-02-NUMBER'],'42-03':['U17-H-42-03'],'42-06':['U17-H-42-06'],'43-01':['U17-H-43-01'],'43-03':['U17-H-43-03'],'43-16':['U17-H-43-16']}
support_map.update({'38-04':['U17-H-38-04'],'39-04':['U17-H-39-04'],'39-07':['U17-H-39-07'],'40-02':['U17-H-40-02'],'40-05':['U17-H-40-05'],'43-10':['U17-H-43-10']})
generated=[]
for r in D['rows']:
 k=r['source_item_id'].removeprefix('EX-XII-XIII-')
 r['whole_frame_support_ids']=support_map.get(k,[])
 for v in r['verbal_occurrences']:
  lemma=v['lemma_id']
  if k=='43-13'and v['surface']=='gelǣrede':
   lemma='gelared';v['lemma_id']=lemma
   actual=next(f for f in L[lemma]['forms']if f['form_id']=='gelared-nom-pl-m-strong')
   v.update({'form_id':actual['form_id'],'form_knowledge_status':'previously_taught','current_context_analysis':{'case':'nominative','number':'plural','gender':'masculine','declension':'strong','morphology_type':'lexical_adjective'},'prior_form_record':copy.deepcopy(actual),'proposed_cell':None,'prior_productive_senses':copy.deepcopy(L[lemma]['senses'])})
  sid=special.get((k,lemma))
  if lemma=='forgiefan':sid='forgiefan-u16-forgive'if k.startswith('41-')else'forgiefan-u14-give'
  if lemma=='healdan'and k=='42-03':sid='healdan-1'
  if not sid:
   ids=new_by_lemma.get(lemma,[])
   if lemma not in ['don','secgan','healdan','onfon','laedan','geseon']and len(ids)==1:sid=ids[0]
  if not sid:sid=reuse.get(lemma)
  if not sid:
   old=[s for s in L.get(lemma,{}).get('senses',[])if s.get('production_taught_in')]
   if lemma=='secgan':sid='secgan-content'
   elif lemma=='don':sid='don-1'
   elif old:sid=old[0]['sense_id']
   else:sid=f'{lemma}-u17-source-sense'
  old=next((s for s in L.get(lemma,{}).get('senses',[])if s['sense_id']==sid),None)
  v['sense_id']=sid;v['sense_knowledge_status']=S[sid]['knowledge_status']if sid in S else'previously_taught'if old and old.get('production_taught_in')else'supplied'
  v['selected_sense_record']=copy.deepcopy(S.get(sid,old))
  if v['selected_sense_record']is None:
   v['selected_sense_record']={'sense_id':sid,'gloss':v['contextual_role_and_meaning'],'knowledge_status':'supplied','scope':'Source-local contextual sense only; see whole-frame support.'}
  v['construction_support_ids']=r['whole_frame_support_ids']
  v['source_hint_reference']= (k=='39-07'and lemma=='asmean')or(k=='42-03'and lemma=='geriman')or(k=='38-09'and v['surface']=='wǣre')
  # Predicate plural agreement is the independently specified bounded productive extension.
  if k=='37-05'and lemma in ['wyrcean','gescieppan']and v['current_context_analysis'].get('verb_form')=='past_participle':
   v['form_knowledge_status']='new_production';v['form_id']=f'{lemma}-u17-past-participle-predicate-plural'
   v['current_context_analysis'].update({'agreement':'predicate_plural_strong_masculine_like','number':'plural'})
   v['derivation']={'feature_id':'u17-predicate-participle-plural','base':'worht'if lemma=='wyrcean'else'gesceapen','ending':'e','evidence_refs':['U17G-FB41','U17G-FB190']}
   generated.append({'lemma_id':lemma,'form_id':v['form_id'],'form':v['surface'],'analysis':v['current_context_analysis'],'knowledge_status':'new_production','derivation':v['derivation']})
  # Generated source-local forms are literal supplied shapes, not pretend productive cells.
  if v['form_knowledge_status']=='supplied':
   if k in ['37-14','42-01','42-02','42-03']or v['source_hint_reference']:
    v['supplied_route_verified']=True
   else:v['supplied_route_verified']=False
D['additional_literal_form_records']=generated
D['unresolved_occurrence_routes']=[{'source_item_id':r['source_item_id'],'surface':v['surface'],'form_id':v['form_id']}for r in D['rows']for v in r['verbal_occurrences']if v.get('supplied_route_verified')is False]
D['status']='205 ordered contextual verbal occurrences with selected sense IDs; see explicit unresolved routes'
(O/'candidate-verbal-bindings.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('unresolved routes',D['unresolved_occurrence_routes'])
