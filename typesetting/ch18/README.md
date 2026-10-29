# Unit 18 exports: independent prose consolidation

The complete [learner PDF](chapter-18.pdf) has **66 pages**; the separate [key](answer-key.pdf) has **32**. Editable masters are [student.md](../../chapters/ch18/student.md) and [answer-key.md](../../chapters/ch18/answer-key.md). All 98 final pages passed actual non-author visual inspection; [page-review.json](page-review.json) binds both PDFs and every page image to individual inspection ledgers.

Both exports retain 60 tasks / 87 requested answers, all 47 final Cook prompts, 55 defined systems / 652 literal cells, two translated examples, the full 226-word passage and all 22 original notes / 29 anchors. The separate key gives models, targets, meanings, explanations, alternatives and diagnoses. [Full parity](content-parity.json) checks 1,221 prose/heading/list blocks, 65 tables and 1,224 table cells. Final logs have no missing-character, font-substitution, box or rerun warnings. [Layout adjustments](layout-adjustments.json) preserve repairs. Cambria and the established 165 × 241 mm layout remain.

Checkpoints: contract `6874c20e7127fa33c41406d1aa6c0b087e59c824`, complete drafts `970fcc1f431f6ce2ccdd1f1c85b2b5e63ae0c16a`, frozen independent solutions `7846befc2c484e8d3e4ff43346da12bf275f5b08`, accepted text `029177713dffa6ff81b81d9a96b41b36e006963f`, complete exports/registers `52ff433bb80c6cf3bf245c5533cdd396362b443f`. [Fresh text review](../../chapters/ch18/review.md), [separate paradigm review](../../chapters/ch18/reviews/paradigms.json) and [amendments](../../chapters/ch18/authoring-amendments.json) retain evidence and resolutions.

## Reproduction

From `typesetting/ch18`, compile the retained TeX twice with LuaLaTeX and Cambria:

```powershell
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-18.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
```

Use `pdftotext -enc UTF-8 -layout` to extract the build PDFs to `build/chapter-18.txt` and `build/answer-key.txt`. The installed executable is `C:/Program Files/Git/mingw64/bin/pdftotext.exe`; PowerShell requires its call operator before a quoted executable path. From the repository root run:

```powershell
python -X utf8 typesetting/ch18/build/_check_content_parity.py
python -X utf8 scripts/check_unit18.py --draft --tex
```

Rerunning assembly can discard manual layout repairs. Rebuilding does not replace accepted PDFs or establish new visual acceptance. Preserve inspected images/ledgers and render changed exports into a fresh version. Do not regenerate sealed audits or rerun register mergers against completed state.
