"""Reconcile Unit 15 only after its independent analysis; never infer acceptance."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(path): return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))
def identity(path):
    raw=(ROOT/path).read_bytes()
    return {'path':str(path).replace('\\','/'), 'sha256':hashlib.sha256(raw).hexdigest(),
            'sha256_normalized_lf':hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest()}
def write(path,data):
    dest=ROOT/path; dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

p=argparse.ArgumentParser();p.add_argument('--candidate',action='store_true');args=p.parse_args()
assert not (ROOT/'chapters/ch15/student.md').exists(), 'Contract must precede prose'
assert not (ROOT/'chapters/ch15/answer-key.md').exists(), 'Contract must precede prose'
b=read('build/unit15-prior-baseline.json')
assert b['git_checkpoint_full']=='9129cdabd21ac9335eca531d42815a5c81ecd8a3'
assert len(b['files'])==2313 and len(b['archive_files'])==134
inv=read('curriculum/proposals/unit15/inventory.json')
tasks=read('curriculum/proposals/unit15/task-plan.json')['tasks']
displays=read('curriculum/proposals/unit15/display-matrices.json')
texts=read('curriculum/proposals/unit15/compositions.json')
validation=read('curriculum/proposals/unit15/validation.json')
reconciliation=({'status':'candidate_only','decisions':['Preflight only; no prose authorized.']}
                if args.candidate else read('sources/audits/unit15-coordinator/reconciliation.json'))
if not args.candidate:
    assert reconciliation['status']=='accepted_for_contract'
    assert validation['status'] in ['pass','passed','accepted','ready_for_contract']
    assert not validation.get('issues'),validation.get('issues')
    assert all(t['dependency_status']=='closed' for t in tasks)
    assert inv['lexical_frames'] and inv['principal_parts'] and inv['pronoun_family_dispositions']
prior=[read(f'chapters/ch{n:02d}/coverage.json') for n in range(1,15)]
old_ids={t['task_id'] for c in prior for t in c['assigned_items'] if t['task_id'].startswith('EX-')}
new_ids={t['task_id'] for t in tasks if t['task_id'].startswith('EX-')}
assert len(old_ids)==406 and len(new_ids)==50 and not old_ids&new_ids
all_ids=old_ids|new_ids
deferred=[d for d in prior[0]['deferred_source_items'] if d.get('source_item_id','').startswith('EX-') and d['source_item_id'] not in all_ids]
assert len(deferred)==len({d['source_item_id'] for d in deferred})==188
assert len(all_ids|{d['source_item_id'] for d in deferred})==644
prompts={r['source_item_id']:r['prompt'] for r in read('sources/audits/unit15-source/exercises-prompts.json')['items']}
assert {t['task_id']:t['prompt'] for t in tasks if t['task_id'] in new_ids}==prompts
assert len(tasks)==105 and len(texts['teaching_examples'])==8
assert [r['word_count'] for r in inv['readings']]==[103,152,160]
assert sum(len(r['original_notes']) for r in inv['readings'])==27
assert sum(len(r['original_note_anchors']) for r in inv['readings'])==33

inputs=['curriculum/UNIT_15_BRIEF.md']
for folder in ['sources/audits/unit15-source','sources/audits/unit15-grammar',
               'sources/audits/unit15-coordinator','curriculum/proposals/unit15']:
    inputs.extend(p.relative_to(ROOT).as_posix() for p in sorted((ROOT/folder).iterdir()) if p.suffix in ['.json','.md','.txt','.py'])
evidence=inv['evidence_catalog']
if isinstance(evidence,list):evidence={r['evidence_id']:{k:v for k,v in r.items() if k!='evidence_id'} for r in evidence}
c={
    'schema_version':2,'chapter_id':'ch15','title':'Negation, quantity and comparison in discourse',
    'status':'candidate_not_authorized' if args.candidate else 'contracted_before_prose',
    'contract_date':'2026-10-26','contract_prepared_before_prose':True,
    'prerequisite_chapters':[f'ch{n:02d}' for n in range(1,15)],
    'prior_checkpoint':b['git_checkpoint_full'][:7],
    'prior_teaching_boundary':'Only the fourteen active contracts and actual registers at 9129cda establish teaching. Recognition and supplied exposure are distinct from production; no archived milestones are inherited.',
    'prior_files':b['files'],'prior_files_lf_sha256':b['files_lf_sha256'],
    'prior_state_record':identity('sources/audits/unit15-coordinator/prior-state.json'),
    'archive_tree_sha256':hashlib.sha256(json.dumps(b['archive_files'],sort_keys=True).encode()).hexdigest(),
    'brief':'curriculum/UNIT_15_BRIEF.md','productive_outcomes':inv['productive_outcomes'],
    'recognition_outcomes':inv['recognition_outcomes'],'bounded_scope':inv['bounded_scope'],
    'explicit_scope_metrics':inv['counts'],'audited_inflection_rules':inv['audited_inflection_rules'],
    'audit_recommendation_precedence':'The reconciled contract assigns teaching. Audit proposals supply evidence; complete morphology does not establish every sense or construction.',
    'display_plan':displays,
    'source_assignment_policy':{
        'canonical_crosswalk':'Assigned/deferred/excluded records across active contracts; planning and archived evidence are not new assignments.',
        'carry_forward_contracts':[identity(f'chapters/ch{n:02d}/coverage.json') for n in range(1,15)],
        'numbered_cook_total':644,'previously_assigned_cook_items':406,
        'new_cook_assignments':sorted(new_ids),'cumulative_assigned_cook_items':456,
        'still_deferred_cook_items':188,'new_exclusions':[], 'resolved_prior_deferral_ids':sorted(new_ids),
        'note':'All 50 exact IX.28–30 and joint X,XI.31 prompts. The 103-word Duties opening argument is not the whole speech; the 152-word preface and 160-word prayer are complete as printed. All original notes remain; Duties160–161 is outside the reading assignment.'},
    'assigned_items':tasks,'key_item_ids':[t['key_id'] for t in tasks],
    'deferred_source_items':deferred,'excluded_source_items':[],'source_alias_assignments':[],
    'source_spans':inv['readings'],'paradigms':inv['paradigms'],'teaching_records':inv['teaching_records'],
    'new_material_examples':texts['teaching_examples'],'new_compositions':[],
    'lexical_inventory':inv['lemmas'],'grammar_inventory':inv['features'],
    'prior_requirements':inv['prior_requirements'],'evidence_catalog':evidence,
    'analysis_inputs':[identity(p) for p in inputs],
    'pre_key_review_exclusions':inv['pre_key_review_exclusions'],
    'authoring_rules':[
        'Preserve all original Cook words, hints, references, controls, group/exercise/item IDs and complete sets. Modern directions/help are separate.',
        'Print every complete assigned matrix literally with rules, stems, important alternatives and sense/number limits. Distinguish logical positions, actual forms, multiword construction components and explicitly unassigned slots.',
        'Teach all required independent forms, senses and uses before their first example/practice. Every supplied expression has visible support throughout its task; exposure is not unaided recall.',
        'Retain all415 exact reading words,27 original notes and33 anchors. Duties is an opening argument, not a whole speech. Source punctuation and source questions remain identifiable apparatus.',
        'Eight translated examples and55 original tasks are new teaching material. The three source passages supply the connected graded readings; no separate new narrative is assigned.',
        'Keep the answer key separate and cover every requested output with meaning, target, explanation, alternatives and useful diagnosis. Distinguish grammatical validity from a stated source target.',
        'A fresh non-author freezes all actual learner solutions in Git before explicit current-key/contract/audit/model comparison access. A separate fresh reviewer checks all complete paradigms, primary evidence and scope.',
        'Resolve material findings; export complete learner/key PDFs, check full content parity and have non-authors inspect every final page. Preserve earlier records/artifacts, update indexes, export Beads and commit locally. Do not draft Unit16.'
    ],
    'issues':{k:'oec-u15'+('' if k=='epic' else '-'+k) for k in ['epic','source','grammar','design','contract','draft','review','paradigms','typeset','finish']},
    'review_status':'not_yet_drafted','amendments':[],
    'validation_at_contract':validation,
    'completion':{'complete':False,'registers_integrated':False,'pdfs_inspected':False},
    'review_independence_protocol':read('sources/audits/unit15-coordinator/review-independence.json'),
    'contract_reconciliation_notes':reconciliation['decisions'],
}
for field in ['form_identity_reconciliation','promotions','lexical_frames','principal_parts',
              'pronoun_family_dispositions','teaching_order_rule','study_sequence','source_task_crosswalk',
              'record_counts_by_scope','record_identity_counts','review_independence']:
    c[field]=inv[field]
dc=displays['counts']
c['contract_metrics']={
    'tasks':len(tasks),'cook_items':len(new_ids),'original_tasks':len(tasks)-len(new_ids),
    'paradigms':len(c['paradigms']),'matrices':len(displays['matrices']),
    'logical_cells':dc['logical_cells'],'literal_form_cells':dc['literal_form_cells'],
    'unassigned_table_slots':dc['unassigned_table_slots'],'component_form_occurrences':dc['component_form_occurrences'],
    'literal_routes':dc['literal_routes'],'derived_cells':dc['derived_cells'],
    'new_examples':len(c['new_material_examples']),'source_words':[r['word_count'] for r in c['source_spans']],
    'source_notes':27,'source_note_anchors':33,
    'requested_output_positions':sum(len(t['output_positions']) for t in tasks),
    'morphology_output_positions':validation['counts']['morphology_output_positions']}
assert c['contract_metrics']['requested_output_positions']==322
path='build/unit15-coverage-candidate.json' if args.candidate else 'chapters/ch15/coverage.json'
write(path,c)
print(path,json.dumps(c['contract_metrics'],ensure_ascii=False))
