"""Check complete appendix text, tables, example access and preserved earlier artifacts."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unicodedata

import check_course_layout as table_checks
from check_course_exports import master_events, texplain
from check_glossary_exports import normalized
from check_pronunciation_exports import pdf_body
from build_course_exports import diagnostics

ROOT = Path(__file__).resolve().parents[1]
STAR = "LITERALRECONSTRUCTIONSTAR"
PDFTOTEXT = Path("C:/Program Files/Git/mingw64/bin/pdftotext.exe")


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def mdplain(value):
    value = value.replace(r"\*", STAR)
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"\*\*([^*]+)\*\*|\*([^*]+)\*", lambda m: m[1] or m[2], value)
    return value.replace(STAR, "*")


def decode_table(value):
    match = re.search(r"\\begin\{longtable\}\{[^\n]*\}\n(.*?)\\end\{longtable\}", value, re.S)
    assert match, "No complete longtable"
    body = match[1]
    header = body.split(r"\toprule", 1)[1].split(r"\midrule", 1)[0].strip()
    data = body.split(r"\endlastfoot", 1)[1]
    rows = [header, *[row for row in re.split(r"(?<!\\)\\\\(?:\[[^\]]*\])?", data) if row.strip()]]
    return [[texplain(cell) for cell in re.split(r"(?<!\\)&", re.sub(r"\\\\\s*$", "", row.strip()))] for row in rows]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--report", default="build/sound-history/export-check.json")
    args = parser.parse_args()
    errors = []

    def check(ok, message):
        if not ok:
            errors.append(message)

    master_path = "appendices/sound-history/student.md"
    tex_path = "typesetting/sound-history/sound-history.tex"
    pdf_path = "typesetting/sound-history/" + ("build/" if args.build else "") + "sound-history.pdf"
    raw = (ROOT / master_path).read_text(encoding="utf-8-sig")
    tex = (ROOT / tex_path).read_text(encoding="utf-8-sig")
    contract = read("appendices/sound-history/coverage.json")
    examples = read(contract["examples"])
    access = read(contract["glossary_access"]["ledger"])
    check(access["master_sha256"] == sha(master_path), "Example inventory refers to a different master")
    bold = [m.group(1).replace(r"\*", "*") for m in re.finditer(r"\*\*(.+?)\*\*", raw)]
    items = {item["text"]: item for item in access["items"]}
    check(len(items) == len(access["items"]), "Duplicate inventory text")
    check(set(bold) == set(items), {"bold_inventory_missing": sorted(set(bold)-set(items)), "unused_inventory": sorted(set(items)-set(bold))})
    oe = {e["entry_id"]: e for e in read("glossaries/entries.json")["old_english_entries"]}
    allowed = {(f["surface"], f["entry_id"]) for g in examples["groups"] for f in g["forms"]}
    other = {r["surface"] for r in examples["non_old_english_examples"]}
    for item in items.values():
        if item["category"] == "old_english":
            check(item["text"].casefold() == item["contract_surface"].casefold(), "Undeclared spelling change: " + item["text"])
            check((item["contract_surface"], item["entry_id"]) in allowed, "Uncontracted OE example: " + item["text"])
            entry = oe.get(item["entry_id"], {})
            check(item["sense_id"] in {s["sense_id"] for s in entry.get("senses", [])}, "Unresolved sense: " + item["text"])
            check(bool(item.get("evidence_refs")), "No example evidence: " + item["text"])
        elif item["category"] in ["reconstruction", "other_language"]:
            check(item["text"] in other, "Uncontracted historical comparison: " + item["text"])
        else:
            check(item["category"] in ["letter", "ending", "sound_correspondence", "environment", "notation", "english_label"], "Unknown inventory category: " + item["text"])
    used_forms = {i["contract_surface"] for i in items.values() if i["category"] == "old_english"}
    check(used_forms == {f for f, entry in allowed}, "Contracted example form omitted")
    check(contract["scope"]["new_assessed_tasks"] == 0, "Unexpected task-scope change")
    check(not re.search(r"<!--\s*(?:item|answer):", raw), "Unexpected assessed task IDs")

    # Independently inventory all Markdown prose and tables using the course
    # checker, preserving escaped reconstruction stars before emphasis removal.
    protected_raw = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", raw.replace(r"\*", STAR))
    tables = table_checks.parse_md(protected_raw)
    document = {"tables": [dict(t, original_index_zero_based=i, revised=t["raw"]) for i, t in enumerate(tables)]}
    title, events, comments = master_events(protected_raw, document)
    title = title.replace(STAR, "*")
    for event in events:
        if "text" in event:
            event["text"] = event["text"].replace(STAR, "*")
    actual = re.findall(r"(?ms)^% appendix-block:(B\d+):(\w+):begin\n(.*?)^% appendix-block:\1:end", tex)
    check(len(actual) == len(events)+1, "Complete block count differs")
    check(bool(actual) and texplain(actual[0][2]) == "APPENDIX " + title, "Title differs")
    visible = ["APPENDIX " + title]
    cells = 0
    for number, (block, event) in enumerate(zip(actual[1:], events), 1):
        if event["kind"] == "table":
            source = tables[event["number"]-1]
            expected = [[mdplain(cell).replace(STAR, "*") for cell in row] for row in [source["headers"], *source["rows"]]]
            decoded = decode_table(block[2])
            check([[normalized(c) for c in row] for row in decoded] == [[normalized(c) for c in row] for row in expected], f"Table {event['number']} cell parity")
            visible.extend(" ".join(row) for row in expected)
            cells += sum(len(row) for row in expected)
        else:
            check(normalized(texplain(block[2])) == normalized(event["text"]), f"Prose block {number} parity")
            visible.append(event["text"])
    check(all("% " + comment in tex for comment in comments), "Missing editorial IDs/comments in TeX")
    raw_pdf = subprocess.run([str(PDFTOTEXT), "-enc", "UTF-8", "-raw", str(ROOT/pdf_path), "-"], capture_output=True, check=True).stdout.decode("utf-8")
    pdf = normalized(pdf_body(raw_pdf, "Sound history"))
    cursor = 0
    missing = []
    for number, text in enumerate(visible, 1):
        wanted = normalized(text)
        at = pdf.find(wanted, cursor)
        if at < 0:
            missing.append({"event": number, "text": text})
        else:
            cursor = at + len(wanted)
    check(not missing, {"missing_pdf_events": missing})
    suspicious = Counter(c for c in raw_pdf if c == "\ufffd" or unicodedata.category(c) in ["Co", "Cn"] or (unicodedata.category(c) == "Cc" and not c.isspace()))
    check(not suspicious, {"suspicious_pdf_characters": dict(suspicious)})
    log_path = "typesetting/sound-history/build/sound-history.log"
    findings = diagnostics((ROOT/log_path).read_text(encoding="utf-8", errors="replace"))
    check(not findings, {"compiler_diagnostics": findings})
    boundary = read(contract["preservation"]["identity_manifest"])
    changed = [row["path"] for row in boundary["files"] if sha(row["path"]) != row["sha256"]]
    check(not changed, {"changed_protected_files": changed})
    report = {"schema_version": 1, "status": "passed" if not errors else "failed",
        "master": master_path, "master_sha256": sha(master_path), "tex": tex_path, "tex_sha256": sha(tex_path),
        "pdf": pdf_path, "pdf_sha256": sha(pdf_path), "pages": raw_pdf.count("\f"),
        "prose_blocks": sum(e["kind"] == "prose" for e in events), "tables": len(tables), "table_cells": cells,
        "pdf_events": len(visible), "bold_spans": len(bold), "distinct_inventoried_spans": len(items),
        "oe_forms": len(used_forms),
        "oe_display_spellings": sum(i["category"] == "old_english" for i in items.values()),
        "new_assessed_tasks": 0, "protected_files": len(boundary["files"]), "changed_protected_files": changed,
        "log": log_path, "log_sha256": sha(log_path), "errors": errors,
        "limits": "Text, coverage and identity checks do not establish historical truth or visual quality. Independent linguistic review and actual every-page inspection remain required."}
    output = ROOT / args.report
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: report[k] for k in ["status", "pages", "prose_blocks", "tables", "table_cells", "oe_forms", "protected_files", "errors"]}, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
