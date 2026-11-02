"""Build a versioned current glossary inventory without rewriting old audits.

Usage: python -X utf8 scripts/refresh_opening_glossary_inventory.py --revision BRIDGE
Importing this module is read-only. See --schema for the compact bridge contract.
Unresolved tokens/references are reported, never guessed or silently excluded.
"""
from collections import Counter, defaultdict
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = "scripts/refresh_opening_glossary_inventory.py"
BASELINES = {
    "surface_inventory": "sources/audits/glossaries/old-english/inventory.json",
    "task_inventory": "sources/audits/glossaries/english/exercise-inventory.json",
    "corpus_manifest": "glossaries/corpus-manifest.json",
    "course_boundary": "glossaries/course-boundary.json",
    "dictionary_presentation": "glossaries/dictionary-presentation.json",
}
TOKENIZER = ROOT / "sources/audits/glossaries/old-english/audit.py"
# This module has a main guard and no top-level writes. Do not import the old
# English inventory or one-use assembly modules: those execute mutations.
_spec = importlib.util.spec_from_file_location("_glossary_exact_tokens", TOKENIZER)
_tokens = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_tokens)
WORD, key, clean_line = _tokens.WORD, _tokens.key, _tokens.clean_line
SHA = re.compile(r"[0-9a-f]{64}\Z")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def json_digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def local(root, relative):
    """All bridge paths are explicit repository-relative paths, never escapes."""
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise ValueError("Expected a nonempty repository-relative POSIX path: " + repr(relative))
    path = Path(relative)
    if path.is_absolute() or ":" in relative or ".." in path.parts:
        raise ValueError("Path escapes repository: " + relative)
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError("Resolved path escapes repository: " + relative)
    return resolved


def read(root, relative):
    return json.loads(local(root, relative).read_text(encoding="utf-8-sig"))


def identity(root, relative):
    return {"path": relative, "sha256": digest(local(root, relative))}


def checked_identity(root, row, errors, label):
    if not isinstance(row, dict) or not SHA.fullmatch(str(row.get("sha256", ""))):
        errors.append("Invalid identity: " + label)
        return
    try:
        if digest(local(root, row["path"])) != row["sha256"]:
            errors.append("Identity differs: " + label + " / " + row["path"])
    except (KeyError, OSError, ValueError) as exc:
        errors.append("Cannot verify identity: " + label + " / " + str(exc))


def output_path(root, relative, occurrences=False):
    path = local(root, relative)
    allowed = [root / "build/opening"]
    if not occurrences:
        allowed.append(root / "docs/revisions/opening")
    if not any(path.is_relative_to(p.resolve()) for p in allowed):
        raise ValueError("Inventory output must stay under build/opening or docs/revisions/opening; "
                         "occurrences must stay under build/opening: " + relative)
    return path


def load_revision(root, relative):
    data = read(root, relative)
    errors = []
    if data.get("schema_version") != 1 or not data.get("revision_id"):
        errors.append("Revision bridge needs schema_version=1 and revision_id")
    for name, expected in BASELINES.items():
        row = data.get("baseline", {}).get(name, {})
        if row.get("path") != expected:
            errors.append("Baseline path must be " + expected)
        checked_identity(root, row, errors, "baseline." + name)
    outputs = data.get("current", {})
    try:
        paths = [output_path(root, outputs[name], name == "occurrences")
                 for name in ["surface_inventory", "task_inventory", "occurrences"]]
        if len(set(paths)) != len(paths) or local(root, relative) in paths:
            errors.append("Output paths must be distinct and cannot overwrite the bridge")
    except (KeyError, ValueError) as exc:
        errors.append(str(exc))
    for field in ["authorized_file_deltas", "surface_dispositions", "reference_forms",
                  "verb_entries", "nonverbal_overrides", "sense_aliases", "task_reviews",
                  "access_bridges"]:
        if field in data and not isinstance(data[field], list):
            errors.append(field + " must be an array")
    if errors:
        raise ValueError("; ".join(errors))
    return data


def boundary_errors(root, bridge):
    """An authorization changes only its named old hash to its named new hash."""
    boundary = read(root, BASELINES["course_boundary"])
    errors, deltas = [], {}
    rows = {r["path"]: r for r in boundary["files"]}
    if len(rows) != len(boundary["files"]):
        errors.append("Duplicate protected path in historical boundary")
    for delta in bridge.get("authorized_file_deltas", []):
        path = delta.get("path")
        if path in deltas or path not in rows:
            errors.append("Duplicate or unprotected authorization path: " + str(path))
            continue
        old = rows[path].get("sha256", rows[path].get("raw_sha256"))
        if delta.get("old_sha256") != old:
            errors.append("Authorization old identity differs from frozen boundary: " + path)
        if not SHA.fullmatch(str(delta.get("new_sha256", ""))) or not delta.get("reason"):
            errors.append("Authorization needs exact new SHA and reason: " + path)
        deltas[path] = delta
    for path, row in rows.items():
        expected = deltas[path].get("new_sha256") if path in deltas else row.get("sha256", row.get("raw_sha256"))
        try:
            if digest(local(root, path)) != expected:
                errors.append("Protected course changed outside exact authorization: " + path)
        except (OSError, ValueError) as exc:
            errors.append("Protected course unavailable: " + path + " / " + str(exc))
    return errors


def unique(values):
    return list(dict.fromkeys(values))


def keyed(rows, field, errors, label):
    result = {}
    for row in rows:
        value = row.get(field)
        if not value or value in result:
            errors.append("Missing/duplicate " + label + ": " + str(value))
        else:
            result[value] = row
    return result


def merge_reference_forms(dictionary, bridge, errors):
    result = {}
    old = [f for e in dictionary["verb_entries"] for f in e["glossary_only_reference_forms"]]
    for form in old + bridge.get("reference_forms", []):
        fid = form.get("form_id")
        if not fid or not form.get("form"):
            errors.append("Reference form lacks identity/spelling")
            continue
        if fid in result and result[fid] != form:
            errors.append("Conflicting reference form ID: " + fid)
        result[fid] = form
    for form in bridge.get("reference_forms", []):
        if (form.get("origin_category") not in ["exact source", "declared normalization", "new teaching material"]
                or not form.get("evidence_refs") or not form.get("formation_evidence")
                or not form.get("teaching_scope")):
            errors.append("Incomplete additive reference provenance: " + str(form.get("form_id")))
    return result


def validate_aliases(bridge, oe, en, register, errors):
    """Aliases never invent coverage; both actual IDs and routes must exist."""
    register_senses = {s["sense_id"]: (l, s) for l in register["lemmas"] for s in l["senses"]}
    aliases = {}
    for row in bridge.get("sense_aliases", []):
        start = len(errors)
        sid, target, eid = row.get("sense_id"), row.get("target_sense_id"), row.get("entry_id")
        if sid in aliases or sid == target or eid not in oe:
            errors.append("Invalid/duplicate sense alias: " + str(sid))
            continue
        senses = {s["sense_id"]: s for s in oe[eid]["senses"]}
        if sid not in senses or target not in senses or sid not in register_senses or target not in register_senses:
            errors.append("Sense alias IDs are not both present under their claimed meaning/head: " + str(sid))
            continue
        new_lemma, new_sense = register_senses[sid]
        old_lemma, _ = register_senses[target]
        if new_lemma["lemma_id"] != oe[eid]["lemma_id"] or old_lemma["lemma_id"] != oe[eid]["lemma_id"]:
            errors.append("Sense alias changes lemma identity: " + sid)
        if row.get("headword") != oe[eid]["headword"]:
            errors.append("Sense alias headword differs: " + sid)
        if row.get("meaning") != senses[sid]["meaning"] or row.get("target_meaning") != senses[target]["meaning"]:
            errors.append("Sense alias declared meanings differ from actual dictionary senses: " + sid)
        if row.get("register_gloss") != new_sense.get("gloss"):
            errors.append("Sense alias register gloss differs: " + sid)
        evidence = set(row.get("evidence_refs", []))
        if (not row.get("scope") or not evidence or not evidence <= set(senses[sid].get("evidence_refs", []))
                or not evidence <= set(new_sense.get("evidence_refs", []))):
            errors.append("Sense alias lacks matching explicit scope/evidence: " + sid)
        routes = [r for e in en.values() for r in e["routes"] if sid in r["sense_ids"]]
        if not routes or any(target not in r["sense_ids"] or eid not in r["entry_ids"] for r in routes):
            errors.append("Sense alias needs explicit new+target IDs on the existing English meaning route: " + sid)
        if len(errors) == start:
            aliases[sid] = {"entry_id": eid, "target_sense_id": target}
    return aliases


def spans(text, key_document=False):
    pattern = r"<!--\s*key:\s*(KEY-[^\s>]+)\s*-->" if key_document else r"<!--\s*item:\s*([^\s>]+)\s*-->"
    matches = list(re.finditer(pattern, text))
    result, duplicates = {}, []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.end():end].strip()
        row = {"line": text.count("\n", 0, match.start()) + 1,
               "block_sha256": hashlib.sha256(block.encode()).hexdigest(), "block": block}
        if match[1] in result:
            duplicates.append(match[1])
        result[match[1]] = row
    return result, duplicates


def task_semantics(task):
    outputs = task.get("output_positions", [])
    output_senses = unique(task.get("required_output_sense_ids", []) +
                           [s for o in outputs for s in o.get("required_output_sense_ids", [])])
    input_senses = unique(task.get("required_input_sense_ids", []) +
                          [s for o in outputs for s in o.get("required_input_sense_ids", [])])
    required = unique(task.get("required_sense_ids", []) + output_senses + input_senses +
                      [s for o in outputs for s in o.get("required_sense_ids", [])])
    supplied = unique(task.get("supplied_sense_ids", []) + [s for o in outputs for s in o.get("supplied_sense_ids", [])])
    mode = task.get("mode", task.get("kind", task.get("task_type", "")))
    if task["task_id"].startswith("EX-"):
        kind = "english_to_old_english_source_translation"
    elif outputs:
        kinds = " ".join(str(o.get("kind", "")) + " " + str(o.get("response_language", "")) for o in outputs).lower()
        kind = "mixed_or_old_english_output" if any(s in kinds for s in ["old_english", "old english", "form"]) else "english_analysis_or_translation_of_old_english"
    elif re.search(r"production|composition|transformation", mode):
        kind = "old_english_production_or_morphology"
    else:
        kind = "english_analysis_or_translation_of_old_english"
    return {"kind": kind, "original_mode": mode, "required_sense_ids": required,
            "required_input_sense_ids": input_senses, "required_output_sense_ids": output_senses,
            "supplied_sense_ids": supplied, "required_feature_ids": task.get("required_feature_ids", [])}


def generate(root, bridge):
    """Pure current scan. Returns two compact inventories and scratch occurrences."""
    errors = boundary_errors(root, bridge)
    inputs = {}

    def source(path, json_value=True):
        inputs[path] = digest(local(root, path))
        return read(root, path) if json_value else local(root, path).read_text(encoding="utf-8-sig")

    data = source("glossaries/entries.json")
    oe = keyed(data["old_english_entries"], "entry_id", errors, "OE entry")
    en = keyed(data["english_entries"], "entry_id", errors, "English entry")
    register = source("lexicon/entries.json")
    sense_ids = {s["sense_id"] for e in oe.values() for s in e["senses"]}
    register_senses = {s["sense_id"] for l in register["lemmas"] for s in l["senses"]}
    validate_aliases(bridge, oe, en, register, errors)
    dictionary = source(BASELINES["dictionary_presentation"])
    reference_forms = merge_reference_forms(dictionary, bridge, errors)
    for e in en.values():
        for route in e["routes"]:
            if not set(route["entry_ids"]) <= set(oe) or not set(route["sense_ids"]) <= sense_ids:
                errors.append("Dangling English route: " + e["entry_id"])
    mapping = defaultdict(set)
    for eid, entry in oe.items():
        for form in [entry["headword"], *entry["forms"]]:
            if WORD.fullmatch(form):
                mapping[key(form)].add(eid)
    lookups = source("glossaries/form-lookup.json")
    for row in lookups["forms"]:
        for eid in row["entry_ids"]:
            if eid not in oe or key(row["surface"]) not in {key(f) for f in oe[eid]["forms"]}:
                errors.append("Dangling/unlisted existing surface route: " + row["surface"] + " / " + eid)
            else:
                mapping[key(row["surface"])].add(eid)
    resolutions = source("sources/audits/glossaries/old-english/resolutions.json")
    excluded = source("sources/audits/glossaries/old-english/reviewed-exclusions.json")
    nonlexical = {key(s): label for label, words in excluded["groups"].items() for s in words}
    special = {key(r["surface"]): r["classification"] for r in resolutions["resolutions"] if r["classification"] != "old_english"}
    for row in lookups["special_dispositions"]:
        special[key(row["surface"])] = row.get("classification", "special_disposition")
    added = keyed(bridge.get("surface_dispositions", []), "surface", errors, "surface disposition")
    for surface, row in added.items():
        k = key(surface)
        if surface != k or not row.get("reason") or not row.get("evidence_refs"):
            errors.append("Disposition needs exact NFC/casefold spelling, reason and evidence: " + surface)
        if row.get("classification") == "old_english":
            targets = row.get("entry_ids", [])
            if not targets or any(eid not in oe or k not in {key(f) for f in oe[eid]["forms"]} for eid in targets):
                errors.append("Unverified explicit lexical disposition: " + surface)
            else:
                mapping[k].update(targets)
        elif row.get("classification") == "nonlexical":
            if k in mapping:
                errors.append("New exclusion would hide a known lexical route: " + surface)
            else:
                nonlexical[k] = row["reason"]
        else:
            errors.append("Unsupported new disposition classification: " + surface)
    manifest = source(BASELINES["corpus_manifest"])
    docs = manifest["documents"]
    if len({r["path"] for r in docs}) != len(docs):
        errors.append("Duplicate corpus path")
    texts, current_manifest = {}, []
    counts, firsts, by_file = Counter(), {}, defaultdict(dict)
    unresolved, occurrences = defaultdict(list), []
    total, excluded_count = 0, 0
    for doc in docs:
        path = doc["path"]
        text = source(path, False)
        texts[path] = text
        current_manifest.append({"path": path, "sha256": inputs[path], "lines": len(text.splitlines())})
        item = section = None
        for number, raw in enumerate(text.splitlines(), 1):
            marker = re.search(r"<!--\s*(?:item|key):\s*(.*?)\s*-->", raw)
            if marker:
                item = marker[1]
            if raw.startswith("#"):
                section, item = raw.lstrip("# "), None
            line = clean_line(raw)
            for match in WORD.finditer(line):
                total += 1
                surface, k = match[0], key(match[0])
                loc = {"surface": surface, "normalized_surface": k, "path": path,
                       "line": number, "column": match.start() + 1}
                if item:
                    loc["item"] = item
                if section:
                    loc["section"] = section
                if k in special:
                    excluded_count += 1
                elif k in mapping:
                    counts[k] += 1
                    firsts.setdefault(k, (path, number))
                    by_file[k].setdefault(path, number)
                    loc.update(classification="matched_exact_surface", entry_ids=sorted(mapping[k]))
                    occurrences.append(loc)
                elif k in nonlexical:
                    excluded_count += 1
                else:
                    loc.update(classification="unresolved", context=line.strip())
                    unresolved[k].append(loc)
                    occurrences.append(loc)
    pending = [{"surface": s, "occurrence_count": len(locs), "sample_locations": locs[:3]}
               for s, locs in sorted(unresolved.items())]
    if pending:
        errors.append("Unresolved current token types: " + str(len(pending)))
    # A separate exact bridge covers already-reviewed supplementary material;
    # it cannot silently change the original 38-master instructional corpus.
    access_reports = []
    for ident in bridge.get("access_bridges", []):
        checked_identity(root, ident, errors, "access bridge")
        access = source(ident["path"])
        master = access.get("master")
        if not isinstance(master, str) or not access.get("master_sha256"):
            errors.append("Unsupported access bridge master identity: " + ident["path"])
            continue
        checked_identity(root, {"path": master, "sha256": access["master_sha256"]}, errors, "access bridge master")
        inputs[master] = digest(local(root, master))
        master_lines = local(root, master).read_text(encoding="utf-8-sig").splitlines()
        lexical_count = 0
        for row in access.get("items", []):
            if row.get("category") != "old_english":
                continue
            lexical_count += 1
            eid, sid = row.get("entry_id"), row.get("sense_id")
            if eid not in oe or row.get("headword") != oe[eid]["headword"]:
                errors.append("Dangling/different access-bridge headword: " + str(row.get("text")))
            elif sid not in {s["sense_id"] for s in oe[eid]["senses"]}:
                errors.append("Dangling access-bridge sense: " + str(sid))
            if not row.get("occurrence_lines") or any(
                    not isinstance(n, int) or n < 1 or n > len(master_lines) or row["text"] not in master_lines[n - 1]
                    for n in row.get("occurrence_lines", [])):
                errors.append("Stale access-bridge occurrence: " + str(row.get("text")))
        if not lexical_count:
            errors.append("Access bridge contains no explicit lexical records: " + ident["path"])
        access_reports.append({"path": ident["path"], "sha256": ident["sha256"], "master": master,
                               "master_sha256": access["master_sha256"], "lexical_records": lexical_count})
    baseline_tasks = source(BASELINES["task_inventory"])["items"]
    baseline_ids = {t["task_id"] for t in baseline_tasks}
    if len(baseline_ids) != len(baseline_tasks):
        errors.append("Duplicate historical task ID")
    contracts = sorted({t["contract"] for t in baseline_tasks})
    reviews = keyed(bridge.get("task_reviews", []), "chapter_id", errors, "task-group review")
    old_docs = {d["path"]: d["sha256"] for d in docs}
    old_boundary = {r["path"]: r.get("sha256", r.get("raw_sha256")) for r in read(root, BASELINES["course_boundary"])["files"]}
    english_by_sense = defaultdict(set)
    for e in en.values():
        for route in e["routes"]:
            for sid in route["sense_ids"]:
                english_by_sense[sid].add(e["entry_id"])
    tasks, group_reports = [], []
    for contract_path in contracts:
        contract = source(contract_path)
        pronunciation = contract_path == "guides/pronunciation/coverage.json"
        chapter = "pronunciation" if pronunciation else contract["chapter_id"]
        folder = "guides/pronunciation" if pronunciation else "chapters/" + chapter
        student_path, key_path = folder + "/student.md", folder + "/answer-key.md"
        for path in [student_path, key_path]:
            if path not in texts:
                errors.append("Task master omitted from original corpus: " + path)
                texts[path] = source(path, False)
        learner, duplicate_learner = spans(texts[student_path])
        answers, duplicate_answers = spans(texts[key_path], True)
        errors.extend("Duplicate learner marker: " + i for i in duplicate_learner)
        errors.extend("Duplicate key marker: " + i for i in duplicate_answers)
        if pronunciation:
            assigned = [{**t, "task_id": t["id"], "group_prompt": g["prompt_type"]}
                        for g in contract["practice"] for t in g["items"]]
        else:
            assigned = contract["assigned_items"]
        expected = {t["task_id"] for t in assigned}
        if len(expected) != len(assigned) or expected != set(learner):
            errors.append("Learner markers differ from active contract: " + chapter)
        binding = {"student_sha256": inputs[student_path], "key_sha256": inputs[key_path],
                   "contract_sha256": inputs[contract_path]}
        changed = any(inputs[p] != old_docs.get(p) for p in [student_path, key_path]) or inputs[contract_path] != old_boundary.get(contract_path)
        if changed:
            review = reviews.get(chapter, {})
            if review.get("status") != "accepted" or any(review.get(k) != v for k, v in binding.items()):
                errors.append("Changed task group needs exact accepted review binding: " + chapter)
            witnesses = review.get("review_evidence", [])
            if not witnesses:
                errors.append("Changed task group lacks review receipt: " + chapter)
            for witness in witnesses:
                checked_identity(root, witness, errors, "task review " + chapter)
        group_reports.append({"chapter_id": chapter, **binding, "changed_from_baseline": changed,
                              "task_count": len(assigned), "review_required": changed})
        for task in assigned:
            tid = task["task_id"]
            key_id = task.get("key_item_id", task.get("key_id")) or "KEY-" + tid
            if key_id not in answers or tid not in learner:
                errors.append("Missing task/key marker: " + tid)
            if pronunciation:
                semantics = {"kind": "pronunciation_only_no_english_to_old_english_requirement",
                             "required_sense_ids": [], "required_input_sense_ids": [],
                             "required_output_sense_ids": [], "supplied_sense_ids": []}
                if task.get("required_sense_ids") or task.get("required_output_sense_ids"):
                    errors.append("Pronunciation task unexpectedly claims translation requirements: " + tid)
            else:
                semantics = task_semantics(task)
            for sid in semantics["required_sense_ids"] + semantics["supplied_sense_ids"]:
                if sid not in sense_ids or sid not in register_senses:
                    errors.append("Unresolved task sense: " + tid + " / " + sid)
            access = sorted({eid for sid in semantics["required_sense_ids"] for eid in english_by_sense[sid]})
            missing = [sid for sid in semantics["required_sense_ids"] if not english_by_sense[sid]]
            if missing:
                errors.append("Missing English access: " + tid + " / " + ", ".join(missing))
            row = {"task_id": tid, "chapter_id": chapter, "contract": contract_path,
                   "contract_record_sha256": json_digest(task), "contract_prompt": task.get("prompt", task.get("group_prompt", "")),
                   "key_item_id": key_id, **semantics, "english_entry_ids": access, "missing_senses": missing}
            for name, path, span in [("student", student_path, learner.get(tid)), ("key", key_path, answers.get(key_id))]:
                row[name] = {"path": path, "master_sha256": inputs[path],
                             **({k: v for k, v in span.items() if k != "block"} if span else {})}
            row["actual_prompt"] = learner.get(tid, {}).get("block", "").split("\n\n", 1)[0]
            if pronunciation:
                row["supplied_forms"] = task.get("forms", [task["form"]] if "form" in task else [])
                row["exclusion_reason"] = "Current task asks for sounds, articulation, syllables or stress; all OE words and meanings are supplied. No English-to-OE production requirement."
            for field in ["output_positions", "source_original_id", "source_locator", "lexical_sense_demands",
                          "lexical_frame_requirements", "local_support", "supplied_support", "target_specification"]:
                if field in task:
                    row[field] = task[field]
            tasks.append(row)
    if {t["task_id"] for t in tasks} != baseline_ids or len(tasks) != len(baseline_tasks):
        errors.append("Current task identity/count differs from frozen inventory")
    # Ensure a new bridge cannot authorize an unused typo/extra task group.
    if set(reviews) - {r["chapter_id"] for r in group_reports}:
        errors.append("Review binding names unknown task group")
    common = {"schema_version": 1, "generator": GENERATOR, "revision_id": bridge["revision_id"],
              "bridge_content_sha256": json_digest(bridge), "input_sha256": dict(sorted(inputs.items())),
              "status": "passed" if not errors else "unresolved", "errors": unique(errors)}
    compact = [[s, sorted(oe[eid]["lemma_id"] for eid in mapping[s]), counts[s], *firsts[s], "current_exact_surface"]
               for s in sorted(counts)]
    inventory = {**common, "manifest": current_manifest,
                 "matching_policy": "NFC + casefold only. Counts are exact spelling occurrences, including English/OE homographs, not OE token frequencies.",
                 "surface_columns": ["surface_NFC_casefold", "lemma_ids", "raw_occurrence_count", "first_path", "first_line", "lookup_route"],
                 "surfaces": compact, "first_locations_by_file": {s: by_file[s] for s in sorted(counts)},
                 "summary": {"corpus_files": len(docs), "total_tokens": total, "matched_surface_types": len(counts),
                             "matched_occurrences": sum(counts.values()), "excluded_occurrences": excluded_count,
                             "unresolved_token_types": len(pending)}, "unresolved": pending,
                 "reference_form_ids": sorted(reference_forms), "access_bridges": access_reports}
    task_inventory = {**common, "items": tasks, "groups": group_reports,
                      "summary": {"tasks": len(tasks), "baseline_tasks": len(baseline_tasks),
                                  "pronunciation_responses": sum(t["chapter_id"] == "pronunciation" for t in tasks)}}
    return inventory, task_inventory, occurrences


def validate_retained(root, bridge):
    """Recompute: retained JSON cannot manufacture coverage by dropping records."""
    inventory, tasks, _ = generate(root, bridge)
    errors = list(inventory["errors"])
    for name, value in [("surface_inventory", inventory), ("task_inventory", tasks)]:
        try:
            if read(root, bridge["current"][name]) != value:
                errors.append("Retained current inventory is stale or differs from actual inputs: " + name)
        except (OSError, ValueError) as exc:
            errors.append("Cannot read current inventory " + name + ": " + str(exc))
    return inventory, tasks, unique(errors)


def write_outputs(root, bridge, inventory, tasks, occurrences, bridge_path):
    outputs = bridge["current"]
    inputs = set(inventory["input_sha256"]) | {bridge_path} | set(BASELINES.values())
    targets = {name: output_path(root, outputs[name], name == "occurrences")
               for name in ["surface_inventory", "task_inventory", "occurrences"]}
    if any(outputs[name] in inputs for name in targets):
        raise ValueError("Output would overwrite a source or historical input")
    for name, path in targets.items():
        if path.exists():
            try:
                first = None
                if name == "occurrences":
                    with path.open(encoding="utf-8") as stream:
                        first = stream.readline()
                prior = json.loads(first) if first is not None else json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                raise ValueError("Refusing to replace unowned output: " + outputs[name])
            if prior.get("generator") != GENERATOR:
                raise ValueError("Refusing to replace unowned output: " + outputs[name])
    for path in targets.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    for name, data in [("surface_inventory", inventory), ("task_inventory", tasks)]:
        targets[name].write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    with targets["occurrences"].open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps({"generator": GENERATOR, "revision_id": bridge["revision_id"],
                                 "type": "occurrence_manifest", "input_sha256": inventory["input_sha256"]}, ensure_ascii=False) + "\n")
        for row in occurrences:
            stream.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def schema():
    return {
        "schema_version": 1, "revision_id": "opening-2026-11-02",
        "baseline": {k: {"path": p, "sha256": "<actual frozen file SHA256>"} for k, p in BASELINES.items()},
        "current": {"surface_inventory": "docs/revisions/opening/glossary-current-inventory.json",
                    "task_inventory": "docs/revisions/opening/glossary-current-exercises.json",
                    "occurrences": "build/opening/glossary/current-occurrences.jsonl"},
        "authorized_file_deltas": [{"path": "<exact path in frozen 137-file boundary>",
                                    "old_sha256": "<frozen raw SHA256>", "new_sha256": "<final accepted raw SHA256>", "reason": "<authorized revision>"}],
        "surface_dispositions": [{"surface": "<exact NFC/casefold token>", "classification": "nonlexical",
                                  "reason": "<actual inspected English/fragment context>", "evidence_refs": ["<review receipt or source record>"]}],
        "reference_forms": [], "verb_entries": [], "nonverbal_overrides": [],
        "sense_aliases": [{"sense_id": "ic-subject", "target_sense_id": "ic-personal", "entry_id": "OE-ic", "headword": "ic",
                           "meaning": "<exact new dictionary sense meaning>", "target_meaning": "I; me; we; us",
                           "register_gloss": "<exact new register gloss>", "scope": "subject forms only", "evidence_refs": ["<refs present in both new sense records>"]}],
        "task_reviews": [{"chapter_id": "ch01", "status": "accepted", "student_sha256": "<final>", "key_sha256": "<final>",
                          "contract_sha256": "<final>", "review_evidence": [{"path": "<review receipt>", "sha256": "<actual>"}]}],
        "access_bridges": [{"path": "appendices/sound-history/glossary-access.json", "sha256": "<actual retained receipt>"}],
        "notes": "Example placeholders are not executable authorization. Arrays may be empty where no additions/reviews are needed. The original 38 masters/task IDs are fixed by frozen baselines; no keys or prose are generated."
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", help="Explicit revision bridge; does not authorize edits to inputs")
    parser.add_argument("--schema", action="store_true", help="Print the bridge schema example without opening course files")
    args = parser.parse_args()
    if args.schema:
        print(json.dumps(schema(), ensure_ascii=False, indent=2))
        return
    if not args.revision:
        parser.error("--revision is required unless --schema is used")
    try:
        bridge = load_revision(ROOT, args.revision)
        inventory, tasks, occurrences = generate(ROOT, bridge)
        write_outputs(ROOT, bridge, inventory, tasks, occurrences, args.revision)
        print(json.dumps({"status": inventory["status"], "surfaces": inventory["summary"], "tasks": tasks["summary"],
                          "outputs": bridge["current"], "errors": inventory["errors"][:20], "error_count": len(inventory["errors"])}, ensure_ascii=False))
        raise SystemExit(bool(inventory["errors"]))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
