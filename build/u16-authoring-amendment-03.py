"""Record Cook number/context repairs and visible-reference assessment roles."""
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path

def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def write(path, data): Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
def identity(path):
    raw=Path(path).read_bytes()
    return {'path':path,'sha256':hashlib.sha256(raw).hexdigest(),
            'sha256_normalized_lf':hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest()}

cp='chapters/ch16/coverage.json'
c=read(cp)
assert not c.get('selected_model_corrections')
assert not any(a['amendment_id']=='U16-A03' for a in c['amendments'])
source='curriculum/proposals/unit16/author-only-cook-sequence-bindings.json'
originals={s['owner_id']:s for s in read(source)['sequences']}
models=copy.deepcopy(originals)
audit_path='build/u16-learner-hint-reference-audit.json'
audit=read(audit_path)
tasks={t['task_id']:t for t in c['assigned_items']}
forms={f['form_id']:f for l in c['lexical_inventory'] for f in l['forms']}
senses={s['sense_id']:s for l in c['lexical_inventory'] for s in l['senses']}
role='given_dictionary_form_position_identification_not_unaided_recall'
changes=[]
for proposed in audit['proposed_role_changes']:
    tid=proposed['task_id']; seq=models[tid]
    token=seq['tokens'][proposed['token_index_one_based']-1]
    assert token['token_index']==proposed['token_index_one_based']
    assert token['surface'].casefold()==proposed['hint_text'].casefold()
    assert proposed['exact_parenthesis'] in tasks[tid]['prompt']
    assert token['assessment_role']=='independent_production'
    before=copy.deepcopy(token)
    token['assessment_role']=role
    token['given_reference']={
        'source':'unchanged original English prompt',
        'exact_parenthesis':proposed['exact_parenthesis'],
        'hint_text':proposed['hint_text'],
        'boundary':'The spelling is visible. Case, number, construction and contextual sense still require application; this is not evidence of unaided lexical or spelling recall.'}
    if tid=='EX-XII-XIII-32-06' and token['token_index']==6:
        assert token['form_id']=='nett-acc-pl'
        token['form_id']='nett-acc-sg'
        token['analysis']['number']='sg'
        token['contextual_analysis']['number']='sg'
    if tid=='EX-XII-XIII-35-09' and token['token_index']==3:
        token['contextual_analysis']['function']='preposition introducing the destination of coming; governs dative'
    if tid=='EX-XII-XIII-36-02' and token['token_index']==5:
        token['contextual_analysis']['function']='preposition introducing the goal of turning; governs dative'
    changes.append({'task_id':tid,'token_index':token['token_index'],'before':before,'after':copy.deepcopy(token)})

affected=sorted({r['task_id'] for r in changes})
assert len(changes)==38 and len(affected)==21
task_changes=[]
for tid in affected:
    seq=models[tid]; task=tasks[tid]; before=copy.deepcopy(task)
    seq['required_form_ids']=sorted({t['form_id'] for t in seq['tokens']})
    seq['required_sense_ids']=sorted({t['sense_id'] for t in seq['tokens']})
    assert len(task['output_positions'])==1
    pos=task['output_positions'][0]
    if tid=='EX-XII-XIII-32-06':
        for holder in [task,pos]:
            for name in ['required_form_ids','required_output_form_ids','tested_form_ids']:
                assert 'nett-acc-pl' in holder[name]
                holder[name]=sorted({'nett-acc-sg' if x=='nett-acc-pl' else x for x in holder[name]})
        old=forms['nett-acc-pl']; new=forms['nett-acc-sg']
        old['used_in_tasks'].remove(tid)
        old['assessed_in'].remove(tid)
        new['used_in_tasks']=sorted(set(new.get('used_in_tasks',[])+[tid]))
    refs=[t for t in seq['tokens'] if t['assessment_role']==role]
    for kind,records in [('form',forms),('sense',senses)]:
        key=kind+'_id'; testkey='tested_'+kind+'_ids'
        independent={t[key] for t in seq['tokens'] if t['assessment_role']=='independent_production'}
        given={t[key] for t in refs}
        removed=set(task[testkey]) & (given-independent)
        task[testkey]=sorted(set(task[testkey])-removed)
        pos[testkey]=sorted(set(pos[testkey])-removed)
        for rid in removed:
            rec=records[rid]
            if tid in rec.get('assessed_in',[]): rec['assessed_in'].remove(tid)
    reference_records=[{'token_index':t['token_index'],'surface':t['surface'],
        'form_id':t['form_id'],'sense_id':t['sense_id'],'assessment_role':role,
        'exact_parenthesis':t['given_reference']['exact_parenthesis']} for t in refs]
    task['given_reference_output_positions']=reference_records
    pos['given_reference_token_positions']=reference_records
    task['grading_obligations']['given_reference_boundary']='Printed Old English hints supply their exact spelling. Apply the taught case/number, agreement, sense and construction; do not count an exact given surface as unaided lexical recall. Same-spelled contextual uses remain distinct.'
    task_changes.append({'task_id':tid,
        'before_tested_forms':before['tested_form_ids'],'after_tested_forms':task['tested_form_ids'],
        'before_tested_senses':before['tested_sense_ids'],'after_tested_senses':task['tested_sense_ids']})

assert models['EX-XII-XIII-32-07']==originals['EX-XII-XIII-32-07'] or all(t['form_id']=='nett-acc-pl' for t in models['EX-XII-XIII-32-07']['tokens'] if t['lemma_id']=='nett')
assert models['EX-XII-XIII-32-06']['tokens'][5]['form_id']=='nett-acc-sg'
assert all(models[t]['text']==originals[t]['text'] for t in models)
assert sum(len(s['tokens']) for s in models.values())==812
correction_path='chapters/ch16/model-binding-amendments.json'
source_identity=identity(source)
correction={
    'chapter_id':'ch16','amendment_id':'U16-A03','status':'pending_independent_verification',
    'source':source,'source_sha256':source_identity['sha256'],
    'source_sha256_normalized_lf':source_identity['sha256_normalized_lf'],
    'visible_hint_audit':identity(audit_path),
    'reason':'Correct singular net in32.6, two stale contextual descriptions of destination tō, and38 exact visible-hint assessment roles; all59 model strings remain unchanged.',
    'corrections':[{'task_id':tid,'original_sequence':originals[tid],
        'original_text':originals[tid]['text'],'corrected_text':models[tid]['text'],
        'changes':[r for r in changes if r['task_id']==tid]} for tid in affected],
    'corrected_sequences':[models[tid] for tid in affected],
    'counts':{'model_sequences':59,'model_tokens':812,'affected_sequences':21,
        'given_reference_role_repairs':38,'number_analysis_repairs':1,'contextual_function_repairs':2,
        'final_model_assessment_roles':dict(Counter(t['assessment_role'] for s in models.values() for t in s['tokens']))}}
write(correction_path,correction)
c['selected_model_corrections']=identity(correction_path)
amendment={
    'amendment_id':'U16-A03','date':'2026-10-27','stage':'authoring',
    'original_contract_checkpoint':'543e214','coordinator':'root',
    'reported_by':['root','unit16_design'],
    'reason':correction['reason'],
    'evidence':['sources/audits/unit16-source/exercises-prompts.json',audit_path,
        'chapters/ch16/answer-key.md','sources/audits/unit16-source/cook-ex-p18-300.png'],
    'correction_record':c['selected_model_corrections'],
    'changes':task_changes,
    'grammatical_scope':'Required contextual forms and senses remain explicit; only unaided recall claims are removed for visible dictionary/form hints. The singular/plural distinction is restored in32.6;32.7 retains plural nets.',
    'unchanged':['All59 exact Cook English prompts and Old English model strings',
        'All learner/key prose, source text, paradigm tables and task/output counts',
        'All teaching statuses and productive boundaries',
        'Sealed packets, prior chapter histories and original translation witnesses'],
    'review_status':'requires_independent_verification'}
# Use a known actual exercise image path rather than an assumed filename.
amendment['evidence']=[x for x in amendment['evidence'] if Path(x).is_file()]
c['amendments'].append(amendment)
write(cp,c)
ledger=read('chapters/ch16/authoring-amendments.json')
ledger['amendments'].append(amendment)
write('chapters/ch16/authoring-amendments.json',ledger)
print(json.dumps(correction['counts'],ensure_ascii=False))
