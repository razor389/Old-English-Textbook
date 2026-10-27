"""Read the actual fifteen active contracts and actual cumulative registers."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent

def read(path):
    raw = (ROOT / path).read_bytes()
    return json.loads(raw.decode('utf-8-sig')), {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}

contracts = []
for n in range(1, 16):
    path = f'chapters/ch{n:02d}/coverage.json'
    d, identity = read(path)
    contracts.append({'identity': identity, **{k: d.get(k) for k in ['chapter_id', 'title', 'status', 'productive_outcomes', 'recognition_outcomes', 'bounded_scope', 'audited_inflection_rules', 'grammar_audit_boundaries', 'prior_teaching_boundary', 'form_identity_reconciliation', 'promotions', 'contract_reconciliation_notes']}, 'actual_assigned_ids': [r.get('item_id', r.get('id')) for r in d.get('assigned_items', [])], 'actual_feature_ids': [r.get('feature_id') for r in d.get('grammar_inventory', [])] if isinstance(d.get('grammar_inventory'), list) else d.get('grammar_inventory')})
lex, lex_identity = read('lexicon/entries.json')
gram, gram_identity = read('curriculum/grammar.json')
snapshot = {'purpose': 'Compact actual-record reading receipt; no new teaching or changes to historical records. The actual cumulative registers and immutable root baseline remain authoritative, not this receipt.', 'contracts_read': [x['identity'] for x in contracts], 'lexicon_identity': lex_identity, 'grammar_identity': gram_identity, 'counts': {'lemmas': len(lex['lemmas']), 'forms': sum(len(x['forms']) for x in lex['lemmas']), 'senses': sum(len(x['senses']) for x in lex['lemmas']), 'features': len(gram['features'])}, 'compaction_note': 'The unused37MB diagnostic duplicate of complete registers was replaced by exact input identities/counts. Actual prior forms/senses/milestones are read directly by the packet builders and preserved in selected dependency records. This diagnostic is not a substitute for the actual records.'}
(OUT / 'prior-records.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
summary = {'counts': snapshot['counts'], 'contracts': contracts}
(OUT / 'prior-scope-audit.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'counts': snapshot['counts'], 'contracts_read': len(contracts)}, ensure_ascii=False))
