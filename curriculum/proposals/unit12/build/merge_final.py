"""Reconcile Unit12 contract inputs; never modify shared registers or contracts."""
import copy,hashlib,json
from collections import defaultdict,Counter
from pathlib import Path
import feature_bindings as FB

ROOT=Path(__file__).resolve().parents[4];OUT=ROOT/'curriculum/proposals/unit12'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def write(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def digest(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def uniq(v):return sorted(set(v))
def prior_status(r):return 'previously_taught' if r.get('production_taught_in') else 'previously_recognition' if r.get('recognition_taught_in') else 'previously_supplied'
def status(r):return r.get('resolved_status',r.get('knowledge_status','unresolved'))
def bundle(data,span,key):
    """Accept a flat tagged collection or explicit source-span bundles."""
    for container in ['readings','source_spans','bundles']:
        if container in data:
            hit=next(x for x in data[container] if x.get('source_span_id')==span)
            return copy.deepcopy(hit.get(key,[]))
    if data.get('source_span_id')==span:return copy.deepcopy(data.get(key,[]))
    return [copy.deepcopy(x) for x in data.get(key,[]) if x.get('source_span_id')==span or span in x.get('source_span_ids',[])]

LP=load('lexicon/entries.json');GP=load('curriculum/grammar.json')
SL=load('sources/audits/unit12-source/lexical-inventory.json')
SG=load('sources/audits/unit12-grammar/grammar-records.json')
SN=load('sources/audits/unit12-source/noun-adjective-paradigms.json')
SP=load('sources/audits/unit12-source/exercises-prompts.json')
CT={t['task_id']:t['target_specification'] for t in load('curriculum/proposals/unit12/cook-targets.json')['targets']}
SD=load('sources/audits/unit12-source/exercises-dependencies.json')
CH=load('sources/audits/unit12-source/cook-local-support.json')
CF=load('sources/audits/unit12-source/cook-construction-requirements.json')
SR=load('sources/audits/unit12-source/reading-source.json')
ST=load('sources/audits/unit12-source/reading-tokens.json')
SH=load('sources/audits/unit12-source/reading-support.json')
SF=load('sources/audits/unit12-source/reading-construction-requirements.json')
SEED=load('curriculum/proposals/unit12/task-seed.json');COMP=load('curriculum/proposals/unit12/composition-seed.json')
PUBLIC=load('curriculum/proposals/unit12/public-sequence-bindings.json')
PRIVATE=load('curriculum/proposals/unit12/author-only-sequence-bindings.json')
PCB=load('curriculum/proposals/unit12/author-only-cook-sequence-bindings.json')
PM=load('curriculum/proposals/unit12/author-only-model-seed.json')
CM=load('sources/audits/unit12-source/author-only-cook-corrected-models.json')
NDP=load('curriculum/proposals/unit12/nominal-display-plan.json')
MAT=load('curriculum/proposals/unit12/display-matrices.json')
base=load('build/unit12-prior-baseline.json');assert LP==base['lexicon'] and GP==base['grammar']

errors=[];unresolved=[];promotions=[];reconciliations=[]
prior_forms={f['form_id']:{**copy.deepcopy(f),'lemma_id':l['lemma_id']} for l in LP['lemmas'] for f in l['forms']}
prior_senses={s['sense_id']:{**copy.deepcopy(s),'lemma_id':l['lemma_id']} for l in LP['lemmas'] for s in l['senses']}
prior_features={f['feature_id']:copy.deepcopy(f) for f in GP['features']}
forms={k:{**v,'resolved_status':prior_status(v)} for k,v in prior_forms.items()}
senses={k:{**v,'resolved_status':prior_status(v)} for k,v in prior_senses.items()}
features={k:{**v,'resolved_status':prior_status(v)} for k,v in prior_features.items()}
all_lemmas={l['lemma_id']:copy.deepcopy(l) for l in LP['lemmas']}
new_lemmas={};new_features={};paradigms=copy.deepcopy(SN['paradigms']+SG['paradigms'])
form_teaching_ids=defaultdict(list)
for p in paradigms:
    for c in p['cells']:
        if c.get('form_id'):form_teaching_ids[c['form_id']].append(p.get('teaching_id',p['paradigm_id']))
for package in [SL,SG]:
    for incoming in package['lemmas']:
        lid=incoming['lemma_id'];old=all_lemmas.get(lid,{})
        result=new_lemmas.setdefault(lid,{k:copy.deepcopy(v) for k,v in incoming.items() if k not in ['forms','senses']})
        result.setdefault('forms',[]);result.setdefault('senses',[]);result['prior_lemma_present']=lid in {l['lemma_id'] for l in LP['lemmas']}
        merged={**old,**copy.deepcopy(incoming)}
        for kind,key,previous,dest in [('forms','form_id',prior_forms,forms),('senses','sense_id',prior_senses,senses)]:
            known={r[key]:copy.deepcopy(r) for r in old.get(kind,[])}
            for incoming_record in incoming.get(kind,[]):
                r=copy.deepcopy(incoming_record);ident=r[key]
                r.setdefault('teaching_ids',form_teaching_ids.get(ident,[]) if kind=='forms' else [])
                if not r['teaching_ids']:r['teaching_ids']=['NEW-U12-LOCAL-HELPS' if r['knowledge_status']=='supplied' else 'NEW-U12-VOC-'+lid.upper()]
                if ident in previous:
                    p=previous[ident]
                    for field in (['form','analysis'] if kind=='forms' else ['gloss']):
                        if field in r and field in p and r[field]!=p[field]:
                            reconciliations.append({'record_type':kind[:-1],'record_id':ident,'canonical_field':field,'preserved_prior_value':copy.deepcopy(p[field]),'unit12_contextual_value':copy.deepcopy(r[field]),'policy':'Preserve the exact existing identity field; record the new context separately.'})
                            r['unit12_contextual_'+field]=copy.deepcopy(r[field]);r[field]=copy.deepcopy(p[field])
                    for field in ['production_taught_in','recognition_taught_in','supplied_in']:r['prior_'+field]=p.get(field)
                    if p.get('production_taught_in') and r['knowledge_status'] in ['new_production','previously_taught']:r['knowledge_status']='previously_taught'
                    elif r['knowledge_status']=='new_production':promotions.append({'record_type':kind[:-1],'record_id':ident,'from':prior_status(p),'to':'new_production','previous_history':{k:p.get(k) for k in ['production_taught_in','recognition_taught_in','supplied_in']},'teaching_ids':r['teaching_ids']})
                duplicates=[x for x in result[kind] if x[key]==ident]
                if duplicates:
                    if duplicates[0]!=r:errors.append({'conflicting_new_identity':ident})
                else:result[kind].append(r)
                known[ident]=r;dest[ident]={**r,'lemma_id':lid,'resolved_status':r['knowledge_status']}
            merged[kind]=list(known.values())
        all_lemmas[lid]=merged

rule_by_id={r['rule_id']:r for r in SN['rules']}
nominal_feature_rules=load('curriculum/proposals/unit12/nominal-feature-map.json')['features']
for item in nominal_feature_rules:
    fid=item['feature_id'];r=rule_by_id[item['rule_id']];new_features[fid]={'feature_id':fid,'description':r.get('description',r.get('rule')),'knowledge_status':'new_production','evidence_refs':r['evidence_refs'],'teaching_ids':item['teaching_ids'],'scope_note':item.get('scope_note','Only the explicitly selected lexical systems; reference cells and unassigned syntax retain their limits.')}
for f in SG['features']+SF.get('features',[])+CF.get('features',[]):
    fid=f['feature_id']
    if fid in new_features and new_features[fid]!=f:errors.append({'conflicting_new_feature':fid})
    new_features[fid]=copy.deepcopy(f)
for fid,f in new_features.items():
    f.setdefault('teaching_ids',['NEW-U12-GRAM-'+fid]);features[fid]={**f,'resolved_status':f['knowledge_status']}

def checked(kind,ident,owner):
    table={'form':forms,'sense':senses,'feature':features}[kind]
    if ident not in table:unresolved.append({'owner':owner,'kind':kind,'id':ident});return None
    r=table[ident]
    if status(r) in ['unresolved','pending','awaiting_specialist_reconciliation']:unresolved.append({'owner':owner,'kind':kind,'id':ident,'status':status(r)})
    return r

USE={k:defaultdict(set) for k in ['forms','senses','features']};ASSESS={k:defaultdict(set) for k in USE}
def requirements(owner,rf,rs,rg,assess=False):
    rf=set(rf);rs=set(rs);rg=set(rg)
    lids={forms[f]['lemma_id'] for f in rf if f in forms}
    if 'se' in lids:rg.add('article-agreement')
    if lids & {'he','ic','thu'}:rg.add('u02-pronoun-reference')
    if any(isinstance(forms[f].get('analysis'),dict) and forms[f]['analysis'].get('declension') in ['strong','weak'] for f in rf if f in forms):rg.add('u03-agreement')
    # Only morphological system features are automatic; argument frames are explicit.
    for f in rf:
        record=forms.get(f)
        if not record:continue
        a=record.get('unit12_contextual_analysis',record.get('analysis',{}))
        if isinstance(a,dict) and a.get('mood')=='indicative':
            candidate='u12-'+record['lemma_id']+'-indicative'
            if candidate in features:rg.add(candidate)
        if isinstance(a,dict) and a.get('mood')=='imperative':
            candidate='u12-'+record['lemma_id']+'-imperative'
            if candidate in features:rg.add(candidate)
        if isinstance(a,dict) and a.get('verb_form')=='participle':
            candidate='u12-'+record['lemma_id']+'-participle-bases'
            if candidate in features:rg.add(candidate)
        if isinstance(a,dict) and a.get('mood')=='infinitive':
            candidate='u12-'+record['lemma_id']+'-modal-infinitive'
            if candidate in features:rg.add(candidate)
    result={}
    for plural,kind,ids in [('forms','form',rf),('senses','sense',rs),('features','feature',rg)]:
        ids=uniq(ids);result['required_'+kind+'_ids']=ids;supplied=[];tested=[]
        for ident in ids:
            r=checked(kind,ident,owner);USE[plural][ident].add(owner)
            if not r:continue
            if status(r) in ['supplied','previously_supplied']:supplied.append(ident)
            elif assess:tested.append(ident);ASSESS[plural][ident].add(owner)
        result['supplied_'+kind+'_ids']=supplied
        if assess:result['tested_'+kind+'_ids']=tested
    return result

def bind(t,owner):
    t=copy.deepcopy(t)
    if t.get('token_type')=='punctuation' or t.get('kind')=='punctuation' or (t.get('surface',t.get('literal'))=='—' and not t.get('form_id')):
        t['token_type']='punctuation'
        if any(t.get(k) for k in ['form_id','sense_id','lemma_id']):errors.append({'punctuation_has_lexical_identity':owner})
        return t
    f=checked('form',t['form_id'],owner);s=checked('sense',t['sense_id'],owner)
    if f and s:
        if f['lemma_id']!=s['lemma_id']:errors.append({'form_sense_lemma_mismatch':owner,'token':t})
        surface=t.get('surface',t.get('literal','')).strip('.,:;!?“”"()[]')
        if surface.casefold()!=f['form'].casefold():errors.append({'surface_mismatch':owner,'token':t,'registered':f['form']})
        if t.get('surface')!=surface:t['source_whitespace_surface']=t.get('surface')
        t.update(surface=surface,form_status=status(f),sense_status=status(s),form=f['form'],analysis=f['analysis'])
    return t

def support(h):
    h=copy.deepcopy(h);covers=h.get('covers',{})
    h['text']=h.get('text',h.get('learner_help',h.get('description','')))
    h['knowledge_status']=h.get('knowledge_status',h.get('status','supplied'))
    h['form_ids']=copy.deepcopy(h.get('form_ids',covers.get('form_ids',[])))
    h['sense_ids']=copy.deepcopy(h.get('sense_ids',covers.get('sense_ids',[])))
    h['feature_ids']=copy.deepcopy(h.get('feature_ids',h.get('feature_refs',covers.get('construction_ids',[]))))
    return h

public_by=defaultdict(list);private_by=defaultdict(list)
for s in PUBLIC['sequences']:public_by[s['owner_id']].append(s)
for s in PRIVATE['sequences']:private_by[s['owner_id']].append(s)
examples=[];compositions=[]
for e in COMP['teaching_examples']:
    ident=e['example_id'];seq=public_by[ident][0];rg=FB.roles(e['provisional_feature_roles'])+FB.EXAMPLE_EXTRA[ident[-2:]]
    examples.append({**copy.deepcopy(e),'origin_category':'new_teaching_material','tokens':[bind(t,ident) for t in seq['tokens']],'target_feature_ids':uniq(rg),'word_count':len(e['text'].split()),'status':'reconciled_pre_contract_design',**requirements(ident,seq['required_form_ids'],seq['required_sense_ids'],rg)})
for c in COMP['compositions']:
    ident=c['composition_id'];seq=public_by[ident][0];rg=FB.roles(c['provisional_feature_roles'])+FB.CONTROLLED_EXTRA
    compositions.append({**copy.deepcopy(c),'origin_category':'new_teaching_material','tokens':[bind(t,ident) for t in seq['tokens']],'word_count':len(c['text'].split()),'status':'reconciled_pre_contract_design',**requirements(ident,seq['required_form_ids'],seq['required_sense_ids'],rg)})

readings=[]
for source in SR['source_spans']:
    source=copy.deepcopy(source)
    source.setdefault('word_count_whitespace',source.get('word_count',len(source['exact_text_without_note_cues'].split())))
    ident=source['source_span_id'];tokens=[bind(t,ident) for t in bundle(ST,ident,'tokens')]
    literal_words=source['exact_text_without_note_cues'].split()
    for index,(token,literal) in enumerate(zip(tokens,literal_words),1):
        if token.get('whitespace_index',token.get('token_index',index))!=index:errors.append({'source_token_order':ident,'expected_index':index,'token':token})
        if token.get('surface')!=literal.strip('.,:;!?“”"()[]'):errors.append({'source_exact_surface_order':ident,'index':index,'literal':literal,'token_surface':token.get('surface')})
        token['token_index']=index;token['literal']=literal
    supports=[support(h) for h in bundle(SH,ident,'supports')];rg=bundle(SF,ident,'required_feature_ids')
    rg += [f['feature_id'] for f in SF.get('features',[]) if f.get('source_span_id')==ident]
    regular=SF.get('prior_or_new_regular_dependencies',{})
    if isinstance(regular,dict):rg+=regular.get(ident,[])
    elif isinstance(regular,list):
        for record in regular:
            if record.get('source_span_id')==ident:rg+=record['required_feature_ids']
    if rg and isinstance(rg[0],dict):rg=[f['feature_id'] for f in rg]
    req=requirements(ident,[t['form_id'] for t in tokens if t.get('form_id')],[t['sense_id'] for t in tokens if t.get('sense_id')],rg)
    if len(tokens)!=source['word_count_whitespace']:errors.append({'source_token_count':ident,'expected':source['word_count_whitespace'],'actual':len(tokens)})
    readings.append({**copy.deepcopy(source),'source_item_id':ident,'text':source['exact_text_without_note_cues'],'learner_text':source['exact_text_without_note_cues'],'display_text':source['exact_text_without_note_cues'],'word_count':source.get('lexical_word_count',source['word_count_whitespace']),'tokens':tokens,'local_support':supports,'teaching_id':'NEW-U12-SOURCE-HELPS',**req})
reading_by={r['source_span_id']:r for r in readings}

cook_deps={d['task_id']:d for d in SD['items']};cook_models={m['task_id']:m for m in CM['items']};original_models={m['task_id']:m for m in PM['models']}
cook_seeds=[]
for prompt in SP['items']:
    ident=prompt['task_id'];local=[h for h in CH['supports'] if ident in h.get('task_ids',[])]
    cook_seeds.append({**copy.deepcopy(prompt),'task_id':ident,'key_id':'KEY-'+ident,'prompt':prompt['prompt_original'],'origin':'exact_source','mode':'production_supported' if local else 'production','input_texts':[]})
tasks=[];models=[]
for seed in SEED['tasks']+cook_seeds:
    t=copy.deepcopy(seed);ident=t['task_id'];cook=ident.startswith('EX-');rf=set();rs=set();local=[]
    sequences=copy.deepcopy(public_by[ident]);t['input_sequences']=sequences;t['input_sequence_ids']=[s['sequence_id'] for s in sequences]
    for seq in sequences+private_by[ident]:rf.update(seq['required_form_ids']);rs.update(seq['required_sense_ids'])
    for seq in sequences:seq['tokens']=[bind(token,ident) for token in seq['tokens']]
    if cook:
        dep=cook_deps[ident];m=copy.deepcopy(cook_models[ident]);rg=[r['feature_id'] if isinstance(r,dict) else r for r in dep['construction_requirements']]
        rf.update(r['form_id'] if isinstance(r,dict) else r for r in dep['form_requirements_unordered'])
        rs.update(r['sense_id'] if isinstance(r,dict) else r for r in dep.get('sense_requirements',dep.get('sense_requirements_unordered',[])))
        local=[support(h) for h in CH['supports'] if ident in h.get('task_ids',[])]
        t['target_specification']=CT[ident]
        t['evidence_refs']=copy.deepcopy(dep.get('source_refs',seed.get('source_image_refs',[])))
        t['source_route_note']=dep.get('audit_note','');t['selected_route_scope']=dep.get('scope','')
        t['lexical_frame_requirements']=copy.deepcopy(dep.get('lexical_frame_requirements',[]))
    else:
        suffix=ident.removeprefix('NEW-U12-');m=copy.deepcopy(original_models[ident]);rg=FB.roles(t['provisional_feature_roles'])+FB.EXTRA.get(suffix,[])
        if m.get('translation_witness_key'):
            m['model']=PM['translation_witness'][m['translation_witness_key']]
            m['translation_origin']='Curriculum designer independent translation witness, prepared before viewing source-editor or coordinator private witnesses.'
        rf.update(m.get('required_output_form_ids',[]))
        rs.update(m.get('required_output_sense_ids',[]))
        if suffix.startswith('F') and not m.get('required_output_sense_ids'):
            for fid in m.get('required_output_form_ids',[]):
                f=checked('form',fid,ident)
                if f:rs.add(all_lemmas[f['lemma_id']]['senses'][0]['sense_id'])
        if suffix.startswith('R'):
            reading=compositions[0];t['reading_id']=reading['composition_id']
            rf.update(reading['required_form_ids']);rs.update(reading['required_sense_ids']);rg+=reading['required_feature_ids']
        if suffix.startswith('S'):
            rid=next(iter(reading_by));reading=reading_by[rid];t['reading_id']=rid
            rf.update(reading['required_form_ids']);rs.update(reading['required_sense_ids']);rg+=reading['required_feature_ids'];local=copy.deepcopy(reading['local_support'])
    t['targeted_feature_ids']=uniq(rg);t.update(requirements(ident,rf,rs,rg,True));t['local_support']=local
    for h in local:
        for kind in ['form','sense','feature']:
            for rid in h.get(kind+'_ids',h.get(kind+'_refs',[])):checked(kind,rid,ident)
    if any(t['supplied_'+kind+'_ids'] for kind in ['form','sense','feature']) and not local:errors.append({'task_requires_unprinted_supplied_support':ident})
    for kind in ['form','sense','feature']:
        covered={rid for h in local for rid in h.get(kind+'_ids',[])}
        missing=set(t['supplied_'+kind+'_ids'])-covered
        if missing:errors.append({'task_supplied_records_missing_specific_help':ident,'kind':kind,'ids':sorted(missing)})
    t['assessment_boundary']='Supplied records remain visible at the point of use and are not tested for independent recall. Recognition cells support analysis, not unscaffolded production. Judge grammatical validity separately from a stated construction target.'
    t['grading_obligations']={'target':t['target_specification'],'essential_meaning':'Preserve participants, reference, number, person, tense and case relations, and the stated distinction between sequential, anterior and intended later events, reported perspective, and active/passive roles.','alternatives':'Accept documented inflectional variants and defensible word order or interpretation. Distinguish a valid alternative from compliance with an explicit target.','diagnoses':'Explain the particular case, agreement, stem, clause-function, mood, reference or unsupported-recall error rather than merely repeating a model.'}
    if t['mode'].startswith('production') or t['mode'].endswith('_production'):
        for kind in ['form','sense','feature']:
            for rid in t['tested_'+kind+'_ids']:
                r=checked(kind,rid,ident)
                if r and status(r) not in ['previously_taught','new_production']:errors.append({'production_requires_nontaught_record':ident,'record':rid,'status':status(r)})
    t['dependency_status']='unresolved' if any(u.get('owner')==ident for u in unresolved) else 'closed'
    m.update(key_id=t['key_id'],target=m.get('target',t['target_specification']),status='reconciled_private_model');models.append(m);tasks.append(t)
assert len(SP['items'])==38 and len(SEED['tasks'])==38
if len(tasks)!=76 or len(models)!=76:errors.append({'task_model_counts':[len(tasks),len(models)]})
if len({t['task_id'] for t in tasks})!=76:errors.append({'duplicate_task_id':True})
for t in tasks:
    if t['task_id'] in {p['task_id'] for p in SP['items']}:
        original=next(p['prompt_original'] for p in SP['items'] if p['task_id']==t['task_id'])
        if t['prompt']!=original:errors.append({'changed_Cook_prompt':t['task_id']})

teaching_records={}
def teaching(tid,kind):return teaching_records.setdefault(tid,{'teaching_id':tid,'type':kind,'graded':False,'form_ids':[],'sense_ids':[],'feature_ids':[],'evidence_refs':[]})
for p in paradigms:
    tr=teaching(p.get('teaching_id',p['paradigm_id']),'paradigm');tr['form_ids'] += [c['form_id'] for c in p['cells'] if c.get('form_id')];tr['evidence_refs']+=p.get('evidence_refs',[])
for pattern in load('curriculum/proposals/unit12/construction-patterns.json')['patterns']:
    tr=teaching(pattern['pattern_id'],'construction_pattern')
    tr['position_count']=pattern['position_count'];tr['new_inflectional_cell_count']=0
    tr['feature_ids']+=pattern['construction_feature_ids']
    for position in pattern['positions']:
        tr['form_ids']+=position['sequence']['required_form_ids']
        tr['sense_ids']+=position['sequence']['required_sense_ids']
    for fid in pattern['construction_feature_ids']:
        tr['evidence_refs']+=features[fid].get('evidence_refs',[])
for l in new_lemmas.values():
    for kind,key in [('forms','form_id'),('senses','sense_id')]:
        for r in l[kind]:
            ident=r[key];r['used_in_tasks']=sorted(USE[kind][ident]);r['assessed_in']=sorted(ASSESS[kind][ident])
            for tid in r['teaching_ids']:
                tr=teaching(tid,'vocabulary_or_local_support');tr[key.replace('_id','_ids')].append(ident);tr['evidence_refs']+=r.get('evidence_refs',[])
for fid,f in new_features.items():
    f['used_in_tasks']=sorted(USE['features'][fid]);f['assessed_in']=sorted(ASSESS['features'][fid])
    for tid in f['teaching_ids']:
        tr=teaching(tid,'grammar');tr['feature_ids'].append(fid);tr['evidence_refs']+=f.get('evidence_refs',[])
for tr in teaching_records.values():
    for key in ['form_ids','sense_ids','feature_ids','evidence_refs']:tr[key]=uniq(tr[key])
prior_requirements={}
for kind,previous in [('forms',prior_forms),('senses',prior_senses),('features',prior_features)]:
    prior_requirements[kind]=[{'id':rid,'knowledge_status':prior_status(previous[rid]),'actual_prior_record':{k:copy.deepcopy(v) for k,v in previous[rid].items() if k!='records_by_chapter'},'used_in_tasks':sorted(USE[kind][rid]),'promoted_in_this_unit':any(p['record_id']==rid for p in promotions)} for rid in sorted(USE[kind]) if rid in previous]

evidence_by={}
for path in ['sources/audits/unit12-source/evidence-catalog.json','sources/audits/unit12-grammar/evidence-catalog.json']:
    if not (ROOT/path).exists():
        unresolved.append({'missing_final_evidence_catalog':path});continue
    cat=load(path);records=cat.get('records',cat.get('evidence',[])) if isinstance(cat,dict) else cat
    if isinstance(records,dict):records=[{'evidence_id':k,**copy.deepcopy(v)} for k,v in records.items()]
    for record in records:
        record=copy.deepcopy(record)
        for image_record in record.get('images',[]):
            if isinstance(image_record,dict) and image_record.get('image') and not image_record.get('path'):
                image_record['path']=image_record['image']
        rid=record.get('evidence_id',record.get('id'))
        if rid in evidence_by and evidence_by[rid]!=record:errors.append({'conflicting_evidence':rid})
        evidence_by[rid]=record
prior_evidence={ref for table in [prior_forms,prior_senses,prior_features] for record in table.values() for ref in record.get('evidence_refs',[])}
for r in [x for l in new_lemmas.values() for kind in ['forms','senses'] for x in l[kind]]+list(new_features.values())+paradigms:
    for ref in r.get('evidence_refs',[]):
        if ref not in evidence_by and ref not in prior_evidence:errors.append({'unresolved_evidence_ref':ref,'owner':r.get('form_id',r.get('sense_id',r.get('feature_id',r.get('paradigm_id'))))})

route_keys={(r['paradigm_id'],r['form_id']) for r in MAT['paradigm_cell_display_routes']}
par_keys={(p['paradigm_id'],c['form_id']) for p in paradigms for c in p['cells'] if c.get('form_id')}
if route_keys!=par_keys:errors.append({'paradigm_display_mismatch':{'missing':sorted(par_keys-route_keys),'extra':sorted(route_keys-par_keys)}})
if len(route_keys)!=len(MAT['paradigm_cell_display_routes']):errors.append({'duplicate_paradigm_display_route':True})
for package in [PUBLIC,PRIVATE,PCB]:errors.extend({'binding_issue':i} for i in package.get('issues',[]))
frames=load('sources/audits/unit12-grammar/lexical-frames.json')['frames']
grammar_rules_path='sources/audits/unit12-grammar/rules.json'
grammar_rules=load(grammar_rules_path)['rules'] if (ROOT/grammar_rules_path).exists() else []
if not grammar_rules:unresolved.append({'missing_final_grammar_rules':grammar_rules_path})
for t in tasks+examples+compositions:t['lexical_frame_ids']=[f['frame_id'] for f in frames if f['sense_id'] in t['required_sense_ids']]

exclusions=uniq([str(p.relative_to(ROOT)).replace('\\','/') for folder in ['curriculum/proposals/unit12','sources/audits/unit12-source','sources/audits/unit12-coordinator'] for p in (ROOT/folder).glob('**/*') if p.is_file() and (p.name.startswith('author-only-') or p.name.startswith('private') or p.name=='compare_witnesses.py')])
input_paths=['lexicon/entries.json','curriculum/grammar.json']
for folder in ['sources/audits/unit12-source','sources/audits/unit12-grammar']:
    input_paths += [str(p.relative_to(ROOT)).replace('\\','/') for p in (ROOT/folder).glob('*.json') if not p.name.startswith(('author-only-','private'))]
display={'matrices_file':'curriculum/proposals/unit12/display-matrices.json','nominal_derivations_file':'curriculum/proposals/unit12/nominal-display-plan.json','grammar_diagnostics_file':'curriculum/proposals/unit12/grammar-display-plan.json','nominal_counts':NDP['counts'],'matrix_count':len(MAT['matrices']),'paradigm_count':len(paradigms),'logical_paradigm_cell_count':len(par_keys),'logical_cell_display_coverage':MAT['paradigm_cell_display_routes'],'shared_model_derivations':NDP['derivations'],'lexical_diagnostics':NDP['diagnostic_rows'],'complete_table_requirement':'New fōt, hęre and brycg systems and every selected verbal system have complete displays. Familiar nominal and adjective families have checked routes to visible models and explicit lexical stems. Participle bases do not assign unlisted inflection or syntax. Twelve habban construction positions bind actual constituent records and are counted separately from inflectional cells.','order':['present and preterite in contextual time','complete supporting lexical systems and diagnostics','habban with object and participle','active and passive event roles','recognition of wesan periphrases','reported sequence without mechanical backshift','translated contextual examples','original form and meaning practice','all Cook VI.19–21','controlled connected account','exact Picts and Scots narrative with local help']}
display['construction_patterns_file']='curriculum/proposals/unit12/construction-patterns.json'
display['construction_patterns']=load('curriculum/proposals/unit12/construction-patterns.json')['patterns']

display['nonparadigm_form_routes']=[{'form_id':f['form_id'],'form':f['form'],'knowledge_status':f['knowledge_status'],'teaching_ids':f['teaching_ids'],'display_kind':'local_support' if f['knowledge_status']=='supplied' else 'vocabulary_literal','scope_note':f.get('scope_note','')} for l in new_lemmas.values() for f in l['forms'] if f['form_id'] not in form_teaching_ids]
display['independent_verbal_display_crosscheck']='curriculum/proposals/unit12/verb-display-crosscheck.json'
inventory={'schema_version':1,'chapter':'ch12','status':'reconciled_pre_contract_design' if not errors and not unresolved else 'reconciliation_incomplete','prerequisite_chapters':[f'ch{i:02}' for i in range(1,12)],'prior_audit':'curriculum/proposals/unit12/prior-audit.json','prior_baseline_checkpoint':'74da7bb','source_authorities':uniq(e['source_id'] for e in evidence_by.values() if e.get('source_id')),'analysis_input_hashes':{p:digest(p) for p in input_paths},'evidence_catalog':list(evidence_by.values()),'lemmas':list(new_lemmas.values()),'features':list(new_features.values()),'paradigms':paradigms,'teaching_records':list(teaching_records.values()),'readings':readings,'prior_requirements':prior_requirements,'form_id_aliases':{},'sense_id_aliases':{},'promotions':promotions,'form_identity_reconciliation':SL.get('prior_form_reconciliations',[])+reconciliations,'display_plan':display,'audited_inflection_rules':SN['rules']+grammar_rules,'lexical_frames':frames,'lexical_frames_source':'sources/audits/unit12-grammar/lexical-frames.json','independent_composition_review':'sources/audits/unit12-source/composition-independent-check.json','independent_composition_grammar_review':'sources/audits/unit12-grammar/public-composition-review.json','independent_image_crosscheck':'curriculum/proposals/unit12/source-crosscheck.json','limits':['The actual eleven-unit baseline alone establishes prior teaching.','Present and preterite are morphological categories; context supplies temporal relations and English translation.','Productive habban compounds use an accusative object and selected uninflected participle bases; the indicative construction display does not invent new inflected words or exhaust all moods.','Reported anterior compounds reuse prior subjunctive morphology; reported simultaneous, anterior and intended later events are distinguished without mechanical backshift.','Wesan with intransitive past participles and present participles is newly assigned for recognition, with contextual interpretation.','Complete participle bases do not assign unlisted adjective declensions or unrestricted auxiliary selection.','Recognition number counterparts, adjective instrumental reference cells and exact supplied source spellings retain their separate scope.','The exact connected source span preserves both paragraphs, all21 attached original notes and source spelling.','Source aids remain visible during supported tasks and never become unaided-recall targets.'],'pre_key_review_exclusions':exclusions,'review_independence':'The reserved reviewer receives public tasks, learner inputs and unordered dependency sets; complete private translations and ordered required outputs remain excluded until independent solutions are frozen.','original_notes_count':sum(len(r['original_notes']) for r in readings),'referenced_source_notes_count':sum(len(r.get('referenced_notes',[])) for r in readings),'local_source_help_count':sum(len(r['local_support']) for r in readings)}
counts={'tasks':len(tasks),'cook_tasks':len(cook_seeds),'original_tasks':len(SEED['tasks']),'teaching_examples':len(examples),'controlled_reading_words':compositions[0]['word_count'],'source_reading_words':sum(r['word_count'] for r in readings),'source_reading_spans':len(readings),'source_notes':inventory['original_notes_count'],'source_referenced_notes':inventory['referenced_source_notes_count'],'source_helps':inventory['local_source_help_count'],'Cook_local_helps':len(CH['supports']),'all_proposed_lemmas':len(new_lemmas),'new_lemma_identities':sum(lid not in {l['lemma_id'] for l in LP['lemmas']} for lid in new_lemmas),'proposed_forms':sum(len(l['forms']) for l in new_lemmas.values()),'proposed_senses':sum(len(l['senses']) for l in new_lemmas.values()),'new_form_identities':sum(f['form_id'] not in prior_forms for l in new_lemmas.values() for f in l['forms']),'new_sense_identities':sum(s['sense_id'] not in prior_senses for l in new_lemmas.values() for s in l['senses']),'features':len(new_features),'paradigms':len(paradigms),'logical_paradigm_cells':len(par_keys),'literal_display_cells':MAT['counts']['literal_cells'],'derived_display_cells':MAT['counts']['derived_cells'],'display_matrices':len(MAT['matrices']),'promotions':len(promotions)}
inventory['review_independence']='The reserved reviewer receives public tasks and unordered dependency sets. A disclosed answer-bearing message exposed EX-VI-21-04 only; no private files were opened. Their independent solve therefore covers75 unexposed tasks. A fresh unexposed reviewer must solve EX-VI-21-04 and freeze that solution before key access. All private files remain excluded until the corresponding independent solutions are frozen.'
inventory['reviewer_exposure']={'exposed_task_ids':['EX-VI-21-04'],'reserved_reviewer_unexposed_task_count':75,'fresh_unexposed_review_required':['EX-VI-21-04'],'cause':'A source-editor coordination message included the proposed answer clause; the recipient promptly disclosed it.','private_files_opened_before_solve':False}
inventory['limits'].append('The selected gemētt cell is present indicative third singular. Explain preterite gemētte without copying the lexical-audit contrast note about an unassigned gemētan past participle into learner prose. No gemētan participle system or extra supplied citation is assigned.')
counts['construction_patterns']=len(display['construction_patterns'])
counts['construction_positions']=sum(p['position_count'] for p in display['construction_patterns'])
counts['construction_new_inflectional_cells']=sum(p['new_inflectional_cell_count'] for p in display['construction_patterns'])
write('inventory.json',inventory)
write('task-plan.json',{'schema_version':1,'chapter':'ch12','status':inventory['status'],'origin_rule':'All38 exact Cook prompts and IDs retained; all38 original tasks declared new teaching material.','key_rule':'One stable private key entry per task.','tasks':tasks})
write('compositions.json',{'schema_version':1,'chapter':'ch12','status':inventory['status'],'private_interpretations':'Complete account/source translations remain in excluded author-only records.','teaching_examples':examples,'compositions':compositions})
write('author-only-models.json',{'schema_version':1,'chapter':'ch12','access':'PRIVATE: exclude until independent solutions are frozen.','models':models})
write('validation.json',{'schema_version':1,'chapter':'ch12','status':inventory['status'],'counts':counts,'errors':errors,'unresolved':unresolved,'pre_key_review_exclusions':exclusions})
print(json.dumps({'counts':counts,'error_count':len(errors),'error_types':dict(Counter(next(iter(e)) for e in errors)),'unresolved_count':len(unresolved),'unresolved':unresolved[:15]},ensure_ascii=False))
