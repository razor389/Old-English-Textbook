"""Render selected registered Cook pages for coordinator source inspection."""
import argparse
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('source', choices=['fb','ex'])
p.add_argument('pages', nargs='+', type=int)
p.add_argument('--dpi', type=int, default=300)
a = p.parse_args()
base = Path('sources/audits/unit16-coordinator')
base.mkdir(parents=True, exist_ok=True)
gs = Path('C:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs')
pdf = Path('sources/cache/cook_fb_1895_2.pdf' if a.source == 'fb' else 'sources/cache/cook_ex_1895.pdf').resolve()
offset = 16 if a.source == 'fb' else 8
for printed in a.pages:
    out = (base / f'cook-{a.source}-p{printed}-{a.dpi}.png').resolve()
    assert not out.exists(), f'Preserve existing render: {out}'
    subprocess.run([str(gs / 'bin/gswin64c.exe'), '-I' + ';'.join(str(gs / d) for d in ['Resource/Init','lib','kanji']),
        '-sDEVICE=png16m', '-r'+str(a.dpi), '-dTextAlphaBits=4', '-dGraphicsAlphaBits=4',
        '-dBATCH','-dNOPAUSE','-dFirstPage='+str(printed+offset),'-dLastPage='+str(printed+offset),
        '-sOutputFile='+str(out),str(pdf)],check=True,stdout=subprocess.DEVNULL)
    print(out.relative_to(Path.cwd()), 'rendered; not yet inspected')
