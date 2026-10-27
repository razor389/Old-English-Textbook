"""Check the actual learner master against the committed Unit16 contract."""
import hashlib
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
C = json.loads((ROOT / 'chapters/ch16/coverage.json').read_text(encoding='utf-8'))
P = ROOT / 'chapters/ch16/student.md'
text = P.read_text(encoding='utf-8')
errors = []
def need(ok, message):
    if not ok:
        errors.append(message)
need(text == unicodedata.normalize('NFC', text), 'Unicode normalization')
for teaching in C['teaching_records']:
    marker = '<!-- teaching: ' + teaching['teaching_id'] + ' -->'
    need(text.count(marker) == 1, 'Teaching location: ' + teaching['teaching_id'])
for matrix in C['display_plan']['matrices']:
    marker = '<!-- table: ' + matrix['matrix_id'] + ' -->'
    need(text.count(marker) == 1, 'Table marker: ' + matrix['matrix_id'])
    match = re.match(r'\s*(\|[^\n]+(?:\n\|[^\n]+)*)', text.split(marker,1)[1]) if marker in text else None
    need(bool(match), 'Literal table: ' + matrix['matrix_id'])
    if match:
        rows = [[cell.strip().replace('**','') for cell in line.strip().strip('|').split('|')] for line in match[1].splitlines()]
        need([rows[0]] + rows[2:] == [matrix['headers']] + matrix['rows'], 'Table content: ' + matrix['matrix_id'])
forms = {f['form_id']: f for l in C['lexical_inventory'] for f in l['forms']}
senses = {s['sense_id']: s for l in C['lexical_inventory'] for s in l['senses']}
features = {f['feature_id']: f for f in C['grammar_inventory']}
ordered_inputs = 0
for task in C['assigned_items']:
    tid = task['task_id']; marker = '<!-- item: ' + tid + ' -->'
    need(text.count(marker) == 1, 'Item marker: ' + tid)
    if marker not in text:
        continue
    tail = text.split(marker,1)[1]
    need(tail.strip().split('\n\n',1)[0] == task['prompt'], 'Prompt: ' + tid)
    body = tail.split('<!-- item:',1)[0].replace('**','')
    cursor = 0
    for sequence in task['input_sequences']:
        at = body.find(sequence['text'],cursor)
        need(at >= 0, 'Ordered input: ' + tid + ': ' + sequence['text'])
        cursor = max(cursor, at + len(sequence['text']))
        ordered_inputs += 1
    for position in task['output_positions']:
        need(text.count('<!-- output: ' + position['output_position_id'] + ' -->') == 1, 'Output marker: ' + position['output_position_id'])
    for kind, records in [('form', forms), ('sense', senses), ('feature', features)]:
        for rid in task.get('tested_' + kind + '_ids', []):
            record = records[rid]
            if record['knowledge_status'] in {'new_production','new_recognition'}:
                need(any(0 <= text.find('<!-- teaching: ' + x + ' -->') < text.index(marker) for x in record['teaching_ids']), 'Teaching order: ' + tid + ': ' + rid)
plain = re.sub(r'\[\^[^\]]+\]', '', text).replace('**','')
for example in C['new_material_examples']:
    need(example['text'] in plain and example['translation'] in text, 'Translated example: ' + example['example_id'])
reading = C['source_spans'][0]
need(reading['learner_text'] in plain, 'Complete exact reading')
for note in reading['original_notes']:
    need('[^' + note['display_id'] + ']: ' + note['original_text'] in text, 'Original note: ' + note['display_id'])
source_body = text.split('<!-- passage: ' + reading['source_span_id'] + ' -->',1)[1].split('### Original notes',1)[0]
need(len(re.findall(r'\[\^P(?:168|169|170)N\d+\]', source_body)) == 59, 'Original note anchor count')
need(len(re.sub(r'\[\^[^\]]+\]', '', source_body).split()) == 444, 'Source word count')
report = {'schema_version':1, 'chapter':'ch16', 'status':'pass' if not errors else 'fail',
    'student_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),
    'coverage_sha256':hashlib.sha256((ROOT/'chapters/ch16/coverage.json').read_bytes()).hexdigest(),
    'counts':{'tasks':len(C['assigned_items']), 'output_positions':sum(len(t['output_positions']) for t in C['assigned_items']),
        'teaching_locations':len(C['teaching_records']), 'tables':len(C['display_plan']['matrices']),
        'ordered_input_sequences':ordered_inputs,'reading_words':444,'original_notes':54,'original_note_anchors':59},
    'errors':errors,
    'scope':'Actual marker, prompt, literal table, translated example, source/apparatus, ordered input and teaching-order check. Linguistic and learner-sufficiency review remains independent.'}
(ROOT/'build/u16-learner-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
