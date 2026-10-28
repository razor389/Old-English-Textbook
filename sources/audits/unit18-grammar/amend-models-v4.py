import json,copy
from pathlib import Path
O=Path('sources/audits/unit18-grammar');p=O/'candidate-models.json';d=json.loads(p.read_text(encoding='utf8'))
(O/'candidate-models-v3-witness.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
changes=[]
for x in d['items']:
 old=x['model']
 for a,b in [('metes','mętes'),('Drihten','Dryhten'),('feoh','fēoh'),('siolfor','seolfor'),('siolfres','seolfres')]:x['model']=x['model'].replace(a,b)
 if old!=x['model']:changes.append({'source_item_id':x['source_item_id'],'before':old,'after':x['model'],'reason':'Use actual prior productive nonverbal surfaces verified by the nominal/source analyst. Leofað is retained as actual libban-pres-3-sg, productive ch02; lifde is its distinct preterite.'})
 x['status']='candidate wording v4 frozen for binding; coordinator review required'
d['rows']=copy.deepcopy(d['items']);d['model_version']='v4';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(O/'model-amendments-v4.json').write_text(json.dumps({'witness':'candidate-models-v3-witness.json','amendments':changes},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('v4:',len(changes),'spelling-alignment amendments')
