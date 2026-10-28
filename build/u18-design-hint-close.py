from pathlib import Path
import copy,json,re
O=Path('curriculum/proposals/unit18')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
inv=read(O/'inventory.json');h=read(O/'source-hint-inventory.json');lex=read('lexicon/entries.json');source=read('sources/audits/unit18-source/exercises-prompts.json');matrices=read(O/'display-matrices.json')['matrices']
lemmas={l['lemma_id']:l for l in inv['lemmas']}
for l in h['lemmas']:
 if l['lemma_id'] not in lemmas:lemmas[l['lemma_id']]=copy.deepcopy(l);inv['lemmas'].append(lemmas[l['lemma_id']])
 else:
  known={f['form_id'] for f in lemmas[l['lemma_id']]['forms']};lemmas[l['lemma_id']]['forms'] += [copy.deepcopy(f) for f in l['forms'] if f['form_id'] not in known]
forms={f['form_id']:(l['lemma_id'],f) for l in lex['lemmas']+inv['lemmas'] for f in l['forms']}
controlpath=Path('sources/audits/unit18-grammar/numeric-control-analysis.json');controls=read(controlpath).get('numeric_controls',[]) if controlpath.exists() else []
def nk(x):return re.sub(r'[^0-9a-z]','',str(x).lower())
def numbers(s):return [nk(x) for x in re.findall(r'\b\d+(?:\.\s*[a-z]|\.\s*\d+)?',s)]
issues=copy.deepcopy(h.get('unresolved',[]))
for r in h['records']:
 inside=r['literal_source_text'][1:-1].strip();exp=[];fids=set(r.get('required_feature_ids',[]));ev=set(r.get('evidence_refs',[]));keys=numbers(inside)
 if r['role']=='visible English target wording':exp.append('Use the bracketed English as the explicit target wording, preserving the complete sentence and every participant: '+inside+'.')
 elif r['role']=='visible English omission, order, number or meaning instruction':
  if inside.startswith('om.'):exp.append('Omit a separate Old English word for the marked English expression '+inside[3:].strip()+'. Preserve its grammatical relation through the surrounding selected construction.')
  elif inside=='verb last':exp.append('Put the finite verb last in this specified clause. This local composition target is not a universal Old English order rule.')
  elif inside=='plur.':exp.append('Address more than one person and select plural personal and finite forms.')
  elif inside=='neut.':exp.append('Use a neuter demonstrative for identifying this, even though the identified boy is a person; the complete identifying clause remains visible in its support.')
  elif inside=='our':exp.append('Retain the explicitly requested first-person plural possessor of the stated things; inflect the possessive with the possessed genitive plural nouns.')
  else:exp.append('Apply the exact source number or order control: '+inside+'.')
 elif r.get('hint_text'):exp.append('The exact lexical or phrase hint '+r['hint_text']+' stays visible. A copied form is a reference position; an uninflected headword must still be inflected when the requested construction requires it.')
 matched=set()
 for g in controls:
  if g['hint_id']==r['reference_id']:
   assert g['source_item_id']==r['task_id'],(g,r)
   assert g['exact_text']==r['literal_source_text'],(g,r)
   exp.append(g['visible_explanation']);ev.update(g.get('evidence_refs',[]));matched.update(keys)
   route=g.get('teaching_or_support_route')
   r['exact_numeric_control_route']=route
   if any(f['feature_id']==route for f in inv['features']):fids.add(route)
   elif any(p['paradigm_id']==route for p in inv['paradigms']):r['exact_numeric_control_paradigm_id']=route
 if keys:
  lids={forms[f][0] for f in r.get('required_form_ids',[]) if f in forms}
  current=[p for p in inv['paradigms'] if p['lemma_id'] in lids]
  prior=[l for l in lex['lemmas'] if l['lemma_id'] in lids]
  r['complete_system_routes']=[{'paradigm_id':p['paradigm_id'],'scope':p.get('scope'),'diagnostic_rule':p.get('diagnostic_rule'),'literal_matrix_ids':[m['matrix_id'] for m in matrices if p['paradigm_id'] in m['paradigm_ids']]} for p in current]
  r['prior_teaching_routes']=sorted({tid for l in prior for f in l['forms'] for tid in f.get('teaching_ids',[])})
  unresolved=[x for x in keys if x not in matched and not (x in ['43','44','47','53','102','105','113','116','131'] and (current or r['prior_teaching_routes']))]
  if unresolved:issues.append({'kind':'numeric_control_without_exact_explanation','reference_id':r['reference_id'],'numeric_keys':unresolved})
  if current:exp.append('The class/form reference is resolved by these complete literal systems and their rules: '+'; '.join(p.get('diagnostic_rule','') for p in current)+'.')
  elif r['prior_teaching_routes']:exp.append('Reuse the actual earlier complete system identified by prior_teaching_routes; the locator alone adds no form or syntactic use.')
 if not exp:exp.append('The source locator is retained exactly and resolved by the explicit current local construction explanation and form routes.')
 r['explanatory_content']=[e for e in exp if e];r['required_feature_ids']=sorted(fids);r['evidence_refs']=sorted(ev);r.setdefault('required_form_ids',[]);r.setdefault('required_sense_ids',[])
 if r.get('dependency_status')!='awaits_exact_hint_identity_join':r['dependency_status']='bound'
h['unresolved']=issues;h['status']='exact_controls_bound' if not issues else 'control_closure_pending';h['counts'].update(hint_input_sequences=len(h['sequences']),hint_input_tokens=sum(len(s['tokens']) for s in h['sequences']),pending=len(issues))
inv['teaching_records'].append({'teaching_id':'NEW-U18-SOURCE-HINTS','kind':'visible_exact_source_controls','form_ids':[f['form_id'] for l in h['lemmas'] for f in l['forms']],'knowledge_status':'supplied','description':'Retain all154 exact source controls with their explicit explanations. Copied source words are visible reference inputs, not independent lexical recall.','source_control_ids':[r['reference_id'] for r in h['records']],'evidence_refs':sorted({e for r in h['records'] for e in r['evidence_refs']}),'lesson_placement':'At each exact Cook prompt, before and during its response.'})
save(O/'inventory.json',inv);save(O/'source-hint-inventory.json',h);print(json.dumps(h['counts'],indent=2));print(json.dumps(issues,ensure_ascii=False)[:5000])
