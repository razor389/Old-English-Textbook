"""One-use deep preservation audit; --final records actual reviewed integration."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def lfsha(path):
    return hashlib.sha256(Path(path).read_bytes().replace(b'\r\n', b'\n')).hexdigest()

def flat(register, kind):
    return {r[kind[:-1] + '_id']: r for l in register['lemmas'] for r in l[kind]}

p = argparse.ArgumentParser()
p.add_argument('--final', action='store_true')
args = p.parse_args()
b = read('build/unit17-prior-baseline.json')
assert len(b['files']) == 2935
c = read('chapters/ch17/coverage.json')
lex = read('lexicon/entries.json' if args.final else 'build/unit17-lexicon-merged.json')
gram = read('curriculum/grammar.json' if args.final else 'build/unit17-grammar-merged.json')
proposed = {'forms': {f['form_id']: f for l in c['lexical_inventory'] for f in l['forms']},
            'senses': {s['sense_id']: s for l in c['lexical_inventory'] for s in l['senses']},
            'features': {f['feature_id']: f for f in c['grammar_inventory']}}
reused = read('build/unit17-register-metrics.json')['reused_supplied_records']
preserved = {}
promotions = {}
for kind, before, after in [
    ('forms', flat(b['lexicon'], 'forms'), flat(lex, 'forms')),
    ('senses', flat(b['lexicon'], 'senses'), flat(lex, 'senses')),
    ('features', {r['feature_id']: r for r in b['grammar']['features']},
     {r['feature_id']: r for r in gram['features']})]:
    assert set(before) <= set(after)
    promotions[kind] = []
    for rid, old in before.items():
        new = after[rid]
        if rid not in proposed[kind] and rid not in reused[kind[:-1]]:
            assert new == old, ('unassigned record changed', rid)
            continue
        for chapter, record in old.get('records_by_chapter', {}).items():
            assert new['records_by_chapter'][chapter] == record, (rid, chapter)
        for milestone in ['recognition_taught_in', 'production_taught_in']:
            if old.get(milestone):
                assert new[milestone] == old[milestone], (rid, milestone)
        for field in ['supplied_in', 'evidence_refs', 'teaching_ids', 'used_in_tasks', 'assessed_in', 'reviewed_chapters']:
            assert set(old.get(field, [])) <= set(new.get(field, [])), (rid, field)
        if kind == 'forms':
            assert old['form'] == new['form'], (rid, 'surface')
            assert old.get('analysis') == new.get('analysis'), (rid, 'earlier analysis')
        if not old.get('production_taught_in') and new.get('production_taught_in') == 'ch17':
            promotions[kind].append(rid)
    for rid, proposal in proposed[kind].items():
        assert after[rid]['records_by_chapter']['ch17'] == proposal, (rid, 'new record')
        if proposal['knowledge_status'] == 'supplied':
            assert after[rid].get('production_taught_in') != 'ch17', (rid, 'supplied became productive')
    for rid, tasks in reused[kind[:-1]].items():
        rec=after[rid]['records_by_chapter']['ch17']
        assert rec['knowledge_status']=='supplied' and set(tasks)<=set(rec['used_in_tasks']),rid
        assert 'ch17' in after[rid]['supplied_in'],rid
        assert not after[rid].get('production_taught_in') and not after[rid].get('recognition_taught_in'),rid
    preserved[kind] = len(before)
old_lemmas = {l['lemma_id']: l for l in b['lexicon']['lemmas']}
new_lemmas = {l['lemma_id']: l for l in lex['lemmas']}
changed_metadata = []
for lid, old in old_lemmas.items():
    new = new_lemmas[lid]
    for chapter, metadata in old.get('metadata_by_chapter', {}).items():
        assert new['metadata_by_chapter'][chapter] == metadata, (lid, chapter, 'metadata history')
    old_meta = {k: v for k, v in old.items() if k not in ['forms', 'senses', 'metadata_by_chapter']}
    new_meta = {k: v for k, v in new.items() if k not in ['forms', 'senses', 'metadata_by_chapter']}
    if old_meta != new_meta:
        assert new['metadata_by_chapter']['through_ch16'] == old_meta, lid
        changed_metadata.append(lid)
for name, before, after in [('lexicon', b['lexicon'], lex), ('grammar', b['grammar'], gram)]:
    assert after['reviewed_chapters'] == before['reviewed_chapters'] + ['ch17'], name
    for eid, evidence in before['evidence_catalog'].items():
        assert after['evidence_catalog'][eid] == evidence, (name, eid)
    for chapter, contract in before['source_contracts'].items():
        assert after['source_contracts'][chapter] == contract, (name, chapter)
prior_paths = [p for p in b['files'] if p not in ['lexicon/entries.json', 'curriculum/grammar.json']]
for path in prior_paths:
    assert sha(path) == b['files'][path] or lfsha(path) == b['files_lf_sha256'][path], path
for path, digest in b['archive_files'].items():
    assert sha(path) == digest, path
report = {
    'chapter_id': 'ch17', 'status': 'accepted' if args.final else 'dry_run_pass',
    'baseline_checkpoint': b['git_checkpoint_full'],
    'method': 'Deep comparison against the immutable sixteen-unit baseline: every unassigned record unchanged, every old per-chapter record and earliest milestone preserved, evidence and source contracts preserved, existing surfaces identical, metadata history retained, new records equal accepted coverage.',
    'metrics': read('build/unit17-register-metrics.json'),
    'earlier_records_preserved': preserved,
    'explicit_prior_promotions': promotions,
    'prior_metadata_retained_for_changed_lemmas': changed_metadata,
    'prior_active_files_preserved': len(prior_paths),
    'archived_files_preserved': len(b['archive_files']),
    'all_earlier_records_by_chapter_preserved': True,
    'all_unassigned_records_unchanged': True,
    'all_earliest_milestones_preserved': True,
    'all_prior_evidence_and_supplied_histories_preserved': True,
    'earlier_source_surfaces_unchanged': True,
    'earlier_form_analyses_unchanged': True,
    'contextual_analysis_reconciliations': len(c['form_identity_reconciliation']),
    'contextual_analysis_register_location': 'lexicon/entries.json:form_analysis_reconciliations_by_chapter.ch17',
    'new_record_status_counts': {k: dict(Counter(r['knowledge_status'] for r in records.values()))
                                 for k, records in proposed.items()},
    'reused_supplied_exposures': reused,
    'bounded_scope': c['bounded_scope'],
    'limits': ['Earlier source forms supplied again receive exposure history without recognition or production milestones.', 'No Unit 18 work or archived teaching milestone is included.']
}
if args.final:
    assert c['textual_review']['status'] == c['presentation_review']['status'] == 'accepted'
    report['accepted_text_checkpoint'] = c['accepted_text_checkpoint']
    report['register_identities'] = [{'path': p, 'sha256': sha(p), 'sha256_normalized_lf': lfsha(p)}
                                     for p in ['lexicon/entries.json', 'curriculum/grammar.json']]
    Path('chapters/ch17/register-integration.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
else:
    Path('build/unit17-register-preservation.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
print(report['status'], preserved, len(prior_paths), 'earlier active files;',
      len(b['archive_files']), 'archive files;', {k: len(v) for k, v in promotions.items()}, 'promotions')
