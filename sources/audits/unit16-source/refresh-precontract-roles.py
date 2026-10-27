"""Refresh only four copied assessment roles after pre-contract reconciliation."""
import json,pathlib,hashlib,sys,datetime
OUT=pathlib.Path(__file__).parent;ROOT=OUT.parents[2]
binding=ROOT/'curriculum/proposals/unit16/author-only-cook-sequence-bindings.json'
depfile=OUT/'exercises-dependencies.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
expected=sys.argv[1]
assert sha(binding)==expected,('Binding identity changed',sha(binding),expected)
deps=json.loads(depfile.read_text(encoding='utf-8'));seq=json.loads(binding.read_text(encoding='utf-8'))
lookup={(s['owner_id'],t['token_index']):t for s in seq['sequences'] for t in s['tokens']}
allowed={('EX-XII-XIII-33-03',15),('EX-XII-XIII-33-10',6),('EX-XII-XIII-34-07',18),('EX-XII-XIII-36-02',5)}
changes=[];identity_fields=['token_index','surface','lemma_id','form_id','sense_id','contextual_analysis','form_status','sense_status']
before_hash=sha(depfile)
for item in deps['items']:
 for t in item['nominal_and_function_dependencies']:
  key=(item['source_item_id'],t['token_index']);new=lookup[key]
  assert all(t.get(k)==new.get(k) for k in identity_fields),('Unexpected non-role change',key)
  fields={k:{'before':t.get(k),'after':new.get(k)} for k in ['assessment_role','support_ids'] if t.get(k)!=new.get(k)}
  if fields:
   assert key in allowed,('Unexpected role position',key)
   changes.append({'source_item_id':key[0],'token_index':key[1],'surface':t['surface'],'form_id':t['form_id'],'sense_id':t['sense_id'],'changes':fields})
   for k in fields:t[k]=new.get(k)
assert len(changes)==4,('Expected exactly four copied-position repairs',len(changes))
depfile.write_text(json.dumps(deps,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
record={'schema_version':1,'stage':'pre-contract integration refresh','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reason':'Unrelated same-task lexical helps had incorrectly marked four independently productive preposition positions as supplied. Repair assessment metadata only; preserve wording, IDs, grammatical analyses and scope statuses.','binding_path':binding.relative_to(ROOT).as_posix(),'binding_sha256':expected,'dependency_before_sha256':before_hash,'dependency_after_sha256':sha(depfile),'positions_checked':sum(len(x['nominal_and_function_dependencies']) for x in deps['items']),'changes':changes}
(OUT/'pre-contract-role-refresh.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'updated_positions':len(changes),'binding_sha256':expected,'dependencies_sha256':sha(depfile)}))
