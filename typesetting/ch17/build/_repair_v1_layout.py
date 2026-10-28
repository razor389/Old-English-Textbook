"""Apply four localized page-review repairs without changing accepted wording."""
import hashlib,json,re,shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1]
report_path=root/'layout-adjustments.json'
report=json.loads(report_path.read_text(encoding='utf-8'))
assert not report.get('v1_page_repairs_applied')
for stem in ['chapter-17','answer-key']:
    for source,target in [(root/'build'/f'{stem}.pdf',root/'build'/f'{stem}-v1.pdf'),
                          (root/f'{stem}.tex',root/'build'/f'{stem}-v1.tex')]:
        assert not target.exists()
        shutil.copyfile(source,target)

def wrap(text,start,end,tag):
    assert text.count(start)==1,(tag,start)
    a=text.index(start)
    b=text.index(end,a)+len(end)
    body=text[a:b]
    body=re.sub(r'(?m)^\\reserve\{\d+\\baselineskip\}\n','',body)
    return text[:a]+'% page-review repair: '+tag+'\n'+r'\par\begin{minipage}{\linewidth}\raggedright'+'\n'+body+'\n'+r'\end{minipage}\par'+'\n'+text[b:]

p=root/'chapter-17.tex'
s=p.read_text(encoding='utf-8')
s=wrap(s,'% mdparagraph:P299:begin','% mdtable:T81:end','U17LF01: participle heading, rules and complete two-form table')
s=wrap(s,'% mdparagraph:P388:begin','\\end{minipage}\\par\n\\par\\endgroup','U17LF02: participial agreement introduction with first complete singular panel')
p.write_text(s,encoding='utf-8',newline='\n')
p=root/'answer-key.tex'
s=p.read_text(encoding='utf-8')
s=wrap(s,'% mdparagraph:P094:begin','% mdparagraph:P096:end','K17-P01: F04 imperative prompt, model and explanation')
s=wrap(s,'% mdparagraph:P543:begin','% mdparagraph:P544:end','K17-P02: keep short Apollo prompt and answer together')
p.write_text(s,encoding='utf-8',newline='\n')
report['adjustments'] += [
 {'finding':'U17LF01','original_pages':[35,36],'change':'Keep P299–P301 and T81 in one short block; remove its competing internal reservation.','reason':'Attach the participle heading and rules to the two-form display.'},
 {'finding':'U17LF02','original_pages':[47,48],'change':'Keep P388–P390 with the first complete singular panel of T111; later panels remain breakable.','reason':'Attach participial agreement explanation to the actual forms.'},
 {'finding':'K17-P01','original_pages':[6,7],'change':'Keep P094–P096 together and remove the independent model reservation.','reason':'Prevent the imperative prompt from separating from its answer.'},
 {'finding':'K17-P02','original_pages':[44,45],'change':'Keep P543–P544 together.','reason':'Optional readability improvement for one short prompt and answer.'}]
report['v1_page_repairs_applied']=True
report['retained_v1_pdfs']={stem:{'path':(root/'build'/f'{stem}-v1.pdf').relative_to(root.parents[1]).as_posix(),
                                      'sha256':hashlib.sha256((root/'build'/f'{stem}-v1.pdf').read_bytes()).hexdigest()}
                            for stem in ['chapter-17','answer-key']}
report['linguistic_masters_changed']=False
report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Applied three attachment repairs and one optional short-answer grouping; preserved v1 PDFs and all accepted wording.')
