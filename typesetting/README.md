# Typesetting

Markdown is the editable master. [book-layout.tex](book-layout.tex) defines the shared LuaLaTeX/Cambria layout: 165 × 241 mm, 11-point body text and 14.3-point leading. Paradigms use 10.5-point type, horizontal rules and consistent labels; identical verbal plural cells share `1–3 pl.`.

The complete [Learner’s Book](full-book/book.pdf), **971 pages**, and [Answer Key](full-book/answer-key.pdf), **488 pages**, contain all accepted components. [Full-volume notes](full-book/README.md) give the assembly, navigation and every-page review evidence.

Separate references are the [12-page pronunciation guide](pronunciation/pronunciation.pdf), [4-page practice key](pronunciation/answer-key.pdf), [12-page sound-history appendix](sound-history/sound-history.pdf), and [Old English–English](glossaries/old-english.pdf) / [English–Old English](glossaries/english.pdf) glossaries of **58 / 100 pages**. Their directory READMEs give complete reproduction and acceptance instructions.

The eighteen units contain **1,227 pages** across 36 learner/key documents. The opening revision changes Unit 1 and three Unit 2 orientation paragraphs; the other unit sources and PDFs retain their accepted identities. Historical table-layout receipts describe their original checkpoint.

| Unit | Learner pages | Key pages | Export notes |
| --- | ---: | ---: | --- |
| 1 | [23](ch01/chapter-01.pdf) | [14](ch01/answer-key.pdf) | [Unit 1](ch01/README.md) |
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

## Current reproduction

For the pronunciation guide and Unit 1, use [the current opening builder/checker](../scripts/build_opening_exports.py), as documented in their [guide](pronunciation/README.md) and [Unit 1](ch01/README.md) notes. Unit 2 retains its complete existing TeX with three paragraph changes; [its notes](ch02/README.md) give compile/check commands. The [glossary checker](glossaries/README.md) requires the explicit current revision bridge.

Rebuild the complete volumes from the exact accepted component manifest:

```powershell
python -B -X utf8 scripts/build_full_book.py --stage all
python -B -X utf8 scripts/check_full_book.py
```

Full content/navigation checks and fresh raster/page review are required before promotion. Build outputs remain in ignored directories. The source manifest and exact preservation overlay distinguish the current revision from its original accepted components.

The older `check_course_layout.py` and table-layout baseline certify the historical presentation-only revision; they are not a current teaching-scope baseline after the opening revision. Do not recapture that baseline or replay historical assemblers/register mergers. Use current contracts, exact revised source identities and the versioned opening checks. Unchanged chapter TeX remains available for direct LuaLaTeX compilation and chapter-specific content verification.
