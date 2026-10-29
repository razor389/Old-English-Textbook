# Unit 16 exports: extended narrative and speech

The accepted table-layout revision has a complete [learner PDF](chapter-16.pdf) of **64 pages** and a separate [answer-key PDF](answer-key.pdf) of **32 pages**. The changed pages and heading repairs passed independent visual review.

Current [export identities and page counts](../../docs/revisions/table-layout/exports.json), [page acceptance](../../docs/revisions/table-layout/page-review.json), and the [validated build report](../../docs/revisions/table-layout/build-report.json) document this presentation revision. The [complete-content checks](../../docs/revisions/table-layout/export-text-review.json) and [logical-table review](../../docs/revisions/table-layout/table-review.json) preserve the teaching and source scope.

Editable masters are [student.md](../../chapters/ch16/student.md) and [answer-key.md](../../chapters/ch16/answer-key.md); complete TeX sources are [chapter-16.tex](chapter-16.tex) and [answer-key.tex](answer-key.tex). The [course presentation revision](../../docs/revisions/table-layout/) records the mapping and checks separately from the original unit review.

Tables follow the shared [layout](../book-layout.tex): 10.5-point type with 13.2-point leading, bold headings, horizontal rules and consistent case/person labels. Identical verbal plural cells share `1–3 pl.`; distinct forms remain separate. Counts of grammatical forms and cells describe the complete logical paradigm, which is unchanged by fewer printed rows. Nominal cases, variants, supported uses and teaching milestones retain their stated scope.

## Reproduction

Run from the repository root with the configured TeX Live, Cambria, Xpdf and Ghostscript installation:

```powershell
python -X utf8 scripts/check_course_layout.py --report build/course-layout-check.json
python -X utf8 scripts/build_course_exports.py --stage all --select ch16/learner,ch16/key --include-unchanged --jobs 2 --render-suffix reproduction-01
python -X utf8 scripts/check_course_exports.py --chapter 16 --report build/course-export-ch16-check.json
```

The shared build command compiles each complete document twice, checks table parity and build diagnostics, extracts its text and renders all pages. Choose a fresh `--render-suffix` for a later changed build. Use `--stage inspect` to inspect existing build products without compiling, or `--stage render` to regenerate page images from them. `--select` accepts comma-separated document IDs such as `ch01/learner,ch03/key`.

The layout check compares expanded logical cells, actual Markdown/TeX tables, protected distinctions and frozen teaching content. The export check independently compares complete master prose, actual TeX cells and captions, and the built PDF text. The `--chapter` restriction above is a unit diagnostic; complete-course acceptance uses the unrestricted command in the [shared reproduction instructions](../README.md#reproduction). A later changed build needs fresh visual review bound to its PDF and page-image identities before it replaces an accepted PDF. Do not rerun historical assemblers, register mergers or baseline captures to rebuild exports.

Reproduction outputs and reports remain under `build/`; the build helper does not replace retained PDFs or rewrite the durable acceptance records linked above.

## Original unit acceptance and content scope

The following records the unit's original linguistic acceptance and export evidence. Its page counts, physical table counts, PDF hashes and inspection claims describe that earlier checkpoint, not acceptance of the current presentation revision. The substantive teaching, task and logical-cell counts remain applicable.

At the original export checkpoint: the complete learner PDF has **67 pages** and the separate answer key **32**. Their editable masters are [student.md](../../chapters/ch16/student.md) and [answer-key.md](../../chapters/ch16/answer-key.md). All 99 final pages passed non-author inspection; [page-review.json](page-review.json) binds the accepted PDF and page-image identities to the individual ledgers.

The exports include all 76 tasks / 179 requested outputs, every one of the 59 assigned Cook prompts, 56 complete bounded systems / 564 cells, four translated examples, the full 444-word gymnasium scene and all 54 original notes / 59 anchors. Supplied reading and composition help remains visible. The key contains the complete translation and every assigned answer with target, meaning, alternatives and relevant diagnosis.

[Full content parity](content-parity.json) verifies 1,146 prose/heading/list blocks, 90 tables and 1,747 table cells including headers. It checks complete Markdown/TeX content and PDF characters; it does not substitute for visual inspection. The final logs have no missing-character, font-substitution, box or rerun warnings. [Layout adjustments](layout-adjustments.json) retain the review and repair history. Cambria and the inherited 165 × 241 mm layout remain in use.

The [contract](../../chapters/ch16/coverage.json) preceded prose at `543e214`. Drafts are saved at `9b75319`, frozen independent solutions at `1bf0e8e`, and accepted text at `bbf014e`. The [independent text review](../../chapters/ch16/review.md) and [separate paradigm review](../../chapters/ch16/reviews/paradigms.json) resolve material findings. Complete exports/registers are saved at `edb1bbb`.

[A08](../../chapters/ch16/presentation-proofreading-amendment.json) and its [non-author confirmation](../../chapters/ch16/reviews/presentation-proofreading.json) document eight reference-spacing corrections after the initial accepted text at `effe431`. The accepted export text includes those corrections; no linguistic content changed.
