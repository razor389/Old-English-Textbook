"""Publish explicit crosswalks without changing the active course."""
import json,pathlib,copy,hashlib
R=pathlib.Path(__file__).resolve().parents[3];O=pathlib.Path(__file__).resolve().parent
def read(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def put(n,d):(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
BASE={x['lemma_id']:x for x in read('lexicon/entries.json')['lemmas']}
packs=[read('sources/audits/unit15-grammar/'+x) for x in ['grammar-records-core.json','grammar-records-families.json','grammar-records-lexical.json','source-support.json']]
U={}
for p in packs:
 for x in p['lemmas']:
  q=U.setdefault(x['lemma_id'],{'lemma_id':x['lemma_id'],'forms':[],'senses':[]})
  q['forms']+=x['forms'];q['senses']+=x['senses']
lex=packs[2];pp=copy.deepcopy(lex['principal_parts'])
extra=[('aetiewan',['ætīewan','ætīewde','ætīewed'],['U15-G-FB72']),('wyrcean',['wyrcean','worhte','worht'],['U15-G-FB69']),('onfon',['onfōn','onfēng','onfēngon','onfangen'],['U15-G-FB55','U15-G-FB67','U15-G-FB308']),('forlaetan',['forlǣtan','forlēt','forlēton','forlǣten'],['U15-G-FB67','U15-G-FB288']),('standan',['standan','stōd','stōdon','standen'],['U15-G-FB65']),('giefan',['giefan','geaf','gēafon','giefen'],['U15-G-FB63'])]
pp.extend({'lemma_id':i,'parts':v,'evidence_refs':e,'scope_note':'Morphological reference; new production only where enumerated in its separate complete system.'} for i,v,e in extra)
PPL={};ppout=[]
def sameform(i,s):
 fs=U.get(i,{}).get('forms',[])+BASE.get(i,{}).get('forms',[])
 matches=[f for f in fs if f['form']==s]
 if not matches:return None
 def score(f):
  a=f.get('contextual_analysis',f['analysis']);return (0 if 'inf' in f['form_id'] or 'participle' in f['form_id'] else 1,0 if a.get('person')==3 else 1,0 if f.get('production_taught_in') or f.get('knowledge_status') in ['new_production','previously_taught'] else 1)
 return sorted(matches,key=score)[0]
for p in pp:
 i=p['lemma_id'];parts=[]
 for j,s in enumerate(p['parts']):
  f=sameform(i,s)
  if not f:
   role='plain_infinitive' if j==0 else 'past_participle' if j==len(p['parts'])-1 else 'preterite_reference'
   f={'form_id':f'{i}-u15-principal-part-{j+1}-reference','form':s,'analysis':{'verb_form':role,'function':'principal_parts_citation_only'},'knowledge_status':'supplied','evidence_refs':p['evidence_refs'],'teaching_ids':['NEW-U15-PRINCIPAL-PARTS'],'scope_note':'Morphology-only reference citation. No independent syntactic use is authorized.','origin_category':'new_teaching_material','evidence_basis':'selected class rule and lexical source, not separately attested for every generated cell'}
   q=PPL.setdefault(i,{'lemma_id':i,'display_headword':p['parts'][0],'part_of_speech':'verb','prior_lemma_present':i in BASE,'forms':[],'senses':[]});q['forms'].append(f)
  status='previously_taught' if f.get('production_taught_in') else f.get('knowledge_status','supplied')
  parts.append({'form_id':f['form_id'],'form':s,'analysis':f['analysis'],'knowledge_status':status,'sense_binding':'morphology_only_reference; no independent lexical use implied','evidence_refs':p['evidence_refs']})
 ppout.append({**p,'parts':parts,'display_category':'morphological_reference','new_syntactic_scope_from_display':False})
put('principal-parts.json',{'schema_version':1,'chapter':'ch15','records':ppout,'lemmas':list(PPL.values()),'scope':'All displayed principal parts bind actual form identities. Supplied citation parts are visible reference material, not recall targets.'})

maps={
 'u15-onfon-payment-acc':('onfon','EX-IX-28-11 EX-IX-28-12'),
 'u15-gelic-object-predicate':('don gelic','EX-IX-29-01'),
 'u15-wid-exchange':('with','EX-IX-28-02 EX-IX-29-04'),
 'u15-forgieldan-payment':('forgieldan','EX-IX-28-01 EX-IX-28-10'),
 'u15-wenan-content':('wenan','EX-IX-28-12'),
 'u15-eall-equative':('eall micel swa','EX-IX-29-02'),
 'u15-ofer-kindness-rank':('ofer god-adjective','EX-IX-29-08 EX-IX-29-10'),
 'u15-swerian-thurh':('swerian thurh','EX-IX-30-01 EX-IX-30-02'),
 'u15-for-exchange':('for','EX-IX-30-04'),
 'u15-laeran-objects':('laeran','EX-IX-30-05 EX-IX-30-06'),
 'u15-aliesan-separation':('aliesan fram','EX-X-XI-31-04'),
 'u15-gehatan-promise':('gehatan','EX-X-XI-31-12')}
frames=[]
for f in lex['features']:
 ids,tasks=maps[f['feature_id']]
 frames.append({'frame_id':f['feature_id'],'feature_id':f['feature_id'],'lemma_ids':ids.split(),'construction':f['description'],'knowledge_status':f['knowledge_status'],'evidence_refs':f['evidence_refs'],'used_in_tasks':tasks.split()})
put('lexical-frames.json',{'schema_version':1,'chapter':'ch15','frames':frames,'scope_note':'Local unusual frames are in source-support.json; no lemma-only inference licenses them.'})

prior=read('sources/audits/unit08-grammar/pronoun-dispositions.json')['records'];disp=[]
new={'ān indefinite':('new_production','New indefinite sense; existing complete singular morphology, no plural promotion.'),'nān':('new_production','Complete24strongNGDA; attributable or substantival, with negative concord.'),'gehwā / gehwæt':('new_production','All8existing recognition cells promoted; singular distributive use.'),'hwā indefinite anyone':('new_production','Prior8NGDA reused for bounded conditional/concessive/free-choice indefinite sense.'),'man impersonal one':('new_production','Only defective nominative singular man, third-singular verb; no imaginary oblique paradigm.'),'swā hwā swā / swā hwæt swā':('new_production','Free-choice with internal case; explicit resumptive pronoun where main-clause case differs.'),'swā hwilc swā / swā hwæðer swā':('bounded_new_production','Swā hwæðer swā between two is productive in the safe resumptive pattern. Swā hwilc swā is family citation only; attracted-case31.12 supplied.'),'ǣgðer':('bounded_new_production','Only invariant ǣgðer ge…ge coordinator, both…and. Inflected either/both family and longer ǣghwæðer remain citation-only.'),'āwiht / ōht':('supplied_citation','Āwiht only in the supported object question; ōht citation variant not an independent target.'),'nāwiht / nōht':('bounded_new_production','Nāwiht accusative object in negative concord. Nōht spelling only citation, not an added recall paradigm.'),'-hwega compounds, including hwæthwega':('supplied','Reuse prior exact hwæthwega object support. Other compounds/orthographic variants are citation-only.'),'nǣnig':('citation_only','Named negative-family alternative; no unused partial paradigm or independent recognition claim.'),'āhwæðer':('citation_only','Either family acknowledged; no unneeded full inflected system assigned.'),'nāhwæðer':('citation_only','Neither family acknowledged; no unneeded full inflected system assigned.'),'other hwā compounds, e.g. āhwā, ǣghwā':('citation_only','Family relationship only, no extra recall or historical variant paradigms.'),'sīn':('deferred','Retain prior justified deferral; no poetic reflexive expansion in this unit.')}
for p in prior:
 status,scope=new.get(p['family'],('previously_taught_with_original_boundaries','Retain actual earlier contract scope; this inventory entry is not a new teaching claim.'))
 disp.append({'family':p['family'],'prior_u08_disposition':p['disposition'],'unit15_disposition':status,'scope':scope,'evidence_refs':['U15-G-FB52','U15-G-FB53','U15-G-W239','U15-G-W240']})
disp.extend([{'family':'būtan except versus without','unit15_disposition':'retain_bounded_prior_scope','scope':'U14 except-through scaffold stays local. U15 uses prior without+dative in30.12; no new general exceptive-clause system.','evidence_refs':['U15-G-EX17']},{'family':'ðȳ comparative/proportional instrumental','unit15_disposition':'reference_only','scope':'Unit15 independently produces paired swā clauses; does not promote every instrumental-degree or historical proportional variant.','evidence_refs':['U15-G-FB156','U15-G-BT-SWITHE']}])
put('pronoun-dispositions.json',{'schema_version':1,'chapter':'ch15','records':disp,'scope_note':'Every explicit Unit8 family disposition revisited. Citation-only alternatives are not falsely counted as taught recognition paradigms.'})

models=read('sources/audits/unit15-grammar/author-only-cook-models.json')['items']
seq={x['owner_id']:x for x in read('curriculum/proposals/unit15/author-only-cook-sequence-bindings.json')['sequences']}
taskfeatures={x['task_id']:x['feature_ids'] for x in read('curriculum/proposals/unit15/task-feature-bindings.json')['records']}
GF={x['feature_id']:x for x in read('curriculum/grammar.json')['features']}
for q in [read('sources/audits/unit15-source/source-support-records.json'),*packs]:
 for f in q.get('features',[]):GF[f['feature_id']]=f
def fs(i):
 f=GF.get(i,{})
 if f.get('production_taught_in') or f.get('recognition_taught_in'):return 'previously_taught'
 return f.get('knowledge_status','unresolved')
helps={}
for h in packs[3]['cook_support']:
 for tid in h['used_in_tasks']:helps.setdefault(tid,[]).append(h['support_id'])
issues=read('curriculum/proposals/unit15/cook-model-validation.json')['issues']
formlookup={};senselookup={}
for p in [read('lexicon/entries.json'),read('sources/audits/unit15-source/source-support-records.json'),*packs,{'lemmas':list(PPL.values())}]:
 for x in p['lemmas']:
  for f in x['forms']:formlookup[f['form_id']]=(x['lemma_id'],f,x.get('part_of_speech',''))
  for s in x['senses']:senselookup[s['sense_id']]=s
out=[]
for m in models:
 tid=m['source_item_id'];s=seq.get(tid,{});vv=[]
 for t in s.get('tokens',[]):
  if t.get('form_id') not in formlookup:continue
  i,f,pos=formlookup[t['form_id']]
  if pos=='verb' or any(k in f['analysis'] for k in ['mood','tense','verb_form','nonfinite']):
   vv.append({'kind':'verb_or_supported_form','lemma_id':i,'form_id':t['form_id'],'sense_id':t['sense_id'],'form':t.get('surface',f['form']),'form_status':t['form_status'],'sense_status':t['sense_status'],'analysis':t.get('contextual_analysis',t['analysis'])})
 ff=list(taskfeatures.get(tid,[]))
 ff=['u12-gehatan-indicative' if f=='u15-gehatan-promise' else f for f in ff]
 for f in frames:
  if tid in f['used_in_tasks'] and f['feature_id'] not in ff:ff.append(f['feature_id'])
 hs=helps.get(tid,[])
 out.append({'item_id':tid,'source_item_id':tid,'disposition':'assign','verbal_requirements':vv,'grammar_requirements':[{'feature_id':f,'knowledge_status':fs(f)} for f in ff],'local_support_ids':hs,'required_feature_ids':ff+hs,'original_controls_and_interpretation':m['grammar_targets'],'targets':m['grammar_targets'],'nominal_dependencies_owner':'sources/audits/unit15-source','token_binding_source':'curriculum/proposals/unit15/author-only-cook-sequence-bindings.json','remaining_unresolved':[q for q in issues if q.get('owner')==tid],'text_binding_current':s.get('text')==m['model']})
put('exercises-verbal-dependencies.json',{'schema_version':1,'chapter':'ch15','scope':'All50 exact planned Cook items. Grammarworker independently composed and inspected their meanings; designer supplied contextual exact token identities for reconciliation.','items':out,'status':'published_crosswalk_pending_last_token_rebuild' if issues else 'closed_token_crosswalk'})
print('Published4interfaces:',len(ppout),'principal-part rows;',len(frames),'frames;',len(disp),'family dispositions;',len(out),'Cook dependencies')
