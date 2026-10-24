"""Repeated Unit 8 dependency, source, display and export checks; not linguistic proof."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []
PRIOR = {f'ch{n:02}' for n in range(1, 8)}


def require(ok, message):
    if not ok:
        ERRORS.append(message)


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def surface(value):
    return value.strip('.,:;!?“”‘’"()').casefold()


def chars(value):
    return re.sub(r'\s+', '', value.replace('\u00ad', '-'))


def identity(path, record):
    p = ROOT / path
    if not p.is_file():
        return False
    raw = p.read_bytes()
    return (hashlib.sha256(raw).hexdigest() == record.get('sha256') or
            hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest() == record.get('sha256_normalized_lf'))


def unique(rows, key):
    result = {}
    for row in rows:
        require(row[key] not in result, 'Duplicate ' + row[key])
        result[row[key]] = row
    return result


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--draft', action='store_true')
    parser.add_argument('--tex', action='store_true')
    args = parser.parse_args()
    c = read('chapters/ch08/coverage.json')
    lex, gram = read('lexicon/entries.json'), read('curriculum/grammar.json')
    old = {'form': {r['form_id']: r for l in lex['lemmas'] for r in l['forms']},
           'sense': {r['sense_id']: r for l in lex['lemmas'] for r in l['senses']},
           'feature': {r['feature_id']: r for r in gram['features']}}
    new = {'form': unique([r for l in c['lexical_inventory'] for r in l['forms']], 'form_id'),
           'sense': unique([r for l in c['lexical_inventory'] for r in l['senses']], 'sense_id'),
           'feature': unique(c['grammar_inventory'], 'feature_id')}
    teaching = unique(c['teaching_records'], 'teaching_id')
    evidence = c['evidence_catalog']

    def record(kind, rid):
        return new[kind].get(rid, old[kind].get(rid))

    def status(kind, rid):
        if rid in new[kind]:
            return new[kind][rid]['knowledge_status']
        r = old[kind].get(rid, {})
        if r.get('production_taught_in') in PRIOR:
            return 'previously_taught'
        if r.get('recognition_taught_in') in PRIOR:
            return 'prior_recognition'
        return 'supplied' if r.get('supplied_in') else 'unresolved'

    for kind, rows in new.items():
        for rid, r in rows.items():
            require(r['knowledge_status'] in {'previously_taught','prior_recognition','new_production','new_recognition','supplied'}, rid + ': invalid scope')
            require(bool(r.get('evidence_refs')), rid + ': no evidence')
            require(bool(r.get('teaching_ids')), rid + ': no teaching location')
            for ref in r.get('evidence_refs', []):
                require(ref in evidence, rid + ': unknown evidence ' + ref)
            for ref in r.get('teaching_ids', []):
                require(ref in teaching, rid + ': unknown teaching ' + ref)
    for eid, e in evidence.items():
        images = list(e.get('images', []))
        if e.get('image'):
            images += e['image'] if isinstance(e['image'], list) else [e['image']]
        for n, image in enumerate(images):
            path = image['path'] if isinstance(image, dict) else image
            exists = (ROOT / path).is_file()
            require(exists or (eid == 'U02-DUAL' and (ROOT / e['record']).is_file()), eid + ': missing image ' + path)
            if exists and isinstance(image, dict) and image.get('sha256'):
                require(identity(path, image), eid + ': image changed')
            hashes = e.get('image_sha256')
            digest = hashes[n] if isinstance(hashes, list) and n < len(hashes) else hashes if isinstance(hashes, str) and len(images) == 1 else None
            if exists and digest:
                require(identity(path, {'sha256': digest}), eid + ': image hash differs')

    tasks = unique(c['assigned_items'], 'task_id')
    require(len(tasks) == len(c['key_item_ids']) == len(set(c['key_item_ids'])) == 66, 'Expected66distinct tasks/keys')
    require(set(c['key_item_ids']) == {t['key_id'] for t in tasks.values()}, 'Task/key crosswalk')
    cook = {r['source_item_id']: r['prompt'] for r in read('sources/audits/unit08-source/exercises-prompts.json')['items']}
    require({tid:t['prompt'] for tid,t in tasks.items() if tid.startswith('EX-')} == cook and len(cook) == 17, 'All17Cook prompts must remain exact')
    for tid, t in tasks.items():
        require(t.get('dependency_status') == 'closed', tid + ': dependencies not closed')
        for kind in new:
            required = t.get(f'required_{kind}_ids', [])
            for rid in required:
                require(status(kind, rid) != 'unresolved', tid + ': unresolved ' + rid)
            allowed = {'previously_taught', 'new_production'}
            if t['mode'] in {'analysis','reading','scaffolded_reading','scaffolded_recognition'}:
                allowed |= {'prior_recognition','new_recognition'}
            for rid in t.get(f'tested_{kind}_ids', []):
                require(rid in required and status(kind,rid) in allowed, tid + ': unlearned target ' + rid)
            for rid in t.get(f'supplied_{kind}_ids', []):
                require(rid in required, tid + ': support not in requirements ' + rid)

    def walk(value):
        if isinstance(value, dict):
            if value.get('form_id') and value.get('form'):
                r = record('form',value['form_id'])
                require(r is not None and surface(r['form']) == surface(value['form']), 'Surface/identity mismatch: '+value['form_id'])
            for child in value.values():
                walk(child)
        elif isinstance(value,list):
            for child in value:
                walk(child)
    walk(c['paradigms'])
    walk(c['display_plan'])
    matrices = c['display_plan']['matrices']
    matrix_ids = unique(matrices, 'matrix_id')
    require(len(c['paradigms']) == 27 and sum(len(p['cells']) for p in c['paradigms']) == 368,
            'Expected 27 complete logical paradigms / 368 cells')
    require(len(matrix_ids) == 36, 'Expected 36 concrete display matrices')
    expected_cells = Counter(cell['form_id'] for p in c['paradigms'] for cell in p['cells'])
    displayed_cells = Counter(fid for m in matrices if m.get('paradigm_ids')
                              for row in m['cell_form_ids'] for ids in row for fid in ids)
    require(expected_cells == displayed_cells, 'Logical-to-printed cell multiset differs')
    audit = read('sources/audits/unit08-grammar/grammar-records.json')
    audited = {p['paradigm_id']:p for p in audit['paradigms']}
    for p in c['paradigms']:
        if p['paradigm_id'] in audited:
            require([(v['form_id'],v['form']) for v in p['cells']] ==
                    [(v['form_id'],v['form']) for v in audited[p['paradigm_id']]['cells']],
                    p['paradigm_id']+': independently audited cells differ')
    for m in matrices:
        require(len(m['rows']) == len(m['cell_form_ids']), m['matrix_id']+': row mapping differs')
        for row, ids in zip(m['rows'],m['cell_form_ids']):
            require(len(row) == len(ids) == len(m['headers']), m['matrix_id']+': column mapping differs')
            for value, fids in zip(row, ids):
                for fid in fids:
                    r = record('form',fid)
                    require(r is not None and surface(r['form']) == surface(value), m['matrix_id']+': wrong cell '+fid)
    for t in tasks.values():
        walk(t.get('input_sequences',[]))
    require(len(c['new_compositions']) == 1 and len(c['new_material_examples']) == 16, 'Expected one composition/sixteen examples')
    passages = c['source_spans'] + c['new_compositions'] + c['new_material_examples']
    for p in passages:
        text = p.get('learner_text',p.get('text',''))
        tokens = p['tokens']
        require(len(text.split()) == len(tokens), 'Passage token count differs')
        for word, token in zip(text.split(),tokens):
            for fid in token.get('form_ids',[token.get('form_id')]):
                r = record('form',fid)
                require(r is not None and surface(word) == surface(r['form']), 'Passage form differs: '+str(fid))
            require(status('sense',token['sense_id']) == token['sense_status'], 'Passage sense scope differs: '+word)
    source = c['source_spans'][0]
    original = read('sources/audits/unit08-source/reading-source.json')
    for field in ['learner_text','original_notes','original_note_cue_order','change_notes']:
        if field in original:
            require(source.get(field) == original[field], 'Source changed: '+field)
    require(len(source['tokens']) == 72 and len(source['local_support']) == 12 and len(source['original_notes']) == 15, 'Expected72source tokens/12helps/15notes')
    require(len(c['new_compositions'][0]['tokens']) == 62, 'Expected62word controlled reading')
    dispositions = {}
    for n in range(1,9):
        chapter = c if n == 8 else read(f'chapters/ch{n:02}/coverage.json')
        for t in chapter['assigned_items']:
            if t['task_id'].startswith('EX-'):
                dispositions[t['task_id']] = 'assigned'
        for field, state in [('deferred_source_items','deferred'),('excluded_source_items','excluded')]:
            for item in chapter.get(field,[]):
                rid = item.get('source_item_id','')
                if rid.startswith('EX-'):
                    dispositions[rid] = state
    require(len(dispositions) == 644 and Counter(dispositions.values()) == {'assigned':130,'deferred':514}, 'Cook crosswalk must be130assigned/514deferred')
    for r in c['analysis_inputs']:
        require(identity(r['path'],r), 'Frozen analysis input changed: '+r['path'])
    for path,digest in c['prior_files'].items():
        if path not in {'lexicon/entries.json','curriculum/grammar.json'}:
            require(identity(path,{'sha256':digest,'sha256_normalized_lf':c['prior_files_lf_sha256'].get(path)}), 'Prior artifact changed: '+path)
    if args.draft or args.tex:
        student = (ROOT/'chapters/ch08/student.md').read_text(encoding='utf-8')
        key = (ROOT/'chapters/ch08/answer-key.md').read_text(encoding='utf-8')
        for label, text in [('student',student),('key',key)]:
            require(text == unicodedata.normalize('NFC',text), label + ': non-NFC text')
        for m in matrices:
            hits = list(re.finditer(r'<!--\s*table:\s*'+re.escape(m['matrix_id'])+r'\s*-->',student))
            require(len(hits) == 1, m['matrix_id']+': matrix marker missing/repeated')
            if len(hits) == 1:
                block = re.match(r'\s*(\|[^\n]+(?:\n\|[^\n]+)*)',student[hits[0].end():])
                require(block is not None, m['matrix_id']+': no adjacent actual table')
                if block:
                    rows = [[v.strip().replace('**','') for v in line.strip().strip('|').split('|')] for line in block[1].splitlines()]
                    require([rows[0]]+rows[2:] == [m['headers']]+m['rows'],m['matrix_id']+': actual labels/forms differ')
        for tid,t in tasks.items():
            hits = list(re.finditer(r'<!--\s*(?:item:\s*)?'+re.escape(tid)+r'\s*-->',student))
            require(len(hits) == 1, tid + ': learner marker missing/repeated')
            if len(hits) == 1:
                prompt = student[hits[0].end():].strip().split('\n\n')[0]
                prompt = re.sub(r'^\d+\.\s*','',prompt)
                require(prompt == t['prompt'],tid+': actual prompt differs')
            require(len(re.findall(r'<!--\s*(?:key:\s*)?'+re.escape(t['key_id'])+r'\s*-->',key)) == 1,tid+': key marker missing/repeated')
        for tid in teaching:
            require(tid in student,tid+': teaching marker missing')
        for p in passages:
            if p.get('speaker_turns'):
                positions = []
                for turn in p['speaker_turns']:
                    value = turn['source_label']+' '+turn['text']
                    positions.append(student.replace('**','').find(value))
                require(all(n >= 0 for n in positions) and positions == sorted(positions), 'Exact ordered source dialogue/speaker labels missing')
            else:
                require(p.get('learner_text',p.get('text','')) in student.replace('**',''), 'Exact passage/example missing')
        for note in source['original_notes']:
            require(note['text'] in student.replace('**',''),'Original note missing')
    if args.tex:
        folder = ROOT/'typesetting/ch08'
        for stem,ids in [('chapter-08',list(tasks)),('answer-key',c['key_item_ids'])]:
            tex = (folder/(stem+'.tex')).read_text(encoding='utf-8')
            pdftext = (folder/'build'/(stem+'.txt')).read_text(encoding='utf-8')
            log = (folder/'build'/(stem+'.log')).read_text(encoding='utf-8',errors='replace')
            require((folder/(stem+'.pdf')).is_file(),stem+': retained PDF missing')
            for tid in ids:
                require(tid in tex,tid+': TeX marker missing')
            for warning in ['Missing character:','Overfull \\hbox','Overfull \\vbox','Underfull \\hbox','Underfull \\vbox','Font shape','Rerun to get','Table widths have changed']:
                require(warning not in log,stem+': '+warning)
            if stem == 'chapter-08':
                for t in tasks.values():
                    require(chars(t['prompt']) in chars(pdftext),t['task_id']+': PDF prompt differs')
    if ERRORS:
        print('\n'.join('ERROR: '+e for e in ERRORS))
        raise SystemExit(1)
    print('Unit8 checks pass:66tasks,17exact Cook prompts,62word controlled reading,72word source/15notes/12helps; dependencies, evidence and earlier artifacts preserved.')


if __name__ == '__main__':
    main()
