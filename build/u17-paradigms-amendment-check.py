"""Independent bounded checks of actual U17-A02 contract bindings; no acceptance."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))

def identity(path):
    raw = (ROOT / path).read_bytes()
    return {'path': path, 'raw_sha256': hashlib.sha256(raw).hexdigest(),
            'normalized_lf_sha256': hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest()}

c = read('chapters/ch17/coverage.json')
spec = read('chapters/ch17/support-amendment-spec.json')
history = read('chapters/ch17/support-amendment-history.json')
base_raw = subprocess.check_output(['git', '-c', 'safe.directory=' + ROOT.as_posix(),
                                    'show', 'ed28a8e:chapters/ch17/coverage.json'], cwd=ROOT)
base = json.loads(base_raw.decode('utf-8-sig'))
models = read('curriculum/proposals/unit17/author-only-cook-sequence-bindings.json')
model_by_task = {x['owner_id']: x for x in models['sequences']}
tasks = {t['task_id']: t for t in c['assigned_items']}
base_tasks = {t['task_id']: t for t in base['assigned_items']}
features = {f['feature_id']: f for f in c['grammar_inventory']}
teachings = {t['teaching_id']: t for t in c['teaching_records']}
findings = []

def check(condition, message, **context):
    if not condition:
        findings.append({'problem': message, **context})
    return condition

check(c['paradigms'] == base['paradigms'], 'Paradigm content changed')
check(c['display_plan'] == base['display_plan'], 'Display plan changed')
check(c['lexical_inventory'] == base['lexical_inventory'], 'Lexical teaching inventory changed')
check(c['prior_requirements'] == base['prior_requirements'], 'Prior requirements changed')
check(len(c['paradigms']) == 110 and sum(len(p['cells']) for p in c['paradigms']) == 1234,
      'Canonical system or cell count changed')
check(len(c['display_plan']['matrices']) == 124, 'Display matrix count changed')
check(len(features) == 64 and len(teachings) == 420, 'Amended feature/teaching count mismatch')

for task_id, task in tasks.items():
    original = base_tasks[task_id]
    for field in ['prompt', 'source_control_records', 'source_instructions']:
        check(task.get(field) == original.get(field), 'Original learner instruction changed',
              task_id=task_id, field=field)

rows = []
for rule in spec['constructions']:
    feature = features[rule['feature_id']]
    teaching = teachings[rule['teaching_id']]
    check(feature['knowledge_status'] == teaching['knowledge_status'] == 'supplied',
          'New construction is not confined to supplied scope', feature_id=rule['feature_id'])
    check(feature['assessed_in'] == [], 'New construction independently assessed', feature_id=rule['feature_id'])
    check(feature['exact_span'] == teaching['support_span'] == rule['text'],
          'Whole phrase differs across feature and teaching records', feature_id=rule['feature_id'])
    for task_id in rule['task_ids']:
        task = tasks[task_id]
        original = history['original_tasks'][task_id]
        check(original == base_tasks[task_id], 'Amendment history differs from frozen original task', task_id=task_id)
        supports = [s for s in task['local_support'] if s.get('feature_id') == rule['feature_id']]
        check(len(supports) == 1, 'Missing or duplicate new support', task_id=task_id)
        support = supports[0]
        positions = support['output_token_positions_one_based']
        canonical = task['assessed_output_tokens']
        model = model_by_task[task_id]
        signature = lambda xs: [(x['literal'], x['surface'], x['form_id'], x['sense_id']) for x in xs]
        check(signature(canonical) == signature(model['tokens']), 'Model surface or lexical identity changed', task_id=task_id)
        check(support['exact_help_text'] == rule['text'], 'Local phrase differs from specification', task_id=task_id)
        check(support['visible_before_and_during_task'] and not support['independent_recall_assessment'],
              'Support visibility or recall boundary incorrect', task_id=task_id)
        sequence = next(x for x in task['input_sequences'] if x['sequence_id'] == support['support_id'])
        check(sequence['text'] == rule['text'], 'Input text differs from supplied phrase', task_id=task_id)
        check([x['source_output_position_one_based'] for x in sequence['tokens']] == positions,
              'Supplied token routing incomplete', task_id=task_id)
        check(len(sequence['tokens']) == len(positions), 'Supplied token count mismatch', task_id=task_id)
        check(rule['feature_id'] in task['supplied_feature_ids'] and rule['feature_id'] not in task['tested_feature_ids'],
              'Task feature scope mismatch', task_id=task_id)
        output = task['output_positions'][0]
        check(set(positions) <= set(output['reference_output_positions'])
              and set(positions) <= set(output['reference_sense_output_positions']),
              'Whole phrase is not reference-only in the output', task_id=task_id)
        token_rows = []
        for position, incoming in zip(positions, sequence['tokens']):
            outgoing = canonical[position - 1]
            check(outgoing['token_index'] == position, 'Canonical token index mismatch', task_id=task_id, position=position)
            check((incoming['surface'], incoming['form_id'], incoming['sense_id']) ==
                  (outgoing['surface'], outgoing['form_id'], outgoing['sense_id']),
                  'Input/output lexical identity mismatch', task_id=task_id, position=position)
            for direction, token in [('input', incoming), ('output', outgoing)]:
                check(token['form_assessment_role'] == token['sense_assessment_role'] == 'visible_reference_position'
                      and token['independent_recall_assessment'] is False,
                      'Supplied token treated as independent recall', task_id=task_id, position=position, direction=direction)
                check(token['local_support_id'] == support['support_id'],
                      'Missing canonical local-support route', task_id=task_id, position=position, direction=direction)
                if token['surface'] == 'cweðende':
                    context = token['contextual_analysis']
                    check(context.get('number') in ['pl', 'plural'] and context.get('case') in ['nom', 'nominative']
                          and context.get('gender') in ['m', 'masculine'],
                          'Current accompanying participle lacks explicit plural contextual analysis; inherited source analysis is singular',
                          task_id=task_id, position=position, direction=direction)
            token_rows.append({
                'position': position, 'surface': outgoing['surface'], 'form_id': outgoing['form_id'],
                'sense_id': outgoing['sense_id'], 'contextual_analysis': outgoing['contextual_analysis'],
                'input_and_output_reference_only': incoming['independent_recall_assessment'] is False
                                                  and outgoing['independent_recall_assessment'] is False,
                'local_support_id': outgoing['local_support_id']})
        rows.append({'task_id': task_id, 'feature_id': rule['feature_id'], 'support_id': support['support_id'],
                     'exact_phrase': rule['text'], 'positions': positions, 'token_checks': token_rows,
                     'unchanged_model_text': model['text'], 'source_prompt_and_controls_preserved': True})

for key in ['U17P-FB184', 'U17P-FB186', 'U17P-FB195']:
    evidence = c['evidence_catalog'][key]
    check(identity(evidence['image_path'])['raw_sha256'] == evidence['image_sha256'],
          'Direct source image identity changed', evidence_id=key)

report = {
    'reviewer': 'unit17_paradigms',
    'status': 'contract_amendment_checks_passed' if not findings else 'contract_amendment_metadata_repair_pending',
    'amendment_id': 'U17-A02',
    'reviewed_contract_identity': identity('chapters/ch17/coverage.json'),
    'reviewed_specification_identity': identity('chapters/ch17/support-amendment-spec.json'),
    'reviewed_history_identity': identity('chapters/ch17/support-amendment-history.json'),
    'base_checkpoint': 'ed28a8e',
    'base_contract_raw_sha256': hashlib.sha256(base_raw).hexdigest(),
    'system_cell_and_matrix_content_preserved': c['paradigms'] == base['paradigms'] and c['display_plan'] == base['display_plan'],
    'prior_teaching_and_lexical_inventory_preserved': c['lexical_inventory'] == base['lexical_inventory'] and c['prior_requirements'] == base['prior_requirements'],
    'source_evidence_review': 'build/u17-paradigms-support-review.json',
    'task_binding_checks': rows,
    'findings': findings,
    'acceptance_limit': 'This checks the actual amended contract. Final learner/key acceptance still requires the coordinator final-master-ready message and actual repaired-master reread.'
}
(ROOT / 'build/u17-paradigms-amendment-check.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n',
                                                           encoding='utf-8', newline='\n')
print(json.dumps({'status': report['status'], 'task_bindings_checked': len(rows), 'findings': findings}, ensure_ascii=False))
