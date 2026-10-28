import json,copy,re
from pathlib import Path
O=Path('sources/audits/unit18-grammar');p=O/'candidate-models.json';d=json.loads(p.read_text(encoding='utf8'))
if not (O/'candidate-models-v1-witness.json').exists():(O/'candidate-models-v1-witness.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
changes=[]
R={
'44.5':[('āscode ūs hwæðer','āscode ūs ealle hwæðer'),('giernan ðæt','giernan ðæs ðæt')],
'45.4':[('gebeorscipe','gebēorscipe')],
'45.6':[('āfyrhte','āfǣred'),('gelǣdde','lǣded'),('ūrra assa','ūrra assena'),('geðēowie','ðēowie')],
'45.7':[('Ēalā hlāford','Lēof'),('ūre sprǣce','ūrre sprǣce')],
'46.2':[('fodor','fōdor')],
'46.3':[('incōme','inēode')],
'46.7':[('Gefyll','Gefyl')],
'46.8':[('mīnne siolforlæfel','mīnne læfel siolfres'),('hē him sealde','hē ðē sealde')],
'46.9':[('hæfdon sumne dǣl ðæs weges gefaren','fōron sumne dǣl ðæs weges'),('gelǣccen','fōn')],
'47.2':[('gelǣhte','fangen'),('ðæs hlāfordes gold','ðīnes hlāfordes gold')],
'48.7':[('hungor','hunger'),('nāðor','nāhwæðer')],
'48.8':[('ofer Egyptum','ofer eallum Egyptum')]
}
for x in d['items']:
 old=x['model']; key=f"{x['exercise']}.{x['item']}"
 for a,b in [('ðām','ðǣm'),(' męn ',' męnn '),(' męn.',' męnn.'),('hwām','hwǣm'),('leofode','lifde')]+R.get(key,[]):x['model']=x['model'].replace(a,b)
 if old!=x['model']:changes.append({'source_item_id':x['item_id'],'before':old,'after':x['model'],'reason':'Exact prompt/hint preservation; actual prior productive surface; source-checked lexical choice. See construction and verbal-system audit for every teaching route.'})
 x['source_item_id']=x['item_id'];x['status']='reconciled candidate wording v2; grammatical support packet and coordinator approval required';x['pending']='No learner prose or assessment assignment until committed contract.'
d['rows']=copy.deepcopy(d['items']);d['schema_version']=2;d['model_version']='v2';d['tokenization']="Python re.findall(r'[^\\W\\d_]+(?:-[^\\W\\d_]+)*', model), one-based positions"
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(O/'model-amendments-v2.json').write_text(json.dumps({'preserved_witness':'candidate-models-v1-witness.json','amendments':changes,'unresolved_evidence':['Direct local name/ethnonym evidence and precise neither coordination catalog pending; model strings are reviewable proposals, not certified key prose.']},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(len(changes),'amended models; 47 rows; initial witness preserved')
