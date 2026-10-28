"""Compare actual Unit17 Markdown matrices to independently source-derived cells.

Produces a check receipt, never acceptance. Manual explanatory prose and key
review is a separate gate. Preserves the original source-stage review receipt.
"""
from pathlib import Path
import importlib.util
import json
import re
import hashlib

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('source_review',ROOT/'build/u17-paradigms-source-check.py')
src=importlib.util.module_from_spec(spec)
spec.loader.exec_module(src)
c=src.read('chapters/ch17/coverage.json')
original=ROOT/'build/u17-paradigms-source-stage.json'
if not original.exists():
    original.write_bytes((ROOT/'chapters/ch17/reviews/paradigms.json').read_bytes())
original_md=ROOT/'build/u17-paradigms-source-stage.md'
if not original_md.exists():
    original_md.write_bytes((ROOT/'chapters/ch17/reviews/paradigms.md').read_bytes())
text=(ROOT/'chapters/ch17/student.md').read_text(encoding='utf-8-sig')
lines=text.splitlines()
markers=[]
for i,l in enumerate(lines):
    match=re.fullmatch(r'<!-- table: (\S+) -->',l)
    if match: markers.append((match[1],i))
actual={}; findings=[]
for mid,start in markers:
    if mid in actual: findings.append({'matrix_id':mid,'problem':'duplicate marker'})
    j=start+1
    while not lines[j].startswith('|'): j+=1
    raw=[]
    while j<len(lines) and lines[j].startswith('|'):
        raw.append((j+1,[x.strip() for x in lines[j].strip().strip('|').split('|')]))
        j+=1
    actual[mid]={'marker_line':start+1,'header_line':raw[0][0],'headers':raw[0][1],
                 'row_line_numbers':[r[0] for r in raw[2:]],'rows':[r[1] for r in raw[2:]]}
expected_matrices={m['matrix_id']:m for m in c['display_plan']['matrices']}
if set(actual)!=set(expected_matrices):
    findings.append({'problem':'matrix coverage','missing':sorted(set(expected_matrices)-set(actual)),
                     'unexpected':sorted(set(actual)-set(expected_matrices))})
matrix_checks=[]
for mid,m in expected_matrices.items():
    a=actual[mid]; issues=[]
    if a['headers']!=m['headers']: issues.append({'type':'headers','actual':a['headers'],'contract':m['headers']})
    if a['rows']!=m['rows']: issues.append({'type':'rows','actual':a['rows'],'contract':m['rows']})
    if issues: findings.append({'matrix_id':mid,'issues':issues})
    matrix_checks.append({'matrix_id':mid,'status':'passed' if not issues else 'mismatch',
                         'student_marker_line':a['marker_line'],'headers':a['headers'],
                         'row_labels':[r[0] for r in a['rows']],'issues':issues})
routes={(r['paradigm_id'],r['logical_cell_id']):r for r in c['display_plan']['paradigm_cell_display_routes']}
cell_checks=[]
for p in c['paradigms']:
    for x in p['cells']:
        r=routes[p['paradigm_id'],x['logical_cell_id']]; a=actual[r['matrix_id']]
        row=r['row_index_zero_based']; col=r['column_index_zero_based']
        surface=a['rows'][row][col]; exp=src.expected(p,x); issues=[]
        if surface!=exp: issues.append({'type':'actual_source_disagreement','actual':surface,'source_expected':exp})
        if surface!=x['form']: issues.append({'type':'actual_contract_disagreement','actual':surface,'contract':x['form']})
        if issues: findings.append({'paradigm_id':p['paradigm_id'],'logical_cell_id':x['logical_cell_id'],'issues':issues})
        cell_checks.append({'paradigm_id':p['paradigm_id'],'logical_cell_id':x['logical_cell_id'],
            'status':'passed' if not issues else 'mismatch','matrix_id':r['matrix_id'],
            'row_index_zero_based':row,'column_index_zero_based':col,
            'student_line':a['row_line_numbers'][row],'actual_surface':surface,
            'source_expected':exp,'actual_column_label':a['headers'][col],
            'actual_row_label':a['rows'][row][0],'issues':issues})
mutable={'status','review_status','completion','amendments','textual_review','presentation_review',
 'contract_checkpoint','complete_drafts_checkpoint','independent_solutions_checkpoint','accepted_text_checkpoint'}
keys=sorted(set(c)-mutable)
payload=json.dumps({k:c[k] for k in keys},ensure_ascii=False,sort_keys=True,separators=(',',':'))
receipt={'reviewer':'unit17_paradigms','status':'mechanical_actual_matrix_check_only',
    'artifact_identities':[src.identity('chapters/ch17/'+n) for n in ['student.md','answer-key.md']],
    'contract_semantic_identity':{'keys':keys,'sha256':hashlib.sha256(payload.encode('utf-8')).hexdigest()},
    'matrix_checks':matrix_checks,'cell_checks':cell_checks,'findings':findings,
    'counts':{'actual_matrices':len(actual),'expected_matrices':len(expected_matrices),
              'logical_cells':len(cell_checks),'mismatches':len(findings)}}
src.write('build/u17-paradigms-master-check.json',receipt)
print(json.dumps(receipt['counts'],ensure_ascii=False))
print(json.dumps(findings,ensure_ascii=False))
print(json.dumps(receipt['artifact_identities'],ensure_ascii=False))
