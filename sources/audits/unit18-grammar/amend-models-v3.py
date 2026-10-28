import json,copy
from pathlib import Path
O=Path('sources/audits/unit18-grammar');p=O/'candidate-models.json';d=json.loads(p.read_text(encoding='utf8'));(O/'candidate-models-v2-witness.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
R={'44.4':[('ēarmlice','earmlice')],'44.6':[('ic hine hām bringe','ic hine ęft hām bringe')],'45.6':[('betweonan','betwēonan')],'45.7':[('wē biddað ðæt','wē biddað ðē ðæt')],'46.4':[('and āscode hwæðer','and āscode hīe hwæðer')],'46.6':[('gē foresægdon','gē mē foresægdon')],'46.8':[('and dō hit on','and dō on')],'46.9':[('hīe būton wǣron','hīe būton byrig wǣron'),('æfter ðǣm mannum','æfter ðissum mannum'),('ðonne gē hīe fōn, ðonne āsciað','ðonne ðū hīe fō, ðonne āsca')],'47.3':[('mid ðǣm ðū','mid ðǣm ðe ðū')],'47.6':[('Iudas ēode in','Iudas inēode')],'47.9':[('āscodest ūs hwæðer','āscodest ūs ǣr hwæðer')],'47.11':[('wē ne scēaweras sindon','wē ne wǣren scēaweras')],'48.2':[('mid his brōðrum gān','mid his brōðrum hām gān')],'48.5':[('cleopode','clēopode')],'48.7':[('ofer eorðan','ofer ealle eorðan'),(' erian ',' ęrian ')],'48.8':[('ofer eallum Egyptum','eallum Egyptum')],'48.9':[('ðæt wē','ðæt gē')]}
changes=[]
for x in d['items']:
 old=x['model'];k=f"{x['exercise']}.{x['item']}"
 for a,b in R.get(k,[]):
  assert a in x['model'],(k,a,x['model'])
  x['model']=x['model'].replace(a,b)
 if old!=x['model']:changes.append({'source_item_id':x['item_id'],'before':old,'after':x['model'],'reason':'Complete clause-by-clause comparison with exact prompts and fresh primary images; no omitted participant, adjunct or source target.'})
 x['status']='candidate wording v3 after complete 47-prompt comparison; coordinator review required'
d['rows']=copy.deepcopy(d['items']);d['model_version']='v3';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(O/'model-amendments-v3.json').write_text(json.dumps({'witness':'candidate-models-v2-witness.json','amendments':changes,'comparison':'All 47 full English prompts compared to every clause of the models; 46.9 you confirmed personally on fresh p31; 48.5 clēopian and 48.7 ęrian confirmed personally on fresh p33.'},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('v3:',len(changes),'amendments, 47 complete models')
