"""Verify complete volume membership, retained text, pagination and actual PDF navigation."""
from __future__ import annotations

import argparse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import unicodedata

from build_full_book import ROOT, OUT, labels, index_heading_id
from build_course_exports import diagnostics

PDFTOTEXT = Path('C:/Program Files/Git/mingw64/bin/pdftotext.exe')
TEXLUA = Path(os.environ.get('LOCALAPPDATA', 'C:/Users/Ross/AppData/Local')) / 'texlive/2026/bin/windows/texlua.exe'
WORK = ROOT / 'build/full-book/check'
ERRORS = []


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def save(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


def check(condition, message, **context):
    if not condition:
        ERRORS.append({'message': message, **context})


def norm(value):
    return re.sub(r'\s+', '', unicodedata.normalize('NFC', value))


def nav_text(value):
    # Cambria's TeX ligatures encode visible hyphens as soft hyphens and
    # convert straight quotes. This projection applies only to newly composed
    # navigation, never to the accepted-body character comparison.
    return unicodedata.normalize('NFC', value).translate(str.maketrans({'\u00ad': '-', '’': "'", '‘': "'", '“': '"', '”': '"'}))


def group(text, pos):
    assert text[pos] == '{'
    depth = 1
    start = pos + 1
    pos += 1
    while depth:
        if text[pos] in '{}' and text[pos - 1] != '\\':
            depth += 1 if text[pos] == '{' else -1
        pos += 1
    return text[start:pos - 1], pos


def remove_navigation(text):
    # Independently remove only the four allowed invisible commands, using their
    # arity and balanced braces; do not trust the generator's replacement ledger.
    pattern = re.compile(r'\\(BookComponent|BookHeading|BookLabel|BookPoint)\{')
    arities = {'BookComponent': 2, 'BookHeading': 4, 'BookLabel': 1, 'BookPoint': 1}
    result, pos = [], 0
    for match in pattern.finditer(text):
        if match.start() < pos:
            continue
        result.append(text[pos:match.start()])
        pos = match.end() - 1
        for _ in range(arities[match[1]]):
            _, pos = group(text, pos)
    result.append(text[pos:])
    return ''.join(result)


def source_checks(manifest, mapping, index):
    for r in read('book/preservation.json')['files']:
        check(sha(r['path']) == r['sha256'], 'Protected file changed', path=r['path'])
    expected = {c['component_id']: c for c in manifest['components']}
    check(len(expected) == 41, 'Expected exactly 41 components')
    check({r['component_id'] for r in mapping['components']} == set(expected), 'Content-map membership')
    for volume, stem, count in [('learner', 'book', 22), ('key', 'answer-key', 19)]:
        selected = manifest['volumes'][volume]
        check(len(selected) == count and len(set(selected)) == count, 'Volume allowlist count', volume=volume)
        check(all(expected[c]['volume'] == volume for c in selected), 'Wrong volume member', volume=volume)
        actual = re.findall(r'\\input\{fragments/([^}]+)\.tex\}', (OUT / (stem + '.tex')).read_text(encoding='utf-8'))
        check(actual == [c.replace('/', '-') for c in selected], 'Actual TeX component membership/order', volume=volume)
    for c in manifest['components']:
        cid = c['component_id']
        for source in c['sources'].values():
            check(sha(source['path']) == source['sha256'], 'Component source changed', path=source['path'])
        raw = (ROOT / c['sources']['tex']['path']).read_text(encoding='utf-8')
        pre, body = raw.split(r'\begin{document}', 1)
        body, after = body.split(r'\end{document}', 1)
        check(not after.strip(), 'Unexpected post-document content', component_id=cid)
        fragment = (OUT / ('fragments/' + cid.replace('/', '-') + '.tex')).read_text(encoding='utf-8')
        generated = fragment.split('% book-source-body:begin\n', 1)[1].rsplit('\n% book-source-body:end', 1)[0]
        restored = remove_navigation(generated)
        restored = ''.join(line for line in restored.splitlines(keepends=True) if line.rstrip('\n') != '% book-navigation: standalone bookmark replaced by volume hierarchy')
        original = ''.join(line for line in body.splitlines(keepends=True) if not line.startswith(r'\pdfbookmark'))
        check(restored == original, 'Retained source body differs after permitted navigation removal', component_id=cid)
        setup = [line for line in pre.splitlines() if line.strip() and not line.startswith('%') and line not in [r'\input{../book-layout.tex}', r'\usepackage{multicol}']]
        setup = [line.replace(r'\newcommand{\runningtitle}', r'\renewcommand{\runningtitle}') for line in setup]
        prefix = fragment.split('% book-source-body:begin\n', 1)[0].splitlines()
        check(prefix == [r'\BookRecto', r'\begingroup', *setup], 'Component-local preamble differs', component_id=cid)
        record = next(r for r in mapping['components'] if r['component_id'] == cid)
        check(sha(record['fragment']) == record['fragment_sha256'], 'Generated fragment receipt stale', component_id=cid)
    check(mapping['manifest_sha256'] == sha('book/contents.json'), 'Content manifest receipt stale')
    check(mapping['index_sha256'] == sha('book/grammar-index.json'), 'Content index receipt stale')
    check(mapping['front_matter_sha256'] == sha('book/front-matter.md'), 'Front matter receipt stale')
    ids = {a['id'] for a in index['anchors']}
    check(len(ids) == len(index['anchors']), 'Duplicate index anchor ID')
    for anchor in index['anchors']:
        source = (ROOT / anchor['tex_path']).read_text(encoding='utf-8').splitlines()
        check(source.count(anchor['tex_anchor']) == 1 and source[anchor['source_line'] - 1] == anchor['tex_anchor'], 'Index anchor is not an exact unique source line', anchor=anchor['id'])
        check(expected[anchor['component_id']]['volume'] == 'learner', 'Index targets answer key', anchor=anchor['id'])
    check({aid for e in index['entries'] for aid in e['anchors']} == ids, 'Missing or unused index anchor')
    heads = {e['heading'] for e in index['entries']}
    pairs = {(e['heading'], e['subheading']) for e in index['entries']}
    check(not heads.intersection(r['heading'] for r in index['see']), 'Redirect obscures substantive index head')
    for r in index['see'] + index['see_also']:
        for target in r['references']:
            check(target['heading'] in heads, 'Cross-reference lacks substantive destination', target=target)
            check(not target.get('subheading') or (target['heading'], target['subheading']) in pairs, 'Cross-reference lacks subentry', target=target)


def inspect_pdf(volume, stem, retained):
    pdf = f'typesetting/full-book/{"" if retained else "build/"}{stem}.pdf'
    out = (WORK / 'retained' if retained else WORK) / (stem + '-navigation.json')
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([str(TEXLUA), str(ROOT / 'scripts/inspect_book_pdf.lua'), str(ROOT / pdf), str(out)], check=True, capture_output=True)
    data = json.loads(out.read_text(encoding='utf-8'))
    return volume, pdf, data


def pdf_pages(path):
    result = subprocess.run([str(PDFTOTEXT), '-enc', 'UTF-8', '-raw', str(ROOT / path), '-'], check=True, capture_output=True)
    raw = result.stdout.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n')
    pages = raw.split('\f')
    assert not pages[-1].strip(), path
    return pages[:-1]


def body_page(raw, header, number, context):
    lines = [s for s in raw.splitlines() if s.strip()]
    options = {norm(header), norm('Old English'), norm(header + ' Old English'), norm('Old English ' + header)}
    seen = []
    for _ in range(2):
        if lines and norm(lines[0]) in options:
            seen.append(lines.pop(0))
    check(norm(' '.join(seen)) in {norm(header + ' Old English'), norm('Old English ' + header)}, 'Missing or changed running header', **context)
    check(bool(lines) and lines[-1].strip() == str(number), 'Missing or incorrect printed folio', **context, expected_folio=number, actual_last_line=lines[-1] if lines else '')
    if lines and lines[-1].strip() == str(number):
        lines.pop()
    return '\n'.join(lines)


def flatten(outlines):
    result = []
    for r in outlines:
        result.append(r)
        result.extend(flatten(r['children']))
    return result


def volume_checks(manifest, mapping, index, inspections, output_dir='typesetting/full-book'):
    pagination = {'schema_version': 1, 'volumes': {}, 'components': []}
    navigation_report = {'schema_version': 1, 'volumes': {}}
    texts = {}
    all_component_text = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        values = list(pool.map(lambda c: (c['component_id'], pdf_pages(c['sources']['pdf']['path'])), manifest['components']))
    all_component_text.update(values)
    byid = {c['component_id']: c for c in manifest['components']}
    text_comparisons = []
    for volume, pdf, actual in inspections:
        stem = 'book' if volume == 'learner' else 'answer-key'
        final_labels = labels(stem)
        check(actual['status'] == 'passed' and not actual['errors'] and not actual['unresolved_internal_targets'], 'PDF navigation inspector failed', volume=volume)
        check(not actual['other_links'], 'Unexpected nonlocal PDF links', volume=volume)
        check(actual['page_labels']['present'], 'No explicit PDF PageLabels', volume=volume)
        for p in actual['pages']:
            check(abs(p['dimensions']['width_pt'] - 165 * 72 / 25.4) < .02 and abs(p['dimensions']['height_pt'] - 241 * 72 / 25.4) < .02, 'Wrong page dimensions', volume=volume, page=p['physical_page'])
            check(p['rotation'] == 0, 'Unexpected rotated page', volume=volume, page=p['physical_page'])
        dests = {d['name']: d for d in actual['named_destinations']}
        body_first = dests[final_labels['component-pronunciation-' + volume]['destination']]['resolved_page']
        offset = body_first - 1
        check(body_first % 2 == 1, 'Arabic body does not begin recto', volume=volume)
        actual_text = pdf_pages(pdf)
        texts[volume] = actual_text
        check(len(actual_text) == actual['page_count'], 'PDF text/page-tree count differs', volume=volume)
        for n, p in enumerate(actual['pages'][offset:], 1):
            check(p['label'] == str(n), 'Arabic PDF page label differs', volume=volume, physical_page=p['physical_page'])
        for name, ref in final_labels.items():
            if name.startswith('end-'):
                continue  # An end label records the final page, but may share the preceding heading's currentHref.
            check(ref['destination'] in dests, 'Aux label lacks actual PDF destination', volume=volume, label=name)
            if ref['destination'] in dests:
                page = dests[ref['destination']]['resolved_page']
                check(actual['page_labels']['labels'][page - 1] == ref['page'], 'Aux label does not land on its cited PDF page', volume=volume, label=name, physical_page=page, cited=ref['page'])
        blank_pages = []
        previous_end = offset
        expected_outlines = []
        printed_toc = []
        for cid in manifest['volumes'][volume]:
            c = byid[cid]
            slug = cid.replace('/', '-')
            first = int(final_labels['component-' + slug]['page'])
            last = int(final_labels['end-' + slug]['page'])
            start, end = first + offset, last + offset
            count = c['standalone_pages']
            check(last - first + 1 == count, 'Component pagination changed', component_id=cid, expected_pages=count, actual_pages=last-first+1)
            check(start % 2 == 1 and first % 2 == 1, 'Component does not start recto', component_id=cid)
            blank_pages.extend(range(previous_end + 1, start))
            previous_end = end
            pagination['components'].append({'component_id': cid, 'volume': volume, 'source_pdf': c['sources']['pdf']['path'], 'source_sha256': c['sources']['pdf']['sha256'], 'source_pages': count, 'first_page': start, 'last_page': end, 'first_label': first, 'last_label': last})
            sources = all_component_text[cid]
            check(len(sources) == count, 'Source PDF count differs from manifest', component_id=cid)
            for i, source in enumerate(sources):
                assembled = actual_text[start + i - 1]
                context = {'component_id': cid, 'source_page': i+1, 'physical_page': start+i}
                sbody = body_page(source, c['running_title'], i+1, context | {'which': 'source'})
                abody = body_page(assembled, c['running_title'], first+i, context | {'which': 'assembled'})
                same = norm(sbody) == norm(abody)
                check(same, 'Complete PDF page text differs', **context)
                if not same:
                    (WORK / (slug + f'-{i+1}-source.txt')).write_text(sbody, encoding='utf-8')
                    (WORK / (slug + f'-{i+1}-assembled.txt')).write_text(abody, encoding='utf-8')
                text_comparisons.append(context | {'equal': same, 'source_body_sha256': hashlib.sha256(norm(sbody).encode()).hexdigest(), 'assembled_body_sha256': hashlib.sha256(norm(abody).encode()).hexdigest()})
            record = next(r for r in mapping['components'] if r['component_id'] == cid)
            expected_outlines.append({'title': c['title'], 'depth': 0, 'page': start, 'destination': final_labels[record['start_label']]['destination']})
            printed_toc.append({'title': c['title'], 'page': first, 'destination': final_labels[record['start_label']]['destination']})
            for heading in record['navigation']:
                ref = final_labels[heading['label']]
                expected_outlines.append({'title': heading['title'], 'depth': 1 if heading['level'] == 'subsection' else 2, 'page': int(ref['page'])+offset, 'destination': ref['destination']})
                if heading['printed_contents']:
                    printed_toc.append({'title': heading['title'], 'page': int(ref['page']), 'destination': ref['destination']})
        index_first = None
        if volume == 'learner':
            ref = final_labels['grammatical-index']
            index_first = int(ref['page']) + offset
            blank_pages.extend(range(previous_end + 1, index_first))
            expected_outlines.append({'title': 'Grammatical index', 'depth': 0, 'page': index_first, 'destination': ref['destination']})
            printed_toc.append({'title': 'Grammatical index', 'page': int(ref['page']), 'destination': ref['destination']})
        else:
            check(previous_end == actual['page_count'], 'Unaccounted final key pages')
        for page in blank_pages:
            check(not actual_text[page-1].strip(), 'Supposed blank verso has content', volume=volume, physical_page=page)
        outlines = flatten(actual['outlines'])
        check(len(outlines) == len(expected_outlines), 'PDF outline count differs', volume=volume, expected=len(expected_outlines), actual=len(outlines))
        for expected, found in zip(expected_outlines, outlines):
            check(norm(expected['title']) == norm(found['title']) and expected['depth'] == found['depth'] and expected['page'] == found['resolved_page'] and expected['destination'] == found['target'].get('name'), 'PDF outline title, hierarchy or target differs', volume=volume, expected=expected, actual=found)
        toc_pages = []
        for page in actual_text[2:offset]:
            lines = [s for s in page.splitlines() if s.strip()]
            if lines and norm(lines[0]) in [norm('Old English Contents'), norm('Contents Old English')]:
                lines.pop(0)
            if lines and re.fullmatch(r'[ivxlcdm]+', lines[-1].strip()):
                lines.pop()
            toc_pages.append('\n'.join(lines))
        toc_text = re.sub(r'\s+', ' ', nav_text('\n'.join(toc_pages)))
        cursor = 0
        for r in printed_toc:
            # Dot leaders are not consistently emitted by Xpdf; the full title
            # and next numeric page must nevertheless occur in their actual order.
            wanted_title = re.sub(r'\s+', ' ', nav_text(r['title']))
            at = toc_text.find(wanted_title, cursor)
            check(at >= cursor, 'Printed contents title missing or out of order', volume=volume, title=r['title'])
            if at >= cursor:
                cursor = at + len(wanted_title)
                tail = toc_text[cursor:]
                m = re.match(r'\s*(?:[.·…]\s*)*([0-9]+)(?=\s|$)', tail)
                check(bool(m) and int(m[1]) == r['page'], 'Printed contents page incorrect', volume=volume, title=r['title'], expected_page=r['page'], following=tail[:35])
                if m:
                    cursor += m.end()
        links = actual['internal_links']
        for r in printed_toc:
            check(any(l['source_page'] <= offset and l['destination'].get('name') == r['destination'] for l in links), 'Contents entry lacks a working PDF link', volume=volume, title=r['title'])
        new = list(range(1, offset+1)) + (list(range(index_first, actual['page_count']+1)) if index_first else [])
        pagination['volumes'][volume] = {'pdf': pdf, 'sha256': sha(pdf), 'pages': actual['page_count'], 'front_matter_pages': offset, 'body_start_physical': body_first, 'index_first_physical': index_first, 'blank_pages': blank_pages, 'new_pages': new, 'page_labels': actual['page_labels']['labels']}
        navigation_report['volumes'][volume] = {'pdf_sha256': sha(pdf), 'inspector_counts': actual['counts'], 'page_label_ranges': actual['page_labels']['ranges'], 'outline_entries_checked': len(expected_outlines), 'contents_entries_checked': len(printed_toc), 'contents': printed_toc, 'named_destinations_checked': len(dests), 'internal_links_checked': len(links), 'unresolved': actual['unresolved_internal_targets'], 'inspector_errors': actual['errors']}
        log = (OUT / 'build' / (stem + '.log')).read_text(encoding='utf-8', errors='replace')
        check(not diagnostics(log), 'Compilation diagnostics', volume=volume, findings=diagnostics(log))
        for marker in ['undefined references', 'multiply defined', 'destination with the same identifier', 'Token not allowed']:
            check(marker not in log, 'Navigation compile warning', volume=volume, warning=marker)
    index_checks(index, inspections, texts, pagination, navigation_report)
    save(output_dir + '/pagination.json', pagination)
    save(output_dir + '/navigation.json', navigation_report)
    save(output_dir + '/text-parity.json', {'schema_version': 1, 'normalization': 'NFC and whitespace only; exact running headers and printed folios checked separately. Every remaining character on every accepted component page compared in order.', 'pages': text_comparisons})
    return pagination, navigation_report


def index_checks(index, inspections, texts, pagination, report):
    actual = next(i[2] for i in inspections if i[0] == 'learner')
    final_labels = labels('book')
    loc = read('typesetting/full-book/index-locations.json')
    check(loc['index_sha256'] == sha('book/grammar-index.json'), 'Index location receipt stale')
    dests = {d['name']: d for d in actual['named_destinations']}
    index_first = pagination['volumes']['learner']['index_first_physical']
    index_text = norm(nav_text('\n'.join(texts['learner'][index_first-1:])))
    index_links = [l for l in actual['internal_links'] if l['source_page'] >= index_first]
    references = 0
    for original, row in zip(index['entries'], loc['entries']):
        check(original == {k:row[k] for k in original}, 'Resolved index entry differs from semantic index', heading=original['heading'], subheading=original['subheading'])
        pages = {}
        for aid in original['anchors']:
            pages.setdefault(int(final_labels[aid]['page']), aid)
        expected = [{'page': p, 'anchor': a, 'destination': final_labels[a]['destination']} for p,a in sorted(pages.items())]
        check(row['references'] == expected, 'Index page references are not actual unique target pages', heading=row['heading'], subheading=row['subheading'])
        lead = row['subheading'] + ', ' if row['subheading'] else ''
        printed = norm(nav_text(lead + ', '.join(str(r['page']) for r in expected)))
        check(printed in index_text, 'Printed index entry/page list absent', heading=row['heading'], subheading=row['subheading'], expected=printed)
        for r in expected:
            references += 1
            check(any(l['destination'].get('name') == r['destination'] for l in index_links), 'Index page reference lacks a working PDF link', anchor=r['anchor'])
    heads = {e['heading'] for e in index['entries']} | {r['heading'] for r in index['see']}
    for h in heads:
        target = index_heading_id(h)
        check(target in dests and dests[target]['resolved_page'] >= index_first, 'Index heading destination absent or outside index', heading=h)
        check(norm(nav_text(h)) in index_text, 'Printed index heading absent', heading=h)
    for r in index['see'] + index['see_also']:
        for target in r['references']:
            name = index_heading_id(target['heading'])
            check(any(l['destination'].get('name') == name for l in index_links), 'Index cross-reference lacks a PDF link', heading=r['heading'], target=target)
    report['index'] = {'semantic_sha256': sha('book/grammar-index.json'), 'entries': len(index['entries']), 'anchors': len(index['anchors']), 'printed_page_references': references, 'substantive_heads': len({e['heading'] for e in index['entries']}), 'see_heads': len(index['see']), 'see_also_heads': len(index['see_also']), 'actual_index_links': len(index_links), 'first_physical_page': index_first, 'first_printed_page': int(final_labels['grammatical-index']['page'])}
    report['index']['ordered_verification'] = ordered_index_check(index, loc, actual, texts['learner'], index_first, pagination['volumes']['learner']['front_matter_pages'])


def ordered_index_check(index, locations, actual, text_pages, index_first, offset):
    """Bind every numeric click to its own ordered head/subentry and printed page.

    Whole-index substring membership is insufficient: distinct headings can have
    identical subentries/page lists. Compare the complete text in order, then
    compare actual annotation rectangles in two-column reading order. Wrapped
    cross-reference annotations are coalesced only for the additional route test;
    all numeric annotations must match one-for-one, without coalescing.
    """
    groups = defaultdict(list)
    for row in locations['entries']:
        groups[row['heading']].append(row)
    see = {r['heading']: r['references'] for r in index['see']}
    also = {r['heading']: r['references'] for r in index['see_also']}
    parts, routes, numeric = [], [], []
    length = 0

    def append(text, destination=None, row=None, number=None):
        nonlocal length
        value = norm(nav_text(text))
        start = length
        parts.append(value)
        length += len(value)
        if destination:
            routes.append(destination)
        if row is not None:
            numeric.append({'heading': row['heading'], 'subheading': row['subheading'], 'printed_reference': number,
                            'destination': destination, 'start': start, 'end': length})

    def crossrefs(refs):
        for i, r in enumerate(refs):
            if i:
                append('; ')
            append(r['heading'] + (', ' + r['subheading'] if r.get('subheading') else ''), index_heading_id(r['heading']))
        append('.')

    append('REFERENCE Grammatical index')
    previous_letter = None
    for head in sorted(set(groups) | set(see), key=lambda v: unicodedata.normalize('NFKD', v).casefold()):
        letter = head[0].upper()
        if letter != previous_letter:
            append(letter)
            previous_letter = letter
        append(head)
        if head in see:
            append('. See ')
            crossrefs(see[head])
            continue
        for row in groups[head]:
            if row['subheading']:
                append(row['subheading'] + ', ')
            for i, ref in enumerate(row['references']):
                if i:
                    append(', ')
                append(str(ref['page']), ref['destination'], row, ref['page'])
        if head in also:
            append('See also ')
            crossrefs(also[head])
    expected = ''.join(parts)
    actual_parts, spans = [], []
    cursor = 0
    for physical in range(index_first, len(text_pages)+1):
        body = body_page(text_pages[physical-1], 'Grammatical index', physical-offset, {'volume': 'learner', 'physical_page': physical})
        value = norm(nav_text(body))
        spans.append({'physical_page': physical, 'start': cursor, 'end': cursor+len(value)})
        actual_parts.append(value)
        cursor += len(value)
    observed = ''.join(actual_parts)
    same = expected == observed
    if not same:
        at = next((i for i, (a,b) in enumerate(zip(expected, observed)) if a != b), min(len(expected), len(observed)))
        check(False, 'Complete ordered index text differs', offset=at, expected_context=expected[max(0,at-70):at+100], actual_context=observed[max(0,at-70):at+100])
    for r in numeric:
        r['printed_on_physical_page'] = next((s['physical_page'] for s in spans if s['start'] <= r['start'] < s['end']), None)
        check(any(s['start'] <= r['start'] and r['end'] <= s['end'] for s in spans), 'Numeric index reference crosses a page boundary', reference=r)

    # Sort by page, column, line, then horizontal position. A four-point line
    # tolerance accommodates glyph-specific link boxes within 13.2-point leading.
    columns = defaultdict(list)
    for link in actual['internal_links']:
        if link['source_page'] < index_first:
            continue
        width = actual['pages'][link['source_page']-1]['dimensions']['width_pt']
        rect = link['rect']
        column = int((rect[0]+rect[2])/2 > width/2)
        columns[(link['source_page'], column)].append(link)
    ordered = []
    for _, links in sorted(columns.items()):
        lines = []
        for link in sorted(links, key=lambda l: -(l['rect'][1]+l['rect'][3])/2):
            y = (link['rect'][1]+link['rect'][3])/2
            if not lines or lines[-1][0]-y > 4:
                lines.append((y, []))
            lines[-1][1].append(link)
        for _, line in lines:
            ordered.extend(sorted(line, key=lambda l: l['rect'][0]))
    actual_numeric = [l for l in ordered if not l['destination'].get('name', '').startswith('index-')]
    check(len(actual_numeric) == len(numeric), 'Numeric index annotation count differs', expected=len(numeric), actual=len(actual_numeric))
    bindings = []
    for wanted, found in zip(numeric, actual_numeric):
        passed = (wanted['destination'] == found['destination'].get('name')
                  and wanted['printed_reference'] + offset == found['resolved_page']
                  and wanted['printed_on_physical_page'] == found['source_page'])
        check(passed, 'Index click is not bound to its own ordered row/reference', expected=wanted, actual=found)
        bindings.append({k:v for k,v in wanted.items() if k not in ['start','end']} | {
            'annotation_index': found['annotation_index'], 'annotation_rect': found['rect'],
            'target_physical_page': found['resolved_page'], 'passed': passed})

    def collapsed(values):
        result = []
        for v in values:
            if not result or result[-1] != v:
                result.append(v)
        return result
    route_match = collapsed(routes) == collapsed([l['destination'].get('name') for l in ordered])
    check(route_match, 'Ordered index route sequence differs after joining wrapped cross-reference rectangles')
    return {'complete_text_exact_order': same, 'normalized_character_count': len(expected),
            'numeric_annotations_checked_one_for_one': len(bindings), 'ordered_wrapped_route_sequence_matches': route_match,
            'numeric_bindings': bindings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--retained', action='store_true', help='Inspect accepted PDFs rather than build PDFs')
    args = parser.parse_args()
    WORK.mkdir(parents=True, exist_ok=True)
    manifest, mapping, index = read('book/contents.json'), read('typesetting/full-book/content-map.json'), read('book/grammar-index.json')
    source_checks(manifest, mapping, index)
    with ThreadPoolExecutor(max_workers=2) as pool:
        inspections = list(pool.map(lambda pair: inspect_pdf(*pair, args.retained), [('learner','book'), ('key','answer-key')]))
    # Retained verification must not invalidate the build pagination identity
    # already bound by raster/proof reviews merely by changing its PDF path.
    output_dir = 'build/full-book/check/retained' if args.retained else 'typesetting/full-book'
    pagination, navigation = volume_checks(manifest, mapping, index, inspections, output_dir)
    index_summary = dict(navigation['index'])
    index_summary['ordered_verification'] = {k:v for k,v in index_summary['ordered_verification'].items() if k != 'numeric_bindings'}
    result = {'schema_version': 1, 'status': 'passed' if not ERRORS else 'failed', 'protected_files': len(read('book/preservation.json')['files']), 'component_sources': 3*len(manifest['components']), 'components': len(manifest['components']), 'retained_body_pages_compared': sum(c['source_pages'] for c in pagination['components']), 'volumes': {k:{f:v[f] for f in ['pdf','sha256','pages','front_matter_pages','index_first_physical']} for k,v in pagination['volumes'].items()}, 'index': index_summary, 'errors': ERRORS}
    save(output_dir + '/checks.json', result)
    print(json.dumps({**result, 'errors': ERRORS[:15]}, ensure_ascii=False))
    return 1 if ERRORS else 0


if __name__ == '__main__':
    raise SystemExit(main())
