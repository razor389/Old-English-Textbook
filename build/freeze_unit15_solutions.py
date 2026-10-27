"""Record completeness after coordinator's full readback; correctness remains review work."""
import hashlib
import json
import re
from pathlib import Path

def identity(path):
    b=Path(path).read_bytes()
    return {'path':path,'raw_sha256':hashlib.sha256(b).hexdigest(),
            'normalized_lf_sha256':hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest()}
student=Path('chapters/ch15/student.md').read_text(encoding='utf-8')
solution=Path('chapters/ch15/independent-solutions.md').read_text(encoding='utf-8')
c=json.loads(Path('chapters/ch15/coverage.json').read_text(encoding='utf-8'))
assert identity('chapters/ch15/student.md')['raw_sha256']=='6caabca8c79ff4ce94beb1ce5c059b0f6cda65427b434bb11a042971b2e0df33'
assert identity('chapters/ch15/independent-solutions.md')['raw_sha256']=='2abad21bf90cf8994afbb7e48ec0807b74ab3d1e4cddf80cb30513845ca592fe'
tasks=re.findall(r'<!-- item: ([^ ]+) -->',solution)
outputs=re.findall(r'<!-- output: ([^ ]+) -->',solution)
assert tasks==re.findall(r'<!-- item: ([^ ]+) -->',student) and len(tasks)==105
assert outputs==re.findall(r'<!-- output: ([^ ]+) -->',student) and len(outputs)==322
assert set(tasks)=={t['task_id'] for t in c['assigned_items']}
assert set(outputs)=={o['output_position_id'] for t in c['assigned_items'] for o in t['output_positions']}
attempts={}
for match in re.finditer(r'<!-- output: ([^ ]+) -->\s*(.*?)(?=<!-- output:|\n## |\Z)',solution,re.S):
    body=match[2].strip()
    assert body and '____' not in body,match[1]
    attempts[match[1]]={'line':solution[:match.start()].count('\n')+1,'actual_attempt_present':True,'response_characters':len(body)}
assert len(attempts)==322
report={
    'chapter_id':'ch15','status':'complete_blind_witness_ready_for_local_git_freeze',
    'date':'2026-10-27','reviewer':'unit15_blind','coordinator':'root',
    'identity':identity('chapters/ch15/independent-solutions.md'),
    'learner_identity':identity('chapters/ch15/student.md'),
    'draft_checkpoint':'3822d4b',
    'strict_protocol':'sources/audits/unit15-coordinator/review-independence.json',
    'coordinator_actual_readback':'Read the entire witness, including all116 form responses, analyses,19 original compositions,50 Cook translations,15 reading tasks and three full translations. Every requested output is attempted in learner order. The completeness gate does not prejudge linguistic correctness or force model-string agreement. Modal uncertainty in30.11 and local alternatives remain explicit.',
    'task_count':105,'output_positions':322,'morphology_cells':116,
    'task_coverage':[{'task_id':t['task_id'],'actual_attempt_present':True,
                      'requested_output_positions':[o['output_position_id'] for o in t['output_positions']]} for t in c['assigned_items']],
    'output_attempts':attempts,
    'independence':{'no_current_author_role':True,'all_tasks_solved_before_key_access':True,
                    'learner_unchanged_during_solve':True,'comparison_access':'NOT YET UNLOCKED; requires subsequent explicit coordinator message after Git commit'},
    'queued_repairs':'Separate paradigm review has identified a missing local support frame in29.9 and minor key scope labels. Both masters remain unchanged until this witness is committed; subsequent repairs and review must preserve the witness.'
}
Path('chapters/ch15/blind-freeze.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Verified105 tasks/322 nonempty attempted outputs; coordinator full readback recorded. Git freeze required next.')
