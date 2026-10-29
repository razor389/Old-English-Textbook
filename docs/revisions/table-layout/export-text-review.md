# Independent export text review

Accepted for complete text coverage at the file hashes in [export-text-review.json](export-text-review.json). All 36 PDFs pass: 1,223 pages, 13,637 non-table prose/heading/task blocks, 22,324 physical table-cell instances and 18 generated captions. The audit found no missing source, vocabulary, task, answer, note or table content.

[The reusable checker](../../../scripts/check_course_exports.py) inventories every current Markdown block independently, decodes actual TeX paragraph bodies and physical tables, and extracts text directly from each actual PDF with Xpdf. The comparison checks document order, complete rows and their cells, captions, title text and all 11,124 non-table editorial comments in TeX. Physical table cells are matched back to the accepted Markdown matrices, including the two existing vocabulary/diagnostic reflows and repeated longtable headers. Unit1 uses an ordered whole-body comparison because its retained TeX has no paragraph markers.

Normalization is limited to Unicode NFC, whitespace introduced by line breaking or extraction, and Xpdf's soft-hyphen encoding of literal hyphens. A separately logged typography projection covers 31 blocks: 20 in Unit1 learner, 10 in Unit1 key, and one Unit10 learner heading. Straight apostrophes render as curly apostrophes; one Unit1 task also renders its straight double quotation marks as curly marks. These differences remain explicit in the machine report. Other punctuation, Old English letters, length marks and variants match.

No replacement, private-use, unassigned or unexpected control characters were found in extracted text. All corresponding build logs are free of missing-character messages. This text audit does not certify page spacing, collisions or clipping; those require the independent visual page review.

Run after any TeX or PDF change:

```powershell
python scripts/check_course_exports.py --report docs/revisions/table-layout/export-text-review.json
```

The checker uses no one-use assembler, temporary cleanup script or previously extracted text file. It reads all compiled PDFs under their unit build directories and binds the results to actual master, TeX and PDF hashes. A formatting repair requires a fresh successful run; any changed pagination also requires updated visual inspection.
