# Table inventory and compact-row audit

Read-only inventory of actual learner/key Markdown, all 18 active contracts and current cumulative registers. This is a presentation audit; it asserts equality of existing cells, not new source verification.

## Counts

| Unit | Tables (learner/key) | Merge identical plural rows | Paired-tense comparison blocks | Single-tense comparison blocks | Number/case pivots |
| --- | --- | --- | --- | --- | --- |
| 1 | 19 | 1 | 0 | 0 | 11 |
| 2 | 24 | 0 | 7 | 0 | 0 |
| 3 | 51 | 0 | 0 | 0 | 15 |
| 4 | 51 | 0 | 0 | 8 | 0 |
| 5 | 53 | 0 | 0 | 12 | 0 |
| 6 | 50 | 12 | 0 | 4 | 0 |
| 7 | 64 | 5 | 0 | 0 | 0 |
| 8 | 48 | 1 | 0 | 0 | 0 |
| 9 | 78 | 18 | 0 | 0 | 0 |
| 10 | 49 | 10 | 0 | 0 | 0 |
| 11 | 52 | 7 | 0 | 0 | 0 |
| 12 | 82 | 10 | 0 | 0 | 0 |
| 13 | 67 | 17 | 0 | 0 | 0 |
| 14 | 55 | 16 | 0 | 0 | 0 |
| 15 | 96 | 16 | 0 | 0 | 0 |
| 16 | 90 | 16 | 0 | 0 | 0 |
| 17 | 124 | 29 | 0 | 0 | 0 |
| 18 | 65 | 18 | 0 | 0 | 0 |

Exact identical plural groups: **176**, saving **352** repeated body rows before other layout changes. Nonidentical complete plural groups: **5**: two Unit 12 full-clause/translation tables and three Unit 15 numbered blank-response grids. None is a conflicting bare-verb plural paradigm. Of the 176 safe groups, 159 are learner tables and 17 are complete key paradigms.

## Recommended transformation

Use 1 sg., 2 sg., 3 sg., 1–3 pl. for personal finite systems. Preserve the exact literal contents of all columns when merging the three plural rows. Unit 1 must still explain we/you/they. Keep imperative 2 sg./2 pl. and impersonal 3 sg. systems bounded. Present-only and preterite-only systems remain single-tense tables.

Unit 2 already combines tenses: give each lemma a Person and number / Present / Preterite table, repeating the earlier shared preterite 1/3 singular form into its two logical slots. Units 4–6 separate present and preterite teaching sections: transpose within each existing comparison block so persons are rows and lemmas columns, splitting only for readable width. Never reorder prose or join sections. Unit 7’s already compact subjunctive blocks may similarly become per-lemma two-row tables (1–3 sg., 1–3 pl.) without expanding into six redundant rows.

Nouns use four full case labels and Singular/Plural columns; preserve side-by-side lemma comparisons with a pair of columns per lemma. Singular-only/plural-only systems remain so. Unit 3 Number/Case adjective tables pivot into four rows and six gender/number columns. Use the later Units 17–18 gender order Masculine, Neuter, Feminine, moving each exact form with its heading. Do not silently add absent instrumental cells or productive scope.

Unit 7–9 separate adjective number blocks require matched lemma, declension and scope before merging; adjacency alone is insufficient. The JSON inventory gives every table’s file, line, marker, heading, literal matrix and proposed actions. Task-specific partial key tables and numbered response grids retain their axes and all response slots; they receive shared typography only. Unit 16’s combined strong/weak adjective series retain all nine rows, including the explicitly bounded instrumental reference row.

## Contract and validation

- Keep canonical logical form/person cells and register milestones intact. A display cell may represent multiple canonical form IDs only when every literal value and scope is compatible.
- Prefer an explicit presentation mapping from prior matrix cells to new displayed cells. Validate every original logical cell has an exact unchanged image in the new display; its reverse expansion must equal the prior labelled matrix.
- Units 8–18 check_unit scripts compare literal headers/rows, with direct row/column coordinates in display references and derived-model relationships. Changing canonical matrices requires remapping all coordinates. A reversible presentation layer avoids rewriting those grammatical mappings.
- Unit 6/7 checker helpers synthesize expected matrices from display-plan tables. Unit 2 has stored surface-row ordering; Unit 3 has six gender-number vectors. Their checker paths must understand the presentation transform.
- Do not change canonical cell counts from 12 to 8 merely because identical plurals print once: twelve logical person/number/tense cells remain. Record physical display-cell counts separately.
- Earlier accepted review records and hashes certify the earlier edition. Add a revision record with new master/PDF identities and independent presentation verification; do not imply old page inspection covers new pagination.

## Important prose dependencies

Unit 7 explicitly says “one four-cell row below” and defines “a column headed all singular or all plural”; update this wording if its tables are transposed. Its statement that every person/number combination is provided remains true after compression. The JSON includes other row/column references for targeted inspection; do not rewrite learner exercise requests merely because answers may use compact tables.

## Coverage limits

This audit checked existing cell equality and presentation scope. No new Old English form, sense, spelling, source attribution or teaching milestone is proposed. The current 13,295 form records and all 644 Cook assignments should remain semantically unchanged.

## Proposed transform module

`scripts/course_tables.py` should expose pure table/document transforms, returning target blocks plus exact source-to-output cell mappings. Merged cells map all three old plural coordinates to one exact literal value; Unit 2 shared preterite 1/3 singular cells map to both logical target positions. Expansion of the mappings must reconstruct every old form cell exactly. The JSON records the proposed API and invariants. No module or master has been changed by this audit.
