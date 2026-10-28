"""Correct an author-preparation explanation without rewriting its frozen witness."""
import hashlib,json
from pathlib import Path
p=Path('chapters/ch18/coverage.json');raw=p.read_bytes();c=json.loads(raw)
assert not c['amendments']
old='The original comment that “for ourselves” may be omitted permits either the visible benefactive/reflexive dative ūs or its omission. The model retains ūs after bohton: we bought wheat for ourselves. It is not an accusative thing purchased.'
new='Ūs is the benefactive/reflexive dative in bohton ūs hwǣte: we bought wheat for ourselves. It refers to the buying subject and is not the accusative thing purchased. The original 45.7 prompt contains no instruction to omit this phrase.'
paths=[('assigned_items',27,'source_control_records',4,'explanatory_content',0),('source_task_crosswalk','original_controls',58,'explanatory_content',0)]
for path in paths:
    obj=c
    for key in path[:-1]:obj=obj[key]
    assert obj[path[-1]]==old
    obj[path[-1]]=new
image='sources/audits/unit18-source/ex-p30.png'
record={
 'amendment_id':'U18-A01','date':'2026-10-28','stage':'authoring',
 'original_contract_checkpoint':'6874c20e7127fa33c41406d1aa6c0b087e59c824',
 'coordinator':'root','reported_by':'unit18_grammar',
 'reason':'The source has a dative/reflexive reference, not an omission instruction. Remove the erroneous source attribution while retaining the original prompt and model.',
 'source_item_id':'EX-XII-XIII-45-07','source_control_id':'U18-HINT-45-07-05',
 'frozen_audit_witness':'sources/audits/unit18-grammar/numeric-control-analysis.json#U18-HINT-45-07-05',
 'primary_inspection':{'path':image,'raw_sha256':hashlib.sha256(Path(image).read_bytes()).hexdigest(),'actually_viewed':True,'reviewer':'root','printed_page':30,'pdf_page_one_based':38,'observation':'Personally reread original45.7: bought wheat (hwǣte,44) for ourselves (161;184.a). No om. instruction accompanies ourselves.'},
 'changes':[{'field_path':'/'+('/'.join(map(str,path))),'before':old,'after':new} for path in paths],
 'contract_raw_sha256_before':hashlib.sha256(raw).hexdigest(),
 'unchanged':['All source prompts, original controls and model text','All task/output targets and dependencies','All forms, senses, features and paradigm cells','Frozen audit/proposal packets and earlier chapters/registers'],
 'review_status':'requires_independent_verification'}
c['amendments'].append(record)
temp=p.with_suffix('.pending.json');temp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');temp.replace(p)
Path('chapters/ch18/authoring-amendments.json').write_text(json.dumps({'chapter_id':'ch18','amendments':[record]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('U18-A01 recorded: two explanatory fields corrected; source prompt/model and frozen packets preserved.')
