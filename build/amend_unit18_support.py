"""Integrate a reviewed, bounded support specification without rewriting its witnesses."""
import copy,hashlib,json,re
from collections import Counter
from pathlib import Path
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ident(p):
    b=Path(p).read_bytes();return {'path':p,'sha256':hashlib.sha256(b).hexdigest(),'sha256_normalized_lf':hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest()}
def union(*v):return list(dict.fromkeys(x for a in v for x in a))
def surf(s):return s.strip('.,:;!?“”‘’"()').casefold()
spec=read('chapters/ch18/support-amendment-spec.json')
assert spec['status']=='primary_evidence_reconciled'
freeze=read('chapters/ch18/blind-freeze.json');witness=sha('chapters/ch18/independent-solutions.md')
assert witness==freeze['identity']['raw_sha256']
c=read('chapters/ch18/coverage.json');assert not c.get('textual_review')
assert [a['amendment_id'] for a in c['amendments']]==['U18-A01','U18-A02','U18-A03','U18-A04']
history={'amendment_id':'U18-A05','contract_raw_sha256_before':sha('chapters/ch18/coverage.json'),'original_tasks':{},'model_changes':[],'support_changes':[],'master_changes':[]}
tasks={t['task_id']:t for t in c['assigned_items']}
source='curriculum/proposals/unit18/author-only-cook-sequence-bindings.json'
original_models={s['owner_id']:s for s in read(source)['sequences']}
models=copy.deepcopy(original_models)
for eid,e in spec['additional_evidence_catalog'].items():
    assert eid not in c['evidence_catalog'] or c['evidence_catalog'][eid]==e
    c['evidence_catalog'][eid]=e
for lemma in spec['new_lexical_records']:
    assert lemma['lemma_id'] not in {l['lemma_id'] for l in c['lexical_inventory']}
    c['lexical_inventory'].append(lemma)
for change in spec['model_changes']:
    tid=change['task_id'];s=models[tid]
    for patch in change['token_changes']:
        token=s['tokens'][patch['position']-1]
        for k,v in patch['expected'].items():assert token[k]==v,(tid,k,token[k],v)
        token.update(copy.deepcopy(patch['values']))
    s['text']=' '.join(t['literal'] for t in s['tokens'])
    s['amendment_id']='U18-A05';s['correction_basis']=change['reason']
    history['model_changes'].append({'task_id':tid,'original_text':original_models[tid]['text'],'corrected_text':s['text'],'reason':change['reason'],'original_sequence':original_models[tid]})
correction={'chapter_id':'ch18','amendment_id':'U18-A05','source':source,'source_sha256':ident(source)['sha256'],'source_sha256_normalized_lf':ident(source)['sha256_normalized_lf'],'corrections':history['model_changes'],'corrected_sequences':[models[x['task_id']] for x in spec['model_changes']],'scope':'One case correction and explicit contextual lexical routes. Original models, analyses and blind attempts are preserved.'}
write('chapters/ch18/selected-model-corrections.json',correction)
c['selected_model_corrections']=ident('chapters/ch18/selected-model-corrections.json')
student=Path('chapters/ch18/student.md').read_text(encoding='utf-8')
key=Path('chapters/ch18/answer-key.md').read_text(encoding='utf-8')
original_masters={'student.md':student,'answer-key.md':key}
new_help_by_task={}
for item in spec['constructions']:
    fid=item['feature_id'];teaching_id=item['teaching_id']
    assert fid not in {f['feature_id'] for f in c['grammar_inventory']}
    assert teaching_id not in {t['teaching_id'] for t in c['teaching_records']}
    assert all(e in c['evidence_catalog'] for e in item['evidence_refs'])
    tids=union([h['task_id'] for h in item['helps']])
    scope='Use the complete visible expression in these tasks; no independent recall or general production of this construction is assigned.'
    feature={'feature_id':fid,'label':item['label'],'description':item['analysis'],'knowledge_status':'supplied','teaching_ids':[teaching_id],'evidence_refs':item['evidence_refs'],'scope_note':scope,'used_in_tasks':tids,'assessed_in':[],'origin_category':'new teaching material','amendment_id':'U18-A05','evidence_application':item['evidence_application']}
    c['grammar_inventory'].append(feature)
    teaching={'teaching_id':teaching_id,'kind':'supplied_whole_frame','description':item['analysis'],'form_ids':[],'sense_ids':[],'feature_ids':[fid],'knowledge_status':'supplied','evidence_refs':item['evidence_refs'],'lesson_placement':'Beside each named Cook item, before its requested response; help stays visible.','scope_note':scope,'amendment_id':'U18-A05'}
    c['teaching_records'].append(teaching)
    c['lexical_frames'].append({'feature_id':fid,'label':item['label'],'knowledge_status':'supplied','description':item['analysis'],'evidence_refs':item['evidence_refs'],'source_items':tids,'teaching_id':teaching_id,'scope_limitation':scope})
    for hindex,help in enumerate(item['helps'],1):
        tid=help['task_id'];task=tasks[tid]
        history['original_tasks'].setdefault(tid,copy.deepcopy(task))
        words=help['text'].split();tokens=models[tid]['tokens']
        starts=[i for i in range(len(tokens)-len(words)+1) if [surf(t['literal']) for t in tokens[i:i+len(words)]]==[surf(w) for w in words]]
        assert len(starts)==1,(tid,help['text'],starts)
        start=starts[0];positions=list(range(start+1,start+len(words)+1))
        sid=tid+'-HELP-'+fid.upper()+'-'+str(hindex)
        selected=copy.deepcopy(tokens[start:start+len(words)])
        support={'support_id':sid,'feature_id':fid,'feature_ids':[fid],'exact_help_text':help['text'],'meaning_and_analysis':help.get('analysis',item['analysis']),'output_token_positions_one_based':positions,'form_ids':sorted({t['form_id'] for t in selected}),'sense_ids':sorted({t['sense_id'] for t in selected}),'evidence_refs':item['evidence_refs'],'whole_frame_routes':[sid],'independent_recall_assessment':False,'visible_before_and_during_task':True,'amendment_id':'U18-A05','origin_category':'new teaching material','evidence_application':item['evidence_application']}
        task['local_support'].append(support)
        for i,(word,tok,pos) in enumerate(zip(words,selected,positions),1):
            tok.update(token_index=i,literal=word,source_output_position_one_based=pos,assessment_role='visible_reference_position',form_assessment_role='visible_reference_position',sense_assessment_role='visible_reference_position',independent_recall_assessment=False,local_support_id=sid,amendment_id='U18-A05')
        task['input_sequences'].append({'sequence_id':sid,'owner_id':tid,'kind':'visible_local_support','text':help['text'],'tokens':selected,'required_feature_ids':[fid],'independent_recall_assessment':False,'amendment_id':'U18-A05'})
        output=task['output_positions'][0];assert len(task['output_positions'])==1
        for field in ['reference_output_positions','reference_sense_output_positions']:
            output[field]=sorted(set(output[field])|set(positions))
        for row in [task,output]:
            row['required_feature_ids']=union(row['required_feature_ids'],[fid])
            row['supplied_feature_ids']=union(row['supplied_feature_ids'],[fid])
        output['explanation_route_ids']=union(output.get('explanation_route_ids',[]),[fid])
        for kind in ['form','sense']:teaching[kind+'_ids']=union(teaching[kind+'_ids'],support[kind+'_ids'])
        new_help_by_task.setdefault(tid,[]).append((teaching_id if hindex==1 else None,support))
        history['support_changes'].append({'task_id':tid,'feature_id':fid,'support_id':sid,'positions':positions,'text':help['text'],'analysis':support['meaning_and_analysis']})
for tid in new_help_by_task:
    task=tasks[tid];output=task['output_positions'][0]
    task['input_sequence_ids']=[s['sequence_id'] for s in task['input_sequences']]
    assessed=copy.deepcopy(models[tid]['tokens'])
    for tok in assessed:
        pos=tok['token_index']
        for kind,field in [('form','reference_output_positions'),('sense','reference_sense_output_positions')]:
            tok[kind+'_assessment_role']='visible_reference_position' if pos in output[field] else 'independent_production'
        matching=[h for _,h in new_help_by_task[tid] if pos in h['output_token_positions_one_based']]
        if matching:
            tok.update(assessment_role='visible_reference_position',independent_recall_assessment=False,local_support_id=matching[0]['support_id'],amendment_id='U18-A05')
    task['assessed_output_tokens']=assessed
    task['assessment_precedence']='U18-A05 corrected sequence identity and canonical task tokens supersede the original proposal only as explicitly recorded in selected-model-corrections.json and support-amendment-history.json.'
    for kind in ['form','sense']:
        output_ids={t[kind+'_id'] for t in assessed}
        input_ids={t[kind+'_id'] for s in task['input_sequences'] for t in s['tokens']}
        field='reference_output_positions' if kind=='form' else 'reference_sense_output_positions'
        supplied={t[kind+'_id'] for t in assessed if t['token_index'] in output[field]}
        tested={t[kind+'_id'] for t in assessed if t['token_index'] not in output[field]}
        for row in [task,output]:
            row['required_input_'+kind+'_ids']=sorted(input_ids)
            row['required_output_'+kind+'_ids']=sorted(output_ids)
            row['required_'+kind+'_ids']=sorted(output_ids|input_ids)
            row['supplied_'+kind+'_ids']=sorted(supplied|input_ids)
            row['tested_'+kind+'_ids']=sorted(tested)
    task['dependency_closure_basis']+=' U18-A05 supplies the evidenced whole expressions and explicitly binds their reference positions; earlier component teaching remains unchanged.'
    marker='<!-- output: '+output['output_position_id']+' -->'
    assert student.count(marker)==1
    helps=[]
    for teaching_id,h in new_help_by_task[tid]:
        if teaching_id:helps.append('<!-- teaching: '+teaching_id+' -->')
        helps.append('**Supplied construction:** **'+h['exact_help_text']+'** — '+h['meaning_and_analysis'])
    student=student.replace(marker,'\n\n'.join(helps)+'\n\n'+marker)
for change in history['model_changes']:
    if change['original_text']!=change['corrected_text']:
        assert key.count(change['original_text'])==1
        key=key.replace(change['original_text'],change['corrected_text'])
for item in spec.get('key_replacements',[]):
    assert key.count(item['before'])==1,item['before']
    key=key.replace(item['before'],item['after'])
for tid,note in spec['key_support_notes'].items():
    task=tasks[tid];marker='<!-- key: '+task['key_id']+' -->'
    at=key.index(marker);start=key.index('**Target and explanation:**',at)
    end=key.index('\n\n',start)
    key=key[:end]+'\n\n**Supplied construction:** '+note+key[end:]
for change in spec.get('task_explanation_replacements',[]):
    task=tasks[change['task_id']]
    for obj,field in [(task,'semantic_and_construction_demands'),(task['output_positions'][0],'target')]:
        if change['before'] in obj[field]:obj[field]=obj[field].replace(change['before'],change['after'])
for kind,rows in [('form',[r for l in c['lexical_inventory'] for r in l['forms']]),('sense',[r for l in c['lexical_inventory'] for r in l['senses']]),('feature',c['grammar_inventory'])]:
    c['record_counts_by_scope'][kind]=dict(Counter(r['knowledge_status'] for r in rows))
    baseline=read('build/unit18-prior-baseline.json')
    old={r[kind+'_id'] for l in baseline['lexicon']['lemmas'] for r in l['forms' if kind=='form' else 'senses']} if kind!='feature' else {r['feature_id'] for r in baseline['grammar']['features']}
    c['record_identity_counts'][kind]={'reused_prior_IDs':sum(r[kind+'_id'] in old for r in rows),'new_IDs':sum(r[kind+'_id'] not in old for r in rows)}
c['explicit_scope_metrics'].update(lemmas=len(c['lexical_inventory']),forms=sum(len(l['forms']) for l in c['lexical_inventory']),senses=sum(len(l['senses']) for l in c['lexical_inventory']),features=len(c['grammar_inventory']),teaching_records=len(c['teaching_records']))
c.setdefault('contextual_identity_amendments',[]).extend(spec.get('contextual_identity_notes',[]))
for name,text in [('student.md',student),('answer-key.md',key)]:
    path='chapters/ch18/'+name
    history['master_changes'].append({'path':path,'sha256_before':sha(path),'sha256_after':hashlib.sha256(text.encode('utf-8')).hexdigest()})
# Contract is saved before the corresponding visible help is installed.
a={'amendment_id':'U18-A05','date':'2026-10-28','stage':'independent_review','original_contract_checkpoint':'6874c20e7127fa33c41406d1aa6c0b087e59c824','complete_drafts_checkpoint':'970fcc1f431f6ce2ccdd1f1c85b2b5e63ae0c16a','independent_solutions_checkpoint':'7846befc2c484e8d3e4ff43346da12bf275f5b08','coordinator':'root','reported_by':['unit18_blind','unit18_paradigms'],'findings':['U18-BLIND-02','U18-BLIND-03','U18-BLIND-04','U18-BLIND-06','U18-BLIND-09','U18-PAR-F03'],'reason':spec['decision'],'specification':'chapters/ch18/support-amendment-spec.json','history':'chapters/ch18/support-amendment-history.json','contract_raw_sha256_before':history['contract_raw_sha256_before'],'unchanged':['All Cook original prompts and controls','All55 paradigms/652cells','Reading and original notes','Frozen blind solutions and access history','Sealed source/proposal packets','Earlier contracts, exports and register milestones'],'review_status':'requires_independent_verification'}
c['amendments'].append(a);write('chapters/ch18/support-amendment-history.json',history);write('chapters/ch18/coverage.json',c)
for name,text in [('student.md',student),('answer-key.md',key)]:Path('chapters/ch18/'+name).write_text(text,encoding='utf-8',newline='\n')
am=read('chapters/ch18/authoring-amendments.json');am['amendments'].append(a);write('chapters/ch18/authoring-amendments.json',am)
assert sha('chapters/ch18/independent-solutions.md')==witness
print('U18-A05 applied; actual independent verification remains required.')
print(json.dumps(c['explicit_scope_metrics'],ensure_ascii=False))
