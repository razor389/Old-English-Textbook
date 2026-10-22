# Project instructions: Cook Expanded

## Goal and scope

Create a carefully graded teaching edition based on Cook's *Exercises in Old English*, with grammar and new vocabulary before exercises and a reading/translation section from *A First Book in Old English* afterward. Each lesson corresponds to one complete numbered exercise in Cook, in source order, including all its items. Use terse grammar-textbook exposition. Complete one requested chapter at a time. The first task is the pilot in `pilot/BRIEF.md`.

Read `STATUS.md`, `EDITORIAL_POLICY.md`, `sources/registry.json`, and the chapter's learning contract before drafting. Treat empty cumulative registers as empty: never assume prior teaching that does not exist.

## Work in a staged editorial team

Use parallel agents for independent source inspection and dependency analysis when available. Keep drafting dependent on the resulting evidence.

- Source editor: verifies selected pages against scan images, transcribes source text, and records exact locators and doubts.
- Curriculum/linguistic analyst: inventories required words, senses, forms, and constructions; proposes a bounded learning contract.
- Lesson author: creates the learner-facing lesson and draft key within that contract.
- Independent reviewer: solves the student tasks before consulting the draft key where practical, then checks grammar, translation, source fidelity, and coverage.
- Coordinator: reconciles findings, owns shared registers, and produces the complete chapter.

An agent may perform more than one role sequentially. Source facts and linguistic claims require evidence; agreement among agents is not evidence of attestation. A reading-only reviewer should not modify the author's chapter. Give each writing agent an exclusive file or directory. Return proposed shared-register changes to the coordinator.

## Source handling

Use the selected edition and scan in the registry. Preserve original group/exercise/item identifiers. Lesson boundaries follow the numbered exercises, not the broader thematic groups; do not split an exercise across lessons to reduce its workload.

Keep source transcription, learner text, and change notes separate. OCR is a finding aid, never the final authority for Old English letters, vowel marks, or section numbers. Check the relevant page image. If an image is ambiguous, log the exact item and seek a second image or source.

For each reused item record: source ID, printed page, scan/PDF page convention, original identifier, and origin category. Use line locators only when actually verified; distinguish editorial line numbering from printed numbering.

Origin categories: exact source; declared normalization; adaptation of a specific passage; new teaching material. Do not describe generated Old English as quoted Cook text. Keep original English prompts alongside editorial clarifications.

## Grading and cumulative knowledge

Audit both exercises and readings before writing the lesson. Record the learning contract in `chapters/chNN/coverage.json` before prose. The item records across these files form the canonical source crosswalk: every audited original item is assigned (with its origin/adaptation status), deferred, or explicitly excluded with a reason. Read all earlier coverage files when choosing the next items.

For each word sense, required form, and construction assign one status:
- previously taught;
- taught now for production;
- taught now for recognition;
- supplied support;
- unresolved.

Core production tasks must be answerable with taught knowledge. A supplied form is allowed only in an explicitly scaffolded task, and the exercise must not simultaneously test independent recall of that form. Reading glosses may support out-of-scope material but must not silently promote it to learned status.

A familiar lemma is not evidence that every inflected form or sense is familiar. A short passage is not automatically a graded passage. If a requirement is unresolved, revise the teaching or supply appropriate support. A reader excerpt may be reduced or deferred with a recorded reason; a required item of the lesson's complete numbered exercise must not be omitted to shrink the chapter. Record any unresolved requirement honestly.

## Language and keys

Follow `EDITORIAL_POLICY.md`. Do not silently regularize unfamiliar spellings, infer missing vowel length, or convert the prose to a different dialect. Prefer attested examples. Any new composition requires checked vocabulary, morphology, syntax, and a clear new-material label.

Make independent translations from the Old English. A familiar Biblical or literary translation is not evidence for the exact wording of this edition.

Keys include model responses, target construction, explanation, essential meaning, representative acceptable alternatives, and useful error diagnoses. Distinguish grammatical validity from compliance with an exercise's stated target. Never reject a valid translation solely for differing from a model string.

## Finish the requested work

Resolve routine editorial choices using the policy and record them. Continue all unblocked work when one reading or analysis is uncertain. Ask the user only when a substantive choice would change the course's intended audience, fidelity, or scope and the available evidence cannot settle it.

A chapter cannot be marked reviewed while material errors remain unresolved. Return the complete chapter and key plus precise unresolved points when source evidence prevents completion. Do not conceal uncertainty with a confident reconstruction.

Before handoff:
- ensure all assigned source items and added tasks have coverage and key entries;
- compare student and key numbering;
- check sources, adaptations, and cumulative dependencies;
- inspect rendered special characters and tables if an export was requested;
- update status and registers without overwriting unrelated work.

No publishing pipeline or new software dependency is needed for the pilot. Add automation later only for a repeated, concrete editorial check.

