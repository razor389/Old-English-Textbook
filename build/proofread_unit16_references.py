"""One-use, reversible eight-space amendment found during visual review."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path

def sha_bytes(raw): return hashlib.sha256(raw).hexdigest()
def write(path, value): Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def semantic(c, keys):
    return sha_bytes(json.dumps({k:c[k] for k in keys},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8'))

student_path=Path('chapters/ch16/student.md')
coverage_path=Path('chapters/ch16/coverage.json')
student_raw=student_path.read_bytes()
assert sha_bytes(student_raw)=='04f539bcefe0ebb231e537d4495d1bd459dbee62dda3f0514f087a9a7eeea49d'
c=json.loads(coverage_path.read_text(encoding='utf-8'))
assert c['textual_review']['status']=='accepted'
before_acceptance=deepcopy(c['textual_review'])
keys=before_acceptance['accepted_contract_semantic_identity']['keys']
assert semantic(c,keys)==before_acceptance['accepted_contract_semantic_identity']['sha256']
replacements=[('on169.1','on 169.1',1),('composition35.3','composition 35.3',1),
              ('at170.14–16','at 170.14–16',1),('page169','page 169',1),
              ('notes6','notes 6',1),('and10','and 10',2),('lines6','lines 6',1)]
student=student_raw.decode('utf-8')
for old,new,count in replacements:
    assert student.count(old)==count,(old,student.count(old))
    student=student.replace(old,new)
assert student.replace(' ','')==student_raw.decode('utf-8').replace(' ','')
assert len(student)-len(student_raw.decode('utf-8'))==8
changes=[]
def walk(value,path=()):
    if isinstance(value,dict):
        return {k:walk(v,path+(k,)) for k,v in value.items()}
    if isinstance(value,list):
        return [walk(v,path+(i,)) for i,v in enumerate(value)]
    if isinstance(value,str):
        if path[0] not in ['assigned_items','source_spans','teaching_records'] or path[-1] not in ['prompt','scope_rationale','explanation']:
            return value
        new=value
        for old,replacement,_ in replacements: new=new.replace(old,replacement)
        if new!=value:
            assert path[0] in ['assigned_items','source_spans','teaching_records'],path
            assert path[-1] in ['prompt','scope_rationale','explanation'],path
            assert new.replace(' ','')==value.replace(' ','')
            changes.append({'path':list(path),'before':value,'after':new})
        return new
    return value
newc=walk(c)
assert len(changes)==8,len(changes)
for field in ['lexical_inventory','grammar_inventory','paradigms','display_plan','analysis_inputs','contract_metrics','new_material_examples']:
    assert newc[field]==c[field],field
for field in ['learner_text','original_notes','original_note_anchors']:
    assert newc['source_spans'][0][field]==c['source_spans'][0][field],field
assert [x['prompt'] for x in newc['assigned_items'] if x['task_id'].startswith('EX-')]==[x['prompt'] for x in c['assigned_items'] if x['task_id'].startswith('EX-')]
student_path.write_text(student,encoding='utf-8',newline='\n')
record='chapters/ch16/presentation-proofreading-amendment.json'
amendment={
    'id':'U16-A08','status':'applied_awaiting_non_author_confirmation',
    'origin':'Four missing-space findings in actual learner-v1 pages56,57,66,67 by unit16_pages_last.',
    'scope':'Insert eight ordinary word spaces before modern page, exercise and note references. No Old English, original source notes, Cook prompt, table, model answer, target or dependency changes.',
    'prior_accepted_text_checkpoint':'effe431',
    'before_textual_acceptance':before_acceptance,
    'student_replacements':[{'before':a,'after':b,'occurrences':n} for a,b,n in replacements],
    'student_before_sha256':sha_bytes(student_raw),
    'student_after_sha256':sha_bytes(student_path.read_bytes()),
    'contract_field_changes':changes,
    'contract_semantic_identity_before':before_acceptance['accepted_contract_semantic_identity'],
    'contract_semantic_identity_after':{**before_acceptance['accepted_contract_semantic_identity'],'sha256':semantic(newc,keys)},
    'unchanged_artifacts':{p:sha_bytes(Path(p).read_bytes()) for p in [
        'chapters/ch16/answer-key.md','chapters/ch16/independent-solutions.md',
        'chapters/ch16/author-translation-witness.md','chapters/ch16/review.md',
        'chapters/ch16/review-ledger.json','chapters/ch16/reviews/paradigms.json']},
    'non_author_review':'chapters/ch16/reviews/presentation-proofreading.json'
}
newc['textual_review']['status']='proofreading_confirmation_pending'
newc['textual_review']['proofreading_addendum']={'record':record,'status':'awaiting_non_author_confirmation'}
write(record,amendment)
write(coverage_path,newc)
print('Applied exactly eight spaces in four learner paragraphs and eight corresponding contract fields; independent confirmation pending.')
