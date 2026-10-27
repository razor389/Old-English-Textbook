"""Bounded consistency checks for this source packet; not a linguistic truth oracle."""
import json,pathlib,hashlib,collections,unicodedata
P=pathlib.Path(__file__).parent;R=P.resolve().parents[2]
def read(n):return json.loads((P/n).read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(n,x):(P/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
checks=[]
def check(name,condition,detail=None):
 checks.append(dict(check=name,passed=bool(condition),detail=detail));assert condition,(name,detail)
prompts=read('exercises-prompts.json');items=prompts['items'];counts=collections.Counter(i['original_exercise'] for i in items)
check('all50 exact item IDs once',len(items)==50 and len({x['source_item_id'] for x in items})==50)
check('complete exercise sets',dict(counts)=={28:12,29:11,30:13,31:14},dict(counts))
check('joint X, XI grouping retained',all(x['original_group']=='X, XI' and x['source_item_id'].startswith('EX-X-XI-31-') for x in items if x['original_exercise']==31))
check('two spanning prompts retain both pages',next(x for x in items if x['source_item_id']=='EX-IX-28-10')['printed_pages']==[15,16] and next(x for x in items if x['source_item_id']=='EX-X-XI-31-03')['printed_pages']==[17,18])
check('final meaningful prompt repairs retained',next(x for x in items if x['source_item_id']=='EX-IX-30-12')['prompt']=='If they can, let them live without me.' and next(x for x in items if x['source_item_id']=='EX-IX-30-06')['prompt']=='He that doeth and teacheth it, he shall be called great (micel).')
check('600dpi blossom hint repair retained','blōstmian, 118' in next(x for x in items if x['source_item_id']=='EX-IX-30-11')['prompt'] and any(x['change_id']=='U15-CN10' for x in read('source-change-notes.json')['changes']))
deps=read('exercises-dependencies.json')['items']
check('nominal audit covers every source item',[(x['source_item_id'],x['prompt']) for x in deps]==[(x['source_item_id'],x['prompt']) for x in items])
src=read('reading-source.json');spans=src['source_spans'];ledger=read('reading-token-ledger.json')['tokens']
check('reading sizes and complete source-word sequence',len(ledger)==415 and [s['word_count'] for s in spans]==[103,152,160] and all(' '.join(t['source_surface'] for t in ledger if t['source_span_id']==s['source_span_id'])==s['learner_text'] for s in spans))
check('reading token IDs unique and positions continuous',len({r['token_id'] for r in ledger})==415 and all([t['token_index_one_based'] for t in ledger if t['source_span_id']==s['source_span_id']]==list(range(1,s['word_count']+1)) for s in spans))
lines={l['source_line_id'] for s in spans for l in s['source_lines']}
check('every word has exact source line provenance',all(r['source_line_ids'] and set(r['source_line_ids'])<=lines for r in ledger))
check('source lexical hyphens keep component identities',all('component_tokens' in r and '-'.join(x['source_component'] for x in r['component_tokens'])==r['source_surface'].strip('.,;:!?“”‘’()') for r in ledger if '-' in r['source_surface']))
app=read('reading-apparatus.json');notes=app['notes']
check('complete original apparatus',len(notes)==27 and sum(len(n['anchors']) for n in notes)==33)
check('all original note anchors resolve',all(a['source_line_id'] in lines for n in notes for a in n['anchors']))
check('unmatched outer speech declared without silently added mark','outer opening quote remains unmatched' in ' '.join(src['normalizations']) and spans[0]['learner_text'].endswith('heofonum.’'))
old=json.loads((R/'lexicon/entries.json').read_text(encoding='utf8'));nom=read('lexical-inventory.json');sup=read('source-support-records.json');grams=[json.loads((R/'sources/audits/unit15-grammar'/n).read_text(encoding='utf8')) for n in ['grammar-records-core.json','grammar-records-lexical.json','grammar-records-families.json']]
F={};S={}
for d in [old,nom,*grams,sup]:
 for l in d['lemmas']:
  for f in l['forms']:F[f['form_id']]=(l['lemma_id'],f)
  for s in l['senses']:S[s['sense_id']]=(l['lemma_id'],s)
check('all415 exact form/sense identities and surfaces agree',all(r['form_id'] in F and r['sense_id'] in S and F[r['form_id']][0]==S[r['sense_id']][0]==r['lemma_id'] and F[r['form_id']][1]['form'].lower()==r['source_surface'].strip('.,;:!?“”‘’()').lower() for r in ledger))
help=read('reading-support.json');helprows=help['lexical_help']+help['grammar_help'];H={h['support_id']:h for h in helprows}
check('all supplied lexical dependencies visibly covered',all(any(r['form_id'] in H[h].get('form_ids',[]) and r['sense_id'] in H[h].get('sense_ids',[]) for h in r.get('support_ids',[]) if h in H) for r in ledger if r['form_status']=='supplied' or r['sense_status']=='supplied'))
check('all source orientation features visibly covered',len(sup['features'])==18 and all(any(g['feature_id'] in h.get('feature_ids',[]) for h in help['grammar_help']) for g in sup['features']))
check('all token support IDs resolve',all(h in H for r in ledger for h in r.get('support_ids',[])))
pars=read('noun-adjective-paradigms.json')['paradigms']
def cellkey(c,k):return c.get(k,c.get('contextual_analysis',c.get('analysis',{})).get(k))
check('complete explicit eight-slot nominal tables',len(pars)==29 and all(len(p['cells'])==8 and {(cellkey(c,'case'),cellkey(c,'number')) for c in p['cells']}=={(c,n) for c in ['nom','gen','dat','acc'] for n in ['sg','pl']} for p in pars))
check('all assigned literal nominal cells resolve',all(c['form_id'] in F and F[c['form_id']][1]['form']==c['form'] for p in pars for c in p['cells'] if c['form_id']))
check('abstract-u plural cells explicitly unassigned',all(c['form'] is None and c['knowledge_status']=='unassigned' for p in pars if p['lemma_id'] in ['haelu','haetu'] for c in p['cells'] if cellkey(c,'number')=='pl'))
check('people-name singular cells explicitly unassigned',all(c['form'] is None and c['knowledge_status']=='unassigned' for p in pars if p['lemma_id'] in ['engle','dene'] for c in p['cells'] if cellkey(c,'number')=='sg'))
check('bounded reference plurals not promoted to production',all(c['knowledge_status']=='new_recognition' for p in pars if p['lemma_id'] in ['aliesend','flaesc','willa','becraeding'] for c in p['cells'] if cellkey(c,'number')=='pl'))
check('complete strengu class reference remains recognition only',all(c['knowledge_status']=='new_recognition' for p in pars if p['lemma_id']=='strengu' for c in p['cells']) and next(l for l in nom['lemmas'] if l['lemma_id']=='strengu')['senses'][0]['knowledge_status']=='new_recognition')
check('prior prophet and bishop identities reused',next(x for x in deps if x['source_item_id']=='EX-IX-29-05')['nominal_requirements'][1]['lemma_id']=='witga' and next(x for x in deps if x['source_item_id']=='EX-X-XI-31-14')['nominal_requirements'][0]['lemma_id']=='bisceop')
check('unn an grant requirement uses genitive salvation',next(x for x in deps if x['source_item_id']=='EX-IX-29-11')['nominal_requirements'][1]['case']=='gen')
check('canonical grammar reading aliases selected',next(r for r in ledger if r['source_span_id']=='FB-IX-DUTIES-FIRST-ARGUMENT' and r['token_index_one_based']==54)['form_id']=='forgieldan-infinitive' and next(r for r in ledger if r['source_span_id']=='FB-IX-DUTIES-FIRST-ARGUMENT' and r['token_index_one_based']==71)['form_id']=='forgieldan-pres-1-sg' and next(r for r in ledger if r['source_span_id']=='FB-X-ALFRED-PREFACE' and r['token_index_one_based']==47)['form_id']=='aegther-u15-invariant')
oldforms={f['form_id']:f for l in old['lemmas'] for f in l['forms']};oldsenses={s['sense_id']:s for l in old['lemmas'] for s in l['senses']}
check('reused earlier form identity preserves original analysis',all(f['form']==oldforms[f['form_id']]['form'] and f['analysis']==oldforms[f['form_id']]['analysis'] for l in nom['lemmas'] for f in l['forms'] if f['form_id'] in oldforms))
check('reused earlier sense identity preserves original gloss',all(s['gloss']==oldsenses[s['sense_id']]['gloss'] for l in nom['lemmas'] for s in l['senses'] if s['sense_id'] in oldsenses))
ev=read('evidence-catalog.json');E={e['evidence_id']:e for e in ev['evidence']};refs=set()
def walk(x):
 if isinstance(x,dict):
  refs.update(x.get('evidence_refs',[]))
  for y in x.values():walk(y)
 elif isinstance(x,list):
  for y in x:walk(y)
for n in ['lexical-inventory.json','reading-source.json','reading-apparatus.json','source-support-records.json','source-change-notes.json','author-only-reading-model.json','exercises-prompts.json']:walk(read(n))
check('all own evidence references resolve',all(e in E for e in refs if e.startswith(('U15-FB-','U15-EX-','U15-WRIGHT-','U15-BT-'))))
check('every claimed primary image exists with sealed hash',all((R/e['image']).exists() and sha(R/e['image'])==e['image_sha256'] and e['personally_viewed'] for e in E.values()))
check('source cache hashes match selected editions',all(sha(R/x['path'])==x['sha256'] for x in read('source-inputs.json')['sources']))
prior=read('prior-scope-audit.json')
check('actual14 active contracts read at baseline',len(prior['contracts'])==14 and prior['counts']==dict(lemmas=830,forms=9710,senses=1017,features=820) and [x['path'] for x in prior['contracts']]==[f'chapters/ch{i:02}/coverage.json' for i in range(1,15)] )
check('baseline contract hashes still match',all(sha(R/x['path'])==x['sha256'] for x in prior['contracts']))
check('baseline cumulative register hashes still match',all(sha(R/x['path'])==x['sha256'] for x in prior['registers']))
check('structured text NFC',all(unicodedata.normalize('NFC',p.read_text(encoding='utf8'))==p.read_text(encoding='utf8') for p in P.glob('*.json')))
result=dict(schema_version=1,status='passed',check_count=len(checks),checks=checks,counts=dict(prompts=50,reading_tokens=415,original_notes=27,note_anchors=33,nominal_lemmas=32,nominal_tables=29,nominal_slot_count=232,nominal_form_records=242,lexical_help_groups=len(help['lexical_help']),construction_help_groups=18,evidence_records=len(E)),limits=['These checks establish packet consistency, not linguistic truth; image inspection and independent review remain necessary.','Final Cook ordered models, adjective/verb/pronoun systems and task integration are owned by the grammar/design workers.','No learner chapter completion or active register integration is certified.'])
dump('validation.json',result)
dump('support-coverage-check.json',dict(schema_version=1,reading_tokens=415,supplied_token_positions=sum(r['form_status']=='supplied' or r['sense_status']=='supplied' for r in ledger),lexical_help_groups=len(help['lexical_help']),construction_help_groups=18,uncovered_supplied_dependencies=[],unresolved_source_tokens=[]))
print(dict(status=result['status'],checks=len(checks),counts=result['counts']))
