# Unit 12 source audit

The source package is ready for the coordinator’s learning contract. It assigns all 38 Cook Group VI items: Exercise 19 (17), Exercise 20 (9), and Exercise 21 (12), printed pp. 9–11 / registered PDF pp. 17–19. No item is redistributed, omitted, or deferred. This report concerns source preparation; it does not certify a lesson, key, review, or export.

The audit starts from the eleven actual active contracts and cumulative lexical/grammar registers at `74da7bb`. The source editor owns only this directory and its named scratch helpers; the coordinator owns Beads and integration.

## Reading and source fidelity

The selected connected extract is `FB-VI-PICTS-SCOTS-RELIEF-01`, editorial title **First Roman relief and the renewed invasion**, from Cook’s *The Invasion of Britain by the Picts and Scots*: printed p. 145, editorial lines 1–7, continuing through p. 146, editorial line 11, ending **and hīe mid ealle foriermdon.** It contains 155 words in two paragraphs. The registered PDF pages are 161–162. Editorial line counts are distinguished from Cook’s printed marginal numbers.

The span gives a complete sequence: raids, appeal, Roman relief, advice and withdrawal, renewed invasion. A separate English context identifies the Britons and the Roman withdrawal before the extract. It adds no words to the Old English. The p. 145 top-of-page continuation of p. 144 note 10 is outside this span; all 21 notes actually attached to the selected text are retained. The nineteenth-century ethnological speculation in p. 145 note 2 is preserved as archival apparatus, not stated as a current course fact.

`reading-source.json` keeps transcription, original notes, note cues, printed-page lines, exclusions, and declared changes separate. Joining line-end hyphenation does not silently change lexical spelling. Exact **onweg**, **ādrifon**, **Rōmanisca**, hooked **ę**, and written quantities remain as printed. Original p. 146 note 13 reads **Lat. cædunt**. No claim based on the initially misread *cuncta* survives.

All 38 English prompts were checked against the three exercise-page images. Wording, omissions, abbreviations, and grammatical hints remain visible. Exercise 21.11 preserves the original adjacency **(om. an)other.** Exercise 20.8 keeps Cook’s **ǣrest** hint while a visible note directs the learner to the already taught agreeing ordinal **ǣrestan**. Exercise 20.4 retains printed **sē ðe**; its long-vowel spelling is locally supplied beside the prior selected **Se ðe**.

## Lexical and grammatical scope

The source proposal contains 90 lemma records, 598 form records, and 90 sense records, including additions to existing lemmas. These figures include locally supplied historical vocabulary; they are not a count of new productive vocabulary. Verb systems and the chapter’s main constructions are separately owned by the grammar analyst.

The 36 complete nominal/adjectival paradigms contain 540 cells: 22 noun systems and 14 strong/weak adjective tables. Every noun has singular/plural NGDA; every adjective table has all gender/number NGDA cells plus separately marked instrumental reference cells. The abstract nouns **gehīersumnes** and **ręst** have singular productive senses and plural reference morphology. Displaying those plural cells creates no unassigned count-plural use.

New patterns and lexical stem diagnostics include **fōt/fēt**, **fēond/fīend**, **hęre**, **ēðel/ēðl-**, **sāwol/sāwl-**, and **wǣpen/wǣpn-**. **Sciphęre** repeats the same-unit hęre model and is marked `new_class: false`. Cook’s expressly allowed expanded hęre stems remain accepted variants. Wright §§416–417 supplies an independent image check for genitive plural **fēonda**; the unrelated **-endra** family is not substituted. **Ēadig** retains its full-vowel selected table with the source-backed optional syncope and endingless alternatives stated explicitly. **Īsern** adjective is distinguished from the earlier iron noun.

The needed rest/repose sense of **ręst** cites the actual Exercise 21.9 hint, not merely Cook’s vocabulary gloss couch/bed. **Fōt** as a measure has its own sense record. **Mildheort** and **stānweall** have directly inspected Bosworth–Toller facsimile support. Dictionary division hyphens are joined only in declared teaching lemmas; BT’s acute quantity in **stán-weall** becomes Cook-style **stānweall** with that change recorded. No vowel length is inferred from modern spelling.

Eleven Cook help groups supply the restricted names, numerals, fixed expression **æt nīehstan**, **lēo**, **nāh**, **nis**, **nolde**, and city ellipsis. The negative **nolde** is a single supplied preterite subjunctive form checked against Cook §139; no full negative paradigm is assigned. Numerical **mā** in Exercise 20.7 follows the grammar analyst/coordinator’s primary dictionary check. The models use the actual prior systems **scēaphierde**, **ceaster**, **sindon**, and **ðā-hwīle-ðe**.

## Dependencies and meaning

Every reading word has an exact form and sense identity in `reading-tokens.json`. Sixteen local help groups cover all supplied forms, senses, and constructions. Regular taught/new dependencies are separately listed in `reading-construction-requirements.json`; local help does not erase earlier learning or promote all senses of familiar words.

The notes preserve these distinctions:

- The initial **and hīe fela gēara…** permits two surface analyses of hīe; context fixes the event, not a uniquely visible nominative/accusative form.
- The senders change from Britons to Romans, and the final attackers are the earlier enemies. Pronouns do not name their referents by morphology alone.
- **Onsęndon** is active Old English despite the compared passive Latin apparatus.
- **Wæs onweg gewiten** is an intransitive completed-state/perfect expression, not a passive.
- The reported condition, purpose, recommendation, source **wið + dative**, instrumental **micle**, and fixed **mid ealle** retain explicit local support.
- **Ealle … ðæt** need not be forced into an overt masculine personal-relative analysis; “all they encountered” is acceptable. The final **rīpe ierðe** is the crop simile, not a new ordinary meaning of the word for people.

Public `exercises-dependencies.json` contains unordered requirements only. All 38 items have a separately retained corrected private model and exact ordered binding: 322 model words altogether. Every supplied model requirement has task-specific visible help; no recognition-only form or sense is required in independent production.

Exercise 20.6 was repaired before resealing: both hortatives use **gewyrcen**, with the prior accusative build-object frame and the newly taught **ābūtan + accusative** phrase. The earlier **dōn** placement frame was restricted to **on + accusative** and is no longer extended here. The English prompt and initial independent witnesses remain unchanged.

Exercise 21.10 now binds its single **swā + noun phrase** to the grammar analyst’s explicitly evidenced predicative-comparison sense and feature. It does not borrow the earlier finite-clause comparison or the two-token degree pattern. The model text and prompt are unchanged.

Exercise 21.5 distinguishes the first **swā** as the degree marker and the second as the comparison standard. Both use the grammar analyst’s new productive sense records under the already assigned two-token equative construction. This replaces the stale finite-comparison sense while preserving the model text and prompt.

## Independent witnesses and limits

The source editor prepared private Cook and source-reading witnesses before consulting the designer’s private witnesses or draft key. The initial provisional strings remain unchanged in `author-only-cook-models.json`; they are evidence of independence, not certified answers. Corrections live separately in `author-only-cook-corrected-models.json` after comparison with the actual registers and primary evidence. The source-reading witnesses agree on the main event chain, changing actors, prior departure, and crop simile. The 53-word new composition also has a separate independent private translation. Its public 12 examples and 38 tasks were inspected for forms, clause meaning, and teachability.

**Limited reviewer pre-exposure:** during the negation/frame discussion, the source editor sent the reserved grammar reviewer one full proposed Exercise 21.4 clause. The reviewer disclosed it to the coordinator. No private witness files or other model answers were sent to that reviewer. The coordinator will obtain a fresh reviewer’s blind 21.4 solution after drafting; the original reserved reviewer must not be described as fully blind on that item. This limitation is also machine-recorded in `validation.json`.

`validation.json` passes the source-package checks with no unresolved source dependency. `evidence-catalog.json` contains 104 source records, including actual image hashes. `manifest.json` seals public artifacts and labels all private witnesses. The next step is the coordinator’s contract checkpoint, followed by learner prose, a separate key, the required independent review, and complete exports.
