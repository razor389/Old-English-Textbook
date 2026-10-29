# Unit 13 exports

The accepted table-layout revision has a complete [learner PDF](chapter-13.pdf) of **51 pages** and a separate [answer-key PDF](answer-key.pdf) of **30 pages**. The changed pages and heading repairs passed independent visual review.

Current [export identities and page counts](../../docs/revisions/table-layout/exports.json), [page acceptance](../../docs/revisions/table-layout/page-review.json), and the [validated build report](../../docs/revisions/table-layout/build-report.json) document this presentation revision. The [complete-content checks](../../docs/revisions/table-layout/export-text-review.json) and [logical-table review](../../docs/revisions/table-layout/table-review.json) preserve the teaching and source scope.

Editable masters are [student.md](../../chapters/ch13/student.md) and [answer-key.md](../../chapters/ch13/answer-key.md); complete TeX sources are [chapter-13.tex](chapter-13.tex) and [answer-key.tex](answer-key.tex). The [course presentation revision](../../docs/revisions/table-layout/) records the mapping and checks separately from the original unit review.

Tables follow the shared [layout](../book-layout.tex): 10.5-point type with 13.2-point leading, bold headings, horizontal rules and consistent case/person labels. Identical verbal plural cells share `1–3 pl.`; distinct forms remain separate. Counts of grammatical forms and cells describe the complete logical paradigm, which is unchanged by fewer printed rows. Nominal cases, variants, supported uses and teaching milestones retain their stated scope.

## Reproduction

Run from the repository root with the configured TeX Live, Cambria, Xpdf and Ghostscript installation:

```powershell
python -X utf8 scripts/check_course_layout.py --report build/course-layout-check.json
python -X utf8 scripts/build_course_exports.py --stage all --select ch13/learner,ch13/key --include-unchanged --jobs 2 --render-suffix reproduction-01
python -X utf8 scripts/check_course_exports.py --chapter 13 --report build/course-export-ch13-check.json
```

The shared build command compiles each complete document twice, checks table parity and build diagnostics, extracts its text and renders all pages. Choose a fresh `--render-suffix` for a later changed build. Use `--stage inspect` to inspect existing build products without compiling, or `--stage render` to regenerate page images from them. `--select` accepts comma-separated document IDs such as `ch01/learner,ch03/key`.

The layout check compares expanded logical cells, actual Markdown/TeX tables, protected distinctions and frozen teaching content. The export check independently compares complete master prose, actual TeX cells and captions, and the built PDF text. The `--chapter` restriction above is a unit diagnostic; complete-course acceptance uses the unrestricted command in the [shared reproduction instructions](../README.md#reproduction). A later changed build needs fresh visual review bound to its PDF and page-image identities before it replaces an accepted PDF. Do not rerun historical assemblers, register mergers or baseline captures to rebuild exports.

Reproduction outputs and reports remain under `build/`; the build helper does not replace retained PDFs or rewrite the durable acceptance records linked above.

## Original unit acceptance and content scope

The following records the unit's original linguistic acceptance and export evidence. Its page counts, physical table counts, PDF hashes and inspection claims describe that earlier checkpoint, not acceptance of the current presentation revision. The substantive teaching, task and logical-cell counts remain applicable.

At the original export checkpoint: the complete learner PDF has **52 pages**; the separate key has **30**. Editable masters: [student.md](../../chapters/ch13/student.md) and [answer-key.md](../../chapters/ch13/answer-key.md). All 90 tasks, vocabulary, defined paradigms, readings, support and original notes are included.

All **82 final pages** passed non-author visual inspection. [Individual ledgers](reviews/) retain page-specific observations and actual PDF/image identities. Wide adjective tables use stacked singular/plural panels at 10.5pt type; the nominal diagnostic table uses linked panels for stems/models and oblique forms. Every original table coordinate remains in the parity reconstruction. [Final acceptance](page-review.json) reconciles all pages, complete parity, unchanged accepted masters and clean logs. The ledgers record actual repairs and reinspections.

### Original content and review

[Complete parity](content-parity.json) covers **805 prose/heading/list blocks, 67 tables, 1,861 cells including headers, and 838 editorial comments**. An independent Markdown inventory matches decoded TeX; full prose matches extracted PDF text after whitespace and soft-hyphen normalization. Visual review includes all tables, endings and special characters.

The learner gives 76 complete defined systems / 1,008 cells in 43 matrices: 562 literal cells and 446 explicit shared-model derivations. Complete paradigms retain their lexical and syntactic limits. All 52 Cook VII.22–25 prompts preserve their wording and IDs, alongside 38 original tasks and twelve translated examples. The 87-word new account prepares the exact 236-word music-and-summons episode from Chad, printed 152.3–153.9 partial / one-based PDF 168–169. All 24 notes and 29 attachments remain, with eighteen reading helps and fourteen Cook help groups.

The fresh [reviewer](../../chapters/ch13/review.md) froze [all solutions](../../chapters/ch13/independent-solutions.md) before key/private-analysis access. A separate [fresh paradigm reviewer](../../chapters/ch13/reviews/paradigms.json) checked every cell route against actual displays and primary evidence. Neither authored a master or graded task. Canonical amendments record accepted source-support and relative-target repairs; original audit records and the frozen witness remain unchanged. No material finding is open.

### Original checkpoints

Checkpoints: contract **`40bb0ba`**, complete drafts **`23199c1`**, blind solutions **`d31c692`**, accepted text **`aec6c7f`**. Complete exports/registers: **`85b6911`**. The [handoff](../../docs/HANDOFF.md) records final closure.
