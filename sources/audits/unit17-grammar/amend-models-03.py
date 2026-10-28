import json,re
from pathlib import Path
P=Path(__file__).resolve().parent;d=json.loads((P/'candidate-models.json').read_text(encoding='utf8'));log=[]
for r in d['rows']:
 old=r['model'];s=old;why=[]
 for a,b,w in [('for ðām ðe','for-ðon-ðe','Select actually productive prior because connective; source quotations retain their original variants.'),('For ðām ðe','For-ðon-ðe','Select actually productive prior because connective.'),('sōðlīce','sōðlice','Use actual productive source quantity and exact40.3 hint.'),('Sōðlīce','Sōðlice','Use actual productive source quantity.'),('efenswā mihtig swā','swā mihtig swā','Prior equative swā…swā; do not introduce unsupported efenswā.')]:
  if a in s:s=s.replace(a,b);why.append(w)
 if r['source_item_id'].endswith('37-10'):s=s.replace('wyrmas','nædran');why.append('Source editor independently checked Ex61 serpent=nædre53.1; avoid unnecessary wyrm-sense extension.')
 if r['source_item_id'].endswith('42-08'):s=s.replace('heora cnēow ','heora cnēo ');why.append('Select the source-editor’s verified taught accusative singular cnēo, matching English knee.')
 if old!=s:
  r['model']=s;r['tokens']=re.findall(r'[A-Za-zĀ-žǢǣȲȳÆæÐðÞþ]+(?:-[A-Za-zĀ-žǢǣȲȳÆæÐðÞþ]+)*',s)
  log.append({'source_item_id':r['source_item_id'],'before':old,'after':s,'reasons':why})
d['amendment_records'].append('sources/audits/unit17-grammar/model-amendments-03.json')
(P/'candidate-models.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(P/'model-amendments-03.json').write_text(json.dumps({'access':'author-only; exclude from blind reviewers','changes':log},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(len(log))
