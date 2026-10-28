"""Record the completed independent review of the final Unit17 masters.

Run only after the actual amended files, all repairs and source evidence have
been personally reviewed. This writes only this reviewer's own records; it does
not execute the coordinator's accept_unit17_text.py or modify the contract.
"""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    'chapters/ch17/student.md': 'f387f880e0423dd8c6adddf9765cba7b05d10bbe3850fc8593045fcfeec9d05a',
    'chapters/ch17/answer-key.md': 'c6710364dde62f50c01f7bfeab57fd6ed813dddaa13d6860cfd55e75b5b2a81d'
}

def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))

def identity(path):
    raw = (ROOT / path).read_bytes()
    return {'path': path, 'raw_sha256': hashlib.sha256(raw).hexdigest(),
            'normalized_lf_sha256': hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest()}

def line_record(path, containing):
    lines = (ROOT / path).read_text(encoding='utf-8').splitlines()
    matches = [(i + 1, line) for i, line in enumerate(lines) if containing in line]
    assert len(matches) == 1, (path, containing, len(matches))
    return {'path': path, 'line': matches[0][0], 'actual_text': matches[0][1]}

def item_text(task_id):
    text = (ROOT / 'chapters/ch17/student.md').read_text(encoding='utf-8')
    start = text.index('<!-- item: ' + task_id + ' -->')
    end = text.find('\n### ', start)
    return text[start:end if end != -1 else len(text)]

for path, expected in EXPECTED.items():
    assert identity(path)['raw_sha256'] == expected, (path, 'Unreviewed master change')

c = read('chapters/ch17/coverage.json')
ledger = read('chapters/ch17/reviews/paradigms.json')
receipt = read('build/u17-paradigms-master-check.json')
amendment = read('build/u17-paradigms-amendment-check.json')
spec = read('chapters/ch17/support-amendment-spec.json')
assert receipt['counts'] == {'actual_matrices': 124, 'expected_matrices': 124,
                              'logical_cells': 1234, 'mismatches': 0}
assert not receipt['findings']
assert amendment['status'] == 'contract_amendment_checks_passed' and not amendment['findings']
assert amendment['reviewed_contract_identity'] == identity('chapters/ch17/coverage.json')
assert amendment['reviewed_specification_identity'] == identity('chapters/ch17/support-amendment-spec.json')
for artifact in receipt['artifact_identities']:
    assert artifact == identity(artifact['path'])

mutable = {'status', 'review_status', 'completion', 'amendments', 'textual_review', 'presentation_review',
           'contract_checkpoint', 'complete_drafts_checkpoint', 'independent_solutions_checkpoint', 'accepted_text_checkpoint'}
keys = sorted(set(c) - mutable)
semantic = {'keys': keys, 'sha256': hashlib.sha256(json.dumps(
    {k: c[k] for k in keys}, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()}
assert receipt['contract_semantic_identity'] == semantic

# Preserve the open-finding stage as an actual immutable review-history artifact.
for extension in ['json', 'md']:
    target = ROOT / f'build/u17-paradigms-preacceptance.{extension}'
    if not target.exists():
        target.write_bytes((ROOT / f'chapters/ch17/reviews/paradigms.{extension}').read_bytes())

student = 'chapters/ch17/student.md'
key = 'chapters/ch17/answer-key.md'
repairs = {
    'P17-01': {
        'resolution': 'The diagnostic now explicitly gives first/third singular gecwæð with æ/ð and second singular gecwǣde/plural gecwǣdon with ǣ/d. The complete unchanged table matches the rule and Cook §106.',
        'verified_passages': [line_record(student, 'In the preterite, first and third singular gecwæð')]
    },
    'P17-02': {
        'resolution': 'Both global sense labels now say taught. The separate original mægen lexical hint and its local non-recall scope remain intact.',
        'verified_passages': [line_record(key, 'with the explicitly taught sense'),
                              line_record(key, 'with the specifically taught princess sense')]
    },
    'P17-03': {
        'resolution': 'The local help identifies a finite desired-content clause under the verb of desire, with the selected subjunctive. It no longer calls the clause purpose.',
        'verified_passages': [line_record(student, 'expressing what all nations desired')],
        'follow_up_repair_history': [
            {'stage': 'first author repair', 'problem': 'The revised help named the exact finite answer gewilnodon even though its form remained independently assessed at39.4 token12.',
             'action': 'Coordinator removed the finite surface while retaining the desired-content explanation.',
             'verification': 'Actual final39.4 help says expressing what all nations desired and contains no gewilnodon.'}
        ]
    },
    'P17-04': {
        'resolution': 'The local help now preserves plural spirits of the storms as the subject of fulfilment.',
        'verified_passages': [line_record(student, 'The spirits of the storms fulfil his word;')],
        'follow_up_repair_history': [
            {'stage': 'first author repair', 'problem': 'The revised help supplied dōð even though its form remained independently assessed at37.8 token12.',
             'action': 'Coordinator removed the finite surface while retaining the plural-subject explanation.',
             'verification': 'Actual final37.8 help contains no dōð; the original dictionary hint dōn remains.'}
        ]
    },
    'P17-05': {
        'resolution': 'The local help now says seat, matching the singular original prompt and of setle model.',
        'verified_passages': [line_record(student, 'Omit the marked their without deleting the seat.')]
    }
}
assert 'dōð' not in item_text('EX-XII-XIII-37-08')
assert 'gewilnodon' not in item_text('EX-XII-XIII-39-04')
for finding in ledger['findings']:
    finding['status'] = 'resolved_verified'
    finding['original_coordinator_disposition'] = finding.get('coordinator_disposition')
    finding['coordinator_disposition'] = 'Author/coordinator repair completed after the blind witness freeze; independently reread and verified against the accepted artifacts.'
    finding['resolution_review'] = repairs[finding['finding_id']]
    finding['resolution_artifact_identities'] = receipt['artifact_identities']

support_verifications = []
for rule in spec['constructions']:
    for task_id in rule['task_ids']:
        text = item_text(task_id)
        expected_help = '**Supplied:** ' + rule['text'] + ' — ' + rule['analysis']
        assert expected_help in text, (task_id, 'Actual visible support does not match the reviewed contract')
        support_verifications.append({'task_id': task_id, 'feature_id': rule['feature_id'],
                                      'status': 'resolved_verified', 'actual_visible_help': expected_help})
for check in ledger['corroborated_supplied_construction_gaps']:
    check['status'] = 'resolved_verified'
    check['resolution'] = 'U17-A02 adds bounded supplied feature, exact task input and full reference positions; final learner prints the complete phrase locally, and final key explicitly excludes independent recall of its government/construction.'
    check['contract_binding_receipt'] = 'build/u17-paradigms-amendment-check.json'
ledger['actual_supplied_construction_verifications'] = support_verifications

# This source was independently viewed for the final key's negative alternative.
bt_path = 'build/u17-blind-bt-b0709.jpg'
bt = identity(bt_path)
bt.update({'actually_viewed': True, 'reviewer': 'unit17_paradigms',
           'inspection_method': 'Personal view_image inspection after final comparison unlock; not inferred from the blind reviewer report.',
           'inspection_phase': 'final key alternative verification',
           'observation': 'Bosworth–Toller printed709, nān I(a), explicitly distinguishes use without other negatives and gives finite examples; I(b) gives use with other negatives. The source supports nān without mandatory ne and the negative-concord alternative ne sīe. No new negation paradigm is claimed.',
           'source_locators': [{'work': 'Bosworth–Toller main dictionary', 'printed_page': 709,
                               'original_identifier': 'nān, I(a) and I(b)'}]})
if not any(x['path'] == bt_path for x in ledger['primary_evidence_image_inspections']):
    ledger['primary_evidence_image_inspections'].append(bt)
for img in ledger['primary_evidence_image_inspections']:
    if img['path'] == 'sources/audits/unit17-source/fb-p38.png':
        img.setdefault('later_personal_inspections', []).append({
            'inspection_phase': 'final key alternative verification',
            'observation': 'Cook §55 says adjectives are weak sometimes after possessives and otherwise strong. Therefore the41.8 prompt does not mandate the weak model: strong ūrne dæghwāmlīcne hlāf is also valid, consistent with prior Unit3 teaching.'})
    assert img['actually_viewed'] is True and identity(img['path'])['raw_sha256'] == img['raw_sha256']

ledger['additional_key_and_metadata_verifications'] = [
    {
        'subject': 'B17-05, Cook41.8 strong/weak alternative', 'status': 'resolved_verified',
        'evidence': ['sources/audits/unit17-source/fb-p38.png', 'chapters/ch03/coverage.json'],
        'rationale': 'Cook §55 explicitly permits weak sometimes after possessives; the actual earlier contract teaches the strong alternative. The printed prompt mandates neither. The final key keeps its valid weak model and accepts strong dæghwāmlīcne.',
        'verified_passage': line_record(key, 'strong **ūrne dæghwāmlīcne hlāf** is also valid')
    },
    {
        'subject': 'Cook43.15 nān and optional negative concord', 'status': 'verified',
        'evidence': [bt_path],
        'rationale': 'Personally inspected nān I(a)/(b) confirms the unchanged negative model is valid and ne sīe is also defensible.',
        'verified_passage': line_record(key, '**Nān** supplies negation here;')
    },
    {
        'subject': 'A02 current cweðende analysis and reference routes', 'status': 'resolved_verified',
        'initial_observation': 'The first amendment copied inherited singular source analysis without specifying current plural context; some new reference-route arrays remained empty despite separate local support IDs.',
        'resolution': 'Current input/output contextual analyses explicitly identify nominative masculine plural accompanying speech. Historical source analysis remains separately preserved. All22 affected input/output tokens now have direct reference-route IDs; every local_support_id and full output reference position is bound.',
        'verification_receipt': 'build/u17-paradigms-amendment-check.json'
    }
]

tasks = {t['task_id']: t for t in c['assigned_items']}
for binding in amendment['task_binding_checks']:
    task = tasks[binding['task_id']]
    sequence = next(x for x in task['input_sequences'] if x['sequence_id'] == binding['support_id'])
    for position, incoming in zip(binding['positions'], sequence['tokens']):
        outgoing = task['assessed_output_tokens'][position - 1]
        for token in [incoming, outgoing]:
            assert binding['support_id'] in token['reference_route_ids']
            assert token['form_assessment_role'] == token['sense_assessment_role'] == 'visible_reference_position'

actual = {(r['paradigm_id'], r['logical_cell_id']): r for r in receipt['cell_checks']}
for row in ledger['cell_route_checks']:
    checked = actual[row['paradigm_id'], row['logical_cell_id']]
    assert checked['status'] == 'passed' and not checked['issues']
    assert row['expected_form_from_reviewed_sources'] == checked['source_expected'] == checked['actual_surface']
    row.update({'status': 'accepted', 'learner_master_checked': True,
                'actual_surface': checked['actual_surface'], 'student_line_at_review': checked['student_line'],
                'actual_column_label': checked['actual_column_label'], 'actual_row_label': checked['actual_row_label'],
                'actual_route_mismatches': []})
for row in ledger['paradigm_checks']:
    assert not row['mismatches']
    row['status'] = 'accepted'
    row['learner_master_checked'] = True
    row['answer_key_uses_checked'] = True
    row['resolved_finding_ids'] = row.pop('open_findings', [])
    row['final_rule_and_scope_verification'] = 'Actual diagnostic prose, exceptions, teaching/reference scopes and key uses reviewed; all relevant findings resolved against the final master identities.'
    if row['paradigm_id'] == 'u17-gecwethan-indicative12':
        row['final_rule_and_scope_verification'] = repairs['P17-01']['resolution']

for row in receipt['matrix_checks']:
    row['status'] = 'accepted'
ledger['actual_matrix_checks'] = receipt['matrix_checks']
expected_pairs = {(p['paradigm_id'], x['logical_cell_id']) for p in c['paradigms'] for x in p['cells']}
assert len(ledger['paradigm_checks']) == 110
assert len(ledger['cell_route_checks']) == 1234
assert {(x['paradigm_id'], x['logical_cell_id']) for x in ledger['cell_route_checks']} == expected_pairs
for paradigm in c['paradigms']:
    row = next(x for x in ledger['paradigm_checks'] if x['paradigm_id'] == paradigm['paradigm_id'])
    assert set(row['checked_logical_cell_ids']) == {x['logical_cell_id'] for x in paradigm['cells']}

ledger['status'] = 'accepted'
ledger['acceptance_scope'] = 'Final learner/key linguistic text, paradigms and amended supplied-construction scopes accepted; rendered-export inspection and active-register integration remain separate coordinator gates.'
ledger['independence'].update({'final_master_ready_unlock_received': True,
                               'final_actual_master_reread_complete': True,
                               'blind_witness_checkpoint_before_comparison': 'ed28a8e',
                               'post_unlock_coordination': 'Shared direct source evidence and corroborated supplied-frame findings after comparison was explicitly unlocked.'})
ledger['independence']['findings_not_disclosed_to_blind_solver_before_unlock'] = ledger['independence'].pop('findings_not_disclosed_to_blind_solver')
ledger['pre_acceptance_review_history'] = [identity('build/u17-paradigms-preacceptance.json'),
                                         identity('build/u17-paradigms-preacceptance.md'),
                                         identity('build/u17-paradigms-master-check-draft.json')]
ledger['accepted_artifact_identities'] = receipt['artifact_identities']
ledger['accepted_contract_semantic_identity'] = semantic
ledger['accepted_contract_artifact_at_review'] = identity('chapters/ch17/coverage.json')
ledger['amendment_verification'] = {'status': 'verified', 'amendment_ids': ['U17-A01', 'U17-A02'],
                                  'contract_binding_receipt': identity('build/u17-paradigms-amendment-check.json'),
                                  'source_support_receipt': identity('build/u17-paradigms-support-review.json'),
                                  'conclusion': 'A01 ordinary-space separation and A02 five supplied phrase bindings are present. Original prompts, models, paradigms, source reading and earlier teaching records are preserved.'}
ledger['material_open_findings'] = 0
ledger['counts'].update({'primary_images_personally_viewed': len(ledger['primary_evidence_image_inspections']),
                         'actual_matrices_checked': 124, 'actual_routes_checked': 1234,
                         'actual_table_mismatches': 0, 'open_findings': 0, 'material_open_findings': 0,
                         'resolved_original_findings': 5, 'resolved_supplied_constructions': 4,
                         'amended_task_bindings_verified': 5})
ledger['manual_master_review'].update({
    'student_lines_reviewed': 'Complete original master1–4791, followed by the complete final diff and actual reread of all changed passages; final master contains4797lines.',
    'final_conclusion': 'All explanatory repairs, supplied constructions, assessment boundaries and added key alternatives verified. No material open finding remains.',
    'conclusion': 'No table-form or key-model mismatch. All original and supplemental findings resolved; final actual masters accepted.',
    'mechanical_receipt': identity('build/u17-paradigms-master-check.json')})
ledger['remaining_gate'] = 'No remaining paradigm/text acceptance work. Export every-page visual inspection and register integration are separate gates and are not certified by this ledger.'

diff = subprocess.check_output(['git', '-c', 'safe.directory=' + ROOT.as_posix(), 'diff', 'ed28a8e', '--',
                                'chapters/ch17/student.md', 'chapters/ch17/answer-key.md'], cwd=ROOT)
(ROOT / 'build/u17-paradigms-final-master-diff.patch').write_bytes(diff)
ledger['reviewed_final_master_diff'] = identity('build/u17-paradigms-final-master-diff.patch')
(ROOT / 'chapters/ch17/reviews/paradigms.json').write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + '\n',
                                                       encoding='utf-8', newline='\n')

md = f"""Unit 17 independent paradigm review — accepted

**The final learner and key text are accepted.** Reviewer: `unit17_paradigms`, an independent non-author. All **110 systems, 124 actual matrices and 1,234 logical cell routes** were checked against personally inspected primary evidence and independently entered expected forms. There are no form, quantity, stem, ending, header, row or route mismatches and no material open findings. The full learner and key were read; every subsequent changed passage was reread against the final actual files.

The companion JSON contains all110 per-paradigm checks and all1234 route checks, plus **{len(ledger['primary_evidence_image_inspections'])} personally viewed image-file receipts** with actual paths, raw SHA-256 values and concrete observations. The original104-image source stage and later115-image stage remain recoverable in [the source-stage JSON](../../../build/u17-paradigms-source-stage.json), [its narrative](../../../build/u17-paradigms-source-stage.md), [the pre-acceptance JSON](../../../build/u17-paradigms-preacceptance.json) and [its narrative](../../../build/u17-paradigms-preacceptance.md). This review is not a claim of blind solving: the contract exposed models. The separate blind witness was frozen at `ed28a8e` before review comparison was unlocked.

All original findings retain their details and are now resolved:

- **P17-01:** the **gecweðan** diagnostic explicitly distinguishes first/third singular **gecwæð** from second singular **gecwǣde** and plural **gecwǣdon**.
- **P17-02:** the key correctly calls the newly productive **mægen** “powers” and **cwēn** “princess” senses **taught**, while preserving the separate local hint boundary.
- **P17-03:** 39.4 is correctly explained as desired content under a verb of desire, with the selected subjunctive.
- **P17-04:** 37.8 retains the plural **spirits of the storms** as subject.
- **P17-05:** 40.6 retains singular **seat**.

The first revisions of P17-03 and P17-04 inadvertently printed the finite answers **gewilnodon** and **dōð** in task help while their forms remained independently assessed. This reviewer flagged both, and reread the final removal of those surfaces. The grammatical explanations remain correct without changing the intended assessment boundary.

**U17-A02** now supplies four constructions in five tasks: **betwēox wīfum** at40.1, **ðus cweðende** at42.5/8, **him tōgēanes** at43.13 and the contiguous model span **Gode swā gecwēme** at43.15. Actual learner help, key explanations, exact input tokens, all reference positions and supplied-only feature scope agree. All22 affected input/output tokens have direct reference routes. The current **cweðende** context is explicitly nominative masculine plural; the inherited singular source analysis is preserved as historical data. No old productive milestone or model was changed. The direct evidence and bounded source applications are recorded in [the support report](../../../build/u17-paradigms-support-review.json); [the amendment check](../../../build/u17-paradigms-amendment-check.json) passes all five task bindings.

The key's additional alternatives were verified independently. Cook §55 permits both the chosen weak **dæghwāmlīcan** and strong **dæghwāmlīcne** after the possessive in41.8; the original prompt mandates neither. Bosworth–Toller709, **nān** I(a)/(b), supports both the unchanged negative expression in43.15 and the optional **ne sīe** concord alternative.

Accepted artifact identities (raw and normalized-LF hashes are identical for both masters):

| Artifact | SHA-256 |
| --- | --- |
| student.md | `{EXPECTED[student]}` |
| answer-key.md | `{EXPECTED[key]}` |
| Contract semantic identity | `{semantic['sha256']}` |

The semantic identity uses exactly the mutable-field exclusions defined in `build/accept_unit17_text.py`; that coordinator helper was read, never executed by this reviewer. The final actual-display receipt is [here](../../../build/u17-paradigms-master-check.json), and the reread master diff is [here](../../../build/u17-paradigms-final-master-diff.patch). Rendered-page inspection and active-register integration remain separate gates.
"""
(ROOT / 'chapters/ch17/reviews/paradigms.md').write_text(md, encoding='utf-8', newline='\n')
print(json.dumps({'status': ledger['status'], 'reviewer': ledger['reviewer'], 'counts': ledger['counts'],
                  'accepted_artifact_identities': ledger['accepted_artifact_identities'],
                  'contract_semantic_sha256': semantic['sha256']}, ensure_ascii=False))
