"""Curated English access routes that a bare reversal of glosses would miss.

All item references point to current assigned prompts and their accepted keys.
Entries are word/phrase aids, never complete keyed sentences.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
inventory = json.loads((OUT/'exercise-inventory.json').read_text(encoding='utf-8'))['items']
tasks = {i['task_id']:i for i in inventory}
senses = {s['sense_id']:s for s in json.loads((OUT/'sense-use-crosswalk.json').read_text(encoding='utf-8'))['senses']}

# English lookup(s) | sense IDs | attesting exercise(s) | scope / useful government
LEXICAL = r'''
cast; throw | weorpan-1 | EX-VI-20-08, EX-VIII-26-07, EX-XII-XIII-32-08 | Accusative thing cast; a following destination has its own government.
cast a net | sendan-1 | EX-XII-XIII-32-06 | sęndan takes the net as accusative object; on + accusative supplies the destination.
nigh; near; at hand | neah-u13-nigh | EX-VII-25-02 | nēah is the predicate in nigh at hand.
draw nigh; come nigh; draw near; approach | nealaecan-u13, genealaecan-1 | EX-VII-23-02, EX-XII-XIII-35-10, EX-V-18-06 | (ge)nēalǣcan takes a dative goal when a goal is expressed.
tell; say | secgan-1 | EX-II-11-09 | Person addressed is dative; direct or reported content is separate.
tell someone to; order someone to | hatan-command | EX-VII-22-09, NEW-U18-C02 | hātan + accusative actor + plain infinitive.
ill; badly | yfele-adverb-u17-local-sense | EX-XII-XIII-43-05, EX-XII-XIII-43-06 | Adverb modifying doing; distinguish the adjective yfel.
deal ill with | don-u18-deal-with, earmlice-u18-local-sense | EX-XII-XIII-44-04 | dōn earmlice wið + person; this task supplies the wið relation.
lad; boy | cnapa-u16-sense | EX-XII-XIII-46-06, EX-XII-XIII-48-02, EX-XII-XIII-48-03 | Masculine weak noun; the task's chosen word for lad.
country; native land; homeland | ethel-1 | EX-XII-XIII-38-08, EX-XII-XIII-39-03 | ēðel in these home-country references; land remains a separate ordinary country word.
fisher; fishers; fisherman; fishermen | fiscere-fisherman-source | EX-V-18-10, EX-IV-17-04, EX-XII-XIII-32-06, EX-XII-XIII-32-07 | Masculine noun; fisherman is only one English surface form of this lookup.
greatly; very | swithe-positive | EX-XII-XIII-38-07, EX-XII-XIII-45-06 | Degree adverb swīðe; retain the separate great/large adjective micel.
increase; grow | weaxan-1 | EX-I-04-18, EX-I-07-14 | Intransitive increase in these commands/wishes; not the transitive īecan increase something.
Jerusalem | hierusalem-u15-source-sense | EX-IX-30-01, EX-XII-XIII-38-03 | English spelling Jerusalem points to the retained Old English name Hierusalem.
journey; travel | faran-1 | EX-XII-XIII-33-03, EX-XII-XIII-46-09 | Verb faran; distinct from noun journey sīðfæt.
labor; labour; toil | winnan-1 | EX-VII-22-04 | Verb; the subject labours with the hands.
labor; labour; work | gewinn-u15-labour | EX-IX-30-09 | Noun in the expression from his labour.
leave; abandon | forlaetan-1 | EX-IX-30-11, EX-XII-XIII-32-07, EX-XII-XIII-32-09 | Accusative thing/place left. Distinguish leave to someone and take leave of.
multitude; number; company | getael-u13-source | EX-VII-25-10 | Singular collective getæl with the supplied dependent expression; retain source participial genitives.
multitude; crowd; company | menigu-u16-reading | EX-XII-XIII-39-02, EX-XII-XIII-42-03 | męnigu also denotes a multitude of things in the locally supplied spice expression.
overtake; catch; seize | fon-1 | EX-XII-XIII-46-09, EX-XII-XIII-47-02 | Accusative person overtaken in these tasks; the source's bracketed caught is the route.
put; set; place | settan-1 | EX-XII-XIII-46-07 | Place an accusative object; destination is a separate phrase.
road; way; path | weg-1 | EX-IX-30-11 | Roads in the quoted song uses weg; do not reverse only the register's path/way labels.
set forth; lay out | lecgean-u18-selected | EX-XII-XIII-46-03 | lęcgean + accusative thing + forð.
spice; spices; herb | wyrt-1 | EX-XII-XIII-38-03, EX-XII-XIII-39-02 | Cook specifically routes these spices to wyrt; wyrtgemang is the separate earlier spice word.
alive; live | libban-1 | EX-XII-XIII-46-05 | The bracketed liveth yet is rendered by finite libban + gīet; an added copula is not required.
amount; part | dael-part-source | EX-XII-XIII-44-01 | dǣl + genitive of the substance, as in sumne dǣl mętes; the amount is accusative object.
arise; rise | risan-1 | EX-VI-21-02 | Earlier taught rīsan supplies this command; prefixed ārīsan is separately used later.
be born | acennan-source | EX-V-18-07 | Source supplies ācęnned in a passive expression; distinguish active beget/produce.
bereft of; despoiled of; deprived of | bereafian-u18-selected | EX-XII-XIII-45-02 | Passive berēafod with genitive of what is lost; active person deprived is accusative.
beseech; pray; request | biddan-beseech-person | EX-VIII-27-09, EX-XII-XIII-45-07 | Accusative person beseeched; ðæt + subjunctive gives the requested act. Prayer to God with gebiddan is a different entry.
carry; bring | bringan-1 | EX-XII-XIII-44-08 | Cook's explicit carry hint selects bringan with accusative presents and dative recipient.
continue; remain; endure | thurhwunian-u17-selected | EX-XII-XIII-39-06 | Intransitive continuing of a building; distinguish the following dative-governing wiðstandan.
deed; deeds; work | weorc-1 | EX-IX-29-05, EX-IX-29-06 | weorc includes deed/action in these prompts; dǣd is a separate lexical option elsewhere.
everlasting; eternal | ece-1 | EX-XII-XIII-32-08 | Adjective ēce, agreeing with the noun it qualifies.
fishhook; fish-hook; hook | angel-1 | EX-VI-20-08, EX-II-11-09 | Compound English spelling and optional fish- lead to the same fishing noun; distinguish ęngel angel.
fowl; bird | fugol-1 | EX-XII-XIII-37-10 | Fowl is collective/plural English here; use the required Old English plural.
gift; grace | giefu-u17-grace | EX-XII-XIII-40-01 | Divine grace in Cook's bracketed gift route; not a license to merge all secular present/gift senses.
hear; listen to; heed | hlystan-u18-selected | EX-XII-XIII-45-07 | hlystan governs genitive of the speech heard; do not copy hīeran's ordinary accusative frame.
knowledge; understanding | andgiet-u15-source-understanding | EX-XII-XIII-43-11 | andgiet denotes the knowledge possessed and desired in this exercise.
look for; seek out; seek | secan-1 | EX-XII-XIII-47-03 | sēcan with accusative sought thing, no extra word for English for/out.
needs; necessarily; of necessity | niede-u18-local-sense | EX-XII-XIII-44-08 | Archaic English needs is an adverb here; do not use the verb need.
neighbor; neighbour | neahgebur-u16-sense | EX-XII-XIII-32-11 | Both English spellings must be findable.
number; count | geriman-u17-source-sense | EX-XII-XIII-42-03 | Exact supplied infinitive gerīman; preserve its marked length from the learner/key, not the bare register identifier/display.
plait; plat; platted | windan-u17-selected | EX-XII-XIII-42-08 | Accusative crown; material follows of. Cook's platted means plaited.
provender; fodder | fodor-1 | EX-XII-XIII-46-02 | Provender is routed by Cook's bracketed fodder to fōdor.
salute; greet | gretan-take-leave | EX-XII-XIII-40-01 | Greeting with accusative person; the same verb also has farewell/leave-taking uses.
say; speak | sprecan-1 | EX-XII-XIII-48-10 | This task explicitly selects sprecan for say; tō marks the addressee.
select; choose | ceosan-1 | EX-XII-XIII-39-01 | Accusative person selected.
soon; immediately; at once | sona-immediately-source | EX-XII-XIII-43-08 | sōna carries soon in this future-reference prompt.
subside; cease | geswican-cease | EX-XII-XIII-32-03 | Absolute command to the sea; distinct from cessation with a genitive complement.
traffic; trade | ceapian-u18-selected | EX-XII-XIII-45-08, EX-XII-XIII-45-09 | Cook's traffic means trade/buy through trade, not modern road traffic.
trust in; believe in | geliefan-u14-believe | EX-IX-30-13, NEW-U14-C03 | gelīefan on + accusative person in this assigned frame.
winged; feathered | gefithred-u17-local-sense | EX-XII-XIII-37-10 | Adjective agreeing with the fowl.
woo; seek in marriage | giernan-u17-selected | EX-XII-XIII-43-14 | Genitive person wooed; keep the marriage-seeking sense distinct from a general want.
year; years of age | winter-1 | EX-X-XI-31-11 | Supplied age expression uses wintra; gēar is the ordinary year lemma elsewhere.
rule; dominion | rice-1 | EX-VI-19-01 | Genitive rīces after geswīcan in ceased to bear rule. Do not insert a literal bear verb.
put down; cast down | aweorpan-u17-selected | EX-XII-XIII-40-06 | Accusative people put down, of + dative point from which.
lift up; exalt; raise | up-ahebban-u17-selected | EX-XII-XIII-40-06 | Accusative people raised; the prefixed verb supplies up.
conceive; imagine | asmean-u17-source-sense | EX-XII-XIII-39-07 | Exact supplied infinitive āsmēan, whose subject is the heart. The unmarked register display asmean is not the selected learner surface.
harp; play the harp | hearpian-u17-source-sense | EX-XII-XIII-42-02 | Preserve the supplied genitive harper/harping expression; headword alone does not reconstruct its syntax.
be multiplied; multiply | gemanigfieldan-multiply | EX-I-04-18, EX-I-07-14 | Assigned passive use with wesan and agreeing gemanigfield/gemanigfielde; do not infer an unassigned active causative frame.
bear; produce seed; bear fruit | beran-produce | EX-I-06-08, EX-VIII-26-06 | Accusative produce; distinguish physical carrying.
yield; produce fruit | wyrcean-yield | EX-I-06-09 | Accusative fruit; birð wæstm is a recognized lexical alternative in the key.
have dominion; bear rule; rule | ricsian-dominion | EX-I-07-01 | rīcsian can be used absolutely; English have/bear need no independent translation.
rule over | gieman-1 | EX-I-06-04, EX-XII-XIII-33-05 | gīeman governs genitive of what is ruled; English over supplies no additional preposition.
deny; refuse | forwiernan-deny | EX-III-15-04, NEW-U10-T01 | Dative person denied, genitive thing denied.
grant; allow | unnan-grant | EX-III-14-07, NEW-U10-T02 | Dative recipient and genitive thing granted; preserve the supported subjunctive command unne.
withstand; resist | withstandan-u17-selected | EX-XII-XIII-39-06 | Dative of what is resisted.
receive | onfon-u14-receive | EX-IX-28-11, EX-XII-XIII-39-06 | Selected payment frame has accusative pęning in 28.11, but selected reward frame dative edlēane in 39.6; show both with their task-specific limits.
reward; repay | agyldan-u16-source | EX-XII-XIII-34-09 | C06 corrects Cook's āgyltan to strong III āgyldan; supplied contracted present āgylt and dative recipient.
need; require | bethurfan-u18-selected | EX-XII-XIII-44-03, NEW-U18-F02 | Genitive thing needed; a relative particle may represent that governed relation.
fear | ondraedan-u13 | EX-VII-24-06, EX-XII-XIII-48-06 | Accusative person feared in 24.6; the supplied reflexive construction in 48.6 has dative self and genitive thing feared. Keep the frames separate.
know | cunnan-u16-acquaintance, witan-content, witan-u16-person | EX-XII-XIII-34-11, EX-XII-XIII-34-12, NEW-U16-C02 | Distinguish acquaintance with a person, learned ability, and knowledge of a fact/question. Follow named cunnan/witan controls.
help | helpan-1 | EX-VI-19-08, NEW-U04-D08 | Dative person helped.
benefit | fremman-1 | EX-II-11-17 | Dative person benefited.
obey | hieran-obey | EX-V-18-04 | Dative person obeyed; distinct from hearing a sound/object.
give; sell | sellan-give, sellan-u13-sell | EX-VII-23-10, EX-XII-XIII-48-06 | sęllan is sell in these two contexts; do not select give solely from the headword's earlier sense.
God; god | god-1, god-u17-deity | EX-I-03-02, EX-IV-17-12 | Preserve proper-name God versus a deity. Do not invent a productive plural of the proper-name sense.
fruit | waestm-1 | EX-I-01-15, EX-VIII-26-06 | Corrected short æ in wæstm under C01, despite the retained erroneous source hint wǣstm.
harvest | haerfest-1 | EX-VI-19-15, EX-VI-19-16 | Masculine noun; rich in uses welig on + dative fruits.
animal; beast; cattle | deor-1, nieten-1 | EX-I-01-14, EX-I-02-12, EX-I-08-10 | Unit 1 selects dēor for animal/beast, nīeten for cattle. Both can denote animals in later contexts; cattle remains plural in the tasks.
darkness | thiestru-1 | EX-I-01-09, EX-II-12-12 | Grammatically plural ðīestru; no singular is assigned.
woman; wife | wif-woman, wif-1 | EX-XII-XIII-36-02, EX-II-11-04 | Context determines woman or wife; grammatical gender remains neuter.
princess; queen | cwen-u17-princess, cwen-u17-queen | EX-XII-XIII-43-06, NEW-U17-F02 | Separate contextual senses of cwēn; the selected accusative singular is endingless.
servant | cniht-u17-servant, theowa-u17-sense, theow-servant-u18-sense | NEW-U17-F01, EX-XII-XIII-38-10, EX-XII-XIII-46-05 | Distinguish the explicit cniht, weak ðēowa and strong ðēow lexical targets.
poor man; poor person | waedla-1, thearfa-1 | NEW-U14-C01, NEW-U14-C02 | wǣdla and ðearfa follow their task's explicit target; do not collapse their lexical identity.
rich; wealthy | welig-source, rice-adjective-u17-sense | EX-II-10-06, EX-XII-XIII-40-07 | Distinguish welig and the substantival rich-people rīce frame.
good; kind | god-adjective-1, god-u15-kind | EX-I-04-03, EX-IX-29-08 | gōd can mean benevolent/kind in the taught person-directed frame; ordinary goodness is broader.
light; a light; luminary | leoht-1, leoht-count-luminary | EX-I-01-09, EX-I-04-05 | Mass light and individual counted lights are separate senses.
name; be named; be called; hight | hatan-1, hatan-u15-be-called | EX-I-06-16, EX-X-XI-31-09 | Active hātan can name an object with a second accusative; hātte is the special be-called form.
finish; accomplish; fill | gefyllan-1, gefyllan-fill-source | NEW-U08-C01 | Both senses occur in one task and require separate English access entries.
pray | gebiddan-u14-pray, biddan-beseech-person | EX-VIII-26-08, EX-XII-XIII-45-07 | Pray to God with the supplied reflexive gebiddan frame versus pray/beseech a person with biddan + accusative.
brother; brethren | brothor-1 | EX-XII-XIII-32-06 | Brethren is an English plural alias, not another Old English lexeme.
garment; raiment; clothing | waed-1, reaf-1, gegierela-u16-sense | EX-III-14-07, EX-III-13-08, EX-XII-XIII-35-09 | Preserve the distinct lexemes and explicit Cook noun hints.
in fact; indeed; truly | sothlice-truly | EX-X-XI-31-13, EX-X-XI-31-01 | Adverbial confirmation; distinct from discourse connective sōðlice where the key uses but/now.
smite; strike | slean-absolute-strike, slean-1, beatan-1 | EX-II-09-11, EX-III-15-22, EX-XII-XIII-42-09 | Slēan has a bounded objectless striking frame for hammers; 42.9 explicitly selects bēatan.
build; make | wyrcean-make, gewyrcean-1 | EX-XII-XIII-39-05, EX-I-05-02 | Preserve the prefixed/unprefixed verb required by the current task; supplied uses do not add new independent paradigms.
hold chief place | healdan-1, ealdorscipe-1 | EX-II-10-11 | healdan with accusative ealdorscipe; no article where Cook omits it.
be sufficient for; suffice | genyhtsumian-u16-source | EX-XII-XIII-34-03 | Supplied complete construction with dative beneficiary; plural books require plural subjunctive.
be astonished | ofwundrian-u17-astonished | EX-XII-XIII-38-07 | Subject plus wesan and supplied participle, with degree/result tō ðan … ðæt.
be gracious toward | glaed-u18-gracious | EX-XII-XIII-45-02 | glæd in this contextual favour sense, wið + person; not merely emotionally glad.
free; go free | freo-u16-sense, freo-u18-local-sense | EX-XII-XIII-35-14, EX-XII-XIII-47-08 | Predicate adjective with appropriate agreement.
blameless; innocent | claene-u18-blameless | EX-XII-XIII-47-04 | Source's blameless is contextual clǣne, not just physical clean.
noon; at noon | middes-u18-local-sense | EX-XII-XIII-45-04 | Whole supplied phrase tō middes dæges; preserve its genitives instead of applying ordinary tō + dative mechanically.
a while ago | hwilum-u18-earlier-time, aer-u13-before | EX-XII-XIII-45-07 | Whole supplied hwīlum ǣr; earlier sometimes alone is insufficient.
homeward; on the way home | hamweard-u18-local-sense | EX-XII-XIII-45-08 | Supplied hāmweard with wesan; distinguish noun hām and directional adverb hām.
thrice; three times | thriwa-u16-sense | EX-XII-XIII-35-06 | ðrīwa is an adverb; not a cardinal with a silently invented time noun.
thy; thine; your; yours | thin-poss-1 | EX-I-08-03, EX-VI-20-05, EX-XII-XIII-47-10 | ðīn identifies one possessor and agrees with the possessed noun. ēower and incer mark plural and dual possessors separately.
sir | leof-u18-sir-address | EX-XII-XIII-45-07 | Supplied respectful lēof address; the older gloss dear alone does not give this lookup.
in the morning | on-u18-morning, morgen-1 | EX-XII-XIII-46-09 | Fixed supplied on morgen has accusative singular in this task.
without; outside | butan-u13-without, butan-u18-outside | EX-XII-XIII-48-03, EX-XII-XIII-46-09 | Būtan + dative can mean without a companion or outside a city; conditional unless is separate.
except; unless | butan-unless-u18-condition | EX-XII-XIII-44-02, EX-XII-XIII-44-06, EX-XII-XIII-48-01 | Būtan introducing the supplied conditional exception; distinguish a prepositional complement.
as lord; appoint as | gesettan-u18-appoint-lord | EX-XII-XIII-48-08 | Supplied appointment frame: accusative person, tō + dative role, and dative people governed.
grieve | ofthyncean-u18-selected | EX-XII-XIII-48-06 | Impersonal third-singular predicate, dative experiencer, and ðæt clause for the cause.
to one another | betweonan-u18-local-sense | EX-XII-XIII-45-06 | Supplied reciprocal betwēonan him; do not translate one and another independently.
against that; in readiness for | ongean-u18-local-sense | EX-XII-XIII-46-03 | Supplied ongēan ðætte + prospective subjunctive clause.
for the benefit of | for-u18-benefit | EX-XII-XIII-48-06 | Supplied for + dative benefit phrase; its possessed noun controls possessive agreement.
instead of; in place of | for-u18-local-sense | EX-XII-XIII-48-02 | for + accusative in this supplied substitution frame.
because of; on account of | for-u18-cause | EX-XII-XIII-45-06 | for + dative cause in this supplied money expression; distinguish causal conjunction because.
as; like | swa-swa-as-source, swa-predicative-as, swilce-u16-as-if | EX-VIII-26-10, EX-XII-XIII-43-01, EX-XII-XIII-43-03 | Keep ordinary comparison, equal degree, as if and the source's stated swā-swā targets distinct.
above; over | ofer-1, ofer-authority | EX-XII-XIII-37-04, EX-XII-XIII-37-13, EX-I-07-12 | Spatial, authority/rank and preference frames have separate government. Follow the bounded task frame, not an unconditional motion rule.
both … and | ge-conjunction-source, aegther-u15-both | EX-VII-24-06, NEW-U15-C09 | ge … ge and ǣgðer ge … ge coordinate the two members. The adjective bēgen is a separate both entry.
whoever; whosoever; whomsoever; whatever; whatsoever | swa-u15-free-choice, swa-hwaet-swa-u15-source-sense | EX-XII-XIII-34-01, EX-XII-XIII-36-08, EX-XII-XIII-39-05, EX-XII-XIII-47-04 | swā hwā/hwæt swā and appropriate case forms; preserve internal clause role and any supplied attraction rather than treating English -ever as an invariant suffix.
which of two; whichever of two | hwaether-which-two, hwaether-u15-free-choice | NEW-U15-C06, EX-X-XI-31-12 | hwæðer for selection between two; supplied exceptional attraction in 31.12 is not the default relative rule.
therein; in it | thaeron-u18-local-sense | EX-XII-XIII-45-08 | Supplied ðǣron points back to the sacks' location.
today; to-day | to-daeg-1, todaeg-u17-local-sense | EX-VI-19-04, EX-XII-XIII-41-08 | Retain source/course spelling variants as routes, not different English meanings.
tomorrow; to-morrow | to-morgen-u13-source | EX-VII-24-09 | Adverb tō-morgen, not separately to plus morning.
in vain | holunga-1 | EX-V-18-05 | hōlunga; not at all in vain uses nālæs hōlunga with the intended negative scope.
at length | niehst-u12-source | EX-VI-19-01 | Whole supplied æt nīehstan.
little by little | styccemaelum-u13 | EX-VII-23-02 | Single adverb styccemǣlum.
take leave of; bid farewell | gretan-take-leave | EX-VI-21-04, EX-VI-21-12, EX-XII-XIII-32-01 | grētan + accusative person/place; no separate take or bid is needed.
be wont to; be accustomed to | gewunian-u13 | EX-VII-22-11 | gewunian + plain infinitive; no separate be auxiliary in the model.
give light to; illuminate | aliehtan-1 | EX-II-12-09 | ālīehtan takes an accusative object, not a dative inferred from English to.
give to drink | sellan-give-drink | EX-III-14-11, EX-IV-17-11 | Supplied sęllan + dative person + plain drincan; no added tō.
come to naught; come to nothing | weorthan-become, naht-u14-source | EX-VIII-26-09 | weorðan tō nāhte, supplied result phrase.
have compassion on; have mercy on; pity | gemiltsian-u14-pity | EX-VIII-27-07, NEW-U14-C04, EX-XII-XIII-46-06 | gemiltsian + dative person. A wish uses the appropriate subjunctive, not a separate have verb.
in return for; in exchange for | with-u15-exchange | EX-IX-28-02, EX-IX-29-04 | wið + dative exchange, distinct from wið + accusative opponent.
round about; all around; in circuit of | ymbhwyrft-u13-source | EX-XII-XIII-42-05 | Supplied on ymbhwyrfte + genitive landmark in this exercise.
once more; again | eft-u13-again-back | EX-IX-28-06 | eft is the repeated-occurrence adverb.
henceforth; hence forth | heonan-forth-u17-local-sense | EX-XII-XIII-40-03 | heonanforð as a whole adverb.
from afar; afar off | feorran-u14-source | EX-VIII-27-06 | feorran; the source supplies the from-afar paraphrase.
go aboard; board | astigan-source | EX-II-11-07, EX-II-11-16 | āstīgan takes the ship as direct accusative in these exercises.
go fishing | on-u16-fishing, fiscnoth-u16-sense | EX-XII-XIII-33-09 | Supplied gān on fiscnoð; do not independently invent a fishing participle.
rich in | welig-rich-in | EX-VI-19-15 | welig on + dative of what is abundant.
in the midst of | tomiddes-midst | EX-I-07-07, EX-I-07-08 | tōmiddes + dative landmark; English of does not require genitive here.
in control of; under one's control | on-control, geweald-dominion | EX-I-08-14, NEW-U08-C02 | on + dative possessed geweald; the spirits controlled remain accusative object of habban.
for food; for a sign | to-function-purpose | EX-I-06-07, EX-I-07-17 | tō + dative function, with an optional separate dative beneficiary.
learn from; learn of | aet-source | EX-VI-21-09 | leornian æt + dative person in the assigned learning frame.
look at; behold | behealdan-u13 | EX-VII-24-11 | behealdan takes accusative objects; distinguish interjection efne behold.
fall in love with | befeallan-u17-source-sense, lufu-u17-local-sense, on-u17-love-goal | EX-XII-XIII-42-01 | Supplied idiom: the person's lufu is the subject of befeallan; on + accusative identifies the beloved. Do not make the person the literal falling subject.
perhaps | wen-u16-sense | EX-XII-XIII-33-08 | wēn is ðæt + present subjunctive in the taught possibility frame.
had rather; prefer; would rather | leof-comp-preferable, wician-1 | EX-II-09-14 | Dative experiencer + is lēofre + plain infinitive. English had rather does not require past time; wician means sojourn/live with here.
as long as; inasmuch as | swa-as-long-as-source, lange-source | EX-III-15-15 | Supplied swā lange swā in this biblical context has inasmuch-as force; do not insist on duration.
is to come; be to come | to-inflected-infinitive | EX-XII-XIII-34-09 | Whole supplied is tō cumanne; bounded be-to use, distinct from purpose after a verb of coming.
for ever and ever | a-ever-u15-source-sense | EX-XII-XIII-37-06, EX-XII-XIII-40-09, EX-XII-XIII-42-06 | Preserve the source-supplied repetition ā ā ā where given; this is not three separately chosen words.
have as wife | to-u16-wife-role | EX-XII-XIII-36-07 | habban + accusative woman + tō wīfe in the supplied role frame.
by the same way | ilca-same, weg-1 | EX-VII-25-12 | Instrumental ðȳ ilcan wege, without an additional by preposition under Cook's omission control.
something of this sort | hwaethwega-u13-source, hwaethwugu-u13-source | EX-VII-25-03 | Supplied hwæthwega swilces; preserve the genitive quality expression and the chosen variant.
provide for oneself; obtain for oneself | tilian-u14-provide | EX-VIII-27-11 | tilian + dative reflexive beneficiary + genitive thing obtained.
be well; be healthy; be hale | gesund-u18-sense, hal-u18-health | EX-XII-XIII-46-04, EX-XII-XIII-46-05 | Adjectives describing health; adverb wel well in performing an action is different.
be hungry | hyngran-hunger, hungrig-1 | NEW-U10-T07, NEW-U11-T08 | Impersonal hyngran uses an accusative experiencer; the adjective hungrig agrees with its subject. Follow the exercise's named construction.
seem good to | thyncan-seem-nominative | NEW-U10-T08 | Subject thing nominative, dative experiencer, agreeing predicate gōd.
no longer; longer | leng-u18-local-sense | EX-XII-XIII-48-04 | lęng as the comparative adverb; clause negation supplies no longer.
neither … nor | nahwaether-u18-local-sense | EX-XII-XIII-48-07 | Whole supplied nāhwæðer ne … ne with finite negative scope; neither excludes both alternatives.
be it so | wesan-be, swa-1 | EX-XII-XIII-41-10 | Independent third-singular subjunctive sīe with hit and swā; no permission verb.
would have come; were it not for | wesan-u18-anterior-counterfactual | EX-XII-XIII-44-07 | Whole supplied past-subjunctive conditional and wesan + cumen result; preserve its counterfactual anterior sense.
that … may; that … might; so that | thaet-purpose | NEW-U11-T07, EX-VII-25-06, EX-XII-XIII-44-06 | Purpose normally uses ðæt + subjunctive in the assigned frames. Do not add a permission modal merely for English may; retain mugan when the prompt explicitly requests it.
lest; so that not | thy-laes-the-lest | NEW-U11-T09, EX-XII-XIII-48-03 | ðȳ-lǣs-ðe with the assigned subjunctive negative-purpose clause.
let; may (wish) | wesan-be | NEW-U07-C01, NEW-U07-C02, EX-XII-XIII-41-10 | An independent wish/hortatory uses a subjunctive; let does not automatically require lǣtan. Literal permission to go uses lǣtan + accusative actor + infinitive.
be able to; can; could | magan-1, cunnan-1 | NEW-U06-M01, NEW-U06-M02, NEW-U06-M11 | mugan expresses ability/capability; cunnan + infinitive emphasizes learned ability. Infinitive is plain, not tō-inflected.
be allowed to; may (permission) | motan-1 | NEW-U06-M06, EX-IX-29-03, EX-XII-XIII-44-02 | mōtan + plain infinitive; permission/prohibition differs from ability and independent wishes.
have to; had to; must; ought to | sculan-1 | NEW-U06-M05, EX-II-11-05 | sculan + plain infinitive for obligation; English have to is not possessive habban. Supplied have something to offer in Unit 6 is a different construction.
want to; wish to; be willing to | willan-1 | NEW-U06-M07, NEW-U06-M10, EX-XII-XIII-33-09 | willan + plain infinitive denotes volition; intention does not assert the action occurred.
be unwilling; refuse to | willan-refuse | EX-II-09-13, EX-II-11-06 | ne + willan, or the licensed contracted negative, with a plain infinitive.
need to | thurfan-1 | NEW-U06-M03 | ðurfan + plain infinitive; distinguish beðurfan + genitive thing needed.
dare to | durran-1 | NEW-U06-M04, EX-XII-XIII-48-03 | durran + plain infinitive; ne dearr denies daring.
more; greater | ma-1, ma-more-numerous, micel-comp-u15-amount, swithe-u16-degree, swithe-u15-preference | EX-VI-20-07, EX-IX-28-12, EX-XII-XIII-32-10, EX-XII-XIII-44-04 | Distinguish more in number, larger amount, greater adjective, more intensely and preferential rather. English more is not one unrestricted OE equivalent.
better; best | god-adjective-comp-1, god-adjective-superl-1, wel-comparative, wel-superlative | NEW-U03-C05, NEW-U03-V03, EX-XII-XIII-35-04 | bętera/bętst are adjectival; bęt/bętst are adverbial in the selected comparison of doing. Give the appropriate form for the task.
this; these; that; those | thes-1, se-that | NEW-U03-D02, EX-I-05-06 | Inflected demonstratives agree with their noun; ðæt also has separate conjunction and relative uses.
his; her; its; their | he-possessor | NEW-U02-C06, NEW-U02-C07, NEW-U02-C08 | Invariant personal genitive possessor; distinguish the same surface used as a governed personal case.
my; mine; our; ours; your; yours | min-poss-1, uncer-poss-1, ure-poss-1, thin-poss-1, incer-poss-1, eower-poss-1 | NEW-U03-P01, NEW-U03-P02, NEW-U03-P03, NEW-U03-P04 | Select possessor person/number, then agree with the possessed noun. Dual possessors have their own forms.
who; whom; what; whose | hwa-interrogative | NEW-U08-Q02, NEW-U08-Q03 | Inflect the interrogative by its role/government; dependent questions and relatives are separate constructions.
no one; nobody; no man; nothing; never | nan-u14-source, nawiht-u15-nothing, naefre-1 | NEW-U15-C01, NEW-U15-C15, EX-XII-XIII-34-02, EX-XII-XIII-43-02 | Use the taught negative expression with finite ne or the licensed negative contraction; negative concord expresses one negation.
each; every; everyone | aelc-each, gehwilc-each, gehwa-each-reference | NEW-U15-C08, NEW-U15-C18, EX-IX-28-01 | ǣlc/gehwilc with a singular noun; personal gehwā for each person. Preserve genitive/other case roles, not only a nominative lookup.
all; whole; everything | eall-all, eall-substantive | NEW-U07-C06, EX-I-06-15 | Distinguish agreement with a noun from substantival all people/everything.
some; a certain; any | sum-some, sum-partitive, an-u15-indefinite, aenig-any, hwa-u14-indefinite-source, hwilc-u13-any | NEW-U08-N01, NEW-U15-C03, NEW-U15-C04, NEW-U15-C19, EX-XII-XIII-32-09 | Keep a certain, a subset, an indefinite person, and interrogative/nonassertive any separate; use the task's required selection word.
one; single; alone | an-1, an-alone, an-u18-local-sense | EX-XII-XIII-47-10, NEW-U03-N01 | ān can be a cardinal or an agreeing alone adjective; supplied ænne in 47.10 is not the omitted indefinite article.
as … as; just as … as | swa-equative-degree, swa-equative-standard | EX-VI-21-05, NEW-U15-C11, EX-XII-XIII-41-01 | swā … swā frames equal degree; distinguish the proportional the larger … the better construction.
the … the (proportional comparison) | swa-u14-proportional-source | NEW-U15-C10 | swā … swā with comparatives; English the is not the definite article here.
than | thonne-than | EX-II-09-15, NEW-U03-C04 | Comparison standard follows ðonne; do not confuse temporal ðonne then/when.
when | tha-when, thonne-when, hwonne-when | NEW-U11-T01, NEW-U11-T02, EX-III-14-13 | ðā factual past, ðonne recurring/future, hwonne interrogative; retain the local clause's mood rules.
while | mid-thy-when, tha-hwile-the-while | NEW-U11-T03, EX-VII-25-03 | Complete conjunctions mid-ðȳ or ðā-hwīle-ðe, as the assigned context requires.
before; after; until | aer-before, aefter-after-source, aefter-u15-after-clause-source, oth-thaet-until | NEW-U11-T04, NEW-U11-T05, EX-X-XI-31-11 | Distinguish adverb, preposition and finite-clause connection; æfter ðǣm ðe is a complete supplied after-clause expression.
because; for (causal) | for-tham-because, for-thon-the-because | EX-II-11-10, NEW-U11-T06 | Causal conjunction is different from prepositional because of/for the benefit of.
although; though; even though | theah-although | NEW-U11-T10, EX-VII-23-13 | ðēah with the taught concessive clause; a subjunctive need not make an admitted fact unreal.
therefore; accordingly | for-thon-the-u16-therefore, eornostlice-thus | EX-XII-XIII-36-05, EX-IX-28-11 | Adverbial consequence must be distinguished from a because clause despite related forms.
if | gif-if | NEW-U11-T11, NEW-U15-C04 | gif does not by itself choose a mood; open, tentative and counterfactual conditions have distinct taught frames.
that; who; which (relative) | the-relative-which, se-relative | NEW-U17-C01, EX-VII-24-01 | Invariant ðe or inflected relative/demonstrative; case belongs to the clause role, not automatically the antecedent's case.
that (reported content) | thaet-conjunction-1 | NEW-U17-C04, NEW-U09-A02 | Content ðæt is separate from demonstrative and relative that; choose mood/time from the reporting construction.
that (result) | thaet-result | NEW-U11-T08, EX-XII-XIII-38-07 | Result clause, often with degree swā/tō ðan; distinguish intended purpose.
to (purpose) | to-inflected-infinitive | NEW-U06-N07, NEW-U06-N08 | tō + inflected infinitive expresses the assigned elementary purpose; modal complements use plain infinitives.
be; is; was; were | wesan-be | CH01-COMP01, CH01-COMP02, NEW-U06-M12 | Copular eom/wæs and bēo indicative series; later passive and compound uses require their own construction.
have; has; had | habban-1, habban-perfect | NEW-U06-M05, NEW-U12-C01, NEW-U12-C02 | Possessive habban versus habban + transitive past participle. Do not translate every English perfect or obligation with possessive have.
be (passive); become (passive) | wesan-passive, weorthan-1 | NEW-U12-C03, NEW-U12-C08 | Appropriate finite wesan/weorðan plus the taught passive participle; distinguish a state, event and simple lexical become.
be … -ing; was … -ing | wesan-present-participle | EX-VII-25-03, EX-XII-XIII-32-09 | Simple OE finite forms can render English progressive aspect; wesan + present participle is only one bounded source construction, not a required default.
had …; have … (completed action) | habban-perfect, wesan-intransitive-perfect | NEW-U12-C01, NEW-U12-C02, EX-VII-25-12, EX-XII-XIII-45-08 | Preserve the action's time relation. Simple preterite, sometimes with ǣr, often renders English perfect/pluperfect; use an analytic construction only where taught/requested.
do; does; did (question or negative helper) | ne-1 | EX-III-15-22, NEW-U08-X03, NEW-U02-C12 | No dummy dōn: inflect the lexical verb, with ne for negation and the taught question order. Lexical do/perform and substitute dōn are separate.
do; did (repeat an action) | don-u16-substitute | EX-XII-XIII-35-04, EX-XII-XIII-35-05, NEW-U16-C03 | dōn can replace the action already mentioned in a comparison; distinguish modern English dummy do.
will; shall (future reference) | wesan-be | EX-III-13-05, EX-VI-21-09, EX-XII-XIII-33-08 | Present morphology can carry future reference; bēo is used in its bounded expected-state frame. Do not add willan unless volition or a stated source target requires it.
would; should | willan-1, sculan-1 | NEW-U12-C06, EX-IX-30-11, EX-XII-XIII-44-02 | Select intention, obligation, reported prospect or counterfactual context; English spelling alone does not determine tense, mood or an OE modal.
there is; there was | wesan-be, weorthan-u16-arise, thaer-there | EX-VII-25-10, EX-XII-XIII-32-04, EX-XII-XIII-38-02 | Presentational there has no obligatory OE word. Cook may supply ðā, use weorðan, or explicitly omit there; locative ðǣr is a distinct retained word.
it (anticipatory or impersonal) | he-1 | EX-VII-23-13, EX-XII-XIII-36-07, EX-IX-29-09 | Hit occurs in some taught impersonal/anticipatory frames; other supplied passives expressly omit it. Follow that whole frame.
a; an | an-u15-indefinite | CH01-COMP04, NEW-U15-C19, EX-XII-XIII-38-02 | No obligatory indefinite article: bare predicates/nouns often translate a/an. ān is used for the taught introducing-a-certain-individual sense, not inserted everywhere.
the | se-the | EX-I-01-01, EX-II-10-11, EX-XII-XIII-39-02 | Select article agreement only where required; preserve all explicit Cook omission controls and bare noun predicates.
of; 's (possession) | se-the | EX-I-03-01, EX-III-13-01, NEW-U03-A09 | Possessive/relational English of or 's often becomes a dependent genitive, not preposition of. Partitive, source and lexical government require their own frames.
to; for (recipient or beneficiary) | ic-personal, thu-personal | CH01-CASE09, NEW-U02-C13, EX-XII-XIII-44-01 | A dative noun/pronoun often expresses the recipient/beneficiary without an added preposition. Distinguish destinations and lexical government.
myself; yourself; himself; herself; ourselves; yourselves; themselves | he-1, ic-personal, thu-personal, self-emphatic-reflexive | NEW-U02-C09, NEW-U02-C10, NEW-U02-C13, NEW-U08-N05 | Ordinary reflexive personal pronouns take the governed case; agreeing self adds the taught emphasis. English -self does not automatically require self.
the sick; the hungry; the righteous; the dead; the living | untrum-people, hungrig-people, rihtwis-people, dead-people, cwic-people | EX-III-14-12, EX-III-15-15, EX-VI-21-05, EX-IV-17-12 | Substantival adjectives take their own agreement/case; do not add man/people/ones where Cook omits it.
one (people in general) | mann-u11-source | NEW-U15-C07, EX-XII-XIII-48-07 | Impersonal man has a singular finite verb; distinguish numeral ān and one selected member of a group.
thou; thee; ye; you | thu-personal | NEW-U02-P01, NEW-U02-P02, NEW-U02-P03, EX-I-08-03 | Singular ðū, dual git and plural gē systems; thou/thee mark singular, ye plural. Unspecified you allows appropriate choices unless the task specifies number.
I; me; we; us; we two; us two | ic-personal | NEW-U02-P01, NEW-U02-P02, NEW-U02-P03 | Select case from the verb/preposition and preserve dual versus plural; dual subjects use plural verb forms.
he; she; it; they; him; her; them | he-1 | NEW-U02-P04, NEW-U02-P05, NEW-U18-A01 | Grammatical gender and antecedent determine reference; it may be represented by masculine/feminine forms for a gendered inanimate noun.
thousand; hundred; high numbers | thusend-local, hund-hundred-source, hundteontig-u17-supplied | EX-IV-17-17, EX-XII-XIII-32-09, EX-XII-XIII-42-02 | High quantities retain the complete local numerical expressions; a glossary headword does not replace the supplied genitive/counting construction.
second time | other-1, sith-u18-sense | EX-XII-XIII-44-07 | Supplied ōðre sīðe means a second time; adverbial instrumental singular, without a separate indefinite article.
'''

rows=[]
GRAMMAR_ONLY_LABELS = {
    'let', 'be … -ing', 'had …', 'do', 'will', 'would', 'there is',
    'it (anticipatory or impersonal)', 'a', 'the', "of", 'to',
    'myself', 'the sick', 'one (people in general)', 'thou', 'I', 'he',
    'thousand',
}
for raw in LEXICAL.strip().splitlines():
    if not raw.strip():continue
    aliases, ids, examples, note = [s.strip() for s in raw.split('|')]
    ids=[s.strip() for s in ids.split(',')]
    examples=[s.strip() for s in examples.split(',')]
    assert all(s in senses for s in ids), (aliases,[s for s in ids if s not in senses])
    assert all(t in tasks for t in examples), (aliases,[t for t in examples if t not in tasks])
    labels=[s.strip() for s in aliases.split(';')]
    grammar_only = labels[0] in GRAMMAR_ONLY_LABELS and not (labels[0]=='do' and '(repeat an action)' in aliases)
    rows.append({'entry_id':f'EN-ACCESS-{len(rows)+1:03d}', 'english_lookups':labels,
                 'entry_kind':'grammar_route' if grammar_only else 'lexical_or_phrase_route',
                 'rendering_kind':'grammar_note' if grammar_only else 'lexical_or_phrase',
                 'sense_ids':ids,'oe_targets':[{'sense_id':s,'lemma_id':senses[s]['lemma_id'],'headword':senses[s]['headword']} for s in ids],
                 'usage_note':note,'example_task_ids':examples,
                 'evidence':[{'task_id':t,'contract':tasks[t]['contract'],'student':tasks[t].get('student'),'key':tasks[t].get('key')} for t in examples]})
    if grammar_only:
        rows[-1]['related_oe_records']=rows[-1].pop('oe_targets')
        rows[-1]['oe_targets']=[]
        rows[-1]['display_rule']='Display as a grammar/phrase note, not a direct English-to-OE word equation.'

data={'schema_version':1,'scope':'Curated actual-prompt aliases, idioms, and grammar access routes supplementing a sense-specific lexical index. Some routes have no single-word equivalent. Instructional English is excluded.',
      'not_a_new_teaching_assignment':True,'source_policy':'Reuse accepted prompt/key/source evidence at the linked current item IDs; preserve the original Cook hints and corrections. Contextual synonym access does not widen an assigned sense or case frame.',
      'target_resolution':'Resolve oe_targets by sense_id to the current canonical glossary entry/display headword. Stored headword is register provenance, not an overriding learner display. Preserve the complete usage_note for grouped choices.',
      'entries':rows}
(OUT/'lookup-additions.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'{len(rows)} curated entries; {sum(len(r["english_lookups"]) for r in rows)} English lookup labels')
