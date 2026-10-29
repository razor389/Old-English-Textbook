"""Check glossary coverage, preserved inputs and complete Markdown/TeX/PDF text.

This does not certify definitions or page appearance: retain independent linguistic
reviews and inspect every rendered page after changing an export.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import unicodedata

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))


def normalized(text):
    # Cambria's visible hyphen glyph extracts as U+00AD in this LuaHBTeX/Xpdf
    # combination. Preserve it as a hyphen, never delete it or fold OE letters.
    return re.sub(r"\s+", "", unicodedata.normalize("NFC", text).replace("\u00ad", "-"))


def md_plain(text):
    return re.sub(r"\*\*([^*]+)\*\*|\*([^*]+)\*", lambda m: m[1] or m[2], text)


def tex_plain(text):
    text = re.sub(r"(?m)^\\needspace.*\n?", "", text).strip()
    if text.startswith(r"\booktitle{GLOSSARY}{"):
        text = text[len(r"\booktitle{GLOSSARY}{"):-1]
    elif re.match(r"\\(?:sub)?section\*\{", text):
        text = re.sub(r"^\\(?:sub)?section\*\{", "", text)[:-1]
    else:
        text = re.sub(r"\\par$", "", text)
    text = text.replace(r"\textbackslash{}", "BACKSLASHMARK")
    text = text.replace(r"\{", "LEFTBRACEMARK").replace(r"\}", "RIGHTBRACEMARK")
    for command in ["textbf", "emph"]:
        text = re.sub(r"\\" + command + r"\{([^{}]*)\}", r"\1", text)
    for character in "&%$#_":
        text = text.replace("\\" + character, character)
    text = text.replace(r"\textasciitilde{}", "~").replace(r"\textasciicircum{}", "^")
    return text.replace("BACKSLASHMARK", "\\").replace("LEFTBRACEMARK", "{").replace("RIGHTBRACEMARK", "}")


def master_blocks(raw):
    result = []
    for chunk in re.split(r"\n\s*\n", raw.strip()):
        if chunk.startswith("<!--"):
            continue
        result.append(md_plain(re.sub(r"^#{1,3} ", "", " ".join(chunk.splitlines()))))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--document", choices=["old-english", "english"])
    parser.add_argument("--report", default="build/glossary-export-check.json")
    args = parser.parse_args()
    errors = []
    def check(condition, message):
        if not condition:
            errors.append(message)
    data = read("glossaries/entries.json")
    oe = {e["entry_id"]: e for e in data["old_english_entries"]}
    en = {e["entry_id"]: e for e in data["english_entries"]}
    forms = read("glossaries/form-lookup.json")
    routes = {r["surface"]: r for r in forms["forms"]}
    inventory = read("sources/audits/glossaries/old-english/inventory.json")
    for surface, lemmas, *_ in inventory["surfaces"]:
        check(surface in routes, "Missing corpus surface: " + surface)
        if surface in routes:
            check(set("OE-" + lid for lid in lemmas) <= set(routes[surface]["entry_ids"]), "Lost lemma route: " + surface)
    check(len(routes) == len(inventory["surfaces"]), "Unexpected surface inventory change")
    for row in forms["forms"]:
        for eid in row["entry_ids"]:
            check(eid in oe, "Dangling form route: " + eid)
            if eid in oe:
                check(row["surface"] in [unicodedata.normalize("NFC", f).casefold() for f in oe[eid]["forms"]], "Unlisted actual form: " + eid + ": " + row["surface"])
    check(not set(routes).intersection(r["surface"].casefold() for r in forms["special_dispositions"]), "Rejected/corrected form in normal lookup")
    register = read("lexicon/entries.json")
    register_lemmas = {l["lemma_id"]: l for l in register["lemmas"]}
    all_register_forms = {f["form_id"]: f for l in register["lemmas"] for f in l["forms"]}
    approved = read("glossaries/approved-review-repairs.json")
    excluded_pp = {r["excluded_form_id"] for r in approved["old_english"]["base_participle_exclusions"]}
    dictionary = read("glossaries/dictionary-presentation.json")
    reference_forms = {f["form_id"]: f for e in dictionary["verb_entries"] for f in e["glossary_only_reference_forms"]}
    diagnostic_sources = {**all_register_forms, **reference_forms}
    for e in oe.values():
        if e["lemma_id"] not in register_lemmas:
            continue
        source_forms = {f["form_id"]: f["form"] for f in register_lemmas[e["lemma_id"]]["forms"]}
        source_records = {f["form_id"]: f for f in register_lemmas[e["lemma_id"]]["forms"]}
        for d in e["diagnostics"]:
            check(all(fid in source_forms and source_forms[fid] in d["forms"] for fid in d["form_ids"]), "Diagnostic provenance differs from displayed forms: " + e["entry_id"] + " / " + d["label"])
            if d["label"] == "past ptcp.":
                for fid in d["form_ids"]:
                    analysis = source_records[fid].get("analysis", {})
                    check(not isinstance(analysis, dict) or not any(analysis.get(k) for k in ["case", "gender", "number", "declension"]), "Inflected form in base participle diagnostic: " + e["entry_id"] + " / " + fid)
                    check(fid not in excluded_pp, "Excluded participle in diagnostic: " + fid)
    for e in oe.values():
        for d in e["printed_diagnostics"]:
            cited = {diagnostic_sources[fid]["form"] for fid in d["form_ids"] if fid in diagnostic_sources}
            check(set(d["forms"]) == cited, "Printed dictionary provenance differs: " + e["entry_id"] + " / " + d["label"])
            check(all(fid in diagnostic_sources for fid in d["form_ids"]), "Unknown printed diagnostic source: " + e["entry_id"])
            if d["label"] == "past ptcp.":
                check(not excluded_pp.intersection(d["form_ids"]), "Inflected principal part in print: " + e["entry_id"])
    for policy in dictionary["verb_entries"]:
        actual = oe[policy["entry_id"]]["printed_diagnostics"]
        for d in policy["printed_diagnostics"]:
            check(d in actual, "Reviewed principal part lost: " + policy["entry_id"] + " / " + d["label"])
        if policy["verb_type"] == "weak":
            check(not any(d["label"] == "pret. pl." for d in actual), "Routine weak plural printed: " + policy["entry_id"])
        check(not policy["missing_core_reference_cells"], "Unresolved dictionary principal part: " + policy["entry_id"])
    for r in approved["old_english"]["diagnostic_repairs"]:
        existing = [d for d in oe[r["entry_id"]]["diagnostics"] if d["label"] == r["label"]]
        check(bool(existing) and set(r["forms"]) <= set(existing[0]["forms"]), "Reviewed diagnostic lost: " + r["entry_id"] + " / " + r["label"])
    expected_senses = {s["sense_id"] for l in register["lemmas"] for s in l["senses"]}
    check(set("OE-" + l["lemma_id"] for l in register["lemmas"]) <= set(oe), "Missing registered headword")
    check(expected_senses <= {s["sense_id"] for e in oe.values() for s in e["senses"]}, "Missing registered OE sense")
    english_senses = {s for e in en.values() for r in e["routes"] for s in r["sense_ids"]}
    check(expected_senses <= english_senses, "Missing English sense access: " + str(sorted(expected_senses - english_senses)))
    for e in en.values():
        for r in e["routes"]:
            check(set(r["entry_ids"]) <= set(oe), "Dangling English target: " + e["entry_id"])
    for x in data["cross_references"]:
        check(set(x["entry_ids"]) <= set(oe), "Dangling cross-reference: " + x["headword"])
        check(x["surface"] in routes and set(x["entry_ids"]) <= set(routes.get(x["surface"], {}).get("entry_ids", [])), "Cross-reference lost exact route: " + x["headword"])
    check(data["cross_references"] == dictionary["cross_references"], "Selective cross-reference policy differs")
    tasks = read("glossaries/exercise-lookup.json")["tasks"]
    task_map = {t["task_id"]: t for t in tasks}
    originals = read("sources/audits/glossaries/english/exercise-inventory.json")["items"]
    check(set(task_map) == {t["task_id"] for t in originals}, "Exercise identity mismatch")
    for t in originals:
        actual = task_map[t["task_id"]]
        check(set(t.get("required_sense_ids", [])) <= set(actual["required_sense_ids"]), "Lost exercise sense: " + t["task_id"])
        covered = {s for eid in actual["english_entry_ids"] for r in en[eid]["routes"] for s in r["sense_ids"]}
        check(set(actual["required_sense_ids"]) <= covered, "Uncovered exercise: " + t["task_id"])
    boundary = read("glossaries/course-boundary.json")
    preserved = boundary.get("files", [])
    for row in preserved:
        raw = (ROOT / row["path"]).read_bytes()
        expected = row.get("sha256", row.get("raw_sha256"))
        check(hashlib.sha256(raw).hexdigest() == expected, "Protected course changed: " + row["path"])
    docs = []
    for stem in ["old-english", "english"]:
        if args.document and stem != args.document:
            continue
        master = ROOT / "glossaries" / (stem + ".md")
        tex = ROOT / "typesetting/glossaries" / (stem + ".tex")
        pdf = ROOT / "typesetting/glossaries" / ("build" if args.build else "") / (stem + ".pdf")
        raw = master.read_text(encoding="utf-8-sig")
        expected_ids = set(oe) | {x["entry_id"] for x in data["cross_references"] if x["disposition"] == "standalone"} if stem == "old-english" else set(en)
        ids = re.findall(r"<!-- entry: (.*?) -->", raw)
        check(set(ids) == expected_ids and len(ids) == len(expected_ids), stem + " entry identity mismatch")
        if stem == "old-english":
            check("Forms in this book:" not in raw, "Exhaustive inflection list printed in dictionary")
            paragraphs = dict(re.findall(r"<!-- entry: (.*?) -->\s*\n\n([^\n]+)", raw))
            for eid, e in oe.items():
                paragraph = normalized(md_plain(paragraphs.get(eid, "")))
                for sense in e["senses"]:
                    if sense["sense_id"] in e.get("printed_sense_overrides", {}):
                        text = e["printed_sense_overrides"][sense["sense_id"]]
                        check(normalized(text.rstrip(" .")) in paragraph, "Reviewed sense display missing: " + eid + " / " + sense["sense_id"])
                        continue
                    meaning = e.get("printed_gloss_overrides", {}).get(sense["meaning"], sense["meaning"])
                    check(normalized(meaning.rstrip(" .")) in paragraph, "Meaning missing from master: " + eid + " / " + sense["sense_id"])
                    if sense.get("usage"):
                        check(normalized(sense["usage"].rstrip(" .")) in paragraph, "Usage missing from master: " + eid + " / " + sense["sense_id"])
                for d in e["printed_diagnostics"]:
                    check(normalized(d["label"] + " " + ", ".join(d["forms"])) in paragraph, "Diagnostic missing from master: " + eid + " / " + d["label"])
            for x in data["cross_references"]:
                ids = x["preserve_lexical_entry_ids"] if x["disposition"] == "append_to_existing_headword" else [x["entry_id"]]
                for eid in ids:
                    paragraph = normalized(md_plain(paragraphs.get(eid, "")))
                    for target in x["targets"]:
                        expected = target["label"] + ": see " + oe[target["entry_id"]]["headword"]
                        check(normalized(expected) in paragraph, "Labelled cross-reference missing from print: " + x["headword"] + " / " + eid)
        blocks = master_blocks(raw)
        tex_blocks = re.findall(r"% glossary-block:(B\d+):begin\n(.*?)\n% glossary-block:\1:end", tex.read_text(encoding="utf-8"), re.S)
        check(len(blocks) == len(tex_blocks), stem + " block count mismatch")
        for i, (plain, (_, source)) in enumerate(zip(blocks, tex_blocks), 1):
            check(normalized(plain) == normalized(tex_plain(source)), f"{stem} Markdown/TeX block {i} differs")
        command = ["C:/Program Files/Git/mingw64/bin/pdftotext.exe", "-enc", "UTF-8", "-raw", str(pdf), "-"]
        extracted = subprocess.check_output(command).decode("utf-8")
        pages = extracted.count("\f")
        furniture = {"Old English", "Old English–English", "English–Old English", "Old English Old English–English", "Old English–English Old English", "Old English English–Old English", "English–Old English Old English"}
        filtered = "\n".join(line for line in extracted.splitlines() if " ".join(line.split()) not in furniture and not re.fullmatch(r"\s*\d+\s*", line))
        continuous = normalized(filtered)
        cursor = 0
        for i, plain in enumerate(blocks, 1):
            expected = normalized(plain)
            found = continuous.find(expected, cursor)
            check(found >= 0, f"{stem} PDF block {i} missing or out of order: {plain[:90]}")
            if found >= 0:
                cursor = found + len(expected)
        log = ROOT / "typesetting/glossaries/build" / (stem + ".log")
        if log.exists():
            diagnostics = log.read_text(encoding="utf-8", errors="replace")
            check(not re.search(r"Missing character:|Overfull \\[hv]box|^!", diagnostics, re.M), stem + " compiler diagnostic requires review")
        docs.append({"id": stem, "pages": pages, "blocks": len(blocks),
                     "master_sha256": hashlib.sha256(master.read_bytes()).hexdigest(),
                     "tex_sha256": hashlib.sha256(tex.read_bytes()).hexdigest(),
                     "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest()})
    result = {"status": "passed" if not errors else "failed", "documents": docs,
              "counts": {"oe_entries": len(oe), "english_entries": len(en), "surfaces": len(routes),
                         "cross_references": len(data["cross_references"]), "tasks": len(tasks), "register_senses": len(expected_senses),
                         "protected_files": len(preserved)}, "errors": errors,
              "limits": "Structural/text checks only; independent linguistic and every-page visual review are required."}
    target = ROOT / args.report
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": result["status"], "counts": result["counts"], "documents": docs,
                      "errors": errors[:12], "error_count": len(errors)}, ensure_ascii=False))
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
