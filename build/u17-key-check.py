"""Key-author structural checks only; no independent-review claim."""
import hashlib,json,re,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf8'))
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
c=read('chapters/ch17/coverage.json');key=(ROOT/'chapters/ch17/answer-key.md').read_text(encoding='utf8')
assert key==unicodedata.normalize('NFC',key),'key not NFC'
tasks={t['task_id']:t for t in c['assigned_items']}
key_ids=re.findall(r'<!-- key: (.*?) -->',key)
output_ids=re.findall(r'<!-- output: (.*?) -->',key)
expected_key=[t['key_id']for t in tasks.values()]
expected_outputs=[p['output_position_id']for t in tasks.values()for p in t['output_positions']]
assert len(key_ids)==len(set(key_ids))==103
assert len(output_ids)==len(set(output_ids))==146
assert set(key_ids)==set(expected_key)
assert set(output_ids)==set(expected_outputs)
models={s['owner_id']:s for s in read('curriculum/proposals/unit17/author-only-cook-sequence-bindings.json')['sequences']}
assert len(models)==82
if c.get('selected_model_corrections'):
 for s in read(c['selected_model_corrections']['path'])['corrected_sequences']:models[s['owner_id']]=s
for tid,t in tasks.items():
 marker='<!-- key: '+t['key_id']+' -->'
 block=key.split(marker,1)[1].split('<!-- key:',1)[0]
 assert t['prompt']in block,tid+': exact prompt absent'
 for p in t['output_positions']:
  om='<!-- output: '+p['output_position_id']+' -->'
  assert om in block,tid+': misplaced output'
  if not tid.startswith('EX-'):assert p['label']in block,p['output_position_id']+': label absent'
  answer=block.split(om,1)[1].split('<!-- output:',1)[0].strip()
  assert len(answer)>30,p['output_position_id']+': empty answer'
 if tid in models:
  actual=block.strip().split('\n\n',1)[0].replace('**','')
  assert actual==models[tid]['text'],tid+': model text changed'
  assert '**Target and explanation:**'in block,tid+': missing explanation'
original={}
for name in ['author-only-original-sequence-bindings.json','author-only-form-bindings.json']:
 for s in read('curriculum/proposals/unit17/'+name)['sequences']:
  oid=s['output_position_id']
  if oid in original:assert original[oid]==s['text']
  original[oid]=s['text']
for oid,model in original.items():
 answer=key.split('<!-- output: '+oid+' -->',1)[1].split('<!-- output:',1)[0]
 assert '**'+model+'**'in answer,oid+': original model changed'
assert '[In this exercise, omit the article and the second personal pronoun throughout.]'in key
assert 'sōna swā 174.8'in key,'Corrected R03 label absent'
assert 'believes speaker'not in key
assert 'gif ðū mē gelīefst'not in key or 'permission'in key
assert key.count('[^key-sources]')==2
witness='chapters/ch17/key-author-reading-translation-witness.md'
wp=(ROOT/witness).read_text(encoding='utf8').strip().split('\n\n')
for p in wp[2:8]:assert p in key,'Independent witness translation paragraph omitted'
receipt={'status':'pass','role':'key author; not independent reviewer','contract_checkpoint_authorizing_draft':'6fc6fc1','contract_amendments_at_check':c.get('amendments',[]),'counts':{'tasks':103,'outputs':146,'exact_cook_models':82,'exact_cook_prompts':82,'original_tasks':21,'bound_original_oe_outputs':len(original),'reading_translation_divisions':3,'key_whitespace_words':len(key.split())},'checks':['One distinct key marker per task and output marker per requested response.','Every exact Cook prompt and its frozen first-paragraph model retained.','Every original output label and bound OE model retained.','All six independent witness translation paragraphs present under the three requested divisions.','Whole Exercise37 instruction and corrected R03 label present.','NFC and endnote reference checked.'],'hashes':{p:sha(p)for p in ['chapters/ch17/coverage.json','chapters/ch17/answer-key.md',witness]},'scope_limit':'This validates author coverage/identity, not linguistic correctness or the unfinished learner draft. Root runs the full check_unit17.py --draft once both manuscripts are ready; final PDF inspection remains required.'}
(ROOT/'build/u17-key-check.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps(receipt['counts'],ensure_ascii=False))
