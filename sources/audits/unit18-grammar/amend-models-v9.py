import json,copy
from pathlib import Path
O=Path(__file__).resolve().parent;p=O/'candidate-models.json';d=json.loads(p.read_text(encoding='utf8'));assert d['model_version']=='v8'
(O/'candidate-models-v8-witness.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
changes=[]
for r in d['items']:
 old=r['model'];r['model']=old.replace('būton','būtan').replace('Būton','Būtan')
 if old!=r['model']:changes.append({'source_item_id':r['source_item_id'],'before':old,'after':r['model'],'reason':'Select the directly checked CookFB280 conjunction būtan, with a distinct supplied unless sense; no checked būton conditional evidence was used. Source editor supplies complete negative-condition frame. No position or verbal changes.'})
 r['status']='candidate wording v9; final precontract model'
d['rows']=copy.deepcopy(d['items']);d['model_version']='v9';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(O/'model-amendments-v9.json').write_text(json.dumps({'witness':'candidate-models-v8-witness.json','amendments':changes},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
p=O/'candidate-verbal-bindings.json';b=json.loads(p.read_text(encoding='utf8'));models={r['source_item_id']:r['model']for r in d['rows']}
for r in b['rows']:r['model']=models[r['source_item_id']];r['model_version']='v9'
b['model_version']='v9';p.write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
for fn in ['build-bindings.py','finalize-verbal-bindings.py']:
 p=O/fn;s=p.read_text(encoding='utf8').replace("'model_version':'v8'","'model_version':'v9'").replace("D['model_version']='v8'","D['model_version']='v9'");p.write_text(s,encoding='utf8')
print('v9 amendments',len(changes))
