# Unit 14 exports

The accepted table-layout revision has a complete [learner PDF](chapter-14.pdf) of **34 pages** and a separate [answer-key PDF](answer-key.pdf) of **21 pages**. The changed pages and heading repairs passed independent visual review.

Current [export identities and page counts](../../docs/revisions/table-layout/exports.json), [page acceptance](../../docs/revisions/table-layout/page-review.json), and the [validated build report](../../docs/revisions/table-layout/build-report.json) document this presentation revision. The [complete-content checks](../../docs/revisions/table-layout/export-text-review.json) and [logical-table review](../../docs/revisions/table-layout/table-review.json) preserve the teaching and source scope.

Editable masters are [student.md](../../chapters/ch14/student.md) and [answer-key.md](../../chapters/ch14/answer-key.md); complete TeX sources are [chapter-14.tex](chapter-14.tex) and [answer-key.tex](answer-key.tex). The [course presentation revision](../../docs/revisions/table-layout/) records the mapping and checks separately from the original unit review.

Tables follow the shared [layout](../book-layout.tex): 10.5-point type with 13.2-point leading, bold headings, horizontal rules and consistent case/person labels. Identical verbal plural cells share `1–3 pl.`; distinct forms remain separate. Counts of grammatical forms and cells describe the complete logical paradigm, which is unchanged by fewer printed rows. Nominal cases, variants, supported uses and teaching milestones retain their stated scope.

## Reproduction

Run from the repository root with the configured TeX Live, Cambria, Xpdf and Ghostscript installation:

```powershell
python -X utf8 scripts/check_course_layout.py --report build/course-layout-check.json
python -X utf8 scripts/build_course_exports.py --stage all --select ch14/learner,ch14/key --include-unchanged --jobs 2 --render-suffix reproduction-01
python -X utf8 scripts/check_course_exports.py --chapter 14 --report build/course-export-ch14-check.json
```

The shared build command compiles each complete document twice, checks table parity and build diagnostics, extracts its text and renders all pages. Choose a fresh `--render-suffix` for a later changed build. Use `--stage inspect` to inspect existing build products without compiling, or `--stage render` to regenerate page images from them. `--select` accepts comma-separated document IDs such as `ch01/learner,ch03/key`.

The layout check compares expanded logical cells, actual Markdown/TeX tables, protected distinctions and frozen teaching content. The export check independently compares complete master prose, actual TeX cells and captions, and the built PDF text. The `--chapter` restriction above is a unit diagnostic; complete-course acceptance uses the unrestricted command in the [shared reproduction instructions](../README.md#reproduction). A later changed build needs fresh visual review bound to its PDF and page-image identities before it replaces an accepted PDF. Do not rerun historical assemblers, register mergers or baseline captures to rebuild exports.

Reproduction outputs and reports remain under `build/`; the build helper does not replace retained PDFs or rewrite the durable acceptance records linked above.

## Original unit acceptance and content scope

The following records the unit's original linguistic acceptance and export evidence. Its page counts, physical table counts, PDF hashes and inspection claims describe that earlier checkpoint, not acceptance of the current presentation revision. The substantive teaching, task and logical-cell counts remain applicable.

At the original export checkpoint: the complete learner PDF has **35 pages**; the separate key has **21**. Editable masters: [student.md](../../chapters/ch14/student.md) and [answer-key.md](../../chapters/ch14/answer-key.md). All 44 tasks, vocabulary, complete defined paradigms, connected reading, support and original notes are included.

All **56 final pages** passed non-author visual inspection. [Individual ledgers](reviews/) retain page-specific observations and final PDF/image identities. [Final acceptance](page-review.json) reconciles every page, complete parity, unchanged accepted masters and clean logs. [Layout adjustments](layout-adjustments.json) record the key's A01 column-width repair and the heading repairs: each indicative heading stays with its rule and complete table, and the Cook VIII.27 heading stays with its first answer. Changed pages were inspected again; byte-identical pages retain their actual earlier inspection records.

### Original content and review

[Complete parity](content-parity.json) covers **521 prose/heading/list blocks, 55 tables, 925 cells including headers, and 470 editorial comments**. An independent Markdown inventory matches decoded TeX; full prose matches extracted PDF text after whitespace and soft-hyphen normalization. Markdown note references become matching numbered superscript endnote labels. Every note definition remains. Visual review includes actual tables, endings and special characters.

The learner gives 38 complete systems / 324 cells in 38 literal matrices, with rules, stem changes and bounded uses. All 21 Cook VIII.26–27 prompts retain their wording and IDs, alongside 23 original tasks and four translated examples. The 159-word Dangers opening, printed 156.1–158.4 / PDF 172–174, retains 24 notes / 25 anchors, 34 reading helps and 20 Cook help groups. The next argument is unassigned.

The fresh [reviewer](../../chapters/ch14/review.md) froze [all solutions](../../chapters/ch14/independent-solutions.md) before key/current-contract/audit access. A separate [fresh paradigm reviewer](../../chapters/ch14/reviews/paradigms.json) checked every cell and rule against actual primary evidence. Neither authored a master or task. Canonical amendments preserve corrections separately from original audit packets; the blind witness is unchanged. No material finding is open.

### Original checkpoints

Checkpoints: contract **`18cfa3a`**, drafts **`e8cf9ce`**, blind solutions **`d78de6f`**, accepted text **`5721c5f`**. Complete exports/registers: **`a56c403`**. The [handoff](../../docs/HANDOFF.md) records final closure.
