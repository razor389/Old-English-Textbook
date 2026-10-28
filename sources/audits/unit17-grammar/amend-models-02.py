"""Second explicit amendment record; initial witness is never overwritten."""
import json,re
from pathlib import Path
P=Path(__file__).resolve().parent
d=json.loads((P/'candidate-models.json').read_text(encoding='utf8'))
changes={
'38-05':('ðæt gemet','ðæt andgiet','Ex54 meaning: andgiet47, personally inspected.'),
'39-06':('edlēan æt','edlēane æt','Cook FB308 onfōn points to164j; FB94 receiving with dative.'),
'40-01':('ðæt God hire mid wǣre','ðæt God wǣre hire mid','Place preposition last as explicitly required by the prompt.'),
'40-08':('his cniht Israel','his cnihte Israel','Cook receiving164j and BT751 IV(a) protection/assistance with dative cnihtum. Israel is locally supplied apposition.'),
'41-04':('ǣnig ðing','nān ðing','Explicit183 target requires negative concord; FB100 gives negative+nān.'),
'42-02':('ðrȳmsetle','ðrymsetle','Exact Cook hint has no length on y; source image governs.'),
'43-14':('fæmnan','fǣmnan','Restore independently checked lemma fǣmne; no silent quantity loss.')}
log=[]
for r in d['rows']:
 k=r['source_item_id'].removeprefix('EX-XII-XIII-')
 if k not in changes:continue
 old,new,why=changes[k]
 if old not in r['model']:raise ValueError(k+' already amended or not found')
 before=r['model'];r['model']=before.replace(old,new)
 r['tokens']=re.findall(r"[A-Za-zĀ-žǢǣȲȳǪǫĚěęÆæÐðÞþ]+(?:-[A-Za-zĀ-žǢǣȲȳǪǫĚěęÆæÐðÞþ]+)*",r['model'])
 log.append({'source_item_id':r['source_item_id'],'before':before,'after':r['model'],'reason':why})
d['amendment_records']=['sources/audits/unit17-grammar/model-amendments-01.json','sources/audits/unit17-grammar/model-amendments-02.json']
(P/'candidate-models.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(P/'model-amendments-02.json').write_text(json.dumps({'access':'author-only; exclude from blind reviewers','changes':log},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Amended',len(log),'models; initial witness preserved.')
