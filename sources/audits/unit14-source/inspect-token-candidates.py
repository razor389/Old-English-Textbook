import json,re
from pathlib import Path
p=Path(__file__).resolve().parent
a=json.loads(Path('lexicon/entries.json').read_text(encoding='utf8'))['lemmas']
toks=json.loads((p/'reading-source.json').read_text(encoding='utf8'))['learner_text'].split()
bound={x['token_index_one_based'] for x in json.loads(Path('sources/audits/unit14-grammar/source-support.json').read_text(encoding='utf8'))['reading_bindings']}
for i,t in enumerate(toks,1):
 if i in bound: continue
 surface=t.strip('.,;')
 print(i,surface,','.join(f['form_id'] for l in a for f in l['forms'] if f['form'].lower()==surface.lower()))
print('SCAN',re.findall(r'images-dictionary/[^"<> ]+', (p/'bt-gecaelan-entry.html').read_text(encoding='utf8')))
