"""Reconcile bounded Unit 13 design; never write the contract or registers."""
from pathlib import Path
from collections import defaultdict
import copy,hashlib,json
R=Path.cwd();O=R/'curriculum/proposals/unit13';issues=[];inputs={}
def load(p,optional=False):
    path=R/p
    if not path.exists():
        if not optional:issues.append({'missing_input':p})
        return {}
    inputs[p]=hashlib.sha256(path.read_bytes()).hexdigest()
    return json.loads(path.read_text(encoding='utf-8-sig'))
def save(n,d):(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def uniq(xs):return sorted(set(x for x in xs if x))
def state(r):return 'previously_taught' if r.get('production_taught_in') else 'previously_recognition' if r.get('recognition_taught_in') else 'previously_supplied'
LP=load('lexicon/entries.json');GP=load('curriculum/grammar.json')
packages=[load(p) for p in ['sources/audits/unit13-source/lexical-inventory.json','sources/audits/unit13-source/source-support-records.json','sources/audits/unit13-grammar/grammar-records.json','sources/audits/unit13-grammar/source-support.json']]
SN=load('sources/audits/unit13-source/noun-adjective-paradigms.json');G=packages[2]
GF=load('sources/audits/unit13-grammar/lexical-frames.json');PP=load('sources/audits/unit13-grammar/principal-parts.json')
SP=load('sources/audits/unit13-source/exercises-prompts.json');SD=load('sources/audits/unit13-source/exercises-dependencies.json')
SR=load('sources/audits/unit13-source/reading-source.json');ST=load('sources/audits/unit13-source/reading-tokens.json')
SH=load('sources/audits/unit13-source/reading-support.json');SF=load('sources/audits/unit13-source/reading-constructions.json')
CH=load('sources/audits/unit13-source/cook-local-support.json');CF=load('sources/audits/unit13-source/construction-requirements.json')
SEED=load('curriculum/proposals/unit13/task-seed.json');COMP=load('curriculum/proposals/unit13/composition-seed.json');CT=load('curriculum/proposals/unit13/cook-targets.json')
PUB=load('curriculum/proposals/unit13/public-sequence-bindings.json');PRIV=load('curriculum/proposals/unit13/author-only-sequence-bindings.json');COOK=load('curriculum/proposals/unit13/author-only-cook-sequence-bindings.json');PM=load('curriculum/proposals/unit13/author-only-model-seed.json')
ND=load('curriculum/proposals/unit13/nominal-display-plan.json');GD=load('curriculum/proposals/unit13/grammar-display-plan.json');MAT=load('curriculum/proposals/unit13/display-matrices.json')
EC=[load('sources/audits/unit13-source/evidence-catalog.json'),load('sources/audits/unit13-grammar/evidence-catalog.json')]
prior={'forms':{f['form_id']:{**copy.deepcopy(f),'lemma_id':l['lemma_id']} for l in LP.get('lemmas',[]) for f in l.get('forms',[])},'senses':{s['sense_id']:{**copy.deepcopy(s),'lemma_id':l['lemma_id']} for l in LP.get('lemmas',[]) for s in l.get('senses',[])},'features':{f['feature_id']:copy.deepcopy(f) for f in GP.get('features',[])}}
allrec={k:{i:{**r,'resolved_status':state(r)} for i,r in rs.items()} for k,rs in prior.items()}
newlem={};newfeat={};promotions=[];reconciliations=[]
for package in packages:
    for lemma in package.get('lemmas',[]):
        lid=lemma['lemma_id'];target=newlem.setdefault(lid,{k:copy.deepcopy(v) for k,v in lemma.items() if k not in ['forms','senses']})
        for key,ident in [('forms','form_id'),('senses','sense_id')]:
            target.setdefault(key,[]);have={r[ident]:r for r in target[key]}
            for record in lemma.get(key,[]):
                r=copy.deepcopy(record);rid=r[ident];old=prior[key].get(rid)
                r.setdefault('knowledge_status','supplied');r.setdefault('teaching_ids',['NEW-U13-VOC-'+lid.upper() if r['knowledge_status']!='supplied' else 'NEW-U13-LOCAL-HELPS'])
                if old:
                    for fld in (['form','analysis'] if key=='forms' else ['gloss']):
                        if fld in r and fld in old and r[fld]!=old[fld]:
                            reconciliations.append(dict(record_type=key[:-1],record_id=rid,canonical_field=fld,preserved_prior_value=copy.deepcopy(old[fld]),unit13_contextual_value=copy.deepcopy(r[fld]),policy='Preserve the original current register identity; refined Unit 13 context is separate.'))
                            r['unit13_contextual_'+fld]=r[fld];r[fld]=copy.deepcopy(old[fld])
                    for field in ['production_taught_in','recognition_taught_in','supplied_in']:r['prior_'+field]=old.get(field)
                    if old.get('production_taught_in'):r['knowledge_status']='previously_taught'
                    elif r['knowledge_status']=='new_production':promotions.append(dict(record_type=key[:-1],record_id=rid,from_status=state(old),to='new_production',previous_history={f:old.get(f) for f in ['production_taught_in','recognition_taught_in','supplied_in']},teaching_ids=r['teaching_ids']))
                if rid in have:
                    # Shared records can acquire several current teaching/evidence locations.
                    prev=have[rid]
                    for fld in ['teaching_ids','evidence_refs','used_in_tasks']:
                        if fld in r:prev[fld]=uniq(prev.get(fld,[])+r[fld])
                    if prev.get('knowledge_status') in ['supplied','new_recognition'] and r['knowledge_status']=='new_production':prev['knowledge_status']='new_production'
                    r=prev
                else:target[key].append(r);have[rid]=r
                allrec[key][rid]={**copy.deepcopy(r),'lemma_id':lid,'resolved_status':r['knowledge_status']}

for package in [G,SF,CF,packages[3]]:
    for f in package.get('features',package.get('requirements',[])):
        if not isinstance(f,dict) or not f.get('feature_id'):continue
        r=copy.deepcopy(f);fid=r['feature_id'];r.setdefault('knowledge_status','supplied');r.setdefault('teaching_ids',r.get('support_ids') or ['NEW-U13-GRAM-'+fid])
        if r['knowledge_status']=='previously_taught':
            if fid not in prior['features']:issues.append(dict(missing_actual_prior_feature=fid))
            continue
        if fid in newfeat:
            for field in ['evidence_refs','used_in_tasks']:
                if field in r:newfeat[fid][field]=uniq(newfeat[fid].get(field,[])+r[field])
            continue
        newfeat[fid]=r;allrec['features'][fid]={**r,'resolved_status':r['knowledge_status']}
nominal_feature_map=[]
for rule in SN.get('rules',[]):
    fid='u13-'+rule['rule_id'].removeprefix('U13-').lower();tid='NEW-U13-GRAM-'+rule['rule_id']
    f=dict(feature_id=fid,description=rule.get('text',rule.get('description','')),knowledge_status='new_production',teaching_ids=[tid],evidence_refs=rule.get('evidence_refs',[]),scope_note='The full recorded nominal systems retain individual sense/number limits; distinct instrumental reference cells create no independent instrumental use.')
    newfeat[fid]=f;allrec['features'][fid]={**f,'resolved_status':'new_production'};nominal_feature_map.append(dict(feature_id=fid,rule_id=rule['rule_id'],teaching_ids=[tid]))
save('nominal-feature-map.json',dict(features=nominal_feature_map))
form_morph_features=defaultdict(set);grammar_feature_map=[]
system_names={'IND':'indicative','SUBJ':'subjunctive','IMP':'imperative','INF':'infinitive-pair','PART':'participle-bases'}
for p in G.get('paradigms',[]):
    kind=p['paradigm_id'].rsplit('-',1)[-1];fid='u13-'+p['lemma_id']+'-'+system_names[kind]
    if fid not in newfeat:
        f=dict(feature_id=fid,description='Complete defined '+system_names[kind]+' morphology for '+p['lemma_id']+'.',knowledge_status='new_production',teaching_ids=[p['paradigm_id']],evidence_refs=p.get('evidence_refs',[]),scope_note=p.get('scope_note',p.get('scope','Individual cell scopes and lexical frames remain binding.')),rule_ids=uniq(allrec['forms'][c['form_id']].get('rule_id') for c in p['cells'] if c['form_id'] in allrec['forms']))
        newfeat[fid]=f;allrec['features'][fid]={**f,'resolved_status':'new_production'}
    for c in p['cells']:form_morph_features[c['form_id']].add(fid)
    grammar_feature_map.append(dict(feature_id=fid,paradigm_id=p['paradigm_id'],form_ids=[c['form_id'] for c in p['cells']]))
save('grammar-feature-map.json',dict(features=grammar_feature_map))

ROLE={
'clause_roles':['u13-clause-role-parsing','u08-clause-order'],
'fronting':['u13-main-fronting-order'],
'correlation':['u11-past-when-then','u11-clause-roles-order'],
'relative_reference':['u08-relative-the','u08-relative-internal-case'],
'coordination':['u13-coordination-predicate-recovery','u02-clause-coordination'],
'reference':['u13-reference-resolution-ambiguity','u02-pronoun-reference'],
'explicit_reference':['u13-reference-resolution-ambiguity'],
'quoted_reference':['u13-quoted-reference','u05-direct-quotation'],
'reported_reference':['u09-content-that','u09-report-reference','u12-reported-sequence'],
'long_sentence':['u13-long-sentence-analysis','u13-clause-role-parsing'],
'order_limits':['u13-main-fronting-order','u13-pronoun-position-limits','u08-clause-order'],
'kinship_systems':['u13-nom-kinship'],
'nominal_systems':['u13-nom-feminine','u13-nom-neuter','u13-nom-syncope','u13-nom-weak'],
'adjective_systems':[f['feature_id'] for f in nominal_feature_map if 'adj' in f['feature_id'] or 'comp' in f['feature_id']],
'verb_systems':[], 'source_reading':[], 'new_reading':[]}
EXTRA={
'01':['u02-direct-object','u13-clause-role-parsing'], '02':['u02-direct-object','u13-main-fronting-order'], '03':['u02-direct-object','u13-main-fronting-order'],
'04':['u11-past-when-then','u02-direct-object','u10-to-destination','u13-long-sentence-analysis'],
'05':['u03-agreement','u13-reference-resolution-ambiguity'], '06':['u05-see-object','u02-clause-coordination','u13-reference-resolution-ambiguity'],
'07':['u05-see-object','on-dative-location','u13-reference-resolution-ambiguity'],
'08':['u05-direct-quotation','u13-quoted-reference','u06-volition-willan','u13-sprecan-conversation-mid'],
'09':['u08-relative-the','u08-relative-internal-case','u10-to-destination'],
'10':['u11-past-when-then','u13-clause-role-parsing'], '11':['u13-coordination-predicate-recovery','on-dative-location'],
'12':['u09-content-that','u09-report-reference','u12-reported-sequence','u03-agreement']}
COMMON_FRAMES={
'A01':['u12-gretan-indicative'], 'A02':['u12-gretan-indicative','u06-cuman-intransitive'],
'A03':['u12-gretan-indicative','u05-intransitive-posture','on-dative-location'],
'A04':['u12-gretan-indicative','u02-giving-recipient'], 'A05':['u03-agreement','on-dative-location','u06-cuman-intransitive'],
'A06':['u05-see-object','u05-intransitive-posture','on-dative-location'], 'A07':['u02-direct-object','u08-direct-questions'],
'A08':['on-dative-location'], 'A09':['on-dative-location'], 'A10':['on-dative-location','u05-intransitive-posture','u06-cuman-intransitive'],
'A11':['u12-gretan-indicative','u06-cuman-intransitive'],
'C01':['u02-direct-object'], 'C02':['u12-gretan-indicative'], 'C03':['u06-cuman-intransitive'],
'C04':['u12-gretan-indicative','u10-to-destination'], 'C05':['u12-gretan-indicative','u10-to-destination'],
'C06':['u06-volition-willan','u13-sprecan-conversation-mid'], 'C07':['u05-see-object','u12-gretan-indicative'], 'C08':['u12-gretan-indicative','u06-cuman-intransitive'],
'S06':['u13-supported-long-fronting']}
READ_FEATURES=uniq(sum([ROLE[k] for k in ['clause_roles','correlation','relative_reference','coordination','reference','quoted_reference']],[])+['u02-direct-object','u02-giving-recipient','u05-intransitive-posture','on-dative-location','u10-to-destination','u09-mid-accompaniment','u06-volition-willan','u13-sprecan-conversation-mid','u13-laedan-person-direction','u03-possessor-reference','genitive-relationship','u03-possessive-agreement'])
for code in ['A11','C03','C08']:COMMON_FRAMES.setdefault(code,[]).append('u04-intransitive-actions')
COMMON_FRAMES['F06']=['u09-new-commands','u13-began-study']
EXTRA['10'].append('u04-intransitive-actions')
USE={k:defaultdict(set) for k in allrec};ASSESSED={k:defaultdict(set) for k in allrec}
def requirements(owner,forms=(),senses=(),features=(),assess=False):
    values={'forms':set(forms),'senses':set(senses),'features':set(features)}
    for fid in values['forms']:values['features'].update(form_morph_features.get(fid,[]))
    lids={allrec['forms'][f]['lemma_id'] for f in values['forms'] if f in allrec['forms']}
    if 'se' in lids:values['features'].add('article-agreement')
    if lids&{'he','ic','thu'}:values['features'].add('u02-pronoun-reference')
    result={}
    for kind,ids in values.items():
        singular=kind[:-1];required=uniq(ids);sup=[];tested=[]
        for rid in required:
            r=allrec[kind].get(rid);USE[kind][rid].add(owner)
            if r is None:issues.append(dict(owner=owner,missing_record_type=kind,missing_id=rid));continue
            if r['resolved_status'] in ['supplied','previously_supplied']:sup.append(rid)
            elif assess:tested.append(rid);ASSESSED[kind][rid].add(owner)
        result['required_'+singular+'_ids']=required;result['supplied_'+singular+'_ids']=sup
        if assess:result['tested_'+singular+'_ids']=tested
    return result
def bind(token,owner):
    t=copy.deepcopy(token);t.pop('referent',None)
    f=allrec['forms'].get(t.get('form_id'));s=allrec['senses'].get(t.get('sense_id'))
    if not f or not s:issues.append(dict(owner=owner,unresolved_token=t.get('token_id',t.get('token_index')),surface=t.get('surface')));return t
    if f['lemma_id']!=s['lemma_id']:issues.append(dict(owner=owner,token_lemma_mismatch=t))
    surface=t.get('surface',t.get('literal','')).strip('.,:;!?“”"()[]')
    if surface.casefold()!=f['form'].casefold():issues.append(dict(owner=owner,surface_mismatch=surface,form_id=f['form_id'],registered=f['form']))
    t.update(surface=surface,form=f['form'],analysis=copy.deepcopy(f.get('analysis')),form_status=f['resolved_status'],sense_status=s['resolved_status'])
    return t
def supports(package):
    result=[]
    for original in package.get('supports',[]):
        h=copy.deepcopy(original);cov=h.get('covers',{});h['text']=h.get('text',h.get('learner_help',''));h['knowledge_status']='supplied'
        for name,key in [('form','form_ids'),('sense','sense_ids'),('feature','construction_ids')]:h[name+'_ids']=uniq(h.get(name+'_ids',[])+cov.get(key,[]))
        h['teaching_id']=h.get('teaching_id',h['support_id']);h['display_obligation']='Print the exact help at its assigned task or reading location; keep it visible during assessment.';result.append(h)
    return result
source_help=supports(SH);cook_help=supports(CH);grammar_help=[]
for row in PP.get('rows',[]):
    lid=row['lemma_id'];citations=row['citations'];h=dict(support_id='NEW-U13-PRINCIPAL-PARTS-'+lid.upper(),teaching_id='NEW-U13-PRINCIPAL-PARTS-'+lid.upper(),knowledge_status='supplied',text='Citation support: '+', '.join(c['form'] if isinstance(c,dict) else c for c in citations)+'. These four printed parts identify the present, preterite singular, preterite plural and past participle stems. Keep the row visible; only the separately assigned systems and uses are recall targets.',form_ids=uniq(c['form_id'] for c in citations if isinstance(c,dict)),sense_ids=uniq(c['sense_id'] for c in citations if isinstance(c,dict)),feature_ids=[],task_ids=['NEW-U13-F05'] if lid=='forceorfan' else [],display_location=row.get('finite_paradigm_id','NEW-U13-PAR-'+lid.upper()+'-IND'),evidence_refs=row.get('evidence_refs',[]),require_independent_recall=False)
    grammar_help.append(h)
public_by=defaultdict(list);private_by=defaultdict(list)
for s in PUB.get('sequences',[]):public_by[s['owner_id']].append(s)
for s in PRIV.get('sequences',[])+COOK.get('sequences',[]):private_by[s['owner_id']].append(s)
private_models={m['task_id']:m for m in PM.get('models',[])}
examples=[]
for e in COMP.get('teaching_examples',[]):
    eid=e['example_id'];seq=public_by[eid][0];rg=EXTRA[eid[-2:]]
    examples.append({**copy.deepcopy(e),'tokens':[bind(t,eid) for t in seq['tokens']],'word_count':len(e['text'].split()),**requirements(eid,seq['required_form_ids'],seq['required_sense_ids'],rg)})
compositions=[]
if COMP.get('new_reading'):
    c=COMP['new_reading'];cid=c['span_id'];seq=public_by[cid][0]
    compositions.append({**copy.deepcopy(c),'composition_id':cid,'tokens':[bind(t,cid) for t in seq['tokens']],**requirements(cid,seq['required_form_ids'],seq['required_sense_ids'],READ_FEATURES)})
readings=[]
if SR:
    rid=SR['span_id'];words=SR['learner_text'].split();tokens=[]
    for i,t in enumerate(ST.get('tokens',[]),1):
        t=bind(t,rid);t.update(token_index=i,literal=words[i-1]);tokens.append(t)
    rg=[f['feature_id'] for f in SF.get('requirements',[])]+['u13-long-sentence-analysis','u13-reference-resolution-ambiguity','u13-supported-long-fronting','u13-pronoun-position-limits']
    readings.append({**copy.deepcopy(SR),'source_span_id':rid,'exact_text_without_note_cues':SR['learner_text'],'word_count_whitespace':len(words),'tokens':tokens,'local_support':source_help,**requirements(rid,[t.get('form_id') for t in tokens],[t.get('sense_id') for t in tokens],rg)})
source_examples=[]
for e in packages[3].get('source_evidence_examples',[]):
    e=copy.deepcopy(e);owner=e.get('example_id',e.get('source_example_id'));tokens=[bind(t,owner) for t in e.get('tokens',[])]
    e.update(tokens=tokens,**requirements(owner,[t.get('form_id') for t in tokens],[t.get('sense_id') for t in tokens],e.get('required_feature_ids',[])));source_examples.append(e)
    grammar_help.append(dict(support_id='NEW-U13-SOURCE-ORDER-HELP',teaching_id='NEW-U13-SOURCE-ORDER-HELP',knowledge_status='supplied',text=e['local_support'],form_ids=e['required_form_ids'],sense_ids=e['required_sense_ids'],feature_ids=[],task_ids=['NEW-U13-A12'],display_location=owner,evidence_refs=e.get('evidence_refs',[]),require_independent_recall=False))

tasks=[];target_by={t['task_id']:t['target_specification'] for t in CT.get('targets',[])}
source_dep={x.get('task_id',x.get('item_id')):x for x in SD.get('items',[])}
def help_for(owner):return [h for h in cook_help+grammar_help if owner in h.get('task_ids',h.get('used_in_tasks',[])) or h.get('task_id')==owner]
def finalize_task(t,rf,rs,rg,local,production=False):
    owner=t['task_id'];req=requirements(owner,rf,rs,rg,assess=True);t.update(req)
    for name,kind in [('form','forms'),('sense','senses'),('feature','features')]:
        locally_supplied={rid for h in local for rid in h.get(name+'_ids',[])}&set(req['required_'+name+'_ids'])
        t['supplied_'+name+'_ids']=uniq(t['supplied_'+name+'_ids']+list(locally_supplied))
        t['tested_'+name+'_ids']=[rid for rid in t['tested_'+name+'_ids'] if rid not in locally_supplied]
        for rid in locally_supplied:ASSESSED[kind][rid].discard(owner)
    t['local_support']=local;t['dependency_status']='closed' if not any(i.get('owner')==owner for i in issues) else 'pending'
    t['assessment_boundary']='Supplied forms, senses and constructions remain visible and are not tested for independent recall. Recognition analysis does not imply production. Judge grammatical validity separately from a stated target.'
    t['grading_obligations']=dict(target=t['target_specification'],essential_meaning='Preserve participants, case relations, agreement, clause dependencies, reference, temporal viewpoint and all original source controls.',alternatives='Accept defensible source variants and ordering alternatives while distinguishing them from explicit exercise targets.',diagnoses='Explain the specific form, case, agreement, lexical sense, clause-boundary, reference or unsupported-recall error.')
    if production:
        for kind in ['forms','senses','features']:
            for rid in req['required_'+kind[:-1]+'_ids']:
                r=allrec[kind].get(rid)
                if r and r['resolved_status'] in ['new_recognition','previously_recognition'] and rid not in t['supplied_'+kind[:-1]+'_ids']:issues.append(dict(owner=owner,recognition_used_for_production=rid,record_type=kind))
    tasks.append(t)
for original in SEED.get('tasks',[]):
    t=copy.deepcopy(original);owner=t['task_id'];code=owner.removeprefix('NEW-U13-');rf=[];rs=[]
    rg=sum([ROLE.get(role,[]) for role in t.get('feature_roles',[])],[])+COMMON_FRAMES.get(code,[])
    seqs=public_by[owner];t['input_sequences']=[]
    for seq in seqs:
        rf+=seq['required_form_ids'];rs+=seq['required_sense_ids'];t['input_sequences'].append({**copy.deepcopy(seq),'tokens':[bind(x,owner) for x in seq['tokens']]})
    for seq in private_by[owner]:rf+=seq['required_form_ids'];rs+=seq['required_sense_ids']
    m=private_models.get(owner,{})
    for cell in m.get('morphological_outputs',[]):
        rf.append(cell['form_id']);f=allrec['forms'].get(cell['form_id'])
        if f:
            lemma=newlem.get(f['lemma_id'])
            if lemma:rs.extend(s['sense_id'] for s in lemma.get('senses',[]) if s['knowledge_status']!='supplied')
    local=help_for(owner)
    if code=='A12' and source_examples:
        e=source_examples[0];rf+=e['required_form_ids'];rs+=e['required_sense_ids'];rg+=e['required_feature_ids'];t['input_example_ids']=[e['example_id']]
    if code=='F05':
        for h in local:rf+=h['form_ids'];rs+=h['sense_ids'];rg+=h['feature_ids']
    if code.startswith('R') and compositions:
        c=compositions[0];rf+=c['required_form_ids'];rs+=c['required_sense_ids'];rg+=c['required_feature_ids'];t['input_span_ids']=[c['span_id']]
    if code.startswith('S') and readings:
        c=readings[0];rf+=c['required_form_ids'];rs+=c['required_sense_ids'];rg+=c['required_feature_ids'];local=source_help;t['input_span_ids']=[c['source_span_id']]
    t['targeted_feature_ids']=uniq(rg);t['input_sequence_ids']=[s['sequence_id'] for s in seqs]
    t['required_input_form_ids']=uniq(f for s in seqs for f in s['required_form_ids'])
    t['required_input_sense_ids']=uniq(f for s in seqs for f in s['required_sense_ids'])
    if code.startswith(('R','S')) and (compositions if code.startswith('R') else readings):
        t['required_input_form_ids']=c['required_form_ids'];t['required_input_sense_ids']=c['required_sense_ids']
    t['required_output_form_ids']=uniq([f for s in private_by[owner] for f in s['required_form_ids']]+[c['form_id'] for c in m.get('morphological_outputs',[])])
    t['required_output_sense_ids']=uniq(f for s in private_by[owner] for f in s['required_sense_ids'])
    finalize_task(t,rf,rs,rg,local,production=t['mode'].startswith('production'))
for item in SP.get('items',[]):
    owner=item['item_id'];dep=source_dep.get(owner,{})
    seqs=private_by[owner];rf=[];rs=[]
    for seq in seqs:rf+=seq['required_form_ids'];rs+=seq['required_sense_ids']
    rg=dep.get('required_feature_ids',dep.get('construction_ids',[]))
    t=dict(task_id=owner,key_id='KEY-'+owner,origin='exact_source',mode='supported_production_translation',prompt=item['prompt'],source_item_id=owner,source_id=item['source_id'],source_group=item['group'],exercise=item['exercise'],item=item['item'],source_locators={k:item[k] for k in ['printed_pages','pdf_pages_one_based','original_identifier']},evidence_refs=item['evidence_refs'],target_specification=target_by[owner],input_texts=[],input_sequences=[],input_sequence_ids=[],requested_outputs=[dict(kind='old_english_translation',count=1)],targeted_feature_ids=uniq(rg))
    t.update(required_input_form_ids=[],required_input_sense_ids=[],required_output_form_ids=uniq(rf),required_output_sense_ids=uniq(rs))
    finalize_task(t,rf,rs,rg,help_for(owner),production=True)

def output_positions(t):
    owner=t['task_id'];result=[]
    def add(kind,label,**fields):result.append(dict(output_position_id=owner+'-O'+str(len(result)+1).zfill(3),kind=kind,label=label,**fields))
    morphology=private_models.get(owner,{}).get('morphological_outputs',[])
    for c in morphology:
        r=allrec['forms'].get(c['form_id'],{});a=c.get('analysis',{})
        add('morphological_form',r.get('lemma_id','')+' '+', '.join(str(v) for v in a.values()),lemma_id=r.get('lemma_id'),requested_analysis=a)
    for request in t['requested_outputs']:
        kind=request['kind']
        if morphology and kind in ['paradigm','form','comparison_diagnostics','commands','participle_bases']:continue
        labels=next((request[k] for k in ['positions','targets','fields','roles','tokens','actors'] if k in request),None)
        if labels is not None:
            for label in labels:add(kind,str(label))
        elif 'per_input' in request:
            for i in range(1,len(t.get('input_texts',[]))+1):
                for label in request['per_input']:add(kind,'Input '+str(i)+': '+label)
        elif 'per_clause' in request:
            for i in range(1,3):
                for label in request['per_clause']:add(kind,'Selected clause '+str(i)+': '+label)
        elif request.get('count'):
            for i in range(1,request['count']+1):add(kind,str(i))
        else:add(kind,request.get('topic',request.get('target',request.get('span_id',request.get('token',kind)))))
    return result
for t in tasks:
    t['requested_output_positions']=output_positions(t)
    if not t['requested_output_positions']:issues.append(dict(owner=t['task_id'],error='no_requested_output_positions'))

paradigms=copy.deepcopy(SN.get('paradigms',[])+G.get('paradigms',[]));teaching=[]
for p in paradigms:
    owner=p.get('teaching_id',p['paradigm_id']);req=requirements(owner,[c['form_id'] for c in p['cells']])
    teaching.append(dict(teaching_id=owner,type='paradigm',graded=False,form_ids=req['required_form_ids'],sense_ids=[],feature_ids=[],evidence_refs=p.get('evidence_refs',[]),display_location='display_plan.paradigm_cell_display_routes'))
for lid,l in newlem.items():
    tid='NEW-U13-VOC-'+lid.upper();req=requirements(tid,(),[s['sense_id'] for s in l.get('senses',[])])
    teaching.append(dict(teaching_id=tid,type='vocabulary',graded=False,form_ids=[],sense_ids=req['required_sense_ids'],feature_ids=[],evidence_refs=l.get('evidence_refs',[]),display_location='vocabulary row '+l['display_headword']))
for fid,f in newfeat.items():
    tid=f['teaching_ids'][0];requirements(tid,features=[fid]);teaching.append(dict(teaching_id=tid,type='grammar_or_local_help',graded=False,form_ids=[],sense_ids=[],feature_ids=[fid],evidence_refs=f.get('evidence_refs',[]),display_location='local help' if f['knowledge_status']=='supplied' else 'grammar explanation and examples'))
for h in source_help+cook_help+grammar_help:
    tid=h['teaching_id'];req=requirements(tid,h['form_ids'],h['sense_ids'],h['feature_ids']);teaching.append(dict(teaching_id=tid,type='local_support',graded=False,form_ids=req['required_form_ids'],sense_ids=req['required_sense_ids'],feature_ids=req['required_feature_ids'],evidence_refs=h.get('evidence_refs',[]),display_location=h.get('source_span_id',h.get('task_ids',[])),text=h['text']))
teacher_by={}
for t in teaching:
    tid=t['teaching_id']
    if tid not in teacher_by:teacher_by[tid]=copy.deepcopy(t);continue
    old=teacher_by[tid]
    for k in ['form_ids','sense_ids','feature_ids','evidence_refs']:old[k]=uniq(old.get(k,[])+t.get(k,[]))
    if t['type']=='local_support':old.update({k:t[k] for k in ['type','text','display_location']})
routes_by_form=defaultdict(list)
for p in paradigms:
    for c in p['cells']:routes_by_form[c['form_id']].append(p['paradigm_id'])
for kind,records in [('forms',[r for l in newlem.values() for r in l['forms']]),('senses',[r for l in newlem.values() for r in l['senses']]),('features',list(newfeat.values()))]:
    key=kind[:-1]+'_id'
    for r in records:
        rid=r[key]
        for tid in r.get('teaching_ids',[]):
            if tid in teacher_by:
                teacher_by[tid][kind[:-1]+'_ids']=uniq(teacher_by[tid].get(kind[:-1]+'_ids',[])+[rid]);continue
            location=routes_by_form.get(rid,[])
            teacher_by[tid]=dict(teaching_id=tid,type='recorded_teaching_alias',graded=False,form_ids=[rid] if kind=='forms' else [],sense_ids=[rid] if kind=='senses' else [],feature_ids=[rid] if kind=='features' else [],evidence_refs=r.get('evidence_refs',[]),display_location=location or 'The corresponding visible vocabulary, grammar or local-help row; the task-specific support contract still applies.',paradigm_ids=location,scope_note='This is a named location for the recorded instruction, not an additional paradigm or a new use inferred from a table.')
teaching=list(teacher_by.values())
for kind,records in allrec.items():
    for rid,r in records.items():
        if rid in USE[kind]:r['used_in_tasks']=uniq(USE[kind][rid]);r['assessed_in']=uniq(ASSESSED[kind][rid])
for l in newlem.values():
    for kind,key in [('forms','form_id'),('senses','sense_id')]:
        for r in l[kind]:r['used_in_tasks']=uniq(USE[kind][r[key]]);r['assessed_in']=uniq(ASSESSED[kind][r[key]])
for fid,f in newfeat.items():f['used_in_tasks']=uniq(USE['features'][fid]);f['assessed_in']=uniq(ASSESSED['features'][fid])
prior_req={kind:[dict(id=rid,knowledge_status=state(prior[kind][rid]),actual_prior_record=copy.deepcopy(prior[kind][rid]),used_in_tasks=uniq(owners),promoted_in_this_unit=any(p['record_id']==rid for p in promotions)) for rid,owners in sorted(USE[kind].items()) if rid in prior[kind]] for kind in prior}
for kind,records in prior_req.items():
    key=kind[:-1]+'_ids'
    for r in records:
        rid=r['id'];r['current_teaching_ids']=uniq(t['teaching_id'] for t in teaching if rid in t.get(key,[]))
        r['current_supplied_in_tasks']=uniq(t['task_id'] for t in tasks if rid in t.get('supplied_'+key,[]))
        r['current_support_teaching_ids']=uniq(h['teaching_id'] for h in source_help+cook_help+grammar_help if rid in h.get(key,[]))
evidence={}
for cat in EC:
    source=cat.get('evidence_catalog',cat.get('evidence',cat))
    if isinstance(source,list):source={r.get('evidence_id',r.get('id')):r for r in source}
    if isinstance(source,dict):evidence.update(source)
excluded=uniq([str(p.relative_to(R)).replace('\\','/') for base in [R/'curriculum/proposals/unit13',R/'sources/audits/unit13-source',R/'sources/audits/unit13-grammar',R/'sources/audits/unit13-coordinator'] for p in base.rglob('*') if p.is_file() and p.suffix in ['.json','.md','.py']]+['chapters/ch13/coverage.json','curriculum/UNIT_13_BRIEF.md','chapters/ch13/answer-key.md','sources/audits/unit13-coordinator/author-only-source-first.md'])
limits=['Only the actual twelve-unit baseline establishes prior teaching.','Clause order is taught as evidenced tendencies, with constituent counting and pronoun exceptions; Cook25.7 retains its own explicit verb-last target.','Reference can remain ambiguous; no nearest-noun or exclusively human masculine-pronoun rule is taught.','Complete morphology assigns only its stated senses, numbers, moods and ordinary uses.','Exact source and Cook aids remain visible during supported tasks and never become unaided-recall requirements.','Existing register surfaces, analyses and histories remain unchanged; current contextual refinements are separately recorded.','The continuous reading ends at153.9 mid wes; the separately supported source-order fragment does not extend it.']
display=dict(matrices=MAT.get('matrices',[]),paradigm_cell_display_routes=MAT.get('paradigm_cell_display_routes',[]),nominal_display_plan='curriculum/proposals/unit13/nominal-display-plan.json',grammar_display_plan='curriculum/proposals/unit13/grammar-display-plan.json',nominal_diagnostic_rows=ND.get('diagnostic_rows',[]),nominal_derivations=ND.get('derivations',[]),grammar_diagnostics=GD.get('diagnostics',[]),counts=MAT.get('counts',MAT.get('nominal_counts',{})),complete_table_requirement='Every defined system has a complete literal matrix or explicit verified model route. Print diagnostic stems, rules, variants and scope limits with the matrices.')
display['grammar_derivations']=GD.get('derivations',[])
display['lexical_diagnostics']=ND.get('diagnostic_rows',[])+[d for d in GD.get('diagnostics',[]) if d.get('row_id')]
for reading in readings:
    reading['teaching_id']='NEW-U13-SOURCE-READING'
    reading['source_image_refs']=uniq(evidence[e]['image_path'] for e in reading.get('evidence_refs',[]) if e in evidence and evidence[e].get('image_path'))
inventory=dict(schema_version=1,chapter='ch13',status='reconciled_pre_contract_design' if not issues else 'pre_contract_design_pending_reconciliation',prerequisite_chapters=[f'ch{i:02}' for i in range(1,13)],prior_audit='curriculum/proposals/unit13/prior-audit.json',prior_baseline_checkpoint='e17fc5f',source_authorities=['sources/registry.json','sources/audits/unit13-source/exercises-prompts.json','sources/audits/unit13-source/reading-source.json','sources/audits/unit13-grammar/grammar-records.json'],analysis_input_hashes=inputs,evidence_catalog=evidence,lemmas=list(newlem.values()),features=list(newfeat.values()),paradigms=paradigms,teaching_records=teaching,readings=readings,source_evidence_examples=source_examples,prior_requirements=prior_req,form_id_aliases={},sense_id_aliases={},promotions=promotions,form_identity_reconciliation=reconciliations,display_plan=display,audited_inflection_rules=SN.get('rules',[])+G.get('rules',[]),lexical_frames=G.get('lexical_frames',[]),limits=limits,pre_key_review_exclusions=excluded,review_independence='The fresh solver receives only the actual learner master, prior accepted units/registers and necessary original page images. Every current audit, proposal, contract analysis and answer-bearing file is withheld until frozen solutions.',original_notes_count=len(SR.get('original_notes',[])),local_source_help_count=len(source_help),local_cook_help_count=len(cook_help))
for data in [PUB,PRIV,COOK]:
    if data.get('issues'):issues.extend(data['issues'])
summary=dict(tasks=len(tasks),cook_tasks=sum(t['task_id'].startswith('EX-') for t in tasks),original_tasks=sum(t['task_id'].startswith('NEW-') for t in tasks),examples=len(examples),new_reading_words=[c['word_count'] for c in compositions],source_words=[r['word_count_whitespace'] for r in readings],paradigms=len(paradigms),cells=sum(len(p['cells']) for p in paradigms),new_inventory_lemmas=len(newlem),features=len(newfeat),prior_required_forms=len(prior_req['forms']),prior_required_senses=len(prior_req['senses']),prior_required_features=len(prior_req['features']))
inventory.update(status='reconciled_pre_contract_design' if not issues else 'pre_contract_design_pending_reconciliation',counts=summary,lexical_frames=GF.get('frames',[]),principal_parts=PP.get('rows',[]),nominal_feature_map=nominal_feature_map,grammar_feature_map=grammar_feature_map,independent_reviews=['sources/audits/unit13-source/nominal-display-review.json','sources/audits/unit13-grammar/public-composition-review.json','sources/audits/unit13-grammar/REPORT.md'],coordinator_preposition_evidence='sources/audits/unit13-coordinator/preposition-evidence.json')
inventory['source_note_anchors']=load('sources/audits/unit13-source/reading-note-anchors.json').get('notes',[])
save('inventory.json',inventory)
save('task-plan.json',dict(schema_version=1,chapter='ch13',status=inventory['status'],origin_rule='All 52 exact Cook prompts and 38 original tasks remain. Original controls are preserved; editorial directions and supplied help are separate.',key_rule='One stable separate key entry per task.',tasks=tasks))
save('compositions.json',dict(schema_version=1,chapter='ch13',status=inventory['status'],private_interpretations='Full graded-reading translations and ordered outputs are excluded author-only records.',teaching_examples=examples,compositions=compositions,source_evidence_examples=source_examples))
save('validation.json',dict(schema_version=1,chapter='ch13',status='pass' if not issues else 'pending',counts=summary,issues=issues,scope='Structural identity checks supplement source/linguistic review and never certify truth by task closure.'))
print(json.dumps(dict(counts=summary,issues=len(issues),sample=issues[:15]),ensure_ascii=False))
