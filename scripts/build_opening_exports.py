"""Assemble/compile complete opening-revision documents in shared Cambria style.

Default output is ignored build/opening/exports. --output-root typesetting
explicitly selects current TeX when reviewed masters are ready. No retained
PDF is replaced. Unit 2 learner is compile-only; preserve its existing layout.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from build_course_exports import diagnostics
import render_course_tables as course_tables
from render_course_tables import inline_tex as flat_inline_tex, render_block

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = {
    "pronunciation/learner": ("guides/pronunciation/student.md", "pronunciation/pronunciation.tex"),
    "pronunciation/key": ("guides/pronunciation/answer-key.md", "pronunciation/answer-key.tex"),
    "ch01/learner": ("chapters/ch01/student.md", "ch01/chapter-01.tex"),
    "ch01/key": ("chapters/ch01/answer-key.md", "ch01/answer-key.tex"),
    "ch02/learner": ("chapters/ch02/student.md", "ch02/chapter-02.tex"),
}
DEFAULT_IDS = list(DOCUMENTS)[:4]
VOCABULARY_HEADERS = ["Noun", "Gender", "Meaning", "G sg", "N pl", "Pattern; limit"]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path):
    return path.resolve().relative_to(ROOT).as_posix()


def workspace_path(value):
    path = (ROOT / value).resolve() if not Path(value).is_absolute() else Path(value).resolve()
    path.relative_to(ROOT)
    return path


def selected(value):
    ids = list(dict.fromkeys(filter(None, value.split(",")))) if value else DEFAULT_IDS
    if set(ids) - DOCUMENTS.keys():
        raise ValueError("Unknown document IDs: " + ", ".join(sorted(set(ids) - DOCUMENTS.keys())))
    return ids


def comments(text):
    return [" ".join(m.split()) for m in re.findall(r"<!--(.*?)-->", text, re.S)]


def inline_tex(text):
    """Retain italic model words inside the guide's bold numbered headings."""
    pieces = re.split(r"(\*\*.*?\*\*)", text)
    return "".join(r"\textbf{"+flat_inline_tex(p[2:-2])+"}"
                   if p.startswith("**") and p.endswith("**") and len(p) >= 4
                   else flat_inline_tex(p) for p in pieces)


def matrices(raw):
    """Builder's line parser; checker inventories Markdown independently."""
    lines = raw.splitlines(keepends=True)
    tables, offset, i = [], 0, 0
    while i < len(lines):
        if lines[i].lstrip().startswith("|") and i + 1 < len(lines) and re.fullmatch(r"\s*\|[- :|]+\|\s*", lines[i+1]):
            begin, block = offset, []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                block.append(lines[i]); offset += len(lines[i]); i += 1
            rows = [[c.strip() for c in re.split(r"(?<!\\)\|", line.strip()[1:-1])] for line in block]
            if len(rows[0]) < 2 or any(len(r) != len(rows[0]) for r in rows):
                raise ValueError("Ragged Markdown table")
            tables.append({"start":begin, "end":offset, "headers":rows[0], "rows":rows[2:], "raw":"".join(block)})
        else:
            offset += len(lines[i]); i += 1
    return tables


def table_matrix(table):
    """Preserve the documented six-field vocabulary in four columns."""
    if table["headers"] == VOCABULARY_HEADERS:
        rows = [[f"{r[0]} ({r[1]})", r[2], f"G sg {r[3]} N pl {r[4]}", r[5]] for r in table["rows"]]
        return {"headers":["Noun; gender","Meaning","Diagnostic forms","Pattern; limit"], "rows":rows}
    return {"headers":table["headers"], "rows":table["rows"]}


def render_opening_table(table, table_id):
    """Use the common renderer, with bounded content-based layout choices.

    The historical row-count threshold alone does not fit the long Unit 1
    reading-support table. Dense prose tables may therefore break across
    pages. The shared style object/file and historical receipts are unchanged.
    """
    matrix = table_matrix(table)
    headers = matrix["headers"]
    widths = None
    if table["headers"] == VOCABULARY_HEADERS:
        widths = [24.0,39.0,28.0,24.564]
    elif headers == ["Word","Supplied meaning","Pronunciation help"]:
        widths = [18.0,21.0,79.376]
    elif headers == ["Position","Ordinary g sound","Model"]:
        widths = [46.0,20.0,52.376]
    elif (len(headers) == 5 and headers[0] == "Case"
          and any(course_tables.markdown_plain(c) == "gegaderungum" for row in matrix["rows"] for c in row)):
        widths = [19.0,23.0,23.0,23.0,24.752]
    characters = sum(len(course_tables.markdown_plain(c)) for row in matrix["rows"] for c in row)
    dense = characters > 1600
    original_style = course_tables.STYLE
    original_inline = course_tables.inline_tex
    try:
        course_tables.inline_tex = inline_tex
        if dense:
            course_tables.STYLE = {**original_style,"longtable_data_rows":0}
        rendered, audit = render_block([matrix], table_id, comments=comments(table["raw"]),
                                       width_overrides={table_id+"-P01":widths} if widths else None)
    finally:
        course_tables.STYLE = original_style
        course_tables.inline_tex = original_inline
    audit["opening_layout"] = {"visible_data_characters":characters,"dense_prose_longtable":dense,
                               "width_override_by_content":widths is not None}
    return rendered, audit


def assemble(raw, document_id, destination):
    if document_id == "ch02/learner":
        raise ValueError("Unit 2 learner is compile/check only; preserve its TeX layout.")
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    if re.search(r"!\[|\[[^\]]+\]\([^)]+\)|^\[\^", raw, re.M) or chr(96) in raw:
        raise ValueError("Unsupported links/code/footnotes; extend both inventories explicitly.")
    tables = matrices(raw)
    parts, cursor = [], 0
    for i, table in enumerate(tables):
        parts.extend([raw[cursor:table["start"]], f"\n\n@@TABLE:{i}@@\n\n"])
        cursor = table["end"]
    parts.append(raw[cursor:])
    body = re.sub(r"(?m)^(<!--.*-->)$", r"\n\1\n", "".join(parts))
    out, table_audit, paragraph_number, title = [], [], 0, None

    def paragraph(text):
        nonlocal paragraph_number
        paragraph_number += 1
        pid = f"P{paragraph_number:03}"
        out.extend([f"% mdparagraph:{pid}:begin", text, f"% mdparagraph:{pid}:end", ""])

    for chunk in re.split(r"\n\s*\n", body.strip()):
        lines = chunk.splitlines()
        if not lines:
            continue
        if lines[0].startswith("# "):
            if title is not None or len(lines) != 1:
                raise ValueError("Expected one single-line title")
            title = lines[0][2:]; continue
        match = re.fullmatch(r"@@TABLE:(\d+)@@", chunk)
        if match:
            i = int(match[1]); table = tables[i]; tid = f"T{i+1:02}"
            rendered, audit = render_opening_table(table, tid)
            out.extend([rendered, ""]); table_audit.append(audit); continue
        if all(line.startswith("<!--") and line.endswith("-->") for line in lines):
            # Keep a supplied sentence frame with the prompt that identifies it.
            # These bounded reservations also keep the first key-table caption
            # with its table; they do not change any master text or task IDs.
            if document_id == "ch01/learner":
                case = re.search(r"item: CH01-CASE(\d+)", chunk)
                if case:
                    lines_needed = 9 if int(case[1]) >= 9 else 7
                    out.append(r"\reserve{" + str(lines_needed) + r"\baselineskip}")
            elif document_id == "ch01/key" and "item: CH01-F01" in chunk:
                out.append(r"\reserve{8\baselineskip}")
            out.extend("% "+c for c in comments(chunk)); continue
        if "<!--" in chunk:
            raise ValueError("Inline prose comments need an explicit handling rule")
        if lines[0].startswith("##"):
            match = re.fullmatch(r"(#{2,4}) (.+)", chunk)
            if not match:
                raise ValueError("Unsupported heading")
            command = {2:"section",3:"subsection",4:"subsubsection"}[len(match[1])]
            out.append(r"\reserve{4\baselineskip}")
            paragraph("\\"+command+"*{"+inline_tex(match[2])+"}")
        elif all(line.startswith("- ") for line in lines):
            out.append(r"\begin{itemize}")
            for line in lines:
                paragraph(r"\item "+inline_tex(line[2:]))
            out.append(r"\end{itemize}")
        elif all(line.startswith("> ") for line in lines):
            paragraph(r"\readingtext{"+inline_tex(" ".join(line[2:] for line in lines))+"}")
        elif all(re.match(r"^\d+\.\s+", line) for line in lines):
            for line in lines:
                number, text = re.match(r"^(\d+)\.\s+(.*)", line).groups()
                paragraph(r"\itempara{"+number+"}{"+inline_tex(text)+"}")
        else:
            text = " ".join(line.strip() for line in lines)
            numbered = re.match(r"^(\d+)\.\s+(.*)", text)
            if numbered:
                paragraph(r"\itempara{"+numbered[1]+"}{"+inline_tex(numbered[2])+"}")
            else:
                rendered = inline_tex(text)
                if re.fullmatch(r"\*\*.+\*\*", text):
                    rendered += r"\par\nobreak"
                paragraph(rendered)
    if title is None:
        raise ValueError("Missing title")
    if document_id.startswith("pronunciation/"):
        prefix = "GUIDE" if document_id.endswith("/learner") else "SEPARATE KEY"
        subtitle = title
        running = "Pronunciation" if document_id.endswith("/learner") else "Pronunciation key"
    else:
        match = re.fullmatch(r"Unit (\d+)\. (.+)", title)
        if not match:
            raise ValueError("Unit title must identify its number")
        prefix, subtitle, running = "UNIT "+match[1], match[2], title
    layout = os.path.relpath(ROOT/"typesetting/book-layout.tex", destination.parent).replace("\\", "/")
    preamble = [
        "% Opening revision; current Markdown assembly, not historical acceptance.",
        "% Editorial master: "+DOCUMENTS[document_id][0],
        "% Master SHA-256: "+digest(ROOT/DOCUMENTS[document_id][0]),
        r"\newcommand{\runningtitle}{"+inline_tex(running)+"}",
        r"\input{"+layout+"}", r"\hyphenpenalty=10000", r"\exhyphenpenalty=10000", r"\emergencystretch=3em",
        r"\newcommand{\reserve}[1]{\par\penalty-100\begingroup\dimen0=\pagegoal\advance\dimen0 by-\pagetotal\ifdim\dimen0<#1\newpage\fi\endgroup}",
        r"\newcommand{\itempara}[2]{\par\addvspace{3pt}\begingroup\raggedright\noindent\hangindent=1.8em\hangafter=1\makebox[1.8em][l]{#1.}#2\par\endgroup}",
        r"\begin{document}", r"\addfontfeatures{Ligatures=TeXOff}", r"\raggedright",
        r"\booktitle{"+prefix+"}{"+inline_tex(subtitle)+"}", "",
    ]
    return "\n".join(preamble+out+[r"\end{document}", ""]), {
        "title":title, "paragraphs":paragraph_number, "tables":len(tables),
        "comments":comments(raw), "table_rendering":table_audit}


def compile_tex(texpath, output, executable):
    output.mkdir(parents=True, exist_ok=True)
    before, passes = digest(texpath), []
    for number in (1, 2):
        output_arg = os.path.relpath(output, texpath.parent).replace("\\", "/")
        command = [executable,"-interaction=nonstopmode","-halt-on-error","-output-directory="+output_arg,texpath.name]
        options = {"creationflags":subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}
        result = subprocess.run(command, cwd=texpath.parent, capture_output=True, text=True, encoding="utf-8", errors="replace", **options)
        stdout = output/f"{texpath.stem}-opening-pass{number}.stdout.txt"
        stdout.write_text(result.stdout+"\n"+result.stderr, encoding="utf-8", newline="\n")
        passes.append({"pass":number,"exit_code":result.returncode,"stdout":relative(stdout),"sha256":digest(stdout)})
        if result.returncode:
            return {"status":"compile_failed","passes":passes,"tail":(result.stdout+result.stderr).splitlines()[-25:]}
        live_log = output/(texpath.stem+".log")
        pass_log = output/f"{texpath.stem}-opening-pass{number}.log"
        shutil.copyfile(live_log,pass_log)
        passes[-1].update(log=relative(pass_log),log_sha256=digest(pass_log),
                          diagnostics=diagnostics(pass_log.read_text(encoding="utf-8",errors="replace")))
    if digest(texpath) != before:
        raise ValueError("TeX changed during compilation")
    log, pdf = output/(texpath.stem+".log"), output/(texpath.stem+".pdf")
    text = log.read_text(encoding="utf-8", errors="replace")
    findings = diagnostics(text)
    pages = re.search(r"Output written on .*?\((\d+) pages?", text, re.S)
    if not pages or not pdf.exists():
        raise ValueError("Missing final PDF/page count")
    return {"status":"diagnostics_pending" if findings else "compiled_clean","passes":passes,
            "pdf":relative(pdf),"pdf_sha256":digest(pdf),"pages":int(pages[1]),
            "log":relative(log),"log_sha256":digest(log),"diagnostics":findings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", required=True, choices=["assemble","compile"])
    parser.add_argument("--select", default="", help="Comma-separated IDs; default the four revised documents.")
    parser.add_argument("--output-root", type=Path, default=Path("build/opening/exports"))
    parser.add_argument("--report", type=Path)
    installed = Path("C:/Users/Ross/AppData/Local/texlive/2026/bin/windows/lualatex.exe")
    parser.add_argument("--lualatex", default=str(installed) if installed.exists() else shutil.which("lualatex") or "lualatex")
    args = parser.parse_args(); ids = selected(args.select)
    if args.stage == "assemble" and "ch02/learner" in ids:
        parser.error("ch02/learner is compile/check only")
    output_root = workspace_path(args.output_root)
    report_path = workspace_path(args.report or Path(f"build/opening/export-{args.stage}.json"))
    report = {"schema_version":1,"revision":"opening","stage":args.stage,
              "created_utc":datetime.now(timezone.utc).isoformat(),"script_sha256":digest(Path(__file__)),
              "layout_sha256":digest(ROOT/"typesetting/book-layout.tex"),"documents":[],
              "helper_sha256":{name:digest(ROOT/"scripts"/name) for name in ["render_course_tables.py","build_course_exports.py"]},
              "historical_receipts_reused":False,"visual_or_linguistic_acceptance_inferred":False}
    for document_id in ids:
        master, tex_relative = DOCUMENTS[document_id]
        texpath = (ROOT/"typesetting"/tex_relative) if document_id == "ch02/learner" else output_root/tex_relative
        item = {"id":document_id,"master":master,"master_sha256":digest(ROOT/master),"tex":relative(texpath)}
        try:
            if args.stage == "assemble":
                tex, inventory = assemble((ROOT/master).read_text(encoding="utf-8-sig"), document_id, texpath)
                texpath.parent.mkdir(parents=True, exist_ok=True)
                texpath.write_text(tex, encoding="utf-8", newline="\n")
                item.update(status="assembled_pending_independent_check",inventory=inventory)
            else:
                item.update(compile_tex(texpath, output_root/Path(tex_relative).parent/"build", args.lualatex))
            item["tex_sha256"] = digest(texpath)
            if digest(ROOT/master) != item["master_sha256"]:
                raise ValueError("Master changed during operation")
        except Exception as error:
            item.update(status="failed",error=str(error))
        report["documents"].append(item)
        print(document_id, item["status"], item.get("pages",""), flush=True)
        if item.get("error"):
            print(item["error"], flush=True)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    passed = all(d["status"] in {"assembled_pending_independent_check","compiled_clean"} for d in report["documents"])
    report["status"] = "pass_pending_content_and_page_review" if passed else "fail"
    report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    print(relative(report_path))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
