# Unit 2 complete exports

The [learner chapter](chapter-02.pdf) has 19 pages; the separate [answer key](answer-key.pdf) has 14. Their complete, hand-reviewed TeX sources are [chapter-02.tex](chapter-02.tex) and [answer-key.tex](answer-key.tex). The editorial masters are [student.md](../../chapters/ch02/student.md) and [answer-key.md](../../chapters/ch02/answer-key.md). The accepted text was not changed during typesetting.

The inherited [Cambria layout](../book-layout.tex) is unchanged: 165 × 241 mm trim, 11-point body text, 14.3-point leading. The seven wide finite-verb tables are displayed as paired present and preterite panels at 10.5 points with 13.2-point leading. Each pair retains the original complete row, with the verb label repeated. All exercise prompts and each key answer with its table and explanations are kept together. Vocabulary and principal-part tables repeat their headers when continued. The connected narrative and complete source reading retain the larger reading style. All 17 learner source notes and the key’s source note and concluding bibliography paragraph are present.

## Verified identities

| File | SHA-256 |
| --- | --- |
| Accepted learner Markdown | `7ac884d55c143f1e5ce6d5eead3b09ec11ea9121cb5f23f4c96e0a9addb0dea2` |
| Accepted key Markdown | `d857f67bf3ee98905dea2b9cbccf21f3f4d88644c3f81e499d18a661c097bdf5` |
| `chapter-02.pdf` | `54eddab2d7f2284a6e4bd82c5da34cb1fd71baa7af11e7db576ada41b10b3a0d` |
| `answer-key.pdf` | `d9ef81ef44157f08d4e9f1e1a450eaa761b30031c986ecbb61608534df3c1608` |

The tracked PDFs are byte-identical copies of the inspected files in `build/`. Copying occurred only after all pages passed the typesetter, coordinator and independent reviewer. No recompilation occurred after the approved image set was made. PDF metadata may change a byte hash on a later rebuild; the frozen identities above identify the reviewed copies.

In `content-parity.json`, `tex_sha256` identifies the compiled working-file bytes, which have CRLF line endings. `.gitattributes` normalizes TeX to LF in Git; the companion `tex_sha256_normalized_lf` identifies the same content with CRLF converted to LF, as found in an LF checkout. Both identities are retained. Adding this metadata did not change the TeX or PDF bytes or require recompilation.

## Content and page checks

[content-parity.json](content-parity.json) records the full comparison with the accepted Markdown. An independent inventory of the masters was compared with decoded bodies of the actual TeX, without using the assembly helper’s generated content maps:

- Learner: 175 paragraph, heading and list blocks; 10 original tables and all 439 original table cells, including headers; all 102 editorial comments.
- Key: 98 paragraph, heading and list blocks; 14 tables and all 245 cells; all 122 editorial comments.
- Both titles, every full prose block in PDF extraction, all 61 learner tasks and their 61 keyed counterparts, all 89 teaching IDs, exact composed readings and examples, and the complete 61-word source passage are retained. The finite panels were reconstructed into the original eight-column rows for cell comparison.

All 33 pages were freshly rendered at 150 dpi as `build/initial-chapter-02-p01.png` through `p19.png` and `build/initial-answer-key-p01.png` through `p14.png`. The typesetter, coordinator and independent reviewer each inspected every page. Tables, reading boundaries, complete task and key blocks, special letters, vowel marks, notes and ordinary prose continuations passed. There were no requested layout repairs. [page-review.json](page-review.json) retains the image hashes and page ledger; [the independent review](../../chapters/ch02/review.md) records the separate presentation verdict.

Final LuaLaTeX logs contain no missing-character, font-substitution, overfull, underfull or rerun warnings. The repository’s concrete export check, `python -X utf8 scripts/check_unit02.py --draft --tex`, passes on these final files. The full content audit additionally covers all prose, vocabulary fields and key explanations, beyond that checker’s required IDs and exact task/reading strings.

Xpdf 4.00 introduces artificial spaces around some macron letters and represents printed literal hyphens as U+00AD in UTF-8 extraction. The checks ignore extraction whitespace and map U+00AD back to `-`; they do not remove hyphens or normalize Old English spelling. Every source-reading and composed-reading word boundary was also checked visually. Ghostscript reports missing optional `FAPIfontmap` and `FAPIcidfmap` files; the embedded Cambria fonts rendered correctly on every page. The installed `rungs` wrapper is broken, so the direct Ghostscript executable is used below.

## Reproduction

Run the following PowerShell commands from `typesetting/ch02/`. The chosen fonts and TeX Live installation must be available; do not silently substitute fonts or spelling. `build/` is ignored. The one-use assembly and parity helpers in that directory are development artifacts, not a publishing pipeline; the complete tracked TeX is the reproducible source.

```powershell
New-Item -ItemType Directory -Force -Path build
& 'C:/Users/Ross/AppData/Local/texlive/2026/bin/windows/lualatex.exe' '-interaction=nonstopmode' '-halt-on-error' '-output-directory=build' 'chapter-02.tex'
& 'C:/Users/Ross/AppData/Local/texlive/2026/bin/windows/lualatex.exe' '-interaction=nonstopmode' '-halt-on-error' '-output-directory=build' 'chapter-02.tex'
& 'C:/Users/Ross/AppData/Local/texlive/2026/bin/windows/lualatex.exe' '-interaction=nonstopmode' '-halt-on-error' '-output-directory=build' 'answer-key.tex'
& 'C:/Users/Ross/AppData/Local/texlive/2026/bin/windows/lualatex.exe' '-interaction=nonstopmode' '-halt-on-error' '-output-directory=build' 'answer-key.tex'
& 'C:/Program Files/Git/mingw64/bin/pdftotext.exe' '-enc' 'UTF-8' '-layout' 'build/chapter-02.pdf' 'build/chapter-02.txt'
& 'C:/Program Files/Git/mingw64/bin/pdftotext.exe' '-enc' 'UTF-8' '-layout' 'build/answer-key.pdf' 'build/answer-key.txt'
& 'C:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs/bin/gswin64c.exe' '-IC:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs/Resource/Init' '-IC:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs/lib' '-IC:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs/kanji' '-sDEVICE=png16m' '-r150' '-dTextAlphaBits=4' '-dGraphicsAlphaBits=4' '-dBATCH' '-dNOPAUSE' '-sOutputFile=build/rebuilt-chapter-02-p%02d.png' 'build/chapter-02.pdf'
& 'C:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs/bin/gswin64c.exe' '-IC:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs/Resource/Init' '-IC:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs/lib' '-IC:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs/kanji' '-sDEVICE=png16m' '-r150' '-dTextAlphaBits=4' '-dGraphicsAlphaBits=4' '-dBATCH' '-dNOPAUSE' '-sOutputFile=build/rebuilt-answer-key-p%02d.png' 'build/answer-key.pdf'
```

Review every newly rendered page and the complete logs before replacing the tracked PDFs. From the repository root, copy the approved products and run the export check:

```powershell
Copy-Item -LiteralPath 'typesetting/ch02/build/chapter-02.pdf' -Destination 'typesetting/ch02/chapter-02.pdf'
Copy-Item -LiteralPath 'typesetting/ch02/build/answer-key.pdf' -Destination 'typesetting/ch02/answer-key.pdf'
python -X utf8 scripts/check_unit02.py --draft --tex
```
