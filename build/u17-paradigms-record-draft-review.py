"""Record completed independent draft review, without accepting pending repairs."""
from pathlib import Path
import copy
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))

def identity(path):
    data = (ROOT / path).read_bytes()
    return {'path': path, 'raw_sha256': hashlib.sha256(data).hexdigest(),
            'normalized_lf_sha256': hashlib.sha256(data.replace(b'\r\n', b'\n').replace(b'\r', b'\n')).hexdigest()}

source = read('build/u17-paradigms-source-stage.json')
receipt = read('build/u17-paradigms-master-check.json')
assert receipt['counts'] == {'actual_matrices': 124, 'expected_matrices': 124,
                              'logical_cells': 1234, 'mismatches': 0}
assert not receipt['findings']
for item in receipt['artifact_identities']:
    assert identity(item['path']) == item

findings = [
    {
        'finding_id': 'P17-01', 'status': 'open', 'severity': 'material',
        'path': 'chapters/ch17/student.md', 'line_at_review': 1544,
        'paradigm_ids': ['u17-gecwethan-indicative12'],
        'observed': 'The preterite contrasts singular æ with ǣ in the second singular and plural, and changes ð to d.',
        'problem': 'The unqualified ð-to-d statement incorrectly suggests that the whole preterite changes consonant. First/third singular gecwæð retains ð; second singular gecwǣde and plural gecwǣdon have d.',
        'requested_repair': 'State the first/third singular æ/ð versus second singular and plural ǣ/d distribution explicitly.',
        'evidence': ['sources/audits/unit17-source/fb-p63.png'],
        'rationale': 'Cook §106 witnesses cwæð versus cwǣdon; the second singular uses the plural stem. Actual table cells are correct.',
        'contract_check': 'The canonical diagnostic says grammatical ð/d alternation and does not claim uniform replacement; no contract amendment is needed.',
        'coordinator_disposition': 'Agreed; repair held until the blind witness is frozen.'
    },
    {
        'finding_id': 'P17-02', 'status': 'open', 'severity': 'material',
        'path': 'chapters/ch17/answer-key.md', 'lines_at_review': [399, 1209],
        'paradigm_ids': ['NEW-U17-NOM-MAEGEN', 'NEW-U17-NOM-CWEN'],
        'observed': ['explicitly supplied sense “powers”', 'specifically supplied princess sense'],
        'problem': 'The key labels the newly productive mægen power and cwēn princess senses as supplied, obscuring their explicit teaching status.',
        'requested_repair': 'Use taught for both sense labels. Preserve the separate fact that the original 37.2 hint supplies its lexical meaning locally, so that item does not independently assess hinted sense recall.',
        'evidence': ['chapters/ch17/coverage.json', 'chapters/ch17/student.md:535', 'chapters/ch17/student.md:775'],
        'rationale': 'maegen-u17-power and cwen-u17-princess are new_production in the frozen teaching contract, and both are explicitly taught in the learner master.',
        'coordinator_disposition': 'Agreed with the distinction between global teaching and the local original hint; repair held until the blind witness is frozen.'
    },
    {
        'finding_id': 'P17-03', 'status': 'open', 'severity': 'material',
        'path': 'chapters/ch17/student.md', 'line_at_review': 3291,
        'paradigm_ids': [],
        'observed': 'The bracket replaces the infinitive “to see” with a purpose clause, “that they might see”.',
        'problem': 'Cook 39.4 has a desired-content/object clause governed by gewilnodon. Calling it a purpose clause misidentifies its relationship to the matrix verb.',
        'requested_repair': 'Call it a finite content clause expressing what they desired. Retain the appropriate subjunctive.',
        'evidence': ['sources/audits/unit17-source/fb-p104.png', 'chapters/ch17/answer-key.md:717'],
        'rationale': 'Cook §194(b) treats a clause dependent on willing or desire as an object/content clause. The key already explains the model correctly.',
        'coordinator_disposition': 'Agreed; repair held until the blind witness is frozen.'
    },
    {
        'finding_id': 'P17-04', 'status': 'open', 'severity': 'material',
        'path': 'chapters/ch17/student.md', 'line_at_review': 2875,
        'paradigm_ids': [],
        'observed': 'The storm fulfils his word.',
        'problem': 'The original 37.8 prompt has plural spirits of the storms as actor, requiring the plural dōð shown in the correct key.',
        'requested_repair': 'The spirits of the storms fulfil his word.',
        'evidence': ['sources/audits/unit17-source/ex-p22.png', 'chapters/ch17/answer-key.md:471'],
        'rationale': 'The learner help must preserve the prompt subject and number rather than substituting singular storm.',
        'coordinator_disposition': 'Agreed; repair held until the blind witness is frozen.'
    },
    {
        'finding_id': 'P17-05', 'status': 'open', 'severity': 'minor',
        'path': 'chapters/ch17/student.md', 'line_at_review': 3459,
        'paradigm_ids': [],
        'observed': 'Omit the marked their without deleting the seats.',
        'problem': 'The original 40.6 prompt has singular seat, and the correct model uses dative singular of setle.',
        'requested_repair': 'Change seats to seat.',
        'evidence': ['sources/audits/unit17-source/ex-p25.png', 'chapters/ch17/answer-key.md:823'],
        'rationale': 'The construction help should not suggest changing the number of the retained noun.',
        'coordinator_disposition': 'Reported to the coordinator for the same post-freeze repair batch.'
    }
]

review = copy.deepcopy(source)
review['status'] = 'actual_masters_checked_pending_prose_repairs'
review['independence'].update({
    'student_master_opened': True, 'answer_key_opened': True,
    'final_review_coordinator_unlock_received': True,
    'completed_drafts_checkpoint': '259b14f',
    'blind_witness_consulted': False,
    'findings_not_disclosed_to_blind_solver': True
})
review['source_stage_history'] = [identity('build/u17-paradigms-source-stage.json'),
                                 identity('build/u17-paradigms-source-stage.md')]
review['reviewed_master_artifact_identities_before_repairs'] = receipt['artifact_identities']
review['reviewed_contract_semantic_identity_before_repairs'] = receipt['contract_semantic_identity']
review['actual_matrix_checks'] = receipt['matrix_checks']
actual_routes = {(r['paradigm_id'], r['logical_cell_id']): r for r in receipt['cell_checks']}
for row in review['cell_route_checks']:
    actual = actual_routes[row['paradigm_id'], row['logical_cell_id']]
    row.update({
        'status': 'actual_form_verified_pending_final_acceptance',
        'learner_master_checked': True,
        'actual_surface': actual['actual_surface'],
        'student_line_at_review': actual['student_line'],
        'actual_column_label': actual['actual_column_label'],
        'actual_row_label': actual['actual_row_label'],
        'actual_route_mismatches': actual['issues']
    })
for row in review['paradigm_checks']:
    row['status'] = 'actual_forms_checked_pending_prose_repairs'
    row['learner_master_checked'] = True
    row['answer_key_uses_checked'] = True
    row['open_findings'] = [f['finding_id'] for f in findings if row['paradigm_id'] in f['paradigm_ids']]
    row['actual_display_check'] = 'All logical cells personally source-derived and compared with the actual Markdown table surfaces, row labels and column labels; no cell or route mismatch.'
review['manual_master_review'] = {
    'student_lines_reviewed': '1–4791, complete master; all table cells additionally checked by independent source-derived comparison',
    'answer_key_lines_reviewed': 'complete master, including every model, target, analysis and reading answer',
    'coverage': ['diagnostic stems and endings', 'quantity and spelling', 'important exceptions',
                 'teaching and reference scope', 'sense status', 'ordinary lexical frames',
                 'local construction help', 'all answer-key uses', 'reading morphology and explanations'],
    'conclusion': 'No table-form or key-model mismatch. Five explanatory wording findings remain open; none requires a change to the frozen paradigm cells, assignments or model answers.',
    'mechanical_receipt': identity('build/u17-paradigms-master-check.json')
}
review['counts'].update({'actual_matrices_checked': 124, 'actual_routes_checked': 1234,
                         'actual_table_mismatches': 0, 'open_findings': len(findings),
                         'material_open_findings': 4})
review['findings'] = findings
review['material_open_findings'] = 4
review['accepted_artifact_identities'] = []
review['accepted_contract_semantic_identity'] = None
review['remaining_gate'] = 'Coordinator is holding author edits until the independent blind witness is frozen. After author repairs, reread every changed passage, recheck actual table routes and identities, and resolve all five findings before acceptance. Export inspection remains separate.'
(ROOT / 'chapters/ch17/reviews/paradigms.json').write_text(
    json.dumps(review, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')

md = """Unit 17 independent paradigm review — actual masters checked; repairs pending

**Acceptance is pending five verified wording repairs.** Reviewer: `unit17_paradigms`. The coordinator explicitly unlocked completed learner and key drafts at `259b14f` under `oec-u17-paradigms`. This reviewer has no current author role and is not the blind solver. The independent blind witness has not been consulted, and these findings have not been disclosed to that reviewer before their unlock.

All 110 systems, 124 actual Markdown matrices and 1,234 logical cell routes were checked against independently source-derived forms. Every actual surface, header and row agrees; there are no cell, stem, quantity, ending or route mismatches. The learner master was read completely, including every diagnostic rule, scope statement, exercise help and reading note. All key models and analyses were read. Correct table cells do not excuse the explanatory findings below.

The source stage's 104 personally viewed page-image receipts, concrete observations, source hashes, prior-contract reads and register checks remain in the companion JSON. The original source-stage records are preserved unchanged in [the JSON snapshot](../../../build/u17-paradigms-source-stage.json) and [the narrative snapshot](../../../build/u17-paradigms-source-stage.md). Their original no-master-access status describes that earlier stage only. The actual matrix comparison receipt is [u17-paradigms-master-check.json](../../../build/u17-paradigms-master-check.json).

The pending findings are:

1. **P17-01 — material:** learner line 1544 overgeneralizes **gecweðan**'s preterite **ð/d** alternation. State explicitly that first/third singular **gecwæð** retains **æ/ð**, while second singular **gecwǣde** and plural **gecwǣdon** have **ǣ/d**. Cook §106 on printed page 63 supplies the distinction. The actual table is correct, and the canonical diagnostic's “grammatical ð/d alternation” does not make the overbroad claim.
2. **P17-02 — material:** key lines 399 and 1209 call the **mægen** “powers” and **cwēn** “princess” senses supplied. Both are explicitly taught for production; use **taught**. The original 37.2 hint still supplies its lexical meaning locally, and that task correctly does not assess independent recall of the hinted meaning. Keep the global teaching status distinct from local hint support.
3. **P17-03 — material:** learner line 3291 calls 39.4's finite desired-content clause a purpose clause. It expresses what they desired, under **gewilnodon**, as in Cook §194(b); the key already correctly describes it as content. Clarify the learner sentence while retaining the subjunctive.
4. **P17-04 — material:** learner line 2875 makes “the storm” the singular actor in 37.8. The prompt's actors are **the spirits of the storms**, and the correct key uses plural **dōð**. Preserve that plural subject in the help.
5. **P17-05 — minor:** learner line 3459 says “without deleting the seats.” The 40.6 prompt has singular **seat**, and the model correctly has **of setle**. Change **seats** to **seat**.

The coordinator agreed P17-01 through P17-04 and has P17-05 for the same repair batch. No paradigm cell, key model, assignment or contract content needs changing for these findings. Author edits are held until the blind witness is frozen. Final acceptance will identify the actual repaired master hashes and the contract semantic identity only after this reviewer rereads the repairs. Exported-page inspection remains a separate later gate.
"""
(ROOT / 'chapters/ch17/reviews/paradigms.md').write_text(md, encoding='utf-8', newline='\n')
print(json.dumps({'status': review['status'], 'systems': len(review['paradigm_checks']),
                  'cells': len(review['cell_route_checks']), 'images': len(review['primary_evidence_image_inspections']),
                  'open_findings': len(findings), 'material_open_findings': review['material_open_findings']}))
