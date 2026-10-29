# Unit 15 design handoff

The proposal is ready for coordinator reconciliation into the learning contract. It is curriculum analysis and task design. The coordinator must save and checkpoint the contract before authoring the learner chapter and key.

All 50 exact Cook prompts are assigned: IX.28 (12), IX.29 (11), IX.30 (13), and joint X, XI.31 (14), printed 15–18 / one-based PDF 23–26. Their original IDs, English wording, hints and controls remain. There are 55 original tasks and 322 requested response positions across all 105 tasks, including 116 individually routed form outputs. The 55 original tasks comprise 9 morphology tasks, 12 analyses, 19 controlled compositions and 15 reading tasks. Eight short translated teaching examples have 50 exact token bindings. There is no added narrative.

The connected source reading is 415 whitespace words: the complete opening argument of Duties (103 words, printed 159 / PDF 175), the complete Preface (152 words, 162 / 178), and the complete Prayer (160 words, 163 / 179). All 27 original notes and 33 anchors are retained separately. Duties is the first argument within a longer outer speech. Its outer quotation continues on 160–161; any added closing mark in the Old English text requires an editorial declaration.

The 69 complete literal matrices contain 691 logical display positions: 675 actual form/expression cells and 16 explicitly unassigned number slots. There are 680 lexical component occurrences. Composite negative be-clauses retain separate ne and positive finite-form IDs. Unassigned plural hǣlu/hǣtu and singular Engle/Dęne positions have no invented lexical forms and make no claim of absolute historical defectiveness. Other abstract/mass/reference cells retain their particular limits. Every table must show its diagnostic stems, endings, stem changes, exceptions and productive/reference scope.

## Authoring interfaces

- `design-outline.md` and `outcomes.json` give the lesson sequence and scope. Group practice compactly; an output-position record is not a separate learner section.
- Present every prerequisite before its first example or exercise. In particular, teach the complete bōc table before the early book examples. The thematic practice stages presume that the grammar and vocabulary preparation is complete.
- `inventory.json` contains reconciled forms, senses, features, teaching records, complete paradigms, source readings and help, prior requirements, promotions, identity preservation and evidence. Its 198 lemma entries include additions to existing lexemes and supplied material; this is not a productive-vocabulary count.
- `task-plan.json` gives all 105 stable task/key IDs, exact prompts, requested outputs, visible help, and required/tested/supplied dependencies. `cook-targets.json` and `original-task-grading.json` distinguish linguistic validity from compliance with a stated target.
- `display-matrices.json`, `nominal-display-plan.json` and `grammar-display-plan.json` contain literal cells and rules. `output-display-routes.json` binds all 116 requested form answers to one exact display cell each. `system-practice-coverage.json` distinguishes complete-system practice from lexical transfer and lists unpractised cells explicitly.
- `public-sequence-bindings.json` binds every new analysis input; `compositions.json` binds the eight translated teaching examples. `reading-output-bindings.json` anchors all 64 reading response positions to exact source words, including every requested pronoun reference and form/mood/meaning triplet.
- `source-task-crosswalk.json` states all source assignments, the explicit Duties continuation boundary, and the disposition of every original note. Some current responses adapt original apparatus questions; the remaining historical questions stay source paratext, with no hidden extra responses.
- `prior-audit.json` records examination of all 14 active earlier contracts and the actual cumulative registers at 9129cda: 830 lemmas / 9,710 forms / 1,017 senses / 820 features.

`task-seed.json`, `author-only-model-seed.json` and the two initial translation witnesses preserve the earlier independent design work. They contain provisional choices and are not final authoring interfaces. `design-reconciliation.json` records later task and identity repairs. Ignored `build/u15-design-*` files are local reproducible helpers; the retained JSON interfaces carry the proposal.

## Private models and review boundary

All current proposal files are excluded from the initial independent learner-solving review, including files with public in their names. The reviewer may use the actual learner chapter with its visible help, accepted prior teaching/registers, and necessary clean original primary images. Freeze every solution before allowing access to the current contract, brief, audits, proposals, annotated token maps, key or private models. `file-boundaries.json` records this boundary.

- `author-only-output-models.json` provides one ordered model for every original response position, including complete translations and all requested explanations.
- `author-only-sequence-bindings.json` binds the 19 selected composition models. `author-only-cook-sequence-bindings.json` binds all 50 grammar-editor Cook models (603 tokens). `author-only-cook-binding-specifications.json` preserves the manually chosen contextual identities behind those bindings; the surface-candidate list is only a diagnostic aid.
- `author-only-source-translation-witness.json` and `author-only-cook-initial-witness.json` remain unchanged. `author-only-witness-reconciliation.json` and `author-only-cook-witness-reconciliation.json` record later corrections and selected models. The source editor's final reader model is explicitly reconciled, not a blind witness.

The eventual key needs each task’s model, essential meaning, target, explanation, defensible alternatives and useful error diagnoses. These private proposals do not replace the independent learner-solving and full paradigm/source reviews.

## Details that must survive integration

Preserve actual earlier form/sense IDs, including the source-origin IDs later promoted to complete production. Reuse `willan-refuse` for unwillingness; the new negative indicative forms and their construction are the extension. Keep the older supplied negative subjunctive nolde distinct. Reuse productive paired ge under `ge-conjunction`, and keep personal partitive uncer separate from agreeing possessive uncer.

For an existing record, the inventory preserves its prior form, analysis and gloss. Where a fuller contextual analysis or teaching gloss is needed, read `unit15_contextual_analysis` and `unit15_contextual_gloss` together with the new scope and status. Do not print a prior reference-only label as the current production scope, or replace a historical identity to make its label look cleaner.

The final source reads 30.12 If they can, so its condition uses ability. Item 30.6 resumes with he and hints micel; it does not demand the same. Fresh 600 dpi inspection confirms the original blōstmian hint in 30.11. The earlier n was an audit transcription error, not a source variant or an emendation of Cook. The initial witnesses retain their mistakes transparently.

In Duties, mann gedēð means one does; do not introduce poor people into that clause. Woruldlīf is worldly life. The Prayer reads gehīersumnesse (obedience), gestaðela and Sīe. Both mīnre sāwle sequences are genitives dependent on dative ðearfe. In the Preface's final appeal, the five specified pronouns refer to reader, Alfred, Alfred, reader, Alfred. Keep the worldly cares as constraints on the explanation.

C06 uses prior cume to practise internal nominative and explicit resumptive dative without forcing an additional leornian subjunctive system solely for the new task. Cook 31.12 retains the complete original learning prompt and its separately audited source support. A12 contrasts actual hēafd- with retained fōtsceamul-, using the complete displayed tables.

All 114 reader help groups and 35 Cook help groups must remain visible where assigned. Supplied material is not tested for independent recall. A complete table does not teach every possible construction or sense; a familiar headword does not establish a new form or use.

## Validation and handoff

All checks listed in `manifest.json` pass with no issues: all 50 exact prompts, each requested output and model, all literal display routes, source-word/apparatus parity, visible support, prior-identity preservation, resolved evidence and Unicode normalization. The proposal establishes a reviewable dependency contract. Unit 15 still requires independent solving, linguistic/editorial review, exported-page inspection, register/status integration and a recoverable local Git checkpoint.

Design edited only its exclusive proposal and helper files. Recommend accepting this proposal and closing oec-u15-design after coordinator acceptance; do not mark Unit 15 complete on this basis.
