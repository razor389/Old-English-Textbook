"""Keep the short C03 composition task with its model after page reinspection."""
import json,re,shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'answer-key.tex'
s=p.read_text(encoding='utf-8')
assert 'K17-P03' not in s
for source,target in [(root/'build/answer-key.pdf',root/'build/answer-key-v2.pdf'),(p,root/'build/answer-key-v2.tex')]:
    assert not target.exists()
    shutil.copyfile(source,target)
a=s.index('% mdparagraph:P125:begin')
end='% mdparagraph:P129:end'
b=s.index(end,a)+len(end)
body=re.sub(r'(?m)^\\reserve\{\d+\\baselineskip\}\n','',s[a:b])
s=s[:a]+'% page-review repair: K17-P03 complete short C03 composition\n'+r'\par\begin{minipage}{\linewidth}\raggedright'+'\n'+body+'\n'+r'\end{minipage}\par'+'\n'+s[b:]
p.write_text(s,encoding='utf-8',newline='\n')
p=root/'layout-adjustments.json'
d=json.loads(p.read_text(encoding='utf-8'))
d['adjustments'].append({'finding':'K17-P03','version':'key-v2','original_pages':[8,9],
    'change':'Keep P125–P129, the complete short C03 task, in one block and remove competing internal reservations.',
    'reason':'A reflow had stranded the C03 heading and task before its model.'})
d['v2_key_pdf_retained']='typesetting/ch17/build/answer-key-v2.pdf'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('K17-P03 repaired; v2 key PDF and TeX retained; accepted wording unchanged.')
