"""Adapt inspected complete-export checks; do not build or accept any document."""
from pathlib import Path
import py_compile

folder = Path('typesetting/ch18/build')
folder.mkdir(parents=True, exist_ok=True)
for name in ['_assemble_unit17.py', '_check_content_parity.py', '_render_pages.py', '_accept_pages.py']:
    target = folder / name.replace('unit17', 'unit18')
    assert not target.exists(), target
    text = (Path('typesetting/ch17/build') / name).read_text(encoding='utf-8')
    for old, new in [('Unit 17', 'Unit 18'), ('UNIT 17', 'UNIT 18'),
                     ('Unit17', 'Unit18'), ('unit17', 'unit18'), ('ch17', 'ch18'),
                     ('chapter-17', 'chapter-18'), ('NEW-U17-', 'NEW-U18-'),
                     ("'unit': '17'", "'unit': '18'"),
                     ('Connected exposition, praise and figurative language', 'Independent prose consolidation'),
                     ('Exposition and praise', 'Prose consolidation'),
                     ('four short examples', 'two short examples')]:
        text = text.replace(old, new)
    text = text.replace(r'P(?:174|175)N\d+[a-z]?', r'P(?:175|176|177)N\d+[a-z]?')
    text = text.replace("'R. The music performance'", "'R. Gifts and departure'")
    target.write_text(text, encoding='utf-8', newline='\n')
    py_compile.compile(str(target), doraise=True)
print('Prepared and syntax-checked Unit18 complete assembly, parity, rendering and page-acceptance helpers. No exports produced or accepted.')
