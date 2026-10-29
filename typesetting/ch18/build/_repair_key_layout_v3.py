"""Resolve the newly observed C-section orphan while retaining v2 witnesses."""
import hashlib,json,re,shutil
from pathlib import Path
out=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['answer-key.tex','build/answer-key.pdf']:
    source=out/name;suffix=source.suffix;target=out/'build'/('answer-key-v2'+suffix)
    assert not target.exists();shutil.copyfile(source,target)
p=out/'answer-key.tex';text=p.read_text(encoding='utf-8');before=sha(p)
pattern=r'\\reserve\{7\\baselineskip\}(\n% mdparagraph:(P\d+):begin\n\\section\*\{C\. Composition\})'
matches=list(re.finditer(pattern,text));assert len(matches)==1
pid=matches[0][2];text=re.sub(pattern,lambda m:'\\clearpage'+m[1],text)
p.write_text(text,encoding='utf-8',newline='\n')
rpath=out/'layout-adjustments.json';r=json.loads(rpath.read_text(encoding='utf-8'))
r['versions'].append({'version':'v2','render_manifest':'typesetting/ch18/build/render-manifest-v2.json','retained_key_pdf':'typesetting/ch18/build/answer-key-v2.pdf','retained_key_pdf_sha256':sha(out/'build/answer-key-v2.pdf'),'retained_key_tex':'typesetting/ch18/build/answer-key-v2.tex','retained_key_tex_sha256':sha(out/'build/answer-key-v2.tex')})
r['repairs'].append({'repair_id':'U18-LAYOUT-03','reported_by':'u18_pages_key','finding_id':'K03','observed_v2_page':3,'change':'Start C. Composition on the page with C01 after reflow exposed a new heading orphan. F retains its existing explicit boundary.','tex_paragraph':pid,'tex_sha256_before':before,'tex_sha256_after':sha(p)})
rpath.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('C heading now begins with its tasks; v2 PDF/TeX and raster witnesses retained.')
