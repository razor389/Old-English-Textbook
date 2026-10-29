"""Repeatable Unit 1 source/contract/content checks; linguistic and page review remain human tasks."""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--chapter', default='ch01', choices=['ch01'], help='this concrete check currently covers Unit 1')
parser.add_argument('--draft', action='store_true', help='also check complete Markdown and keys')
parser.add_argument('--tex', action='store_true', help='also check TeX IDs and extracted PDF text')
args = parser.parse_args()
errors = []

def check(ok, message):
    if not ok:
        errors.append(message)

def read_json(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))

def clean(text):
    text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    text = re.sub(r'^\s*>\s?', '', text, flags=re.M)
    text = text.replace('**', '').replace('`', '')
    return ' '.join(text.split())

def unique(values, label):
    check(len(values) == len(set(values)), 'Duplicate ' + label)

chapter = ROOT / 'chapters' / args.chapter
c = read_json(chapter / 'coverage.json')
tasks = c['assigned_items']
taskids = [t['item_id'] for t in tasks]
keyids = [t['key_item_id'] for t in tasks]
reqs = c['requirements']
unique(taskids, 'task IDs')
unique(keyids, 'key IDs')
unique([r['requirement_id'] for r in reqs], 'requirement IDs')
check(set(keyids) == set(c['key_item_ids']), 'Contract key list differs from assigned tasks')
form_records = [f for l in c['lexical_inventory'] for f in l['forms']]
sense_records = [s for l in c['lexical_inventory'] for s in l['senses']]
unique([l['lemma_id'] for l in c['lexical_inventory']], 'lemma IDs')
unique([f['form_id'] for f in form_records], 'form IDs')
unique([s['sense_id'] for s in sense_records], 'sense IDs')
unique([f['feature_id'] for f in c['grammar_inventory']], 'feature IDs')
forms = {f['form_id']: f for f in form_records}
senses = {s['sense_id']: s for s in sense_records}
features = {f['feature_id']: f for f in c['grammar_inventory']}
teachids = {t['teaching_id'] for t in c['teaching_records']}
for t in tasks:
    for field, records in [('required_form_ids', forms), ('required_sense_ids', senses), ('required_feature_ids', features)]:
        check(set(t.get(field, [])) <= records.keys(), t['item_id'] + ': unresolved ' + field)
    for fid in t.get('tested_form_ids', []):
        check(forms.get(fid, {}).get('knowledge_status') == 'new_production', t['item_id'] + ': unprepared production ' + fid)
    if t['kind'] == 'independent_production':
        check(not t.get('supplied_form_ids'), t['item_id'] + ': supplied form in independent production')
        for sid in t['required_sense_ids']:
            check(senses[sid]['knowledge_status'] == 'new_production', t['item_id'] + ': unprepared sense ' + sid)
        for fid in t['required_feature_ids']:
            check(features[fid]['knowledge_status'] == 'new_production', t['item_id'] + ': unprepared construction ' + fid)
for r in reqs:
    check(r['knowledge_status'] not in ('unresolved', 'previously_taught'), r['requirement_id'] + ': unexpected prior/unresolved status')
    check(set(r['evidence_refs']) <= c['evidence_catalog'].keys(), r['requirement_id'] + ': unresolved evidence')
    check(set(r['coverage_location']['teaching_ids']) <= teachids, r['requirement_id'] + ': unresolved teaching location')
    check(set(r['item_ids']) <= set(taskids), r['requirement_id'] + ': unresolved task')
def evidence_paths(value):
    if isinstance(value, dict):
        for child in value.values():
            yield from evidence_paths(child)
    elif isinstance(value, list):
        for child in value:
            yield from evidence_paths(child)
    elif isinstance(value, str) and value.startswith(('sources/', 'reference/')) and Path(value).suffix in ('.png', '.jpg', '.md', '.json', '.txt'):
        yield value

for evidence_id, record in c['evidence_catalog'].items():
    for p in evidence_paths(record):
        check((ROOT / p).exists(), evidence_id + ': missing evidence path ' + p)
unique([e['example_id'] for e in c['new_material_examples']], 'example IDs')
for example in c['new_material_examples']:
    for field, records in [('required_form_ids', forms), ('required_sense_ids', senses), ('required_feature_ids', features)]:
        check(set(example[field]) <= records.keys(), example['example_id'] + ': unresolved ' + field)
    check(set(example['evidence_refs']) <= c['evidence_catalog'].keys(), example['example_id'] + ': unresolved evidence')
    for fid in example['required_form_ids']:
        check(forms[fid]['knowledge_status'] == 'new_production' or fid in example['supplied_form_ids'], example['example_id'] + ': unsupported form ' + fid)
        match = next((r for r in reqs if r.get('form_id') == fid), {})
        check(example['example_id'] in match.get('example_ids', []), example['example_id'] + ': missing reciprocal form link ' + fid)

# A reference-only reconstruction must never quietly acquire an assessment or milestone.
sea = forms['sae-gen-pl']
check(sea['form'] == '*sǣwa' and sea['knowledge_status'] == 'supplied', 'Sea reconstruction status changed')
check(not sea.get('proposed_production_taught_in') and not sea.get('proposed_recognition_taught_in'), 'Sea reconstruction has proposed learning milestone')
check(all('sae-gen-pl' not in t['required_form_ids'] for t in tasks), 'Sea reconstruction is assessed')

# Independently reconstruct the 644 source IDs from the checked structural inventory.
inventory = read_json('sources/audits/course-map/inventory.json')
expected = {(e['group'], e['exercise'], n) for e in inventory['exercises'] for n in range(1,e['item_count']+1)}
dispositions = []
for t in tasks + c['deferred_source_items'] + c['excluded_source_items']:
    loc = t.get('source_locator', {})
    if loc.get('source_id') == 'cook_ex_1895':
        dispositions.append((loc['original_group'], loc['exercise_number'], loc['item_number']))
check(set(dispositions) == expected, 'Incomplete Cook item crosswalk')
unique(dispositions, 'Cook dispositions')

source_files = [
    ROOT / 'sources/transcriptions/cook-ex-01.md',
    ROOT / 'sources/transcriptions/cook-ex-02.md',
    ROOT / 'sources/audits/unit01-source/exercise-3.md',
]
for exercise, path in enumerate(source_files, 1):
    text = path.read_text(encoding='utf-8')
    source_prompts = dict(re.findall(r'^([0-9]+)\.\s+(.+?)\s*$', text, re.M))
    for t in tasks:
        loc = t.get('source_locator', {})
        if loc.get('source_id') == 'cook_ex_1895' and loc.get('exercise_number') == exercise:
            check(source_prompts.get(str(loc['item_number'])) == t['prompt'], t['item_id'] + ': source prompt mismatch')

reading = c['source_spans'][0]
check(reading['source_text'].split() == [t['source_token'] for t in reading['tokens']], 'Reading token map differs from source span')
for token in reading['tokens']:
    check(token['form_id'] in forms and token['sense_id'] in senses, 'Reading token has unresolved lexical reference')
for path in list(chapter.glob('*.md')) + list(chapter.glob('*.json')):
    text = path.read_text(encoding='utf-8')
    check(text == unicodedata.normalize('NFC', text), 'Non-NFC file ' + str(path.relative_to(ROOT)))

if args.draft:
    student = (chapter / 'student.md').read_text(encoding='utf-8')
    key = (chapter / 'answer-key.md').read_text(encoding='utf-8')
    student_ids = re.findall(r'<!--\s*item:\s*([^\s>]+)\s*-->', student)
    key_ids = re.findall(r'<!--\s*key:\s*([^\s>]+)\s*-->', key)
    unique(student_ids, 'learner item comments')
    unique(key_ids, 'key comments')
    check(set(student_ids) == set(taskids), 'Learner task IDs differ: missing=' + str(sorted(set(taskids)-set(student_ids))) + '; extra=' + str(sorted(set(student_ids)-set(taskids))))
    check(set(key_ids) == set(keyids), 'Key IDs differ: missing=' + str(sorted(set(keyids)-set(key_ids))) + '; extra=' + str(sorted(set(key_ids)-set(keyids))))
    comments = ' '.join(re.findall(r'<!--(.*?)-->', student, flags=re.S))
    for tid in teachids:
        check(tid in comments, 'Missing teaching location ' + tid)
    plain = clean(student)
    for t in tasks:
        if t['origin'] == 'exact_source':
            check(t['prompt'] in plain, 'Missing exact learner prompt ' + t['item_id'])
    check(clean(reading['source_text']) in plain, 'Learner reading differs from the exact display span')
    for example in c['new_material_examples']:
        check(example['example_id'] in comments, 'Missing example ID ' + example['example_id'])
        check(clean(example['text']) in plain, 'Missing illustrative example ' + example['example_id'])

if args.tex:
    out = ROOT / 'typesetting' / args.chapter
    for stem, expected_ids in [('chapter-01', taskids), ('answer-key', keyids)]:
        tex = (out / (stem + '.tex')).read_text(encoding='utf-8')
        for item_id in expected_ids:
            check(item_id in tex, stem + ': missing TeX ID ' + item_id)
        pdftext = clean((out / 'build' / (stem + '.txt')).read_text(encoding='utf-8'))
        if stem == 'chapter-01':
            for t in tasks:
                if t['origin'] == 'exact_source':
                    check(t['prompt'] in pdftext, 'PDF missing exact prompt ' + t['item_id'])
            # Xpdf 4.00 inserts spaces after some macrons in this Cambria PDF.
            # Compare every Unicode character except whitespace; the separate
            # page review must verify actual word boundaries and the intact span.
            reading_chars = re.sub(r'\s+', '', clean(reading['source_text']))
            pdf_chars = re.sub(r'\s+', '', pdftext)
            check(reading_chars in pdf_chars, 'PDF reading characters differ or the span is interrupted')
        log = (out / 'build' / (stem + '.log')).read_text(encoding='utf-8', errors='replace')
        for warning in ['Missing character:', 'Overfull \\hbox', 'Overfull \\vbox', 'Underfull \\hbox', 'Underfull \\vbox', 'Font shape']:
            check(warning not in log, stem + ': log contains ' + warning)

if errors:
    print('\n'.join('ERROR: ' + e for e in errors))
    sys.exit(1)
print(f'{args.chapter}: PASS — {len(tasks)} tasks, {len(forms)} forms, {len(senses)} senses, {len(features)} constructions; {len(dispositions)} Cook dispositions; source and reference checks.')
print('Structural checks only. Independent linguistic and page-by-page visual review remain required.')
