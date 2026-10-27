"""Close the reconciled Unit16 design proposal; seal only current audited inputs."""
import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'curriculum/proposals/unit16'
args = argparse.ArgumentParser()
args.add_argument('--seal', action='store_true')
args = args.parse_args()

def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))

def write(name, value):
    (DEST / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def identity(path):
    p = ROOT / path
    return {'path': str(path).replace('\\', '/'), 'bytes': p.stat().st_size,
            'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

validation = read('curriculum/proposals/unit16/validation.json')
assert validation['issues'] == [], validation['issues']
expected = {'tasks': 76, 'cook_items': 59, 'original_tasks': 17,
            'requested_output_positions': 179, 'morphology_output_positions': 56,
            'morphology_single_form_positions': 45, 'morphology_phrase_positions': 3,
            'morphology_explanation_positions': 8, 'morphology_old_english_positions': 48,
            'morphology_form_tokens': 51, 'paradigms': 56, 'paradigm_cells': 564,
            'source_words': 444, 'source_notes': 54, 'source_note_anchors': 59,
            'examples': 4, 'cook_model_tokens': 812}
assert all(validation['counts'][key] == value for key, value in expected.items())
inv = read('curriculum/proposals/unit16/inventory.json')
plan = read('curriculum/proposals/unit16/task-plan.json')
models = read('curriculum/proposals/unit16/author-only-output-models.json')
requested = [p['output_position_id'] for t in plan['tasks'] for p in t['output_positions']]
targets = [p['output_position_id'] for t in models['tasks'] for p in t['outputs']]
assert len(set(requested)) == len(requested) == 179
assert set(requested) == set(targets) and len(targets) == 179
assert len(plan['tasks']) == 76
for task in plan['tasks']:
    for position in task['output_positions']:
        if position['kind'] == 'form':
            assert position['paradigm_id'] and position['cell_id'] and position['display_routes']
    task['dependency_status'] = 'closed'
    task['dependency_closure_basis'] = 'Exact prior records or explicit current teaching, recognition, and local supplied support are reconciled; every requested position has a private reviewable target.'
assert len(plan['tasks'][0]['tested_form_ids']) == 12, 'F01 must retain independent inflection production.'
features = {f['feature_id']: f for f in inv['features']}
assert 'natural gender' in features['U16-CSUP-12-FRAME']['actual_supplied_text']
reading = inv['readings'][0]
assert len(reading['tokens']) == 444
assert reading['tokens'][322]['sense_id'] == 'haelu-u11-source', 'T323 safety/rescue is supplied, not prior salvation production.'
assert reading['tokens'][210]['sense_id'] == 'on-u16-at-work', 'T211 continues on ðǣm plegan across the editorial line boundary.'
assert len(reading['original_notes']) == 54 and len(reading['original_note_anchors']) == 59
assert all(reading['tokens'][n]['surface'] == t['surface'] and
           reading['tokens'][n]['sense_id'] == t['sense_id'] for n, t in enumerate(
               read('sources/audits/unit16-source/reading-token-ledger.json')['tokens']))
assert read('curriculum/proposals/unit16/sequence-binding-validation.json')['errors'] == []
for path, expected_hash in inv['analysis_input_hashes'].items():
    assert identity(path)['sha256'] == expected_hash, path

status = 'reconciled_ready_for_contract'
plan['status'] = status
inv['status'] = status
inv['unresolved_integration'] = {'issues': []}
inv['dependency_closure'] = {'status': 'closed', 'tasks': 76, 'unresolved': [],
    'scope': 'A reconciled proposal for coordinator acceptance; chapter prose, independent learner/key review, export inspection and register integration remain later gates.'}
validation['status'] = 'ready_for_contract'
validation['dependency_status'] = 'closed'
validation['scope_counts'] = {
    'forms': dict(Counter(f['knowledge_status'] for l in inv['lemmas'] for f in l['forms'])),
    'senses': dict(Counter(s['knowledge_status'] for l in inv['lemmas'] for s in l['senses'])),
    'features': dict(Counter(f['knowledge_status'] for f in inv['features'])),
    'explicit_promotions': len(inv['promotions'])}
validation['assessment_scope_reconciliation'] = {
    'rule': 'Supplied form and sense scopes are independent. A supplied citation form does not supply its whole productive sense; a supplied sense does not supply other uses of its form.',
    'cook_role_only_repairs': ['EX-XII-XIII-33-03:T15', 'EX-XII-XIII-33-10:T06', 'EX-XII-XIII-34-07:T18', 'EX-XII-XIII-36-02:T05'],
    'cook_linguistic_bindings_changed': False,
    'original_form_tasks': 'Productive inflections remain independent; answers identical to provided dictionary forms retain their reference role.'}
for name, data in [('inventory.json', inv), ('task-plan.json', plan), ('validation.json', validation)]:
    write(name, data)
for name in ['display-matrices.json', 'compositions.json', 'outcomes.json']:
    data = read('curriculum/proposals/unit16/' + name)
    data['status'] = status
    for example in data.get('teaching_examples', []):
        example['status'] = 'reconciled_exact_tokens_bound'
    write(name, data)
# The inventory embeds the same four accepted teaching examples.
inv['new_material_examples'] = read('curriculum/proposals/unit16/compositions.json')['teaching_examples']
write('inventory.json', inv)

if args.seal:
    source_manifest_path = 'sources/audits/unit16-source/artifact-manifest.json'
    grammar_manifest_path = 'sources/audits/unit16-grammar/manifest.json'
    source_manifest = read(source_manifest_path)
    grammar_manifest = read(grammar_manifest_path)
    assert source_manifest['status'].startswith('sealed')
    assert grammar_manifest['status'].startswith('sealed')
    assert read('sources/audits/unit16-source/validation.json')['errors'] == []
    assert not grammar_manifest.get('remaining_material_blockers')
    for item in source_manifest['artifacts'] + grammar_manifest['files'] + grammar_manifest['external_reconciled_inputs']:
        assert identity(item['path'])['sha256'] == item['sha256'], item['path']
    operative = {
        'inventory.json', 'task-plan.json', 'display-matrices.json', 'compositions.json',
        'author-only-output-models.json', 'author-only-cook-sequence-bindings.json',
        'author-only-original-sequence-bindings.json', 'reading-token-bindings.json',
        'validation.json', 'outcomes.json', 'source-task-crosswalk.json', 'prior-audit.json',
        'sequence-binding-validation.json', 'design-audit-report.md', 'reading-sense-reconciliation.json'}
    artifacts = []
    for p in sorted(DEST.iterdir()):
        if p.is_file() and p.name != 'artifact-manifest.json':
            item = identity(p.relative_to(ROOT))
            item['role'] = 'operative reconciled proposal' if p.name in operative else 'retained derivation, seed, or independent audit provenance; not an alternative assignment contract'
            artifacts.append(item)
    input_paths = sorted(set(inv['analysis_input_hashes']) | {
        source_manifest_path, grammar_manifest_path,
        'sources/audits/unit16-source/reading-token-ledger.json',
        'sources/audits/unit16-source/exercises-dependencies.json',
        'sources/audits/unit16-source/evidence-catalog.json',
        'sources/audits/unit16-grammar/exercises-verbal-dependencies.json',
        'sources/audits/unit16-grammar/author-only-cook-models.json',
        'sources/audits/unit16-grammar/evidence-catalog.json',
        'sources/audits/unit16-coordinator/evidence-catalog.json',
        'sources/audits/unit16-coordinator/reward-correction.json',
        'lexicon/entries.json', 'curriculum/grammar.json'})
    write('artifact-manifest.json', {
        'schema_version': 1, 'chapter': 'ch16', 'packet': 'unit16-design',
        'status': 'sealed_reconciled_design_proposal',
        'sealed_at_utc': datetime.now(timezone.utc).isoformat(), 'baseline_commit': 'e1d94be',
        'counts': validation['counts'], 'scope_counts': validation['scope_counts'],
        'artifacts': artifacts, 'reconciled_inputs': [identity(p) for p in input_paths],
        'remaining_material_blockers': [],
        'scope_limit': 'The coordinator must accept and commit the canonical contract before prose. This seal does not certify the unwritten chapter, independent review, export, or register integration.'})
print(json.dumps({'status': 'sealed_reconciled_design_proposal' if args.seal else status,
                  'tasks_closed': 76, 'counts': validation['counts'], 'scope_counts': validation['scope_counts']}, ensure_ascii=False))
