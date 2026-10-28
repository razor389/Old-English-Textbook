"""Record the coordinator's readback of the two preposition spelling changes."""
from pathlib import Path
import hashlib
import json

def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def identity(p): return {'path':p,'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()}
changes=read('sources/audits/unit18-grammar/model-amendments-v8.json')['amendments']
old={x['item_id']:x['model'] for x in read('sources/audits/unit18-grammar/candidate-models-v7-witness.json')['items']}
new={x['item_id']:x['model'] for x in read('sources/audits/unit18-grammar/candidate-models.json')['items']}
for x in changes:
    assert old[x['source_item_id']]==x['before']
    assert new[x['source_item_id']]==x['after']
assert {sid for sid in old if old[sid]!=new[sid]}=={x['source_item_id'] for x in changes}
report={
    'chapter_id':'ch18','reviewer':'coordinator','stage':'precontract author readback',
    'earlier_comparisons_preserved':[
        identity('sources/audits/unit18-coordinator/prompt-model-comparison.json'),
        identity('sources/audits/unit18-coordinator/prompt-model-v7-addendum.json')],
    'current_models':identity('sources/audits/unit18-grammar/candidate-models.json'),
    'amendments':changes,
    'observations':'Personally read both complete changed sentences against the exact prompts. Būtan byrig expresses outside the city in46.9; būtan ðǣm cnapan expresses absence of the boy in48.3. The selected preposition spelling is distinguished from unchanged conjunction būton in the unless clauses. The two contextual senses retain their independently checked teaching or local-support status.',
    'scope_limit':'Author-preparation comparison only; full dependency validation and independent review remain required.'
}
Path('sources/audits/unit18-coordinator/prompt-model-v8-addendum.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Recorded both v8 changes without altering earlier comparison witnesses.')
