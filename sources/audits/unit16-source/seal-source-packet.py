"""One-time source reconciliation report and hash manifest for Unit16."""
import json,pathlib,re,hashlib,collections,datetime,unicodedata
OUT=pathlib.Path(__file__).parent;ROOT=OUT.parents[2]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def own(n):return read('sources/audits/unit16-source/'+n)
def dump(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
lex=own('lexical-inventory.json');par=own('noun-adjective-paradigms.json');ledger=own('reading-token-ledger.json');r=own('reading-source.json')['source_spans'][0];app=own('reading-apparatus.json');prompts=own('exercises-prompts.json');deps=own('exercises-dependencies.json');catalog=own('evidence-catalog.json')
prior=read('lexicon/entries.json')['lemmas'];grammar=read('sources/audits/unit16-grammar/grammar-records.json')['lemmas'];verbal=read('sources/audits/unit16-grammar/reading-verbal-support.json')['lemmas']
alllem=prior+lex['lemmas']+grammar+verbal
forms={};senses={}
for l in alllem:
 for f in l.get('forms',[]):forms[f['form_id']]=(l['lemma_id'],f)
 for s in l.get('senses',[]):senses[s['sense_id']]=(l['lemma_id'],s)
errors=[];checks=[]
def check(label,ok,detail=None):
 checks.append({'check':label,'passed':bool(ok),'detail':detail})
 if not ok:errors.append(label)
check('59 complete English prompts in original item order',len(prompts['items'])==59 and [p['source_item_id'] for p in prompts['items']]==[f'EX-XII-XIII-{e}-{i:02}' for e,n in [(32,11),(33,10),(34,13),(35,14),(36,11)] for i in range(1,n+1)])
check('59 dependency records match exact English prompts',len(deps['items'])==59 and all(a['source_item_id']==b['source_item_id'] and a['prompt']==b['prompt'] for a,b in zip(prompts['items'],deps['items'])))
check('444 ordered reading tokens and51 editorial source lines',len(ledger['tokens'])==444 and len(r['source_lines'])==51 and r['word_count']==444)
check('54 original notes and59 preserved anchor positions',len(app['notes'])==54 and sum(len(x['anchors']) for x in app['notes'])==59)
check('No unresolved lexical bindings',not ledger['unresolved'])
contextual_required={31:'fultum-u15-source-sense',85:'apollonius-u16-reading',133:'theod-u16-region',156:'apollonius-u16-reading',211:'on-u16-at-work',232:'apollonius-u16-reading',315:'apollonius-u16-reading',323:'haelu-u11-source',371:'apollonius-u16-reading'}
check('Source-local nominal senses retain their declared supplied scope',all(ledger['tokens'][n-1]['sense_id']==sid and ledger['tokens'][n-1]['sense_status']=='supplied' for n,sid in contextual_required.items()))
bad=[]
for t in ledger['tokens']:
 if t.get('form_id') not in forms or t.get('sense_id') not in senses:bad.append([t['token_id'],'missing identity']);continue
 lid,f=forms[t['form_id']];slid,s=senses[t['sense_id']]
 if lid!=t['lemma_id'] or slid!=lid:bad.append([t['token_id'],'lemma mismatch',lid,slid,t['lemma_id']])
 if unicodedata.normalize('NFC',f['form']).casefold()!=unicodedata.normalize('NFC',t['surface']).casefold():bad.append([t['token_id'],'surface mismatch',f['form'],t['surface']])
check('Every reading form/sense belongs to its stated lemma and exact surface',not bad,bad)
oldforms={f['form_id']:f for l in prior for f in l.get('forms',[])}
badold=[f['form_id'] for l in lex['lemmas'] for f in l['forms'] if f['form_id'] in oldforms and (f['form']!=oldforms[f['form_id']]['form'] or f['analysis']!=oldforms[f['form_id']]['analysis'])]
check('Reused actual form surfaces and original analyses preserved',not badold,badold)
dup=[]
for l in lex['lemmas']:
 for field,idkey in [('forms','form_id'),('senses','sense_id')]:
  ids=[x[idkey] for x in l[field]]
  if len(ids)!=len(set(ids)):dup.append([l['lemma_id'],field])
check('No duplicate source lemma/form/sense identities',not dup and len(lex['lemmas'])==len({x['lemma_id'] for x in lex['lemmas']}),dup)
check('26 nominal/adjective tables with356 cells',len(par['paradigms'])==26 and sum(len(p['cells']) for p in par['paradigms'])==356)
scopebad=[]
for p in par['paradigms']:
 if p['lemma_id']=='begen' and len(p['cells'])!=12:scopebad.append(p['paradigm_id'])
 if p['paradigm_id'].startswith('NEW-U16-ADJ') and len(p['cells'])!=50:scopebad.append(p['paradigm_id'])
check('Complete newly introduced adjective/both systems',not scopebad,scopebad)
missing=[]
for name in ['lexical-inventory.json','noun-adjective-paradigms.json','reading-token-ledger.json','reading-constructions.json','exercise-constructions.json','exercises-dependencies.json']:
 for ref in set(re.findall(r'U16-(?:FB|EX|WRIGHT|MT)-P\d+',(OUT/name).read_text(encoding='utf-8'))):
  if ref not in catalog:missing.append([name,ref])
check('Every source-owned page evidence reference resolves',not missing,missing)
images=[]
for eid,e in catalog.items():
 p=ROOT/e.get('image',e.get('image_path',''))
 if not p.is_file():images.append([eid,'image missing',str(p)])
 elif e.get('image_sha256') and sha(p)!=e['image_sha256']:images.append([eid,'hash mismatch'])
check('Retained evidence images exist and hashes match',not images,images)
pathbad=[]
for x in deps['items']:
 for k in ['nominal_inventory_path','paradigm_path','verbal_and_clause_dependency_path','contextual_binding_snapshot']:
  if not (ROOT/x[k]).is_file():pathbad.append([x['source_item_id'],k,x[k]])
check('Exercise dependency file references resolve',not pathbad,pathbad)
binding_path=ROOT/'curriculum/proposals/unit16/author-only-cook-sequence-bindings.json'
binding=json.loads(binding_path.read_text(encoding='utf-8'))
selected={(s['owner_id'],t['token_index']):t for s in binding['sequences'] for t in s['tokens']}
rolebad=[]
for item in deps['items']:
 for t in item['nominal_and_function_dependencies']:
  key=(item['source_item_id'],t['token_index']);current=selected[key]
  for field in ['assessment_role','support_ids']:
   if t.get(field)!=current.get(field):rolebad.append([*key,field])
check('All copied nominal/function assessment roles match final contextual bindings',not rolebad,rolebad)
validation={'schema_version':1,'status':'passed' if not errors else 'failed','checks':checks,'errors':errors,'scope':'Structural validation plus the recorded manual contextual review; not a substitute for coordinator contract/key review.','counts':{'prompts':59,'reading_tokens':444,'source_lines':51,'source_notes':54,'source_anchors':59,'nominal_tables':26,'nominal_cells':356,'lexical_proposals':len(lex['lemmas']),'evidence_records':len(catalog),'reading_frames':21,'exercise_frames':19,'nominal_and_function_exercise_positions':sum(len(x['nominal_and_function_dependencies']) for x in deps['items'])}}
dump('validation.json',validation)
if errors:print(json.dumps(validation,ensure_ascii=False,indent=1));raise SystemExit(1)
report={'schema_version':1,'status':'source packet sealed for integration','baseline':'e1d94be968e89ecfc4918ed58d850702e5d0e57e','scope':{'exercises':'All59 exact joint-group XII,XIII items32–36 assigned; no redistribution or omission.','reading':'Cook FB168.1–170.16 /PDF184–186, complete Gymnasium subsection,444 words.','earlier_reading_overlap':'No reassignment of the earlier Unit6 fisherman gift/direction excerpt; the current scene is later and separately located.'},'manual_review':['Personally inspected source prompt pages and reading pages; source OCR used only as a finding aid.','Earlier teaching checked against all15 actual contracts and both actual cumulative registers before proposals.','All444 tokens reviewed contextually; design independently reviewed full-ledger cases/persons/senses and the resulting corrections are explicit.','Every nominal/function position in the59 Cook models is copied from the reconciled contextual binding with exact form/sense identities and support roles.','F05 nearu four-cell contrasts and bēgen+sunu phrases independently certified against viewed Wright/Cook tables and actual prior sunu records.'],'resolved_findings':['34.3 books, not hooks; hooked sęndan/nętt32.6; source168.2 ōð-ðæt. These repair audit transcription, not source errors.','35.10 retains then ðā and short-e beran.','nętt zero nominative/accusative plural checked against Wright174–175 cyn(n) model and explicit nett membership.','hǣle retains actual haelu-acc-sg-source and safety/rescue sense; oath context locally supplied.','John endings independently checked in primary WS Matthew114/PDF124; initial I→J alone declared to follow Cook’s hint.','Source169note10 Latin describes rubbing with ointment and rejuvenation; no shoulder/neck noun. Original Latin remains exact and relevant meaning is supplied in English.','The previously noted geong strong/weak genitive identity collision is resolved with distinct IDs.','Ordinary old preposition forms are separated from source-local senses, including back-adverbs, playing partners, means, clothing and speech addressees.'],'preserved_source_uncertainties':['169.3 geslægene awkward agreement remains exact and locally supported.','169.5–7 nested reference/linkage remains explicitly uncertain as Cooknote6 states; negative næfde retained.','169.11 top remains tentatively ball; the OE/Latin discrepancy is presented rather than harmonized.','170.2–4 missing closing quotation mark and170.15 mixed speech levels are preserved and documented.','168.3 meahte and169.9 hęrede do not supply uniquely recognizable mood endings; contextual analyses are not unaided mood-identification targets.'],'scope_decisions':['Reading-only rare nouns/forms and whole constructions remain supplied; overlapping taught forms retain actual prior IDs.','Complete new nearu adjective and bēgen plural system receive tables and explicit basic uses; familiar nouns are derived from checked shared models.','Selected mass/abstract/title senses do not invent count plurals.','mǣden table selects the zero plural permitted for disyllabic neuters by Cook47.1, with retained-e stem under47.7; it is a declared model derivation, not an assertion that every dialect/source has only this form.','Original source notes remain separate from modern helps; Latin needed for the assigned discrepancy task is explained in English.'],'remaining_source_questions':[],'validation_path':'sources/audits/unit16-source/validation.json','integration_note':'Coordinator owns canonical contract, shared registers, learner/key prose, export review and final completion. Sealing this packet does not certify those later stages.'}
if (OUT/'pre-contract-role-refresh.json').exists():report['pre_contract_metadata_refresh']=own('pre-contract-role-refresh.json')
if (OUT/'pre-contract-sense-refresh.json').exists():report['pre_contract_sense_refresh']=own('pre-contract-sense-refresh.json')
dump('source-audit-report.json',report)
artifacts=[]
for p in sorted(OUT.iterdir()):
 if p.is_file() and p.suffix in ['.json','.py'] and p.name!='artifact-manifest.json':artifacts.append({'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size,'role':'audit input/finding aid' if p.name in ['nominal-prior-candidates.json'] else 'source packet'})
dump('artifact-manifest.json',{'schema_version':1,'status':'sealed after source reconciliation','generated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'artifacts':artifacts,'image_catalog':'sources/audits/unit16-source/evidence-catalog.json','external_dependencies':['sources/audits/unit16-grammar/reading-verbal-support.json','sources/audits/unit16-grammar/exercises-verbal-dependencies.json','curriculum/proposals/unit16/author-only-cook-sequence-bindings.json'],'counts':validation['counts']})
print(json.dumps({'status':validation['status'],'counts':validation['counts'],'manifest_artifacts':len(artifacts)},ensure_ascii=False))
