# Course records

The completed eighteen-unit course records teaching in its active coverage contracts and cumulative grammar and lexical registers.

## IDs and source assignment

Use active chapter IDs `ch01`, `ch02`, etc. Keep Cook IDs independent of the new chapter: `EX-I-02-07` always means Group I, Exercise 2, item 7. Keep reused source IDs stable. New tasks use IDs such as `ch01-prep-01`; examples and reading segments also have stable IDs. Lemma, sense, form, and grammar-feature IDs should survive changes in display spelling.

`curriculum/COOK_MAP.md` indexes the course allocation. Source inventories locate checked evidence. The assigned/deferred/excluded arrays across active `chapters/chNN/coverage.json` files form the canonical assignment crosswalk. A later assignment resolves an earlier active deferral without deleting its history.

## Learning contracts

Prepare `chapters/chNN/coverage.json` before prose using the template. Read all earlier active contracts. Record outcomes, the full paradigm scope, basic syntactic uses, original source items, added tasks/examples, reading spans, and every required sense/form/construction. Link each task to its requirements and key entry. Record precise source locators and all normalizations or adaptations.

Knowledge statuses are `previously_taught`, `new_production`, `new_recognition`, `supplied`, and `unresolved`. A full paradigm must have checked forms and an explicit teaching scope. It does not automatically teach every construction using those forms. Independent production requires productive knowledge; supplied support must be local and must not be tested for independent recall.

## Grammar and lexicon

Each grammar feature needs a stable ID, exact description, prerequisites, nullable recognition/production milestones, supplied-exposure chapters, evidence, and unresolved notes. Use precise features rather than a single milestone for an entire category such as verbs.

Each lemma needs headword, part of speech, senses, source spellings, aliases, evidence, and relevant gender/declension or verb-class information. Each sense and inflected form needs its own ID, analysis/evidence, and teaching milestones. Register actual paradigmatic forms; the same spelling in different cells may need distinct form records. Unknown values stay null with a tracked issue until resolved.

Only the coordinator merges registers after review. Workers submit proposed changes in their assigned files. Preserve earlier active milestones when adding new forms or uses. Source evidence supports linguistic claims; only the active contracts and reviewed registers establish teaching milestones.

## Review and work tracking

Beads records tasks, owners, blockers, and acceptance criteria. Chapter contracts record pedagogical coverage. Source records establish evidence. A closed issue is not proof of attestation or mastery.

Before handoff check unique IDs, valid references, complete source assignment, matching student/key numbering, supported paradigms, production prerequisites, UTF-8/NFC, and rendered pages. Automated checks do not certify idiom or linguistic correctness. Add reusable checking scripts only when a repeated concrete need emerges.
