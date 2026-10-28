import json,re
from pathlib import Path
P=Path(__file__).resolve().parent;d=json.loads((P/'candidate-models.json').read_text(encoding='utf8'));log=[]
changes=[('sind','sindon','Use actual prior productive third-plural form, not supplied-only sind variant.'),('healt','hielt','Select actual prior taught umlauted present3sg healdan, not an unlicensed spelling.'),('geseald','seald','Select productive sęllan past participle; ge-variant was only citation notation.'),('mihte','meahte','Select actual productive magan preterite.'),('nāmon','nōmon','Select actual productive niman preterite and Cook63 explicitly marked ō.')]
for r in d['rows']:
 old=r['model'];s=old;why=[]
 for a,b,w in changes:
  if re.search(r'\b'+a+r'\b',s):s=re.sub(r'\b'+a+r'\b',b,s);why.append(w)
 if old!=s:
  r['model']=s;r['tokens']=re.findall(r'[A-Za-zĀ-žǢǣȲȳÆæÐðÞþ]+(?:-[A-Za-zĀ-žǢǣȲȳÆæÐðÞþ]+)*',s)
  log.append({'source_item_id':r['source_item_id'],'before':old,'after':s,'reasons':why,'token_count_changed':False})
d['amendment_records'].append('sources/audits/unit17-grammar/model-amendments-05.json')
(P/'candidate-models.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(P/'model-amendments-05.json').write_text(json.dumps({'access':'author-only; exclude from blind reviewers','changes':log},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(len(log))
