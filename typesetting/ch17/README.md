# Unit 17 exports: connected exposition, praise and figurative language

The complete [learner PDF](chapter-17.pdf) has **94 pages** and the separate [answer key](answer-key.pdf) **45**. Their editable masters are [student.md](../../chapters/ch17/student.md) and [answer-key.md](../../chapters/ch17/answer-key.md). All 139 final pages passed non-author inspection; [page-review.json](page-review.json) binds the final PDFs and page images to the individual inspection ledgers.

The exports include all 103 tasks / 146 answer positions, all 82 assigned Cook prompts, 110 complete bounded systems / 1,234 literal cells, four translated examples, the full 252-word music-performance episode and all 19 original notes / 20 anchors. Original source notes and modern help remain separate. The key gives the complete translation, models, targets, essential meanings, alternatives and diagnoses.

[Full content parity](content-parity.json) verifies 1,724 prose/heading/list blocks, 124 tables and 2,200 table cells including headers. It checks complete Markdown/TeX content and PDF characters alongside visual inspection. The final logs have no missing-character, font-substitution, box or rerun warnings. [Layout adjustments](layout-adjustments.json) retain the repair history. Cambria and the inherited 165 × 241 mm layout remain in use.

The [contract](../../chapters/ch17/coverage.json) preceded prose at `6fc6fc1`. Drafts are saved at `259b14f`, frozen independent solutions at `ed28a8e`, and accepted text at `a137171`. The [fresh text review](../../chapters/ch17/review.md) and [separate paradigm review](../../chapters/ch17/reviews/paradigms.json) resolve material findings. [Authoring amendments](../../chapters/ch17/authoring-amendments.json) preserve the original decisions and later repairs. Complete exports/registers are saved at `99fcc3a`.

## Reproduction

Build the retained TeX from `typesetting/ch17` using LuaLaTeX and Cambria. Repeat each command if the log requests stable references:

```powershell
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-17.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
```

Extract the build PDFs to `build/chapter-17.txt` and `build/answer-key.txt` with `pdftotext -enc UTF-8 -layout`. From the repository root run:

```powershell
python -X utf8 typesetting/ch17/build/_check_content_parity.py
python -X utf8 scripts/check_unit17.py --draft --tex
```

The installed Xpdf executable is `C:/Program Files/Git/mingw64/bin/pdftotext.exe`; use PowerShell’s call operator before the quoted path. The assembly helper records the initial conversion; rerunning it can discard manual layout repairs. Rebuilding does not replace the accepted PDFs or establish a new visual review. Render changed exports into a fresh version and preserve earlier inspected images and ledgers. Typesetting does not regenerate the active registers or sealed source packets.
