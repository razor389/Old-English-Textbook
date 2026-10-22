"""Concrete Unit 2 contract/text checks; linguistic and visual review remain separate."""
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
def cleaned(s):
    return s.strip('.,:;!?“”‘’"()').casefold()

def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--draft', action='store_true')
    parser.add_argument('--tex', action='store_true', help='Check complete TeX IDs, extracted PDF content and clean LuaLaTeX logs')
    args = parser.parse_args()
    c = read('chapters/ch02/coverage.json')
    lex = read('lexicon/entries.json')
    grammar = read('curriculum/grammar.json')
    old_forms = {f['form_id']: f for l in lex['lemmas'] for f in l['forms']}
    old_senses = {s['sense_id']: s for l in lex['lemmas'] for s in l['senses']}
    old_features = {f['feature_id']: f for f in grammar['features']}
    forms = unique([f for l in c['lexical_inventory'] for f in l['forms']], 'form_id', 'form')
    senses = unique([s for l in c['lexical_inventory'] for s in l['senses']], 'sense_id', 'sense')
    features = unique(c['grammar_inventory'], 'feature_id', 'feature')
    maps = {'form': (forms, old_forms), 'sense': (senses, old_senses), 'feature': (features, old_features)}
    evidence = c['evidence_catalog']
    teaching = unique(c['teaching_records'], 'teaching_id', 'teaching record')
    def status(kind, item):
        new, old = maps[kind]
        if item in new:
            return new[item]['knowledge_status']
        if item in old and old[item].get('production_taught_in') == 'ch01':
            return 'previously_taught'
        if item in old and old[item].get('recognition_taught_in') == 'ch01':
            return 'prior_recognition'
        return 'unresolved'
    for kind, (new, old) in maps.items():
        for item, rec in new.items():
            require(rec['knowledge_status'] in {'previously_taught','new_production','new_recognition','supplied'}, f'{item}: invalid knowledge status')
            require(bool(rec.get('evidence_refs')), f'{item}: no evidence')
            for ref in rec.get('evidence_refs', []):
                require(ref in evidence, f'{item}: unknown evidence {ref}')
            require(bool(rec.get('teaching_ids')), f'{item}: no teaching/support location')
            for ref in rec.get('teaching_ids', []):
                require(ref in teaching, f'{item}: unknown teaching record {ref}')
    for ref, rec in evidence.items():
        for path in rec.get('images', []):
            retained_or_recorded = (ROOT / path).is_file() or (ref=='U02-DUAL' and (ROOT / rec['record']).is_file())
            require(retained_or_recorded, f'{ref}: missing image {path}')
        if rec.get('image'):
            paths = rec['image'] if isinstance(rec['image'], list) else [rec['image']]
            for path in paths:
                require((ROOT / path).is_file(), f'{ref}: missing image {path}')
    tasks = unique(c['assigned_items'], 'task_id', 'task')
    require(len(tasks) == 61, 'Expected61 graded tasks')
    require(len(set(c['key_item_ids'])) == 61, 'Expected61 unique key IDs')
    require(set(c['key_item_ids']) == {t['key_id'] for t in tasks.values()}, 'Task/key crosswalk differs')
    for tid, task in tasks.items():
        require(bool(task['prompt']), f'{tid}: empty prompt')
        require('awaiting' not in task.get('dependency_status','').lower() and 'unresolved' not in task.get('dependency_status','').lower(), f'{tid}: unresolved dependencies')
        for kind in maps:
            required = task.get(f'required_{kind}_ids', [])
            tested = task.get(f'tested_{kind}_ids', [])
            require(bool(required), f'{tid}: no {kind} dependencies')
            for item in required:
                require(status(kind,item) != 'unresolved', f'{tid}: unresolved {kind} {item}')
            for item in tested:
                require(item in required, f'{tid}: tested {kind} outside requirements: {item}')
                permitted = {'previously_taught','new_production'} if task['mode'] in {'production','composition'} else {'previously_taught','prior_recognition','new_production','new_recognition'}
                require(status(kind,item) in permitted, f'{tid}: unlearned independently tested {kind} {item}')
        if task['mode'] in {'production','composition'}:
            require(bool(task.get('tested_form_ids')), f'{tid}: production task has no tested forms')
        for item in task.get('supplied_form_ids',[]):
            require(item in task['required_form_ids'], f'{tid}: supplied form outside requirements {item}')
    verb_paradigms = [p for p in c['paradigms'] if 'finite_form_ids' in p]
    require(len(verb_paradigms) == 23, 'Expected23 verb paradigms')
    expected = {(tense,person,number) for tense in ['present','preterite'] for person in [1,2,3] for number in ['singular','plural']}
    for p in verb_paradigms:
        rows = [forms[i] for i in p['finite_form_ids']]
        require(len(rows) == 12, f'{p["lemma_id"]}: incomplete finite paradigm')
        require({(f['analysis']['tense'],f['analysis']['person'],f['analysis']['number']) for f in rows} == expected, f'{p["lemma_id"]}: finite cells differ')
        require(len(p['surface_row']) == 7, f'{p["lemma_id"]}: incomplete surface row')
        for f in rows:
            require(f['knowledge_status'] == ('new_recognition' if p['lemma_id']=='nabban' else 'new_production'), f'{f["form_id"]}: wrong finite scope')
    pronouns = [f for l in c['lexical_inventory'] if l['lemma_id'] in {'ic','thu','he'} for f in l['forms']]
    require(len(pronouns) == 40, 'Expected40 pronoun cells')
    require(sum(f['knowledge_status']=='new_recognition' for f in pronouns)==6, 'Expected6 recognition-only personal genitives')
    for f in pronouns:
        if f['knowledge_status']=='new_recognition':
            require(f['analysis']['case']=='genitive' and f['analysis']['person'] in [1,2], f'{f["form_id"]}: wrong pronoun boundary')
    require(len(c['new_compositions'])==2 and len(c['new_material_examples'])==8, 'Connected-text/example count differs')
    alltexts = c['source_spans'] + c['new_compositions'] + c['new_material_examples']
    for passage in alltexts:
        pid = passage.get('source_record_id', passage.get('composition_id', passage.get('example_id')))
        text = passage.get('source_text', passage.get('text',''))
        tokens = passage['tokens']
        require(len(text.split())==len(tokens), f'{pid}: token count differs')
        for word, token in zip(text.split(), tokens):
            require(word==token.get('source_token',token.get('token')), f'{pid}: token text differs')
            for kind in ['form','sense']:
                item=token[f'{kind}_id']
                require(status(kind,item)==token[f'{kind}_status'], f'{pid}: {item} token status differs: {status(kind,item)} / {token[f"{kind}_status"]}')
            rec = forms.get(token['form_id'], old_forms.get(token['form_id']))
            require(rec is not None and cleaned(word)==cleaned(rec['form']), f'{pid}: token surface mismatches {token["form_id"]}: {word}')
    source = c['source_spans'][0]
    require(source['word_count']==61 and len(source['tokens'])==61, 'Sabbath word count differs')
    faithful = ' '.join((ROOT/'sources/audits/unit02-reading/source-text.txt').read_text(encoding='utf-8').split())
    require(source['source_text']==faithful, 'Sabbath differs from audited transcription')
    carry = c['source_assignment_policy']
    prior_bytes=(ROOT/carry['carry_forward_contract']).read_bytes()
    require(hashlib.sha256(prior_bytes).hexdigest()==carry['carry_forward_sha256'] or hashlib.sha256(prior_bytes.replace(b'\r\n',b'\n')).hexdigest()==carry.get('carry_forward_lf_sha256'), 'Prior contract changed')
    require(carry['new_cook_assignments']==[] and carry['resolved_prior_deferral_ids']==[], 'Unexpected changed Cook assignments/deferrals')
    for path in ['chapters/ch01/student.md','chapters/ch01/answer-key.md']:
        prior_bytes=(ROOT/path).read_bytes()
        require(hashlib.sha256(prior_bytes).hexdigest()==c['prior_files'][path] or hashlib.sha256(prior_bytes.replace(b'\r\n',b'\n')).hexdigest()==c.get('prior_files_lf_sha256',{}).get(path), f'Unit1 text changed: {path}')
    for path in ['chapters/ch02/coverage.json'] + (['chapters/ch02/student.md','chapters/ch02/answer-key.md'] if args.draft else []):
        raw=(ROOT/path).read_text(encoding='utf-8')
        require(raw==unicodedata.normalize('NFC',raw), f'{path}: non-NFC text')
    if args.draft or args.tex:
        student=(ROOT/'chapters/ch02/student.md').read_text(encoding='utf-8')
        key=(ROOT/'chapters/ch02/answer-key.md').read_text(encoding='utf-8')
        parts=re.split(r'<!--\s*(?:item:\s*)?(NEW-U02-[A-Z][0-9]+)\s*-->',student)
        prompts={parts[i]: re.sub(r'^\d+\.\s*','',parts[i+1].strip().split('\n\n')[0]) for i in range(1,len(parts),2)}
        table_rows=[[cell.strip().replace('**','') for cell in line.strip().strip('|').split('|')] for line in student.splitlines() if line.startswith('|')]
        for tid, task in tasks.items():
            require(len(re.findall(r'<!--\s*(?:item:\s*)?'+re.escape(tid)+r'\s*-->',student))==1, f'{tid}: learner ID not present exactly once')
            require(len(re.findall(r'<!--\s*(?:key:\s*)?'+re.escape(task['key_id'])+r'\s*-->',key))==1, f'{tid}: key ID not present exactly once')
            require(prompts.get(tid)==task['prompt'], f'{tid}: prompt differs from saved contract')
        for tid in teaching:
            require(tid in student, f'{tid}: teaching location missing from learner')
        for passage in alltexts:
            texts=[turn['text'] for turn in passage['turns']] if passage.get('turns') else [passage.get('source_text',passage.get('text',''))]
            plain=re.sub(r'\*\*|(?<!\w)\*(?!\s)|(?<!\s)\*(?!\w)', '', student)
            for text in texts:
                require(text in plain, f'{passage.get("reading_id",passage.get("composition_id",passage.get("example_id")))}: exact text missing from learner')
        for p in verb_paradigms:
            head=next(l['display_headword'] for l in c['lexical_inventory'] if l['lemma_id']==p['lemma_id'])
            require([head]+p['surface_row'] in table_rows, f'{p["lemma_id"]}: complete selected table row missing or misplaced')
            require([part['display'] for part in p['principal_parts']] in table_rows, f'{p["lemma_id"]}: principal-part row missing')
            for form in p['surface_row']:
                require(form in student, f'{p["lemma_id"]}: {form} missing from learner')
        for f in pronouns:
            require(f['form'] in student, f'{f["form_id"]}: pronoun missing from learner')
    if args.tex:
        def chars(text): return re.sub(r'\s+','',text)
        for stem,ids in [('chapter-02',list(tasks)),('answer-key',c['key_item_ids'])]:
            folder=ROOT/'typesetting/ch02'
            tex=(folder/(stem+'.tex')).read_text(encoding='utf-8')
            pdftext=(folder/'build'/(stem+'.txt')).read_text(encoding='utf-8')
            # Xpdf 4.00 encodes these visibly printed literal hyphens as U+00AD.
            # Preserve the hyphen in character checks; do not discard it.
            pdftext=pdftext.replace('\u00ad','-')
            log=(folder/'build'/(stem+'.log')).read_text(encoding='utf-8',errors='replace')
            require((folder/(stem+'.pdf')).is_file(), f'{stem}: final PDF absent')
            for tid in ids:
                require(tid in tex,f'{stem}: missing TeX task/key ID {tid}')
            for warning in ['Missing character:', 'Overfull \\hbox', 'Overfull \\vbox', 'Underfull \\hbox', 'Underfull \\vbox', 'Font shape', 'Rerun to get', 'Table widths have changed']:
                require(warning not in log,f'{stem}: log contains {warning}')
            if stem=='chapter-02':
                for tid in teaching: require(tid in tex,f'{tid}: missing TeX teaching ID')
                for tid,task in tasks.items():
                    require(chars(task['prompt']) in chars(pdftext),f'{tid}: PDF prompt characters differ or prompt split by running matter')
                for passage in alltexts:
                    texts=[turn['text'] for turn in passage['turns']] if passage.get('turns') else [passage.get('source_text',passage.get('text',''))]
                    for text in texts:
                        require(chars(text) in chars(pdftext),'PDF exact reading/example characters differ or interrupted')
    if errors:
        print('\n'.join('ERROR: '+e for e in errors))
        raise SystemExit(1)
    print(f'Unit2 checks pass: {len(tasks)} tasks;23 complete verb paradigms;40 pronoun cells;61 source tokens;2 connected texts;8 examples.' + (' Learner/key structural parity checked.' if args.draft or args.tex else ' Contract only.') + (' TeX/PDF character and log checks pass.' if args.tex else ''))

if __name__=='__main__':
    main()
