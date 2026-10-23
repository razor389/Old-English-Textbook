# Unit 3 exports

The learner PDF has **30 pages**; the separate key has **19**. The editable masters are [student.md](../../chapters/ch03/student.md) and [answer-key.md](../../chapters/ch03/answer-key.md). These are complete exports, including all vocabulary, recoverable full paradigms, 70 tasks, ten examples, both connected readings, local reading help, and source notes. They are not specimen selections.

Textual and presentation review are accepted. All **49 final pages** were visually inspected by reviewers who did not author the corresponding master, with every finding resolved and the final file identities checked.

## Content and review

[content-parity.json](content-parity.json) records independent comparison of the Markdown block inventory with the actual TeX: **282 learner and 128 key paragraph/heading/list blocks**, **29 learner and 22 key tables**, and **1,063 learner and 505 key table cells including headers**. Every editorial comment is preserved. All complete prose blocks also occur in the extracted PDF character stream, with only whitespace and Xpdf soft-hyphen encoding normalized. The four literal error asterisks in X2 remain characters, not Markdown emphasis.

The grammar presents 78 complete recoverable paradigms through full model tables, complete special tables and explicit stem substitutions. Independent review reproduced every one of their 1,565 unique form records from the learner's displays and rules; the export does not expand those economical patterns into redundant tables.

The [textual review](../../chapters/ch03/review.md) preserves independent solving before key access and the resolution of every finding. The final page ledgers under [reviews](reviews/) identify the actual PDF and rendered-page hashes. The coordinator's consolidated [page-review.json](page-review.json) records final presentation acceptance and file identities. Earlier render findings are retained in the ledgers; they do not certify an uninspected later file.

## Rebuilding

Use LuaLaTeX with Cambria installed and the packages in [book-layout.tex](../book-layout.tex). The inherited trim is 165 × 241 mm; body type is 11/14.3 pt. Tables normally use 10.5/13.2 pt; two wide key tables use 10/12.8 pt. Unit 3 changes no shared layout or earlier export.

From this directory, create `build` if needed, then run:

```powershell
New-Item -ItemType Directory -Force build
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-03.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-03.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
pdftotext -enc UTF-8 -layout build/chapter-03.pdf build/chapter-03.txt
pdftotext -enc UTF-8 -layout build/answer-key.pdf build/answer-key.txt
```

The verified toolchain is LuaHBTeX 1.24.0 / TeX Live 2026, Xpdf `pdftotext`, and Ghostscript 10.08.0 at 150 dpi with text/graphics antialiasing. On this Windows installation LuaLaTeX needs access to the TeX/font directories under the owner's account. The final build logs contain no overfull/underfull boxes, missing characters, or unresolved rerun warnings.

The page-reservation helper flushes the page builder before measuring remaining space. The first complete strong/weak models start together, and each hēah caption stays with its table. All tasks are kept with their labels; long apparatus tables repeat their headings across pages. The final TeX includes the hand-reviewed column widths and pagination adjustments. One-use assembly scratch files are ignored and are not authoritative replacements for this TeX.

From the repository root, run `python -X utf8 scripts/check_unit03.py --draft --tex` after rebuilding the ignored logs and extracted text. This checks concrete contract, ID, source, prompt, character and build requirements; it does not replace linguistic review or visual inspection. PDF metadata may differ on rebuilding. Raw and normalized-LF hashes distinguish original working files from Git line-ending conversion; no spelling normalization is implied.

Only copy rebuilt PDFs over the retained final PDFs after complete parity and page review. The final images can be reproduced with Ghostscript's `png16m` device, `-r150`, `-dTextAlphaBits=4` and `-dGraphicsAlphaBits=4`; the local TeX Live Ghostscript also needs its `Resource/Init`, `lib` and `kanji` directories supplied with `-I`.

The pre-prose contract was saved at `9626f6f`; independently accepted text at `e528af8`; complete exports and reviewed registers at **`95c68d6`**. Later presentation-only captions and emphasis changes were independently checked and are recorded in the review. This export stage adds no new grammatical or lexical scope.
