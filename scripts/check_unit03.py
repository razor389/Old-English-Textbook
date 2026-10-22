"""Concrete Unit 3 coverage and export checks; not a substitute for linguistic review."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
errors = []

def require(condition, message):
    if not condition:
        errors.append(message)

def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))

def unique(rows, key, label):
    result = {}
    for row in rows:
        require(row[key] not in result, f'Duplicate {label}: {row[key]}')
        result[row[key]] = row
    return result

def surface(text):
    return text.strip('.,:;!?“”‘’"()').casefold()

def chars(text):
    return re.sub(r'\s+', '', text.replace('\u00ad', '-'))

def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--draft', action='store_true')
    parser.add_argument('--tex', action='store_true')
    args = parser.parse_args()
    c = read('chapters/ch03/coverage.json')
    lex = read('lexicon/entries.json')
    gram = read('curriculum/grammar.json')
    old_forms = {f['form_id']: f for l in lex['lemmas'] for f in l['forms']}
    old_senses = {s['sense_id']: s for l in lex['lemmas'] for s in l['senses']}
    old_features = {f['feature_id']: f for f in gram['features']}
    forms = unique([f for l in c['lexical_inventory'] for f in l['forms']], 'form_id', 'form')
    senses = unique([s for l in c['lexical_inventory'] for s in l['senses']], 'sense_id', 'sense')
    features = unique(c['grammar_inventory'], 'feature_id', 'feature')
    maps = {'form': (forms, old_forms), 'sense': (senses, old_senses), 'feature': (features, old_features)}
    teaching = unique(c['teaching_records'], 'teaching_id', 'teaching record')
    evidence = c['evidence_catalog']

    def status(kind, item):
        new, old = maps[kind]
        if item in new:
            return new[item]['knowledge_status']
        if item in old and old[item].get('production_taught_in') in {'ch01', 'ch02'}:
            return 'previously_taught'
        if item in old and old[item].get('recognition_taught_in') in {'ch01', 'ch02'}:
            return 'prior_recognition'
        return 'unresolved'

    for kind, (new, old) in maps.items():
        for item, rec in new.items():
            require(rec['knowledge_status'] in {'previously_taught', 'new_production', 'new_recognition', 'supplied'}, f'{item}: invalid knowledge status')
            require(bool(rec.get('evidence_refs')), f'{item}: no evidence')
            require(bool(rec.get('teaching_ids')), f'{item}: no teaching/support location')
            for ref in rec.get('evidence_refs', []):
                require(ref in evidence, f'{item}: unknown evidence {ref}')
            for ref in rec.get('teaching_ids', []):
                require(ref in teaching, f'{item}: unknown teaching record {ref}')
    for ref, record in evidence.items():
        paths = record.get('images', [])
        if record.get('image'):
            paths += record['image'] if isinstance(record['image'], list) else [record['image']]
        for path in paths:
            retained_or_recorded = (ROOT/path).is_file() or (ref == 'U02-DUAL' and (ROOT/record['record']).is_file())
            require(retained_or_recorded, f'{ref}: missing image {path}')
    tasks = unique(c['assigned_items'], 'task_id', 'task')
    require(len(tasks) == 70, 'Expected 70 graded tasks')
    require(len(set(c['key_item_ids'])) == 70, 'Expected 70 unique key IDs')
    require(set(c['key_item_ids']) == {t['key_id'] for t in tasks.values()}, 'Task/key crosswalk differs')
    cook_ids = {f'EX-I-04-{i:02}' for i in range(1, 18)}
    require({tid for tid in tasks if tid.startswith('EX-')} == cook_ids, 'Cook assignment differs from I.4.1–17')
    cook_source = read('sources/audits/unit03-source/exercise-4.json')
    for item in cook_source['items'][:17]:
        require(tasks[item['source_item_id']]['prompt'] == item['source_prompt'], f'{item["source_item_id"]}: original Cook prompt altered')
    for tid, task in tasks.items():
        require(bool(task['prompt']), f'{tid}: empty prompt')
        require(not any(w in task.get('dependency_status', '').lower() for w in ['awaiting', 'unresolved']), f'{tid}: unresolved dependencies')
        for kind in maps:
            required = task.get(f'required_{kind}_ids', [])
            tested = task.get(f'tested_{kind}_ids', [])
            require(bool(required), f'{tid}: no {kind} dependencies')
            for item in required:
                require(status(kind, item) != 'unresolved', f'{tid}: unresolved {kind} {item}')
            for item in tested:
                require(item in required, f'{tid}: tested {kind} outside requirements {item}')
                allowed = {'previously_taught', 'new_production'} if task['mode'] in {'production', 'composition'} else {'previously_taught', 'prior_recognition', 'new_production', 'new_recognition'}
                require(status(kind, item) in allowed, f'{tid}: unlearned independent target {item}')
        for item in task.get('supplied_form_ids', []):
            require(item in task['required_form_ids'], f'{tid}: supplied form outside requirements {item}')
    paradigms = unique(c['paradigms'], 'paradigm_id', 'paradigm')
    for pid, paradigm in paradigms.items():
        ids = paradigm['form_ids']
        require(len(ids) == len(set(ids)), f'{pid}: repeated cell IDs')
        for fid in ids:
            require(fid in forms or fid in old_forms, f'{pid}: unknown cell {fid}')
        declension = paradigm.get('declension')
        expected_count = {'strong':26, 'weak':24, 'demonstrative':18}.get(declension)
        if expected_count:
            require(len(ids) == expected_count, f'{pid}: incomplete {declension} paradigm')
        if paradigm['lemma_id'] in {'twegen', 'thrie'}:
            require(len(ids) == 12, f'{pid}: incomplete two/three paradigm')
        if paradigm['lemma_id'] in {'thing', 'leoht'}:
            require(len(ids) == 8, f'{pid}: incomplete noun paradigm')
        if paradigm.get('surface_rows') and declension in {'strong', 'weak'}:
            require(len(paradigm['surface_rows']) == 6 and all(len(row) == 4 for row in paradigm['surface_rows']), f'{pid}: incomplete displayed NGDA matrix')
            for label, row in zip(paradigm['row_order'], paradigm['surface_rows']):
                gender, number = label.split('.')
                for case, spelling in zip(paradigm['case_order'], row):
                    candidates = [forms.get(fid, old_forms.get(fid)) for fid in ids]
                    matched = [f for f in candidates if f['analysis'].get('case') == case and f['analysis'].get('gender') == gender and f['analysis'].get('number') == number]
                    require(len(matched) == 1 and matched[0]['form'] == spelling, f'{pid}: matrix disagrees with {gender}/{number}/{case} record')
    require(len(c['new_compositions']) == 1 and len(c['new_material_examples']) == 10, 'Expected one connected composition and ten examples')
    passages = c['source_spans'] + c['new_compositions'] + c['new_material_examples']
    for passage in passages:
        pid = passage.get('source_record_id', passage.get('composition_id', passage.get('example_id')))
        text = passage.get('source_text', passage.get('text', ''))
        tokens = passage['tokens']
        require(len(text.split()) == len(tokens), f'{pid}: token count differs')
        for word, token in zip(text.split(), tokens):
            require(word == token.get('source_token', token.get('token')), f'{pid}: token text differs')
            for kind in ['form', 'sense']:
                item = token[f'{kind}_id']
                require(status(kind, item) == token[f'{kind}_status'], f'{pid}: status differs for {item}')
            record = forms.get(token['form_id'], old_forms.get(token['form_id']))
            require(record is not None and surface(word) == surface(record['form']), f'{pid}: token surface differs for {token["form_id"]}')
    source = c['source_spans'][0]
    faithful = ' '.join((ROOT/'sources/audits/unit03-source/fourth-day-text.txt').read_text(encoding='utf-8').split())
    require(source['source_text'] == faithful, 'Fourth-day passage differs from audited transcription')
    require(source['word_count'] == 109 and len(source['tokens']) == 109, 'Fourth-day count differs')
    require('twā miclu lēoht:' in source['source_text'], 'Source colon lost')
    carry = c['source_assignment_policy']
    require(set(carry['new_cook_assignments']) == cook_ids, 'Canonical assignment crosswalk differs')
    require(carry['total_assigned_cook_items'] == 63 and carry['still_deferred_cook_items'] == 581, 'Canonical Cook totals differ')
    for path, digest in c['prior_files'].items():
        if path in {'lexicon/entries.json', 'curriculum/grammar.json'}:
            continue
        raw = (ROOT/path).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == digest or hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest() == c.get('prior_files_lf_sha256',{}).get(path), f'Prior reviewed file changed: {path}')
    paths = ['chapters/ch03/coverage.json']
    if args.draft or args.tex:
        paths += ['chapters/ch03/student.md', 'chapters/ch03/answer-key.md']
    for path in paths:
        raw = (ROOT/path).read_text(encoding='utf-8')
        require(raw == unicodedata.normalize('NFC', raw), f'{path}: non-NFC text')
    if args.draft or args.tex:
        student = (ROOT/paths[1]).read_text(encoding='utf-8')
        key = (ROOT/paths[2]).read_text(encoding='utf-8')
        pattern = r'<!--\s*(?:item:\s*)?((?:NEW-U03-[A-Z]\d+)|(?:EX-I-04-\d+))\s*-->'
        parts = re.split(pattern, student)
        prompts = {parts[i]: re.sub(r'^\d+\.\s*', '', parts[i+1].strip().split('\n\n')[0]) for i in range(1, len(parts), 2)}
        for tid, task in tasks.items():
            require(len(re.findall(r'<!--\s*(?:item:\s*)?'+re.escape(tid)+r'\s*-->', student)) == 1, f'{tid}: learner ID not present exactly once')
            require(len(re.findall(r'<!--\s*(?:key:\s*)?'+re.escape(task['key_id'])+r'\s*-->', key)) == 1, f'{tid}: key ID not present exactly once')
            require(prompts.get(tid) == task['prompt'], f'{tid}: prompt differs from contract')
        for tid in teaching:
            require(tid in student, f'{tid}: teaching/support location missing')
        plain = student.replace('**', '')
        for passage in passages:
            require(passage.get('source_text', passage.get('text', '')) in plain, 'Exact reading/example missing from learner')
    if args.tex:
        for stem, ids in [('chapter-03', list(tasks)), ('answer-key', c['key_item_ids'])]:
            folder = ROOT/'typesetting/ch03'
            tex = (folder/(stem+'.tex')).read_text(encoding='utf-8')
            pdftext = (folder/'build'/(stem+'.txt')).read_text(encoding='utf-8')
            log = (folder/'build'/(stem+'.log')).read_text(encoding='utf-8', errors='replace')
            require((folder/(stem+'.pdf')).is_file(), f'{stem}: final PDF missing')
            for tid in ids:
                require(tid in tex, f'{stem}: missing TeX ID {tid}')
            for warning in ['Missing character:', 'Overfull \\hbox', 'Overfull \\vbox', 'Underfull \\hbox', 'Underfull \\vbox', 'Font shape', 'Rerun to get', 'Table widths have changed']:
                require(warning not in log, f'{stem}: log contains {warning}')
            if stem == 'chapter-03':
                for tid in teaching:
                    require(tid in tex, f'{tid}: missing TeX teaching ID')
                for tid, task in tasks.items():
                    require(chars(task['prompt']) in chars(pdftext), f'{tid}: PDF prompt differs or is interrupted by running matter')
                for passage in passages:
                    require(chars(passage.get('source_text', passage.get('text', ''))) in chars(pdftext), 'PDF exact reading/example differs or is interrupted')
    if errors:
        print('\n'.join('ERROR: '+e for e in errors))
        raise SystemExit(1)
    print(f'Unit 3 checks pass: {len(tasks)} tasks, 17 Cook assignments, 109 source tokens, one connected composition, ten examples; no unresolved dependency references.' + (' Learner/key IDs and exact prompts checked.' if args.draft or args.tex else '') + (' TeX/PDF character and log checks pass.' if args.tex else ''))

if __name__ == '__main__':
    main()
