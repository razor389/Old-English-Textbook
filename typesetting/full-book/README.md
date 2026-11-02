# Complete course volumes

| Volume | Physical pages | Contents |
| --- | ---: | --- |
| [Learner’s Book](book.pdf) | 967 | Pronunciation, Units 1–18, sound history, both glossaries, table of contents and grammatical index |
| [Answer Key](answer-key.pdf) | 486 | Pronunciation answers, Units 1–18 keys and table of contents |

The learner volume has twelve pages of Roman-numbered front matter, 938 Arabic-numbered component pages including eight blank versos, and a seventeen-page grammatical index at printed pages 939–955. Its 930 original content pages are complete. The key has four front-matter pages and 482 Arabic-numbered pages, including seven blank versos; all 475 original key pages are complete. Title and deliberate blank pages omit visible folios. Each component begins on a recto.

Contents entries and page numbers are linked. PDF bookmarks include nested sections. The grammatical index has 447 entries under 112 substantive headings, with 74 see headings and 32 see-also groups. Its 493 printed references derive from 360 actual explanation/paradigm targets. Unit sections, exercises and original source locators retain their local numbering.

The [assembly manifest](../../book/contents.json) records exact accepted source identities. The [contract](../../book/coverage.json) preceded implementation at `feb01c8`. Original Markdown, component TeX/PDFs, teaching registers and source evidence remain unchanged. The combined fragments contain only reversible navigation annotations and local document setup. Font features and the shared 165 × 241 mm Cambria layout are retained.

## Reproduction

Run from the repository root with the configured TeX Live 2026, Cambria, Xpdf, Ghostscript, Python and PowerShell/System.Drawing installation:

```powershell
python -X utf8 scripts/build_full_book.py --stage all
python -X utf8 scripts/check_full_book.py
python -X utf8 scripts/render_full_book.py sources
python -X utf8 scripts/render_full_book.py source-pixels
python -X utf8 scripts/render_full_book.py combined
python -X utf8 scripts/render_full_book.py compare
python -X utf8 scripts/render_full_book.py proofs
```

The builder verifies the preservation boundary, generates all 41 fragments, compiles both complete volumes, resolves the index from actual labels, and recompiles until pagination stabilizes. `--stage assemble` and `--stage compile` separate those steps; `--volume learner` or `--volume key` limits compilation. Build PDFs, logs, auxiliary files and raster proofs remain in ignored build directories. A rebuild does not replace the accepted PDFs automatically.

The checker independently removes only the permitted navigation commands and compares every retained TeX body with its accepted source. It compares all 1,405 component pages’ complete PDF text, headers and folios; verifies the positive volume allowlists, source hashes and page counts; and inspects actual PDF destinations, link annotations, bookmarks and page labels through the installed LuaTeX PDF reader. The whole index is compared in heading/subentry order, and each of its 493 numeric link rectangles is bound to its own row, visible index page and target. New navigation text alone has a documented soft-hyphen/quote extraction projection. Accepted-body character comparison uses only NFC and whitespace normalization.

The renderer checks the PDF identities before and after each run. It compares decoded RGB pixels from the page top through 225 mm at 150 dpi, including every body line and running header. A full-width blank guard at 224–226 mm verifies that the cutoff separates content from the changed folio. Footers are checked separately through extracted folios and labelled native-pixel proofs. Every page has a labelled reduced full-page proof and a readable folio proof; every new or changed page has a full-size proof. Generation alone is not visual acceptance.

Review the complete new build and bind its page/proof identities before promoting it. Use `python -X utf8 scripts/check_full_book.py --retained` to verify the retained PDFs after promotion; this writes a separate result under `build/full-book/check/retained/` and preserves the reviewed build reports. PDF metadata can change the file hash on reproduction even when content is identical; fresh exports need fresh acceptance.

## Evidence

The [export review](export-review.json) binds the final PDF identities and independent reviews. [Content provenance](content-map.json), [page accounting](pagination.json), [complete page-text parity](text-parity.json), [navigation](navigation.json), [index locations](index-locations.json), [machine checks](checks.json) and [raster comparison](raster-comparison.json) retain the reproducible evidence. The [index amendments](../../book/amendments.json) preserve all resolved findings without rewriting the source proposals.

Independent reviews cover [the early index](../../book/reviews/index-early.md), [the late index](../../book/reviews/index-late.md), [navigation and new pages](../../book/reviews/navigation.md), [all learner pages](../../book/reviews/learner-pages.md) and [all key pages](../../book/reviews/key-pages.md). Their receipts distinguish reduced page inspection, native-pixel folio inspection and full-size page inspection. Prior detailed page acceptance is inherited only where exact body/header pixel identity is established.
