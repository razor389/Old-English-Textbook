import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'curriculum/proposals/unit16'


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def save(name, data):
    (DEST / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


inv = read('curriculum/proposals/unit16/inventory.json')
base = read('lexicon/entries.json')['lemmas']
forms = {f['form_id']: (l, f) for l in base + inv['lemmas'] for f in l['forms']}
senses = {s['sense_id']: (l, s) for l in base + inv['lemmas'] for s in l['senses']}
routes = {r['form_ids'][0]: r for r in read('curriculum/proposals/unit16/display-matrices.json')['paradigm_cell_display_routes']}
tasks, models, sequences, input_sequences, reference_lemmas = [], [], [], [], []


def start(n, prompt, features):
    tid = f'NEW-U16-F{n:02d}'
    task = {'task_id': tid, 'key_item_id': 'KEY-' + tid, 'origin': 'new_teaching_material', 'task_type': 'morphology',
            'prompt': prompt, 'inputs': [], 'output_positions': [], 'required_feature_ids': features,
            'local_support': [], 'dependency_status': 'exact_forms_bound_pending_reconciliation',
            'grading_visibility_rule': 'Labels request forms by lemma, person, number, tense or case; the target surfaces belong only to the private model.'}
    model = {'task_id': tid, 'outputs': []}
    tasks.append(task)
    models.append(model)
    return task, model


def add_form(task, model, label, form_ids, sense_ids, gloss):
    oid = task['task_id'] + f'-O{len(task["output_positions"]) + 1:03d}'
    task['output_positions'].append({'output_position_id': oid, 'output_id': oid, 'kind': 'form' if len(form_ids) == 1 else 'old_english_translation', 'label': label,
        'response_language': 'Old English', 'required_form_ids': form_ids, 'required_sense_ids': sense_ids,
        'display_routes': [copy.deepcopy(routes[fid]) for fid in form_ids if fid in routes]})
    if len(form_ids)==1:
        route=routes[form_ids[0]]
        task['output_positions'][-1]['paradigm_id']=route['paradigm_id']
        task['output_positions'][-1]['cell_id']=route['logical_cell_id']
    target = ' '.join(forms[fid][1]['form'] for fid in form_ids)
    model['outputs'].append({'output_position_id': oid, 'output_id': oid, 'model': target, 'essential_meaning': gloss,
        'valid_alternatives': 'A documented spelling variant may be linguistically valid; assess separately whether the requested selected table form was given.',
        'target_compliance': label})
    tokens = []
    for n, (fid, sid) in enumerate(zip(form_ids, sense_ids), 1):
        lemma, form = forms[fid]
        sense_lemma, sense = senses[sid]
        assert lemma['lemma_id'] == sense_lemma['lemma_id'], (fid, sid)
        tokens.append({'token_index': n, 'literal': form['form'], 'surface': form['form'], 'lemma_id': lemma['lemma_id'],
            'form_id': fid, 'sense_id': sid, 'analysis': form['analysis'], 'contextual_analysis': form.get('contextual_analysis', form['analysis']),
            'form_status': 'previously_taught' if form.get('production_taught_in') else form['knowledge_status'],
            'sense_status': 'previously_taught' if sense.get('production_taught_in') else sense['knowledge_status']})
    sequences.append({'sequence_id': oid + '-MODEL', 'owner_id': task['task_id'], 'output_position_id': oid, 'kind': 'output', 'text': target, 'tokens': tokens,
        'required_form_ids': form_ids, 'required_sense_ids': sense_ids, 'status': 'selected_forms_bound'})


def explain(task, model, label, target, meaning):
    oid = task['task_id'] + f'-O{len(task["output_positions"]) + 1:03d}'
    task['output_positions'].append({'output_position_id': oid, 'output_id': oid, 'kind': 'explanation', 'label': label, 'response_language': 'English'})
    model['outputs'].append({'output_position_id': oid, 'output_id': oid, 'model': target, 'essential_meaning': meaning,
        'valid_alternatives': 'Accept equivalent accurate wording.', 'target_compliance': label})


t, m = start(1, 'Give the selected forms requested below. For each verb, explain the stem changes linking your three answers. Retain the prefixes and the selected spelling.',
             ['u16-aceorfan-indicative', 'u16-forleosan-indicative', 'u16-thwean-indicative', 'u16-iernan-indicative'])
groups = [
 ('āceorfan', 'aceorfan', 'aceorfan-u16', [('pres-2-sg', 'present indicative, you singular'), ('pret-2-sg', 'preterite indicative, you singular'), ('pret-3-pl', 'preterite indicative, they')],
  'The selected present second singular has ie; the preterite second singular and plural have u. The ā- prefix remains.'),
 ('forlēosan', 'forleosan', 'forleosan-u16', [('pres-3-sg', 'present indicative, he'), ('pret-2-sg', 'preterite indicative, you singular'), ('pret-3-pl', 'preterite indicative, they')],
  'The present third singular has īe and contracted -st; the preterite second singular and plural have u and r in place of s.'),
 ('ðwēan', 'thwean', 'thwean-u16', [('pres-3-sg', 'present indicative, he'), ('pret-2-sg', 'preterite indicative, you singular'), ('pret-3-pl', 'preterite indicative, they')],
  'The contracted present third singular has ieh; preterite second singular and plural have ōg, contrasting with singular first/third ōh.'),
 ('iernan', 'iernan', 'iernan-u16', [('pres-3-sg', 'present indicative, he'), ('pret-3-sg', 'preterite indicative, he'), ('pret-3-pl', 'preterite indicative, they')],
  'The selected stems are iern-, arn, and urn-. Preserve the metathesized r and the selected ie spelling.')]
for headword, lid, sid, selectors, rule in groups:
    for suffix, label in selectors:
        add_form(t, m, f'{headword}: {label}', [lid + '-' + suffix], [sid], label)
    explain(t, m, headword + ': explain the stem relations', rule, rule)

t, m = start(2, 'Give the selected forms requested below. Then explain the two stated contrasts. These are separate positions even when their spelling coincides.',
             ['u16-smierwan-indicative', 'u16-bewendan-indicative', 'u16-plegian-indicative', 'u16-beheafdian-indicative', 'u16-gefyllan-utterance', 'u16-forgiefan-forgive'])
specs = [
 ('smierwan-pres-1-sg', 'smierwan-u16', 'smierwan: present indicative, I'),
 ('smierwan-pres-2-sg', 'smierwan-u16', 'smierwan: present indicative, you singular'),
 ('smierwan-pret-3-sg', 'smierwan-u16', 'smierwan: preterite indicative, she'),
 ('bewendan-pres-1-sg', 'bewendan-u16', 'bewęndan: present indicative, I'),
 ('bewendan-pret-3-sg', 'bewendan-u16', 'bewęndan: preterite indicative, he'),
 ('plegian-pret-3-pl', 'plegian-u16-play', 'plegian: preterite indicative, they'),
 ('beheafdian-pret-3-pl', 'beheafdian-u16', 'behēafdian: preterite indicative, they'),
 ('gefyllan-participle-citation', 'gefyllan-u16-fulfil', 'gefyllan: uninflected past participle'),
 ('forgiefan-pp-bare-source', 'forgiefan-u16-forgive', 'forgiefan: uninflected past participle')]
for fid, sid, label in specs:
    add_form(t, m, label, [fid], [sid], label)
explain(t, m, 'Explain the smierwan stem distribution shown by your answers', 'The w remains in the present first singular but is absent in the selected present second singular and preterite; the selected series keeps ie.', 'Identify the w alternation without imposing one unchanged stem on every cell.')
explain(t, m, 'Explain what the two bewęndan answers establish about identifying tense from spelling alone', 'Bewęnde can be present first singular or preterite first/third singular. Subject and context identify the position; identical spelling does not erase the distinction.', 'Recognize syncretism and the need for context.')

t, m = start(3, 'For each listed verb, give a command to one person and then to more than one. Use the selected command pair taught in this unit.', ['u06-imperative-use'])
for lid, headword, sid in [('aceorfan', 'āceorfan', 'aceorfan-u16'), ('blissian', 'blissian', 'blissian-u16'), ('smierwan', 'smierwan', 'smierwan-u16'), ('arisan', 'ārīsan', 'arisan-u14-arise'), ('forlaetan', 'forlǣtan', 'forlaetan-1'), ('geswican', 'geswīcan', 'geswican-cease'), ('efthweorfan', 'ęfthweorfan', 'efthweorfan-u13')]:
    for number, label in [('sg', 'one addressee'), ('pl', 'more than one addressee')]:
        add_form(t, m, headword + ': ' + label, [lid + '-imp-2-' + number], [sid], 'Command: ' + label)

t, m = start(4, 'Give the requested present-subjunctive forms and the two infinitive forms. The labels specify the form, not an English tense-conversion rule.', ['u16-expectation-findan', 'u16-indefinite-relative-fedan', 'u16-iernan-frame'])
for lid, headword, sid in [('findan', 'findan', 'findan-1'), ('fedan', 'fēdan', 'fedan-feed-source')]:
    for number, label in [('sg', 'third singular'), ('pl', 'third plural')]:
        add_form(t, m, headword + ': present subjunctive, ' + label, [lid + '-pres-subj-3-' + number], [sid], 'Present subjunctive, ' + label)
add_form(t, m, 'iernan: plain infinitive', ['iernan-infinitive'], ['iernan-u16'], 'to run, plain infinitive')
add_form(t, m, 'iernan: inflected infinitive after tō (give the infinitive only)', ['iernan-inflected-infinitive'], ['iernan-u16'], 'to run, inflected infinitive')

t, m = start(5, 'Give the four requested strong forms of nearu. Then translate the three phrases using bēgen and sunu, without adding an article. Finally explain the stem alternation and the number of both.', ['u16-system-nearu', 'u16-system-begen', 'u09-sunu-u-stem'])
for fid, label in [('nearu-nom-sg-m-strong', 'nearu: masculine nominative singular'), ('nearu-acc-sg-m-strong', 'nearu: masculine accusative singular'), ('nearu-gen-sg-m-strong', 'nearu: masculine genitive singular'), ('nearu-dat-pl-m-strong', 'nearu: masculine dative plural')]:
    add_form(t, m, label, [fid], ['nearu-u16-sense'], label)
for case, label in [('acc', 'both sons, accusative'), ('gen', 'of both sons, genitive'), ('dat', 'to both sons, dative')]:
    add_form(t, m, label, ['begen-' + case + '-pl-m', 'sunu-' + case + '-pl'], ['begen-u16-sense', 'sunu-1'], label)
explain(t, m, 'Explain the nearu stem alternation shown by your answers', 'The masculine nominative singular ends in -u. Before the selected -es and -um endings the stem has w; the selected accusative nearone has o before -ne.', 'State the actual u/o/w distribution; do not attach every ending mechanically to nearu.')
explain(t, m, 'Explain the grammatical number of both in the phrases', 'Bēgen has plural forms. Its reference is to two, but it does not supply a separate dual declension; agreement with dual personal pronouns elsewhere still uses the plural both forms.', 'Distinguish semantic two from the inflectional dual.')

# Dictionary forms in the directions are explicit input, not required recall.
headword_groups = [
 [('aceorfan','aceorfan-u16'),('forleosan','forleosan-u16'),('thwean','thwean-u16'),('iernan','iernan-u16')],
 [('smierwan','smierwan-u16'),('bewendan','bewendan-u16'),('plegian','plegian-u16-play'),('beheafdian','beheafdian-u16'),('gefyllan','gefyllan-u16-fulfil'),('forgiefan','forgiefan-u16-forgive')],
 [('aceorfan','aceorfan-u16'),('blissian','blissian-u16'),('smierwan','smierwan-u16'),('arisan','arisan-u14-arise'),('forlaetan','forlaetan-1'),('geswican','geswican-cease'),('efthweorfan','efthweorfan-u13')],
 [('findan','findan-1'),('fedan','fedan-feed-source'),('iernan','iernan-u16')],
 [('nearu','nearu-u16-sense'),('begen','begen-u16-sense'),('sunu','sunu-1')]]
for task, group in zip(tasks,headword_groups):
    for n,(lid,sid) in enumerate(group,1):
        lemma=senses[sid][0]
        sense=senses[sid][1]
        headword=lemma['display_headword']
        choices=[(fid,f) for fid,(l,f) in forms.items() if l['lemma_id']==lid and f['form']==headword]
        if lid in ('nearu','begen','sunu'):
            exact={'nearu':'nearu-nom-sg-m-strong','begen':'begen-nom-pl-m','sunu':'sunu-nom-sg'}[lid]
            choices=[(exact,forms[exact][1])]
        else:
            choices=[x for x in choices if 'infinitive' in x[0] or 'principal-part-1-reference' in x[0]]
        if not choices:
            fid=lid+'-u16-direction-headword-reference'
            refs=sorted(set(lemma.get('evidence_refs',[])+sense.get('evidence_refs',[])))
            if not refs:
                refs=sorted({r for own,f0 in forms.values() if own['lemma_id']==lid for r in f0.get('evidence_refs',[])})
            f={'form_id':fid,'form':headword,'analysis':{'verb_form':'headword_reference','function':'citation_only'},
               'knowledge_status':'supplied','teaching_ids':['NEW-U16-DIRECTION-HEADWORDS'],'evidence_refs':refs,
               'scope_note':'Dictionary headword supplied in an instruction; no independent infinitive use or recall is assigned by this reference label.'}
            reference_lemmas.append({'lemma_id':lid,'display_headword':headword,'part_of_speech':lemma['part_of_speech'],'forms':[f],'senses':[]})
            forms[fid]=(lemma,f)
            choices=[(fid,f)]
        fid,f=sorted(choices,key=lambda x:(not bool(x[1].get('production_taught_in')), 'reference' in x[0],len(x[0])))[0]
        sense=senses[sid][1]
        task['inputs'].append(headword)
        seq={'sequence_id':task['task_id']+f'-HEADWORD-{n:02d}','owner_id':task['task_id'],'kind':'input','text':headword,
             'tokens':[{'token_index':1,'literal':headword,'surface':headword,'lemma_id':lid,'form_id':fid,'sense_id':sid,'analysis':f['analysis'],
                        'contextual_analysis':{'function':'dictionary form supplied in the task direction; not an independent-output target'},
                        'form_status':'previously_taught' if f.get('production_taught_in') else f.get('knowledge_status','supplied'),
                        'sense_status':'previously_taught' if sense.get('production_taught_in') else sense.get('knowledge_status','supplied')}],
             'required_form_ids':[fid],'required_sense_ids':[sid],'status':'explicitly_supplied_direction_input'}
        input_sequences.append(seq)

save('form-task-plan.json', {'schema_version': 1, 'chapter': 'ch16', 'status': 'selected_forms_bound_pending_reconciliation', 'tasks': tasks})
save('author-only-form-models.json', {'schema_version': 1, 'chapter': 'ch16', 'visibility': 'author_only', 'tasks': models})
save('author-only-form-bindings.json', {'schema_version': 1, 'chapter': 'ch16', 'visibility': 'author_only', 'sequences': sequences})
save('form-input-bindings.json', {'schema_version': 1, 'chapter': 'ch16', 'sequences': input_sequences})
save('input-reference-records.json', {'schema_version':1,'chapter':'ch16','lemmas':reference_lemmas,'features':[]})
print(json.dumps({'tasks': len(tasks), 'outputs': sum(len(t['output_positions']) for t in tasks), 'oe_outputs': len(sequences)}, ensure_ascii=False))
