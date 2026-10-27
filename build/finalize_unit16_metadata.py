"""Record actual Unit16 acceptance; never bypass linguistic or presentation gates."""
import argparse
import hashlib
import json
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('stage', choices=['presentation', 'complete'])
p.add_argument('--exports-checkpoint')
a = p.parse_args()
def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def write(path, data): Path(path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
c = read('chapters/ch16/coverage.json')
assert c['textual_review']['status'] == 'accepted'
s = c['textual_review']['accepted_contract_semantic_identity']
payload = json.dumps({k:c[k] for k in s['keys']},ensure_ascii=False,sort_keys=True,separators=(',',':'))
assert hashlib.sha256(payload.encode('utf-8')).hexdigest() == s['sha256']
pages = read('typesetting/ch16/page-review.json')
assert pages['status'] == 'PASS' and not pages['unresolved_findings']
assert pages['every_final_page_visually_inspected_by_non_author']
for doc in pages['documents']:
    assert sha(doc['path']) == doc['sha256']
c['presentation_review'] = {
    'status':'accepted','record':'typesetting/ch16/page-review.json',
    'record_sha256':sha('typesetting/ch16/page-review.json'),
    'page_totals':pages['page_totals'], 'complete_content_parity':'typesetting/ch16/content-parity.json',
    'every_page_inspected_by_non_author':True, 'unresolved_findings':[],
    'documents':[{k:d[k] for k in ['kind','path','sha256','pages']} for d in pages['documents']]
}
if a.stage == 'presentation':
    layout = read('typesetting/ch16/layout-adjustments.json')
    layout['status'] = 'accepted_after_non_author_reinspection'
    layout['final_page_totals'] = pages['page_totals']
    layout['final_documents'] = [{k:d[k] for k in ['kind','path','sha256','pages']} for d in pages['documents']]
    layout['final_review_record'] = 'typesetting/ch16/page-review.json'
    layout['final_review_record_sha256'] = sha('typesetting/ch16/page-review.json')
    layout['final_content_parity'] = 'typesetting/ch16/content-parity.json'
    layout['all_reported_findings_resolved_or_withdrawn'] = True
    layout['linguistic_masters_changed'] = False
    layout['acceptance_limit'] = 'The identified final exports passed full parity, clean logs and non-author inspection of every page. Individual ledgers preserve the actual inspections, repairs and verified byte-identical reuse.'
    write('typesetting/ch16/layout-adjustments.json', layout)
    c['status'] = 'text_and_exports_accepted_registers_pending'
    c['review_status'] = 'accepted_text_and_exports'
else:
    reg = read('chapters/ch16/register-integration.json')
    assert reg['status'] == 'accepted'
    for record in reg['register_identities']:
        assert sha(record['path']) == record['sha256']
    c['status'] = 'reviewed_complete'
    c['review_status'] = 'accepted_text_and_exports'
    c['completion'] = {
        'complete':True,'registers_integrated':True,'pdfs_inspected':True,'date':'2026-10-27',
        'register_integration':'chapters/ch16/register-integration.json',
        'presentation_review':'typesetting/ch16/page-review.json',
        'learner_pdf':'typesetting/ch16/chapter-16.pdf','key_pdf':'typesetting/ch16/answer-key.pdf',
        'all_assigned_tasks_reviewed':c['contract_metrics']['tasks'],'all_cook_items_retained':59,
        'next_unit_policy':'Unit17 remains undrafted; begin only when requested.',
        'checkpoint_note':'Completion files and Beads export are saved locally; final handoff records the resulting revision.'
    }
    if a.exports_checkpoint:
        c['completion']['complete_exports_registers_checkpoint'] = a.exports_checkpoint
    co = read('chapters/ch16/coordinator-review.json')
    co['status'] = 'accepted_complete'
    co['presentation_acceptance'] = {'record':'typesetting/ch16/page-review.json','sha256':sha('typesetting/ch16/page-review.json'),'page_totals':pages['page_totals']}
    co['register_integration'] = {'record':'chapters/ch16/register-integration.json','sha256':sha('chapters/ch16/register-integration.json'),'metrics':reg['metrics'],'earlier_active_artifacts_preserved':reg['prior_active_files_preserved'],'archive_files_preserved':reg['archived_files_preserved']}
    co['remaining_gates'] = []
    co['scope_limit'] = 'Unit16 complete; no Unit17 drafting. Authors do not claim fresh blind independence. Original witnesses, sealed audits, earlier chapters and archive are preserved.'
    write('chapters/ch16/coordinator-review.json',co)
write('chapters/ch16/coverage.json',c)
print('Recorded actual Unit16 '+a.stage+' acceptance without changing substantive teaching.')
