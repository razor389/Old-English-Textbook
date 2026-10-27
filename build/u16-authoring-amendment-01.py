"""Clarify three stale sense notes without changing the contracted teaching scope."""
import json
from pathlib import Path

path = Path('chapters/ch16/coverage.json')
c = json.loads(path.read_text(encoding='utf-8'))
assert c['contract_prepared_before_prose']
assert not any(a.get('amendment_id') == 'U16-A01' for a in c['amendments'])
senses = {s['sense_id']: s for l in c['lexical_inventory'] for s in l['senses']}
features = {f['feature_id']: f for f in c['grammar_inventory']}
changes = []
for sid, fid in [
    ('plegian-u16-play', 'u16-plegian-play'),
    ('cleopian-u16-cry', 'u16-cleopian-cry'),
    ('iernan-u16', 'u16-iernan-frame')
]:
    sense, frame = senses[sid], features[fid]
    assert sense['knowledge_status'] == frame['knowledge_status'] == 'new_production'
    before = sense['scope_note']
    assert before == 'Only the explicitly supplied contextual use; no independent recall.'
    after = 'New production within the assigned frame: ' + frame['scope_note']
    changes.append({'sense_id': sid, 'field': 'scope_note', 'before': before,
                    'after': after, 'already_contracted_frame': fid,
                    'evidence_refs': frame['evidence_refs']})
    sense['scope_note'] = after
amendment = {
    'amendment_id': 'U16-A01', 'date': '2026-10-27', 'stage': 'authoring',
    'original_contract_checkpoint': '543e214', 'coordinator': 'root',
    'reported_by': 'unit16_design',
    'reason': 'A source-only default note survived merging into three explicitly productive senses. Their existing productive statuses, frames, full verbal systems and assessed tasks establish the agreed scope; the stale notes contradicted it.',
    'changes': changes,
    'unchanged': ['All source and model text', 'All form/sense/feature identities',
                  'Knowledge statuses and productive boundaries', 'Paradigms and task targets',
                  'Sealed audit/proposal packets and initial witnesses'],
    'review_status': 'requires_independent_verification'
}
c['amendments'].append(amendment)
path.write_text(json.dumps(c, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
record = Path('chapters/ch16/authoring-amendments.json')
assert not record.exists()
record.write_text(json.dumps({'chapter_id': 'ch16', 'amendments': [amendment]},
                            ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
print('U16-A01: three contradictory scope notes aligned with their existing productive frames.')
