# Exercise 1.7–16: lexical evidence

Checked 21 October 2026. This is source evidence and proposed analysis, not learner prose or a source answer key. The coordinator owns final curriculum decisions and shared-register changes. Machine-readable candidate data are in [candidate-entries.json](candidate-entries.json).

All *Exercises* page references below are to `cook_ex_1895`, the selected 1895 scan in `sources/registry.json`. PDF numbers are one-based, with PDF page = printed page + 8 in this vocabulary. Images named `ex-pdf-N.png` use the actual PDF number; images named `ex-vocab-NNN.png` use **local rendering sequence numbers**, not PDF numbers: rendering sequence 1 = PDF48 = printed40. For the latter, PDF = sequence + 47. Every listed headword and the relevant section reference has been visually checked. No line numbers are asserted.

The English noun pairs are independently transcribed in `sources/transcriptions/ch01/exercise-1.md`. The word lists below are lexical witnesses, not Cook's answers to those pairs. Article+noun combinations in the JSON are newly prepared teaching phrases assembled from attested headwords and checked article morphology.

| Item | Target | Checked Cook spelling | Gender/class selected from Cook | Printed / PDF page | Source entry |
|---|---|---|---|---|---|
| 1.7 | dry land | drȳgnes | feminine, §51.5 | 45 / 53 | dry land |
| 1.7 | water | wæter | neuter, §47.1, 6 | 67 / 75 | water |
| 1.8 | image | an(d)līcnes | feminine, §51.5 | 51 / 59 | image |
| 1.8 | likeness | gelīcnes | feminine, §51.5 | 53 / 61 | likeness |
| 1.9 | light | lēoht | neuter, §47 | 53 / 61 | light, subst. |
| 1.9 | darkness (plur.) | ðīestru | plural; Cook directs to neuter §47 | 44 / 52 | darkness |
| 1.10 | sign | tācen | neuter, §47 | 62 / 70 | sign |
| 1.10 | season | tīd | feminine, §51.1 | 61 / 69 | season |
| 1.11 | spirit | gāst | masculine, §43 | 63 / 71 | spirit |
| 1.11 | life | līf | neuter, §47 | 53 / 61 | life |
| 1.12 | creature | gesceaft | feminine, §51.b | 44 / 52 | creature |
| 1.12 | food | męte | masculine in -e, §44 | 48 / 56 | food |
| 1.13 | year | gēar | neuter, §47 | 68 / 76 | year |
| 1.13 | day, repeated | dæg | masculine, §43.2 | 44 / 52 | day |
| 1.14 | man | mann | umlaut masculine, §46 | 54 / 62 | man |
| 1.14 | animal | dēor | neuter, §47 | 38 / 46 | animal |
| 1.15 | tree, repeated | trēo | neuter, §47.3 | 65 / 73 | tree |
| 1.15 | fruit | wǣstm | masculine, §43 | 48 / 56 | fruit |
| 1.16 | firmament | fæstnes | feminine, §51.5 | 48 / 56 | firmament |
| 1.16 | abyss | nēowolnes | feminine, §51.5 | 37 / 45 | abyss |

This supplies **18 new nouns** beyond the twelve unique nouns of 1.1–6. *Day* and *tree* recur; they are not new vocabulary items. Only the listed nominative singular forms are needed in production, except **ðīestru**, which requires nominative plural. The declension descriptions are classification support, not a claim that learners have mastered those paradigms.

The section references in the English–Old English vocabulary refer to *A First Book in Old English*. The gender conclusions above are therefore evidence-based inferences from Cook's own cross-references: §43 is headed “Masculines ending in a consonant” (printed28/PDF44); §44 “Masculines in -e” (30/46); §46 “Umlaut masculines” (31/47); §47 “Strong neuters” (32/48); §51 “Strong feminines” (34/50), with pattern b on 35/51 and -nes consonant doubling in §51.5 on 36/52. All those headings and statements were visually checked, with local images `fb-pdf-N.png`. Page33/PDF49, checked in `../ch01/grammar-pdf-3.png`, gives the special tree and water notes.

## Source spellings requiring particular care

- **drȳgnes** has a printed macron over y, clearly visible on [45/53](ex-pdf-53.png); the unmarked OCR form must not be accepted as transcription. Reader p124/PDF140 agrees.
- **męte** has Cook's hooked e, represented here by **ę U+0119**. The original [48/56](ex-pdf-56.png) is clear. This code-point representation should be declared in the editorial notes; do not silently replace it with plain e.
- **andlīcnes** is one spelling explicitly allowed by the vocabulary's **an(d)līcnes**. Choosing it is selection of a listed variant, not invention of a consonant or macron.
- **ðīestru** has eth and a macron over i. The exercise itself prints “(plur.)”, and the source editor has checked *First Book* p123 note7, which expressly identifies it as plural. Teach the required plural phrase **ðā ðīestru**. For the learner table, “plural noun” is enough: [Bosworth–Toller, *þeóstru*](https://bosworthtoller.com/31770) records feminine and neuter formations, while Cook sends this form to §47. This lesson need not imply that all historical uses have one invariant gender.
- **trēo** is the exact nominative headword Cook supplies for *tree*; §47.3 allows the w-bearing variant and explains its appearance before endings. No need to replace trēo with a more familiar modern textbook headword.

## Declared correction: wǣstm → wæstm

Cook consistently prints **wǣstm**: *Exercises* p48/PDF56; *First Book* Reader I p125/PDF141 (twice); and the *First Book* glossary p320/PDF336. The last two checked witnesses are [Reader I](fb-pdf-141.png) and [glossary](fb-pdf-336.png). This is not a stray printer error established by comparison with Cook's other pages.

The coordinator has selected **wæstm** for learner text as an explicit correction of vowel quantity under the user's correction policy. [Peter S. Baker's modern Old English Aerobics glossary](https://glossary.oldenglishaerobics.net/oeaginfo.php?objid=xwaestm&objtype=gentry) supplies the unlengthened form and identifies it as strong masculine with the fruit sense. [Bosworth–Toller, *wæstm*](https://bosworthtoller.com/34463) corroborates the spelling and agricultural/fruit sense. The JSON preserves **source_spelling: wǣstm** and **headword: wæstm** and labels the change. Source transcription remains faithful.

Cook also offers **ofet** as an alternative in the fruit entry, but the agreed correction permits retaining the reader's lexeme without adding a second production word.

## Semantic boundaries and alternatives

**Creature:** use **gesceaft**, in the sense of a created being or thing. It is not confined to an animal. Cook's 1.12 target and the 1.14 animal target should not be made artificially synonymous. The [Bosworth–Toller entry](https://bosworthtoller.com/15847) records both feminine and neuter usage; Cook's explicit §51.b supports the feminine pattern selected here. The neuter variant is historically valid and should not be dismissed as impossible if encountered in independent work. A target-vocabulary exercise may still ask specifically for the taught feminine form.

**Animal:** **dēor** is expressly the *Exercises* translation of *animal* on p38. Its sense is broader than modern English *deer*. Do not use the latter as the sole gloss or reject *beast* in the key.

**Food:** **męte** means food broadly. Its relationship to modern *meat* does not restrict it to animal flesh. The vocabulary gives several alternatives, so a task that requires this noun should state that requirement. A valid independent alternative is not automatically a linguistic error.

**Season:** **tīd** can mean a period or appointed time; the English prompt does not force one of four meteorological seasons. Preserve Cook's prompt and clarify the relevant sense.

**Firmament:** **fæstnes** is the vault/expanse of heaven in the creation narrative. Cook's reader p124/PDF140 has the term in the making and division of the waters and the naming as heaven. [Bosworth–Toller](https://bosworthtoller.com/10033) explicitly supports this sense and feminine gender. Cook also offers rodor and the Latin loan firmamentum; no need to teach them for this lesson.

**Abyss:** **nēowolnes** means the deep or a deep place. Cook's p37 *abyss* entry and p44 *deep, subst.* entry agree. [Bosworth–Toller, printed p716, *neowolness*](https://www.germanic-lexicon-project.org/html/oe_bosworthtoller/b0716.html) supports feminine gender and the abyss sense. That external entry supports semantics and gender; its differently marked headword is not a warrant for silently altering Cook's vowel marks.

## Handoff

No source-image ambiguity remains in these eighteen lexical selections. The wæstm editorial correction and the representation of hooked e must remain visible in change notes. The report does not certify the still-to-be-written lesson or key. The coordinator should carry the required sense and exact nominative form into the learning contract and distinguish nominative article compliance from general grammatical validity.
