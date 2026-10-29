# Unit 17 exports: connected exposition, praise and figurative language

The accepted table-layout revision has a complete [learner PDF](chapter-17.pdf) of **92 pages** and a separate [answer-key PDF](answer-key.pdf) of **45 pages**. The changed pages and heading repairs passed independent visual review. The key is byte-unchanged from its accepted export; only the learner PDF was rebuilt.

Current [export identities and page counts](../../docs/revisions/table-layout/exports.json), [page acceptance](../../docs/revisions/table-layout/page-review.json), and the [validated build report](../../docs/revisions/table-layout/build-report.json) document this presentation revision. The [complete-content checks](../../docs/revisions/table-layout/export-text-review.json) and [logical-table review](../../docs/revisions/table-layout/table-review.json) preserve the teaching and source scope.

Editable masters are [student.md](../../chapters/ch17/student.md) and [answer-key.md](../../chapters/ch17/answer-key.md); complete TeX sources are [chapter-17.tex](chapter-17.tex) and [answer-key.tex](answer-key.tex). The [course presentation revision](../../docs/revisions/table-layout/) records the mapping and checks separately from the original unit review.

Tables follow the shared [layout](../book-layout.tex): 10.5-point type with 13.2-point leading, bold headings, horizontal rules and consistent case/person labels. Identical verbal plural cells share `1–3 pl.`; distinct forms remain separate. Counts of grammatical forms and cells describe the complete logical paradigm, which is unchanged by fewer printed rows. Nominal cases, variants, supported uses and teaching milestones retain their stated scope.

## Reproduction

Run from the repository root with the configured TeX Live, Cambria, Xpdf and Ghostscript installation:

```powershell
python -X utf8 scripts/check_course_layout.py --report build/course-layout-check.json
python -X utf8 scripts/build_course_exports.py --stage all --select ch17/learner,ch17/key --include-unchanged --jobs 2 --render-suffix reproduction-01
python -X utf8 scripts/check_course_exports.py --chapter 17 --report build/course-export-ch17-check.json
```

The shared build command compiles each complete document twice, checks table parity and build diagnostics, extracts its text and renders all pages. Choose a fresh `--render-suffix` for a later changed build. Use `--stage inspect` to inspect existing build products without compiling, or `--stage render` to regenerate page images from them. `--select` accepts comma-separated document IDs such as `ch01/learner,ch03/key`.

The layout check compares expanded logical cells, actual Markdown/TeX tables, protected distinctions and frozen teaching content. The export check independently compares complete master prose, actual TeX cells and captions, and the built PDF text. The `--chapter` restriction above is a unit diagnostic; complete-course acceptance uses the unrestricted command in the [shared reproduction instructions](../README.md#reproduction). A later changed build needs fresh visual review bound to its PDF and page-image identities before it replaces an accepted PDF. Do not rerun historical assemblers, register mergers or baseline captures to rebuild exports.

Reproduction outputs and reports remain under `build/`; the build helper does not replace retained PDFs or rewrite the durable acceptance records linked above.

## Original unit acceptance and content scope

The following records the unit's original linguistic acceptance and export evidence. Its page counts, physical table counts, PDF hashes and inspection claims describe that earlier checkpoint, not acceptance of the current presentation revision. The substantive teaching, task and logical-cell counts remain applicable.

At the original export checkpoint: the complete learner PDF has **94 pages** and the separate answer key **45**. Their editable masters are [student.md](../../chapters/ch17/student.md) and [answer-key.md](../../chapters/ch17/answer-key.md). All 139 final pages passed non-author inspection; [page-review.json](page-review.json) binds the final PDFs and page images to the individual inspection ledgers.

The exports include all 103 tasks / 146 answer positions, all 82 assigned Cook prompts, 110 complete bounded systems / 1,234 literal cells, four translated examples, the full 252-word music-performance episode and all 19 original notes / 20 anchors. Original source notes and modern help remain separate. The key gives the complete translation, models, targets, essential meanings, alternatives and diagnoses.

[Full content parity](content-parity.json) verifies 1,724 prose/heading/list blocks, 124 tables and 2,200 table cells including headers. It checks complete Markdown/TeX content and PDF characters alongside visual inspection. The final logs have no missing-character, font-substitution, box or rerun warnings. [Layout adjustments](layout-adjustments.json) retain the repair history. Cambria and the inherited 165 × 241 mm layout remain in use.

The [contract](../../chapters/ch17/coverage.json) preceded prose at `6fc6fc1`. Drafts are saved at `259b14f`, frozen independent solutions at `ed28a8e`, and accepted text at `a137171`. The [fresh text review](../../chapters/ch17/review.md) and [separate paradigm review](../../chapters/ch17/reviews/paradigms.json) resolve material findings. [Authoring amendments](../../chapters/ch17/authoring-amendments.json) preserve the original decisions and later repairs. Complete exports/registers are saved at `99fcc3a`.
