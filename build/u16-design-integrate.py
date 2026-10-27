import copy
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'curriculum/proposals/unit16'


def read(path, default=None):
    p = ROOT / path
    return json.loads(p.read_text(encoding='utf-8-sig')) if p.exists() else default


def save(name, value):
    (DEST / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


baseline = read('lexicon/entries.json')['lemmas']
prior_lemmas = {x['lemma_id']: x for x in baseline}
prior_forms = {f['form_id']: (l['lemma_id'], f) for l in baseline for f in l['forms']}
prior_senses = {s['sense_id']: (l['lemma_id'], s) for l in baseline for s in l['senses']}
prior_grammar_raw = read('curriculum/grammar.json')
prior_features = {x['feature_id']: x for x in prior_grammar_raw['features']}
sources = [
    'sources/audits/unit16-source/lexical-inventory.json',
    'sources/audits/unit16-grammar/grammar-records.json',
    'sources/audits/unit16-grammar/source-support.json',
    'sources/audits/unit16-source/reading-support.json',
    'sources/audits/unit16-source/reading-constructions.json',
    'sources/audits/unit16-source/exercise-support.json',
    'sources/audits/unit16-source/exercise-constructions.json',
    'sources/audits/unit16-grammar/reading-verbal-support.json',
    'curriculum/proposals/unit16/input-reference-records.json',
]
packets = [(p, read(p)) for p in sources if (ROOT / p).exists()]
lemmas, features, identities, conflicts = {}, {}, [], []


def merge_record(target, incoming, key, baseline_records):
    rid = incoming[key]
    record = copy.deepcopy(incoming)
    if rid in baseline_records:
        old = baseline_records[rid][1]
        if key == 'form_id' and old['form'] != record['form']:
            conflicts.append({'id': rid, 'kind': 'prior_surface_conflict', 'old': old['form'], 'new': record['form']})
        if record.get('analysis') != old.get('analysis') and key == 'form_id':
            record.setdefault('contextual_analysis', record.get('analysis', {}))
            record['analysis'] = copy.deepcopy(old['analysis'])
            identities.append({'form_id': rid, 'decision': 'Preserve actual prior analysis and surface; keep current contextual analysis separately.', 'prior_analysis': old['analysis'], 'contextual_analysis': record['contextual_analysis']})
        record['prior_scope'] = {k: old.get(k) for k in ('recognition_taught_in', 'production_taught_in', 'supplied_in')}
        if old.get('production_taught_in'):
            record['knowledge_status'] = 'previously_taught'
    if rid not in target:
        target[rid] = record
        return
    existing = target[rid]
    if key == 'form_id' and existing['form'] != record['form']:
        conflicts.append({'id': rid, 'kind': 'packet_surface_conflict', 'old': existing['form'], 'new': record['form']})
    for listkey in ('evidence_refs', 'teaching_ids', 'used_in_tasks', 'assessed_in'):
        existing[listkey] = sorted(set(existing.get(listkey, [])) | set(record.get(listkey, [])))
    for field, value in record.items():
        existing.setdefault(field, value)


for path, packet in packets:
    for lemma in packet.get('lemmas', []):
        lid = lemma['lemma_id']
        if lid not in lemmas:
            lemmas[lid] = {k: copy.deepcopy(v) for k, v in lemma.items() if k not in ('forms', 'senses')}
            lemmas[lid]['forms'], lemmas[lid]['senses'] = {}, {}
            lemmas[lid]['prior_lemma_present'] = lid in prior_lemmas
        target = lemmas[lid]
        for form in lemma.get('forms', []):
            form=copy.deepcopy(form)
            if not form.get('teaching_ids'):
                prior=prior_forms.get(form['form_id'],(None,{}))[1]
                form['teaching_ids']=['NEW-U16-PRIOR-RECALL' if prior.get('production_taught_in') else 'NEW-U16-READING-SUPPORT' if 'reading' in path else 'NEW-U16-COOK-SUPPORT' if form.get('knowledge_status')=='supplied' else 'NEW-U16-GRAMMAR']
            merge_record(target['forms'], form, 'form_id', prior_forms)
        for sense in lemma.get('senses', []):
            sense=copy.deepcopy(sense)
            if not sense.get('teaching_ids'):
                prior=prior_senses.get(sense['sense_id'],(None,{}))[1]
                sense['teaching_ids']=['NEW-U16-PRIOR-RECALL' if prior.get('production_taught_in') else 'NEW-U16-READING-SUPPORT' if 'reading' in path else 'NEW-U16-COOK-SUPPORT' if sense.get('knowledge_status')=='supplied' else 'NEW-U16-GRAMMAR']
            merge_record(target['senses'], sense, 'sense_id', prior_senses)
    packet_features=copy.deepcopy(packet.get('features',[]))+copy.deepcopy(packet.get('constructions',[]))
    if path.endswith('/exercise-support.json') and not (ROOT/'sources/audits/unit16-source/exercise-constructions.json').exists():
        source_prompts={p['source_item_id']:p for p in read('sources/audits/unit16-source/exercises-prompts.json')['items']}
        for support in packet.get('supports',[]):
            packet_features.append({'feature_id':support['support_id']+'-FRAME','label':support['actual_supplied_text'],
                'description':support['explanation'],'knowledge_status':'supplied','support_refs':[support['support_id']],
                'teaching_ids':['NEW-U16-COOK-SUPPORT'],'origin_category':'new teaching material',
                'scope_note':'Only the listed exact lexical/phrase help is supplied; no unrestricted productive frame or paradigm is inferred.',
                'evidence_refs':sorted({r for tid in support['source_item_ids'] for r in source_prompts[tid]['evidence_refs']})})
    for feature in packet_features:
        feature=copy.deepcopy(feature)
        feature.setdefault('description',feature.get('actual_supplied_text',feature.get('scope_note','')))
        if not feature.get('teaching_ids'):
            feature['teaching_ids']=['NEW-U16-READING-SUPPORT' if 'reading' in path else 'NEW-U16-COOK-SUPPORT' if feature.get('knowledge_status')=='supplied' else 'NEW-U16-GRAMMAR']
        features[feature['feature_id']] = feature

nominals = read('sources/audits/unit16-source/noun-adjective-paradigms.json')
grammar = read('sources/audits/unit16-grammar/grammar-records.json')
paradigms = copy.deepcopy(nominals['paradigms']) + copy.deepcopy(grammar['paradigms'])
for p in paradigms:
    p['cells'] = p.pop('forms', p.get('cells', []))
    p.setdefault('label', p.get('headword', p['lemma_id']))
    p.setdefault('scope', p.get('teaching_scope', 'See the explicit form and use scopes.'))
    for cell in p['cells']:
        cell.setdefault('cell_id', cell['form_id'])
        cell.setdefault('form_ids', [cell['form_id']])
        cell.setdefault('teaching_ids', [p['paradigm_id']])
        cell.setdefault('contextual_analysis', copy.deepcopy(cell['analysis']))
        fid = cell['form_id']
        if fid in prior_forms and prior_forms[fid][1].get('production_taught_in'):
            cell['knowledge_status'] = 'previously_taught'
        if fid in lemmas[p['lemma_id']]['forms']:
            cell['analysis'] = copy.deepcopy(lemmas[p['lemma_id']]['forms'][fid]['analysis'])
        if p in nominals['paradigms']:
            pass

# Nominal system records state morphology scope only; basic case uses are prior
# dependencies and lexical frames remain independently bounded.
for p in paradigms:
    if p['paradigm_id'].startswith(('NEW-U16-NOM-', 'NEW-U16-ADJ-')):
        fid = 'u16-system-' + p['lemma_id']
        features[fid] = {'feature_id': fid, 'label': p['label'] + ': selected nominal system',
            'description': p['scope'], 'scope_note': p['scope'], 'knowledge_status': 'new_production',
            'teaching_ids': [p['paradigm_id']], 'evidence_refs': p['evidence_refs'],
            'origin_category': 'new_teaching_material', 'rules': p.get('rules', []),
            'basic_uses': p.get('basic_uses', [])}

matrices, routes, component_routes = [], [], []
case_order = ['nom', 'gen', 'dat', 'acc']
case_names = dict(zip(case_order + ['ins'], ['Nominative', 'Genitive', 'Dative', 'Accusative', 'Instrumental']))


def short(value):
    return {'singular': 'sg', 'plural': 'pl', 'masculine': 'm', 'feminine': 'f', 'neuter': 'n',
            'nominative': 'nom', 'genitive': 'gen', 'dative': 'dat', 'accusative': 'acc', 'instrumental': 'ins'}.get(value, value)


for p in paradigms:
    cells = p['cells']
    for c in cells:
        c['_a'] = {k: short(v) if isinstance(v, str) else v for k, v in c['contextual_analysis'].items()}
    if len(cells) == 50:
        headers = ['Series / case', 'M sg', 'F sg', 'N sg', 'M pl', 'F pl', 'N pl']
        positions = [(strength, case) for strength in ('strong', 'weak') for case in case_order + (['ins'] if strength == 'strong' else [])]
        groups = [('m', 'sg'), ('f', 'sg'), ('n', 'sg'), ('m', 'pl'), ('f', 'pl'), ('n', 'pl')]
        row_specs = [(strength.title() + ' ' + case_names[case].lower(), [next((c for c in cells if c['_a'].get('strength', c['_a'].get('declension')) == strength and c['_a'].get('case') == case and c['_a'].get('gender') == g and c['_a'].get('number') == n), None) for g, n in groups]) for strength, case in positions]
    elif cells[0]['_a'].get('case'):
        plural_gender = len(cells) == 12 and all(c['_a'].get('number') == 'pl' for c in cells)
        numbers = [n for n in ('sg', 'pl') if any(c['_a'].get('number') == n for c in cells)]
        groups = [('m', 'pl'), ('f', 'pl'), ('n', 'pl')] if plural_gender else [(None, n) for n in numbers]
        headers = ['Case'] + (['M plural', 'F plural', 'N plural'] if plural_gender else ['Singular' if n == 'sg' else 'Plural' for n in numbers])
        row_specs = [(case_names[case], [next((c for c in cells if c['_a'].get('case') == case and c['_a'].get('number') == n and (g is None or c['_a'].get('gender') == g)), None) for g, n in groups]) for case in case_order]
    elif len(cells) in (6, 12) and all(c['_a'].get('person') for c in cells):
        tenses = [t for t in ('present', 'preterite') if any(c['_a'].get('tense') == t for c in cells)]
        headers = ['Person / number'] + [t.title() for t in tenses]
        row_specs = [(f'{person} {number}', [next(c for c in cells if c['_a'].get('person') == person and c['_a'].get('number') == number and c['_a'].get('tense') == tense) for tense in tenses]) for number in ('sg', 'pl') for person in (1, 2, 3)]
    else:
        headers = ['Position', 'Form']
        row_specs = []
        for c in cells:
            a = c['_a']
            label = ', '.join(str(v) for k, v in a.items() if k in ('verb_form', 'nonfinite', 'mood', 'tense', 'person', 'number', 'case', 'use', 'function')) or c['form_id']
            row_specs.append((label, [c]))
    matrix = {'matrix_id': p['paradigm_id'] + '-DISPLAY', 'title': p['label'], 'paradigm_ids': [p['paradigm_id']],
              'headers': headers, 'rows': [], 'cell_form_ids': [], 'cell_logical_ids': [], 'cell_knowledge_statuses': [],
              'evidence_refs': p['evidence_refs'], 'scope': p['scope'], 'rules': p.get('rules_and_exceptions', p.get('rules', [])),
              'display_obligation': 'Print every assigned literal cell with its rules, stem changes, basic uses, and productive/reference limits. An em dash marks a nonapplicable position.'}
    seen = []
    for ri, (label, row_cells) in enumerate(row_specs):
        matrix['rows'].append([label] + [c['form'] if c else '—' for c in row_cells])
        matrix['cell_form_ids'].append([[]] + [c['form_ids'] if c else [] for c in row_cells])
        matrix['cell_logical_ids'].append([None] + [c['cell_id'] if c else None for c in row_cells])
        matrix['cell_knowledge_statuses'].append(['label'] + [c['knowledge_status'] if c else 'not_applicable' for c in row_cells])
        for ci, c in enumerate(row_cells, 1):
            if not c:
                continue
            seen.append(c['cell_id'])
            route = {'paradigm_id': p['paradigm_id'], 'logical_cell_id': c['cell_id'], 'form_ids': c['form_ids'],
                     'display_kind': 'literal', 'matrix_id': matrix['matrix_id'], 'row_index_zero_based': ri,
                     'column_index_zero_based': ci, 'surface': c['form'], 'analysis': c['contextual_analysis'],
                     'knowledge_status': c['knowledge_status'], 'evidence_refs': c['evidence_refs'],
                     'operation': {'type': 'literal_surface', 'value': c['form']}}
            routes.append(route)
            for index, fid in enumerate(c['form_ids'], 1):
                component_routes.append(dict(route, component_index_one_based=index, form_id=fid))
    assert Counter(seen) == Counter(c['cell_id'] for c in cells), (p['paradigm_id'], len(seen), len(cells))
    for c in cells:
        c.pop('_a')
    matrices.append(matrix)

evidence = {}
for n in range(1, 16):
    c = read(f'chapters/ch{n:02d}/coverage.json')
    evidence.update(c.get('evidence_catalog', {}))
for path in ('sources/audits/unit16-source/evidence-catalog.json', 'sources/audits/unit16-grammar/evidence-catalog.json', 'sources/audits/unit16-coordinator/evidence-catalog.json'):
    catalog = read(path, {})
    records=catalog.get('records',catalog.get('evidence_catalog',catalog))
    if isinstance(records,list):
        records={r['evidence_id']:{k:v for k,v in r.items() if k!='evidence_id'} for r in records}
    evidence.update(records)

teaching = {}
all_records = [(k, rec) for l in lemmas.values() for k in ('forms', 'senses') for rec in l[k].values()] + [('features', f) for f in features.values()]
for kind, record in all_records:
    key = {'forms': 'form_id', 'senses': 'sense_id', 'features': 'feature_id'}[kind]
    for tid in record.get('teaching_ids', []):
        target = teaching.setdefault(tid, {'teaching_id': tid, 'type': 'explicit_teaching_record', 'form_ids': [], 'sense_ids': [], 'feature_ids': [], 'evidence_refs': []})
        target[key + 's'].append(record[key])
        target['evidence_refs'] += record.get('evidence_refs', [])
for p in paradigms:
    target = teaching.setdefault(p['paradigm_id'], {'teaching_id': p['paradigm_id'], 'form_ids': [], 'sense_ids': [], 'feature_ids': [], 'evidence_refs': []})
    target.update({'type': 'complete_paradigm', 'title': p['label'], 'scope_note': p['scope'], 'paradigm_id': p['paradigm_id'], 'display_matrix_id': p['paradigm_id'] + '-DISPLAY', 'rules': p.get('rules_and_exceptions', p.get('rules', [])), 'basic_uses': p.get('basic_uses', [])})
for t in teaching.values():
    for key in ('form_ids', 'sense_ids', 'feature_ids', 'evidence_refs'):
        t[key] = sorted(set(t.get(key, [])))
    t.setdefault('title', t['teaching_id'])
    if t['teaching_id']=='NEW-U16-COOK-SUPPORT':
        t['type']='supplied_source_help';t['title']='Exact Cook construction and lexical helps'
        t['support_cards']=read('sources/audits/unit16-grammar/source-support.json',{}).get('cook_support',[])
        t['scope_note']='Print every assigned help before its task; supplied positions are not tested for unaided recall.'
    if t['teaching_id']=='NEW-U16-READING-SUPPORT':
        t['type']='supplied_reading_help';t['title']='Local forms and constructions in the exact Gymnasium reading'
        t['support_cards']=read('sources/audits/unit16-grammar/reading-verbal-support.json',{}).get('items',[])
        t['scope_note']='Local comprehension support only; do not generalize complete conjugational systems from these source tokens.'

for lemma in lemmas.values():
    lemma['forms'] = list(lemma['forms'].values())
    lemma['senses'] = list(lemma['senses'].values())
counts = {'lemmas': len(lemmas), 'forms': sum(len(l['forms']) for l in lemmas.values()), 'senses': sum(len(l['senses']) for l in lemmas.values()), 'features': len(features), 'paradigms': len(paradigms), 'paradigm_cells': len(routes), 'display_matrices': len(matrices), 'teaching_records': len(teaching)}
missing_evidence = sorted({ref for _, rec in all_records for ref in rec.get('evidence_refs', []) if ref not in evidence})
inventory = {'schema_version': 1, 'chapter': 'ch16', 'status': 'integration_in_progress_not_sealed', 'prior_baseline_checkpoint': 'e1d94be',
             'prior_baseline_counts': {'lemmas': 955, 'forms': 10470, 'senses': 1207, 'features': 950}, 'prerequisite_chapters': [f'ch{n:02d}' for n in range(1,16)],
             'analysis_input_hashes': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p, _ in packets},
             'evidence_catalog': evidence, 'lemmas': list(lemmas.values()), 'features': list(features.values()), 'paradigms': paradigms,
             'teaching_records': list(teaching.values()), 'form_identity_reconciliation': identities,
             'principal_parts': read('sources/audits/unit16-grammar/principal-parts.json', {}),
             'lexical_frames': read('sources/audits/unit16-grammar/lexical-frames.json', {}),
             'audited_inflection_rules': nominals.get('rules', []), 'counts': counts,
             'unresolved_integration': {'conflicts': conflicts, 'missing_evidence_refs': missing_evidence, 'pending': ['Selected prior dependencies and sequence bindings', 'Remaining source and grammar supports', 'All task output and reading token closure']}}
save('inventory.json', inventory)
save('display-matrices.json', {'schema_version': 1, 'chapter': 'ch16', 'status': 'literal_tables_from_current_worker_packets', 'matrices': matrices, 'paradigm_cell_display_routes': routes, 'component_form_routes': component_routes,
                             'counts': {'matrices': len(matrices), 'logical_cells': len(routes), 'literal_cells': len(routes), 'literal_form_cells':len(routes), 'literal_routes':len(routes), 'unassigned_table_slots':0, 'component_form_occurrences':len(component_routes), 'derived_cells': 0, 'component_routes': len(component_routes)}})
save('integration-validation.json', {'schema_version': 1, 'chapter': 'ch16', 'status': 'not_sealed', 'counts': counts, 'conflicts': conflicts, 'missing_evidence_refs': missing_evidence})
print(json.dumps({'counts': counts, 'conflicts': conflicts, 'missing_evidence_refs': len(missing_evidence)}, ensure_ascii=False))
