"""Render selected primary pages for independent visual inspection."""
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parent
GS=Path('C:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs')
for page in range(29,34):
    dest=OUT/f'ex-p{page}.png'
    if not dest.exists():
        subprocess.run([str(GS/'bin/gswin64c.exe'),'-I'+';'.join(str(GS/d) for d in ('Resource/Init','lib','kanji')),'-q','-sDEVICE=png16m','-r180',f'-dFirstPage={page+8}',f'-dLastPage={page+8}','-dBATCH','-dNOPAUSE',f'-sOutputFile={dest}',str(ROOT/'sources/cache/cook_ex_1895.pdf')],check=True,stdout=subprocess.DEVNULL)
    print(dest.relative_to(ROOT))
