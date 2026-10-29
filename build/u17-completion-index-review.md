# Unit 17 completion-index writer: bounded read-only review

The revised writer has no remaining blocking defect in the requested scope. This is a static review of `build/write_unit17_completion_indexes.py`, not execution of the writer or acceptance of Unit 17 completion. The reviewed writer SHA-256 is `dadec0b827b1031dd8178e740d16caf1ae4306f009130140afd265b1343c8472`. Its syntax was parsed without execution.

Two findings were reported to the coordinator and repaired during this review:

- The proposed COURSE_PLAN paragraph originally attributed all 146 answer positions to the four examples and 21 original tasks. It now states that the 21 originals request **64 responses**, while all **103 tasks request 146**. Those counts match the actual amended contract.
- The writer originally neither checked nor printed the amended feature/teaching totals. It now derives and asserts **64 grammar features / 420 teaching records**, compares them with `explicit_scope_metrics`, and prints them in the course-plan paragraph. The current contract satisfies both checks.

The limited preservation and link checks found the following:

- All current textual replacement anchors occur exactly once. README retains the sixteen earlier unit paragraphs and appends Unit 17 with the correct learner/key PDF paths.
- COURSE_PLAN changes only the Unit 17 table row, appends its current assignment account and makes older crosswalk totals explicitly historical. The Unit 18 row remains untouched. COOK_MAP preserves earlier rows and accounts while recording 597 assigned / 47 deferred / none excluded; 515 + 82 = 597. The 82-item distribution is 14/10/7/10/12/9/20.
- STATUS reuses all sixteen existing completion-table rows before appending Unit 17. HANDOFF reuses its sixteen checkpoint rows, resolving Unit 16’s former “This handoff checkpoint” to `defa800` and assigning that relative label only to Unit 17. Both new summaries explicitly keep Unit 18 undrafted and require a new user request before it begins.
- The four registry source IDs exist exactly where the writer expects: Cook Exercises and First Book in `selected_sources`, Wright and Bosworth–Toller in `supporting_sources`. None already has `unit17_use`. The writer adds that field without replacing earlier source values or unit-use histories. JSON reformatting does not change their semantic content.
- The new links to the source report, grammar report, curriculum report, coordinator reconciliation, primary-inspection ledger, numeral decision, nīwe decision, prior-state record, blind-freeze record and independence protocol all resolve to existing files. The planned learner/key and export-index links use the correct retained Unit 17 destinations. Future export-only records cannot yet be checked for existence.
- The historical baseline is accurate: `defa8008f6887a1f5f6afe9db27431d500a03f67`, 1,067 lemmas, 11,188 forms, 1,376 senses, 1,080 features; 2,935 earlier active files including the two registers, leaving 2,933 fixed nonregister artifacts.

Page and integration metrics are correctly deferred to the accepted records. The writer reads learner/key/total pages and parity counts from `page-review.json`, and cumulative register totals and Unit 17 milestones from `register-integration.json`. Their field names agree with the existing page-acceptance and integration-check producers. It does not substitute the still-current sixteen-unit register totals for the future integrated totals.

At this review, neither final `typesetting/ch17/page-review.json` nor `chapters/ch17/register-integration.json` exists, and the canonical completion flags remain false. Consequently, actual final page and post-integration totals cannot yet be certified. The writer appropriately requires those records and accepted textual, presentation and integration statuses before writing completion claims.

Checkpoint roles remain distinct: contract, complete drafts, frozen independent solutions and accepted text come from separate canonical fields; complete exports/registers use the explicitly supplied `--exports-checkpoint`; the final handoff is separately labelled in the checkpoint table. The writer does not present the accepted-text checkpoint as the completed export/register or final-handoff checkpoint.

Only this review file was written. The completion writer was not run; no shared index, master, contract, key, source, register, review or Beads record was changed by this check.
