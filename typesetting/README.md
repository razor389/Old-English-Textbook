# Typesetting

Markdown is the editable master. [book-layout.tex](book-layout.tex) defines the shared LuaLaTeX/Cambria layout: 165 × 241 mm, 11-point body text and 14.3-point leading. Paradigm tables use 10.5-point type with 13.2-point leading, bold headings, horizontal rules and consistent labels. Identical verbal plural forms share `1–3 pl.`; all distinct forms and complete logical paradigms remain.

The separate introductory [pronunciation guide](pronunciation/pronunciation.pdf), 9 pages, and [practice key](pronunciation/answer-key.pdf), 3 pages, use this layout. Their [export notes and reproduction commands](pronunciation/README.md) cover both complete documents. They are additional front matter; the build and page totals for the 36 unit documents below remain unchanged.

The accepted [course presentation revision](../docs/revisions/table-layout/) rebuilt 34 complete documents, comprising 1,146 pages, with clean compilation and table-parity checks. Unit 17's 45-page key and Unit 18's 32-page key are byte-unchanged. The eighteen units total **1,223 pages**, down from 1,232. Independent reviewers accepted the changed pages and subsequent heading repairs; the links below identify the retained PDFs.

The [export manifest](../docs/revisions/table-layout/exports.json) records current page counts and PDF identities. [Page acceptance](../docs/revisions/table-layout/page-review.json) binds the reviewed pages to those exports; the [validated build report](../docs/revisions/table-layout/build-report.json), [complete-content checks](../docs/revisions/table-layout/export-text-review.json), and [logical-table review](../docs/revisions/table-layout/table-review.json) retain the verification evidence.

| Unit | Learner pages | Key pages | Export notes |
| --- | ---: | ---: | --- |
| 1 | [21](ch01/chapter-01.pdf) | [12](ch01/answer-key.pdf) | [Unit 1](ch01/README.md) |
| 2 | [20](ch02/chapter-02.pdf) | [14](ch02/answer-key.pdf) | [Unit 2](ch02/README.md) |
| 3 | [31](ch03/chapter-03.pdf) | [21](ch03/answer-key.pdf) | [Unit 3](ch03/README.md) |
| 4 | [21](ch04/chapter-04.pdf) | [18](ch04/answer-key.pdf) | [Unit 4](ch04/README.md) |
| 5 | [26](ch05/chapter-05.pdf) | [21](ch05/answer-key.pdf) | [Unit 5](ch05/README.md) |
| 6 | [26](ch06/chapter-06.pdf) | [27](ch06/answer-key.pdf) | [Unit 6](ch06/README.md) |
| 7 | [39](ch07/chapter-07.pdf) | [30](ch07/answer-key.pdf) | [Unit 7](ch07/README.md) |
| 8 | [29](ch08/chapter-08.pdf) | [24](ch08/answer-key.pdf) | [Unit 8](ch08/README.md) |
| 9 | [42](ch09/chapter-09.pdf) | [26](ch09/answer-key.pdf) | [Unit 9](ch09/README.md) |
| 10 | [40](ch10/chapter-10.pdf) | [29](ch10/answer-key.pdf) | [Unit 10](ch10/README.md) |
| 11 | [42](ch11/chapter-11.pdf) | [30](ch11/answer-key.pdf) | [Unit 11](ch11/README.md) |
| 12 | [46](ch12/chapter-12.pdf) | [30](ch12/answer-key.pdf) | [Unit 12](ch12/README.md) |
| 13 | [51](ch13/chapter-13.pdf) | [30](ch13/answer-key.pdf) | [Unit 13](ch13/README.md) |
| 14 | [34](ch14/chapter-14.pdf) | [21](ch14/answer-key.pdf) | [Unit 14](ch14/README.md) |
| 15 | [63](ch15/chapter-15.pdf) | [30](ch15/answer-key.pdf) | [Unit 15](ch15/README.md) |
| 16 | [64](ch16/chapter-16.pdf) | [32](ch16/answer-key.pdf) | [Unit 16](ch16/README.md) |
| 17 | [92](ch17/chapter-17.pdf) | [45](ch17/answer-key.pdf) | [Unit 17](ch17/README.md) |
| 18 | [64](ch18/chapter-18.pdf) | [32](ch18/answer-key.pdf) | [Unit 18](ch18/README.md) |

The unit export notes preserve original linguistic acceptance, complete-content evidence and earlier checkpoint identities separately from this presentation revision. Original review ledgers certify their identified files; they do not certify a new render automatically. Logical-cell totals and teaching milestones are unchanged even where a compact row represents three persons.

## Reproduction

Run from the repository root with the configured TeX Live, Cambria, Xpdf and Ghostscript installation:

```powershell
python -X utf8 scripts/check_course_layout.py --report build/course-layout-check.json
python -X utf8 scripts/build_course_exports.py --stage all --include-unchanged --jobs 2 --render-suffix reproduction-01
python -X utf8 scripts/check_course_exports.py --report build/course-export-check.json
```

The shared build command compiles each complete document twice, checks table parity and build diagnostics, extracts its text and renders all pages. Choose a fresh `--render-suffix` for a later changed build. Use `--stage inspect` to inspect existing build products without compiling, or `--stage render` to regenerate page images from them. `--select` accepts comma-separated document IDs such as `ch01/learner,ch03/key`.

The layout check compares expanded logical cells, actual Markdown/TeX tables, protected distinctions and frozen teaching content. The export check independently compares complete master prose, actual TeX cells and captions, and the built PDF text. The unrestricted export command checks all 36 documents; `--chapter N` is available only for a limited unit diagnostic. A later changed build needs fresh visual review bound to its PDF and page-image identities before it replaces an accepted PDF. Do not rerun historical assemblers, register mergers or baseline captures to rebuild exports.

The build helper records compilation, diagnostics, extracted text, PDF identities and raster identities in `build/style-audit/build-report.json`; reproduction reports and page images remain under `build/`. The accepted build report is retained separately at [docs/revisions/table-layout/build-report.json](../docs/revisions/table-layout/build-report.json). Rebuilding does not promote PDFs or rewrite the durable acceptance records. The existing selected fonts and packages must be available; any font substitution requires explicit review. Never alter Old English letters or quantity marks to accommodate a font.

The retained TeX includes complete learner/key content and deliberate pagination adjustments. The common renderer and mapping maintain table presentation; historical one-use authoring helpers are not the current export workflow. Preserve stable task, key and teaching IDs throughout rebuilds.
