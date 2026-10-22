# Chapter 1: complete PDFs

The learner chapter and answer key are complete exports of the authoritative [student chapter](../../chapters/ch01/student.md) and [answer key](../../chapters/ch01/answer-key.md). They include all thirty nouns, all twenty-five tasks and answers, the reading and its support, and the source notes. The earlier specimen is a superseded development proof, not a deliverable.

## Files

- `chapter-01.tex` → [chapter-01.pdf](chapter-01.pdf): complete learner chapter, five pages.
- `answer-key.tex` → [answer-key.pdf](answer-key.pdf): complete answer key, three pages.
- `book-layout.tex`: shared layout.
- `build/`: compilation products, rendered page images, and development proofs.

The Markdown remains the editorial master. The TeX sources preserve its prose and numbering. Stable item identifiers are retained as comments; bibliographic references appear in the endnotes. External links remain live in PDF. Links to local editorial files retain their visible labels without PDF hyperlinks, so the PDFs do not depend on the repository's directory structure.

## Design and fonts

LuaLaTeX uses a provisional 165 × 241 mm page, 11-point body text with 14.3-point leading, compact black headings, and restrained spacing. Tables repeat their headings if they continue onto another page. The design is a working book layout, not a final publication format.

Cambria supplies the text, with Latin Modern Mono available for identifiers in development materials. These fonts and all packages were already installed. Explicit Cambria bold and italic filenames avoid a local family-name lookup problem. The body face was checked directly in LuaLaTeX: regular Cambria, not the bold face. UTF-8/NFC spellings and vowel marks are preserved.

The separate `build/character-proof.tex` and PDF test **þ ð æ ǣ ā ē ī ō ū ȳ ę** and capitals in regular, italic, bold, and bold italic. The font proof compiled without missing-character or font-substitution warnings and was visually inspected. TeX Gyre Termes was rejected because it lacks precomposed **ǣ**, **ȳ**, and their capitals.

## Build and inspect

Run in `typesetting/ch01` from PowerShell:

```powershell
New-Item -ItemType Directory -Force build | Out-Null
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-01.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-01.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
rungs '-dSAFER' '-dBATCH' '-dNOPAUSE' '-sDEVICE=png16m' '-r144' '-dTextAlphaBits=4' '-dGraphicsAlphaBits=4' '-sOutputFile=build/chapter-01-%02d.png' 'build/chapter-01.pdf'
rungs '-dSAFER' '-dBATCH' '-dNOPAUSE' '-sDEVICE=png16m' '-r144' '-dTextAlphaBits=4' '-dGraphicsAlphaBits=4' '-sOutputFile=build/answer-key-%02d.png' 'build/answer-key.pdf'
```

Check both logs for missing characters, font substitutions, and overfull boxes, then inspect all rendered pages, especially continued tables and Old English marks. After the checks pass, copy the complete PDFs to this directory:

```powershell
Copy-Item -LiteralPath build/chapter-01.pdf -Destination chapter-01.pdf
Copy-Item -LiteralPath build/answer-key.pdf -Destination answer-key.pdf
```

The restricted execution environment requires permission to run the installed TeX Live executables from AppData. No new dependency or general publishing pipeline is introduced. The source crosswalk, linguistic evidence, and editorial decisions remain in the chapter's coverage file and editorial record.

Final compact build, 22 October 2026: both files compiled twice; neither log has missing-character, font-substitution, overfull-box, or underfull-box warnings. The coordinator inspected all eight rendered pages. The complete vocabulary and model tables fit on single pages; preparation, reading, and source notes are kept together. Content parity and the independent review are recorded in [the chapter review](../../chapters/ch01/review.md).
