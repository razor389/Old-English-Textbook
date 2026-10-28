import json,copy
from pathlib import Path
O=Path(__file__).resolve().parent
p=O/'candidate-models.json';d=json.loads(p.read_text(encoding='utf8'))
assert d['model_version']=='v6'
(O/'candidate-models-v6-witness.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
changes=[]
for r in d['items']:
 old=r['model'];r['model']=r['model'].replace('fēoh','feoh').replace('mīnne læfel seolfres','mīnne seolfrenne læfel').replace('ðȳlǣs','ðȳ-lǣs-ðe')
 if old!=r['model']:changes.append({'source_item_id':r['source_item_id'],'before':old,'after':r['model'],'reason':'Select printed feoh without inferred length (Cook47.5); supplied seolfrenne rather than an insufficiently supported material-genitive extension; actual taught ðȳ-lǣs-ðe spelling. Earlier recommendation that feoh was already productive was withdrawn after the actual register check.'})
 r['status']='candidate wording v7; source and actual cumulative records reconciled; coordinator contract pending'
d['rows']=copy.deepcopy(d['items']);d['model_version']='v7'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(O/'model-amendments-v7.json').write_text(json.dumps({'witness':'candidate-models-v6-witness.json','amendments':changes},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
p=O/'build-bindings.py';s=p.read_text(encoding='utf8').replace("'model_version':'v6'","'model_version':'v7'");s=s[:s.index("used=sorted(")];p.write_text(s,encoding='utf8')
p=O/'build-senses-features.py';s=p.read_text(encoding='utf8').replace('nim mīnne læfel seolfres','nim mīnne seolfrenne læfel').replace('The material genitive seolfres identifies the silver cup;','Supplied seolfrenne is the strong accusative masculine singular adjective agreeing with the cup;').replace('The nominal/source packet supplies the material and name relations with evidence.','The nominal/source packet supplies the exact silver-adjective form with evidence; no independent adjective system is inferred.').replace("['U18G-EX31','U18G-FB90'])","['U18G-EX31','U18G-EX62'])").replace('ðȳlǣs','ðȳ-lǣs-ðe').replace('Sp rece/sprece','Sprece')
new="sup('U18-H-48-02',['48.2'],'lǣt ðone cnapan mid his brōðrum hām gān','Complete permission frame: singular lǣt addresses Joseph; accusative ðone cnapan is the actor of plain infinitive gān. The boy goes home with his brothers. The accusative actor is not the recipient of a finite command and gān has no person ending. This local frame does not infer unrestricted causative/permissive infinitives from the familiar verb alone.', ['U18G-EX32','U18G-FB95','U18G-FB105','U18G-FB106'])\n"
s=s.replace("refs=[]\n",new+"refs=[]\n");p.write_text(s,encoding='utf8')
print('v7 amendments',len(changes))
