# Table style and build audit

This is an inspection report for `oec-style.1`. No active learner, key, contract, register, TeX or PDF was edited. `styling.json` records the inventory, individual images actually inspected and their identities.

## Recommended common style

Use the current later-unit design: Cambria, table type 10.5 pt with 13.2 pt leading, 4 pt column separation and array stretch 1.10. Keep ragged-right text, bold column headings, ordinary upright forms, and booktabs top/header/bottom rules without vertical rules. The shared document is 165 × 241 mm with 11/14.3 pt body text. Consistency means the same hierarchy, axes and rules; narrow and wide paradigms still need appropriate column widths.

Use full case names in Nominative, Genitive, Dative, Accusative order, with singular/plural as columns. Singular-only senses remain explicitly singular-only. Do not hide scope dashes or starred reconstructions. For adjective matrices, the late-unit solution is two stacked panels, one singular and one plural, with case rows and three gender columns. This keeps 10.5 pt type instead of shrinking seven columns. Later matrices generally use Masculine, Neuter, Feminine; preserve each labelled form correspondence when standardizing earlier order.

Verbs should have person/number rows and tense columns where the two tenses are taught together. Earlier comparisons can use lemma columns in separate already-established tense sections; large comparisons should be divided into readable panels. The requested `1–3 pl.` label is appropriate only where all three source cells and their scope agree. A common form must still map to all three logical person slots. Separate pronoun persons, imperative 2 plural, and nonfinite rows are not candidates for this merge. The row audit establishes actual linguistic candidates and exceptions.

## Observed differences

Unit 1 ordinary paradigms are set at body size, 11 pt, while its vocabulary/support tables and later tables use 10.5 pt. Its noun tables put case-plus-number down the first column, sometimes comparing several nouns. Unit 2 compares verbs as rows with person/number columns, already grouping `All pl.` and some preterite `1/3 sg.` cells. Units 17–18 typically give one named system at a time, case or person rows, ordinary black booktabs rules, and accompanying descriptions kept with the first table. Unit 18 repeats the same finite plural form on three rows; merging those rows gives a straightforward space saving.

Personally inspected retained learner images: Unit 1 p.2; Unit 2 p.4; Unit 18 pp.3, 9, 18. All visible letters, macrons and rules are clear. Unit 1's fisc/męte table is complete in both current TeX and the actual p.2 image; an initially reported missing body was a truncated tool excerpt, not a file defect. No visual acceptance of new exports is implied by these old-page samples.

## Existing conversion and parity architecture

Every unit has its own one-use `_assemble_unitNN.py` under `typesetting/chNN/build/`. These scripts are not a stable full-course pipeline. Unit 1 and Unit 2 execute assembly at module import; do not import them merely to reuse their functions. Later assemblers have guards, but reassembly still discards post-assembly manual layout repairs. Separate repair helpers survive for Units 9, 10, 15, 17 and 18. The complete inventory is in the companion JSON.

Unit 1 has 17 learner and two key table environments and no `mdtable` or `mdparagraph` markers. It needs one-time ordinal matching of complete table groups to master tables and explicit handling of its six-field vocabulary reflow into four printed columns. Do not rebuild its surrounding prose or source-note formatting simply to update paradigms.

Units 2–18 have stable `% mdtable:TNN:begin/end` blocks. Their table count differs from the number of actual TeX environments when one Markdown table becomes multiple panels. Unit 2 has 10 learner Markdown blocks but 17 environments because seven wide finite tables split into present/preterite panels. Later seven-column adjectives likewise split into two environments. Prose, heading, list and reading blocks have separate `% mdparagraph:Pnnn:begin/end` markers, allowing byte-preservation and independent content comparisons outside changed tables.

Some later table blocks also close an outer introductory minipage. Their net minipage balance is minus one: ch16 T22–T25; ch17 T55, T57, T59, T61, T63, T65, T67, T69, T111 and T113; ch18 T20, T22, T24, T26, T28, T30 and T32. All other inspected table blocks balance minipages. Preserve or deliberately relocate this closing command while replacing the block. Otherwise the new document will contain an unclosed minipage or an unmatched end. Later generators close the intro after the first adjective panel so the second may paginate naturally.

`_check_content_parity.py` independently parses the Markdown, decodes actual TeX paragraph/table text and compares complete content; it does not trust generated `*-content-map.json`. Existing panel reconstructions are hardcoded per unit. New transformations need explicit reflow maps or updated independent reconstruction, especially when a single old Markdown table becomes several new tables. These scripts also compare prose Unicode sequences with pdftotext extraction, preserve all editorial comments and check titles. Keep these checks, adapted to the compact table shape.

The chapter-level `scripts/check_unit*.py` also enforce literal table shapes. For example Unit 2 requires the old horizontal `surface_row`; Unit 18 compares every marked actual Markdown matrix exactly against the contract's stored headers and rows. Later checks enforce prior artifact identities. A presentation revision must reconcile these checks through a declared current presentation representation or reversible expansion. Do not change grammatical register entries merely to make the new display pass, or recapture an old immutable baseline as if this revision never happened.

## Safe implementation route

1. Freeze the present revision and inventory all original logical table coordinates, table markers, teaching IDs, prose, tasks and keys. The new course revision should explicitly record presentation changes.
2. Apply deterministic Markdown transforms with an old-coordinate-to-new-coordinate map. Verify expansion reproduces every form, variant, dash, reconstruction mark and labelled scope. Normalize headings only through explicit aliases.
3. Introduce one shared table emitter for the agreed style. Replace only corresponding blocks in the retained TeX. Preserve all non-table text and existing page/heading repairs. Insert stable table markers into Unit 1 through verified ordinal matching. Preserve extra outer-minipage closes and labels.
4. Compare decoded TeX cells to current Markdown, and independently expand compact forms against the frozen logical forms. Check all paragraph/comment/task identities. Do not count repeated headers as teaching cells, and do not claim that fewer printed cells remove logical coverage.
5. Compile affected complete documents twice, verify clean glyph/font/box diagnostics and full extraction parity, inspect every newly rendered page and update acceptance identities/page counts. Existing old-page reviews remain historical witnesses; they cannot certify the new pagination.

No font replacement, spelling change or contraction of a teaching scope is required for the requested layout revision.
