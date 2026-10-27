# Unit 15 exports

The complete [learner PDF](chapter-15.pdf) has **64 pages**; the [separate key](answer-key.pdf) has **30**. Editable masters: [student.md](../../chapters/ch15/student.md) and [answer-key.md](../../chapters/ch15/answer-key.md). All 105 tasks, vocabulary, complete defined paradigms, three connected readings, support and original notes are included.

All **94 final pages** passed non-author visual inspection. [Individual ledgers](reviews/) retain page-specific observations and final PDF/image identities. [Final acceptance](page-review.json) reconciles every page, complete parity, unchanged accepted masters and clean logs. [Layout adjustments](layout-adjustments.json) record the actual repairs and reinspection history. Byte-identical page reuse identifies the specific previously inspected image.

## Content and review

[Complete parity](content-parity.json) covers **1154 prose/heading/list blocks, 96 tables, 1,772 cells including headers, and 1806 editorial comments**. An independent Markdown inventory matches decoded TeX; full prose matches extracted PDF text after whitespace and soft-hyphen normalization. Original note references retain D/P/R-prefixed numbers, with general source notes numbered separately. Every definition remains. Visual review includes actual tables, endings and special characters.

The learner gives 69 defined systems / 691 positions, comprising 675 form/expression cells and 16 explicitly unassigned slots. All 50 Cook IX.28–30 and joint X, XI.31 prompts retain wording and IDs, alongside 55 original tasks and eight examples. The three exact source readings total 415 words and retain 27 notes / 33 anchors, 114 reading helps and 36 Cook help groups. The continuation of Duties on pp. 160–161 remains unassigned.

The fresh [reviewer](../../chapters/ch15/review.md) froze [all solutions](../../chapters/ch15/independent-solutions.md) before key/current-contract/audit access. A separate [fresh paradigm reviewer](../../chapters/ch15/reviews/paradigms.json) checked every position and rule against primary evidence. Neither authored a master or task. Canonical amendments preserve corrections separately from sealed packets and the unchanged blind witness. No material finding is open.

## Rebuilding

Retained TeX preserves the reviewed layout. Use LuaLaTeX with Cambria and [book-layout.tex](../book-layout.tex): 165 × 241 mm trim, body 11/14.3 pt, tables 10.5/13.2 pt, source notes 10/12.8 pt. Both documents use `Ligatures=TeXOff`. Earlier exports and shared layout remain unchanged.

From this directory:

```powershell
New-Item -ItemType Directory -Force build
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-15.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-15.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
& 'C:/Program Files/Git/mingw64/bin/pdftotext.exe' -enc UTF-8 -layout build/chapter-15.pdf build/chapter-15.txt
& 'C:/Program Files/Git/mingw64/bin/pdftotext.exe' -enc UTF-8 -layout build/answer-key.pdf build/answer-key.txt
```

The checked toolchain is TeX Live 2026 LuaHBTeX 1.24.0, Xpdf pdftotext 4.00 and Ghostscript. This Windows installation needs access to the owner's font caches. Final logs contain no missing characters, overfull/underfull boxes, font substitutions or unresolved rerun warnings.

From the repository root, `python -X utf8 scripts/check_unit15.py --draft --tex` checks task/key references, exact prompts/readings, literal tables, model/dependency bindings, evidence identities and logs. It supplements linguistic and visual review. Render every page with Ghostscript `png16m`, `-r150 -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -dBATCH -dNOPAUSE`, supplying TeX Live's `Resource/Init`, `lib` and `kanji` through `-I`.

Build products and rendered page images are ignored unless explicitly retained; ledgers preserve inspected identities. Source evidence images remain tracked. One-use helpers are not required generators; reassembly can discard layout repairs. Rebuilt PDF metadata can differ, so replace retained PDFs only after full parity and page review.

Checkpoints: contract **`ff7f7c8`**, drafts **`3822d4b`**, blind solutions **`ecbdc44`**, accepted text **`0ec6ae3`**. Complete exports/registers: **`a80bf34`**. The [handoff](../../docs/HANDOFF.md) records final closure.
