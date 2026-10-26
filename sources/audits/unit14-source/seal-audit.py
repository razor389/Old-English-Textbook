import hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[2]
def role(p):
 if p.name.startswith('author-only-'):return 'author_only_private_model_or_witness'
 if p.suffix in ['.png','.jpg']:return 'unused_finder_render' if p.name=='cook-ex-p54.png' else 'primary_page_image'
 if p.suffix=='.html':return 'finding_aid_only'
 if p.suffix=='.py':return 'bounded_audit_helper'
 return 'source_audit_artifact'
files=[p for p in sorted(P.iterdir()) if p.is_file() and p.name!='artifact-manifest.json']
records=[{'path':p.relative_to(R).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'role':role(p)} for p in files]
obj={'schema_version':1,'status':'source_audit_complete_for_contract_integration','baseline_checkpoint':'c2cb7d6','inspection_agent':'unit14_source','date':'2026-10-26','validation':'sources/audits/unit14-source/validation.json','file_count':len(records),'files':records,'exclusions':['This manifest excludes its own hash. No claim is made that the learner chapter is complete.']}
(P/'artifact-manifest.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print({'files':len(records),'bytes':sum(r['bytes'] for r in records)})
