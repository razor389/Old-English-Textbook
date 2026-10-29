import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))


def write(path, data):
    destination = ROOT / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


parser = argparse.ArgumentParser()
parser.add_argument("mode", choices=["prior", "forms", "features"])
parser.add_argument("values", nargs="*")
args = parser.parse_args()
lexicon = read("lexicon/entries.json")
grammar = read("curriculum/grammar.json")

if args.mode == "prior":
    records = []
    for chapter in range(1, 16):
        path = f"chapters/ch{chapter:02d}/coverage.json"
        raw = (ROOT / path).read_bytes()
        contract = json.loads(raw.decode("utf-8-sig"))
        records.append({
            "chapter_id": contract["chapter_id"],
            "path": path,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "status": contract["status"],
            "productive_outcomes": contract.get("productive_outcomes", []),
            "recognition_outcomes": contract.get("recognition_outcomes", []),
            "bounded_scope": contract.get("bounded_scope", []),
            "paradigm_ids": [p["paradigm_id"] for p in contract.get("paradigms", [])],
            "teaching_record_ids": [t.get("teaching_id") for t in contract.get("teaching_records", [])],
        })
    exact_ids = {
        "u02-personal-pronouns", "u02-dual-agreement", "u02-pronoun-reference",
        "u02-third-person-possessors", "u02-direct-quotation", "u05-direct-quotation",
        "u06-modal-cunnan", "u06-witan-object", "u06-don-object",
        "u09-content-that", "u09-reported-statement", "u09-report-reference",
        "u09-dependent-question", "u09-dependent-whether", "u09-command-infinitive",
        "u09-perception-infinitive", "u09-dative-speaking-recipient",
        "u12-narrative-time", "u12-preterite-anterior", "u12-habban-perfect",
        "u12-wesan-intransitive-perfect", "u12-wesan-present-participle",
        "u12-active-passive", "u12-reported-sequence",
        "u13-clause-role-parsing", "u13-main-fronting-order", "u13-pronoun-position-limits",
        "u13-reference-resolution-ambiguity", "u13-coordination-predicate-recovery",
        "u13-quoted-reference", "u13-long-sentence-analysis", "u13-dependent-order-tendencies",
        "u13-correlative-clause-reference", "u15-negative-concord",
    }
    actual = [f for f in grammar["features"] if f["feature_id"] in exact_ids]
    data = {
        "schema_version": 1,
        "chapter": "ch16",
        "status": "prior_authority_inspection",
        "baseline_revision": "e1d94be",
        "reading_rule": 'All fifteen complete active JSON contracts and both complete actual registers were parsed; teaching boundaries and the relevant actual records were inspected.',
        "register_counts": {
            "lemmas": len(lexicon["lemmas"]),
            "forms": sum(len(l.get("forms", [])) for l in lexicon["lemmas"]),
            "senses": sum(len(l.get("senses", [])) for l in lexicon["lemmas"]),
            "features": len(grammar["features"]),
        },
        "register_files": [
            {"path": p, "sha256": hashlib.sha256((ROOT / p).read_bytes()).hexdigest()}
            for p in ["lexicon/entries.json", "curriculum/grammar.json"]
        ],
        "contracts": records,
        "relevant_actual_feature_records": actual,
        "missing_requested_feature_ids": sorted(exact_ids - {f["feature_id"] for f in actual}),
        "sense_boundaries": [
            {
                "lemma_id": l["lemma_id"],
                "display_headword": l["display_headword"],
                "actual_sense_records": l["senses"],
            }
            for l in lexicon["lemmas"] if l["lemma_id"] in {"cunnan", "witan", "don", "gretan", "geseon", "secgan", "cwethan"}
        ],
    }
    write("curriculum/proposals/unit16/prior-audit.json", data)
    print(json.dumps({"counts": data["register_counts"], "contracts": len(records), "features": len(actual), "missing": data["missing_requested_feature_ids"]}, ensure_ascii=False))
elif args.mode == "forms":
    requested = set(args.values)
    for lemma in lexicon["lemmas"]:
        for form in lemma.get("forms", []):
            if form["form"] in requested:
                print(json.dumps({"lemma_id": lemma["lemma_id"], **{k: form.get(k) for k in ["form_id", "form", "analysis", "contextual_analysis", "production_taught_in", "recognition_taught_in"]}}, ensure_ascii=False))
elif args.mode == "features":
    for feature in grammar["features"]:
        if feature["feature_id"] in args.values:
            print(json.dumps(feature, ensure_ascii=False, indent=2))
