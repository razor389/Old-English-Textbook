# Pronunciation export page review

Visual review passes for the corrected actual exports: 12 learner pages and four key pages. Every page was viewed at native 150 dpi RGB resolution, including full text areas, headers and footers. No clipping, overflow, missing glyphs or detached headings remain. The exact master, TeX, PDF and page-image hashes are recorded in pronunciation-pages.json.

The first inspection covered all 19 pages of the earlier build and found three material premature breaks: learner pages 7 and 10 and key page 2 each contained only two or three lines before an avoidable near-empty remainder. Those original page records and findings remain in the JSON history.

The exporter reservation macro was restored to include the previously accepted \penalty-100 after \par. Scratch compilation and complete content checks passed. A fresh actual build then passed content checking, and all 16 corrected pages were inspected. Section 6 now follows the continuation on learner page 7; subsection C follows B8 on learner page 9; key section B follows the A4 comment on key page 2.

Accepted PDF identities:

- Learner: 9d7458c317ae720e3c90e9c2e7edc2ee4cfe2b3bac47f8ba4da2f9908022e7f4.
- Key: 4df9dc2c6362ed33ac5bcf0c6517241e4b1e4590349a182c94097274c5bbab42.

This receipt establishes visual export acceptance. Linguistic review and retained-PDF integration are separate coordinator responsibilities.
