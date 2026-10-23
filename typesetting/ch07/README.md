# Unit 7 exports

The complete [learner PDF](chapter-07.pdf) has **37 pages**; the [separate key](answer-key.pdf) has **30**. The editable masters are [student.md](../../chapters/ch07/student.md) and [answer-key.md](../../chapters/ch07/answer-key.md). Both exports contain the complete independently accepted unit: vocabulary, paradigms, explanations, examples, all 80 tasks, both connected readings, local help and source notes.

All **67 final pages** passed non-author visual inspection. The [individual ledgers](reviews/) retain page-specific observations, inspection provenance and exact image/PDF identities. Three learner columns and the key's A07 first column were widened before inspection to contain long forms. The sole visual finding, U07-PF01, separated an example from its translation across learner pages 1–2. A TeX-only space reservation keeps them together. Both revised pages were directly reopened; all other 35 learner images were independently verified byte-identical to the inspected version. The key needed no further repair. [Final presentation acceptance](page-review.json) reconciles every page, final identity and clean build log.

## Complete content and independent review

[Content parity](content-parity.json) compares every Markdown block with the actual TeX: **407 learner and 283 key prose/heading/list blocks**, **46 learner and 18 key tables**, and **1,071 learner and 297 key table cells including headers**. All **499 editorial comments** are preserved. Complete prose also matches the extracted PDF character stream, with only whitespace and Xpdf soft-hyphen encoding normalized.

The learner gives **82 logical paradigms with 1,060 cells**: 56 complete present/preterite subjunctive systems including the alternative bēo present, five new indicative systems, a command pair, twelve participle pairs, five complete strong/weak participle-agreement models, and the full relevant forms of eall, ǣlc and geweald. The 41 actual morphology matrices identify every person, number, case, gender and tense covered by a compact row. Displaying a form does not extend its stated syntactic scope.

All **80 graded tasks** have separate models, targets, explanations, alternatives and diagnoses. The **34 exact Cook prompts** are I.4.18 and all of I.6–7. Eleven new examples and the **56-word connected account**, “Binding the animals,” retain their checked wording. The full **89-word fifth-day Creation paragraph** is Cook's *First Book*, printed p126 / one-based PDF142, editorial prose lines 5–14. All ten local support groups and eighteen original notes, numbered 4–21, are included. The canonical numbered Cook crosswalk is 113 assigned and 531 deferred items, with none omitted or excluded; the earlier birds alias is contained in this source assignment.

The [independent review](../../chapters/ch07/review.md), [frozen pre-key solutions](../../chapters/ch07/independent-solutions.md) and [review ledger](../../chapters/ch07/review-ledger.json) record actual task solving, complete displayed-form checks, source-image evidence and key comparison. The reviewer authored neither master and discloses prior grammar-audit work. The qualified spatial *ofer* explanation was clarified and independently verified against Fulk before textual acceptance. Neither Markdown master nor the frozen solutions changed during export.

## Rebuilding

Use LuaLaTeX with Cambria and the packages in [book-layout.tex](../book-layout.tex). The trim is 165 × 241 mm; body type is 11/14.3 pt, tables 10.5/13.2 pt and final source references 10/12.8 pt. Both documents use `Ligatures=TeXOff` to preserve literal punctuation. The learner's shorter running title is “Unit 7. Subjunctive and passive”; its full title remains on the opening page. Unit 7 changes no shared layout or earlier export.

From this directory:

```powershell
New-Item -ItemType Directory -Force build
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-07.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-07.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
pdftotext -enc UTF-8 -layout build/chapter-07.pdf build/chapter-07.txt
pdftotext -enc UTF-8 -layout build/answer-key.pdf build/answer-key.txt
```

The verified toolchain is LuaHBTeX 1.24.0 / TeX Live 2026, Xpdf `pdftotext`, and Ghostscript 10.08.0. On this Windows installation LuaLaTeX needs access to the owner's TeX/font caches. Final logs contain no overfull/underfull boxes, missing characters, font substitutions or unresolved rerun warnings.

From the repository root, `python -X utf8 scripts/check_unit07.py --draft --tex` verifies contract references, all task/key IDs, actual form matrices, exact prompts/passages, source metadata and image identities, special-character retention and clean logs. It does not replace linguistic or visual review. Raw hashes and normalized-LF companions distinguish checkout line-ending conversion from content changes. The substantive contract has a separate accepted hash so that completion metadata does not masquerade as a change to the learning contract.

Render every page using Ghostscript's `png16m` device with `-r150 -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -dBATCH -dNOPAUSE`. The installed TeX Live Ghostscript needs its `Resource/Init`, `lib` and `kanji` directories supplied with `-I`. The final learner render set is `learner-v2`; the key is `key-v1`. Export-page images and build products are ignored, while their reviewed identities and repair history are retained in the ledgers. The audited source-page PNGs committed with the Unit 7 evidence remain tracked.

Retained TeX is authoritative for rebuilding. One-use assembly and parity helpers under ignored `build/` directories are working aids, not required generators. Reassembly would discard the reviewed column widths and space reservation. PDF metadata can change on rebuilding. Copy a rebuilt PDF over the retained export only after complete content and page review.

Checkpoints: contract before prose **`74404d8`**, complete drafts **`db1ef63`**, frozen pre-key solutions **`aa31f25`**, accepted text **`089039d`**. Complete exports and reviewed registers are saved at **`b186c8b`**. The subsequent [handoff](../../docs/HANDOFF.md) records final Beads closure and completion metadata without changing accepted masters or PDFs.
