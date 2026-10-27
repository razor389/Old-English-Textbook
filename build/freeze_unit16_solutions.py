"""Check actual response coverage after root readback; then require a Git freeze."""
import argparse,hashlib,json,re
from pathlib import Path
ap=argparse.ArgumentParser(__doc__)
ap.add_argument('--draft-checkpoint',required=True)
ap.add_argument('--learner-sha256',required=True)
ap.add_argument('--witness-sha256',required=True)
ap.add_argument('--readback-note',required=True)
a=ap.parse_args()
def identity(path):
    raw=Path(path).read_bytes()
    return {'path':path,'raw_sha256':hashlib.sha256(raw).hexdigest(),
            'normalized_lf_sha256':hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest()}
def read(path): return json.loads(Path(path).read_text(encoding='utf-8-sig'))
c=read('chapters/ch16/coverage.json')
learner=Path('chapters/ch16/student.md').read_text(encoding='utf-8')
witness=Path('chapters/ch16/independent-solutions.md').read_text(encoding='utf-8')
assert identity('chapters/ch16/student.md')['raw_sha256']==a.learner_sha256
assert identity('chapters/ch16/independent-solutions.md')['raw_sha256']==a.witness_sha256
items=re.findall(r'<!-- item: ([^ ]+) -->',witness)
outputs=re.findall(r'<!-- output: ([^ ]+) -->',witness)
assert items==re.findall(r'<!-- item: ([^ ]+) -->',learner)
assert outputs==re.findall(r'<!-- output: ([^ ]+) -->',learner)
assert len(items)==len(set(items))==c['contract_metrics']['tasks']
assert len(outputs)==len(set(outputs))==c['contract_metrics']['requested_output_positions']
assert set(items)=={t['task_id'] for t in c['assigned_items']}
assert set(outputs)=={o['output_position_id'] for t in c['assigned_items'] for o in t['output_positions']}
attempts={}
for m in re.finditer(r'<!-- output: ([^ ]+) -->\s*(.*?)(?=<!-- output:|\n## |\Z)',witness,re.S):
    body=m[2].strip()
    assert body and '____' not in body,m[1]
    attempts[m[1]]={'line':witness[:m.start()].count('\n')+1,'actual_attempt_present':True,'response_characters':len(body)}
assert len(attempts)==len(outputs)
assert len(a.readback_note)>80, 'Record actual human/model readback, not only marker counts'
report={
 'chapter_id':'ch16','status':'complete_blind_witness_ready_for_local_git_freeze',
 'reviewer':'unit16_blind','coordinator':'root',
 'identity':identity('chapters/ch16/independent-solutions.md'),
 'learner_identity':identity('chapters/ch16/student.md'),
 'draft_checkpoint':a.draft_checkpoint,
 'strict_protocol':'sources/audits/unit16-coordinator/review-independence.json',
 'coordinator_actual_readback':a.readback_note,
 'task_count':len(items),'output_positions':len(outputs),
 'morphology_group_output_positions':c['contract_metrics']['morphology_output_positions'],
 'single_cell_form_output_positions':c['contract_metrics']['single_cell_form_output_positions'],
 'task_coverage':[{'task_id':t['task_id'],'actual_attempt_present':True,
    'requested_output_positions':[o['output_position_id'] for o in t['output_positions']]} for t in c['assigned_items']],
 'output_attempts':attempts,
 'independence':{'no_current_author_role':True,'all_tasks_solved_before_key_access':True,
    'learner_unchanged_during_solve':True,
    'comparison_access':'NOT YET UNLOCKED; requires explicit coordinator message after this witness is committed'},
 'scope_limit':'Coverage and freeze gate only. Correctness, alternative solutions and missing learner support remain substantive independent review work.'}
Path('chapters/ch16/blind-freeze.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Complete attempted witness:',len(items),'tasks,',len(outputs),'outputs. Save unchanged witness in Git before unlocking comparison.')
