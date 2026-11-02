# Pronunciation guide and practice key

The complete [learner PDF](pronunciation.pdf) has **12 pages**. The [separate key](answer-key.pdf) has **4 pages** and answers all **25** practice questions. Read the guide before Unit 1; word meanings and the short reading's grammar are supplied.

The guide gives an ordered procedure for **c** and **g**: check letter combinations, distinguish initial from noninitial positions, select palatal **g**, then distinguish stopped from continuous nonpalatal **g**. It states the limits of spelling rules and supplies lexical exceptions. American English cues and mouth instructions explain the sounds; three optional phonetic symbols appear once each. Practice applies the rules to words reserved from the worked examples. The closing sentence adapts Cook's Creation opening.

The editable [learner master](../../guides/pronunciation/student.md), [key](../../guides/pronunciation/answer-key.md), [coverage contract](../../guides/pronunciation/coverage.json), and [example inventory](../../guides/pronunciation/examples.json) record scope and provenance. The current [revision contract](../../docs/revisions/opening/contract.json) was saved before prose at `2540765`. The [independent review](../../docs/revisions/opening/reviews/pronunciation-review.md) records solutions frozen before key access and the resolution of the supplied **sēcan** exception. Its key identity is connected to the final LF-only master by the [newline receipt](../../docs/revisions/opening/reviews/pronunciation-key-newlines.json).

Current acceptance uses the opening revision's [export receipts](../../docs/revisions/opening/exports/) and [every-page review](../../docs/revisions/opening/reviews/pronunciation-pages.json). Earlier `export-review.json`, `content-check.json`, and `page-review-*.json` files retain the original 9-page/3-page acceptance; they do not certify the revised text.

The shared Cambria layout uses 11-point body text and 10.5-point tables. Headings reserve enough following space without creating premature page breaks. Assemble and compile from the repository root:

```powershell
python -B -X utf8 scripts/build_opening_exports.py --stage assemble --select pronunciation/learner,pronunciation/key --output-root typesetting --report build/opening/pronunciation-assemble.json
python -B -X utf8 scripts/build_opening_exports.py --stage compile --select pronunciation/learner,pronunciation/key --output-root typesetting --report build/opening/pronunciation-compile.json
python -B -X utf8 scripts/check_opening_exports.py --select pronunciation/learner,pronunciation/key --output-root typesetting --report build/opening/pronunciation-check.json
python -B -X utf8 scripts/check_opening_revision.py --scope pronunciation --report build/opening/pronunciation-domain-check.json
```

The export check compares all Markdown prose, table cells, ordered task IDs, and complete PDF text, and checks compiler diagnostics and special characters. Add `--pdf-location retained` to check the retained PDFs. The domain check protects the source controls and files outside the authorized revision. Neither check replaces independent linguistic review or inspection of every changed page. Only accepted build PDFs replace the retained files; logs and page images remain ignored under `build/`.

The earlier `check_pronunciation_exports.py` command belongs to the historical initial acceptance. Use the opening revision checks above for these revised masters. Local commits preserve the work; remote pushes remain user-controlled.
