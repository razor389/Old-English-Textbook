"""Exact contextual verb inventory. Keeps prior analysis dictionaries literally intact."""
import json,re,copy
from pathlib import Path
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
L={x['lemma_id']:x for x in json.load(open(R/'lexicon/entries.json',encoding='utf8'))['lemmas']}
V=json.load(open(O/'verbal-systems.json',encoding='utf8'))
rows=json.load(open(O/'candidate-models.json',encoding='utf8'))['rows']
F=[]
for lid,l in L.items():
 if l.get('part_of_speech') not in ['verb','auxiliary','modal verb'] and not any(isinstance(f.get('analysis'),dict)and'mood'in f['analysis']for f in l['forms']):continue
 for f in l['forms']:F.append((lid,f,'previously_taught' if f.get('production_taught_in')else 'prior_recognition' if f.get('recognition_taught_in')else 'prior_supplied'))
for s in V['systems']:
 for f in s['cells']:F.append((s['lemma_id'],f,f['knowledge_status']))
def analysis(code):
 if code=='inf':return {'verb_form':'plain_infinitive'}
 if code=='inflected':return {'verb_form':'inflected_infinitive'}
 if code in ['pp','prp']:return {'verb_form':'participle','tense':'past' if code=='pp'else'present','agreement':'base'}
 if code[0]=='m':return {'mood':'imperative','person':int(code[1]),'number':'sg'if code[2]=='s'else'pl'}
 return {'mood':{'i':'indicative','s':'subjunctive'}[code[0]],'tense':{'p':'present','t':'preterite'}[code[1]],'person':int(code[2]),'number':'sg'if code[3]=='s'else'pl'}
def normalized(a):
 if not isinstance(a,dict):return {}
 a=copy.deepcopy(a)
 if a.get('number')in ['singular','plural']:a['number']={'singular':'sg','plural':'pl'}[a['number']]
 if a.get('nonfinite')=='infinitive':a['verb_form']='inflected_infinitive' if a.get('infinitive_type')=='inflected' else 'plain_infinitive'
 if a.get('nonfinite')in ['participle','past_participle','present_participle']:
  a['verb_form']='participle';a['tense']=a.get('tense')or('past'if a['nonfinite']=='past_participle'else'present');a['agreement']=a.get('inflection','base')
 if a.get('form')=='infinitive citation':a['verb_form']='plain_infinitive'
 if a.get('contextual_parse')=='pp-bare':a.update(verb_form='participle',tense='past',agreement='base')
 return a
spec={
'44.1':'cwæð:it3s gāð:m2p bycgað:m2p',
'44.2':'cwæð:it3s swōr:it3s mōsten:st1p cuman:inf bringen:sp1p',
'44.3':'sęndan:inf wilt:ip2s gāð:ip1p bycgað:ip1p beðurfon:ip1p',
'44.4':'dydon:it2p sægdon:it2p hæfden:st2p',
'44.5':'āscode:it3s lifde:st3s hæfden:st1p andswarodon:it1p wiston:it1p wolde:st3s giernan:inf lǣdden:st1p',
'44.6':'cwæð:it3s sęnd:m2s mægen:sp1p bycgan:inf beðurfon:ip1p forweorðen:sp1p bringe:sp1s sīe:sp1s',
'44.7':'nǣre:st3s wǣren:st1p cumen:pp',
'44.8':'cwæð:it3s dōn:inf sculon:ip2p dōð:m2p willað:ip2p nimað:m2p bringað:m2p',
'45.1':'nimað:m2p gāð:m2p',
'45.2':'gedō:sp3s āgiefe:sp3s hæfð:ip3s eom:ip1s berēafod:pp',
'45.3':'nōmon:it3p fōron:it3p',
'45.4':'geseah:it3s cwæð:it3s lǣd:m2s gearca:m2s mægen:sp3p etan:inf',
'45.5':'dyde:it3s boden:pp wæs:it3s',
'45.6':'wǣron:it3p wurdon:it3p āfǣred:pp sægdon:it3p fundon:it1p sindon:ip1p lǣded:pp berēafie:sp3s ðēowie:sp3s',
'45.7':'cwǣdon:it3p biddað:ip1p hlyste:sp2s wǣron:it1p bohton:it1p',
'45.8':'cēapodon:it1p wǣron:it1p undydon:it1p fundon:it1p sealdon:it1p',
'45.9':'brōhton:it1p cēapianne:inflected witon:ip1p dyde:it3s',
'46.1':'cwæð:it3s sīe:sp3s ondrǣdað:m2p sealde:it3s',
'46.2':'ðwōgon:it3p sealde:it3s',
'46.3':'lęgdon:it3p inēode:st3s',
'46.4':'oncnēow:it3s āscode:it3s wǣre:st3s lifde:st3s',
'46.5':'cwǣdon:it3p is:ip3s leofað:ip3s',
'46.6':'geseah:it3s cwæð:it3s is:ip3s foresægdon:it2p cwæð:it3s gemiltsie:sp3s',
'46.7':'bēad:it3s cwæð:it3s gefyl:m2s sęte:m2s',
'46.8':'nim:m2s sealde:it3s dō:m2s dyde:it3s',
'46.9':'fōron:it3p wǣron:it3p fōron:it3p cwæð:it3s ārīs:m2s gā:m2s fō:sp2s āsca:m2s wolden:st3p forgieldan:inf',
'47.1':'forstǣlon:it2p wæs:it3s',
'47.2':'dyde:it3s boden:pp wæs:it3s fangen:pp wǣron:it3p cwǣdon:it3p fundon:it1p brōhton:it1p wēnst:ip2s stǣlen:st1p',
'47.3':'sēc:m2s sīe:sp3s ofslægen:pp finde:sp2s',
'47.4':'cwæð:it3s finde:sp1s sīe:sp3s sīen:sp3p',
'47.5':'sōhte:it3s funde:it3s gewęndon:it3p',
'47.6':'inēode:it3s fēollon:it3p',
'47.7':'cwæð:it3s dōn:inf woldon:it2p',
'47.8':'sīe:sp3s forstæl:it3s gāð:m2p',
'47.9':'cwæð:it3s āscodest:it2s hæfden:st1p',
'47.10':'cwǣdon:it1p habbað:ip1p hæfð:ip3s lufað:ip3s',
'47.11':'bīetst:ip2s bringen:sp1p gesēo:sp2s wite:sp2s wǣren:st1p',
'48.1':'swōr:it1s brōhte:st1s cwæð:it1s bringe:sp1s sīe:sp1s',
'48.2':'lǣt:m2s gān:inf sīe:sp1s',
'48.3':'dearr:ip1s gān:inf gesēo:sp1s',
'48.4':'meahte:it3s diernan:inf ādrāf:it3s wǣre:st3s',
'48.5':'wēop:it3s clēopode:it3s cwæð:it3s eom:ip1s leofað:ip3s',
'48.6':'ondrǣdað:m2p ofðynce:sp3s sealdon:it2p sęnde:it3s',
'48.7':'wæs:it3s sculon:ip3p ęrian:inf rīpan:inf mæg:ip3s',
'48.8':'gāð:m2p sęcgað:m2p gesętte:it3s bēodað:m2p cume:sp3s wunie:sp3s',
'48.9':'dōð:m2p forweorðen:sp2p',
'48.10':'gesēoð:ip2p is:ip3s hīerað:ip2p sprece:ip1s'}
manual={('44.7','nǣre'):('wesan','wesan-u18-naere-counterfactual-supplied','U18-H-44-07'),('44.7','cumen'):('cuman','cuman-u18-cumen-counterfactual-supplied','U18-H-44-07'),('48.5','clēopode'):('cleopian','cleopian-u18-marked-preterite-3-sg-supplied','U18-H-48-05')}
issues=[]
def bind(k,txt,specstring,reading=False):
 ts=re.findall(r'[^\W\d_]+(?:-[^\W\d_]+)*',txt);v=[];start=0
 for n,sp in enumerate(specstring.split(),1):
  surf,code=sp.split(':');a=analysis(code)
  pos=next((i for i in range(start,len(ts))if ts[i].lower()==surf),None)
  if pos is None:raise ValueError((k,surf,ts[start:]))
  start=pos+1
  candidates=[(lid,f,st)for lid,f,st in F if f['form'].lower()==surf and all(normalized(f['analysis']).get(ak)==av for ak,av in a.items())]
  if k=='47.11' and surf=='bīetst':candidates=[c for c in candidates if c[0]=='beodan']
  candidates.sort(key=lambda c:{'previously_taught':0,'new_production':1,'prior_recognition':2,'prior_supplied':3}.get(c[2],9))
  chosen=next((c for c in candidates if c[2]in['previously_taught','new_production']),None)
  support=None
  if (k,surf)in manual:
   lid,fid,support=manual[(k,surf)];f={'form_id':fid,'form':ts[pos],'analysis':a,'knowledge_status':'supplied','evidence_refs':['U18G-EX29','U18G-FB102']if k=='44.7'else['U18G-EX33','U18G-FB73','U18G-FB74']};st='supplied'
  elif chosen:lid,f,st=chosen
  else:
   issues.append({'item':k,'position':pos+1,'surface':ts[pos],'analysis':a,'candidates':[{ 'lemma':lid,'id':f['form_id'],'status':st,'analysis':f['analysis']}for lid,f,st in candidates]});lid=(candidates[0][0]if candidates else'UNRESOLVED');f={'form_id':'UNRESOLVED','form':ts[pos],'analysis':a};st='unresolved'
  rec={'position':pos+1,'word_position':pos+1,'token':ts[pos],'surface':ts[pos],'lemma_id':lid,'form_id':f['form_id'],'form_status':st,'knowledge_status':st,'analysis':copy.deepcopy(f['analysis']),'contextual_analysis':a,'form_record':copy.deepcopy(f),'support_id':support,'sense_id':None,'sense_status':'pending exact sense reconciliation'}
  if reading:rec['word_id']=f'U18-RWORD-{pos+1:03}'
  if len({c[0]for c in candidates if c[2]in['previously_taught','new_production']})>1:issues.append({'ambiguous_lemma':k,'surface':surf,'choices':[(c[0],c[1]['form_id'])for c in candidates]})
  v.append(rec)
 return v
out=[]
for r in rows:
 k=f"{r['exercise']}.{r['item']}";out.append({'source_item_id':r['source_item_id'],'model':r['model'],'model_version':'v10','verbal_occurrences':bind(k,r['model'],spec[k])})
D={'schema_version':1,'status':'form inventory; sense/construction reconciliation in progress','baseline':'0eda277','model_version':'v10','rows':out,'counts':{'rows':len(out),'verbal_occurrences':sum(len(r['verbal_occurrences'])for r in out)},'issues':issues}
(O/'candidate-verbal-bindings.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(D['counts']));print(json.dumps(issues,ensure_ascii=False,indent=1))
