# Glossary data and display design

Preliminary independent audit, 29 October 2026, for `oec-gloss-design`. This is a design and metadata-resolution handoff, not acceptance certification. No shared register, contract, lesson, Beads or Git record was changed. The coordinator supplied baseline `0c4d27031697abd8ed74ae70e5e72bdd9573e2b4`.

## Recommended result

Produce an alphabetical Old English–English glossary with conventional citation headwords, concise meanings, evidenced gender/class and diagnostic forms. Under each entry add a compact **Forms in this book** list containing the distinct actual printed forms. Add selective **see** entries for difficult forms such as męnn, eom, is and suppletive or markedly changed verb forms. This makes every covered surface searchable in the PDF without repeating its destination headword in a separate long index. Keep a complete occurrence-to-entry/form/sense map in the data.

Produce a separately edited English–Old English index for exercise meanings and expressions. Index **give** and **sell** separately even though sęllan can answer both; distinguish **need a thing** (beðurfan + genitive) from **need to** (ðurfan + infinitive). Include complete supplied idioms where the exercise requires them. English task instructions and grammatical terminology are not words to translate. Reversing whole gloss strings or splitting them mechanically at semicolons will not produce a usable index.

## Actual scale

The eighteen active contracts and actual cumulative registers were loaded in full. Their lexical inventories contain all 1,265 register lemma IDs. This says nothing by itself about unregistered wording in the actual book.

| Measure | Count |
| --- | ---: |
| Lemma records | 1,265 |
| Distinct current headword strings, casefold/NFC | 1,247 |
| Sense records | 1,687 |
| Logical/contextual form records | 13,295 |
| Distinct registered form strings, casefold/NFC | 5,625 |
| Single-word form strings | 5,585 |
| Distinct form–lemma routes | 5,724 |
| Surfaces associated with multiple lemmas | 94 |
| Supplied-only senses / forms | 703 / 974 |
| Grammar features / evidence records | 1,214 / 2,184 |

These are the narrow register headword/form baseline, not the separate corpus agent's expanded alias counts. There are 16 duplicate-headword groups, including ǣr, hund, rīce, būtan and gōd. Use separate POS/sense subentries under a shared printed heading; do not conflate their data.

Bare headwords plus all existing sense-gloss strings total 44,483 characters. Separate form→headword strings total 96,335 before analysis or layout. Grouped surfaces plus two-character separators require **49,596** characters, before labels and exceptional notes. At an illustrative 70–85 two-column entry-lines per page, even a one-line-per-surface index needs roughly 67–81 pages before wrapping. Grouped lists use substantially less space. Actual typesetting, especially long verb lists, must settle page counts.

A crude candidate rule, selecting single-word forms whose first two diacritic-folded letters differ from the headword, produces 393 surfaces / 395 routes. This is a review queue for selective cross-references, not a linguistic parser: remove obvious rows, add difficult variants missed by the rule, and retain a complete machine map regardless. The queue is in `analysis.json`.

## Diagnostics and grammar

Reuse actual course practice: Unit1's noun table gives gender, genitive singular and nominative plural; Unit3 distinguishes vowel/consonant adjective stems and exceptional direct forms; Units4–5 print four principal parts; Unit6 distinguishes usable infinitives from conventional/defective verb labels; later units often put the information in prose and literal paradigms rather than a vocabulary table.

For nouns give genitive singular and nominative plural where evidenced, adding an exceptional dative such as męnn. For strong verbs give preterite singular, preterite plural and participle, plus changed third-singular present when useful. For weak verbs give the preterite and participle. For irregular/defective systems give the actual useful forms and the unit reference. Do not synthesize unsupported diagnostics to fill a template. Singular-only senses, plural-only nouns, names, starred reconstructions and supplied citations retain their stated limits.

Only 59 lemma records have a top-level principal-parts list. Only 186 have nonempty top-level diagnostic fields. Structured form analyses yield diagnostic candidates for 738 lemmas. Noun gender is absent or null in 186 current noun-POS records. Thus top-level extraction would produce an incomplete glossary despite apparently complete register counts.

The audit resolves gender for 108 of those 186 from explicit structured form analyses, 59 from explicit unstructured source analyses, and six more from actual learner explanations: næddre f., gesihð f., storm m., gewinn n., rēðnes f., fierst m. Each resolution retains form IDs/evidence or an exact learner location. No noun in the 78-member second group has a productive sense milestone. The **13 remaining** questions are węcg, ōra, gagates, fæc, dīegelnes, gebrec, ōrmōdnes, ȳð, intinga, lēo, hord, clif and Englisc (language). Source-metadata rows were checked; they repeat source-local scope without a gender. Secure supplied forms and meanings can appear while a gender field remains unset. No full productive paradigm is being inferred.

Use grammar records for complements and government, not just the forms. For example, the sęllan drink-infinitive expression is explicitly supplied, whereas ordinary giving has an accusative thing and dative recipient. The beðurfan genitive frame has its own bounded evidence; do not write an unrestricted universal government rule.

## Cumulative metadata that needs display curation

`analysis.json` contains 42 headword/POS variation records and a proposed display resolution for each, with original sense IDs, evidence refs and historical metadata keys. Most changes are harmless terminology or promotions; a few would materially mislead if the latest label were printed unchanged.

- **mann** currently displays **man**, POS **impersonal subject**, with an impersonal-only scope note. The productive noun mann, mannes, męnn and human-being sense remain. Print the noun and distinguish impersonal man.
- **se** requires article, demonstrative and relative senses, with sēo/ðæt lookup. **ðonne** includes conjunction “than” and adverb “then”; **ðēah** includes conjunction “although” and adverb “nevertheless”.
- **for-ðon** can be causal in Unit11 and consequential in Unit16. A short spelling alone does not select “therefore”. Preserve the context-specific sense routes.
- **Apollonius** has an early gloss “to Apollonius” because the form is Apollonie; the dative translation belongs to that form, not to the name's headword definition.
- **wesan** now has a top-level supplied-only scope note despite its accumulated productive paradigms. No latest lemma-level scope note can summarize the complete teaching history safely.
- **eft/ęft** are real course spellings; the unmarked historical **geseon** metadata is not evidence for a new spelling variant beside gesēon.

Thirteen source-only/local/expression POS labels have separate meaningful learner-label proposals. For example, ðǣr becomes “adverb”; Pentapolis “proper place name”; ðēowa manna “noun phrase”. Tōdǣlen/tōdǣlden remain explicitly inflected verb forms unless a citation-evidence route is added. This avoids pretending that “source-only” is a part of speech or that every local form already establishes a dictionary paradigm.

## Alphabetization and lookup

Use **a, æ, b … t, þ/ð, u … z**. Ignore length marks and hooks in the primary sort key only; keep æ separate after a and give thorn/eth one rank after t. Case does not affect position. Preserve all marks and letters in display and exact surface lookup. Word-divider hyphens/spaces may be ignored in the primary word key, with the exact spelling and stable ID breaking ties. Sort ge- literally under g: there are 127 current ge-initial headings, including lexical compounds. Do not automatically strip ge- or treat a prefixed verb as its base. Add a participial or unprefixed pointer only from an evidenced relation.

## Pronunciation and source evidence

The guide has 57 example records. Twelve actual printed surfaces are absent from the narrow register headword/form lookup: āc, eorl, cyrice, cēlan, frosc, ecg, docga, sengan, cnīf, cnīfas, hǣlðu and forðām. The OE inventory agent independently reconciled and confirmed this list; an earlier all-covered summary was corrected. These do not necessarily require eleven new lemma records: cnīf/cnīfas belong together, cyrice can route to cirice with guide spelling evidence, and hǣlðu may route to hǣlu after exact confirmation. Retain the individual evidence in `guides/pronunciation/examples.json`. Hliehhan is an unused candidate and does not enter merely because it is in the planning pool.

I personally inspected Cook First Book p13/PDF29 (§17), confirming mann/męnn and hook/quantity typography, and p59/PDF75 (§102), confirming the class-I stem model, rīdan membership and present dental examples. Other source claims reuse the named accepted audit/catalog records and actual lesson wording; this audit does not claim a fresh image check of every glossary word. Input hashes and inspected-image hashes are recorded.

## Handoff and checks

`analysis.json` supplies input identities, exact counts, proposed schema, 42 metadata resolutions, 173 supported missing-gender resolutions, 13 remaining gender questions, 13 source-label resolutions, gloss overrides, entry exemplars, all diagnostic candidates, the opaque-form review queue and 14 coverage checks. The coordinator should reconcile these with the independent actual-text and exercise inventories before writing the glossary contract.

The necessary acceptance checks are occurrence completeness; sense-specific exercise coverage; supported diagnostics and government; exact spellings/normalization notes; non-dangling cross-references; explicit handling of wrong forms, stems/endings, non-OE quotations and source errors; and data/Markdown/TeX/PDF parity with every page inspected. Printing a word for reference does not change its teaching milestone. Machine coverage and a closed task are not linguistic acceptance.
