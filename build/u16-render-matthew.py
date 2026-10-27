"""Render precise original Matthew pages; output alone is not inspection."""
from pathlib import Path
import subprocess
root=Path(__file__).resolve().parents[1]
gs=Path('C:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs')
for pdfpage,name in [(9,'title'),(5,'preface-piii'),(124,'p114')]:
    dest=root/'sources/audits/unit16-coordinator'/('matthew-'+name+'-300.png')
    assert not dest.exists(), 'Preserve existing source render'
    subprocess.run([str(gs/'bin/gswin64c.exe'),'-I'+';'.join(str(gs/d) for d in ['Resource/Init','lib','kanji']),
        '-sDEVICE=png16m','-r300','-dTextAlphaBits=4','-dGraphicsAlphaBits=4','-dBATCH','-dNOPAUSE',
        '-dFirstPage='+str(pdfpage),'-dLastPage='+str(pdfpage),'-sOutputFile='+str(dest),
        str(root/'sources/cache/matthew_kemble_hardwick_1858.pdf')],check=True,stdout=subprocess.DEVNULL)
    print(dest.relative_to(root).as_posix(),'rendered; not yet inspected')
