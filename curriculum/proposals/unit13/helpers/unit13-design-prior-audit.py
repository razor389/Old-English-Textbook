"""Read the complete actual twelve-unit baseline; certify identity, not truth."""
from pathlib import Path
import json,hashlib
R=Path.cwd();O=R/'curriculum/proposals/unit13'
def load(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
baseline=load('build/unit13-prior-baseline.json');lex=load('lexicon/entries.json');grammar=load('curriculum/grammar.json')
assert lex==baseline['lexicon'] and grammar==baseline['grammar']
contracts=[]
for i in range(1,13):
    path=f'chapters/ch{i:02}/coverage.json';c=load(path)
    contracts.append(dict(chapter_id=c.get('chapter_id',f'ch{i:02}'),path=path,sha256=sha(path),status=c['status'],title=c.get('title'),productive_outcomes=c.get('productive_outcomes',[]),recognition_outcomes=c.get('recognition_outcomes',[]),bounded_scope=c.get('bounded_scope',[]),assigned_item_count=len(c.get('assigned_items',[])),logical_paradigm_count=len(c.get('paradigms',[])),amendment_ids=[a.get('amendment_id',a.get('id',a.get('finding'))) for a in c.get('amendments',[])]))
forms=[f for l in lex['lemmas'] for f in l.get('forms',[])];senses=[s for l in lex['lemmas'] for s in l.get('senses',[])]
counts=dict(lemmas=len(lex['lemmas']),forms=len(forms),senses=len(senses),features=len(grammar['features']))
assert counts==dict(lemmas=647,forms=8235,senses=778,features=599)
for records,key in [(lex['lemmas'],'lemma_id'),(forms,'form_id'),(senses,'sense_id'),(grammar['features'],'feature_id')]:assert len(records)==len({r[key] for r in records})
report=dict(schema_version=1,chapter='ch13',baseline_checkpoint=baseline['git_checkpoint'],baseline_full_checkpoint=baseline['git_checkpoint_full'],baseline_capture='build/unit13-prior-baseline.json',retained_baseline_record='sources/audits/unit13-coordinator/prior-state.json',status='complete_actual_files_parsed_and_needed_records_individually_inspected',counts=counts,registers=[dict(path=p,sha256=sha(p),matches_frozen_actual_baseline=True) for p in ['lexicon/entries.json','curriculum/grammar.json']],earlier_contracts=contracts,read_scope='All twelve actual coverage JSON files and both full cumulative registers were parsed. The educational scopes and amendments were inspected; every identity used in the proposed unit is looked up individually and carried into inventory.prior_requirements with actual current record and task usage. This checks prerequisite identity and recorded scope, not a new linguistic certification of all earlier teaching.',boundaries=['','A familiar headword supplies only its actual recorded forms and senses.','Table display alone does not establish syntactic use.','Earlier supplied or recognition records require explicit current scope and local support before new tasks can use them.','Existing form surfaces, analyses, senses, histories and IDs are preserved; refined current context is separate.','Known limitations include modal gaps, reference-only plurals and instrumentals, individual passive/participle scopes and reading-only variants.'])
(O/'prior-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(counts))
