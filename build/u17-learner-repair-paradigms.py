"""Apply only the four coordinator-authorized post-witness learner wording repairs."""
from pathlib import Path
import difflib
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
changes=[
    {'finding_id':'P17-01',
     'before':'The present second and third singular have i. The preterite contrasts singular æ with ǣ in the second singular and plural, and changes ð to d. Retain the lexical prefix ge-.',
     'after':'The present second and third singular have i. In the preterite, first and third singular gecwæð retain æ and ð; second singular gecwǣde and plural gecwǣdon have ǣ and d. Retain the lexical prefix ge-.'},
    {'finding_id':'P17-03',
     'before':'The bracket replaces the infinitive “to see” with a purpose clause, “that they might see”; use the appropriate subjunctive. The rank comparison after ofer is dative as Cook §166 directs.',
     'after':'The bracket replaces the infinitive “to see” with the finite clause “that they might see”, expressing what they desired under gewilnodon. This desired-content clause takes the subjunctive (Cook §194.b). The rank comparison after ofer is dative as Cook §166 directs.'},
    {'finding_id':'P17-04',
     'before':'The storm fulfils his word. Keep that meaning of dōn distinct from a general act of making.',
     'after':'The spirits of the storms fulfil his word. The plural subject takes dōð; keep this fulfilment sense of dōn distinct from a general act of making.'},
    {'finding_id':'P17-05',
     'before':'The mighty and the humble are weak masculine plural adjectives naming people. Omit the marked their without deleting the seats.',
     'after':'The mighty and the humble are weak masculine plural adjectives naming people. Omit the marked their without deleting the seat.'},
]
sha=lambda b:hashlib.sha256(b).hexdigest()
student=ROOT/'chapters/ch17/student.md'
helper=ROOT/'build/u17-learner-draft.py'
before_bytes=student.read_bytes()
before=before_bytes.decode('utf-8')
helper_before=helper.read_text(encoding='utf-8')
for change in changes:
    assert before.count(change['before'])==1,change['finding_id']+' learner before-text count'
    assert helper_before.count(change['before'])==1,change['finding_id']+' helper before-text count'
after=before
helper_after=helper_before
for change in changes:
    after=after.replace(change['before'],change['after'])
    helper_after=helper_after.replace(change['before'],change['after'])
snapshot=ROOT/'build/u17-learner-before-paradigm-repairs.md'
assert not snapshot.exists(),'Repair snapshot already exists; do not overwrite the before witness'
snapshot.write_bytes(before_bytes)
student.write_text(after,encoding='utf-8',newline='\n')
helper.write_text(helper_after,encoding='utf-8',newline='\n')
patch=''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),
                                 fromfile='student.md before P17 repairs',tofile='student.md after P17 repairs'))
(ROOT/'build/u17-learner-paradigm-repairs.patch').write_text(patch,encoding='utf-8',newline='\n')
receipt={'authorization':'Coordinator task after blind witness frozen at ed28a8e',
         'findings_source':'chapters/ch17/reviews/paradigms.md',
         'status':'author_repairs_applied_pending_independent_recheck',
         'changed_files':['chapters/ch17/student.md','build/u17-learner-draft.py'],
         'before_snapshot':'build/u17-learner-before-paradigm-repairs.md',
         'exact_patch':'build/u17-learner-paradigm-repairs.patch',
         'before_learner_sha256':sha(before_bytes),
         'after_learner_sha256':sha(student.read_bytes()),
         'after_helper_sha256':sha(helper.read_bytes()),
         'changes':changes,
         'scope':'Only the four specified prose replacements. No table, model, prompt, reading, marker, contract, key, source, register or review edit.'}
(ROOT/'build/u17-learner-paradigm-repairs.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
report=ROOT/'build/u17-learner-report.md'
append='\n## Authorized repairs after the frozen blind witness\n\n'
append+='After the blind witness was frozen at `ed28a8e`, the coordinator authorized P17-01, P17-03, P17-04 and P17-05. These four learner wording repairs are applied; independent reviewer acceptance is still pending. The previous final hash above records the initial handoff, not this repaired master.\n\n'
for change in changes:
    append+='**'+change['finding_id']+'**\n\nBefore: '+change['before']+'\n\nAfter: '+change['after']+'\n\n'
append+='Before learner SHA-256: `'+receipt['before_learner_sha256']+'`.\n\n'
append+='Repaired learner SHA-256: `'+receipt['after_learner_sha256']+'`.\n\n'
append+='Repaired assembly-helper SHA-256: `'+receipt['after_helper_sha256']+'`.\n\n'
append+='The complete before-master snapshot, exact unified patch and structured change/hash record are respectively `build/u17-learner-before-paradigm-repairs.md`, `build/u17-learner-paradigm-repairs.patch` and `build/u17-learner-paradigm-repairs.json`. The changes preserve all literal tables, models, prompts, reading text and markers. The learner-only self-check is rerun after this repair. No independent acceptance is claimed.\n'
report.write_text(report.read_text(encoding='utf-8').rstrip()+'\n'+append,encoding='utf-8',newline='\n')
print('Applied four authorized prose repairs.')
print('Learner SHA-256:',receipt['after_learner_sha256'])
