"""Check only blind-phase artifacts and strict-allowlist identities.

This does not read the current coverage contract, key, audits, or other reviews.
Marker equality and nonempty responses do not certify linguistic correctness.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
root = Path(__file__).resolve().parents[1]
learner_path = root / "chapters/ch17/student.md"
witness_path = root / "chapters/ch17/independent-solutions.md"
pattern = re.compile(r"<!-- (item|output): ([^>]+?) -->")


def identity(path):
    raw = path.read_bytes()
    return {
        "path": path.relative_to(root).as_posix(),
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "lf_sha256": hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest(),
    }


learner = learner_path.read_text(encoding="utf-8-sig")
witness = witness_path.read_text(encoding="utf-8-sig")
learner_markers = pattern.findall(learner)
witness_markers = pattern.findall(witness)
assert witness_markers == learner_markers, "Actual marker order/count differs"
assert len([x for x in witness_markers if x[0] == "item"]) == 103
assert len([x for x in witness_markers if x[0] == "output"]) == 146
for found in re.finditer(r"<!-- output: ([^>]+?) -->(.*?)(?=<!-- (?:item|output):|\Z)", witness, re.S):
    body = found.group(2).strip()
    assert body and len(body) > 2, f"Empty response: {found.group(1)}"
assert not re.search(r"\b(?:TODO|TBD|PLACEHOLDER)\b", witness)

baseline_paths = [root / f"chapters/ch{i:02}/coverage.json" for i in range(1, 17)]
baseline = []
for path in baseline_paths:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    baseline.append({
        **identity(path),
        "chapter_id": data["chapter_id"],
        "status": data["status"],
        "method": "Direct JSON parse; outcomes and bounded scopes read, actual prior forms/frames checked through cumulative registers. No linked audit/key opened.",
    })
registers = []
for relative, key in [("lexicon/entries.json", "lemmas"), ("curriculum/grammar.json", "features")]:
    path = root / relative
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    registers.append({
        **identity(path),
        "status": data["status"],
        "reviewed_chapters": data["reviewed_chapters"],
        "record_count": len(data[key]),
        "method": 'Direct queries of actual form, sense, construction and teaching-milestone records.',
    })

intake = {
    "schema_version": 1,
    "chapter": "ch17",
    "reviewer": "unit17_blind",
    "author_roles": [],
    "phase": "blind_solving_complete_pending_coordinator_freeze",
    "acceptance_claimed": False,
    "coordinator_issue": "oec-u17-review",
    "beads_writer": "root only; this worker executed no bd command",
    "git_actions": "none by this worker",
    "learner": identity(learner_path),
    "witness": identity(witness_path),
    "counts": {"actual_tasks": 103, "actual_requested_outputs": 146, "attempted_outputs": 146},
    "mechanical_check": "Exact combined item/output marker order equals current learner master; each output segment is nonempty. This is coverage evidence only.",
    "substantive_witness_statement": "Every composition has actual Old English, every analysis prompt an answer, and all three reading divisions full translations. The coordinator must read the actual responses before freeze.",
    "other_allowed_reads": [identity(root / p) for p in [
        "AGENTS.md", "EDITORIAL_POLICY.md", "sources/audits/unit17-coordinator/review-independence.json"
    ]],
    "earlier_active_contracts": baseline,
    "actual_registers": registers,
    "earlier_student_masters_opened": [],
    "original_primary_images_viewed": [],
    "external_linguistic_lookup": [],
    "prohibited_current_files_opened": [],
    "access_attestation": "No ch17 coverage/brief/key/audit/proposal/token-map/authorial translation/review/helper exposing answers was opened. Only the neutral named protocol was read in the current coordinator audit directory. No broad search of current source directories was performed.",
    "freeze_gate": "Only root's explicit later unlock after actual-response inspection and unchanged-witness Git commit permits comparison. No inferred unlock.",
    "own_helper": "build/u17-blind-validate.py",
}
out = root / "chapters/ch17/reviews/blind-intake.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(intake, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"learner": intake["learner"], "witness": intake["witness"], "counts": intake["counts"], "intake": out.relative_to(root).as_posix()}, ensure_ascii=False, indent=2))
