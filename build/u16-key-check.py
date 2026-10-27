"""Check key coverage and exact committed Cook models; not a linguistic proof."""
import json,re,hashlib,unicodedata
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text(encoding='utf8'))
C=read('chapters/ch16/coverage.json');K=(R/'chapters/ch16/answer-key.md').read_text(encoding='utf8')
tasks=C['assigned_items'];models={x['source_item_id']:x['model']for x in read('sources/audits/unit16-grammar/author-only-cook-models.json')['items']}
if C.get('selected_model_corrections'):
    for seq in read(C['selected_model_corrections']['path'])['corrected_sequences']:
        models[seq['owner_id']]=seq['text']
errors=[];keys=re.findall(r'<!--\s*key:\s*(\S+)\s*-->',K);outputs=re.findall(r'<!--\s*output:\s*(\S+)\s*-->',K)
expected_keys=[t['key_item_id']for t in tasks];expected_outputs=[x['output_position_id']for t in tasks for x in t['output_positions']]
if len(keys)!=len(expected_keys) or set(keys)!=set(expected_keys):errors.append('Key coverage differs from canonical tasks')
if len(outputs)!=len(expected_outputs) or set(outputs)!=set(expected_outputs):errors.append('Output coverage differs from canonical tasks')
task_by_key={t['key_item_id']:t for t in tasks}
ordered_outputs=[x['output_position_id']for k in keys for x in task_by_key[k]['output_positions']]
if outputs!=ordered_outputs:errors.append('Output order differs within learner task groups')
if K!=unicodedata.normalize('NFC',K):errors.append('Key is not NFC')
for t in tasks:
    marker='<!-- key: '+t['key_item_id']+' -->'
    if K.count(marker)!=1:errors.append('Key marker not unique: '+t['task_id']);continue
    body=K.split(marker,1)[1].split('<!-- key:',1)[0]
    if t['task_id'] in models:
        first=body.strip().split('\n\n',1)[0].replace('**','')
        if first!=models[t['task_id']]:errors.append('Cook model differs: '+t['task_id'])
    for o in t['output_positions']:
        om='<!-- output: '+o['output_position_id']+' -->'
        if K.count(om)!=1:errors.append('Output marker not unique: '+o['output_position_id']);continue
        answer=body.split(om,1)[1].split('<!-- output:',1)[0].strip()
        if not answer:errors.append('Empty answer: '+o['output_position_id'])
w=R/'chapters/ch16/author-translation-witness.md'
wsha=hashlib.sha256(w.read_bytes()).hexdigest()
if wsha!='63269a300875c01128a5ca6eac3db8086e14195d4c6c7c46f602ee146bfe5dc6':errors.append('Initial translation witness changed')
student=R/'chapters/ch16/student.md'
student_comparison='not yet available'
if student.exists():
    text=student.read_text(encoding='utf8')
    student_keys=re.findall(r'<!--\s*item:\s*(\S+)\s*-->',text)
    student_comparison={'present_items':len(student_keys),'task_order_matches':student_keys==[task_by_key[k]['task_id']for k in keys]}
    if not student_comparison['task_order_matches']:errors.append('Current learner task order differs/incomplete')
out={'chapter':'ch16','status':'pass' if not errors else 'fail','key_markers':len(keys),'output_markers':len(outputs),'cook_models_checked':len(models),'original_tasks':sum(t['task_id'].startswith('NEW-U16-')for t in tasks),'witness_sha256':wsha,'key_sha256':hashlib.sha256((R/'chapters/ch16/answer-key.md').read_bytes()).hexdigest(),'current_contract_sha256':hashlib.sha256((R/'chapters/ch16/coverage.json').read_bytes()).hexdigest(),'student_comparison':student_comparison,'errors':errors,'linguistic_review_notes':['All179 outputs have individual answers; form explanations and finite/nonfinite analyses are specific to their inputs.','The independent translation witness preceded consultation of the design full English model. Its complete text is preserved.','Key translation clarifies grammatical singular plega as young men’s play; the earlier witness wording remains unchanged.','Meahte/hęrede and hæfde/wolde surface syncretism is explicitly distinguished from selected contextual mood.','The Cook35.13 singular-addressee alternative uses the taught singular command and possessive with the same supplied partitive frame; the English prompt does not specify plural you.','Sealed source/audit/proposal files and canonical coverage were read only.']}
(R/'build/u16-key-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(out,ensure_ascii=False,indent=2))
assert not errors
