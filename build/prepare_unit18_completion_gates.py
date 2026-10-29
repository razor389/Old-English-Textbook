"""Adapt inspected preservation and completion gates without running them."""
from pathlib import Path
import py_compile

for name in ['check_unit17_integration.py', 'finalize_unit17_metadata.py']:
    target = Path('build') / name.replace('unit17', 'unit18')
    assert not target.exists(), target
    text = (Path('build') / name).read_text(encoding='utf-8')
    # Change the previous forward boundary before replacing the current unit.
    text = text.replace('No Unit 18 work is included.',
                        'No unrequested sequel is included.')
    text = text.replace('Unit18 remains undrafted; begin only when requested.',
                        'The planned eighteen-unit course is complete; further work requires a new request.')
    text = text.replace('Unit17 complete; no Unit18 drafting.',
                        'Unit18 and the planned course complete; no unrequested sequel drafted.')
    for old, new in [('unit17', 'unit18'), ('Unit17', 'Unit18'), ('Unit 17', 'Unit 18'),
                     ('ch17', 'ch18'), ('chapter-17', 'chapter-18'),
                     ('through_ch16', 'through_ch17'), ('sixteen-unit baseline', 'seventeen-unit baseline'),
                     ("len(b['files']) == 2935", "len(b['files']) == 3290"),
                     ("'all_cook_items_retained':82", "'all_cook_items_retained':47, 'course_cook_items_assigned':644")]:
        text = text.replace(old, new)
    target.write_text(text, encoding='utf-8', newline='\n')
    py_compile.compile(str(target), doraise=True)
print('Prepared Unit18 deep preservation and final metadata gates; syntax checked only.')
