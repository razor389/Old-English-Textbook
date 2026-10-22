# Unit 2 grammar source audit

Source editor: `opening_source`, 22 October 2026. Source work only: no learner prose, exercise key, assignment contract, registers, or Beads edits. This audit is ready for contract reconciliation. It does not itself establish learning milestones.

The completed inventory is [paradigms.json](paradigms.json): **23 verb lemmas, 276 distinct finite cells, 40 personal-pronoun cells, and 14 bounded rules**. Every verb has all three persons in singular and plural in both present and preterite indicative. The seven-value `surface_row` is a compact view, not a replacement for the twelve recorded cells. The source inventory includes all four Class III verbs and all ten of Cook's Class I §113 diagnostic domains, along with irregular Class I, the two short Class I families, and Class II. Each lemma has a selected sense, source references, separate citation forms, variants, and a statement limiting the syntax licensed by its paradigm.

## Inputs and source method

Read the active instructions, status, policy, workflow/handoff, course plan/map, registry, **actual** `chapters/ch01/coverage.json`, `curriculum/grammar.json`, and `lexicon/entries.json`. Unit 1's noun/article case forms, bounded case uses, and eom/wæs indicative are genuinely taught. Its hē/hit, sealde, geworht, and other reading-support forms were supplied. None supplies a prior personal-pronoun or weak-verb paradigm milestone. No new numbered Cook exercise set is assigned by this audit; the course map plans new tasks for Unit 2.

Primary source: Cook, *A First Book in Old English*, second edition, 1895, registry ID `cook_fb_1895_2`. Cached PDF SHA256: `693537064f0dc335b6dd9e57079e07e2e5311383c9b102406019bbf4fb70d0f3`. For the body, **printed page +16 = one-based PDF page**. Grammar paragraph numbers are original source identifiers. Tables do not have invented source line numbers. The reading has printed line markers, and this report uses those only where identified.

`cook-fb-finding.txt` is an OCR finding aid, never the authority for a letter or length mark. The PNGs in this directory were rendered directly from the selected scan and visually inspected. Dictionary pages in `../unit02-reading/` were independently inspected by the reading source editor and then by this auditor; the JSON links their actual paths. Images preserve originals. Removing a dictionary hyphen in `ge-fyllan` → `gefyllan` is a declared presentation choice; it is not a claim about a freely productive prefix.

Some complete tables are **compositions from explicit source rules**, not twelve verbatim attestations. `evidence_basis` says so in every finite cell. Cook prints full paradigms for hīeran, sęllan, fręmman, nęrian, lufian and the four III verbs; his “etc.” past cells are expanded using §96. The other Class I rows combine his diagnostic principal parts, lexical class assignment, and present/dental rules. Prefixed verbs combine a separately checked prefixed dictionary entry with its named pattern. This distinction must survive integration.

Two supplementary checks resolve facts that should not be attributed to an unlocated Cook sentence:

- **U02-DUAL:** Ringe and Taylor, *The Development of Old English* (2014), §1.1.2, printed p.6 / preview PDF21, explicitly says plural verb forms are used with dual-pronoun subjects. The coordinator's [record](../unit02-supplementary/dual-agreement.md) and actual page image were read. This imports no spelling.
- **U02-WRIGHT-VERBS:** Wright and Wright, *Old English Grammar*, second edition (1914), §§305, 476, 524, 528–529, 532–533, printed pp.151, 248, 267, 269–270, 273 / PDF171, 268, 287, 289–290, 293. The reading source editor made an independent morphology check; this auditor inspected all six supporting images. Wright corroborates cyst, sęttan's contraction, inherited gemination in fyllan, the exact gierwan present row, and the efnan headword. Cook's ę/ð and quantities remain the selected spelling.

## Personal pronouns and possessive boundaries

Cook §§81–83, printed pp.48–50 / PDF64–66, supplies the complete system. Selected rows are:

| Person/number | Nominative | Genitive | Dative | Accusative |
|---|---|---|---|---|
| 1 singular | ic | mīn | mē | mē |
| 1 dual | wit | uncer | unc | unc |
| 1 plural | wē | ūre | ūs | ūs |
| 2 singular | ðū | ðīn | ðē | ðē |
| 2 dual | git | incer | inc | inc |
| 2 plural | gē | ēower | ēow | ēow |
| 3 masculine singular | hē | his | him | hine |
| 3 neuter singular | hit | his | him | hit |
| 3 feminine singular | hēo | hiere | hiere | hīe |
| 3 plural, all genders | hīe | hiera | him | hīe |

The macron in **hīe** is printed in Cook's `hī(e)`. `hi(e)re` and `hi(e)ra` have no macron. `hine`, `hiene`, `hire`, `hira`, and `heora` are not to be given invented vowel length. `hiere` and `hiera` are the selected targets; `hire`/`hira` remain valid unassigned source variants. Optional and less common forms are separate JSON variants, not competing required recall targets.

All six first-/second-person genitive cells are recommended **new recognition**, while the remaining thirty-four selected cells are **new production** in separately taught constructions. Cook §83 distinguishes inflecting possessives mīn, ðīn, ūre, ēower, uncer, incer (and sīn) from indeclinable his, hi(e)re, hi(e)ra. Learning a personal genitive does not teach the strong adjective endings required by its agreeing possessive use. Defer that system, sīn, and self. Third-person possessive choice follows the possessor; it does not change with the case, number, or gender of the possessed noun.

Cook §82 says personal pronouns serve for reflexives. §§184(a,b), pp.100–101 / PDF116–117, distinguishes reflexive dative and accusative uses and prints **hē geręste hine**. The bounded productive self-resting frame is therefore secure. A personal-pronoun form alone does not prove coreference: hine can mean “him” or “himself” in different constructions. The Sabbath passage's first hine refers back to God; its later hine refers to the day. Dative self-beneficiary examples can be cited without pretending that all reflexive verb-government patterns have been taught.

## Weak indicative families and exceptions

The JSON's selected complete rows cover these families:

| Cook family | Selected representative(s) | Diagnostic preterite |
|---|---|---|
| §113 ordinary long stem | hīeran | hīerde |
| §113 doubled consonant, represented by ll | gefyllan, from fyllan | gefylde |
| §113 ss/ff/pp | cyssan | cyste |
| §113 tt | sęttan | sętte |
| §113 consonant + d | sęndan | sęnde |
| §113 vowel + d | lǣdan | lǣdde |
| §113 c/p/x | īecan | īecte |
| §113 consonant + t | geręstan | geręste |
| §113 vowel + t | mētan | mētte |
| §113 rw/lw | gierwan | gierede |
| §114 irregular ll | sęllan | sealde |
| §114 irregular rc | gewyrcean | geworhte |
| §115(a) short geminate | gefręmman | gefręmede |
| §115(b) consonant + sonorant | ęfnan | ęfnede |
| §116 short -ian | nęrian | nęrede |
| §§118–119 Class II | lufian, geblētsian, gehālgian | lufode, geblētsode, gehālgode |
| §§120–124 Class III, all four | habban, libban, sęcgan, hycgan | hæfde, lifde, sægde, hogode |
| §121 negative companion | nabban | næfde |

The **22 affirmative lemmas** have production-form recommendations; **nabban's twelve cells are recognition-only**. Form production is compatible with diagnostic morphology tasks; it does not silently grant every lexeme a productive sentence frame.

Teach the ordinary present and past endings with the surface changes, not as an unchecked instruction to append endings to an infinitive. Short fręmman/nęrian families retain gemination/i in 1sg and plural but not 2/3sg. Class II -ian is distinguished lexically from short Class I -ian; lufian's -ast/-að and -ode contrast with nęrian's -est/-eð and -ede. The four Class III systems must remain distinct: libbe/leofast/leofað, hæbbe/hæfst/hæfð, sęcge/sægst/sægð, hycge/hygst/hygð. No long quantity has been inferred for leofast, lifde, sægde, or hogode.

For long/dental Class I, Cook §§33–35, pp.24–25, and §§113–117 explain simplification and dental changes. Keep the contrasts sęnde : lǣdde and geręste : mētte. Surface forms such as cyst, sętt, and sęnde can have several analyses. Selected geręstan 2sg present is the full-ending **geręstest**, 3sg **geręst**; **geręst** is also an accepted contracted 2sg variant, independently secured by Wright §476. The gierwan row **gierwe, gierest, giereð, gierwað** is directly corroborated by Wright §529, while Cook explicitly allows present w retained or omitted. Do not regularize it to a uniform w rule.

The short-stem treatment records the exceptions together: Cook §115 gives ęfnde alongside ęfnede, and lęcgan has lęgde/lēde rather than regular *lęgede. The selected ęfnan headword uses Cook's printed ęfn- stem; Wright §532 explicitly supplies efnan “perform” and both past types. Its remaining cells are transparently built by the cited pattern. **hyngran is not a substitute productive personal paradigm**: Cook §§171,190 gives the impersonal mē hyngrede. Likewise ēhtan is only a source comparison for the consonant+t family, not an assigned new lemma or a government model. An early proposed “genitive-only” warning has not been retained: Cook p.149 / PDF165 actually prints **and hiera gewinnan hīe ēhton and slōgon**, with accusative hīe and coordinated verbs. This does not warrant assigning every government pattern of ēhtan; it prevents an exclusive rule being imposed on the unassigned verb without a lexical audit.

§114's other lexical irregulars are not silently treated as regular, but they are not new assignments either. The bounded productive representatives are sęllan and gewyrcean; the source's wider list remains reference evidence for later vocabulary. Teaching their patterns does not require independently producing every lexical item printed in Cook's grammar.

## The reading verbs and lexical government

The six Sabbath verbs have their own checked lexical entries; no free ge- rule is needed:

| Lemma | Selected sense | Dictionary locator | Actual source finite form |
|---|---|---|---|
| gefyllan | finish; accomplish a work | p.292 / PDF308, §113 | gefylde |
| gewyrcean | make; build | p.296 / PDF312, §114 | geworhte |
| geręstan | rest; repose, with reflexive accusative | p.294 / PDF310, §§113,184b | geręste |
| gefręmman | perform; accomplish a work | p.292 / PDF308, §115a | gefręmede |
| geblētsian | bless | p.290 / PDF306, §118 | geblētsode |
| gehālgian | hallow | p.292 / PDF308, §118 | gehālgode |

Cook's source paragraph p.128 / PDF144 supplies these actual past forms. `geblēdsian` is a dictionary spelling variant, not a replacement for the reading's geblētsode. The passive opening, strong verbs, relative clauses, temporal accusative phrase, adjectives, and infinitival ending remain the reading auditor's separately supplied dependencies. Identifying a weak finite form does not remove those supports.

The ordinary direct-object rule is **§168**, p.96 / PDF112; §169 concerns an infinitival subject and is outside this unit. Normal accusative objects can be used with the checked senses of hear, love, kiss, set/place, send, lead, save, meet/find, perform/make, bless, hallow, and possess; a recipient/destination must have its own licensed frame. The source actually gives accusative work with finishing/performing/making. “Fill with a substance” is not acquired from gefyllan's separate “finish a work” sense or from its dictionary pointer to §156. Giving continues the already established dative-recipient/accusative-thing frame, now with an independently taught finite paradigm.

For **īecan, gierwan, ęfnan, hycgan**, the conservative recommendation is morphology-only tasks until a concrete syntactic frame is separately evidenced. The English gloss “prepare” does not by itself certify a newly composed food-preparation example; a full hycgan table does not teach complement clauses. For sęcgan, a bounded direct-report frame is checked: p.132 / PDF148 has the speaker headings **Se smið sægð:** and **Se trēowwyrhta sægð:** followed by their own utterances. This supports direct quotation with an independent clause, not indirect speech or unrestricted complement syntax.

## Negation and citation forms

`ne (ni), not` is checked in the vocabulary, p.306 / PDF322. The source sequence **and gē mē drincan ne sealdon** (p.136 / PDF152, printed line 6) places ne immediately before the finite verb. It is evidence for the negative sequence, not permission to test the infinitive in that sentence. Productive tasks should use ne with the introduced noncontracting weak verbs.

Cook §29 says habban's initial h is **frequently**, not universally, lost after ne. The complete nabban companion from §121 is recorded for recognition. A valid contracted or uncontracted alternative is not an error merely because it differs from the recall target. This unit does not assign negative-copula forms or negative concord. §183's multiple negatives remain outside the bounded simple-negation production rule.

Infinitive and past-participle citations are separate from the twelve finite cells. They identify dictionary entries and principal parts only. Displaying `(ge)hīered`, `geworht`, or `gefręmed` does not teach a ge-prefix rule, participial agreement, passive/perfect syntax, or independent participle production. Cook's optional parentheses are preserved in citation records; the source reading's actual forms remain unchanged.

## Corrections during audit and handoff

The independent morphology crosscheck identified an overgeneralization in the initial optional-variant list. Proposed **cyseð/cysest** and **gefyleð/gefylest** were not certified by Cook's sęllan table: inherited ss/ll cannot be treated automatically as fręmman's j-gemination in full-ending forms. Those proposals and other unnecessary mechanically generated full-ending variants were removed. Wright explicitly prints older **cysseþ**, and his fyllan discussion distinguishes inherited gemination. This is a correction to this audit's preliminary inference, not a claim that the selected source contains an error or that every historical single-consonant spelling is impossible. The selected cyst, gefylst, and gefylð cells were unaffected. Exact source variants remain recorded separately; the variant list is not exhaustive.

The source editor has not opened any Unit 2 answer key or expected-answer/task-model file. A later independent reviewer must still solve the learner material before reading its key. Source truth, pedagogical scope, assignment acceptance, and completed review remain separate gates.

No material source uncertainty remains in the selected inventory. The coordinator should retain the per-cell evidence basis, the six recognition-only personal genitives, the recognition-only nabban system, citation-only nonfinites, the lexical government boundaries, and the reading's supplied constructions when building the contract. This report recommends source-task acceptance, not completion of Unit 2.
