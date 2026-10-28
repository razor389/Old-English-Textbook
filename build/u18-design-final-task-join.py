from pathlib import Path
from collections import Counter
import copy
import hashlib
import json
import re
import unicodedata

O=Path('curriculum/proposals/unit18')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def norm(s):return unicodedata.normalize('NFC',s.strip('.,;:!?“”‘’\"()')).casefold()
def state(r):
    if r.get('production_taught_in'):return 'previously_taught'
    if r.get('recognition_taught_in'):return 'prior_recognition'
    return r.get('knowledge_status','supplied' if r.get('supplied_in') else 'unresolved')
lex=read('lexicon/entries.json');gram=read('curriculum/grammar.json');inv=read(O/'inventory.json')
old={'form':{f['form_id']:f for l in lex['lemmas'] for f in l['forms']},'sense':{s['sense_id']:s for l in lex['lemmas'] for s in l['senses']},'feature':{f['feature_id']:f for f in gram['features']}}
reg=copy.deepcopy(old)
owners={k:{r[k+'_id']:l['lemma_id'] for l in lex['lemmas'] for r in l[field]} for k,field in [('form','forms'),('sense','senses')]}
for l in inv['lemmas']:
    for k,field in [('form','forms'),('sense','senses')]:
        reg[k].update({r[k+'_id']:r for r in l[field]});owners[k].update({r[k+'_id']:l['lemma_id'] for r in l[field]})
reg['feature'].update({f['feature_id']:f for f in inv['features']})
tasks=read(O/'task-plan.json')['tasks'];bytask={t['task_id']:t for t in tasks}
cookpacket=read(O/'author-only-cook-sequence-bindings.json');cook={s['owner_id']:s for s in cookpacket['sequences']}
hints=read(O/'source-hint-inventory.json');hintseq={s['sequence_id']:s for s in hints['sequences']}
featuremap={r['task_id']:r['feature_ids'] for r in read(O/'source-feature-bindings.json')['rows']}
sourceprompts=read('sources/audits/unit18-source/exercises-prompts.json')
grammarpacket=read('sources/audits/unit18-grammar/senses-constructions-support.json')
readingverbs=read('sources/audits/unit18-grammar/reading-verbal-bindings.json')
controls=read(O/'input-reference-records.json')['records']
issues=[];supportseqs=[];supportrows=[]

def deps(seqs,k):return sorted({t[k+'_id'] for s in seqs for t in s['tokens'] if t.get(k+'_id')})
def route_span(words,phrase):
    want=[norm(w) for w in phrase.split()]
    got=[norm(w) for w in words]
    return [list(range(i+1,i+len(want)+1)) for i in range(len(got)-len(want)+1) if got[i:i+len(want)]==want]
def local_seq(tid,sid,tokens,text,feature_ids=None):
    ts=copy.deepcopy(tokens)
    for i,t in enumerate(ts,1):
        t['source_output_position_one_based']=t['token_index'];t['token_index']=i
        t['assessment_role']='visible_reference_position';t['independent_recall_assessment']=False
        t['form_assessment_role']='visible_reference_position';t['sense_assessment_role']='visible_reference_position'
    return {'sequence_id':sid,'owner_id':tid,'kind':'visible_local_support','text':text,'tokens':ts,'required_feature_ids':feature_ids or [],'independent_recall_assessment':False}

for tid,seq in cook.items():
    t=bytask[tid];t['input_sequences']=[];t['input_sequence_ids']=[]
    ts=seq['tokens'];words=seq['text'].split();routes={i:[] for i in range(1,len(ts)+1)}
    itemcontrols=[r for r in hints['records'] if r['task_id']==tid]
    reqfeatures=set(featuremap.get(tid,[]))
    for r in itemcontrols:
        reqfeatures.update(r.get('required_feature_ids',[]))
        if r.get('input_sequence_id'):
            hs=copy.deepcopy(hintseq[r['input_sequence_id']]);t['input_sequences'].append(hs)
            for tok in ts:
                if any(tok.get('lemma_id')==h.get('lemma_id') and norm(tok['surface'])==norm(h['surface']) for h in hs['tokens']):routes[tok['token_index']].append(r['reference_id'])
    short='.'.join(str(int(x)) for x in tid.split('-')[-2:])
    t['local_support']=[]
    for f in inv['features']:
        if state(f)!='supplied' or short not in f.get('source_items',[]):continue
        phrase=f.get('support_span')
        if not phrase:continue
        spans=[]
        for part in phrase.split('; '):spans.extend(route_span(words,part))
        if not spans:
            issues.append({'kind':'supplied_frame_not_located','task_id':tid,'feature_id':f['feature_id'],'phrase':phrase});continue
        reqfeatures.add(f['feature_id'])
        for ni,positions in enumerate(spans,1):
            sid=tid+'-HELP-'+f['feature_id']+(('-'+str(ni)) if len(spans)>1 else '')
            chosen=[ts[i-1] for i in positions]
            sq=local_seq(tid,sid,chosen,' '.join(words[i-1] for i in positions),[f['feature_id']])
            t['input_sequences'].append(sq);supportseqs.append(sq)
            row={'support_id':sid,'feature_id':f['feature_id'],'output_token_positions_one_based':positions,'exact_help_text':sq['text'],
                'meaning_and_analysis':f.get('whole_frame_analysis',f.get('description')),'evidence_refs':f['evidence_refs'],'independent_recall_assessment':False,'visible_before_and_during_task':True}
            t['local_support'].append(row);supportrows.append(row)
            for i in positions:routes[i].append(sid)
    # Every deliberately supplied lexical element receives explicit word-level help,
    # even when the whole syntactic frame is already visible.
    for tok in ts:
        if not tok.get('form_id') or not tok.get('sense_id'):
            issues.append({'kind':'unbound_cook_token','task_id':tid,'position':tok['token_index'],'surface':tok['surface']});continue
        f=reg['form'].get(tok['form_id']);s=reg['sense'].get(tok['sense_id'])
        if not f or not s:
            issues.append({'kind':'missing_cook_record','task_id':tid,'token':tok});continue
        needed=state(f) not in ['previously_taught','new_production'] or state(s) not in ['previously_taught','new_production']
        if needed:
            sid=tid+'-LEXICAL-HELP-'+str(tok['token_index']).zfill(3)
            sq=local_seq(tid,sid,[tok],tok['surface'])
            t['input_sequences'].append(sq);supportseqs.append(sq);routes[tok['token_index']].append(sid)
            row={'support_id':sid,'output_token_positions_one_based':[tok['token_index']],'exact_help_text':tok['surface'],
                'form_id':tok['form_id'],'sense_id':tok['sense_id'],'meaning':s.get('contextual_gloss',s['gloss']),
                'analysis':tok.get('contextual_analysis',tok.get('analysis')),
                'scope':'Use this exact visible form and local meaning in this task. It is not an independent recall target or a grant of the remaining lexical system.',
                'evidence_refs':sorted(set(f.get('evidence_refs',[])+s.get('evidence_refs',[]))),
                'whole_frame_routes':[x for x in routes[tok['token_index']] if '-HELP-' in x],
                'independent_recall_assessment':False,'visible_before_and_during_task':True}
            t['local_support'].append(row);supportrows.append(row)
        tok['reference_route_ids']=routes[tok['token_index']]
        tok['assessment_role']='visible_reference_position' if tok['reference_route_ids'] else 'independent_production'
        tok['independent_recall_assessment']=not bool(tok['reference_route_ids'])
        tok['form_assessment_role']=tok['assessment_role']
        tok['sense_reference_route_ids']=sorted(set(tok['reference_route_ids']+[r['reference_id'] for r in itemcontrols if r.get('input_sequence_id') and any(h.get('lemma_id')==tok['lemma_id'] and h.get('sense_id')==tok['sense_id'] for h in hintseq[r['input_sequence_id']]['tokens'])]))
        tok['sense_assessment_role']='visible_reference_position' if tok['sense_reference_route_ids'] else 'independent_production'
        tok['form_status']=state(f);tok['sense_status']=state(s)
    seq['dependency_status']='closed' if all(x.get('form_id') and x.get('sense_id') for x in ts) else 'unresolved'
    pos=t['output_positions'][0];pos['output_id']=pos['output_position_id'];pos['kind']='translation';pos['output_sequence_id']=seq['sequence_id']
    for k in ['form','sense']:
        t['required_input_'+k+'_ids']=deps(t['input_sequences'],k);t['required_output_'+k+'_ids']=deps([seq],k)
        t['required_'+k+'_ids']=sorted(set(t['required_input_'+k+'_ids']+t['required_output_'+k+'_ids']))
        t['tested_'+k+'_ids']=sorted({x[k+'_id'] for x in ts if x.get(k+'_id') and x.get(k+'_assessment_role')=='independent_production'})
        t['supplied_'+k+'_ids']=sorted({x[k+'_id'] for x in ts if x.get(k+'_id') and x.get(k+'_assessment_role')=='visible_reference_position'}|set(t['required_input_'+k+'_ids']))
        for key in ['required_input_','required_output_','required_','tested_','supplied_']:pos[key+k+'_ids']=copy.deepcopy(t[key+k+'_ids'])
    t['required_feature_ids']=sorted(reqfeatures)
    t['supplied_feature_ids']=sorted(f for f in reqfeatures if state(reg['feature'].get(f,{}))=='supplied')
    t['tested_feature_ids']=sorted(f for f in reqfeatures if state(reg['feature'].get(f,{})) in ['previously_taught','new_production'])
    pos['required_feature_ids']=t['required_feature_ids'];pos['tested_feature_ids']=t['tested_feature_ids'];pos['supplied_feature_ids']=t['supplied_feature_ids']
    pos['reference_output_positions']=[x['token_index'] for x in ts if x.get('assessment_role')=='visible_reference_position']
    pos['reference_sense_output_positions']=[x['token_index'] for x in ts if x.get('sense_assessment_role')=='visible_reference_position']
    t['input_sequence_ids']=[s['sequence_id'] for s in t['input_sequences']]
    t['source_control_records']=itemcontrols
    t['source_instructions']=[copy.deepcopy(i) for i in sourceprompts['instructions'] if i['instruction_id'] in t.get('source_instruction_refs',[])]
    t['dependency_status']=seq['dependency_status'];t['dependency_closure_basis']='Exact ordered selected model identities, every original control, complete current teaching, and explicit visible support for every supplied form, sense and whole construction.'

reading=inv.get('readings',[None])[0]
for t in tasks:
    if t['task_id'].startswith('EX-'):continue
    if t.get('source_task_refs'):
        inherited=[bytask[tid] for tid in t['source_task_refs']]
        t['source_input_bindings']=[{'kind':'learner_previous_response_with_original_prompt_and_all_support','task_id':x['task_id'],'model_identity_ref':'author-only-cook-sequence-bindings.json#'+x['task_id'],'private_model_not_a_new_learner_input':True} for x in inherited]
        for k in ['form','sense','feature']:
            t['required_'+k+'_ids']=sorted(set(t.get('required_'+k+'_ids',[]))|{rid for x in inherited for rid in x['required_'+k+'_ids']})
            t['supplied_'+k+'_ids']=sorted(set(t.get('supplied_'+k+'_ids',[]))|{rid for x in inherited for rid in x['supplied_'+k+'_ids']})
            t['tested_'+k+'_ids']=[] if k!='feature' else [rid for rid in t['required_feature_ids'] if state(reg['feature'][rid]) in ['previously_taught','new_production','new_recognition']]
        t['required_feature_ids']=sorted(set(t['required_feature_ids'])|{'u18-literal-contextual-interpretation'})
        t['tested_feature_ids']=sorted(set(t['tested_feature_ids'])|{'u18-literal-contextual-interpretation'})
        for k in ['form','sense']:t['required_input_'+k+'_ids']=t['required_'+k+'_ids']
        t['mode']='supported_interpretation_analysis';t['dependency_status']='closed' if all(x['dependency_status']=='closed' for x in inherited) else 'unresolved'
    if t.get('source_span_id'):
        if reading is None:
            issues.append({'kind':'reading_join_missing','task_id':t['task_id']});continue
        t['source_input_bindings']=[{'source_span_id':reading['source_span_id'],'token_start_one_based':1,'token_end_one_based':226,'visible_in_assigned_reading':True,'local_help_ids':[s['support_id'] for s in reading['local_support']]}]
        for k in ['form','sense']:
            t['required_input_'+k+'_ids']=deps([reading],k);t['required_output_'+k+'_ids']=[];t['required_'+k+'_ids']=t['required_input_'+k+'_ids'];t['tested_'+k+'_ids']=[];t['supplied_'+k+'_ids']=t['required_'+k+'_ids']
        t['required_feature_ids']=reading['required_feature_ids'];t['supplied_feature_ids']=[fid for fid in t['required_feature_ids'] if state(reg['feature'][fid])=='supplied'];t['tested_feature_ids']=[fid for fid in t['required_feature_ids'] if state(reg['feature'][fid]) in ['previously_taught','new_production','new_recognition','prior_recognition']]
        t['mode']='supported_reading_analysis';t['dependency_status']=reading['dependency_status']
    for p in t['output_positions']:
        if p['response_language']=='English':
            for k in ['form','sense','feature']:
                p['required_'+k+'_ids']=copy.deepcopy(t['required_'+k+'_ids']);p['supplied_'+k+'_ids']=copy.deepcopy(t['supplied_'+k+'_ids']);p['tested_'+k+'_ids']=[] if k!='feature' else copy.deepcopy(t['tested_feature_ids'])
            p['analysis_basis']='Visible assigned input and/or the explicitly requested prior responses in this task; no supplied lexical recall is assessed.'

# A supplied feature used for an interpretation question stays supplied; the
# question tests applying the visible explanation, never memorizing its frame.
for t in tasks:
    for k in ['form','sense','feature']:
        for rid in t.get('required_'+k+'_ids',[]):
            if rid not in reg[k] or state(reg[k].get(rid,{}))=='unresolved':issues.append({'kind':'unresolved_required_identity','task_id':t['task_id'],'record_kind':k,'record_id':rid})
        for rid in t.get('tested_'+k+'_ids',[]):
            allowed=['previously_taught','new_production']+(['prior_recognition','new_recognition'] if 'analysis' in t['mode'] else [])
            if state(reg[k].get(rid,{})) not in allowed:issues.append({'kind':'untaught_tested','task_id':t['task_id'],'record_kind':k,'record_id':rid,'status':state(reg[k].get(rid,{}))})

# A complete private model contract exists for every requested answer, including
# source compositions. These are preparation records, never learner-facing labels.
modelpacket=read(O/'author-only-output-models.json')
modelrows={m['output_position_id']:m for m in modelpacket['models']}
for t in tasks:
    for p in t['output_positions']:
        oid=p['output_position_id']
        if t['task_id'] in cook:
            q=cook[t['task_id']]
            modelrows[oid]={'output_position_id':oid,'task_id':t['task_id'],'model':q['text'],'output_sequence_id':q['sequence_id'],'target':p['target'],'essential_meaning':p['essential_meaning'],'explanation':q.get('context_review'),'explanation_feature_ids':p['required_feature_ids'],'alternatives':p['alternatives_policy'],'error_diagnosis':p['error_diagnosis']}
        else:
            m=modelrows[oid];m.setdefault('explanation',m.get('model') if p['response_language']=='English' else p['target']);m['explanation_feature_ids']=p.get('required_feature_ids',[])
        p['author_only_model_ref']='curriculum/proposals/unit18/author-only-output-models.json#'+oid
        p['explanation_route_ids']=p.get('required_feature_ids',[])
modelpacket['models']=list(modelrows.values());modelpacket['status']='one private response model per requested output';save(O/'author-only-output-models.json',modelpacket)
save(O/'task-plan.json',{'schema_version':1,'chapter':'ch18','status':'ready_for_contract' if not issues else 'final_join_pending_validation','tasks':tasks,'counts':{'tasks':len(tasks),'requested_output_positions':sum(len(t['output_positions']) for t in tasks),'closed_tasks':sum(t['dependency_status']=='closed' for t in tasks)},'unresolved':issues})
cookpacket['status']='exact_selected_models_bound; private';cookpacket['unresolved']=[] if not issues else issues
save(O/'author-only-cook-sequence-bindings.json',cookpacket)
save(O/'source-support-routes.json',{'schema_version':1,'chapter':'ch18','status':'visible_support_routes','rows':supportrows,'sequences':supportseqs,'counts':{'support_rows':len(supportrows),'support_sequences':len(supportseqs)}})
print(json.dumps({'tasks':len(tasks),'closed':sum(t['dependency_status']=='closed' for t in tasks),'issues':len(issues),'support_sequences':len(supportseqs)},indent=2))
print(json.dumps(issues,ensure_ascii=False,indent=2)[:7000])
