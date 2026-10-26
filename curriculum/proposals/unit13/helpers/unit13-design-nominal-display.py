"""Complete Unit 13 nominal routes; reuse only an explicit identical family."""
from pathlib import Path
import copy, json
ROOT=Path.cwd(); OUT=ROOT/'curriculum/proposals/unit13'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def save(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
source=load('sources/audits/unit13-source/lexical-inventory.json')
pars=load('sources/audits/unit13-source/noun-adjective-paradigms.json')['paradigms']
policy=load('sources/audits/unit13-source/nominal-display-plan.json')
lemmas={l['lemma_id']:l for l in source['lemmas']}
literal=set(policy['full_matrix_lemma_ids'])

def slot(c):
    a=c['analysis'];return tuple(a.get(k) for k in ['case','number','gender','declension'])
def family(p):
    l=lemmas[p['lemma_id']]
    return l['part_of_speech'],l.get('gender'),l.get('declension_model')
def operations(p,m):
    target=lemmas[p['lemma_id']];model=lemmas[m['lemma_id']]
    ts=target.get('diagnostic_stem');ms=model.get('diagnostic_stem')
    if not isinstance(ts,str) or not isinstance(ms,str) or not ms:return None
    cells={slot(c):c for c in m['cells']}
    if set(cells)!={slot(c) for c in p['cells']}:return None
    routes={}
    for c in p['cells']:
        mc=cells[slot(c)];a=c['analysis']
        if mc['form'].startswith(ms):
            ending=mc['form'][len(ms):];result=ts+ending
            op=dict(type='replace_initial_model_stem',model_stem=ms,target_stem=ts,retained_model_ending=ending,diagnostic_field='diagnostic_stem')
        elif a['number']=='sg' and a['case'] in ['nom','acc'] and mc['form']==model['display_headword']:
            result=target['display_headword'];op=dict(type='diagnostic_headword',diagnostic_field='headword',model_cell_role='uninflected_nominative_or_accusative_singular')
        else:return None
        if result!=c['form']:return None
        routes[c['form_id']]=dict(model_cell=mc,result=result,operation=op)
    return routes

models=[];chosen=[];derivations_by={}
for p in sorted(pars,key=lambda p:(p['lemma_id'] not in literal,pars.index(p))):
    model=None;ops=None
    if p['lemma_id'] not in literal:
        for m in chosen:
            if family(p)!=family(m):continue
            candidate=operations(p,m)
            if candidate is not None:model=m;ops=candidate;break
    if model is None:model=p;chosen.append(p)
    models.append((p,model));derivations_by[p['paradigm_id']]=ops
models.sort(key=lambda pm:pars.index(pm[0]))

names={'nom':'Nominative','gen':'Genitive','dat':'Dative','acc':'Accusative','ins':'Instrumental'}
matrices=[];positions={}
for p,m in models:
    if p['paradigm_id']!=m['paradigm_id']:continue
    adj=lemmas[p['lemma_id']]['part_of_speech']=='adjective'
    declensions=list(dict.fromkeys(c['analysis'].get('declension') for c in p['cells']))
    for decl in declensions:
        cells=[c for c in p['cells'] if c['analysis'].get('declension')==decl]
        mid=p['paradigm_id']+('-'+decl.upper() if adj else '')
        slots={slot(c):c for c in cells}
        headers=['Case','Masculine singular','Feminine singular','Neuter singular','Masculine plural','Feminine plural','Neuter plural'] if adj else ['Case','Singular','Plural']
        cols=[('sg','m'),('sg','f'),('sg','n'),('pl','m'),('pl','f'),('pl','n')] if adj else [('sg',cells[0]['analysis']['gender']),('pl',cells[0]['analysis']['gender'])]
        cases=['nom','gen','dat','acc']+(['ins'] if any(c['analysis']['case']=='ins' for c in cells) else [])
        rows=[];ids=[];statuses=[]
        for ri,case in enumerate(cases):
            row=[names[case]];rid=[[]];state=['label']
            for ci,(number,gender) in enumerate(cols,1):
                c=slots.get((case,number,gender,decl))
                if c is None:
                    assert case=='ins',(mid,case,number,gender)
                    row.append('as dative');rid.append([]);state.append('reference_to_displayed_dative');continue
                row.append(c['form']);rid.append([c['form_id']]);state.append(c['knowledge_status'])
                positions[(p['paradigm_id'],c['form_id'])]=dict(matrix_id=mid,row_index_zero_based=ri,column_index_zero_based=ci,row_label=names[case],column_label=headers[ci])
            rows.append(row);ids.append(rid);statuses.append(state)
        title=p['headword']+(' — '+decl+' adjective' if adj else ' — '+{'m':'masculine','f':'feminine','n':'neuter'}[cells[0]['analysis']['gender']]+' noun')
        matrices.append(dict(matrix_id=mid,title=title,headers=headers,rows=rows,cell_form_ids=ids,cell_knowledge_statuses=statuses,paradigm_ids=[p['paradigm_id']],evidence_refs=p['evidence_refs'],scope=p.get('scope_note',p.get('scope')),display_note='Every assigned cell is literal here. Reference number and instrumental cells retain their explicit limits; they establish no additional sense or use.'))

routes=[];derived=[]
for p,m in models:
    pid=p['paradigm_id'];mid=m['paradigm_id']
    for c in p['cells']:
        if pid==mid:
            routes.append(dict(form_id=c['form_id'],paradigm_id=pid,display_kind='literal',**positions[(pid,c['form_id'])],operation=dict(type='literal_surface',value=c['form'])));continue
        item=derivations_by[pid][c['form_id']];mc=item['model_cell'];pos=positions[(mid,mc['form_id'])]
        op={**item['operation'],'source_model_form_id':mc['form_id'],'source_model_display':pos,'diagnostic_row_id':'NEW-U13-DIAG-'+p['lemma_id'].upper()}
        recipe='Use the complete diagnostic headword in this uninflected singular position.' if op['type']=='diagnostic_headword' else 'Replace '+op['model_stem']+' with '+op['target_stem']+' in the displayed model; retain ending '+(op['retained_model_ending'] or '∅')+'.'
        d=dict(form_id=c['form_id'],paradigm_id=pid,target_analysis=c['analysis'],model_paradigm_id=mid,model_form_id=mc['form_id'],model_analysis=mc['analysis'],model_display=pos,diagnostic_row_id=op['diagnostic_row_id'],operation=op,recipe=recipe,result=item['result'],expected_source_proposal_form=c['form'],surface_match=True,knowledge_status=c['knowledge_status'],evidence_refs=c['evidence_refs'])
        derived.append(d);routes.append(dict(form_id=c['form_id'],paradigm_id=pid,display_kind='explicit_derivation',derivation_form_id=c['form_id'],diagnostic_row_id=d['diagnostic_row_id'],model_form_id=mc['form_id'],**pos))

diagnostics=[]
for p,m in models:
    l=lemmas[p['lemma_id']]
    diagnostics.append(dict(row_id='NEW-U13-DIAG-'+l['lemma_id'].upper(),lemma_id=l['lemma_id'],headword=l['display_headword'],part_of_speech=l['part_of_speech'],gender=l.get('gender'),lexical_model=l['declension_model'],diagnostic_stem=l.get('diagnostic_stem'),diagnostic_forms=l.get('diagnostic_forms',{}),paradigm_ids=[p['paradigm_id']],printed_model_ids=[x['matrix_id'] for x in matrices if m['paradigm_id'] in x['paradigm_ids']],cell_routes=[c['form_id'] for c in p['cells']],scope_notes=[p.get('scope_note',p.get('scope'))],accepted_variants=l.get('accepted_variants',{}),source_headword=l.get('source_headword'),headword_origin=l.get('headword_origin'),headword_change_note=l.get('headword_change_note'),evidence_refs=l['evidence_refs'],display_obligation='Print the full stem, required diagnostic forms, model references, stem rules, accepted variants and recognition limits beside the model tables.'))
counts=dict(paradigm_count=len(pars),logical_cells=sum(len(p['cells']) for p in pars),matrices=len(matrices),literal_cells=len(routes)-len(derived),derived_cells=len(derived),diagnostic_rows=len(diagnostics))
assert len(routes)==counts['logical_cells']
assert len({(r['paradigm_id'],r['form_id']) for r in routes})==len(routes)
save('nominal-display-plan.json',dict(schema_version=1,chapter='ch13',status='complete_nominal_routes_pending_independent_crosscheck',counts=counts,source='sources/audits/unit13-source/noun-adjective-paradigms.json',selection_rationale='The audit’s required full systems are literal. Sharing is restricted to identical audited family and complete slots, using a visible model and exact checked lexical stem. Every cell must reproduce the audited surface; failures retain complete literal matrices. Combined strong/weak logical systems have visibly separate matrices.',model_choices=[dict(paradigm_id=p['paradigm_id'],model_paradigm_id=m['paradigm_id']) for p,m in models],diagnostic_rows=diagnostics,derivations=derived,cell_display_routes=routes))
save('display-matrices.json',dict(schema_version=1,chapter='ch13',status='nominal_complete_grammar_pending',origin='Literal full models and complete explicit same-family derivations; scope and rules remain independently evidenced.',nominal_counts=counts,matrices=matrices,paradigm_cell_display_routes=routes))
print(json.dumps(counts))
