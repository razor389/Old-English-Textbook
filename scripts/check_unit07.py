"""Repeated Unit 7 coverage, dependency, display and export checks; not linguistic proof."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []
PRIOR = {f'ch{n:02}' for n in range(1, 7)}


def require(condition, message):
    if not condition:
        ERRORS.append(message)


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def index(rows, key, label):
    out = {}
    for row in rows:
        require(row[key] not in out, f'Duplicate {label}: {row[key]}')
        out[row[key]] = row
    return out


def surface(value):
    return value.strip('.,:;!?“”‘’"()').casefold()


def chars(value):
    return re.sub(r'\s+', '', value.replace('\u00ad', '-'))


def same_identity(path, record):
    raw = (ROOT / path).read_bytes()
    return (hashlib.sha256(raw).hexdigest() == record.get('sha256') or
            hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest() ==
            record.get('sha256_normalized_lf'))


def expected_tables(c):
    """Yield actual complete matrices, with stable markers for each printed subtable."""
    lemmas = {l['lemma_id']: l for l in c['lexical_inventory']}
    for table in c['display_plan']['tables']:
        tid, kind = table['table_id'], table['kind']
        if 'print_matrices' in table:
            for n, matrix in enumerate(table['print_matrices'], 1):
                yield tid + f'-{n}', [matrix['columns']] + [
                    [r['case']] + [v['form'] for v in r['cells']] for r in matrix['rows']]
        elif 'print_rows' in table:
            yield tid, [table['print_headers']] + [
                [r.get('label', r.get('case'))] + [v['form'] for v in r['cells']]
                for r in table['print_rows']]
        elif kind in {'subjunctive_matrix', 'compact_subjunctive_matrix', 'participle_pairs'}:
            yield tid, [table['columns']] + [[r.get('headword', r.get('label',
                lemmas.get(r.get('lemma_id'), {}).get('display_headword')))] + r['forms']
                for r in table['rows']]
        elif kind in {'alternative_present_subjunctive', 'imperative_pair'}:
            yield tid, [table['columns'], table['forms']]
        elif kind == 'predicate_participle_variants':
            yield tid, [['Verb', 'Uninflected', 'Plural masculine-like']] + [
                [lemmas[r['lemma_id']]['display_headword'], r['uninflected'], r['plural_masculine_like']]
                for r in table['rows']]


def check_display_tables(c, student):
    for tid, expected in expected_tables(c):
        hits = list(re.finditer(r'<!--\s*table:\s*' + re.escape(tid) + r'\s*-->', student))
        require(len(hits) == 1, f'{tid}: matrix marker not unique')
        if len(hits) != 1:
            continue
        block = re.match(r'\s*(\|[^\n]+(?:\n\|[^\n]+)*)', student[hits[0].end():])
        require(block is not None, f'{tid}: no adjacent table')
        if block is not None:
            rows = [[cell.strip().replace('**', '') for cell in line.strip().strip('|').split('|')]
                    for line in block[1].splitlines()]
            require([rows[0]] + rows[2:] == expected, f'{tid}: displayed label or cell differs')


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--draft', action='store_true')
    parser.add_argument('--tex', action='store_true')
    args = parser.parse_args()
    c = read('chapters/ch07/coverage.json')
    lex, gram = read('lexicon/entries.json'), read('curriculum/grammar.json')
    old = {'form': {f['form_id']: f for l in lex['lemmas'] for f in l['forms']},
           'sense': {s['sense_id']: s for l in lex['lemmas'] for s in l['senses']},
           'feature': {f['feature_id']: f for f in gram['features']}}
    new = {'form': index([f for l in c['lexical_inventory'] for f in l['forms']], 'form_id', 'form'),
           'sense': index([s for l in c['lexical_inventory'] for s in l['senses']], 'sense_id', 'sense'),
           'feature': index(c['grammar_inventory'], 'feature_id', 'feature')}
    teaching = index(c['teaching_records'], 'teaching_id', 'teaching')
    evidence = c['evidence_catalog']

    def status(kind, rid):
        if rid in new[kind]:
            return new[kind][rid]['knowledge_status']
        r = old[kind].get(rid, {})
        if r.get('production_taught_in') in PRIOR:
            return 'previously_taught'
        if r.get('recognition_taught_in') in PRIOR:
            return 'prior_recognition'
        return 'supplied' if r.get('supplied_in') else 'unresolved'

    def form(fid):
        return new['form'].get(fid, old['form'].get(fid))

    for kind, records in new.items():
        for rid, r in records.items():
            require(r['knowledge_status'] in {'previously_taught', 'prior_recognition',
                    'new_production', 'new_recognition', 'supplied'}, f'{rid}: invalid scope')
            require(bool(r.get('evidence_refs')), f'{rid}: no evidence')
            require(bool(r.get('teaching_ids')), f'{rid}: no teaching/support location')
            for ref in r.get('evidence_refs', []):
                require(ref in evidence, f'{rid}: unknown evidence {ref}')
            for ref in r.get('teaching_ids', []):
                require(ref in teaching, f'{rid}: unknown teaching {ref}')
    for eid, record in evidence.items():
        images = list(record.get('images', []))
        if record.get('image'):
            images += record['image'] if isinstance(record['image'], list) else [record['image']]
        for image_number, image in enumerate(images):
            path = image['path'] if isinstance(image, dict) else image
            exists = (ROOT / path).is_file()
            require(exists or (eid == 'U02-DUAL' and (ROOT / record['record']).is_file()),
                    f'{eid}: missing retained image {path}')
            if exists and isinstance(image, dict) and image.get('sha256'):
                require(same_identity(path, image), f'{eid}: changed image {path}')
            digests = record.get('image_sha256')
            digest = (digests[image_number] if isinstance(digests, list) and image_number < len(digests)
                      else digests if isinstance(digests, str) and len(images) == 1 else None)
            if exists and digest:
                require(same_identity(path, {'sha256': digest}), f'{eid}: source image identity differs: {path}')

    tasks = index(c['assigned_items'], 'task_id', 'task')
    require(len(tasks) == 80 and len(c['key_item_ids']) == len(set(c['key_item_ids'])) == 80,
            'Expected 80 tasks and distinct keys')
    require(set(c['key_item_ids']) == {t['key_id'] for t in tasks.values()}, 'Task/key crosswalk')
    cook = {r['source_item_id']: r['prompt'] for r in read(
        'sources/audits/unit07-source/exercises-prompts.json')['items']}
    require({tid: t['prompt'] for tid, t in tasks.items() if tid.startswith('EX-')} == cook,
            'All 34 Cook prompts must remain exact')
    for tid, task in tasks.items():
        require(bool(task.get('prompt')), f'{tid}: empty prompt')
        require(not any(w in task.get('dependency_status', '').lower()
                        for w in ['pending', 'unresolved', 'awaiting']), f'{tid}: dependencies open')
        for kind in new:
            required = task.get(f'required_{kind}_ids', [])
            for rid in required:
                require(status(kind, rid) != 'unresolved', f'{tid}: unresolved {kind} {rid}')
            for rid in task.get(f'tested_{kind}_ids', []):
                require(rid in required, f'{tid}: tested {kind} not required: {rid}')
                allowed = {'previously_taught', 'new_production'}
                if task['mode'] in {'analysis', 'reading', 'scaffolded_reading', 'scaffolded_recognition'}:
                    allowed |= {'prior_recognition', 'new_recognition'}
                require(status(kind, rid) in allowed, f'{tid}: unlearned independent target {rid}')
            for rid in task.get(f'supplied_{kind}_ids', []):
                require(rid in required, f'{tid}: supplied {kind} not required: {rid}')
    paradigms = index(c['paradigms'], 'paradigm_id', 'paradigm')
    counts = Counter(p['kind'] for p in paradigms.values())
    require(counts == {'present_preterite_subjunctive': 56, 'present_preterite_indicative': 5,
                       'imperative': 1, 'participle_formation_pair': 12, 'participle_agreement': 5,
                       'strong_quantifier_declension': 2, 'noun_declension': 1},
            f'Incomplete system roster: {counts}')
    expected_sizes = {'present_preterite_subjunctive': 12, 'present_preterite_indicative': 12,
                      'imperative': 2, 'participle_formation_pair': 2, 'participle_agreement': 48,
                      'strong_quantifier_declension': 24, 'noun_declension': 8}
    for pid, p in paradigms.items():
        ids = p['form_ids']
        expected = expected_sizes[p['kind']] + (6 if pid == 'NEW-U07-SUBJ-wesan' else 0)
        require(len(ids) == len(set(ids)) == expected, f'{pid}: incomplete or repeated cells')
        for fid in ids:
            require(form(fid) is not None, f'{pid}: unknown cell {fid}')
            scope = 'new_recognition' if fid.startswith('geweald-') and fid.endswith('-pl') else 'new_production'
            require(status('form', fid) == scope, f'{pid}: incorrect cell scope {fid}')
    # Compare selected cells with the separately prepared grammar evidence.
    aliases = c['form_id_aliases']
    audited = []
    mood_audit = read('sources/audits/unit07-grammar/subjunctive-systems.json')
    for system in mood_audit['systems']:
        audited.extend(system['full_person_number_cells'])
        audited.extend(system.get('alternative_present_cells', []))
    for system in read('sources/audits/unit07-grammar/new-verb-systems.json')['systems']:
        audited.extend(system['full_indicative_cells'])
    for system in read('sources/audits/unit07-grammar/nominal-systems.json')['systems']:
        audited.extend(system['forms'])
    for cell in audited:
        fid = aliases.get(cell['form_id'], cell['form_id'])
        actual = form(fid)
        require(actual is not None and surface(actual['form']) == surface(cell['form']),
                f'{fid}: independent grammar surface differs')
        if actual:
            for field, value in cell['analysis'].items():
                require(actual['analysis'].get(field) == value,
                        f'{fid}: independent grammar analysis differs: {field}')
    for model in read('sources/audits/unit07-grammar/participle-agreement.json')['models']:
        display = next(t for t in c['display_plan']['tables']
                       if t['kind'] == 'full_participle_agreement' and t['citation'] == model['citation'])
        for cell in model['full_cells']:
            candidates = [v for v in display['cells'] if all(
                v['analysis'][k] == cell[k] for k in ['case', 'number', 'gender', 'declension'])]
            require(len(candidates) == 1 and candidates[0]['form'] == cell['form'],
                    f'{model["citation"]}: audited agreement cell differs: {cell}')
    # Compare every display surface with the underlying contracted identities.
    def walk_display(value):
        if isinstance(value, dict):
            if 'form_id' in value and 'form' in value:
                r = form(value['form_id'])
                require(r is not None and surface(r['form']) == surface(value['form']),
                        f'Display identity differs: {value["form_id"]}')
            for child in value.values():
                walk_display(child)
        elif isinstance(value, list):
            for child in value:
                walk_display(child)
    walk_display(c['display_plan'])

    passages = c['source_spans'] + c['new_compositions'] + c['new_material_examples']
    for tid, task in tasks.items():
        for sequence in task.get('input_sequences', []):
            for token in sequence:
                record = form(token['form_id'])
                require(record is not None and surface(record['form']) == surface(token['form']),
                        f'{tid}: input-token surface differs')
                for kind in ['form', 'sense']:
                    require(status(kind, token[f'{kind}_id']) == token[f'{kind}_status'],
                            f'{tid}: input-token {kind} scope differs')
    for passage in passages:
        pid = passage.get('source_record_id', passage.get('composition_id', passage.get('example_id')))
        value = passage.get('learner_text', passage.get('text', ''))
        tokens = passage['tokens']
        require(len(value.split()) == len(tokens), f'{pid}: token count')
        for word, token in zip(value.split(), tokens):
            ids = token.get('form_ids', [token.get('form_id')])
            scopes = token.get('form_statuses', [token.get('form_status')])
            for fid, scope in zip(ids, scopes):
                record = form(fid)
                require(record is not None and surface(word) == surface(record['form']),
                        f'{pid}: unknown form/wrong surface {word}: {fid}')
                require(status('form', fid) == scope, f'{pid}: incorrect form status: {word}')
            require(status('sense', token['sense_id']) == token['sense_status'],
                    f'{pid}: incorrect sense status: {word}')
    require(len(c['new_compositions']) == 1 and len(c['new_compositions'][0]['tokens']) == 56,
            'Expected complete 56-word account')
    require(len(c['new_material_examples']) == 11, 'Expected eleven checked examples')
    require(len(c['source_spans']) == 1, 'Expected one contiguous source paragraph')
    source = c['source_spans'][0]
    original = read('sources/audits/unit07-source/reading-source.json')
    for field in ['learner_text', 'line_preserving_transcription_without_note_cues', 'original_notes',
                  'original_note_cue_order', 'change_notes']:
        require(source[field] == original[field], f'Source changed: {field}')
    require(len(source['tokens']) == len(source['learner_text'].split()) == 89, 'Expected 89 source words')
    require(len(source['supports']) == 10 and len(source['original_notes']) == 18,
            'Expected ten supports and all eighteen original notes')
    require([n['original_note_number'] for n in source['original_notes']] == list(range(4, 22)),
            'Original note numbering differs')
    for fid in ['swimman-pres-part-acc-n-pl-source', 'fleogan-pres-part-acc-n-pl-source',
                'libban-pres-part-acc-n-pl-source']:
        require(status('form', fid) == 'new_recognition', f'{fid}: exact recognition scope lost')
    for kind, rid in [('sense', 'ofer-1'), ('feature', 'u07-spatial-ofer')]:
        require('U07-F-36-OFER' in new[kind][rid]['evidence_refs'], f'{rid}: spatial government evidence lost')

    dispositions = {}
    for n in range(1, 8):
        contract = c if n == 7 else read(f'chapters/ch{n:02}/coverage.json')
        for task in contract['assigned_items']:
            if task['task_id'].startswith('EX-'):
                dispositions[task['task_id']] = 'assigned'
        for field, disposition in [('deferred_source_items', 'deferred'), ('excluded_source_items', 'excluded')]:
            for item in contract.get(field, []):
                rid = item.get('source_item_id', '')
                if rid.startswith('EX-'):
                    dispositions[rid] = disposition
    require(len(dispositions) == 644 and Counter(dispositions.values()) == {'assigned': 113, 'deferred': 531},
            'Canonical Cook crosswalk must retain 113 assigned / 531 deferred')
    require(dispositions.get('EX-I-04-18') == 'assigned', 'I.4.18 must be resolved')
    require(c['source_alias_assignments'][0]['canonical_source_record_id'] == source['source_record_id'],
            'Prior birds alias unresolved')
    for record in c['analysis_inputs']:
        require(same_identity(record['path'], record), f'Frozen analysis input changed: {record["path"]}')
    for path, digest in c['prior_files'].items():
        if path not in {'lexicon/entries.json', 'curriculum/grammar.json'}:
            require(same_identity(path, {'sha256': digest,
                    'sha256_normalized_lf': c.get('prior_files_lf_sha256', {}).get(path)}),
                    f'Prior reviewed file changed: {path}')

    masters = ['chapters/ch07/coverage.json']
    if args.draft or args.tex:
        masters += ['chapters/ch07/student.md', 'chapters/ch07/answer-key.md']
    for path in masters:
        raw = (ROOT / path).read_text(encoding='utf-8')
        require(raw == unicodedata.normalize('NFC', raw), f'{path}: non-NFC text')
    if args.draft or args.tex:
        student, key = [(ROOT / path).read_text(encoding='utf-8') for path in masters[1:]]
        check_display_tables(c, student)
        for tid, task in tasks.items():
            pattern = r'<!--\s*(?:item:\s*)?' + re.escape(tid) + r'\s*-->'
            hits = list(re.finditer(pattern, student))
            require(len(hits) == 1, f'{tid}: learner marker not unique')
            if len(hits) == 1:
                prompt = student[hits[0].end():].strip().split('\n\n')[0]
                prompt = re.sub(r'^\d+\.\s*', '', prompt)
                require(prompt == task['prompt'], f'{tid}: prompt differs from contract')
            require(len(re.findall(r'<!--\s*(?:key:\s*)?' + re.escape(task['key_id']) + r'\s*-->', key)) == 1,
                    f'{tid}: key marker not unique')
        for tid in teaching:
            require(tid in student, f'{tid}: missing teaching/support marker')
        for passage in passages:
            value = passage.get('learner_text', passage.get('text', ''))
            require(value in student.replace('**', ''), 'Exact learner passage/example missing')
        for note in source['original_notes']:
            require(note['text'] in student.replace('**', ''), f'Original note missing: {note["original_note_number"]}')
    if args.tex:
        folder = ROOT / 'typesetting/ch07'
        for stem, ids in [('chapter-07', list(tasks)), ('answer-key', c['key_item_ids'])]:
            tex = (folder / (stem + '.tex')).read_text(encoding='utf-8')
            pdftext = (folder / 'build' / (stem + '.txt')).read_text(encoding='utf-8')
            log = (folder / 'build' / (stem + '.log')).read_text(encoding='utf-8', errors='replace')
            require((folder / (stem + '.pdf')).is_file(), f'{stem}: retained PDF missing')
            for tid in ids:
                require(tid in tex, f'{stem}: missing TeX marker {tid}')
            for warning in ['Missing character:', 'Overfull \\hbox', 'Overfull \\vbox',
                            'Underfull \\hbox', 'Underfull \\vbox', 'Font shape',
                            'Rerun to get', 'Table widths have changed']:
                require(warning not in log, f'{stem}: {warning}')
            if stem == 'chapter-07':
                for task in tasks.values():
                    require(chars(task['prompt']) in chars(pdftext), f'{task["task_id"]}: PDF prompt differs')
                for tid in teaching:
                    require(tid in tex, f'{tid}: TeX teaching marker missing')
    if ERRORS:
        print('\n'.join('ERROR: ' + error for error in ERRORS))
        raise SystemExit(1)
    print('Unit 7 checks pass: 80 tasks, 34 exact Cook prompts; 82 complete paradigms; '
          '89-word source and 56-word account; dependencies, evidence and earlier files preserved.' +
          (' Complete learner matrices, prompts, key/teaching markers and passages checked.' if args.draft or args.tex else '') +
          (' TeX/PDF markers and clean logs checked.' if args.tex else ''))


if __name__ == '__main__':
    main()
