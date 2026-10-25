# Unit 10 exports

The complete [learner PDF](chapter-10.pdf) has **40 pages**; the [separate key](answer-key.pdf) has **29**. The editable masters are [student.md](../../chapters/ch10/student.md) and [answer-key.md](../../chapters/ch10/answer-key.md). All 89 tasks, vocabulary, paradigms, readings, local help and source notes are included.

All **69 final pages** passed non-author visual inspection. [Individual ledgers](reviews/) retain page-specific observations and exact PDF/image identities. Wide adjective paradigms use stacked singular/plural panels at unchanged 10.5pt type. Independent parity reconstructs every original seven-column coordinate; repeated case labels are page furniture. The long unnan key entry permits natural page breaks between complete tables and commentary. Task labels remain with their prompts or answers. Five table widths were redistributed after initial box diagnostics; all linguistic content, headers, cells and accepted Markdown remain unchanged. Non-author proof found four stranded key section headings. TeX-only page breaks place each with its first answer. All eight changed key pages were directly reinspected, and the other 21 final key images were independently verified byte-identical to their inspected predecessors. All 40 learner pages retain direct v1 inspection. [Final acceptance](page-review.json) reconciles every page, full content parity, unchanged accepted masters and clean build logs.

## Content and review

[Complete parity](content-parity.json) covers **775 prose/heading/list blocks, 49 tables, 1205 cells including headers, and 546 editorial comments**. An independent Markdown inventory matches decoded TeX; full prose matches extracted PDF text after whitespace and soft-hyphen normalization. Visual review includes all tables, endings and special characters.

The learner gives **56 defined paradigms / 779 supported cells** through 36 matrices and 29 lexical diagnostic rows: 306 literal nominal cells, 336 explicit model derivations and 137 literal grammar cells. Exceptional fæder, hand and gāt are printed in full. Unnan retains a visible gap for the unsupported present second singular, with no invented form. Complete forms retain their stated lexical and syntactic scope.

All **55 Cook III.13–15 prompts** retain their wording and identifiers, alongside 34 original tasks and fourteen translated examples. The **50-word new account**, “The stranger and the monk,” precedes the exact **59-word Judgment opening**, Cook p134 / one-based PDF150, editorial lines1–7 anchored by printed5. All fourteen original notes and nine source helps remain. Two exercise expressions remain supplied. The following royal speech is outside the assignment.

The [reviewer](../../chapters/ch10/review.md) solved all 89 actual tasks before key/private-answer access. [Frozen solutions](../../chapters/ch10/independent-solutions.md) and the [ledger](../../chapters/ch10/review-ledger.json) retain the comparison, actual display routes, fresh source checks and resolved findings. The reviewer authored neither master nor graded task and discloses earlier grammar/public-composition work. No material finding remains open.

Review amendment **U10-AMEND-01** completes the instrumental and adjective locators as Cook §§174–178, pp97–99, and §§55–60, pp38–41, and synchronizes the supplied **swā lange swā** scope with its already printed *inasmuch as* interpretation. Original audit annotations remain preserved; assignments and teaching statuses do not change.

## Rebuilding

Markdown remains the editable master. Retained TeX preserves reviewed layout repairs. Use LuaLaTeX with Cambria and [book-layout.tex](../book-layout.tex): 165 × 241 mm trim, body 11/14.3 pt, tables 10.5/13.2 pt and source endnotes 10/12.8 pt. Both documents use `Ligatures=TeXOff`; no earlier export or shared layout changed.

From this directory:

```powershell
New-Item -ItemType Directory -Force build
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-10.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-10.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
pdftotext -enc UTF-8 -layout build/chapter-10.pdf build/chapter-10.txt
pdftotext -enc UTF-8 -layout build/answer-key.pdf build/answer-key.txt
```

The checked toolchain is TeX Live 2026 LuaHBTeX, Xpdf pdftotext and Ghostscript. This Windows installation needs access to the owner's font caches. Final logs contain no overfull/underfull boxes, missing characters, font substitutions or unresolved rerun warnings.

From the repository root, `python -X utf8 scripts/check_unit10.py --draft --tex` checks actual task/key references, exact prompts/passages, literal and derived paradigms, evidence identities and logs. It does not replace linguistic or visual review. Render all pages with Ghostscript `png16m`, `-r150 -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -dBATCH -dNOPAUSE`, supplying TeX Live's `Resource/Init`, `lib` and `kanji` through `-I`.

Build products and export-page images are ignored; inspected identities remain in the ledgers. Source evidence images remain tracked. One-use helpers in ignored build directories are not required generators; rerunning assembly can discard reviewed repairs. Rebuilt PDF metadata can differ, so replace retained PDFs only after full parity and page review.

Checkpoints: contract **`86e073f`**, complete drafts **`a1f8d6f`**, pre-key solutions **`3684087`**, accepted text **`08ed659`**. Complete exports and reviewed registers are saved at **`126e927`**. The [handoff](../../docs/HANDOFF.md) records final closure.
