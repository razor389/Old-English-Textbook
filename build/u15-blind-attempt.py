from pathlib import Path
import re, hashlib, unicodedata

# Independent responses composed from the learner master; no key/model import.
answers = {}
def put(task, *responses):
    if task in answers:
        raise ValueError(task)
    answers[task] = list(responses)

put('NEW-U15-F01',
    'ne eom', 'ne eart', 'nis', 'ne sindon', 'ne sindon', 'ne sindon',
    'næs', 'nǣre', 'næs', 'nǣron', 'nǣron', 'nǣron',
    'Six person/number positions in each of two tenses give twelve positions. Identical spellings do not erase the person, number or tense supplied by the subject and context. In the selected series ne stays separate in present first singular, second singular and all three plural persons; nis and the negative preterites are contracted.')
put('NEW-U15-F02',
    'næbbe', 'næfst', 'næfð', 'nabbað', 'nabbað', 'nabbað',
    'næfde', 'næfdest', 'næfde', 'næfdon', 'næfdon', 'næfdon',
    'I do not have (it): present denial of possession.',
    'They do not have (it): present denial of possession.',
    'I did not have (it): past denial of possession.',
    'They did not have (it): past denial of possession.')
put('NEW-U15-F03',
    'nelle', 'nelt', 'nele', 'nellað', 'nellað', 'nellað',
    'nolde', 'noldest', 'nolde', 'noldon', 'noldon', 'noldon',
    'Ic nelle gān: I am unwilling/refuse to go.',
    'Ðū nelt gān: you (singular) are unwilling/refuse to go.',
    'Ic nolde gān: I was unwilling/refused to go.',
    'Ðū noldest gān: you (singular) were unwilling/refused to go.')
put('NEW-U15-F04',
    'nān', 'nānes', 'nānum', 'nānne',
    'nāne', 'nānra', 'nānum', 'nāne',
    'nān', 'nānre', 'nānre', 'nāne',
    'nāna', 'nānra', 'nānum', 'nāna',
    'nān', 'nānes', 'nānum', 'nān',
    'nān', 'nānra', 'nānum', 'nān',
    'The head noun supplies gender and number; the phrase’s role or governing word supplies case. Nānum is dative throughout this four-case table, but can be masculine/neuter singular or any gender plural. Context chooses among those cells; it does not make every dative spelling a unique cell.')
put('NEW-U15-F05',
    'gehwā', 'gehwæs', 'gehwǣm', 'gehwone',
    'gehwæt', 'gehwæs', 'gehwǣm', 'gehwæt',
    'Personal gehwā distributes over persons one at a time; neuter gehwæt denotes everything. Both have singular grammar. Reference to a group of many does not create a plural declension, and personal reference has one common column rather than distinct masculine and feminine ones.')
put('NEW-U15-F06',
    'bōc', 'bēc', 'bēc', 'bōc', 'bēc', 'bōca', 'bōcum', 'bēc',
    'tōð', 'tōðes', 'tēð', 'tōð', 'tēð', 'tōða', 'tōðum', 'tēð',
    'Selected bēc changes ō to ē in genitive/dative singular and nominative/accusative plural. Selected tēð has the change in dative singular and nominative/accusative plural.',
    'Bōc is nominative or accusative singular; bēc has four possible cells. Tōð is nominative or accusative singular; tēð has three possible cells. The sentence distinguishes their roles. In these selected tables bōca/tōða are uniquely genitive plural, bōcum/tōðum dative plural, and tōðes genitive singular; variants do not cancel the distinctions of the selected table.')
put('NEW-U15-F07',
    'sweostor', 'sweostor', 'sweostor', 'sweostor', 'sweostor', 'sweostra', 'sweostrum', 'sweostor',
    'Sweostor has three distinct selected surfaces (sweostor, sweostra, sweostrum), versus four for bōc (bōc, bēc, bōca, bōcum).',
    'Sweostor itself covers all four singular cases and nominative/accusative plural. Syntactic role, agreement and context must still identify the cell: sameness of spelling is not sameness of grammatical function.')
put('NEW-U15-F08',
    'hǣtu', 'hǣte', 'hǣte', 'hǣte', 'hǣlu', 'hǣlu', 'hǣlu', 'hǣlu',
    'Hǣtu has nominative -u and selected oblique -e; hǣlu is unchanged in every selected singular case.',
    'Plural cells are outside the assigned meanings and recall scope. No count-plural sense of heat or salvation follows from the reference class strengu, and an unassigned cell is not a claim that no historical plural could exist.')
put('NEW-U15-F09',
    'gerēfa', 'gerēfan', 'gerēfan', 'gerēfan', 'gerēfan', 'gerēfena', 'gerēfum', 'gerēfan',
    'lēoðwyrhta', 'lēoðwyrhtan', 'lēoðwyrhtan', 'lēoðwyrhtan', 'lēoðwyrhtan', 'lēoðwyrhtena', 'lēoðwyrhtum', 'lēoðwyrhtan',
    'The compound has the weak masculine noun wyrhta as its final head. Add the weak endings after the whole lēoðwyrht- stem; lēoð- does not receive a second independent case ending.')

put('NEW-U15-A01',
    'Nān and ne.', 'No man comes: the assertion that any man comes is denied.',
    'Nǣfre and ne.', 'The king never came: there was no occasion on which he came.',
    'Nān, nāwiht and ne.', 'No man has anything: the clause denies any possession by any man, not merely possession of all things. All three negatives express the one denial.')
put('NEW-U15-A02',
    'Nā negates a contrasted participant; the assertion that I myself go remains affirmative.',
    'Ōðer, another person, is excluded in contrast with ic self.',
    'Ne negates the finite assertion ic gā: I do not go.')
put('NEW-U15-A03',
    'Interrogative hwā.', 'Who comes?', 'Hwā is the nominative subject of cymð.',
    'Indefinite hwā in a possible condition.', 'If anyone comes, I shall give him a book.', 'Hwā is subject of cume; ic is subject of the main-clause sęlle.',
    'Hwā is part of the free-choice frame swā hwā swā.', 'Whoever comes, I shall give him a book.', 'Hwā is subject of cume; ic is subject of sęlle, and him resumes the possible visitor as recipient.')
put('NEW-U15-A04',
    'Ǣlc distributes one penny to each individual man.',
    'Mann heads the nominative singular subject, so hæfð is third singular.',
    'Ealle gathers all the indicated men into the plural group said to have food.',
    'Męnn heads the nominative plural subject, so habbað is plural (third person here).')
put('NEW-U15-A05',
    'Ǣgðer ge … ge means both … and: I love both the king and his son.',
    'Ðone cyning, the accusative king.',
    'His sunu, his son, also accusative.',
    'Both are included; the statement does not select just one.')
put('NEW-U15-A06',
    'Man is the impersonal subject: one/people in general.',
    'Sceal is third-person singular.',
    'Se mann is the nominative singular subject referring to a particular man.',
    'Gǣð is third-person singular.',
    'The general human reference of impersonal man still has singular grammar and only the assigned nominative subject use. It does not supply a plural or oblique pronoun system; ordinary count mann has its separate noun inflection.')
put('NEW-U15-A07',
    'This book is as good as that book: equality in goodness.',
    'Sēo bōc, that book, is the equal-degree standard; “is good” is understood with it.',
    'I love light more than darkness: a preference for light.',
    'Ðīestru is the alternative object of the same loving, accusative like lēoht; ðonne does not make it nominative.',
    'The larger this book is, the better it is: corresponding increases of degree.',
    'Swā hēo bętere is correlates with swā ðēos bōc māre is; hēo refers to the feminine book. These clauses do not assert equal size and goodness.')
put('NEW-U15-A08',
    'Hwā is nominative, as subject of cume in the free-choice clause.',
    'Him is dative, the recipient of the book in the main clause.',
    'The explicit him resumes the same person with the case required by sęlle. The subject need not become dative merely because its referent receives the gift.')
put('NEW-U15-A09',
    'Uncer is the personal genitive “of us two,” identifying the group from which one is selected.',
    'Uncer is the possessive “our (two people’s),” agreeing with subject hūs in nominative neuter singular.',
    'Ānum is dative singular, because the selected person is the recipient of a gift.',
    'The selected group contains two people: the personal pronoun is dual. Only one of the two is selected by ānum.')
put('NEW-U15-A10',
    'Does he have anything? An information-seeking question.',
    'He has nothing. A denial of possession.',
    'He has something. An assertion of possession.',
    'Nāwiht specifies that no thing is possessed, and finite ne marks negation of hæfð. They form negative concord, one denial, without turning it into a positive assertion.')
put('NEW-U15-A11',
    'Indefinite ān: a certain/unnamed man came, introducing a visitor.',
    'Cardinal ān: one man came, in contrast with two.',
    'Both senses modify the same masculine singular nominative subject mann and therefore use the same strong nominative masculine singular ān. Discourse distinguishes the meanings.')
put('NEW-U15-A12',
    'hēafd-', 'hēafdu', 'fōtsceamul-',
    'Hēafod loses its unstressed o before an ending, but fōtsceamul keeps the u of the final element -sceamul-. Blanket deletion would wrongly yield a stem such as fōtsceaml-; the long vowel in fōt- is not a rule for deleting every later medial vowel.')

put('NEW-U15-C01', 'Nān mann ne hæfð bōc; gehwā hæfð męte.')
put('NEW-U15-C02', 'Ic næfde ðā bōc, and ic nolde gān.')
put('NEW-U15-C03', 'Hæfð se cyning ǣnige bōc? Hē nāne bōc ne hæfð.')
put('NEW-U15-C04', 'Gif hwā bōc hæbbe, ic him pęning sęlle.')
put('NEW-U15-C05', 'Swā hwā swā gā, ic him pęning sęlle.')
put('NEW-U15-C06', 'Swā hwæðer ðissa twēgra suna swā ǣrest cume, ic him ðā bōc sęlle.')
put('NEW-U15-C07', 'Man mæg gān.')
put('NEW-U15-C08', 'Ǣlc sunu hæfð āne bōc; ealle ðā suna habbað męte.')
put('NEW-U15-C09', 'Ic gesēo ǣgðer ge ðone cyning ge his sunu.')
put('NEW-U15-C10', 'Swā ðæt hūs māre is, swā hit bętere is.')
put('NEW-U15-C11', 'Ðēos bōc is swā gōd swā sēo bōc, ac ðæs cyninges bōc is bętere.')
put('NEW-U15-C12', 'Hē lufað męte swīðor ðonne wīn.')
put('NEW-U15-C13', 'Ne gā; sęle ðǣm ðearfan ðā bōc. Here ðearfa is the earlier noun “poor person”; ðǣm is its dative singular determiner.')
put('NEW-U15-C14', 'Hē self gǣð, and nā ōðer.')
put('NEW-U15-C15', 'Ic nāwiht nānum ne sęlle.')
put('NEW-U15-C16', 'Nānes mannes sunu ne cymð.')
put('NEW-U15-C17', 'Se cyning næfð nāna bēc.')
put('NEW-U15-C18', 'Se cyning gesiehð gehwone; gehwæs sunu is gōd.')
put('NEW-U15-C19', 'Ān mann cōm, and hē hæfde bōc.')

put('EX-IX-28-01',
    'Ǣlc ðe for mīnum naman his hūs oððe his brōðor oððe his sweostor oððe his fæder oððe his mōdor oððe his wīf oððe his bearn oððe his land forlǣtt, him mid hundtēontigum forgolden bið, and hē ðǣr-tō-ēacan ēce līf hæfð.\n\nThe initial ǣlc is resumed by him; the supplied repayment clause ends in bið. Brōðor, sweostor, bearn and land are plural accusatives here; fæder, mōdor and wīf are singular. Both promised results are retained.')
put('EX-IX-28-02', 'Hē sealde gehwǣm pęning wið his dæges weorce.')
put('EX-IX-28-03', 'Hē sęnde hīe on his wīngeard.')
put('EX-IX-28-04', 'Hē geseah ōðre on strǣte standende īdle.')
put('EX-IX-28-05', 'Ðā cwæð hē: “Gāð gē ēac on mīnne wīngeard, and ic ēow sęlle ðæt riht is.” The supplied ðæt introduces “what is right”; no interrogative hwæt is substituted.')
put('EX-IX-28-06', 'Ęft ēode hē ūt ymbe ðā siextan and nigoðan tīd, and dyde gelīce.')
put('EX-IX-28-07', 'Ðā ymbe ðā endleftan tīd ēode hē ūt, and fand ōðre standende.')
put('EX-IX-28-08', 'Ðā cwæð hē: “Hwȳ standað gē hēr ealne dæg īdle?”')
put('EX-IX-28-09', 'Ðā cwǣdon hīe: “For-ðon-ðe nān mann ūs ne hȳrode.”')
put('EX-IX-28-10', 'Sōðlice ðā hit ǣfen geworden wæs, ðā cwæð ðæs wīngeardes hlāford tō his gerēfan: “Cleopa ðā wyrhtan, and forgield him hiera mēde.”')
put('EX-IX-28-11', 'Eornostlice ðā ðā cōmon ðe ymbe ðā endleftan tīd cōmon, ðā onfēngon hīe ǣlc his pęning. The relative clause ends in cōmon; onfēngon agrees with hīe while ǣlc his pęning distributes the payment.')
put('EX-IX-28-12', 'And ðā ðe ðǣr ǣrest cōmon wēndon ðæt hīe māre onfōn sceolden. Sceolden expresses the expected outcome in the past report, not a duty to receive.')

put('EX-IX-29-01', 'Ðū dydest hīe ūs gelīce, ðe hęfignessa on ðisses dæges hǣte bǣron. The relative refers to ūs; gelīce is an accusative plural predicate agreeing with hīe, while ūs is the dative comparison standard.')
put('EX-IX-29-02', 'Nim ðæt ðīn is, and gā; ic ðissum eall swā micel sęlle swā ðē. Both ðissum and ðē are dative recipients, with the second giving understood.')
put('EX-IX-29-03', 'Ne mōt ic dōn ðæt ic wille? I take “may” as permission; mæg would instead foreground ability.')
put('EX-IX-29-04', 'Ne cōme ðū tō mē tō wyrceanne wið ānum pęninge?')
put('EX-IX-29-05', 'Hē wæs wer and wītga, mihtig on worde and on weorce beforan Gode and eallum folce.')
put('EX-IX-29-06', 'Ðæt is se dōm, ðæt lēoht cōm on woruld, and męnn lufodon ðīestru swīðor ðonne ðæt lēoht, for-ðon-ðe hiera weorc yfel wǣron. Yfel is the selected strong neuter plural predicate agreeing with weorc.')
put('EX-IX-29-07', 'God ne sęnde his sunu on woruld ðæt hē ðā woruld dēmde, ac ðæt sēo woruld ðurh hine hǣled wǣre. The contrasting purposes fix the scope: the sending occurred, but its purpose was salvation rather than condemnation. Dēmde and wǣre are past subjunctives in the purpose clauses.')
put('EX-IX-29-08', 'Ēower mēd bið miclu, and gē bēoð ðæs Hēahstan bearn, for-ðon-ðe hē is gōd ofer ungeðancfulle and yfele. Miclu is feminine nominative singular with mēd; the two substantival objects after ofer are accusative plural.')
put('EX-IX-29-09', 'Giefað, and ēow bið giefen. I take the address as plural, as in the surrounding sayings; singular Gief, and ðē bið giefen conveys the same saying to one addressee where the English does not fix number.')
put('EX-IX-29-10', 'Se leornungcniht nis ofer his lārēow.')
put('EX-IX-29-11', 'Ætīew ūs ðīne mildheortnesse, and unne ūs ðīnre hǣlu. The second-person subjunctive unne serves as the addressed command; its granted thing is genitive.')

put('EX-IX-30-01', 'Ne swęre ðurh heofon, for-ðon-ðe hē is Godes setl; ne ðurh eorðan, for-ðon-ðe hēo is his fōtsceamul; ne ðurh Hierusalem, for-ðon-ðe hēo is mǣres cyninges burg. The oath standards are accusative, and each later ne shares the initial command. Hē refers to masculine heofon; hēo refers to feminine earth/city.')
put('EX-IX-30-02', 'Ne swęre ðurh ðīn hēafod, for-ðon-ðe ðū ne meaht ān hǣr hwīt oððe blæc wyrcean.')
put('EX-IX-30-03', 'Sīe ēower word ðus: “Hit is; hit nis.” Sīe is a third-singular wish about word, although the possessors addressed are plural.')
put('EX-IX-30-04', 'Gē hīerdon ðæt cweden wæs: “Ēage for ēagan, and tōð for tēð.” The first noun in each exchange is nominative, the noun after for dative.')
put('EX-IX-30-05', 'Se ðe ān of ðissum lǣstum bebodum tōwierpð and męnn swā lǣrð, sē bið lǣst hāten on heofona rīce. The teaching clause ends in its verb lǣrð. Ān is accusative neuter singular; its of-group is dative plural.')
put('EX-IX-30-06', 'Se ðe hit dēð and lǣrð, sē bið micel hāten.')
put('EX-IX-30-07', 'Gē hīerdon ðæt on ealdum tīdum cweden wæs: “Ne sleah.”')
put('EX-IX-30-08', 'Is hit ðīn eorðe? Ðīn agrees with nominative feminine singular eorðe; the endingless feminine form is still agreement.')
put('EX-IX-30-09', 'Hē hæfð æt his gewinne ðæt hē mæg.')
put('EX-IX-30-10', 'Sēo sunne forbærnde his feld.')
put('EX-IX-30-11', 'Ðā wegas sculon blōstmian, ðā wegas sculon blōstmian; swā fægeru brȳd sceal hiere hām forlǣtan.\n\nAttempt with reservation: I understand “should” as a present expectation/obligation, hence sculon rather than a report of past obligation. The prompt gives no wider setting to settle a contrary-to-fact reading (sceoldon) or a wished-for one (for example scylen). The newly supplied blōstmian covers both “blossom” and “bloom”. Fægeru is the selected strong feminine nominative singular; hām is an accusative noun.')
put('EX-IX-30-12', 'Gif hīe magon, lǣt hīe libban būtan mē. This follows the supplied permission construction. Gif hīe magon, libben hīe būtan mē would be an optative alternative, not the same construction.')
put('EX-IX-30-13', 'Hē nǣfre ne forlǣtt ðā ðe on hine gelīefað. I take “trust in” as the confidence/belief expressed by the earlier gelīefan on + accusative frame, rather than adding an untaught verb.')

put('EX-X-XI-31-01', 'Ic wāt sōðlice ðæt mīn Ālīesend leofað.')
put('EX-X-XI-31-02', 'On mīnum flǣsce ic God gesēo, ic self, and nā ōðer. Gesēo has future reference in the promise; nā excludes another observer rather than negating my seeing.')
put('EX-X-XI-31-03', 'Hē wæs lǣred Godes willan tō dōnne.')
put('EX-X-XI-31-04', 'Ne lǣd ūs on costnunge, ac ālīes ūs fram yfele.')
put('EX-X-XI-31-05', 'Sīe ðīn nama gehālgod.')
put('EX-X-XI-31-06', 'Geweorðe ðīn willa on eorðan swā-swā on heofonum.')
put('EX-X-XI-31-07', 'Nān Engla cyning næs swā micel swā Ælfred.')
put('EX-X-XI-31-08', 'Hē feaht wið Dęnum; hē dēmde his folc; hē geworhte āwęndednessa of Lǣdene; hē wæs lēoðwyrhta.')
put('EX-X-XI-31-09', 'His mōdor hātte Osburg, and his fæder Æthelwulf. The naming verb is understood again in the second clause; supplied hātte is passive naming, not active hēt.')
put('EX-X-XI-31-10', 'Hē lifde twā and fīftig gēara.')
put('EX-X-XI-31-11', 'Hē leornode bēcrǣdinge æfter ðǣm ðe hē twęlf wintra eald wæs.')
put('EX-X-XI-31-12', 'His mōdor hæfde bōc Engliscra lēoða, ðā hēo gehēt swā hwæðrum hiere twēgra suna swā hīe ǣrest leornode. The supplied attracted recipient hwæðrum is retained, and leornode has the supplied prospective subjunctive sense. Feminine hīe is the book being learned.')
put('EX-X-XI-31-13', 'Ælfred āscode hīe: “Wilt ðū sōðlice ðā bōc ānum uncer sęllan, ðǣm ðe hīe ǣrest ongiett?” Uncer selects from the two speakers’ group; ðǣm is appositional to the dative recipient ānum, while relative ðe is subject of ongiett.')
put('EX-X-XI-31-14', 'Asser, Ælfredes bisceop, wrāt bōc ðæs cyninges līfes.')

put('NEW-U15-D01',
    'He withheld the Savior’s goods, neglecting the gift entrusted to him rather than using it generously; he refused to remember the promised reward for doing good in the Savior’s name.',
    'The Savior will remove him from his bounty, and the rich man will become a pauper in worldly life.',
    'The giver’s good deed will be repaid a hundredfold; giving to one of the least counts as giving to the Savior, who promises eternal bliss in heaven in return.',
    'The Savior speaks to the rich man (ðǣm wlancan). Within the embedded gospel saying, the speaker addresses the plural gē/ēow, the people giving to the least.')
put('NEW-U15-D02',
    'Noldest is negative willan, preterite indicative second singular: “you would not/refused.” It governs plain infinitive geðęncean, “remember/bear in mind”: why did you refuse to remember?',
    'Ic wille states the present speaker’s continuing intention to repay. Embedding that intention in what the man should have remembered does not require mechanical past-tense backshift; the present promise remains in force.')
put('NEW-U15-D03',
    'Swā-hwæt-swā: whatever the addressees give, an accusative neuter free-choice object of sęllað.',
    'Ānum of mīnum ðǣm lǣstum: to one of the speaker’s least ones.',
    'Mē: the Savior himself, the recipient whom giving to the least benefits.',
    'Hit resumes the thing given as the accusative object of the second sęllað.')
put('NEW-U15-D04',
    'Ānum is dative singular as recipient. Of governs the dative plural group mīnum ðǣm lǣstum; lǣstum is substantival “least ones.” The phrase selects one recipient from that group; this of-group is not a genitive merely because its meaning is partitive.',
    'Wið governs dative singular ðǣm: “in return for that,” referring to the gift/deed. It expresses reciprocal reward, not selection of one member from a group.')
put('NEW-U15-D05',
    'The Savior said to the rich man: “Why were you so tenacious of my goods, which I gave you? Why did you neglect the gift which I gave you? I shall now remove you from my bounty, which I granted you; then you will be a pauper in worldly life. Why did you refuse to remember that I intend to recompense each person for a good deed that one does for my name’s sake? I shall repay it to him a hundredfold, as it is stated and said in my Gospel: ‘Whatever you give to one of my least ones, you always give it to me, and in return for that I shall give you eternal bliss in heaven.’\n\nThe outer speech remains open, as in this bounded selection; the embedded saying ends here. “Stated and said” retains the two participles without making two different gospel statements.')

put('NEW-U15-P01',
    'Word be worde: verbal correspondence, word for word.',
    'Andgiet of andgiete: correspondence of meaning, sense for sense.',
    'Various and manifold worldly cares troubled Alfred both mentally and physically; the cares affecting the kingdoms he governed were very hard to count.',
    'After studying the book and translating it from Latin into English discourse/prose, he subsequently made it into verse.',
    'He asks each willing reader to pray for him and not blame him if the reader understands it more correctly than Alfred could, since people work within their understanding and available leisure.')
put('NEW-U15-P02',
    'Hē before gebidde is the prospective reader.',
    'Hine after for is Alfred, for whom the reader is to pray.',
    'Him before ne wīte is Alfred, whom the reader is asked not to blame.',
    'Hē after gif is the reader.',
    'Hē after ðonne is Alfred.',
    'The comparison contrasts a reader’s possibly more correct understanding with what Alfred could understand/render. The two hē tokens do not name the same subject despite their identical spelling.')
put('NEW-U15-P03',
    '“Both in mind and in body”: ǣgðer ge … ge coordinates the two on + dative expressions on mōde and on līchaman, including both spheres of affliction.',
    'Ðā bisga, “the cares,” is the main nominative plural subject; sind is the finite plural verb. Ūs is the dative person for whom they are hard to count, and swīðe earfoðrīme is their predicate.',
    'Ðe on his dagum on ðā rīcu becōmon: “which befell those kingdoms in his days.” The antecedent is the cares, and relative ðe is subject of plural becōmon; the kingdoms are the goal after on.',
    'Ðe hē underfangen hæfde: “which he had received/taken charge of.” The antecedent is ðā rīcu, and relative ðe is object of underfangen; Alfred is hē, subject of singular hæfde.')
put('NEW-U15-P04',
    'Rihtlicor compares how correctly the reader may understand the book with how correctly Alfred could. After ðonne hē meahte, “understand it” (at that degree of correctness) is understood; the text does not compare their moral worth.',
    'Ne negates wīte, “blame,” in the requested subjunctive clause. “And not blame him” continues the request introduced by ðæt and coordinated with “pray for him”; it is not an assertion that the reader already does not blame Alfred.')
put('NEW-U15-P05',
    'King Alfred was the translator of this book, and translated it from book-Latin into English, as it is now arranged. Sometimes he set word for word, sometimes sense for sense, as he could then explain it most clearly and most intelligibly, limited by the various and manifold worldly cares that often troubled him both in mind and in body. The cares that befell, in his days, the kingdoms he had taken charge of are very hard for us to count; and nevertheless, when he had studied this book and translated it from Latin into English prose, he then made it subsequently into verse, as it is now arranged.\n\nAnd now he asks, and for God’s name’s sake entreats, each of those whom it may please to read this book to pray for him, and not blame him if the reader understands it more correctly than Alfred could; because each person must, according to the measure of his understanding and according to his available leisure, speak what he speaks and do what he does.\n\n“Prose” renders the English spelle in its contrast with the following verse; “English discourse” would keep the more literal lexical sense. The reader and Alfred are named in the comparison to preserve the distinct referents of hē.')

put('NEW-U15-R01',
    'gewissie', 'Present subjunctive, second singular, in the requested ðæt clause.', 'That you guide me better than my conduct towards you has deserved.',
    'gewissa', 'Imperative, second singular.', 'Guide me according to your will and for my soul’s benefit, better than I myself may know.',
    'gestaðela', 'Imperative, second singular.', 'Establish/make steadfast my mind according to your will and for my soul’s benefit.',
    'gestranga', 'Imperative, second singular.', 'Strengthen me against the devil’s temptations.',
    'āfierr', 'Imperative, second singular.', 'Remove from me foul lust and every unrighteousness.',
    'gescield', 'Imperative, second singular.', 'Protect me against my visible and invisible adversaries.',
    'tǣc', 'Imperative, second singular.', 'Teach me to do your will.')
put('NEW-U15-R02',
    'For introduces grounds of entreaty: by/for the sake of God’s great mercy, the holy cross’s sign, Saint Mary’s virginity, Saint Michael’s obedience, and all God’s saints’ love and their merits. These are the grounds on which the speaker appeals for guidance.',
    'For governs dative singular tācne, “by the sign.” The whole ðǣre hālgan rōde is genitive singular, “of the holy cross,” dependent on tācne. The preposition does not directly govern rōde in this phrase.')
put('NEW-U15-R03',
    'First standard: ic āworhte tō ðē, what the speaker has deserved by his conduct towards God. He requests better guidance/treatment than his merits warrant.',
    'Second standard: ic self cunne, what the speaker himself may know. He requests guidance for God’s will and his soul’s good beyond his own knowledge.',
    'Cunne is present subjunctive first singular of cunnan, “than I myself may know,” in the comparison accompanying the petition. It does not simply assert the extent of his knowledge, and it is not a past indicative. The exact omitted content is understood from the guidance sought; “know how to direct myself” is an interpretive expansion, not an extra written verb.')
put('NEW-U15-R04',
    'Ic, the praying speaker, is the actor who would love; ðē is God, the person loved and the prayer’s addressee.',
    'Mæge is present subjunctive first singular; lufian is its plain infinitive.',
    'Purpose: the requested teaching/guidance is so that the speaker may love God fervently above all things.',
    'Lof and wuldor are the things wished to be God’s; ðē is dative God, the recipient of praise and glory. God remains the addressee, not the grammatical subject of a second-person command.',
    'Sīe is present subjunctive, singular, used optatively.',
    'An independent concluding wish/doxology: may praise and glory be to you now and for ever. It is not another subordinate purpose clause.')
put('NEW-U15-R05',
    'Lord, almighty God, Maker and Ruler of all created things, I beseech you by your great mercy, and by the sign of the holy cross, and by Saint Mary’s virginity, and by Saint Michael’s obedience, and by the love of all your saints and their merits, that you guide me better than I have deserved by my conduct towards you. And guide me according to your will and for my soul’s benefit, better than I myself may know; and establish my mind according to your will and for my soul’s benefit; and strengthen me against the devil’s temptations; and remove from me foul lust and all unrighteousness; and protect me against my adversaries, visible and invisible; and teach me to do your will, so that I may love you fervently above all things, with pure thought and with a pure body.\n\nBecause you are my Creator and my Redeemer, my Help, my Comfort, my Trust and my Hope. May praise and glory be to you now and ever, ever, ever, for ever without any end. Amen.')

student = Path('chapters/ch15/student.md')
student_bytes = student.read_bytes()
student_sha = hashlib.sha256(student_bytes).hexdigest()
assert student_sha == '6caabca8c79ff4ce94beb1ce5c059b0f6cda65427b434bb11a042971b2e0df33', 'Learner master changed during blind solve'
text = student_bytes.decode('utf-8')
items = list(re.finditer(r'<!-- item: ([^ ]+) -->', text))
assert len(items) == 105
header = f'''# Unit 15 — independent blind solutions

Solver: unit15_blind, a fresh non-author. These are initial attempted answers, not an accepted review or a certification of the supplied teaching. Completed from the actual learner master, its visible helps, and targeted checks in accepted earlier learner masters and the actual fourteen-unit registers. No Unit 15 key, coverage contract, brief, audit/model metadata, token maps, translation witnesses or author helpers were opened. No contact with the paradigm reviewer.

Learner file: chapters/ch15/student.md
Learner SHA256: `{student_sha}`
Lexicon SHA256 at consultation: `673e3982d8af0cc5784a781e390cb1eba06b67aeed56d9acaa45412bd1ed89f8`
Grammar register SHA256 at consultation: `9b799a32b858fbce8ae5b8f38954e4b6a486f8abc245e51818bff17e86630040`

Every requested output is attempted below in actual learner order. An output number matches its printed response-grid or response-list number, not its position across a table row. Forms were solved with the displayed selected systems available; the witness does not claim source-image verification of every paradigm. Source exercises are new answers to Cook’s preserved prompts. Reading translations were composed independently from the actual Old English with the learner’s local support. Reservations and alternative readings are recorded beside the affected answers. The freeze begins on submission to the coordinator; subsequent comparison must leave this witness unchanged.

'''
parts = [header]
seen = []
total = 0
for i, item in enumerate(items):
    task = item.group(1)
    end = items[i+1].start() if i+1 < len(items) else len(text)
    outputs = re.findall(r'<!-- output: ([^ ]+) -->', text[item.end():end])
    response = answers[task]
    assert len(response) == len(outputs), (task, len(response), len(outputs))
    parts.append(f'## {task}\n\n<!-- item: {task} -->\n\n')
    for output, answer in zip(outputs, response):
        assert answer.strip()
        parts.append(f'<!-- output: {output} -->\n\n{answer}\n\n')
    seen.append(task)
    total += len(outputs)
assert set(seen) == set(answers), (set(seen)-set(answers), set(answers)-set(seen))
assert total == 322, total
result = unicodedata.normalize('NFC', ''.join(parts))
target = Path('chapters/ch15/independent-solutions.md')
target.write_text(result, encoding='utf-8', newline='\n')
print(f'{len(seen)} tasks; {total} attempted outputs; 116 morphology cells.')
print('student_sha256=' + student_sha)
print('witness_sha256=' + hashlib.sha256(target.read_bytes()).hexdigest())

