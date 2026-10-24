# Typesetting

Markdown is the editorial master. `book-layout.tex` carries forward the previous course's LuaLaTeX/Cambria layout: 165 × 241 mm, 11-point body text, 14.3-point leading, restrained black headings, and separate learner/key documents. Its fonts and Old English characters were inspected in the earlier complete PDFs. The generic running-title macro is new; every new unit still needs a fresh rendered-page check.

The complete [Unit 1 exports](ch01/README.md) are reviewed: [learner PDF](ch01/chapter-01.pdf), 22 pages, and [key PDF](ch01/answer-key.pdf), 12 pages. Their source TeX, complete-content checks, page ledger and reproduction instructions are retained.

The complete [Unit 2 exports](ch02/README.md) are also reviewed: [learner PDF](ch02/chapter-02.pdf), 19 pages, and [key PDF](ch02/answer-key.pdf), 14 pages. Complete TeX, content parity and every-page inspection are recorded with the exports.

The reviewed [Unit 3 exports](ch03/README.md) have 30 learner and 19 key pages; the reviewed [Unit 4 exports](ch04/README.md) have 20 learner and 19 key pages. Their complete content checks, independent page ledgers and final file identities are retained alongside the TeX and PDFs. The reviewed [Unit 5 exports](ch05/README.md) have 25 learner and 21 key pages, with all 46 final pages independently inspected and complete content parity recorded.

The reviewed [Unit 6 exports](ch06/README.md) have 25 learner and 28 key pages. The reviewed [Unit 7 exports](ch07/README.md) have 37 learner and 30 key pages. Both units retain complete content checks, independent every-page ledgers and final identities. Unit 7's learner example/translation reservation was rechecked on the two affected pages; the other 35 learner images remained identical to their inspected versions.

The reviewed [Unit 8 exports](ch08/README.md) have **30 learner and 24 key pages**. All 54 pages have independent visual records; complete text/table parity and final file identities accompany both full PDFs.

Use `chapter-template.tex` as a minimal document shell for later units. Create a unit directory, put complete learner and key TeX files there, and input `../book-layout.tex`. Set `\runningtitle` before the input. Build from that directory with LuaLaTeX, writing products to its ignored `build/` directory. Run sufficient passes for stable references.

Compare all content with Markdown: paradigms, vocabulary, source prompts, added tasks, reading support, keys, IDs, and notes. Inspect every page and check the logs for missing characters, font substitutions, and box warnings. Copy the final complete PDFs out of `build/` only after review. Preserve stable IDs in TeX comments.

The archived [Chapter 1](../reference/previous-course/typesetting/ch01/README.md) and [Chapter 2](../reference/previous-course/typesetting/ch02/README.md) contain full worked TeX documents and reviewed PDFs. They are typography and evidence references, not active chapter drafts. No automatic publishing pipeline is installed.

Cambria and the existing TeX Live installation are available on the seed machine. Another machine must have the chosen fonts and packages or make an explicit reviewed font substitution. Do not silently change the Old English spelling or vowel marks to suit a font.
