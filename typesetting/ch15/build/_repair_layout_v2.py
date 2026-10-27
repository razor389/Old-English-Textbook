"""Apply only the page-specific, nonlinguistic repairs found in v1 review."""
import json
import re
from pathlib import Path

OUT = Path('typesetting/ch15')
OPEN = r'\par\begin{minipage}{\linewidth}\raggedright'
CLOSE = r'\end{minipage}\par\addvspace{4pt}'

def wrap_table(text, paragraph, table):
    start = text.index('% mdparagraph:' + paragraph + ':begin')
    marker = '% mdtable:' + table + ':end'
    end = text.index(marker, start) + len(marker)
    block = text[start:end]
    block = re.sub(r'\\reserve\{\d+\\baselineskip\}\n', '', block)
    return text[:start] + OPEN + '\n' + block + '\n' + CLOSE + text[end:]

def extend_next_box(text, paragraph):
    start = text.index('% mdparagraph:' + paragraph + ':begin')
    opening = text.index(OPEN, start)
    before = re.sub(r'\\reserve\{\d+\\baselineskip\}\n', '', text[start:opening])
    return text[:start] + OPEN + '\n' + before + text[opening + len(OPEN):]

learner = (OUT / 'chapter-15.tex').read_text(encoding='utf-8')
assert '% layout-v2-repairs' not in learner
for paragraph, table in [('P128', 'T42'), ('P153', 'T53'), ('P175', 'T63')]:
    learner = wrap_table(learner, paragraph, table)
learner = learner.replace('\\reserve{7\\baselineskip}\n% mdparagraph:P166:begin',
                          '\\reserve{32\\baselineskip}\n% mdparagraph:P166:begin', 1)
learner = learner.replace('\\reserve{28\\baselineskip}\n% mdparagraph:P167:begin',
                          '% mdparagraph:P167:begin', 1)
for paragraph in ['P270', 'P361', 'P766', 'P780']:
    learner = extend_next_box(learner, paragraph)
# Keep Cook28.10's help label and first support paragraph in the prompt box.
start = learner.index('% mdparagraph:P421:begin')
end_marker = '% mdparagraph:P422:end'
end = learner.index(end_marker, start) + len(end_marker)
block = learner[start:end]
assert block.count(CLOSE) == 1
learner = learner[:start] + block.replace(CLOSE, '') + '\n' + CLOSE + learner[end:]
learner = '% layout-v2-repairs: non-author v1 findings; masters unchanged\n' + learner
(OUT / 'chapter-15.tex').write_text(learner, encoding='utf-8', newline='\n')

key = (OUT / 'answer-key.tex').read_text(encoding='utf-8')
assert '% layout-v2-repairs' not in key
old = '\\clearpage\n% mdparagraph:P004:begin'
assert key.count(old) == 1
key = key.replace(old, '% mdparagraph:P004:begin', 1)
for paragraph in ['P004', 'P302']:
    key = extend_next_box(key, paragraph)
key = '% layout-v2-repairs: non-author v1 findings; masters unchanged\n' + key
(OUT / 'answer-key.tex').write_text(key, encoding='utf-8', newline='\n')

record = {
    'chapter_id': 'ch15', 'status': 'v2_requires_compilation_parity_and_visual_reinspection',
    'linguistic_masters_changed': False,
    'v1': {'learner_pages': 64, 'key_pages': 30,
           'manifest': 'typesetting/ch15/build/render-manifest-v1.json'},
    'repairs': [
        {'document': 'learner', 'v1_pages': [18, 21, 25],
         'change': 'Keep the laeran, forlaetan and gelic entry captions with their first complete table using unbreakable layout groups; every table cell and caption is unchanged.'},
        {'document': 'learner', 'v1_pages': [23],
         'change': 'Reserve the principal-parts heading with its introduction and reference table, and remove the later reserve that stranded the heading.'},
        {'document': 'learner', 'v1_pages': [34, 39],
         'change': 'Extend each opening task layout group to include its section heading.'},
        {'document': 'learner', 'v1_pages': [43],
         'change': 'Extend Cook28.10 prompt group through the first help paragraph so the modern-help label cannot stand alone.'},
        {'document': 'learner', 'v1_pages': [61, 62],
         'change': 'Keep the prayer source heading and title with the full reading, and the R01-R05 task introduction with R01.'},
        {'document': 'key', 'v1_pages': [1, 24],
         'change': 'Remove the inherited forced page break before F and keep its heading with F01; keep the Duties section heading with D01.'}
    ],
    'withdrawn_findings': [
        {'document': 'key', 'v1_page': 3,
         'description': 'Suspected F03 header collision withdrawn by the reviewer after personally re-viewing the actual image. The columns are clearly separated; no table-width change was made.'}
    ],
    'acceptance_limit': 'These records describe repairs only. Actual final parity, clean logs and non-author page inspection are required separately.'
}
(OUT / 'layout-adjustments.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
print('Applied v1 page findings to TeX only; compilation and reinspection pending.')
