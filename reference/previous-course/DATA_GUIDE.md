# Minimal records

The JSON files start empty intentionally. Populate them from the pilot's evidence; do not manufacture a full course before the pilot.

## Stable IDs

Use a chapter ID such as `ch01`. Keep source exercise IDs independent of chapter numbers: `EX-I-01-09` identifies original group I, Exercise 1, item 9 wherever it appears in the new course. Added tasks use IDs such as `ch01-prep-01` or `ch01-reading-01`.

Grammar feature and lemma IDs are durable keys. Do not use a changing display spelling as the only identifier.

## Grammar register

Each entry in `curriculum/grammar.json` needs:
- `feature_id`, precise description, and prerequisite feature IDs;
- `recognition_taught_in` and `production_taught_in`, independently nullable;
- source references with edition and grammar section/page;
- status and unresolved notes.

A broad label such as “verbs” is insufficient for a milestone. Record the particular forms or construction actually taught.

## Vocabulary register

Each entry in `lexicon/entries.json` needs:
- lemma ID, display headword, and part of speech;
- separately identified senses and references;
- relevant gender/declension or verb-class/principal-form information;
- source spellings and carefully distinguished lookup aliases;
- an array of needed inflected forms, with grammatical analysis and evidence;
- chapter milestones for each sense/form, distinguishing recognition, production, and supplied exposure.

Use null and an issue note for unknown information. An unknown field must be resolved before a task depends on it.

## Chapter coverage

Copy `templates/coverage.json` into `chapters/chNN/coverage.json`; this is the chapter's learning contract, prepared before prose. Use the object shapes in `templates/coverage.example.json`, which contains clearly marked placeholders and no linguistic claims. For every assigned task or reading segment record:
- item ID and origin category;
- source locator, or references supporting new composition;
- required lemma-sense-form combinations;
- grammar feature IDs;
- knowledge status and the lesson section or gloss providing coverage;
- key entry ID;
- review issues.

Allowed knowledge statuses: `previously_taught`, `new_production`, `new_recognition`, `supplied`, `unresolved`.

A reading segment may contain supplied material. An independent production target must have a production milestone. A supplied element in a scaffolded production task must be stated in that task and must not count as independent mastery.

Across chapters, the assigned, deferred, and excluded source-item arrays form the canonical source crosswalk. Account for every audited item. An assigned adaptation records its original item ID and changes. Deferred and excluded records need a reason; a proposed destination can remain null when not yet determined. An item deferred in an earlier chapter can later be assigned; the later assignment resolves that earlier deferral, without erasing the history.

## Checks to add after the pilot

Start with referential integrity: unique IDs, existing references, assigned tasks with keys, and unresolved dependencies. Then add spelling/Unicode checks and reports of unintroduced forms where reliable.

Do not claim that matching every token to a lemma proves grammatical or pedagogical correctness. Automated parsing suggestions need review, and legitimate variant spellings must not be rejected indiscriminately.

