"""Full verbal matrices; group complete command/nonfinite pairs compactly."""
from pathlib import Path
import json
R=Path.cwd();O=R/'curriculum/proposals/unit13'
def load(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def save(n,d):(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
G=load('sources/audits/unit13-grammar/grammar-records.json');D=load('curriculum/proposals/unit13/display-matrices.json')
D['matrices']=[m for m in D['matrices'] if not m.get('grammar_display')]
D['paradigm_cell_display_routes']=[x for x in D['paradigm_cell_display_routes'] if not x.get('grammar_display')]
lex={l['lemma_id']:l for l in G['lemmas']};forms={f['form_id']:f for l in G['lemmas'] for f in l.get('forms',[])}
N={'singular':'sg','plural':'pl','past':'preterite'}
def analysis(c):
    record=forms.get(c['form_id'],{});a=record.get('analysis',{})
    a=dict(a) if isinstance(a,dict) else {}
    for field in ['contextual_analysis','unit13_contextual_analysis']:
        if isinstance(record.get(field),dict):a.update(record[field])
    if isinstance(c.get('analysis'),dict):a.update(c['analysis'])
    a.update({k:c[k] for k in ['person','number','tense','mood','verb_form','nonfinite','inflection','case'] if k in c})
    return {k:N.get(v,v) if isinstance(v,str) else v for k,v in a.items()}
def kind(p):
    pid=p['paradigm_id']
    for suffix in ['IND','SUBJ','IMP','INF','PART']:
        if pid.endswith('-'+suffix):return suffix
    raise ValueError('Unclassified complete system '+pid)
groups={k:[] for k in ['IND','SUBJ','IMP','INF','PART']}
for p in G['paradigms']:groups[kind(p)].append(p)
routes=[];matrices=[];diagnostics=[];derivations=[]
weak_ii_stems={'fordilgian':'fordilg','gewunian':'gewun','ascian':'āsc','halsian':'hāls','wunian':'wun','hatian':'hat'}
weak_ii_model=next(p for p in G['paradigms'] if p['paradigm_id']=='NEW-U13-PAR-FORDILGIAN-IND')
weak_ii_derived={p['paradigm_id']:p for p in G['paradigms'] if p['lemma_id'] in weak_ii_stems and p['lemma_id']!='fordilgian' and kind(p)=='IND'}
def build(mid,title,headers,rows,cellids,statuses,ps):
    matrices.append(dict(matrix_id=mid,title=title,headers=headers,rows=rows,cell_form_ids=cellids,cell_knowledge_statuses=statuses,paradigm_ids=[p['paradigm_id'] for p in ps],evidence_refs=sorted({e for p in ps for e in p.get('evidence_refs',[])}),scope='Complete defined systems; ordinary uses and reference limits remain those of the individual diagnostic rows.',scope_by_paradigm={p['paradigm_id']:p.get('scope',p.get('scope_note')) for p in ps},grammar_display=True,display_note='Every listed form is literal; no unassigned mood, adjective inflection or lexical frame is inferred.'))
    system=kind(ps[0]);matrices[-1]['system_kind']=system
    if system in ['IND','SUBJ','IMP']:matrices[-1]['mood']={'IND':'indicative','SUBJ':'subjunctive','IMP':'imperative'}[system]
    byform={c['form_id']:(p,c) for p in ps for c in p['cells']}
    for ri,row in enumerate(cellids):
        for ci,ids in enumerate(row):
            for fid in ids:
                p,c=byform[fid]
                assert rows[ri][ci]==c['form']
                routes.append(dict(form_id=fid,paradigm_id=p['paradigm_id'],display_kind='literal',matrix_id=mid,row_index_zero_based=ri,column_index_zero_based=ci,row_label=rows[ri][0],column_label=headers[ci],grammar_display=True,operation=dict(type='literal_surface',value=c['form']),analysis=analysis(c)))

for k in ['IND','SUBJ']:
    for p in groups[k]:
        if p['paradigm_id'] in weak_ii_derived:continue
        rows=[];ids=[];statuses=[]
        for number in ['sg','pl']:
            for person in [1,2,3]:
                row=[str(person)+' '+('singular' if number=='sg' else 'plural')];rid=[[]];rs=['label']
                for tense in ['present','preterite']:
                    matches=[c for c in p['cells'] if all(analysis(c).get(key)==v for key,v in dict(number=number,person=person,tense=tense).items())]
                    assert len(matches)==1,(p['paradigm_id'],number,person,tense)
                    c=matches[0];row.append(c['form']);rid.append([c['form_id']]);rs.append(c['knowledge_status'])
                rows.append(row);ids.append(rid);statuses.append(rs)
        title=lex[p['lemma_id']]['display_headword']+' — present and preterite '+('indicative' if k=='IND' else 'subjunctive')
        build(p['paradigm_id'],title,['Person / number','Present','Preterite'],rows,ids,statuses,[p])

for k,title,headers in [('IMP','Complete singular and plural commands',['Verb','Singular','Plural']),('INF','Complete plain and inflected infinitives',['Verb','Plain infinitive','Inflected infinitive']),('PART','Complete present and past participle bases',['Verb','Present participle','Past participle'])]:
    if not groups[k]:continue
    rows=[];ids=[];statuses=[]
    for p in groups[k]:
        assert len(p['cells'])==2,(p['paradigm_id'],len(p['cells']))
        if k=='IMP':cs=sorted(p['cells'],key=lambda c:analysis(c).get('number')!='sg')
        elif k=='INF':cs=sorted(p['cells'],key=lambda c:'inflected' in c['form_id'])
        else:cs=sorted(p['cells'],key=lambda c:not ('present' in c['form_id'] or 'prespart' in c['form_id'] or analysis(c).get('tense')=='present'))
        rows.append([lex[p['lemma_id']]['display_headword']]+[c['form'] for c in cs]);ids.append([[]]+[[c['form_id']] for c in cs]);statuses.append(['label']+[c['knowledge_status'] for c in cs])
    build('NEW-U13-DISPLAY-'+k,title,headers,rows,ids,statuses,groups[k])

for p in weak_ii_derived.values():
    for c in p['cells']:
        a=analysis(c)
        matches=[mc for mc in weak_ii_model['cells'] if analysis(mc)==a]
        assert len(matches)==1,(p['paradigm_id'],a)
        mc=matches[0];model_stem=weak_ii_stems['fordilgian'];target_stem=weak_ii_stems[p['lemma_id']]
        assert mc['form'].startswith(model_stem)
        ending=mc['form'][len(model_stem):];result=target_stem+ending
        assert result==c['form'],(p['paradigm_id'],c['form'],result)
        model_route=next(r for r in routes if r['form_id']==mc['form_id'])
        pos={k:model_route[k] for k in ['matrix_id','row_index_zero_based','column_index_zero_based','row_label','column_label']}
        d=dict(form_id=c['form_id'],paradigm_id=p['paradigm_id'],target_analysis=a,model_paradigm_id=weak_ii_model['paradigm_id'],model_form_id=mc['form_id'],model_analysis=analysis(mc),model_display=pos,diagnostic_row_id='NEW-U13-CHECK-'+p['lemma_id'].upper()+'-IND',operation=dict(type='replace_lexical_stem',model_stem=model_stem,target_stem=target_stem,retained_model_ending=ending),recipe='Replace initial '+model_stem+' with '+target_stem+' in the complete displayed indicative model; retain '+ending+'.',result=result,expected_source_proposal_form=c['form'],surface_match=True,knowledge_status=c['knowledge_status'],evidence_refs=p.get('evidence_refs',[])+['U13-FB73','U13-FB74'])
        d['operation'].update(diagnostic_row_id=d['diagnostic_row_id'],diagnostic_field='diagnostic_stem',source_model_form_id=mc['form_id'],source_model_display=pos)
        d['operation']['type']='replace_initial_model_stem'
        derivations.append(d);routes.append(dict(form_id=c['form_id'],paradigm_id=p['paradigm_id'],display_kind='explicit_derivation',grammar_display=True,derivation_form_id=c['form_id'],diagnostic_row_id=d['diagnostic_row_id'],model_form_id=mc['form_id'],**pos))

for p in G['paradigms']:
    diagnostics.append(dict(paradigm_id=p['paradigm_id'],lemma_id=p['lemma_id'],headword=lex[p['lemma_id']]['display_headword'],scope=p.get('scope',p.get('scope_note')),lexical_diagnostics=[dict(form_id=c['form_id'],form=c['form'],analysis=analysis(c),knowledge_status=c['knowledge_status']) for c in p['cells']],evidence_refs=p.get('evidence_refs',[]),accepted_variants=p.get('accepted_variants',{}),display_obligation='Print the lexical rules, principal parts, stem changes, variants and ordinary frame scope with the complete matrices.'))
    diagnostics[-1]['row_id']=p['paradigm_id'].replace('NEW-U13-PAR-','NEW-U13-CHECK-')
    diagnostics[-1]['rule_ids']=sorted({forms[c['form_id']]['rule_id'] for c in p['cells'] if forms[c['form_id']].get('rule_id')})
    if p['lemma_id'] in weak_ii_stems and kind(p)=='IND':diagnostics[-1]['diagnostic_stem']=weak_ii_stems[p['lemma_id']]
    if p['paradigm_id'] in weak_ii_derived:
        diagnostics[-1].update(row_id='NEW-U13-CHECK-'+p['lemma_id'].upper()+'-IND',diagnostic_stem=weak_ii_stems[p['lemma_id']],complete_model_paradigm_id=weak_ii_model['paradigm_id'],rule_id='U13-R-WII',lexical_diagnostics=[x for x in diagnostics[-1]['lexical_diagnostics'] if x['analysis'].get('person')==3 and x['analysis'].get('number')=='sg'],display_obligation='Print the full lexical stem, third singular present and preterite, exact model reference and replace-stem rule. Every remaining indicative cell is obtained by the same explicit checked replacement; all12 routes are retained. Ordinary lexical frames remain separately taught.')
assert len(routes)==sum(len(p['cells']) for p in G['paradigms'])
D['matrices']+=matrices;D['paradigm_cell_display_routes']+=routes
D['status']='complete_nominal_and_grammar_routes_pending_independent_crosscheck'
D['grammar_counts']=dict(paradigms=len(G['paradigms']),logical_cells=len(routes),literal_cells=len(routes)-len(derivations),derived_cells=len(derivations),matrices=len(matrices),evidence_gap_positions=0)
D['counts']=dict(matrices=len(D['matrices']),logical_cells=len(D['paradigm_cell_display_routes']),literal_cells=D['nominal_counts']['literal_cells']+len(routes)-len(derivations),derived_cells=D['nominal_counts']['derived_cells']+len(derivations))
save('display-matrices.json',D);save('grammar-display-plan.json',dict(schema_version=1,chapter='ch13',status='complete',counts=D['grammar_counts'],diagnostics=diagnostics,derivations=derivations,cell_display_routes=routes,model_choice='The six audited weakII stems share one complete indicative model only after all12 cell surfaces match exact stem replacement. Every other finite system is literal; commands and nonfinite pairs are complete grouped tables.',errors=[]))
print(json.dumps(D['counts']))
