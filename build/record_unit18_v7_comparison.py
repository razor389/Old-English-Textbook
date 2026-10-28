"""Retain a separate readback of changed v7 models; preserve the v6 witness."""
from pathlib import Path
import hashlib
import json

def read(path): return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def identity(path):
    raw=Path(path).read_bytes()
    return {'path':path,'sha256':hashlib.sha256(raw).hexdigest()}
prior_path='sources/audits/unit18-coordinator/prompt-model-comparison.json'
current_path='sources/audits/unit18-grammar/candidate-models.json'
amendment_path='sources/audits/unit18-grammar/model-amendments-v7.json'
old={x['source_item_id']:x['candidate_model_at_readback'] for x in read(prior_path)['items']}
new={x['item_id']:x['model'] for x in read(current_path)['items']}
changes=read(amendment_path)['amendments']
for change in changes:
    sid=change['source_item_id']
    assert old[sid]==change['before'],sid
    assert new[sid]==change['after'],sid
assert {sid for sid in old if old[sid]!=new[sid]}=={x['source_item_id'] for x in changes}
report={
    'chapter_id':'ch18','reviewer':'coordinator','stage':'precontract author readback',
    'prior_comparison_preserved':identity(prior_path),
    'current_models':identity(current_path),'amendment_record':identity(amendment_path),
    'changed_items':[x['source_item_id'] for x in changes],
    'observations':[
        'Personally read all six v7 amended sentences against their retained English prompts. Participants, quantities, clause relations and source controls remain intact.',
        'The four unmarked feoh occurrences preserve the selected source spelling. This does not claim a historically short vowel or invalidate a documented differently marked spelling.',
        '46.8 now uses mīnne seolfrenne læfel, with the complete supplied masculine accusative adjective phrase. The v6 material-genitive choice is preserved as a superseded proposal, not relabeled impossible Old English.',
        '48.3 now selects the actually prior-taught ðȳ-lǣs-ðe spelling; its negative-purpose function and the father’s grief are unchanged.',
        '48.2 retains the complete supplied permission/substitution frame. Personally viewed Crawford195 corroborates the permissive command and for hine; this additional evidence does not turn the model into an exact source quotation.'
    ],
    'remaining_gates':['Complete dependency joins','Canonical contract before prose','Fresh independent learner and paradigm review']
}
Path('sources/audits/unit18-coordinator/prompt-model-v7-addendum.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Retained v6 comparison unchanged and recorded all six v7 changes separately.')
