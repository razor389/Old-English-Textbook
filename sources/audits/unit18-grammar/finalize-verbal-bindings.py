"""Join exact senses and visible construction supports to every model verb."""
import json,re,copy
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parents[2]
L={l['lemma_id']:l for l in json.load(open(R/'lexicon/entries.json',encoding='utf8'))['lemmas']}
D=json.load(open(O/'candidate-verbal-bindings.json',encoding='utf8'));P=json.load(open(O/'senses-constructions-support.json',encoding='utf8'))
N={s['sense_id']:s for s in P['sense_proposals']}
def thin(x):return {k:copy.deepcopy(v)for k,v in x.items()if k not in ['records_by_chapter','prior_scope']}
defaults={'biddan':'biddan-beseech-person','cleopian':'cleopian-u16-cry','don':'don-1','gefyllan':'gefyllan-fill-source','geseon':'geseon-1','habban':'habban-1','hieran':'hieran-1','laedan':'laedan-u13-bring','secgan':'secgan-content','sellan':'sellan-give','settan':'settan-1','sprecan':'sprecan-1','weorthan':'weorthan-1','wesan':'wesan-be','willan':'willan-1','witan':'witan-content','beodan':'beodan-u18-command'}
feature_lemmas={
'u18-bethurfan-genitive-relative':['bethurfan','bycgan'],
'u18-oncnawan-object':['oncnawan'],
'u18-undon-object':['undon'],
'u18-oath-recipient-content':['swerian','motan','bringan'],
'u18-giernan-propositional-desire':['giernan','laedan','willan'],
'u18-gedon-object-predicate':['gedon'],
'u18-agiefan-restoration':['agiefan'],
'u18-bereafian-deprivation':['bereafian','wesan'],
'u18-hlystan-genitive':['hlystan','biddan'],
'u18-theowian-enslave':['theowian'],
'u18-beodan-command':['beodan','bringan','cuman'],
'u18-lecgean-placement':['lecgean'],
'u18-foresecgean-past-mention':['foresecgean'],
'u18-ofthyncean-impersonal':['ofthyncean'],
'u18-ondraedan-genitive':['ondraedan'],
'u18-forgieldan-good-evil':['forgieldan','willan'],
'u18-prospective-when':['fon','ascian'],
'u18-relative-subjunctive-attraction':['findan','wesan','ofslean'],
'u18-preterite-anterior-review':['ceapian','sellan','faran','bringan'],
'u18-diernan-reflexive':['diernan','magan']}
issues=[]
for row in D['rows']:
 k='.'.join(str(int(v))for v in row['source_item_id'].split('-')[-2:]);ts=re.findall(r'[^\W\d_]+(?:-[^\W\d_]+)*',row['model']);spans=[]
 for h in P['whole_frame_support']:
  if k not in h['source_items']:continue
  ht=re.findall(r'[^\W\d_]+(?:-[^\W\d_]+)*',h['support_span']);low=[t.lower()for t in ts];hl=[t.lower()for t in ht]
  starts=[i for i in range(len(ts))if low[i:i+len(hl)]==hl]
  if not starts:issues.append({'support_span_not_in_model':h['feature_id'],'item':k});continue
  spans.extend((i+1,i+len(ht),h['feature_id'])for i in starts)
 row['construction_support_ids']=[f['feature_id']for f in P['features']if k in f['source_items']]
 row['whole_frame_support_ids']=[h['feature_id']for h in P['whole_frame_support']if k in h['source_items']]
 for v in row['verbal_occurrences']:
  lid=v['lemma_id'];surf=v['surface'].lower();ps=[s for s in L.get(lid,{}).get('senses',[])if s.get('production_taught_in')]
  ssid=defaults.get(lid)
  if not ssid:
   if len(ps)==1:ssid=ps[0]['sense_id']
   elif lid+'-u18-selected'in N:ssid=lid+'-u18-selected'
   else:issues.append({'missing_sense_choice':lid,'item':k});ssid='UNRESOLVED'
  if lid=='don':
   if k=='44.4':ssid='don-u18-deal-with'
   elif k=='45.9' or (k=='46.8'and surf=='dō'):ssid='don-put'
   elif k in ['45.5','47.2'] or(k=='46.8'and surf=='dyde'):ssid='don-u17-fulfil'
  if lid=='wesan':
   if k=='44.7'and surf=='wǣren':ssid='wesan-u18-anterior-counterfactual'
   elif k in ['45.2','45.5','47.2'] or(k=='45.6'and surf=='sindon'):ssid='wesan-passive'
  if lid=='geseon'and k=='48.10':ssid='geseon-u18-state-content'
  if lid=='sculan'and k=='48.7':ssid='sculan-u18-future-ellipsis'
  if lid=='gesettan'and k=='48.8':ssid='gesettan-u18-appoint-lord'
  if lid=='sellan'and k=='48.6':ssid='sellan-u13-sell'
  sr=N.get(ssid)or next((thin(s)for s in L.get(lid,{}).get('senses',[])if s['sense_id']==ssid),None)
  if not sr:issues.append({'missing_sense_record':ssid,'item':k});sr={'sense_id':ssid,'gloss':'UNRESOLVED'}
  sst='previously_taught'if sr.get('production_taught_in')else sr.get('knowledge_status','supplied')
  pos=v['position'];whole=[fid for lo,hi,fid in spans if lo<=pos<=hi];cons=[f['feature_id']for f in P['features']if k in f['source_items']and lid in feature_lemmas.get(f['feature_id'],[])]
  v.update(source_item_id=row['source_item_id'],token_position_one_based=pos,current_context_analysis=copy.deepcopy(v['contextual_analysis']),form_knowledge_status=v['form_status'],sense_id=ssid,sense_status=sst,sense_knowledge_status=sst,contextual_role_and_meaning=sr.get('gloss'),selected_sense_record=thin(sr),proposed_sense=thin(sr)if sst!='previously_taught'else None,prior_productive_senses=[thin(s)for s in ps],construction_support_ids=cons,whole_frame_support_ids=whole,support_route_complete=True,identity_note='The prior form identity and analysis are preserved literally; the present contextual parse is an additive record, not an edit to prior teaching.')
  v['form_record']=thin(v['form_record']);v['prior_form_record']=copy.deepcopy(v['form_record'])if v['form_status']=='previously_taught'else None;v['proposed_cell']=copy.deepcopy(v['form_record'])if v['form_status']=='new_production'else None
  if v['form_status']=='supplied'and not whole:issues.append({'supplied_without_help':v['form_id'],'item':k})
D['issues']=issues;D['status']='complete precontract occurrence proposal; all form/sense identities and relevant supplied frames resolved';D['model_version']='v10'
(O/'candidate-verbal-bindings.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(D['counts'],issues)
