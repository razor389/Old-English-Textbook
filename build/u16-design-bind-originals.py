import copy
import json
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "curriculum/proposals/unit16"


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))


def save(name, value):
    (DEST / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


lexicon = read("lexicon/entries.json")
forms = {}
senses = {}
for lemma in lexicon["lemmas"]:
    for form in lemma["forms"]:
        forms[form["form_id"]] = (lemma["lemma_id"], form)
    for sense in lemma["senses"]:
        senses[sense["sense_id"]] = (lemma["lemma_id"], sense)
for lemma in read("curriculum/proposals/unit16/inventory.json")["lemmas"]:
    for form in lemma["forms"]:
        if form["form_id"] not in forms:
            forms[form["form_id"]] = (lemma["lemma_id"], form)
    for sense in lemma["senses"]:
        if sense["sense_id"] not in senses:
            senses[sense["sense_id"]] = (lemma["lemma_id"], sense)

aliases = {
    "the_mn": ("se-m-nom-sg", "se-the"),
    "the_ma": ("se-m-acc-sg", "se-the"),
    "the_na": ("se-n-acc-sg", "se-the"),
    "the_fa": ("se-f-acc-sg", "se-the"),
    "that_ma": ("se-m-acc-sg", "se-that"),
    "the_pln": ("se-all-nom-pl", "se-the"),
    "king_n": ("cyning-nom-sg", "cyning-source"),
    "king_a": ("cyning-acc-sg", "cyning-source"),
    "son_n": ("sunu-nom-sg", "sunu-1"),
    "son_a": ("sunu-acc-sg", "sunu-1"),
    "son_d": ("sunu-dat-sg", "sunu-1"),
    "father_n": ("faeder-nom-sg", "faeder-1"),
    "man_n": ("mann-nom-sg", "mann-1"),
    "man_a": ("mann-acc-sg", "mann-1"),
    "men_n": ("mann-nom-pl", "mann-1"),
    "book_a": ("boc-acc-sg", "boc-1"),
    "ship_a": ("scip-acc-sg", "scip-1"),
    "he_n": ("he-m-nom-sg", "he-1"),
    "him_d": ("he-m-dat-sg", "he-1"),
    "his": ("he-m-gen-sg", "he-possessor"),
    "they_n": ("he-nom-pl", "he-1"),
    "you_pln": ("thu-nom-pl", "thu-personal"),
    "I": ("ic-nom-sg", "ic-personal"),
    "me_d": ("ic-dat-sg", "ic-personal"),
    "saw": ("geseon-pret-3-sg", "geseon-1"),
    "saw_action": ("geseon-pret-3-sg", "geseon-perceive-action"),
    "went": ("gan-pret-3-sg", "gan-1"),
    "went_sub": ("gan-preterite-subj-3-sg", "gan-1"),
    "go_inf": ("gan-infinitive", "gan-1"),
    "come_inf": ("cuman-infinitive-citation", "cuman-come"),
    "came_sub": ("cuman-preterite-subj-3-sg", "cuman-come"),
    "said": ("secgan-pret-3-sg", "secgan-1"),
    "reported": ("secgan-pret-3-sg", "secgan-content"),
    "knew_content": ("witan-pret-3-sg", "witan-content"),
    "know_content_1": ("witan-pres-1-sg", "witan-content"),
    "that": ("thaet-conjunction-invariant", "thaet-conjunction-1"),
    "there": ("thaer-invariant-source", "thaer-there"),
    "here": ("her-invariant", "her-1"),
    "was_sub3": ("wesan-preterite-subj-3-sg", "wesan-be"),
    "am": ("wesan-pres-1-sg", "wesan-be"),
    "is": ("wesan-pres-3-sg", "wesan-be"),
    "made": ("gewyrcean-past-participle", "gewyrcean-1"),
    "had_aux_sub3": ("habban-preterite-subj-3-sg", "habban-perfect"),
    "sing_inf": ("singan-infinitive-citation", "singan-1"),
    "intended_sub3": ("willan-preterite-subj-3-sg", "willan-1"),
    "give_imp": ("sellan-imp-2-sg", "sellan-give"),
    "gave": ("sellan-pret-3-sg", "sellan-give"),
    "can_skill1": ("cunnan-pres-1-sg", "cunnan-1"),
    "can_skill2p": ("cunnan-pres-2-pl", "cunnan-1"),
    "well": ("wel-positive", "wel-positive"),
    "better": ("wel-comparative", "wel-comparative"),
    "than": ("thonne-invariant", "thonne-than"),
    "and": ("and-invariant", "and-1"),
    "so": ("swa-invariant", "swa-1"),
    "know_person1": ("cunnan-pres-1-sg", "cunnan-u16-acquaintance"),
    "know_person2p": ("cunnan-pres-2-pl", "cunnan-u16-acquaintance"),
    "played3": ("plegian-pret-3-sg", "plegian-u16-play"),
    "played3p": ("plegian-pret-3-pl", "plegian-u16-play"),
    "did3p": ("don-pret-3-pl", "don-u16-substitute"),
}

contexts = {
    "made": {"nonfinite": "past_participle", "use": "uninflected base with transitive habban compound", "note": "Retain the old record's source-passive analysis; Unit12 explicitly teaches this selected participle in the transitive compound."},
    "that": {"invariant": True, "function": "content conjunction", "note": "The prior source-shaped analysis remains intact; the current finite content clause is a taught Unit9 use."},
    "went_sub": {"tense": "preterite", "mood": "subjunctive", "person": 3, "number": "singular", "surface_ambiguity": "Third-singular indicative ēode has the same surface and is a defensible factual alternative in A02."},
    "so": {"invariant": True, "function": "manner adverb recovering the preceding action", "note": "This is prior swa-1, not the unrelated later proportional-comparison contextual annotation."},
}

seed = read("curriculum/proposals/unit16/task-seed.json")
models = read("curriculum/proposals/unit16/author-only-model-seed.json")
examples = read("curriculum/proposals/unit16/composition-seed.json")
task_by_id = {t["task_id"]: t for t in seed["tasks"]}
model_by_output = {o["output_id"]: o for t in models["tasks"] for o in t["outputs"]}
example_by_id = {e["example_id"]: e for e in examples["teaching_examples"]}

specifications = [
    ("NEW-U16-A01-IN01", "input", "NEW-U16-A01", 0, "the_mn king_n saw his son_a he_n went"),
    ("NEW-U16-A02-IN01", "input", "NEW-U16-A02", 0, "the_mn king_n saw_action the_ma son_a go_inf"),
    ("NEW-U16-A02-IN02", "input", "NEW-U16-A02", 1, "the_mn king_n knew_content that the_mn son_n went_sub"),
    ("NEW-U16-A03-IN01", "input", "NEW-U16-A03", 0, "he_n reported that the_mn king_n there was_sub3"),
    ("NEW-U16-A03-IN02", "input", "NEW-U16-A03", 1, "he_n reported that the_mn king_n the_na ship_a made had_aux_sub3"),
    ("NEW-U16-A03-IN03", "input", "NEW-U16-A03", 2, "he_n reported that the_mn king_n sing_inf intended_sub3"),
    ("NEW-U16-A01-O003-MODEL", "output", "NEW-U16-A01-O003", None, "the_mn king_n went"),
    ("NEW-U16-A01-O004-MODEL", "output", "NEW-U16-A01-O004", None, "the_mn son_n went"),
    ("NEW-U16-C01-O001-MODEL", "output", "NEW-U16-C01-O001", None, "the_mn king_n said his son_d give_imp me_d the_fa book_a"),
    ("NEW-U16-C01-O002-MODEL", "output", "NEW-U16-C01-O002", None, "the_mn son_n gave him_d the_fa book_a"),
    ("NEW-U16-C02-O002-MODEL", "output", "NEW-U16-C02-O002", None, "I can_skill1 sing_inf"),
    ("NEW-U16-C02-O003-MODEL", "output", "NEW-U16-C02-O003", None, "I know_content_1 that he_n here is"),
    ("NEW-U16-C02-O001-MODEL", "output", "NEW-U16-C02-O001", None, "I know_person1 the_ma man_a"),
    ("NEW-U16-C03-O001-MODEL", "output", "NEW-U16-C03-O001", None, "the_pln men_n played3p well the_mn king_n played3 better than they_n did3p"),
    ("NEW-U16-EXAMPLE-01-TEXT", "example", "NEW-U16-EXAMPLE-01", None, "the_mn father_n said I am here the_mn father_n reported that he_n there was_sub3"),
    ("NEW-U16-EXAMPLE-02-TEXT", "example", "NEW-U16-EXAMPLE-02", None, "he_n saw_action the_ma man_a come_inf he_n knew_content that the_mn man_n came_sub"),
    ("NEW-U16-EXAMPLE-03-TEXT", "example", "NEW-U16-EXAMPLE-03", None, "you_pln know_person2p the_ma king_a you_pln can_skill2p sing_inf"),
    ("NEW-U16-EXAMPLE-04-TEXT", "example", "NEW-U16-EXAMPLE-04", None, "he_n played3 well and they_n did3p so"),
]

errors = []
sequences = []

for sequence_id, kind, owner_id, position, alias_text in specifications:
    if kind == "input":
        text = task_by_id[owner_id]["inputs"][position]
    elif kind == "output":
        text = model_by_output[owner_id]["model"]
    else:
        text = example_by_id[owner_id]["text"]
    literals = text.split()
    alias_ids = alias_text.split()
    if len(literals) != len(alias_ids):
        errors.append({"sequence_id": sequence_id, "error": "token_count", "text_count": len(literals), "specification_count": len(alias_ids)})
        continue
    tokens = []
    for number, (literal, alias) in enumerate(zip(literals, alias_ids), 1):
        surface = literal.strip(".,;:!?‘’“”\"'()[]")
        form_id, sense_id = aliases[alias]
        if form_id not in forms or sense_id not in senses:
            errors.append({"sequence_id": sequence_id, "token_index": number, "error": "missing_id", "form_id": form_id, "sense_id": sense_id})
            continue
        form_lemma, form = forms[form_id]
        sense_lemma, sense = senses[sense_id]
        if form_lemma != sense_lemma:
            errors.append({"sequence_id": sequence_id, "token_index": number, "error": "lemma_mismatch"})
        if unicodedata.normalize("NFC", surface).casefold() != unicodedata.normalize("NFC", form["form"]).casefold():
            errors.append({"sequence_id": sequence_id, "token_index": number, "error": "surface_mismatch", "literal": literal, "form": form["form"]})
        if not (form.get("production_taught_in") or form.get("knowledge_status") == "new_production") or not (sense.get("production_taught_in") or sense.get("knowledge_status") == "new_production"):
            errors.append({"sequence_id": sequence_id, "token_index": number, "error": "not_assigned_production", "form_id": form_id, "sense_id": sense_id})
        tokens.append({
            "token_index": number, "literal": literal, "surface": surface,
            "lemma_id": form_lemma, "form_id": form_id, "sense_id": sense_id,
            "analysis": copy.deepcopy(form["analysis"]),
            "contextual_analysis": copy.deepcopy(contexts.get(alias, form.get("contextual_analysis", form["analysis"]))),
            "form_status": "previously_taught" if form.get("production_taught_in") else form.get("knowledge_status", "unresolved"),
            "sense_status": "previously_taught" if sense.get("production_taught_in") else sense.get("knowledge_status", "unresolved"),
            "prior_form_production": form.get("production_taught_in"),
            "prior_sense_production": sense.get("production_taught_in"),
        })
    record = {"sequence_id": sequence_id, "owner_id": owner_id.rsplit("-O", 1)[0] if kind == "output" else owner_id, "kind": kind, "text": text, "tokens": tokens, "required_form_ids": sorted({t["form_id"] for t in tokens}), "required_sense_ids": sorted({t["sense_id"] for t in tokens}), "status": "bound_to_exact_prior_or_assigned_current_records"}
    if kind == "output":
        record["output_position_id"] = owner_id
    sequences.append(record)

pending = []
save("public-sequence-bindings.json", {"schema_version": 1, "chapter": "ch16", "status": "complete_original_sentence_bindings", "sequences": [s for s in sequences if s["kind"] == "input"]})
save("author-only-sequence-bindings.json", {"schema_version": 1, "chapter": "ch16", "visibility": "author_only", "status": "complete_original_sentence_bindings", "sequences": [s for s in sequences if s["kind"] == "output"]})
save("composition-bindings.json", {"schema_version": 1, "chapter": "ch16", "status": "complete_four_example_bindings", "sequences": [s for s in sequences if s["kind"] == "example"]})
save("sequence-binding-validation.json", {"schema_version": 1, "chapter": "ch16", "status": "pass" if not errors else "fail", "scope": "The original sentence inputs/outputs and four examples; form tasks, Cook models and reading have separate ledgers.", "bound_sequences": len(sequences), "bound_tokens": sum(len(s["tokens"]) for s in sequences), "errors": errors, "pending": pending})
print(json.dumps({"sequences": len(sequences), "tokens": sum(len(s["tokens"]) for s in sequences), "errors": errors, "pending_groups": len(pending)}, ensure_ascii=False))
