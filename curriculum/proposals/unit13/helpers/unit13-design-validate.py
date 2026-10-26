"""Concrete repeated integrity checks for the reconciled Unit 13 design."""
from pathlib import Path
from collections import Counter
import copy,hashlib,json
R=Path.cwd();O=R/'curriculum/proposals/unit13'
def load(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def save(n,d):(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
I=load('curriculum/proposals/unit13/inventory.json');TP=load('curriculum/proposals/unit13/task-plan.json');C=load('curriculum/proposals/unit13/compositions.json');V=load('curriculum/proposals/unit13/validation.json')
issues=V['issues'];checks=[]
def check(ok,label,**detail):
    checks.append(dict(check=label,passed=bool(ok),**detail))
    if not ok:issues.append(dict(check=label,**detail))
L=load('lexicon/entries.json');G=load('curriculum/grammar.json')
prior={'forms':{f['form_id']:{**f,'lemma_id':l['lemma_id']} for l in L['lemmas'] for f in l['forms']},'senses':{s['sense_id']:{**s,'lemma_id':l['lemma_id']} for l in L['lemmas'] for s in l['senses']},'features':{f['feature_id']:f for f in G['features']}}
records=copy.deepcopy(prior)
for l in I['lemmas']:
    for kind in ['forms','senses']:
        for r in l[kind]:records[kind][r[kind[:-1]+'_id']]={**r,'lemma_id':l['lemma_id']}
for f in I['features']:records['features'][f['feature_id']]=f
tasks=TP['tasks'];ids=[t['task_id'] for t in tasks]
check(len(ids)==len(set(ids))==90,'90 unique task IDs',count=len(ids))
check(len({t['key_id'] for t in tasks})==90,'90 separate key IDs')
prompts=load('sources/audits/unit13-source/exercises-prompts.json')['items'];byid={t['task_id']:t for t in tasks}
check(len(prompts)==52 and all(p['item_id'] in byid and p['prompt']==byid[p['item_id']]['prompt'] for p in prompts),'all 52 original prompts preserved exactly')
check(Counter(p['exercise'] for p in prompts)=={22:15,23:13,24:12,25:12},'complete original exercise groups')
private=load('curriculum/proposals/unit13/author-only-sequence-bindings.json')['sequences']+load('curriculum/proposals/unit13/author-only-cook-sequence-bindings.json')['sequences']
public=load('curriculum/proposals/unit13/public-sequence-bindings.json')['sequences']
for seq in public+private:
    check(len(seq['text'].split())==len(seq['tokens']),'every sequence word is bound',sequence_id=seq['sequence_id'])
    for token in seq['tokens']:
        for kind,key in [('forms','form_id'),('senses','sense_id')]:
            if token[key] not in records[kind]:issues.append(dict(sequence_id=seq['sequence_id'],missing=token[key]))
        if token['form_id'] in records['forms']:
            f=records['forms'][token['form_id']]
            if f['form'].casefold()!=token['surface'].casefold():issues.append(dict(sequence_id=seq['sequence_id'],surface=token['surface'],form_id=token['form_id'],registered=f['form']))
for reading in I['readings']:
    check(len(reading['tokens'])==reading['word_count_whitespace']==236,'236 source word tokens',span=reading['source_span_id'])
    check(' '.join(t['literal'] for t in reading['tokens'])==' '.join(reading['exact_text_without_note_cues'].split()),'source literal sequence preserved')
    check(all('referent' not in t for t in reading['tokens']),'public source bindings exclude answer-like referent fields')
check(len(C['teaching_examples'])==12 and len(C['compositions'])==1 and C['compositions'][0]['word_count']==87,'12 examples and connected 87-word new account')
check(len(I['source_evidence_examples'])==1 and len(I['source_evidence_examples'][0]['tokens'])==4,'separate four-token corroborative source fragment')
allslots=[p['output_position_id'] for t in tasks for p in t['requested_output_positions']]
check(len(allslots)==len(set(allslots)) and all(t['requested_output_positions'] for t in tasks),'all requested output positions have unique IDs',count=len(allslots))
models=load('curriculum/proposals/unit13/author-only-model-seed.json')['models']
check(sum(len(m.get('morphological_outputs',[])) for m in models)==101,'101 explicit morphology output bindings')
for t in tasks:
    for name,kind in [('form','forms'),('sense','senses'),('feature','features')]:
        req=t['required_'+name+'_ids'];sup=t['supplied_'+name+'_ids'];tested=t['tested_'+name+'_ids']
        check(set(sup).isdisjoint(tested),'supplied records excluded from recall targets',task_id=t['task_id'],record_type=kind)
        for rid in req:
            if rid not in records[kind]:issues.append(dict(task_id=t['task_id'],missing_id=rid,record_type=kind))
        covered={rid for h in t['local_support'] for rid in h.get(name+'_ids',[])}
        missing=set(sup)-covered
        if missing:issues.append(dict(task_id=t['task_id'],missing_visible_support=sorted(missing),record_type=kind))
        for rid in t.get('required_output_'+name+'_ids',[]):
            r=records[kind].get(rid,{})
            status=r.get('knowledge_status')
            productive=r.get('production_taught_in') or status in ['new_production','previously_taught']
            if not productive and rid not in sup:issues.append(dict(task_id=t['task_id'],unsupported_output=rid,record_type=kind,status=status))
for kind,reqs in I['prior_requirements'].items():
    for r in reqs:
        if prior[kind].get(r['id'])!=r['actual_prior_record']:issues.append(dict(prior_record_changed=r['id'],record_type=kind))
        if not r['used_in_tasks']:issues.append(dict(unused_prior_requirement=r['id']))
        if r['current_supplied_in_tasks'] and not r['current_support_teaching_ids']:issues.append(dict(prior_supplied_without_current_teaching=r['id']))
    for rid,r in records[kind].items():
        if rid not in prior[kind]:continue
        for fld in ['form','analysis'] if kind=='forms' else ['gloss'] if kind=='senses' else []:
            if r.get(fld)!=prior[kind][rid].get(fld):issues.append(dict(prior_identity_rewritten=rid,field=fld))
pars=I['paradigms'];routes=I['display_plan']['paradigm_cell_display_routes'];cells={(p['paradigm_id'],c['form_id']):c for p in pars for c in p['cells']}
check(len(cells)==len(routes)==1008 and set(cells)=={(r['paradigm_id'],r['form_id']) for r in routes},'complete route for every one of 1008 cells')
mat={m['matrix_id']:m for m in I['display_plan']['matrices']};derivs={d['form_id']:d for d in I['display_plan']['nominal_derivations']+I['display_plan'].get('grammar_derivations',[])}
diags={d['row_id']:d for d in I['display_plan']['lexical_diagnostics']}
for route in routes:
    m=mat[route['matrix_id']];display=m['rows'][route['row_index_zero_based']][route['column_index_zero_based']];cell=cells[(route['paradigm_id'],route['form_id'])]
    if route['display_kind']=='literal':result=display
    else:
        d=derivs[route['form_id']];op=d['operation'];diag=diags[d['diagnostic_row_id']]
        if op['type']=='diagnostic_headword':result=diag['headword']
        else:
            check(display.startswith(op['model_stem']),'displayed model starts with stated stem',form_id=route['form_id'])
            result=diag[op['diagnostic_field']]+display[len(op['model_stem']):]
            check(display[len(op['model_stem']):]==op['retained_model_ending'],'retained model ending verified',form_id=route['form_id'])
        check(result==d['result'],'derivation recipe matches recorded result',form_id=route['form_id'])
    if result!=cell['form']:issues.append(dict(displayed_form_mismatch=route['form_id'],actual=result,expected=cell['form']))
check(len(mat)==43 and len(derivs)==446,'economical complete display counts',matrices=len(mat),derived_cells=len(derivs))
for evidence in I['evidence_catalog'].values():
    path=evidence.get('image_path');expected=evidence.get('image_sha256')
    if path and expected:
        p=R/path
        if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:issues.append(dict(evidence_image_changed=evidence.get('evidence_id'),path=path))
lemma_ids={l['lemma_id'] for l in L['lemmas']+I['lemmas']}
owners=set(ids)|{r['source_span_id'] for r in I['readings']}|{e['example_id'] for e in C['teaching_examples']+I['source_evidence_examples']}|{c['composition_id'] for c in C['compositions']}
for frame in I['lexical_frames']:
    for lid in frame.get('lemma_ids',[]):
        if lid not in lemma_ids:issues.append(dict(frame_id=frame['frame_id'],missing_lemma_id=lid))
    for owner in frame.get('used_in_tasks',[]):
        if owner not in owners:issues.append(dict(frame_id=frame['frame_id'],unknown_task_usage=owner))
def evidence_refs(value):
    if isinstance(value,dict):
        for key,item in value.items():
            if key=='evidence_refs' and isinstance(item,list):yield from item
            elif key not in ['actual_prior_record','prior_history','records_by_chapter']:yield from evidence_refs(item)
    elif isinstance(value,list):
        for item in value:yield from evidence_refs(item)
prior_evidence=set(evidence_refs(L))|set(evidence_refs(G))
needed=set(evidence_refs(I))|set(evidence_refs(TP))|set(evidence_refs(C))
unknown=needed-set(I['evidence_catalog'])-prior_evidence
check(not unknown,'every evidence reference resolves to checked current or actual prior evidence',unknown=sorted(unknown))
audit=load('curriculum/proposals/unit13/prior-audit.json')
for entry in audit['registers']+audit['earlier_contracts']:
    path=entry.get('path');expected=entry.get('sha256')
    if path and expected:check(hashlib.sha256((R/path).read_bytes()).hexdigest()==expected,'prior audited artifact unchanged',path=path)
required_exclusions=['sources/audits/unit13-coordinator/author-only-source-first.md','sources/audits/unit13-source/reading-tokens.json','curriculum/proposals/unit13/author-only-cook-sequence-bindings.json']
check(all(p in I['pre_key_review_exclusions'] for p in required_exclusions),'explicit blind-review exclusions retained')
V.update(status='pass' if not issues else 'pending',issues=issues,checks=checks,counts={**V['counts'],'requested_output_positions':len(allslots),'morphology_output_positions':101,'display_matrices':len(mat),'literal_display_cells':len(routes)-len(derivs),'derived_display_cells':len(derivs)},review_basis=['sources/audits/unit13-source/nominal-display-review.json','sources/audits/unit13-grammar/public-composition-review.json','sources/audits/unit13-grammar/validation.json'])
save('validation.json',V)
for name in ['inventory.json','task-plan.json','compositions.json']:
    d=load('curriculum/proposals/unit13/'+name);d['status']='reconciled_pre_contract_design' if not issues else 'pre_contract_design_pending_reconciliation';save(name,d)
print(json.dumps(dict(checks=len(checks),issues=len(issues),sample=issues[:15],counts=V['counts']),ensure_ascii=False))
