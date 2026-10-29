# Selective dictionary cross-references

The proposed print inventory is ready for integration: **300 selected spellings, 306 target routes, no unresolved exact-form targets**. Of these spellings, 289 need standalone pointers and 11 need an additional pointer beside an existing lexical entry. The full 5,580-surface lookup remains internal and unchanged.

The explicit inventory is in [cross-reference-policy.json](cross-reference-policy.json), under `cross_references`. Every record supplies `surface`, stable `entry_id`, target `entry_ids`, labelled `targets`, a corpus locator, and `disposition`. Each target retains its lemma ID, available exact register form IDs and evidence references. Some reviewed source variants have no separate register form ID; their accepted surface route and corpus locator supply the evidence. These are not newly generated forms.

The previous generator used a difference in the first two folded letters to select pointers. That rule missed changed present stems after prefixes, including **ācierfð → āceorfan**, and expanded ordinary ending families such as **hogast, hogdon, hogodest**. It also suppressed an additional route whenever a spelling already had a lexical head. The proposed inventory replaces that heuristic: 128 spellings are newly selected and 293 old spellings are intentionally omitted.

| Selection reason | Target routes |
| --- | ---: |
| Changed or contracted present | 89 |
| Evidenced alternative changed present | 14 |
| Opaque principal stem | 55 |
| Suppletion or negative contraction | 18 |
| Pronoun or demonstrative | 71 |
| Opaque nominal or numeral form | 23 |
| Degree form | 12 |
| Lexical spelling variant | 20 |
| Additional homograph retained | 4 |

The verb selection gives priority to vowel-changing third-person singulars, including prefixed verbs. A comparison with every current present-third-singular diagnostic found no missing vowel-changing form; its only unmatched candidate was transparent **wille**, whose final **-e** caused the crude vowel comparison. Exact alternatives such as **bierð, bīet, bȳhð, drīehð, brīt, flīegð, hǣt, līð** were checked against the actual course discussion. Their quantities and letters remain unchanged.

Ordinary strong preterites stay in the infinitive entry's principal parts. Extra pointers select representative suppletive, irregular weak, preterite-present or markedly contracted stems. They do not reproduce every plural, second-person, subjunctive or participial ending. Transparent weak forms such as **hīerde, hīerdon, hīered** and ordinary dental contractions such as **bint, rītt, wrītt** do not receive automatic standalone entries. A few frequent, independently opaque forms of **wesan** and negative contractions warrant their own labels. Source-bounded forms such as **nāt** retain the actual supplied analysis rather than gaining a new paradigm.

The nonverbal inventory replaces the useful part of the removed form lists. It covers opaque personal and demonstrative forms, selected noun stem changes, irregular numeral forms, useful degree forms and actual lexical variants. It does not expand routine noun or adjective endings. The checked course tables distinguish **mēder, dehter, brēðer** as dative singular; **byrig** and **bēc** as genitive/dative singular and nominative/accusative plural; and **fēt, tēð** as dative singular and nominative/accusative plural. Both **bā** and **twā** have feminine and neuter plural uses in the register.

Preserve these ambiguities in print:

- **bīett** points to both **bēatan** and **bēodan**; **flīehð** points to both **flēogan** and **flēon**.
- **bierst** is a present second-singular variant of **beran**, as well as a third-singular form of **berstan**.
- **fēt** points to the noun **fōt** and the third singular of **fēdan**.
- **sēo** points to the demonstrative and to forms of **sēon**; **sǣde** points to **sęcgan** and the dative of **sǣd**.
- Adverbial **bętst → wel** must appear beside the existing adjective entry. **ðā, ðæt, ðearf, hwȳ** and possessive-head homographs likewise retain their lexical meanings and additional pointers.

Existing comparative and superlative adjective headwords remain lexical entries; they should gain the positive-head links proposed by the design reviewer. Missing form-only degree routes are included here, including exact **gingstan, hēahstan, rihtlicor, sweotolost, andgietfullicost, swīðlicor**. No unattested comparative or normalized degree citation is supplied.

Validation checked every proposed surface/target against the accepted exact lookup, resolved every target head, read every proposed display label, and checked the important source alternatives and case labels against the actual course tables. All target labels are explicit; there are no generic unresolved “form” placeholders. Full morphology remains in the internal records, so a selected print label does not purport to list every possible analysis of that spelling.

The earlier 82-page PDF review is preserved as evidence for that superseded export. It cannot certify the forthcoming compact dictionary layout; newly rendered pages require visual inspection after integration.
