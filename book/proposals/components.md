# Accepted component inventory and assembly proposal

All **41 accepted components** are present. All **123 current master, TeX and PDF hashes match their primary acceptance records exactly**. Independent Xpdf extraction confirms every recorded page count: **930 learner pages** across 22 components and **475 key pages** across 19 components. No missing component, identity discrepancy or acceptance blocker was found. Exact paths, SHA-256 values, PDF counts and acceptance-record selectors are in `components.json`.

The learner volume should contain pronunciation, Units 1–18, sound history, Old English–English and English–Old English, in that order. The key volume should contain the pronunciation practice key followed by Units 1–18 keys. Use these positive allowlists; keep accepted worked examples and supplied support in the learner text.

| Component | Learner pages | Key pages |
| --- | ---: | ---: |
| Pronunciation | 9 | 3 |
| Unit 1 | 21 | 12 |
| Unit 2 | 20 | 14 |
| Unit 3 | 31 | 21 |
| Unit 4 | 21 | 18 |
| Unit 5 | 26 | 21 |
| Unit 6 | 26 | 27 |
| Unit 7 | 39 | 30 |
| Unit 8 | 29 | 24 |
| Unit 9 | 42 | 26 |
| Unit 10 | 40 | 29 |
| Unit 11 | 42 | 30 |
| Unit 12 | 46 | 30 |
| Unit 13 | 51 | 30 |
| Unit 14 | 34 | 21 |
| Unit 15 | 63 | 30 |
| Unit 16 | 64 | 32 |
| Unit 17 | 92 | 45 |
| Unit 18 | 64 | 32 |
| Sound-history appendix | 12 | — |
| Old English–English glossary | 58 | — |
| English–Old English glossary | 100 | — |
| **Standalone total** | **930** | **475** |

Current unit acceptance comes from `docs/revisions/table-layout/exports.json`, its complete-content review and its page ledger. Earlier per-unit records describe earlier checkpoints and must not replace that current binding. Pronunciation, glossaries and sound history have separate accepted export ledgers under their typesetting directories. Their retained visual-receipt hashes also match. This inventory identifies those acceptances; it does not claim fresh visual inspection of 1,405 standalone pages.

## Assembly constraints

The retained TeX bodies can be assembled reproducibly with the unchanged shared Cambria layout. Load `book-layout.tex` once and `multicol` once. Every component currently inputs `../book-layout.tex` in its preamble; none has external body inputs. Extract the body between its single document markers and retain its local setup. Six exact setup variants are recorded. In particular, Unit 1’s paragraph helpers and the early/later `reserve` implementations differ and should remain distinct.

Put each component in its own group, locally renew `runningtitle`, and clear its pending page **before ending the group**. Keep font features local: learners 1–4 and keys 1–3 do not use `Ligatures=TeXOff`, whereas the other 34 bodies do. The glossary size, ragged-column setting, 6 mm column separation and custom `needspace` definition also belong to their components. The accepted bodies contain 65 `clearpage`, 3 `newpage`, 2,355 `reserve` and 3,642 `needspace` calls; preserve them.

Recto component starts preserve the source’s odd/even margin geometry and running-header positions. With unchanged component pagination, the learner content needs 8 inserted blank versos, for 938 Arabic body pages before a new index; the key needs 7, for 482 body pages. These are forecasts excluding front matter and any final blank verso. Roman front matter and a single Arabic sequence per volume are compatible with the retained bodies: none resets page counters or uses `label`, `ref`, `pageref`, `hypertarget` or `hyperlink`. No existing body footnotes, running marks or macro definitions were found.

All 53 explicit `pdfbookmark` commands occur in the glossaries. Two destinations collide: `outline-B00001` names both opening titles; `outline-B01321` names Old English **T** and English **P**. Prefix every destination by component and set its hierarchy from the supplied bookmark ledger. Retain each glossary title as its component bookmark, with Entries/letters/quoted-error material beneath it; avoid adding a duplicate opening title. Shared layout already loads Unicode `hyperref`.

## Navigation and verification

Generate contents and grammar-index entries from external component/section metadata. Preserve the visible starred headings, embedded section numbers, task IDs and source references. Insert stable, uniquely named anchors and resolve page numbers after compilation. Do not reuse standalone page numbers as the new index’s page numbers.

The coordinator’s proposed verification is appropriate: compare complete component text, then render standalone and assembled pages identically and compare decoded header/body pixels. The comparison cutoff must include the lowest body/table content and exclude only the changed footer. Record the exact source-to-global page map; inspect every new footer, all new front matter/index pages, explicit blanks and every body page whose pixels differ. A clean compiler log alone cannot transfer the prior page acceptance.

No prior file or tracker state was changed. This proposal contains no new teaching or linguistic claim. Assembly, navigation design, final export checks, documentation and Git/Beads completion remain coordinator-owned.
