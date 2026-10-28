"""Read-only-to-masters independent closure check for Unit17 review."""
import hashlib, json, re
from pathlib import Path

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

c = read('chapters/ch17/coverage.json')
l = read('lexicon/entries.json')
g = read('curriculum/grammar.json')
student = Path('chapters/ch17/student.md').read_text(encoding='utf-8')
prior = {'form': {}, 'sense': {}, 'feature': {}}
current = {'form': {}, 'sense': {}, 'feature': {}}
for lemma in l['lemmas']:
    for kind, field in [('form','forms'),('sense','senses')]:
        for row in lemma.get(field, []):
            prior[kind][row[kind+'_id']] = row
for row in g['features']:
    prior['feature'][row['feature_id']] = row
for lemma in c['lexical_inventory']:
    for kind, field in [('form','forms'),('sense','senses')]:
        for row in lemma.get(field, []):
            current[kind][row[kind+'_id']] = row
for row in c['grammar_inventory']:
    current['feature'][row['feature_id']] = row

errors = []
routes = []
def productive(kind, rid):
    old, new = prior[kind].get(rid), current[kind].get(rid)
    if old and old.get('production_taught_in'):
        return 'actual_prior_register:'+old['production_taught_in']
    if new and new.get('knowledge_status') in ('new_production','previously_taught'):
        return 'current_contract:'+new['knowledge_status']
    return None

for task in c['assigned_items']:
    for out in task['output_positions']:
        for kind in prior:
            req = set(out.get('required_'+kind+'_ids', []))
            tested = set(out.get('tested_'+kind+'_ids', []))
            supplied = set(out.get('supplied_'+kind+'_ids', []))
            for rid in req:
                if rid not in prior[kind] and rid not in current[kind]:
                    errors.append([out['output_position_id'],kind,rid,'missing exact identity'])
            for rid in tested:
                route = productive(kind, rid)
                new = current[kind].get(rid, {})
                if not route and kind == 'feature' and new.get('knowledge_status') == 'new_recognition' and out.get('response_language') == 'English':
                    route = 'current_contract:new_recognition_in_English_analysis_with_visible_inputs'
                routes.append({'output_position_id':out['output_position_id'],'kind':kind,'record_id':rid,'production_route':route})
                if not route:
                    errors.append([out['output_position_id'],kind,rid,'tested without productive milestone'])
            if tested - req:
                errors.append([out['output_position_id'],kind,sorted(tested-req),'tested absent from required'])
            if supplied - req:
                errors.append([out['output_position_id'],kind,sorted(supplied-req),'supplied absent from required'])

markers = re.findall(r'<!-- teaching: ([^ ]+) -->', student)
expected = [t['teaching_id'] for t in c['teaching_records']]
missing_teaching = sorted(set(expected)-set(markers))
if missing_teaching:
    errors.append(['teaching_markers',missing_teaching])
summary = {'status':'pass' if not errors else 'needs_adjudication',
 'scope':'Checks exact identity existence and productive assessment milestones; linguistic absence of an unrecorded needed construction still requires the independent manual solve and review.',
 'contract_raw_sha256':hashlib.sha256(Path('chapters/ch17/coverage.json').read_bytes()).hexdigest(),
 'task_count':len(c['assigned_items']),
 'output_count':sum(len(t['output_positions']) for t in c['assigned_items']),
 'tested_routes_checked':len(routes),'teaching_record_count':len(expected),
 'errors':errors,'tested_record_routes':routes}
Path('build/u17-blind-dependency-check.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in summary.items() if k!='tested_record_routes'},ensure_ascii=False,indent=2))
