import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=json.loads((R/'curriculum/proposals/unit16/author-only-cook-candidates.json').read_text(encoding='utf-8'))
lemmas={}
surfaces={}
for seq in p['sequences']:
    for t in seq['tokens']:
        for lid, senses in t['sense_candidates_by_lemma'].items():
            lemmas.setdefault(lid,{})
            lemmas[lid].update({s['sense_id']:s for s in senses})
        surfaces.setdefault(t['surface'].casefold(), t['form_candidates'])
out={'lemmas':[{ 'lemma_id':lid,'senses':list(s.values())} for lid,s in sorted(lemmas.items())], 'surfaces':[{'surface':surface,'candidates':c} for surface,c in sorted(surfaces.items())]}
(R/'curriculum/proposals/unit16/author-only-binding-review.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('\n'.join(lid+': '+' | '.join(sid+'='+s['gloss'] for sid,s in records.items()) for lid,records in sorted(lemmas.items())))
print('SURFACE_COUNT',len(surfaces))
