from pathlib import Path
import copy
import json

O=Path('curriculum/proposals/unit18')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
inv=read(O/'inventory.json');lex=read('lexicon/entries.json');g=read('curriculum/grammar.json')
src=copy.deepcopy(read('sources/audits/unit18-source/reading-source.json')['source_spans'][0])
ledger=read('sources/audits/unit18-source/reading-token-audit.json');local=read('sources/audits/unit18-source/local-support.json')
verbs=read('sources/audits/unit18-grammar/reading-verbal-bindings.json');vmap={r.get('token_position_one_based',r.get('position')):r for r in verbs['verbal_occurrences']}
aliases={a['source_proposal']['form_id']:a['canonical_binding'] for a in inv.get('source_proposal_identity_reconciliation',[])}
forms={f['form_id']:(l['lemma_id'],f) for l in lex['lemmas']+inv['lemmas'] for f in l['forms']}
senses={s['sense_id']:(l['lemma_id'],s) for l in lex['lemmas']+inv['lemmas'] for s in l['senses']}
features={f['feature_id']:f for f in g['features']+inv['features']}
def state(r):
    return 'previously_taught' if r.get('production_taught_in') else 'prior_recognition' if r.get('recognition_taught_in') else r.get('knowledge_status','supplied' if r.get('supplied_in') else 'unresolved')
issues=[];support=[]
for r in local.get('reading_phrase_support',[]):
    positions=r.get('reading_token_positions_one_based',[])
    if not positions:continue
    fid=r['support_id'];tid='NEW-U18-GRAM-'+fid.upper()
    f={'feature_id':fid,'label':r['help_text'],'description':r['help_text'],'whole_frame_analysis':r['help_text'],'knowledge_status':'supplied','teaching_ids':[tid],'evidence_refs':r['evidence_refs'],
        'token_positions_one_based':positions,'exact_span':r['phrase'],'scope_note':'This complete visible reading expression only; no independent recall.'}
    inv['features'].append(f);features[fid]=f
    inv['teaching_records'].append({'teaching_id':tid,'kind':'visible_reading_phrase','feature_ids':[fid],'description':r['help_text'],'exact_span':r['phrase'],'evidence_refs':r['evidence_refs'],'knowledge_status':'supplied','lesson_placement':'Beside the exact source passage, before all reading tasks.'})
    support.append({'support_id':fid,'feature_id':fid,**copy.deepcopy(r),'token_positions_one_based':positions,'visible_before_and_during_task':True})
for raw in local.get('forms',[]):
    positions=raw.get('reading_token_positions_one_based',[])
    if not positions:continue
    fid=inv.get('form_id_aliases',{}).get(raw['form_id'],raw['form_id'])
    support.append({'support_id':raw['support_id'],'token_positions_one_based':positions,'exact_help_text':raw['form'],
        'form_id':fid,'sense_id':raw['sense_id'],'meaning':raw['gloss'],'analysis':raw['analysis'],
        'editorial_support_explanation':raw['help_text'],'source_support_record':'sources/audits/unit18-source/local-support.json#'+raw['support_id'],
        'evidence_refs':raw['evidence_refs'],'independent_recall_assessment':False,'visible_before_and_during_task':True})
for r in verbs['whole_frame_support']:
    support.append({'support_id':r['feature_id'],'feature_id':r['feature_id'],**copy.deepcopy(r),'meaning_and_analysis':r['whole_frame_analysis'],'visible_before_and_during_task':True})
for r in ledger.get('local_help_spans',[]):
    # The source ledger repeats its separate phrase packet, which also carries
    # Cook-only spans. Keep one route per actual reading support identity.
    if any(x['support_id']==r['support_id'] for x in support):continue
    positions=r.get('token_positions_one_based',r.get('reading_token_positions_one_based',[]))
    if not positions and not (r.get('token_start_one_based') and r.get('token_end_one_based')):continue
    support.append(copy.deepcopy(r)|{'token_positions_one_based':positions,'visible_before_and_during_task':True})

tokens=[]
for i,(word,original) in enumerate(zip(src['learner_text'].split(),ledger['tokens']),1):
    r=copy.deepcopy(original)
    if i in vmap:
        v=vmap[i]
        for field in ['lemma_id','form_id','sense_id','current_context_analysis','contextual_role_and_meaning','form_knowledge_status','sense_knowledge_status']:
            if field in v:r[field]=copy.deepcopy(v[field])
        r['whole_frame_support_ids']=v.get('whole_frame_support_ids',r.get('whole_frame_support_ids',[]))
    if r['form_id'] in aliases:r.update(aliases[r['form_id']])
    r['form_id']=inv.get('form_id_aliases',{}).get(r.get('form_id'),r.get('form_id'))
    fid=r.get('form_id');sid=r.get('sense_id');f=forms.get(fid);s=senses.get(sid)
    if not f or not s:
        issues.append({'position':i,'surface':word,'missing_form_id':fid if not f else None,'missing_sense_id':sid if not s else None})
    tok={'token_index':i,'reading_token_id':r['reading_token_id'],'literal':word,'surface':word.strip('.,;:!?“”‘’\"()'),'lemma_id':r['lemma_id'],'form_id':fid,'sense_id':sid,
        'analysis':copy.deepcopy(f[1]['analysis']) if f else None,'contextual_analysis':r['current_context_analysis'],'contextual_role_and_meaning':r['contextual_role_and_meaning'],
        'form_status':state(f[1]) if f else 'unresolved','sense_status':state(s[1]) if s else 'unresolved','assessment_role':'visible_source_reading_position','independent_recall_assessment':False,
        'support_route_ids':sorted(set(r.get('local_help_ids',[])+r.get('whole_frame_support_ids',[]))),
        'source_analysis_record':'sources/audits/unit18-source/reading-token-audit.json#'+r['reading_token_id'],
        'verbal_analysis_record':'sources/audits/unit18-grammar/reading-verbal-bindings.json#'+r['reading_token_id'] if i in vmap else None}
    for frame in support:
        if (i in frame.get('token_positions_one_based',[]) or frame.get('token_start_one_based',999)<=i<=frame.get('token_end_one_based',0)) and frame['support_id'] not in tok['support_route_ids']:tok['support_route_ids'].append(frame['support_id'])
    if f and s and (state(f[1]) not in ['previously_taught','new_production','new_recognition','prior_recognition'] or state(s[1]) not in ['previously_taught','new_production','new_recognition','prior_recognition']) and not any(i in z.get('token_positions_one_based',[]) and z.get('form_id')==fid and z.get('sense_id')==sid for z in support):
        hid='U18-READ-LEXICAL-'+str(i).zfill(3)
        support.append({'support_id':hid,'token_positions_one_based':[i],'exact_help_text':tok['surface'],'form_id':fid,'sense_id':sid,'meaning':s[1].get('contextual_gloss',s[1]['gloss']),
            'analysis':tok['contextual_analysis'],'contextual_explanation':tok['contextual_role_and_meaning'],'evidence_refs':sorted(set(f[1].get('evidence_refs',[])+s[1].get('evidence_refs',[]))),
            'independent_recall_assessment':False,'visible_before_and_during_task':True})
        tok['support_route_ids'].append(hid)
    tokens.append(tok)
src['tokens']=tokens;src['sequence_id']=src['source_span_id'];src['kind']='exact_source_reading';src['local_support']=support
apparatus=read('sources/audits/unit18-source/reading-apparatus.json')['notes']
src['original_notes']=copy.deepcopy(apparatus)
src['original_note_anchors']=[{'apparatus_id':n['apparatus_id'],'original_note_number':n['original_note_number'],'printed_page':n['printed_page'],**copy.deepcopy(a)} for n in apparatus for a in n['anchors']]
src['context']=read('sources/audits/unit18-source/reading-context.json')
src['required_feature_ids']=sorted({f['feature_id'] for f in verbs['whole_frame_support']}|{f['support_id'] for f in local.get('reading_phrase_support',[]) if f.get('reading_token_positions_one_based')}|{'u02-pronoun-reference','u02-third-person-possessors','u09-content-that','u12-reported-sequence','u08-relative-the','u08-relative-internal-case','u11-mid-thy-temporal','u11-purpose','u15-free-choice','u12-habban-perfect','u17-literal-contextual-interpretation'})
src['dependency_status']='closed' if not issues else 'unresolved'
src['assessment_scope']='Supported reading and interpretation with the exact passage, all original notes and complete local help visible; no source-only independent recall.'
inv['readings']=[src];inv['unresolved_integration']+=issues
save(O/'inventory.json',inv);save(O/'reading-bindings.json',{'schema_version':1,'chapter':'ch18','status':src['dependency_status'],'source_span':src,'counts':{'tokens':len(tokens),'original_notes':len(apparatus),'original_note_anchors':len(src['original_note_anchors']),'local_support':len(support)},'unresolved':issues})
print(json.dumps({'tokens':len(tokens),'support_rows':len(support),'issues':issues},ensure_ascii=False,indent=2))
