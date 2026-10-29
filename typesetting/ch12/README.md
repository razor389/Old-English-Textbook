# Unit 12 exports

The accepted table-layout revision has a complete [learner PDF](chapter-12.pdf) of **46 pages** and a separate [answer-key PDF](answer-key.pdf) of **30 pages**. The changed pages and heading repairs passed independent visual review.

Current [export identities and page counts](../../docs/revisions/table-layout/exports.json), [page acceptance](../../docs/revisions/table-layout/page-review.json), and the [validated build report](../../docs/revisions/table-layout/build-report.json) document this presentation revision. The [complete-content checks](../../docs/revisions/table-layout/export-text-review.json) and [logical-table review](../../docs/revisions/table-layout/table-review.json) preserve the teaching and source scope.

Editable masters are [student.md](../../chapters/ch12/student.md) and [answer-key.md](../../chapters/ch12/answer-key.md); complete TeX sources are [chapter-12.tex](chapter-12.tex) and [answer-key.tex](answer-key.tex). The [course presentation revision](../../docs/revisions/table-layout/) records the mapping and checks separately from the original unit review.

Tables follow the shared [layout](../book-layout.tex): 10.5-point type with 13.2-point leading, bold headings, horizontal rules and consistent case/person labels. Identical verbal plural cells share `1–3 pl.`; distinct forms remain separate. Counts of grammatical forms and cells describe the complete logical paradigm, which is unchanged by fewer printed rows. Nominal cases, variants, supported uses and teaching milestones retain their stated scope.

## Reproduction

Run from the repository root with the configured TeX Live, Cambria, Xpdf and Ghostscript installation:

```powershell
python -X utf8 scripts/check_course_layout.py --report build/course-layout-check.json
python -X utf8 scripts/build_course_exports.py --stage all --select ch12/learner,ch12/key --include-unchanged --jobs 2 --render-suffix reproduction-01
python -X utf8 scripts/check_course_exports.py --chapter 12 --report build/course-export-ch12-check.json
```

The shared build command compiles each complete document twice, checks table parity and build diagnostics, extracts its text and renders all pages. Choose a fresh `--render-suffix` for a later changed build. Use `--stage inspect` to inspect existing build products without compiling, or `--stage render` to regenerate page images from them. `--select` accepts comma-separated document IDs such as `ch01/learner,ch03/key`.

The layout check compares expanded logical cells, actual Markdown/TeX tables, protected distinctions and frozen teaching content. The export check independently compares complete master prose, actual TeX cells and captions, and the built PDF text. The `--chapter` restriction above is a unit diagnostic; complete-course acceptance uses the unrestricted command in the [shared reproduction instructions](../README.md#reproduction). A later changed build needs fresh visual review bound to its PDF and page-image identities before it replaces an accepted PDF. Do not rerun historical assemblers, register mergers or baseline captures to rebuild exports.

Reproduction outputs and reports remain under `build/`; the build helper does not replace retained PDFs or rewrite the durable acceptance records linked above.

## Original unit acceptance and content scope

The following records the unit's original linguistic acceptance and export evidence. Its page counts, physical table counts, PDF hashes and inspection claims describe that earlier checkpoint, not acceptance of the current presentation revision. The substantive teaching, task and logical-cell counts remain applicable.

At the original export checkpoint: the complete learner PDF has **47 pages**; the separate key has **30**. Editable masters: [student.md](../../chapters/ch12/student.md) and [answer-key.md](../../chapters/ch12/answer-key.md). All 76 tasks, vocabulary, complete defined systems, readings, support and source notes are included.

All **77 final pages** passed non-author visual inspection. [Individual ledgers](reviews/) retain page-specific observations and exact PDF/image identities. Wide adjective tables use stacked singular/plural panels at unchanged 10.5pt type, with visible captions. The parity check reconstructs the original seven-column coordinates. Lexical definitions stay with their first display or derivation; each Cook prompt stays with its answer. The key's diagnostic table has enough width for geopenian. [Final acceptance](page-review.json) reconciles every final page, complete parity, unchanged accepted masters and clean build logs. The ledgers record repairs and reinspections.

### Original content and review

[Complete parity](content-parity.json) covers **796 prose/heading/list blocks, 82 tables, 1,124 cells including headers, and 572 editorial comments**. An independent Markdown inventory matches decoded TeX; full prose matches extracted PDF text after whitespace and soft-hyphen normalization. Visual review includes tables, endings and special characters.

The learner gives **62 complete defined systems / 692 cells**, using 44 marked matrices and 29 lexical diagnostic rows: 368 literal cells and 324 explicit model derivations. Exceptional patterns are printed in full. The twelve habban construction positions are a separate display using actual finite auxiliary, object and participle forms; they add no synthetic lexical forms. Complete morphology retains its stated lexical and syntactic limits.

All **38 Cook VI.19–21 prompts** preserve their wording and identifiers, alongside 38 original tasks and twelve translated examples. The **53-word new account**, “A house and a return,” prepares the exact **155-word** first Roman relief and renewed invasion extract from Cook's Picts and Scots narrative: printed pp. 145–146 / one-based PDF 161–162, editorial 145.1 through 146.11 (partial), ending **and hīe mid ealle foriermdon.** All 21 attached original notes, sixteen reading helps and eleven Cook help groups remain. Earlier Roman withdrawal is separate English context. Original historical speculation remains labelled archival apparatus.

The main [reviewer](../../chapters/ch12/review.md) froze [solutions](../../chapters/ch12/independent-solutions.md) before opening key/private answer files. The record distinguishes 75 unexposed tasks from an exposed check of Cook 21.4, whose proposed clause had accidentally appeared in a source discussion. A fresh reviewer froze an [unexposed 21.4 solution](../../chapters/ch12/reviews/fresh-21-04-solutions.md) before key access and completed a separate [primary-source paradigm review](../../chapters/ch12/reviews/paradigms.json). The [main ledger](../../chapters/ch12/review-ledger.json) records every actual task, all 692 cell routes, source checks, alternatives and adjudications. No material finding remains open. Neither reviewer authored a master or graded task. Original audit records and frozen witnesses remain unchanged; the two canonical amendments are recorded in coverage and review.

### Original checkpoints

Checkpoints: contract **`3ec8787`**, complete drafts **`4c9bcd8`**, main pre-key solutions **`a48c232`**, fresh pre-key solution **`b52a9d3`**, accepted text **`61f4ea4`**. The [handoff](../../docs/HANDOFF.md) records complete exports, register integration and final closure.
