"""Keep the adjective section opening together after the v2 reflow."""
import json
from pathlib import Path

folder = Path('typesetting/ch15')
path = folder / 'chapter-15.tex'
text = path.read_text(encoding='utf-8')
assert '% layout-v3-repair' not in text
start = text.index('% mdparagraph:P168:begin')
marker = '% mdparagraph:P170:end'
end = text.index(marker, start) + len(marker)
block = text[start:end].replace('\\reserve{7\\baselineskip}\n', '')
text = (text[:start] + '\\par\\begin{minipage}{\\linewidth}\\raggedright\n' + block
        + '\n\\end{minipage}\\par\\addvspace{4pt}\n' + text[end:])
path.write_text('% layout-v3-repair: keep adjective section opening together\n' + text,
                encoding='utf-8', newline='\n')
record_path = folder / 'layout-adjustments.json'
record = json.loads(record_path.read_text(encoding='utf-8'))
record['status'] = 'v3_learner_requires_compilation_parity_and_visual_reinspection'
record['repairs'].append({
    'document': 'learner', 'found_in_version': 'v2', 'v2_pages': [24, 25],
    'change': 'Keep the adjective section heading, its subheading and opening paragraph in one layout group. No wording, table or source change.'
})
record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
print('Repaired the one remaining learner section opening; key v2 unchanged.')
