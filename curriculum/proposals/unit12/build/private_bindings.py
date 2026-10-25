"""Private required output identities. Reserved solver must not read."""
from pathlib import Path
import importlib.util,json,copy
spec=importlib.util.spec_from_file_location('u12public',Path(__file__).with_name('public_bindings.py'))
pub=importlib.util.module_from_spec(spec);spec.loader.exec_module(pub)
SPECS={
'C01':['ic-nom-pl habban-pres-1-pl|@habban-result se-n-acc-sg hus-acc-sg gewyrcean-past-participle'],
'C02':['he-nom-pl habban-pret-3-pl|@habban-result se-n-acc-sg hus-acc-sg gewyrcean-past-participle'],
'C03':['se-all-nom-pl mann-nom-pl bindan-pret-3-pl se-n-acc-sg hors-acc-sg','se-n-nom-sg hors-nom-sg weorthan-pret-3-sg|weorthan-1 bindan-participle-citation'],
'C04':['se-m-nom-sg munuc-nom-sg secgan-pres-3-sg thaet-conjunction-invariant he-m-nom-sg wesan-present-subj-3-sg her-invariant','se-m-nom-sg munuc-nom-sg secgan-pret-3-sg thaet-conjunction-invariant he-m-nom-sg wesan-preterite-subj-3-sg her-invariant'],
'C05':[pub.E['10']], 'C06':[pub.E['11']],
'C07':['gierwan-imp-2-sg se-m-acc-sg mete-acc-sg','ic-nom-sg @have-result-1 se-m-acc-sg mete-acc-sg @gierwed'],
'C08':['se-f-nom-sg brycg-nom-sg wesan-pret-3-sg|wesan-passive gewyrcean-past-participle','@then cuman-pret-3-sg mann-nom-sg'],
'R04':['se-n-nom-sg hus-nom-sg wesan-pres-3-sg|wesan-passive gewyrcean-past-participle']}
data=pub.load('curriculum/proposals/unit12/author-only-model-seed.json')
seqs=[]
for m in data['models']:
 code=m['task_id'].removeprefix('NEW-U12-')
 if code not in SPECS:continue
 assert len(m['old_english_outputs'])==len(SPECS[code]),code
 for i,(text,refs) in enumerate(zip(m['old_english_outputs'],SPECS[code]),1):
  seq=pub.make_sequence(m['task_id']+f'-OUTPUT{i}',text,refs,m['task_id'],'private_required_model_output')
  if seq:seqs.append(seq)
pattern_path=Path('curriculum/proposals/unit12/construction-patterns.json')
if pattern_path.exists():
 for pattern in pub.load(str(pattern_path))['patterns']:
  for position in pattern['positions']:
   seq=copy.deepcopy(position['sequence'])
   seq.update(sequence_id=position['position_id']+'-F06-OUTPUT',owner_id='NEW-U12-F06',kind='private_required_model_output')
   seqs.append(seq)
pub.write('author-only-sequence-bindings.json',{'schema_version':1,'chapter':'ch12','access':'PRIVATE: excluded until independent solutions are frozen.','status':'closed' if not pub.issues else 'pending_audit_records','sequences':seqs,'issues':pub.issues})
print(json.dumps({'sequences':len(seqs),'tokens':sum(len(s['tokens']) for s in seqs),'issues':pub.issues},ensure_ascii=False))
