"""Remove obsolete article requirements after the reviewed30.1 model correction."""
import json
from pathlib import Path

p=Path('chapters/ch15/coverage.json');c=json.loads(p.read_text(encoding='utf-8'))
t=next(t for t in c['assigned_items'] if t['task_id']=='EX-IX-30-01')
for field in ['required_sense_ids','required_output_sense_ids','tested_sense_ids']:
    assert 'se-the' in t[field],field
    t[field].remove('se-the')
for pos in t['output_positions']:
    pos['required_sense_ids'].remove('se-the')
for kind,rid,task in [('forms','se-m-gen-sg','EX-IX-30-01'),('forms','he-f-dat-sg','EX-X-XI-31-13'),('senses','se-the','EX-IX-30-01')]:
    key=kind[:-1]+'_id'
    for r in c['prior_requirements'][kind]:
        if r[key]==rid:
            for field in ['used_in_tasks','assessed_in']:
                r[field]=[v for v in r.get(field,[]) if v!=task]
next(a for a in c['amendments'] if a['amendment_id']=='U15-AM03')['changes'].append('Removed obsolete se-the sense requirements from30.1 and stale current-task usage links for the removed article/dative forms; actual earlier register history is unchanged.')
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Removed obsolete article-sense/current-task requirements; masters and frozen sources unchanged.')
