"""Capture the actual fifteen-unit state once; never rerun after integration."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'sources/audits/unit16-coordinator'
OUT.mkdir(parents=True, exist_ok=True)
def read(path): return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))
def write(path, data):
    (ROOT / path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
def identity(path):
    raw = (ROOT / path).read_bytes()
    return hashlib.sha256(raw).hexdigest(), hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest()

destination = ROOT / 'build/unit16-prior-baseline.json'
assert not destination.exists(), 'Immutable baseline already exists'
paths = (ROOT / 'build/u16-prior-tracked-paths.txt').read_text(encoding='utf-8-sig').splitlines()
mutable = {'.beads/issues.jsonl', 'README.md', 'STATUS.md', 'docs/HANDOFF.md',
           'curriculum/COURSE_PLAN.md', 'curriculum/COOK_MAP.md', 'sources/README.md',
           'sources/registry.json', 'typesetting/README.md'}
register_paths = ['lexicon/entries.json', 'curriculum/grammar.json']

fixed = [p for p in paths if p not in mutable and (not p.startswith('.beads/'))]
hashes = {p: identity(p) for p in fixed}
lex, gram = [read(p) for p in register_paths]
expected = [f'ch{i:02d}' for i in range(1, 16)]
assert lex['reviewed_chapters'] == gram['reviewed_chapters'] == expected
contracts = []
for chapter in expected:
    path = f'chapters/{chapter}/coverage.json'
    c = read(path)
    assert c.get('completion', {}).get('complete') is True or (chapter == 'ch01' and c['status'] == 'reviewed_complete' and c['review_status'] == 'passed'), chapter
    contracts.append({
        'chapter_id': chapter, 'path': path, 'identity': identity(path), 'top_level_keys':list(c),
        'title': c.get('title', c.get('chapter_title', chapter)), 'status': c['status'],
        'productive_outcomes': c.get('productive_outcomes'),
        'recognition_outcomes': c.get('recognition_outcomes'),
        'bounded_scope': c.get('bounded_scope'),
        'assigned_items': len(c['assigned_items']),
        'new_lexical_entries': len(c.get('lexical_inventory', [])),
        'grammar_inventory': [{k: f.get(k) for k in ['feature_id', 'description', 'knowledge_status', 'scope_note']} for f in c.get('grammar_inventory', [])],
        'source_spans': [{k:s.get(k) for k in ['source_span_id','source_id','origin_category','locator','printed_pages','pdf_pages','learner_text','scope_note']} for s in c.get('source_spans', [])],
    })
counts = {'lemmas': len(lex['lemmas']), 'forms': sum(len(l['forms']) for l in lex['lemmas']),
          'senses': sum(len(l['senses']) for l in lex['lemmas']), 'features': len(gram['features'])}
assert counts == {'lemmas':955, 'forms':10470, 'senses':1207, 'features':950}
baseline = {'chapter_id': 'ch16', 'git_checkpoint_full': 'e1d94be968e89ecfc4918ed58d850702e5d0e57e', 'lexicon': lex, 'grammar': gram, 'counts': counts, 'files': {p: v[0] for p, v in hashes.items()}, 'files_lf_sha256': {p: v[1] for p, v in hashes.items()}, 'mutable_shared_indexes': sorted(mutable)}
write('build/unit16-prior-baseline.json', baseline)
retained = {k:v for k,v in baseline.items() if k not in ['lexicon','grammar']}
retained['immutable_local_snapshot'] = 'build/unit16-prior-baseline.json'
retained['snapshot_sha256'] = identity('build/unit16-prior-baseline.json')[0]
retained['method'] = 'Loaded every full active contract and both actual cumulative registers; captured every tracked fixed artifact including earlier tracked helpers. Orientation is a finding aid: exact needed senses, forms and uses must be checked in their actual records. Earlier records and source evidence remain preserved.'
write('sources/audits/unit16-coordinator/prior-state.json', retained)
write('build/u16-prior-contract-orientation.json', contracts)
pattern = re.compile(r'narrat|report|speech|quot|complement|clause|government|sequence|partici|conditional|relative|infinit|imperat|discourse|reference', re.I)
features = [f for f in gram['features'] if pattern.search(json.dumps({k:v for k,v in f.items() if k not in ['records_by_chapter','evidence_refs']},ensure_ascii=False))]
write('build/u16-relevant-prior-features.json', features)
write('build/u16-prior-lemma-index.json', [{k:l.get(k) for k in ['lemma_id','headword','part_of_speech','gender','class','gloss','notes']} for l in lex['lemmas']])
print('Captured immutable baseline:', counts, len(fixed) - 2, 'fixed non-register artifacts;')
print('Read all fifteen complete contracts and both registers; relevant prior construction records:',len(features))
for c in contracts:
    print(c['chapter_id'], c['title'], c['assigned_items'], 'tasks; boundaries:', c['bounded_scope'])
print('Lexical production milestones:',dict(Counter(f.get('production_taught_in') for l in lex['lemmas'] for f in l['forms'])))
print('Grammar production milestones:',dict(Counter(f.get('production_taught_in') for f in gram['features'])))
