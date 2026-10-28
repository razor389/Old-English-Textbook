"""Apply the independently identified reference and alternative-answer repairs."""
import hashlib,json
from pathlib import Path
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
freeze=read('chapters/ch18/blind-freeze.json')
assert freeze['identity']['raw_sha256']==sha('chapters/ch18/independent-solutions.md')
p='chapters/ch18/coverage.json';before=sha(p);c=read(p)
assert [a['amendment_id'] for a in c['amendments']]==['U18-A01','U18-A02','U18-A03']
changes=[]
def walk(x,path):
    if isinstance(x,dict):
        for k,v in x.items():
            if k=='context_review_basis' and isinstance(v,str) and v.startswith('Whoever has the cup is dative'):
                new=v.replace('Whoever has the cup','Whoever has the alleged stolen property')
                changes.append({'field_path':'/'+('/'.join(map(str,path+[k]))),'before':v,'after':new});x[k]=new
            else:walk(v,path+[k])
    elif isinstance(x,list):
        for i,v in enumerate(x):walk(v,path+[i])
walk(c,[]);assert len(changes)==13,len(changes)
task=next(t for t in c['assigned_items'] if t['task_id']=='EX-XII-XIII-48-09')
output=task['output_positions'][0];old=output['alternatives_policy']
output['alternatives_policy']+=' Both swā and previously taught ðus are valid adverbs of manner here; Cook specifies no swā-only lexical target. The object pronoun ðis does not express the requested manner.'
changes.append({'field_path':'EX-XII-XIII-48-09/output_positions/0/alternatives_policy','before':old,'after':output['alternatives_policy']})
file=Path('chapters/ch18/answer-key.md');original=file.read_bytes();text=original.decode('utf-8')
replacements=[
('The cup remains accusative hit.','**Hit** is neuter accusative singular here, resuming the alleged stolen gold or silver in 47.2 (both neuter). A version directly resuming masculine **læfel** instead uses **hine**; preserve its reference consistently.'),
('identifies whichever person has the cup.','identifies whichever person has the alleged stolen property; neuter **hit** continues 47.2’s gold/silver reference, while direct reference to **læfel** would use **hine**.'),
('The target is manner **swā**, not the object pronoun ðis “this.”','The target is an adverb of manner: **swā** or **ðus**, not the object pronoun **ðis** “this.”')]
for old,new in replacements:
    assert text.count(old)==1,(old,text.count(old))
    text=text.replace(old,new)
file.write_text(text,encoding='utf-8',newline='\n')
a={'amendment_id':'U18-A04','date':'2026-10-28','stage':'independent_review','original_contract_checkpoint':'6874c20e7127fa33c41406d1aa6c0b087e59c824','complete_drafts_checkpoint':'970fcc1f431f6ce2ccdd1f1c85b2b5e63ae0c16a','independent_solutions_checkpoint':'7846befc2c484e8d3e4ff43346da12bf275f5b08','coordinator':'root','reported_by':'unit18_blind','findings':['U18-BLIND-07','U18-BLIND-08'],'reason':'Explain hit through the preceding neuter gold/seolfor and accept the taught manner adverb ðus where Cook imposes no swā-only target.','changes':changes,'master_changes':[{'path':file.as_posix(),'raw_sha256_before':hashlib.sha256(original).hexdigest(),'raw_sha256_after':sha(file),'replacements':[{'before':x,'after':y} for x,y in replacements]}],'evidence_basis':['Cook Exercises printed32,47.2–4: neuter gold/seolfor precede hit; masculine læfel would require hine.','Cook Exercises printed33,48.9: English thus without a lexical control.','Active Unit07 production: thus-invariant-source and thus-thus-source.'],'primary_evidence':[{'path':q,'raw_sha256':sha(q)} for q in ['sources/audits/unit18-source/ex-p32.png','sources/audits/unit18-source/ex-p33.png']],'contract_raw_sha256_before':before,'unchanged':['All exact source prompts, controls and models','All paradigms, cells, form/sense identities and teaching scope','Frozen independent solutions, sealed audits and earlier artifacts'],'review_status':'requires_independent_verification'}
c['amendments'].append(a);write(p,c)
h=read('chapters/ch18/authoring-amendments.json');h['amendments'].append(a);write('chapters/ch18/authoring-amendments.json',h)
assert freeze['identity']['raw_sha256']==sha('chapters/ch18/independent-solutions.md')
print('U18-A04 applied: key reference and valid alternative clarified; independent verification required.')
