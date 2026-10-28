"""Preview or apply the five authorized U17-A02 learner-help replacements."""
from pathlib import Path
import argparse
import difflib
import hashlib
import json
import re
import runpy
import unicodedata

ROOT=Path(__file__).resolve().parents[1]
student=ROOT/'chapters/ch17/student.md'
helper=ROOT/'build/u17-learner-draft.py'
preview=ROOT/'build/u17-learner-A02-preview.md'
record=ROOT/'build/u17-learner-A02-repairs.json'
sha=lambda b:hashlib.sha256(b).hexdigest()
allowed=['EX-XII-XIII-40-01','EX-XII-XIII-42-05','EX-XII-XIII-42-08',
         'EX-XII-XIII-43-13','EX-XII-XIII-43-15']
def block(text,tid):
    marker='<!-- item: '+tid+' -->'
    start=text.index(marker)
    end=text.find('<!-- item:',start+len(marker))
    return text[start:end if end>=0 else len(text)]
def mask(text):
    for tid in allowed:
        text=text.replace(block(text,tid),'<!-- authorized item: '+tid+' -->\n')
    return text

ap=argparse.ArgumentParser(__doc__)
ap.add_argument('--apply',action='store_true')
args=ap.parse_args()
if not args.apply:
    before_bytes=student.read_bytes()
    before=before_bytes.decode('utf-8')
    ns=runpy.run_path(str(helper),run_name='u17_learner_preview')
    after=unicodedata.normalize('NFC',''.join(ns['OUT']).rstrip()+'\n')
    assert mask(before)==mask(after),'Preview changes outside the five authorized items'
    assert len(ns['EMITTED'])==420,'Expected 420 teaching records'
    # Earlier independent-review repairs must survive the refreshed helper.
    earlier=json.loads((ROOT/'build/u17-learner-paradigm-repairs.json').read_text(encoding='utf-8'))
    for repair in earlier['changes']:
        assert repair['after'] in before and repair['after'] in after,repair['finding_id']+' not preserved'
    changes=[{'task_id':tid,'before':block(before,tid),'after':block(after,tid)} for tid in allowed]
    assert all(c['before']!=c['after'] for c in changes),'All five authorized items must change'
    preview.write_text(after,encoding='utf-8',newline='\n')
    (ROOT/'build/u17-learner-before-A02.md').write_bytes(before_bytes)
    patch=''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),
                  fromfile='student.md before U17-A02',tofile='student.md after U17-A02'))
    (ROOT/'build/u17-learner-A02-repairs.patch').write_text(patch,encoding='utf-8',newline='\n')
    receipt={'amendment_id':'U17-A02','status':'preview_checked_before_apply',
             'before_learner_sha256':sha(before_bytes),'after_learner_sha256':sha(preview.read_bytes()),
             'helper_sha256':sha(helper.read_bytes()),
             'contract_sha256':sha((ROOT/'chapters/ch17/coverage.json').read_bytes()),
             'allowed_tasks':allowed,'changes_outside_allowed_tasks':False,
             'prior_paradigm_repairs_preserved':[x['finding_id'] for x in earlier['changes']],
             'changes':changes,
             'scope':'Three single-word helps replaced by complete supplied phrases; accompanying-speech help added at 42.5 and 42.8 with one new marker first at 42.5. All explanation text is taken verbatim from amended contract meaning_and_analysis.'}
    record.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('Preview checked: changes restricted to all five authorized tasks; four prior repairs preserved.')
    print(patch)
else:
    receipt=json.loads(record.read_text(encoding='utf-8'))
    assert receipt['status']=='preview_checked_before_apply'
    assert sha(student.read_bytes())==receipt['before_learner_sha256'],'Learner changed since preview'
    assert sha(helper.read_bytes())==receipt['helper_sha256'],'Helper changed since preview'
    assert sha(preview.read_bytes())==receipt['after_learner_sha256'],'Preview changed'
    assert sha((ROOT/'chapters/ch17/coverage.json').read_bytes())==receipt['contract_sha256'],'Contract changed since preview'
    student.write_bytes(preview.read_bytes())
    receipt['status']='author_amendment_applied_pending_independent_recheck'
    record.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    report=ROOT/'build/u17-learner-report.md'
    append='\n## U17-A02: complete supplied expressions\n\n'
    append+='The coordinator recorded U17-A02 in the canonical contract before these learner edits. A preview comparison verified that the only learner changes are within Cook 40.1, 42.5, 42.8, 43.13 and 43.15. The four prior P17 prose repairs remain verbatim.\n\n'
    append+='Cook 40.1 now supplies **betwēox wīfum**; Cook 43.13 **him tōgēanes**; and Cook 43.15 **Gode swā gecwēme**, replacing their earlier single-word supplied lines. Cook 42.5 and 42.8 now supply **ðus cweðende**; the new accompanying-speech teaching marker occurs first at 42.5, with the complete help repeated at 42.8. All five meaning-and-analysis explanations are verbatim amended-contract text.\n\n'
    append+='Before learner SHA-256: `'+receipt['before_learner_sha256']+'`.\n\n'
    append+='Revised learner SHA-256: `'+receipt['after_learner_sha256']+'`.\n\n'
    append+='Assembly-helper SHA-256: `'+receipt['helper_sha256']+'`.\n\n'
    append+='Contract SHA-256 used: `'+receipt['contract_sha256']+'`.\n\n'
    append+='The exact before/after task blocks and unified patch are recorded in `build/u17-learner-A02-repairs.json` and `build/u17-learner-A02-repairs.patch`; the original learner master is preserved in `build/u17-learner-before-A02.md`. No contract, key, model, table, prompt, reading, source, register or review was edited. The learner-only check is rerun after application; independent acceptance remains pending.\n'
    report.write_text(report.read_text(encoding='utf-8').rstrip()+'\n'+append,encoding='utf-8',newline='\n')
    print('Applied U17-A02 learner help in exactly five task blocks.')
    print('Learner SHA-256:',receipt['after_learner_sha256'])
