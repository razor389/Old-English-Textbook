# Independent review of the late-half grammatical index

Reviewed **170 entries, 174 target occurrences and 41 cross-reference records** from `book/proposals/index-late.json` as represented in the merged index. **No material linguistic, teaching-scope or cross-reference errors found.** All four optional complementary locators have been added and verified. No semantic or locator finding remains open.

Review date: 2026-11-02. Reviewer: `/root/sound_design`. Beads issue: `oec-book-index-audit` (coordinator-owned).

## Input identity

| Input | SHA-256 |
| --- | --- |
| `book/proposals/index-late.json` | `0253de2357bf904bea70f5dcc479dd25356078bfd41d23f68e5cad6e1298d53b` |
| `book/grammar-index.json` | `1e586faae494115a658098dafa658f30d9a54e61924cf828f7227943d2556062` |
| `book/coverage.json` | `6e51c7c2c47b2c2bbdf77c5b784a89d291e499e9ab45c20c9cc134d9a36f2195` |

All 30 component master/TeX/contract identities and the cumulative grammar register match the proposal inputs. This identity check supports reproducibility; semantic review used actual learner paragraphs and table cells.

## Final semantic receipt

Accepted for index SHA-256 `1e586faae494115a658098dafa658f30d9a54e61924cf828f7227943d2556062` (447 entries, 360 unique anchors). The full initial semantic review used `2ad8c18c41cd7fae1bf26aecc45ffc93324237736279f14117e33cf9080060d8`; that identity is preserved in the JSON review history. The bounded follow-up rechecked all 174 original late target occurrences, verified all four complementary paragraphs, rebound all 170 late entries by `proposal_records` after sorting, and resolved all 68 alias destinations again. All 31 source input identities remain unchanged.

A final metadata-only amendment changes the early consonant-cluster evidence line from 122 to 120. All 170 late entry labels/routes, 174 original target occurrences, four additions, 41 alias records and 31 source identities were rechecked as unchanged; the prior semantic receipt is preserved in JSON history.

The four late amendments match `book/amendments.json` exactly. Earlier-half amendments remain under the independent early reviewer’s remit. Final PDF navigation is still a separate pending review.

## Findings — implemented and verified

### IL-01 — Add a direct target for shared dative-shaped instrumental forms.

Implemented and verified optional refinement. Affected proposal: `book/proposals/index-late.json#/entries/63`; merged entry: `book/grammar-index.json#/entries/176`. Added anchor: `bk-ch10-learner-458dfac355a0`.

The selected paragraph introduces distinct masculine/neuter singular instrumental forms; the shared shapes are explained after the two tables. The existing topic label is accurate, but one complementary target makes its second half directly accessible.

Add `chapters/ch10/student.md:772`, supported by:

> Nouns use the dative-shaped form for this instrumental relation: **męte** does not acquire a new ending. Feminine singular and all plural modifiers likewise share their forms with the dative. Thus the feminine singular forms are **ðǣre** and strong **gōdre**, and the plural forms **ðǣm** and **gōdum**. Shared shape does not remove the distinction of function. In a weak adjective, use the corresponding weak dative shape; the new adjectives' separate instrumental cells remain reference.

Exact unique whole TeX line at `typesetting/ch10/chapter-10.tex:1260`:

```tex
Nouns use the dative-shaped form for this instrumental relation: \textbf{męte} does not acquire a new ending. Feminine singular and all plural modifiers likewise share their forms with the dative. Thus the feminine singular forms are \textbf{ðǣre} and strong \textbf{gōdre}, and the plural forms \textbf{ðǣm} and \textbf{gōdum}. Shared shape does not remove the distinction of function. In a weak adjective, use the corresponding weak dative shape; the new adjectives' separate instrumental cells remain reference.
```

### IL-02 — Add a direct target for sīðfæt within the three-noun alternation entry.

Implemented and verified optional refinement. Affected proposal: `book/proposals/index-late.json#/entries/84`; merged entry: `book/grammar-index.json#/entries/227`. Added anchor: `bk-ch11-learner-20cd80791fd4`.

The selected paragraph names and explains bæð and geat. The separately explained masculine sīðfæt paradigm follows later and deserves its own page reference under the combined label.

Add `chapters/ch11/student.md:367`, supported by:

> **sīðfæt**, journey; passage (masculine). Stem **sīðfæt-**. Genitive singular **sīðfætes**; dative singular **sīðfæte**; nominative plural **sīðfatas**. The singular uses sīðfæt- and the plural **sīðfat-**. This noun is masculine, so its nominative and accusative plural take -as.

Exact unique whole TeX line at `typesetting/ch11/chapter-11.tex:543`:

```tex
\textbf{sīðfæt}, journey; passage (masculine). Stem \textbf{sīðfæt-}. Genitive singular \textbf{sīðfætes}; dative singular \textbf{sīðfæte}; nominative plural \textbf{sīðfatas}. The singular uses sīðfæt- and the plural \textbf{sīðfat-}. This noun is masculine, so its nominative and accusative plural take -as.
```

### IL-03 — Add a direct target for anticipated until.

Implemented and verified optional refinement. Affected proposal: `book/proposals/index-late.json#/entries/145`; merged entry: `book/grammar-index.json#/entries/398`. Added anchor: `bk-ch11-learner-81a31350b2d5`.

The selected paragraph explains before. The until paragraph is separate. The shared anticipated-event scope is correct; the complementary target improves navigation to the second conjunction.

Add `chapters/ch11/student.md:89`, supported by:

> **Oð-ðæt**, “until”, gives the endpoint of an action or state. Use the subjunctive for the selected anticipated endpoint. **Hēr** means “here”.

Exact unique whole TeX line at `typesetting/ch11/chapter-11.tex:132`:

```tex
\textbf{Oð-ðæt}, “until”, gives the endpoint of an action or state. Use the subjunctive for the selected anticipated endpoint. \textbf{Hēr} means “here”.
```

### IL-04 — Reuse the existing unnan-command target as a second target under Verbs.

Implemented and verified optional refinement. Affected proposal: `book/proposals/index-late.json#/entries/153`; merged entry: `book/grammar-index.json#/entries/409`. Added anchor: `bk-ch10-learner-4160a02bc5fd`.

The current Verbs target explains the present indicative evidence gap. The later command-substitute paragraph is already indexed under Subjunctive; reusing that anchor gives both halves of the Verbs subheading a direct reference.

Add `chapters/ch10/student.md:1066`, supported by:

> For a direct addressed command “grant”, use **unne** to one addressee and **unnen** to several. These are the second-person subjunctive forms used as command substitutes. Cook labels unne “Imper.”; Fulk describes the subjunctive substitution. Both accounts support the same singular surface. Do not make a formal plural command in -að, or mistake command unne for the missing indicative cell. The preterite plural indicative ūðon and subjunctive ūðen differ in their final vowel.

Exact unique whole TeX line at `typesetting/ch10/chapter-10.tex:1784`:

```tex
For a direct addressed command “grant”, use \textbf{unne} to one addressee and \textbf{unnen} to several. These are the second-person subjunctive forms used as command substitutes. Cook labels unne “Imper.”; Fulk describes the subjunctive substitution. Both accounts support the same singular surface. Do not make a formal plural command in -að, or mistake command unne for the missing indicative cell. The preterite plural indicative ūðon and subjunctive ūðen differ in their final vowel.
```

Reuse existing anchor `bk-ch10-learner-4160a02bc5fd`.

## Scope and cross-reference checks

- Compared 319 nearby teaching bindings with the actual grammar register and literal teaching markers: no mismatches.
- Read the active Unit 10–18 bounded-scope and recognition-outcome records and the appendix’s optional-reference scope.
- Preserved recognition-only **wesan** participial constructions, supplied cross-clause fronting analysis, the negative paradigms’ stated indicative scope, selected third-singular impersonal frames, and contrary-present condition limits.
- Complete tables do not add count senses, unattested paradigm cells, unrestricted syntax or production milestones. The selected index labels do not imply those additions.
- Resolved all 68 destinations in 31 see and 10 see-also records. No destination or retained route is missing. `Prefixes` correctly becomes see-also because substantive merged entries exist.
- Actual Unit 13 table rows support the kinship, **frēond** and **burg** targets; the chosen table headings avoid the original distant shared overview paragraph.

## Independence and limits

The reviewer did not author the late proposal or merged index. The reviewer authored the separate early proposal and the previously accepted sound-history learner prose. Here the appendix check concerns independent index labeling, relevance and scope; it is not represented as a fresh independent audit of the underlying historical-linguistic prose. No keys were consulted. No shared source, proposal, register or index file was edited.

The final assembled PDF’s page references, link destinations and visible placement will receive a separate review after the corrected build. The source-level review does not claim that navigation review has passed.

## Complete entry coverage

Each row was compared with the actual learner explanation or paradigm. Detailed exact quotes, selected TeX anchors, scope bindings and per-entry judgments are retained in `index-late.json`. Proposal numbers are zero-based JSON entry indexes.

| Late entry | Topic | Actual master target(s) | Decision |
| --- | --- | --- | --- |
| 0 | Ablaut — inherited vowel alternation versus umlaut | `appendices/sound-history/student.md:221` | Accepted |
| 1 | Accusative — duration | `chapters/ch12/student.md:1363` | Accepted |
| 2 | Accusative — experiencer with impersonal hyngran | `chapters/ch10/student.md:700` | Accepted |
| 3 | Action substitution — dōn repeats an earlier action | `chapters/ch16/student.md:1046` | Accepted |
| 4 | Adjectives — bare strong forms naming people | `chapters/ch11/student.md:889` | Accepted |
| 5 | Adjectives — direct address | `chapters/ch11/student.md:903` | Accepted |
| 6 | Adjectives — doubled consonants before endings | `chapters/ch10/student.md:456` | Accepted |
| 7 | Adjectives — lexical final -e | `chapters/ch10/student.md:370` | Accepted |
| 8 | Adjectives — predicate and attributive agreement | `chapters/ch10/student.md:320` | Accepted |
| 9 | Adjectives — substantival use versus a separate noun | `chapters/ch14/student.md:60` | Accepted |
| 10 | Adjectives — used as nouns for people | `chapters/ch10/student.md:603` | Accepted |
| 11 | Adverbs — comparison of swīðe | `chapters/ch15/student.md:754` | Accepted |
| 12 | Adverbs — direction, time and relation | `chapters/ch16/student.md:1116` | Accepted |
| 13 | Analogy — restoration and reshaping | `appendices/sound-history/student.md:153` | Accepted |
| 14 | Apocope — final high-vowel loss | `appendices/sound-history/student.md:193` | Accepted |
| 15 | Apposition — case agreement of names and titles | `chapters/ch11/student.md:555` | Accepted |
| 16 | Back mutation | `appendices/sound-history/student.md:149` | Accepted |
| 17 | Breaking | `appendices/sound-history/student.md:43` | Accepted |
| 18 | Case — case of a phrase and its internal dependents | `chapters/ch10/student.md:13` | Accepted |
| 19 | Causation — dōn with a finite ðæt clause | `chapters/ch16/student.md:1056` | Accepted |
| 20 | Cause clauses — factual reasons | `chapters/ch11/student.md:107` | Accepted |
| 21 | Clauses — adverbial relations and mood | `chapters/ch11/student.md:3` | Accepted |
| 22 | Clauses — boundaries in long sentences | `chapters/ch13/student.md:220` | Accepted |
| 23 | Commands — dative addressee with bēodan | `chapters/ch18/student.md:1395` | Accepted |
| 24 | Comparatives — weak inflection, including predicates | `chapters/ch11/student.md:849` | Accepted |
| 25 | Comparison — equality: swā ... swā | `chapters/ch12/student.md:1383` | Accepted |
| 26 | Comparison — exact equality of amount | `chapters/ch15/student.md:790` | Accepted |
| 27 | Comparison — finite swā clauses | `chapters/ch11/student.md:217` | Accepted |
| 28 | Comparison — mā as more in number | `chapters/ch12/student.md:1381` | Accepted |
| 29 | Comparison — mā modifying an action | `chapters/ch11/student.md:223` | Accepted |
| 30 | Comparison — nominal swā phrase | `chapters/ch12/student.md:1385` | Accepted |
| 31 | Comparison — preference with swīðor ... ðonne | `chapters/ch15/student.md:772` | Accepted |
| 32 | Comparison — proportional: the more ... the more | `chapters/ch15/student.md:750` | Accepted |
| 33 | Compensatory lengthening | `appendices/sound-history/student.md:213` | Accepted |
| 34 | Concession — ðēah and the subjunctive | `chapters/ch11/student.md:175` | Accepted |
| 35 | Conditions — open and contrary-present | `chapters/ch11/student.md:187` | Accepted |
| 36 | Content clauses — anticipatory genitive ðæs with giernan | `chapters/ch18/student.md:1359` | Accepted |
| 37 | Contraction — loss of h and adjacent vowels | `appendices/sound-history/student.md:211` | Accepted |
| 38 | Coordination — both ... and: ǣgðer ge ... ge | `chapters/ch15/student.md:744` | Accepted |
| 39 | Coordination — shared subjects and omitted predicates | `chapters/ch13/student.md:177` | Accepted |
| 40 | Dative — experiencer with ðyncan | `chapters/ch10/student.md:678` | Accepted |
| 41 | Dative — object of onfōn and gemiltsian | `chapters/ch14/student.md:832` | Accepted |
| 42 | Dative — recipient, beneficiary and governed person | `chapters/ch10/student.md:653` | Accepted |
| 43 | Direct speech — speaker and addressee reference | `chapters/ch13/student.md:218` | Accepted |
| 44 | Ellipsis — recovering a predicate and its agreement | `chapters/ch13/student.md:187` | Accepted |
| 45 | Figurative language — grammar and contextual interpretation | `chapters/ch17/student.md:15` | Accepted |
| 46 | Gemination | `appendices/sound-history/student.md:181` | Accepted |
| 47 | Genitive — dependent and possessive | `chapters/ch10/student.md:15` | Accepted |
| 48 | Genitive — governed by verbs | `chapters/ch10/student.md:39` | Accepted |
| 49 | Genitive — grounds for a reward | `chapters/ch17/student.md:2669` | Accepted |
| 50 | Genitive — measurement of breadth or height | `chapters/ch12/student.md:1365` | Accepted |
| 51 | Genitive — partitive whole after a selection word | `chapters/ch10/student.md:617` | Accepted |
| 52 | Genitive — personal partitive uncer versus possessive uncer | `chapters/ch15/student.md:722` | Accepted |
| 53 | Genitive — requesting and expecting a thing | `chapters/ch16/student.md:1062` | Accepted |
| 54 | Genitive — subjective and objective | `chapters/ch10/student.md:27` | Accepted |
| 55 | Genitive — thing with a dative person | `chapters/ch10/student.md:43` | Accepted |
| 56 | Government — a prefix does not preserve the base verb’s frame | `chapters/ch14/student.md:774` | Accepted |
| 57 | Impersonal constructions — hyngran: accusative experiencer | `chapters/ch10/student.md:700` | Accepted |
| 58 | Impersonal constructions — man with a singular verb | `chapters/ch15/student.md:714` | Accepted |
| 59 | Impersonal constructions — ofðyncean: dative experiencer and content clause | `chapters/ch18/student.md:1305` | Accepted |
| 60 | Indefinite reference — hwā and hwæt | `chapters/ch15/student.md:685` | Accepted |
| 61 | Indefinite reference — ān: a certain individual | `chapters/ch15/student.md:677` | Accepted |
| 62 | Instrumental — bare means and mid with dative | `chapters/ch10/student.md:750` | Accepted |
| 63 | Instrumental — distinct forms and shared dative shapes | `chapters/ch10/student.md:752` | Accepted; IL-01 resolved |
| 64 | Mood — statement, command and wish in praise | `chapters/ch17/student.md:2597` | Accepted |
| 65 | Negation — constituent contrast with nā | `chapters/ch15/student.md:665` | Accepted |
| 66 | Negation — finite ne and negative be-series | `chapters/ch15/student.md:560` | Accepted |
| 67 | Negation — nabban: negative possession | `chapters/ch15/student.md:583` | Accepted |
| 68 | Negation — negative concord | `chapters/ch15/student.md:653` | Accepted |
| 69 | Negation — negative willan: unwillingness and refusal | `chapters/ch15/student.md:606` | Accepted |
| 70 | Negation — nān: strong declension | `chapters/ch15/student.md:629` | Accepted |
| 71 | Nouns — -nes and doubled s | `chapters/ch14/student.md:32` | Accepted |
| 72 | Nouns — abstracts in -u | `chapters/ch15/student.md:386` | Accepted |
| 73 | Nouns — frēond and its alternating stem | `chapters/ch13/student.md:414` | Accepted |
| 74 | Nouns — h-loss and compensatory lengthening: seolh | `chapters/ch11/student.md:418` | Accepted |
| 75 | Nouns — hand and woruld: endingless accusative | `chapters/ch10/student.md:153` | Accepted |
| 76 | Nouns — kinship: fæder | `chapters/ch10/student.md:121` | Accepted |
| 77 | Nouns — kinship: mōdor, dohtor and brōðor | `chapters/ch13/student.md:414; chapters/ch13/student.md:414; chapters/ch13/student.md:414` | Accepted |
| 78 | Nouns — kinship: sweostor | `chapters/ch15/student.md:367` | Accepted |
| 79 | Nouns — root: burg | `chapters/ch13/student.md:414` | Accepted |
| 80 | Nouns — root: bōc and tōð | `chapters/ch15/student.md:335` | Accepted |
| 81 | Nouns — root: gāt and its vowel alternation | `chapters/ch10/student.md:181` | Accepted |
| 82 | Nouns — shortened stems before endings | `chapters/ch10/student.md:80` | Accepted |
| 83 | Nouns — syncope: wuldor | `chapters/ch14/student.md:228` | Accepted |
| 84 | Nouns — vowel alternation by number: bæð, geat, sīðfæt | `chapters/ch11/student.md:331` | Accepted; IL-02 resolved |
| 85 | Object predicates — adjective after perception | `chapters/ch10/student.md:1072` | Accepted |
| 86 | Object predicates — calling someone blessed | `chapters/ch17/student.md:2621` | Accepted |
| 87 | Object predicates — making equal and a dative standard | `chapters/ch15/student.md:1562` | Accepted |
| 88 | Palatal diphthongization | `appendices/sound-history/student.md:131` | Accepted |
| 89 | Palatalization — consonants and change order | `appendices/sound-history/student.md:171` | Accepted |
| 90 | Participles — agreement with the object in habban constructions | `chapters/ch12/student.md:97` | Accepted |
| 91 | Participles — bare and agreeing plural predicates | `chapters/ch17/student.md:2591` | Accepted |
| 92 | Participles — base forms and passive predicates | `chapters/ch11/student.md:1069` | Accepted |
| 93 | Participles — naming people while retaining verbal complements | `chapters/ch17/student.md:2585` | Accepted |
| 94 | Participles — wesan with intransitive past participle (recognition) | `chapters/ch12/student.md:127` | Accepted |
| 95 | Participles — wesan with present participle (recognition) | `chapters/ch12/student.md:139` | Accepted |
| 96 | Passive voice — agentless clauses and the affected subject | `chapters/ch12/student.md:103` | Accepted |
| 97 | Passive voice — event and state readings | `chapters/ch12/student.md:121` | Accepted |
| 98 | Passive voice — retained genitive of possessions with berēafian | `chapters/ch18/student.md:1377` | Accepted |
| 99 | Perception — accusative actor with infinitive | `chapters/ch10/student.md:1094` | Accepted |
| 100 | Perception — infinitive actor versus finite-clause subject | `chapters/ch16/student.md:1022` | Accepted |
| 101 | Possession — predicative genitive and agreeing possessive | `chapters/ch12/student.md:1367` | Accepted |
| 102 | Prepositions — case of a phrase containing a genitive | `chapters/ch10/student.md:1124` | Accepted |
| 103 | Prepositions — on: the right-side idiom | `chapters/ch10/student.md:1120` | Accepted |
| 104 | Pronouns — bēgen: both, with plural inflection | `chapters/ch16/student.md:518` | Accepted |
| 105 | Pronouns — distributive gehwā and gehwæt | `chapters/ch15/student.md:693` | Accepted |
| 106 | Purpose clauses — finite ðæt clauses and their subjects | `chapters/ch11/student.md:121` | Accepted |
| 107 | Purpose clauses — negative: lest | `chapters/ch11/student.md:145` | Accepted |
| 108 | Quantity — fela with genitive plural | `chapters/ch10/student.md:633` | Accepted |
| 109 | Quantity — singular distribution and a plural whole | `chapters/ch15/student.md:718` | Accepted |
| 110 | Quantity — substantival micel and māre | `chapters/ch15/student.md:780` | Accepted |
| 111 | Raising — older e-to-i change versus later umlaut | `appendices/sound-history/student.md:119` | Accepted |
| 112 | Reconstruction | `appendices/sound-history/student.md:15` | Accepted |
| 113 | Reference — ambiguous antecedents | `chapters/ch13/student.md:169` | Accepted |
| 114 | Reference — gender, number and case of pronouns | `chapters/ch13/student.md:139` | Accepted |
| 115 | Reflexive constructions — accusative object: conceal oneself | `chapters/ch18/student.md:1449` | Accepted |
| 116 | Reflexive constructions — accusative with gebiddan | `chapters/ch14/student.md:814` | Accepted |
| 117 | Reflexive constructions — beneficiary with tilian | `chapters/ch14/student.md:836` | Accepted |
| 118 | Reflexive constructions — dative with a genitive feared thing | `chapters/ch18/student.md:1419` | Accepted |
| 119 | Reflexive constructions — dative with bewęndan | `chapters/ch16/student.md:1074` | Accepted |
| 120 | Relative clauses — free choice: whoever, whatever, whichever of two | `chapters/ch15/student.md:736` | Accepted |
| 121 | Relative clauses — indefinite or possible antecedents and the subjunctive | `chapters/ch17/student.md:2633` | Accepted |
| 122 | Relative clauses — internal genitive despite an accusative antecedent | `chapters/ch18/student.md:1335` | Accepted |
| 123 | Relative clauses — subjunctive in an optative setting | `chapters/ch18/student.md:1437` | Accepted |
| 124 | Relative clauses — temporal: the day when | `chapters/ch11/student.md:227` | Accepted |
| 125 | Reported speech — anterior habban construction | `chapters/ch12/student.md:175` | Accepted |
| 126 | Reported speech — person and place viewpoint | `chapters/ch16/student.md:1012` | Accepted |
| 127 | Reported speech — simultaneous, anterior and intended-later events | `chapters/ch12/student.md:155` | Accepted |
| 128 | Reported speech — willan and intended action | `chapters/ch12/student.md:185` | Accepted |
| 129 | Result clauses — asserted result versus intended purpose | `chapters/ch11/student.md:157` | Accepted |
| 130 | Smoothing — Late West Saxon and Anglian | `appendices/sound-history/student.md:159` | Accepted |
| 131 | Sound changes | `appendices/sound-history/student.md:3` | Accepted |
| 132 | Sound changes — fronting and restoration | `appendices/sound-history/student.md:26` | Accepted |
| 133 | Subjunctive — anticipated before and until | `chapters/ch11/student.md:99` | Accepted |
| 134 | Subjunctive — before an event anticipated from a past viewpoint | `chapters/ch17/student.md:2651` | Accepted |
| 135 | Subjunctive — commands with unnan | `chapters/ch10/student.md:1066` | Accepted |
| 136 | Subjunctive — contrary-present conditions | `chapters/ch11/student.md:205` | Accepted |
| 137 | Subjunctive — expectation and a possible provider | `chapters/ch16/student.md:920` | Accepted |
| 138 | Syllable weight — light and heavy stems | `appendices/sound-history/student.md:195` | Accepted |
| 139 | Syncope — internal vowel loss and analogy | `appendices/sound-history/student.md:205` | Accepted |
| 140 | Tense — completed action with habban | `chapters/ch12/student.md:51` | Accepted |
| 141 | Tense — completed action with habban: past viewpoint | `chapters/ch12/student.md:67` | Accepted |
| 142 | Tense — narrative succession | `chapters/ch12/student.md:15` | Accepted |
| 143 | Tense — present with future reference | `chapters/ch10/student.md:1100` | Accepted |
| 144 | Tense — preterite with anterior meaning | `chapters/ch12/student.md:33; chapters/ch18/student.md:1443` | Accepted |
| 145 | Time clauses — anticipated before and until | `chapters/ch11/student.md:75` | Accepted; IL-03 resolved |
| 146 | Time clauses — mid-ðȳ | `chapters/ch11/student.md:63` | Accepted |
| 147 | Time clauses — past when ... then: ðā | `chapters/ch11/student.md:19` | Accepted |
| 148 | Time clauses — prospective when with subjunctive | `chapters/ch18/student.md:1431` | Accepted |
| 149 | Time clauses — recurring or prospective when: ðonne | `chapters/ch11/student.md:37` | Accepted |
| 150 | Time clauses — while and simultaneous events | `chapters/ch11/student.md:49` | Accepted |
| 151 | Umlaut — historical i/j condition | `appendices/sound-history/student.md:69` | Accepted |
| 152 | Umlaut — noun and derivational alternations | `appendices/sound-history/student.md:89; appendices/sound-history/student.md:97` | Accepted |
| 153 | Verbs — preterite-present unnan; evidence gap and command substitute | `chapters/ch10/student.md:1034` | Accepted; IL-04 resolved |
| 154 | Verner’s law — inherited consonant alternation | `appendices/sound-history/student.md:234` | Accepted |
| 155 | Word formation — adjectives in -lic | `chapters/ch14/student.md:38` | Accepted |
| 156 | Word formation — adverbs in -e and -lice | `chapters/ch14/student.md:45` | Accepted |
| 157 | Word formation — agent nouns in -end | `chapters/ch14/student.md:23` | Accepted |
| 158 | Word formation — compounds and the final head | `chapters/ch14/student.md:17` | Accepted |
| 159 | Word formation — derivation versus inflection | `chapters/ch14/student.md:15` | Accepted |
| 160 | Word formation — ge- in lexical verbs and participles | `chapters/ch14/student.md:56` | Accepted |
| 161 | Word formation — noun suffixes: -ung, -scipe, -nes, -dōm | `chapters/ch14/student.md:23` | Accepted |
| 162 | Word formation — prefixes and their lexical limits | `chapters/ch14/student.md:49` | Accepted |
| 163 | Word formation — whole-word meanings and limits of analysis | `chapters/ch14/student.md:19` | Accepted |
| 164 | Word order — constituents and fronting | `chapters/ch13/student.md:36` | Accepted |
| 165 | Word order — finite-second tendency in main clauses | `chapters/ch13/student.md:48` | Accepted |
| 166 | Word order — fronting across a clause boundary (supplied analysis) | `chapters/ch13/student.md:222` | Accepted |
| 167 | Word order — late verbs in dependent clauses | `chapters/ch13/student.md:57` | Accepted |
| 168 | Word order — limits on verb-final rules | `chapters/ch13/student.md:133` | Accepted |
| 169 | Word order — subject pronouns after an initial adverbial | `chapters/ch13/student.md:89` | Accepted |

All 170 entries are represented above. The JSON also records the 41 individually checked cross-reference records and their resolved merged destinations.
