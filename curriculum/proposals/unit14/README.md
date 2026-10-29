# Unit 14 design handoff

The proposal is ready for coordinator reconciliation into the learning contract. It is analysis and task design, not a drafted learner chapter or a completed chapter. The coordinator must save the contract before authoring the lesson and key.

All 21 original Cook VIII.26–27 prompts are retained with their original identifiers and wording. There are 23 new tasks: six morphology tasks, six word-family or structural analyses, four short compositions and seven reading tasks. The complete opening argument of *The Dangers of Greatness* supplies the connected reading: 159 words, printed 156.1–158.4, one-based PDF 172–174. Its 24 original notes and 25 anchors remain recorded separately from the linguistic text. Four short teaching examples are new composition; there is no second reading.

The 38 literal paradigm tables contain 324 cells: 18 nominal systems with 144 cells, and 20 verbal systems with 180 cells. The verbal scope is nine indicative systems, five subjunctive systems, four participle-base pairs and two imperative pairs. Every cell has an exact surface and display route. Nominal cells have 116 productive and 28 reference assignments. Tables must display the reference limits and the diagnostic stems, principal parts, ending rules and exceptions. Displaying a form does not teach every possible use of it.

## Authoring inputs

- `design-outline.md` and `outcomes.json` explain the bounded scope and sequence.
- `inventory.json` reconciles source and grammar records with the actual prior registers. Its 113 current lemma entries include additions to existing lexemes and supplied records; the count is not a productive-vocabulary total. It includes the teaching records, 1,571-entry evidence catalog, source passage, exact support, prior requirements, formation evidence, identity reconciliation and morphology plan.
- `task-plan.json` specifies all 44 tasks, stable key IDs, visible inputs/support, required/tested/supplied dependencies and 156 requested output positions. There are 74 individually identified morphology outputs. The final task IDs govern assignment.
- `display-matrices.json`, `nominal-display-plan.json` and `grammar-display-plan.json` provide all literal cells and diagnostic rules. The empty `lexical_diagnostics` field means there are no shared-model stem reconstruction routes; `lexical_scope_summary` is descriptive.
- `compositions.json` and `public-sequence-bindings.json` bind the four new teaching examples and other new learner inputs to exact forms and senses.
- `cook-targets.json` records every original item's intended target, defensible alternatives and likely errors.
- `prior-audit.json` records the examination of all thirteen earlier active contracts and the actual cumulative registers at baseline `c2cb7d6`.

`task-seed.json` and `composition-seed.json` preserve the human-readable design inputs; the assembled inventory, task plan and exact display matrices are the final integration interfaces. Ignored `build/u14-design-*` files are reproducible helper scripts, not learner material.

## Private models and reviewer boundary

All files in this proposal directory are excluded from the initial independent learner-solving review, including files whose names look public. The reviewer may use the actual learner chapter, accepted prior learner material/registers, and necessary original primary page images. They must freeze all solutions before seeing the current contract, brief, audits, proposals, annotated source/token maps, key or private models.

- `author-only-model-seed.json` gives ordered models and explanations for all 23 original tasks, with exact morphology outputs and output positions.
- `author-only-sequence-bindings.json` binds the four new composition models.
- `author-only-cook-sequence-bindings.json` binds all 21 source-editor Cook models, comprising 273 tokens. The independent initial source witness remains in the source audit.
- `author-only-source-translation-witness.json` preserves the design analyst's independent initial rendering of the actual primary pages.
- `author-only-witness-reconciliation.json` records the later lexical correction and the final six-unit rendering. The source editor's independently prepared final reader model is `sources/audits/unit14-source/author-only-reading-model.json`.

The final key needs one entry per task, its requested target, essential meaning, explanation, useful error diagnoses and defensible alternatives. A valid Old English alternative may still fail a stated Cook vocabulary or final-verb control. The proposed models do not replace that editorial work.

## Reconciled details to preserve

Use the primary-image quantities **dūst** and **gōdwębb**. Treat wound as the feminine noun and retain the original erroneous §43 hint with a visible correction to the noun's proper declension reference. Translate source **līegum** as thunderbolts/lightning, following Cook printed 303 / PDF 319; the initial translation witnesses remain unchanged and their corrections are separately documented.

The noun **gōd** goods/possessions is distinct from adjective **gōd**. A06 contrasts that lexical noun with the prior article-plus-weak **rihtwīs** personal expression, specifically licensed by `u11-articled-righteous-persons`. C04 uses the actual prior recipient and command frames `u12-sendan-recipient` and `u12-sendan-imperative`. Keep the existing **forlǣtan** paradigm and teach only the newly bounded leave-peace-to frame; do not introduce a redundant **lǣfan** system.

Cook 26.7 and 27.2 select a final finite auxiliary; 27.10 selects a final finite verb inside the concessive clause. Preserve the bare relative-particle targets and the original participant, number and reference controls. Actual prior forms such as **cymð**, **birð**, **wierð**, **fēoll**, **yfele** and **gatum** retain their recorded identities. Selected 26.10 uses **ne wæs**; 27.9 uses the prior **hālsian** request frame.

The sealed family audit's EALDORDOM row still names preliminary task S06. The final assignment is S05, which explicitly requires the -dōm family analysis and the genitive relationship. Inventory records this reconciliation without altering the sealed evidence. S06 instead compares the repeated conclusions.

All 20 Cook help groups and 34 reading help groups must remain visible with their assigned tasks. Previously supplied citation forms remain supplied; explicit support teaching records bind the reused leornian, sōð, swīð, berstan, tōberstan, weorðan and forweorðan citations without promoting them. General negation and quantity remain later scope. Analysis of an attested family does not authorize arbitrary coinage or an unrecorded meaning.

## Validation and handoff

`validation.json` and `validation-extra.json` both pass with no issues. They cover exact original prompts, every required input/output identity, visible help for supplied requirements, exclusion of supplied material from independent testing, all 324 literal routes, source text/apparatus parity, preservation of prior identities, resolved evidence references and Unicode normalization. Source and grammar packets also report passing validations. These are dependency and evidence checks; the independent learner-solving, paradigm, source, editorial and exported-page reviews remain coordinator work.

`manifest.json` records the final proposal files and source input hashes. `file-boundaries.json` records ownership and the initial review exclusion. No shared contract, register, index, Beads state, Git state, prior chapter was modified by this design worker. Recommend accepting this proposal and closing `oec-u14-design` after coordinator acceptance; do not mark Unit 14 complete on this basis.
