# Unit 8 exports

The accepted table-layout revision has a complete [learner PDF](chapter-08.pdf) of **29 pages** and a separate [answer-key PDF](answer-key.pdf) of **24 pages**. The changed pages and heading repairs passed independent visual review.

Current [export identities and page counts](../../docs/revisions/table-layout/exports.json), [page acceptance](../../docs/revisions/table-layout/page-review.json), and the [validated build report](../../docs/revisions/table-layout/build-report.json) document this presentation revision. The [complete-content checks](../../docs/revisions/table-layout/export-text-review.json) and [logical-table review](../../docs/revisions/table-layout/table-review.json) preserve the teaching and source scope.

Editable masters are [student.md](../../chapters/ch08/student.md) and [answer-key.md](../../chapters/ch08/answer-key.md); complete TeX sources are [chapter-08.tex](chapter-08.tex) and [answer-key.tex](answer-key.tex). The [course presentation revision](../../docs/revisions/table-layout/) records the mapping and checks separately from the original unit review.

Tables follow the shared [layout](../book-layout.tex): 10.5-point type with 13.2-point leading, bold headings, horizontal rules and consistent case/person labels. Identical verbal plural cells share `1–3 pl.`; distinct forms remain separate. Counts of grammatical forms and cells describe the complete logical paradigm, which is unchanged by fewer printed rows. Nominal cases, variants, supported uses and teaching milestones retain their stated scope.

## Reproduction

Run from the repository root with the configured TeX Live, Cambria, Xpdf and Ghostscript installation:

```powershell
python -X utf8 scripts/check_course_layout.py --report build/course-layout-check.json
python -X utf8 scripts/build_course_exports.py --stage all --select ch08/learner,ch08/key --include-unchanged --jobs 2 --render-suffix reproduction-01
python -X utf8 scripts/check_course_exports.py --chapter 8 --report build/course-export-ch08-check.json
```

The shared build command compiles each complete document twice, checks table parity and build diagnostics, extracts its text and renders all pages. Choose a fresh `--render-suffix` for a later changed build. Use `--stage inspect` to inspect existing build products without compiling, or `--stage render` to regenerate page images from them. `--select` accepts comma-separated document IDs such as `ch01/learner,ch03/key`.

The layout check compares expanded logical cells, actual Markdown/TeX tables, protected distinctions and frozen teaching content. The export check independently compares complete master prose, actual TeX cells and captions, and the built PDF text. The `--chapter` restriction above is a unit diagnostic; complete-course acceptance uses the unrestricted command in the [shared reproduction instructions](../README.md#reproduction). A later changed build needs fresh visual review bound to its PDF and page-image identities before it replaces an accepted PDF. Do not rerun historical assemblers, register mergers or baseline captures to rebuild exports.

Reproduction outputs and reports remain under `build/`; the build helper does not replace retained PDFs or rewrite the durable acceptance records linked above.

## Original unit acceptance and content scope

The following records the unit's original linguistic acceptance and export evidence. Its page counts, physical table counts, PDF hashes and inspection claims describe that earlier checkpoint, not acceptance of the current presentation revision. The substantive teaching, task and logical-cell counts remain applicable.

At the original export checkpoint: the complete learner PDF has **30 pages**; the separate key has **24**. The editable masters are [student.md](../../chapters/ch08/student.md) and [answer-key.md](../../chapters/ch08/answer-key.md). Both exports contain the complete independently accepted unit: explanations, vocabulary, paradigms, examples, all 66 tasks, both readings, local help and source notes.

All **54 final pages** passed non-author visual inspection. [Individual ledgers](reviews/) retain page-specific observations, actual inspection provenance and exact PDF/image identities. The initial layout keeps short examples with their translations and all four source-dialogue turns together in consistent reading type. Page proof prompted a one-word introductory correction, independently reaccepted at 72ee930: the examples have no visible numbers, so the word numbered was removed. TeX-only repairs attach Cook exercise labels to their prompts and begin key Q02 on a fresh page for comfortable footer clearance. The final v2 render changes learner pages 1, 21 and 22 and key pages 5–18. Reviewers directly reopened all seventeen changed pages and independently verified that the remaining thirty-seven page images are byte-identical to the versions they inspected. [Final presentation acceptance](page-review.json) reconciles every page, the accepted masters, complete parity and clean build logs. No material presentation issue remains open.

### Original complete content and independent review

[Content parity](content-parity.json) compares every Markdown block with the actual TeX: **600 prose/heading/list blocks**, **48 tables**, **793 table cells including headers** and **402 editorial comments**. Complete prose also matches the extracted PDF character stream, with only whitespace and Xpdf soft-hyphen encoding normalized. The independent table comparison and every-page inspection cover forms, headings, endings and special characters.

The learner gives **27 logical paradigms with 368 cells in 36 print matrices**. Complete selected interrogative, indefinite and minor demonstrative systems accompany questions and ordinary relatives. Ætēowian has full assigned indicative/subjunctive systems, scīnan full subjunctives, geblētsian both commands, and līf its singular/plural declension. Tables identify every covered person, number, case and gender. Display does not extend a form's stated syntactic or recognition scope.

All **66 graded tasks** have separate models, targets, explanations, alternatives and diagnoses; **all seventeen Cook I.8 prompts** remain exact. Sixteen new examples and the **62-word dialogue**, “The ship and the fish,” retain their checked wording. The exact **72-word, four-turn merchant opening** comes from Cook's *First Book*, printed pp. 129–130 / one-based PDF pp. 145–146: three editorially counted dialogue lines on p. 129, then printed lines 1–7 on p. 130. All **twelve helps and fifteen original notes** are retained. Historical note questions are not additional course tasks. The following goods catalogue remains unassigned.

The [independent review](../../chapters/ch08/review.md), [frozen pre-key solutions](../../chapters/ch08/independent-solutions.md) and [full ledger](../../chapters/ch08/review-ledger.json) record actual solving, all displayed-form checks, source-image evidence and key comparison. The reviewer authored neither master and discloses prior grammar-audit/public-example work. Frozen solution errors and defensible alternatives are adjudicated in the review rather than silently rewriting that witness. Initial page proof caught the phrase “numbered examples” despite invisible example numbers. Removing “numbered” was independently verified and checkpointed before the final exports; all tasks, tables, source text and the frozen witness remain unchanged.

### Original checkpoints

Checkpoints: contract before prose **`8751984`**, full drafts **`d20c6d5`**, frozen pre-key solutions **`9763993`**, accepted text **`72ee930`**. Complete exports and reviewed registers are saved at **`d36f134`**. The [handoff](../../docs/HANDOFF.md) records final Beads closure and completion metadata.
