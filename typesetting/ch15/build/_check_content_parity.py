"""One-use audit of Unit 15 Markdown against emitted TeX, not an assembly step."""
from pathlib import Path
import hashlib
import json
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'typesetting/ch15'
NOTE_NUMBERS = {}


def norm(text):
    return ' '.join(unicodedata.normalize('NFC', text).split())


def mdplain(text):
    text = re.sub(r'\[\^([^\]]+)\]', lambda m: str(NOTE_NUMBERS[m[1]]), text)
    text = re.sub(r'(?<!\w)\*([^*\n]+?)\*(?!\w)', r'\1', text.replace('**', ''))
    return norm(text)


def group(text, pos):
    assert text[pos] == '{', (text, pos)
    depth = 1
    start = pos + 1
    pos += 1
    while depth:
        if text[pos] == '\\':
            pos += 2
            continue
        if text[pos] == '{':
            depth += 1
        elif text[pos] == '}':
            depth -= 1
        pos += 1
    return text[start:pos-1], pos


def texplain(text):
    # A deliberately narrow decoder; unknown commands fail the comparison.
    output = []
    pos = 0
    while pos < len(text):
        char = text[pos]
        if char != '\\':
            output.append(char)
            pos += 1
            continue
        match = re.match(r'\\([A-Za-z]+\*?|[^A-Za-z])', text[pos:])
        assert match, text[pos:]
        name = match[1]
        pos += len(match[0])
        if name in ('textbf','emph','section*','subsection*','readingtext','textsuperscript'):
            inner, pos = group(text, pos)
            output.append(texplain(inner))
        elif name == 'itempara':
            number, pos = group(text, pos)
            inner, pos = group(text, pos)
            output.append(number + '. ' + texplain(inner))
        elif name in ('begin','end'):
            environment, pos = group(text, pos)
            assert environment == 'minipage', environment
            if name == 'begin':
                _, pos = group(text, pos)
        elif name == 'allowbreak':
            if text[pos:pos+2] == '{}':
                pos += 2
        elif name in ('par','raggedright','item'):
            output.append(' ')
        elif name in ('&','%','$','#','_','{','}'):
            output.append(name)
        elif name in ('textbackslash','textasciitilde','textasciicircum'):
            output.append({'textbackslash':'\\','textasciitilde':'~','textasciicircum':'^'}[name])
            if text[pos:pos+2] == '{}':
                pos += 2
        else:
            raise AssertionError('Unknown TeX command: ' + name)
    return norm(''.join(output))


def master_content(raw):
    global NOTE_NUMBERS
    labels = re.findall(r'^\[\^([^\]]+)\]:', raw, re.M)
    assert len(labels) == len(set(labels))
    general_labels = [label for label in labels if not re.fullmatch(r'[DPR]\d+', label)]
    NOTE_NUMBERS = {label: label if re.fullmatch(r'[DPR]\d+', label)
                    else general_labels.index(label) + 1 for label in labels}
    assert set(re.findall(r'\[\^([^\]]+)\]', raw)) == set(labels)
    # Independently inventory every nonblank Markdown block, without importing
    # the assembly helper or reading its generated content-map files.
    paragraphs, tables, comments = [], [], []
    raw = re.sub(r'(?m)^(<!--.*-->)$', r'\n\1\n', raw)
    chunks = re.split(r'\n\s*\n', raw.strip())
    title = None
    for chunk in chunks:
        lines = chunk.splitlines()
        if lines[0].startswith('# '):
            assert len(lines) == 1 and title is None
            title = lines[0][2:]
        elif all(line.startswith('<!--') for line in lines):
            comments.extend(re.fullmatch(r'<!--\s*(.*?)\s*-->', line)[1] for line in lines)
        elif lines[0].startswith('|'):
            assert all(line.startswith('|') for line in lines)
            cells = [[mdplain(cell) for cell in line.strip('|').split('|')] for line in lines]
            assert all(re.fullmatch(r':?-+:?', cell) for cell in cells[1])
            tables.append([cells[0]] + cells[2:])
        elif lines[0].startswith('- '):
            assert all(line.startswith('- ') for line in lines)
            paragraphs.extend(mdplain(line[2:]) for line in lines)
        elif lines[0].startswith('##'):
            assert len(lines) == 1
            paragraphs.append(mdplain(re.sub(r'^#+ ', '', lines[0])))
        elif lines[0].startswith('> '):
            assert all(line.startswith('> ') for line in lines)
            paragraphs.append(mdplain(' '.join(line[2:] for line in lines)))
        elif re.match(r'^\d+\.\s+', lines[0]):
            assert all(re.match(r'^\d+\.\s+', line) for line in lines)
            paragraphs.extend(mdplain(line) for line in lines)
        else:
            assert not any(line.startswith(('<!--', '|', '##', '- ')) for line in lines)
            paragraphs.append(mdplain(' '.join(lines)))
    return title, paragraphs, tables, comments


def main():
    report = {
        'unit': '15',
        'method': 'Independent block inventory from accepted Markdown; decoded actual TeX paragraph bodies, all table rows and cells, and every editorial comment. Full non-whitespace Unicode sequences also checked in extracted PDF prose after removal of running matter and normalization of Xpdf soft-hyphen encoding to the original literal hyphen.',
        'formatting_changes': [
            'Both documents use Ligatures=TeXOff to preserve the masters\' literal punctuation in extracted PDF text.',
            'Every paradigm cell is printed in a complete small matrix at readable 10.5pt type. Any layout changes preserve every original coordinate, header and cell.',
            'The three exact source readings use the reading style; the eight short examples stay with their translations.',
            'Cook labels remain with their prompts; final page-specific repairs are recorded in the page review.',
            'Line wrapping, emphasis commands and page furniture differ from Markdown; linguistic text and punctuation are preserved.'
            ,'Original source-note references and definitions retain their D/P/R-prefixed numbers; general source notes use a separate numerical sequence. All definition text remains.'
        ],
        'documents': []
    }
    for master, stem in [('student.md','chapter-15'), ('answer-key.md','answer-key')]:
        source_path = ROOT / 'chapters/ch15' / master
        tex_path = OUT / (stem + '.tex')
        source = source_path.read_text(encoding='utf-8')
        tex = tex_path.read_text(encoding='utf-8')
        title, paragraphs, tables, comments = master_content(source)
        expected_title = title.split('. ', 1)[1]
        assert r'\booktitle{UNIT 15}{' + expected_title + '}' in tex
        texparagraphs = re.findall(r'% mdparagraph:(P\d+):begin\n(.*?)\n% mdparagraph:\1:end', tex, re.S)
        decoded = [texplain(body) for _, body in texparagraphs]
        assert len(decoded) == len(paragraphs), (stem, len(decoded), len(paragraphs))
        for index, (actual, expected) in enumerate(zip(decoded, paragraphs), 1):
            assert actual == expected, (stem, index, actual, expected)
        tableblocks = re.findall(r'% mdtable:(T\d+):begin\n(.*?)\n% mdtable:\1:end', tex, re.S)
        assert len(tableblocks) == len(tables)
        cell_count = 0
        for (tid, body), expected in zip(tableblocks, tables):
            rows = []
            for line in body.splitlines():
                if ' & ' in line and line.endswith(r'\\'):
                    rows.append([texplain(cell) for cell in line[:-2].split(' & ')])
            if '% table-reflow: singular-plural-panels' in body:
                assert len(expected[0])==7 and len(rows)==2*len(expected),(stem,tid)
                size=len(expected)
                first,second=rows[:size],rows[size:]
                assert all(len(a)==len(b)==4 and a[0]==b[0] for a,b in zip(first,second)),(stem,tid)
                rows=[a+b[1:] for a,b in zip(first,second)]
            elif '% table-reflow: nominal-diagnostic-panels' in body:
                assert expected[0]==['Noun','Stem','G singular','D singular','N plural','Model'],(stem,tid)
                first=[r for r in rows if len(r)==3]
                second=[r for r in rows if len(r)==4]
                for panel in [first,second]:
                    if len(panel)>1 and panel[1]==panel[0]:panel.pop(1)
                assert len(first)==len(second)==len(expected),(stem,tid)
                assert all(a[0]==b[0] for a,b in zip(first,second)),(stem,tid)
                rows=[[a[0],a[1],b[1],b[2],b[3],a[2]] for a,b in zip(first,second)]
            # A repeated longtable header is page furniture, not a second row.
            elif len(rows) > 1 and rows[1] == rows[0]:
                rows.pop(1)
            assert rows == expected, (stem, tid, rows, expected)
            cell_count += sum(len(row) for row in expected)
        for comment in comments:
            assert '% ' + comment in tex, (stem, comment)

        extracted = (OUT / 'build' / (stem + '.txt')).read_text(encoding='utf-8')
        pages = extracted.split('\f')
        cleaned = []
        for page in pages:
            lines = page.splitlines()
            lines = [line for line in lines if not ('Old English' in line and 'Unit 15.' in line)]
            while lines and not lines[-1].strip():
                lines.pop()
            if lines and re.fullmatch(r'\s*\d+\s*', lines[-1]):
                lines.pop()
            cleaned.append('\n'.join(lines))
        pdfchars = re.sub(r'\s+', '', unicodedata.normalize('NFC', '\n'.join(cleaned))).replace('\u00ad', '-')
        missing_pdf = []
        for pid, expected in zip([pid for pid, _ in texparagraphs], paragraphs):
            # Printed bullet is separate furniture; all paragraph contents remain.
            wanted = re.sub(r'\s+', '', expected)
            if wanted not in pdfchars:
                missing_pdf.append({'id':pid,'expected':expected})
        assert not missing_pdf, (stem, missing_pdf)
        report['documents'].append({
            'master':source_path.relative_to(ROOT).as_posix(),
            'master_sha256':hashlib.sha256(source_path.read_bytes()).hexdigest(),
            'tex':tex_path.relative_to(ROOT).as_posix(),
            'tex_sha256':hashlib.sha256(tex_path.read_bytes()).hexdigest(),
            'tex_sha256_normalized_lf':hashlib.sha256(tex_path.read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
            'paragraph_heading_list_blocks':len(paragraphs),
            'original_tables':len(tables),
            'original_table_cells_including_headers':cell_count,
            'all_editorial_comments_preserved':len(comments),
            'paragraph_and_cell_parity':'PASS',
            'pdf_complete_paragraph_character_parity':'PASS',
            'title_parity':'PASS',
            'source_notes':'All source-note paragraphs and apparatus tables included in the complete block/cell counts above.'
        })
    (OUT / 'content-parity.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
