# Independent table review

Accepted for text, grammatical tables and retained TeX content. The acceptance identities are recorded in [table-review.json](table-review.json). PDF compilation and page inspection remain separate acceptance gates.

The review covers all 36 learner/key masters: 1,118 original table groups, 486 changed groups, 1,280 current matrices and 22,785 original header/body cells. There are 194 exact plural-row merges. Every complete logical paradigm remains represented.

The reviewer used an independent Markdown parser, grammatical-coordinate comparator and TeX decoder. Neither authoring implementation was imported or used as the evidence for acceptance. Replacing the actual revised blocks by their originals and reversing exactly 24 declared prose edits reproduced every baseline master hash. This proves that the intervening task text, source readings, notes and key explanations also survive, subject only to those declared edits.

Every original source coordinate has a destination. Literal forms, alternatives, vowel marks and reconstruction marks match exactly. A separate comparison expands shared person labels and checks case, number, gender, person, tense, mood, lemma, strong/weak series and reference scope. Actual retained TeX cells and captions match the current matrices, including physical panel splits. All 24 prose replacements are present in TeX. The existing Unit1 vocabulary and Unit13 diagnostic reflows were reconstructed independently.

The first pass identified remaining shared-person aliases, eighteen missed plural merges in keys with spelled-out person labels, and additional full subjunctive/command paradigms and nominal headers with inconsistent presentation. Both amendments are now present in actual files and pass the complete comparison. A fresh course-wide scan finds no unaddressed full-paradigm alias or repeated identical three-person plural group.

Four complete-clause tables retain their distinct persons: Unit12 learner T01/T02 and key T07/T08. Unit15 learner T71–T73 retain all numbered response cells. Pronoun duals remain separate, all imperative systems preserve second-person scope, and the Unit2 *habban* key retains its exact subject pronouns. Partial diagnostic tables keep their task-specific axes; the explicit exceptions are Unit2 key T02 and the six mixed command/infinitive reference tables in Unit6.

All 644 Cook assignments and their prompts and key identities remain unchanged. The reviewer checked 197 complete coverage fields and both cumulative register objects: 1,265 lemmas and 1,214 grammar features. Five source-span objects have bounded source-excerpt identifier and provenance-note changes, recorded by baseline and current hashes. Reversing only those transformations restored all five whole objects to their baseline hashes; the other 192 fields match directly. Reading text, original source notes, support and grammatical records are unchanged.

Nine negative controls confirm that the independent comparator rejects altered vowel length, swapped gender headings, a dual relabelled plural, deleted reference scope, an imperative broadened to all persons, a changed lemma association, an incorrect mood label, an omitted weak-preterite singular row and a broadened numbered response label.

Run the retained check with:

```powershell
python scripts/check_course_layout.py --report build/course-layout-check.json
```

The check passes for the accepted masters and current TeX. It has no dependency on temporary audit scripts or prose. Whole-master and logical-mapping hashes bind the text acceptance; TeX content is decoded afresh so formatting repairs can be checked without treating a new file hash as proof of changed language. Any such repair requires a fresh successful run, and the final PDFs require their own build and page-inspection records.
