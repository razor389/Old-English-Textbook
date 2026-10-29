# Unit 7 exports

The accepted table-layout revision has a complete [learner PDF](chapter-07.pdf) of **39 pages** and a separate [answer-key PDF](answer-key.pdf) of **30 pages**. The changed pages and heading repairs passed independent visual review.

Current [export identities and page counts](../../docs/revisions/table-layout/exports.json), [page acceptance](../../docs/revisions/table-layout/page-review.json), and the [validated build report](../../docs/revisions/table-layout/build-report.json) document this presentation revision. The [complete-content checks](../../docs/revisions/table-layout/export-text-review.json) and [logical-table review](../../docs/revisions/table-layout/table-review.json) preserve the teaching and source scope.

Editable masters are [student.md](../../chapters/ch07/student.md) and [answer-key.md](../../chapters/ch07/answer-key.md); complete TeX sources are [chapter-07.tex](chapter-07.tex) and [answer-key.tex](answer-key.tex). The [course presentation revision](../../docs/revisions/table-layout/) records the mapping and checks separately from the original unit review.

Tables follow the shared [layout](../book-layout.tex): 10.5-point type with 13.2-point leading, bold headings, horizontal rules and consistent case/person labels. Identical verbal plural cells share `1–3 pl.`; distinct forms remain separate. Counts of grammatical forms and cells describe the complete logical paradigm, which is unchanged by fewer printed rows. Nominal cases, variants, supported uses and teaching milestones retain their stated scope.

## Reproduction

Run from the repository root with the configured TeX Live, Cambria, Xpdf and Ghostscript installation:

```powershell
python -X utf8 scripts/check_course_layout.py --report build/course-layout-check.json
python -X utf8 scripts/build_course_exports.py --stage all --select ch07/learner,ch07/key --include-unchanged --jobs 2 --render-suffix reproduction-01
python -X utf8 scripts/check_course_exports.py --chapter 7 --report build/course-export-ch07-check.json
```

The shared build command compiles each complete document twice, checks table parity and build diagnostics, extracts its text and renders all pages. Choose a fresh `--render-suffix` for a later changed build. Use `--stage inspect` to inspect existing build products without compiling, or `--stage render` to regenerate page images from them. `--select` accepts comma-separated document IDs such as `ch01/learner,ch03/key`.

The layout check compares expanded logical cells, actual Markdown/TeX tables, protected distinctions and frozen teaching content. The export check independently compares complete master prose, actual TeX cells and captions, and the built PDF text. The `--chapter` restriction above is a unit diagnostic; complete-course acceptance uses the unrestricted command in the [shared reproduction instructions](../README.md#reproduction). A later changed build needs fresh visual review bound to its PDF and page-image identities before it replaces an accepted PDF. Do not rerun historical assemblers, register mergers or baseline captures to rebuild exports.

Reproduction outputs and reports remain under `build/`; the build helper does not replace retained PDFs or rewrite the durable acceptance records linked above.

## Original unit acceptance and content scope

The following records the unit's original linguistic acceptance and export evidence. Its page counts, physical table counts, PDF hashes and inspection claims describe that earlier checkpoint, not acceptance of the current presentation revision. The substantive teaching, task and logical-cell counts remain applicable.

At the original export checkpoint: the complete learner PDF has **37 pages**; the separate key has **30**. The editable masters are [student.md](../../chapters/ch07/student.md) and [answer-key.md](../../chapters/ch07/answer-key.md). Both exports contain the complete independently accepted unit: vocabulary, paradigms, explanations, examples, all 80 tasks, both connected readings, local help and source notes.

All **67 final pages** passed non-author visual inspection. The [individual ledgers](reviews/) retain page-specific observations, inspection provenance and exact image/PDF identities. Three learner columns and the key's A07 first column were widened before inspection to contain long forms. The sole visual finding, U07-PF01, separated an example from its translation across learner pages 1–2. A TeX-only space reservation keeps them together. Both revised pages were directly reopened; all other 35 learner images were independently verified byte-identical to the inspected version. The key needed no further repair. [Final presentation acceptance](page-review.json) reconciles every page, final identity and clean build log.

### Original complete content and independent review

[Content parity](content-parity.json) compares every Markdown block with the actual TeX: **407 learner and 283 key prose/heading/list blocks**, **46 learner and 18 key tables**, and **1,071 learner and 297 key table cells including headers**. All **499 editorial comments** are preserved. Complete prose also matches the extracted PDF character stream, with only whitespace and Xpdf soft-hyphen encoding normalized.

The learner gives **82 logical paradigms with 1,060 cells**: 56 complete present/preterite subjunctive systems including the alternative bēo present, five new indicative systems, a command pair, twelve participle pairs, five complete strong/weak participle-agreement models, and the full relevant forms of eall, ǣlc and geweald. The 41 actual morphology matrices identify every person, number, case, gender and tense covered by a compact row. Displaying a form does not extend its stated syntactic scope.

All **80 graded tasks** have separate models, targets, explanations, alternatives and diagnoses. The **34 exact Cook prompts** are I.4.18 and all of I.6–7. Eleven new examples and the **56-word connected account**, “Binding the animals,” retain their checked wording. The full **89-word fifth-day Creation paragraph** is Cook's *First Book*, printed p126 / one-based PDF142, editorial prose lines 5–14. All ten local support groups and eighteen original notes, numbered 4–21, are included. The canonical numbered Cook crosswalk is 113 assigned and 531 deferred items, with none omitted or excluded; the earlier birds alias is contained in this source assignment.

The [independent review](../../chapters/ch07/review.md), [frozen pre-key solutions](../../chapters/ch07/independent-solutions.md) and [review ledger](../../chapters/ch07/review-ledger.json) record actual task solving, complete displayed-form checks, source-image evidence and key comparison. The reviewer authored neither master and discloses prior grammar-audit work. The qualified spatial *ofer* explanation was clarified and independently verified against Fulk before textual acceptance. Neither Markdown master nor the frozen solutions changed during export.

### Original checkpoints

Checkpoints: contract before prose **`74404d8`**, complete drafts **`db1ef63`**, frozen pre-key solutions **`aa31f25`**, accepted text **`089039d`**. Complete exports and reviewed registers are saved at **`b186c8b`**. The subsequent [handoff](../../docs/HANDOFF.md) records final Beads closure and completion metadata without changing accepted masters or PDFs.
