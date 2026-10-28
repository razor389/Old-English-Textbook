"""Inspect actual contracted support locations for reused supplied identities."""
import json
from pathlib import Path
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
c=read('chapters/ch17/coverage.json')
b=read('build/unit17-prior-baseline.json')
proposed={kind:{r[kind+'_id'] for l in c['lexical_inventory'] for r in l[kind+'s']} for kind in ['form','sense']}
proposed['feature']={r['feature_id'] for r in c['grammar_inventory']}
prior={kind:{r[kind+'_id']:r for l in b['lexicon']['lemmas'] for r in l[kind+'s']} for kind in ['form','sense']}
prior['feature']={r['feature_id']:r for r in b['grammar']['features']}
helps=[{'owner':t['task_id'],**h} for t in c['assigned_items'] for h in t.get('local_support',[])]
helps += [{'owner':s['source_span_id'],**h} for s in c['source_spans'] for h in s.get('local_support',[])]
findings=[]
for kind in proposed:
    used={rid for t in c['assigned_items'] for rid in t.get('supplied_'+kind+'_ids',[])}
    for rid in sorted(used-proposed[kind]):
        p=prior[kind][rid]
        if p.get('production_taught_in') or p.get('recognition_taught_in'): continue
        teaching=[r['teaching_id'] for r in c['teaching_records'] if rid in r.get(kind+'_ids',[])]
        support=[h for h in helps if h.get(kind+'_id')==rid or rid in h.get(kind+'_ids',[])]
        findings.append({'kind':kind,'id':rid,'teaching':teaching,'support':[{'owner':h['owner'],'support_id':h['support_id'],'text':h.get('exact_help_text',h.get('source_form')),'evidence':h.get('evidence_refs')} for h in support]})
Path('build/unit17-reused-support-diagnostic.json').write_text(json.dumps(findings,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for f in findings:
    if not f['teaching']:
        print(f['kind'],f['id'],'explicit helps',len(f['support']),f['support'][:1])
print('Total reused supplied identities',len(findings),'missing both',sum(not f['teaching'] and not f['support'] for f in findings))
