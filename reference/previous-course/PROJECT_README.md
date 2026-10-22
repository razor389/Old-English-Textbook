# Cook Expanded

Status: Chapters 1–2 are complete and independently reviewed. Each includes the complete corresponding Cook exercise, the required grammar and vocabulary, a supported reading clause, and a separate explanatory key.

| Chapter | Complete lesson | Complete key | Scope |
|---|---|---|---|
| 1. Naming the world | [PDF](typesetting/ch01/chapter-01.pdf), 5 pages | [PDF](typesetting/ch01/answer-key.pdf), 3 pages | Thirty production nouns; all sixteen items of Exercise 1 |
| 2. Plural nouns | [PDF](typesetting/ch02/chapter-02.pdf), 5 pages | [PDF](typesetting/ch02/answer-key.pdf), 3 pages | Twenty-two plural forms, three new noun lemmas; all twelve items of Exercise 2 |

Editable sources and reviews: [Chapter 1 lesson](chapters/ch01/student.md), [key](chapters/ch01/answer-key.md), [review](chapters/ch01/review.md); [Chapter 2 lesson](chapters/ch02/student.md), [key](chapters/ch02/answer-key.md), [review](chapters/ch02/review.md). Each chapter has separate editorial notes. Chapter 2 carries forward the correction **wǣstm → wæstm** and explains the strong-neuter **-u**/zero contrast through stem weight.

## Aim

Build an expanded teaching edition of Albert S. Cook's *Exercises in Old English*. Each chapter introduces the grammar and vocabulary its exercises require, then provides a graded reading and translation section drawn from *A First Book in Old English*. Work chapter by chapter, keeping an explicit record of what the learner has learned.

The essential rule: every required word sense, inflected form, and construction must be previously taught, taught now, or explicitly supplied. A supplied reading gloss does not establish productive mastery.

## Working assumptions

The audience and typesetting direction were agreed on 21 October 2026; the compact textbook style and one-to-one exercise mapping were specified on 22 October. Other editorial defaults remain revisable after the pilot:

- Adult independent learner with no assumed Old English, Latin, or Greek. Standard grammar terminology is assumed familiar.
- The user's own Old English experience does not count as a course prerequisite. Keep the book self-contained for other learners.
- Roughly 30 new vocabulary items per lesson is acceptable to the user; control grammar and task demands separately from vocabulary count.
- Terse grammar-textbook exposition in the spirit of Thackston and Lambdin: rules, paradigms, vocabulary, and exercises, with minimal coaching. Keys use compact answers and shared notes. A general grammar terminology appendix may be added later.
- Each lesson corresponds to one complete numbered exercise in Cook, in source order, with all its items. Original group, exercise, and item numbers remain traceable.
- Teach the grammar and vocabulary needed for the full exercise. Select or shorten the accompanying reading to suit the lesson; do not split the composition exercise across lessons.
- Use Cook's 1895 *Exercises* and the 1895 second edition of *First Book* as the initial source pair.
- Retain Cook's prose spelling baseline. Any display normalization is explicit and reversible.
- Correct demonstrable errors in Cook when supported by contemporary linguistic evidence; preserve the source transcription and explain each correction in an editorial note.
- Keep the student text and the answers in separate files.
- The completed pilot corresponds to Exercise 1; Chapter 2 follows the same one-to-one mapping. Teaching contracts and readings for Chapter 3 onward remain to be audited.
- Keep source references and editorial commentary in section footnotes or endnotes so they do not interrupt the explanations.
- Print/PDF typesetting system: LuaLaTeX. Keep editable chapter text in Markdown and deliver the complete chapter and a separate complete key, including all vocabulary and tasks. Font and page design remain provisional.

## Continue the project

1. Read this file, `AGENTS.md`, `STATUS.md`, and the completed chapters.
2. Keep chapter revisions in the existing local Git repository; no publication is required.
3. Use the pilot to assess workload and presentation within the agreed one-exercise-per-lesson structure.
4. When the next chapter is requested, use `prompts/NEXT_CHAPTER.txt` and read all earlier coverage files and cumulative registers.

`pilot/BRIEF.md` and `prompts/FIRST_RUN.txt` remain as the record of the initial task; the first chapter does not need to be restarted.

You do not need custom agents or an API application to start. The supplied prompts define editorial roles in ordinary language. Availability of parallel execution depends on the Codex client/account; the same roles can run sequentially.

## Files and responsibilities

| File or directory | Purpose |
|---|---|
| `AGENTS.md` | Persistent project rules for Codex |
| `EDITORIAL_POLICY.md` | Audience, spelling, provenance, and assessment decisions |
| `sources/registry.json` | Edition and scan identities |
| `sources/OPENING_AUDIT.md` | Checked opening-source findings and editorial implications |
| `curriculum/SEQUENCE.md` | Provisional progression and rules for changing it |
| `curriculum/grammar.json` | Nineteen reviewed grammar/orientation records; supplied knowledge kept separate |
| `lexicon/entries.json` | Forty-three reviewed lemma records; form and sense milestones distinguish taught and supplied material |
| `chapters/ch01/`, `chapters/ch02/` | Reviewed lessons, keys, coverage contracts, editorial notes, and independent reviews |
| `typesetting/ch01/`, `typesetting/ch02/` | Complete chapters and keys in LuaLaTeX/PDF; editable lessons remain in Markdown |
| `pilot/BRIEF.md` | Bounded first chapter task |
| `templates/` | Student chapter, key, coverage, and review templates |
| `prompts/` | First-run and later-chapter task instructions |
| `DATA_GUIDE.md` | Record meanings and ID conventions |
| `STATUS.md` | Completed work, open questions, and next action |

Continue with `chapters/ch03/` when requested. Each chapter's `coverage.json` is its learning contract, prepared before prose. Across chapters, its assigned/deferred/excluded item records form the canonical source crosswalk. Create source transcriptions under `sources/transcriptions/`. The coordinator is the only agent that merges changes into shared grammar and vocabulary records.

## What counts as a finished chapter

A finished chapter has a scan-checked source basis, a coherent learning contract, grammar, vocabulary, preparation exercises, attributed Cook exercises, a supported reading, translation tasks, a separate explanatory key, and a resolved review report. Every required item must have an answer or assessment criterion. Record remaining uncertainty rather than calling it verified.

Scripts can check references, IDs, Unicode, and missing answers once there are real chapters. They cannot certify Old English grammar or idiom. Avoid building a publishing system before the pilot establishes the teaching method.

## Sources and documentation

Book editions, supporting scholarship, and page locators are in `sources/registry.json`. The opening audit separates observed source facts from editorial recommendations. Full scans are linked and cached locally outside Git; selected inspection images are retained with the transcription and analysis records.

Official Codex guidance: [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) and [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents). These pages support the project-instructions and delegation mechanisms; the editorial workflow in this package is a proposed design.

Prepared 21 October 2026; revised 22 October 2026.

