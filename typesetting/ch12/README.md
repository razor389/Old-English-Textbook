# Unit 12 exports

The complete [learner PDF](chapter-12.pdf) has **47 pages**; the [separate key](answer-key.pdf) has **30**. Editable masters: [student.md](../../chapters/ch12/student.md) and [answer-key.md](../../chapters/ch12/answer-key.md). All 76 tasks, vocabulary, complete defined systems, readings, support and source notes are included.

All **77 final pages** passed non-author visual inspection. [Individual ledgers](reviews/) retain page-specific observations and exact PDF/image identities. Wide adjective tables use stacked singular/plural panels at unchanged 10.5pt type, with visible captions. The parity check reconstructs the original seven-column coordinates. Lexical definitions stay with their first display or derivation; each Cook prompt stays with its answer. The key's diagnostic table has enough width for geopenian. [Final acceptance](page-review.json) reconciles every final page, complete parity, unchanged accepted masters and clean build logs. The ledgers record repairs and reinspections.

## Content and review

[Complete parity](content-parity.json) covers **796 prose/heading/list blocks, 82 tables, 1,124 cells including headers, and 572 editorial comments**. An independent Markdown inventory matches decoded TeX; full prose matches extracted PDF text after whitespace and soft-hyphen normalization. Visual review includes tables, endings and special characters.

The learner gives **62 complete defined systems / 692 cells**, using 44 marked matrices and 29 lexical diagnostic rows: 368 literal cells and 324 explicit model derivations. Exceptional patterns are printed in full. The twelve habban construction positions are a separate display using actual finite auxiliary, object and participle forms; they add no synthetic lexical forms. Complete morphology retains its stated lexical and syntactic limits.

All **38 Cook VI.19–21 prompts** preserve their wording and identifiers, alongside 38 original tasks and twelve translated examples. The **53-word new account**, “A house and a return,” prepares the exact **155-word** first Roman relief and renewed invasion extract from Cook's Picts and Scots narrative: printed pp. 145–146 / one-based PDF 161–162, editorial 145.1 through 146.11 (partial), ending **and hīe mid ealle foriermdon.** All 21 attached original notes, sixteen reading helps and eleven Cook help groups remain. Earlier Roman withdrawal is separate English context. Original historical speculation remains labelled archival apparatus.

The main [reviewer](../../chapters/ch12/review.md) froze [solutions](../../chapters/ch12/independent-solutions.md) before opening key/private answer files. The record distinguishes 75 unexposed tasks from an exposed check of Cook 21.4, whose proposed clause had accidentally appeared in a source discussion. A fresh reviewer froze an [unexposed 21.4 solution](../../chapters/ch12/reviews/fresh-21-04-solutions.md) before key access and completed a separate [primary-source paradigm review](../../chapters/ch12/reviews/paradigms.json). The [main ledger](../../chapters/ch12/review-ledger.json) records every actual task, all 692 cell routes, source checks, alternatives and adjudications. No material finding remains open. Neither reviewer authored a master or graded task. Original audit records and frozen witnesses remain unchanged; the two canonical amendments are recorded in coverage and review.

## Rebuilding

Markdown remains the editable master. Retained TeX preserves the reviewed layout. Use LuaLaTeX with Cambria and [book-layout.tex](../book-layout.tex): 165 × 241 mm trim, body 11/14.3 pt, tables 10.5/13.2 pt and source endnotes 10/12.8 pt. Both documents use `Ligatures=TeXOff`; earlier exports and the shared layout remain unchanged.

From this directory:

```powershell
New-Item -ItemType Directory -Force build
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-12.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-12.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
pdftotext -enc UTF-8 -layout build/chapter-12.pdf build/chapter-12.txt
pdftotext -enc UTF-8 -layout build/answer-key.pdf build/answer-key.txt
```

The checked toolchain is TeX Live 2026 LuaHBTeX, Xpdf pdftotext and Ghostscript. This Windows installation needs access to the owner's font caches. Final logs contain no overfull/underfull boxes, missing characters, font substitutions or unresolved rerun warnings.

From the repository root, `python -X utf8 scripts/check_unit12.py --draft --tex` checks task/key references, exact prompts/passages, literal and derived paradigms, evidence identities and logs. It supplements linguistic and visual review. Render all pages with Ghostscript `png16m`, `-r150 -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -dBATCH -dNOPAUSE`, supplying TeX Live's `Resource/Init`, `lib` and `kanji` through `-I`.

Build products and export-page images are ignored; inspected identities remain in the ledgers. Source evidence images remain tracked. One-use helpers in ignored build directories are not required generators; rerunning assembly can discard reviewed repairs. Rebuilt PDF metadata can differ, so replace retained PDFs only after full parity and page review.

Checkpoints: contract **`3ec8787`**, complete drafts **`4c9bcd8`**, main pre-key solutions **`a48c232`**, fresh pre-key solution **`b52a9d3`**, accepted text **`61f4ea4`**. The [handoff](../../docs/HANDOFF.md) records complete exports, register integration and final closure.
