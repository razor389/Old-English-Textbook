# Unit 9 exports

The complete [learner PDF](chapter-09.pdf) has **44 pages**; the [separate key](answer-key.pdf) has **26**. The editable masters are [student.md](../../chapters/ch09/student.md) and [answer-key.md](../../chapters/ch09/answer-key.md). Both exports contain the complete independently accepted unit, including vocabulary, paradigms, all 97 tasks, both readings, local help and source notes.

All **70 final pages** passed non-author visual inspection. [Individual ledgers](reviews/) retain page-specific observations and exact PDF/image identities. Initial compilation identified twelve horizontal overflows in five noun diagnostic tables. Their column widths were redistributed to fit the complete Old English forms at the unchanged 10.5-point table size; all cell text remains unchanged. Visual proof found one detached vocabulary caption on learner page 12. The caption and its complete table are now bound together on page 13. Both changed pages were directly re-inspected; the other 42 learner images were independently verified byte-identical to their inspected predecessors. All 26 key pages remain the directly inspected v1 images. No master or linguistic text changed. [Final acceptance](page-review.json) reconciles every page, full content parity, unchanged accepted masters and clean build logs. No material presentation issue remains open.

## Content and review

[Complete parity](content-parity.json) covers **825 prose/heading/list blocks, 78 tables, 1461 table cells including headers, and 607 editorial comments**. An independent Markdown inventory is compared with actual decoded TeX; full prose also matches the extracted PDF character stream after whitespace and soft-hyphen normalization. Every-page inspection includes all tables, endings and special characters.

The learner presents **87 logical paradigms / 876 cells through 57 matrices**. Three new noun classes appear in full. Familiar classes use complete printed models and 54 lexical diagnostic rows: **336 nominal cells are literal and 312 explicitly derived**. All **228 verb cells** are printed. Seventeen complete indicative systems, six command pairs and sēcan subjunctives accompany the bounded complement grammar. Tables do not extend a form's stated sense, syntax or recognition scope.

All **64 original Cook II.9–12 prompts** remain exact, alongside 33 original tasks and twelve translated examples. The **52-word new dialogue**, “The fisherman and his companion,” precedes the exact **62-word, four-turn Choice of Occupations opening**, Cook's *First Book*, p131 / one-based PDF147. Prose lines7–15 are counted editorially with printed10/15 as anchors. All **thirteen original notes and eleven local help groups** remain. The preceding merchandise/price exchange and subsequent smith speech are outside the excerpt. The ivory, living-creatures and 365-day exercise phrases remain explicitly supplied.

The [independent reviewer](../../chapters/ch09/review.md) solved all 97 actual tasks before key/private-answer access. [Frozen solutions](../../chapters/ch09/independent-solutions.md) and the [full ledger](../../chapters/ch09/review-ledger.json) retain the comparison, every paradigm display route, source evidence and resolved findings. The reviewer authored neither master nor graded task and discloses earlier grammar/public-composition work. Witness errors and valid alternatives are adjudicated without rewriting the frozen solutions.

## Rebuilding

Retained TeX is authoritative. Use LuaLaTeX with Cambria and [book-layout.tex](../book-layout.tex): 165 × 241 mm trim, body 11/14.3 pt, tables 10.5/13.2 pt and source endnotes 10/12.8 pt. Both documents use `Ligatures=TeXOff`. No shared layout or earlier export changed.

From this directory:

```powershell
New-Item -ItemType Directory -Force build
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-09.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-09.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
pdftotext -enc UTF-8 -layout build/chapter-09.pdf build/chapter-09.txt
pdftotext -enc UTF-8 -layout build/answer-key.pdf build/answer-key.txt
```

The verified toolchain is LuaHBTeX 1.24.0 / TeX Live 2026, Xpdf pdftotext, and Ghostscript 10.08.0. This Windows installation needs access to the owner's TeX/font caches. Final logs contain no overfull/underfull boxes, missing characters, font substitutions or unresolved rerun warnings.

From the repository root, `python -X utf8 scripts/check_unit09.py --draft --tex` checks actual task/key references, exact prompts/passages, literal and derived paradigm mappings, evidence identities and logs. It does not replace linguistic or visual review. Raw and normalized-LF identities distinguish checkout conversion from text changes; the substantive contract identity allows later completion metadata without altering reviewed content.

Render every page with Ghostscript `png16m`, `-r150 -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -dBATCH -dNOPAUSE`, supplying TeX Live's `Resource/Init`, `lib` and `kanji` through `-I`. Final image sets are **learner-v2** and **key-v1**. Build products and export-page images are ignored; inspected identities remain in the ledgers. Source evidence images remain tracked. One-use helpers in ignored build directories are not required generators; rerunning assembly can discard reviewed layout repairs. Rebuilt PDF metadata can differ, so replace retained PDFs only after complete parity and page review.

Checkpoints: contract **`aafd2a1`**, complete drafts **`c45cc58`**, pre-key solutions **`72a5b2d`**, accepted text **`7f81e43`**. Complete exports and reviewed registers are ready for their local checkpoint. The [handoff](../../docs/HANDOFF.md) records tracker closure and final completion metadata.
