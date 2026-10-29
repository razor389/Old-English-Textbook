# Complete glossary exports

The [Old English–English PDF](old-english.pdf) has **58 pages** and 1,301 lexical entries with 300 selected cross-reference spellings. The [English–Old English PDF](english.pdf) has **100 pages** and 2,049 English headings. Both export their full [editable masters](../../glossaries/README.md), including usage introductions and the Old English correction appendix.

All **158 pages** were actually inspected. The [export ledger](export-review.json), [complete-content report](content-check.json), [layout decisions](presentation-decisions.json) and linked page ledgers bind acceptance to the retained masters, TeX and PDFs. Independent linguistic review is recorded separately under [glossaries/review](../../glossaries/review/). The complete surface and exercise checks cover 5,580 actual forms, 1,417 tasks and all 1,687 register senses. All 137 protected earlier course files retain their identities.

The shared 165 × 241 mm Cambria layout uses 10.5-point entries with 13.2-point leading, two columns and a 6 mm gap. Old English entry paragraphs have 3.8-point spacing; English has 4-point spacing. The Old English introduction uses the entry size and fits one page; the correction appendix is full width. The renderer preserves these choices, attaches alphabet headings to entries and avoids balancing overflow in the final Old English columns. Earlier 82-page Old English and 101-page English proofs are superseded.

## Reproduction

From the repository root, using the configured TeX Live, Cambria and Xpdf installation:

```powershell
python -X utf8 scripts/build_glossary_exports.py
New-Item -ItemType Directory -Force typesetting/glossaries/build | Out-Null
Push-Location typesetting/glossaries
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build old-english.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build old-english.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build english.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build english.tex
Pop-Location
python -X utf8 scripts/check_glossary_exports.py --build --report build/glossary-export-check.json
```

The renderer converts the full Markdown masters without regenerating vocabulary. The check compares ordered Markdown blocks, TeX and complete PDF text; verifies lexical, selected cross-reference and exercise routes; checks diagnostic provenance and compiler messages; and checks the protected course boundary. Omit `--build` to check the retained PDFs. A recreated PDF may have a different binary hash because of build metadata; inspect its actual content and pages before replacing an accepted PDF.

Render every page of a changed PDF at 150 dpi or better with the configured Ghostscript installation, and record an actual page-by-page inspection. Text checks and matching counts do not certify visual or linguistic quality. Logs and raster images remain ignored under `build/`; the compact page ledgers retain image hashes and observations. Historical raw/LF review identities are documented in [record-identities.json](../../glossaries/record-identities.json).

The glossary commands are separate from the 36-document unit builder and the pronunciation export check. Local Git revisions preserve the work; remote pushes remain user-controlled.

The [master whitespace receipt](../../glossaries/master-whitespace-rebind.json) connects earlier raw-master hashes to the retained Markdown after trailing-space cleanup. Regenerating both TeX files produced byte-identical output, so the page inspections and PDF identities remain valid.
