import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "curriculum/proposals/unit16"
DEST.mkdir(parents=True, exist_ok=True)


def save(name, value):
    (DEST / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


tasks = []
private = []


def task(short, kind, prompt, inputs, outputs, features=(), notes=()):
    identifier = "NEW-U16-" + short
    public_outputs = []
    private_outputs = []
    for number, output in enumerate(outputs, 1):
        label, language, target, essentials, alternatives = output
        output_id = f"{identifier}-O{number:03d}"
        public_outputs.append({"output_position_id": output_id, "output_id": output_id, "kind": "old_english_translation" if language == "Old English" else "explanation", "label": label, "response_language": language})
        private_outputs.append({"output_position_id": output_id, "output_id": output_id, "model": target, "essential_meaning": essentials, "valid_alternatives": alternatives, "target_compliance": "Check the stated task instruction separately from general linguistic validity."})
    tasks.append({
        "task_id": identifier, "key_item_id": "KEY-" + identifier,
        "origin": "new_teaching_material", "task_type": kind,
        "prompt": prompt, "inputs": inputs,
        "output_positions": public_outputs,
        "required_feature_ids": list(features),
        "local_support": [], "dependency_status": "pending_exact_binding_and_independent_reconciliation",
        "design_notes": list(notes),
        "grading_visibility_rule": "Public output labels describe the response requested; private target text and grammatical solutions are not printed in the learner response grid.",
    })
    private.append({"task_id": identifier, "outputs": private_outputs})


task("A01", "reference_analysis",
     "Give the two defensible readings of the final hē. Then rewrite the second sentence twice, replacing only hē with an explicit noun phrase so that each reading is unambiguous. The first sentence identifies the king's son.",
     ["Se cyning geseah his sunu. Hē ēode."], [
         ("First reading", "English", "Hē may refer to the king.", "One possible masculine singular actor is the king.", "The two readings may be given in either order."),
         ("Second reading", "English", "Hē may refer to the son.", "The other possible masculine singular actor is the son; nearest position does not prove it.", "The two readings may be given in either order."),
         ("First explicit version", "Old English", "Se cyning ēode.", "The king went.", "Exchange the order of the two explicit versions if the reading labels are exchanged."),
         ("Second explicit version", "Old English", "Se sunu ēode.", "The son went.", "Exchange the order of the two explicit versions if the reading labels are exchanged."),
     ], ["u02-pronoun-reference", "u02-third-person-possessors", "u13-reference-resolution-ambiguity", "u06-gan-intransitive"])

task("A02", "complement_analysis",
     "Translate both sentences. For each, identify the expression denoting the person who went, its case and its relation to the verb of going. Then compare the two forms of go: which is nonfinite, which is finite, and does the spelling of the finite form distinguish its mood here?",
     ["Se cyning geseah ðone sunu gān.", "Se cyning wiste ðæt se sunu ēode."], [
         ("Sentence 1 translation", "English", "The king saw the son go.", "The king perceives the son's going.", "The king saw the son walking is defensible if the bounded action sense is preserved."),
         ("Sentence 2 translation", "English", "The king knew that the son went.", "Knowledge has a finite content complement with the son as its subject.", "Had gone is defensible with an explicitly stated anterior context; it is not forced by the form alone."),
         ("Sentence 1 actor", "English", "Ðone sunu is accusative singular and the actor of the perception infinitive gān.", "Accusative actor belongs to the gesēon plus infinitive frame.", "Equivalent precise syntactic terminology is accepted."),
         ("Sentence 2 actor", "English", "Se sunu is nominative singular, the subject of finite ēode inside the ðæt clause.", "The internal subject keeps nominative case.", "Equivalent precise syntactic terminology is accepted."),
         ("Verb-form comparison", "English", "Gān is a plain infinitive. Ēode is a third-singular preterite finite form; its indicative and subjunctive spellings coincide, so spelling alone cannot choose between them.", "Finite versus nonfinite is clear; indicative versus subjunctive is not uniquely recoverable from ēode's surface.", "A contextual report-subjunctive analysis or factual-indicative analysis is defensible if its evidence limit is acknowledged."),
     ], ["u09-perception-infinitive", "u09-content-that", "u09-reported-statement", "u13-clause-role-parsing"])

task("A03", "temporal_analysis",
     "Translate each report. For each, identify and parse every finite verb, identify any participle or infinitive (or state that there is none), and explain what the construction and context show about the time of the reported situation. In sentence 1 the king is there at the time of saying; in sentence 2 the ship-making is complete; in sentence 3 the singing is intended but has not yet occurred. Your explanation must connect these contexts with the actual verb groups and explain why automatic English backshift is insufficient; merely repeating the time hint is not an answer.",
     ["Hē sægde ðæt se cyning ðǣr wǣre.", "Hē sægde ðæt se cyning ðæt scip geworht hæfde.", "Hē sægde ðæt se cyning singan wolde."], [
         ("Sentence 1 translation", "English", "He said that the king was there.", "The king's presence is simultaneous with the past reporting viewpoint.", "Equivalent past report preserving simultaneous presence."),
         ("Sentence 1 finite forms", "English", "Sægde is third-singular preterite indicative of sęcgan; wǣre is third-singular preterite subjunctive of wesan in the reported clause.", "Distinguish the reporting finite verb from the reported finite verb; wǣre is not a past participle.", "Equivalent complete parsing; the homographic second-singular indicative wǣre is excluded by se cyning."),
         ("Sentence 1 nonfinite forms", "English", "There is no nonfinite verb in this sentence.", "Both verb forms are finite.", "None is sufficient when finite forms have been correctly identified."),
         ("Sentence 1 construction and time", "English", "The finite ðæt report contains preterite subjunctive wǣre. The stated context makes the king's presence simultaneous with the past saying; past mood/tense morphology does not force a prior completed event.", "Tie relative simultaneity to the actual finite report and supplied viewpoint, rather than mechanically translating every past form as earlier than the report.", "Equivalent explanation tied to the stated context."),
         ("Sentence 2 translation", "English", "He said that the king had made the ship.", "The ship-making precedes the saying and is complete at that viewpoint.", "Equivalent explicit anterior translation."),
         ("Sentence 2 finite forms", "English", "Sægde is third-singular preterite indicative. Hæfde is the third-singular preterite finite auxiliary of the content clause, selected here as report subjunctive; the indicative surface is identical.", "Finite auxiliary and reporting verb are distinct; do not call geworht finite.", "A contextual indicative report is defensible if the identical surface and factual choice are explained."),
         ("Sentence 2 nonfinite form", "English", "Geworht is the uninflected past participial base of gewyrcean; it combines with hæfde and the accusative patient ðæt scip.", "Prior Unit12 transitive habban compound, not an automatic passive.", "Equivalent complete participle identification."),
         ("Sentence 2 construction and time", "English", "The transitive habban-plus-participle group presents the making as complete at the past reporting viewpoint. The action is therefore anterior; this follows from the complete verb group and context, not from English backshift alone.", "Identify the construction that licenses the anterior interpretation.", "Equivalent explanation preserving completed action and past viewpoint."),
         ("Sentence 3 translation", "English", "He said that the king intended to sing.", "The report presents the king's intention; it does not assert completed singing.", "Would sing is acceptable when understood as intended later action, not a guarantee of fulfillment."),
         ("Sentence 3 finite forms", "English", "Sægde is third-singular preterite indicative. Wolde is the third-singular preterite finite volitional verb, selected here as report subjunctive; the indicative has the same surface.", "The past form wolde is finite and does not itself assert that singing occurred.", "A contextual factual indicative report is defensible with the syncretism explained."),
         ("Sentence 3 nonfinite form", "English", "Singan is a plain infinitive complement of wolde.", "The infinitive supplies the intended action, with the king as its understood actor.", "Equivalent identification."),
         ("Sentence 3 construction and time", "English", "Willan with a plain infinitive presents volition or intention. The supplied context places the intended singing after the saying, but neither the construction nor English would guarantees fulfillment.", "Connect the intended-later reading to willan plus infinitive, rather than imposing an automatic future auxiliary meaning.", "Equivalent explanation retaining volition and noncompletion."),
     ], ["u09-content-that", "u09-reported-statement", "u12-reported-sequence", "u12-habban-perfect"])

task("C01", "controlled_composition",
     "Translate the complete exchange. Use sęcgan for the reporting verb and sęllan for give: The king said to his son, 'Give me the book.' The son gave him the book. Then identify the referents of the first-person and third-person recipient pronouns in your translation.",
     [], [
         ("Speech and command", "Old English", "Se cyning sægde his suna: ‘Sęle mē ðā bōc.’", "The king tells his son to give the book to the king, using a singular command.", "Tō plus a properly governed recipient with an independently taught saying frame is grammatically possible, but the selected model uses the prior dative sęcgan recipient."),
         ("Executed action", "Old English", "Se sunu sealde him ðā bōc.", "The son gives the book to the king in the narrator's past account.", "Se cyning as an explicit dative recipient is not correctly inflected; ðǣm cyninge is a valid unambiguous noun alternative, but the pronoun-analysis target still needs a recipient pronoun."),
         ("Recipient reference", "English", "Quoted mē and narrative him both denote the king; their persons differ because the speech and narration have different viewpoints.", "Same recipient across the quotation boundary; first-person quoted speaker becomes third-person narrative referent.", "Equivalent explanation naming the two viewpoints."),
     ], ["u02-direct-quotation", "u09-dative-speaking-recipient", "u02-giving-recipient", "u13-quoted-reference"])

task("C02", "controlled_composition",
     "Translate these three statements separately. Use cunnan in the first two and witan in the third; then explain the complement selected in each: I know that man. I know how to sing. I know that he is here.",
     [], [
         ("Statement 1", "Old English", "Ic cann ðone mann.", "Acquaintance with the specified man, not learned ability.", "Other evidenced knowing vocabulary may be grammatical but does not meet the stated cunnan target."),
         ("Statement 2", "Old English", "Ic cann singan.", "Learned ability to sing.", "Equivalent person-one present cunnan plus the taught plain infinitive."),
         ("Statement 3", "Old English", "Ic wāt ðæt hē hēr is.", "Knowledge of the stated fact that he is here.", "A contextually justified subjunctive sīe is grammatical; the factual-indicative model does not exclude contextual alternatives."),
         ("Complement comparison", "English", "Cunnan has an accusative person in statement 1 and a plain infinitive in statement 2. Witan has a finite ðæt content clause in statement 3.", "The first cunnan sense is newly taught acquaintance; familiar skill morphology did not already establish it.", "Equivalent precise grammatical description."),
     ], ["u06-modal-cunnan", "u09-content-that", "u16-cunnan-person"], ["This is a bounded contrast of the selected complements, not an exclusive cunnan-for-persons/witan-for-facts rule. Cook35.7 explicitly uses witan with a person. The new cunnan-u16-acquaintance sense must be present in the reconciled grammar inventory before this task closes."])

task("C03", "controlled_composition",
     "Translate both clauses, using plegian for the first two expressed actions and dōn for the final repeated action: The men played well; the king played better than they did. Explain what the last verb replaces and why it is plural.",
     [], [
         ("Whole comparison", "Old English", "Ðā męnn plegodon wel; se cyning plegode bęt ðonne hīe dydon.", "The king's play is better than the men's; dydon recovers their playing, with plural subject agreement.", "A grammatical comparison repeating plegodon is valid language but misses the explicit substitute-dōn target. Exact selected plegian spelling follows the grammar packet."),
         ("Recovered action and agreement", "English", "Dydon stands for played and agrees with hīe, referring to the men.", "The comparison does not introduce a different action or give dōn the king as subject.", "Equivalent explanation."),
     ], ["u13-coordination-predicate-recovery", "u16-don-substitute", "u16-adverbial-action-comparison"], ["The new absolute-plegian and substitute-dōn frames and the comparative clause feature must be bound before closure."])

reading = "FB-XII-APOLLONIUS-GYMNASIUM"

task("R01", "whole_reading_translation",
     "Translate the whole gymnasium scene, from Æfter ðisum wordum through tō his gereorde. Keep the local help and original notes available. Preserve the changes of speaker, the complete action sequence and the places where the edition acknowledges uncertainty.",
     [{"source_span_id": reading, "scope": "complete"}], [
         ("Whole translation", "English", "A complete independently prepared translation of all five source paragraphs is required; the source-first translation witness and the exact source govern the eventual model.", "Arrival and announcement; bath and game; recognition and service; departure and inquiry; identification and invitation. No clause or direct utterance may be silently omitted.", "Accept defensible lexical and syntactic alternatives, especially the explicitly supported ambiguities at169.5–7,169.11–13 and170.15–16. Do not substitute the Latin for the actual Old English."),
     ], [], ["This output is a full translation, not a paraphrase of the narrative summary. The private whole-translation model must be reconciled against the actual source before authoring."])

task("R02", "reading_discourse_analysis",
     "Explain the sequence and grounds of the encounter in five brief answers, citing the relevant words or source lines: what brings Apollonius into the bath; what attracts the king's notice during the game; what the king says about the young man; what the messenger infers and from what evidence; and what the king finally orders.",
     [{"source_span_id": reading, "scope": "complete"}], [
         ("Entry into the bath", "English", "He hears the public announcement that the bath is open, removes the half cloak and enters.", "Announcement and action linked; earlier fisherman context remains outside this passage.", "Equivalent source-grounded account at168.8–12."),
         ("The game", "English", "Apollonius catches and returns the ball quickly and does not let it fall; the king recognizes his skill.", "Skill motivates recognition; do not invent a contest result.", "Equivalent account anchored168.18–169.7."),
         ("The king's statement", "English", "He dismisses his companions and calls the young man his equal, with the qualifying expression ðæs-ðe mē ðyncð.", "Direct statement of equality; do not force the preceding unclear knowledge clause into certainty.", "As it seems to me/as I think for the qualifying expression."),
         ("The messenger's conclusion", "English", "He identifies Apollonius as shipwrecked from his poor clothing, even if Apollonius himself keeps silent.", "The evidence is the garment, not a narrated confession.", "Equivalent account anchored170.8–14."),
         ("Final order", "English", "The king orders the man to go quickly and tell Apollonius that the king invites or asks him to come to his meal.", "Messenger, invitee and royal meal are distinct participants; arrival at the feast is outside the assignment.", "Equivalent rendering retaining the source's speech-level shifts."),
     ])

task("R03", "reading_reference_analysis",
     "Identify the referent and grammatical role of each selected pronoun. Use the local context and original notes; distinguish a contextual interpretation from what its ending alone proves.",
     [{"source_span_id": reading, "anchors": ["169.4 hine after slōh", "169.14 him after hē", "169.15 hē immediately before hine lǣdde", "169.15 hine before lǣdde", "169.16 him before ðā siððan", "170.9 hē after ðæt"]}], [
         ("169.4 hine", "English", "The ball: masculine accusative singular, the object understood with letting it fall.", "An inanimate masculine noun permits hine; original169note3 identifies the ball.", "Explain the causative/perception-type actor relation to feallan if using narrower syntactic terminology."),
         ("169.14 him", "English", "The king, dative person served by Apollonius.", "Do not take the nearest hē as necessarily its referent.", "Equivalent dative-beneficiary/recipient-of-service terminology."),
         ("169.15 hē before hine", "English", "Apollonius, nominative singular actor of lǣdde; original note14 identifies him.", "Apollonius leads the king.", "Equivalent statement tied to the printed note."),
         ("169.15 hine", "English", "The king Arcestrates, accusative singular person led; original note15 identifies him.", "The two adjacent masculine singular pronouns have different referents.", "Equivalent statement."),
         ("169.16 him", "English", "Apollonius, dative reflexive with his turning away; it is not another person to whom he gives something.", "The narrator returns to Apollonius's departure.", "Equivalent bounded reflexive analysis supported by note16 and its grammatical reference."),
         ("170.9 hē", "English", "Apollonius, nominative subject inside ðæt hē wæs ...; the preceding observer is the messenger.", "Different subjects across the clause boundary; original170note8 identifies Apollonius.", "Equivalent clear participant account."),
     ])

task("R04", "reading_clause_analysis",
     "For each passage give its relation to the surrounding clause, identify its finite verb or finite verb group, and state the form's mood with the help provided. Treat the source-specific constructions within their stated limits.",
     [{"source_span_id": reading, "anchors": ["168.1–2 ðe him getǣht wæs", "168.2 ōð-ðæt hē becōm", "168.3 hwone hē biddan meahte", "169.9 ðæt se cyning hine hęrede", "170.6 hwæt se geonga mann sīe", "170.13 Ðēah hē hit self forswīge"]}], [
         ("168.1–2 relation", "English", "A relative clause modifying weg, the path that had been shown to Apollonius.", "Relative reference, not a new independent event.", "Which was shown to him is also a defensible temporal rendering."),
         ("168.1–2 finite group", "English", "Getǣht wæs, with finite wæs; a supported passive group.", "Wæs is preterite indicative third singular; getǣht is nonfinite.", "Equivalent finite-versus-participle identification."),
         ("168.2 relation", "English", "Temporal endpoint: until he came to the city gate.", "The coming ends the preceding journey.", "Equivalent temporal account."),
         ("168.2 finite form", "English", "Becōm, preterite indicative third singular.", "Actual source indicative, not an automatic until-subjunctive rule.", "Equivalent parsing."),
         ("168.3 relation", "English", "Dependent question: whom he might ask for support of life.", "Hwone belongs inside the question as the requested person's accusative form.", "Equivalent indirect-question description."),
         ("168.3 finite group", "English", "Meahte is the finite preterite modal; biddan is a plain infinitive. The exact modal spelling is locally supported and is syncretic between singular indicative and subjunctive.", "Do not identify biddan as finite or force mood from meahte alone.", "A contextually justified subordinate/modal analysis is accepted with the syncretism stated."),
         ("169.9 relation", "English", "Content heard by Apollonius: that the king praised him.", "The inner ðæt clause supplies what he heard, inside the temporal clause.", "Equivalent nesting description."),
         ("169.9 finite form", "English", "Hęrede is third-singular preterite of praise; the selected context is factual praise, with indicative/subjunctive surface syncretism acknowledged.", "He heard actual praise; no independent hęrian system is inferred from local support.", "Equivalent precise form analysis preserving the evidence limit."),
         ("170.6 relation", "English", "Dependent question after the order to find out: what or what kind of person the young man is.", "Identity/status question; do not mechanically replace hwæt by hwā.", "Who he is is acceptable idiomatic translation if the form and originalnote7 distinction are explained."),
         ("170.6 finite form", "English", "Sīe, present subjunctive third singular of wesan.", "Distinct subjunctive form inside the question.", "Equivalent parsing."),
         ("170.13 relation", "English", "Concession: even if he himself keeps it silent, his clothing reveals him.", "Silence does not prevent the evidence of clothing.", "Although he conceals it is defensible if contextual openness is acknowledged."),
         ("170.13 finite form", "English", "Forswīge, present subjunctive third singular, with the complete local support supplied.", "Do not claim an independently taught complete forswīgan system from this token.", "Equivalent parsing."),
     ], [], ["Final source/grammar support must corroborate each contextual parsing; uncertain modal and weak-preterite moods are explicitly not graded as uniquely distinguishable by spelling."])

task("R05", "reading_speech_analysis",
     "Analyse the final invitation at170.14–16. Identify the outer speaker, his immediate addressee, the person denoted by him, the person denoted by se cyning, and the person denoted by ðē and ðū. Then explain why the original note describes a mixture of direct and indirect construction. Preserve the actual wording while explaining it.",
     [{"source_span_id": reading, "anchors": ["170.14–16"]}], [
         ("Outer speaker", "English", "King Arcestrates.", "The king gives the order.", "The king."),
         ("Immediate addressee", "English", "The messenger or servant who has returned from Apollonius.", "Gā and sęge are directed to this man.", "The king's man or attendant."),
         ("Him", "English", "Apollonius, the person to whom the message is to be delivered.", "Dative recipient of tell.", "The young man."),
         ("Se cyning", "English", "Arcestrates, named in the message in the third person.", "The message refers to its royal sender.", "The king who is speaking outside the message."),
         ("Ðē and ðū", "English", "Apollonius, addressed within the message as its recipient and the subject of cume.", "Second person belongs to the future delivery of the message, not the immediate servant.", "The intended invitee."),
         ("Construction", "English", "After sęge him ðæt the source shifts to the message as addressed to Apollonius: se cyning bitt ðē ðæt ðū cume. The introductory reporting construction and the direct-address pronouns are combined, as originalnote15 states.", "Keep the exact source and acknowledge the change of speech level; do not silently regularize all pronouns.", "Equivalent explanation of the mixed construction without declaring every such source report a universal rule."),
     ])

task("R06", "reading_evidence_limits",
     "Consult printed page169, original notes6 and10 (not text lines6 and10), together with the modern help explaining their Latin parallels in English. For each location, give a defensible translation of the actual Old English and explain the limit the note places on a confident interpretation. No knowledge or translation of Latin is required; do not replace the Old English with the Latin account.",
     [{"source_span_id": reading, "anchors": ["169.5–7", "169.11–13"], "original_notes": ["FB-U16-169-N6", "FB-U16-169-N10"]}], [
         ("169.5–7 translation", "English", "The king then recognized the young man's skill, so that he knew that he had no equal in the game.", "Preserve the repeated he/his structure and the actual negative without claiming that all referents are certain.", "A defensible reading in which the last he refers to Apollonius or the king is acceptable with an explicit explanation; the following direct statement of equality must not be suppressed."),
         ("169.5–7 limit", "English", "Cook calls the clause unclear and supplies a Latin account. The surface alone does not uniquely settle both he referents or the exact relation of the clauses.", "Do not certify one antecedent solely from the nearest noun or substitute the Latin for the OE.", "Equivalent source-sensitive explanation."),
         ("169.11–13 translation", "English", "With a skilled hand he swung the top or ball so swiftly that the king felt as if he had been changed from old age to youth.", "Translate OE swang ðone top and the resulting impression while preserving the local lexical uncertainty.", "A carefully justified sense of top supported by the printed note is acceptable; silently replacing the Old English action by the Latin rubbing action is not."),
         ("169.11–13 limit", "English", "Cook says that the Old English departs from a Latin account of rubbing or anointing the king with ointment and suggests top may mean the same as the ball word. This is a textual and lexical difficulty; the Latin contains no shoulder noun and does not establish that the printed Old English expresses the same action.", "Keep translation, interpretation and comparison text separate; the relevant Latin meaning is supplied in English.", "Equivalent account that acknowledges the note's tentative wording."),
     ])

for item in tasks:
    if item["task_id"].startswith("NEW-U16-R"):
        item["source_span_id"] = reading
        item["mode"] = "supported_reading"
        item["assessment_boundary"] = "The exact source, all original notes and all modern help remain visible; no supplied dependency becomes an unaided-recall target."

examples = [
    {"example_id": "NEW-U16-EXAMPLE-01", "text": "Se fæder sægde: ‘Ic eom hēr.’ Se fæder sægde ðæt hē ðǣr wǣre.", "translation": "The father said, 'I am here.' The father said that he was there.", "pedagogical_purpose": "The same speaker becomes third person in a report; here/there assumes that the reporter is speaking from another place.", "feature_ids": ["u02-direct-quotation", "u09-content-that", "u09-reported-statement", "u09-report-reference", "u13-quoted-reference"]},
    {"example_id": "NEW-U16-EXAMPLE-02", "text": "Hē geseah ðone mann cuman. Hē wiste ðæt se mann cōme.", "translation": "He saw the man come. He knew that the man came.", "pedagogical_purpose": "The perceived actor is accusative with an infinitive; the finite content-clause subject is nominative. The second sentence uses the reported subjunctive.", "feature_ids": ["u09-perception-infinitive", "u09-content-that", "u09-reported-statement"]},
    {"example_id": "NEW-U16-EXAMPLE-03", "text": "Gē cunnon ðone cyning; gē cunnon singan.", "translation": "You know the king; you know how to sing.", "pedagogical_purpose": "The new personal-acquaintance sense takes a person as object; the prior skill sense takes a plain infinitive. Witan can also take a person, as Cook35.7 shows; this is not an exclusive lexical partition.", "feature_ids": ["u06-modal-cunnan", "u16-cunnan-person"]},
    {"example_id": "NEW-U16-EXAMPLE-04", "text": "Hē plegode wel, and hīe dydon swā.", "translation": "He played well, and they did so.", "pedagogical_purpose": "Dōn recovers the preceding playing action while retaining its own subject and number.", "feature_ids": ["u13-coordination-predicate-recovery", "u16-don-substitute"], "pending_feature": "plegian ordinary use"},
]
for item in examples:
    item.update({"origin": "new_teaching_material", "graded": False, "status": "pending_exact_binding_and_independent_reconciliation", "display_obligation": "Print the complete Old English, translation and bounded point after the relevant forms, senses and frames have been made available."})

save("task-seed.json", {"schema_version": 1, "chapter": "ch16", "status": "provisional_analysis_not_contract", "tasks": tasks, "pending_form_task_groups": ["F01 distinctive strong/contracted indicative positions", "F02 weak-system and prior-command/new-indicative contrasts", "F03 six new complete command pairs", "F04 findan/fēdan present-subjunctive singular/plural"], "cook_assignment": "All59 unchanged source prompts will be merged once stable models and source dependencies are reconciled."})
witness_path = DEST / "author-only-reading-translation-witness.json"
if witness_path.exists():
    witness = json.loads(witness_path.read_text(encoding="utf-8"))
    reading_task = next(t for t in private if t["task_id"] == "NEW-U16-R01")
    reading_task["outputs"][0]["model"] = "\n\n".join(witness["paragraphs"])
    reading_task["outputs"][0]["translation_witness"] = "curriculum/proposals/unit16/author-only-reading-translation-witness.json"
save("author-only-model-seed.json", {"schema_version": 1, "chapter": "ch16", "visibility": "author_only", "status": "provisional_analysis_not_key", "tasks": private})
save("composition-seed.json", {"schema_version": 1, "chapter": "ch16", "status": "provisional_analysis_not_contract", "teaching_examples": examples, "new_reading": None})
print(json.dumps({"tasks": len(tasks), "outputs": sum(len(t["output_positions"]) for t in tasks), "examples": len(examples)}, ensure_ascii=False))
