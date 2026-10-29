# Compact dictionary design

**Ready for integration.** Remove all printed “Forms in this book” lists. Preserve all exact surface routes internally. The current 1,020 form-list paragraphs occupy 60,270 characters, about 24.6% of the OE master; deleting them does not delete a lexical entry or meaning.

Nouns retain gender and evidenced genitive singular/nominative plural. Of 499 noun entries, 312 have both diagnostics, 33 only a genitive, 6 only a plural, and 148 neither. All 663 existing diagnostic groups (664 displayed surfaces) match their recorded form provenance and case/number analysis. None of the 148 without diagnostics has a form marked as taught for production. Sixteen supplied/reference noun genders remain unset; do not fill them by guessing.

Two exact display repairs matter: masculine **sǣ** has genitive **sǣs**; its additional **sǣ** genitive belongs to an explicitly feminine source use and must be labelled that way. **Ðīestru** is plural only and belongs with the source’s strong neuters; separate that number restriction from the gender field and infer no singular.

Keep selected variant/opaque-form help when lists disappear: **bōce → bōc**, **burge/byrig → burg**, and the kinship datives **mēder, dehter, brēðer**. Mēder/dehter have separately qualified late genitive alternatives; they are not plural diagnostics. The cross-reference reviewer owns the complete selective allowlist.

| Positive | Comparative | Superlative or bounded source form |
|---|---|---|
| lēof | lēofra | lēofost |
| eald | ieldra | ieldest |
| gōd | bętera | bętst |
| yfel | wiersa | wierrest |
| micel | māra | mǣst |
| lȳtel | lǣssa | lǣst |
| swēte | swētra | swētest |
| wīs | wīsra | — |
| dēorwierðe | dēorwierðra | — |
| fæger | fægerra | fægerestan (supplied superl. acc. f. sg.) |
| smylte | — | smyltestan (supplied superl. acc. m. sg.) |
| swīð | swīðra | — |
| hēah | — | Hēahstan (supplied superl. gen. m. sg.) |
| geong | — | gingstan (supplied superl. acc./gen. m. sg.) |
| wel | bęt | bętst |
| wīde | wīdor | wīdost |
| swīðe | swīðor | swīðost |
| rihtlīce | rihtlicor | — |
| sweotole | — | sweotolost |
| andgietfullice | — | andgietfullicost |
| swīðlice | swīðlicor | — |

The JSON gives exact source lemma, entry, form and evidence IDs for all additions. Seven complete adjective series come directly from Unit 3’s comparison table and Unit 13’s swēte discussion; partial later series retain only their checked cells. **Swīðra** links to swīð only in “stronger/fiercer”; its right-hand/side sense stays separate. Adjective and adverb **bętst** retain distinct routes.

Editorial notes and integration instructions in the JSON are not learner prose. Print only the grammatical labels, selected forms and concise usage/stem notes.

A comparison form may belong to a separate existing lemma: for example, gōd’s comparative is recorded under god-adjective-comp. The renderer/checker must follow the explicit source_entry_id/source_lemma_id rather than pretending the form belongs to the positive lemma’s register record.

Use short stem notes for micel/micl-, lȳtel/lȳtl-, hālig/hālg-, mihtig/mihtg- and contracted hēah. These are lookup aids, not replacement declension tables. Preserve the separate noun hālga and its hālgena plural-genitive distinction.

Pronouns, determiners and numerals retain concise grammatical guidance and selected irregular-form pointers. Function words retain their case and construction notes. Proper names, loans and exact supplied forms keep their honest source labels; no new paradigm is inferred. Verb principal parts follow the separately reviewed verb policy.

The coverage contract must distinguish exhaustive internal resolution from selective printed access. Keep all internal entry/sense/form identities, ambiguous routes and correction dispositions. Check every selected printed diagnostic and cross-reference, then verify full Markdown/TeX/PDF parity. No chapter, cumulative register, assignment or English entry changes.

This is a design and evidence handoff. It does not accept an export that has not yet been generated or visually reviewed.
