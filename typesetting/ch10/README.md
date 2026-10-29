# Unit 10 exports

The accepted table-layout revision has a complete [learner PDF](chapter-10.pdf) of **40 pages** and a separate [answer-key PDF](answer-key.pdf) of **29 pages**. The changed pages and heading repairs passed independent visual review.

Current [export identities and page counts](../../docs/revisions/table-layout/exports.json), [page acceptance](../../docs/revisions/table-layout/page-review.json), and the [validated build report](../../docs/revisions/table-layout/build-report.json) document this presentation revision. The [complete-content checks](../../docs/revisions/table-layout/export-text-review.json) and [logical-table review](../../docs/revisions/table-layout/table-review.json) preserve the teaching and source scope.

Editable masters are [student.md](../../chapters/ch10/student.md) and [answer-key.md](../../chapters/ch10/answer-key.md); complete TeX sources are [chapter-10.tex](chapter-10.tex) and [answer-key.tex](answer-key.tex). The [course presentation revision](../../docs/revisions/table-layout/) records the mapping and checks separately from the original unit review.

Tables follow the shared [layout](../book-layout.tex): 10.5-point type with 13.2-point leading, bold headings, horizontal rules and consistent case/person labels. Identical verbal plural cells share `1–3 pl.`; distinct forms remain separate. Counts of grammatical forms and cells describe the complete logical paradigm, which is unchanged by fewer printed rows. Nominal cases, variants, supported uses and teaching milestones retain their stated scope.

## Reproduction

Run from the repository root with the configured TeX Live, Cambria, Xpdf and Ghostscript installation:

```powershell
python -X utf8 scripts/check_course_layout.py --report build/course-layout-check.json
python -X utf8 scripts/build_course_exports.py --stage all --select ch10/learner,ch10/key --include-unchanged --jobs 2 --render-suffix reproduction-01
python -X utf8 scripts/check_course_exports.py --chapter 10 --report build/course-export-ch10-check.json
```

The shared build command compiles each complete document twice, checks table parity and build diagnostics, extracts its text and renders all pages. Choose a fresh `--render-suffix` for a later changed build. Use `--stage inspect` to inspect existing build products without compiling, or `--stage render` to regenerate page images from them. `--select` accepts comma-separated document IDs such as `ch01/learner,ch03/key`.

The layout check compares expanded logical cells, actual Markdown/TeX tables, protected distinctions and frozen teaching content. The export check independently compares complete master prose, actual TeX cells and captions, and the built PDF text. The `--chapter` restriction above is a unit diagnostic; complete-course acceptance uses the unrestricted command in the [shared reproduction instructions](../README.md#reproduction). A later changed build needs fresh visual review bound to its PDF and page-image identities before it replaces an accepted PDF. Do not rerun historical assemblers, register mergers or baseline captures to rebuild exports.

Reproduction outputs and reports remain under `build/`; the build helper does not replace retained PDFs or rewrite the durable acceptance records linked above.

## Original unit acceptance and content scope

The following records the unit's original linguistic acceptance and export evidence. Its page counts, physical table counts, PDF hashes and inspection claims describe that earlier checkpoint, not acceptance of the current presentation revision. The substantive teaching, task and logical-cell counts remain applicable.

At the original export checkpoint: the complete learner PDF has **40 pages**; the separate key has **29**. The editable masters are [student.md](../../chapters/ch10/student.md) and [answer-key.md](../../chapters/ch10/answer-key.md). All 89 tasks, vocabulary, paradigms, readings, local help and source notes are included.

All **69 final pages** passed non-author visual inspection. [Individual ledgers](reviews/) retain page-specific observations and exact PDF/image identities. Wide adjective paradigms use stacked singular/plural panels at unchanged 10.5pt type. Independent parity reconstructs every original seven-column coordinate; repeated case labels are page furniture. The long unnan key entry permits natural page breaks between complete tables and commentary. Task labels remain with their prompts or answers. Five table widths were redistributed after initial box diagnostics; all linguistic content, headers, cells and accepted Markdown remain unchanged. Non-author proof found four stranded key section headings. TeX-only page breaks place each with its first answer. All eight changed key pages were directly reinspected, and the other 21 final key images were independently verified byte-identical to their inspected predecessors. All 40 learner pages retain direct v1 inspection. [Final acceptance](page-review.json) reconciles every page, full content parity, unchanged accepted masters and clean build logs.

### Original content and review

[Complete parity](content-parity.json) covers **775 prose/heading/list blocks, 49 tables, 1205 cells including headers, and 546 editorial comments**. An independent Markdown inventory matches decoded TeX; full prose matches extracted PDF text after whitespace and soft-hyphen normalization. Visual review includes all tables, endings and special characters.

The learner gives **56 defined paradigms / 779 supported cells** through 36 matrices and 29 lexical diagnostic rows: 306 literal nominal cells, 336 explicit model derivations and 137 literal grammar cells. Exceptional fæder, hand and gāt are printed in full. Unnan retains a visible gap for the unsupported present second singular, with no invented form. Complete forms retain their stated lexical and syntactic scope.

All **55 Cook III.13–15 prompts** retain their wording and identifiers, alongside 34 original tasks and fourteen translated examples. The **50-word new account**, “The stranger and the monk,” precedes the exact **59-word Judgment opening**, Cook p134 / one-based PDF150, editorial lines1–7 anchored by printed5. All fourteen original notes and nine source helps remain. Two exercise expressions remain supplied. The following royal speech is outside the assignment.

The [reviewer](../../chapters/ch10/review.md) solved all 89 actual tasks before key/private-answer access. [Frozen solutions](../../chapters/ch10/independent-solutions.md) and the [ledger](../../chapters/ch10/review-ledger.json) retain the comparison, actual display routes, fresh source checks and resolved findings. The reviewer authored neither master nor graded task and discloses earlier grammar/public-composition work. No material finding remains open.

Review amendment **U10-AMEND-01** completes the instrumental and adjective locators as Cook §§174–178, pp97–99, and §§55–60, pp38–41, and synchronizes the supplied **swā lange swā** scope with its already printed *inasmuch as* interpretation. Original audit annotations remain preserved; assignments and teaching statuses do not change.

### Original checkpoints

Checkpoints: contract **`86e073f`**, complete drafts **`a1f8d6f`**, pre-key solutions **`3684087`**, accepted text **`08ed659`**. Complete exports and reviewed registers are saved at **`126e927`**. The [handoff](../../docs/HANDOFF.md) records final closure.
