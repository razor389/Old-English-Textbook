"""Retain review boundaries and recoverable design helpers after validation."""
from pathlib import Path
import hashlib,json,shutil
R=Path.cwd();O=R/'curriculum/proposals/unit13'
def load(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def save(n,d):(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
V=load('curriculum/proposals/unit13/validation.json')
if V['status']!='pass':raise SystemExit('Do not seal a design with unresolved validation issues.')
helpers=O/'helpers';helpers.mkdir(exist_ok=True)
for p in (R/'build').glob('unit13-design-*.py'):
    shutil.copyfile(p,helpers/p.name)
for name in ['composition-seed.json','task-seed.json','cook-targets.json','file-boundaries.json']:
    d=load('curriculum/proposals/unit13/'+name);d['status']='ready_for_coordinator_contract_reconciliation';save(name,d)
for name in ['nominal-display-plan.json','grammar-display-plan.json','display-matrices.json']:
    d=load('curriculum/proposals/unit13/'+name);d['status']='independently_checked_complete_routes';save(name,d)
d=load('curriculum/proposals/unit13/author-only-model-seed.json');d['status']='audited_private_design_seeds_before_contract_and_fresh_review';save('author-only-model-seed.json',d)
exclusions=sorted({str(p.relative_to(R)).replace('\\','/') for folder in ['curriculum/proposals/unit13','sources/audits/unit13-source','sources/audits/unit13-grammar','sources/audits/unit13-coordinator'] for p in (R/folder).rglob('*') if p.is_file() and p.suffix in ['.json','.md','.py']}|{'curriculum/UNIT_13_BRIEF.md','chapters/ch13/coverage.json','chapters/ch13/answer-key.md','sources/audits/unit13-coordinator/author-only-source-first.md','curriculum/proposals/unit13/manifest.json'})
exclusions=sorted(set(exclusions)|{str(p.relative_to(R)).replace('\\','/') for p in (R/'build').glob('unit13-design-*.py')})
I=load('curriculum/proposals/unit13/inventory.json');I['pre_key_review_exclusions']=exclusions
for path in I['analysis_input_hashes']:
    if path.startswith('curriculum/proposals/unit13/') and (R/path).exists():I['analysis_input_hashes'][path]=hashlib.sha256((R/path).read_bytes()).hexdigest()
save('inventory.json',I)
B=load('curriculum/proposals/unit13/file-boundaries.json');B['explicit_pre_key_review_exclusions']=exclusions;B['recoverable_helpers']='helpers/ contains the actual design scripts; every helper is excluded during blind solving because some contain or derive ordered models.';save('file-boundaries.json',B)
files=[]
for p in sorted(O.rglob('*')):
    if not p.is_file() or p.name=='manifest.json':continue
    files.append(dict(path=str(p.relative_to(R)).replace('\\','/'),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size,role='author_only' if p.name.startswith('author-only-') else 'design_helper_excluded_before_frozen_solutions' if p.suffix=='.py' else 'editorial_design_input_excluded_before_frozen_solutions'))
dependencies=[]
for folder in ['sources/audits/unit13-source','sources/audits/unit13-grammar']:
    for p in sorted((R/folder).glob('*.json')):
        dependencies.append(dict(path=str(p.relative_to(R)).replace('\\','/'),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
manifest=dict(schema_version=1,chapter='ch13',status='design_complete_ready_for_coordinator_contract',owner='unit13_design',writing_boundary='curriculum/proposals/unit13/ and own ignored build helpers only; no registers, shared contract, prior unit, Beads or Git writes.',baseline_checkpoint='e17fc5f',counts=V['counts'],validation='curriculum/proposals/unit13/validation.json',files=files,source_and_grammar_dependencies=dependencies,pre_key_review_exclusions=exclusions,blind_solver_allowlist=['actual learner master after accepted contract','accepted earlier units and cumulative registers','necessary original page images'],gate='No learner or key master before the coordinator has reconciled and committed the learning contract. Later independent review remains separate from this design audit.',open_material_issues=[])
save('manifest.json',manifest)
print(json.dumps(dict(status=manifest['status'],files=len(files),source_and_grammar_dependencies=len(dependencies),pre_key_exclusions=len(exclusions),counts=V['counts'])))
