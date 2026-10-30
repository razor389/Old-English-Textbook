# Sound-history appendix export

The complete [learner PDF](sound-history.pdf) has **12 pages**. Its editable master is [student.md](../../appendices/sound-history/student.md); [sound-history.tex](sound-history.tex) is generated from that entire master. The appendix uses the shared Cambria layout, with eight tables and thirteen source notes. It has no exercises or answer key.

The contract preceded prose at `86ca81e`. Independent [Cook](../../appendices/sound-history/review/cook.md) and [Fulk](../../appendices/sound-history/review/fulk.md) reviews accept all nine sections, fifteen example groups and twenty-five historical claims. The [amendments](../../appendices/sound-history/authoring-amendments.json) retain the stress-scope correction and two clarity refinements. All 44 Old English forms have existing dictionary routes in the [additive access inventory](../../appendices/sound-history/glossary-access.json).

The [complete-content check](content-check.json) covers all 91 prose and heading blocks, eight tables / 100 cells, 242 bold example and notation occurrences, and the complete ordered PDF text. Compilation has no overfull/underfull boxes, missing characters or other reported diagnostics. All 191 protected earlier course/glossary files retain their exact identities. These checks support, rather than replace, the independent linguistic review and [actual twelve-page inspection](page-review.json). The [export receipt](export-review.json) binds the final artifacts and evidence.

An initial proof exposed narrow noun-table headings and an incorrect intercolumn-space allocation. The builder now allocates the actual table padding, uses an elastic right margin and gives the two noun-form columns adequate width. All content is unchanged. The reference table continues onto page 11 with its header repeated; the final row and all thirteen source notes were inspected.

## Reproduction

Run from the repository root with Python, LuaLaTeX and Cambria installed:

```powershell
python -X utf8 scripts/build_sound_history_export.py
New-Item -ItemType Directory -Force typesetting/sound-history/build | Out-Null
Push-Location typesetting/sound-history
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build sound-history.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build sound-history.tex
Pop-Location
python -X utf8 scripts/check_sound_history_export.py --build --report build/sound-history/reproduction-check.json
```

The checker uses the installed Xpdf `pdftotext` at `C:/Program Files/Git/mingw64/bin/pdftotext.exe`, as the existing glossary checker does. Update that tool path if reproducing on another machine. LuaLaTeX must be able to read the installed Windows font files. Logs and raster proofs stay in ignored build directories.

Inspect every page of a reproduction before replacing the retained PDF. The accepted proof was rasterized with Ghostscript at 150 dpi, with text and graphics antialiasing set to 4; per-page image identities are in the page receipt. A fresh PDF may have different creation metadata and needs a new export identity. The checker without `--build` checks the retained PDF against the current master, TeX, inventory and compiler log:

```powershell
python -X utf8 scripts/check_sound_history_export.py --report build/sound-history/retained-check.json
```
