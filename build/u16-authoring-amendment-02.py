"""Repair current help wording while preserving sealed packets and prior histories."""
import json
from pathlib import Path

p = Path('chapters/ch16/coverage.json')
c = json.loads(p.read_text(encoding='utf-8'))
assert not any(a.get('amendment_id') == 'U16-A02' for a in c['amendments'])
changes = []
replacements = {
    'Direct object top is the actual OE object. Do not substitute the Latin shoulder/rubbing action.':
        'Direct object top is the actual Old English object. The Latin parallel describes rubbing or anointing with ointment; it contains no shoulder or neck noun. Keep that separate event distinct from the Old English.',
    'Source genitive route expression, followed by relative ðe. Compare the bounded genitive-route teaching and Cook35.3 model Gā ðæs weges ðe ðū cōme; retain this exact source phrasing with its past-time reference.':
        'Source genitive route expression, followed by relative ðe. Apply the bounded genitive-route use taught earlier in this unit, retaining this exact source phrasing and its past-time reference.'
}
def walk(value, path=''):
    if isinstance(value, dict):
        for key, child in value.items():
            if key in ['records_by_chapter', 'metadata_by_chapter', 'prior_record', 'amendments']:
                continue
            location = path + '/' + key
            if isinstance(child, str) and child in replacements:
                replacement = replacements[child]
                changes.append({'path': location, 'before': child, 'after': replacement})
                value[key] = replacement
            else:
                walk(child, location)
    elif isinstance(value, list):
        for i, child in enumerate(value): walk(child, path + '/' + str(i))
walk(c)
assert len(changes) == 7
task = next(t for t in c['assigned_items'] if t['task_id'] == 'EX-XII-XIII-35-07')
binding = next(b for support in task['local_support'] for b in support.get('bindings', []) if b['sense_id'] == 'se-relative')
old = binding['gloss']
assert old == 'which, referring to the mountains and hills'
binding['gloss'] = 'who; the one who, referring to the man'
changes.append({'task_id': task['task_id'], 'sense_id': 'se-relative', 'field': 'local_support.bindings.gloss', 'before': old, 'after': binding['gloss']})
sense = next(s for l in c['lexical_inventory'] for s in l['senses'] if s['sense_id'] == 'se-relative')
assert sense['contextual_gloss'] == old
sense['contextual_gloss'] = 'who; whom; that, referring to a person in the assigned clauses'
changes.append({'sense_id': 'se-relative', 'field': 'current contextual_gloss', 'before': old, 'after': sense['contextual_gloss']})
amendment = {
    'amendment_id': 'U16-A02', 'date': '2026-10-27', 'stage': 'authoring',
    'original_contract_checkpoint': '543e214', 'coordinator': 'root',
    'reported_by': ['root', 'unit16_design'],
    'reason': 'Remove a stale erroneous shoulder reference from local help; replace an explicit Cook35.3 answer in reading help with the already-taught route rule; make current relative-pronoun glosses fit their current personal referents rather than an earlier mountains-and-hills passage.',
    'changes': changes,
    'evidence': ['sources/audits/unit16-coordinator/primary-inspections.json',
                 'sources/audits/unit16-coordinator/evidence-catalog.json',
                 'chapters/ch08/coverage.json',
                 'sources/audits/unit16-source/exercises-prompts.json'],
    'unchanged': ['Exact source and Cook prompts', 'All model strings and target identities',
                  'Form analyses, teaching statuses, paradigms and task counts',
                  'Prior per-chapter records and original contextual glosses within them',
                  'Sealed audit/proposal packets and initial witnesses'],
    'review_status': 'requires_independent_verification'
}
c['amendments'].append(amendment)
p.write_text(json.dumps(c, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
record = Path('chapters/ch16/authoring-amendments.json')
ledger = json.loads(record.read_text(encoding='utf-8'))
ledger['amendments'].append(amendment)
record.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
print('U16-A02:', len(changes), 'current help/gloss fields clarified; historical records preserved.')
