from pathlib import Path
import subprocess
scripts=['inventory','choices','local-join','cook-binding-join','reading-join','forms','task-plan','feature-map','hint-inputs','hint-close','final-task-join','final-metadata','validate']
for name in scripts:
 p=Path('build/u18-design-'+name+'.py')
 print('\nRUN '+p.name,flush=True)
 r=subprocess.run(['python','-X','utf8',str(p)],capture_output=True,text=True,encoding='utf8')
 print(r.stdout[-9000:],end='',flush=True)
 if r.stderr:print(r.stderr[-6000:],flush=True)
 if r.returncode:raise SystemExit(r.returncode)
