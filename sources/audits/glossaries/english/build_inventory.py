"""Reproducible item-level English lookup audit of the accepted course.

This reads current contracts/learner/key masters, not draft source inventories.
It deliberately keeps the accepted semantic labels intact: indexes are curated
separately rather than treating punctuation in a gloss as linguistic analysis.
"""
import collections
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / 'sources/audits/glossaries/english'
BUILD = ROOT / 'build/glossary-en'
BUILD.mkdir(parents=True, exist_ok=True)

def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))

def write(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def spans(path):
    text = (ROOT / path).read_text(encoding='utf-8-sig')
    marker = r'<!--\s*key:\s*KEY-([^\s>]+)\s*-->' if path.endswith('answer-key.md') else r'<!--\s*item:\s*([^\s>]+)\s*-->'
    found = list(re.finditer(marker, text))
    result = {}
    for n, match in enumerate(found):
        end = found[n+1].start() if n+1 < len(found) else len(text)
        block = text[match.end():end].strip()
        result[match.group(1)] = {'path':path, 'line':text.count('\n',0,match.start())+1, 'text':block}
    return result

def unique(values):
    return list(dict.fromkeys(values))

lex = read('lexicon/entries.json')
senses = {}
forms = {}
for lemma in lex['lemmas']:
    for sense in lemma.get('senses',[]):
        senses[sense['sense_id']] = (lemma,sense)
    for form in lemma.get('forms',[]):
        forms[form['form_id']] = (lemma,form)

items = []
counts = []
used = collections.defaultdict(list)
unresolved = []
input_hashes = {}
for contract in sorted((ROOT / 'chapters').glob('ch*/coverage.json')):
    relative = contract.relative_to(ROOT).as_posix()
    data = read(relative)
    chapter = data['chapter_id']
    student_path = f'chapters/{chapter}/student.md'
    key_path = f'chapters/{chapter}/answer-key.md'
    student = spans(student_path)
    key = spans(key_path)
    for p in [relative,student_path,key_path]:
        input_hashes[p] = hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
    for task in data['assigned_items']:
        task_id = task['task_id']
        output_records = task.get('output_positions',[])
        output_senses = unique(task.get('required_output_sense_ids',[]) +
            [s for output in output_records for s in output.get('required_output_sense_ids',[])])
        required_senses = unique(task.get('required_sense_ids',[]) + output_senses +
            [s for output in output_records for s in output.get('required_sense_ids',[])])
        mode = task.get('mode',task.get('kind',task.get('task_type','')))
        if task_id.startswith('EX-'):
            scope = 'english_to_old_english_source_translation'
        elif output_records:
            kinds = ' '.join(str(o.get('kind','')) + ' ' + str(o.get('response_language','')) for o in output_records).lower()
            scope = 'mixed_or_old_english_output' if ('old_english' in kinds or 'old english' in kinds or 'form' in kinds) else 'english_analysis_or_translation_of_old_english'
        elif re.search(r'production|composition|transformation',mode):
            scope = 'old_english_production_or_morphology'
        else:
            scope = 'english_analysis_or_translation_of_old_english'
        record = {
            'task_id':task_id, 'chapter_id':chapter, 'contract':relative,
            'kind':scope, 'original_mode':mode, 'prompt':task['prompt'],
            'student':{k:v for k,v in student.get(task_id,{}).items() if k!='text'},
            'key':{k:v for k,v in key.get(task_id,{}).items() if k!='text'},
            'key_item_id':task.get('key_item_id',task.get('key_id')),
            'required_sense_ids':required_senses,
            'required_output_sense_ids':output_senses,
            'supplied_sense_ids':task.get('supplied_sense_ids',[]),
            'required_feature_ids':task.get('required_feature_ids',[]),
        }
        for field in ['source_locator','source_locators','source_metadata','source_record','source','source_control_records','source_control_guidance','source_control_strings','source_instructions','source_instruction_refs','source_route_note','correction_ids','local_support','supplied_support','editorial_directions','learner_directions','target_specification','lexical_frame_ids','lexical_frame_requirements','lexical_sense_demands']:
            if task.get(field):
                record[field]=task[field]
        if task.get('source_original_id'):
            record['source_original_id']=task['source_original_id']
        if output_records:
            record['outputs']=[{k:v for k,v in output.items() if k in ['output_position_id','output_id','kind','label','response_language','required_sense_ids','required_input_sense_ids','required_output_sense_ids','supplied_sense_ids','tested_sense_ids','essential_meaning']} for output in output_records]
        if not record['student'] or not record['key']:
            unresolved.append({'task_id':task_id,'problem':'missing accepted-master item marker','student':bool(record['student']),'key':bool(record['key'])})
        items.append(record)
        for sense_id in required_senses:
            used[sense_id].append({'task_id':task_id,'role':'old_english_output' if sense_id in output_senses else scope,'supplied':sense_id in task.get('supplied_sense_ids',[])})
    counts.append({'chapter_id':chapter,'tasks':len(data['assigned_items']),'cook_items':sum(i['task_id'].startswith('EX-') for i in data['assigned_items'])})

pron = read('guides/pronunciation/coverage.json')
for group in pron['practice']:
    for subtask in group['items']:
        items.append({'task_id':subtask['id'],'chapter_id':'pronunciation','contract':'guides/pronunciation/coverage.json','kind':'pronunciation_only_no_english_to_old_english_requirement','prompt':group['prompt_type'],'input':subtask,'required_sense_ids':[],'exclusion_reason':'All Old English examples and meanings are supplied; the learner answers sound questions in English. Instructional words are not translation vocabulary.'})

sense_uses=[]
for sense_id, occurrences in sorted(used.items()):
    if sense_id not in senses:
        unresolved.append({'sense_id':sense_id,'problem':'required sense absent from register'})
        continue
    lemma,sense=senses[sense_id]
    entry={'sense_id':sense_id,'lemma_id':lemma['lemma_id'],'headword':lemma['display_headword'],'part_of_speech':lemma['part_of_speech'],'gloss':sense['gloss'],
           'used_in_tasks':[o['task_id'] for o in occurrences], 'old_english_output_task_ids':[o['task_id'] for o in occurrences if o['role'] in ['old_english_output','english_to_old_english_source_translation','old_english_production_or_morphology','mixed_or_old_english_output']],
           'supplied_task_ids':[o['task_id'] for o in occurrences if o['supplied']], 'evidence_refs':sense.get('evidence_refs',[])}
    for field in ['gender','verb_class','declension_model']:
        if lemma.get(field): entry[field]=lemma[field]
    for field in ['scope_note','usage_note','notes','production_taught_in','recognition_taught_in','supplied_in']:
        if sense.get(field) is not None:entry[field]=sense[field]
    sense_uses.append(entry)

summary={'schema_version':1,'scope':'All current assigned chapter tasks plus every numbered pronunciation response. English instructions and key exposition are not translation vocabulary.',
         'counts':{'chapter_tasks':sum(c['tasks'] for c in counts),'cook_items':sum(c['cook_items'] for c in counts),'original_chapter_tasks':sum(c['tasks']-c['cook_items'] for c in counts),'pronunciation_responses':sum(len(g['items']) for g in pron['practice']), 'exercise_senses':len(sense_uses),'exercise_lemmas':len(set(s['lemma_id'] for s in sense_uses))},
         'chapter_counts':counts,'unresolved':unresolved,'input_sha256':input_hashes}
write('exercise-inventory.json',{'schema_version':1,'items':items})
write('sense-use-crosswalk.json',{'schema_version':1,'senses':sense_uses})
write('inventory-summary.json',summary)
(BUILD/'cook-prompts.txt').write_text('\n'.join(i['task_id']+' | '+i['prompt'] for i in items if i['task_id'].startswith('EX-'))+'\n',encoding='utf-8')
(BUILD/'original-prompts.txt').write_text('\n'.join(i['task_id']+' | '+i['prompt'] for i in items if not i['task_id'].startswith('EX-'))+'\n',encoding='utf-8')
(BUILD/'senses.txt').write_text('\n'.join(s['sense_id']+' | '+s['headword']+' | '+s['gloss'] for s in sense_uses)+'\n',encoding='utf-8')
print(json.dumps(summary['counts']))
print('Unresolved marker/reference checks:',len(unresolved))
