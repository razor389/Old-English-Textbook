"""Separate an original-task expression from its editorial locator."""
import hashlib,json
from pathlib import Path
p=Path('chapters/ch18/coverage.json');raw=p.read_bytes();c=json.loads(raw)
assert [a['amendment_id'] for a in c['amendments']]==['U18-A01']
before='swā-hwæt-swā176.2';after='swā-hwæt-swā 176.2';changes=[]
def walk(x,path):
    if isinstance(x,dict):
        for k,v in x.items():
            if isinstance(v,str) and before in v:
                replacement=v.replace(before,after)
                changes.append({'field_path':'/'+('/'.join(map(str,path+[k]))),'before':v,'after':replacement});x[k]=replacement
            else:walk(v,path+[k])
    elif isinstance(x,list):
        for i,v in enumerate(x):walk(v,path+[i])
walk(c,[]);assert changes
master_changes=[]
for name in ['student.md','answer-key.md']:
    file=Path('chapters/ch18')/name;old=file.read_bytes();text=old.decode('utf-8')
    assert text.count(before)==1,(name,text.count(before))
    file.write_text(text.replace(before,after),encoding='utf-8',newline='\n')
    master_changes.append({'path':file.as_posix(),'raw_sha256_before':hashlib.sha256(old).hexdigest(),'exact_typographic_change':{'before':before,'after':after}})
a={'amendment_id':'U18-A02','date':'2026-10-28','stage':'authoring','original_contract_checkpoint':'6874c20e7127fa33c41406d1aa6c0b087e59c824','coordinator':'root','reported_by':'root','reason':'Add an ordinary space between the cited Old English expression and its modern page/line locator in NEW-U18-R04-O002.','changes':changes,'master_changes':master_changes,'contract_raw_sha256_before':hashlib.sha256(raw).hexdigest(),'unchanged':['All source text and Cook prompts','All models, answer targets and dependency identities','All paradigm cells and teaching scope','Frozen audits and earlier artifacts'],'review_status':'requires_independent_verification'}
c['amendments'].append(a);temp=p.with_suffix('.pending.json');temp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');temp.replace(p)
path=Path('chapters/ch18/authoring-amendments.json');hist=json.loads(path.read_text(encoding='utf-8'));hist['amendments'].append(a);path.write_text(json.dumps(hist,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('U18-A02: one original-task locator separated in both masters and',len(changes),'contract fields.')
