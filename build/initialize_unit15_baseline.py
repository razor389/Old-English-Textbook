"""Capture the actual fourteen-unit state once; never rerun after integration."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'sources/audits/unit15-coordinator'
OUT.mkdir(parents=True, exist_ok=True)
def read(path): return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))
def write(path, data):
    (ROOT / path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
def identity(path):
    raw = (ROOT / path).read_bytes()
    return hashlib.sha256(raw).hexdigest(), hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest()

destination = ROOT / 'build/unit15-prior-baseline.json'
assert not destination.exists(), 'Immutable baseline already exists'
paths = (ROOT / 'build/u15-prior-tracked-paths.txt').read_text(encoding='utf-8-sig').splitlines()
mutable = {'.beads/issues.jsonl', 'README.md', 'STATUS.md', 'docs/HANDOFF.md',
           'curriculum/COURSE_PLAN.md', 'curriculum/COOK_MAP.md', 'sources/README.md',
           'sources/registry.json', 'typesetting/README.md'}
register_paths = ['lexicon/entries.json', 'curriculum/grammar.json']

fixed = [p for p in paths if p not in mutable and (not p.startswith('.beads/'))]
hashes = {p: identity(p) for p in fixed}
lex, gram = [read(p) for p in register_paths]
expected = [f'ch{i:02d}' for i in range(1, 15)]
assert lex['reviewed_chapters'] == gram['reviewed_chapters'] == expected
contracts = []
for chapter in expected:
    path = f'chapters/{chapter}/coverage.json'
    c = read(path)
    assert c.get('completion', {}).get('complete') is True or (chapter == 'ch01' and c['status'] == 'reviewed_complete' and c['review_status'] == 'passed'), chapter
    # Read each full contract, including every record; retain an orientation
    # summary, not a substitute for consulting actual form/sense/use records.
    contracts.append({
        'chapter_id': chapter, 'path': path, 'identity': identity(path),
        'title': c.get('title', c.get('chapter_title', chapter)), 'status': c['status'],
        'productive_outcomes': c.get('productive_outcomes'),
        'recognition_outcomes': c.get('recognition_outcomes'),
        'bounded_scope': c.get('bounded_scope'),
        'assigned_items': len(c['assigned_items']),
        'new_lexical_entries': len(c.get('lexical_inventory', [])),
        'grammar_inventory': [{k: f.get(k) for k in ['feature_id', 'description', 'knowledge_status', 'scope_note']} for f in c.get('grammar_inventory', [])],
        'source_spans': c.get('source_spans'),
    })
counts = {'lemmas': len(lex['lemmas']), 'forms': sum(len(l['forms']) for l in lex['lemmas']),
          'senses': sum(len(l['senses']) for l in lex['lemmas']), 'features': len(gram['features'])}
assert counts == {'lemmas':830, 'forms':9710, 'senses':1017, 'features':820}
baseline = {'chapter_id': 'ch15', 'git_checkpoint_full': '9129cdabd21ac9335eca531d42815a5c81ecd8a3', 'lexicon': lex, 'grammar': gram, 'counts': counts, 'files': {p: v[0] for p, v in hashes.items()}, 'files_lf_sha256': {p: v[1] for p, v in hashes.items()}, 'mutable_shared_indexes': sorted(mutable)}
write('build/unit15-prior-baseline.json', baseline)
retained = {k:v for k,v in baseline.items() if k not in ['lexicon','grammar']}
retained['immutable_local_snapshot'] = 'build/unit15-prior-baseline.json'
retained['snapshot_sha256'] = identity('build/unit15-prior-baseline.json')[0]
retained['method'] = 'Read every active contract and both actual registers; captured every tracked fixed artifact including earlier tracked build helpers. Shared course indexes may be updated only for Unit15; earlier teaching records and source evidence remain preserved.'
write('sources/audits/unit15-coordinator/prior-state.json', retained)
write('build/u15-prior-contract-orientation.json', contracts)
pattern = re.compile(r'negative|negation|indefinit|distribut|compar|quantit|proportion|concord|except|free.choice|nān|ǣnig|gehwā', re.I)
features = [f for f in gram['features'] if pattern.search(json.dumps({k:v for k,v in f.items() if k not in ['records_by_chapter','evidence_refs']},ensure_ascii=False))]
write('build/u15-relevant-prior-features.json', features)
print('Captured immutable baseline:', counts, len(fixed) - 2, 'fixed non-register artifacts;')
print('Parsed all fourteen contracts; relevant prior construction records:',len(features))
for c in contracts:
    print(c['chapter_id'], c['title'], c['assigned_items'], 'tasks; boundaries:', c['bounded_scope'])
