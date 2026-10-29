"""Repair observed key heading/prompt breaks; preserve accepted linguistic content."""
import hashlib,json,re
from pathlib import Path
root=Path(__file__).resolve().parents[3];out=root/'typesetting/ch18'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((out/'build/render-manifest-v1.json').read_text(encoding='utf-8'))
path=out/'answer-key.tex';old=path.read_text(encoding='utf-8');before=sha(path)
assert r'\section*{F. Forms and grammatical roles}' in old
old_heading='\\reserve{7\\baselineskip}\n% mdparagraph:P054:begin\n\\section*{F. Forms and grammatical roles}'
new_heading='\\clearpage\n% mdparagraph:P054:begin\n\\section*{F. Forms and grammatical roles}'
assert old.count(old_heading)==1
text=old.replace(old_heading,new_heading)
pattern=re.compile(r'(% mdparagraph:(P\d+):begin\n\\textbf\{[^\n]*\}\n% mdparagraph:\2:end)\n\n\\reserve\{5\\baselineskip\}\n(% mdparagraph:(P\d+):begin\n\\textbf\{[^\n]*\}\n% mdparagraph:\4:end)')
pairs=[]
def keep(m):
    pairs.append([m[2],m[4]])
    return '\\par\\begin{minipage}{\\linewidth}\\raggedright\n'+m[1]+'\n\n'+m[3]+'\n\\end{minipage}\\par'
text=pattern.sub(keep,text)
assert ['P024','P025'] in pairs and ['P086','P087'] in pairs,pairs
path.write_text(text,encoding='utf-8',newline='\n')
record={'chapter_id':'ch18','status':'repairs_awaiting_non_author_reinspection','linguistic_masters_changed':False,'versions':[{'version':'v1','render_manifest':'typesetting/ch18/build/render-manifest-v1.json','page_totals':{k:d['pages'] for k,d in manifest['documents'].items()},'review_witness':'typesetting/ch18/build/u18-pages-key-v1-review.json'}],'repairs':[{'repair_id':'U18-LAYOUT-01','reported_by':'u18_pages_key','finding_id':'K01','observed_v1_page':4,'change':'Start the F section on a new page so its heading remains with the first task.','tex_paragraph':'P054'},{'repair_id':'U18-LAYOUT-02','reported_by':'u18_pages_key','finding_id':'K02','observed_v1_pages':[2,6],'change':'Keep each adjacent short bold prompt/model pair in a single small minipage; allow its explanation to continue naturally.','paragraph_pairs':pairs}],'tex_identity_before':before,'tex_identity_after':sha(path),'scope':'Presentation only. All accepted paragraphs, cells, comments and characters require renewed full parity; every changed final page requires actual non-author inspection.'}
(out/'layout-adjustments.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
# Correct a descriptive report sentence: this unit has a continuous ordinary
# reading paragraph; neither the accepted master nor its PDF is changed here.
p=out/'build/_check_content_parity.py';s=p.read_text(encoding='utf-8')
before_description='The complete source scene uses the reading style with natural paragraph/page breaks; two short examples stay with their translations.'
after_description='The complete source scene is retained as continuous text with natural paragraph/page breaks; two short examples stay with their translations.'
assert s.count(before_description)==1
p.write_text(s.replace(before_description,after_description),encoding='utf-8',newline='\n')
print('Kept',len(pairs),'short prompt/model pairs; F section begins with its content. Linguistic masters unchanged.')
