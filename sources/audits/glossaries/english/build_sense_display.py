"""Reviewed lexical sense display and English access, separate from registers.

The explicit table records editorial decisions for source inflections, syntax,
contextual senses and raw metadata. Simple semantic glosses are retained as
reviewed; their semicolon-separated synonyms remain separate access labels.
"""
import json
import re
from pathlib import Path

OUT=Path(__file__).resolve().parent
SOURCE=json.loads((OUT/'sense-use-crosswalk.json').read_text(encoding='utf8'))['senses']

# sense ID | short display gloss | English access labels (; separated) | qualifier
OVERRIDES=r'''
aberan-u11-source | carry | carry; bear | Supplied carried form; retain the ā-prefix.
abraham-u14-source | Abraham | Abraham | Biblical patriarch; supplied name forms.
aefter-according-to-source | according to | according to | With dative.
aefter-after-source | after | after | Temporal preposition with dative.
aefter-u15-after-clause-source | after | after | In the supplied finite-clause conjunction æfter ðǣm ðe.
aefter-u16-follow | after; following | after; follow | With a person followed.
aefter-u16-seeking | after; in search of | after; in search of; inquire after | Person sought or inquired after; keep this lexical frame distinct from temporal after.
aelc-each | each; every | each; every | With singular noun; substantival each follows the case required by its clause.
aegther-u15-both | both | both; both … and | In ǣgðer ge … ge.
aet-source | from | from; learn from; learn of | æt + dative person with learn.
aet-u15-proceeds | from; out of | from; out of | Proceeds of work, in the assigned expression.
aetgaedere-u11-source | together; at once | together; at once | Paired with samod in the supplied source.
aethelthryth-u13-source | Etheldred; Æthelthryth | Etheldred; Æthelthryth | Proper name.
aethelwald-u11-source | Æthelwald | Æthelwald | Proper name in apposition to father.
aethele-u16-reading | noble people | noble people; the noble | Substantival adjective in the source.
agan-depart-u16-source | go away | go away; depart | Supplied gone-away form; distinct from āgan possess.
aginnan-u16-source | begin | begin | Supplied source form began.
aliefan-u16-source | permit; allow | permit; allow; be permitted | Impersonal permission frame, with dative permitted person; consult the complete supplied expression.
alutan-u17-selected | bow; incline oneself | bow; incline oneself | Reflexive meaning in the assigned use.
an-u15-indefinite | a certain | a certain; a; an | Introduces an unnamed singular individual; not an obligatory indefinite article.
and-1 | and | and | Simple coordination.
andgietfullice-u15-source-sense | most intelligibly | intelligibly; most intelligibly | Supplied superlative adverb.
apollines-u17-local-sense | Apollo | Apollo | The god, distinct from Apollonius.
apollonius-person | Apollonius | Apollonius | Supplied dative person in the assigned source expression.
ar-u14-source | honour; high position | honour; honor; high office; high position | Contextual rank or office, not a new general meaning of every ār form.
arcestrates-u16-reading | Arcestrates | Arcestrates | King of the region in the story; supplied name forms.
arcestrates-u18-local-sense | Arcestrates | Arcestrates | The king; supplied name forms.
ascian-u13 | ask about | ask; ask about; inquire | Person asked and matter inquired about have the taught lexical frame.
ascian-u16-source | ask about | ask about | Supplied source form asked about.
asmean-u17-source-sense | conceive | conceive; imagine | Exact supplied infinitive āsmēan in the heart-conceiving expression; not an independently assigned full paradigm.
astreccean-u13 | prostrate oneself | prostrate oneself | Reflexive accusative; the before phrase retains its own case/construal.
astyrian-u17-reading | move; set in motion | move; set in motion | Supplied source sense.
athenian-u13-attend | direct; stretch toward | direct; turn one's attention to | Directing the mind toward what is heard; supplied figurative phrase.
athindan-u11-source | swollen | swollen | Supplied weak participial adjective describing the sea.
awyrcean-u15-source-sense | do; deserve | do; perform; deserve | In the source, deserving through one's conduct; retain the complete local frame.
ban-1 | bone; ivory | bone; ivory | Ivory is elpes bān, literally elephant's bone.
bathian-u16-source | bathe | bathe | Supplied source form bathed.
be-according-source | according to | according to | With dative.
be-u14-concerning-source | concerning; about | concerning; about | With dative.
be-u14-reference-source | by that; from that | by that; from that; on that evidence | Refers to the preceding proposition; supplied expression.
be-u15-source-word-by-word | word by word | word by word | In word be worde; literal correspondence.
be-u16-grasp | by | by | Body part by which a person is led; supplied grasping phrase.
be-u17-south | in the south | in the south; south | Only in supplied be sūðan.
be-u18-inference | by that; on that evidence | by that; from that; on that evidence | Evidence/inference frame, not an unrestricted source preposition.
be-u18-permission | by permission | by permission; with permission | Supplied permission expression.
becuman-occur-source | occur; come about | occur; come about | Of the calm in the source.
becuman-u15-source-sense | come upon; befall | come upon; befall | Retain the source's affected participant.
befeallan-u17-source-sense | fall in love | fall in love with | Supplied idiom makes lufu love the subject, its possessor the lover, and on + accusative the beloved.
beforan-before-motion | before; ahead of | before; ahead of | Person ahead of whom another goes; keep the assigned directional frame.
beforan-u13-positioning | before; in front of | before; in front of | Accusative landmark in the positioning construal; static dative can be a different valid construal.
began-u13-study | pursue; practise | pursue; practice; practise | Study is the thing pursued.
begyrdan-u16-source | gird; clothe | gird; clothe | Supplied participial clothing expression.
behealdan-u16-source | observe | observe; look at | Supplied source form observed.
belg-1 | bellows | bellows | Selected plural instrument use.
belimpan-u16-source | belong; relate | belong; relate to | Supplied participial construction.
ben-u11-source | prayer; petition | prayer; petition | Source dative plural after tō.
beran-produce | bear; produce | bear; produce; bear seed; bear fruit | Accusative produce; distinct from physical carrying.
beran-rich-source | rich in; productive of | rich in; productive of | Supplied berende on + dative ore expression; participial adjective.
bereafian-u18-selected | despoil; deprive of | despoil; deprive of; bereft of | Accusative person deprived, genitive thing lost; passive retains that genitive.
beseon-u16-source | look; turn one's gaze | look; turn one's gaze | Supplied source form and frame.
beseon-u18-reading | look toward | look toward | Target of the look follows the supplied phrase.
bethurfan-u18-selected | need; require | need; require | Genitive thing needed.
betweonan-u18-local-sense | between; to one another | between; to one another | Supplied reciprocal betwēonan him in 45.6.
betweox-among-source | among | among | Accusative in the exact supplied phrases; not a universal case rule.
bewaefan-u16-source | wrap; clothe | wrap; clothe | Supplied participial clothing expression.
biddan-beseech-person | beseech; entreat | beseech; entreat; pray | Accusative person; the requested action can be a ðæt clause.
biddan-u18-farewell | wish well; bid farewell | wish well; bid farewell | Supplied farewell formula.
biegan-u11-source | bend | bend | Supplied past bent; retain the source's unmarked ie in its actual form.
bletsian-bless-source | bless | bless | Supplied third-singular preterite; God is the understood subject.
blinnan-u11-source | cease | cease | Supplied wæs blinnende periphrasis.
blissian-u13-source | rejoice | rejoice | Source genitive plural present-participle use, of people rejoicing.
bradnes-1 | surface; face | surface; face | Of the deep in the assigned expression.
braedan-u14-source | spread; extend | spread; extend | Supplied source form spreads.
bufan-above | above | above | With dative landmark in the taught spatial frame.
butan-u13-without | without | without | With dative.
ceapian-u18-selected | trade; traffic | trade; traffic; buy | Traffic means trade; retain the supplied trading frame.
cirice-u13-source | oratory | oratory; place of prayer | Chad's separate place of prayer; distinct from the ordinary church sense.
cneo-u11-source | knee | knee | Supplied accusative plural knees.
cucu-alive-source | alive; living | alive; living | Supplied accusative neuter plural adjective.
cunnan-1 | know how; be able | know how; be able to | Learned skill; plain infinitive complement.
cunnan-u16-acquaintance | know; be acquainted with | know; be acquainted with | Accusative person known; distinct from learned ability.
cwethan-u13-saying-source | say | say | Source genitive plural present participle, of people saying.
cwethan-u15-source-sense | say | say | Supplied preterite said.
cwic-people | living people | living people; the living | Substantival adjective.
cyrenisc-of-cyrene | Cyrenian; of Cyrene | Cyrenian; of Cyrene | Geographical adjective.
cythan-announce | announce; make known | announce; make known; tell | Dative person informed; content is separate.
dead-people | dead people | dead people; the dead | Substantival adjective.
deorwierth-comp-1 | more precious | more precious | Comparative adjective; distinct from an adverb modifying an action.
diegelnes-u11-source | retreat; seclusion | retreat; seclusion | Supplied plural after of.
dom-1 | judgment | judgment; Day of Judgment | dōmes dæg means Day of Judgment.
dom-u16-judgment | judgment | judgment | A judgment made in judging, distinct from doom/fate.
don-beneficiary | do for; do to | do; do for; do to | Dative beneficiary/affected person; thing done is accusative when expressed.
don-u15-make | make; render | make; render | Accusative object with agreeing object predicate.
don-u16-cause | cause; bring about | cause; make it be that | dōn with the taught finite ðæt content/result frame.
don-u16-substitute | do | do; did | Replaces an action already mentioned; distinct from English dummy do.
don-u17-fulfil | fulfil; carry out | fulfil; fulfill; carry out | A word or command is fulfilled.
don-u18-deal-with | deal with; behave toward | deal with; behave toward | Assigned wið person frame; manner is separately expressed.
eac-also | also | also | Also in the combination ēac swilce.
eadmod-u17-humble-people | humble people; the lowly | humble people; the lowly | Substantival adjective.
eahta-1 | eight | eight | Cardinal 8.
eala-address-wish | O! | O | Interjection in address, exclamation or wish.
eald-superl-u18-local-sense | eldest; oldest | eldest; oldest | Substantival person/eldest brother in this source context.
eald-u17-elderly | old people; the elderly | old people; the elderly | Substantival adjective.
ealdor-chief-u14-component-source | chief; king | chief; king | This noun is distinct from the homonymous noun meaning life.
eall-completely-u12-source | completely | completely | Only in the fixed phrase mid ealle.
eall-u15-just | just; exactly | just; exactly | Degree emphasis in eall swā.
earfothrime-u15-source-sense | innumerable; hard to count | innumerable; hard to count | Assigned source adjective.
earm-u18-local-sense | the poor; the unfortunate | the poor; unfortunate people | Substantival adjective.
earnung-u15-source-sense | merit; good service | merit; good service | Source plural merits/services.
efne-behold | behold! | behold | Interjection, distinct from the verb behealdan look at.
eft-again-also | again; also | again; also | The source note also permits the additive sense.
egypta-u16-sense | Egyptians | Egyptians; Egypt | Egypta land denotes Egypt, literally land of the Egyptians; supplied name forms.
elpenbaenen-u17-local-sense | ivory; made of ivory | ivory; made of ivory | Adjective of material.
eltheodig-u16-reading | foreigners; strangers | foreigners; strangers | Substantival adjective.
endlefan-1 | eleven | eleven | Cardinal 11.
engle-1 | the English | English people; the English | People, distinct from the language/adjective.
englisc-language-u15-source-sense | English | English | Language noun.
eower-poss-1 | your; yours | your; yours | Plural possessors; inflection agrees with the possessed noun.
faec-u11-source | interval; while | interval; while | Noun in the supplied time expression.
faeder-1 | father | father | Includes the spiritual father relationship in the assigned prompts.
faesthafol-u15-source-sense | tenacious; withholding | tenacious; withholding | Genitive of what is held back in the source.
farne-u11-source | Farne | Farne | Island; supplied proper-name form after in.
feawe-u16-sense | few people | few; few people | Substantival use in the assigned expression.
fela-many | many; a large number of | many; a large number of | Genitive of the things counted in the taught frame.
feolan-1 | penetrate | penetrate | Preserve the supplied/taught lexical frame; not a synonym for every kind of entering.
feower-1 | four | four | Cardinal 4.
fierst-u11-source | period; interval | period; interval | Masculine noun in the source time expression.
fif-1 | five | five | Cardinal 5.
fisccynn-fish-kinds-source | kinds of fish | kinds of fish; fish kind | Supplied accusative neuter plural.
fleon-u11-source | flee | flee | Supplied third-plural present; distinct from flēogan fly.
folc-source | people | people | Collective singular.
folc-u17-peoples | peoples | peoples; nations | Distinct peoples or national groups; plural sense.
for-thon-the-because | because | because | Causal conjunction.
for-thon-the-u16-therefore | therefore; for that reason | therefore; for that reason | Adverbial consequence, distinct from because.
for-u11-source | for; for the sake of | for; for the sake of | Case follows each complete supplied accusative/dative expression.
for-u15-exchange | in exchange for | for; in exchange for | With dative.
for-u15-source-appeal | by; for the sake of | by; for the sake of | Grounds of entreaty in the prayer; keep the supplied phrase.
for-u15-source-cause | because of | because of | Dative hindering circumstance.
for-u15-source-why | why; for what reason | why; for what reason | In for hwȳ or for hwon.
for-u18-local-sense | instead of; in place of | instead of; in place of | Accusative in the supplied substitution frame.
forgiefan-u11-source | give; grant | give; grant | Supplied granted sense at Cook 143.18; not forgive here.
forgieldan-u15-pay | pay; repay; requite | pay; repay; requite; recompense | Dative recipient, accusative thing repaid in the selected frame.
forlaetan-u14-leave-to | leave to | leave; leave to | Thing left and recipient retain their taught roles.
forlaetan-u17-reading | set aside | set aside | Supplied source sense.
forth-forth-source | forth | forth; bring forth | Adverbial particle with the bringing/producing verb.
forthteon-u17-reading | present; perform | present; perform | Source performance sense; retain the actual form's spelling.
forwiernan-deny | deny; refuse | deny; refuse | Dative person denied, genitive thing denied.
fot-foot-source | foot | foot; feet | Supplied body-part form feet; distinct from the length-measure sense.
fram-1 | from | from | Separation, with dative in the taught frame.
fram-rest-from | from | from; rest from | Only the supplied rest-from-work construction.
fullfremman-finish | finish; complete | finish; complete | Supplied passive use.
fuluhtere-u16-sense | baptizer; Baptist | baptizer; Baptist | Baptist as John's title in the assigned passage.
furthor-u17-local-sense | further; any more | further; any more | Adverb in the supplied no-spirit-more expression.
gagates-u11-source | jet | jet | The stone; Latin loan-name in the source.
galnes-u15-source-sense | lust | lust | Assigned source sense.
gan-u13-gang-source | go | go | Supplied imperative gang.
gangan-u16-source | go; enter | go; enter | Supplied circumstantial participial phrase.
ge-paired-source | both … and | both … and | Paired ge … ge.
gebiddan-u11-source | pray | pray | Supplied wæs gebiddende, rendered prayed in this source.
gebrec-u11-source | crash; noise | crash; noise | Supplied accusative singular.
gebringan-u11-source | bring | bring | Supplied preterite with plural winds as subject; retain the prefix.
gedaelan-1 | divide; separate | divide; separate | Preserve the assigned separation frame.
gedon-do-make | do; make | do; make | Supplied passive fulfilment formula.
gedon-u15-source-arrangement | make; arrange | make; arrange | The present form/arrangement of the translation in the source.
gefeallan-u18-reading | fall in love | fall in love | Figurative falling of the heart; supplied idiom differs in prefix from befeallan in 42.1.
geferian-1 | carry; bear | carry; bear | Supplied passive movement; was carried/borne.
gefremman-1 | perform; accomplish | perform; accomplish | A work is the thing accomplished.
gefyllan-1 | finish; accomplish | finish; accomplish | A work is the thing completed; distinct from fill.
gegaderung-1 | gathering; collection; congregation | gathering; collection; congregation | Congregations of waters in the source.
gehieran-u11-source | hear | hear | Supplied prefixed third-singular preterite.
gehiersumian-u16-source | serve; obey | serve; obey | Supplied source form and government.
gehwa-each-reference | each one; everyone; everything | each one; everyone; everything | Personal gehwā and neuter gehwæt; the early reference status does not by itself establish production.
gelaeccan-u16-source | catch | catch | Supplied caught form.
geleornian-u17-reading | learn; master | learn; master | Learn a skill or performance in the source.
gelimpan-u11-source | happen; befall | happen; befall | Supplied preterite subjunctive in might befall us.
gelimpan-u14-source | happen; come about | happen; come about | Supplied preterite source form.
gemanigfieldan-multiply | be multiplied | be multiplied; multiply | Assigned passive with agreeing gemanigfield/gemanigfielde; no independent active causative frame is assigned.
gemengan-u16-source | join; mingle | join; mingle | Supplied source form.
gemengan-u17-reading | mix | mix; mingle | Mix sound with song in the supplied performance expression.
gemetan-u11-source | find | find | Supplied past participle gemētt in a passive.
gemiltsian-u14-pity | pity; have compassion on | pity; have compassion on; have mercy on | Dative person.
genealaecan-u16-source | approach | approach; draw near | Supplied source form approached.
genyhtsumian-u16-source | suffice; be sufficient for | suffice; be sufficient for | Complete supplied construction with dative beneficiary.
geond-u16-sense | along; through | along; through | With accusative.
geong-u18-local-sense | youngest | youngest | Supplied superlative use; not a new general gloss of positive geong.
geornfull-u13-source | occupied; intent | occupied; intent | Source mental-attention context.
geriman-u17-source-sense | number; count | number; count | Exact supplied infinitive gerīman; not an independently assigned full paradigm.
gesettan-1 | set; place | set; place | Supplied gesętte.
gesettan-u11-source | placed; situated | placed; situated | Supplied participial complement of understood us; not the identical-looking finite preterite.
gesettan-u18-appoint-lord | appoint as lord | appoint; appoint as; set as lord | Supplied frame with person appointed, tō + dative role, and dative people governed.
gesihth-u11-source | sight; gaze | sight; gaze | Supplied accusative singular.
geslean-u14-source | strike; smite | strike; smite | Supplied past/participial source form.
geslean-u16-source | strike | strike | Supplied source form struck.
gesmierwan-u16-source | anoint | anoint | Supplied source form anointed.
gesmyltan-u11-source | become calm | become calm; subside | Supplied preterite of the sea becoming calm.
gestandan-u14-source | assail; come upon | assail; come upon | Supplied source sense.
gestillan-cease-source | cease; become still | cease; become still | Intransitive in the source storm relative.
geswengan-u14-source | toss; shake | toss; shake | Supplied participial source use.
gesweotolian-u16-source | reveal; make clear | reveal; make clear | Supplied source form.
gesyndig-1 | favourable; fair | favorable; favourable; fair | Of winds.
getaecan-u16-source | show; direct | show; direct | Supplied source form.
gethraestan-u14-source | afflict; beat | afflict; beat | Supplied participial source use.
gewaegan-u14-source | buffet; shake | buffet; shake | Supplied participial source use.
geweald-dominion | control; rule; dominion | control; rule; dominion | Ordinary singular; on gewealde is the taught control phrase.
gewendan-u16-source | turn; change back | turn; change back | Supplied source form.
gewinn-u15-labour | labour; work | labor; labour; work | Noun, distinct from labour as a verb.
gewinna-u12-source | enemy; opponent | enemy; opponent | Supplied plural source forms.
gewitan-know-u16-source | find out; learn | find out; learn | Knowledge verb, distinct from gewītan depart.
gewitan-u17-decree-pass | pass away; cease to hold | pass; pass away; cease to hold | Of a decree.
gewyrcean-object-predicate | make; render | make; render | Accusative object with an agreeing predicate noun/adjective.
giefu-u18-local-sense | gift | gift; present | Supplied plural gifts.
gieman-1 | rule over | rule over | Genitive of what is ruled; no additional over preposition.
giernan-u17-selected | desire; request; woo | desire; request; ask for; woo; seek in marriage | Genitive desired thing/person in the selected frames, including the maiden wooed.
gif-if | if | if | Mood is determined by the open, tentative or counterfactual condition, not by gif alone.
glaed-u18-gracious | gracious; favourably disposed | gracious; favorably disposed; favourably disposed | With wið + person in the supplied gracious-toward frame.
god-1 | God | God | Proper divine name; no productive plural sense is assigned.
god-goods-1 | goods; property | goods; good things; property | Plural lexical noun.
god-goods-u18-local-sense | good; benefit; kindness | good; benefit; kindness | Nominal good in the repayment contrast.
god-u17-deity | god; deity | god; deity | Common deity sense, distinct from the proper divine name.
gretan-take-leave | greet; take leave of | greet; salute; take leave of; bid farewell | Accusative person/place; greeting and farewell depend on context.
gylt-u17-sense | debt | debt | Includes the prayer's moral debt.
habban-perfect | have | have; has; had | Auxiliary with transitive past participle for the taught completed-action/result construction.
haelend-1 | Saviour; Jesus | Saviour; Savior; Jesus | Proper title.
hal-u17-local-sense | hale; well | hale; well | Supplied greeting.
halig-u15-source-sense | holy ones; saints | saints; holy ones | Substantival adjective in the source.
ham-1 | home; homeward | home; homeward; homewards | Directional adverb; distinct from the noun home.
hand-1 | hand; side | hand; side | Side in right-/left-hand expressions.
hatan-u15-be-called | be called; be named | be called; be named; hight | Special hātte form in the assigned naming expression.
he-1 | he; she; it; they | he; she; it; they; him; her; them | Personal pronoun; gender/number and governed case determine the selected form and reference.
he-possessor | his; her; its; their | his; her; its; their | Invariant genitive possessors, unlike agreeing possessive adjectives.
he-u15-source-sense | their | their | Source genitive possessor.
heah-adverb-u14-source | high | high | Adverbial height, distinct from an agreeing adjective.
heah-u14-exalted-source | high in rank; exalted | high; exalted | Rank/status sense in the supplied source.
heah-u15-highest-title | the Highest | Highest; the Highest | Divine title.
healt-u16-sense | lame; halt | lame; halt | Adjective describing impaired walking; not the command halt/stop.
hearpian-u17-source-sense | harp | harp; play the harp | Supplied genitive harper/harping construction, with instrument; do not reconstruct it from the infinitive alone.
heofone-1 | heaven; sky | heaven; sky | Weak feminine lexical alternative in the source.
heofonlice-u11-source | from heaven; heavenly | from heaven; heavenly | Source expression at Cook 143.17.
herian-u13-praising-source | praise | praise | Genitive plural present-participle use, of people praising.
herian-u16-source | praise | praise | Supplied source form praised.
hider-source | hither; here | hither; here | Motion toward the speaker, distinct from location hēr.
hieran-perceive-action | hear an action | hear; hear someone do something | Accusative perceived actor plus plain infinitive in the taught perception construction.
hiw-kind-source | form; kind | form; kind | Supplied dative neuter plural.
hlaest-source | wares; merchandise; cargo | wares; merchandise; cargo | Selected plural source use.
hlifian-u14-source | tower | tower | Verb meaning stand/tower high in the source; distinct from noun tower.
horn-u17-sense | horn; strength; dignity | horn; strength; dignity | Strength/dignity is the figurative force in 37.14, not a replacement for the literal source horn.
hreosan-u14-source | fall | fall | Supplied present participle falling.
hund-hundred-source | hundred | hundred | Only the complete supplied hundred-sheep expression at its first appearance; later numerical frames remain locally specified.
hundteontig-u15-source-sense | a hundredfold | hundredfold; a hundredfold | A hundred in return, in the supplied recompense expression.
hundteontig-u17-supplied | hundred | hundred | Within the complete supplied 144,000 expression; do not infer an independent high-number system.
hungrig-people | hungry people | hungry people; the hungry | Substantival adjective.
hwa-interrogative | who? what? | who; whom; whose; what | Case follows role/government; distinguish personal and neuter reference.
hwa-u15-source-why | what reason | why; what reason | Instrumental hwon in the supplied why expressions.
hwaether-u15-free-choice | whichever of two | whichever of two | In swā hwæðer swā; the supplied attraction example has a special case arrangement.
hwaethwega-u13-source | something | something | Supplied local indefinite form; no unrestricted new paradigm.
hwaethwugu-u13-source | something | something; something of that sort | Supplied hwæthwugu swilces.
hwilc-partitive | which | which; which of | Selection from a group expressed in genitive.
hwilc-u13-any | any; some | any; some | Indefinite adjective, distinct from an interrogative.
hwilum-u18-earlier-time | a while ago | a while ago; formerly | Only in supplied hwīlum ǣr; earlier hwīlum sometimes is not enough.
hwonne-when | when? | when | Direct interrogative.
hyngran-hunger | be hungry | be hungry; hunger | Impersonal construction with accusative experiencer.
hyngran-u17-hungry-participle | hungry; hungering | hungry; hungering | Present participle used substantivally in the assigned frame.
ic-genitive-attributive-source | our | our | Personal genitive plural used attributively in the exact ūre hǣle expression.
ic-genitive-citation | of me; of us | of me; of us | Personal genitive citation forms identifying person/number; this record alone does not teach an attributive possessive use.
ic-personal | I; me; we; us | I; me; we; us; we two; us two | Singular, dual and plural personal forms; select governed case.
ic-u15-partitive-dual | of us two | of us two | Personal genitive dual after a selection word.
idel-u15-idle | idle | idle; not working | Distinct from empty/void.
in-u11-source | in; on | in; on | With dative in the exact locations/circumstances.
in-u13-directed-source | toward; onto | toward; towards; onto | Supplied phrase directing the mind toward these things.
in-u13-inward-source | in; inward | in; inward | Adverbial direction.
incer-poss-1 | your; yours | your; yours | Two possessors; agreeing possessive.
ingan-u16-source | enter; go in | enter; go in | Supplied past source form.
ingangan-u13-source | enter; go in | enter; go in | Supplied present-participle phrase.
intinga-u11-source | cause; sake | cause; sake; for the sake of | Within supplied for intingan expressions.
isern-1 | iron | iron | Metal noun.
israelites-name-u17-local-sense | Israelites | Israelites | Supplied genitive plural name form.
jews-name-u17-local-sense | Jews | Jews | Supplied genitive plural name form.
laedan-u13-bring | lead; bring; take | lead; bring; take | A person is the object in the assigned frame.
laedan-u16-carry | carry; take | carry; take | A person is conveyed in this supplied frame.
laeden-u15-source-sense | Latin | Latin | The language.
lang-u11-source | long | long | Adjective agreeing with the time interval fæc.
lange-source | long | long; as long as | In supplied swā lange swā; its biblical inasmuch-as force is explained locally.
lazarus-u14-source | Lazarus | Lazarus; Lazaruses | The parable's poor man; supplied plural denotes people like him.
lead-1 | lead | lead | Metal noun, not the verb lead.
lecgean-place-source | lay; place | lay; place; set | Supplied source form.
leof-comp-preferable | preferable; dearer | preferable; prefer; had rather; would rather | Dative experiencer + is lēofre + infinitive in the taught preference frame.
leof-u18-sir-address | sir | sir | Supplied respectful address lēof.
leoht-count-luminary | light; luminary | light; a light; luminary | Individual countable light, distinct from mass light.
libban-u16-source | living | living; alive | Supplied weak participial adjective.
licgan-u14-source | lie; be lying | lie; be lying | Supplied participle describing the possessed persons, not a habban perfect.
lieg-u14-source | thunderbolt; lightning | thunderbolt; lightning; levin | Source levin sense.
lif-lived-life | life | life; lives | An individual's lived life, including cognate accusative with libban.
lystan-u15-source-sense | please; be desired | please; desire | Impersonal source expression; keep the complete supplied frame.
lytel-superl-u15-rank | least | least | In rank or importance.
ma-1 | more | more | Adverb of amount.
ma-again | more; again | more; again; never more | In the negative phrase never more/never again.
ma-more-numerous | more | more | More in number, distinct from degree or greater value.
maegen-u17-power | power; strength | power; strength; heavenly powers | Heavenly powers in 37.2 is the contextual plural use.
maere-u15-great | great; renowned | great; renowned | Distinct from simple physical size where the task requires the renowned sense.
magan-u16-source | be able; could | can; could; might; be able to | Supplied modal form; ordinary capability, not permission.
mann-u11-source | one; people in general | one; people in general | Impersonal man with singular finite verb.
micel-comp-1 | greater; larger | greater; larger | Comparative adjective.
micel-comp-greater-worth | greater; more important | greater; more; more important | Value/importance in the life/raiment comparison.
micel-comp-u15-amount | more; a greater amount | more; greater amount | Nominal/attributive quantity, distinct from more in number.
micel-superl-1 | greatest; largest | greatest; largest | Superlative adjective.
micel-u15-amount | much; an amount | much; amount | Quantity sense.
micel-u17-loud | great; loud | great; loud | Loud is the contextual force with a voice.
mid-circumstance-source | with | with | Circumstances of risk or loss in the supplied phrase.
mid-completely-u12-source | completely | completely | Only in fixed mid ealle.
mid-manner-source | with | with; with compassion | Manner in the supplied compassion phrase.
mid-u13-along-source | with; along with | with; along with | Supplied mid wes, be with them.
mid-u13-clothing | with | with; clothed with | Dative garment in the assigned clothing frame.
mid-u13-interlocutor | with | with; speak with | Dative conversational partner.
mid-u13-manner-source | with | with | Accompanying quality or mental disposition in the source.
mid-u14-adornment | with | with; adorned with | Material or clothing in the supplied adornment phrase.
mid-u16-source-clothing | with | with; clothed with; wrapped with | Exact cloth/cloak complements of begyrd and bewǣfed.
mid-victory-u12-source | with | with; with victory | Manner/circumstance of victory.
middes-u18-local-sense | at noon | noon; at noon; midday | Whole supplied tō middes dæges, with genitives.
miht-u14-powers-source | powers; powerful people | powers; powerful people | Those holding high station in the source's concluding human application.
mihtig-u17-powerful-people | the powerful; the mighty | the powerful; the mighty | Substantival adjective.
monath-u17-local-sense | month | month | Source plural months.
myngian-u16-source | admonish; prompt | admonish; prompt | Supplied participial source use.
na-u15-constituent | not | not | Negates a contrasted constituent, distinct from finite ne.
nacod-people | naked people | naked people; the naked | Substantival adjective.
naeddre-u11-source | snake; adder | snake; adder | Supplied weak feminine plural.
nagan-local | not have; not possess | not have; not possess | Negative possessive verb in its supplied forms.
niehst-u12-source | at length | at length | Whole supplied æt nīehstan.
nieten-1 | animal; beast; cattle | animal; beast; cattle | Cattle is the selected plural use; retain the early task distinction from dēor.
nigon-1 | nine | nine | Cardinal 9.
nytan-u16-source | not know | not know | Supplied negative knowing form.
of-u11-source | from; out of | from; out of | With dative.
of-u15-source-correspondence | sense for sense | sense for sense | Literal correspondence in the supplied translation expression.
of-u15-source-partitive | of; from | of; from; one of | Portion from a whole in the supplied partitive phrases; dative whole.
of-u16-old-age | from | from | Starting condition of old age in the supplied rejuvenation comparison.
of-u17-begetting | of; from | of; from; begotten of | Origin of wisdom in the supplied begetting statement.
of-u17-generation-range | from | from; from generation to generation | Starting generation in the supplied temporal range.
ofer-1 | over; across | over; across; above | Spatial frame; case varies with the specific construction. Do not impose a universal motion rule.
ofer-authority | over | over; have dominion over | Accusative dependent in the taught authority frame.
ofer-u15-rank | above | above | Rank, with accusative.
ofer-u15-toward | toward | toward; kind toward | In gōd ofer + accusative people.
ofer-u16-rejoicing | over; about | over; about; rejoice over | Object of rejoicing, with the assigned accusative frame.
ofer-u17-rank-dative | above | above | Rank, with explicitly supplied dative complement; retain this limit.
ofer-u18-preference | above; more than | above; more than | Preference in the supplied comparison.
ofthyncean-u18-selected | grieve; displease | grieve; displease | Impersonal third singular with dative experiencer and a content clause.
on-1 | in; on | in; on | Dative for the taught ordinary location construction.
on-according-form-source | according to | according to; in forms of | Only the supplied classificatory expression with hīw.
on-adverb-u16-sense | on | on; have on | Adverb in the cloak-wearing relative clause.
on-alive-source | alive | alive | Only in supplied on līfe.
on-control | in one's control | in control; under one's control | on + dative possessed geweald.
on-divided-into-two-source | into; in two | into; in two | Supplied division expression.
on-glory-source | in | in; in glory | Supported expression in his majesty/glory.
on-in-name | in one's name | in one's name | Assigned name phrase.
on-into-goal | into; onto | into; onto | Accusative goal of placement in the taught frame.
on-placement-side-source | at one's side | at one's side; at the right side; at the left side | Accusative hand in the bounded placement expression.
on-respect | in; with respect to | in; with respect to | Quality or domain of description.
on-rich-source | rich in | rich in | Only in supplied berende on + dative.
on-side-idiom | on one's side | on the right side; on the left side | Supplied side expression; preserve its local case.
on-storm-circumstance | in | in; in a storm | Supplied circumstance of the storm.
on-time-supplied | in the beginning | in the beginning | Whole supplied on anginne.
on-u14-belief | in | in; believe in; trust in | Accusative person believed/trusted in.
on-u14-lifetime-source | during; in | during; in one's life | Supplied lifetime expression.
on-u14-people-domain-source | among; in | among; in | Dative people among whom friends are obtained.
on-u15-source-circumstance | in | in; in the heat | Circumstance of the day's heat in the supplied source.
on-u15-source-during | during | during; in | Dative time expression.
on-u15-source-worldly-life | in worldly life | in worldly life | Supplied temporal/situational expression.
on-u16-at-work | at work; engaged in | at work; engaged in | Only the exact supplied activity phrases.
on-u16-clothing | in; wearing | in; wearing | Supplied on scēapa gegierelum, in sheep's garments.
on-u16-fishing | fishing | fishing; go fishing | Supplied on fiscnoð after gān.
on-u17-chanced-domain | upon; into | upon; into; chance upon | Supplied chancing-upon idiom.
on-u17-generation-range | to | to; from generation to generation | Succeeding generation in the supplied temporal range.
on-u17-love-goal | upon | upon; fall in love with | Accusative beloved in the supplied love-falls-upon idiom.
on-u17-rejoicing | in | in; rejoice in | Source/object of joy in the supplied frame.
on-u18-morning | in the morning | in the morning | Whole supplied on morgen; accusative singular.
on-u18-selling-goal | into | into; sell into | Destination of sale in the supplied expression.
on-unrest-u12-source | in; amid | in; amid | Circumstances of the stated unrest.
oncnawan-u16-source | recognize; perceive | recognize; perceive | Supplied past source form.
onfon-u17-person | receive; accept | receive; accept | A person received into care in the supplied frame.
ongean-u18-local-sense | by the time that | against that; by the time that; in readiness for | Complete supplied ongēan ðætte clause.
ongietan-u11-source | understand; perceive | understand; perceive | Supplied infinitive after a modal.
onginnan-u12-source | begin | begin | Supplied preterite began.
onginnan-u17-reading | begin | begin | Supplied playing/praising action as complement.
ontynan-u13-source | open | open | Supplied preterite opened.
ora-u11-source | ore; vein of metal | ore; vein of metal | Supplied dative plural after on.
oth-u13-until | up to; until | up to; until | With accusative.
other-u14-rest-source | remaining; the rest | remaining; the rest | The rest of the forest/earth in the source.
pentapolis-place | Pentapolis | Pentapolis | Cyrenian region in this story.
piht-u12-source | Picts | Picts | Supplied people-name forms.
plegian-u17-reading | act; perform | act; perform | Performance context; ordinary play is a separate assigned sense.
pund-u17-sense | pound | pound | Weight measure in the supplied gold quantity.
rice-adjective-u17-sense | rich; wealthy | rich; wealthy; rich people; the rich | Includes substantival rich people in the assigned frame.
ricsian-dominion | rule; have dominion | rule; bear rule; have dominion | Used absolutely in the taught frame; no new object government.
rihtlice-u15-source-sense | more correctly | correctly; more correctly | Supplied comparative adverb.
rihtwis-people | righteous people | righteous people; the righteous | Substantival adjective.
rinan-u14-source | rain | rain | Supplied impersonal source clause with past rīnde.
saed-u17-descendants | seed; descendants | seed; offspring; descendants | Collective descendants, distinct from literal seed.
sanctus-latin-u15-source-sense | Saint; holy | Saint; holy | Latin word in the source title.
scrydan-u17-reading | dress oneself | dress oneself | Supplied reflexive use.
sculan-u13-interpretive-source | should; be to | should; be to | Supplied question about what events were to mean; retain its reported/interpretive force.
sculan-u18-future-ellipsis | shall; be yet to come | shall; be yet to come | Supplied gīet sculon fīf, with be explicitly omitted.
se-relative | who; which; that | who; whom; whose; which; that | Inflected relative; case follows its clause role.
se-the-u11-source | which; that | which; that | Supplied se-ðe relative complex referring to the storm.
se-those-waters-substantival | those | those | Supplied substantival dative plural referring to waters.
se-u11-source | so that | so that | Only in supplied tō ðon ðætte result connection.
se-u13-after-that | after that | after that | Only in temporal æfter ðon.
se-u17-degree-marker | so; to that degree | so; to that degree | Only in supplied tō ðan … ðæt.
secgan-u15-source-sense | say | say | Supplied source preterite.
secgan-u17-call | call; declare to be | call; declare to be | Object with the stated agreeing predicate.
self-emphatic-reflexive | self; the same person | self; myself; yourself; himself; herself; ourselves; yourselves; themselves | Agreeing emphatic/reflexive self; ordinary reflexive personal pronouns do not always require it.
sellan-give-drink | give to drink | give to drink | Supplied dative person + plain drincan, without tō.
seolfor-1 | silver | silver | Metal noun.
seolfren-u18-local-sense | silver; made of silver | silver; made of silver | Material adjective, distinct from the noun seolfor.
seofon-1 | seven | seven | Cardinal 7.
settan-u17-establish | appoint; establish | appoint; establish; make a decree | With accusative entity/decree in the assigned frame.
siex-1 | six | six | Cardinal 6.
siextig-sixty-source | sixty | sixty | Within the supplied 365-days expression.
singan-u13-singing-source | sing | sing | Source genitive plural present participle, of people singing.
siththan-u16-sense | since; after; afterwards | since; after; afterwards | Conjunction since/after versus adverb afterwards.
slean-absolute-strike | strike; smite | strike; smite | Objectless striking in the assigned hammer sentences.
slean-u13-signal | make a signal | signal; make a signal | Only in supplied slōg tācen.
slean-u16-source | strike | strike | Supplied past source form.
smeagan-u13-source | ponder; consider | ponder; consider | Supplied preterite source form.
smylte-superl-u11-source | very calm; calmest | very calm; calmest | Supplied superlative adjective describing the sea.
sona-as-soon-source | as soon as | as soon as | In sōna swā.
sothlice-1 | now; but | now; but; for its part | Discourse connective corresponding to source Latin autem, distinct from truly.
standan-stand | oppose; stand against | oppose; stand against | Supplied standan ongēan frame, distinct from simple stand.
stanen-u17-local-sense | stone; made of stone | stone; made of stone | Material adjective.
stilnes-u11-source | stillness; calm | stillness; calm | Supplied genitive singular.
strang-u11-source | strong | strong | Masculine singular predicate in the source.
strang-u14-attributive-source | strong | strong | Attributive adjective with wind in the source.
straet-public-place-u15 | public place | public place | Street used as a gathering place in the assigned prompt.
sum-partitive | some | some; some of | Members selected from a group; genitive whole.
suthan-u17-local-sense | in the south; from the south | south; in the south; from the south | Retain the supplied spatial expression.
swa-as-correlative-source | as | as; as soon as | Only in sōna swā.
swa-as-long-as-source | as long as; inasmuch as | as long as; inasmuch as | Whole swā lange swā phrase; the assigned biblical expression need not imply duration.
swa-equative-degree | as | as; as … as | First degree-marker in equal comparison.
swa-equative-standard | as | as; as … as | Introduces the comparison standard.
swa-predicative-as | as; like | as; like | Predicative comparison.
swa-swa-u13-approximately | about; approximately | about; approximately | Approximation in the supplied source expression.
swa-u14-proportional-source | the … the | the … the; the more … the more | Proportional comparison, not the definite article.
swa-u15-free-choice | whoever; whatever | whoever; whosoever; whomsoever; whatever; whatsoever; whichever | swā hwā/hwæt/hwæðer swā; the internal pronoun's case and type must fit the clause.
sweotole-u15-source-sense | most clearly | clearly; most clearly | Supplied superlative adverb.
swigian-u17-reading | be silent | be silent; keep silent | Supplied source sense.
swilce-likewise | likewise | likewise | Adverb, distinct from inflected swilc such.
swilce-u16-as-if | as if | as if | Supplied apparent-rejuvenation comparison.
swingan-u16-source | swing; brandish | swing; brandish | Supplied past source form.
swithe-u15-preference | rather; more | rather; more | Preferential comparative swīðor.
swithe-u16-degree | more | more | Comparative degree of an action/feeling, not a count of objects.
swithlice-u14-source | more violently; more severely | more violently; more severely | Supplied comparative adverb.
swithra-1 | right | right; right-hand side | Right-hand/side expression, distinct from stronger.
swithra-u14-stronger-source | stronger; fiercer | stronger; fiercer | Comparative degree, distinct from right-side sense.
tabele-u17-sense | tablet; table | tablet; table of the law | Tables of the law, not an unrestricted furniture meaning.
teon-bring-forth-source | bring forth; produce | bring forth; produce | Supplied third-plural present subjunctive, with waters as subject.
tha-hwaethre-u14-source | nevertheless; yet | nevertheless; yet | Whole supplied connective.
thaes-the-u12-source | as soon as | as soon as | Complete source construction with sōna.
thaes-the-u16-as-seems | as | as; as it seems | Only in supplied ðæs-ðe mē ðyncð.
thaet-conjunction-1 | that | that | Content conjunction, distinct from demonstrative/relative that.
thaet-conjunction-u11-source | that; so that | that; so that | Supplied expanded spelling; distinguish content from result by the source clause.
thaet-purpose | so that; in order that | so that; in order that | Purpose conjunction with the assigned subjunctive construction.
thaet-result | that; so that | that; so that | Asserted result, distinct from intended purpose.
thaet-u16-uncertain-link | that | that | Cook leaves the source linkage uncertain; do not impose one content/result classification.
the-relative-subject-waters | which; that | which; that | Subject-relative referring to the waters.
the-u15-after-clause-source | after | after | Only as the clause marker in the whole supplied æfter ðǣm ðe expression.
theah-u15-source-nevertheless | nevertheless; yet | nevertheless; yet | Independent adverb, distinct from concessive conjunction although.
thearf-u15-source-sense | benefit; good; need | benefit; good; need | Source contextual nouns; retain the local expression.
thencan-u13-source | think | think | Supplied source preterite.
thenian-u16-source | serve; attend | serve; attend | Supplied preterite source form.
theow-servant-phrase-u18-local-sense | enslaved men; servants | enslaved men; servants | Whole supplied phrase ðēowa manna.
theow-u16-reading | the unfree; enslaved people | unfree; enslaved people | Substantival adjective in the source comparison.
thin-poss-1 | your; yours | your; yours; thy; thine | One possessor; agrees with the possessed noun.
thing-1 | thing | thing; things | Ordinary singular/plural noun.
thing-matters | thing; fact; matter | thing; fact; matter | Matter known/discussed, distinct from a generic physical object.
thonne-then-source | then | then | Sequence of future judgment events.
thu-genitive-citation | of you | of you | Personal genitive citation identifying singular/dual/plural; not by itself an attributive possessive lesson.
thu-personal | you | you; thou; thee; ye; you two | Personal singular/dual/plural and governed cases; dual subjects take plural verb forms.
thurh-u15-oath | by | by; swear by; conjure by | Accusative oath standard.
thurh-u16-means | through; by means of | through; by means of; by what | Supplied service/evidence expressions, including Ðurh hwæt.
thusend-local | thousand | thousand | Within the complete supplied high-number expression.
thyncan-seem-nominative | seem | seem; seem good to | Nominative thing that seems, dative experiencer and agreeing predicate.
thyncan-u16-source | seem | seem | Supplied past source form.
tid-hour-u13-source | hour | hour | Time measure in the supplied intervals.
tien-1 | ten | ten | Cardinal 10.
to-aid-protection-u12-source | for aid; for protection | for aid; for protection | Whole supplied purpose expressions.
to-at-prayer-source | at; in response to | at; in response to | Only the exact at-the-prayers expression.
to-death-result | to | to; to death | Endpoint/result death.
to-directed-prayer-source | to; toward | to; toward | Person to whom knees/prayer are directed in the supplied phrase.
to-function-purpose | for; to serve as | for; for food; for a sign | tō + dative function; a separate dative beneficiary may accompany it.
to-inflected-infinitive | to; in order to | to; in order to | With the inflected infinitive; ordinary modal complements use a plain infinitive.
to-result-connective-source | so that | so that | Only in supplied tō ðon ðætte result connection.
to-u13-addressee-source | to | to; say to | Postposed in the supplied cwæð him tō speech phrase.
to-u13-at-root-source | at; to | at; to; at the root of | Bounded supplied root expression with genitive dependent and dative root.
to-u14-result-source | to; into | to; into; come to nothing | Result in supplied tō lore, tō sorge or tō nāhte.
to-u14-speech-addressee-source | to | to; say to | The person addressed in speech.
to-u15-source-conformity | in accordance with | in accordance with | A will as the goal of guidance in the supplied prayer.
to-u15-source-directed-conduct | toward | toward; towards | Conduct toward a person in the supplied expression.
to-u15-source-eternity | for ever | for ever; forever | Whole fixed tō worulde.
to-u15-source-translation-result | into; to | into; to; translate into | Resulting language/literary form.
to-u15-source-why | why; for what purpose | why; for what purpose | Only in tō hwon.
to-u16-belonging | to | to; belong to | Complement of belonging in the supplied frame.
to-u16-body-care | for | for; water for the feet | Care of a body part in the supplied expression.
to-u16-rejuvenation | to | to; to youth | Resulting condition of youth in the supplied comparison.
to-u16-wife-role | as wife | as wife; to wife | Only the supplied tō wīfe role phrase.
to-u17-degree-result | so; to that degree | so; to that degree | Whole supplied tō ðan … ðæt result construction.
todaelan-1 | separate; distinguish | separate; distinguish | Source forms tōdǣlen/tōdǣlden are retained; no silently invented citation spelling.
tomiddes-midst | in the midst of | in the midst of | With dative landmark.
top-u16-reading | ball? | ball | Tentative source interpretation; retain the question mark and uncertainty.
torr-u14-crag-source | crag | crag | Probable contextual sense in Cook's note, distinct from earlier tower.
toslitan-tear-source | tear | tear; tear apart | Supplied past source form.
totwaeman-separate | divide; separate | divide; separate | Waters divided from waters in the supplied frame.
totwaeman-separate-beings | separate | separate | Beings separated in the assigned frame.
toweorpan-u15-break | break; overthrow | break; overthrow | Break a commandment in the assigned use.
twegen-divided-in-two-source | two; in two | two; in two | Two parts in the supplied division expression.
twelf-1 | twelve | twelve | Cardinal 12.
unaethele-u16-reading | people not noble | people not noble; the unnoble | Substantival adjective in the supplied contrast.
uncer-poss-1 | our; ours | our; ours | Two possessors; agreeing possessive.
under-below | under | under; below | Dative landmark in the taught static frame.
under-u13-direction | under | under | Directional accusative in the assigned entry-under-the-roof frame.
undertheodan-u13-added-source | add; subjoin | add; subjoin | Supplied passive/participial addition to speech.
unrim-u17-local-sense | abundance; uncounted quantity | abundance; quantity; uncounted quantity | Supplied quantity with genitive of the substance.
unscrydan-u16-source | undress; take off | undress; take off | Supplied source form; retain its object/reflexive roles.
unrihtwis-people | unrighteous people | unrighteous people; the unrighteous | Substantival adjective.
untrum-people | sick people | sick people; the sick | Substantival adjective.
up-ahebban-lift-source | lift up | lift up; raise | Supplied source form.
up-ahebban-u11-source | lift up | lift up; raise | Supplied first-plural preterite.
upgan-go-up | go up; come up | go up; come up | From the water in the supplied expression.
ure-poss-1 | our; ours | our; ours | Plural possessors; agreeing possessive.
utgan-u16-source | go out | go out | Supplied past source form.
utgangan-u11-source | come out | come out | Supplied present participle; source permits its interpretation with earlier action.
wafian-u13-source | be amazed | be amazed; be in astonishment | Supplied source form.
weallan-u11-source | surge; boil | surge; boil | Supplied present participle used adjectivally of the sea.
wecg-u11-source | metal; ingot | metal; ingot | Supplied genitive plural dependent on veins.
weg-u14-access-source | way; means of access | way; means of access | Figurative access to the Father in the declaration; distinct from physical road.
wen-u16-sense | expectation; chance | expectation; chance; perhaps | wēn is ðæt + subjunctive supplies the taught perhaps construction.
wendan-u16-source | turn; return | turn; return | Supplied source form.
weorthan-1 | become; be | become; be | Auxiliary of the assigned passive event with a past participle.
weorthan-u17-reading | come about; result | come about; result | Supplied resultative expression.
wepan-u12-source | weeping; tearful | weeping; tearful | Supplied participial/adjectival use.
wer-u11-source | man | man | Supplied genitive singular.
wesan-be | be | be; am; is; are; was; were | Copular present/past identification or state; other auxiliary constructions are separate senses.
wesan-intransitive-perfect | be | be; have come; had come | Auxiliary with intransitive past participle in the specified compound constructions.
wesan-passive | be | be; be done | Passive auxiliary with the assigned participle.
wesan-present-participle | be | be; be doing | Auxiliary with a present participle in the supplied construction; not a universal English-progressive equivalent.
wesan-u15-source-sense | be | be; are | Supplied plural present copula.
wesan-u16-impersonal-seemed | seem | seem | Only in the supplied impersonal expression it seemed to the king.
wesan-u17-reading | not be | not be | Supplied negative nǣre in reported supposition.
wesan-u18-anterior-counterfactual | would have come | would have come | Supplied past-subjunctive wesan + cumen in the counterfactual result.
willan-purpose-source | might | might | Only in the exact supplied purpose construction with watching/seeing infinitives.
willan-refuse | be unwilling; refuse | be unwilling; refuse | With ne or a licensed negative contraction; followed by plain infinitive.
winstre-source | left | left; left-hand side | Supplied side phrase.
wis-wise-man-source | wise man; wise one | wise man; wise one | Substantival direct address.
witan-content | know | know; know that; know whether | A stated fact or the answer to a question as complement.
witan-u16-person | know | know; know a person | Person as object in the specifically taught frame; distinguish cunnan's acquaintance uses.
with-u13-proximity | by; beside; at | by; beside; at | Accusative landmark in the taught proximity phrase.
with-u15-exchange | in return for | for; in return for; in exchange for | With dative; distinct from opponent/hostility.
with-u16-players | with; against | with; against; play with | Dative fellow players in the exact supplied playing frame.
with-u17-conversation | with | with; have speech with | Supplied conversational counterpart; do not infer hostility.
witodlice-source | now; and | now; and | Discourse connective.
wlanc-u15-source-sense | proud; wealthy | proud; wealthy; rich | Contextually the rich man addressed.
wudu-u14-source | wood; forest | wood; forest | Collective vegetation, not a new material sense.
wundrian-u13-source | wonder | wonder; be wondering | Supplied source form.
wyrcean-make | make; build | make; build | Supplied unprefixed form; preserve explicit task controls.
wyrcean-yield | yield; produce | yield; produce fruit | Accusative fruit in the taught/source expression.
wyrhta-u15-source-maker | Maker; Creator | Maker; Creator | Divine title, distinct from ordinary workman.
yfel-u15-noun-evil-source | evil | evil | Substantive noun in fram yfele.
yfel-u15-substantive | evil; evil people | evil; evil people; the evil | Substantival adjective in the assigned use.
ymbe-u15-about-time | about | about | Approximate time, with accusative.
ymbhwyrft-u13-source | circuit | circuit; round about; all around | Whole on ymbhwyrfte expression means all around; supplied dependent landmark.
ymbsellan-u13-source | surround; envelop | surround; envelop | Supplied source form.
ymbsellan-u14-source | surround; beset | surround; beset | Supplied source form.
ymbsittan-u17-reading | sit around | sit around | Supplied participle referring to people sitting around.
yth-u11-source | wave | wave | Supplied dative plural after fram.
'''

overrides={}
for line in OVERRIDES.strip().splitlines():
    sid,gloss,labels,qualifier=[s.strip() for s in line.split('|')]
    assert sid not in overrides,sid
    overrides[sid]={'display_gloss':gloss,'english_lookup_labels':[s.strip() for s in labels.split(';')],'usage_qualifier':qualifier}

# A second pass against the accepted lexical-frame audits supplies government
# and removes the remaining contextual descriptions from the lookup label.
REFINEMENTS=r'''
abutan-around | around; about | around; about | With accusative.
aceorfan-u16 | cut off | cut off | Accusative thing cut; of in the assigned expression is a separate off particle.
adrifan-expel | drive out; expel | drive out; expel | Accusative person expelled; fram + dative may mark the point of separation.
aefter-u16-follow | after; following | after; follow | Dative person followed, including motion after that person.
aeswician-u16 | offend; cause to stumble | offend; cause to stumble | Accusative person; ethical/metaphorical offence in the assigned use.
afedan-1 | support; nourish | support; nourish | Accusative person supported.
aliehtan-1 | illuminate; give light to | illuminate; give light to | Accusative person or thing illuminated.
andswarian-answer | answer; reply | answer; reply | Dative addressee; the reply may be given as direct speech.
ascian-u13 | ask about | ask; ask about | Accusative person asked, genitive matter asked about; an indirect question may express the matter.
astigan-source | go aboard; board | go aboard; board | Accusative ship boarded in the assigned frame.
baethstede-u16-reading | bathing place; gymnasium | bathing place; gymnasium | Gymnasium is the contextual interpretation in the supplied reading.
beatan-1 | beat; strike | beat; strike | Accusative person or thing struck.
bebeodan-u13 | command; instruct | command; instruct | Dative addressee and a ðæt clause with subjunctive for the commanded action.
beforan-before-motion | before; ahead of | before; ahead of | Dative person, including going or sending ahead of that person.
beforan-before-source | before; in front of | before; in front of | Dative landmark in the static frame.
began-1 | ply; practise | ply; practise; practice | Accusative trade or occupation.
beheafdian-u16 | behead | behead | Accusative person beheaded.
behealdan-u13 | behold; look at | behold; look at | Accusative object seen.
beran-1 | carry | carry; bear | Accusative person or thing carried.
bewendan-u16 | turn | turn | The assigned reflexive frame uses dative him and tō + dative goal.
biddan-1 | ask; request | ask; request | Genitive thing requested; an accusative person may be added.
bindan-1 | bind; tie | bind; tie | Accusative person or thing bound.
blawan-1 | blow | blow | Intransitive in the assigned bellows sentence.
blissian-u16 | rejoice | rejoice | Intransitive; mid + dative companion or ofer + accusative cause of joy in the assigned frames.
bringan-1 | bring | bring | Accusative thing or person brought; tō + dative destination/person, or the assigned bare dative recipient.
butan-besides | besides; apart from | besides; apart from | Dative excluded person or thing.
bycgan-source | buy | buy | Accusative goods bought.
ceosan-1 | choose | choose | Accusative person or thing chosen.
ciepan-source | sell | sell | Accusative goods sold.
cleopian-u15-call | call; summon | call; summon | Accusative person summoned; distinguish intransitive cry aloud.
cleopian-u16-cry | cry aloud | cry; cry aloud | Intransitive, with the words cried given as direct speech.
cythan-announce | announce; make known | announce; make known | Dative person informed; accusative thing announced or a ðæt content clause.
dene-1 | Danes | Danes; the Danes | Plural people-name.
don-put | put; place | put; place | Accusative object; on + accusative goal in the assigned frame.
don-u16-cause | cause; bring about | cause; bring about | With a finite ðæt clause; its actor is nominative within that clause.
drifan-1 | drive | drive | Accusative person or thing driven.
drincan-1 | drink | drink | Accusative liquid drunk.
eall-substantive | all people; everything | all; all people; everything | Substantival: plural for people, neuter singular for everything.
ehtan-persecute | pursue; persecute | pursue; persecute | Accusative person in the selected production frame; a separately supported genitive alternative is not the selected target.
fedan-feed-source | feed; nourish | feed; nourish | Accusative being fed; food may be mid + dative or a bare instrumental in the assigned expressions.
feohtan-1 | fight; contend | fight; contend | Intransitive; wið + accusative opponent.
findan-1 | find | find | Accusative person or thing found.
fleon-flee | flee; flee from; avoid | flee; flee from; avoid | Intransitive or with accusative person/thing avoided.
fon-1 | seize; catch | seize; catch | Accusative patient in the selected frame.
for-beneficiary | for; on behalf of | for; on behalf of | Dative beneficiary.
forceorfan-u13 | cut down; cut off | cut down; cut off | Accusative tree or thing cut.
forgiefan-u14-give | give; grant | give; grant | Accusative thing given and dative recipient; the thing may be understood from context.
forgiefan-u16-forgive | forgive | forgive | Accusative sin, dative person forgiven; in a passive the sin becomes nominative and the person remains dative.
forlaetan-1 | abandon; forsake | abandon; forsake | Accusative person or thing left.
forleosan-u16 | lose | lose | Accusative thing lost.
fot-measure | foot | foot; feet | Unit of length, distinct from the body-part sense.
fremman-1 | benefit | benefit; do good to | Dative beneficiary.
gebiddan-u14-pray | pray | pray | With an accusative reflexive pronoun in the assigned prayer frame.
gefyllan-u16-fulfil | fulfil | fulfil; fulfill | Accusative prediction fulfilled; passive subjunctive in the assigned purpose construction.
gegaderian-1 | gather | gather | Accusative people or things gathered.
gehatan-promise | promise | promise | Accusative thing promised; a dative recipient may be added.
gemang-among | among | among | Accusative group in the selected sending-among frame.
gemetan-find | find; meet | find; meet | Accusative person or thing found/met.
genealaecan-1 | approach; draw near | approach; draw near | Dative person, place or event approached.
geneosian-visit | visit | visit | Accusative person in the selected prefixed-verb frame.
geopenian-open | open | open | Accusative thing opened, including mouth or eyes.
geseon-objectless | see | see | Absolute use, with no expressed object.
geseon-perceive-action | see | see; see someone do something | Accusative perceived actor and plain infinitive.
geseon-u16-content | see | see; see that | With a content clause stating the circumstance seen.
geseon-u18-state-content | see | see; see how | With the assigned clause describing how a state of affairs stands.
gestillan-1 | quell; settle | quell; settle | Accusative disturbance settled; distinguish intransitive become still.
geswican-cease | cease | cease; cease from | Genitive thing ceased from.
geswican-fail | fail; cease | fail; cease | Intransitive without a genitive complement in the selected frame.
geweorthian-1 | distinguish; adorn | distinguish; adorn | Accusative person adorned; mid + dative equipment or adornment.
gewitan-depart | depart; go away | depart; go away | Intransitive; fram + dative departure point is optional. The assigned frame requires no reflexive.
gierwan-1 | prepare | prepare | Accusative thing prepared.
habban-1 | have; possess | have; possess | Accusative possession; distinguish the perfect auxiliary.
halsian-u16-conjure | conjure; solemnly charge | conjure; solemnly charge | Accusative person; ðurh + accusative oath standard; a requested ðæt clause may follow.
healdan-u16-keep | keep; observe | keep; observe | Accusative saying or command observed.
helpan-1 | help | help | Dative person helped.
hieran-obey | obey | obey | Dative person obeyed.
hlystan-u18-selected | listen to; heed | listen to; heed; hear | Genitive person or thing listened to; hear is the contextual prompt wording.
hweorfan-u11-source | return; turn back | return; turn back | Supplied source preterite.
hydan-1 | hide; conceal | hide; conceal | Accusative thing hidden; wesan forms the assigned passive.
iernan-u16 | run | run | Intransitive; geond + accusative path. A perception construction may make its actor accusative.
isern-adjective-1 | iron; made of iron | iron; made of iron | Adjective of material.
leornian-learn | learn | learn | Accusative thing learned; æt + dative person/source.
mid-by-means | with; by means of | with; by means of | Dative instrument or means.
niman-1 | take | take | Accusative person or thing taken, including food.
oferwyrcean-u17-selected | overlay; cover | overlay; cover | Accusative object, mid + dative material used to cover it.
on-in-name | in one's name | in one's name; in the name of | on + dative naman, with genitive possessor.
on-sabbath-temporal | on | on | Time preposition in the stated-day expression.
on-side-idiom | on one's side | on one's side; on the side of | The bounded on … hand side expression uses accusative, including with standan.
onfon-u14-receive | receive; accept | receive; accept | Dative thing received in this selected frame; the later accusative payment frame is separate.
ongean-against | against; opposite | against; opposite | Accusative landmark or opponent.
onliesan-u13 | release | release | Accusative person or thing released.
plegian-u16-play | play | play | Intransitive; the reading supplies local wið participant and mid instrument phrases.
raedan-1 | read | read | Accusative text, or absolute with no expressed object.
ridan-1 | ride | ride | Intransitive in the introduced frame.
rowan-source | row | row | Intransitive; the assigned route is expressed with ofer.
sceawian-1 | watch; observe | watch; observe | Accusative person or event watched, including a journey.
scencan-pour | pour out; give to drink | pour; pour out; give to drink | Accusative drink, dative recipient.
sceththan-1 | hurt; injure | hurt; injure | Dative person harmed.
scrydan-clothe | clothe; dress | clothe; dress | Accusative person clothed in this introduced frame.
secan-1 | seek | seek | Accusative person or thing sought.
secgan-content | tell; say | tell; say | Dative addressee and a reported statement or question as content.
sellan-u13-sell | sell | sell | Accusative thing sold.
sendan-1 | send | send | Accusative person or thing sent, dative recipient.
singan-1 | sing | sing | Intransitive in the introduced frame.
slean-kill | slay; kill | slay; kill | Accusative person killed.
smierwan-u16 | anoint | anoint | Accusative body part or person, mid + dative material.
sprecan-u13-converse | speak with | speak; speak with; converse with | mid + dative interlocutor in the taught production frame.
thearfa-1 | poor person; needy person | poor person; needy person | Noun referring to a person.
tholian-source | suffer; endure | suffer; endure | Accusative hardship endured.
thurh-through | through | through | Accusative landmark or medium.
thurh-u14-mediated-source | through; by | through; by | Mediated action through a person in the supplied frame.
thwean-u16 | wash | wash | Accusative body part, mid + dative liquid.
thyncan-seem-source | seem | seem | Dative experiencer; the thing that seems is nominative.
tilian-u14-provide | obtain; provide | obtain; provide; provide for oneself | Genitive thing procured; dative reflexive beneficiary in the assigned frame.
to-destination | to | to | Dative destination.
to-u18-directed-look | toward | toward; towards | Target of a look in the supplied frame.
togelaedan-source | bring | bring | Accusative thing brought, dative recipient.
totwaeman-separate-beings | separate | separate | Accusative beings separated; fram + dative other party.
unnan-grant | grant; allow | grant; allow | Dative person, genitive thing granted.
welig-rich-in | rich in; abounding in | rich in; abounding in | on + dative thing abounded in.
wenan-u15-suppose | suppose; expect; think | suppose; expect; think | Genitive thing expected in the selected nominal frame; content-clause uses are separately taught.
weorpan-1 | throw | throw | Accusative thing thrown.
weorthan-become | become | become | Nominative subject and agreeing nominative predicate.
weorthan-u16-arise | arise; come about | arise; come about | Intransitive with a nominative subject, including the arising of a calm.
wician-1 | sojourn; lodge | sojourn; lodge | Intransitive; mid + dative person with whom one lodges.
witan-u16-person | know | know; know a person | Accusative person in this taught frame; cunnan has a separate acquaintance sense.
with-against | against; opposed to | against; opposed to | Accusative opponent.
with-u18-local-sense | toward | toward; towards | Conduct toward a person in the supplied local frame.
writan-1 | write | write | Accusative text written.
wuldrian-u16 | glorify | glorify | Accusative person; an accusative reflexive expresses glorifying oneself.
wyrcean-work | work; perform | work; perform | Accusative work or deed.
'''
for line in REFINEMENTS.strip().splitlines():
    sid,gloss,labels,qualifier=[s.strip() for s in line.split('|')]
    overrides[sid]={'display_gloss':gloss,'english_lookup_labels':[s.strip() for s in labels.split(';')],'usage_qualifier':qualifier}

source_by_id={s['sense_id']:s for s in SOURCE}
assert not (set(overrides)-set(source_by_id)), sorted(set(overrides)-set(source_by_id))
NUMBERS={'4':'four','5':'five','6':'six','7':'seven','8':'eight','9':'nine','10':'ten','11':'eleven','12':'twelve'}

def simple_labels(gloss):
    # Only semicolons in reviewed ordinary lexical glosses delimit synonym labels.
    labels=[v.strip().rstrip('?!.') for v in gloss.split(';')]
    return list(dict.fromkeys(NUMBERS.get(v,v) for v in labels if v))

records=[]
for source in SOURCE:
    sid=source['sense_id']; edited=overrides.get(sid)
    values=edited or {'display_gloss':source['gloss'],'english_lookup_labels':simple_labels(source['gloss']),'usage_qualifier':''}
    record={'sense_id':sid,'lemma_id':source['lemma_id'],'register_headword':source['headword'],**values,
            'editorial_status':'reviewed_explicit_reconciliation' if edited else 'reviewed_retained_lexical_gloss',
            'original_gloss':source['gloss'],'used_in_tasks':source['used_in_tasks'],'evidence_refs':source.get('evidence_refs',[]),
            'difficult_item':bool(edited),'unresolved':[]}
    if sid in ['asmean-u17-source-sense','geriman-u17-source-sense']:
        record['display_headword_override']={'asmean-u17-source-sense':'āsmēan','geriman-u17-source-sense':'gerīman'}[sid]
        record['headword_evidence']='Accepted current learner/key and exact retained Cook hint: '+('EX-XII-XIII-39-07' if sid.startswith('asmean') else 'EX-XII-XIII-42-03')
    if sid in ['top-u16-reading','torr-u14-crag-source','thaet-u16-uncertain-link']:
        record['retained_source_uncertainty']=True
    records.append(record)

assert len(records)==1681
EXTRA_EDITS={
    'the-u17-concessive-marker':('clause marker',[], 'Only in supplied ðēah ðe, although; ðe alone is not an equivalent of although.'),
    'swithe-u15-superlative':('most; very greatly',['most','very greatly'],'Superlative swīðost; recognition reference, not independent production.'),
    'slean-u15-kill':('kill',['kill'],'Accusative person; the bounded negative command uses selected short-vowel imperative sleah.'),
    'unrihtwis-1':('unrighteous',['unrighteous'],'Adjective, distinct from the substantive unrighteous people.'),
    'agan-possess':('have; possess',['have','possess','own'],'Accusative possession; positive present and preterite indicative in the taught scope.'),
    'strengu-1':('strength',['strength'],'Recognition class-reference noun; preserve the source spelling and do not infer a plural count meaning.'),
}
register=json.loads((OUT.parents[3]/'lexicon/entries.json').read_text(encoding='utf8'))
additional=[]
for lemma in register['lemmas']:
    for sense in lemma['senses']:
        sid=sense['sense_id']
        if sid not in EXTRA_EDITS:continue
        gloss,labels,qualifier=EXTRA_EDITS[sid]
        record={'sense_id':sid,'lemma_id':lemma['lemma_id'],'register_headword':lemma['display_headword'],
                'display_gloss':gloss,'english_lookup_labels':labels,'usage_qualifier':qualifier,
                'editorial_status':'reviewed_additional_register_sense','original_gloss':sense['gloss'],
                'used_in_tasks':[],'evidence_refs':sense.get('evidence_refs',[]),'difficult_item':True,'unresolved':[],
                'coverage_note':'Absent from the aggregate required_sense_ids of assigned tasks; retained for complete register/OE coverage.'}
        if sid=='the-u17-concessive-marker':
            record['used_in_tasks']=['EX-XII-XIII-43-10']
            record['coverage_note']='The register scope and supplied whole ðēah ðe concession bind this sense to EX-XII-XIII-43-10, although the task required_sense_ids omits this component. The independent prompt check recovers the phrase; no teaching milestone is added.'
            record['phrase_access']={'english_lookup_labels':['although','though','even though'],'old_english_phrase':'ðēah ðe','usage_note':'Supplied whole concessive conjunction in EX-XII-XIII-43-10.'}
        additional.append(record)
assert {s['sense_id'] for s in additional}==set(EXTRA_EDITS)
assert not ({s['sense_id'] for s in records}&set(EXTRA_EDITS))
assert len(records)+len(additional)==sum(len(l['senses']) for l in register['lemmas'])==1687
output={'schema_version':1,'scope':'Every sense referenced by current assigned exercise tasks. Meaning and English access are edited separately from source/register identity. These entries do not create new teaching milestones.',
        'usage_evidence_policy':'Case government was checked against the accepted lexical-frames.json audits for Units 04–16, the later accepted senses/constructions audits, and the current prompts/keys. Original sense evidence_refs remain attached; the gloss is not a new source transcription.',
        'counts':{'senses':len(records),'explicit_reconciliations':len(overrides),'retained_lexical_glosses':len(records)-len(overrides),'additional_register_senses':len(additional),'all_register_senses':len(records)+len(additional)},'senses':records,'additional_register_senses':additional}
(OUT/'sense-display.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(output['counts']))
print('Residual display metadata:')
for r in records:
    if not r['difficult_item'] and (re.search(r'[/:()]',r['display_gloss']) or len(r['display_gloss'].split())>8 or re.search(r'\b(source|supplied|selected|reference|indicative|subjunctive|participle|ordinary|singular|plural|form|construction|taught)\b',r['display_gloss'],re.I)):
        print(r['sense_id'],'|',r['display_gloss'])
