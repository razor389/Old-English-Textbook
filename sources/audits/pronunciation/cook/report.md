# Cook pronunciation audit

The selected second edition of Cook’s *A First Book in Old English* (1895) supports the course’s spelling and quantity conventions, a distinction between long and short vowels and consonants, and practical treatment of the unfamiliar letters. Its sound values should not simply be identified with Fulk’s. The [evidence record](evidence.json) contains thirteen source summaries, the twenty exact rows of Cook’s vowel table, and the identities of eight personally inspected page images.

## Inspection and locators

Inspected printed **5–10 and 18–19**, corresponding to one-based PDF **21–26 and 34–35**, in `sources/cache/cook_fb_1895_2.pdf`. Its SHA-256 matches the source registry: `693537064f0dc335b6dd9e57079e07e2e5311383c9b102406019bbf4fb70d0f3`. Section numbers, not invented line numbers, locate the evidence. The source finding aid was used to find pages; all reported source claims were checked in the page images. The vowel-table signs were additionally inspected at 300 dpi.

The [Internet Archive record](https://archive.org/details/firstbookinolden00cookrich) confirms the selected 1895 edition’s bibliographic identity. The repository’s registered Wikimedia PDF supplies the pagination; other derivatives need not have the same offsets.

## Decisions required before prose

1. **Use a declared modern sound convention.** Cook’s §5 expressly offers approximations. Its diphthong rows are `ea = æ + uh`, `ēa = ē + ah`, `eo = e + o`, `ēo = ē + o`, `ie = i + ĕh`, and `īe = ī + ĕh`. The first component of long **ēa is actually ē** in the printed table. These are not the same choices as Fulk’s reported æu/eu/iu convention.
2. **Resolve final fricative voicing explicitly.** Cook §8, printed 8–9, gives voiced f/s/ð after a voiced sound at syllable end as well as between voiced sounds. His wording is broader than Fulk’s word-final voiceless rule. The source difference belongs in the editorial record; the learner should receive one coherent rule with necessary limits.
3. **Replace misleading modern English cues.** Cook distinguishes *last* from *man*, gives *care* for ǣ, *they* for ē, *tone* for ō, and *broad* for short o. Those instructions are unreliable when copied directly into a modern American guide: accent differences, nasal raising, r-colouring and final glides matter. Familiar words should be starting points with a short adjustment, not false exact equivalences.
4. **Use articulation for missing sounds.** Cook’s y/ȳ note already supplies a useful method: rounded lips with the tongue position for *it* or *deem*. His German *ach/ich* examples for noninitial h need an accompanying mouth-position explanation for the intended audience. His parenthetical treatment of g as a spirant is insufficient for a complete distribution rule; use Fulk for that detail.

## Usable material and limits

Cook §§2–4 support interchangeable thorn/eth spellings, the editorial nature of hooked **ę/ǫ**, pronounced unstressed syllables, macrons on long vowels or the first letter of long diphthongs, and the distinction between vowel length and syllable weight. The hooks do not create extra vowel sounds in his table. Hooked **ǫ** is not **œ/oe**.

The image-verified length contrasts in §4 include **god/gōd**, **ac/āc**, **is/īs**, and **tol/tōl** with their printed meanings. These are useful supplied pronunciation examples without assuming prior vocabulary knowledge. Some other contrasts have additional consonant or inflectional complications; the coordinator should choose only those suited to the guide’s established rules.

Cook §7 supports audible consonants in **wr, wl, cn**; k/ch values of c; g/y values of g; **cg** like the middle of *bridge*; **ng** like *finger* with a separate palatal possibility; and non-silent h, including its unfamiliar later-word values. Section 10 calls **sc** approximately *sh* and explicitly exempts **ęngel, Englisc** from palatal ng. A spelling-only front-vowel rule must not erase those qualifications.

Section 11 illustrates doubled consonants with **sunnum**, divided **sun-num**, and *penknife*. The practical target is consonant duration, without an inserted vowel. Section 23 places ordinary stress near the beginning but distinguishes prefixed verbs and **be-, ge-, sometimes for-** nouns/adjectives. Its historical discussion of vowel weakening and syncope does not authorize a learner to omit written vowels.

Cook gives no aspiration rule or explicit trill instruction in the inspected pronunciation sections. His description of initial **hl/hn/hr/hw** does not itself establish the voiceless-sonorant analysis. His core vowel table omits **io** and **œ/oe**; their absence is not evidence of a sound value. Other relevant Cook historical pages were located only through OCR, not audited here. Any such added claims need the independent Fulk evidence or a further bounded inspection.

## Handoff

This is source inspection and editorial analysis, not a learner draft or a new teaching milestone. No exercise assignment, register, chapter contract, shared index, Beads record, or Git history was changed. The coordinator can close `oec-pron-cook` once the source differences have been reconciled in the guide contract.
