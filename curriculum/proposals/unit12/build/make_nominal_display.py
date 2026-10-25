"""Complete nominal displays with auditable shared-family stem substitution."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];OUT=ROOT/'curriculum/proposals/unit12'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def write(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
source=load('sources/audits/unit12-source/lexical-inventory.json')
pars=load('sources/audits/unit12-source/noun-adjective-paradigms.json')['paradigms']
lemmas={l['lemma_id']:l for l in source['lemmas']}
byid={p['paradigm_id']:p for p in pars}
def slot(c):
 a=c['analysis'];return(a['case'],a['number'],a.get('gender'),a.get('declension'))
def diagnostic(p):return lemmas[p['lemma_id']]
def family(p):
 l=diagnostic(p);return(l['part_of_speech'],l.get('gender'),l['declension_model'],p['cells'][0]['analysis'].get('declension'))
def operations(target,model):
 """Every source cell must be reproduced; a failing family remains literal."""
 tl=diagnostic(target);ml=diagnostic(model);ms=ml.get('diagnostic_stem');ts=tl.get('diagnostic_stem')
 if not isinstance(ms,str) or not ms or not isinstance(ts,str):return None
 mc={slot(c):c for c in model['cells']};result={}
 if set(mc)!={slot(c) for c in target['cells']}:return None
 for c in target['cells']:
  m=mc[slot(c)];a=c['analysis']
  if m['form'].startswith(ms):
   ending=m['form'][len(ms):];surface=ts+ending
   op={'type':'replace_initial_model_stem','model_stem':ms,'target_stem':ts,'diagnostic_field':'diagnostic_stem','retained_model_ending':ending,'ending_operation':'take_literal_model_surface_suffix_after_exact_initial_model_stem'}
  elif a['case']=='nom' and a['number']=='sg' and m['form']==ml['display_headword']:
   surface=tl['display_headword'];op={'type':'diagnostic_headword','diagnostic_field':'headword','model_cell_role':'nominative_singular_uses_full_headword'}
  else:return None
  if surface!=c['form']:return None
  result[c['form_id']]={'model_cell':m,'result':surface,'operation':op}
 return result

# Fresh exceptional systems are always literal; other words share only an
# audited declension family, identical complete slots and checked surfaces.
always_literal={'fot','brycg','here','ethel'}
models=[];chosen=[];plans={}
for p in sorted(pars,key=lambda p:(p['lemma_id'] not in always_literal,pars.index(p))):
 selected=None;ops=None
 if p['lemma_id'] not in always_literal:
  for model in chosen:
   if family(p)!=family(model):continue
   candidate=operations(p,model)
   if candidate is not None:selected=model;ops=candidate;break
 if selected is None:selected=p;chosen.append(p)
 models.append((p,selected['paradigm_id']));plans[p['paradigm_id']]=ops
models.sort(key=lambda x:pars.index(x[0]))
case_names={'nom':'Nominative','gen':'Genitive','dat':'Dative','acc':'Accusative','ins':'Instrumental'}
matrices=[];positions={}
for p,mid in models:
 if p['paradigm_id']!=mid:continue
 adj=p['cells'][0]['analysis'].get('declension') in ['strong','weak']
 slots={slot(c):c for c in p['cells']};decl=p['cells'][0]['analysis'].get('declension')
 headers=['Case','Masculine singular','Feminine singular','Neuter singular','Masculine plural','Feminine plural','Neuter plural'] if adj else ['Case','Singular','Plural']
 cols=[('sg','m'),('sg','f'),('sg','n'),('pl','m'),('pl','f'),('pl','n')] if adj else [('sg',p['cells'][0]['analysis']['gender']),('pl',p['cells'][0]['analysis']['gender'])]
 rows=[];ids=[];states=[]
 for ri,case in enumerate(['nom','gen','dat','acc','ins'] if adj else ['nom','gen','dat','acc']):
  row=[case_names[case]];ir=[[]];sr=['label']
  for ci,(number,gender) in enumerate(cols,1):
   c=slots.get((case,number,gender,decl))
   if c is None:
    assert case=='ins',(mid,case,number,gender)
    row.append('as dative');ir.append([]);sr.append('reference_to_displayed_dative')
   else:
    row.append(c['form']);ir.append([c['form_id']]);sr.append(c['knowledge_status'])
    positions[(mid,c['form_id'])]={'matrix_id':mid,'row_index_zero_based':ri,'column_index_zero_based':ci,'row_label':case_names[case],'column_label':headers[ci]}
  rows.append(row);ids.append(ir);states.append(sr)
 title=p['headword']+(' — '+decl+' adjective' if adj else ' — '+{'m':'masculine','f':'feminine','n':'neuter'}.get(p['cells'][0]['analysis']['gender'],'')+' noun')
 matrices.append({'matrix_id':mid,'title':title,'headers':headers,'rows':rows,'cell_form_ids':ids,'cell_knowledge_statuses':states,'paradigm_ids':[mid],'evidence_refs':p['evidence_refs'],'scope':p.get('scope_note',p.get('scope')),'display_note':'Every assigned morphology cell is literal. Instrumental reference positions retain their status and point to the visible dative counterpart.' if adj else 'Full nominative, genitive, dative and accusative singular/plural. Reference number cells retain their labeled scope.'})
routes=[];derivations=[]
for p,mid in models:
 for c in p['cells']:
  if p['paradigm_id']==mid:
   routes.append({'form_id':c['form_id'],'paradigm_id':p['paradigm_id'],'display_kind':'literal',**positions[(mid,c['form_id'])]});continue
  item=plans[p['paradigm_id']][c['form_id']];mc=item['model_cell'];pos=positions[(mid,mc['form_id'])]
  op={**item['operation'],'source_model_form_id':mc['form_id'],'source_model_display':pos,'diagnostic_row_id':'NEW-U12-DIAG-'+p['lemma_id'].upper()}
  recipe=('Use the full diagnostic headword in the model’s nominative-singular position.' if op['type']=='diagnostic_headword' else 'Replace the displayed model stem '+op['model_stem']+' with diagnostic stem '+op['target_stem']+'; retain ending '+(op['retained_model_ending'] or '∅')+'.')
  d={'form_id':c['form_id'],'paradigm_id':p['paradigm_id'],'target_analysis':c['analysis'],'model_paradigm_id':mid,'model_form_id':mc['form_id'],'model_analysis':mc['analysis'],'model_display':pos,'diagnostic_row_id':op['diagnostic_row_id'],'operation':op,'recipe':recipe,'result':item['result'],'expected_source_proposal_form':c['form'],'surface_match':True,'knowledge_status':c['knowledge_status'],'evidence_refs':c['evidence_refs']}
  derivations.append(d);routes.append({'form_id':c['form_id'],'paradigm_id':p['paradigm_id'],'display_kind':'explicit_derivation','derivation_form_id':c['form_id'],'diagnostic_row_id':d['diagnostic_row_id'],'model_form_id':mc['form_id'],**pos})
diagnostics=[]
for lid in dict.fromkeys(p['lemma_id'] for p in pars):
 l=lemmas[lid];ps=[p for p in pars if p['lemma_id']==lid]
 diagnostics.append({'row_id':'NEW-U12-DIAG-'+lid.upper(),'lemma_id':lid,'headword':l['display_headword'],'part_of_speech':l['part_of_speech'],'gender':l.get('gender'),'lexical_model':l['declension_model'],'diagnostic_stem':l.get('diagnostic_stem'),'diagnostic_forms':l.get('diagnostic_forms',{}),'paradigm_ids':[p['paradigm_id'] for p in ps],'printed_model_ids':sorted({m for p,m in models if p['lemma_id']==lid}),'cell_routes':[r['form_id'] for r in routes if r['paradigm_id'] in [p['paradigm_id'] for p in ps]],'scope_notes':[p.get('scope_note',p.get('scope')) for p in ps],'accepted_variants':{p['paradigm_id']:p.get('accepted_variants',{}) for p in ps},'evidence_refs':l['evidence_refs'],'display_obligation':'Print all diagnostic stems, exceptional forms, accepted variants and model references beside the shared tables.'})
counts={'paradigm_count':len(pars),'logical_cells':sum(len(p['cells']) for p in pars),'matrices':len(matrices),'literal_cells':len(routes)-len(derivations),'derived_cells':len(derivations),'diagnostic_rows':len(diagnostics)}
write('nominal-display-plan.json',{'schema_version':1,'chapter':'ch12','status':'source_nominal_display_reconciled_pending_grammar','counts':counts,'source':'sources/audits/unit12-source/noun-adjective-paradigms.json','selection_rationale':'New fōt, brycg, hęre and ēðel systems are literal. Further sharing is confined to the source-audited declension family, identical complete slots, explicit diagnostic stems and exact successful surface derivation for every cell. Every failed match remains a literal full table. The final recorded model choices are individually reviewed.','model_choices':[{'paradigm_id':p['paradigm_id'],'model_paradigm_id':mid} for p,mid in models],'diagnostic_rows':diagnostics,'derivations':derivations,'cell_display_routes':routes})
write('display-matrices.json',{'schema_version':1,'chapter':'ch12','status':'nominal_complete_verb_addition_pending','origin':'Every logical morphology cell is literal or explicitly derived from one visible same-family model and diagnostic stem.','nominal_counts':counts,'matrices':matrices,'paradigm_cell_display_routes':routes})
print(json.dumps(counts))
