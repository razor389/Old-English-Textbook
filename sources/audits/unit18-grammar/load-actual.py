import json,hashlib
from pathlib import Path
R=Path.cwd();O=R/'sources/audits/unit18-grammar'
l=json.loads((R/'lexicon/entries.json').read_text(encoding='utf8'));g=json.loads((R/'curriculum/grammar.json').read_text(encoding='utf8'))
cs=[]
for n in range(1,18):
 p=R/f'chapters/ch{n:02}/coverage.json';b=p.read_bytes();c=json.loads(b);cs.append({'path':str(p.relative_to(R)),'sha256':hashlib.sha256(b).hexdigest(),'scope':{k:v for k,v in c.items()if k in ['chapter_id','productive_outcomes','recognition_outcomes','bounded_scope','audited_inflection_rules']}})
(O/'all-prior-contract-scope.json').write_text(json.dumps(cs,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('\n'.join(f"{c['scope'].get('chapter_id')}: {c['scope'].get('bounded_scope')}"for c in cs))
print('\nLEXEMES\n'+'\n'.join(x['lemma_id']+' '+x['display_headword']+' '+str([(s['gloss'],s.get('production_taught_in'))for s in x['senses']])for x in l['lemmas'] if x['part_of_speech'] in ['verb','noun','adjective']))
