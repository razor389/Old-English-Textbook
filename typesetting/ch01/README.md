# Unit 1 exports

Complete reviewed exports, 22 October 2026: [learner PDF](chapter-01.pdf), **22 pages**, and [separate key PDF](answer-key.pdf), **12 pages**. Editable masters are [student.md](../../chapters/ch01/student.md) and [answer-key.md](../../chapters/ch01/answer-key.md). Complete TeX sources are [chapter-01.tex](chapter-01.tex) and [answer-key.tex](answer-key.tex), using the shared [layout](../book-layout.tex).

Cambria, 165 × 241 mm trim, 11-point body and 14.3-point leading are retained. Paradigms remain intact. The vocabulary retains all six original fields in four readable columns, with genitive and plural diagnostics on separate lines. Long tables repeat their headings. Case frames and key answer blocks stay together. Old English words are not automatically hyphenated.

## Complete-content and page checks

The separate content audit compared all 183 learner and 107 key prose/task/note paragraphs, 17 learner and two key tables, all 44 vocabulary entries and their 264 original fields, every reading-help row, all source notes, and the exact 69-word reading. All 92 learner task IDs, 92 key IDs, 79 teaching IDs and eight example IDs survive in TeX comments. The Markdown masters retain their textual-review hashes.

The coordinator and independent reviewer inspected every page, including all paradigms, hooked e, eth/thorn, vowel marks, the starred sea reconstruction, source prompts, reading, explanations and endnotes. Initial pagination repairs kept CASE02/CASE10 help with their frames and two key headings with their content. A later apparent reading-table header issue disappeared in a fresh direct image view; identical bitmap hashes established that no further TeX change was needed. See the [independent page ledger](../../chapters/ch01/review.md) for every page and finding.

After the final additional learner compile, the coordinator rendered all 22 pages again as `build/verified-chapter-01-pNN.png`. Every bitmap SHA-256 matched the inspected `final-chapter-01-pNN.png` series. The key's inspected series is `build/final-answer-key-pNN.png`, pages 01–12. Final PDF copies match the stable build files byte for byte. Both LuaLaTeX logs have no missing-character, font, overfull/underfull box, reference, or table-width warnings. `python -X utf8 scripts/check_unit.py --draft --tex`, run from the repository root, passes.

Xpdf 4.00 inserts some artificial spaces after macron letters in extracted text. The reading-only character comparison ignores whitespace while preserving all other Unicode characters and punctuation; word boundaries were checked visually. Exact Cook prompt checks remain strict. Ghostscript reports missing optional FAPI map files but renders the embedded fonts correctly. Neither limitation requires a spelling or font substitution.

## Reproduction

Run from this directory with the existing TeX Live 2026 installation and Cambria fonts. The build directory and temporary render/text/log products are ignored by Git. TeX is maintained directly; the one-use initial assembly helper is not a conversion pipeline.

```powershell
New-Item -ItemType Directory -Path build -Force
foreach ($unitStem in 'chapter-01', 'answer-key') {
    foreach ($unitPass in 1..2) {
        & 'C:/Users/Ross/AppData/Local/texlive/2026/bin/windows/lualatex.exe' '-interaction=nonstopmode' '-halt-on-error' '-output-directory=build' "$unitStem.tex"
    }
    & 'C:/Program Files/Git/mingw64/bin/pdftotext.exe' '-enc' 'UTF-8' '-layout' "build/$unitStem.pdf" "build/$unitStem.txt"
}
```

Repeat LuaLaTeX if a table-width or reference warning requests another pass. Inspect both logs and every rendered page before replacing the reviewed PDF copies. To render each complete PDF at the inspection resolution:

```powershell
foreach ($unitStem in 'chapter-01', 'answer-key') {
    & 'C:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs/bin/gswin64c.exe' `
        '-IC:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs/Resource/Init' `
        '-IC:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs/lib' `
        '-IC:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs/kanji' `
        '-sDEVICE=png16m' '-r150' '-dTextAlphaBits=4' '-dGraphicsAlphaBits=4' `
        '-dBATCH' '-dNOPAUSE' "-sOutputFile=build/check-$unitStem-p%02d.png" "build/$unitStem.pdf"
}
```

Use a fresh image filename when verifying a changed render. The optional raster products need not be committed; the complete TeX, PDFs, content checks and review record are retained.

## Reviewed file identities

SHA-256 of the final PDF bytes:

| File | SHA-256 |
|---|---|
| chapter-01.pdf | `2a59aae475ca3bf98d07d73d7a7af3f9656e5caf2c0c8547e38e9a4f760064d0` |
| answer-key.pdf | `3d5a72d2d5f6f78010235e76dceb6eb5268db24328b102745f439845359d693f` |

Recompilation can change PDF metadata and therefore byte hashes. New output still requires content and page verification before it replaces these reviewed copies.
