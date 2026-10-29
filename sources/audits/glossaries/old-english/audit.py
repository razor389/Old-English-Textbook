"""Audit glossary coverage against the complete published Markdown corpus.

Run from the repository root. Outputs intended for manual inspection go in
build/glossary-oe; compact, reviewable coverage data stay beside this script.
No spelling normalization beyond NFC and case folding is used for a match.
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OWN = Path(__file__).resolve().parent
OUT = ROOT / "build/glossary-oe"
WORD = re.compile(r"[^\W\d_]+(?:[-‐‑][^\W\d_]+)*", re.UNICODE)
OE_MARKS = set("æþðāǣēīōūȳęǫǣœ")


def key(text):
    return unicodedata.normalize("NFC", text).casefold()


def clean_line(line):
    line = re.sub(r"<!--.*?-->", "", line)
    line = re.sub(r"<[^>]+>", "", line)
    line = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", line)
    line = re.sub(r"https?://\S+", "", line)
    return line


def serial(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    register = json.loads((ROOT / "lexicon/entries.json").read_text(encoding="utf-8"))
    mapping = defaultdict(dict)
    phrases = defaultdict(set)
    lemmas = {}

    def add(surface, lemma_id, route, evidence=None):
        if not isinstance(surface, str):
            return
        surface = surface.strip().strip("* ")
        optional = re.search(r"\(([A-Za-zæþðāǣēīōūȳęǫ]+)\)", surface)
        if optional and " " not in surface:
            add(surface[:optional.start()] + surface[optional.end():], lemma_id, route + ":optional_omitted", evidence)
            add(surface[:optional.start()] + optional[1] + surface[optional.end():], lemma_id, route + ":optional_included", evidence)
            return
        # Alternative spellings separated by comma or slash retain their own
        # exact spellings. Parenthesized explanatory prose is not a form.
        for part in re.split(r"\s*[,;/]\s*", surface):
            if WORD.fullmatch(part):
                record = mapping[key(part)].setdefault(lemma_id, {"lemma_id": lemma_id, "routes": [], "evidence_refs": []})
                if route not in record["routes"]:
                    record["routes"].append(route)
                record["evidence_refs"] = sorted(set(record["evidence_refs"]) | set(evidence or []))
            elif part and len(WORD.findall(part)) > 1:
                phrases[key(part)].add(lemma_id)

    for lemma in register["lemmas"]:
        lid = lemma["lemma_id"]
        lemmas[lid] = {
            "headword": lemma.get("display_headword", lid),
            "part_of_speech": lemma.get("part_of_speech"),
            "gender": lemma.get("gender"),
            "senses": [{"sense_id": s["sense_id"], "gloss": s.get("gloss", ""), "evidence_refs": s.get("evidence_refs", [])} for s in lemma.get("senses", [])],
        }
        add(lemma.get("display_headword", ""), lid, "headword", lemma.get("evidence_refs"))
        for spelling in lemma.get("source_spellings", []):
            add(spelling, lid, "source_spelling", lemma.get("evidence_refs"))
        for form in lemma.get("forms", []):
            add(form.get("form", ""), lid, "form:" + form["form_id"], form.get("evidence_refs"))
        # The cumulative register deliberately keeps source alternatives outside
        # its teaching-milestone forms. They still belong in a lookup glossary.
        def variants(value, route, inherited_refs=None):
            if isinstance(value, str):
                add(value, lid, route, inherited_refs)
            elif isinstance(value, list):
                for member in value:
                    variants(member, route, inherited_refs)
            elif isinstance(value, dict):
                refs = value.get("evidence_refs", inherited_refs)
                for field in ("form", "forms", "variant", "variants", "accepted_variants", "alternatives"):
                    if field in value:
                        variants(value[field], route, refs)
        for field in ("variants", "accepted_variants", "valid_alternatives", "principal_parts"):
            variants(lemma.get(field), field, lemma.get("evidence_refs"))
        for form in lemma.get("forms", []):
            for field in ("variants", "accepted_variants"):
                variants(form.get(field), "form_" + field, form.get("evidence_refs"))

    guide = json.loads((ROOT / "guides/pronunciation/examples.json").read_text(encoding="utf-8"))
    guide_map = {key(e["form"]): e for e in guide["examples"]}
    register_surface_count = len(mapping)
    amendments_path = OWN / "resolutions.json"
    amendments = json.loads(amendments_path.read_text(encoding="utf-8")) if amendments_path.exists() else {"resolutions": []}
    resolved = {key(r["surface"]): r for r in amendments["resolutions"]}
    review_path = OWN / "reviewed-exclusions.json"
    reviewed_exclusions = json.loads(review_path.read_text(encoding="utf-8")) if review_path.exists() else {}
    nonlexical = {token: group for group, values in reviewed_exclusions.get("groups", {}).items() for token in values}
    for surface, record in resolved.items():
        if record["classification"] == "old_english":
            for lid in record.get("lemma_ids", []):
                add(surface, lid, "audit_resolution", record.get("evidence_refs"))

    paths = [ROOT / "guides/pronunciation/student.md", ROOT / "guides/pronunciation/answer-key.md"]
    paths += [ROOT / f"chapters/ch{n:02}/{name}.md" for n in range(1, 19) for name in ("student", "answer-key")]
    all_words = defaultdict(list)
    suspect = defaultdict(list)
    known = defaultdict(list)
    excluded = defaultdict(list)
    manifest = []
    for path in paths:
        raw = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()
        manifest.append({"path": rel, "sha256_lf": hashlib.sha256(raw.encode()).hexdigest(), "lines": len(raw.splitlines())})
        item = section = None
        for line_number, raw_line in enumerate(raw.splitlines(), 1):
            m = re.search(r"<!-- item: (.*?) -->", raw_line)
            if m:
                item = m[1]
            if raw_line.startswith("#"):
                section = raw_line.lstrip("# ")
                item = None
            line = clean_line(raw_line)
            if not line.strip():
                continue
            emphasized = [(m.start(), m.end()) for m in re.finditer(r"\*\*[^*]+\*\*|(?<!\*)\*[^*]+\*(?!\*)|`[^`]+`", line)]
            table = line.lstrip().startswith("|")
            for match in WORD.finditer(line):
                token = match[0]
                k = key(token)
                loc = {"path": rel, "line": line_number, "surface": token}
                if item:
                    loc["item"] = item
                loc["context"] = line.strip()
                is_emph = any(a <= match.start() < b for a, b in emphasized)
                flags = []
                if is_emph:
                    flags.append("emphasized")
                if table:
                    flags.append("table")
                if set(k) & OE_MARKS:
                    flags.append("oe_letters")
                if match.start() > 0 and line[match.start()-1] in "-‐‑":
                    flags.append("suffix")
                if match.end() < len(line) and line[match.end()] in "-‐‑":
                    flags.append("prefix")
                if flags:
                    loc["flags"] = flags
                all_words[k].append(loc)
                if k in resolved and resolved[k]["classification"] != "old_english":
                    excluded[k].append(loc)
                elif k in mapping or k in guide_map:
                    known[k].append(loc)
                elif k in nonlexical:
                    excluded[k].append(loc)
                else:
                    suspect[k].append(loc)

    compact = []
    for surface in sorted(known):
        # Every occurrence is retained in the transient concordance.  Persist
        # one location per file and the full count to keep the audit reviewable.
        locations = {}
        for loc in known[surface]:
            locations.setdefault(loc["path"], {k: v for k, v in loc.items() if k != "context"})
        record = {"surface": surface, "occurrence_count": len(known[surface]), "first_locations_by_file": list(locations.values()), "lemma_candidates": list(mapping.get(surface, {}).values())}
        if surface in guide_map:
            record["pronunciation_example"] = guide_map[surface]
        compact.append(record)
    summary = {
        "corpus_files": len(paths),
        "total_tokens": sum(map(len, all_words.values())),
        "distinct_tokens": len(all_words),
        "registered_lemmas": len(lemmas),
        "registered_exact_surfaces": register_surface_count,
        "indexed_exact_surfaces_with_resolutions": len(mapping),
        "matched_surface_types": len(known),
        "unmatched_candidate_types": len(suspect),
        "pronunciation_only_types_in_corpus": sorted(s for s in known if s in guide_map and s not in mapping),
        "explicitly_resolved_nonword_types": len(excluded),
    }
    (OUT / "all-token-concordance.json").write_text(serial(all_words), encoding="utf-8")
    (OUT / "unmatched-candidates.json").write_text(serial(suspect), encoding="utf-8")
    lines = []
    for token, locs in sorted(suspect.items()):
        flags = sorted(set(f for l in locs for f in l.get("flags", [])))
        context = locs[0]["context"]
        lines.append(f"{token}\t{len(locs)}\t{','.join(flags)}\t{locs[0]['path']}:{locs[0]['line']}\t{context}")
    (OUT / "unmatched-candidates.tsv").write_text("\n".join(lines)+"\n", encoding="utf-8")
    (OUT / "all-unmatched-types.txt").write_text("\n".join(sorted(set(all_words) - set(known)))+"\n", encoding="utf-8")
    (OUT / "known-lemma-summary.json").write_text(serial(lemmas), encoding="utf-8")
    detailed = {"schema_version": 1, "status": "unresolved" if suspect else "all corpus surface types have a lookup or reviewed exclusion disposition", "matching_policy": "NFC + case folding only; explicit alternatives and resolutions only; no inferred vowel lengths or generic thorn/eth replacement. Surface matches may also occur as English homographs or morphological stems, so occurrence counts are not OE token-frequency claims.", "manifest": manifest, "summary": summary, "surfaces": compact}
    (OUT / "detailed-inventory.json").write_text(serial(detailed), encoding="utf-8")
    compact_rows = []
    for row in compact:
        first = row["first_locations_by_file"][0]
        route = "register_or_explicit_resolution" if row["lemma_candidates"] else "pronunciation_example"
        compact_rows.append([row["surface"], sorted(r["lemma_id"] for r in row["lemma_candidates"]), row["occurrence_count"], first["path"], first["line"], route])
    del detailed["surfaces"]
    detailed["surface_columns"] = ["surface_NFC_casefold", "lemma_ids", "raw_occurrence_count", "first_path", "first_line", "lookup_route"]
    detailed["disposition_files"] = ["resolutions.json", "reviewed-exclusions.json"]
    header = json.dumps(detailed, ensure_ascii=False, indent=2)[:-2]
    # One compact row per surface remains easy to diff without committing the
    # multi-megabyte concordance, register snapshot, or repeated evidence data.
    content = header + ',\n  "surfaces": [\n' + ',\n'.join('    '+json.dumps(row, ensure_ascii=False) for row in compact_rows) + '\n  ]\n}\n'
    (OWN / "inventory.json").write_text(content, encoding="utf-8")
    print(serial(summary))


if __name__ == "__main__":
    main()
