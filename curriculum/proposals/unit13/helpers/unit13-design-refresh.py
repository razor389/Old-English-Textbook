"""Rebuild the bounded design from the frozen baseline and checked audits."""
from pathlib import Path
import hashlib,json,subprocess,sys
base=Path(__file__).resolve().parent
prior=json.loads(Path('curriculum/proposals/unit13/prior-audit.json').read_text(encoding='utf-8'))
for entry in prior['registers']:
    if hashlib.sha256(Path(entry['path']).read_bytes()).hexdigest()!=entry['sha256']:
        raise SystemExit('Restore the accepted pre-Unit-13 baseline in an isolated checkout before rebuilding this historical proposal.')
names=['seed','nominal-display','grammar-display','bind','bind-cook','private-seed','cook-targets','prior-audit','assemble','validate','manifest']
for name in names:
    subprocess.run([sys.executable,'-X','utf8',str(base/('unit13-design-'+name+'.py'))],check=True)
