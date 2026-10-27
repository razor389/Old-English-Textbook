"""Adapt this project's inspected publication helpers without changing prior units."""
from pathlib import Path
import py_compile
root=Path(__file__).resolve().parents[1]
dest=root/'typesetting/ch16/build'
dest.mkdir(parents=True,exist_ok=True)
for source,target in [('_assemble_unit15.py','_assemble_unit16.py'),('_check_content_parity.py','_check_content_parity.py'),('_render_pages.py','_render_pages.py'),('_accept_pages.py','_accept_pages.py')]:
    path=dest/target
    assert not path.exists(), 'Preserve any independently edited helper'
    text=(root/'typesetting/ch15/build'/source).read_text(encoding='utf-8')
    for old,new in [('Unit 15','Unit 16'),('Unit15','Unit16'),('UNIT 15','UNIT 16'),('ch15','ch16'),('chapter-15','chapter-16'),('unit15','unit16'),("'unit': '15'","'unit': '16'")]:
        text=text.replace(old,new)
    if source=='_assemble_unit15.py':
        text=text.replace('Negation and quantity','Narrative and speech').replace('Negation, quantity and comparison in discourse','Extended narrative and speech')
        text=text.replace("[h.lower() for h in header[1:4]]==['masculine singular','feminine singular','neuter singular']", "[h.lower() for h in header[1:4]] in [['masculine singular','feminine singular','neuter singular'],['m sg','f sg','n sg']]")
        text=text.replace("r'[DPR]\\d+'", "r'(?:[DPR]\\d+|P(?:168|169|170)N\\d+)'")
        # This complete reading spans several pages. Each paragraph may break;
        # never place the whole444-word scene inside an unbreakable minipage.
        text=text.replace("source_dialogue_open=True\n                    out.append(r'\\par\\begin{minipage}{\\linewidth}\\raggedright')", "source_dialogue_open=True")
        text=text.replace("source_dialogue_open = True\n                out.append(r'\\par\\begin{minipage}{\\linewidth}\\raggedright')", "source_dialogue_open = True")
        text=text.replace("if source_dialogue_open and reading_next == 0:\n                out.append(r'\\end{minipage}\\par')", "if source_dialogue_open and reading_next == 0:\n                out.append(r'\\par')")
        text=text.replace("Cook (?:IX|X, XI)", "Cook (?:XII, XIII|XII,XIII)")
        text=text.replace("body.startswith(('**F01.', '**F04.', '**S01.'))", "body.startswith(('**F01.', '**F02.', '**F03.', '**F04.', '**F05.', '**R01.'))")
        # Key item markers alone also need to leave full translation/form groups
        # breakable. The actual emitted layout is inspected after compilation.
        text=text.replace("if task_marker and not label_pending:\n                close_task()\n                out += [r'\\par\\begin{minipage}{\\linewidth}\\raggedright']\n                task_open = True", "if task_marker and not label_pending:\n                close_task()\n                if stem == 'answer-key' and any(code in body for code in ['-F01','-F02','-F03','-F04','-F05','-R01']):\n                    out.append(r'\\reserve{8\\baselineskip}')\n                else:\n                    out += [r'\\par\\begin{minipage}{\\linewidth}\\raggedright']\n                    task_open = True")
    elif source=='_check_content_parity.py':
        text=text.replace("r'[DPR]\\d+'", "r'(?:[DPR]\\d+|P(?:168|169|170)N\\d+)'")
        text=text.replace('The three exact source readings use the reading style; the eight short examples stay with their translations.', 'The complete source scene uses the reading style with natural paragraph/page breaks; four short examples stay with their translations.')
        text=text.replace('D/P/R-prefixed numbers','page-specific original note labels')
    path.write_text(text,encoding='utf-8',newline='\n')
    py_compile.compile(str(path),doraise=True)
    print(path.relative_to(root).as_posix(),'prepared, not run')
