# Unit 11 exports

The accepted table-layout revision has a complete [learner PDF](chapter-11.pdf) of **42 pages** and a separate [answer-key PDF](answer-key.pdf) of **30 pages**. The changed pages and heading repairs passed independent visual review.

Current [export identities and page counts](../../docs/revisions/table-layout/exports.json), [page acceptance](../../docs/revisions/table-layout/page-review.json), and the [validated build report](../../docs/revisions/table-layout/build-report.json) document this presentation revision. The [complete-content checks](../../docs/revisions/table-layout/export-text-review.json) and [logical-table review](../../docs/revisions/table-layout/table-review.json) preserve the teaching and source scope.

Editable masters are [student.md](../../chapters/ch11/student.md) and [answer-key.md](../../chapters/ch11/answer-key.md); complete TeX sources are [chapter-11.tex](chapter-11.tex) and [answer-key.tex](answer-key.tex). The [course presentation revision](../../docs/revisions/table-layout/) records the mapping and checks separately from the original unit review.

Tables follow the shared [layout](../book-layout.tex): 10.5-point type with 13.2-point leading, bold headings, horizontal rules and consistent case/person labels. Identical verbal plural cells share `1–3 pl.`; distinct forms remain separate. Counts of grammatical forms and cells describe the complete logical paradigm, which is unchanged by fewer printed rows. Nominal cases, variants, supported uses and teaching milestones retain their stated scope.

## Reproduction

Run from the repository root with the configured TeX Live, Cambria, Xpdf and Ghostscript installation:

```powershell
python -X utf8 scripts/check_course_layout.py --report build/course-layout-check.json
python -X utf8 scripts/build_course_exports.py --stage all --select ch11/learner,ch11/key --include-unchanged --jobs 2 --render-suffix reproduction-01
python -X utf8 scripts/check_course_exports.py --chapter 11 --report build/course-export-ch11-check.json
```

The shared build command compiles each complete document twice, checks table parity and build diagnostics, extracts its text and renders all pages. Choose a fresh `--render-suffix` for a later changed build. Use `--stage inspect` to inspect existing build products without compiling, or `--stage render` to regenerate page images from them. `--select` accepts comma-separated document IDs such as `ch01/learner,ch03/key`.

The layout check compares expanded logical cells, actual Markdown/TeX tables, protected distinctions and frozen teaching content. The export check independently compares complete master prose, actual TeX cells and captions, and the built PDF text. The `--chapter` restriction above is a unit diagnostic; complete-course acceptance uses the unrestricted command in the [shared reproduction instructions](../README.md#reproduction). A later changed build needs fresh visual review bound to its PDF and page-image identities before it replaces an accepted PDF. Do not rerun historical assemblers, register mergers or baseline captures to rebuild exports.

Reproduction outputs and reports remain under `build/`; the build helper does not replace retained PDFs or rewrite the durable acceptance records linked above.

## Original unit acceptance and content scope

The following records the unit's original linguistic acceptance and export evidence. Its page counts, physical table counts, PDF hashes and inspection claims describe that earlier checkpoint, not acceptance of the current presentation revision. The substantive teaching, task and logical-cell counts remain applicable.

At the original export checkpoint: the complete learner PDF has **42 pages**; the separate key has **31**. Editable masters: [student.md](../../chapters/ch11/student.md) and [answer-key.md](../../chapters/ch11/answer-key.md). All 92 tasks, vocabulary, paradigms, readings, support and source notes are included.

All **73 final pages** passed non-author visual inspection. [Individual ledgers](reviews/) retain page-specific observations and exact PDF/image identities. Wide adjective paradigms use stacked singular/plural panels at unchanged 10.5pt type, with visible strong/weak captions kept with their tables. Independent parity reconstructs the original seven-column coordinates; repeated case labels serve the panel layout. The open-condition context stays with its example and translation. Two key section headings were moved with their first answers. Source notes follow the last short reading task to avoid an almost empty page. All 33 changed learner pages and four changed key pages received fresh visual inspection; the remaining images were verified identical to their inspected predecessors. [Final acceptance](page-review.json) reconciles every final page, complete parity, unchanged accepted masters and clean build logs.

A diagnostic comparison confirmed regular Cambria and its distinct bold face; the heavy appearance of small text in the page images did not indicate a leaked bold setting or font substitution. The proof records retain the diagnostic identities and the withdrawn concern. The shared layout and font settings were not changed.

### Original content and review

[Complete parity](content-parity.json) covers **860 prose/heading/list blocks, 52 tables, 1075 cells including headers, and 607 editorial comments**. An independent Markdown inventory matches decoded TeX; full prose matches extracted PDF text after whitespace and soft-hyphen normalization. Visual review includes tables, endings and special characters.

The learner gives **61 complete defined systems / 826 cells**, with 38 marked matrices and 38 lexical diagnostic rows: 486 literal cells and 340 explicit model derivations. Exceptional patterns are printed in full. A further four-cell Hǣlend title table repeats its assigned singular forms. The full morphology retains its stated lexical and syntactic limits.

All **46 Cook IV.16–17/V.18 prompts** preserve their wording and identifiers, alongside 46 original tasks and fourteen translated examples. The **59-word new account** prepares two exact source spans: the **35-word Britain metals-and-jet passage**, Cook p139 / one-based PDF155, editorial lines 1–4, and the complete **195-word sea-rescue episode**, pp142–143 / PDF158–159, editorial lines 142.8–143.14. The dash in the Britain span is punctuation. All 32 attached original notes, one referenced note and 21 reading helps remain. Five Cook expressions retain local support. Preceding storm context appears separately in English.

The [reviewer](../../chapters/ch11/review.md) solved all 92 actual tasks, including 104 morphology outputs and three complete translations, before key/private-answer access. [Frozen solutions](../../chapters/ch11/independent-solutions.md) and the [ledger](../../chapters/ch11/review-ledger.json) retain the comparison, source checks and adjudications. The reviewer authored neither master nor graded task and discloses earlier grammar/public-composition work. A separate [non-author paradigm review](../../chapters/ch11/reviews/paradigms.json) checks all 826 actual display routes against primary evidence. No material finding remains open.

Amendment **U11-AMEND-01** binds Cook 17.17 to the relative form actually taught in Unit 8. **U11-AMEND-02** corrects three newly introduced weak genitive-plural cells from blacra to **blæcra**, following Cook §§57.2,60 and Wright §§424–425,440. **U11-AMEND-03** adds a compact note on the already evidenced and key-accepted contracted participles fēd/hȳd alongside the selected fēded/hȳded bases. **U11-AMEND-04** makes eleven canonical adjective-table titles visible in the editable learner and export. The reviewer independently verified that removing only those captions restores the earlier accepted learner bytes exactly; initial acceptance at `8c21a9a` is preserved alongside the final caption supplement. The original audit and frozen witness remain preserved; the review adjudicates the witness's inherited explanation explicitly. Task wording, required outputs and teaching milestones are unchanged.

### Original checkpoints

Checkpoints: contract **`a9c6ce5`**, complete drafts **`730dffe`**, pre-key solutions **`f2b3974`**, accepted text **`460b825`**. Complete exports and reviewed registers are saved at **`b096aca`**. The [handoff](../../docs/HANDOFF.md) records final closure.
