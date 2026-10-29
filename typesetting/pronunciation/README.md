# Pronunciation guide and practice key

The complete [learner PDF](pronunciation.pdf) has **9 pages**, including one page of source notes. The [separate key](answer-key.pdf) has **3 pages** and answers all **25** practice questions. Read the guide before Unit 1; every word meaning and the short reading's grammar are supplied.

American English examples identify individual sounds. Plain instructions explain tongue position, lip rounding, airflow and voice where an ordinary American equivalent is unavailable. Three optional phonetic symbols appear once each; there are no transcription exercises. The guide selects explicit Cook/Fulk conventions, with differences explained in the source notes. Its short sentence is a declared adaptation of Cook's Creation opening.

The editable [learner master](../../guides/pronunciation/student.md), [key](../../guides/pronunciation/answer-key.md), [contract](../../guides/pronunciation/coverage.json), and [example inventory](../../guides/pronunciation/examples.json) retain teaching scope and provenance. The contract was saved before prose at `b97019e`. Independent solutions were frozen before key comparison at `14ae55c`; the amended D3 solution and adaptation assessment were frozen at `3ef400e`. The [independent review](../../guides/pronunciation/review/review.md) resolves all material findings. The [source audit](../../sources/audits/pronunciation/cook/anginn-note.md) preserves the investigation of an unselected example.

The [export ledger](export-review.json), [complete-content check](content-check.json), [learner page review](page-review-learner.json), and [key page review](page-review-key.json) bind acceptance to the retained files. All twelve pages were actually inspected. All 129 protected earlier course files retain their recorded identities; the eighteen-unit assignments and cumulative registers are unchanged.

The shared Cambria layout uses 11-point body text and 10.5-point tables; the final source-note page uses 9.5-point type. The full simple-vowel table stays together, and the C6 key explanation is kept on one page. Retained TeX includes these pagination decisions. Do not rerun the one-use initial assembler to reproduce the accepted layout.

## Reproduction

From the repository root, with the configured TeX Live, Cambria and Xpdf installation:

```powershell
New-Item -ItemType Directory -Force typesetting/pronunciation/build | Out-Null
Push-Location typesetting/pronunciation
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build pronunciation.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build pronunciation.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
Pop-Location
python -X utf8 scripts/check_pronunciation_exports.py --build --report build/pronunciation-export-check.json
```

The check independently compares the Markdown prose and table inventory with the retained TeX and complete PDF text. It also checks ordered task/key IDs, special characters, compiler diagnostics and protected course identities. Omit `--build` after compilation to check the retained PDFs. A changed export needs fresh rendering and inspection of every page before it replaces an accepted PDF; the text check alone does not certify page appearance or pronunciation accuracy. Build logs and page images remain ignored under `build/`.

These two front-matter documents have their own check and reproduction commands. The existing course build command continues to cover the 36 unit documents. Local commits preserve the work; remote pushes remain user-controlled.
