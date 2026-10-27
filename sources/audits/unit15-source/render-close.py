import pathlib,subprocess
R=pathlib.Path(__file__).resolve().parents[3];P=pathlib.Path(__file__).parent
G=pathlib.Path('C:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs')
for n in [159,162,163]:
 subprocess.run([str(G/'bin/gswin64c.exe'),'-I'+';'.join(str(G/d) for d in ('Resource/Init','lib','kanji')),'-q','-sDEVICE=png16m','-r400','-dBATCH','-dNOPAUSE',f'-dFirstPage={n+16}',f'-dLastPage={n+16}',f'-sOutputFile={(P/f"reader-p{n}-400.png").as_posix()}',str(R/'sources/cache/cook_fb_1895_2.pdf')],check=True)
