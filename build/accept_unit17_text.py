"""Guarded coordinator acceptance of independent Unit17 text and paradigm reviews."""
import argparse, hashlib, json
from pathlib import Path

def read(path): return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def sha(raw): return hashlib.sha256(raw).hexdigest()
def write(path,data): Path(path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def check_artifacts(records,required):
    assert {r['path'] for r in records} == required
    for r in records:
        raw=Path(r['path']).read_bytes()
        assert sha(raw)==r['raw_sha256'] and sha(raw.replace(b'\r\n',b'\n'))==r['normalized_lf_sha256'],r['path']
def check_semantic(c,record):
    mutable = {'status','review_status','completion','amendments','textual_review','presentation_review','contract_checkpoint','complete_drafts_checkpoint','independent_solutions_checkpoint','accepted_text_checkpoint'}
    assert set(record['keys']) == set(c) - mutable
    payload=json.dumps({k:c[k] for k in record['keys']},ensure_ascii=False,sort_keys=True,separators=(',',':'))
    assert sha(payload.encode('utf-8'))==record['sha256']

p=argparse.ArgumentParser()
for n in ['solutions-checkpoint','drafts-checkpoint','contract-checkpoint']: p.add_argument('--'+n,required=True)
args=p.parse_args()
c=read('chapters/ch17/coverage.json')
r=read('chapters/ch17/review-ledger.json')
pr=read('chapters/ch17/reviews/paradigms.json')
for ledger in [r, pr]:
    if isinstance(ledger['accepted_artifact_identities'], dict):
        ledger['accepted_artifact_identities'] = list(ledger['accepted_artifact_identities'].values())
assert r['status']=='accepted_pre_export' and pr['status']=='accepted'
assert r['counts']['material_open_findings']==0 and not pr['material_open_findings']
assert r['reviewer']=='unit17_blind' and pr['reviewer']=='unit17_paradigms'
assert r['independence']['blind_solutions_checkpoint']==args.solutions_checkpoint
assert r['independence']['no_current_author_role'] is True
assert r['independence']['all_tasks_solved_before_key_access'] is True
assert {t['task_id'] for t in r['task_reviews']}=={t['task_id'] for t in c['assigned_items']}
assert len(r['task_reviews'])==len(c['assigned_items'])==c['contract_metrics']['tasks']
assert all(t['status']=='accepted' for t in r['task_reviews'])
expected_outputs={o['output_position_id'] for t in c['assigned_items'] for o in t['output_positions']}
assert {o['output_position_id'] for o in r['output_position_reviews']}==expected_outputs
assert len(r['output_position_reviews'])==len(expected_outputs)==c['contract_metrics']['requested_output_positions']
assert all(o['status']=='accepted' for o in r['output_position_reviews'])
checks=pr['paradigm_checks']
assert len(checks)==len(c['paradigms'])
assert {v['paradigm_id'] for v in checks}=={v['paradigm_id'] for v in c['paradigms']}
expected={p['paradigm_id']:{v.get('cell_id',v.get('form_id')) for v in p['cells']} for p in c['paradigms']}
for row in checks:
    assert row['status']=='accepted'
    assert set(row['checked_logical_cell_ids'])==expected[row['paradigm_id']]
    assert not row['mismatches']
assert len(pr['cell_route_checks'])==sum(len(p['cells']) for p in c['paradigms'])
assert {(v['paradigm_id'],v['logical_cell_id']) for v in pr['cell_route_checks']}=={(pid,cid) for pid,ids in expected.items() for cid in ids}
assert all(v['status']=='accepted' for v in pr['cell_route_checks'])
check_artifacts(r['accepted_artifact_identities'],{'chapters/ch17/'+n for n in ['student.md','answer-key.md','independent-solutions.md']})
check_artifacts(pr['accepted_artifact_identities'],{'chapters/ch17/student.md','chapters/ch17/answer-key.md'})
for ledger in [r,pr]:
    check_semantic(c,ledger['accepted_contract_semantic_identity'])
    inspections = ledger.get('primary_evidence_image_inspections') or ledger.get('fresh_page_image_inspections', [])
    assert inspections
    for image in inspections:
        assert image['actually_viewed'] is True
        assert sha(Path(image['path']).read_bytes())==image['raw_sha256']
    for finding in ledger.get('findings',[]):
        assert finding.get('status', finding.get('resolution_status')) in ['resolved','resolved_verified','accepted','verified','withdrawn','adjudicated']
raw=Path('chapters/ch17/coverage.json').read_bytes()
c['status']='text_accepted_exports_pending'
c['review_status']='accepted_pre_export'
c['contract_checkpoint']=args.contract_checkpoint
c['complete_drafts_checkpoint']=args.drafts_checkpoint
c['independent_solutions_checkpoint']=args.solutions_checkpoint
for amendment in c['amendments']:
    amendment['review_status']='verified_by_independent_review'
    amendment['review_record']='chapters/ch17/review.md'
c['textual_review']={
 'status':'accepted','reviewer':'unit17_blind','record':'chapters/ch17/review.md','ledger':'chapters/ch17/review-ledger.json',
 'review_record_sha256':sha(Path('chapters/ch17/review.md').read_bytes()),
 'review_ledger_sha256':sha(Path('chapters/ch17/review-ledger.json').read_bytes()),
 'accepted_artifacts':{Path(a['path']).name:{'sha256':a['raw_sha256'],'sha256_normalized_lf':a['normalized_lf_sha256']} for a in r['accepted_artifact_identities']},
 'counts':r['counts'],'accepted_contract_semantic_identity':r['accepted_contract_semantic_identity'],
 'accepted_contract_artifact_at_review':{'sha256':sha(raw),'sha256_normalized_lf':sha(raw.replace(b'\r\n',b'\n'))},
 'identity_scope_note':'Both masters, frozen blind solutions, and substantive contract content are identified. Subsequent completion metadata does not alter accepted teaching.',
 'independent_solutions_checkpoint':args.solutions_checkpoint,
 'independence':'Fresh non-author solved all contracted actual learner tasks before key/private-audit access; coordinator froze the witness in Git before unlocking comparison. A separate fresh non-author checked every paradigm and display route against primary evidence.',
 'fresh_review':{'record':'chapters/ch17/reviews/paradigms.json','sha256':sha(Path('chapters/ch17/reviews/paradigms.json').read_bytes())},
 'material_open_findings':0,
 'scope_limit':'Complete exports, every-page visual inspection and register integration remain separate gates.'}
write('chapters/ch17/coverage.json',c)
amendments=read('chapters/ch17/authoring-amendments.json')
amendments['current_verification']={
    'status':'accepted_by_independent_review',
    'amendment_ids':[x['amendment_id'] for x in c['amendments']],
    'text_review':'chapters/ch17/review.md',
    'paradigm_review':'chapters/ch17/reviews/paradigms.json',
    'accepted_contract_semantic_sha256':r['accepted_contract_semantic_identity']['sha256'],
    'history_note':'Each amendment retains its original creation-stage status; this field records the subsequent independent verification.'}
write('chapters/ch17/authoring-amendments.json',amendments)
co=read('chapters/ch17/coordinator-review.json')
co['status']='accepted_independent_text_review'
co['independent_acceptance']={'record':'chapters/ch17/review.md','ledger':'chapters/ch17/review-ledger.json','paradigms':'chapters/ch17/reviews/paradigms.json','material_open_findings':0}
co['automated_checks']['teaching_locations']=len(c['teaching_records'])
co['accepted_artifact_identities']=r['accepted_artifact_identities']
co['independence_limit']='Root and the source, grammar and design authors do not claim fresh blind independence. A fresh non-author froze every solution at '+args.solutions_checkpoint+' before explicit comparison access; a separate fresh non-author verified the paradigms.'
co['remaining_gates']=['Produce complete LuaLaTeX exports, full parity and every-page non-author inspection.','Integrate preserved registers, update README/indexes/status/handoff, export Beads and commit locally.']
co['scope_limit']='Independent text and paradigm review accepted. Export inspection and register integration remain separate gates. Earlier draft observations and identities are retained as historical records.'
write('chapters/ch17/coordinator-review.json',co)
print('Independent text and paradigm reviews accepted; exports remain pending.')
