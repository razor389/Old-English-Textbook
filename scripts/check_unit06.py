"""Repeated concrete Unit 6 contract/export checks; linguistic review is separate."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []
PRIOR = {f'ch{n:02}' for n in range(1, 6)}


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


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--draft', action='store_true')
    parser.add_argument('--tex', action='store_true')
    args = parser.parse_args()
    c = read('chapters/ch06/coverage.json')
    lex = read('lexicon/entries.json')
    gram = read('curriculum/grammar.json')
    old = {
        'form': {f['form_id']: f for l in lex['lemmas'] for f in l['forms']},
        'sense': {s['sense_id']: s for l in lex['lemmas'] for s in l['senses']},
        'feature': {f['feature_id']: f for f in gram['features']},
    }
    new = {
        'form': index([f for l in c['lexical_inventory'] for f in l['forms']], 'form_id', 'form'),
        'sense': index([s for l in c['lexical_inventory'] for s in l['senses']], 'sense_id', 'sense'),
        'feature': index(c['grammar_inventory'], 'feature_id', 'feature'),
    }
    teaching = index(c['teaching_records'], 'teaching_id', 'teaching record')
    evidence = c['evidence_catalog']

    def status(kind, rid):
        if rid in new[kind]:
            return new[kind][rid]['knowledge_status']
        record = old[kind].get(rid, {})
        if record.get('production_taught_in') in PRIOR:
            return 'previously_taught'
        if record.get('recognition_taught_in') in PRIOR:
            return 'prior_recognition'
        return 'unresolved'

    def form(fid):
        return new['form'].get(fid, old['form'].get(fid))

    for kind, records in new.items():
        for rid, record in records.items():
            require(record['knowledge_status'] in {'previously_taught', 'prior_recognition',
                    'new_production', 'new_recognition', 'supplied'}, f'{rid}: invalid scope')
            require(bool(record.get('evidence_refs')), f'{rid}: no evidence')
            require(bool(record.get('teaching_ids')), f'{rid}: no teaching/support location')
            for ref in record.get('evidence_refs', []):
                require(ref in evidence, f'{rid}: unknown evidence {ref}')
            for ref in record.get('teaching_ids', []):
                require(ref in teaching, f'{rid}: unknown teaching location {ref}')
    for eid, record in evidence.items():
        images = list(record.get('images', []))
        if record.get('image'):
            images += record['image'] if isinstance(record['image'], list) else [record['image']]
        for image in images:
            path = image['path'] if isinstance(image, dict) else image
            exists = (ROOT / path).is_file()
            require(exists or (eid == 'U02-DUAL' and (ROOT / record['record']).is_file()),
                    f'{eid}: missing retained image {path}')
            if exists and isinstance(image, dict) and image.get('sha256'):
                require(same_identity(path, image), f'{eid}: changed image {path}')

    tasks = index(c['assigned_items'], 'task_id', 'task')
    require(len(tasks) == 72, 'Expected 72 graded tasks')
    require(not any(tid.startswith('EX-') for tid in tasks), 'Unit 6 adds no numbered Cook set')
    require(len(set(c['key_item_ids'])) == 72, 'Expected 72 distinct key IDs')
    require(set(c['key_item_ids']) == {t['key_id'] for t in tasks.values()}, 'Task/key crosswalk')
    for tid, task in tasks.items():
        require(bool(task.get('prompt')), f'{tid}: empty prompt')
        require(not any(w in task.get('dependency_status', '').lower()
                        for w in ['pending', 'unresolved', 'awaiting']), f'{tid}: dependencies open')
        for kind in new:
            required = task.get(f'required_{kind}_ids', [])
            tested = task.get(f'tested_{kind}_ids', [])
            for rid in required:
                require(status(kind, rid) != 'unresolved', f'{tid}: unresolved {kind} {rid}')
            for rid in tested:
                require(rid in required, f'{tid}: tested {kind} not required: {rid}')
                allowed = {'previously_taught', 'new_production'}
                if task['mode'] not in {'production', 'composition', 'supported_production'}:
                    allowed |= {'prior_recognition', 'new_recognition'}
                if kind == 'feature' and rid in task.get('recognition_feature_ids', []):
                    allowed |= {'prior_recognition', 'new_recognition'}
                require(status(kind, rid) in allowed, f'{tid}: unlearned independent target {rid}')
            for rid in task.get(f'supplied_{kind}_ids', []):
                require(rid in required, f'{tid}: supplied {kind} not required: {rid}')

    paradigms = index(c['paradigms'], 'paradigm_id', 'paradigm')
    counts = Counter(p['kind'] for p in paradigms.values())
    require(counts == {'present_preterite_indicative': 10, 'alternate_present_indicative': 1,
                       'imperative': 44, 'nonfinite': 46}, f'Incomplete system roster: {counts}')
    for pid, paradigm in paradigms.items():
        ids = paradigm['form_ids']
        cells = [form(fid) for fid in ids]
        require(len(ids) == len(set(ids)), f'{pid}: repeated cell ID')
        require(all(cells), f'{pid}: missing cell')
        if not all(cells):
            continue
        require(all(status('form', fid) == 'new_production' for fid in ids), f'{pid}: cell scope')
        kind = paradigm['kind']
        if kind in {'present_preterite_indicative', 'alternate_present_indicative'}:
            tenses = ['present', 'preterite'] if kind.startswith('present_preterite') else ['present']
            expected = {(t, str(p), n) for t in tenses for p in [1, 2, 3] for n in ['sg', 'pl']}
            actual = {({'pres': 'present', 'pret': 'preterite'}.get(f['analysis'].get('tense'),
                        f['analysis'].get('tense')), str(f['analysis'].get('person')),
                       f['analysis'].get('number')) for f in cells}
            require(actual == expected and len(cells) == len(expected), f'{pid}: finite completeness')
        elif kind == 'imperative':
            require(len(cells) == 2 and {str(f['analysis'].get('person')) for f in cells} == {'2'}
                    and {f['analysis'].get('number') for f in cells} == {'sg', 'pl'},
                    f'{pid}: imperative completeness')
        else:
            require(len(cells) == 2, f'{pid}: plain/inflected pair incomplete')

    audit = read('sources/audits/unit06-grammar/paradigms.json')
    aliases = c['form_id_aliases']
    selected = []
    for verb in audit['verbs']:
        selected.extend(verb['finite_cells'])
    for extension in audit['extensions']:
        selected.extend(cell for cell in extension['cells']
                        if cell.get('recommended_knowledge_status') == 'new_production')
    require(len(selected) == 306, 'Expected 306 audited selected verbal cells')
    for cell in selected:
        fid = aliases.get(cell['form_id'], cell['form_id'])
        actual = form(fid)
        require(actual is not None and actual['form'] == cell['form'],
                f'{fid}: selected cell differs from independent grammar audit')
        if actual:
            for field in ['person', 'number', 'mood', 'tense', 'nonfinite']:
                if field in cell:
                    require(actual['analysis'].get(field) == cell[field],
                            f'{fid}: selected grammatical analysis differs: {field}')

    passages = c['source_spans'] + c['new_compositions'] + c['new_material_examples']
    for passage in passages:
        pid = passage.get('source_record_id', passage.get('composition_id', passage.get('example_id')))
        value = passage.get('learner_text', passage.get('text', passage.get('source_text', '')))
        tokens = passage['tokens']
        require(len(value.split()) == len(tokens), f'{pid}: token count')
        for word, token in zip(value.split(), tokens):
            require(form(token['form_id']) is not None, f'{pid}: unknown form {token["form_id"]}')
            record = form(token['form_id'])
            if record:
                require(surface(word) == surface(record['form']), f'{pid}: wrong surface {word}')
            for kind in ['form', 'sense']:
                require(status(kind, token[f'{kind}_id']) == token[f'{kind}_status'],
                        f'{pid}: incorrect {kind} status at {word}')
    require(len(c['new_compositions']) == 1 and len(c['new_compositions'][0]['tokens']) == 68,
            'Expected complete 68-word controlled dialogue')
    require(len(c['new_material_examples']) == 10, 'Expected ten checked examples')
    require(len(c['source_spans']) == 1, 'Expected one contiguous source excerpt')
    source = c['source_spans'][0]
    faithful = (ROOT / 'sources/audits/unit06-source/source-text.txt').read_text(encoding='utf-8').strip()
    learner = (ROOT / 'sources/audits/unit06-source/learner-excerpt.txt').read_text(encoding='utf-8').strip()
    require(source['source_text'] == faithful, 'Source transcription changed')
    require(source['learner_text'] == learner, 'Learner source excerpt changed')
    require(len(source['tokens']) == 76 and len(learner.split()) == 76, 'Source count differs')
    require(len(source['local_support']) == 10 and len(source['source_notes']) == 3,
            'Complete source support/apparatus required')
    for spelling in ['læg', 'gīet', 'geseah', 'ūpāhōf', 'tō sęllanne']:
        require(spelling in learner, f'Source spelling lost: {spelling}')

    dispositions = {}
    for n in range(1, 7):
        contract = c if n == 6 else read(f'chapters/ch{n:02}/coverage.json')
        for task in contract['assigned_items']:
            if task['task_id'].startswith('EX-'):
                dispositions[task['task_id']] = 'assigned'
        for field, disposition in [('deferred_source_items', 'deferred'), ('excluded_source_items', 'excluded')]:
            for item in contract.get(field, []):
                rid = item.get('source_item_id', '')
                if rid.startswith('EX-'):
                    dispositions[rid] = disposition
    require(len(dispositions) == 644 and Counter(dispositions.values()) == {'assigned': 79, 'deferred': 565},
            'Canonical Cook crosswalk must retain 79 assigned / 565 deferred')
    require(dispositions.get('EX-I-04-18') == 'deferred', 'I.4.18 remains deferred')
    for record in c['analysis_inputs']:
        require(same_identity(record['path'], record), f'Frozen analysis input changed: {record["path"]}')
    for path, digest in c['prior_files'].items():
        if path not in {'lexicon/entries.json', 'curriculum/grammar.json'}:
            require(same_identity(path, {'sha256': digest,
                    'sha256_normalized_lf': c.get('prior_files_lf_sha256', {}).get(path)}),
                    f'Prior reviewed file changed: {path}')

    master_paths = ['chapters/ch06/coverage.json']
    if args.draft or args.tex:
        master_paths += ['chapters/ch06/student.md', 'chapters/ch06/answer-key.md']
    for path in master_paths:
        raw = (ROOT / path).read_text(encoding='utf-8')
        require(raw == unicodedata.normalize('NFC', raw), f'{path}: non-NFC text')
    if args.draft or args.tex:
        student = (ROOT / master_paths[1]).read_text(encoding='utf-8')
        key = (ROOT / master_paths[2]).read_text(encoding='utf-8')
        parts = re.split(r'<!--\s*(?:item:\s*)?(NEW-U06-[A-Z]\d+)\s*-->', student)
        prompts = {parts[i]: re.sub(r'^\d+\.\s*', '', parts[i+1].strip().split('\n\n')[0])
                   for i in range(1, len(parts), 2)}
        for tid, task in tasks.items():
            require(len(re.findall(r'<!--\s*(?:item:\s*)?' + re.escape(tid) + r'\s*-->', student)) == 1,
                    f'{tid}: learner marker not present exactly once')
            require(len(re.findall(r'<!--\s*(?:key:\s*)?' + re.escape(task['key_id']) + r'\s*-->', key)) == 1,
                    f'{tid}: key marker not present exactly once')
            require(prompts.get(tid) == task['prompt'], f'{tid}: prompt differs from contract')
        for tid in teaching:
            require(tid in student, f'{tid}: missing teaching/support marker')
        for passage in passages:
            value = passage.get('learner_text', passage.get('text', passage.get('source_text', '')))
            require(value in student.replace('**', ''), 'Exact learner reading/example missing')
        for note in source['source_notes'].values():
            note_text = note.split(': ', 1)[-1]
            require(note_text in student.replace('**', ''), f'Original source note missing: {note_text}')
    if args.tex:
        folder = ROOT / 'typesetting/ch06'
        for stem, ids in [('chapter-06', list(tasks)), ('answer-key', c['key_item_ids'])]:
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
            if stem == 'chapter-06':
                for task in tasks.values():
                    require(chars(task['prompt']) in chars(pdftext), f'{task["task_id"]}: PDF prompt differs')
                for tid in teaching:
                    require(tid in tex, f'{tid}: TeX teaching marker missing')
    if ERRORS:
        print('\n'.join('ERROR: ' + error for error in ERRORS))
        raise SystemExit(1)
    print('Unit 6 checks pass: 72 tasks; complete indicative, imperative and infinitive systems; '
          '76-word source and 68-word dialogue; Cook crosswalk and earlier files preserved.' +
          (' Learner/key markers and exact prompts checked.' if args.draft or args.tex else '') +
          (' TeX/PDF markers and clean logs checked.' if args.tex else ''))


if __name__ == '__main__':
    main()
