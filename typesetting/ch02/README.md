# Unit 2 complete exports

The accepted table-layout revision has a complete [learner PDF](chapter-02.pdf) of **20 pages** and a separate [answer-key PDF](answer-key.pdf) of **14 pages**. The changed pages and heading repairs passed independent visual review.

Current [export identities and page counts](../../docs/revisions/table-layout/exports.json), [page acceptance](../../docs/revisions/table-layout/page-review.json), and the [validated build report](../../docs/revisions/table-layout/build-report.json) document this presentation revision. The [complete-content checks](../../docs/revisions/table-layout/export-text-review.json) and [logical-table review](../../docs/revisions/table-layout/table-review.json) preserve the teaching and source scope.

Editable masters are [student.md](../../chapters/ch02/student.md) and [answer-key.md](../../chapters/ch02/answer-key.md); complete TeX sources are [chapter-02.tex](chapter-02.tex) and [answer-key.tex](answer-key.tex). The [course presentation revision](../../docs/revisions/table-layout/) records the mapping and checks separately from the original unit review.

Tables follow the shared [layout](../book-layout.tex): 10.5-point type with 13.2-point leading, bold headings, horizontal rules and consistent case/person labels. Identical verbal plural cells share `1–3 pl.`; distinct forms remain separate. Counts of grammatical forms and cells describe the complete logical paradigm, which is unchanged by fewer printed rows. Nominal cases, variants, supported uses and teaching milestones retain their stated scope.

## Reproduction

Run from the repository root with the configured TeX Live, Cambria, Xpdf and Ghostscript installation:

```powershell
python -X utf8 scripts/check_course_layout.py --report build/course-layout-check.json
python -X utf8 scripts/build_course_exports.py --stage all --select ch02/learner,ch02/key --include-unchanged --jobs 2 --render-suffix reproduction-01
python -X utf8 scripts/check_course_exports.py --chapter 2 --report build/course-export-ch02-check.json
```

The shared build command compiles each complete document twice, checks table parity and build diagnostics, extracts its text and renders all pages. Choose a fresh `--render-suffix` for a later changed build. Use `--stage inspect` to inspect existing build products without compiling, or `--stage render` to regenerate page images from them. `--select` accepts comma-separated document IDs such as `ch01/learner,ch03/key`.

The layout check compares expanded logical cells, actual Markdown/TeX tables, protected distinctions and frozen teaching content. The export check independently compares complete master prose, actual TeX cells and captions, and the built PDF text. The `--chapter` restriction above is a unit diagnostic; complete-course acceptance uses the unrestricted command in the [shared reproduction instructions](../README.md#reproduction). A later changed build needs fresh visual review bound to its PDF and page-image identities before it replaces an accepted PDF. Do not rerun historical assemblers, register mergers or baseline captures to rebuild exports.

Reproduction outputs and reports remain under `build/`; the build helper does not replace retained PDFs or rewrite the durable acceptance records linked above.

## Original unit acceptance and content scope

The following records the unit's original linguistic acceptance and export evidence. Its page counts, physical table counts, PDF hashes and inspection claims describe that earlier checkpoint, not acceptance of the current presentation revision. The substantive teaching, task and logical-cell counts remain applicable.

At the original export checkpoint: the learner chapter has 19 pages; the separate answer key has 14. Their complete, hand-reviewed TeX sources are [chapter-02.tex](chapter-02.tex) and [answer-key.tex](answer-key.tex). The editorial masters are [student.md](../../chapters/ch02/student.md) and [answer-key.md](../../chapters/ch02/answer-key.md). The accepted text was not changed during typesetting.

The inherited [Cambria layout](../book-layout.tex) is unchanged: 165 × 241 mm trim, 11-point body text, 14.3-point leading. The seven wide finite-verb tables are displayed as paired present and preterite panels at 10.5 points with 13.2-point leading. Each pair retains the original complete row, with the verb label repeated. All exercise prompts and each key answer with its table and explanations are kept together. Vocabulary and principal-part tables repeat their headers when continued. The connected narrative and complete source reading retain the larger reading style. All 17 learner source notes and the key’s source note and concluding bibliography paragraph are present.

### Original verified identities

| File | SHA-256 |
| --- | --- |
| Accepted learner Markdown | `7ac884d55c143f1e5ce6d5eead3b09ec11ea9121cb5f23f4c96e0a9addb0dea2` |
| Accepted key Markdown | `d857f67bf3ee98905dea2b9cbccf21f3f4d88644c3f81e499d18a661c097bdf5` |
| `chapter-02.pdf` | `54eddab2d7f2284a6e4bd82c5da34cb1fd71baa7af11e7db576ada41b10b3a0d` |
| `answer-key.pdf` | `d9ef81ef44157f08d4e9f1e1a450eaa761b30031c986ecbb61608534df3c1608` |

The tracked PDFs are byte-identical copies of the inspected files in `build/`. Copying occurred only after all pages passed the typesetter, coordinator and independent reviewer. No recompilation occurred after the approved image set was made. PDF metadata may change a byte hash on a later rebuild; the frozen identities above identify the reviewed copies.

In `content-parity.json`, `tex_sha256` identifies the compiled working-file bytes, which have CRLF line endings. `.gitattributes` normalizes TeX to LF in Git; the companion `tex_sha256_normalized_lf` identifies the same content with CRLF converted to LF, as found in an LF checkout. Both identities are retained. Adding this metadata did not change the TeX or PDF bytes or require recompilation.

### Original content and page checks

[content-parity.json](content-parity.json) records the full comparison with the accepted Markdown. An independent inventory of the masters was compared with decoded bodies of the actual TeX, without using the assembly helper’s generated content maps:

- Learner: 175 paragraph, heading and list blocks; 10 original tables and all 439 original table cells, including headers; all 102 editorial comments.
- Key: 98 paragraph, heading and list blocks; 14 tables and all 245 cells; all 122 editorial comments.
- Both titles, every full prose block in PDF extraction, all 61 learner tasks and their 61 keyed counterparts, all 89 teaching IDs, exact composed readings and examples, and the complete 61-word source passage are retained. The finite panels were reconstructed into the original eight-column rows for cell comparison.

All 33 pages were freshly rendered at 150 dpi as `build/initial-chapter-02-p01.png` through `p19.png` and `build/initial-answer-key-p01.png` through `p14.png`. The typesetter, coordinator and independent reviewer each inspected every page. Tables, reading boundaries, complete task and key blocks, special letters, vowel marks, notes and ordinary prose continuations passed. There were no requested layout repairs. [page-review.json](page-review.json) retains the image hashes and page ledger; [the independent review](../../chapters/ch02/review.md) records the separate presentation verdict.

Final LuaLaTeX logs contain no missing-character, font-substitution, overfull, underfull or rerun warnings. The repository’s concrete export check, `python -X utf8 scripts/check_unit02.py --draft --tex`, passes on these final files. The full content audit additionally covers all prose, vocabulary fields and key explanations, beyond that checker’s required IDs and exact task/reading strings.

Xpdf 4.00 introduces artificial spaces around some macron letters and represents printed literal hyphens as U+00AD in UTF-8 extraction. The checks ignore extraction whitespace and map U+00AD back to `-`; they do not remove hyphens or normalize Old English spelling. Every source-reading and composed-reading word boundary was also checked visually. Ghostscript reports missing optional `FAPIfontmap` and `FAPIcidfmap` files; the embedded Cambria fonts rendered correctly on every page. The installed `rungs` wrapper is broken, so the direct Ghostscript executable is used below.
