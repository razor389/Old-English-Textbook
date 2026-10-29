# Independent review of the dictionary verb policy

All **81 added reference forms pass the independent linguistic check**, and the revised verb entries are accepted. I found no incorrect spelling, vowel quantity, lexical prefix, class-based formation or principal-part selection. The actual revised master contains every added form in the correct entry. All reported corrections are resolved.

I did not author the policy or these additions. I personally opened and read all 22 cited Cook grammar images, printed pp.59–80, and additionally checked Cook dictionary pp.293 and 306 and Bosworth–Toller Supplement p.378. The JSON receipt records the hashes of all 25 images, one independent assessment for each added form, and the class/scope result for every policy entry. The policy's own review flag was not treated as evidence.

The check covered all **372 verb entries**: 97 strong, 107 weak, 11 preterite-present, 8 irregular and 3 impersonal cores, plus 146 explicitly bounded citations. I read all 372 actual Markdown verb paragraphs in three batches, including the complete paragraphs for all 81 additions. The exact master and data hashes, paragraph hashes and integration results are in [dictionary-verb-independent.json](dictionary-verb-independent.json).

The source checks substantiate the difficult choices:

- Strong participles use the correct class vowel and consonant series: for example **āloten**, **āworpen**, **forstolen**, **gecweden**, **flogen** and **wiðstanden**. Present or singular-preterite vowels were not copied into the wrong principal part.
- Cook §§113–117 permit the selected full **-ed** forms and dental contractions. Thus **āfēded**, **scrȳded**, **tōgelǣded**, **gestilled**, **grētt** and **spǣtt** have specific source-pattern support.
- Cook's dictionary explicitly assigns **genēalǣcan** and **nēalǣcan** to §113 on pp.293 and 306. Their **-ced** reference formations follow that class and the course's selected **-cte** series. Bosworth–Toller confirms that the alternative **-hte** past also exists; the reference does not silently substitute it.
- Weak-I **hęrian → hęred** and **scęððan → scęðed** remain distinct from the weak-II **-od** formations. **Gearcod** preserves the actual gearcian lexeme without inventing another ge- prefix.
- Cook explicitly labels **āgen** adjectival. The individual preterite-present paradigms supply **(ge)cunnen**, **(ge)unnen** and **(ge)witen**. Missing modal participles are described as absent from the checked paradigm, not universally unattested.
- The diagnostic label **pret. 1 sg.** is justified: Cook p.62 expressly gives **funde** for findan's third-singular preterite. Impersonal entries retain third-singular labels.
- All six identified inflected-participle records remain excluded from base principal parts. Their internal surface routes are preserved. The complete 5,580-surface lookup hash is unchanged.

Two provenance refinements were requested and are now resolved in the coordinator snapshot. **GLOSS-DICT-PP-lecgean**, **(ge)lęgd**, is directly printed in Cook's p.71 note and is therefore exact source. **GLOSS-DICT-PP-thencan**, **(ge)ðōht**, records a declared thorn-to-eth normalization of the p.70 citation. Neither correction changes the learner form. The refined origin counts are **13 exact source, 1 declared normalization and 67 rule formations**, totaling 81.

**DVI-03 is resolved:** **OE-durran, OE-motan, OE-magan and OE-sculan** now print the conventional-citation/Unit-6 caveat once while retaining the separate statement about the absence of a past-participle citation. I reread all four corrected paragraphs; their grammatical forms are unchanged.

The coordinator also resolved the two inherited gloss-style observations through explicit Old-English-side print overrides: **gesęndan** now says “send back”, and **ðrēan** says “chastise; strike”. I reread both. Their canonical source meanings and English exercise routes remain unchanged. Together with the four modal corrections, these are the only six changed verb paragraphs; the remaining 366 paragraph hashes are identical to the first master receipt.

Accepted final master SHA256: `db8eb1253d5729998e3e115668b663fe0f9b0fe71cfee9ab3e148cd39f1aedee`. The final nonverbal batch was rebound by exact comparison of all 372 previously read verb paragraphs: every paragraph is byte-for-byte unchanged.

This receipt does not accept PDF pagination. The compact export still requires its own visual inspection.
