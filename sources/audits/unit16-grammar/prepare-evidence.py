"""Render selected primary pages; OCR locates but does not verify forms."""
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
GS=Path('C:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs')
groups=[('ex','cook_ex_1895.pdf',8,[38,40,42,43,44,49,54,56,57,59,60,63,65,66]),('fb','cook_fb_1895_2.pdf',16,[50,51,59,61,64,65,66,67,68,69,70,71,72,73,74,75,76,79,96,97,167,279,280,282,284,288,290,292,294,295,296,300,301,306,309,313,323])]
for prefix,pdf,offset,pages in groups:
    for page in pages:
        dest=OUT/f'{prefix}-p{page}.png'
        if dest.exists(): continue
        matches=list((ROOT/'sources/audits').glob(f'unit*/{prefix}-p{page}.png'))
        matches=[p for p in matches if p.parent!=OUT]
        if matches:
            print('reuse',page,matches[-1].relative_to(ROOT)); continue
        subprocess.run([str(GS/'bin/gswin64c.exe'),'-I'+';'.join(str(GS/d) for d in ('Resource/Init','lib','kanji')),'-q','-sDEVICE=png16m','-r160',f'-dFirstPage={page+offset}',f'-dLastPage={page+offset}','-dBATCH','-dNOPAUSE',f'-sOutputFile={dest}',str(ROOT/'sources/cache'/pdf)],check=True,stdout=subprocess.DEVNULL)
        print('rendered',prefix,page)
