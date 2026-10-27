import json
from pathlib import Path

p = Path('chapters/ch15/coverage.json')
c = json.loads(p.read_text(encoding='utf-8'))
labels = {
    'comparative': 'Comparative',
    'positive': 'Positive',
    'superlative': 'Superlative',
    'imperative; 2; plural': 'Imperative, 2nd plural',
    'imperative; 2; singular': 'Imperative, 2nd singular',
    'infinitive; citation': 'Infinitive (citation form)',
    'inflected infinitive; gerund; after tō': 'Inflected infinitive after tō',
    'inflected_infinitive': 'Inflected infinitive',
    'past_participle; citation_only': 'Past participle (citation form)',
    'past_participle; selected base form': 'Past participle (base form)',
    'plain_infinitive': 'Plain infinitive',
    'present_participle; selected base form': 'Present participle (base form)',
}
changes = []
for m in c['display_plan']['matrices']:
    if m['headers'][0] == 'Position':
        for i, row in enumerate(m['rows']):
            before = row[0]
            row[0] = labels[before]
            changes.append({'matrix_id': m['matrix_id'], 'row_index': i,
                            'before': before, 'after': row[0]})
c['source_spans'][2]['tokens'][157]['analysis']['source_analysis'] = 'strong dative masculine singular agreeing with ęnde'
c['lexical_inventory'][40]['forms'][0]['analysis']['source_analysis'] = 'strong dative masculine singular; agreement is identified in each reading context'
c['amendments'].append({
    'amendment_id': 'U15-AM01', 'date': '2026-10-27',
    'stage': 'authorship after contract checkpoint ff7f7c8, before complete drafts',
    'reason': 'Readable paradigm labels and correction of a copied contextual annotation.',
    'changes': changes,
    'contextual_correction': 'Prayer token 158, ǣghwilcum, agrees with ęnde, not the męnn of the Duties passage. The shared inventory analysis is made contextual-neutral. Gender, case, number, spelling, IDs, teaching scope and output routes are unchanged.',
    'source_basis': 'Cook First Book printed 163, final line of prayer; exact reading already inspected and retained in source_spans.',
    'frozen_inputs': 'Original sealed source, grammar and design packets remain unchanged; canonical amendment records the correction.',
    'review_status': 'pending_independent_review'
})
p.write_text(json.dumps(c, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
print(f'Amended {len(changes)} readable row labels and two contextual annotations.')
