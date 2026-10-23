# Unit 7 source audit

Source-editor handoff, 23 October 2026. This audit covers **all 34 assigned Cook prompts** and the complete fifth-day Creation paragraph. It proposes no Unit 8 work and does not itself assign or certify teaching. The coordinator owns Beads, the coverage contract, canonical source dispositions and registers.

The six actual active contracts and cumulative registers were checked against the immutable `build/unit07-prior-baseline.json`, checkpoint `47b92a4`. Earlier source exposure and bare participial citations were not treated as teaching. No earlier active file, register, registry, brief, or archived file was changed by this source editor.

## Stable deliverables

- `exercises-prompts.json`: all 34 exact prompts, original IDs, page/PDF locators and image identities. I.4.18 plus I.6.1–16 and I.7.1–17; no omission or proposed deferral.
- `exercise-requirements.json`: one requirement audit per prompt, actual earlier lexical senses/statuses, new frames and complete-system demands. The original Exercise 4 note refers to **55**, not the OCR reading 65. Exercise 7.11 crosses printed pages 3–4.
- `reading-source.json`: exact 89-word fifth-day paragraph, separate ten-line transcription and learner flow, all original notes 4–21, source hash, boundary and presentation changes.
- `reading-tokens.json`: all 89 occurrences, exact surface forms, form and sense identities/statuses, their actual earlier records, and local support links. Separate statuses prevent a prior form from silently promoting a new sense or construction. All claimed prior productive forms and senses have actual production milestones in the baseline; validation found no missing prior IDs.
- `reading-support.json`: ten explicit support spans for the reading's remaining dependencies.
- `lexical-metadata.json`: image-backed headwords, lexical source spelling, word class, gender where applicable, exact evidence and bounded scope for all sixteen new/promoted lexical candidates covered here.
- `evidence.json`: the pages actually inspected, each with printed and one-based PDF page, image path and SHA256. `rendered-images.json` also records rendering-only pages as pending; mere rendering is not evidence of inspection.
- `composition-review.json`: independent acceptance of the 56-word new account and eleven teaching examples at the recorded seed hash. The Old English was solved before consulting the author's private intended reading.
- `author-only-reading-witness.json` and `author-only-composition-solution.json`: private independent translations/analysis. A later learner-task reviewer must solve first and must not open these witnesses prematurely.

The ignored helper `build/unit07-source-audit.py` reconstructs the structured audit; `build/unit07-source-render.py` renders selected scan pages. Neither helper changes shared course data.

## Source boundaries and assignment

The exact reading is Cook's *First Book*, second edition, printed **126 / one-based PDF 142**, editorial prose lines **5–14**, from **God cwæð ēac swilce** through **se fīfta dæg.** It is the complete fifth day. The sixth-day continuation on printed 127 was inspected solely as evidence for authority with **ofer + accusative** and related lexical frames; it is not proposed as another reading assignment.

The fifth-day paragraph subsumes the earlier deferred record **`ch02-text-01`**, alias **`ch02-reader-birds`**, at printed 126 editorial lines 12–13. The coordinator should reconcile that alias into the new whole-paragraph assignment without silently duplicating it or rewriting earlier contracts. Printed marginal anchors 5, 10 and 15 support the editorial prose-line count; not every line bears a printed numeral.

No Old English word or ending was changed. Line wrapping and the two line-end hyphens in *swimmendu* and *styriendlicu* are removed only in the learner flow. Original superscript cues are represented by a separate complete note inventory. Source **męrgen**, **styriendlicu**, **cucu**, **blētsode**, and all quantities remain visible.

## Findings that control teaching and support

The Cook sets require more than a headline mood/passive lesson. They require full selected systems of **gīeman**, **rīcsian**, **gemanigfieldan**, **wyrcean** and the promoted **tōtwǣman**; a full applicable neuter **geweald** declension; deliberate productive **eall**; full agreeing **ǣlc**; ordinary naming with two accusatives; and the specified spatial, function and adverbial uses. Existing **swīðe** “very” is already productive. **Beran** “bear/produce seed or fruit” needs a sense addition beyond the earlier “carry.”

The headword is **ǣlc**, with long ǣ. The macron was checked in an enlarged portion of FB printed274 and independently by the grammar editor in that image and Exercises printed46. Earlier short spelling in audit conversation was an error; the stable metadata is corrected. **Gemanigfieldan** has no printed quantity mark in *field*. The dictionary's **ge-manig-fieldan**, **ge-weald**, **tō-twǣman**, and **fisc-cynn** are separately retained as source headwords; joining those lexical hyphens is declared presentation.

**Gīeman** governs a genitive (FB296, §156f on91). It must not be converted by an automatic accusative-object passive recipe. **Ofer** in authority expressions takes the overt accusatives attested in the sixth-day speech (FB127). **Bufan**, **under**, and **tōmiddes** have image-verified local dative examples in the second day (FB124). Spatial **ofer eorðan** itself does not identify a unique case: the weak singular form is accusative/dative syncretic. General motion syntax is not established by these examples.

The selected prior **lyft** is **neuter**, and selected prior **sǣ** is **masculine**. Independent examples must follow those selections unless a separate system is taught. A draft requirement that called *lyft* feminine was caught against the immutable register and corrected before handoff. The source phrase **ðǣre sǣ wæteru** is specifically **feminine genitive singular**, “waters of the sea”; it is separately supplied, with its own form identity. It does not silently promote a feminine *sǣ* paradigm.

In **under ðǣre heofonan fæstnesse**, *heofonan* is genitive singular and *fæstnesse* dative. The article is formally feminine genitive/dative and can be construed with the dependent or the head; do not uniquely grade that article's case. This ambiguity is distinct from the syntactically determinate genitive in “waters of the sea.”

**Tēon** is present third-plural subjunctive with waters as subject; **tugon** is past third-plural indicative. Both belong to supplied “bring forth,” not automatically prior “draw/pull.” The object-relative **ðe** and following subject **ðā wæteru** are explicitly identified by original notes12–13. The relative construction and **on hiera hīwum / æfter hiera cynne** remain supported.

The source-only lemmas **æfter**, **cucu**, **fisccynn**, **forð**, **hīw**, and plain **blētsian** all have checked headwords and word classes; **fisccynn/hīw** are neuter under §47. Cook expressly calls **cucu** irregular in his system. **Blētsode** does not inherit the earlier prefixed verb *geblētsian*. **Styriendlicu** is a separate supplied source form; the prior selected neuter accusative plural was *styriendlic*.

The original source recommendation leaves **swimmendu**, **flēogendu** and **libbendu** supplied. The coordinator has since reconciled **only those three exact neuter accusative plural forms** to new recognition, explicitly explained and assessed through R3. The contract's `scope_reconciliations` should preserve this narrow override without promoting other cells or independent production. The original audit recommendation remains recorded as evidence.

**Weaxað, bēoð, gefyllað** address a plural “you” by imperatives. **Ðā fuglas bēon** then has a third-person plural subject and subjunctive wish. **Gemanigfielde** is the source plural past participle, expressly identified in note19. **Gefyllað** has supplied “fill” rather than the earlier “finish/accomplish work.” The closing **wæs geworden** is an intransitive result formula; it is not an ordinary passive of a transitive verb.

## New-composition check

The current new account and eleven examples were checked independently from their Old English and from the actual earlier register identities. Identical spellings were not used to infer earlier mood teaching: *helpe*, *gān*, *swimme*, *cōme*, *hulpe* and *bēo* each need the new contextual analysis where used. The account is coherent and uses selected masculine sea in its related example. The final account uses an ordinary past passive without introducing a new narrative sense of *nū*.

The example **Ðā dēor sindon bundene** is defensible under Cook §62: a verbal predicate may be indeclinable or end like a strong masculine. The selected adjectival model separately gives strong neuter nominative/accusative plural **bundenu**, with **bundene** and **bunden** accepted as variants under Cook §57.3 and its paradigm. These adjective variants overlap the verbal-predicate spellings. The distinction is that verbal predicates need not follow obligatory attributive agreement; neither spelling is thereby invalid attributively. The composition review now records this reconciliation after inspection of Cook printed39/PDF55 and printed41/PDF57.

## Handoff

The source audit is ready for coordinator reconciliation and source-task closure. The coordinator still must save the agreed contract before prose, map the proposed IDs and scope overrides, complete the author/key work, obtain independent learner-task review, and finish export inspection. This handoff does not certify any of those later stages. The design agent owns private Cook models; no worker has written Beads.
