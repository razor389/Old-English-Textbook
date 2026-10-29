# Course presentation revision

The eighteen-unit course now uses shared `1–3 pl.` rows for identical verbal plurals and a consistent later-unit style for conjugation and declension tables. The revision removes 388 repeated body rows across 194 groups. Full clauses, separate commands, pronouns and numbered response grids retain their necessary distinctions. Complete logical paradigms and all 644 Cook assignments are preserved.

The 36 accepted PDFs total 1,223 pages, nine fewer than the initial complete course. Thirty-four documents were rebuilt; the Unit 17 and 18 keys retain their accepted bytes. Fresh independent inspection covered 738 initial changed page images and 14 replacement images after three heading repairs. Final acceptance comprises 739 directly inspected current pages, 407 pages byte-identical to previously inspected pages and 77 pages in the two unchanged keys.

- [Pre-implementation contract](contract.json) and [initial complete-course baseline](baseline.json).
- [Reversible table mapping](tables.json) and [independent table review](table-review.md).
- [Current export identities](exports.json), [compilation evidence](build-report.json), [complete text parity](export-text-review.md) and [every-page acceptance](page-review.json).
- [Retained source evidence](source-evidence.json) and [independent source/project review](cleanup-review.md).

Canonical contract arrays retain logical form coordinates. Current physical rows, panels and page counts are separate presentation data. Each chapter's `presentation_revision` object points to its current accepted PDFs. Earlier unit reviews continue to identify their original authoring checkpoints.

Run the shared checks from the repository root:

```powershell
python -X utf8 scripts/check_course_layout.py --report build/course-layout-check.json
python -X utf8 scripts/check_course_exports.py --report build/course-export-check.json
```

Rebuild complete documents with `python -X utf8 scripts/build_course_exports.py --stage all --include-unchanged --jobs 2 --render-suffix reproduction-01`. Build products remain separate until their actual output is reviewed. Retained TeX includes the accepted layout repairs; do not rerun historical assemblers or register mergers to reproduce the current edition.
