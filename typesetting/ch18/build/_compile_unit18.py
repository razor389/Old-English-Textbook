"""Compile accepted Unit18 text twice with the existing LuaLaTeX installation."""
import argparse,json,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parents[3]
out=root/'typesetting/ch18'
p=argparse.ArgumentParser();p.add_argument('--document',choices=['learner','key','both'],default='both');a=p.parse_args()
c=json.loads((root/'chapters/ch18/coverage.json').read_text(encoding='utf-8'))
assert c.get('textual_review',{}).get('status')=='accepted'
assert c.get('accepted_text_checkpoint')
for document,stem in [('learner','chapter-18'),('key','answer-key')]:
    if a.document not in ['both',document]:continue
    for run in [1,2]:
        r=subprocess.run(['lualatex','-interaction=nonstopmode','-halt-on-error','-output-directory=build',stem+'.tex'],cwd=out,capture_output=True,text=True,encoding='utf-8',errors='replace')
        (out/'build'/f'{stem}-pass{run}.stdout.txt').write_text(r.stdout+'\n'+r.stderr,encoding='utf-8')
        print(stem,'pass',run,'exit',r.returncode)
        if r.returncode:
            print('\n'.join((r.stdout+'\n'+r.stderr).splitlines()[-70:]));sys.exit(r.returncode)
    print(next((line for line in r.stdout.splitlines() if line.startswith('Output written on')),'Inspect compilation log for output details.'))
