# Unit 6 exports

The complete [learner PDF](chapter-06.pdf) has **25 pages**; the [separate key](answer-key.pdf) has **28**. The editable masters are [student.md](../../chapters/ch06/student.md) and [answer-key.md](../../chapters/ch06/answer-key.md). Both exports contain the complete independently accepted unit: vocabulary, paradigms, explanations, examples, all 72 tasks, both connected readings, local help and source notes.

All **53 final pages** passed non-author visual inspection. The [individual ledgers](reviews/) retain page-specific observations and exact image/PDF identities. The learner's weak-I table has a wider first column to contain gefręmman. The key's final source note [8] is kept together so its original-note quotation does not break across pages 27–28. Both revised key pages were directly reopened; all other key images were independently confirmed byte-identical to the initially inspected images. [Final presentation acceptance](page-review.json) reconciles every page, final artifact identity and clean build log.

## Complete content and independent review

[Content parity](content-parity.json) compares every Markdown block with the actual TeX: **315 learner and 247 key prose/heading/list blocks**, **13 learner and 37 key tables**, and **439 learner and 585 key table cells including headers**. All **468 editorial comments** are preserved. Complete prose also matches the extracted PDF character stream, with only whitespace and Xpdf soft-hyphen encoding normalized.

The learner teaches ten complete present/preterite indicative systems and the six-cell alternative bēo present: **126 new indicative cells**. It also gives **44 complete imperative pairs** and **46 plain/inflected infinitive pairs**, making **306 new verbal cells** in twelve actual form matrices. The earlier eom series is displayed for comparison with its original milestones. Defective citation labels and unselected forms retain their explicit limits.

All **72 graded tasks** have separate models and explanations. Ten new examples, the **68-word controlled journey dialogue**, and the **76-word fisherman gift/first-direction excerpt** retain their checked wording. The original excerpt includes all ten support groups and three original notes. It is a declared excerpt, not the fisherman's whole speech. Unit 6 adds no numbered Cook exercise assignments; the canonical crosswalk remains 79 assigned and 565 deferred items.

The [independent review](../../chapters/ch06/review.md), [frozen pre-key solutions](../../chapters/ch06/independent-solutions.md) and [review ledger](../../chapters/ch06/review-ledger.json) record actual task solving, complete paradigm recovery, source-image checks and key comparison. All four material findings were resolved before export: the C6/X5 prompt clarifications, X4's subject/agreement explanation, and image-checked metadata for 23 new supplied-only lemmas. Neither Markdown master nor the frozen solutions changed during typesetting.

## Rebuilding

Use LuaLaTeX with Cambria and the packages in [book-layout.tex](../book-layout.tex). The trim is 165 × 241 mm; body type is 11/14.3 pt, tables 10.5/13.2 pt and source notes 10/12.8 pt. Both documents use `Ligatures=TeXOff` to preserve literal punctuation. The learner's shorter running title is “Unit 6. Irregular verbs”; its full title is retained on the opening page. Unit 6 changes no shared layout or earlier export.

From this directory:

```powershell
New-Item -ItemType Directory -Force build
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-06.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-06.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
pdftotext -enc UTF-8 -layout build/chapter-06.pdf build/chapter-06.txt
pdftotext -enc UTF-8 -layout build/answer-key.pdf build/answer-key.txt
```

The verified toolchain is LuaHBTeX 1.24.0 / TeX Live 2026, Xpdf `pdftotext`, and Ghostscript 10.08.0. On this Windows installation LuaLaTeX needs access to the owner's TeX/font caches. Final logs have no overfull/underfull boxes, missing characters, font substitutions or unresolved rerun warnings. A separate typography check confirmed that ordinary prose and translations use regular Cambria and explicitly emphasized words use Cambria Bold; the apparent heaviness at 150 dpi was not a font-selection error.

From the repository root, `python -X utf8 scripts/check_unit06.py --draft --tex` verifies contract references, every task/key ID, actual form matrices, exact prompts/passages, source metadata, special-character retention and clean logs. It does not replace linguistic or visual review. Raw hashes and normalized-LF companions distinguish checkout line-ending conversion from content changes.

Render every page using Ghostscript's `png16m` device with `-r150 -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -dBATCH -dNOPAUSE`. The installed TeX Live Ghostscript needs its `Resource/Init`, `lib` and `kanji` directories supplied with `-I`. The final learner render set is `learner-v1`; the key is `key-v2`. Images and build products are ignored, while their reviewed identities and repair history are retained in the ledgers.

Retained TeX is authoritative for rebuilding. One-use assembly and parity helpers under ignored `build/` directories are working aids, not required generators. Reassembly would discard the reviewed table-width and page-break refinements. PDF metadata can change on rebuilding. Copy a rebuilt PDF over the retained export only after complete content and page review.

The source/contract checkpoint is **`3bfc05e`**, complete drafts **`2e2b275`**, frozen pre-key solutions **`f42beb0`**, and accepted text **`3955a2a`**. The final handoff records the complete exports/registers checkpoint and subsequent Beads closure without changing the accepted masters or PDFs.
