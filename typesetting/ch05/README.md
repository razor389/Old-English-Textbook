# Unit 5 exports

The complete [learner PDF](chapter-05.pdf) has **25 pages**; the [separate key](answer-key.pdf) has **21**. The editable masters are [student.md](../../chapters/ch05/student.md) and [answer-key.md](../../chapters/ch05/answer-key.md). Both exports contain the complete independently accepted unit, including all paradigms, vocabulary, examples, tasks, readings, local help and source notes.

All **46 final pages** passed non-author visual inspection. The [page ledgers](reviews/) retain page-specific observations and image/PDF identities. A page break before the learner's cumulative review keeps X2's supplied citations with its task. Revised pages 22–23 were directly reopened; all other learner images were independently confirmed byte-identical to the previously inspected images. The key required no repair. [Final presentation acceptance](page-review.json) reconciles every page, final artifact identity and clean build log.

## Complete content and independent review

[Content parity](content-parity.json) compares every Markdown block with the actual TeX: **342 learner and 212 key prose/heading/list blocks**, **19 learner and 34 key tables**, and **600 learner and 306 key table cells including headers**. All **474 editorial comments** are preserved. Complete prose also matches the extracted PDF character stream, with only whitespace and Xpdf soft-hyphen encoding normalized.

The learner displays **33 complete present/preterite indicative systems**, with all three persons singular and plural recoverable: **396 finite cells** and **132 principal-part positions**. The 66 nonfinite positions remain supplied citations. All sixteen unchanged Cook I.5 prompts appear among the **67 graded tasks**. Eight examples, a 51-word new account, the unchanged 69-word first-day revisit and the complete 58-word second-day reading retain their exact text. All 18 local supports and 34 relevant original source notes are included.

The [independent review](../../chapters/ch05/review.md), [frozen pre-key solutions](../../chapters/ch05/independent-solutions.md) and [review ledger](../../chapters/ch05/review-ledger.json) record actual task solving, complete display recovery, source-image checks and every key comparison. No material finding remains. Neither Markdown master nor the frozen solutions changed during typesetting.

## Rebuilding

Use LuaLaTeX with Cambria and the packages in [book-layout.tex](../book-layout.tex). The trim is 165 × 241 mm; body type is 11/14.3 pt, tables 10.5/13.2 pt and source notes 10/12.8 pt. Unit 5 changes no shared layout or earlier export. Both documents use `Ligatures=TeXOff` to preserve literal punctuation. Tables retain their complete rows; the learner's cumulative review and both source-note sections begin on fresh pages.

From this directory:

```powershell
New-Item -ItemType Directory -Force build
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-05.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-05.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
pdftotext -enc UTF-8 -layout build/chapter-05.pdf build/chapter-05.txt
pdftotext -enc UTF-8 -layout build/answer-key.pdf build/answer-key.txt
```

The verified toolchain is LuaHBTeX 1.24.0 / TeX Live 2026, Xpdf `pdftotext`, and Ghostscript 10.08.0. On this Windows installation LuaLaTeX needs access to the owner's TeX/font caches. Final logs have no overfull/underfull boxes, missing characters, font substitutions or unresolved rerun warnings.

From the repository root, `python -X utf8 scripts/check_unit05.py --draft --tex` verifies contract references, every task/key ID, exact prompts/passages, special-character retention and clean logs. It does not replace linguistic or visual review. Raw hashes and normalized-LF companions distinguish checkout line-ending conversion from content changes.

Render every page using Ghostscript's `png16m` device with `-r150 -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -dBATCH -dNOPAUSE`. The installed TeX Live Ghostscript needs its `Resource/Init`, `lib` and `kanji` directories supplied with `-I`. The final learner render set is `learner-v2`; the key is `key-v1`. Images and build products are ignored, while their reviewed identities are retained in the ledgers.

Retained TeX is authoritative for rebuilding. One-use assembly and parity helpers under ignored `build/` directories are working aids, not required generators. PDF metadata can change on rebuilding. Copy a rebuilt PDF over the retained export only after complete content and page review.

The source/contract checkpoint is **`fc29cf9`**, complete drafts **`a28b266`**, frozen pre-key solutions **`d807acf`**, and accepted text **`7bbb334`**. Complete exports and reviewed registers are saved at **`37a52c3`**. The subsequent handoff records final Beads closure and completion metadata without changing the accepted masters or PDFs.
