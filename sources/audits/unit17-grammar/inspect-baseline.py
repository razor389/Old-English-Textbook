"""Read the complete active baseline and make a compact identity/scope receipt."""
import json, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
def read(rel):
    b=(ROOT/rel).read_bytes()
    return json.loads(b), {'path':rel,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}

lex,lr=read('lexicon/entries.json')
gram,gr=read('curriculum/grammar.json')
contracts=[]
scopes=[]
for n in range(1,17):
    c,r=read(f'chapters/ch{n:02}/coverage.json')
    contracts.append(r)
    scopes.append({k:v for k,v in c.items() if k in ['chapter_id','title','productive_outcomes','recognition_outcomes','bounded_scope','grammar_audit_boundaries','audited_inflection_rules']})
receipt={'baseline':'defa800','complete_contracts_parsed':contracts,'registers':[lr,gr],
 'counts':{'lemmas':len(lex['lemmas']),'forms':sum(len(x['forms']) for x in lex['lemmas']),'senses':sum(len(x['senses']) for x in lex['lemmas']),'features':len(gram['features'])},
 'boundary':'Only actual production/recognition milestones confer teaching. Supplied history do not.',
 'reader':'unit17_grammar'}
(OUT/'baseline-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'build/u17-grammar-prior-scopes.json').write_text(json.dumps(scopes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
compact=[]
for x in lex['lemmas']:
    compact.append({'lemma_id':x['lemma_id'],'headword':x['display_headword'],'pos':x.get('part_of_speech'),
    'senses':[{k:s.get(k) for k in ['sense_id','gloss','production_taught_in','recognition_taught_in','supplied_in']} for s in x['senses']],
    'forms':[{k:f.get(k) for k in ['form_id','form','analysis','production_taught_in','recognition_taught_in','supplied_in']} for f in x['forms']]})
(ROOT/'build/u17-grammar-prior-lexicon.json').write_text(json.dumps(compact,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'build/u17-grammar-prior-features.json').write_text(json.dumps([{k:f.get(k) for k in ['feature_id','description','production_taught_in','recognition_taught_in','supplied_in']} for f in gram['features']],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(receipt['counts'])
