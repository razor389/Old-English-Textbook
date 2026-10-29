# Unit 15 exports

The accepted table-layout revision has a complete [learner PDF](chapter-15.pdf) of **63 pages** and a separate [answer-key PDF](answer-key.pdf) of **30 pages**. The changed pages and heading repairs passed independent visual review.

Current [export identities and page counts](../../docs/revisions/table-layout/exports.json), [page acceptance](../../docs/revisions/table-layout/page-review.json), and the [validated build report](../../docs/revisions/table-layout/build-report.json) document this presentation revision. The [complete-content checks](../../docs/revisions/table-layout/export-text-review.json) and [logical-table review](../../docs/revisions/table-layout/table-review.json) preserve the teaching and source scope.

Editable masters are [student.md](../../chapters/ch15/student.md) and [answer-key.md](../../chapters/ch15/answer-key.md); complete TeX sources are [chapter-15.tex](chapter-15.tex) and [answer-key.tex](answer-key.tex). The [course presentation revision](../../docs/revisions/table-layout/) records the mapping and checks separately from the original unit review.

Tables follow the shared [layout](../book-layout.tex): 10.5-point type with 13.2-point leading, bold headings, horizontal rules and consistent case/person labels. Identical verbal plural cells share `1–3 pl.`; distinct forms remain separate. Counts of grammatical forms and cells describe the complete logical paradigm, which is unchanged by fewer printed rows. Nominal cases, variants, supported uses and teaching milestones retain their stated scope.

## Reproduction

Run from the repository root with the configured TeX Live, Cambria, Xpdf and Ghostscript installation:

```powershell
python -X utf8 scripts/check_course_layout.py --report build/course-layout-check.json
python -X utf8 scripts/build_course_exports.py --stage all --select ch15/learner,ch15/key --include-unchanged --jobs 2 --render-suffix reproduction-01
python -X utf8 scripts/check_course_exports.py --chapter 15 --report build/course-export-ch15-check.json
```

The shared build command compiles each complete document twice, checks table parity and build diagnostics, extracts its text and renders all pages. Choose a fresh `--render-suffix` for a later changed build. Use `--stage inspect` to inspect existing build products without compiling, or `--stage render` to regenerate page images from them. `--select` accepts comma-separated document IDs such as `ch01/learner,ch03/key`.

The layout check compares expanded logical cells, actual Markdown/TeX tables, protected distinctions and frozen teaching content. The export check independently compares complete master prose, actual TeX cells and captions, and the built PDF text. The `--chapter` restriction above is a unit diagnostic; complete-course acceptance uses the unrestricted command in the [shared reproduction instructions](../README.md#reproduction). A later changed build needs fresh visual review bound to its PDF and page-image identities before it replaces an accepted PDF. Do not rerun historical assemblers, register mergers or baseline captures to rebuild exports.

Reproduction outputs and reports remain under `build/`; the build helper does not replace retained PDFs or rewrite the durable acceptance records linked above.

## Original unit acceptance and content scope

The following records the unit's original linguistic acceptance and export evidence. Its page counts, physical table counts, PDF hashes and inspection claims describe that earlier checkpoint, not acceptance of the current presentation revision. The substantive teaching, task and logical-cell counts remain applicable.

At the original export checkpoint: the complete learner PDF has **64 pages**; the separate key has **30**. Editable masters: [student.md](../../chapters/ch15/student.md) and [answer-key.md](../../chapters/ch15/answer-key.md). All 105 tasks, vocabulary, complete defined paradigms, three connected readings, support and original notes are included.

All **94 final pages** passed non-author visual inspection. [Individual ledgers](reviews/) retain page-specific observations and final PDF/image identities. [Final acceptance](page-review.json) reconciles every page, complete parity, unchanged accepted masters and clean logs. [Layout adjustments](layout-adjustments.json) record the actual repairs and reinspection history. Byte-identical page reuse identifies the specific previously inspected image.

### Original content and review

[Complete parity](content-parity.json) covers **1154 prose/heading/list blocks, 96 tables, 1,772 cells including headers, and 1806 editorial comments**. An independent Markdown inventory matches decoded TeX; full prose matches extracted PDF text after whitespace and soft-hyphen normalization. Original note references retain D/P/R-prefixed numbers, with general source notes numbered separately. Every definition remains. Visual review includes actual tables, endings and special characters.

The learner gives 69 defined systems / 691 positions, comprising 675 form/expression cells and 16 explicitly unassigned slots. All 50 Cook IX.28–30 and joint X, XI.31 prompts retain wording and IDs, alongside 55 original tasks and eight examples. The three exact source readings total 415 words and retain 27 notes / 33 anchors, 114 reading helps and 36 Cook help groups. The continuation of Duties on pp. 160–161 remains unassigned.

The fresh [reviewer](../../chapters/ch15/review.md) froze [all solutions](../../chapters/ch15/independent-solutions.md) before key/current-contract/audit access. A separate [fresh paradigm reviewer](../../chapters/ch15/reviews/paradigms.json) checked every position and rule against primary evidence. Neither authored a master or task. Canonical amendments preserve corrections separately from sealed packets and the unchanged blind witness. No material finding is open.

### Original checkpoints

Checkpoints: contract **`ff7f7c8`**, drafts **`3822d4b`**, blind solutions **`ecbdc44`**, accepted text **`0ec6ae3`**. Complete exports/registers: **`a80bf34`**. The [handoff](../../docs/HANDOFF.md) records final closure.
