"""Prepare inspected freeze, independent-review and preserved-register gates.

No acceptance or integration is performed by this preparatory helper.
"""
from pathlib import Path
import py_compile

for name in ['freeze_unit17_solutions.py', 'accept_unit17_text.py', 'merge_unit17_registers.py']:
    target = Path('build') / name.replace('unit17', 'unit18')
    assert not target.exists(), target
    text = (Path('build') / name).read_text(encoding='utf-8-sig')
    for old, new in [('unit17', 'unit18'), ('Unit17', 'Unit18'),
                     ('Unit 17', 'Unit 18'), ('ch17', 'ch18'),
                     ('through_ch16', 'through_ch17'), ('Units 1–17', 'Units 1–18')]:
        text = text.replace(old, new)
    target.write_text(text, encoding='utf-8', newline='\n')
    py_compile.compile(str(target), doraise=True)
print('Prepared Unit18 freeze, independent acceptance and guarded register integration helpers; syntax checked only.')
