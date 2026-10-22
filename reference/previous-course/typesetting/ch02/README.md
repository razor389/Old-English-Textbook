# Chapter 2: Plural nouns

This directory uses the approved compact Chapter 1 layout for the complete [student chapter](../../chapters/ch02/student.md) and separate [answer key](../../chapters/ch02/answer-key.md). The complete [learner PDF](chapter-02.pdf) has five pages; the [key PDF](answer-key.pdf) has three. Both passed content comparison, coordinator inspection, and independent inspection of every rendered page on 22 October 2026; see the [review](../../chapters/ch02/review.md).

The exports retain all twenty-two vocabulary rows, all twelve prompts of Cook's Group I, Exercise 2, nine added tasks and their answers, the reading with all four support rows, and all four source notes in each document. The learner PDF includes both numbered examples and the requested strong-neuter weight explanation; the key explains **sǣd** in review 3. Markdown remains the editorial master. Stable item identifiers are retained in TeX comments; readers see ordinary section and task numbering. External links remain live; links to local editorial files retain their visible labels without PDF hyperlinks.

## Files

- `chapter-02.tex` → `chapter-02.pdf`: complete learner chapter.
- `answer-key.tex` → `answer-key.pdf`: complete answer key.
- `book-layout.tex`: approved compact layout, copied for this chapter.
- `build/`: compilation products and rendered page images.

## Design

LuaLaTeX; Cambria; a provisional 165 × 241 mm page; 11-point body text with 14.3-point leading; compact black headings and restrained spacing. Tables repeat their headings if continued. The running title is “Plural nouns.” Typography and spelling follow the approved Chapter 1 treatment, including UTF-8/NFC text and unchanged vowel marks. The existing Cambria faces were checked for the required Old English characters in regular, italic, bold, and bold italic during Chapter 1. The actual Chapter 2 characters and tables have also passed inspection. Final logs contain no missing-character, font-substitution, or box warnings.

The exposition's arrows use the standard LaTeX math arrow. No fonts, packages, converter, or publishing pipeline are added. The TeX sources are complete chapter files maintained alongside their Markdown originals.

## Build and inspect

Run in `typesetting/ch02` from PowerShell:

```powershell
New-Item -ItemType Directory -Force build | Out-Null
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-02.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-02.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
rungs '-dSAFER' '-dBATCH' '-dNOPAUSE' '-sDEVICE=png16m' '-r144' '-dTextAlphaBits=4' '-dGraphicsAlphaBits=4' '-sOutputFile=build/chapter-02-%02d.png' 'build/chapter-02.pdf'
rungs '-dSAFER' '-dBATCH' '-dNOPAUSE' '-sDEVICE=png16m' '-r144' '-dTextAlphaBits=4' '-dGraphicsAlphaBits=4' '-sOutputFile=build/answer-key-%02d.png' 'build/answer-key.pdf'
```

Check both logs for missing characters, font substitutions, and box warnings. Inspect every rendered page, including continued tables and the reading. Compare all vocabulary rows, source items, added task identifiers, model answers, and notes with the approved Markdown. After these checks pass, copy the complete PDFs to this directory:

```powershell
Copy-Item -LiteralPath build/chapter-02.pdf -Destination chapter-02.pdf
Copy-Item -LiteralPath build/answer-key.pdf -Destination answer-key.pdf
```

The restricted execution environment requires permission to run the installed TeX Live executables from AppData. Compilation and rendering are performed by the coordinator for this chapter.
