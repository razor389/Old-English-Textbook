"""Prepare guarded Unit16 integration helpers; do not execute acceptance gates."""
from pathlib import Path
import py_compile
root=Path(__file__).resolve().parents[1]
for name in ['merge_unit15_registers.py','check_unit15_integration.py','accept_unit15_text.py','finalize_unit15_metadata.py']:
    target=root/'build'/name.replace('unit15','unit16')
    assert not target.exists(), 'Preserve independently edited helper'
    text=(root/'build'/name).read_text(encoding='utf-8')
    for old,new in [('No Unit 16','No Unit 17'),('no Unit16','no Unit17'),('Unit16 remains','Unit17 remains'),('through_ch14','through_ch15'),('fourteen-unit','fifteen-unit'),('Unit 15','Unit 16'),('Unit15','Unit16'),('unit15','unit16'),('ch15','ch16'),('chapter-15','chapter-16'),('Units 1–15','Units 1–16')]:
        text=text.replace(old,new)
    if name=='check_unit15_integration.py':
        text=text.replace("len(b['files']) == 2313","len(b['files']) == 2637")
    elif name=='accept_unit15_text.py':
        text=text.replace("len(c['assigned_items'])==105","len(c['assigned_items'])==c['contract_metrics']['tasks']")
        text=text.replace("len(expected_outputs)==322","len(expected_outputs)==c['contract_metrics']['requested_output_positions']")
        text=text.replace('all105 actual learner tasks','all contracted actual learner tasks')
    elif name=='finalize_unit15_metadata.py':
        text=text.replace("'all_assigned_tasks_reviewed':105,'all_cook_items_retained':50", "'all_assigned_tasks_reviewed':c['contract_metrics']['tasks'],'all_cook_items_retained':59")
    target.write_text(text,encoding='utf-8',newline='\n')
    py_compile.compile(str(target),doraise=True)
    print(target.relative_to(root).as_posix(),'prepared, not run')
