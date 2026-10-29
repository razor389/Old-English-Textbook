# Unit 4 exports

The accepted table-layout revision has a complete [learner PDF](chapter-04.pdf) of **21 pages** and a separate [answer-key PDF](answer-key.pdf) of **18 pages**. The changed pages and heading repairs passed independent visual review.

Current [export identities and page counts](../../docs/revisions/table-layout/exports.json), [page acceptance](../../docs/revisions/table-layout/page-review.json), and the [validated build report](../../docs/revisions/table-layout/build-report.json) document this presentation revision. The [complete-content checks](../../docs/revisions/table-layout/export-text-review.json) and [logical-table review](../../docs/revisions/table-layout/table-review.json) preserve the teaching and source scope.

Editable masters are [student.md](../../chapters/ch04/student.md) and [answer-key.md](../../chapters/ch04/answer-key.md); complete TeX sources are [chapter-04.tex](chapter-04.tex) and [answer-key.tex](answer-key.tex). The [course presentation revision](../../docs/revisions/table-layout/) records the mapping and checks separately from the original unit review.

Tables follow the shared [layout](../book-layout.tex): 10.5-point type with 13.2-point leading, bold headings, horizontal rules and consistent case/person labels. Identical verbal plural cells share `1–3 pl.`; distinct forms remain separate. Counts of grammatical forms and cells describe the complete logical paradigm, which is unchanged by fewer printed rows. Nominal cases, variants, supported uses and teaching milestones retain their stated scope.

## Reproduction

Run from the repository root with the configured TeX Live, Cambria, Xpdf and Ghostscript installation:

```powershell
python -X utf8 scripts/check_course_layout.py --report build/course-layout-check.json
python -X utf8 scripts/build_course_exports.py --stage all --select ch04/learner,ch04/key --include-unchanged --jobs 2 --render-suffix reproduction-01
python -X utf8 scripts/check_course_exports.py --chapter 4 --report build/course-export-ch04-check.json
```

The shared build command compiles each complete document twice, checks table parity and build diagnostics, extracts its text and renders all pages. Choose a fresh `--render-suffix` for a later changed build. Use `--stage inspect` to inspect existing build products without compiling, or `--stage render` to regenerate page images from them. `--select` accepts comma-separated document IDs such as `ch01/learner,ch03/key`.

The layout check compares expanded logical cells, actual Markdown/TeX tables, protected distinctions and frozen teaching content. The export check independently compares complete master prose, actual TeX cells and captions, and the built PDF text. The `--chapter` restriction above is a unit diagnostic; complete-course acceptance uses the unrestricted command in the [shared reproduction instructions](../README.md#reproduction). A later changed build needs fresh visual review bound to its PDF and page-image identities before it replaces an accepted PDF. Do not rerun historical assemblers, register mergers or baseline captures to rebuild exports.

Reproduction outputs and reports remain under `build/`; the build helper does not replace retained PDFs or rewrite the durable acceptance records linked above.

## Original unit acceptance and content scope

The following records the unit's original linguistic acceptance and export evidence. Its page counts, physical table counts, PDF hashes and inspection claims describe that earlier checkpoint, not acceptance of the current presentation revision. The substantive teaching, task and logical-cell counts remain applicable.

At the original export checkpoint: the complete learner PDF has **20 pages**; the separate key has **19**. The editable masters are [student.md](../../chapters/ch04/student.md) and [answer-key.md](../../chapters/ch04/answer-key.md). Both exports include all contracted material: the full selected indicative systems, principal parts, noun tables, 52 tasks, eight examples, both connected readings, local reading help and source notes.

The texts and all **39 final pages** are independently accepted. Every page was visually inspected by a non-author; revised pages were reopened and unchanged images checked for byte identity. The page ledgers under [reviews](reviews/) preserve all findings and their resolutions. Consolidated acceptance and final file identities are recorded in [page-review.json](page-review.json).

### Original content and review

[content-parity.json](content-parity.json) compares every Markdown block with the actual TeX: **233 learner and 161 key prose/heading/list blocks**, **18 learner and 33 key tables**, and **563 learner and 575 key table cells including headers**. All 370 editorial comments are preserved. Complete prose also matches the extracted PDF character stream, with only whitespace and Xpdf soft-hyphen encoding normalized. The learner's three literal error asterisks remain characters.

The learner presents 26 complete finite systems: 24 productive and two recognition references, each with all three persons in singular and plural for present and preterite indicative. The clearly labelled common plural columns recover all **312 finite cells**. All **104 principal-part entries** and **32 noun cells** are included. Nonfinite citations and locally supplied reading forms retain their stated scope.

The [independent review](../../chapters/ch04/review.md) preserves all 52 solutions before key access, complete paradigm recovery and source/dependency checks. Neither master has changed since textual acceptance. Page ledgers identify the PDF and each actual rendered image; revised pages require direct reinspection, while byte-identical images retain their original visual inspection.

### Original checkpoints

The pre-prose source/contract checkpoint is **`856a5fa`**; independently accepted text is **`5f47f26`**; complete exports and integrated registers are saved at **`12663ff`**. The subsequent handoff revision records final Beads closure and completion metadata without changing the accepted masters or PDFs.
