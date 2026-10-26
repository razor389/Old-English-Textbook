# Unit 14 exports

The complete [learner PDF](chapter-14.pdf) has **35 pages**; the [separate key](answer-key.pdf) has **21**. Editable masters: [student.md](../../chapters/ch14/student.md) and [answer-key.md](../../chapters/ch14/answer-key.md). All 44 tasks, vocabulary, complete defined paradigms, connected reading, support and original notes are included.

All **56 final pages** passed non-author visual inspection. [Individual ledgers](reviews/) retain page-specific observations and final PDF/image identities. [Final acceptance](page-review.json) reconciles every page, complete parity, unchanged accepted masters and clean logs. [Layout adjustments](layout-adjustments.json) record the key's A01 column-width repair and the heading repairs: each indicative heading stays with its rule and complete table, and the Cook VIII.27 heading stays with its first answer. Changed pages were inspected again; byte-identical pages retain their actual earlier inspection records.

## Content and review

[Complete parity](content-parity.json) covers **521 prose/heading/list blocks, 55 tables, 925 cells including headers, and 470 editorial comments**. An independent Markdown inventory matches decoded TeX; full prose matches extracted PDF text after whitespace and soft-hyphen normalization. Markdown note references become matching numbered superscript endnote labels. Every note definition remains. Visual review includes actual tables, endings and special characters.

The learner gives 38 complete systems / 324 cells in 38 literal matrices, with rules, stem changes and bounded uses. All 21 Cook VIII.26–27 prompts retain their wording and IDs, alongside 23 original tasks and four translated examples. The 159-word Dangers opening, printed 156.1–158.4 / PDF 172–174, retains 24 notes / 25 anchors, 34 reading helps and 20 Cook help groups. The next argument is unassigned.

The fresh [reviewer](../../chapters/ch14/review.md) froze [all solutions](../../chapters/ch14/independent-solutions.md) before key/current-contract/audit access. A separate [fresh paradigm reviewer](../../chapters/ch14/reviews/paradigms.json) checked every cell and rule against actual primary evidence. Neither authored a master or task. Canonical amendments preserve corrections separately from original audit packets; the blind witness is unchanged. No material finding is open.

## Rebuilding

Retained TeX preserves the reviewed layout. Use LuaLaTeX with Cambria and [book-layout.tex](../book-layout.tex): 165 × 241 mm trim, body 11/14.3 pt, tables 10.5/13.2 pt, source notes 10/12.8 pt. Both documents use `Ligatures=TeXOff`. Earlier exports and the shared layout are unchanged. Specific page repairs remain in the actual TeX and page ledgers.

From this directory:

```powershell
New-Item -ItemType Directory -Force build
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-14.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-14.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
& 'C:/Program Files/Git/mingw64/bin/pdftotext.exe' -enc UTF-8 -layout build/chapter-14.pdf build/chapter-14.txt
& 'C:/Program Files/Git/mingw64/bin/pdftotext.exe' -enc UTF-8 -layout build/answer-key.pdf build/answer-key.txt
```

The checked toolchain is TeX Live 2026 LuaHBTeX 1.24.0, Xpdf pdftotext 4.00 and Ghostscript. The pdftotext path above is the installed Windows location, outside this shell's PATH. This installation needs access to the owner's font caches. Final logs contain no missing characters, overfull/underfull boxes, font substitutions or unresolved rerun warnings.

From the repository root, `python -X utf8 scripts/check_unit14.py --draft --tex` checks actual task/key references, exact prompts and reading, all literal cells, selected Cook model/dependency bindings, evidence identities and logs. It supplements linguistic and visual review. Render every page with Ghostscript `png16m`, `-r150 -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -dBATCH -dNOPAUSE`, supplying TeX Live's `Resource/Init`, `lib` and `kanji` through `-I`.

Build products and rendered page images are ignored; inspected identities remain in the ledgers. Source evidence images remain tracked. Ignored one-use helpers are not required generators; reassembly can discard layout repairs. Rebuilt PDF metadata can differ, so replace retained PDFs only after full parity and page review.

Checkpoints: contract **`18cfa3a`**, drafts **`e8cf9ce`**, blind solutions **`d78de6f`**, accepted text **`5721c5f`**. Complete exports/registers: **`this export checkpoint`**. The [handoff](../../docs/HANDOFF.md) records final closure.
