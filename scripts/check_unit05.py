"""Concrete Unit 5 coverage and export checks; not a substitute for linguistic review."""
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
    c = read('chapters/ch05/coverage.json')
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
        if item in old and old[item].get('production_taught_in') in {'ch01', 'ch02', 'ch03', 'ch04'}:
            return 'previously_taught'
        if item in old and old[item].get('recognition_taught_in') in {'ch01', 'ch02', 'ch03', 'ch04'}:
            return 'prior_recognition'
        return 'unresolved'

    for kind, (new, old) in maps.items():
        for item, rec in new.items():
            require(rec['knowledge_status'] in {'previously_taught', 'prior_recognition', 'new_production', 'new_recognition', 'supplied'}, f'{item}: invalid knowledge status')
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
        for image_record in paths:
            path = image_record['path'] if isinstance(image_record, dict) else image_record
            retained_or_recorded = (ROOT/path).is_file() or (ref == 'U02-DUAL' and (ROOT/record['record']).is_file())
            require(retained_or_recorded, f'{ref}: missing image {path}')
            if isinstance(image_record, dict) and image_record.get('sha256') and (ROOT/path).is_file():
                require(hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == image_record['sha256'], f'{ref}: image identity differs {path}')
    tasks = unique(c['assigned_items'], 'task_id', 'task')
    require(len(tasks) == 67, 'Expected 67 graded tasks')
    require(len(set(c['key_item_ids'])) == 67, 'Expected 67 unique key IDs')
    require(set(c['key_item_ids']) == {t['key_id'] for t in tasks.values()}, 'Task/key crosswalk differs')
    cook_ids = {f'EX-I-05-{n:02}' for n in range(1,17)}
    require({tid for tid in tasks if tid.startswith('EX-')} == cook_ids, 'All16 CookI.5 items must be assigned exactly once')
    require(all(tasks[tid].get('origin') in {'exact_source','source','source_exercise'} for tid in cook_ids), 'Cook origin must be exact source')
    source_items={item['source_item_id']:item for item in read('sources/audits/unit05-source/exercise-5.json')['items']}
    require(set(source_items)==cook_ids, 'Source audit must contain exactly16 CookI.5 items')
    for tid in cook_ids:
        require(tasks[tid]['prompt']==source_items[tid]['original_english_prompt'], f'{tid}: original English prompt changed')
        require(tasks[tid].get('source_item_id')==tid, f'{tid}: source identity missing')
        loc=tasks[tid].get('source_locator',{})
        require(loc.get('source_id')=='cook_ex_1895' and loc.get('original_group')=='I', f'{tid}: original group/source locator missing')
        require(loc.get('exercise_number')==5 and loc.get('item_number')==int(tid[-2:]), f'{tid}: original exercise/item locator missing')
        require(loc.get('printed_page')==3 and loc.get('pdf_page_1_based')==11, f'{tid}: printed/PDF locator missing')
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
                allowed = {'previously_taught', 'new_production'} if task['mode'] in {'production', 'composition', 'supported_production'} else {'previously_taught', 'prior_recognition', 'new_production', 'new_recognition'}
                if kind == 'feature' and item in task.get('recognition_feature_ids', []):
                    allowed |= {'prior_recognition','new_recognition'}
                require(status(kind, item) in allowed, f'{tid}: unlearned independent target {item}')
        for item in task.get('recognition_feature_ids', []):
            require(item in task.get('tested_feature_ids', []), f'{tid}: recognition feature is not an actual tested target')
        for item in task.get('supplied_form_ids', []):
            require(item in task['required_form_ids'], f'{tid}: supplied form outside requirements {item}')
    paradigms = unique(c['paradigms'], 'paradigm_id', 'paradigm')
    for pid, paradigm in paradigms.items():
        ids = paradigm['form_ids']
        require(len(ids) == len(set(ids)), f'{pid}: repeated cell IDs')
        for fid in ids:
            require(fid in forms or fid in old_forms, f'{pid}: unknown cell {fid}')
        cells = [forms.get(fid, old_forms.get(fid)) for fid in ids]
        require(len(ids) == 12, f'{pid}: incomplete finite indicative system')
        expected = {(tense, str(person), number) for tense in ['present','preterite'] for person in [1,2,3] for number in ['sg','pl']}
        actual = {({'pres':'present','pret':'preterite'}.get(f['analysis'].get('tense'),f['analysis'].get('tense')), str(f['analysis'].get('person')), f['analysis'].get('number')) for f in cells if f}
        require(actual == expected, f'{pid}: finite tense/person/number cells differ')
        require(all(f and f['knowledge_status'] == 'new_production' for f in cells), f'{pid}: finite teaching scope differs')
    require(len(paradigms) == 33, 'Expected33 complete productive finite systems')
    grammar_audit=read('sources/audits/unit05-grammar/paradigms.json')
    for verb in grammar_audit['verbs']:
        for cell in verb['finite_cells']:
            require(cell['form_id'] in forms and forms[cell['form_id']]['form']==cell['form'], f'{cell["form_id"]}: selected finite cell differs from frozen grammar audit')
        lemma=next(l for l in c['lexical_inventory'] if l['lemma_id']==verb['lemma_id'])
        require([x['form'] for x in lemma['principal_parts']]==[x['form'] for x in verb['citation_principal_parts']], f'{verb["lemma_id"]}: principal parts differ from source-audited selection')
    require(len(c['new_compositions']) == 1, 'Expected one connected composition')
    passages = c['source_spans'] + c['new_compositions'] + c['new_material_examples']
    for passage in passages:
        pid = passage.get('source_record_id', passage.get('composition_id', passage.get('example_id')))
        text = passage.get('source_text', passage.get('text', ''))
        tokens = passage['tokens']
        require(len(text.split()) == len(tokens), f'{pid}: token count differs')
        for word, token in zip(text.split(), tokens):
            literal=token.get('source_token', token.get('token'))
            require(word == literal if literal is not None else surface(word)==surface(token.get('form','')), f'{pid}: token text differs')
            for kind in ['form', 'sense']:
                item = token[f'{kind}_id']
                require(status(kind, item) == token[f'{kind}_status'], f'{pid}: status differs for {item}')
            record = forms.get(token['form_id'], old_forms.get(token['form_id']))
            require(record is not None and surface(word) == surface(record['form']), f'{pid}: token surface differs for {token["form_id"]}')
    reviewed_seed=read('curriculum/proposals/unit05/composition-seed.json')
    seed_review=read('sources/audits/unit05-source/composition-review.json')
    seed_identity=next(x for x in c['analysis_inputs'] if x['path']==seed_review['reviewed_input'])
    seed_raw=(ROOT/seed_review['reviewed_input']).read_bytes()
    require(seed_identity['sha256']==seed_review['input_sha256'], 'Contract does not preserve independently reviewed composition input identity')
    require(hashlib.sha256(seed_raw).hexdigest()==seed_review['input_sha256'] or hashlib.sha256(seed_raw.replace(b'\r\n',b'\n')).hexdigest()==seed_identity['sha256_normalized_lf'], 'Independently reviewed composition content changed')
    seed_texts={x.get('composition_id',x.get('example_id')):x['candidate_text'] for x in reviewed_seed['compositions']+reviewed_seed['teaching_examples']}
    for passage in c['new_compositions']+c['new_material_examples']:
        pid=passage.get('composition_id',passage.get('example_id'))
        require(passage['text']==seed_texts[pid], f'{pid}: new text differs from independently reviewed candidate')
    require(len(c['source_spans']) == 2, 'Expected first-day revisit and complete second day')
    first,second=c['source_spans']
    earlier=read('chapters/ch01/coverage.json')['source_spans'][0]
    require(first['source_text'] == earlier['source_text'], 'First-day revisit differs from original exact assignment')
    require(first['word_count'] == 69 and len(first['tokens']) == 69, 'First-day word count differs')
    require(first.get('assignment_status') == 'revisit', 'First-day must be explicitly a revisit')
    faithful=' '.join((ROOT/'sources/audits/unit05-source/second-day-text.txt').read_text(encoding='utf-8').split())
    require(second['source_text'] == faithful, 'Second day differs from image-checked transcription')
    require(second['word_count']==58 and len(second['tokens'])==58, 'Complete second-day word count differs')
    require(second.get('assignment_status') == 'assigned', 'Second-day new assignment missing')
    for spelling in ['ęft','tōtwǣme','tōtwǣmde','Heofonan','ōðer']:
        require(spelling in second['source_text'], f'Source spelling lost: {spelling}')
    carry = c['source_assignment_policy']
    require(set(carry['new_cook_assignments']) == cook_ids, 'Canonical assignment crosswalk differs')
    require(carry['total_assigned_cook_items'] == 79 and carry['still_deferred_cook_items'] == 565, 'Canonical Cook totals differ')
    assignments = {}
    for chapter in ['ch01','ch02','ch03','ch04','ch05']:
        chapter_contract = c if chapter == 'ch05' else read(f'chapters/{chapter}/coverage.json')
        for item in chapter_contract['assigned_items']:
            if item['task_id'].startswith('EX-'):
                assignments[item['task_id']] = 'assigned'
        for field, disposition in [('deferred_source_items','deferred'),('excluded_source_items','excluded')]:
            for item in chapter_contract.get(field, []):
                item_id = item.get('source_item_id', '')
                if item_id.startswith('EX-'):
                    assignments[item_id] = disposition
    require(len(assignments) == 644, 'Canonical crosswalk does not account for all 644 Cook items')
    require(sum(v == 'assigned' for v in assignments.values()) == 79 and sum(v == 'deferred' for v in assignments.values()) == 565, 'Folded active-contract crosswalk differs')
    for input_record in c['analysis_inputs']:
        raw = (ROOT/input_record['path']).read_bytes()
        actual = hashlib.sha256(raw).hexdigest()
        normalized = hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest()
        require(actual == input_record['sha256'] or normalized == input_record.get('sha256_normalized_lf'), f'Frozen analysis input changed: {input_record["path"]}')
    for path, digest in c['prior_files'].items():
        if path in {'lexicon/entries.json', 'curriculum/grammar.json'}:
            continue
        raw = (ROOT/path).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == digest or hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest() == c.get('prior_files_lf_sha256',{}).get(path), f'Prior reviewed file changed: {path}')
    paths = ['chapters/ch05/coverage.json']
    if args.draft or args.tex:
        paths += ['chapters/ch05/student.md', 'chapters/ch05/answer-key.md']
    for path in paths:
        raw = (ROOT/path).read_text(encoding='utf-8')
        require(raw == unicodedata.normalize('NFC', raw), f'{path}: non-NFC text')
    if args.draft or args.tex:
        student = (ROOT/paths[1]).read_text(encoding='utf-8')
        key = (ROOT/paths[2]).read_text(encoding='utf-8')
        pattern = r'<!--\s*(?:item:\s*)?(NEW-U05-[A-Z]\d+|EX-I-05-\d+)\s*-->'
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
        for stem, ids in [('chapter-05', list(tasks)), ('answer-key', c['key_item_ids'])]:
            folder = ROOT/'typesetting/ch05'
            tex = (folder/(stem+'.tex')).read_text(encoding='utf-8')
            pdftext = (folder/'build'/(stem+'.txt')).read_text(encoding='utf-8')
            log = (folder/'build'/(stem+'.log')).read_text(encoding='utf-8', errors='replace')
            require((folder/(stem+'.pdf')).is_file(), f'{stem}: final PDF missing')
            for tid in ids:
                require(tid in tex, f'{stem}: missing TeX ID {tid}')
            for warning in ['Missing character:', 'Overfull \\hbox', 'Overfull \\vbox', 'Underfull \\hbox', 'Underfull \\vbox', 'Font shape', 'Rerun to get', 'Table widths have changed']:
                require(warning not in log, f'{stem}: log contains {warning}')
            if stem == 'chapter-05':
                for tid in teaching:
                    require(tid in tex, f'{tid}: missing TeX teaching ID')
                for tid, task in tasks.items():
                    require(chars(task['prompt']) in chars(pdftext), f'{tid}: PDF prompt differs or is interrupted by running matter')
                for passage in passages:
                    require(chars(passage.get('source_text', passage.get('text', ''))) in chars(pdftext), 'PDF exact reading/example differs or is interrupted')
    if errors:
        print('\n'.join('ERROR: '+e for e in errors))
        raise SystemExit(1)
    print(f'Unit5 checks pass: {len(tasks)} tasks, all16 CookI.5 prompts, two exact source spans,33 complete finite paradigms and one connected composition; no unresolved dependency references.' + (' Learner/key IDs and exact prompts checked.' if args.draft or args.tex else '') + (' TeX/PDF character and log checks pass.' if args.tex else ''))

if __name__ == '__main__':
    main()
