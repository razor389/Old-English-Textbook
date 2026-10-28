"""One-use Unit 16 assembly aid, ignored build artifact. Hand-review emitted TeX."""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'typesetting/ch16'
NOTE_NUMBERS = {}


def inline(text):
    # Balanced book-title italics are markup; an unpaired reconstructed-form
    # asterisk remains literal. Double-star emphasis is handled first.
    pieces = re.split(r'(\[\^[^\]]+\]|\*\*.*?\*\*|(?<!\w)\*[^*\n]+?\*(?!\w))', text)
    replacements = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%',
                    '$': r'\$', '#': r'\#', '_': r'\_', '/': r'/\allowbreak{}', '{': r'\{',
                    '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    def escape(s):
        return ''.join(replacements.get(c, c) for c in s)
    result = []
    for s in pieces:
        if re.fullmatch(r'\[\^[^\]]+\]', s):
            result.append(r'\textsuperscript{' + str(NOTE_NUMBERS[s[2:-1]]) + '}')
        elif s.startswith('**') and s.endswith('**'):
            result.append(r'\textbf{' + escape(s[2:-2]) + '}')
        elif s.startswith('*') and s.endswith('*') and len(s) > 2:
            result.append(r'\emph{' + escape(s[1:-1]) + '}')
        else:
            result.append(escape(s))
    return ''.join(result)


def blocks(raw):
    lines = raw.splitlines()
    result = []
    i = 1
    while i < len(lines):
        s = lines[i].strip()
        if not s:
            i += 1
            continue
        if s.startswith('<!--'):
            result.append(('comment', re.match(r'<!--\s*(.*?)\s*-->', s)[1]))
            i += 1
        elif s.startswith('##'):
            mark, title = s.split(' ', 1)
            result.append(('heading', (len(mark), title)))
            i += 1
        elif s.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            result.append(('table', [rows[0]] + rows[2:]))
        elif s.startswith('- '):
            items = []
            while i < len(lines) and lines[i].strip().startswith('- '):
                items.append(lines[i].strip()[2:])
                i += 1
            result.append(('list', items))
        elif s.startswith('> '):
            quoted = []
            while i < len(lines) and lines[i].strip().startswith('> '):
                quoted.append(lines[i].strip()[2:])
                i += 1
            result.append(('quote', ' '.join(quoted)))
        elif re.match(r'^\d+\.\s+', s):
            # Numbered model answers remain separate paragraphs.
            para = [s]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r'^\d+\.\s+', lines[i].strip()) and not lines[i].strip().startswith(('##', '<!--', '|', '- ', '> ')):
                para.append(lines[i].strip())
                i += 1
            result.append(('paragraph', ' '.join(para)))
        else:
            para = [s]
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith(('##', '<!--', '|', '- ')):
                para.append(lines[i].strip())
                i += 1
            result.append(('paragraph', ' '.join(para)))
    return result


def emit_table(rows, table_id, out, close_intro=False):
    header, data = rows[0], rows[1:]
    out.append('% mdtable:' + table_id + ':begin')
    if header==['Noun','Stem','G singular','D singular','N plural','Model']:
        # Two linked panels preserve readable type for long diagnostic forms.
        out += ['% table-reflow: nominal-diagnostic-panels',r'\par\begingroup',r'\fontsize{10.5}{13.2}\selectfont']
        for columns,widths in [([0,1,5],[48,48,22.37]),([0,2,3,4],[31,29,29,26.56])]:
            panel_header=[header[i] for i in columns]
            panel_data=[[row[i] for i in columns] for row in data]
            tabular(panel_data,panel_header,widths,'longtable',out)
            out.append(r'\par\addvspace{5pt}')
        out += [r'\par\endgroup','% mdtable:' + table_id + ':end','']
        return
    if len(header)==7 and [h.lower() for h in header[1:4]] in [['masculine singular','feminine singular','neuter singular'],['m sg','f sg','n sg']]:
        # Preserve readable 10.5pt type: print the two numbers in stacked panels.
        # The parity audit reconstructs all original seven-column coordinates.
        out += ['% table-reflow: singular-plural-panels']
        for panel_number, columns in enumerate(([0,1,2,3],[0,4,5,6])):
            out += [r'\par\begingroup',r'\fontsize{10.5}{13.2}\selectfont']
            out.append(r'\par\begin{minipage}{\linewidth}\raggedright')
            panel_header=[header[i] for i in columns]
            panel_data=[[row[i] for i in columns] for row in data]
            tabular(panel_data,panel_header,[22,31.18,31.18,31.18],'tabular',out)
            out.append(r'\end{minipage}\par')
            out.append(r'\par\endgroup')
            if panel_number == 0 and close_intro:
                out.append(r'\end{minipage}\par')
            out.append(r'\par\addvspace{5pt}')
        out += ['% mdtable:' + table_id + ':end','']
        return
    # Initial widths only; all emitted tables are hand-reviewed after compile.
    n=len(header)
    available=124 - 2.812*(n-1)
    weights=[]
    for col in range(n):
        lengths=[len(re.sub(r'\*\*','',row[col])) for row in rows]
        words=[max(map(len,re.sub(r'\*\*','',row[col]).split()),default=0) for row in rows]
        weights.append(max(10, min(65, max(lengths)*0.45 + max(words)*0.55)))
    widths=[round(available*w/sum(weights),2) for w in weights]
    # The first compile exposed unbreakable Old English forms in these source
    # columns. Widen them at the same 10.5pt type and preserve total table width.
    reviewed_widths = {
        'T58': [18.5, 26.31, 73.57],
        'T65': [24, 58, 36.38],
        'T90': [26, 44.5, 47.88],
    }
    if table_id in reviewed_widths:
        assert n == 3
        widths = reviewed_widths[table_id]
    out += [r'\par\begingroup', r'\fontsize{10.5}{13.2}\selectfont']
    tabular(data, header, widths, 'longtable' if len(data)>16 else 'tabular', out)
    out += [r'\par\endgroup', '']
    out.append('% mdtable:' + table_id + ':end')
    if close_intro:
        out.append(r'\end{minipage}\par')


def tabular(data, header, widths, env, out):
    spec = '@{}' + ''.join(r'>{\raggedright\arraybackslash}p{' + str(w) + 'mm}' for w in widths) + '@{}'
    out += [r'\setlength{\LTleft}{0pt}\setlength{\LTright}{\fill}']
    if env == 'tabular':
        out.append(r'\noindent')
    out.append(r'\begin{' + env + '}{' + spec + '}')
    row = ' & '.join(r'\textbf{' + inline(c) + '}' for c in header) + r' \\'
    out += [r'\toprule', row, r'\midrule']
    if env == 'longtable':
        out += [r'\endfirsthead', r'\toprule', row, r'\midrule', r'\endhead',
                r'\midrule', r'\multicolumn{' + str(len(header)) + r'}{r}{\footnotesize Continued on the following page.}\\',
                r'\endfoot', r'\bottomrule', r'\endlastfoot']
    for data_row in data:
        out.append(' & '.join(inline(c) for c in data_row) + r' \\')
    if env == 'tabular':
        out.append(r'\bottomrule')
    out.append(r'\end{' + env + '}')


def assemble(master, stem, title):
    global NOTE_NUMBERS
    path = ROOT / 'chapters/ch16' / master
    raw = path.read_text(encoding='utf-8')
    labels = re.findall(r'^\[\^([^\]]+)\]:', raw, re.M)
    assert len(labels) == len(set(labels))
    general_labels = [label for label in labels if not re.fullmatch(r'(?:[DPR]\d+|P(?:168|169|170)N\d+)', label)]
    NOTE_NUMBERS = {label: label if re.fullmatch(r'(?:[DPR]\d+|P(?:168|169|170)N\d+)', label)
                    else general_labels.index(label) + 1 for label in labels}
    assert set(re.findall(r'\[\^([^\]]+)\]', raw)) == set(labels)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    bs = blocks(raw)
    coverage = json.loads((ROOT / 'chapters/ch16/coverage.json').read_text(encoding='utf-8'))
    source_paragraphs = {
        p.get('source_span_id', p.get('span_id', '')):
            len(re.split(r'\n\s*\n', p['learner_text'].strip()))
        for p in coverage['source_spans']
    }
    out = [
        '% Complete reviewed Unit 16; editorial master: chapters/ch16/' + master,
        '% Markdown SHA-256: ' + digest,
        '% One-use initial assembly followed by complete content and page review.',
        r'\newcommand{\runningtitle}{Unit 16. ' + ('Answer key' if stem == 'answer-key' else 'Narrative and speech') + '}',
        r'\input{../book-layout.tex}',
        r'\hyphenpenalty=10000', r'\exhyphenpenalty=10000', r'\emergencystretch=3em',
        r'\newcommand{\itempara}[2]{\par\addvspace{3pt}\noindent\hangindent=1.8em\hangafter=1\makebox[1.8em][l]{#1.}#2\par}',
        r'\newcommand{\reserve}[1]{\par\penalty-100\begingroup\dimen0=\pagegoal\advance\dimen0 by-\pagetotal\ifdim\dimen0<#1\newpage\fi\endgroup}',
        r'\begin{document}', r'\raggedright',
        r'\booktitle{UNIT 16}{' + title + '}', ''
    ]
    task_open = False
    out.insert(out.index(r'\begin{document}') + 1, r'\addfontfeatures{Ligatures=TeXOff}')
    label_pending = False
    reading_next = 0
    source_dialogue_open = False
    notes_open = False
    intro_open = False
    heading_kept_paragraph = None
    pnum = tnum = 0
    audit = {'master':str(path.relative_to(ROOT)), 'master_sha256':digest, 'paragraphs':[], 'tables':[]}
    def close_task():
        nonlocal task_open
        if task_open:
            out.extend([r'\end{minipage}\par\addvspace{4pt}', ''])
            task_open = False
    for idx, (kind, body) in enumerate(bs):
        if kind == 'comment':
            if body.startswith('example:'):
                # Keep the short Old English example with its English translation.
                out.append(r'\reserve{8\baselineskip}')
            if body.startswith('teaching:') and task_open and not label_pending:
                close_task()
            task_marker = body.startswith('item:') or (body.startswith('key:') and not (idx > 0 and bs[idx-1][0] == 'comment' and bs[idx-1][1].startswith('item:')))
            if task_marker and not label_pending:
                close_task()
                if 'NEW-U16-' in body:
                    out.append(r'\reserve{8\baselineskip}')
                else:
                    out += [r'\par\begin{minipage}{\linewidth}\raggedright']
                    task_open = True
            if task_marker:
                label_pending = False
            if body.startswith('passage:'):
                passage_id=body.split(':',1)[1].strip()
                reading_next=source_paragraphs.get(passage_id,1)
                if passage_id in source_paragraphs:
                    source_dialogue_open=True
            elif body.startswith('composition:'):
                reading_next = 1
            elif body.startswith('source:'):
                # Preserve every paragraph in each contracted source span.
                source_id = body.split(':', 1)[1].strip()
                reading_next = source_paragraphs[source_id]
                source_dialogue_open = True
            out.append('% ' + body)
        elif kind == 'heading':
            close_task()
            level, heading = body
            source_notes = heading in ('10. Original source apparatus', 'Sources', 'Source notes', 'Sources and original reading notes', 'Source and editorial notes', 'Sources and editorial notes', 'Source and form notes', 'Cook’s original notes and source information', '13. Cook’s original notes','13. Cook’s original notes and attachments') or heading.endswith('Sources and selected forms')
            task_heading=bool(re.fullmatch(r'(?:[FACDPRS]\d{2}|Cook (?:XII, XIII|XII,XIII)\.\d+\.\d+)',heading))
            if task_heading:
                if re.fullmatch(r'[FACR]\d{2}', heading):
                    # Multi-output original tasks may span a page. Keep their
                    # heading with the opening prompt, not their whole body.
                    out.append(r'\reserve{8\baselineskip}')
                else:
                    out += [r'\par\begin{minipage}{\linewidth}\raggedright']
                    task_open=True
                label_pending=True
            elif source_notes:
                # Endnotes can follow the final short reading task; do not strand
                # that task alone on a page merely to force a fresh notes page.
                out.append(r'\reserve{8\baselineskip}' if stem == 'chapter-16' else r'\clearpage')
            elif stem == 'answer-key' and (heading in ('Cumulative review','F. Complete forms','F. Complete forms and constructions','R. The bishop and the monk','R. The gymnasium scene','S. The Dangers of Greatness') or re.fullmatch(r'Cook XII, XIII\.\d+',heading)):
                out.append(r'\clearpage')
            else:
                following = [(j,b) for j,b in enumerate(bs[idx+1:],idx+1) if b[0] != 'comment'][:2]
                if len(following)==2 and following[0][1][0]=='paragraph' and following[1][1][0]=='table':
                    # Keep a section heading with its introductory prose and
                    # the first rows of the following breakable reference table.
                    out.append(r'\reserve{18\baselineskip}')
                    heading_kept_paragraph = following[0][0]
                else:
                    out.append(r'\reserve{7\baselineskip}')
            macro = 'section*' if level == 2 else 'subsection*'
            pnum += 1
            pid = 'P' + str(pnum).zfill(3)
            out += ['% mdparagraph:' + pid + ':begin', '\\' + macro + '{' + inline(heading) + '}', '% mdparagraph:' + pid + ':end', '']
            audit['paragraphs'].append({'id':pid,'kind':'heading','text':heading})
            if source_notes:
                out += [r'\begingroup\fontsize{10}{12.8}\selectfont']
                if stem == 'chapter-16':
                    out.append(r'\setlength{\parskip}{1.5pt}')
                notes_open = True
        elif kind == 'table':
            tnum += 1
            tid = 'T' + str(tnum).zfill(2)
            emit_table(body, tid, out, close_intro=intro_open)
            intro_open = False
            audit['tables'].append({'id':tid,'source_rows':body,'reflow':'singular/plural panels' if len(body[0])==7 else 'same columns'})
        elif kind == 'list':
            out.append(r'\begin{itemize}')
            for item in body:
                pnum += 1
                pid = 'P' + str(pnum).zfill(3)
                out += ['% mdparagraph:' + pid + ':begin', r'\item ' + inline(item), '% mdparagraph:' + pid + ':end']
                audit['paragraphs'].append({'id':pid,'kind':'list_item','text':item})
            out += [r'\end{itemize}', '']
        elif kind in ('paragraph', 'quote'):
            if stem=='chapter-16' and re.match(r'^\*\*[^*]+\*\* — ',body):
                following = [b for b in bs[idx+1:] if b[0] != 'comment'][:3]
                table_at = next((j for j,b in enumerate(following) if b[0]=='table'),None)
                if table_at is not None and all(b[0]=='paragraph' for b in following[:table_at]) and len(following[table_at][1])<=10:
                    # The descriptor and stem rule travel with the first complete
                    # small matrix. Adjectival plural panels may follow naturally.
                    assert not intro_open and not task_open
                    out.append(r'\par\begin{minipage}{\linewidth}\raggedright')
                    intro_open = True
            if not task_open and not intro_open and idx != heading_kept_paragraph:
                following = next((b for b in bs[idx+1:] if b[0] != 'comment'), None)
                if following and following[0] == 'table':
                    # Keep a paradigm's noun caption or verbal rule paragraph
                    # with its complete small table, at the existing type size.
                    table_lines = 2 * len(following[1]) + 6 if len(following[1][0]) == 7 else len(following[1]) + 4
                    prose_lines = max(2, (len(body) + 64) // 65)
                    out.append(r'\reserve{' + str(min(28, table_lines + prose_lines)) + r'\baselineskip}')
            if body.startswith(('Context:', 'Open condition:', 'Contrary-present condition:')):
                # Keep each viewpoint label with its example and translation.
                out.append(r'\reserve{12\baselineskip}')
            if not task_open and not intro_open and re.fullmatch(r'\*\*[^*]+\*\*', body):
                # Keep standalone tense/support labels with following matter.
                following = next((b for b in bs[idx+1:] if b[0] != 'comment'), None)
                if following and following[0] == 'table':
                    row_count = len(following[1])
                    reserve_lines = 2 * row_count + 6 if len(following[1][0]) == 7 else row_count + 4
                    out.append(r'\reserve{' + str(min(22, reserve_lines)) + r'\baselineskip}')
                else:
                    out.append(r'\reserve{5\baselineskip}')
            next_is_task_marker = idx+1<len(bs) and bs[idx+1][0]=='comment' and bs[idx+1][1].startswith(('item:', 'key:'))
            if re.fullmatch(r'\*\*(?:[A-Z]\d+|(?:Cook )?[IVX]+\.\d+\.\d+)\.(?: [^*]+)?\*\*', body) or (re.fullmatch(r'\*\*[^*]+\*\*',body) and next_is_task_marker):
                marker_before_label = idx > 0 and bs[idx-1][0] == 'comment' and bs[idx-1][1].startswith(('item:', 'key:'))
                if marker_before_label and task_open:
                    label_pending = False
                else:
                    close_task()
                    if stem == 'answer-key' and body.startswith(('**F01.', '**F02.', '**F03.', '**F04.', '**F05.', '**R01.')):
                        # The full construction displays and the full source
                        # translation with commentary need natural page breaks.
                        out.append(r'\reserve{8\baselineskip}')
                        task_open = False
                    else:
                        out += [r'\par\begin{minipage}{\linewidth}\raggedright']
                        task_open = True
                    label_pending = True
            pnum += 1
            pid = 'P' + str(pnum).zfill(3)
            out.append('% mdparagraph:' + pid + ':begin')
            number = re.match(r'^(\d+)\.\s+(.*)$', body)
            if number:
                out.append(r'\itempara{' + number[1] + '}{' + inline(number[2]) + '}')
            elif reading_next or kind == 'quote':
                if source_dialogue_open:
                    out.append(r'\readingtext{' + inline(body) + '}')
                else:
                    out += [r'\par\begin{minipage}{\linewidth}\raggedright', r'\readingtext{' + inline(body) + '}', r'\end{minipage}\par']
                reading_next = max(0, reading_next - 1)
            else:
                out.append(inline(body))
            out += ['% mdparagraph:' + pid + ':end', '']
            audit['paragraphs'].append({'id':pid,'kind':'paragraph','text':body})
            if source_dialogue_open and reading_next == 0:
                out.append(r'\par')
                source_dialogue_open = False
    close_task()
    assert not intro_open
    if notes_open:
        out.append(r'\endgroup')
    out += [r'\end{document}', '']
    (OUT / (stem + '.tex')).write_text('\n'.join(out), encoding='utf-8')
    (OUT / 'build' / (stem + '-content-map.json')).write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(stem, len(audit['paragraphs']), 'paragraph/list/heading blocks;', len(audit['tables']), 'tables')


if __name__ == '__main__':
    coverage=json.loads((ROOT/'chapters/ch16/coverage.json').read_text(encoding='utf-8'))
    assert coverage.get('textual_review',{}).get('status')=='accepted', 'Independent textual acceptance required before typesetting'
    if '--key-only' not in sys.argv:
        assemble('student.md','chapter-16','Extended narrative and speech')
    if '--learner-only' not in sys.argv:
        assemble('answer-key.md','answer-key','Answer key')
