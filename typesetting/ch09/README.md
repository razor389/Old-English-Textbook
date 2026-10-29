# Unit 9 exports

The accepted table-layout revision has a complete [learner PDF](chapter-09.pdf) of **42 pages** and a separate [answer-key PDF](answer-key.pdf) of **26 pages**. The changed pages and heading repairs passed independent visual review.

Current [export identities and page counts](../../docs/revisions/table-layout/exports.json), [page acceptance](../../docs/revisions/table-layout/page-review.json), and the [validated build report](../../docs/revisions/table-layout/build-report.json) document this presentation revision. The [complete-content checks](../../docs/revisions/table-layout/export-text-review.json) and [logical-table review](../../docs/revisions/table-layout/table-review.json) preserve the teaching and source scope.

Editable masters are [student.md](../../chapters/ch09/student.md) and [answer-key.md](../../chapters/ch09/answer-key.md); complete TeX sources are [chapter-09.tex](chapter-09.tex) and [answer-key.tex](answer-key.tex). The [course presentation revision](../../docs/revisions/table-layout/) records the mapping and checks separately from the original unit review.

Tables follow the shared [layout](../book-layout.tex): 10.5-point type with 13.2-point leading, bold headings, horizontal rules and consistent case/person labels. Identical verbal plural cells share `1–3 pl.`; distinct forms remain separate. Counts of grammatical forms and cells describe the complete logical paradigm, which is unchanged by fewer printed rows. Nominal cases, variants, supported uses and teaching milestones retain their stated scope.

## Reproduction

Run from the repository root with the configured TeX Live, Cambria, Xpdf and Ghostscript installation:

```powershell
python -X utf8 scripts/check_course_layout.py --report build/course-layout-check.json
python -X utf8 scripts/build_course_exports.py --stage all --select ch09/learner,ch09/key --include-unchanged --jobs 2 --render-suffix reproduction-01
python -X utf8 scripts/check_course_exports.py --chapter 9 --report build/course-export-ch09-check.json
```

The shared build command compiles each complete document twice, checks table parity and build diagnostics, extracts its text and renders all pages. Choose a fresh `--render-suffix` for a later changed build. Use `--stage inspect` to inspect existing build products without compiling, or `--stage render` to regenerate page images from them. `--select` accepts comma-separated document IDs such as `ch01/learner,ch03/key`.

The layout check compares expanded logical cells, actual Markdown/TeX tables, protected distinctions and frozen teaching content. The export check independently compares complete master prose, actual TeX cells and captions, and the built PDF text. The `--chapter` restriction above is a unit diagnostic; complete-course acceptance uses the unrestricted command in the [shared reproduction instructions](../README.md#reproduction). A later changed build needs fresh visual review bound to its PDF and page-image identities before it replaces an accepted PDF. Do not rerun historical assemblers, register mergers or baseline captures to rebuild exports.

Reproduction outputs and reports remain under `build/`; the build helper does not replace retained PDFs or rewrite the durable acceptance records linked above.

## Original unit acceptance and content scope

The following records the unit's original linguistic acceptance and export evidence. Its page counts, physical table counts, PDF hashes and inspection claims describe that earlier checkpoint, not acceptance of the current presentation revision. The substantive teaching, task and logical-cell counts remain applicable.

At the original export checkpoint: the complete learner PDF has **44 pages**; the separate key has **26**. The editable masters are [student.md](../../chapters/ch09/student.md) and [answer-key.md](../../chapters/ch09/answer-key.md). Both exports contain the complete independently accepted unit, including vocabulary, paradigms, all 97 tasks, both readings, local help and source notes.

All **70 final pages** passed non-author visual inspection. [Individual ledgers](reviews/) retain page-specific observations and exact PDF/image identities. Initial compilation identified twelve horizontal overflows in five noun diagnostic tables. Their column widths were redistributed to fit the complete Old English forms at the unchanged 10.5-point table size; all cell text remains unchanged. Visual proof found one detached vocabulary caption on learner page 12. The caption and its complete table are now bound together on page 13. Both changed pages were directly re-inspected; the other 42 learner images were independently verified byte-identical to their inspected predecessors. All 26 key pages remain the directly inspected v1 images. No master or linguistic text changed. [Final acceptance](page-review.json) reconciles every page, full content parity, unchanged accepted masters and clean build logs. No material presentation issue remains open.

### Original content and review

[Complete parity](content-parity.json) covers **825 prose/heading/list blocks, 78 tables, 1461 table cells including headers, and 607 editorial comments**. An independent Markdown inventory is compared with actual decoded TeX; full prose also matches the extracted PDF character stream after whitespace and soft-hyphen normalization. Every-page inspection includes all tables, endings and special characters.

The learner presents **87 logical paradigms / 876 cells through 57 matrices**. Three new noun classes appear in full. Familiar classes use complete printed models and 54 lexical diagnostic rows: **336 nominal cells are literal and 312 explicitly derived**. All **228 verb cells** are printed. Seventeen complete indicative systems, six command pairs and sēcan subjunctives accompany the bounded complement grammar. Tables do not extend a form's stated sense, syntax or recognition scope.

All **64 original Cook II.9–12 prompts** remain exact, alongside 33 original tasks and twelve translated examples. The **52-word new dialogue**, “The fisherman and his companion,” precedes the exact **62-word, four-turn Choice of Occupations opening**, Cook's *First Book*, p131 / one-based PDF147. Prose lines7–15 are counted editorially with printed10/15 as anchors. All **thirteen original notes and eleven local help groups** remain. The preceding merchandise/price exchange and subsequent smith speech are outside the excerpt. The ivory, living-creatures and 365-day exercise phrases remain explicitly supplied.

The [independent reviewer](../../chapters/ch09/review.md) solved all 97 actual tasks before key/private-answer access. [Frozen solutions](../../chapters/ch09/independent-solutions.md) and the [full ledger](../../chapters/ch09/review-ledger.json) retain the comparison, every paradigm display route, source evidence and resolved findings. The reviewer authored neither master nor graded task and discloses earlier grammar/public-composition work. Witness errors and valid alternatives are adjudicated without rewriting the frozen solutions.

### Original checkpoints

Checkpoints: contract **`aafd2a1`**, complete drafts **`c45cc58`**, pre-key solutions **`72a5b2d`**, accepted text **`7f81e43`**. Complete exports and reviewed registers are saved at **`140e2bd`**. The [handoff](../../docs/HANDOFF.md) records tracker closure and final completion metadata.
