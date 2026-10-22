# Editorial policy

Version 0.6: compact grammar-textbook style and one lesson per complete numbered exercise agreed on 22 October 2026, following the audience, vocabulary, correction, citation, and complete-PDF decisions of 21 October. Other working defaults remain provisional.

## Audience and teaching purpose

Assume an adult studying independently with no prior Old English but familiarity with standard grammar terminology. Explain how grammatical categories operate in Old English and introduce language-specific distinctions; elementary definitions of standard terms need not interrupt the lesson. The user's own Old English and language-learning experience is not a prerequisite for other readers. Keep the assigned work self-contained. A general terminology appendix may be added later.

Use a terse grammar-textbook presentation, following the user's preference for the economy of Thackston and Lambdin: compact rules, paradigms, vocabulary, examples, and exercises. Omit motivational framing, study coaching, repeated instructions, and explanations of standard terminology. State each rule once; retain every form and explanation actually needed to complete the tasks. Self-contained does not require discursive exposition.

Maintain two goals: reading Old English and producing controlled Old English in Cook's composition exercises. These require separate milestones.

Keep lessons one-to-one with Cook's numbered exercises, in source order: one complete exercise, including all its items, per lesson. A thematic source group may contain several lessons. The dependency audit determines the grammar and vocabulary that must precede that exercise; it does not split the exercise into smaller lessons. Select or shorten the accompanying reader extract to keep it manageable. Preserve the full crosswalk and record unresolved source problems rather than silently omitting an exercise item.

## Editions and textual layers

Use the two sources in `sources/registry.json`. Their dates match, but every individual page and section reference must still be checked.

Store a faithful transcription of the chosen printed edition. This is a transcription of Cook's edited text, not a manuscript transcription. In the learner text, any departure from that transcription must be traceable.

Keep exposition focused on the language. Place source citations, textual provenance, and editorial corrections in footnotes or endnotes tied to the relevant section, rather than repeatedly naming Cook in explanations or adding source columns to the learning tables. Preserve full item-level evidence in coverage and editorial records. Use ordinary exercise numbers for readers; retain stable internal IDs in source comments and the crosswalk. Newly prepared material must remain identified in the section notes.

The user authorizes corrections where contemporary linguistic understanding establishes that Cook is in error. Preserve the original in the source transcription; give the learner the supported correction and a concise editorial note. In the chapter's editorial record, identify the exact original, the replacement or revised analysis, the evidence, and the affected items. Distinguish a demonstrated error from a valid variant or a change of editorial convention. A correction must not be based solely on an agent's memory or on a different dictionary's preferred form. Record the appropriate origin category and any consequent coverage/key changes.

Cook describes the prose normalization to an Early West Saxon basis in *First Book*, preface vii; he excepts poetry. That is the initial prose baseline for this project. See the primary source listed in the registry. Do not describe the whole reader as uniformly normalized.

## Typography and spelling

- Use UTF-8 and Unicode NFC in working text.
- Preserve printed thorn, eth, ash, spelling, and vowel marks in the source transcription.
- Preserve linguistic distinctions when removing line-wrap artifacts.
- Use modern page layout without silently modernizing the language.
- Resolve difficult type from page images; log uncertain readings.
- Do not add speculative vowel marks or pronunciation markings.
- Search aliases can omit marks, but must not alter displayed text.
- If a consistent learner-facing spelling policy is later adopted, document its mapping and exceptions before applying it across chapters.

## Typesetting direction

LuaLaTeX is the provisional choice for the print/PDF edition. Retain Markdown as the editable chapter text and deliver a complete chapter PDF and a separate complete answer-key PDF. Include all vocabulary, all assigned tasks, the reading and its support, and section endnotes; a selected-page specimen does not satisfy the chapter deliverable. Test the actual letters and vowel marks in the selected font, including italic and bold where used, and inspect every rendered page. Font and trim size remain provisional. General-purpose conversion or publishing automation should wait for a repeated editorial need.

## New vocabulary

The user accepts roughly 30 new vocabulary items per lesson. This is a workload reference, not a quota or cap: include the vocabulary required by the lesson's complete source exercise, and do not assume untaught grammar. Distinguish the production list from additional supplied reading support.

The learner table should contain the headword, relevant sense, part of speech, grammatical information needed now, and required forms. Put source references in section notes and detailed records. For nouns, supply verified gender and a useful declension/form indication; for verbs, supply the forms actually needed in the chapter. Avoid dumping every paradigm into the initial word list.

The internal lexicon should be fuller: senses, attested/source spellings, analysis, form-level milestones, and references. A word that has only appeared in a gloss remains a supplied item until explicitly taught.

## Readings

Prefer an unchanged, manageable extract from the selected reader with planned support. Grade by lexical, morphological, syntactic, and task demands. A gloss should supply the actual help needed; a dictionary headword alone may not explain a difficult form or construction.

If adaptation is necessary, label it and record every linguistic change. An optional fuller source passage can follow a controlled adaptation. Do not imply an adaptation is an unmodified historical quotation.

The earliest chapters may use phrase recognition and short supported clauses while continuous passages become appropriate. Label fragments as fragments. Maintain the requested reading/translation section in every chapter; do not disguise an uncontrolled passage as beginner work.

## Assessment

Provide comprehension and selective parsing before full translation. Early instructions can be in modern English. For reading translations, separate a close explanatory rendering from fluent English when that clarifies the syntax.

Production keys identify the intended construction and allow defensible alternatives. State required vocabulary or constructions in the question if they are assessment criteria. Editorial assistance and model answers are newly prepared material unless a separately identified source supplies them.

Keep the key compact. Tables and numbered answers may share a statement of the target construction, grammatical explanation, variant guidance, and common errors. Retain a model and essential meaning for every task; repeat commentary only when an item needs a distinct explanation.

## Review and revisions

A second agent's agreement does not certify correctness. Use actual sources for doubtful morphology, meanings, and constructions. Record disagreements by item.

When an earlier lesson changes what is taught, inspect the downstream items that rely on it. Do not silently change prerequisites in later chapters. Keep each completed chapter as a recoverable Git revision.

