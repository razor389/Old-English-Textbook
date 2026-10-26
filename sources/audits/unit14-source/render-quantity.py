from pathlib import Path
import subprocess
root=Path(__file__).resolve().parent
gs=Path('C:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs')
for p in [283,296]:
    dest=root/f'cook-fb-p{p}-quantity.png'
    subprocess.run([str(gs/'bin/gswin64c.exe'),'-I'+';'.join(str(gs/d) for d in ('Resource/Init','lib','kanji')),'-sDEVICE=png16m','-r400',f'-dFirstPage={p+16}',f'-dLastPage={p+16}','-dBATCH','-dNOPAUSE',f'-sOutputFile={dest}','sources/cache/cook_fb_1895_2.pdf'],check=True,stdout=subprocess.DEVNULL)
