"""One-use, evidence-backed repair of four supplied constructions after blind review."""
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def union(*values):
    return list(dict.fromkeys(x for value in values for x in value))
def surface(word):
    return word.strip('.,:;!?“”‘’"()').casefold()

spec = read('chapters/ch17/support-amendment-spec.json')
assert spec['evidence_status'] == 'primary_images_verified_by_independent_reviewers'
assert len(spec['constructions']) == 4
assert sha('chapters/ch17/independent-solutions.md') == '32d031c180ea67429cf2772ffc1e009596f82eb8c1851c8c8a93375d88985a36'
c = read('chapters/ch17/coverage.json')
assert not any(a['amendment_id']=='U17-A02' for a in c['amendments'])
assert not c.get('textual_review')
history = {'chapter_id':'ch17','amendment_id':'U17-A02',
           'contract_sha256_before':sha('chapters/ch17/coverage.json'),
           'blind_solutions_checkpoint':'ed28a8e',
           'original_tasks':{},'original_teaching_records':{},'changes':[]}
tasks = {t['task_id']:t for t in c['assigned_items']}
teach = {t['teaching_id']:t for t in c['teaching_records']}
models = {s['owner_id']:s for s in read('curriculum/proposals/unit17/author-only-cook-sequence-bindings.json')['sequences']}
for eid, evidence in spec.get('additional_evidence_catalog', {}).items():
    assert eid not in c['evidence_catalog'] or c['evidence_catalog'][eid]==evidence
    c['evidence_catalog'][eid]=evidence

for item in spec['constructions']:
    fid, teaching_id = item['feature_id'], item['teaching_id']
    assert fid not in {r['feature_id'] for r in c['grammar_inventory']}
    assert item['evidence_refs'] and all(e in c['evidence_catalog'] for e in item['evidence_refs'])
    short_ids = [f"{tasks[t]['original_exercise']}.{tasks[t]['original_item']}" for t in item['task_ids']]
    feature = {'feature_id':fid,'label':item['label'],'description':item['analysis'],
               'scope_note':'Use only this visibly supplied expression in the named tasks; no independent recall or general constructional production is assigned.',
               'knowledge_status':'supplied','teaching_ids':[teaching_id],
               'evidence_refs':item['evidence_refs'],'source_items':short_ids,
               'used_in_tasks':item['task_ids'],'assessed_in':[],
               'exact_span':item['text'],'amendment_id':'U17-A02',
               'origin_category':'new teaching material',
               'evidence_application':item['evidence_application']}
    c['grammar_inventory'].append(feature)
    if teaching_id in teach:
        teaching=teach[teaching_id]
        history['original_teaching_records'][teaching_id]=copy.deepcopy(teaching)
    else:
        teaching={'teaching_id':teaching_id,'kind':'supplied_whole_frame',
                  'form_ids':[],'sense_ids':[],'feature_ids':[],
                  'knowledge_status':'supplied','source_items':short_ids,
                  'lesson_placement':'Beside each named Cook item, before its requested response; help stays visible.'}
        c['teaching_records'].append(teaching)
        teach[teaching_id]=teaching
    teaching.update(description=item['analysis'],support_span=item['text'],
                    scope_note=feature['scope_note'],amendment_id='U17-A02')
    teaching['feature_ids']=union(teaching.get('feature_ids',[]),[fid])
    teaching['evidence_refs']=union(teaching.get('evidence_refs',[]),item['evidence_refs'])

    for tid in item['task_ids']:
        task=tasks[tid]
        history['original_tasks'][tid]=copy.deepcopy(task)
        original_tokens=models[tid]['tokens']
        words=item['text'].split()
        starts=[i for i in range(len(original_tokens)-len(words)+1)
                if [surface(t['literal']) for t in original_tokens[i:i+len(words)]]==[surface(w) for w in words]]
        assert len(starts)==1,(tid,item['text'],starts)
        start=starts[0]
        positions=list(range(start+1,start+len(words)+1))
        selected=copy.deepcopy(original_tokens[start:start+len(words)])
        support_id=item.get('replace_support_ids',{}).get(tid,tid+'-HELP-'+fid.upper())
        existing=[s for s in task['local_support'] if s['support_id']==support_id]
        assert len(existing)==(1 if tid in item.get('replace_support_ids',{}) else 0)
        support=existing[0] if existing else {'support_id':support_id}
        support.update(feature_id=fid,feature_ids=[fid],exact_help_text=item['text'],
                       meaning_and_analysis=item['analysis'],
                       output_token_positions_one_based=positions,
                       form_ids=sorted({t['form_id'] for t in selected}),
                       sense_ids=sorted({t['sense_id'] for t in selected}),
                       evidence_refs=union(support.get('evidence_refs',[]),item['evidence_refs']),
                       independent_recall_assessment=False,visible_before_and_during_task=True,
                       amendment_id='U17-A02',origin_category='new teaching material',
                       evidence_application=item['evidence_application'])
        support['whole_frame_routes']=union(support.get('whole_frame_routes',[]),[support_id])
        if not existing:
            task['local_support'].append(support)
        sequences=[s for s in task['input_sequences'] if s['sequence_id']==support_id]
        assert len(sequences)==len(existing)
        seq=sequences[0] if sequences else {'sequence_id':support_id,'owner_id':tid,'kind':'visible_local_support'}
        for i,(word,tok,pos) in enumerate(zip(words,selected,positions),1):
            tok.update(token_index=i,literal=word,source_output_position_one_based=pos,
                       assessment_role='visible_reference_position',form_assessment_role='visible_reference_position',
                       sense_assessment_role='visible_reference_position',independent_recall_assessment=False,
                       local_support_id=support_id,amendment_id='U17-A02')
        seq.update(text=item['text'],tokens=selected,required_feature_ids=[fid],
                   independent_recall_assessment=False,amendment_id='U17-A02')
        if not sequences:
            task['input_sequences'].append(seq)
        task['input_sequence_ids']=[s['sequence_id'] for s in task['input_sequences']]
        output=task['output_positions'][0]
        assert len(task['output_positions'])==1
        output['reference_output_positions']=sorted(set(output['reference_output_positions'])|set(positions))
        output['reference_sense_output_positions']=sorted(set(output['reference_sense_output_positions'])|set(positions))
        for row in [task,output]:
            row['required_feature_ids']=union(row['required_feature_ids'],[fid])
            row['supplied_feature_ids']=union(row['supplied_feature_ids'],[fid])
        # Canonical task-level tokens supersede only the archived proposal's
        # assessment annotations. Text, spelling, morphology and sense identity stay exact.
        assessed=copy.deepcopy(original_tokens)
        for tok in assessed:
            pos=tok['token_index']
            for kind,field in [('form','reference_output_positions'),('sense','reference_sense_output_positions')]:
                tok[kind+'_assessment_role']='visible_reference_position' if pos in output[field] else tok[kind+'_assessment_role']
            if pos in positions:
                tok.update(assessment_role='visible_reference_position',independent_recall_assessment=False,
                           local_support_id=support_id,amendment_id='U17-A02')
        task['assessed_output_tokens']=assessed
        task['assessment_precedence']='U17-A02 canonical task tokens and output reference positions supersede original proposal assessment roles only; the archived model text and lexical identities are unchanged.'
        for kind in ['form','sense']:
            supplied_positions=set(output['reference_output_positions' if kind=='form' else 'reference_sense_output_positions'])
            supplied={t[kind+'_id'] for t in assessed if t['token_index'] in supplied_positions}
            tested={t[kind+'_id'] for t in assessed if t['token_index'] not in supplied_positions}
            input_ids={t[kind+'_id'] for s in task['input_sequences'] for t in s['tokens']}
            for row in [task,output]:
                row['required_input_'+kind+'_ids']=sorted(input_ids)
                row['required_'+kind+'_ids']=sorted(set(row['required_output_'+kind+'_ids'])|input_ids)
                row['supplied_'+kind+'_ids']=sorted(supplied|input_ids)
                row['tested_'+kind+'_ids']=sorted(tested)
            teaching[kind+'_ids']=union(teaching.get(kind+'_ids',[]),support[kind+'_ids'])
        task['dependency_closure_basis']+=' U17-A02 supplies the complete evidenced local construction and binds every copied position explicitly; existing productive component milestones are unchanged.'
        history['changes'].append({'task_id':tid,'feature_id':fid,'support_id':support_id,
                                   'exact_help_text':item['text'],'reference_positions':positions,
                                   'meaning_and_analysis':item['analysis']})

for kind,rows in [('form',[r for l in c['lexical_inventory'] for r in l['forms']]),
                  ('sense',[r for l in c['lexical_inventory'] for r in l['senses']]),
                  ('feature',c['grammar_inventory'])]:
    c['record_counts_by_scope'][kind]=dict(Counter(r['knowledge_status'] for r in rows))
c['record_identity_counts']['feature']['new_IDs']+=4
c['explicit_scope_metrics'].update(features=len(c['grammar_inventory']),teaching_records=len(c['teaching_records']))
assert len(c['grammar_inventory'])==64 and len(c['teaching_records'])==420
amendment={'amendment_id':'U17-A02','date':'2026-10-28','stage':'independent_review',
           'original_contract_checkpoint':'6fc6fc1','complete_drafts_checkpoint':'259b14f',
           'independent_solutions_checkpoint':'ed28a8e','coordinator':'root',
           'reported_by':'unit17_blind','findings':['B17-01','B17-02','B17-03','B17-04'],
           'reason':'Four unfamiliar constructions were not fully supplied in learner help and task bindings. Supply complete phrases with their case/role, retaining all source prompts and model text.',
           'specification':'chapters/ch17/support-amendment-spec.json',
           'history':'chapters/ch17/support-amendment-history.json',
           'changes':history['changes'],'contract_raw_sha256_before':history['contract_sha256_before'],
           'unchanged':['All source prompts and models','All 110 systems / 1234 cells','Reading and original notes',
                        'Frozen blind witness','Sealed source/proposal packets','Earlier chapters and all prior register milestones'],
           'review_status':'requires_independent_verification'}
c['amendments'].append(amendment)
write('chapters/ch17/support-amendment-history.json',history)
write('chapters/ch17/coverage.json',c)
a=read('chapters/ch17/authoring-amendments.json')
a['amendments'].append(amendment)
write('chapters/ch17/authoring-amendments.json',a)
print('U17-A02 contract saved before learner help: four supplied constructions, five task routes, 64 features, 420 teaching records. Masters unchanged; independent verification required.')
