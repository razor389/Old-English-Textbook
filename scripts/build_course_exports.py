"""Compile and rasterize the complete course after a declared table revision.

Build products remain under each unit's build directory.  This command never
replaces retained PDFs, edits a master/TeX file, or asserts visual acceptance.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

from render_course_tables import verify_revised_tables


ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "docs/revisions/table-layout/baseline.json"
MAPPING = ROOT / "docs/revisions/table-layout/tables.json"
REPORT = ROOT / "build/style-audit/build-report.json"
COMPARISON_REPORT = ROOT / "build/style-audit/page-comparison.json"
PDFTOTEXT = Path("C:/Program Files/Git/mingw64/bin/pdftotext.exe")
GSROOT = Path("C:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs")
GS = GSROOT / "bin/gswin64c.exe"
LUALATEX = Path("C:/Users/Ross/AppData/Local/texlive/2026/bin/windows/lualatex.exe")
DIAGNOSTIC_PATTERNS = [
    "Missing character:", "Overfull \\hbox", "Overfull \\vbox",
    "Underfull \\hbox", "Underfull \\vbox", "Font shape",
    "LaTeX Font Warning", "Package fontspec Warning", "Rerun to get",
    "Table widths have changed",
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest(path: Path, normalized_lf: bool = False) -> str:
    data = path.read_bytes()
    if normalized_lf:
        data = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def command(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    options = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", **options)


def diagnostics(log: str) -> list[dict[str, Any]]:
    lines = log.splitlines()
    findings = []
    for index, line in enumerate(lines):
        if any(pattern in line for pattern in DIAGNOSTIC_PATTERNS):
            findings.append({"log_line": index + 1, "message": line,
                             "context": lines[max(0, index-1):index+5]})
    return findings


def document_records(include_unchanged: bool, selection: set[str]) -> list[dict[str, Any]]:
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    mapping = json.loads(MAPPING.read_text(encoding="utf-8"))
    by_document = {(d["chapter"], d["document_kind"]): d for d in mapping["documents"]}
    records = []
    for chapter in range(1, 19):
        for kind, stem, mapping_kind in [("learner", f"chapter-{chapter:02}", "student"),
                                         ("key", "answer-key", "answer-key")]:
            label = f"ch{chapter:02}/{kind}"
            if selection and label not in selection:
                continue
            path = ROOT / f"typesetting/ch{chapter:02}/{stem}.tex"
            before = baseline["files"][relative(path)]
            changed = digest(path, True) not in before.values()
            if not changed and not include_unchanged and not selection:
                continue
            records.append({"id": label, "chapter": chapter, "kind": kind, "stem": stem,
                            "tex_path": relative(path), "changed_since_baseline": changed,
                            "baseline_tex_sha256": before["sha256"],
                            "table_records": by_document[(chapter, mapping_kind)]["tables"]})
    if selection != {d["id"] for d in records} and selection:
        raise ValueError("Invalid document selection: " + ", ".join(sorted(selection - {d["id"] for d in records})))
    return records


def compile_document(document: dict[str, Any]) -> dict[str, Any]:
    path = ROOT / document["tex_path"]
    folder, stem = path.parent, document["stem"]
    build = folder / "build"
    build.mkdir(exist_ok=True)
    report = {k: v for k, v in document.items() if k != "table_records"}
    report.update({"status": "in_progress", "started_utc": stamp(),
                   "tex_sha256": digest(path), "tex_sha256_normalized_lf": digest(path, True),
                   "mapping_sha256": digest(MAPPING), "passes": []})
    report["table_parity"] = verify_revised_tables(path.read_bytes().decode("utf-8"), document["table_records"])
    for run in (1, 2):
        result = command([str(LUALATEX), "-interaction=nonstopmode", "-halt-on-error",
                          "-output-directory=build", path.name], folder)
        stdout = build / f"{stem}-table-layout-pass{run}.stdout.txt"
        stdout.write_text(result.stdout + "\n" + result.stderr, encoding="utf-8", newline="\n")
        report["passes"].append({"pass": run, "exit_code": result.returncode, "output": relative(stdout)})
        if result.returncode:
            report.update({"status": "compile_failed", "failure_tail": (result.stdout + "\n" + result.stderr).splitlines()[-30:],
                           "finished_utc": stamp()})
            return report
    report.update(inspect_build(document))
    report["finished_utc"] = stamp()
    return report


def inspect_build(document: dict[str, Any]) -> dict[str, Any]:
    path = ROOT / document["tex_path"]
    folder, stem = path.parent, document["stem"]
    build = folder / "build"
    pdf, logpath, txt = (build / (stem + suffix) for suffix in (".pdf", ".log", ".txt"))
    log = logpath.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"Output written on .*?\((\d+) pages?", log, re.S)
    if not match or not pdf.exists():
        raise ValueError("Build PDF/page count is missing for " + document["id"])
    warnings = diagnostics(log)
    extraction = command([str(PDFTOTEXT), "-enc", "UTF-8", "-layout", str(pdf), str(txt)], folder)
    if extraction.returncode:
        raise RuntimeError(extraction.stderr)
    report = {"status": "diagnostics_pending" if warnings else "compiled_clean",
              "tex_sha256": digest(path), "tex_sha256_normalized_lf": digest(path, True),
              "pdf_path": relative(pdf), "pdf_sha256": digest(pdf), "pages": int(match[1]),
              "log_path": relative(logpath), "log_sha256": digest(logpath), "diagnostics": warnings,
              "text_path": relative(txt), "text_sha256": digest(txt), "text_extraction_exit_code": extraction.returncode,
              "table_parity": verify_revised_tables(path.read_bytes().decode("utf-8"), document["table_records"]),
              "visual_review": "not_performed_by_build_helper"}
    retained = folder / (stem + ".pdf")
    report["retained_pdf_path"] = relative(retained)
    report["retained_pdf_sha256_untouched"] = digest(retained)
    return report


def render_document(document: dict[str, Any], compiled: dict[str, Any], suffix: str,
                    base_directory: str = "build/table-layout-pages") -> dict[str, Any]:
    if compiled["diagnostics"]:
        raise ValueError("Resolve compiler diagnostics before rendering " + document["id"])
    folder_name = document["kind"] + ("-" + suffix if suffix else "")
    target = ROOT / base_directory / f"ch{document['chapter']:02}" / folder_name
    witness = target / "render-manifest.json"
    if target.exists():
        if not witness.exists():
            raise ValueError("Existing render folder has no identity manifest: " + relative(target))
        previous = json.loads(witness.read_text(encoding="utf-8"))
        if previous["pdf_sha256"] != compiled["pdf_sha256"]:
            raise ValueError("PDF changed; use --render-suffix for a fresh image witness: " + relative(target))
        if not all((ROOT / row["path"]).exists() and digest(ROOT / row["path"]) == row["sha256"] for row in previous["images"]):
            raise ValueError("Existing render image identity changed")
        return previous
    target.mkdir(parents=True)
    pdf = ROOT / compiled["pdf_path"]
    args = [str(GS), "-I" + ";".join(str(GSROOT / part) for part in ["Resource/Init", "lib", "kanji"]),
            "-sDEVICE=png16m", "-r150", "-dTextAlphaBits=4", "-dGraphicsAlphaBits=4",
            "-dBATCH", "-dNOPAUSE", "-sOutputFile=" + str(target / "page-%03d.png"), str(pdf)]
    result = command(args, ROOT)
    (target / "render.stdout.txt").write_text(result.stdout + "\n" + result.stderr, encoding="utf-8", newline="\n")
    if result.returncode:
        raise RuntimeError("Ghostscript failed: " + result.stderr[-2000:])
    paths = sorted(target.glob("page-*.png"))
    if len(paths) != compiled["pages"]:
        raise ValueError("Rendered image count differs from compiled page count")
    manifest = {"document": document["id"], "status": "rendered_only_not_visually_reviewed",
                "pdf_path": compiled["pdf_path"], "pdf_sha256": compiled["pdf_sha256"],
                "pages": compiled["pages"], "dpi": 150, "rendered_utc": stamp(),
                "images": [{"page": i, "path": relative(path), "sha256": digest(path)} for i, path in enumerate(paths, 1)]}
    witness.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return manifest


def compare_document_pages(document: dict[str, Any], compiled: dict[str, Any]) -> dict[str, Any]:
    """Compare exact image bytes across all old pages of the same document."""
    original = ROOT / f"typesetting/ch{document['chapter']:02}/{document['stem']}.pdf"
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    original_hash = digest(original)
    if original_hash != baseline["files"][relative(original)]["sha256"]:
        raise ValueError("Retained original PDF no longer matches the baseline")
    current_pdf = ROOT / compiled["pdf_path"]
    if digest(current_pdf) != compiled["pdf_sha256"]:
        raise ValueError("Revised PDF changed after its recorded render")
    result = command([str(PDFTOTEXT), "-enc", "UTF-8", "-layout", str(original), "-"], ROOT)
    if result.returncode:
        raise RuntimeError(result.stderr)
    page_count = result.stdout.count("\f") + bool(result.stdout.split("\f")[-1].strip())
    if not page_count:
        raise ValueError("Original PDF has no extracted pages")
    original_record = {"pdf_path": relative(original), "pdf_sha256": original_hash,
                       "pages": page_count, "diagnostics": []}
    old_render = render_document(document, original_record, "", "build/table-layout-original-pages")
    new_render = compiled["render"]
    old_by_hash: dict[str, list[dict[str, Any]]] = {}
    for row in old_render["images"]:
        if digest(ROOT / row["path"]) != row["sha256"]:
            raise ValueError("Original rendered image changed")
        old_by_hash.setdefault(row["sha256"], []).append(row)
    pages, unmatched, matched, shifted = [], [], 0, 0
    for row in new_render["images"]:
        if digest(ROOT / row["path"]) != row["sha256"]:
            raise ValueError("Revised rendered image changed")
        old = old_by_hash.get(row["sha256"], [])
        entry = {"new_page": row["page"], "new_image": row["path"], "new_image_sha256": row["sha256"],
                 "status": "byte_identical_candidate" if old else "unmatched_requires_visual_inspection",
                 "old_matches": [{"old_page": candidate["page"], "old_image": candidate["path"],
                                  "old_image_sha256": candidate["sha256"]} for candidate in old],
                 "review_acceptance_inferred": False}
        pages.append(entry)
        if old:
            matched += 1
            shifted += not any(candidate["page"] == row["page"] for candidate in old)
        else:
            unmatched.append({"page": row["page"], "path": row["path"], "sha256": row["sha256"]})
    if digest(original) != original_hash:
        raise ValueError("Original retained PDF changed during comparison")
    return {"document": document["id"], "method": "Actual original and revised PDFs rasterized with identical Ghostscript flags; exact SHA-256 match against every original page in this document, including other page numbers. No crop, masking, perceptual comparison or inferred review acceptance.",
            "original_pdf": relative(original), "original_pdf_sha256": original_hash,
            "revised_pdf": compiled["pdf_path"], "revised_pdf_sha256": compiled["pdf_sha256"],
            "dpi": 150, "original_page_count": page_count, "new_page_count": compiled["pages"],
            "byte_identical_candidates": matched, "matched_only_at_different_old_page_number": shifted,
            "unmatched_page_count": len(unmatched), "pages": pages, "unmatched_pages": unmatched}


def compare_pages(documents: list[dict[str, Any]], jobs: int) -> None:
    build = json.loads(REPORT.read_text(encoding="utf-8"))
    report = {"status": "identity_comparison_only_not_review_acceptance", "started_utc": stamp(),
              "baseline_checkpoint": "1c9e53a", "render_settings": "Ghostscript png16m,150dpi,TextAlphaBits4,GraphicsAlphaBits4; identical GS executable/resource paths for original and revised PDF",
              "documents": {}, "errors": {}}
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        futures = {pool.submit(compare_document_pages, document, build["documents"][document["id"]]): document for document in documents}
        for future in as_completed(futures):
            document = futures[future]
            try:
                result = future.result()
                report["documents"][document["id"]] = result
                print(document["id"], result["byte_identical_candidates"], "identical;", result["unmatched_page_count"], "unmatched", flush=True)
            except Exception as error:
                report["errors"][document["id"]] = str(error)
                print(document["id"], "comparison failed:", error, flush=True)
            COMPARISON_REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    report["finished_utc"] = stamp()
    report["totals"] = {key: sum(d[key] for d in report["documents"].values()) for key in ["original_page_count", "new_page_count", "byte_identical_candidates", "matched_only_at_different_old_page_number", "unmatched_page_count"]}
    COMPARISON_REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(report["totals"], flush=True)
    if report["errors"]:
        raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=["list", "compile", "inspect", "render", "compare", "all"], default="compile")
    parser.add_argument("--select", default="", help="Comma-separated IDs such as ch01/learner,ch03/key")
    parser.add_argument("--include-unchanged", action="store_true")
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--render-suffix", default="", help="Fresh version suffix after an already-rendered PDF changes")
    args = parser.parse_args()
    if not 1 <= args.jobs <= 4 or not re.fullmatch(r"[a-zA-Z0-9_-]*", args.render_suffix):
        parser.error("Use 1–4 jobs and a simple render suffix")
    selection = set(filter(None, args.select.split(",")))
    documents = document_records(args.include_unchanged, selection)
    if args.stage == "list":
        for document in documents:
            print(document["id"], "changed" if document["changed_since_baseline"] else "unchanged")
        print(len(documents), "selected documents")
        return
    if args.stage == "compare":
        compare_pages(documents, args.jobs)
        return
    report = json.loads(REPORT.read_text(encoding="utf-8")) if REPORT.exists() else {
        "revision_id": "course-table-layout-2026-10", "baseline_checkpoint": "1c9e53a",
        "scope": "Complete-document compilation, actual table parity and raster generation; no visual acceptance or retained-PDF replacement.",
        "documents": {}, "adjustments": [], "runs": []}
    report["mapping_sha256"] = digest(MAPPING)
    run = {"started_utc": stamp(), "stage": args.stage, "selection": [d["id"] for d in documents]}
    report["runs"].append(run)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    def process(document: dict[str, Any]) -> dict[str, Any]:
        if args.stage in {"compile", "all"}:
            item = compile_document(document)
        else:
            item = dict(report["documents"].get(document["id"], {}))
            item.update({k: v for k, v in document.items() if k != "table_records"})
            item.update(inspect_build(document))
        if args.stage in {"render", "all"} and item["status"] == "compiled_clean":
            item["render"] = render_document(document, item, args.render_suffix)
        return item

    failed = False
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        future_map = {pool.submit(process, document): document for document in documents}
        for future in as_completed(future_map):
            document = future_map[future]
            try:
                item = future.result()
            except Exception as error:
                item = {"id": document["id"], "status": "helper_failed", "error": str(error)}
            old = report["documents"].get(document["id"])
            if old and old.get("pdf_sha256") != item.get("pdf_sha256"):
                item["previous_builds"] = old.get("previous_builds", []) + [{k: old[k] for k in ["pdf_sha256", "pages", "tex_sha256", "diagnostics"] if k in old}]
            elif old and "previous_builds" in old:
                item["previous_builds"] = old["previous_builds"]
            report["documents"][document["id"]] = item
            failed |= item["status"] != "compiled_clean"
            print(document["id"], item["status"], item.get("pages", "?"), "pages;",
                  len(item.get("diagnostics", [])), "diagnostics", flush=True)
            if "error" in item:
                print(item["error"], flush=True)
            for finding in item.get("diagnostics", []):
                print("  " + finding["message"], flush=True)
            if item.get("failure_tail"):
                print("\n".join(item["failure_tail"][-8:]), flush=True)
            REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    run["finished_utc"] = stamp()
    report["status"] = "diagnostics_or_failures_pending" if any(d["status"] != "compiled_clean" for d in report["documents"].values()) else "compiled_clean_pending_page_review"
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(relative(REPORT), flush=True)
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
