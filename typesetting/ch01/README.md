# Unit 1 exports

The accepted table-layout revision has a complete [learner PDF](chapter-01.pdf) of **21 pages** and a separate [answer-key PDF](answer-key.pdf) of **12 pages**. The changed pages and heading repairs passed independent visual review.

Current [export identities and page counts](../../docs/revisions/table-layout/exports.json), [page acceptance](../../docs/revisions/table-layout/page-review.json), and the [validated build report](../../docs/revisions/table-layout/build-report.json) document this presentation revision. The [complete-content checks](../../docs/revisions/table-layout/export-text-review.json) and [logical-table review](../../docs/revisions/table-layout/table-review.json) preserve the teaching and source scope.

Editable masters are [student.md](../../chapters/ch01/student.md) and [answer-key.md](../../chapters/ch01/answer-key.md); complete TeX sources are [chapter-01.tex](chapter-01.tex) and [answer-key.tex](answer-key.tex). The [course presentation revision](../../docs/revisions/table-layout/) records the mapping and checks separately from the original unit review.

Tables follow the shared [layout](../book-layout.tex): 10.5-point type with 13.2-point leading, bold headings, horizontal rules and consistent case/person labels. Identical verbal plural cells share `1–3 pl.`; distinct forms remain separate. Counts of grammatical forms and cells describe the complete logical paradigm, which is unchanged by fewer printed rows. Nominal cases, variants, supported uses and teaching milestones retain their stated scope.

## Reproduction

Run from the repository root with the configured TeX Live, Cambria, Xpdf and Ghostscript installation:

```powershell
python -X utf8 scripts/check_course_layout.py --report build/course-layout-check.json
python -X utf8 scripts/build_course_exports.py --stage all --select ch01/learner,ch01/key --include-unchanged --jobs 2 --render-suffix reproduction-01
python -X utf8 scripts/check_course_exports.py --chapter 1 --report build/course-export-ch01-check.json
```

The shared build command compiles each complete document twice, checks table parity and build diagnostics, extracts its text and renders all pages. Choose a fresh `--render-suffix` for a later changed build. Use `--stage inspect` to inspect existing build products without compiling, or `--stage render` to regenerate page images from them. `--select` accepts comma-separated document IDs such as `ch01/learner,ch03/key`.

The layout check compares expanded logical cells, actual Markdown/TeX tables, protected distinctions and frozen teaching content. The export check independently compares complete master prose, actual TeX cells and captions, and the built PDF text. The `--chapter` restriction above is a unit diagnostic; complete-course acceptance uses the unrestricted command in the [shared reproduction instructions](../README.md#reproduction). A later changed build needs fresh visual review bound to its PDF and page-image identities before it replaces an accepted PDF. Do not rerun historical assemblers, register mergers or baseline captures to rebuild exports.

Reproduction outputs and reports remain under `build/`; the build helper does not replace retained PDFs or rewrite the durable acceptance records linked above.

## Original unit acceptance and content scope

The following records the unit's original linguistic acceptance and export evidence. Its page counts, physical table counts, PDF hashes and inspection claims describe that earlier checkpoint, not acceptance of the current presentation revision. The substantive teaching, task and logical-cell counts remain applicable.

At the original export checkpoint: complete reviewed exports, 22 October 2026: learner PDF, **22 pages**, and separate key PDF, **12 pages**. Editable masters are [student.md](../../chapters/ch01/student.md) and [answer-key.md](../../chapters/ch01/answer-key.md). Complete TeX sources are [chapter-01.tex](chapter-01.tex) and [answer-key.tex](answer-key.tex), using the shared [layout](../book-layout.tex).

Cambria, 165 × 241 mm trim, 11-point body and 14.3-point leading are retained. Paradigms remain intact. The vocabulary retains all six original fields in four readable columns, with genitive and plural diagnostics on separate lines. Long tables repeat their headings. Case frames and key answer blocks stay together. Old English words are not automatically hyphenated.

### Original complete-content and page checks

The separate content audit compared all 183 learner and 107 key prose/task/note paragraphs, 17 learner and two key tables, all 44 vocabulary entries and their 264 original fields, every reading-help row, all source notes, and the exact 69-word reading. All 92 learner task IDs, 92 key IDs, 79 teaching IDs and eight example IDs survive in TeX comments. The Markdown masters retain their textual-review hashes.

The coordinator and independent reviewer inspected every page, including all paradigms, hooked e, eth/thorn, vowel marks, the starred sea reconstruction, source prompts, reading, explanations and endnotes. Initial pagination repairs kept CASE02/CASE10 help with their frames and two key headings with their content. A later apparent reading-table header issue disappeared in a fresh direct image view; identical bitmap hashes established that no further TeX change was needed. See the [independent page ledger](../../chapters/ch01/review.md) for every page and finding.

After the final additional learner compile, the coordinator rendered all 22 pages again as `build/verified-chapter-01-pNN.png`. Every bitmap SHA-256 matched the inspected `final-chapter-01-pNN.png` series. The key's inspected series is `build/final-answer-key-pNN.png`, pages 01–12. Final PDF copies match the stable build files byte for byte. Both LuaLaTeX logs have no missing-character, font, overfull/underfull box, reference, or table-width warnings. `python -X utf8 scripts/check_unit.py --draft --tex`, run from the repository root, passes.

Xpdf 4.00 inserts some artificial spaces after macron letters in extracted text. The reading-only character comparison ignores whitespace while preserving all other Unicode characters and punctuation; word boundaries were checked visually. Exact Cook prompt checks remain strict. Ghostscript reports missing optional FAPI map files but renders the embedded fonts correctly. Neither limitation requires a spelling or font substitution.

### Original reviewed file identities

SHA-256 of the final PDF bytes:

| File | SHA-256 |
|---|---|
| chapter-01.pdf | `2a59aae475ca3bf98d07d73d7a7af3f9656e5caf2c0c8547e38e9a4f760064d0` |
| answer-key.pdf | `3d5a72d2d5f6f78010235e76dceb6eb5268db24328b102745f439845359d693f` |

Recompilation can change PDF metadata and therefore byte hashes. New output still requires content and page verification before it replaces these reviewed copies.
