"""Preserve and correct a modern reference-spacing error before draft review."""
import hashlib,json
from pathlib import Path
path=Path('chapters/ch17/coverage.json')
raw=path.read_bytes()
c=json.loads(raw)
task=next(t for t in c['assigned_items'] if t['task_id']=='NEW-U17-R03')
output=next(o for o in task['output_positions'] if o['output_position_id']=='NEW-U17-R03-O001')
before='Classify sōna swā174.8 and explain its time relation.'
after='Classify sōna swā 174.8 and explain its time relation.'
assert output['label']==before
assert not Path('chapters/ch17/authoring-amendments.json').exists()
amendment={
    'amendment_id':'U17-A01','date':'2026-10-28','stage':'authoring',
    'original_contract_checkpoint':'6fc6fc1','coordinator':'root','reported_by':'unit17_design',
    'reason':'Separate the cited Old English expression from its modern page/line reference with an ordinary space.',
    'changes':[{'output_position_id':output['output_position_id'],'field':'label','before':before,'after':after}],
    'unchanged':['All Old English source and models','All English Cook prompts','Tasks, answer targets, scope, record identities and paradigm cells','Sealed audit/proposal packets and original witnesses'],
    'contract_raw_sha256_before':hashlib.sha256(raw).hexdigest(),
    'review_status':'requires_independent_verification'
}
output['label']=after
c['amendments'].append(amendment)
path.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
Path('chapters/ch17/authoring-amendments.json').write_text(json.dumps({'chapter_id':'ch17','amendments':[amendment]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('U17-A01: inserted one ordinary space before the modern R03 reference; original retained.')
