# Unit 13 exports

The complete [learner PDF](chapter-13.pdf) has **52 pages**; the [separate key](answer-key.pdf) has **30**. Editable masters: [student.md](../../chapters/ch13/student.md) and [answer-key.md](../../chapters/ch13/answer-key.md). All 90 tasks, vocabulary, defined paradigms, readings, support and original notes are included.

All **82 final pages** passed non-author visual inspection. [Individual ledgers](reviews/) retain page-specific observations and actual PDF/image identities. Wide adjective tables use stacked singular/plural panels at 10.5pt type; the nominal diagnostic table uses linked panels for stems/models and oblique forms. Every original table coordinate remains in the parity reconstruction. [Final acceptance](page-review.json) reconciles all pages, complete parity, unchanged accepted masters and clean logs. The ledgers record actual repairs and reinspections.

## Content and review

[Complete parity](content-parity.json) covers **805 prose/heading/list blocks, 67 tables, 1,861 cells including headers, and 838 editorial comments**. An independent Markdown inventory matches decoded TeX; full prose matches extracted PDF text after whitespace and soft-hyphen normalization. Visual review includes all tables, endings and special characters.

The learner gives 76 complete defined systems / 1,008 cells in 43 matrices: 562 literal cells and 446 explicit shared-model derivations. Complete paradigms retain their lexical and syntactic limits. All 52 Cook VII.22–25 prompts preserve their wording and IDs, alongside 38 original tasks and twelve translated examples. The 87-word new account prepares the exact 236-word music-and-summons episode from Chad, printed 152.3–153.9 partial / one-based PDF 168–169. All 24 notes and 29 attachments remain, with eighteen reading helps and fourteen Cook help groups.

The fresh [reviewer](../../chapters/ch13/review.md) froze [all solutions](../../chapters/ch13/independent-solutions.md) before key/private-analysis access. A separate [fresh paradigm reviewer](../../chapters/ch13/reviews/paradigms.json) checked every cell route against actual displays and primary evidence. Neither authored a master or graded task. Canonical amendments record accepted source-support and relative-target repairs; original audit records and the frozen witness remain unchanged. No material finding is open.

## Rebuilding

Retained TeX preserves the reviewed layout. Use LuaLaTeX with Cambria and [book-layout.tex](../book-layout.tex): 165 × 241 mm trim, body 11/14.3 pt, tables 10.5/13.2 pt and source notes 10/12.8 pt. The final learner editorial page keeps 10pt type with 12pt leading to avoid a two-line spill. Key reading sections and notes flow without unnecessary forced page breaks. Both documents use `Ligatures=TeXOff`; earlier exports and the shared layout are unchanged.

From this directory:

```powershell
New-Item -ItemType Directory -Force build
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-13.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-13.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
& 'C:/Program Files/Git/mingw64/bin/pdftotext.exe' -enc UTF-8 -layout build/chapter-13.pdf build/chapter-13.txt
& 'C:/Program Files/Git/mingw64/bin/pdftotext.exe' -enc UTF-8 -layout build/answer-key.pdf build/answer-key.txt
```

The checked toolchain is TeX Live 2026 LuaHBTeX 1.24.0, Xpdf pdftotext 4.00 and Ghostscript. The pdftotext path above is the installed Windows location; it is not on this shell’s PATH. This installation needs access to the owner’s font caches. Final logs contain no missing characters, overfull/underfull boxes, font substitutions or unresolved rerun warnings.

From the repository root, `python -X utf8 scripts/check_unit13.py --draft --tex` checks task/key references, exact prompts/passages, literal and derived paradigms, evidence identities and logs. It supplements linguistic and visual review. Render every page with Ghostscript `png16m`, `-r150 -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -dBATCH -dNOPAUSE`, supplying TeX Live’s `Resource/Init`, `lib` and `kanji` through `-I`.

Build products and export-page images are ignored; inspected identities remain in the ledgers. Source evidence images remain tracked. Ignored one-use helpers are not required generators; rerunning assembly can discard layout repairs. Rebuilt PDF metadata can differ, so replace retained PDFs only after full parity and page review.

Checkpoints: contract **`40bb0ba`**, complete drafts **`23199c1`**, blind solutions **`d31c692`**, accepted text **`aec6c7f`**. Complete exports/registers: **`this export checkpoint`**. The [handoff](../../docs/HANDOFF.md) records final closure.
