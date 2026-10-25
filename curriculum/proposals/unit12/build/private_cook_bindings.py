"""PRIVATE exact Cook-model bindings after independent witness reconciliation."""
from pathlib import Path
import json
import public_bindings as B
models=B.load('sources/audits/unit12-source/author-only-cook-corrected-models.json')['items']
routes={r['task_id']:r for r in B.load('sources/audits/unit12-source/exercises-dependencies.json')['items']}
sequences=[]
for m in models:
 ident=m['task_id'];route=routes[ident]
 if 'ordered_bindings' in m:
  refs=[r['form_id']+'|'+r['sense_id'] for r in m['ordered_bindings']]
 elif 'ordered_token_bindings' in m:
  refs=[r if isinstance(r,str) else r['form_id']+'|'+r['sense_id'] for r in m['ordered_token_bindings']]
 elif 'ordered_sense_ids' in m:
  assert len(m['ordered_form_ids'])==len(m['ordered_sense_ids']),ident
  refs=[f+'|'+s for f,s in zip(m['ordered_form_ids'],m['ordered_sense_ids'])]
 else:
  senses={}
  for record in route.get('sense_requirements',route.get('sense_requirements_unordered',[])):
   sid=record['sense_id'];lemma=B.senses[sid]['lemma_id'];senses.setdefault(lemma,set()).add(sid)
  refs=[]
  for fid in m['ordered_form_ids']:
   lemma=B.forms[fid]['lemma_id'];candidates=senses.get(lemma,set())
   if len(candidates)!=1:raise ValueError((ident,fid,'needs explicit ordered sense',sorted(candidates)))
   refs.append(fid+'|'+next(iter(candidates)))
 seq=B.make_sequence(ident+'-MODEL',m['model'],' '.join(refs),ident,'private_Cook_model_output')
 if not seq:continue
 for kind,sourcekey in [('form','form_requirements_unordered'),('sense','sense_requirements')]:
  records=route.get(sourcekey,route.get(sourcekey+'_unordered',[]))
  expected={r[kind+'_id'] if isinstance(r,dict) else r for r in records};actual=set(seq['required_'+kind+'_ids'])
  if expected!=actual:B.issues.append({'task_id':ident,'error':'private/public '+kind+' sets differ','only_public':sorted(expected-actual),'only_private':sorted(actual-expected)})
 sequences.append(seq)
B.write('author-only-cook-sequence-bindings.json',{'schema_version':1,'chapter':'ch12','access':'PRIVATE: exclude until independent solutions are frozen.','status':'closed' if not B.issues else 'pending_record_reconciliation','sequences':sequences,'issues':B.issues})
print(json.dumps({'Cook_sequences':len(sequences),'tokens':sum(len(s['tokens']) for s in sequences),'issue_count':len(B.issues),'issues':B.issues[:15]},ensure_ascii=False))
