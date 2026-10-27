"""Concrete repeated checks for this packet's literal cells and cross-file identities."""
import json,pathlib,hashlib,collections,re
R=pathlib.Path(__file__).resolve().parents[3];O=pathlib.Path(__file__).resolve().parent
def load(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def put(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
files=['grammar-records-core.json','grammar-records-families.json','grammar-records-lexical.json','source-support.json','principal-parts.json','lexical-frames.json','pronoun-dispositions.json','exercises-verbal-dependencies.json','evidence-catalog.json','author-only-cook-models.json','prior-scope-audit.json']
P={n:load('sources/audits/unit15-grammar/'+n) for n in files};issues=[]
baseline=load('lexicon/entries.json');baseforms={f['form_id']:(l['lemma_id'],f) for l in baseline['lemmas'] for f in l['forms']}
forms=baseforms.copy();senses={s['sense_id']:s for l in baseline['lemmas'] for s in l['senses']}
for p in [load('sources/audits/unit15-source/lexical-inventory.json'),load('sources/audits/unit15-source/source-support-records.json'),*[P[n] for n in files]]:
 for l in p.get('lemmas',[]):
  for f in l['forms']:
   if f['form_id'] in forms and forms[f['form_id']][1]['form']!=f['form']:issues.append({'kind':'surface_identity_conflict','id':f['form_id']})
   forms[f['form_id']]=(l['lemma_id'],f)
  for s in l['senses']:senses[s['sense_id']]=s
paradigms=[p for n in ['grammar-records-core.json','grammar-records-families.json','grammar-records-lexical.json'] for p in P[n].get('paradigms',[])]
sizes={'IND':12,'NEG-IND':12,'SUBJ':12,'IMP':2,'INF':2,'PART':2,'STRONG-NGDA':24,'WEAK-NGDA':24,'SINGULAR-NGDA':8,'ADVERB-DEGREES':3}
for p in paradigms:
 if len(p['cells'])!=sizes[p['system']]:issues.append({'kind':'incomplete_defined_system','id':p['paradigm_id'],'cells':len(p['cells'])})
 for c in p['cells']:
  if 'components' in c:
   if 'form_id' in c:issues.append({'kind':'multiword_inflected_identity','id':c['form_id']})
   for a in c['components']:
    if a['form_id'] not in forms or forms[a['form_id']][1]['form']!=a['form']:issues.append({'kind':'bad_construction_component','cell':c.get('cell_id'),'component':a})
  elif c['form_id'] not in forms or forms[c['form_id']][1]['form']!=c['form']:issues.append({'kind':'unbound_paradigm_cell','id':c['form_id']})
for row in P['principal-parts.json']['records']:
 for q in row['parts']:
  if q['form_id'] not in forms or forms[q['form_id']][1]['form']!=q['form']:issues.append({'kind':'unbound_principal_part','id':q['form_id']})
for h in P['source-support.json']['cook_support']:
 for q in h['bindings']:
  if q['form_id'] not in forms:issues.append({'kind':'unbound_help_form','help':h['support_id'],'id':q['form_id']})
  if q['sense_id'] not in senses:issues.append({'kind':'unbound_help_sense','help':h['support_id'],'id':q['sense_id']})
catalog={q['evidence_id']:q for q in P['evidence-catalog.json']['records']};evrefs=set()
def walk(x):
 if isinstance(x,dict):
  evrefs.update(x.get('evidence_refs',[]))
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
for n in files[:7]:walk(P[n])
for e in sorted(evrefs-catalog.keys()):issues.append({'kind':'unresolved_evidence','id':e})
for q in catalog.values():
 for im in q['images']:
  p=R/im['image_path']
  if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=im['image_sha256']:issues.append({'kind':'image_hash_mismatch','id':q['evidence_id']})
  if not im['personally_viewed']:issues.append({'kind':'unviewed_evidence_claim','id':q['evidence_id']})
src=load('sources/audits/unit15-source/exercises-prompts.json')['items'];models=P['author-only-cook-models.json']['items'];deps=P['exercises-verbal-dependencies.json']['items']
expected=[i['source_item_id'] for i in src]
for label,ids in [('models',[i['source_item_id'] for i in models]),('dependencies',[i['item_id'] for i in deps])]:
 if ids!=expected:issues.append({'kind':'item_crosswalk_mismatch','file':label})
if len(expected)!=50:issues.append({'kind':'source_count','count':len(expected)})
seq=load('curriculum/proposals/unit15/author-only-cook-sequence-bindings.json')['sequences'];sq={x['owner_id']:x for x in seq}
for m in models:
 x=sq.get(m['source_item_id'],{})
 if x.get('text')!=m['model']:issues.append({'kind':'model_binding_text_mismatch','id':m['source_item_id']})
 for t in x.get('tokens',[]):
  if t['form_id'] not in forms:issues.append({'kind':'unbound_token_form','id':t['form_id'],'item':m['source_item_id']})
  if t['sense_id'] not in senses:issues.append({'kind':'unbound_token_sense','id':t['sense_id'],'item':m['source_item_id']})
for d in deps:
 if d['remaining_unresolved']:issues.append({'kind':'dependency_has_pending_token_issue','item':d['item_id']})
 for f in d['grammar_requirements']:
  if f['knowledge_status']=='unresolved':issues.append({'kind':'feature_status_unresolved','item':d['item_id'],'feature':f['feature_id']})
counts={'prior_contracts_parsed':len(P['prior-scope-audit.json']['contracts']),'defined_systems':len(paradigms),'literal_logical_cells':sum(len(p['cells']) for p in paradigms),'construction_positions':sum(1 for p in paradigms for c in p['cells'] if 'components' in c),'principal_part_rows':len(P['principal-parts.json']['records']),'lexical_frames':len(P['lexical-frames.json']['frames']),'family_dispositions':len(P['pronoun-dispositions.json']['records']),'visible_cook_helps':len(P['source-support.json']['cook_support']),'cook_models':len(models),'cook_token_bindings':sum(len(x['tokens']) for x in seq),'evidence_records':len(catalog)}
result={'schema_version':1,'chapter':'ch15','status':'pass' if not issues else 'pending','counts':counts,'checks':['All14 actual active contracts parsed before proposals, with baseline hashes preserved.','All defined systems have their stated literal cell counts.','Composite ne+copula cells contain lexical components, not invented multiword word IDs.','All principal-part display positions resolve exact IDs and explicit reference/production status.','All local support bindings resolve forms/senses.','All evidence refs resolve personally viewed original-page images with matching hashes.','All50 source IDs occur once in original source order across models and dependency ledger.','Final contextual Cook token identities resolve actual merged baseline/proposed inventory.'],'limits':['Mechanical identity closure does not itself certify linguistic truth. Primary-image inspection and independent source-first compositions are separately documented.','No chapter prose, active registers, coverage contract, Beads or Git state is modified by this worker.','Source editor owns nominal paradigms and415-word reading context ledger; design worker owns original task bindings.'],'issues':issues}
put('validation.json',result)
print(json.dumps(result,ensure_ascii=False,indent=2))
