"""Validate the concrete source packet before coordinator integration."""
import hashlib,json,re,unicodedata
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[2]
def read(path):return json.loads((R/path).read_text(encoding='utf8'))
def own(name):return json.loads((P/name).read_text(encoding='utf8'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
errors=[];checks=[]
def check(condition,label):
 checks.append({'check':label,'passes':bool(condition)})
 if not condition:errors.append(label)
def strings(x):
 if isinstance(x,str):yield x
 elif isinstance(x,list):
  for y in x:yield from strings(y)
 elif isinstance(x,dict):
  for k,y in x.items():yield k;yield from strings(y)
jsons={p.name:json.loads(p.read_text(encoding='utf8')) for p in P.glob('*.json') if p.name not in ['validation.json','artifact-manifest.json']}
badnfc=[name for name,d in jsons.items() if any(unicodedata.normalize('NFC',s)!=s for s in strings(d))]
check(not badnfc,'All JSON keys/strings NFC: '+str(badnfc))
prompts=own('exercises-prompts.json')['items'];expected=[f'EX-VIII-{ex}-{n:02d}' for ex,total in [(26,10),(27,11)] for n in range(1,total+1)]
check([p['source_item_id'] for p in prompts]==expected,'Exactly VIII26.1–10 and27.1–11, original ordered IDs retained')
items=own('items.json')['source_items']
check([i['source_item_id'] for i in items]==expected,'All21 source items assigned once')
check(all(a['prompt']==b['prompt'] for a,b in zip(prompts,items)),'Prompt text unchanged across source and integrated item audit')
par=own('noun-adjective-paradigms.json')['paradigms'];li=own('lexical-inventory.json')['lemmas']
check(len(par)==18 and sum(len(p['cells']) for p in par)==144,'Eighteen complete nominal systems and144cells')
for p in par:
 cells={(f.get('contextual_analysis',f['analysis'])['case'],f.get('contextual_analysis',f['analysis'])['number']) for f in p['cells']}
 check(cells=={(c,n) for c in ['nom','gen','dat','acc'] for n in ['sg','pl']},'All eight required cells: '+p['lemma_id'])
prior=read('lexicon/entries.json')['lemmas'];pf={f['form_id']:f for l in prior for f in l['forms']};ps={s['sense_id']:s for l in prior for s in l['senses']}
ourlemmas=li+own('source-support-records.json')['lemmas']
identity=[]
for l in ourlemmas:
 for f in l['forms']:
  if f['form_id'] in pf and (f['form']!=pf[f['form_id']]['form'] or f['analysis']!=pf[f['form_id']]['analysis']):identity.append(f['form_id'])
 for s in l['senses']:
  if s['sense_id'] in ps and s['gloss']!=ps[s['sense_id']]['gloss']:identity.append(s['sense_id'])
check(not identity,'Prior form surfaces/analyses and sense glosses preserved: '+str(identity))
F={};S={}
for path in ['lexicon/entries.json','sources/audits/unit14-source/lexical-inventory.json','sources/audits/unit14-source/source-support-records.json','sources/audits/unit14-grammar/grammar-records.json','sources/audits/unit14-grammar/source-support.json']:
 for l in read(path)['lemmas']:
  for f in l['forms']:F[f['form_id']]=(l['lemma_id'],f)
  for s in l['senses']:S[s['sense_id']]=(l['lemma_id'],s)
reader=own('reading-token-ledger.json');models=own('author-only-cook-models.json')
check(reader['count']==len(reader['tokens'])==159,'All159 reading tokens explicitly bound')
check(' '.join(t['source_surface'] for t in reader['tokens'])==own('reading-source.json')['learner_text'],'Reading ledger exactly reconstructs learner text')
check([m['source_item_id'] for m in models['items']]==expected,'All21 private model item IDs align')
check(models['token_count']==sum(len(m['tokens']) for m in models['items'])==273,'All273 Cook model tokens explicitly bound')
bad=[]
for t in reader['tokens']+[t for m in models['items'] for t in m['tokens']]:
 fid,sid=t['form_id'],t['sense_id']
 if fid not in F or sid not in S:bad.append((t['token_id'],'missing record'));continue
 lid,f=F[fid];slid,s=S[sid]
 surf=t.get('surface',t.get('source_surface')).strip('.,;')
 if lid!=slid or lid!=t['lemma_id'] or surf.lower()!=f['form'].lower():bad.append((t['token_id'],fid,sid,surf))
check(not bad,'Every token has exact same-lemma form/sense identity and case-normalized surface: '+str(bad))
check(own('support-coverage-check.json')['passes'],'Every supplied reading/Cook dependency maps to visible help')
app=own('reading-apparatus.json')
check(len(app['notes'])==24 and len(app['anchors'])==25,'All24 original selected notes and25 anchors retained')
check(all(a['apparatus_id'] in {n['apparatus_id'] for n in app['notes']} for a in app['anchors']),'Every apparatus anchor resolves')
check('C04' in (R/'sources/CORRECTIONS.md').read_text(encoding='utf8') and 'C05' in (R/'sources/CORRECTIONS.md').read_text(encoding='utf8'),'Source corrections C04/C05 documented centrally')
ev=own('evidence-catalog.json')['evidence'];evmap={e['evidence_id']:e for e in ev}
check(len(evmap)==len(ev)==71,'Unique71 source evidence records')
check(all(e.get('personally_viewed') for e in ev),'All claimed primary evidence personally viewed')
check(all(digest(R/e['image_path'])==e['image_sha256'] for e in ev if 'image_path' in e),'All evidence image hashes match')
check(all(digest(R/e['path'])==e['sha256'] for e in own('source-inputs.json')['sources']),'Both selected source PDF hashes match')
ureg=set()
for d in jsons.values():
 ureg.update(s for s in strings(d) if s.startswith('U14-LEX-') or s.startswith('U14-FB-P') or s.startswith('U14-EX-P') or s.startswith('U14-SRC-P') or s.startswith('U14-BT-'))
check(ureg<=set(evmap),'Every Unit14 source evidence ID resolves locally: '+str(sorted(ureg-set(evmap))))
baseline=own('prior-scope-audit.json')
check(len(baseline['contracts'])==13,'All thirteen prior contracts audited')
check(all(digest(R/c['path'])==c['sha256'] for c in baseline['contracts']),'Prior contract hashes unchanged during source work')
check(baseline['registers'][0]['lemmas']==758 and baseline['registers'][0]['forms']==9308 and baseline['registers'][0]['senses']==918 and baseline['registers'][1]['features']==730,'Declared prior register baseline758/9308/918/730')
result={'schema_version':1,'status':'passed' if not errors else 'failed','checks':checks,'check_count':len(checks),'errors':errors,'counts':{'cook_items':21,'cook_tokens':273,'reading_tokens':159,'nominal_systems':18,'nominal_cells':144,'apparatus_notes':24,'apparatus_anchors':25,'evidence_records':71},'scope':'Concrete source-data validation only. Linguistic evidence remains the personally inspected primary pages and coordinated independent review; JSON validity does not certify linguistic truth.'}
(P/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'status':result['status'],'checks':len(checks),'errors':errors},ensure_ascii=False))
if errors:raise SystemExit(1)
