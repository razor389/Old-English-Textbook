import json,copy
from pathlib import Path
O=Path(__file__).resolve().parent;p=O/'candidate-models.json';d=json.loads(p.read_text(encoding='utf8'));assert d['model_version']=='v7'
(O/'candidate-models-v7-witness.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
changes=[]
for r in d['items']:
 old=r['model'];r['model']=old.replace('būton byrig','būtan byrig').replace('būton ðǣm cnapan','būtan ðǣm cnapan')
 if old!=r['model']:changes.append({'source_item_id':r['source_item_id'],'before':old,'after':r['model'],'reason':'Use the actually taught preposition spelling būtan for outside/without, with the new spatial sense separately supplied. Preserve conjunction būton elsewhere. No word position changes.'})
 r['status']='candidate wording v8; final precontract model'
d['rows']=copy.deepcopy(d['items']);d['model_version']='v8';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(O/'model-amendments-v8.json').write_text(json.dumps({'witness':'candidate-models-v7-witness.json','amendments':changes},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
for fn in ['build-bindings.py','finalize-verbal-bindings.py']:
 p=O/fn;s=p.read_text(encoding='utf8').replace("'model_version':'v7'","'model_version':'v8'").replace("D['model_version']='v7'","D['model_version']='v8'");p.write_text(s,encoding='utf8')
p=O/'build-senses-features.py';s=p.read_text(encoding='utf8').replace('būton ðǣm cnapan','būtan ðǣm cnapan').replace('Būton with dative denotes absence','Būtan with dative denotes absence').replace("['U18G-EX32','U18G-FB95','U18G-FB105','U18G-FB106'])","['U18G-EX32','U18G-FB96','U18G-FB105','U18G-FB106'])").replace("'U18G-BT749',",'');p.write_text(s,encoding='utf8')
print('v8 amendments',len(changes))
