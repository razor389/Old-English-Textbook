from pathlib import Path
from collections import defaultdict
import copy
import hashlib
import json

OUT=Path('curriculum/proposals/unit18')
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
lex=read('lexicon/entries.json'); gram=read('curriculum/grammar.json')
old_lemmas={l['lemma_id']:l for l in lex['lemmas']}
old_forms={f['form_id']:(l,f) for l in lex['lemmas'] for f in l['forms']}
old_senses={s['sense_id']:(l,s) for l in lex['lemmas'] for s in l['senses']}
nominal=read('sources/audits/unit18-source/noun-adjective-paradigms.json')
nominal_senses=read('sources/audits/unit18-source/nominal-sense-audit.json')
verbal=read('sources/audits/unit18-grammar/verbal-systems.json')
grammar_packet=read('sources/audits/unit18-grammar/senses-constructions-support.json')
candidate_verbs=read('sources/audits/unit18-grammar/candidate-verbal-bindings.json')
reading_path=Path('sources/audits/unit18-grammar/reading-verbal-bindings.json')
reading_verbs=read(reading_path) if reading_path.exists() else {'verbal_occurrences':[],'whole_frame_support':[]}
verb_occurrences=[]
for row in candidate_verbs['rows']:
    for raw in row['verbal_occurrences']:
        o=copy.deepcopy(raw);o.setdefault('source_item_id',row['source_item_id']);verb_occurrences.append(o)
verb_occurrences+=copy.deepcopy(reading_verbs['verbal_occurrences'])
for o in verb_occurrences:
    o.setdefault('form_knowledge_status',o.get('form_status',o.get('knowledge_status')))
    o.setdefault('sense_knowledge_status',o.get('sense_status'))
    o.setdefault('current_context_analysis',o.get('contextual_analysis',o.get('analysis',{})))
    o.setdefault('contextual_role_and_meaning','Exact context-bound source/model occurrence.')

source_prompts={r['source_item_id']:r for r in read('sources/audits/unit18-source/exercises-prompts.json')['items']}
paradigms=copy.deepcopy(nominal['paradigms'])
for v in verbal['systems']:
    p=copy.deepcopy(v)
    p['paradigm_id']=p['system_id']
    p['system_scope_code']=p['scope']
    p['scope']=p.get('teaching_scope',p['scope'])+' Defined morphological system: '+p['system_scope_code']
    p['part_of_speech']='participle' if 'agreement48' in p['system_id'] else 'verb'
    p['diagnostic_rule']=' '.join(p.get('derivation_rules',[]))
    for c in p['cells']:
        c['teaching_ids']=[c.get('proposed_teaching_id',p['paradigm_id'])]
        c['evidence_refs']=p.get('evidence_refs',[])
        c['scope_note']=p['scope']
    paradigms.append(p)
lemmas={}; issues=[]; reconciliations=[]; aliases={}

def entity(lid,headword,pos):
    if lid not in lemmas:
        prior=old_lemmas.get(lid)
        lemmas[lid]={'lemma_id':lid,'display_headword':prior.get('display_headword') if prior else headword,
            'part_of_speech':prior.get('part_of_speech') if prior else pos,'prior_lemma_present':bool(prior),
            'source_spellings':copy.deepcopy(prior.get('source_spellings',[])) if prior else [headword],
            'forms':[],'senses':[],'evidence_refs':[],
            'prior_record_ref':'lexicon/entries.json#/lemmas/'+str(lex['lemmas'].index(prior)) if prior else None}
    return lemmas[lid]

def prior_scope(record):
    return {k:copy.deepcopy(record.get(k)) for k in ['knowledge_status','recognition_taught_in','production_taught_in','supplied_in','status','reviewed_in','coverage_contract']}

def morph(a):
    if not isinstance(a,dict):return {}
    value_map={'nominative':'nom','genitive':'gen','dative':'dat','accusative':'acc','instrumental':'inst','ins':'inst',
        'singular':'sg','plural':'pl','masculine':'m','feminine':'f','neuter':'n','present':'present','preterite':'preterite'}
    out={}
    for k,v in a.items():
        k={'strength':'declension'}.get(k,k)
        if k in ['case','number','gender','tense','mood','person','declension','degree','verb_form','nonfinite','infinitive_type']:
            out[k]=value_map.get(v,v) if isinstance(v,str) else v
    if out.get('degree')=='positive': out.pop('degree')
    return out

def bind_cell(p,c):
    lid=p['lemma_id']; original_id=c['form_id']; previous=None
    direct=old_forms.get(original_id)
    if direct:
        if direct[0]['lemma_id']!=lid or direct[1]['form'].casefold()!=c['form'].casefold():
            issues.append({'kind':'same_ID_surface_or_lemma_conflict','paradigm_id':p['paradigm_id'],'cell':copy.deepcopy(c),'prior':copy.deepcopy(direct[1])})
        else: previous=direct[1]
    if previous is None and lid in old_lemmas:
        equivalent=[f for f in old_lemmas[lid]['forms'] if f['form']==c['form'] and morph(f['analysis'])==morph(c['analysis']) and morph(c['analysis'])]
        if len(equivalent)==1:
            previous=equivalent[0]
            aliases[original_id]=previous['form_id']
        elif len(equivalent)>1:
            issues.append({'kind':'multiple_exact_prior_morphology_candidates','logical_cell_id':original_id,'candidate_ids':[x['form_id'] for x in equivalent]})
    form=copy.deepcopy(c)
    form['logical_cell_id']=original_id
    form['cell_id']=original_id
    form['teaching_ids']=[p['paradigm_id']]
    form['contextual_analysis']=copy.deepcopy(c['analysis'])
    if previous:
        form['form_id']=previous['form_id']; form['form']=previous['form']; form['analysis']=copy.deepcopy(previous['analysis'])
        form['prior_scope']=prior_scope(previous)
        form['knowledge_status']='previously_taught' if previous.get('production_taught_in') else c['knowledge_status']
        form['prior_metadata_preservation']='Keep all existing metadata, earliest milestones and records_by_chapter untouched; add the current contextual analysis/status separately.'
        reconciliations.append({'logical_cell_id':original_id,'form_id':form['form_id'],'match':'same_ID' if original_id==form['form_id'] else 'same_lemma_surface_and_explicit_morphology',
            'prior_surface':previous['form'],'prior_analysis':copy.deepcopy(previous['analysis']),'current_contextual_analysis':copy.deepcopy(c['analysis']),
            'prior_scope':prior_scope(previous),'current_status':form['knowledge_status']})
    else:
        form['prior_scope']=None
        near=[f['form_id'] for f in old_lemmas.get(lid,{}).get('forms',[]) if f['form']==c['form']]
        if near:
            form['other_prior_same_surface_ids']=near
            form['identity_note']='No automatic identity from spelling alone; prior records remain separate until their analyses are reconciled.'
    row=entity(lid,p.get('headword',p.get('title',lid)),p.get('part_of_speech','verb'))
    if not any(x['form_id']==form['form_id'] for x in row['forms']): row['forms'].append(form)
    row['evidence_refs']=sorted(set(row['evidence_refs']+form.get('evidence_refs',[])))
    return form

for p in paradigms:
    p['cells']=[bind_cell(p,c) for c in p['cells']]
    row=lemmas[p['lemma_id']]
    if p.get('part_of_speech')=='noun':
        genders={c.get('contextual_analysis',{}).get('gender') for c in p['cells']}
        if len(genders)==1:row['gender']=next(iter(genders))
        row['declension_model']=p.get('model')
    if p.get('part_of_speech')=='verb':row.setdefault('selected_verbal_system_ids',[]).append(p['paradigm_id'])


context_forms=[]
frame_by_id={f['feature_id']:f for f in grammar_packet['whole_frame_support']+reading_verbs['whole_frame_support']}
for o in verb_occurrences:
    fid=o['form_id'];lid=o['lemma_id']
    if fid in old_forms or any(fid==f['form_id'] for l in lemmas.values() for f in l['forms']):continue
    if o['form_knowledge_status']!='supplied':continue
    ev=sorted({e for route in o.get('construction_support_ids',[])+o.get('whole_frame_support_ids',[]) for e in frame_by_id.get(route,{}).get('evidence_refs',[])})
    ev=ev or source_prompts.get(o['source_item_id'],{}).get('evidence_refs',[]) or ['U18G-FB175','U18G-FB176','U18G-FB177']
    c={'form_id':fid,'form':o['surface'],'analysis':copy.deepcopy(o['current_context_analysis']),'knowledge_status':'supplied',
        'evidence_refs':ev,'scope_note':o['contextual_role_and_meaning']+' Only the visible whole frame/source help; no independent recall.',
        'source_items':[o['source_item_id']],'support_feature_ids':o.get('construction_support_ids',[])+o.get('whole_frame_support_ids',[])}
    p={'lemma_id':lid,'headword':o.get('headword',lid),'part_of_speech':'verb','paradigm_id':'NEW-U18-VERBAL-CONTEXT-HELP'}
    context_forms.append(bind_cell(p,c))

all_senses=copy.deepcopy(nominal_senses['senses'])
for p in paradigms:
    if p.get('sense_proposal'):
        all_senses.append(dict(p['sense_proposal'],lemma_id=p['lemma_id'],headword=p['headword'],part_of_speech='verb',
            evidence_refs=p.get('evidence_refs',[]),source_items=p.get('source_items',[]),teaching_ids=[p['paradigm_id']]))
for s in grammar_packet['sense_proposals']+reading_verbs.get('sense_proposals',[]):
    all_senses=[v for v in all_senses if v['sense_id']!=s['sense_id']]
    all_senses.append(dict(s,part_of_speech='verb'))
for o in verb_occurrences:
    s=o.get('selected_sense_record') or o.get('proposed_sense')
    if not s and o.get('sense_id')=='onginnan-u18-reading':
        s={'sense_id':o['sense_id'],'gloss':'begin, with the explicitly supplied playing/praising action','knowledge_status':'supplied','scope_note':o['contextual_role_and_meaning']+' Only the complete visible source frame.','evidence_refs':['U18G-FB175','U18G-FB176','U18G-FB177'],'source_items':[o['source_item_id']]}
    if not s and o.get('sense_id') and o.get('contextual_gloss') and o.get('sense_knowledge_status')=='supplied':
        routes=o.get('construction_support_ids',[])+o.get('whole_frame_support_ids',[])
        ev=sorted({e for route in routes for e in frame_by_id.get(route,{}).get('evidence_refs',[])})
        s={'sense_id':o['sense_id'],'gloss':o['contextual_gloss'],'knowledge_status':'supplied','scope_note':o['contextual_role_and_meaning']+' Only the visible whole source frame; no independent recall.','evidence_refs':ev or ['U18G-FB175','U18G-FB176','U18G-FB177'],'source_items':[o['source_item_id']]}
    if not s or s['sense_id'] in old_senses or any(x['sense_id']==s['sense_id'] for x in all_senses):continue
    all_senses.append({k:copy.deepcopy(v) for k,v in dict(s,lemma_id=o['lemma_id'],part_of_speech='verb').items() if k in ['lemma_id','headword','part_of_speech','sense_id','gloss','knowledge_status','scope','scope_note','evidence_refs','source_items']})
for s in all_senses:
    if not s.get('evidence_refs'):
        occurrences=[o for o in verb_occurrences if o.get('sense_id')==s['sense_id']]
        s['evidence_refs']=sorted({e for o in occurrences for rid in o.get('construction_support_ids',[])+o.get('whole_frame_support_ids',[]) for e in frame_by_id.get(rid,{}).get('evidence_refs',[])})
        if not s['evidence_refs']:s['evidence_refs']=sorted({e for o in occurrences for e in source_prompts.get(o['source_item_id'],{}).get('evidence_refs',[])})
    row=entity(s['lemma_id'],s.get('headword',s['lemma_id']),s.get('part_of_speech','noun'))
    sense=copy.deepcopy(s)
    if s['sense_id'] in old_senses:
        old=old_senses[s['sense_id']][1]
        sense['gloss']=old['gloss']; sense['contextual_gloss']=s['gloss']; sense['prior_scope']=prior_scope(old)
        sense['knowledge_status']='previously_taught' if old.get('production_taught_in') else s['knowledge_status']
        sense['prior_metadata_preservation']='Original sense gloss and histories remain unchanged; contextual gloss is additive.'
        if old['gloss']!=s['gloss']:
            reconciliations.append({'sense_id':s['sense_id'],'match':'existing_sense_ID','prior_gloss':old['gloss'],'current_contextual_gloss':s['gloss'],'prior_scope':prior_scope(old),'current_status':sense['knowledge_status']})
    else: sense['prior_scope']=None
    sense['teaching_ids']=['NEW-U18-VOC-'+sense['sense_id'].upper()]
    if not any(x['sense_id']==sense['sense_id'] for x in row['senses']): row['senses'].append(sense)
    row['evidence_refs']=sorted(set(row['evidence_refs']+s.get('evidence_refs',[])))

dictionary_references=[]
for supplied in [r for r in grammar_packet['dictionary_reference_positions']+verbal.get('reference_only',[]) if r.get('form_id') and r.get('lemma_id')]:
    c=copy.deepcopy(supplied);lid=c['lemma_id']
    if 'analysis' not in c:c['analysis']=copy.deepcopy(old_forms[c['form_id']][1]['analysis'])
    c['evidence_refs']=c.get('evidence_refs') or sorted({e for p in paradigms if p['lemma_id']==lid for e in p.get('evidence_refs',[])}) or old_forms.get(c['form_id'],({},{}))[1].get('evidence_refs',[])
    c['scope_note']=c.get('support_scope','Visible dictionary reference only; no independent infinitive use or recall is assigned.')
    p={'lemma_id':lid,'headword':c.get('headword',c['form']),'part_of_speech':'verb','paradigm_id':'NEW-U18-DICTIONARY-REFERENCES'}
    dictionary_references.append(bind_cell(p,c))

matrices=[]; routes=[]
case_names={'nom':'Nominative','gen':'Genitive','dat':'Dative','acc':'Accusative','inst':'Instrumental','ins':'Instrumental'}
def matrix(p,mid,title,headers,rowkeys,colkeys,cell_at):
    rows=[]; ids=[]; statuses=[]; logical=[]
    for ri,rk in enumerate(rowkeys):
        row=[case_names.get(rk,rk)]; idrow=[[]]; statrow=['label']; logrow=[None]
        for ci,ck in enumerate(colkeys,1):
            c=cell_at(rk,ck)
            row.append(c['form'] if c else '—'); idrow.append([c['form_id']] if c else []); statrow.append(c['knowledge_status'] if c else 'not_applicable'); logrow.append(c['logical_cell_id'] if c else None)
            if c:
                routes.append({'paradigm_id':p['paradigm_id'],'logical_cell_id':c['logical_cell_id'],'form_ids':[c['form_id']],
                    'display_kind':'literal','matrix_id':mid,'row_index_zero_based':ri,'column_index_zero_based':ci,
                    'surface':c['form'],'analysis':copy.deepcopy(c['analysis']),'contextual_analysis':copy.deepcopy(c['contextual_analysis']),
                    'knowledge_status':c['knowledge_status'],'evidence_refs':c.get('evidence_refs',[]),'operation':{'type':'literal_surface','value':c['form']}})
        rows.append(row); ids.append(idrow); statuses.append(statrow); logical.append(logrow)
    matrices.append({'matrix_id':mid,'title':title,'paradigm_ids':[p['paradigm_id']],'headers':headers,'rows':rows,
        'cell_form_ids':ids,'cell_logical_ids':logical,'cell_knowledge_statuses':statuses,'evidence_refs':p.get('evidence_refs',[]),
        'scope':p.get('scope'),'rules':[p.get('diagnostic_rule')] if p.get('diagnostic_rule') else [],
        'display_obligation':'Print every literal cell with its rules and scope. Em dash is a nonapplicable display slot, not an invented form or a claim of lexical defectiveness.'})

for p in paradigms:
    cells=p['cells']; pos=p.get('part_of_speech')
    if pos=='noun':
        nums=['sg','pl'] if any(c['contextual_analysis'].get('number')=='pl' for c in cells) else ['sg']
        matrix(p,p['paradigm_id']+'-DISPLAY',p['headword'],['Case']+['Singular' if n=='sg' else 'Plural' for n in nums],['nom','gen','dat','acc'],nums,
            lambda case,num:next((c for c in cells if c['contextual_analysis'].get('case')==case and c['contextual_analysis'].get('number')==num),None))
    elif pos in ['adjective','participle']:
        for strength in ['strong','weak']:
            chosen=[c for c in cells if morph(c['contextual_analysis']).get('declension')==strength]
            rowkeys=['nom','gen','dat','acc']+(['inst'] if any(morph(c['contextual_analysis']).get('case')=='inst' for c in chosen) else [])
            cols=[(n,g) for n in ['sg','pl'] for g in ['m','n','f']]
            matrix(p,p['paradigm_id']+'-'+strength.upper()+'-DISPLAY',p['headword']+' — '+strength,
                ['Case','Masculine singular','Neuter singular','Feminine singular','Masculine plural','Neuter plural','Feminine plural'],rowkeys,cols,
                lambda case,ng:next((c for c in chosen if morph(c['contextual_analysis']).get('case')==case and (morph(c['contextual_analysis']).get('number'),morph(c['contextual_analysis']).get('gender'))==ng),None))
    elif pos=='verb':
        if p['paradigm_id'].endswith('past-predicate2'):
            matrix(p,p['paradigm_id']+'-DISPLAY',p['headword']+' — bounded predicate alternatives',
                ['Predicate form','Literal surface'],['Uninflected predicate base (singular or plural)','Agreeing plural predicate'],['surface'],
                lambda kind,_:next((c for c in cells if (morph(c['contextual_analysis']).get('number')=='pl')==kind.startswith('Agreeing')),None))
            continue
        for mood in ['indicative','imperative','subjunctive']:
            chosen=[c for c in cells if c['contextual_analysis'].get('mood')==mood]
            if not chosen: continue
            tenses=[t for t in ['present','preterite'] if any(c['contextual_analysis'].get('tense')==t for c in chosen)] or ['command']
            people=[(person,num) for num in ['sg','pl'] for person in [1,2,3] if any(morph(c['contextual_analysis']).get('person')==person and morph(c['contextual_analysis']).get('number')==num for c in chosen)]
            person_labels={pn:str(pn[0])+(' singular' if pn[1]=='sg' else ' plural') for pn in people}
            matrix(p,p['paradigm_id']+'-'+mood.upper()+'-DISPLAY',p['headword']+' — '+mood,
                ['Person and number']+[t.title() for t in tenses],people,tenses,
                lambda pn,tense:next((c for c in chosen if (morph(c['contextual_analysis']).get('person'),morph(c['contextual_analysis']).get('number'))==pn and (c['contextual_analysis'].get('tense', 'command')==tense)),None))
            for row in matrices[-1]['rows']: row[0]=person_labels[tuple(row[0])]
        chosen=[c for c in cells if c['contextual_analysis'].get('verb_form')=='participle' or c['contextual_analysis'].get('nonfinite')=='participle']
        if chosen:
            tense_order=['present','past']
            matrix(p,p['paradigm_id']+'-PARTICIPLES-DISPLAY',p['headword']+' — participle formation pair',
                ['Type','Form'],tense_order,['surface'],
                lambda tense,_:next((c for c in chosen if c['contextual_analysis'].get('tense')==tense),None))
    else: issues.append({'kind':'unhandled_paradigm_display','paradigm_id':p['paradigm_id'],'part_of_speech':pos})
    routed={r['logical_cell_id'] for r in routes if r['paradigm_id']==p['paradigm_id']}
    remaining=[c for c in cells if c['logical_cell_id'] not in routed]
    if remaining and pos=='verb':
        matrix(p,p['paradigm_id']+'-BOUNDED-NONFINITE-DISPLAY',p['headword']+' — additional bounded forms',
            ['Type','Form'],[c['logical_cell_id'] for c in remaining],['surface'],
            lambda cid,_:next(c for c in remaining if c['logical_cell_id']==cid))
        for row in matrices[-1]['rows']:
            a=next(c['contextual_analysis'] for c in remaining if c['logical_cell_id']==row[0])
            row[0]=str(a['verb_form']).replace('_',' ').capitalize() if a.get('verb_form') else '; '.join(str(k).replace('_',' ')+' '+str(v).replace('_',' ') for k,v in a.items())

assert len(routes)==sum(len(p['cells']) for p in paradigms),(len(routes),sum(len(p['cells']) for p in paradigms))
assert len({(r['paradigm_id'],r['logical_cell_id']) for r in routes})==len(routes)
teaching=[]
for p in paradigms:
    teaching.append({'teaching_id':p['paradigm_id'],'kind':'complete_bounded_paradigm','lemma_id':p['lemma_id'],
        'form_ids':[c['form_id'] for c in p['cells']],'sense_ids':[s['sense_id'] for s in lemmas[p['lemma_id']]['senses']],
        'rules':[p.get('diagnostic_rule')],'scope':p.get('scope'),'evidence_refs':p.get('evidence_refs',[]),
        'matrix_ids':[m['matrix_id'] for m in matrices if p['paradigm_id'] in m['paradigm_ids']],
        'lesson_placement':'Before any independent task using these forms/senses; pair the complete table with its selected ordinary frames.'})
for row in lemmas.values():
    for sense in row['senses']:
        teaching.append({'teaching_id':'NEW-U18-VOC-'+sense['sense_id'].upper(),'kind':'bounded_lexical_sense',
            'lemma_id':row['lemma_id'],'sense_ids':[sense['sense_id']],'gloss':sense['gloss'],'contextual_gloss':sense.get('contextual_gloss'),
            'knowledge_status':sense['knowledge_status'],'evidence_refs':sense.get('evidence_refs',[]),'scope':sense.get('scope'),
            'source_items':sense.get('source_items',[])})
features=[]
for raw in grammar_packet['features']+grammar_packet['whole_frame_support']+reading_verbs['whole_frame_support']:
    f=copy.deepcopy(raw);fid=f['feature_id'];f['teaching_ids']=['NEW-U18-GRAM-'+fid.upper()]
    if fid in {v['feature_id'] for v in gram['features']}:
        old=next(v for v in gram['features'] if v['feature_id']==fid)
        f['prior_scope']=prior_scope(old);f['contextual_description']=f.get('description',f.get('whole_frame_analysis'))
        f['description']=old.get('description');f['knowledge_status']='previously_taught' if old.get('production_taught_in') else f['knowledge_status']
    elif f['knowledge_status']=='previously_taught':
        issues.append({'kind':'new_feature_ID_claims_prior_teaching','feature_id':fid})
    f.setdefault('description',f.get('whole_frame_analysis'));f.setdefault('scope_note',f.get('limitation',f.get('description')))
    f.setdefault('label',f.get('description','').split('.')[0]);features.append(f)
    teaching.append({'teaching_id':f['teaching_ids'][0],'kind':'supplied_whole_frame' if f['knowledge_status']=='supplied' else 'bounded_construction',
        'feature_ids':[fid],'knowledge_status':f['knowledge_status'],'description':f.get('contextual_description',f['description']),
        'support_span':f.get('support_span'),'evidence_refs':f['evidence_refs'],'source_items':f.get('source_items',[]),
        'lesson_placement':'Before the earliest task that requires this construction; whole supplied help remains visible at every use.'})
teaching.append({'teaching_id':'NEW-U18-DICTIONARY-REFERENCES','kind':'visible_dictionary_references','form_ids':[r['form_id'] for r in dictionary_references],
    'knowledge_status':'supplied','scope':'Print the exact dictionary forms with their meanings and citation role. Do not test independent recall or infer independent infinitival syntax from a citation.',
    'evidence_refs':sorted({e for c in dictionary_references for e in c['evidence_refs']})})
teaching.append({'teaching_id':'NEW-U18-VERBAL-CONTEXT-HELP','kind':'visible_whole_frame_verbal_help','form_ids':[r['form_id'] for r in context_forms],
    'knowledge_status':'supplied','scope':'Each exact source/answer form is supplied with its role, meaning and whole phrase. No component independent recall is claimed.',
    'evidence_refs':sorted({e for c in context_forms for e in c['evidence_refs']})})
result={'schema_version':1,'chapter':'ch18','status':'work_in_progress_nominal_and_verbal_join; do_not_freeze',
    'baseline':'0eda277 actual seventeen active contracts/registers','lemmas':list(lemmas.values()),'features':features,
    'paradigms':paradigms,'teaching_records':teaching,'form_identity_reconciliation':reconciliations,
    'form_id_aliases':aliases,'audited_inflection_rules':nominal.get('rules',[]),
    'lexical_frames':grammar_packet['features']+grammar_packet['whole_frame_support'],'principal_parts':[{'lemma_id':p['lemma_id'],**p['citation_reference']} for p in paradigms if p.get('citation_reference')],
    'unresolved_integration':issues+['Lexical/construction frames, source helps, all source-output token sense/analysis bindings, and task joins are still pending.'],
    'analysis_input_hashes':{p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in ['sources/audits/unit18-source/noun-adjective-paradigms.json','sources/audits/unit18-source/nominal-sense-audit.json','sources/audits/unit18-grammar/verbal-systems.json','sources/audits/unit18-grammar/senses-constructions-support.json']},
    'counts':{'lemmas':len(lemmas),'forms':sum(len(l['forms']) for l in lemmas.values()),'senses':sum(len(l['senses']) for l in lemmas.values()),'paradigms':len(paradigms),'literal_cells':len(routes),'identity_aliases':len(aliases),'identity_issues':len(issues)}}
(OUT/'inventory.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'display-matrices.json').write_text(json.dumps({'schema_version':1,'chapter':'ch18','status':result['status'],'matrices':matrices,'paradigm_cell_display_routes':routes,
    'component_form_routes':[dict(r,component_index_one_based=1,form_id=r['form_ids'][0]) for r in routes],
    'counts':{'matrices':len(matrices),'logical_cells':len(routes),'literal_form_cells':len(routes),'unassigned_table_slots':0,'nonapplicable_visual_padding_slots':sum(1 for m in matrices for row in m['cell_form_ids'] for cell in row[1:] if not cell),'component_form_occurrences':len(routes),'literal_routes':len(routes),'derived_cells':0,'component_routes':len(routes),'unrouted_assigned_cells':0}},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result['counts'],indent=2))
print(json.dumps(issues,ensure_ascii=False,indent=2)[:6000])
