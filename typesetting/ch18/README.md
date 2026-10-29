# Unit 18 exports: independent prose consolidation

The accepted table-layout revision has a complete [learner PDF](chapter-18.pdf) of **64 pages** and a separate [answer-key PDF](answer-key.pdf) of **32 pages**. The changed pages and heading repairs passed independent visual review. The key is byte-unchanged from its accepted export; only the learner PDF was rebuilt.

Current [export identities and page counts](../../docs/revisions/table-layout/exports.json), [page acceptance](../../docs/revisions/table-layout/page-review.json), and the [validated build report](../../docs/revisions/table-layout/build-report.json) document this presentation revision. The [complete-content checks](../../docs/revisions/table-layout/export-text-review.json) and [logical-table review](../../docs/revisions/table-layout/table-review.json) preserve the teaching and source scope.

Editable masters are [student.md](../../chapters/ch18/student.md) and [answer-key.md](../../chapters/ch18/answer-key.md); complete TeX sources are [chapter-18.tex](chapter-18.tex) and [answer-key.tex](answer-key.tex). The [course presentation revision](../../docs/revisions/table-layout/) records the mapping and checks separately from the original unit review.

Tables follow the shared [layout](../book-layout.tex): 10.5-point type with 13.2-point leading, bold headings, horizontal rules and consistent case/person labels. Identical verbal plural cells share `1–3 pl.`; distinct forms remain separate. Counts of grammatical forms and cells describe the complete logical paradigm, which is unchanged by fewer printed rows. Nominal cases, variants, supported uses and teaching milestones retain their stated scope.

## Reproduction

Run from the repository root with the configured TeX Live, Cambria, Xpdf and Ghostscript installation:

```powershell
python -X utf8 scripts/check_course_layout.py --report build/course-layout-check.json
python -X utf8 scripts/build_course_exports.py --stage all --select ch18/learner,ch18/key --include-unchanged --jobs 2 --render-suffix reproduction-01
python -X utf8 scripts/check_course_exports.py --chapter 18 --report build/course-export-ch18-check.json
```

The shared build command compiles each complete document twice, checks table parity and build diagnostics, extracts its text and renders all pages. Choose a fresh `--render-suffix` for a later changed build. Use `--stage inspect` to inspect existing build products without compiling, or `--stage render` to regenerate page images from them. `--select` accepts comma-separated document IDs such as `ch01/learner,ch03/key`.

The layout check compares expanded logical cells, actual Markdown/TeX tables, protected distinctions and frozen teaching content. The export check independently compares complete master prose, actual TeX cells and captions, and the built PDF text. The `--chapter` restriction above is a unit diagnostic; complete-course acceptance uses the unrestricted command in the [shared reproduction instructions](../README.md#reproduction). A later changed build needs fresh visual review bound to its PDF and page-image identities before it replaces an accepted PDF. Do not rerun historical assemblers, register mergers or baseline captures to rebuild exports.

Reproduction outputs and reports remain under `build/`; the build helper does not replace retained PDFs or rewrite the durable acceptance records linked above.

## Original unit acceptance and content scope

The following records the unit's original linguistic acceptance and export evidence. Its page counts, physical table counts, PDF hashes and inspection claims describe that earlier checkpoint, not acceptance of the current presentation revision. The substantive teaching, task and logical-cell counts remain applicable.

At the original export checkpoint: the complete learner PDF has **66 pages**; the separate key has **32**. Editable masters are [student.md](../../chapters/ch18/student.md) and [answer-key.md](../../chapters/ch18/answer-key.md). All 98 final pages passed actual non-author visual inspection; [page-review.json](page-review.json) binds both PDFs and every page image to individual inspection ledgers.

Both exports retain 60 tasks / 87 requested answers, all 47 final Cook prompts, 55 defined systems / 652 literal cells, two translated examples, the full 226-word passage and all 22 original notes / 29 anchors. The separate key gives models, targets, meanings, explanations, alternatives and diagnoses. [Full parity](content-parity.json) checks 1,221 prose/heading/list blocks, 65 tables and 1,224 table cells. Final logs have no missing-character, font-substitution, box or rerun warnings. [Layout adjustments](layout-adjustments.json) preserve repairs. Cambria and the established 165 × 241 mm layout remain.

Checkpoints: contract `6874c20e7127fa33c41406d1aa6c0b087e59c824`, complete drafts `970fcc1f431f6ce2ccdd1f1c85b2b5e63ae0c16a`, frozen independent solutions `7846befc2c484e8d3e4ff43346da12bf275f5b08`, accepted text `029177713dffa6ff81b81d9a96b41b36e006963f`, complete exports/registers `52ff433bb80c6cf3bf245c5533cdd396362b443f`. [Fresh text review](../../chapters/ch18/review.md), [separate paradigm review](../../chapters/ch18/reviews/paradigms.json) and [amendments](../../chapters/ch18/authoring-amendments.json) retain evidence and resolutions.
