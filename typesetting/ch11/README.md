# Unit 11 exports

The complete [learner PDF](chapter-11.pdf) has **42 pages**; the [separate key](answer-key.pdf) has **31**. Editable masters: [student.md](../../chapters/ch11/student.md) and [answer-key.md](../../chapters/ch11/answer-key.md). All 92 tasks, vocabulary, paradigms, readings, support and source notes are included.

All **73 final pages** passed non-author visual inspection. [Individual ledgers](reviews/) retain page-specific observations and exact PDF/image identities. Wide adjective paradigms use stacked singular/plural panels at unchanged 10.5pt type, with visible strong/weak captions kept with their tables. Independent parity reconstructs the original seven-column coordinates; repeated case labels serve the panel layout. The open-condition context stays with its example and translation. Two key section headings were moved with their first answers. Source notes follow the last short reading task to avoid an almost empty page. All 33 changed learner pages and four changed key pages received fresh visual inspection; the remaining images were verified identical to their inspected predecessors. [Final acceptance](page-review.json) reconciles every final page, complete parity, unchanged accepted masters and clean build logs.

A diagnostic comparison confirmed regular Cambria and its distinct bold face; the heavy appearance of small text in the page images did not indicate a leaked bold setting or font substitution. The proof records retain the diagnostic identities and the withdrawn concern. The shared layout and font settings were not changed.

## Content and review

[Complete parity](content-parity.json) covers **860 prose/heading/list blocks, 52 tables, 1075 cells including headers, and 607 editorial comments**. An independent Markdown inventory matches decoded TeX; full prose matches extracted PDF text after whitespace and soft-hyphen normalization. Visual review includes tables, endings and special characters.

The learner gives **61 complete defined systems / 826 cells**, with 38 marked matrices and 38 lexical diagnostic rows: 486 literal cells and 340 explicit model derivations. Exceptional patterns are printed in full. A further four-cell Hǣlend title table repeats its assigned singular forms. The full morphology retains its stated lexical and syntactic limits.

All **46 Cook IV.16–17/V.18 prompts** preserve their wording and identifiers, alongside 46 original tasks and fourteen translated examples. The **59-word new account** prepares two exact source spans: the **35-word Britain metals-and-jet passage**, Cook p139 / one-based PDF155, editorial lines 1–4, and the complete **195-word sea-rescue episode**, pp142–143 / PDF158–159, editorial lines 142.8–143.14. The dash in the Britain span is punctuation. All 32 attached original notes, one referenced note and 21 reading helps remain. Five Cook expressions retain local support. Preceding storm context appears separately in English.

The [reviewer](../../chapters/ch11/review.md) solved all 92 actual tasks, including 104 morphology outputs and three complete translations, before key/private-answer access. [Frozen solutions](../../chapters/ch11/independent-solutions.md) and the [ledger](../../chapters/ch11/review-ledger.json) retain the comparison, source checks and adjudications. The reviewer authored neither master nor graded task and discloses earlier grammar/public-composition work. A separate [non-author paradigm review](../../chapters/ch11/reviews/paradigms.json) checks all 826 actual display routes against primary evidence. No material finding remains open.

Amendment **U11-AMEND-01** binds Cook 17.17 to the relative form actually taught in Unit 8. **U11-AMEND-02** corrects three newly introduced weak genitive-plural cells from blacra to **blæcra**, following Cook §§57.2,60 and Wright §§424–425,440. **U11-AMEND-03** adds a compact note on the already evidenced and key-accepted contracted participles fēd/hȳd alongside the selected fēded/hȳded bases. **U11-AMEND-04** makes eleven canonical adjective-table titles visible in the editable learner and export. The reviewer independently verified that removing only those captions restores the earlier accepted learner bytes exactly; initial acceptance at `8c21a9a` is preserved alongside the final caption supplement. The original audit and frozen witness remain preserved; the review adjudicates the witness's inherited explanation explicitly. Task wording, required outputs and teaching milestones are unchanged.

## Rebuilding

Markdown remains the editable master. Retained TeX preserves the reviewed layout. Use LuaLaTeX with Cambria and [book-layout.tex](../book-layout.tex): 165 × 241 mm trim, body 11/14.3 pt, tables 10.5/13.2 pt and source endnotes 10/12.8 pt. Both documents use `Ligatures=TeXOff`; earlier exports and the shared layout remain unchanged.

From this directory:

```powershell
New-Item -ItemType Directory -Force build
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-11.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-11.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
pdftotext -enc UTF-8 -layout build/chapter-11.pdf build/chapter-11.txt
pdftotext -enc UTF-8 -layout build/answer-key.pdf build/answer-key.txt
```

The checked toolchain is TeX Live 2026 LuaHBTeX, Xpdf pdftotext and Ghostscript. This Windows installation needs access to the owner's font caches. Final logs contain no overfull/underfull boxes, missing characters, font substitutions or unresolved rerun warnings.

From the repository root, `python -X utf8 scripts/check_unit11.py --draft --tex` checks task/key references, exact prompts/passages, literal and derived paradigms, evidence identities and logs. It supplements linguistic and visual review. Render all pages with Ghostscript `png16m`, `-r150 -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -dBATCH -dNOPAUSE`, supplying TeX Live's `Resource/Init`, `lib` and `kanji` through `-I`.

Build products and export-page images are ignored; inspected identities remain in the ledgers. Source evidence images remain tracked. One-use helpers in ignored build directories are not required generators; rerunning assembly can discard reviewed repairs. Rebuilt PDF metadata can differ, so replace retained PDFs only after full parity and page review.

Checkpoints: contract **`a9c6ce5`**, complete drafts **`730dffe`**, pre-key solutions **`f2b3974`**, accepted text **`460b825`**. Complete exports and reviewed registers are saved at **`b096aca`**. The [handoff](../../docs/HANDOFF.md) records final closure.
