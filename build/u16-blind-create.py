from pathlib import Path
import hashlib
import re
import unicodedata

source = Path('chapters/ch16/student.md')
raw = source.read_bytes()
student = raw.decode('utf-8-sig')
answers = {}

def add(item, *values):
    assert item not in answers
    answers[item] = list(values)

add('NEW-U16-F01',
    'ācierfst', 'ācurfe', 'ācurfon',
    'The present second singular uses ācierf- (ie beside infinitival eo); the preterite second singular and plural share ācurf-, with -e and -on respectively. The prefix ā- remains. The first/third-singular preterite ācearf has a different vowel and is not the stem for these two preterite answers.',
    'forlīest', 'forlure', 'forluron',
    'The third-singular present changes ēo to īe and contracts the s + dental sequence to -st. The second-singular and plural preterites use forlur-, changing both the vowel and s to r, with -e and -on. Retain for-.',
    'ðwiehð', 'ðwōge', 'ðwōgon',
    'The selected contracted present third singular has ðwieh-. The second-singular and plural preterites have ðwōg- with -e/-on; the first/third-singular preterite instead has ðwōh. Thus the preterite g is not obtained by merely adding an ending to ðwōh.',
    'iernð', 'arn', 'urnon',
    'The present uses iern-, the first/third-singular preterite arn, and the plural preterite urn- + -on. The r stays after the vowel in all three selected stems; these are not the alternative irn-/yrn- spellings.')

add('NEW-U16-F02',
    'smierwe', 'smierest', 'smierede', 'bewęnde', 'bewęnde', 'plegodon', 'behēafdodon', 'gefylled', 'forgiefen',
    'Smierw- occurs in present first singular; the second singular drops w (smierest), and the preterite likewise lacks w (smierede). The selected ie remains throughout these answers.',
    'Bewęnde can be present indicative first singular or preterite indicative first/third singular. Its spelling alone does not settle tense or person: the stated subject and clause context do so.')

add('NEW-U16-F03', 'āceorf', 'āceorfað', 'blissa', 'blissiað', 'smiere', 'smierwað', 'ārīs', 'ārīsað', 'forlǣt', 'forlǣtað', 'geswīc', 'geswīcað', 'ęfthweorf', 'ęfthweorfað')
add('NEW-U16-F04', 'finde', 'finden', 'fēde', 'fēden', 'iernan', 'iernanne')
add('NEW-U16-F05', 'nearu — strong masculine nominative singular, identical to the given headword.', 'nearone', 'nearwes', 'nearwum', 'bēgen suna', 'bēgra suna', 'bǣm sunum (also bām sunum).',
    'The unextended nominative is nearu; nearo- precedes consonantal -ne in nearone, whereas nearw- precedes the vowel endings -es and -um in nearwes/nearwum.',
    'Bēgen and its inflections are grammatically plural, although they denote exactly two. The nouns are plural too. There is no separate dual declension of both; even beside dual unc/inc its dative is plural bǣm.')

add('NEW-U16-A01', 'The king saw his son. The king went.', 'The king saw his son. The king’s son went.', 'Se cyning ēode.', 'Ðæs cyninges sunu ēode. (Se sunu ēode also resolves the reference in this two-sentence setting.)')
add('NEW-U16-A02', 'The king saw the son go.', 'The king knew that the son went (or had gone, if a prior event is intended).',
    'Ðone sunu is accusative masculine singular, the actor of infinitival gān in the perception complement of geseah.',
    'Se sunu is nominative masculine singular, the subject of finite ēode within the ðæt-clause.',
    'Gān is the plain, nonfinite infinitive. Ēode is finite preterite third singular in this clause. The indicative and subjunctive third-singular preterites have the same spelling, so ēode alone cannot decide the mood; the finite clause and interpretation establish its use.')
add('NEW-U16-A03',
    'He said that the king was there.',
    'Sægde: sęcgan, preterite indicative third singular in the matrix narration (its surface also coincides with a subjunctive). Wǣre: wesan, preterite subjunctive third singular, agreeing with se cyning in the report.',
    'There is no participle or infinitive.',
    'The report uses finite wǣre to present the king’s state at the time of saying. Its preterite morphology in reported content does not itself place the state before the speech. The given simultaneous context, rather than automatic English backshift, fixes the temporal relation.',
    'He said that the king had made the ship.',
    'Sægde: preterite indicative third singular of sęcgan in the matrix. Hæfde: preterite third singular of habban; indicative and subjunctive are formally identical. A reported-content subjunctive reading is natural, but its spelling does not prove that mood.',
    'Geworht is the past participle of wyrcan, combined with hæfde; it is not another finite preterite.',
    'Geworht hæfde is the habban perfect group. With the stated completed making, it places the making before the past speech, hence “had made”. This is different from merely changing every English present to a past after said: the participle-plus-auxiliary construction supplies the completed-event relation.',
    'He said that the king intended/wanted to sing (or: would sing, with the stated intention).',
    'Sægde: matrix preterite indicative third singular of sęcgan. Wolde: preterite third singular of willan, agreeing with se cyning; indicative and subjunctive spellings coincide. It can be interpreted as subjunctive within the report, without claiming the ending uniquely identifies it.',
    'Singan is a plain infinitive, the intended action governed by wolde.',
    'Wolde singan locates an intention at the past reporting viewpoint; the singing is still prospective in the given context. The preterite wolde does not assert that singing happened earlier, and “would” here must not erase volition or be treated as a mechanical past-tense replacement for any future.')

add('NEW-U16-C01', 'Se cyning sægde his suna: “Sęle mē ðā bōc.”', 'Se sunu sealde him ðā bōc.',
    'Mē inside the king’s quotation is dative first singular and denotes the king. Him in the subsequent narration is dative third singular and again denotes the king, the book’s recipient; the son is the nominative giver. Tō his suna is also possible for the speech addressee.')
add('NEW-U16-C02', 'Ic cann ðone mann.', 'Ic cann singan.', 'Ic wāt ðæt hē hēr is.',
    'In the first, cunnan takes accusative ðone mann as the person known. In the second it takes plain infinitive singan, expressing learned ability. In the third witan takes a finite factual ðæt-clause, with its own nominative hē and finite is. Personal-object witan is also possible in the language but would not meet the requested first-statement verb.')
add('NEW-U16-C03', 'Ðā męnn plegodon wel; se cyning plegode bęt ðonne hīe dydon.',
    'Dydon substitutes for plegodon, “played”, in the comparison; it agrees with plural hīe (the men), not singular se cyning. Both the first and second expressed playing actions use plegian as requested.')

add('EX-XII-XIII-32-01', 'Ic ēow ealle grēte.')
add('EX-XII-XIII-32-02', 'Ðā hīe swilce twēntig furlanga oððe ðrītig rēowon, ðā gesāwon hīe ðone Hǣlend uppan ðǣm sǣ gān.\n\nRēowon is the taught simple preterite, here anterior to the seeing: “when they had rowed”. Unit 12 expressly permits an English pluperfect rendering of a simple Old English preterite. I have not fabricated an independently productive rōwan participle. The temporal finite verb and the perception infinitive are both final in their respective groups, satisfying the printed order direction whichever group it is intended to control.')
add('EX-XII-XIII-32-03', 'Hē ārās and bebēad ðǣm winde and cwæð tō ðǣm sǣ: “Geswīc.”\n\nI use the current productive intransitive cease command for “Subside”. Gestil is a possible lexical alternative, but earlier learner material taught its command with transitive “quell/settle”; the intransitive storm use in Unit 11 was supplied. A key requiring gestil alone would need to distinguish that dependency from general grammatical validity.')
add('EX-XII-XIII-32-04', 'Se wind geswāc, and wearð micel smyltnes.')
add('EX-XII-XIII-32-05', 'Ðū hīerst his stefne, and ðū ne wāst hwanon hē cume, ne hwider hē gā.\n\nThe two unknown dependent questions use present subjunctives. Uncontracted ne wāst is deliberate; the clause still means “you do not know”.')
add('EX-XII-XIII-32-06', 'Hē geseah twēgen brōðor hiera nętt on ðone sǣ sęndan; hīe wǣron fisceras.')
add('EX-XII-XIII-32-07', 'And hē sægde him: “Cumað æfter mē, and ic dō ðæt git bēoð manna fisceras”; and hīe sōna forlēton hiera nętt.\n\nGit is dual nominative but has plural bēoð; the causative complement remains a finite ðæt-clause.')
add('EX-XII-XIII-32-08', 'Gif ðīn hand oððe ðīn fōt ðē ǣswicað, āceorf hit of and weorp fram ðē; bętere ðē is ðæt ðū healt on līf gā, ðonne ðū twā handa and twēgen fēt hæbbe and on ēce fȳr sīe worpen.\n\nThe second commanded object is omitted as requested; hit first resumes either body part. The comparative clause keeps the supplied subjunctives and omits a repeated ðæt after ðonne.')
add('EX-XII-XIII-32-09', 'Gif hwilc mann hæfð hund scēapa and forlīest ān of ðǣm, ne forlǣtt hē ðā nigon and hundnigontig on ðǣm muntum, and gǣð and sēcð ðæt ān ðe forwearð?\n\nThere is no English-style do auxiliary. Ðæt ān ðe supplies a demonstrative-plus-relative equivalent of “the one that”, with neuter reference to scēap.')
add('EX-XII-XIII-32-10', 'And gif hit gelimpð ðæt hē hit finde, sōðlice ic ēow sęcge ðæt hē blissað swīðor ofer ðæt ān ðonne ofer ðā nigon and hundnigontig.')
add('EX-XII-XIII-32-11', 'Ðonne hē hām cymð, hē cleopað tōgædere his frīend and his nēahgebūras and cwyð: “Blissiað mid mē, for-ðon-ðe ic fand mīn forloren scēap.”\n\nFand is the expressly retained first-singular preterite. Forloren modifies neuter accusative scēap. No auxiliary have is inserted.')

add('EX-XII-XIII-33-01', 'And intō ðǣm hūse gangende hīe fundon ðæt cild mid Marian his mēder.')
add('EX-XII-XIII-33-02', 'Ārīs and nim ðæt cild and his mōdor on niht and flēoh tō Egypta lande and bēo ðǣr oð-ðæt ic ðē sęcge.\n\nNiht retains its learned unchanged dative singular. The until-clause has its finite verb last.')
add('EX-XII-XIII-33-03', 'Hē ārās ðā and nam ðæt cild and his mōdor on niht and fērde on Egypta land, ðæt hit gefylled wǣre, ðæt fram Dryhtne ðurh ðone wītegan gecweden wæs: “Of Egyptum ic cleopode mīnne sunu.”\n\nThe first ðæt is the purpose conjunction; the later relative ðæt resumes neuter hit, the utterance. The passive purpose has wǣre without a separate modal translating “might”. The prophecy has a simple preterite, as the prompt omits have. A resumptive ðæt ... ðæt ðe arrangement is another defensible relative construction, but I have used the indicated demonstrative relative.')
add('EX-XII-XIII-33-04', 'Hwæs magon hīe biddan?')
add('EX-XII-XIII-33-05', 'Sēo sunne gīemð ðæs dæges.\n\nGīeman’s earlier productive rule-over construction governs the genitive; an accusative copied from English would miss the requested government.')
add('EX-XII-XIII-33-06', 'Hīe wēndon nāhtes būtan dēaðes selfes.')
add('EX-XII-XIII-33-07', 'Ðū geswīcst ðīnes weorces.\n\nThe present can express the future here. Ðū wilt ðīnes weorces geswīcan would instead explicitly introduce willingness/intention and is not needed simply because the English has wilt.')
add('EX-XII-XIII-33-08', 'Wēn is ðæt hē frēond finde.')
add('EX-XII-XIII-33-09', 'Hē sægde him: “Ic wille on fiscnoð gān”; hīe sægdon: “And wē willað mid ðē gān.”')
add('EX-XII-XIII-33-10', 'Hīe ēodon ūt and ēodon on scip and ne fēngon nāwiht on ðǣre niht.')

add('EX-XII-XIII-34-01', 'Swā hwā swā ðū sīe, ne forlǣt mē.\n\nI take the unnumbered you as singular. A consistently plural address, with gē/sīen/forlǣtað, would express a different number assumption rather than an inflection error.')
add('EX-XII-XIII-34-02', 'Gif ðū nānne ne finde ðe ðē fēde, ęfthweorf hider.\n\nThe two present subjunctives mark the hypothetical finding and possible provider. Nānne is the selected accusative of nān; the negatives express one negation.')
add('EX-XII-XIII-34-03', 'Genyhtsumien mīna bēc unc bǣm.\n\nThe complete sentence is supplied. The books control plural genyhtsumien; unc is dual dative, and bǣm plural dative.')
add('EX-XII-XIII-34-04', 'Bēgen ðā cnapan sind wel gelǣrede.')
add('EX-XII-XIII-34-05', 'Hīe wǣron bēgen rihtwīse beforan Gode.\n\nThis selects masculine plural referents. The English prompt alone does not state their genders; a supported feminine pair would require bā and rihtwīsa rather than be rejected merely for differing from this choice.')
add('EX-XII-XIII-34-06', 'Ic ðē hālsie ðurh ðone libbendan God, ðæt ðū ūs sęcge hwæðer ðū Crist sīe, Godes sunu.\n\nÐē is the accusative person charged, ūs the dative recipient of telling, and hwæðer introduces the uncertain identification. An embedded gif for “if/whether” would need its own teaching or lexical support; the taught hwæðer states the intended question clearly.')
add('EX-XII-XIII-34-07', 'Ic ēow sęcge: “Æfter ðissum gē gesēoð Mannes Sunu on ðā swīðran hand Godes mægenðrymmes sittan and on heofones wolcnum cuman.”\n\nThe accusative perceived person has two plain infinitives. No separate things or shall is necessary. The fixed right-hand phrase is retained from the help.')
add('EX-XII-XIII-34-08', 'Sīe inc æfter incrum gelēafan.')
add('EX-XII-XIII-34-09', 'Sōðlice Mannes Sunu is tō cumanne on his Fæder wuldre, and ðonne āgylt hē ǣlcum be his āgnum weorce.\n\nThe impending-coming phrase and corrected reward clause are supplied. There is no independently manufactured āgyltan paradigm.')
add('EX-XII-XIII-34-10', 'Ðonne Crist cymð, ðonne ne wāt nān mann hwanon hē sīe.\n\nThe unknown origin is an embedded question, hence sīe. The future arrival can be conveyed by the present; I have selected indicative cymð. A prospective subjunctive cume is a defensible alternative with a less asserted temporal situation.')
add('EX-XII-XIII-34-11', 'Se Hǣlend cleopode and lǣrde on ðǣm temple and cwæð: “Mē gē cunnon, and gē witon hwanon ic sīe; and ic ne cōm fram mē selfum, ac sē is sōð sē ðe mē sęnde, ðone gē ne cunnon.”\n\nCunnan has the personal objects; witan introduces the question. The final ðone is an accusative demonstrative relative referring to the sender. Fram governs dative mē selfum.')
add('EX-XII-XIII-34-12', 'Gē hine ne cūðon; ic hine cann, and gif ic sęcge ðæt ic hine ne cunne, ic bēo ēow gelīc; ac ic hine cann and ic healde his sprǣce.\n\nCūðon is preterite, not a new perfect; cunne is final in the reported negative clause and fulfils the indicated subjunctive target. Ēow is dative with gelīc. The personal witan construction is also valid language, though I have consistently selected cunnan here.')
add('EX-XII-XIII-34-13', 'Gif ic mē selfne wuldrie, nis mīn wuldor nāwiht; mīn fæder is sē ðe mē wuldrað, be ðǣm gē cweðað ðæt hē ēower God sīe.\n\nNis begins the naught clause as requested. Mē selfne is masculine accusative reflexive. The final sīe belongs to reported content; be governs relative dative ðǣm.')

add('EX-XII-XIII-35-01', 'Fōh ðisne ðoðor.\n\nThe earlier accusative-catching verb fōn supplies a complete taught route. A plural addressee would take fōð.')
add('EX-XII-XIII-35-02', 'Hwā fēng ðone sweartan ðoðor?')
add('EX-XII-XIII-35-03', 'Gā ðæs weges ðe ðū cōme.\n\nThe route is genitive, and cōme is the second-singular preterite for the addressed person’s earlier arrival, not an automatic present subjunctive.')
add('EX-XII-XIII-35-04', 'Ic nǣfre bęt ne plegode ðonne ic tō-dæg dyde.')
add('EX-XII-XIII-35-05', 'Hēo nǣfre bęt ne sang ðonne hēo nū dyde.\n\nThe English’s unusual “did now” is retained: nū marks the relevant current performance from the chosen viewpoint, while dyde remains preterite.')
add('EX-XII-XIII-35-06', 'Ðrīwa ic ðolode forlidennesse; niht and dæg ic wæs on ðissum sǣ.\n\nNiht and dæg are accusatives of duration, unlike on ðissum sǣ, the dative location.')
add('EX-XII-XIII-35-07', 'Ic wiste sumne mann sē ðe wæs lǣded ōð ðone ðriddan heofon and ðǣr hīerde ðā word ðe nān eorðlic mann ne mæg sprecan.\n\nWiste obeys the requested witan, whose object is personal accusative sumne mann. The carried man is subject of the passive and then of hearing. The two negatives in the last relative convey one prohibition/inability.')
add('EX-XII-XIII-35-08', 'Ēalā, hū nearu is ðæt geat and se weg ðe tō līfe lǣtt, and swīðe fēawe sind ðe ðone weg findað.\n\nThe first coordination and singular agreement are the explicitly supplied source expression; this does not authorize singular agreement with arbitrary coordinated subjects.')
add('EX-XII-XIII-35-09', 'Hīe cumað tō ēow on scēapa gegierelum, ac innan hīe sind wulfas.')
add('EX-XII-XIII-35-10', 'Ðā hē nēalǣcte ðǣre ceastre geate, ðā wæs ðǣr dēad mann boren.\n\nNēalǣcan takes dative geate; ðǣre ceastre is the genitive dependent of that gate. The man is nominative as passive subject.')
add('EX-XII-XIII-35-11', 'Ic gesēo mǣden geond ðā strǣte iernan.')
add('EX-XII-XIII-35-12', 'Smiere mē mid ęle.')
add('EX-XII-XIII-35-13', 'Sęllað ūs of ēowrum ęle.\n\nThe supplied possessive is plural, so the selected command also addresses a plural audience.')
add('EX-XII-XIII-35-14', 'Gif se sunu ēow ālīest, gē bēoð sōðlice frige.')

add('EX-XII-XIII-36-01', 'Ne dēme gē be ansīene, ac dēmað rihtne dōm.\n\nThe first plural command is shortened immediately before gē; the second has ordinary -að. Dōm is accusative, with masculine accusative rihtne.')
add('EX-XII-XIII-36-02', 'Ðā bewęnde hē him tō ðǣm wīfe and cwæð: “Gesiehst ðū ðis wīf? Ic ēode intō ðīnum hūse; ðū mē ne sealdest wæter tō mīnum fōtum; ðēos ðwōh mīne fēt mid hiere tēarum.”\n\nHim first is subject-directed dative reflexive. The neuter noun wīf has neuter ðis; the supplied feminine ðēos then resumes the actual woman. Ðwōh is preterite, with no added have.')
add('EX-XII-XIII-36-03', 'Ðū mē coss ne sealdest; ðēos, siððan ic inēode, ne geswāc ðæt hēo mīne fēt ne cyste.\n\nSealdest is last in its clause. The supplied pair of cessation negatives means that her kissing continued; the second ne does not negate the occurrence of kisses.')
add('EX-XII-XIII-36-04', 'Mīn hēafod ðū mid ęlum ne smieredest; ðēos smierede mīne fēt mid sealfe.')
add('EX-XII-XIII-36-05', 'For-ðon ic ðē sęcge: “Manega synna hiere sind forgiefen, for-ðon-ðe hēo mē swīðe lufode.”\n\nThe sins are the plural passive subject; hiere is still dative. The prescribed bare forgiefen is retained. Lufode is last in the causal clause.')
add('EX-XII-XIII-36-06', 'Lǣs lufað ðǣm ðe lǣs forgiefen is.\n\nThe entire compressed sentence is supplied. The first lǣs is the specified accusative of degree; the second is nominative amount forgiven. The person loving is the understood matrix subject, not an ordinary dative subject licensed by lufian.')
add('EX-XII-XIII-36-07', 'Hit ne ālīefð ðē hīe tō wīfe habban.\n\nI retain the supplied impersonal clause, with no added is and with hīe accusative as the person had as wife.')
add('EX-XII-XIII-36-08', 'Ðā gehēt hē mid āðe hiere ðæt tō sęllanne, swā hwæs swā hēo hine bǣde.\n\nThe supplied sentence keeps giving’s accusative ðæt distinct from the genitive requested thing hwæs in the biddan clause, and has accusative hine for the person asked.')
add('EX-XII-XIII-36-09', 'Ðā cwæð hēo, fram hiere mēder myngod: “Sęle mē on disce Johannes ðæs fuluhteres hēafod.”\n\nJohannes is the supplied genitive, accompanied by genitive ðæs fuluhteres; hēafod is the accusative thing requested.')
add('EX-XII-XIII-36-10', 'Ðā āsęnde hē and behēafdode Johannem on ðǣm cwearterne.\n\nThe first verb’s unexpressed patient follows the supplied “sent someone” instruction. Johannem is the supplied accusative name.')
add('EX-XII-XIII-36-11', 'And mann brōhte his hēafod on disce.\n\nMann expresses an indefinite person, English “one”. Ān brōhte his hēafod on disce is also defensible if one individual is being singled out.')

add('NEW-U16-R01', '''After these words he went along the road that had been shown to him, until he came to the gate of the city and went in there. While he was thinking whom he might ask for support to live on, he saw a lightly clad boy running through the street. The boy was anointed with oil and girded with a linen cloth, and carried in his hand the young men's games [that is, their gaming equipment, in context], belonging to the bathing place. He called with a loud voice and said, “Listen, you townspeople! Listen, you foreigners, free and enslaved, noble and not noble! The bathing place is open.”

When Apollonius heard that, he stripped himself of the half cloak he had on and went into the bath. While he observed every single one of them at their work, he sought his equal, but could not find him there in the company. Then suddenly Arcestrates, king of that whole region, came with a large company of his men and entered the bath. The king began to play ball with his companions. And Apollonius joined in the king's game, as God willed, and, running, caught the ball and sent it back, struck with swift speed, to the playing king. Again he [in the natural sequence, the king] sent it back; he [Apollonius] struck quickly, so that he never let it fall. The king then recognized the young man's agility, [so] that he knew that he had no equal in that game. Then he said to his companions, “Go away from here; this young man, as it seems to me, is my equal.”

When Apollonius heard that the king praised him, he ran quickly and approached the king, and with a trained hand he swung the top [tentatively, ball] with such great swiftness that it seemed to the king as if he had been changed from old age to youth. After that, he [Apollonius] attended him [the king] agreeably on his royal seat. When he [the king, in my contextual reading] went out of the bath, he [Apollonius] led him [the king] by the hand, and then afterwards turned away himself [Apollonius] from there by the way he had come before.

Then, after Apollonius had gone away, the king said to his men, “I swear by the common welfare that I have never bathed better than I did today, through the service of I know not what young man.” Then he looked towards one of his men and said, “Go and find out what sort of man the young man is who served me so well today.”

The man then went after Apollonius. When he saw that he [Apollonius] was wrapped in a dirty cloak, he returned to the king and said, “The young man you asked about is a shipwrecked man.” Then the king said, “By what do you know that?” The man answered him and said, “Even if he himself keeps it unspoken, his clothing reveals him.” Then the king said, “Go quickly and tell him that ‘the king asks you to come to his meal.’”

Limits kept explicit: (i) lightly clad follows the supplied range of nacod; “naked” is another literal rendering but total nudity is not established. (ii) The equipment explanation expands contextual plegan, whose literal noun is play/game, and belimpende qualifies it. (iii) I have translated the unusual geslægene phrase without silently repairing the Old English ending. (iv) In the nested knowledge/equal clause, [so] is tentative, and I leave the repeated he/his unresolved; both the exact connection and whose lack of an equal is meant remain uncertain. Næfde is negative. The Latin comparison concerns the king's former unmatched ability but is not a replacement text. (v) Top is tentatively a ball, and the Old English says swung it; the Latin ointment/rubbing account cannot silently supply a shoulder or neck or replace that action. (vi) The king-as-subject of ūtēode is a contextual reading of the exit, not something its ending proves; the original notes explicitly settle the subsequent leader and led person. (vii) I close the English oath before the next narrative sentence for readability, although the edition lacks the expected closing mark. The last quotation retains the mixed reported introduction and directly addressed invitation; it is not silently recast as an ordinary third-person report.''')
add('NEW-U16-R02',
    'He hears the herald’s announcement that the bathing place is open (Se bæðstęde is open), then removes his half cloak and enters (168.10–12, hē hine unscrȳdde ... ēode intō ðǣm ðwēale). The prior road and city entrance lead him to the announcement; no invitation from the king precedes this entry.',
    'Apollonius catches the ball while running and returns it swiftly, then keeps hitting without letting it fall (gelæhte ... ongēan gesęnde; nǣfre feallan ne lēt, 169.1–5). The king recognizes ðæs geongan snelnesse, the young man’s agility (169.5–6).',
    'He dismisses his companions and calls the youth his equal: Gāð ēow heonan; ðes cniht ... is mīn gelīca (169.7–8). The qualification ðæs-ðe mē ðyncð means “as it seems to me”.',
    'The messenger concludes that he is a shipwrecked man (forliden mann), after seeing him wrapped in a dirty cloak (mid horgum sciccelse bewǣfed, 170.9–11). He explains that even if the man is silent, his clothing reveals his condition: his gegierela hine gesweotolað (170.13–14).',
    'The king orders the messenger to go quickly and deliver an invitation to his meal: Gā hrædlīce, and sęge him ... cume tō his gereorde (170.14–16).')
add('NEW-U16-R03',
    'Hine denotes the ball (P169N3); it is masculine accusative singular, the actor/thing allowed to fall in feallan ne lēt. It belongs to that let-plus-infinitive group, not simply to the earlier slōh because the excerpt begins near it.',
    'Him is the king, dative masculine singular as the person served by ðēnode. The dative proves the grammatical role; the serving situation supplies the referent.',
    'Hē is Apollonius (P169N14), nominative masculine singular, subject of lǣdde. The immediately preceding exit clause does not force this hē to denote the same person as its own subject.',
    'Hine is Arcestrates/the king (P169N15), accusative masculine singular, object of lǣdde: the person led by the hand.',
    'Him is a dative reflexive referring to Apollonius, the subject of gewęnde: he turned away himself. It is not another recipient of leading or serving. The reflexive interpretation is supported by P169N16 and the local help, not by the shape him alone.',
    'Hē denotes Apollonius (P170N8), nominative masculine singular, subject of wæs ... bewǣfed inside the finite ðæt-clause perceived by the messenger. The messenger remains the subject of geseah.')
add('NEW-U16-R04',
    'A relative clause modifying ðone weg; the route is what was shown, and him is the person to whom it was shown.',
    'Getǣht wæs: passive past participle plus finite wæs, third-singular preterite indicative of wesan. Getǣht itself has no finite mood.',
    'An until-clause fixing the endpoint of the preceding going.',
    'Becōm: third-singular preterite indicative of becuman.',
    'An embedded interrogative complement of ðōhte: whom he might ask for support. Hwone is accusative person asked; the requested support is genitive.',
    'Biddan meahte: plain infinitive plus finite third-singular preterite meahte. Indicative and subjunctive have the same surface here; possibility within thought supports the supplied “might” interpretation, without a uniquely identifying mood ending.',
    'A finite content clause giving what Apollonius heard: that the king praised him.',
    'Hęrede: third-singular preterite, understood indicatively for the actual praise in this context, as the help states. Its spelling is also possible for the preterite subjunctive, so morphology alone is inconclusive.',
    'A dependent question after gewite, “find out”: what sort/status of man the young man is.',
    'Sīe: third-singular present subjunctive of wesan, subject se geonga mann; here it belongs to the dependent question.',
    'A concessive clause: even if he himself keeps the matter silent, the following main clause says his clothing reveals him.',
    'Forswīge: third-singular present subjunctive, as explicitly supplied for this source construction. Hit is its object, not its subject.')
add('NEW-U16-R05',
    'The king, Arcestrates, speaking after the messenger’s explanation.',
    'The messenger, commanded by singular Gā and sęge.',
    'Apollonius, dative recipient of the message in sęge him.',
    'The same king who gives the outer command, now designated in the message as “the king”.',
    'Both denote Apollonius, the invited person: ðē is accusative object of bitt, whereas ðū is nominative subject of cume.',
    'The outer sęge him ðæt starts a report introduced by “tell him that”, but its content is phrased as words directly addressed to Apollonius: “the king asks you that you come ...”. Thus him in the outer command becomes second-person ðē/ðū in the embedded quoted message. Cume is the invitation’s dependent subjunctive. A fully indirect report would keep third-person reference to the invitee, while a regular direct quotation would have a different introductory framing. The original mixes these levels, as P170N15 says; the actual wording should be preserved, not corrected into a uniform system.')
add('NEW-U16-R06',
    '“The king then recognized the young man’s agility, [so] that he knew that he had no equal in that game.” I preserve the nested ðæt clauses and the negative næfde. The bracketed connection and the repeated pronouns remain provisional.',
    'P169N6 explicitly says the clause is unclear. Its Latin parallel concerns the king’s previously unmatched skill, which helps with the context but cannot uniquely assign each Old English hē/his or turn næfde into “had an equal”. A contextual paraphrase must display that uncertainty rather than suppress the troublesome negative or replace the sentence by the Latin account.',
    '“With a trained hand he swung the top [tentatively, ball] with such great swiftness that it seemed to the king as though he had been changed from old age to youth.” The seeming is impersonal, with the king as dative experiencer; the rejuvenation belongs to the swilce comparison.',
    'P169N10 says the Old English differs from its Latin parallel and only tentatively identifies top with ðoðor. The English account retains swinging an object; the Latin describes rubbing/anointing with wrestlers’ ointment. It supplies neither a shoulder nor a neck. Neither the object’s precise sense nor the physical action may be silently resolved by translating the Latin instead; wǣre is an imagined comparison, not a claim that literal rejuvenation occurred.')

parts = re.split(r'<!-- item: ([A-Z0-9-]+) -->', student)
actual_ids = parts[1::2]
assert len(actual_ids) == 76 and set(actual_ids) == set(answers)
sha = hashlib.sha256(raw).hexdigest()
register_hashes = {name: hashlib.sha256(Path(name).read_bytes()).hexdigest()
                   for name in ['lexicon/entries.json', 'curriculum/grammar.json']}
header = f'''# Unit 16 — independent blind solutions

Reviewer: `/root/unit16_blind`, fresh non-author. This is the initial solve, before any key, contract or current audit comparison. It is to become immutable when the coordinator freezes it; later corrections belong in separate review records.

Learner identity: `chapters/ch16/student.md`, raw-byte SHA-256 `{sha}`. The coordinator identified its draft checkpoint as `9b75319`; I did not read the key or contract at that checkpoint.

Baseline identities: `lexicon/entries.json` SHA-256 `{register_hashes['lexicon/entries.json']}`; `curriculum/grammar.json` SHA-256 `{register_hashes['curriculum/grammar.json']}`. Both identify the fifteen-unit baseline, not newly accepted Unit 16 teaching.

Exposure record: I read the current learner master, `AGENTS.md`, `EDITORIAL_POLICY.md`, the neutral `sources/audits/unit16-coordinator/review-independence.json`, and permitted portions/search results of the actual baseline registers and earlier accepted learner masters (Units 8–15). Register searches were limited to existing lexical forms, senses and scope; references inside those allowed registers were not followed into contracts or review files. No current coverage contract, brief, audits, proposals, answer key, token map, ordered model, author/root translation witness or answer-exposing helper was opened. No external lookup or original scan was used. The full current learner text and its visible supplied help are permitted support, not an independent prior translation witness.

Method: all actual item and output markers are reproduced below in the learner’s order. Original English prompts are copied from that learner master; the answers are my compositions and analyses. For tasks with local supplied complete expressions, I retain those expressions and identify their use. Alternatives and doubts are recorded at the relevant output. I used the taught simple preterite in Cook 32.2 rather than assume a productive rōwan past participle, and selected the newly taught intransitive geswīc in 32.3 rather than promote an earlier supplied intransitive gestillan use. These are explicit choices to be assessed at comparison, not claims about a hidden model. No unresolved omission forced an external lookup. Source uncertainties in R01/R06 remain genuine uncertainties rather than alleged student errors.

Completeness: 76 learner tasks; 179 distinct requested output positions, each attempted. Structural counts below do not certify linguistic correctness.

'''
rendered = [header]
output_total = 0
for n in range(1, len(parts), 2):
    item, body = parts[n], parts[n+1]
    pieces = re.split(r'<!-- output: ([A-Z0-9-]+) -->', body)
    prompt = pieces[0].strip()
    # Preserve the complete actual prompt and local help while removing unrelated
    # teaching metadata; only the reviewer-owned witness is written.
    prompt = re.sub(r'\n?<!-- teaching: [^\n]+ -->\n?', '\n', prompt)
    prompt = re.sub(r'\n{3,}', '\n\n', prompt)
    ids = pieces[1::2]
    assert len(ids) == len(answers[item]), (item, len(ids), len(answers[item]))
    rendered += [f'## {item}\n\n<!-- item: {item} -->\n\n{prompt}\n\n']
    for j, oid in enumerate(ids):
        assert oid == f'{item}-O{j+1:03d}'
        remainder = pieces[2+2*j].strip()
        first_line = remainder.splitlines()[0] if remainder else ''
        label = first_line.split('____________________')[0].rstrip() if first_line.startswith('(') else ''
        answer = answers[item][j].strip()
        assert answer and '____________________' not in answer
        rendered.append(f'<!-- output: {oid} -->\n\n{label + " " if label else ""}{answer}\n\n')
        output_total += 1
assert output_total == 179
out = unicodedata.normalize('NFC', ''.join(rendered))
Path('chapters/ch16/independent-solutions.md').write_text(out, encoding='utf-8', newline='\n')
print('learner_sha256', sha)
print('items', len(actual_ids), 'outputs', output_total)
print('witness_sha256', hashlib.sha256(out.encode('utf-8')).hexdigest())
