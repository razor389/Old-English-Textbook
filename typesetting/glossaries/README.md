# Complete glossary exports

The [Old English–English PDF](old-english.pdf) has **58 pages** and 1,305 lexical entries with 300 selected cross-reference spellings. The [English–Old English PDF](english.pdf) has **100 pages** and 2,054 English headings. Both export their full [editable masters](../../glossaries/README.md), including usage introductions and the Old English correction appendix.

All **158 current pages** were actually inspected. The [current export receipt](opening-2026-11-02-export-review.json), [complete-content report](opening-2026-11-02-content-check.json), and [independent integration review](../../docs/revisions/opening/reviews/glossary-integration-final.json) bind acceptance to the revised masters, TeX and PDFs. Current coverage includes all 5,587 actual surface types, 1,417 tasks and 1,690 register senses. The original 137-file boundary remains frozen; the [revision bridge](../../docs/revisions/opening/glossary-supplement.json) records 21 exact authorized deltas. Earlier export/page/whitespace receipts remain evidence for their named checkpoints.

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
python -X utf8 scripts/check_glossary_exports.py --build --revision docs/revisions/opening/glossary-supplement.json --report build/glossary-export-check.json
```

The renderer converts the full Markdown masters without regenerating vocabulary. The check compares ordered Markdown blocks, TeX and complete PDF text; verifies lexical, selected cross-reference and exercise routes; checks diagnostic provenance and compiler messages; and checks the protected course boundary. Omit `--build` to check the retained PDFs. A recreated PDF may have a different binary hash because of build metadata; inspect its actual content and pages before replacing an accepted PDF.

Render every page of a changed PDF at 150 dpi or better with the configured Ghostscript installation, and record an actual page-by-page inspection. Text checks and matching counts do not certify visual or linguistic quality. Logs and raster images remain ignored under `build/`; the compact page ledgers retain image hashes and observations. Historical raw/LF review identities are documented in [record-identities.json](../../glossaries/record-identities.json).

The glossary commands are separate from the 36-document unit builder and the pronunciation export check. Local Git revisions preserve the work; remote pushes remain user-controlled.

For deliberate corpus or task changes, refresh the versioned inventory with `scripts/refresh_opening_glossary_inventory.py --revision docs/revisions/opening/glossary-supplement.json` after the exact source, review and lookup bindings are reconciled. Do not rewrite the original inventories or rerun historical dictionary assemblers. The earlier [whitespace receipt](../../glossaries/master-whitespace-rebind.json) applies only to its original checkpoint.
