"""Render the bounded primary pages used by the nominal/source audit."""
from pathlib import Path
import subprocess

OUT = Path(__file__).resolve().parent
GS = Path('C:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs')
PAGES = [314,315,38,285,305,321,27,28,29,31,32,33,34,35,36,37,273,274,276,280,281,283,287,289,296,297,298,299,303,306,308,312,313,317,318,320,322,323,324]
for p in PAGES:
    dest = OUT / f'cook-fb-p{p}.png'
    if dest.exists():
        continue
    args = [str(GS/'bin/gswin64c.exe'), '-I'+';'.join(str(GS/d) for d in ('Resource/Init','lib','kanji')), '-sDEVICE=png16m', '-r180', f'-dFirstPage={p+16}', f'-dLastPage={p+16}', '-dBATCH', '-dNOPAUSE', f'-sOutputFile={dest}', 'sources/cache/cook_fb_1895_2.pdf']
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(p, flush=True)
for p in [53,54,58]:
    dest = OUT / f'cook-ex-p{p}.png'
    if dest.exists():
        continue
    args = [str(GS/'bin/gswin64c.exe'), '-I'+';'.join(str(GS/d) for d in ('Resource/Init','lib','kanji')), '-sDEVICE=png16m', '-r200', f'-dFirstPage={p+8}', f'-dLastPage={p+8}', '-dBATCH', '-dNOPAUSE', f'-sOutputFile={dest}', 'sources/cache/cook_ex_1895.pdf']
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('EX',p, flush=True)
