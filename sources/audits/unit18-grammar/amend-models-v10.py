import json,copy
from pathlib import Path
O=Path(__file__).resolve().parent;p=O/'candidate-models.json';d=json.loads(p.read_text(encoding='utf8'));assert d['model_version']=='v9'
(O/'candidate-models-v9-witness.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
changes=[]
for r in d['items']:
 old=r['model'];r['model']=old.replace('for ēowre ðearfe','for ēowerre ðearfe')
 if old!=r['model']:changes.append({'source_item_id':r['source_item_id'],'before':old,'after':r['model'],'reason':'The selected for+benefit phrase takes dative. Use actual prior feminine dative singular possessive ēowerre, not accusative ēowre relabelled as a dative. No unattested contracted variant is added; positions and verbs are unchanged.'})
 r['status']='candidate wording v10; final precontract model'
d['rows']=copy.deepcopy(d['items']);d['model_version']='v10';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(O/'model-amendments-v10.json').write_text(json.dumps({'witness':'candidate-models-v9-witness.json','amendments':changes},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
p=O/'candidate-verbal-bindings.json';b=json.loads(p.read_text(encoding='utf8'));models={r['source_item_id']:r['model']for r in d['rows']}
for r in b['rows']:r['model']=models[r['source_item_id']];r['model_version']='v10'
b['model_version']='v10';p.write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
for fn in ['build-bindings.py','finalize-verbal-bindings.py']:
 p=O/fn;s=p.read_text(encoding='utf8').replace("'model_version':'v9'","'model_version':'v10'").replace("D['model_version']='v9'","D['model_version']='v10'");p.write_text(s,encoding='utf8')
print('v10 amendments',len(changes))
