"""Independently check current opening Markdown, TeX, and complete PDF text.

Uses the existing strict TeX decoder, not an assembly receipt or old table
acceptance. --tex-only checks scratch parser output before compilation.
Unit 2's current TeX is read without reassembly; unmarked prose is permitted
only when complete decoded body text agrees with the current master.
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import unicodedata
import check_course_layout as tables
from check_course_exports import chars, group, master_events, norm, quote_projection, texplain
from build_course_exports import diagnostics
from render_course_tables import decode_tex_tables

ROOT = Path(__file__).resolve().parents[1]
# Deliberately not imported from the emitter.
DOCUMENTS = {
    "pronunciation/learner": ("guides/pronunciation/student.md","pronunciation/pronunciation.tex"),
    "pronunciation/key": ("guides/pronunciation/answer-key.md","pronunciation/answer-key.tex"),
    "ch01/learner": ("chapters/ch01/student.md","ch01/chapter-01.tex"),
    "ch01/key": ("chapters/ch01/answer-key.md","ch01/answer-key.tex"),
    "ch02/learner": ("chapters/ch02/student.md","ch02/chapter-02.tex"),
}
TABLE_BLOCK = re.compile(r"(?ms)^% mdtable:(T\d+):begin\r?\n(.*?)^% mdtable:\1:end")
CAPTION = re.compile(r"(?ms)^% course-caption:(T\d+):(\d+):begin\r?\n(.*?)^% course-caption:\1:\2:end")
PARAGRAPH = re.compile(r"(?ms)^% mdparagraph:(P\d+):begin\r?\n(.*?)^% mdparagraph:\1:end")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path):
    return path.resolve().relative_to(ROOT).as_posix()


def mdplain(value):
    value = re.sub(r"<!--.*?-->", "", value)
    value = value.replace(r"\*", "\uE000").replace("**", "")
    value = re.sub(r"(?<!\w)\*([^*\n]+?)\*(?!\w)", r"\1", value)
    return norm(value.replace("\uE000", "*"))


def expected_tables(table):
    """Explicit current-master projection, independent of render audits."""
    rows = [[mdplain(c) for c in row] for row in [table["headers"], *table["rows"]]]
    if rows[0] == ["Noun","Gender","Meaning","G sg","N pl","Pattern; limit"]:
        return [[["Noun; gender","Meaning","Diagnostic forms","Pattern; limit"]] +
                [[r[0]+" ("+r[1]+")",r[2],"G sg "+r[3]+" N pl "+r[4],r[5]] for r in rows[1:]]]
    if len(rows[0]) <= 5:
        return [rows]
    columns = [[0]+list(range(start,min(start+3,len(rows[0])))) for start in range(1,len(rows[0]),3)]
    return [[[row[c] for c in cols] for row in rows] for cols in columns]


def strip_layout(text):
    """Discard only known invisible commands before strict visible decoding."""
    pattern = re.compile(r"\\(?:reserve|addfontfeatures|addvspace|vspace\*?)")
    result, pos = [], 0
    for match in pattern.finditer(text):
        if match.start() < pos:
            continue
        result.append(text[pos:match.start()])
        _, pos = group(text, match.end())
    result.append(text[pos:])
    return "".join(result)


def difference(wanted, actual):
    stop = min(len(wanted),len(actual))
    at = next((i for i in range(stop) if wanted[i] != actual[i]),stop)
    return {"first_difference":at,"expected_length":len(wanted),"actual_length":len(actual),
            "expected_context":wanted[max(0,at-80):at+180],"actual_context":actual[max(0,at-80):at+180]}


def pdf_body(raw, running):
    pages = []
    headers = {"Old English",running,"Old English "+running,running+" Old English"}
    for page in raw.replace("\r\n","\n").replace("\r","\n").split("\f"):
        lines = page.splitlines()
        while lines and not lines[0].strip():
            lines.pop(0)
        for _ in range(2):
            if lines and norm(lines[0]) in headers:
                lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        if lines and re.fullmatch(r"\s*\d+\s*",lines[-1]):
            lines.pop()
        pages.append("\n".join(lines))
    return "\n".join(pages)


def remove_furniture(gap, furniture):
    remaining = gap
    used = []
    for _ in range(len(gap)+1):
        if not remaining:
            return "", used
        found = next((x for x in furniture if remaining.startswith(x)),None)
        if found is None:
            return remaining, used
        used.append(found); remaining = remaining[len(found):]
    raise ValueError("Furniture removal did not advance")


def inspect(document_id, output_root, tex_only, pdf_location, pdftotext):
    master_name, tex_name = DOCUMENTS[document_id]
    mpath = ROOT/master_name
    tpath = ROOT/"typesetting"/tex_name if document_id == "ch02/learner" else output_root/tex_name
    ppath = output_root/Path(tex_name).parent/("build" if pdf_location == "build" else "")/(tpath.stem+".pdf")
    logpath = output_root/Path(tex_name).parent/"build"/(tpath.stem+".log")
    errors = []
    def check(ok, message):
        if not ok:
            errors.append(message)
    raw = mpath.read_text(encoding="utf-8-sig").replace("\r\n","\n").replace("\r","\n")
    tex = tpath.read_text(encoding="utf-8-sig").replace("\r\n","\n").replace("\r","\n")
    identity = {"master":master_name,"master_sha256":digest(mpath),"tex":rel(tpath),"tex_sha256":digest(tpath)}
    parsed = tables.parse_md(raw)
    inventory = {"tables":[dict(t,original_index_zero_based=i,revised=t["raw"]) for i,t in enumerate(parsed)]}
    title, events, _ = master_events(raw,inventory)
    prose = [e["text"] for e in events if e["kind"] == "prose"]
    if document_id.startswith("pronunciation/"):
        prefix = "GUIDE" if document_id.endswith("/learner") else "SEPARATE KEY"
        subtitle = title
    else:
        match = re.fullmatch(r"Unit (\d+)\. (.+)",title)
        if not match:
            raise ValueError("Invalid master title")
        prefix, subtitle = "UNIT "+match[1], match[2]
    expected_title = prefix+" "+subtitle
    comments = [norm(x) for x in re.findall(r"<!--(.*?)-->",raw,re.S)]
    tags = {x.split(":",1)[0] for x in comments if ":" in x}
    actual_comments = []
    for line in tex.splitlines():
        if line.startswith("% "):
            value = norm(line[2:])
            if value.split(":",1)[0] in tags:
                actual_comments.append(value)
    check(actual_comments == comments, {"type":"editorial_comment_or_ID_order","expected":comments,"actual":actual_comments})
    for tag in ["item","answer"]:
        ids = [c.split(":",1)[1].strip() for c in comments if c.startswith(tag+":")]
        check(len(ids) == len(set(ids)), {"type":"duplicate_master_ID","tag":tag})
    paragraphs = list(PARAGRAPH.finditer(tex))
    if document_id != "ch02/learner":
        check([p[1] for p in paragraphs] == [f"P{i:03}" for i in range(1,len(prose)+1)], "Missing, duplicate or unordered paragraph markers")
        for number,(marked,wanted) in enumerate(zip(paragraphs,prose),1):
            check(chars(texplain(marked[2])) == chars(wanted), {"type":"marked_prose","paragraph":number,"expected":wanted,"actual":texplain(marked[2])})
    blocks = list(TABLE_BLOCK.finditer(tex))
    if document_id != "ch02/learner":
        check([b[1] for b in blocks] == [f"T{i:02}" for i in range(1,len(parsed)+1)], "Missing, duplicate or unordered table markers")
    check(len(re.findall(r"(?m)^% mdtable:T\d+:begin",tex)) == len(blocks), "Unpaired table markers")
    actual_matrices = []
    for block in blocks:
        actual_matrices.extend(decode_tex_tables(block[2]))
    wanted_matrices = [matrix for t in parsed for matrix in expected_tables(t)]
    check(actual_matrices == wanted_matrices, {"type":"complete_table_cells","expected_matrices":len(wanted_matrices),"actual_matrices":len(actual_matrices),
          "first_mismatch":next((i+1 for i,(a,b) in enumerate(zip(wanted_matrices,actual_matrices)) if a != b),None)})
    check(not tables.ERRORS, {"type":"table_decoder","errors":list(tables.ERRORS)})
    tables.ERRORS.clear()
    all_envs = len(re.findall(r"\\begin\{(?:tabular|longtable)\}",tex))
    check(all_envs == len(actual_matrices), "Unmarked/undecoded physical table")
    for block in blocks:
        for table in re.finditer(r"\\begin\{longtable\}.*?\\end\{longtable\}",block[2],re.S):
            first = re.search(r"\\toprule(.*?)\\midrule",table[0],re.S)[1]
            repeated = table[0].split(r"\endfirsthead",1)[1].split(r"\endhead",1)[0]
            check(first == re.search(r"\\toprule(.*?)\\midrule",repeated,re.S)[1], "Repeated table header differs")
    body = tex.split(r"\begin{document}",1)[1].split(r"\end{document}",1)[0]
    body = TABLE_BLOCK.sub(lambda m:"\n".join(c[3] for c in CAPTION.finditer(m[2])),body)
    decoded = chars(texplain(strip_layout(body)))
    expected = chars(expected_title+" "+" ".join(prose))
    check(decoded == expected, {"type":"complete_visible_TeX_prose",**difference(expected,decoded)})
    running_match = re.search(r"\\newcommand\{\\runningtitle\}",tex)
    running_raw,_ = group(tex,running_match.end())
    running = texplain(running_raw)
    result = {"id":document_id,**identity,"paragraphs":len(prose),"marked_paragraphs":len(paragraphs),
              "markdown_tables":len(parsed),"physical_tables":len(actual_matrices),
              "logical_table_cells":sum(len(row) for t in parsed for row in [t["headers"],*t["rows"]]),
              "editorial_comments":len(comments),"ordered_editorial_ID_comments":comments,
              "errors":errors,"pdf_checked":False,"missing_pdf_events":[]}
    if tex_only:
        return result
    rawpdf = subprocess.run([pdftotext,"-enc","UTF-8","-raw",str(ppath),"-"],capture_output=True,check=True).stdout.decode("utf-8")
    pdf = chars(pdf_body(rawpdf,running))
    projected = quote_projection(pdf)
    visible = [{"kind":"title","text":expected_title}]
    for event in events:
        if event["kind"] == "prose":
            visible.append(event)
        else:
            for matrix in expected_tables(parsed[event["number"]-1]):
                visible.extend({"kind":"table_row","table":event["number"],"text":" ".join(row)} for row in matrix)
    furniture = {"•",chars("Continued on the following page."),chars("Continued on next page.")}
    furniture.update(chars(" ".join(matrix[0])) for matrix in wanted_matrices)
    furniture = sorted({quote_projection(s) for s in furniture if s},key=len,reverse=True)
    cursor, missing, gaps, projections, allowed = 0, [], [], [], []
    for i,event in enumerate(visible,1):
        wanted = chars(event["text"])
        at = projected.find(quote_projection(wanted),cursor)
        if at < 0:
            missing.append({"event":i,**event}); continue
        gap = projected[cursor:at]
        remainder, used = remove_furniture(gap,furniture)
        if remainder:
            gaps.append({"before_event":i,"unexpected":remainder[:500],"length":len(remainder)})
        if used:
            allowed.append({"before_event":i,"furniture":used})
        if pdf[at:at+len(wanted)] != wanted:
            projections.append({"event":i,"expected":wanted,"actual":pdf[at:at+len(wanted)]})
        cursor = at+len(wanted)
    remainder, used = remove_furniture(projected[cursor:],furniture)
    if remainder:
        gaps.append({"after_final_event":True,"unexpected":remainder[:500],"length":len(remainder)})
    if used:
        allowed.append({"after_final_event":True,"furniture":used})
    check(not gaps, {"type":"unexpected_PDF_text","gaps":gaps})
    suspicious = Counter(c for c in rawpdf if c == "\ufffd" or unicodedata.category(c) in ["Co","Cn"] or (unicodedata.category(c) == "Cc" and not c.isspace()))
    check(not suspicious, {"type":"suspicious_PDF_Unicode","characters":dict(suspicious)})
    log = logpath.read_text(encoding="utf-8",errors="replace")
    findings = diagnostics(log)
    check(not findings, {"type":"compile_diagnostics","findings":findings})
    page_count = rawpdf.count("\f")+bool(rawpdf.split("\f")[-1].strip())
    logged = re.search(r"Output written on .*?\((\d+) pages?",log,re.S)
    check(logged is not None and int(logged[1]) == page_count, "PDF/log page count differs")
    check(digest(mpath) == identity["master_sha256"] and digest(tpath) == identity["tex_sha256"], "Inputs changed during check")
    result.update(pdf_checked=True,pdf=rel(ppath),pdf_sha256=digest(ppath),pages=page_count,
                  log=rel(logpath),log_sha256=digest(logpath),pdf_events=len(visible),
                  missing_pdf_events=missing,unexpected_pdf_gaps=gaps,allowed_pdf_furniture=allowed,
                  typographic_quote_projections=projections,diagnostics=findings)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--select",default="",help="Comma-separated IDs; optionally include ch02/learner.")
    parser.add_argument("--output-root",type=Path,default=Path("build/opening/exports"))
    parser.add_argument("--tex-only",action="store_true")
    parser.add_argument("--pdf-location",choices=["build","retained"],default="build")
    parser.add_argument("--pdftotext",default=shutil.which("pdftotext") or "C:/Program Files/Git/mingw64/bin/pdftotext.exe")
    parser.add_argument("--report",type=Path,default=Path("build/opening/export-check.json"))
    args = parser.parse_args()
    ids = list(dict.fromkeys(filter(None,args.select.split(",")))) if args.select else list(DOCUMENTS)[:4]
    if set(ids)-DOCUMENTS.keys():
        parser.error("Unknown document ID")
    output = (ROOT/args.output_root).resolve()
    reports = []
    for document_id in ids:
        try:
            result = inspect(document_id,output,args.tex_only,args.pdf_location,args.pdftotext)
        except Exception as error:
            result = {"id":document_id,"errors":[{"type":"check_exception","message":str(error)}],"missing_pdf_events":[]}
        reports.append(result)
        print(document_id,len(result["errors"]),"errors;",len(result["missing_pdf_events"]),"missing PDF events",flush=True)
    passed = all(not r["errors"] and not r["missing_pdf_events"] for r in reports)
    report = {"schema_version":1,"status":"pass" if passed else "fail",
              "scope":"current Markdown→actual TeX" if args.tex_only else "current Markdown→actual TeX→complete ordered PDF text",
              "created_utc":datetime.now(timezone.utc).isoformat(),"script_sha256":digest(Path(__file__)),
              "historical_acceptance_reused":False,
              "method":"Independent current Markdown inventory; strict existing TeX prose/table decoders; full prose equality; all physical table cells; exact ordered editorial comments/IDs. PDF events follow the master and explicit table projections. Extra text is rejected except recorded repeated table headers, bullets and continuation furniture. Only NFC/whitespace/soft-hyphen and reported typographic quote projections are permitted.",
              "documents":reports,
              "limitations":"Content parity and compiler diagnostics do not establish linguistic correctness or visual page acceptance; actual independent review and page inspection remain necessary."}
    dest = (ROOT/args.report).resolve(); dest.relative_to(ROOT)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    print(rel(dest))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
