"""Check fixed source controls and bounded dependencies during the opening revision.

This complements independent linguistic review and the complete export checks;
it does not decide whether a task is pedagogically novel or an OE answer valid.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def canonical(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--scope", choices=["pronunciation", "unit1", "all"], default="all")
    ap.add_argument("--report", default="build/opening/domain-check.json")
    args = ap.parse_args()
    errors = []
    checks = []

    def check(condition, name, **detail):
        checks.append(name)
        if not condition:
            errors.append({"check": name, **detail})

    controls = read("docs/revisions/opening/controls.json")
    u1 = read("chapters/ch01/coverage.json")
    learner = (ROOT / "chapters/ch01/student.md").read_text(encoding="utf-8")
    key = (ROOT / "chapters/ch01/answer-key.md").read_text(encoding="utf-8")
    source_items = [x for x in u1["assigned_items"] if x["task_id"].startswith("EX-")]
    check(canonical(source_items) == controls["cook_items_canonical_sha256"], "All 46 complete Cook assignment records unchanged")
    for row in controls["cook_items"]:
        match = re.search(r"<!-- item: " + re.escape(row["task_id"]) + r" -->\s*\n\s*([^\n]+)", learner)
        prompt = re.sub(r"^\d+\.\s*", "", match[1]).replace("**", "") if match else None
        check(prompt == row["prompt"], "Exact Cook learner prompt " + row["task_id"], actual=prompt)
    check(controls["source_reading_markdown"] in learner, "Exact 69-word Cook reading unchanged")
    check(canonical(u1["paradigms"]) == controls["noun_paradigms_canonical_sha256"], "Existing logical noun/article/copula paradigm records unchanged")
    before_copula = learner.split("## 8.", 1)[0]
    actual_tables = re.findall(r"(?m)^\|[^\n]+\n\|[ |:\-]+\n(?:\|[^\n]+\n?)+", before_copula)
    check(actual_tables == controls["noun_article_table_blocks"], "All existing noun/article table cells unchanged")
    if "cook_key_section" in controls:
        actual = key.split("## 13.", 1)[1].split("## 14.", 1)[0]
        check(actual == controls["cook_key_section"], "All 46 Cook key models unchanged")
    boundary = read("docs/revisions/opening/preservation.json")
    changed = []
    for row in boundary["files"]:
        data = (ROOT / row["path"]).read_bytes()
        exact = hashlib.sha256(data).hexdigest() == row["sha256"]
        portable = row.get("sha256_normalized_lf") == hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()
        if not (exact or portable):
            changed.append(row["path"])
    check(not changed, "Unchanged files outside authorized revision", changed=changed)

    if args.scope in ["pronunciation", "all"]:
        contract = read("docs/revisions/opening/contract.json")["pronunciation"]
        cover = read("guides/pronunciation/coverage.json")
        text = (ROOT / "guides/pronunciation/student.md").read_text(encoding="utf-8-sig")
        answers = (ROOT / "guides/pronunciation/answer-key.md").read_text(encoding="utf-8-sig")
        ids = re.findall(r"<!-- item: (PRON-P\d+[a-z]) -->", text)
        key_ids = re.findall(r"<!-- answer: (PRON-P\d+[a-z]) -->", answers)
        check(ids == key_ids == list(contract["practice"]), "All 25 pronunciation learner/key IDs in order")
        records = [x for g in cover["practice"] for x in g["items"]]
        check({x["id"]: x["forms"] for x in records} == contract["practice"], "Practice forms match contracted reserved groups")
        check(all("form" not in x for x in records), "No stale singular example fields beside revised form groups")
        worked = text.split("## 7. Practice", 1)[0]
        bold = {s.casefold() for s in re.findall(r"\*\*([^*]+)\*\*", worked)}
        leaked = [s for s in contract["reserved_new_words"] if s.casefold() in bold]
        check(not leaked, "Reserved fresh words absent from worked exposition", leaked=leaked)
        check(all(s not in worked for s in ["gescēop", "heofonan", "eorðan"]), "Final reading targets are not earlier worked examples")
        check(all(text.count("[" + s + "]") <= 1 for s in ["ɣ", "x", "ç"]), "IPA limited to single introductory uses")
        examples = read("guides/pronunciation/examples.json")["examples"]
        example_forms = {x["form"] for x in examples}
        needed = {s for ss in contract["practice"].values() for s in ss}
        check(needed <= example_forms, "Every assessed pronunciation word has source evidence", missing=sorted(needed-example_forms))

    if args.scope in ["unit1", "all"]:
        tasks = u1["assigned_items"]
        ids = [x["task_id"] for x in tasks]
        learner_ids = re.findall(r"<!-- item: ([^ ]+) -->", learner)
        key_ids = re.findall(r"<!-- item: ([^ ]+) -->", key)
        check(len(ids) == len(set(ids)) == 92, "All 92 Unit 1 task IDs unique")
        check(set(ids) == set(learner_ids) == set(key_ids), "All Unit 1 tasks have learner and key counterparts")
        forms = {f["form_id"]: f for l in u1["lexical_inventory"] for f in l["forms"]}
        senses = {s["sense_id"] for l in u1["lexical_inventory"] for s in l["senses"]}
        features = {f["feature_id"] for f in u1["grammar_inventory"]}
        for item in tasks:
            required = set(item.get("required_form_ids", []))
            classified = set(item.get("tested_form_ids", []) + item.get("recognized_form_ids", []) + item.get("supplied_form_ids", []))
            check(required == classified, "Classified form dependencies " + item["task_id"], difference=sorted(required ^ classified))
            check(required <= forms.keys(), "Known form dependencies " + item["task_id"], missing=sorted(required-forms.keys()))
            check(set(item.get("required_sense_ids", [])) <= senses, "Known sense dependencies " + item["task_id"])
            check(set(item.get("required_feature_ids", [])) <= features, "Known grammar dependencies " + item["task_id"])
            bad = [fid for fid in item.get("tested_form_ids", []) if fid in forms and forms[fid]["knowledge_status"] not in ["new_production", "previously_taught"]]
            check(not bad, "Production uses taught forms " + item["task_id"], forms=bad)
        nominated = ["ic-nom-sg", "ic-nom-dual", "ic-nom-pl", "thu-nom-sg", "thu-nom-dual", "thu-nom-pl", "he-m-nom-sg", "he-n-nom-sg", "he-f-nom-sg", "he-nom-pl"]
        for fid in nominated:
            check(fid in forms and forms[fid]["knowledge_status"] == "new_production", "Taught subject form " + fid)
            check(any(fid in t.get("tested_form_ids", []) for t in tasks), "Contextual productive subject task " + fid)

    report = {"status": "fail" if errors else "pass", "scope": args.scope, "checks": len(checks),
              "protected_files": len(boundary["files"]), "errors": errors,
              "limitations": "Exact controls, inventories and dependency statuses only. Independent source/linguistic/novelty review and full PDF text plus actual page inspection are separate requirements."}
    path = ROOT / args.report
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: report[k] for k in ["status", "scope", "checks", "protected_files", "errors"]}, ensure_ascii=False))
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
