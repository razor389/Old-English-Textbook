"""Reproducible page renders for the Unit16 source audit."""
import pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[3]; OUT=pathlib.Path(__file__).parent
GS=pathlib.Path('C:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs')
kind=sys.argv[1]; pages=[int(x) for x in sys.argv[2:]]
for p in pages:
    pdf='cook_ex_1895.pdf' if kind=='ex' else 'cook_fb_1895_2.pdf'
    offset=8 if kind=='ex' else 16
    dpi=600 if kind.startswith('close-') else 300
    if kind=='close-ex': pdf='cook_ex_1895.pdf'; offset=8
    if kind=='wright': pdf='wright_oe_1914.pdf'; offset=20
    subprocess.run([str(GS/'bin/gswin64c.exe'),'-I'+';'.join(str(GS/d) for d in ('Resource/Init','lib','kanji')),'-q','-sDEVICE=png16m',f'-r{dpi}',f'-dFirstPage={p+offset}',f'-dLastPage={p+offset}','-dBATCH','-dNOPAUSE',f'-sOutputFile={OUT.as_posix()}/{kind}-p{p}.png',str(ROOT/'sources/cache'/pdf)],check=True)
