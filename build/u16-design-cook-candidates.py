import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "curriculum/proposals/unit16"


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))


sources = [
    "lexicon/entries.json",
    "sources/audits/unit16-source/lexical-inventory.json",
    "sources/audits/unit16-grammar/grammar-records.json",
    "sources/audits/unit16-grammar/source-support.json",
]
forms = {}
lemma_senses = defaultdict(dict)
loaded = []
for path in sources:
    if not (ROOT / path).exists():
        continue
    data = read(path)
    loaded.append(path)
    for lemma in data.get("lemmas", []):
        for sense in lemma.get("senses", []):
            lemma_senses[lemma["lemma_id"]][sense["sense_id"]] = {
                key: sense.get(key) for key in ["sense_id", "gloss", "knowledge_status", "production_taught_in", "recognition_taught_in"]
            }
        for form in lemma.get("forms", []):
            form_id = form["form_id"]
            if form_id not in forms:
                forms[form_id] = {
                    "lemma_id": lemma["lemma_id"],
                    **{key: form.get(key) for key in ["form_id", "form", "analysis", "contextual_analysis", "knowledge_status", "production_taught_in", "recognition_taught_in"]},
                    "input_paths": [path],
                }
            else:
                forms[form_id]["input_paths"].append(path)
                if path != "lexicon/entries.json":
                    forms[form_id]["proposed_current_scope"] = {key: form.get(key) for key in ["knowledge_status", "contextual_analysis", "scope_note"]}

surfaces = defaultdict(list)
for form in forms.values():
    surfaces[form["form"].casefold()].append(form)

models = read("sources/audits/unit16-grammar/author-only-cook-models.json")
prompts = {item["source_item_id"]: item for item in read("sources/audits/unit16-source/exercises-prompts.json")["items"]}
sequences = []
missing = defaultdict(list)
summary = []
for item in models["items"]:
    task_id = item["source_item_id"]
    tokens = []
    for index, literal in enumerate(item["model"].split(), 1):
        surface = literal.strip(".,;:!?‘’“”\"'()[]")
        candidates = surfaces.get(surface.casefold(), [])
        if not candidates:
            missing[surface].append([task_id, index])
        tokens.append({
            "token_index": index,
            "literal": literal,
            "surface": surface,
            "form_candidates": candidates,
            "sense_candidates_by_lemma": {lemma_id: list(lemma_senses[lemma_id].values()) for lemma_id in sorted({candidate["lemma_id"] for candidate in candidates})},
            "selected": None,
            "status": "unselected_candidate_listing_not_a_binding",
        })
    source_match = item.get("source_prompt") == prompts[task_id]["prompt"]
    sequences.append({"sequence_id": task_id + "-MODEL", "owner_id": task_id, "text": item["model"], "tokens": tokens, "source_prompt_exact": source_match, "model_unresolved": item.get("unresolved", []), "status": "candidates_only"})
    summary.append({"task_id": task_id, "tokens": len(tokens), "unmatched": sum(not token["form_candidates"] for token in tokens), "multiple_form_candidates": sum(len(token["form_candidates"]) > 1 for token in tokens), "source_prompt_exact": source_match})

(DEST / "author-only-cook-candidates.json").write_text(json.dumps({"schema_version": 1, "chapter": "ch16", "private": True, "pre_key_excluded": True, "status": "candidate_listing_not_contextual_assignment", "input_paths": loaded, "sequences": sequences}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(DEST / "cook-candidate-summary.json").write_text(json.dumps({"schema_version": 1, "chapter": "ch16", "status": "candidate_listing_only", "tasks": summary, "unmatched_surfaces": dict(missing), "rule": "Surface matching finds possible records; it does not settle morphology, sense, reference or teaching status. Every final token requires an explicit contextual choice and validation."}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"models": len(sequences), "tokens": sum(len(sequence["tokens"]) for sequence in sequences), "unmatched_surfaces": sorted(missing), "source_prompt_mismatches": [row["task_id"] for row in summary if not row["source_prompt_exact"]], "loaded": loaded}, ensure_ascii=False))
