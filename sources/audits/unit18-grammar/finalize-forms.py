import json,copy
from pathlib import Path
O=Path('sources/audits/unit18-grammar');p=O/'candidate-models.json';d=json.loads(p.read_text(encoding='utf8'));(O/'candidate-models-v4-witness.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
R={'44.7':[('ōðre sīð','ōðerne sīð')],'44.8':[('and æcern.','and æcernu.')],'45.3':[('nāmon','nōmon'),('fērdon','fōron')],'45.6':[('wē sind hider','wē sindon hider')],'46.9':[('fērdon','fōron')],'48.4':[('nǣre','ne wǣre')],'48.9':[('Dōð ðis','Dōð swā')]};changes=[]
for x in d['items']:
 old=x['model'];k=f"{x['exercise']}.{x['item']}"
 for a,b in R.get(k,[]):assert a in x['model'],(k,a);x['model']=x['model'].replace(a,b)
 if old!=x['model']:changes.append({'source_item_id':x['source_item_id'],'before':old,'after':x['model'],'reason':'Coordinator/design clause review and actual-form bindings: accusative time agreement; selected æcernu plural; thus swā; prior nōmon/sindon/fōron; no inferred contraction in48.4.'})
 x['status']='candidate wording v5 frozen after coordinator/design clause and actual-form reconciliation'
d['rows']=copy.deepcopy(d['items']);d['model_version']='v5';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(O/'model-amendments-v5.json').write_text(json.dumps({'witness':'candidate-models-v4-witness.json','amendments':changes},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
p=O/'build-verbal-systems.py';s=p.read_text(encoding='utf8');mark="D={'schema_version':1"
extra="add('findan','findan','corrective-preterite6',['U18G-FB54','U18G-FB55','U18G-FB61','U18G-FB62'],['Cook93/95: first and third singular indicative share the preterite singular stem fand; second singular funde uses the plural stem.','The earlier findan-pret-3-sg record says funde. Preserve that record and its milestones unchanged; this Unit18 correction has a distinct form ID. Display all six preterite cells to make the contrast explicit. Funde remains valid second-singular indicative and past-subjunctive morphology, not the selected third-singular past in47.5.'],['47.5'],pt=six('fand','funde','fand','fundon'))\n"
assert extra not in s;s=s.replace(mark,extra+mark);p.write_text(s,encoding='utf8')
p=O/'build-bindings.py';s=p.read_text(encoding='utf8').replace("if a.get('contextual_parse')=='pp-bare':","if a.get('form')=='infinitive citation':a['verb_form']='plain_infinitive'\n if a.get('contextual_parse')=='pp-bare':")
s=s.replace("'45.3':'nāmon:it3p fērdon:it3p'","'45.3':'nōmon:it3p fōron:it3p'").replace('sind:ip1p','sindon:ip1p').replace('fērdon:it3p','fōron:it3p').replace("diernan:inf ādrāf:it3s nǣre:st3s","diernan:inf ādrāf:it3s wǣre:st3s").replace("'model_version':'v4'","'model_version':'v5'")
s=s.replace("manual={", "manual={('44.7','nǣre'):('wesan','wesan-u18-naere-counterfactual-supplied','U18-H-44-07'),")
s=s.replace("candidates.sort(key=", "if k=='47.11' and surf=='bīetst':candidates=[c for c in candidates if c[0]=='beodan']\n  candidates.sort(key=")
p.write_text(s,encoding='utf8');print('v5 amendments',len(changes))
