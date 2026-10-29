# Unit 6 exports

The accepted table-layout revision has a complete [learner PDF](chapter-06.pdf) of **26 pages** and a separate [answer-key PDF](answer-key.pdf) of **27 pages**. The changed pages and heading repairs passed independent visual review.

Current [export identities and page counts](../../docs/revisions/table-layout/exports.json), [page acceptance](../../docs/revisions/table-layout/page-review.json), and the [validated build report](../../docs/revisions/table-layout/build-report.json) document this presentation revision. The [complete-content checks](../../docs/revisions/table-layout/export-text-review.json) and [logical-table review](../../docs/revisions/table-layout/table-review.json) preserve the teaching and source scope.

Editable masters are [student.md](../../chapters/ch06/student.md) and [answer-key.md](../../chapters/ch06/answer-key.md); complete TeX sources are [chapter-06.tex](chapter-06.tex) and [answer-key.tex](answer-key.tex). The [course presentation revision](../../docs/revisions/table-layout/) records the mapping and checks separately from the original unit review.

Tables follow the shared [layout](../book-layout.tex): 10.5-point type with 13.2-point leading, bold headings, horizontal rules and consistent case/person labels. Identical verbal plural cells share `1–3 pl.`; distinct forms remain separate. Counts of grammatical forms and cells describe the complete logical paradigm, which is unchanged by fewer printed rows. Nominal cases, variants, supported uses and teaching milestones retain their stated scope.

## Reproduction

Run from the repository root with the configured TeX Live, Cambria, Xpdf and Ghostscript installation:

```powershell
python -X utf8 scripts/check_course_layout.py --report build/course-layout-check.json
python -X utf8 scripts/build_course_exports.py --stage all --select ch06/learner,ch06/key --include-unchanged --jobs 2 --render-suffix reproduction-01
python -X utf8 scripts/check_course_exports.py --chapter 6 --report build/course-export-ch06-check.json
```

The shared build command compiles each complete document twice, checks table parity and build diagnostics, extracts its text and renders all pages. Choose a fresh `--render-suffix` for a later changed build. Use `--stage inspect` to inspect existing build products without compiling, or `--stage render` to regenerate page images from them. `--select` accepts comma-separated document IDs such as `ch01/learner,ch03/key`.

The layout check compares expanded logical cells, actual Markdown/TeX tables, protected distinctions and frozen teaching content. The export check independently compares complete master prose, actual TeX cells and captions, and the built PDF text. The `--chapter` restriction above is a unit diagnostic; complete-course acceptance uses the unrestricted command in the [shared reproduction instructions](../README.md#reproduction). A later changed build needs fresh visual review bound to its PDF and page-image identities before it replaces an accepted PDF. Do not rerun historical assemblers, register mergers or baseline captures to rebuild exports.

Reproduction outputs and reports remain under `build/`; the build helper does not replace retained PDFs or rewrite the durable acceptance records linked above.

## Original unit acceptance and content scope

The following records the unit's original linguistic acceptance and export evidence. Its page counts, physical table counts, PDF hashes and inspection claims describe that earlier checkpoint, not acceptance of the current presentation revision. The substantive teaching, task and logical-cell counts remain applicable.

At the original export checkpoint: the complete learner PDF has **25 pages**; the separate key has **28**. The editable masters are [student.md](../../chapters/ch06/student.md) and [answer-key.md](../../chapters/ch06/answer-key.md). Both exports contain the complete independently accepted unit: vocabulary, paradigms, explanations, examples, all 72 tasks, both connected readings, local help and source notes.

All **53 final pages** passed non-author visual inspection. The [individual ledgers](reviews/) retain page-specific observations and exact image/PDF identities. The learner's weak-I table has a wider first column to contain gefręmman. The key's final source note [8] is kept together so its original-note quotation does not break across pages 27–28. Both revised key pages were directly reopened; all other key images were independently confirmed byte-identical to the initially inspected images. [Final presentation acceptance](page-review.json) reconciles every page, final artifact identity and clean build log.

### Original complete content and independent review

[Content parity](content-parity.json) compares every Markdown block with the actual TeX: **315 learner and 247 key prose/heading/list blocks**, **13 learner and 37 key tables**, and **439 learner and 585 key table cells including headers**. All **468 editorial comments** are preserved. Complete prose also matches the extracted PDF character stream, with only whitespace and Xpdf soft-hyphen encoding normalized.

The learner teaches ten complete present/preterite indicative systems and the six-cell alternative bēo present: **126 new indicative cells**. It also gives **44 complete imperative pairs** and **46 plain/inflected infinitive pairs**, making **306 new verbal cells** in twelve actual form matrices. The earlier eom series is displayed for comparison with its original milestones. Defective citation labels and unselected forms retain their explicit limits.

All **72 graded tasks** have separate models and explanations. Ten new examples, the **68-word controlled journey dialogue**, and the **76-word fisherman gift/first-direction excerpt** retain their checked wording. The original excerpt includes all ten support groups and three original notes. It is a declared excerpt, not the fisherman's whole speech. Unit 6 adds no numbered Cook exercise assignments; the canonical crosswalk remains 79 assigned and 565 deferred items.

The [independent review](../../chapters/ch06/review.md), [frozen pre-key solutions](../../chapters/ch06/independent-solutions.md) and [review ledger](../../chapters/ch06/review-ledger.json) record actual task solving, complete paradigm recovery, source-image checks and key comparison. All four material findings were resolved before export: the C6/X5 prompt clarifications, X4's subject/agreement explanation, and image-checked metadata for 23 new supplied-only lemmas. Neither Markdown master nor the frozen solutions changed during typesetting.

### Original checkpoints

The source/contract checkpoint is **`3bfc05e`**, complete drafts **`2e2b275`**, frozen pre-key solutions **`f42beb0`**, and accepted text **`3955a2a`**. Complete exports and reviewed registers are saved at **`ce4ee34`**. The subsequent handoff records final Beads closure and completion metadata without changing the accepted masters or PDFs.
