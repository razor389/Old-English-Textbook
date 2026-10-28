"""Record the coordinator's actual final precontract readback, without rewriting witnesses."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def write(p,d): (ROOT/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def ident(p): return {'path':p,'sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest()}

assert not (ROOT/'chapters/ch18/student.md').exists()
c=read('build/unit18-coverage-candidate.json')
assert read('build/unit18-check.json')['status']=='pass'
manifest=read('sources/audits/unit18-source/manifest.json')
for f in manifest['files']:
    raw=(ROOT/f['path']).read_bytes()
    assert len(raw)==f['size_bytes'] and hashlib.sha256(raw).hexdigest()==f['sha256'],f['path']
assert len(manifest['files'])==96
reading=c['source_spans'][0]
assert reading['tokens'][224]['form_id']=='ic-acc-pl'
assert reading['tokens'][224]['analysis']['case']=='accusative'
assert reading['tokens'][5]['sense_id']=='geseon-u16-content'
assert reading['tokens'][5]['sense_status']=='supplied'
fpath='sources/audits/unit18-coordinator/token-review-findings.json'
f=read(fpath)
f['status']='resolved_and_verified_in_final_candidate'
f['findings'][0]['status']='resolved'
f['findings'][0]['verified_final_route']=reading['tokens'][224]
f['findings'][0]['resolution_check']='Final candidate contains the actual prior accusative identity, accusative contextual role and both visible whole-frame routes; strict dependency checker passes. No earlier artifact or register was changed.'
write(fpath,f)
r=read('sources/audits/unit18-coordinator/reconciliation.json')
r['status']='accepted_for_contract'
r['open_source_queries']=[]
r['decisions']=[
    'Assign all47 exact joint XII, XIII Exercises44–48 in their complete8/9/9/11/10 sets, including all154 original aids and controls with45 numeric explanations. Earlier597 assignments remain unchanged: final canonical total644, zero deferred or excluded.',
    'Assign only the exact connected226-word Apollonius love, gifts and farewell episode175.18–177.2, with26 physical lines,22 notes and29 anchors. Joseph is English composition; neither an OE Joseph reading nor Apollonius as Teacher is assigned.',
    'Accept the stable v10 models after direct prompt/meaning readback of all47 items and final amendments. The v9 conditional būtan spelling and v10 feminine dative ēowerre join their separately scoped local explanations. Preserve every earlier witness and withdrawn hypothesis.',
    'Accept55 defined inflectional systems,652 literal cells in64 matrices, including26 nominal/adjectival systems470cells and29 bounded verbal systems182cells. Complete named scopes, stem rules and exceptions accompany display; references and supplied cells do not grant unassigned senses or syntax.',
    'Accept60 tasks with87 answers:47 Cook compositions and13 original groups40 outputs. The form work has10 completeOE sentence outputs and3 explanatory answers, with no isolated-cell drill. Two translated examples precede tasks; no new connected narrative is composed.',
    'Preserve source lęcgeað and ðēowa manna. The initial transcription errors are ours, not Cook errata. Reconstructed pre-correction semantic witnesses are accurately labelled and match the coordinator earlier capture; no raw-original-byte claim is made.',
    'Supply the whole servant phrases. BT1053 supports the noun; BT1054 actually prints the adjective with r. Strong-noun/appositional interpretation of the r-less source remains bounded inference, not an independently tested unique historical classification.',
    'Preserve Unit4 findan third-singular funde as valid under its explicit exception and primary evidence. The preliminary contrary finding is withdrawn; no earlier correction or register rewrite is warranted.',
    'Reading225ūs uses actual prior ic-acc-pl, matching Cook177note2 and184b; its previous dative audit witness is retained. Reading6geseah uses supplied content-clause sense geseon-u16-content, distinct from ordinary visual-object seeing.',
    'Crawford1922 is registered as supporting corroboration only, with exact title/edition/cache identity and bounded printed/PDF mapping. Proper-name support, second-time instrumental, æcernu and substitution evidence have specific locators; no inference that this was Cook’s edition is made.',
    'All supplied output dependencies have visible local support; actual prior senses and analyses remain immutable, with contextual parses separate. Root read all226 token roles, the complete verbal/nominal systems, original tasks and final response contracts in addition to primary images.',
    'Current source, grammar, design and coordinator work is author preparation. A fresh reviewer must solve all87 actual outputs before current key/contract/audit/model access, with solutions frozen unchanged in Git; a separate fresh reviewer verifies all652 paradigm cells. Complete exports and actual non-author inspection of every final page remain mandatory.'
]
r['accepted_metrics']=c['contract_metrics']
r['final_inventory_metrics']={k:c.get(k) for k in ['record_counts_by_scope','record_identity_counts']}
r['accepted_reports']=[ident(p) for p in [
    'sources/audits/unit18-source/source-gate-report.json',
    'sources/audits/unit18-source/query-resolutions.json',
    'sources/audits/unit18-source/manifest.json',
    'sources/audits/unit18-grammar/grammar-report.md',
    'sources/audits/unit18-grammar/packet-validation.json',
    'curriculum/proposals/unit18/REPORT.md',
    'curriculum/proposals/unit18/validation.json']]
r['source_manifest_check']={'files_checked':96,'result':'all exact sizes and hashes match'}
r['strict_candidate_check']={'path':'build/unit18-check.json','result':'pass; all dependencies, source controls, display routes, evidence and prior artifact checks'}
r['remaining_gates']=['canonical contract committed before prose','complete learner and separate key','fresh blind solving and complete independent paradigm review','material findings resolved','complete LuaLaTeX exports and all-page non-author inspection','preserving register merge and final indexes','Beads export and local Git checkpoint']
r['next_gate']='Write and commit canonical coverage.json; only then authorize learner and key prose.'
write('sources/audits/unit18-coordinator/reconciliation.json',r)
print('Final precontract reconciliation accepted;96 source manifest identities verified;225 accusative and6 supplied content sense verified.')
