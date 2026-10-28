"""Apply independently reported explanatory repairs only after the blind Git freeze."""
import argparse,hashlib,json,re
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--solutions-checkpoint',required=True);args=ap.parse_args()
assert re.fullmatch(r'[0-9a-f]{40}',args.solutions_checkpoint)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
freeze=read('chapters/ch18/blind-freeze.json')
assert freeze['independence']['all_tasks_solved_before_key_access']
assert freeze['identity']['raw_sha256']==sha('chapters/ch18/independent-solutions.md')
p=Path('chapters/ch18/coverage.json');raw=p.read_bytes();c=json.loads(raw)
assert [a['amendment_id'] for a in c['amendments']]==['U18-A01','U18-A02']
old='Retain the explicitly requested first-person plural possessor of the stated things; inflect the possessive with the possessed genitive plural nouns.'
new='The parenthesis (our) belongs to the English expression (our)selves, reinforcing the preceding us. In the supplied clause, ūs selfe means ourselves: selfe agrees with accusative plural ūs. This parenthesis does not introduce a possessive modifying the things.'
changes=[]
def walk(x,path):
    if isinstance(x,dict):
        for k,v in x.items():
            if isinstance(v,str) and v==old:
                changes.append({'field_path':'/'+('/'.join(map(str,path+[k]))),'before':v,'after':new});x[k]=new
            else:walk(v,path+[k])
    elif isinstance(x,list):
        for i,v in enumerate(x):
            if v==old:changes.append({'field_path':'/'+('/'.join(map(str,path+[i]))),'before':v,'after':new});x[i]=new
            else:walk(v,path+[i])
walk(c,[]);assert len(changes)==2,len(changes)
master_changes=[]
for name,before,after in [('student.md',old,new),('answer-key.md','The king’s quoted commands','Jacob’s quoted commands')]:
    file=Path('chapters/ch18')/name;original=file.read_bytes();text=original.decode('utf-8')
    assert text.count(before)==1,(name,text.count(before))
    file.write_text(text.replace(before,after),encoding='utf-8',newline='\n')
    master_changes.append({'path':file.as_posix(),'raw_sha256_before':hashlib.sha256(original).hexdigest(),'raw_sha256_after':sha(file),'before':before,'after':after})
images=['sources/audits/unit18-source/ex-p30.png','sources/audits/unit18-source/ex-p29.png']
a={'amendment_id':'U18-A03','date':'2026-10-28','stage':'independent_review','original_contract_checkpoint':'6874c20e7127fa33c41406d1aa6c0b087e59c824','complete_drafts_checkpoint':'970fcc1f431f6ce2ccdd1f1c85b2b5e63ae0c16a','independent_solutions_checkpoint':args.solutions_checkpoint,'coordinator':'root','reported_by':['unit18_blind','unit18_paradigms'],'reason':'Correct the reflexive English hint explanation in45.6 and identify Jacob as the speaker of44.1. Preserve actual independent attempts and every prompt/model.','changes':changes,'master_changes':master_changes,'source_items':['EX-XII-XIII-45-06','EX-XII-XIII-44-01'],'source_control_id':'U18-HINT-45-06-07','primary_evidence':[{'path':x,'raw_sha256':sha(x)} for x in images],'contract_raw_sha256_before':hashlib.sha256(raw).hexdigest(),'unchanged':['All exact source prompts, controls and models','All task/output targets and dependencies','All paradigms, cells, form/sense identities and teaching scope','All frozen independent solutions, sealed audits and earlier artifacts'],'review_status':'requires_independent_verification'}
c['amendments'].append(a);temp=p.with_suffix('.pending.json');write(temp,c);temp.replace(p)
h=read('chapters/ch18/authoring-amendments.json');h['amendments'].append(a);write('chapters/ch18/authoring-amendments.json',h)
assert freeze['identity']['raw_sha256']==sha('chapters/ch18/independent-solutions.md')
print('U18-A03 applied after frozen solutions; both explanatory findings await independent re-verification.')
