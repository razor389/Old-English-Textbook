import json,re
from pathlib import Path
P=Path(__file__).resolve().parent;d=json.loads((P/'candidate-models.json').read_text(encoding='utf8'))
r=next(r for r in d['rows']if r['source_item_id']=='EX-XII-XIII-40-01');old=r['model']
assert 'Godes gife'in old
r['model']=old.replace('Godes gife','Godes giefe');r['tokens']=re.findall(r'[A-Za-zĀ-žǢǣȲȳÆæÐðÞþ]+(?:-[A-Za-zĀ-žǢǣȲȳÆæÐðÞþ]+)*',r['model'])
d['amendment_records'].append('sources/audits/unit17-grammar/model-amendments-11.json')
(P/'candidate-models.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(P/'model-amendments-11.json').write_text(json.dumps({'access':'author-only; exclude from blind reviewers','changes':[{'source_item_id':r['source_item_id'],'before':old,'after':r['model'],'reason':'Select giefe consistently with the source worker’s supplied grace phrase and the registered headword giefu; the earlier gift sense alone does not teach grace. Nominal worker owns exact form/sense status.','token_count_changed':False}]},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('One contextual source spelling amended; all82 remain.')
