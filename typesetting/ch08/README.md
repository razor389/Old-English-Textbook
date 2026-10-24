# Unit 8 exports

The complete [learner PDF](chapter-08.pdf) has **30 pages**; the [separate key](answer-key.pdf) has **24**. The editable masters are [student.md](../../chapters/ch08/student.md) and [answer-key.md](../../chapters/ch08/answer-key.md). Both exports contain the complete independently accepted unit: explanations, vocabulary, paradigms, examples, all 66 tasks, both readings, local help and source notes.

All **54 final pages** passed non-author visual inspection. [Individual ledgers](reviews/) retain page-specific observations, actual inspection provenance and exact PDF/image identities. The initial layout keeps short examples with their translations and all four source-dialogue turns together in consistent reading type. Page proof prompted a one-word introductory correction, independently reaccepted at 72ee930: the examples have no visible numbers, so the word numbered was removed. TeX-only repairs attach Cook exercise labels to their prompts and begin key Q02 on a fresh page for comfortable footer clearance. The final v2 render changes learner pages 1, 21 and 22 and key pages 5–18. Reviewers directly reopened all seventeen changed pages and independently verified that the remaining thirty-seven page images are byte-identical to the versions they inspected. [Final presentation acceptance](page-review.json) reconciles every page, the accepted masters, complete parity and clean build logs. No material presentation issue remains open.

## Complete content and independent review

[Content parity](content-parity.json) compares every Markdown block with the actual TeX: **600 prose/heading/list blocks**, **48 tables**, **793 table cells including headers** and **402 editorial comments**. Complete prose also matches the extracted PDF character stream, with only whitespace and Xpdf soft-hyphen encoding normalized. The independent table comparison and every-page inspection cover forms, headings, endings and special characters.

The learner gives **27 logical paradigms with 368 cells in 36 print matrices**. Complete selected interrogative, indefinite and minor demonstrative systems accompany questions and ordinary relatives. Ætēowian has full assigned indicative/subjunctive systems, scīnan full subjunctives, geblētsian both commands, and līf its singular/plural declension. Tables identify every covered person, number, case and gender. Display does not extend a form's stated syntactic or recognition scope.

All **66 graded tasks** have separate models, targets, explanations, alternatives and diagnoses; **all seventeen Cook I.8 prompts** remain exact. Sixteen new examples and the **62-word dialogue**, “The ship and the fish,” retain their checked wording. The exact **72-word, four-turn merchant opening** comes from Cook's *First Book*, printed pp. 129–130 / one-based PDF pp. 145–146: three editorially counted dialogue lines on p. 129, then printed lines 1–7 on p. 130. All **twelve helps and fifteen original notes** are retained. Historical note questions are not additional course tasks. The following goods catalogue remains unassigned.

The [independent review](../../chapters/ch08/review.md), [frozen pre-key solutions](../../chapters/ch08/independent-solutions.md) and [full ledger](../../chapters/ch08/review-ledger.json) record actual solving, all displayed-form checks, source-image evidence and key comparison. The reviewer authored neither master and discloses prior grammar-audit/public-example work. Frozen solution errors and defensible alternatives are adjudicated in the review rather than silently rewriting that witness. Initial page proof caught the phrase “numbered examples” despite invisible example numbers. Removing “numbered” was independently verified and checkpointed before the final exports; all tasks, tables, source text and the frozen witness remain unchanged.

## Rebuilding

Use LuaLaTeX with Cambria and the packages in [book-layout.tex](../book-layout.tex). The trim is 165 × 241 mm; body type is 11/14.3 pt, tables 10.5/13.2 pt and final source references 10/12.8 pt. Both documents use `Ligatures=TeXOff` to preserve literal punctuation. The learner's running title is “Unit 8. Questions and relatives”; its full title appears on the opening page. Unit 8 changes no shared layout or earlier export.

From this directory:

```powershell
New-Item -ItemType Directory -Force build
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-08.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-08.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
pdftotext -enc UTF-8 -layout build/chapter-08.pdf build/chapter-08.txt
pdftotext -enc UTF-8 -layout build/answer-key.pdf build/answer-key.txt
```

The verified toolchain is LuaHBTeX 1.24.0 / TeX Live 2026, Xpdf `pdftotext`, and Ghostscript 10.08.0. On this Windows installation LuaLaTeX needs access to the owner's TeX/font caches. Final logs contain no overfull/underfull boxes, missing characters, font substitutions or unresolved rerun warnings.

From the repository root, `python -X utf8 scripts/check_unit08.py --draft --tex` checks concrete contract references, all task/key IDs and actual matrices, exact prompts/passages, source identities, special-character retention and logs. It is not linguistic proof or visual inspection. Raw hashes and normalized-LF companions distinguish checkout conversion from content changes; a separate substantive contract hash permits later completion metadata without changing the reviewed learning contract.

Render every page with Ghostscript's `png16m` device and `-r150 -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -dBATCH -dNOPAUSE`. The installed TeX Live Ghostscript needs its `Resource/Init`, `lib` and `kanji` directories supplied with `-I`. The final sets are **learner-v2** and **key-v2**. Export-page images and build products are ignored; their reviewed identities and provenance are retained in the ledgers. Audited source-page images remain tracked.

Retained TeX is authoritative for rebuilding. The one-use assembly/parity aids under ignored `build/` directories are not required generators; reassembly can discard reviewed presentation adjustments. PDF metadata can change during rebuilding. Replace a retained PDF only after complete content and page review.

Checkpoints: contract before prose **`8751984`**, full drafts **`d20c6d5`**, frozen pre-key solutions **`9763993`**, accepted text **`72ee930`**. Complete exports and reviewed registers are ready for their local checkpoint. The [handoff](../../docs/HANDOFF.md) records final Beads closure and completion metadata.
