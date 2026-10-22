# Typesetting

Markdown is the editorial master. `book-layout.tex` carries forward the previous course's LuaLaTeX/Cambria layout: 165 × 241 mm, 11-point body text, 14.3-point leading, restrained black headings, and separate learner/key documents. Its fonts and Old English characters were inspected in the earlier complete PDFs. The generic running-title macro is new; every new unit still needs a fresh rendered-page check.

The complete [Unit 1 exports](ch01/README.md) are reviewed: [learner PDF](ch01/chapter-01.pdf), 22 pages, and [key PDF](ch01/answer-key.pdf), 12 pages. Their source TeX, complete-content checks, page ledger and reproduction instructions are retained.

The complete [Unit 2 exports](ch02/README.md) are also reviewed: [learner PDF](ch02/chapter-02.pdf), 19 pages, and [key PDF](ch02/answer-key.pdf), 14 pages. Complete TeX, content parity and every-page inspection are recorded with the exports.

Use `chapter-template.tex` as a minimal document shell for later units. Create a unit directory, put complete learner and key TeX files there, and input `../book-layout.tex`. Set `\runningtitle` before the input. Build from that directory with LuaLaTeX, writing products to its ignored `build/` directory. Run sufficient passes for stable references.

Compare all content with Markdown: paradigms, vocabulary, source prompts, added tasks, reading support, keys, IDs, and notes. Inspect every page and check the logs for missing characters, font substitutions, and box warnings. Copy the final complete PDFs out of `build/` only after review. Preserve stable IDs in TeX comments.

The archived [Chapter 1](../reference/previous-course/typesetting/ch01/README.md) and [Chapter 2](../reference/previous-course/typesetting/ch02/README.md) contain full worked TeX documents and reviewed PDFs. They are typography and evidence references, not active chapter drafts. No automatic publishing pipeline is installed.

Cambria and the existing TeX Live installation are available on the seed machine. Another machine must have the chosen fonts and packages or make an explicit reviewed font substitution. Do not silently change the Old English spelling or vowel marks to suit a font.
