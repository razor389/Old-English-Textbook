import json,re
from pathlib import Path
P=Path(__file__).resolve().parent;d=json.loads((P/'candidate-models.json').read_text(encoding='utf8'));log=[]
changes=[('Drihten','Dryhten'),('Drihtnes','Dryhtnes'),('ðām','ðǣm'),('fugolas','fuglas'),('micele','micle'),('mihtigan','mihtgan'),('hire','hiere'),('heora','hiera'),('ealle nēowolnessa','ealla nēowolnessa')]
for r in d['rows']:
 old=r['model'];s=old
 for a,b in changes:s=re.sub(r'\b'+a+r'\b',b,s)
 if old!=s:
  r['model']=s;r['tokens']=re.findall(r'[A-Za-zĀ-žǢǣȲȳÆæÐðÞþ]+(?:-[A-Za-zĀ-žǢǣȲȳÆæÐðÞþ]+)*',s)
  log.append({'source_item_id':r['source_item_id'],'before':old,'after':s,'reason':'Deliberately select actual prior productive spelling/inflection in new composition; exact Cook prompts and reading are untouched.','token_count_changed':False})
d['amendment_records'].append('sources/audits/unit17-grammar/model-amendments-06.json')
(P/'candidate-models.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(P/'model-amendments-06.json').write_text(json.dumps({'access':'author-only; exclude from blind reviewers','changes':log},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(len(log))
