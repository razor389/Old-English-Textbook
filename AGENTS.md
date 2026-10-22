# Project instructions: Old English, Cook / Lambdin-style

## Read first

Read `STATUS.md`, `EDITORIAL_POLICY.md`, `curriculum/COURSE_PLAN.md`, `curriculum/COOK_MAP.md`, `sources/registry.json`, and `docs/WORKFLOW.md`. Run `bd prime` and `bd ready`. Before chapter work, read every earlier active coverage contract and the actual cumulative registers.

The initial task is to establish the course outline and source mapping, then develop the first unit under `curriculum/UNIT_01_BRIEF.md`. No new-course chapter is complete at initialization. Empty registers mean no prior teaching.

## Scope and structure

Build a self-contained course for an adult with no prior Old English and familiarity with standard grammar terminology. Use terse exposition in the spirit of Lambdin and Thackston. Follow the practical organization of Lambdin's Gothic course; historical grammar belongs in brief explanatory notes or later supplementary material.

Organize chapters around grammatical units. Present a complete singular/plural declension when introducing a noun class, and complete clearly defined verbal paradigms when introducing a conjugational system. Include the rules governing endings, stem changes, and important exceptions together. Teach basic uses alongside the forms; advanced syntax may develop later. A chapter may cover several study sessions and several Cook exercises. Vocabulary size follows the material; there is no thirty-word ceiling.

The old one-Cook-exercise-per-chapter rule is superseded. Preserve Cook's original group/exercise/item IDs and English prompts when regrouping. Retain complete exercise sets where pedagogically coherent; record any redistribution or deferral at item level. Never silently omit difficult items. Prefer connected readings with sufficient grammatical groundwork and explicit support.

`reference/previous-course/` is a historical evidence snapshot, not the active syllabus or instructions. Its files, statuses, and learning milestones describe another course. Reuse checked facts and documented corrections; establish all new-course teaching milestones afresh. Do not edit the snapshot during ordinary chapter work.

## Beads and parallel editorial work

Use Beads for actionable work, blockers, and handoffs. Read an issue before starting it; use explicit IDs. The coordinator is the sole Beads writer in the seeded embedded-Dolt setup and assigns bounded work to agents. Workers return findings and proposed status changes to the coordinator. Serialize all `bd` commands; the installed embedded backend supports one writer. Do not run workers against independently initialized trackers for the same project.

Use parallel agents for independent source inspection and curriculum analysis when available. Give each writing agent exclusive files. Draft only after their evidence is reconciled in a learning contract. The stages are source editor, curriculum/linguistic analyst, lesson author, independent reviewer, and coordinator. A reviewer should solve learner tasks before reading the draft key where practical and should modify only their own review files. The coordinator owns shared source indexes, registers, chapter contracts, and final integration.

Claims, dependencies, and issue closure do not certify linguistic truth. Require actual source evidence. Keep meaningful task descriptions and completion notes; export Beads before a Git checkpoint as documented in `docs/WORKFLOW.md`. Commit locally; do not invent a remote or push requirement.

## Sources and grading

Use the selected editions and scans in the registry. OCR is a finding aid. Verify Old English letters, length marks, and locators against page images. Record printed page, scan/PDF convention, original identifier, and origin category: exact source, declared normalization, adaptation of a specific passage, or new teaching material. Distinguish printed line numbers from editorial counting. Keep transcription, learner text, and change notes separate.

Audit exercises and reading before prose. Record `chapters/chNN/coverage.json` first. Across active chapter contracts, assigned/deferred/excluded source records form the canonical assignment crosswalk. The inherited audit index and planning map are evidence and planning aids, not new assignments.

For each needed sense, form, and construction record: previously taught, new production, new recognition, supplied, or unresolved. Full paradigm tables need evidence and an explicit teaching scope; displaying a cell does not establish that all its syntactic uses have been taught. Independent production must use taught material. Supplied forms may support explicitly scaffolded tasks, without testing their independent recall. Familiar headwords do not imply familiarity with every form or sense.

Resolve unresolved dependencies by teaching, supplying support, revising a task, or recording a justified deferral. A larger vocabulary is acceptable; unexplained grammar is not.

## Language, keys, and completion

Follow `EDITORIAL_POLICY.md`. Correct demonstrated source errors with evidence and notes; preserve originals. Do not silently regularize spelling, infer vowel length, or change dialect. Mark new composition and verify its vocabulary, morphology, syntax, and intended meaning.

Prepare translations independently from the actual Old English. Keys need models, targets, essential meaning, explanations, defensible alternatives, and useful error diagnoses; shared compact notes are encouraged. Distinguish valid language from compliance with a stated target.

Before closing a chapter: reconcile every assigned item with its key; check source and dependency references; resolve material review errors; inspect every exported page and special character; update active registers and status; export Beads; save a recoverable local Git revision. Complete one requested chapter at a time. Add automation only for a repeated concrete check.

Resolve routine choices autonomously within these decisions. Ask only when available evidence cannot settle a substantive change to audience, fidelity, or scope. Continue independent work while a specific uncertainty is investigated.
