# Chapter 1: editorial record

Chapter ID: `ch01`. Prepared 21 October 2026. The learner chapter, key, and learning contract are separate files. This record explains source selection, lexical decisions, and changes; it is not an additional set of learner prerequisites.

## Audience and scope decisions

The user studies Old English already, but the course assumes no prior Old English. Standard grammar terminology is assumed; a terminology appendix may be added later. The user accepts roughly thirty new vocabulary items per lesson. Accordingly, this chapter assigns all sixteen items of Group I, Exercise 1: thirty distinct noun targets, with day and tree each repeated. The article forms and conjunction are also taught explicitly. Four additional reading forms are supplied for this passage only.

The production scope is nominative definite noun phrases, lexical gender, coordination with **and**, and the single plural noun phrase **ðā ðīestru**. This does not establish general plural formation, oblique cases, a complete noun paradigm, verb conjugation, or adjective declension. The selected reading introduces recognition of a nominative subject with explicit support for its predicate.

## Source crosswalk and textual layers

- **Cook exercises:** `cook_ex_1895`, printed p.1, selected PDF p.9 (one-based), Group I, Exercise 1, items 1–16. Each English prompt is reproduced without rewording. The instruction to use nominative noun phrases and the chapter's vocabulary is new editorial teaching material. Cook supplies no Old English answer strings on that page.
- **Reading:** `cook_fb_1895_2`, Reader I, printed p.123, selected PDF p.139. The assigned text is the second sentence's first clause, from **Sēo** to **ǣmtig;**. It is an extracted clause; the original sentence continues. Three apparatus cues (4, 5, 6) are omitted, and the line break is reflowed. All linguistic wording and the semicolon are preserved. Its origin is recorded as declared normalization of the apparatus, with no linguistic adaptation.
- **Deferred candidate:** the opening sentence beginning **On anginne** was audited and is explicitly deferred in `coverage.json` because of its additional construction and form demands.
- Exercise 2 and the rest of Reader I are outside the detailed item audit. Visibility on a page is not recorded as completion of an audit.

Faithful source text and page checks are in [the exercise transcription](../../sources/transcriptions/ch01/exercise-1.md), [the reader transcription](../../sources/transcriptions/ch01/reader-I-opening.md), and [the verification report](../../sources/transcriptions/ch01/verification.md). Reader line counts, where given there, are editorial counts, not printed line-number labels.

All worked Old English phrases and model composition answers are newly prepared teaching material. Their vocabulary and morphology have separate source evidence. They are not described as quotations from Cook.

## C01: correction of vowel quantity in “fruit”

**Cook's form:** **wǣstm**, Exercises p.48 / PDF56, vocabulary s.v. fruit; the same quantity marking occurs in First Book p.125 / PDF141 and vocabulary p.320 / PDF336.

**Learner form:** **wæstm**, masculine, nominative singular, fruit/produce. The change affects the production vocabulary, Exercise 1.15's model response, its form requirement, and the cumulative lexical entry. The original English prompt is unchanged.

**Evidence and decision:** Peter S. Baker's modern [Old English Aerobics glossary entry](https://glossary.oldenglishaerobics.net/oeaginfo.php?objid=xwaestm&objtype=gentry) gives **wæstm**, strong masculine, fruit, in a glossary that distinguishes vowel lengths. Merja Stenroos, [“Nu is þeo Leore For-Leten: Conventionality, Complexity and Substitution Sets in Historical English Spelling”](https://doi.org/10.17811/selim.29.2024.109-25), *SELIM* 29 (2024), 109–125, explicitly includes **wæstm** among the lexemes with Old English short /æ/ in Table 1, p.118 (publisher PDF p.10). The table concerns later reflexes, but states the Old English vowel category directly; the decision does not infer quantity merely from an unmarked manuscript spelling. Its [page image](../../sources/analysis/ch01-lexical/stenroos-2024-p118.png) has been checked. [Bosworth–Toller, wæstm](https://bosworthtoller.com/34463) corroborates the lexical form.

Adopt the short vowel in the teaching text under the user's explicit authorization to correct errors with a note. Cook's long marking is consistent within the selected books, so this is a declared correction of vowel quantity, not a claim to have identified a printer's isolated typo. The source spelling remains in the evidence and lexicon provenance.

## V01: “evening” is a valid gender variant

Cook's vocabulary, Exercises p.46 / PDF54, refers **ǣfen** to First Book §47.7, p.33 / PDF49, which places it among neuters. Retain the neuter model **ðæt ǣfen**. Masculine **se ǣfen** is also grammatical: [Bosworth–Toller's supplement](https://bosworthtoller.com/37608) explicitly adds the neuter to the masculine and provides an attested example; [Vezzosi (2023), p.164](https://doi.org/10.36253/lea-1824-484x-14824) also recognizes both genders. This is variation, not an error in Cook. The key accepts the masculine while explaining the selected neuter practice target. The alternative does not silently establish a separate production milestone.

## Other controlled choices

- Preserve **gærs** from Cook's vocabulary; do not replace it silently with another spelling.
- Select **trēo** for production; First Book §47.3, p.33 / PDF49 expressly also allows nominative **trēow**, which the key recognizes.
- Select **heofon**, masculine. First Book §53.3, p.37 / PDF53 distinguishes it from weak feminine **heofone**; the gender does not transfer unchanged between those forms.
- Select feminine **gesceaft** with Cook. [Bosworth–Toller, ge-sceaft](https://bosworthtoller.com/15847) also records neuter usage with attested examples. The key accepts the corresponding neuter phrase while distinguishing it from the selected gender practice.
- Use the article forms **se**, **sēo**, **ðæt**, **ðā** as printed in First Book §84, p.50 / PDF66. Its note separately gives emphatic **sē**. These four forms do not constitute the complete demonstrative paradigm.
- Preserve Cook's **ę** in **męte** as Unicode U+0119. First Book §3, p.5 / PDF21 explains its historical distinction; no new pronunciation contrast is invented.
- Treat **sōðlice** in the reading as a connective (“now,” “for its part”), on the evidence of p.123 note 5, Latin *autem*. Its general dictionary meanings “indeed, truly” are acknowledged in the key. Both **īdel** and **ǣmtig** can mean empty/void; the key does not manufacture a sharp distinction between them or require a familiar Biblical translation.

## Evidence and review records

The first twelve noun entries, the grammatical audit, and the four reading supports are recorded in [the curriculum proposals](../../sources/analysis/ch01/curriculum-proposals.json) and [dependency report](../../sources/analysis/ch01/dependency-report.md). The remaining noun evidence is recorded separately by the lexical checker. These are evidence proposals; the coordinator owns the merged coverage, grammar, and lexical registers.

The independent reviewer solved all twenty-five learner tasks before reading the prepared key, then checked the source images, linguistic evidence, and coverage. The [review report](review.md) records the independent solution, minor repairs, and final approval; no material or minor linguistic finding remains open. The coordinator merged the reviewed proposals into the shared lexicon and grammar registers, retaining null teaching milestones for the supplied reading forms and construction; the reviewer independently checked the complete merged records against the proposals.

## Learner presentation and export

The lesson and key use ordinary task numbers within named sections. Stable IDs remain in HTML comments in Markdown, TeX comments in the print source, and the coverage crosswalk. Section endnotes carry source citations, the new-material declaration, valid variants, and correction C01. Removing inline editorial commentary has not removed any vocabulary, task, required support, or model answer. Individual key references are preserved in the assigned coverage records as well as the section citations.

On 22 October the user requested a substantially terser presentation, citing Thackston and Lambdin. The lesson now uses compact rules, a nominative article paradigm, three brief examples, vocabulary, and exercises. Study coaching and repeated explanations have been removed. The key retains all twenty-five responses and their essential meanings; common construction, agreement, variant, and error guidance is stated once for the relevant group. This presentation change does not alter the learning contract or the cumulative milestones. The independent reviewer checked the compressed text against all forty-eight requirements and the saved independent answers, then verified content and all eight rendered pages of the complete PDFs. No findings remain open.

The requested exports are the complete chapter and a separate complete key, including all thirty vocabulary nouns, all twenty-five tasks, the reading and support, and the notes. Font and page design remain provisional; the one-to-one lesson/exercise boundary is agreed, while later teaching contracts, readings, and final page design remain to be established.

The user also confirmed one lesson per complete numbered exercise in Cook, in source order. Chapter 1 already satisfies this rule with all sixteen items of Group I, Exercise 1. This supersedes the original provisional plan to split dense exercises; the separate reader-selection audit and recorded deferral remain valid.
