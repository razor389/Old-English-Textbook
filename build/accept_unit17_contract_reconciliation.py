"""Record the coordinator's completed pre-prose reconciliation, once."""
import hashlib
import json
from pathlib import Path

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def write(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')

assert not Path('chapters/ch17/student.md').exists()
assert not Path('chapters/ch17/answer-key.md').exists()
candidate = read('build/unit17-coverage-candidate.json')
check = read('build/unit17-check.json')
assert check['status'] == 'pass' and check['candidate'] and not check['errors']
manifest = read('sources/audits/unit17-source/manifest.json')
for entry in manifest['files']:
    assert hashlib.sha256(Path(entry['path']).read_bytes()).hexdigest() == entry['sha256'], entry['path']
validation = read('curriculum/proposals/unit17/validation.json')
assert validation['status'] == 'pass' and not validation['issues']
for path, digest in validation['input_hashes'].items():
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest, path

findings_path = 'sources/audits/unit17-coordinator/token-review-findings.json'
findings = read(findings_path)
tokens = {t['token_index']: t for t in candidate['source_spans'][0]['tokens']}
for finding in findings['findings']:
    for expected in finding['verified_positions']:
        actual = tokens[expected['position']]
        for key in ['surface', 'lemma_id', 'form_id', 'sense_id', 'contextual_role_and_meaning']:
            assert actual[key] == expected[key], (expected['position'], key)
        assert actual['sense_status'] == expected['sense_knowledge_status']
    finding['status'] = 'resolved_verified_in_final_contract_candidate'
findings['status'] = 'all_seven_repairs_verified_in_final_contract_candidate'
findings['canonical_join_verified'] = True
write(findings_path, findings)

path = 'sources/audits/unit17-coordinator/reconciliation.json'
report = read(path)
assert report['status'] == 'awaiting_complete_source_and_curriculum_packets'
report['status'] = 'accepted_for_contract'
report['accepted_date'] = '2026-10-28'
report['decisions'].extend([
    'Retain full-stem mægenes, mægene, mægena and mægenum, with the separately evidenced nominative/accusative plural mægnu. Preserve the withdrawn contraction proposal and its correction in the sealed source packet.',
    'Assign all four singular cases of abstract andgiet. Plural count/faculty senses are outside this assignment; this is no claim that the noun lacks plurals. The earlier complete neuter class remains the foundation.',
    'Explicitly teach the people senses of mihtig and ēaðmōd and the bounded personal-adjective frames of geong, eald, mihtig, ēaðmōd and rīce. An adjective table alone does not teach these uses.',
    'The permission verb gelīefst has its own supplied homonym identity; preserve the actual earlier belief records. Verify all seven reading-token repairs in the final contract join.',
    'Supply nīwne sang as one bounded phrase. Wright pages 49, 213 and 214 support quantity and the rule-derived masculine accusative; no claim of a separately attested nīwne token or inspected BT724 page is made.',
    'Carry all eleven source-proposal identity mappings into the contract. For 73 Cook positions distinguish independent choice of inflection from a supplied lexical meaning.'
])
report['final_metrics'] = candidate['explicit_scope_metrics']
report['verified_source_manifest_files'] = len(manifest['files'])
report['source_reports_read'] = [
    'sources/audits/unit17-source/source-report.md',
    'sources/audits/unit17-grammar/REPORT.md',
    'curriculum/proposals/unit17/REPORT.md'
]
report['pending_acceptance'] = []
report['remaining_gates'] = ['Checkpoint canonical contract before prose', 'Complete learner and separate key', 'Fresh blind solve and full paradigm review', 'Complete LuaLaTeX exports and every-page inspection', 'Preserved-register integration and final local checkpoint']
write(path, report)
print('Accepted final source/curriculum reconciliation and verified all seven token repairs in candidate.')
