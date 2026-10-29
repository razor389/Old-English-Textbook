# Sound-history appendix: course and glossary design audit

The course needs a connected historical account of breaking, umlaut and related changes. It already teaches selected results: syncope, æ/a noun alternation, eald/ieldra/ieldest, changed present singulars, strong principal parts and palatal pronunciation. The appendix should explain those patterns’ history without replacing the practical lexical rules.

This audit inspected all eighteen active contracts, the actual registers and the relevant student text. The register still has 1,265 lemmas, 13,295 forms, 1,687 senses and 1,214 grammar features. The machine-readable [analysis](analysis.json) records exact identities, teaching anchors, examples, form/sense IDs and dictionary routes. Historical causes and earlier stages remain subject to the independent Cook/Fulk image audits; this is a design proposal, not their source acceptance.

## Existing explanations

| Existing material | Location | Appendix’s additional work |
| --- | --- | --- |
| dæg/dagas and hwæl/hwalas | Unit 1, §§3–4 | Explain fronting/restoration, with historical conditions. |
| fugol/fugles and light/heavy neuter plurals | Unit 1, §§3–4 | Distinguish syncope, final vowel loss and syllable weight historically. |
| eald/ieldra/ieldest called an umlaut series | Unit 3, comparison section | Explain the former i/j trigger and its later disappearance. |
| drīfan/drāf/drifon/drifen; selected singular present changes | Unit 4, §§1–2 and Class II | Separate inherited ablaut from conditioned mutation. |
| giefan/geaf/gēafon/giefen and cweðan ð/d | Unit 5, Class V | Explain palatal effects and, briefly, inherited consonant alternation. |
| j-present bide/lige/site; seoh/sēoð | Unit 6, command forms | Explain gemination and contraction if source evidence permits. |
| Present subjunctive without indicative singular mutation | Unit 7, opening rules | Preserve the existing scope; history does not license changing every mood. |
| bæð/baðu and geat/gatu; later syncope refinements | Units 11–13 | Connect familiar lexical patterns with distinct historical mechanisms. |
| fōt/fēt, bōc/bēc, tōð/tēð | Units 12 and 15 | Use already covered nouns for the central umlaut explanation. |
| Hard cēlan despite ē; palatal and nonpalatal consonants | Pronunciation guide, §4 | Show why the order of changes can matter more than current spelling. |

No student-text search result supplies a general breaking explanation. Source apparatus contains historical questions, but the course repeatedly says those are not additional tasks. Do not silently assign them through the appendix.

## Proposed shape

1. Reading a historical explanation: optional scope, notation, sound versus spelling and a short front/back/rounding orientation.
2. Fronting and restoration, beginning with dæg/dagas.
3. Breaking, with one main example and a second consonant environment.
4. i-umlaut: its former trigger and its surviving results in nouns, derivation, comparison and selected present singulars. This deserves the largest section.
5. Other sources of diphthong spellings: back mutation, palatal diphthongization and a concise, dialect-qualified smoothing note.
6. Consonants and change order: palatalization and gemination.
7. Vowel loss, syllable weight and a short contraction note.
8. Ablaut, inherited consonant alternation and analogy, distinguishing conditioned change from inherited stem series.
9. A compact process/trigger/familiar-result/limitation table and source notes.

Aim for approximately 8–12 complete pages in the course layout, giving breaking and i-umlaut the fullest treatment and grouping the smaller related processes. The eighteen example groups are a selection pool, not a requirement to print them all. Use worked comparisons, not formal exercises; no separate key is needed. Gloss every example and keep all new historical material optional. A small number of source-audited earlier forms can make a vanished conditioning vowel visible; an entire reconstructed paradigm is unnecessary.

## Examples and dictionary access

The proposal supplies eighteen example groups with exact course anchors. The strongest reusable choices include fōt/fēt, mann/męnn, dōm/dēman, eald/ieldra/ieldest, būgan/bȳgð, drīfan/drāf/drifon/drifen, fugol/fugles and the giefan principal parts. bearn, heorte, heofon and seofon are existing headwords for source-audited breaking/back-mutation discussion. The course’s short **geaf** must remain distinct from long **gēafon**.

Several identical surfaces have other routes: fēt also belongs to fēdan; dēman can belong to noun dēma; bīett can belong to bēatan; cuman can belong to noun cuma; giefen is also a present subjunctive form. The appendix ledger must identify the selected lemma, sense and grammatical form, not merely show that the string occurs in a glossary.

Preserve the accepted glossary masters, PDFs and frozen 38-master audit. Add an appendix-specific access ledger, preferably `appendices/sound-history/glossary-access.json`. An additional attested inflection or dialect spelling can be sourced locally and routed to an existing dictionary headword; absence from the frozen 5,580-surface inventory is not a reason by itself to reject a good example. A genuinely new lemma needs an explicit bounded supplement. Reconstructed pre-OE stages, other languages, stem symbols and rule letters must be classified separately, not passed off as attested Old English. There are no new tasks requiring expansion of the exercise-only English glossary.

## Notation and scope cautions

An appendix asterisk must be defined as a reconstruction mark. Unit 3 explicitly uses asterisks for proposed errors, so the local distinction is necessary. Escape a literal star within Markdown emphasis; the exact earlier form must first be source-verified. Use a chronological arrow only for historical development; use “beside” or a colon for coexisting paradigm forms.

For the eventual learner master, bold every cited Old English word, reconstructed historical example and letter/ending used as an object; italicize explanatory English terminology. A complete inventory of those bold spans can distinguish attested forms, reconstructions, other-language comparisons and fragments.

No new IPA is needed for this outline. Plain words for fronting, rounding and consonant position can refer back to the pronunciation guide. Preserve Cook’s ę, quantity marks and source-specific exceptions; Fulk’s transcription is not permission for silent normalization. In particular, feoh/fēos cannot be simplified into a claim that an absent printed macron proves historical shortness.

Breaking, back mutation and palatal diphthongization must remain separate explanations even where their results share spellings. Current visible endings need not preserve old triggers. A strong past is not produced by applying umlaut to an infinitive; a changed weak past does not become a strong verb. Dialect, chronology and analogy belong in concise limitations, not an unrestricted form-generation chart.

Only the files in this proposal directory and ignored design scratch files were written. The coordinator should reconcile source claims, freeze the appendix contract, then commission prose and independent review.
