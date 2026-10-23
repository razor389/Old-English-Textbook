# Unit 4 exports

The complete learner PDF has **20 pages**; the separate key has **19**. The editable masters are [student.md](../../chapters/ch04/student.md) and [answer-key.md](../../chapters/ch04/answer-key.md). Both exports include all contracted material: the full selected indicative systems, principal parts, noun tables, 52 tasks, eight examples, both connected readings, local reading help and source notes.

The texts and all **39 final pages** are independently accepted. Every page was visually inspected by a non-author; revised pages were reopened and unchanged images checked for byte identity. The page ledgers under [reviews](reviews/) preserve all findings and their resolutions. Consolidated acceptance and final file identities are recorded in [page-review.json](page-review.json).

## Content and review

[content-parity.json](content-parity.json) compares every Markdown block with the actual TeX: **233 learner and 161 key prose/heading/list blocks**, **18 learner and 33 key tables**, and **563 learner and 575 key table cells including headers**. All 370 editorial comments are preserved. Complete prose also matches the extracted PDF character stream, with only whitespace and Xpdf soft-hyphen encoding normalized. The learner's three literal error asterisks remain characters.

The learner presents 26 complete finite systems: 24 productive and two recognition references, each with all three persons in singular and plural for present and preterite indicative. The clearly labelled common plural columns recover all **312 finite cells**. All **104 principal-part entries** and **32 noun cells** are included. Nonfinite citations and locally supplied reading forms retain their stated scope.

The [independent review](../../chapters/ch04/review.md) preserves all 52 solutions before key access, complete paradigm recovery and source/dependency checks. Neither master has changed since textual acceptance. Page ledgers identify the PDF and each actual rendered image; revised pages require direct reinspection, while byte-identical images retain their original visual inspection.

## Rebuilding

Use LuaLaTeX with Cambria and the packages in [book-layout.tex](../book-layout.tex). The trim is 165 × 241 mm; body type is 11/14.3 pt, tables 10.5/13.2 pt and source notes 10/12.8 pt. Unit 4 changes no shared layout or earlier export.

From this directory:

```powershell
New-Item -ItemType Directory -Force build
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-04.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-04.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
pdftotext -enc UTF-8 -layout build/chapter-04.pdf build/chapter-04.txt
pdftotext -enc UTF-8 -layout build/answer-key.pdf build/answer-key.txt
```

The verified toolchain is LuaHBTeX 1.24.0 / TeX Live 2026, Xpdf `pdftotext`, and Ghostscript 10.08.0 at 150 dpi with text/graphics antialiasing. On this Windows installation LuaLaTeX needs access to the owner's TeX/font caches. The final logs must have no overfull/underfull boxes, missing characters, font substitutions or unresolved rerun warnings.

The key uses `Ligatures=TeXOff` to preserve the master's straight apostrophes. Its R2 table has hand-reviewed column widths, and the cumulative-review heading starts with X1. Learner source notes use 1.5 pt paragraph spacing so the final explanatory sentence stays on the notes page. These are presentation changes; no wording, form or punctuation is removed or normalized. All tasks remain with their labels and all finite/noun tables remain complete.

From the repository root, run `python -X utf8 scripts/check_unit04.py --draft --tex` after rebuilding the ignored text/log files. This checks contract references, task/key IDs, exact prompts, source passages, special characters and clean logs. It does not replace linguistic or visual review. Raw and normalized-LF hashes distinguish checkout conversion from content changes.

Retained TeX is authoritative for rebuilding. One-use assembly and parity helpers under ignored `build/` directories are working aids, not required generators. PDF metadata can change on rebuilding. Copy a rebuilt PDF over the retained export only after content and page review.

Page images use Ghostscript's `png16m` device with `-r150 -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -dBATCH -dNOPAUSE`. The installed TeX Live Ghostscript also needs its `Resource/Init`, `lib` and `kanji` directories supplied with `-I`. Final ledgers retain the image hashes even though render files are ignored.

The pre-prose source/contract checkpoint is **`856a5fa`**; independently accepted text is **`5f47f26`**. Complete exports and integrated registers are saved in the subsequent local checkpoint recorded in the root status and handoff.
