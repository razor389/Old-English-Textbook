"""Consolidate reusable audit interfaces without ordered learner answers."""
import copy,json,re
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[2]
def read(path):return json.loads((R/path).read_text(encoding='utf8'))
def write(name,obj):(P/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
gram=read('sources/audits/unit14-grammar/source-support.json')
nom=read('sources/audits/unit14-source/source-support-records.json')
reader=read('sources/audits/unit14-source/reading-token-ledger.json')
rs=read('sources/audits/unit14-source/reading-support.json')
models=read('sources/audits/unit14-source/author-only-cook-models.json')
deps=read('sources/audits/unit14-source/exercises-dependencies.json')
vdeps={x['item_id']:x for x in read('sources/audits/unit14-grammar/exercises-verbal-dependencies.json')['items']}
def normalize(h):
 h=copy.deepcopy(h)
 h.setdefault('form_ids',sorted({b['form_id'] for b in h.get('bindings',[]) if b.get('form_id')}))
 h.setdefault('sense_ids',sorted({b['sense_id'] for b in h.get('bindings',[]) if b.get('sense_id')}))
 h.setdefault('construction_ids',[h['feature_id']] if h.get('feature_id') else [])
 h['covers']={'form_ids':h['form_ids'],'sense_ids':h['sense_ids'],'construction_ids':h['construction_ids']}
 return h
rhelps=[]
for h in rs['lexical_help']:
 t=[reader['tokens'][i-1] for i in h['token_indices']]
 h['evidence_refs']=sorted({e for row in t for e in row['evidence_refs']})
 h['used_in_tasks']=['FB-VIII-DANGERS-OPENING-ARGUMENT']
 h['analyses']=[{'form':row['source_surface'].strip('.,;'),'analysis':row['analysis']} for row in t]
 h['text']='; '.join(dict.fromkeys(row['source_surface'].strip('.,;')+' — '+row['gloss']+(' ('+row['analysis']['source_analysis']+')' if 'source_analysis' in row['analysis'] else '') for row in t))
 rhelps.append(normalize(h))
rhelps += [normalize(h) for h in gram['reading_support']]
rs['supports']=rhelps
rs['interface_note']='supports is the normalized combined array. covers repeats form_ids/sense_ids/construction_ids as a keyed object for consumers; original lexical_help/grammar_help remain for provenance.'
write('reading-support.json',rs)

chelps=[normalize(h) for h in gram['cook_support']]
for l in nom['lemmas']:
 uses=[(item['source_item_id'],t) for item in models['items'] for t in item['tokens'] if t['lemma_id']==l['lemma_id'] and ('supplied' in [t['form_status'],t['sense_status']])]
 if not uses:continue
 h={'support_id':'U14-COOK-LEX-'+l['lemma_id'].upper(),'kind':'lexical_help','title':l['display_headword'],'text':'; '.join(dict.fromkeys(t['surface']+' — '+t['gloss']+(' ('+t['analysis']['source_analysis']+')' if 'source_analysis' in t['analysis'] else '') for iid,t in uses)),'form_ids':sorted({t['form_id'] for iid,t in uses}),'sense_ids':sorted({t['sense_id'] for iid,t in uses}),'evidence_refs':sorted({e for iid,t in uses for e in t['evidence_refs']}),'used_in_tasks':sorted({iid for iid,t in uses}),'scope':'Printed exact local aid; no independent recall of the supplied dependency is required.'}
 chelps.append(normalize(h))
write('cook-local-support.json',{'schema_version':1,'supports':chelps,'policy':'Supplied forms, senses and constructions must be printed beside or directly accessible from the listed Cook items. They are not independent recall targets. Full ordered models remain author-only.'})

# Bind every source item to the same models and unordered requirements.
constructions=[]
for item in deps['items']:
 iid=item['source_item_id'];v=vdeps[iid]
 relevant=[h for h in chelps if iid in h.get('used_in_tasks',[])]
 ids=sorted(set(v.get('required_feature_ids',[])+[c for h in relevant for c in h['construction_ids']]))
 item['required_feature_ids']=ids
 item['local_support_ids']=sorted({h['support_id'] for h in relevant})
 item['targets']=v['targets']
 item['source_control_notes']=v['original_controls_and_interpretation']
 constructions.append({'item_id':iid,'source_item_id':iid,'required_feature_ids':ids,'requirements':v.get('grammar_requirements',[]),'local_support_ids':item['local_support_ids'],'source_controls':item['source_control_notes'],'unresolved':[]})
write('exercises-dependencies.json',deps)
write('construction-requirements.json',{'schema_version':1,'items':constructions,'scope':'Existing/new/supplied construction references from the independent grammar packet; morphology and senses are separately enumerated in exercises-dependencies.json.'})
prompts=read('sources/audits/unit14-source/exercises-prompts.json')
dmap={i['source_item_id']:i for i in deps['items']}
items=[]
for p in prompts['items']:
 d=dmap[p['source_item_id']]
 item={**p,'item_id':p['source_item_id'],'disposition':'assigned','dependency_audit_ref':'exercises-dependencies.json#'+p['source_item_id'],'required_form_ids':d['required_form_ids'],'required_sense_ids':d['required_sense_ids'],'required_feature_ids':d['required_feature_ids'],'local_support_ids':d['local_support_ids'],'original_controls_and_interpretation':d['source_control_notes'],'model_ref':'author-only-cook-models.json#'+p['source_item_id'],'correction_ids':(['C01'] if p['source_item_id']=='EX-VIII-26-06' else ['C04'] if p['source_item_id']=='EX-VIII-27-04' else []),'unresolved':[]}
 items.append(item)
write('items.json',{'schema_version':1,'source_items':items,'count':21,'exercise_counts':{'VIII.26':10,'VIII.27':11},'all_original_prompts_retained':True,'reading':{'source_span_id':'FB-VIII-DANGERS-OPENING-ARGUMENT','disposition':'assigned','source_ref':'reading-source.json','tokens_ref':'reading-token-ledger.json','support_ref':'reading-support.json','apparatus_ref':'reading-apparatus.json','correction_ids':['C05'],'unresolved':[]}})

def coverage(rows,helps,where):
 f={f for h in helps for f in h['form_ids']};s={s for h in helps for s in h['sense_ids']}
 return [where+':'+str(t.get('token_id'))+':'+kind+':'+t[kind+'_id'] for t in rows for kind,covered in [('form',f),('sense',s)] if t[kind+'_status']=='supplied' and t[kind+'_id'] not in covered]
gaps=coverage(reader['tokens'],rhelps,'reading')+coverage([t for i in models['items'] for t in i['tokens']],chelps,'cook')
write('support-coverage-check.json',{'schema_version':1,'reading_tokens':159,'cook_tokens':models['token_count'],'reading_help_groups':len(rhelps),'cook_help_groups':len(chelps),'uncovered_supplied_dependencies':gaps,'passes':not gaps})
print({'reading_help_groups':len(rhelps),'cook_help_groups':len(chelps),'gaps':gaps})
