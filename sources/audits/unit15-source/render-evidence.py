import pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[3]
GS=pathlib.Path('C:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs')
prefix=[str(GS/'bin/gswin64c.exe'),'-I'+';'.join(str(GS/d) for d in ('Resource/Init','lib','kanji')),'-q','-sDEVICE=png16m','-r200','-dBATCH','-dNOPAUSE']
source=sys.argv[1];offset=16 if source=='fb' else 8;pdf='cook_fb_1895_2.pdf' if source=='fb' else 'cook_ex_1895.pdf'
for p in map(int,sys.argv[2:]):
 dest=ROOT/f'build/u15-source-{source}-p{p}.png'
 if not dest.exists():subprocess.run(prefix+[f'-dFirstPage={p+offset}',f'-dLastPage={p+offset}',f'-sOutputFile={dest.as_posix()}',str(ROOT/'sources/cache'/pdf)],check=True)
 print(dest.relative_to(ROOT).as_posix())
