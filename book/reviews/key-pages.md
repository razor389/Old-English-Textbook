# Complete key: page review

Accepted for the final 486-page key PDF. No material or optional layout, assembly, or folio findings remain.

Reviewer: `/root/sound_design`. The reviewer did not author the assembly or its new front matter, but did author the raster verifier. The manual inspection recorded here is separate from automated comparison; it is not a fresh linguistic solution of the previously accepted key tasks.

## Actual inspection

- All 486 pages inspected in 31 labelled contact sheets as reduced structural overviews.
- All 486 footer strips inspected at native pixel resolution in 21 labelled folio sheets.
- All 11 new/blank pages inspected individually at native page resolution: physical pages 1–4, 8, 56, 96, 124, 234, 346, and 454.
- All 475 retained source pages from 19 key components have exactly equal decoded RGB header/body pixels in the accepted source and assembled PDF. No mismatch or cutoff-guard flag occurred.

The page overviews show consistent margins, complete tables and paragraphs, expected component transitions, and no clipping, collision, or unexpected blank content. Reduced pages are not used to claim word-by-word linguistic review: exact pixel equality establishes preservation of the previously accepted text and special characters. New front matter and changed footer content were inspected at native size.

## New pages and folios

The title, volume description, and complete 19-component contents page fit cleanly. The contents gives starting folios 1, 5, 17, 31, 53, 71, 93, 121, 151, 175, 201, 231, 261, 291, 321, 343, 373, 405, and 451. Physical page 4 is a clean blank verso.

Front-matter PDF labels are i–iv; only ii and iii are printed. Arabic labels run continuously from 1 through 482. The seven inserted body blanks occupy folios 4, 52, 92, 120, 230, 342, and 450, with no printed folio or stray header/body text. All component starts are recto. Every printed numeral agrees with its page label and sits at the expected outside edge without clipping.

## Pixel boundary and evidence

All source and combined pages were rendered at 150 dpi as RGB8, 974 × 1423 pixels, using identical Ghostscript parameters. Exact decoded RGB bytes were compared through row 1327, inclusive, at the 225 mm footer cutoff. Every full-width pixel in the 224–226 mm guard band is white. Every excluded footer strip was then visually checked at native resolution; it contains no omitted body text.

| Evidence | SHA-256 |
|---|---|
| Pdf | `a8b4c6df5864c51abf51161fd7d6f1a63e13fa88c8bb38d805e52e6c6ebbccd8` |
| Comparison | `f81718fc48128c912db2bc9d4b7ace360a384bd74fde01c6e6a86a52d59ce95f` |
| Proof manifest | `5e41d4f30b34b5c567e859c00ff7806c5ce0f00ab2d858bec765243d2925e3a3` |
| Pagination | `f9899f54384485dba00dfd147f248510f944493194b99802ceb2c97c0aa8343c` |
| Renderer | `f42b0427a61f8f8559f95b45889dc17885fbb9320e6f23f9deee84ca1f328c06` |
| Actual view ledger | `c4e5ec348bd63abde7b3706d62dd1ee1206b6e17395af77443b54929590da771` |

The machine-readable receipt in `book/reviews/key-pages.json` embeds all 63 actual-view records and maps each of the 486 pages to its contact proof, footer proof, source page, native raster hash, and full-page inspection where required. Reproducible raster and proof artifacts remain under ignored `build/full-book/raster/`; their manifest identities are bound above.

Acceptance applies only to the PDF hash recorded here.
