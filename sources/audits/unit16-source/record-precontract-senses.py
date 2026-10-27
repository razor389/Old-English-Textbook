"""Record the nine reviewed source-sense repairs against the retained snapshot."""
import json,pathlib,hashlib,datetime
OUT=pathlib.Path(__file__).parent;ROOT=OUT.parents[2]
oldp=ROOT/'build/u16-source-pre-sense-refresh.json';newp=OUT/'reading-token-ledger.json'
old=json.loads(oldp.read_text(encoding='utf-8'));new=json.loads(newp.read_text(encoding='utf-8'))
lex={l['lemma_id']:l for l in json.loads((OUT/'lexical-inventory.json').read_text(encoding='utf-8'))['lemmas']}
changes=[];fields=['sense_id','sense_status','prior_sense_scope','sense_supply','contextual_sense_rationale']
for a,b in zip(old['tokens'],new['tokens']):
 assert all(a[k]==b[k] for k in ['token_id','surface','lemma_id','form_id','analysis']),a['token_id']
 if a['sense_id']!=b['sense_id']:
  changes.append({'token_id':b['token_id'],'surface':b['surface'],'form_id':b['form_id'],'before':{k:a.get(k) for k in fields},'after':{k:b.get(k) for k in fields}})
assert len(changes)==9,len(changes)
retained=[{'token_id':t['token_id'],'surface':t['surface'],'lemma_id':t['lemma_id'],'sense_id':t['sense_id']} for t in new['tokens'] if t['lemma_id'] in lex and t['sense_id'] not in [s['sense_id'] for s in lex[t['lemma_id']]['senses']]]
record={'schema_version':1,'stage':'pre-contract source-sense correction','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reason':'Coordinator detected hǣle wrongly inheriting productive salvation instead of supplied safety/rescue. Audit found seven analogous nominal fallbacks and one line-boundary on169.6–7 activity phrase. All nine now bind their already-declared supplied source sense. No text, form identity, original analysis or lexical teaching changes.','before_ledger_sha256':hashlib.sha256(oldp.read_bytes()).hexdigest(),'after_ledger_sha256':hashlib.sha256(newp.read_bytes()).hexdigest(),'changes':changes,'remaining_prior_sense_review':{'status':'reviewed; retained contextually appropriate earlier senses','rationale_by_lemma':{'on':'Spatial goal and location, distinct from local clothing/fishing/activity supplies.','wesan':'Ordinary state, passive or earlier recognition-only intransitive perfect, distinct from the local impersonal seemed expression.','to':'Spatial goal/orientation and separately supplied speech-addressee use, distinct from local belonging/rejuvenation roles.','geseon':'Accusative participant plus infinitive, distinct from the local finite-content clause.','mid':'Means, accompaniment and explicitly supplied manner, distinct from local clothing complements.','thaet-conjunction':'Ordinary content or factual result, distinct from the one source-uncertain169.6 link.','of':'Out of the bath, ordinary spatial source, distinct from old-age transition and partition.','thurh':'Oath standard at170.2, distinct from service/evidence means.'},'positions':retained}}
(OUT/'pre-contract-sense-refresh.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'corrected_tokens':len(changes),'retained_prior_sense_positions':len(retained),'ledger_sha256':record['after_ledger_sha256']}))
