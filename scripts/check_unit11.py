"""Repeated Unit 11 dependency, source, display and export checks; not linguistic proof."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []
PRIOR = {f'ch{n:02}' for n in range(1, 11)}


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
    c = read('chapters/ch11/coverage.json')
    lex, gram = read('lexicon/entries.json'), read('curriculum/grammar.json')
    old = {'form': {r['form_id']: r for l in lex['lemmas'] for r in l['forms']},
           'sense': {r['sense_id']: r for l in lex['lemmas'] for r in l['senses']},
           'feature': {r['feature_id']: r for r in gram['features']}}
    new = {'form': unique([r for l in c['lexical_inventory'] for r in l['forms']], 'form_id'),
           'sense': unique([r for l in c['lexical_inventory'] for r in l['senses']], 'sense_id'),
           'feature': unique(c['grammar_inventory'], 'feature_id')}
    owners = {
        kind: {r[kind+'_id']: l['lemma_id']
               for inventory in [lex['lemmas'], c['lexical_inventory']]
               for l in inventory for r in l[field]}
        for kind, field in [('form','forms'), ('sense','senses')]
    }
    for kind, field in [('form','forms'), ('sense','senses')]:
        old_owner = {r[kind+'_id']:l['lemma_id'] for l in lex['lemmas'] for r in l[field]}
        new_owner = {r[kind+'_id']:l['lemma_id'] for l in c['lexical_inventory'] for r in l[field]}
        for rid in old_owner.keys() & new_owner.keys():
            require(old_owner[rid] == new_owner[rid], rid+': existing identity moved to another lemma')
            if kind == 'form':
                require(old[kind][rid]['form'] == new[kind][rid]['form'], rid+': existing source surface changed')
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
            hashes = e.get('image_sha256',e.get('sha256'))
            digest = hashes[n] if isinstance(hashes, list) and n < len(hashes) else hashes if isinstance(hashes, str) and len(images) == 1 else None
            if exists and digest:
                require(identity(path, {'sha256': digest}), eid + ': image hash differs')

    tasks = unique(c['assigned_items'], 'task_id')
    require(len(tasks) == len(c['key_item_ids']) == len(set(c['key_item_ids'])) == 92, 'Expected92distinct tasks/keys')
    require(set(c['key_item_ids']) == {t['key_id'] for t in tasks.values()}, 'Task/key crosswalk')
    cook = {r['task_id']: r['prompt_original'] for r in read('sources/audits/unit11-source/exercises-prompts.json')['items']}
    require({tid:t['prompt'] for tid,t in tasks.items() if tid.startswith('EX-')} == cook and len(cook) == 46, 'All46Cook prompts must remain exact')
    for tid, t in tasks.items():
        require(t.get('dependency_status') == 'closed', tid + ': dependencies not closed')
        for kind in new:
            required = t.get(f'required_{kind}_ids', [])
            for rid in required:
                require(status(kind, rid) != 'unresolved', tid + ': unresolved ' + rid)
            allowed = {'previously_taught', 'new_production'}
            if t['mode'] in {'analysis','reading','scaffolded_reading','scaffolded_recognition',
                            'supported_comprehension','supported_analysis','supported_translation'}:
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
            if value.get('form_id') and value.get('sense_id'):
                require(owners['form'].get(value['form_id']) == owners['sense'].get(value['sense_id']),
                        'Form/sense lemma mismatch: '+value['form_id'])
            for child in value.values():
                walk(child)
        elif isinstance(value,list):
            for child in value:
                walk(child)
    walk(c['paradigms'])
    walk(c['display_plan'])
    matrices = c['display_plan']['matrices']
    matrix_ids = unique(matrices, 'matrix_id')
    require(len(c['paradigms']) == 61 and sum(len(p['cells']) for p in c['paradigms']) == 826,
            'Expected61logical paradigms/826supported cells')
    require(len(matrix_ids) == 38, 'Expected38complete matrices')
    expected_cells = Counter(cell['form_id'] for p in c['paradigms'] for cell in p['cells'])
    displayed_cells = Counter(fid for m in matrices if m.get('paradigm_ids')
                              for row in m['cell_form_ids'] for ids in row for fid in ids)
    derived_cells = Counter(d['form_id'] for d in c['display_plan']['shared_model_derivations'])
    require(expected_cells == displayed_cells + derived_cells, 'Logical/display/derived cell multiset differs')
    require(sum(displayed_cells.values()) == 486 and sum(derived_cells.values()) == 340,
            'Expected486literal/340derived cells')
    require(not (set(displayed_cells) & set(derived_cells)), 'Cell claimed both literal and derived')
    all_cells = {v['form_id']: v for p in c['paradigms'] for v in p['cells']}
    diagnostics = {d['row_id']:d for d in c['display_plan']['lexical_diagnostics']}
    cell_owner = {v['form_id']:p for p in c['paradigms'] for v in p['cells']}
    routes = c['display_plan']['paradigm_cell_display_routes']
    require(Counter(r['form_id'] for r in routes) == expected_cells, 'Display route coverage differs')

    def normalized_analysis(a):
        mapping = {'nominative':'nom','genitive':'gen','dative':'dat','accusative':'acc',
                   'instrumental':'ins','singular':'sg','plural':'pl',
                   'masculine':'m','feminine':'f','neuter':'n'}
        return {k:mapping.get(v,v) if isinstance(v,str) else v for k,v in a.items()}

    for d in c['display_plan']['shared_model_derivations']:
        fid, mid = d['form_id'], d['model_form_id']
        cell, model = all_cells[fid], all_cells[mid]
        ca, ma = normalized_analysis(cell['analysis']), normalized_analysis(model['analysis'])
        require(not cell_owner[fid].get('new_class'), fid+': new class needs full literal display')
        for k in ['case','number','gender','declension']:
            require(ca.get(k)==ma.get(k),fid+': model '+k+' differs')
        require(displayed_cells[mid]==1,fid+': model not printed exactly once')
        loc=d['model_display']; m=matrix_ids[loc['matrix_id']]
        ri,ci=loc['row_index_zero_based'],loc['column_index_zero_based']
        require(mid in m['cell_form_ids'][ri][ci],fid+': incorrect model coordinate')
        require(loc['row_label']==m['rows'][ri][0] and loc['column_label']==m['headers'][ci],fid+': model label differs')
        op=d['operation']; diag=diagnostics[op['diagnostic_row_id']]
        value=diag[op['diagnostic_field']]
        if op['type']=='diagnostic_headword':
            calculated=value
            require(ca['number']=='sg' and ca['case'] in {'nom','acc'},fid+': invalid headword rule')
        else:
            require(op['type']=='replace_initial_model_stem',fid+': unknown derivation')
            require(op['source_model_form_id']==mid and op['source_model_display']==loc,fid+': model identity differs')
            require(model['form'].startswith(op['model_stem']),fid+': stem not present in model')
            suffix=model['form'][len(op['model_stem']):]
            require(suffix==op['retained_model_ending'] and value==op['target_stem'],fid+': diagnostic or ending differs')
            model_diags=[r for r in diagnostics.values() if r['lemma_id']==cell_owner[mid]['lemma_id']]
            require(len(model_diags)==1 and model_diags[0]['diagnostic_stem']==op['model_stem'],fid+': model stem lacks diagnostic')
            calculated=value+suffix
        require(calculated==d['result']==cell['form'],fid+': reconstructed surface differs')

    audit=read('sources/audits/unit11-grammar/grammar-records.json')
    audited={p['paradigm_id']:p for p in audit['paradigms']}
    audited.update({p['paradigm_id']:p for p in read('sources/audits/unit11-source/noun-adjective-paradigms.json')['paradigms']})
    for p in c['paradigms']:
        require(p['paradigm_id'] in audited,p['paradigm_id']+': no source paradigm')
        if p['paradigm_id'] in audited:
            require([(v['form_id'],v['form']) for v in p['cells']]==
                    [(v['form_id'],v['form']) for v in audited[p['paradigm_id']]['cells']],
                    p['paradigm_id']+': audited cells differ')
    for m in matrices:
        require(len(m['rows'])==len(m['cell_form_ids']),m['matrix_id']+': row mapping differs')
        for row,ids in zip(m['rows'],m['cell_form_ids']):
            require(len(row)==len(ids)==len(m['headers']),m['matrix_id']+': column mapping differs')
            for ci,(value,fids) in enumerate(zip(row,ids)):
                for fid in fids:
                    r=record('form',fid)
                    require(r is not None and surface(r['form'])==surface(value),m['matrix_id']+': wrong cell '+fid)
                    analysis=normalized_analysis(all_cells[fid].get('analysis',all_cells[fid]))
                    if m['headers'][0]=='Person / number':
                        label=row[0].split()
                        require(analysis['person']==int(label[0]) and analysis['number']==('sg' if label[1]=='singular' else 'pl'),fid+': person/number label differs')
                        require(analysis['tense']==m['headers'][ci].lower(),fid+': tense label differs')
                        require(analysis.get('mood')=='indicative',fid+': indicative matrix mood differs')
                    elif m['headers'][0]=='Addressee':
                        require(analysis['person']==2 and analysis['number']==('sg' if row[0]=='Singular' else 'pl'),fid+': command label differs')
                        require(analysis.get('mood')=='imperative',fid+': command matrix mood differs')
                    elif m['headers']==['Form','Base']:
                        require(analysis.get('verb_form')=='participle' and analysis.get('agreement')=='base',fid+': participle base label differs')
                        require(analysis.get('tense')==row[0].split()[0].lower(),fid+': participle tense label differs')
                    elif m['headers']==['Form','Infinitive']:
                        require(analysis.get('mood')=='infinitive' and analysis.get('type')==row[0].split()[0].lower(),fid+': infinitive type label differs')
                    elif m['headers'][0]=='Gender / number':
                        require(analysis['gender']==row[0][0].lower() and analysis['number']=='sg' and analysis['case']=='ins',fid+': instrumental label differs')
                    elif m['headers'][0]=='Case':
                        require(analysis['case']==row[0][:3].lower(),fid+': case label differs')
                        header=m['headers'][ci].lower()
                        require(analysis['number']==('sg' if 'singular' in header else 'pl'),fid+': number label differs')
                        if header.split()[0] in {'masculine','feminine','neuter'}:
                            require(analysis['gender']==header[0],fid+': gender label differs')
    for t in tasks.values():
        walk(t.get('input_sequences',[]))
    require(len(c['new_compositions']) == 1 and len(c['new_material_examples']) == 14, 'Expected one composition/fourteen examples')
    passages = c['source_spans'] + c['new_compositions'] + c['new_material_examples']
    for p in passages:
        text = p.get('learner_text',p.get('text',''))
        tokens = p['tokens']
        require(len(text.split()) == len(tokens), 'Passage token count differs')
        for word, token in zip(text.split(),tokens):
            if token.get('token_type') == 'punctuation' or token.get('kind') == 'punctuation':
                require(not token.get('form_id') and not token.get('form_ids') and not token.get('sense_id'), 'Punctuation has lexical identity')
                require(word == token.get('surface', token.get('token', word)), 'Punctuation surface differs')
                continue
            for fid in token.get('form_ids',[token.get('form_id')]):
                r = record('form',fid)
                require(r is not None and surface(word) == surface(r['form']), 'Passage form differs: '+str(fid))
                require(owners['form'].get(fid) == owners['sense'].get(token.get('sense_id')),
                        'Passage form/sense lemma differs: '+word)
                if token.get('lemma_id'):
                    require(owners['form'].get(fid) == token['lemma_id'], 'Passage declared lemma differs: '+word)
                if token.get('form_status'):
                    expected_status = {'previously_supplied':'supplied','previously_recognition':'prior_recognition'}.get(token['form_status'],token['form_status'])
                    require(status('form',fid)==expected_status,'Passage form scope differs: '+word)
            expected_status = {'previously_supplied':'supplied','previously_recognition':'prior_recognition'}.get(token['sense_status'],token['sense_status'])
            require(status('sense',token['sense_id']) == expected_status, 'Passage sense scope differs: '+word)
    originals = read('sources/audits/unit11-source/reading-source.json')['source_spans']
    require(len(c['source_spans']) == len(originals) == 2, 'Expected two source spans')
    for source, original in zip(c['source_spans'], originals):
        require(source['teaching_id'] in teaching, source['source_span_id']+': unknown source-help teaching location')
        require(source['learner_text'].split() == original['exact_text_without_note_cues'].split(), 'Exact source wording differs')
        for field in ['original_notes', 'referenced_notes']:
            actual_notes, expected_notes = source.get(field, []), original.get(field, [])
            require(len(actual_notes) == len(expected_notes), field + ': count differs')
            for actual, expected in zip(actual_notes, expected_notes):
                require(actual.get('text_original', actual.get('text')) == expected.get('text_original', expected.get('text')), field + ': content differs')
        require(bool(source['local_support']), 'Source help absent')
    require([len(p['tokens']) for p in c['source_spans']] == [36,195], 'Expected36/195 whitespace source tokens')
    require(sum(len(p.get('original_notes',[])) for p in c['source_spans']) == 32, 'Expected32 original notes')
    require(sum(len(p.get('referenced_notes',[])) for p in c['source_spans']) == 1, 'Expected one referenced note')
    require(len(c['new_compositions'][0]['tokens']) == 59, 'Expected59word controlled reading')
    dispositions = {}
    for n in range(1,12):
        chapter = c if n == 11 else read(f'chapters/ch{n:02}/coverage.json')
        for t in chapter['assigned_items']:
            if t['task_id'].startswith('EX-'):
                dispositions[t['task_id']] = 'assigned'
        for field, state in [('deferred_source_items','deferred'),('excluded_source_items','excluded')]:
            for item in chapter.get(field,[]):
                rid = item.get('source_item_id','')
                if rid.startswith('EX-'):
                    dispositions[rid] = state
    require(len(dispositions) == 644 and Counter(dispositions.values()) == {'assigned':295,'deferred':349}, 'Cook crosswalk must be295assigned/349deferred')
    for r in c['analysis_inputs']:
        require(identity(r['path'],r), 'Frozen analysis input changed: '+r['path'])
    for path,digest in c['prior_files'].items():
        if path not in {'lexicon/entries.json','curriculum/grammar.json'}:
            require(identity(path,{'sha256':digest,'sha256_normalized_lf':c['prior_files_lf_sha256'].get(path)}), 'Prior artifact changed: '+path)
    if args.draft or args.tex:
        student = (ROOT/'chapters/ch11/student.md').read_text(encoding='utf-8')
        key = (ROOT/'chapters/ch11/answer-key.md').read_text(encoding='utf-8')
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
                tail = student[hits[0].end():]
                next_item = re.search(r'<!--\s*item:\s*',tail)
                task_body = tail[:next_item.start()] if next_item else tail
                positions = [task_body.replace('**','').find(s['text']) for s in t.get('input_sequences',[])]
                require(all(p >= 0 for p in positions) and positions == sorted(positions),
                        tid+': actual ordered analysis inputs missing or changed')
            require(len(re.findall(r'<!--\s*(?:key:\s*)?'+re.escape(t['key_id'])+r'\s*-->',key)) == 1,tid+': key marker missing/repeated')
        for tid in teaching:
            require(tid in student,tid+': teaching marker missing')
        for d in diagnostics.values():
            require(d['headword'] in student and d['diagnostic_stem'] in student,d['lemma_id']+': diagnostic absent')
            for mid in d['printed_model_ids']:
                require(mid in matrix_ids and mid in student,d['lemma_id']+': printed model absent')
        for p in passages:
            if p.get('speaker_turns'):
                positions = []
                for turn in p['speaker_turns']:
                    value = turn['source_label']+' '+turn['text']
                    positions.append(student.replace('**','').find(value))
                require(all(n >= 0 for n in positions) and positions == sorted(positions), 'Exact ordered source dialogue/speaker labels missing')
            else:
                require(p.get('learner_text',p.get('text','')) in student.replace('**',''), 'Exact passage/example missing')
        for source in c['source_spans']:
            for note in source.get('original_notes',[]) + source.get('referenced_notes',[]):
                require(note.get('text_original',note.get('text')) in student.replace('**',''),'Original/referenced note missing')
    if args.tex:
        folder = ROOT/'typesetting/ch11'
        for stem,ids in [('chapter-11',list(tasks)),('answer-key',c['key_item_ids'])]:
            tex = (folder/(stem+'.tex')).read_text(encoding='utf-8')
            pdftext = (folder/'build'/(stem+'.txt')).read_text(encoding='utf-8')
            log = (folder/'build'/(stem+'.log')).read_text(encoding='utf-8',errors='replace')
            require((folder/(stem+'.pdf')).is_file(),stem+': retained PDF missing')
            for tid in ids:
                require(tid in tex,tid+': TeX marker missing')
            for warning in ['Missing character:','Overfull \\hbox','Overfull \\vbox','Underfull \\hbox','Underfull \\vbox','Font shape','Rerun to get','Table widths have changed']:
                require(warning not in log,stem+': '+warning)
            if stem == 'chapter-11':
                for t in tasks.values():
                    require(chars(t['prompt']) in chars(pdftext),t['task_id']+': PDF prompt differs')
    if ERRORS:
        print('\n'.join('ERROR: '+e for e in ERRORS))
        raise SystemExit(1)
    print('Unit11 checks pass:92tasks,46exact Cook prompts,59word controlled reading,two exact sources/32original notes/one referenced note; dependencies, evidence and earlier artifacts preserved.')


if __name__ == '__main__':
    main()
