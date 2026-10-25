"""Seal reconciled design inputs after all concrete checks, without shared writes."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[4];OUT=ROOT/'curriculum/proposals/unit12'
def load(name):return json.loads((OUT/name).read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
v=load('validation.json');inv=load('inventory.json')
assert not v['errors'] and not v['unresolved'],v
assert inv['status']=='reconciled_pre_contract_design'
assert v['counts']['tasks']==76 and v['counts']['cook_tasks']==38
artifacts=[p for p in OUT.glob('*.json') if p.name!='manifest.json']+list(OUT.glob('*.md'))+list((OUT/'build').glob('*.py'))
files={str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in sorted(artifacts)}
manifest={'schema_version':1,'chapter':'ch12','status':'reconciled_pre_contract_design','prior_baseline_checkpoint':'74da7bb','counts':v['counts'],'files':files,'analysis_inputs':inv['analysis_input_hashes'],'pre_key_review_exclusions':inv['pre_key_review_exclusions'],'checks':['All38 exact Cook prompts retained with original group/exercise/item identifiers.','All76 task IDs have one private model and stable key ID.','Every public and expected-output lexical token has an explicit checked form/sense binding; punctuation has no invented lexical identity.','All required forms, senses and features resolve against actual prior records or independently audited Unit12 records.','Independent production requires productive records; supplied source aids remain visible.','All paradigm cells have exactly one literal or explicit diagnostic display route.','Public composition and complete source translations were independently construed before key comparison.','No shared register or chapter contract was written by the designer.'],'remaining_gates':['Coordinator checkpoint of reconciled coverage contract before prose.','Learner and separate key masters.','Reserved reviewer independently solves actual learner tasks before opening private key material.','Resolve material review findings, complete LuaLaTeX exports and page inspection, register/status integration and local Git checkpoint.']}
manifest['reviewer_exposure']=inv['reviewer_exposure']
manifest['remaining_gates'][2]='Reserved reviewer independently solves75 unexposed tasks. A fresh unexposed reviewer solves EX-VI-21-04; both witnesses are frozen before corresponding private key access.'
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'sealed_files':len(files),'counts':v['counts']},ensure_ascii=False))
