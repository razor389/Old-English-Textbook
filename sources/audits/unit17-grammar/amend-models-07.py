import json,re
from pathlib import Path
P=Path(__file__).resolve().parent;d=json.loads((P/'candidate-models.json').read_text(encoding='utf8'));log=[]
changes={'38-06':('manigfealde ðēnunga','manigfealda ðēnunga','Strong ACC.F.PL agrees with services; select the declared-a paradigm ending.'),'39-04':('ealle ðēoda','ealla ðēoda','Strong NOM.F.PL agrees with nations; select productive ealla.'),'40-03':('ealle cnēorissa','ealla cnēorissa','Strong NOM.F.PL agrees with generations.'),'40-04':('micle ðing','miclu ðing','Great things is ACC.N.PL, requiring selected miclu; micle is not its required gender/number cell.'),'41-02':('ealle ðing','eall ðing','All things is ACC.N.PL, requiring selected eall.')}
for r in d['rows']:
 k=r['source_item_id'].removeprefix('EX-XII-XIII-')
 if k not in changes:continue
 a,b,w=changes[k];old=r['model']
 if a not in old:raise ValueError(k)
 r['model']=old.replace(a,b);r['tokens']=re.findall(r'[A-Za-zĀ-žǢǣȲȳÆæÐðÞþ]+(?:-[A-Za-zĀ-žǢǣȲȳÆæÐðÞþ]+)*',r['model'])
 log.append({'source_item_id':r['source_item_id'],'before':old,'after':r['model'],'reason':w,'token_count_changed':False})
d['amendment_records'].append('sources/audits/unit17-grammar/model-amendments-07.json')
(P/'candidate-models.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(P/'model-amendments-07.json').write_text(json.dumps({'access':'author-only; exclude from blind reviewers','changes':log},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(len(log))
