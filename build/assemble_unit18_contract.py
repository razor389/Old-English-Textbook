"""Reconcile this unit's audited proposal into the canonical contract before prose."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def read(path): return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))
def identity(path):
    raw=(ROOT/path).read_bytes()
    return {'path':str(path).replace('\\','/'),'sha256':hashlib.sha256(raw).hexdigest(),
            'sha256_normalized_lf':hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest()}
def write(path,data):
    destination=ROOT/path;destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

ap=argparse.ArgumentParser(__doc__);ap.add_argument('--candidate',action='store_true');args=ap.parse_args()
assert not (ROOT/'chapters/ch18/student.md').exists(), 'Contract must precede learner prose'
assert not (ROOT/'chapters/ch18/answer-key.md').exists(), 'Contract must precede key prose'
b=read('build/unit18-prior-baseline.json')
assert b['git_checkpoint_full']=='0eda27783a3830fbd10bebef3702e27c15ff837c'
assert len(b['files']) == 3290
inv=read('curriculum/proposals/unit18/inventory.json')
tasks=read('curriculum/proposals/unit18/task-plan.json')['tasks']
displays=read('curriculum/proposals/unit18/display-matrices.json')
texts=read('curriculum/proposals/unit18/compositions.json')
validation=read('curriculum/proposals/unit18/validation.json')
reconciliation=({'status':'candidate_only','decisions':['Preflight only; prose not authorized.']}
                if args.candidate else read('sources/audits/unit18-coordinator/reconciliation.json'))
if not args.candidate:
    assert reconciliation['status']=='accepted_for_contract'
    assert validation['status'] in ['pass','passed','accepted','ready_for_contract']
    assert not validation.get('issues'),validation.get('issues')
    assert all(t['dependency_status']=='closed' for t in tasks)
    assert inv['lexical_frames'] and inv['principal_parts']
prior=[read(f'chapters/ch{n:02d}/coverage.json') for n in range(1,18)]
old_ids={t['task_id'] for c in prior for t in c['assigned_items'] if t['task_id'].startswith('EX-')}
new_ids={t['task_id'] for t in tasks if t['task_id'].startswith('EX-')}
assert len(old_ids)==597 and len(new_ids)==47 and not old_ids&new_ids
all_ids=old_ids|new_ids
deferred=[d for d in prior[0]['deferred_source_items'] if d.get('source_item_id','').startswith('EX-') and d['source_item_id'] not in all_ids]
assert len(deferred)==len({d['source_item_id'] for d in deferred})==0
assert len(all_ids|{d['source_item_id'] for d in deferred})==644
prompts={r['source_item_id']:r['prompt'] for r in read('sources/audits/unit18-source/exercises-prompts.json')['items']}
assert {t['task_id']:t['prompt'] for t in tasks if t['task_id'] in new_ids}==prompts
assert len(tasks)==len({t['task_id'] for t in tasks})
assert len(texts['teaching_examples'])==2
assert [r['word_count'] for r in inv['readings']]==[226]
assert sum(len(r['original_notes']) for r in inv['readings'])==22
assert sum(len(r['original_note_anchors']) for r in inv['readings'])==29
inputs=['curriculum/UNIT_18_BRIEF.md']
for folder in ['sources/audits/unit18-source','sources/audits/unit18-grammar',
               'sources/audits/unit18-coordinator','curriculum/proposals/unit18']:
    inputs.extend(p.relative_to(ROOT).as_posix() for p in sorted((ROOT/folder).iterdir()) if p.suffix in ['.json','.md','.txt','.py'])
evidence=inv['evidence_catalog']
if isinstance(evidence,list):evidence={r['evidence_id']:{k:v for k,v in r.items() if k!='evidence_id'} for r in evidence}
c = {'schema_version': 2, 'chapter_id': 'ch18', 'title': 'Independent prose consolidation', 'status': 'candidate_not_authorized' if args.candidate else 'contracted_before_prose', 'contract_date': '2026-10-28', 'contract_prepared_before_prose': True, 'prerequisite_chapters': [f'ch{n:02d}' for n in range(1, 18)], 'prior_checkpoint': b['git_checkpoint_full'][:7], 'prior_teaching_boundary': 'Only the seventeen active contracts and actual registers at 0eda277 establish teaching. Recognition and supplied exposure remain distinct from production.', 'prior_files': b['files'], 'prior_files_lf_sha256': b['files_lf_sha256'], 'prior_state_record': identity('sources/audits/unit18-coordinator/prior-state.json'), 'brief': 'curriculum/UNIT_18_BRIEF.md', 'productive_outcomes': inv['productive_outcomes'], 'recognition_outcomes': inv['recognition_outcomes'], 'bounded_scope': inv['bounded_scope'], 'explicit_scope_metrics': inv['counts'], 'audited_inflection_rules': inv['audited_inflection_rules'], 'audit_recommendation_precedence': 'This reconciled contract assigns teaching. Audit proposals supply evidence; complete morphology does not establish every sense or construction.', 'display_plan': displays, 'source_assignment_policy': {'canonical_crosswalk': 'Assigned/deferred/excluded records across active contracts; planning does not create new assignments.', 'carry_forward_contracts': [identity(f'chapters/ch{n:02d}/coverage.json') for n in range(1, 18)], 'numbered_cook_total': 644, 'previously_assigned_cook_items': 597, 'new_cook_assignments': sorted(new_ids), 'cumulative_assigned_cook_items': 644, 'still_deferred_cook_items': 0, 'new_exclusions': [], 'resolved_prior_deferral_ids': sorted(new_ids), 'note': 'All 47 exact joint XII, XIII Exercises 44–48 prompts retain the complete Joseph composition sequence and every original aid/control. The exact226-word gifts-and-farewell episode at175.18–177.2 is complete, with22 original notes and29 anchors; Apollonius as Teacher remains unassigned. All644 numbered Cook items are now assigned across active contracts.'}, 'assigned_items': tasks, 'key_item_ids': [t['key_id'] for t in tasks], 'deferred_source_items': deferred, 'excluded_source_items': [], 'source_alias_assignments': [], 'source_spans': inv['readings'], 'paradigms': inv['paradigms'], 'teaching_records': inv['teaching_records'], 'new_material_examples': texts['teaching_examples'], 'new_compositions': [], 'lexical_inventory': inv['lemmas'], 'grammar_inventory': inv['features'], 'prior_requirements': inv['prior_requirements'], 'evidence_catalog': evidence, 'analysis_inputs': [identity(p) for p in inputs], 'pre_key_review_exclusions': inv['pre_key_review_exclusions'], 'authoring_rules': ['Preserve all 47 Cook prompts, hints, references, lexical, number and order controls with original joint group/exercise/item IDs. Modern directions/help stay separate.', 'Print every introduced complete system with governing endings, stems, alternations, exceptions and sense/number limits. Any prior complete model must have an exact visible teaching and derivation route.', 'Teach every independently required form, sense and construction before first use; keep supplied support visible at the task. Prior exposure alone does not establish production.', 'Retain the exact 226-word reading, 22 original notes and 29 anchors. Preserve uncertainty, negation, source-specific constructions and quotation punctuation; explain them without silent normalization.', 'Two translated examples and the contracted original tasks are new teaching material; no additional narrative is composed. Source questions become tasks only when explicitly assigned.', 'Provide a separate key for every requested output with model, target, essential meaning, explanation, defensible alternatives and useful diagnosis. Distinguish valid language from a stated target.', 'A fresh non-author freezes every actual solution in Git before explicit key/current-contract/audit/model access. A separate fresh reviewer checks complete paradigms against primary evidence.', 'Resolve material findings, export complete learner/key PDFs, check full content parity and obtain non-author inspection of every final page. Preserve prior artifacts and records, update indexes, export Beads and commit locally. Do not begin an unrequested unit or supplement.'], 'issues': {k: 'oec-u18' + ('' if k == 'epic' else '-' + k) for k in ['epic', 'source', 'grammar', 'design', 'contract', 'draft', 'review', 'paradigms', 'typeset', 'finish']}, 'review_status': 'not_yet_drafted', 'amendments': [], 'validation_at_contract': validation, 'completion': {'complete': False, 'registers_integrated': False, 'pdfs_inspected': False}, 'review_independence_protocol': read('sources/audits/unit18-coordinator/review-independence.json'), 'contract_reconciliation_notes': reconciliation['decisions']}
for field in ['form_identity_reconciliation','source_proposal_identity_reconciliation','promotions','lexical_frames','principal_parts',
              'pronoun_family_dispositions','teaching_order_rule','study_sequence','source_task_crosswalk',
              'record_counts_by_scope','record_identity_counts','review_independence']:
    if field in inv:c[field]=inv[field]
dc=displays['counts']
c['contract_metrics']={
    'tasks':len(tasks),'cook_items':47,'original_tasks':len(tasks)-47,
    'paradigms':len(c['paradigms']),'matrices':len(displays['matrices']),
    **{k:dc[k] for k in ['logical_cells','literal_form_cells','unassigned_table_slots','component_form_occurrences','literal_routes','derived_cells']},
    'new_examples':2,'source_words':[226],'source_notes':22,'source_note_anchors':29,
    'requested_output_positions':sum(len(t['output_positions']) for t in tasks),
    'morphology_output_positions':validation['counts']['morphology_output_positions'],
    'single_cell_form_output_positions':sum(p['kind']=='form' for t in tasks for p in t['output_positions'])}
path='build/unit18-coverage-candidate.json' if args.candidate else 'chapters/ch18/coverage.json'
write(path,c)
print(path,json.dumps(c['contract_metrics'],ensure_ascii=False))
