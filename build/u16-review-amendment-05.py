"""Apply independent current-context corrections without rewriting earlier packets."""
import copy,hashlib,json
from pathlib import Path
def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def write(path,value): Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def identity(path):
    raw=Path(path).read_bytes()
    return {'path':path,'sha256':hashlib.sha256(raw).hexdigest(),
            'sha256_normalized_lf':hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest()}
c=read('chapters/ch16/coverage.json')
assert not any(a['amendment_id']=='U16-A05' for a in c['amendments'])
assert Path('chapters/ch16/blind-freeze.json').is_file()
source='curriculum/proposals/unit16/author-only-cook-sequence-bindings.json'
base={s['owner_id']:s for s in read(source)['sequences']}
models=copy.deepcopy(base)
previous_ref=c['selected_model_corrections']
assert previous_ref==identity(previous_ref['path'])
previous=read(previous_ref['path'])
for s in previous['corrected_sequences']: models[s['owner_id']]=copy.deepcopy(s)
proposal_path='build/u16-paradigms-context-findings.json'
proposal=read(proposal_path)
assert len(proposal['repairs'])==proposal['repair_count']==37
changes=[]
for p in proposal['repairs']:
    seq=models[p['task_id']]
    assert seq['sequence_id']==p['sequence_id']
    token=seq['tokens'][p['token_index']-1]
    assert token['token_index']==p['token_index']
    assert token['surface']==p['expected_surface'],(p,token['surface'])
    before=copy.deepcopy(token)
    key=p['contextual_analysis_key']
    old=token['contextual_analysis'].get(key)
    assert old!=p['proposed_value']
    token['contextual_analysis'][key]=p['proposed_value']
    assert {k:v for k,v in token.items() if k!='contextual_analysis'}=={k:v for k,v in before.items() if k!='contextual_analysis'}
    changes.append({**p,'previous_value':old,'before_token':before,'after_token':copy.deepcopy(token)})
affected=sorted(tid for tid in models if models[tid]!=base[tid])
for tid,seq in models.items():
    assert seq['text']==base[tid]['text']
    assert [t['literal'] for t in seq['tokens']]==[t['literal'] for t in base[tid]['tokens']]
new_path='chapters/ch16/model-binding-review-amendments.json'
record={
 'chapter_id':'ch16','amendment_id':'U16-A05','status':'applied_after_independent_findings',
 'source':source,'source_sha256':identity(source)['sha256'],
 'source_sha256_normalized_lf':identity(source)['sha256_normalized_lf'],
 'previous_correction_record':previous_ref,'independent_proposal':identity(proposal_path),
 'reason':'Preserve the original and A03 records; use current clause-specific contextual descriptions for37 independently identified token coordinates.',
 'contextual_changes':changes,
 'corrections':[{'task_id':tid,'original_sequence':base[tid],
      'original_text':base[tid]['text'],'corrected_text':models[tid]['text'],
      'amendment_chain':['U16-A03']+(['U16-A05'] if any(p['task_id']==tid for p in changes) else [])}
     for tid in affected],
 'corrected_sequences':[models[tid] for tid in affected],
 'counts':{'all_sequences':59,'all_tokens':812,'contextual_coordinate_repairs':37,
     'contextual_tasks':len({p['task_id'] for p in changes}),'cumulative_override_sequences':len(affected)},
 'unchanged':'All text, source prompts, form/sense IDs, assessment roles, original analyses and sealed input packets. Only the indicated contextual_analysis descriptions change relative to A03.'}
# A03 belongs in a task chain only when that task actually had an A03 override.
a03_tasks={s['owner_id'] for s in previous['corrected_sequences']}
for row in record['corrections']:
    if row['task_id'] not in a03_tasks: row['amendment_chain'].remove('U16-A03')
write(new_path,record)
c['selected_model_corrections']=identity(new_path)
amendment={
 'amendment_id':'U16-A05','date':'2026-10-27','stage':'independent_review',
 'coordinator':'root','reported_by':'unit16_paradigms','finding_id':'U16-PAR-03',
 'original_contract_checkpoint':'543e214','complete_drafts_checkpoint':'9b75319','blind_solutions_checkpoint':'1bf0e8e',
 'reason':record['reason'],'previous_correction_record':previous_ref,
 'correction_record':c['selected_model_corrections'],'independent_proposal':identity(proposal_path),
 'counts':record['counts'],'evidence_basis':proposal['evidence'],
 'scope':'Current model token contextual_analysis only. Original analyses and earlier records remain historical; task-specific descriptions now fit their actual governing clauses.',
 'unchanged':record['unchanged'],'review_status':'requires_independent_verification'}
c['amendments'].append(amendment)
write('chapters/ch16/coverage.json',c)
ledger=read('chapters/ch16/authoring-amendments.json')
ledger['amendments'].append(amendment)
write('chapters/ch16/authoring-amendments.json',ledger)
print(record['counts'])
print('32.2:',models['EX-XII-XIII-32-02']['text'])
print('32.3:',models['EX-XII-XIII-32-03']['text'])
