"""Render selected registered primary pages; rendering is not inspection."""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = pathlib.Path(__file__).parent
GS = pathlib.Path('C:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs')
kind, *pages = sys.argv[1:]
pdf, offset = ('cook_ex_1895.pdf', 8) if kind == 'ex' else ('cook_fb_1895_2.pdf', 16)
for page in map(int, pages):
    subprocess.run([
        str(GS / 'bin/gswin64c.exe'), '-I' + ';'.join(str(GS / d) for d in ('Resource/Init', 'lib', 'kanji')),
        '-q', '-sDEVICE=png16m', '-r300', f'-dFirstPage={page + offset}',
        f'-dLastPage={page + offset}', '-dBATCH', '-dNOPAUSE',
        f'-sOutputFile={OUT.as_posix()}/{kind}-p{page}.png', str(ROOT / 'sources/cache' / pdf),
    ], check=True)
