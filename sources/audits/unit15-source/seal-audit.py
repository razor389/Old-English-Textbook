import json,pathlib,hashlib
P=pathlib.Path(__file__).parent;R=P.resolve().parents[2]
files=[]
for p in sorted(P.iterdir()):
 if not p.is_file() or p.name=='artifact-manifest.json':continue
 role='primary_page_image' if p.suffix.lower() in ['.png','.jpg'] else 'bounded_audit_helper' if p.suffix=='.py' else 'author_only_private_model' if p.name.startswith('author-only-') else 'finding_aid_not_final_binding' if p.name=='reading-token-candidates.json' or p.suffix=='.html' else 'source_audit_artifact'
 files.append(dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),role=role))
out=dict(schema_version=1,status='source_audit_complete_for_contract_integration',baseline_checkpoint='9129cda',inspection_agent='unit15_source',date='2026-10-26',validation='sources/audits/unit15-source/validation.json',file_count=len(files),files=files,coordination_dependencies=['Final Cook ordered models are owned by unit15_grammar; final task binding by unit15_design.'],resolved_reconciliation='Full strengu recognition class reference, prior wītga/bisceop reuse, genitive hǣlu with unnan and ordinary reader IDs/senses reconciled against the published grammar inventories.',exclusions=['Manifest excludes its own hash. No learner chapter or active-register completion is asserted.'])
(P/'artifact-manifest.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(dict(files=len(files),status=out['status']))
