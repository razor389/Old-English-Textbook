"""Author readback and identity checks; this is not a blind review."""
import json,re,hashlib,unicodedata
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text(encoding='utf8'))
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
C=load('chapters/ch18/coverage.json');tasks={t['task_id']:t for t in C['assigned_items']};key=(R/'chapters/ch18/answer-key.md').read_text(encoding='utf8')
assert key==unicodedata.normalize('NFC',key)
kids=re.findall(r'<!-- key: (.*?) -->',key);oids=re.findall(r'<!-- output: (.*?) -->',key)
assert len(kids)==len(set(kids))==60
assert len(oids)==len(set(oids))==87
assert set(kids)=={t['key_id']for t in tasks.values()}
assert set(oids)=={p['output_position_id']for t in tasks.values()for p in t['output_positions']}
cook={s['owner_id']:s for s in load('curriculum/proposals/unit18/author-only-cook-sequence-bindings.json')['sequences']}
assert len(cook)==47
assert sum(len(s['text'].split())for s in cook.values())==940
translation_parts=[]
for number in range(1,4):
 block=key.split(f'<!-- output: NEW-U18-R01-O{number:03} -->',1)[1].split('<!-- output:',1)[0].strip()
 body=block.split('\n\n',1)[1].split('**Target and explanation:**',1)[0]
 translation_parts.append(' '.join(body.split()))
witness=load('sources/audits/unit18-grammar/independent-reading-translation.json')['translation']
assert ' '.join(translation_parts)==' '.join(' '.join(witness).split()),'Independent witness wording changed'
readback=[]
for tid,t in tasks.items():
 block=key.split('<!-- key: '+t['key_id']+' -->',1)[1].split('<!-- key:',1)[0]
 assert t['prompt']in block,tid+' exact prompt'
 if tid in cook:
  model=block.strip().split('\n\n',1)[0].replace('**','');assert model==cook[tid]['text'],tid+' model changed'
  assert '**Target and explanation:**'in block
 for p in t['output_positions']:
  om='<!-- output: '+p['output_position_id']+' -->';assert om in block
  tail=block.split(om,1)[1].split('<!-- output:',1)[0]
  assert len(tail.strip())>60,p['output_position_id']+' empty answer'
  if tid.startswith('NEW-'):assert p['label']in tail
  readback.append({'task_id':tid,'output_position_id':p['output_position_id'],'status':'authored and checked','target':p['target'],'essential_meaning_basis':'exact Cook English prompt and unchanged selected model'if tid.startswith('EX-')else'exact original label plus stated participants, roles and time relations','explanation':'individual answer paragraph','alternatives':'shared grammatical-order/equivalent-wording policy plus item-specific distinctions where relevant','diagnosis':'individual answer paragraph identifies the relevant role, case, agreement, tense/mood or interpretation error'})
original={}
for fn in ['author-only-original-sequence-bindings.json','author-only-form-bindings.json']:
 for s in load('curriculum/proposals/unit18/'+fn)['sequences']:
  if s.get('kind')=='output'or s.get('output_position_id'):
   oid=s.get('output_position_id')
   if oid:original[oid]=s['text']
for oid,model in original.items():
 answer=key.split('<!-- output: '+oid+' -->',1)[1].split('<!-- output:',1)[0]
 assert '**'+model+'**'in answer,oid+' bound model absent'
for n in C['source_spans'][0]['original_notes']:assert n['original_text']in key,n['apparatus_id']
assert len(C['source_spans'][0]['original_notes'])==22
assert sum(len(n['anchors'])for n in C['source_spans'][0]['original_notes'])==29
assert 'ōðre sīðe'in key and 'hē funde'in key and 'for ēowerre ðearfe'in key
assert 'accusative reflexive'in key and 'superlative'in key and 'greatest part/portion'in key
assert 'does not narrate'in key and 'source gives no instruction to omit'in key
assert key.count('[^key-sources]')==2
assert all('unresolved'not in x.lower()for x in re.findall(r'\bUNRESOLVED\b',key))
result={'status':'pass','role':'key author; not independent or blind reviewer','contract_checkpoint_authorizing_prose':'6874c20e7127fa33c41406d1aa6c0b087e59c824','contract_amendments_at_readback':C.get('amendments',[]),'counts':{'tasks':60,'requested_outputs':87,'exact_cook_models':47,'exact_cook_prompts':47,'original_tasks':13,'original_answers':40,'bound_original_oe_outputs':len(original),'reading_translation_divisions':3,'original_reading_notes':22,'original_note_anchors_retained':29,'key_whitespace_words':len(key.split())},'checks':['One key marker per task and one output marker per requested response.','Every Cook model is the unchanged first paragraph after its key marker, matching the official checker convention.','Every original output label and bound Old English model is present.','All47 source prompts and all13 original task prompts are exact.','All22 original reading note texts and29 anchor relationships are retained.','Reading translation derives from the preserved independent witness; only division boundaries and surrounding explanation differ.','Critical distinctions read back:44.7 instrumental/counterfactual perfect;47.5 valid funde;47.11 present commandest;48.6 dative ēowerre;48.7 omitted be; reading6 finite-content see sense and225 accusative reflexive; delayed relative; greatest-part superlative; proposed rather than completed final rest.','NFC and endnote reference checked.'],'output_readback':readback,'hashes':{p:sha(p)for p in ['chapters/ch18/coverage.json','chapters/ch18/answer-key.md','sources/audits/unit18-grammar/independent-reading-translation.json']},'source_problem_reported':{'item':'45.7','issue':'A frozen audit explanation incorrectly attributed permission to omit for ourselves to Cook. Exact prompt contains no such omission instruction.','disposition':'Coordinator recorded bounded amendment U18-A01; key retains and explains ūs, and all frozen audit/proposal files remain untouched by this author.'},'unresolved_points':[],'scope_limit':'Author verification establishes coverage, exact model/prompt identity and the stated readback. It does not replace independent solving, source review, full learner/key integration checking or inspection of exported PDF pages.'}
(R/'chapters/ch18/key-author-readback.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps(result['counts'],ensure_ascii=False))
