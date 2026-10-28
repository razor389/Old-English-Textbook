import json,re
from pathlib import Path
P=Path(__file__).resolve().parent;d=json.loads((P/'candidate-models.json').read_text(encoding='utf8'));log=[]
changes={'42-01':('befeoll','befēoll','CookFB66§109 fēoll and exact175.20 gefēoll; retain prompt be- prefix in supplied adaptation.'),'37-10':('fugolas','fuglas','Use prior productive fuglas; do not silently assert long-vowel-stem variant as prior-taught.'),'39-02':('dēorwyrðra','dēorwierðra','Reuse prior productive dēorwierðe stem and its genitive plural.'),'43-09':('clīewene','ðoðre','Ex40 ball=ðoðor43, with full existing productivech16 system. Source spelling/quantity inspected by source editor.')}
for r in d['rows']:
 k=r['source_item_id'].removeprefix('EX-XII-XIII-')
 if k not in changes:continue
 a,b,w=changes[k];old=r['model']
 if a not in old:raise ValueError(k)
 r['model']=old.replace(a,b);r['tokens']=re.findall(r'[A-Za-zĀ-žǢǣȲȳÆæÐðÞþ]+(?:-[A-Za-zĀ-žǢǣȲȳÆæÐðÞþ]+)*',r['model'])
 log.append({'source_item_id':r['source_item_id'],'before':old,'after':r['model'],'reason':w})
d['amendment_records'].append('sources/audits/unit17-grammar/model-amendments-04.json')
(P/'candidate-models.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(P/'model-amendments-04.json').write_text(json.dumps({'access':'author-only; exclude from blind reviewers','changes':log},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(len(log))
