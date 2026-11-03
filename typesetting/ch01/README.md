# Unit 1 exports

The current [learner PDF](chapter-01.pdf) has **23 pages**; its separate [answer key](answer-key.pdf) has **14 pages**. The opening revision teaches all ten nominative subject forms beside the copula, labels all 44 noun entries with a section and model noun, and uses new contexts for original practice. All 46 Cook prompts and their complete key section remain unchanged.

The [independent linguistic review](../../docs/revisions/opening/reviews/unit1-review.md), [assessment/register acceptance](../../docs/revisions/opening/reviews/unit1-register-acceptance.json), [complete content check](../../docs/revisions/opening/exports/unit1-check.json), and [all-page visual review](../../docs/revisions/opening/reviews/unit1-pages-final.json) cover the current edition. All 92 tasks have corresponding reviewed answers; the exact Creation passage and complete logical paradigms are retained. Supplied help and reference checks do not count as independent mastery.

Editable masters are [student.md](../../chapters/ch01/student.md) and [answer-key.md](../../chapters/ch01/answer-key.md). Complete TeX sources are [chapter-01.tex](chapter-01.tex) and [answer-key.tex](answer-key.tex), using the shared Cambria layout. The [revision reconciliation](../../docs/revisions/opening/unit1-reconciliation.json) records current PDF identities and the administrative completion bridge.

## Reproduction

Run from the repository root:

```powershell
python -B -X utf8 scripts/build_opening_exports.py --stage assemble --select ch01/learner,ch01/key --output-root typesetting --report build/opening/unit1-assemble.json
python -B -X utf8 scripts/build_opening_exports.py --stage compile --select ch01/learner,ch01/key --output-root typesetting --report build/opening/unit1-compile.json
python -B -X utf8 scripts/check_opening_exports.py --select ch01/learner,ch01/key --output-root typesetting --report build/opening/unit1-check.json
python -B -X utf8 scripts/check_opening_revision.py --scope all --report build/opening/domain-check.json
```

These commands produce build copies and reports; they do not promote PDFs automatically. A changed export needs fresh complete-content and all-page visual acceptance. Historical unit/table-layout receipts remain evidence for their own checkpoints; do not rerun old assemblers, baseline captures or register mergers against the revised course.

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
