"""Literal complete matrices for the exact new verbal systems."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];OUT=ROOT/'curriculum/proposals/unit12'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def write(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
g=load('sources/audits/unit12-grammar/grammar-records.json');d=load('curriculum/proposals/unit12/display-matrices.json')
d['matrices']=[m for m in d['matrices'] if not m.get('grammar_display')]
d['paradigm_cell_display_routes']=[r for r in d['paradigm_cell_display_routes'] if not r.get('grammar_display')]
forms={f['form_id']:f for l in g['lemmas'] for f in l.get('forms',[])}
headwords={l['lemma_id']:l['display_headword'] for l in g['lemmas']}
class_labels={'adrifan':'strong verb','gehatan':'strong verb','fleon':'contracted strong verb','gemetan':'weak verb','geopenian':'weak verb','gretan':'weak verb','cythan':'weak verb','ehtan':'weak verb','agan':'preterite-present verb','leornian':'weak verb','sendan':'weak verb','bringan':'mixed verb','weorpan':'strong verb','gewyrcean':'weak verb','gierwan':'weak verb','settan':'weak verb','gewitan':'strong verb','sittan':'strong verb','geneosian':'weak verb'}
class_labels['risan']='strong verb'
diagnostics=[];errors=[];seen=set()
for p in g['paradigms']:
    pid=p['paradigm_id'];cells=p['cells'];rows=[];ids=[];states=[]
    def analysis(c):return {**forms[c['form_id']].get('analysis',{}),**c.get('analysis',{}),**{k:v for k,v in c.items() if k in ['person','number','tense','mood','verb_form']}}
    if pid.endswith('-IND'):
        headers=['Person / number','Present','Preterite']
        for number in ['sg','pl']:
            for person in [1,2,3]:
                row=[str(person)+' '+('singular' if number=='sg' else 'plural')];rid=[[]];rs=['label']
                for tense in ['present','preterite']:
                    hits=[c for c in cells if analysis(c).get('person')==person and analysis(c).get('number')==number and analysis(c).get('tense')==tense]
                    assert len(hits)==1,(pid,person,number,tense,hits)
                    c=hits[0];row.append(c['form']);rid.append([c['form_id']]);rs.append(c['knowledge_status'])
                rows.append(row);ids.append(rid);states.append(rs)
    elif pid.endswith('-IMP'):
        headers=['Addressee','Command']
        for number in ['sg','pl']:
            hits=[c for c in cells if analysis(c).get('number')==number];assert len(hits)==1,(pid,number,hits)
            c=hits[0];rows.append(['Singular' if number=='sg' else 'Plural',c['form']]);ids.append([[],[c['form_id']]]);states.append(['label',c['knowledge_status']])
    elif pid.endswith('-PASSIVE-PRED'):
        headers=['Predicate form','Past participle']
        assert len(cells)==2,(pid,len(cells))
        for c in cells:
            label='Plural -e variant' if c['form_id'].endswith('pred-pl') else 'Uninflected base'
            rows.append([label,c['form']]);ids.append([[],[c['form_id']]]);states.append(['label',c['knowledge_status']])
    elif pid.endswith('-PART') or 'INF' in pid:
        headers=['Form','Base' if pid.endswith('-PART') else 'Infinitive']
        assert len(cells)==2,(pid,len(cells))
        for c in cells:
            a=analysis(c);ispart=pid.endswith('-PART')
            label=('Present participle' if 'pres' in c['form_id'] else 'Past participle') if ispart else ('Inflected infinitive' if 'inflected' in c['form_id'] else 'Plain infinitive')
            rows.append([label,c['form']]);ids.append([[],[c['form_id']]]);states.append(['label',c['knowledge_status']])
    else:raise ValueError('Unplanned verbal paradigm '+pid)
    scope=p.get('scope',p.get('scope_note',''))
    system_label='present and preterite indicative' if pid.endswith('-IND') else 'singular and plural commands' if pid.endswith('-IMP') else 'present and past participle bases' if pid.endswith('-PART') else 'plain and inflected infinitives'
    title=headwords[p['lemma_id']]+' — '+class_labels[p['lemma_id']]+': '+system_label
    matrix={'matrix_id':pid,'title':title,'headers':headers,'rows':rows,'cell_form_ids':ids,'cell_knowledge_statuses':states,'paradigm_ids':[pid],'evidence_refs':p['evidence_refs'],'scope':scope,'grammar_display':True,'display_note':'All cells in this precisely defined system are literal. Participle bases do not assign unlisted adjective cells or compound tense uses. Recognition cells remain reference.'}
    d['matrices'].append(matrix)
    for ri,row in enumerate(ids):
        for ci,cellids in enumerate(row):
            for fid in cellids:
                if (pid,fid) in seen:errors.append({'duplicate_display_route':[pid,fid]})
                seen.add((pid,fid))
                if rows[ri][ci]!=forms[fid]['form']:errors.append({'display_surface_mismatch':fid})
                d['paradigm_cell_display_routes'].append({'form_id':fid,'paradigm_id':pid,'display_kind':'literal','matrix_id':pid,'row_index_zero_based':ri,'column_index_zero_based':ci,'row_label':rows[ri][0],'column_label':headers[ci],'grammar_display':True,'operation':{'type':'literal_surface','value':rows[ri][ci]},'analysis':forms[fid]['analysis']})
    diagnostics.append({'paradigm_id':pid,'lemma_id':p['lemma_id'],'scope':scope,'lexical_diagnostics':[{'form_id':c['form_id'],'form':c['form'],'analysis':analysis(c)} for c in cells],'derivation_policy':'Literal complete system within explicitly bounded mood/nonfinite scope.','evidence_refs':p['evidence_refs']})
d['status']='complete_nominal_and_grammar_display_design'
d['grammar_counts']={'paradigms':len(g['paradigms']),'logical_cells':sum(len(p['cells']) for p in g['paradigms']),'literal_cells':len(seen),'evidence_gap_positions':0}
d['counts']={'matrices':len(d['matrices']),'logical_cells':len(d['paradigm_cell_display_routes']),'literal_cells':d['nominal_counts']['literal_cells']+len(seen),'derived_cells':d['nominal_counts']['derived_cells']}
write('display-matrices.json',d)
write('grammar-display-plan.json',{'schema_version':1,'chapter':'ch12','status':'complete' if not errors else 'incomplete','counts':d['grammar_counts'],'diagnostics':diagnostics,'errors':errors})
print(json.dumps({'counts':d['counts'],'grammar_counts':d['grammar_counts'],'errors':errors}))
