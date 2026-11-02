# Opening-unit design proposal

Recommend the **complete nominative subject inventory in Unit 1**, with the complete four-case personal-pronoun tables and remaining uses retained in Unit 2. This is a complete bounded subject system beside the copula, not a claim to teach all personal-pronoun uses. No keys or independent-solution files were opened for this proposal.

Unit 1 explicitly excludes OE pronouns (student lines 217 and 386). COP01–06 therefore ask only for English-labelled forms, while all eight independent compositions and both mini-passages use third-person noun subjects. The learner cannot independently use the full copula with a speaker or addressee. This is a practical grammatical gap.

## Choice of sequence

The ten nominative cells make every copula person usable immediately: **ic, ðū, hē, hit, hēo, wit, git, wē, gē, hīe**. They support identification, location and present/past contrast using vocabulary already assigned. Unit 2 can then develop the meaningful contrast between familiar subjects and newly inflected objects, recipients and possessors alongside independently conjugated action verbs.

Moving all forty personal cells into Unit 1 is possible: its four noun cases already have basic uses. But it adds thirty cells beyond the subject inventory, including six reference-only genitives, ambiguous object forms and invariant possessors. Meaningful coverage would add a substantial case/reference syllabus to a unit with 44 noun lemmas and many stem alternations, often still dependent on supplied action verbs. The recommended sequence has a clearer communicative progression; its justification is not merely fewer edits.

Unit 2 should retain all forty cells in complete tables: ten reviewed nominatives, twenty-four newly productive obliques and six newly recognized genitives. No introduced noun paradigm is reduced. The distinction between a subject inventory and a full personal declension must be stated explicitly.

Cook §81, pp.48–49 / PDF64–65 supplies the selected forms; both retained page images were inspected for this proposal. Ringe and Taylor §1.1.2, p.6 / publisher-preview PDF21 supplies the explicit dual-agreement statement in the checked U02-DUAL record. Cook remains the spelling baseline. Existing Unit 1 noun evidence is in `sources/audits/unit01-source/expanded-grammar.md`; no new noun forms are proposed.

## Necessary prerequisites and limits

- Explain speaker, addressee and third-person reference, then pair the forms with the complete present and preterite copula.
- **Wit/git** mean “we two/you two” and take ordinary plural verb forms. There is no dual verb ending or third-person dual pronoun. Ordinary plurals do not categorically exclude two; a task can explicitly request the dual.
- Teach **hē/hit/hēo** with masculine/neuter/feminine antecedents, including familiar inanimates. English “it” does not automatically select **hit**. **Hīe** serves every plural gender. Gender and number constrain reference but do not always make an antecedent unique.
- Keep the shared **1–3 pl.** copula row, while displaying the distinct subject pronouns completely in a separate inventory or explicitly mapped column.
- No oblique personal form, possessive, reflexive, adjective predicate, question, copular negation or extra tense is licensed by this addition. The Creation passage still needs its exact unfamiliar verbs and larger clause support.

## Exact teaching records

Only these ten existing form IDs acquire earlier recognition/production milestones after review:

| Form | Existing form ID |
|---|---|
| ic | `ic-nom-sg` |
| ðū | `thu-nom-sg` |
| hē | `he-m-nom-sg` |
| hit | `he-n-nom-sg` |
| hēo | `he-f-nom-sg` |
| wit | `ic-nom-dual` |
| git | `thu-nom-dual` |
| wē | `ic-nom-pl` |
| gē | `thu-nom-pl` |
| hīe | `he-nom-pl` |

All currently begin recognition and production at ch02. Preserve those old records in the revision history. **Hē/hit** also have supplied-in-ch01 history; keep that original exposure witness. Do not promote accusative **hit**, or feminine/plural accusative **hīe**, merely because their spelling matches a new subject form.

Existing `u02-personal-pronouns`, `u02-pronoun-reference` and `u02-dual-agreement` descriptions include oblique or object-agreement scope. Keep their broad milestones at Unit 2 and add bounded Unit 1 subject, dual-subject agreement and subject-reference features. The JSON gives proposed IDs, exact old descriptions and all thirty unchanged Unit 2 cells.

The sense records need the same care: `ic-personal` explicitly includes “me/us”, while `he-1` includes ordinary object cases. Prefer bounded subject-only teaching records (`ic-subject`, `thu-subject`, `he-subject`) if the schema cannot qualify a sense milestone by exact form IDs. These are teaching-scope refinements under existing headwords, not invented meanings. Reusing current semantic sense IDs is also viable if the per-chapter record and integrator enforce the precise nominative limit. Root should settle this representation before prose.

Preserve personal-genitive recognition and later milestones: Unit 3 `u03-possessive-agreement`; `thu-gen-pl` productive only in its Unit 9 partitive frame; `ic-gen-dual` productive only in its Unit 15 partitive frame. Earlier subject teaching must not move any of these.

## Vocabulary-to-model links

Use **section + one named model** consistently: **§3: fisc**, **§4: hof**, **§4: sǣd**, **§4: tācen**, and so on. This uses the existing numbered sections and avoids 24 new paradigm numbers. Each target must be visible in its table header or caption. Twenty-three models already meet this condition. Add an explicit **ðīestru** caption above its generic “Case / Plural” table (current line 197); the noun is currently named only in the preceding paragraph. The 18 current logical paradigm records and every selected case/number cell remain unchanged.

The retained `typesetting/ch01/chapter-01.tex` confirms the ambiguity: vocabulary lines 534, 560, 570 and 598 give only §4 for **ǣfen, wæter, tācen, nīeten**; light/heavy entries share “hof/sǣd”. These labels need precision, not new morphology.

| Vocabulary noun | Proposed reference |
|---|---|
| ǣfen | §4: ǣfen |
| morgen | §3: morgen |
| dæg | §3: dæg |
| niht | §7: niht |
| eorðe | §6: eorðe; S |
| heofon | §3: fisc |
| fisc | §3: fisc |
| fugol | §3: fugol |
| gærs | §4: sǣd; S |
| sǣd | §4: sǣd |
| trēo | §4: trēo |
| wyrt | §5: wyrt |
| drȳgnes | §5: andlīcnes; S |
| wæter | §4: wæter |
| andlīcnes | §5: andlīcnes |
| gelīcnes | §5: andlīcnes |
| lēoht | §4: sǣd; S |
| ðīestru | §7: ðīestru; P; G pl ðīestra |
| tācen | §4: tācen |
| tīd | §5: tīd |
| gāst | §3: fisc |
| līf | §4: sǣd; S |
| gesceaft | §5: gesceaft |
| męte | §3: męte; S |
| gēar | §4: sǣd |
| man | §7: mann |
| dēor | §4: sǣd |
| wæstm | §3: fisc |
| fæstnes | §5: andlīcnes; S |
| nēowolnes | §5: andlīcnes; S |
| sǣ | §7: sǣ |
| hwæl | §3: hwæl |
| nīeten | §4: nīeten |
| anginn | §4: sǣd |
| God | §3: fisc; divine name, singular |
| brādnes | §5: andlīcnes; S |
| gegaderung | §5: gegaderung |
| lyft | §4: sǣd; S |
| frætwung | §5: gegaderung; S |
| weorc | §4: sǣd |
| cynn | §4: sǣd |
| steorra | §6: steorra |
| līehting | §5: gegaderung; S |
| hof | §4: hof |

The heavy model includes short vowels plus clusters or doubled consonants: **gærs/cynn** follow **sǣd**, not **hof**. In **anginn**, use stressed **-ginn**. **Trēo** retains its own model and exceptional **trēowu**. The four disyllabic references identify their actual selected retained/syncopating models; the monosyllabic weight rule must not replace those paradigms.

Keep every S/P limit, the singular divine-name scope, and the untested reconstructed **\*sǣwa** cell. Valid alternatives remain valid: **trēow, wætru**, vowel retention beside the selected **fugol/morgen** syncope, feminine plural **-e**, **-ung** oblique **-a**, and **nihte**. A model label selects the requested target without declaring every alternative erroneous. Keep correction C01 **wæstm**, with short **æ** and no **dæg/hwæl** alternation before its cluster.

## Fresh-context practice

Keep all 46 exact Cook prompts. Preserve the useful existing case-role reversals and giving contrasts. Add transfer in stages:

1. Resolve a speaker/addressee/reference situation and produce the subject plus present or past copula. Revise COP01–06 while retaining the six person targets; cover three third-singular genders and add explicit dual targets.
2. Replace a repeated subject in a short account with a pronoun, including inanimate masculine/feminine antecedents. The answer must depend on context and meaning.
3. Use a specific vocabulary model in a fresh taught combination: contrast **hof/sǣd**, **tācen/wæter/ǣfen/nīeten**, **trēo**, weak models and an individual exception. Do not independently test recognition-only plurals or reconstructed forms.
4. Let a small scene or before/after report determine which statement fits and what person, number or tense needs correction. English instructions avoid importing OE question or negative syntax.
5. Add a connected copular exchange/account requiring reference or tense tracking across sentences, plus a brief constrained response. English speaker labels need no **sęcgan** construction; avoid untaught subject ellipsis or clause coordination.

This is task architecture, not final learner prompts. Before prose, contract every form, sense, construction, response and separate key counterpart. Each selected subject cell needs productive application; printing or copying a table is not contextual transfer. New noun-model applications should differ from the worked examples while using assigned senses. Require independent solving before key access, and distinguish a valid source variant from a specifically requested target.

## Minimal Unit 2 changes

At line 3, replace only the opening claim that personal pronouns are wholly introduced here: the unit now completes familiar subject pronouns with their other cases. Keep its recognition-only genitive/nabban and citation limits.

At line 7, present person and dual agreement as a short recap, and state that the complete tables repeat known nominatives beside new obliques. At line 38, distinguish reviewing nominatives from learning the new oblique cells; retain the possessive warning. The JSON preserves the exact current wording of all three locations.

The complete tables, ordinary oblique explanations and P01–P06 remain useful cumulative practice. No existing prompt must be deleted. The JSON identifies 42 Unit 2 tasks with exact nominated form dependencies whose prior/new provenance changes; all other target requirements remain intact. It also identifies the affected examples, both connected compositions and the Sabbath reading at exact contract pointers, together with the three complete paradigm/lexical teaching records and current prerequisite-identity fields that need a revision bridge.

## Downstream work

Update the Unit 1 contract before prose, then Unit 2’s active prerequisite records. Keep original per-chapter histories and later accepted prior-scope witnesses rather than rerunning historical whole-course integration helpers. Revise the two unit briefs and course-plan descriptions; no Cook item assignment changes.

The three dictionary headwords **OE-ic, OE-thu, OE-he** already cover the forms and meanings. Re-audit revised masters and new English prompts, mapping any bounded sense IDs to existing meanings. Preserve frozen 38-master/exact-5580 acceptance as historical evidence and add current revision coverage.

The index needs precise Unit 1 subject, dual and reference targets while retaining Unit 2 full-declension, genitive, object and reflexive targets. A complete-declension entry must not point only to nominatives. Existing entry pointers and anchor IDs are in the JSON; resolve actual pages after the new export.

Re-export complete affected Unit 1 learner/key and Unit 2 learner components, then rebuild both assembled volumes, contents, folios, bookmarks and index against newly accepted component identities. Repeat affected independent solving and actual page inspection. Run preservation comparisons against the updated accepted components and unchanged others; an explicit revision amendment must supersede the old protected-input assumptions. Update README, STATUS and HANDOFF after acceptance.
