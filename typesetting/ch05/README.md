# Unit 5 exports

The accepted table-layout revision has a complete [learner PDF](chapter-05.pdf) of **26 pages** and a separate [answer-key PDF](answer-key.pdf) of **21 pages**. The changed pages and heading repairs passed independent visual review.

Current [export identities and page counts](../../docs/revisions/table-layout/exports.json), [page acceptance](../../docs/revisions/table-layout/page-review.json), and the [validated build report](../../docs/revisions/table-layout/build-report.json) document this presentation revision. The [complete-content checks](../../docs/revisions/table-layout/export-text-review.json) and [logical-table review](../../docs/revisions/table-layout/table-review.json) preserve the teaching and source scope.

Editable masters are [student.md](../../chapters/ch05/student.md) and [answer-key.md](../../chapters/ch05/answer-key.md); complete TeX sources are [chapter-05.tex](chapter-05.tex) and [answer-key.tex](answer-key.tex). The [course presentation revision](../../docs/revisions/table-layout/) records the mapping and checks separately from the original unit review.

Tables follow the shared [layout](../book-layout.tex): 10.5-point type with 13.2-point leading, bold headings, horizontal rules and consistent case/person labels. Identical verbal plural cells share `1–3 pl.`; distinct forms remain separate. Counts of grammatical forms and cells describe the complete logical paradigm, which is unchanged by fewer printed rows. Nominal cases, variants, supported uses and teaching milestones retain their stated scope.

## Reproduction

Run from the repository root with the configured TeX Live, Cambria, Xpdf and Ghostscript installation:

```powershell
python -X utf8 scripts/check_course_layout.py --report build/course-layout-check.json
python -X utf8 scripts/build_course_exports.py --stage all --select ch05/learner,ch05/key --include-unchanged --jobs 2 --render-suffix reproduction-01
python -X utf8 scripts/check_course_exports.py --chapter 5 --report build/course-export-ch05-check.json
```

The shared build command compiles each complete document twice, checks table parity and build diagnostics, extracts its text and renders all pages. Choose a fresh `--render-suffix` for a later changed build. Use `--stage inspect` to inspect existing build products without compiling, or `--stage render` to regenerate page images from them. `--select` accepts comma-separated document IDs such as `ch01/learner,ch03/key`.

The layout check compares expanded logical cells, actual Markdown/TeX tables, protected distinctions and frozen teaching content. The export check independently compares complete master prose, actual TeX cells and captions, and the built PDF text. The `--chapter` restriction above is a unit diagnostic; complete-course acceptance uses the unrestricted command in the [shared reproduction instructions](../README.md#reproduction). A later changed build needs fresh visual review bound to its PDF and page-image identities before it replaces an accepted PDF. Do not rerun historical assemblers, register mergers or baseline captures to rebuild exports.

Reproduction outputs and reports remain under `build/`; the build helper does not replace retained PDFs or rewrite the durable acceptance records linked above.

## Original unit acceptance and content scope

The following records the unit's original linguistic acceptance and export evidence. Its page counts, physical table counts, PDF hashes and inspection claims describe that earlier checkpoint, not acceptance of the current presentation revision. The substantive teaching, task and logical-cell counts remain applicable.

At the original export checkpoint: the complete learner PDF has **25 pages**; the separate key has **21**. The editable masters are [student.md](../../chapters/ch05/student.md) and [answer-key.md](../../chapters/ch05/answer-key.md). Both exports contain the complete independently accepted unit, including all paradigms, vocabulary, examples, tasks, readings, local help and source notes.

All **46 final pages** passed non-author visual inspection. The [page ledgers](reviews/) retain page-specific observations and image/PDF identities. A page break before the learner's cumulative review keeps X2's supplied citations with its task. Revised pages 22–23 were directly reopened; all other learner images were independently confirmed byte-identical to the previously inspected images. The key required no repair. [Final presentation acceptance](page-review.json) reconciles every page, final artifact identity and clean build log.

### Original complete content and independent review

[Content parity](content-parity.json) compares every Markdown block with the actual TeX: **342 learner and 212 key prose/heading/list blocks**, **19 learner and 34 key tables**, and **600 learner and 306 key table cells including headers**. All **474 editorial comments** are preserved. Complete prose also matches the extracted PDF character stream, with only whitespace and Xpdf soft-hyphen encoding normalized.

The learner displays **33 complete present/preterite indicative systems**, with all three persons singular and plural recoverable: **396 finite cells** and **132 principal-part positions**. The 66 nonfinite positions remain supplied citations. All sixteen unchanged Cook I.5 prompts appear among the **67 graded tasks**. Eight examples, a 51-word new account, the unchanged 69-word first-day revisit and the complete 58-word second-day reading retain their exact text. All 18 local supports and 34 relevant original source notes are included.

The [independent review](../../chapters/ch05/review.md), [frozen pre-key solutions](../../chapters/ch05/independent-solutions.md) and [review ledger](../../chapters/ch05/review-ledger.json) record actual task solving, complete display recovery, source-image checks and every key comparison. No material finding remains. Neither Markdown master nor the frozen solutions changed during typesetting.

### Original checkpoints

The source/contract checkpoint is **`fc29cf9`**, complete drafts **`a28b266`**, frozen pre-key solutions **`d807acf`**, and accepted text **`7bbb334`**. Complete exports and reviewed registers are saved at **`37a52c3`**. The subsequent handoff records final Beads closure and completion metadata without changing the accepted masters or PDFs.
