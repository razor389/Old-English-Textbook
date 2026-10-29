"""Check both pronunciation masters, TeX, PDF text, and the recorded course boundary."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unicodedata

import check_course_layout as tables
from check_course_exports import chars, group, master_events, norm, quote_projection, texplain
from build_course_exports import diagnostics

ROOT=Path(__file__).resolve().parents[1]
PDFTOTEXT=Path("C:/Program Files/Git/mingw64/bin/pdftotext.exe")

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def mdplain(value):
    return norm(value.replace("**","").replace("*",""))

def pdf_body(raw,running):
    pages=[]
    for page in raw.replace("\r\n","\n").replace("\r","\n").split("\f"):
        lines=page.splitlines()
        while lines and not lines[0].strip():lines.pop(0)
        headers={"Old English",running,"Old English "+running,running+" Old English"}
        for _ in range(2):
            if lines and norm(lines[0]) in headers:lines.pop(0)
        while lines and not lines[-1].strip():lines.pop()
        if lines and re.fullmatch(r"\s*\d+\s*",lines[-1]):lines.pop()
        pages.append("\n".join(lines))
    return "\n".join(pages)

def inspect(kind,master,stem,use_build,expected_ids):
    mpath=ROOT/master
    raw=mpath.read_text(encoding="utf-8-sig").replace("\r\n","\n")
    tpath=ROOT/f"typesetting/pronunciation/{stem}.tex"
    tex=tpath.read_text(encoding="utf-8-sig").replace("\r\n","\n")
    ppath=tpath.parent/("build" if use_build else "")/f"{stem}.pdf"
    errors=[]
    def check(ok,message):
        if not ok:errors.append(message)
    ts=tables.parse_md(raw)
    doc={"tables":[dict(t,original_index_zero_based=i,revised=t["raw"]) for i,t in enumerate(ts)]}
    title,events,comments=master_events(raw,doc)
    prose=[e["text"] for e in events if e["kind"]=="prose"]
    groups=re.findall(r"(?ms)^% mdparagraph:(P\d+):begin\n(.*?)^% mdparagraph:\1:end",tex)
    check(len(groups)==len(prose),"Prose block count")
    for i,(actual,wanted) in enumerate(zip(groups,prose),1):
        check(texplain(actual[1])==wanted,{"type":"tex_prose","paragraph":i,"expected":wanted,"actual":texplain(actual[1])})
    check(all("% "+c in tex for c in comments),"Missing editorial comments in TeX")
    label="item" if kind=="learner" else "answer"
    ids=re.findall(r"<!--\s*"+label+r":\s*(PRON-P\d+[a-z])\s*-->",raw)
    check(ids==expected_ids,{"type":"response_id_order","expected":expected_ids,"actual":ids})
    if kind=="learner":
        for symbol in ["x","ç","ɣ"]:check(raw.count("["+symbol+"]")<=1,"Repeated introductory IPA "+symbol)
    tm=re.search(r"\\booktitle(\{.*)",tex)
    first,pos=group(tm[1],0)
    second,pos=group(tm[1],pos)
    prefix="GUIDE" if kind=="learner" else "SEPARATE KEY"
    check(texplain(first)==prefix and texplain(second)==title,"Title parity")
    tgroups=list(re.finditer(r"(?ms)^% mdtable:(T\d+):begin\n(.*?)^% mdtable:\1:end",tex))
    check(len(tgroups)==len(ts),"Table count")
    actual_tables=[]
    for i,(tg,t) in enumerate(zip(tgroups,ts),1):
        decoded=tables.decode_tex(tg[2])
        expected=[[mdplain(c) for c in row] for row in [t["headers"],*t["rows"]]]
        check(decoded==[expected],{"type":"tex_table","table":i})
        actual_tables.append(expected)
    errors.extend(tables.ERRORS);tables.ERRORS.clear()
    visible=[{"kind":"title","text":prefix+" "+title}]
    for event in events:
        if event["kind"]=="prose":visible.append(event)
        else:
            for row in actual_tables[event["number"]-1]:
                visible.append({"kind":"table_row","table":event["number"],"text":" ".join(row)})
    rawpdf=subprocess.run([str(PDFTOTEXT),"-enc","UTF-8","-raw",str(ppath),"-"],capture_output=True,check=True).stdout.decode("utf-8")
    running="Pronunciation" if kind=="learner" else "Pronunciation key"
    pdf=chars(pdf_body(rawpdf,running))
    projected=quote_projection(pdf)
    cursor=0
    missing=[]
    projections=[]
    for i,event in enumerate(visible,1):
        wanted=chars(event["text"])
        at=pdf.find(wanted,cursor)
        if at<0:
            at=projected.find(quote_projection(wanted),cursor)
            if at>=0:projections.append(i)
        if at<0:missing.append({"event":i,**event})
        else:cursor=at+len(wanted)
    suspicious=Counter(c for c in rawpdf if c=="\ufffd" or unicodedata.category(c) in ["Co","Cn"] or (unicodedata.category(c)=="Cc" and not c.isspace()))
    check(not suspicious,{"type":"suspicious_pdf_characters","characters":dict(suspicious)})
    logpath=tpath.parent/"build"/f"{stem}.log"
    log=logpath.read_text(encoding="utf-8",errors="replace")
    warnings=diagnostics(log)
    check(not warnings,{"type":"compile_diagnostics","findings":warnings})
    return {"kind":kind,"master":master,"master_sha256":digest(mpath),"tex":tpath.relative_to(ROOT).as_posix(),
            "tex_sha256":digest(tpath),"pdf":ppath.relative_to(ROOT).as_posix(),"pdf_sha256":digest(ppath),
            "pages":rawpdf.count("\f"),"response_ids":ids,"prose_blocks":len(prose),
            "tables":len(ts),"table_cells":sum(len(row) for t in actual_tables for row in t),
            "pdf_events":len(visible),"missing_pdf_events":missing,"quote_projections":projections,
            "errors":errors,"log":logpath.relative_to(ROOT).as_posix(),"log_sha256":digest(logpath)}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--build",action="store_true",help="Check newly built PDFs instead of retained PDFs.")
    ap.add_argument("--report",type=Path,default=Path("build/pronunciation-export-check.json"))
    args=ap.parse_args()
    c=json.loads((ROOT/"guides/pronunciation/coverage.json").read_text(encoding="utf-8"))
    expected=[item["id"] for g in c["practice"] for item in g["items"]]
    assert len(expected)==len(set(expected))==c["expected_numbered_responses"]
    reports=[inspect("learner","guides/pronunciation/student.md","pronunciation",args.build,expected),
             inspect("key","guides/pronunciation/answer-key.md","answer-key",args.build,expected)]
    boundary=json.loads((ROOT/c["boundaries"]["identity_manifest"]).read_text(encoding="utf-8"))
    changed=[row["path"] for row in boundary["files"] if digest(ROOT/row["path"])!=row["sha256"]]
    passed=not changed and all(not d["errors"] and not d["missing_pdf_events"] for d in reports)
    report={"status":"pass" if passed else "fail","method":"Independent Markdown inventory and TeX decoder reused from course checks; complete ordered raw-PDF prose/table-row coverage; response IDs, Unicode and compile diagnostics; raw identities of all protected earlier course files.",
            "documents":reports,"protected_file_count":len(boundary["files"]),"changed_protected_files":changed,
            "limitations":"Text/glyph and identity checks do not certify pronunciation accuracy or visual page quality; independent review and actual page inspection remain required."}
    output=args.report if args.report.is_absolute() else ROOT/args.report
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps({"status":report["status"],"documents":len(reports),"errors":sum(len(d["errors"]) for d in reports),"missing_pdf_events":sum(len(d["missing_pdf_events"]) for d in reports),"changed_protected_files":changed},indent=2))
    return 0 if passed else 1

if __name__=="__main__":
    raise SystemExit(main())
