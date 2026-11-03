# Complete course volumes

| Volume | Physical pages | Contents |
| --- | ---: | --- |
| [Learner’s Book](book.pdf) | 971 | Pronunciation, Units 1–18, sound history, both glossaries, linked contents and grammatical index |
| [Answer Key](answer-key.pdf) | 488 | Pronunciation answers, Units 1–18 keys and linked contents |

The learner volume has twelve Roman-numbered front-matter pages, 942 Arabic-numbered component pages (935 content pages and seven blank versos), and a seventeen-page index at printed pages **943–959**. The key has four front-matter pages and 484 Arabic-numbered pages (478 content pages and six blank versos). Components begin on rectos; title and deliberate blank pages omit visible folios.

The index has **450 entries under 112 substantive headings**, 75 see headings and 32 see-also groups. Its **500 printed page references** derive from 364 actual explanation/paradigm targets. Contents links, nested PDF bookmarks and continuous page labels are verified. The learner volume contains no answer keys.

The [manifest](../../book/contents.json) and [current component inventory](../../book/proposals/opening-components.json) bind 41 accepted components and 123 source identities. The [opening integration](../../docs/revisions/opening/book-integration.json) records seven changed components and 33 exact old-to-new protected-file deltas; the other protected identities are preserved. Original manifests, index and boundary remain in [revision history](../../docs/revisions/opening/book-history/). The combined fragments add only reversible navigation and local setup; complete accepted component bodies are preserved.

## Reproduction

Run from the repository root with the configured LuaLaTeX, Cambria, Xpdf, Ghostscript and PowerShell/System.Drawing installation:

```powershell
python -B -X utf8 scripts/build_full_book.py --stage all
python -B -X utf8 scripts/check_full_book.py
python -B -X utf8 scripts/render_full_book.py sources --jobs 4
python -B -X utf8 scripts/render_full_book.py source-pixels --jobs 4
python -B -X utf8 scripts/render_full_book.py combined --jobs 4
python -B -X utf8 scripts/render_full_book.py compare --jobs 4
python -B -X utf8 scripts/render_full_book.py proofs --jobs 4
```

The builder verifies all protected and source identities, generates 41 fragments, resolves the index from actual labels, and recompiles until pagination stabilizes. `--stage assemble` resets the index placeholder; use `--stage compile` for subsequent compilation of an existing assembly. Rebuilding does not promote PDFs automatically.

The checker compares all **1,413 component pages** in complete text, verifies every source body after removing only allowed navigation commands, checks answer separation, headers, folios, destinations, bookmarks and labels, and binds all 500 numeric index links to their actual visible rows and targets. The renderer compares decoded body/header RGB pixels at 150 dpi through 225 mm, with a full-width 224–226 mm blank guard separating the changed folio. Footer proofs are inspected separately.

## Current acceptance

The [opening export receipt](opening-2026-11-02-export-review.json) binds the current PDFs, machine checks and independent page reviews. [Complete text parity](text-parity.json), [page accounting](pagination.json), [navigation](navigation.json), [index locations](index-locations.json), [checks](checks.json), and [pixel comparison](raster-comparison.json) describe this build. All **1,459 final pages** have labelled page/folio review; new navigation, index and deliberate blank pages have full-size inspection. Source detail is inherited only where exact decoded body/header pixels match accepted standalone pages.

The [semantic index review](../../book/reviews/opening-index-semantic.json) is separate from actual PDF navigation validation. The original `export-review.json` and earlier book reviews remain historical acceptances of their identified PDFs. After promotion, `python -B -X utf8 scripts/check_full_book.py --retained` verifies retained copies and writes a separate check receipt.
