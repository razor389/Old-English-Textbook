"""Unit 18 curriculum analyst's complete prior-contract/register load receipt."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'curriculum/proposals/unit18'

def load(path):
    raw = (ROOT / path).read_bytes()
    return json.loads(raw), {'path': path, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

contracts = []
receipt = []
for n in range(1, 18):
    path = f'chapters/ch{n:02}/coverage.json'
    obj, ident = load(path)
    contracts.append(obj)
    ident.update(chapter=obj['chapter_id'], status=obj['status'], assigned_count=len(obj['assigned_items']), paradigm_count=len(obj.get('paradigms', [])), teaching_count=len(obj.get('teaching_records', [])))
    receipt.append(ident)

lexicon, ident = load('lexicon/entries.json')
receipt.append(ident)
grammar, ident = load('curriculum/grammar.json')
receipt.append(ident)
summaries = [{k: c[k] for k in ('chapter_id', 'productive_outcomes', 'recognition_outcomes', 'bounded_scope') if k in c} for c in contracts]
record = {'purpose': 'All seventeen active contracts and both actual cumulative registers loaded in full before curriculum analysis. No archived learning milestone imported.', 'files': receipt, 'counts': {'lemmas': len(lexicon['lemmas']), 'forms': sum(len(x.get('forms', [])) for x in lexicon['lemmas']), 'senses': sum(len(x.get('senses', [])) for x in lexicon['lemmas']), 'features': len(grammar['features'])}, 'contract_scope': summaries}
(OUT / 'prior-audit.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'loaded': len(receipt), 'counts': record['counts'], 'scope': summaries}, ensure_ascii=False, indent=2))
