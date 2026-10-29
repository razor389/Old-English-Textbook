# Unit 3 exports

The accepted table-layout revision has a complete [learner PDF](chapter-03.pdf) of **31 pages** and a separate [answer-key PDF](answer-key.pdf) of **21 pages**. The changed pages and heading repairs passed independent visual review.

Current [export identities and page counts](../../docs/revisions/table-layout/exports.json), [page acceptance](../../docs/revisions/table-layout/page-review.json), and the [validated build report](../../docs/revisions/table-layout/build-report.json) document this presentation revision. The [complete-content checks](../../docs/revisions/table-layout/export-text-review.json) and [logical-table review](../../docs/revisions/table-layout/table-review.json) preserve the teaching and source scope.

Editable masters are [student.md](../../chapters/ch03/student.md) and [answer-key.md](../../chapters/ch03/answer-key.md); complete TeX sources are [chapter-03.tex](chapter-03.tex) and [answer-key.tex](answer-key.tex). The [course presentation revision](../../docs/revisions/table-layout/) records the mapping and checks separately from the original unit review.

Tables follow the shared [layout](../book-layout.tex): 10.5-point type with 13.2-point leading, bold headings, horizontal rules and consistent case/person labels. Identical verbal plural cells share `1–3 pl.`; distinct forms remain separate. Counts of grammatical forms and cells describe the complete logical paradigm, which is unchanged by fewer printed rows. Nominal cases, variants, supported uses and teaching milestones retain their stated scope.

## Reproduction

Run from the repository root with the configured TeX Live, Cambria, Xpdf and Ghostscript installation:

```powershell
python -X utf8 scripts/check_course_layout.py --report build/course-layout-check.json
python -X utf8 scripts/build_course_exports.py --stage all --select ch03/learner,ch03/key --include-unchanged --jobs 2 --render-suffix reproduction-01
python -X utf8 scripts/check_course_exports.py --chapter 3 --report build/course-export-ch03-check.json
```

The shared build command compiles each complete document twice, checks table parity and build diagnostics, extracts its text and renders all pages. Choose a fresh `--render-suffix` for a later changed build. Use `--stage inspect` to inspect existing build products without compiling, or `--stage render` to regenerate page images from them. `--select` accepts comma-separated document IDs such as `ch01/learner,ch03/key`.

The layout check compares expanded logical cells, actual Markdown/TeX tables, protected distinctions and frozen teaching content. The export check independently compares complete master prose, actual TeX cells and captions, and the built PDF text. The `--chapter` restriction above is a unit diagnostic; complete-course acceptance uses the unrestricted command in the [shared reproduction instructions](../README.md#reproduction). A later changed build needs fresh visual review bound to its PDF and page-image identities before it replaces an accepted PDF. Do not rerun historical assemblers, register mergers or baseline captures to rebuild exports.

Reproduction outputs and reports remain under `build/`; the build helper does not replace retained PDFs or rewrite the durable acceptance records linked above.

## Original unit acceptance and content scope

The following records the unit's original linguistic acceptance and export evidence. Its page counts, physical table counts, PDF hashes and inspection claims describe that earlier checkpoint, not acceptance of the current presentation revision. The substantive teaching, task and logical-cell counts remain applicable.

At the original export checkpoint: the learner PDF has **30 pages**; the separate key has **19**. The editable masters are [student.md](../../chapters/ch03/student.md) and [answer-key.md](../../chapters/ch03/answer-key.md). These are complete exports, including all vocabulary, recoverable full paradigms, 70 tasks, ten examples, both connected readings, local reading help, and source notes. They are not specimen selections.

Textual and presentation review are accepted. All **49 final pages** were visually inspected by reviewers who did not author the corresponding master, with every finding resolved and the final file identities checked.

### Original content and review

[content-parity.json](content-parity.json) records independent comparison of the Markdown block inventory with the actual TeX: **282 learner and 128 key paragraph/heading/list blocks**, **29 learner and 22 key tables**, and **1,063 learner and 505 key table cells including headers**. Every editorial comment is preserved. All complete prose blocks also occur in the extracted PDF character stream, with only whitespace and Xpdf soft-hyphen encoding normalized. The four literal error asterisks in X2 remain characters, not Markdown emphasis.

The grammar presents 78 complete recoverable paradigms through full model tables, complete special tables and explicit stem substitutions. Independent review reproduced every one of their 1,565 unique form records from the learner's displays and rules; the export does not expand those economical patterns into redundant tables.

The [textual review](../../chapters/ch03/review.md) preserves independent solving before key access and the resolution of every finding. The final page ledgers under [reviews](reviews/) identify the actual PDF and rendered-page hashes. The coordinator's consolidated [page-review.json](page-review.json) records final presentation acceptance and file identities. Earlier render findings are retained in the ledgers; they do not certify an uninspected later file.

### Original checkpoints

The pre-prose contract was saved at `9626f6f`; independently accepted text at `e528af8`; complete exports and reviewed registers at **`95c68d6`**. Later presentation-only captions and emphasis changes were independently checked and are recorded in the review. This export stage adds no new grammatical or lexical scope.
