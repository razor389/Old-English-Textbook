import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "curriculum/proposals/unit16"


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))


def save(name, value):
    (DEST / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


source = read("sources/audits/unit16-source/exercises-prompts.json")
reading = read("sources/audits/unit16-source/reading-source.json")
apparatus = read("sources/audits/unit16-source/reading-apparatus.json")
tasks = read("curriculum/proposals/unit16/task-seed.json")["tasks"]
counts = {exercise: sum(item["original_exercise"] == exercise for item in source["items"]) for exercise in range(32, 37)}
assert counts == {32: 11, 33: 10, 34: 13, 35: 14, 36: 11}, counts
assert len({item["source_item_id"] for item in source["items"]}) == 59
assert reading["total_word_count"] == 444
assert len(apparatus["notes"]) == 54
assert sum(len(note["anchors"]) for note in apparatus["notes"]) == 59

cook_items = []
for item in source["items"]:
    cook_items.append({
        **item,
        "task_id": item["source_item_id"],
        "key_item_id": "KEY-" + item["source_item_id"],
        "disposition": "assigned_in_proposal",
        "prompt_sha256": hashlib.sha256(item["prompt"].encode("utf-8")).hexdigest(),
        "assignment_rationale": "Retain the complete coherent Cook set; exact local support resolves any expressly supplied dependency without dropping a clause or item.",
    })

save("source-task-crosswalk.json", {
    "schema_version": 1,
    "chapter": "ch16",
    "status": "provisional_design_before_canonical_contract",
    "canonical_assignment_rule": "Only active chapter contracts assign source items. This proposal retains all59 original joint-group items; the later Unit16 contract will resolve prior deferrals without rewriting earlier contracts.",
    "cook_items": cook_items,
    "reading_spans": [{
        "source_span_id": span["source_span_id"], "title": span["title"],
        "source_id": span["source_id"], "original_identifier": span["original_identifier"],
        "printed_pages": span["printed_pages"], "pdf_pages_one_based": span["pdf_pages_one_based"],
        "start": span["start"], "end": span["end"], "word_count": span["word_count"],
        "line_number_convention": span["line_number_convention"],
        "prior_overlap": span["prior_overlap"],
        "task_ids": [task["task_id"] for task in tasks if task.get("source_span_id") == span["source_span_id"]],
    } for span in reading["source_spans"]],
    "unassigned_reading_boundary": "The subsequent Apollonius at the Feast begins after the selected scene on printed170; it is outside this assignment. The earlier storm and fisherman passages remain their prior contracts' supported readings.",
    "apparatus": {"path": "sources/audits/unit16-source/reading-apparatus.json", "note_ids": [note["apparatus_id"] for note in apparatus["notes"]], "note_count": 54, "anchor_count": 59, "rule": "Retain every original note and anchor separately from modern help. Original questions remain paratext unless an explicit task requests an output; no Latin knowledge is assumed."},
    "learner_display_rule": "Print each Cook prompt exactly as the checked source transcription, including all lexical hints, omission directions, number and order controls. Print the whole444word reading, separate original notes, and complete assigned modern helps.",
    "new_teaching_material": {"current_task_ids": [task["task_id"] for task in tasks], "pending_form_groups": [f"NEW-U16-F{i:02d}" for i in range(1, 6)], "teaching_example_ids": [f"NEW-U16-EXAMPLE-{i:02d}" for i in range(1, 5)], "new_narrative": False},
    "counts": {"cook_items": 59, "by_exercise": counts, "reading_words": 444, "reading_spans": 1, "source_notes": 54, "source_note_anchors": 59, "prospective_canonical_assigned": 515, "prospective_canonical_deferred": 129, "excluded": 0},
})

save("outcomes.json", {
    "schema_version": 1, "chapter": "ch16", "status": "proposed_scope_pending_final_dependency_reconciliation",
    "productive_outcomes": [
        "Produce every productive position of the complete selected nominal, adjectival and verbal systems, using their actual diagnostic stems, endings, exceptions and expressly bounded senses; preserve recognition-only, supplied and reference-only positions within their stated scope.",
        "Preserve subjects, objects, recipients and relative internal cases across extended clauses; distinguish perception actors with infinitives from nominative subjects of finite content clauses.",
        "Trace participants across quotation, reported content and narrated execution; recognize genuine ambiguity and use explicit nouns when an output requires unambiguous reference.",
        "Interpret simultaneous, anterior and intended-later situations from complete verb groups and context without automatic English backshift or an automatic future auxiliary.",
        "Use the newly assigned personal-acquaintance sense of cunnan, the separately evidenced personal-object witan, substitute-action dōn and bounded adverbial action comparison; do not impose an exclusive persons/facts division on the knowing verbs.",
        "Use each additional explicitly taught lexical government or complement frame required by Cook32–36, keeping complete local helps visible for dependencies deliberately left supplied.",
        "Translate all59 unchanged Cook prompts with every clause, participant, lexical hint, omission and word-order control accounted for; distinguish linguistic validity from compliance with an explicit target.",
    ],
    "recognition_outcomes": [
        "Translate the complete444word gymnasium scene with its local support, preserving arrival, announcement, game, recognition, service, departure, inquiry and invitation.",
        "Analyse the selected source pronouns, clause relations, finite and nonfinite forms, moods and relative temporal viewpoints without assigning productive mastery from a supplied token.",
        "Explain the final source mixture of direct and indirect construction through its actual speaker, immediate addressee and intended message recipient.",
        "Identify the edition's stated uncertainties in the king's knowledge/equal clause and the top passage, using supplied English explanations of the Latin parallels while translating the actual Old English.",
    ],
    "bounded_scope": [
        "The actual fifteen-unit contracts and registers at e1d94be alone establish prior teaching. A prior headword, source exposure or complete table does not license an untaught sense, use or unassigned mood.",
        "New nominal systems using familiar prior classes retain the stated count, mass, abstract, title and proper-name limits. No number sense or defective position is invented to fill a rectangle.",
        "All newly introduced verbal systems are complete within their stated indicative, present-subjunctive, imperative or nonfinite scope; citation principal parts do not silently create other moods or syntax.",
        "The new nearu adjective system retains its u/w alternation and complete strong/weak positive morphology. The new both system is plural; it does not acquire invented singular forms.",
        "Cunnan and witan have overlapping lexical possibilities. The selected complement contrast is a bounded teaching target, not an exclusive persons-versus-facts rule.",
        "Source-specific, rare and deliberately supplied Cook constructions remain supported during assessment. Their exact form, sense and whole-frame records must all be bound; no supplied help is tested as unaided recall.",
        "The exact reading ends at170.16 tō his gereorde. Earlier Apollonius readings and the following feast are not silently reassigned.",
        "The reading retains every original note and anchor. Its missing closing speech mark and ambiguous constructions are explained separately rather than silently normalized into a different Old English text.",
        "Every new composition is declared teaching material. Every requested output has an explicit target, essential meaning, defensible alternatives and relevant error diagnosis before the prose gate.",
        "Four short translated examples precede the corresponding practice after their prerequisites; there is no additional invented narrative.",
    ],
    "teaching_order_rule": "All required morphology, lexical meanings and grammar frames precede independent practice. Each translated example follows its own actual prerequisites. The practice stages group study, not postpone a dependency until after an output. All assigned local helps remain visible during supported work.",
    "study_sequence": [
        {"stage": 1, "title": "Participants and complete clauses", "examples": ["NEW-U16-EXAMPLE-01", "NEW-U16-EXAMPLE-02"], "practice": ["NEW-U16-A01", "NEW-U16-A02"]},
        {"stage": 2, "title": "Complete new forms and ordinary uses", "practice": ["NEW-U16-F01", "NEW-U16-F02", "NEW-U16-F03", "NEW-U16-F04", "NEW-U16-F05"]},
        {"stage": 3, "title": "Knowing, repeated actions and relative time", "examples": ["NEW-U16-EXAMPLE-03", "NEW-U16-EXAMPLE-04"], "practice": ["NEW-U16-C02", "NEW-U16-C03", "NEW-U16-A03"]},
        {"stage": 4, "title": "Speech and narrated action", "practice": ["NEW-U16-C01", "XII,XIII.32", "XII,XIII.33"]},
        {"stage": 5, "title": "Extended reports, comparison and lexical government", "practice": ["XII,XIII.34", "XII,XIII.35", "XII,XIII.36"]},
        {"stage": 6, "title": "The complete gymnasium scene", "practice": ["NEW-U16-R01", "NEW-U16-R02", "NEW-U16-R03", "NEW-U16-R04", "NEW-U16-R05", "NEW-U16-R06"]},
    ],
})
print(json.dumps({"cook": len(cook_items), "reading_words": reading["total_word_count"], "notes": len(apparatus["notes"]), "anchors": sum(len(note["anchors"]) for note in apparatus["notes"]), "scope_files": 2}))
