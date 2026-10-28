import json,re
from pathlib import Path
P=Path(__file__).resolve().parent;d=json.loads((P/'candidate-models.json').read_text(encoding='utf8'));log=[]
changes={'37-10':('eall nīeten','eall nīetenu','Cattle is explicitly plural; choose the actual productive neuter plural nīetenu.'),'38-02':('Sum cwēn','Sumu cwēn','Choose actual productive strong nominative feminine singular sumu.'),'43-09':('ðoðre','ðoðore','Actual prior DAT.SG retains medial vowel; the first stem syllable is short.'),'43-01':('ðǣra wyrta','ðāra wyrta','Choose actual prior productive genitive-plural demonstrative ðāra.')}
for r in d['rows']:
 k=r['source_item_id'].removeprefix('EX-XII-XIII-')
 if k not in changes:continue
 a,b,w=changes[k];old=r['model']
 if a not in old:raise ValueError(k)
 r['model']=old.replace(a,b);r['tokens']=re.findall(r'[A-Za-zĀ-žǢǣȲȳÆæÐðÞþ]+(?:-[A-Za-zĀ-žǢǣȲȳÆæÐðÞþ]+)*',r['model'])
 log.append({'source_item_id':r['source_item_id'],'before':old,'after':r['model'],'reason':w,'token_count_changed':False})
d['amendment_records'].append('sources/audits/unit17-grammar/model-amendments-08.json')
(P/'candidate-models.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(P/'model-amendments-08.json').write_text(json.dumps({'access':'author-only; exclude from blind reviewers','changes':log},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(len(log))
