"""Initial Unit15 key assembly after contract ff7f7c8; never rerun over reviewed prose."""
import json
from pathlib import Path
import unicodedata

ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
c=read('chapters/ch15/coverage.json')
assert c['contract_prepared_before_prose'] and c['status']=='contracted_before_prose'
dest=ROOT/'chapters/ch15/answer-key.md'
assert not dest.exists(),'Do not overwrite an authored/reviewed key'
tasks={t['task_id']:t for t in c['assigned_items']}
matrices={m['matrix_id']:m for m in c['display_plan']['matrices']}
comps={s['owner_id']:s['text'] for s in read('curriculum/proposals/unit15/author-only-sequence-bindings.json')['sequences']}
cook={s['owner_id']:s['text'] for s in read('curriculum/proposals/unit15/author-only-cook-sequence-bindings.json')['sequences']}
out=['# Unit 15 — Answer key','',
 'The Old English composition answers are new teaching material. The three reading translations render the wording printed by Cook. A model gives one defensible answer; the notes distinguish its grammatical target from other valid language.','',
 'Preserve the meaning, case relations, agreement, tense and clause connections. Cook’s explicit lexical hints, omissions and word-order controls are separate requirements. Original composition directions likewise name their required patterns. Elsewhere, a different grammatical order or an evidenced spelling variant is acceptable. Supplied expressions and reading helps remain available during the tasks; their unaided recall is not required.','',
 'N = nominative, G = genitive, D = dative, A = accusative. Complete tables below answer each requested position, including positions whose spellings coincide. Negative concord normally requires one negative English proposition, rather than a word-for-word accumulation of English negatives.','']
seen=[];outputs=[]
def para(text):out.extend([text,''])
def heading(text):para('## '+text)
def item(tid,label,model=None):
    t=tasks[tid];seen.append(tid)
    para('### '+label)
    para('<!-- key: '+t['key_id']+' -->')
    if model is not None:para(model)
    # These locators attach every response position to the following solution.
    # The human reviewer must still verify the actual answers, not just IDs.
    for p in t['output_positions']:
        out.append('<!-- output: '+p['output_position_id']+' -->');outputs.append(p['output_position_id'])
    out.append('')
def table(headers,rows):
    out.append('| '+' | '.join(headers)+' |')
    out.append('| '+' | '.join('---' for _ in headers)+' |')
    out.extend('| '+' | '.join(row)+' |' for row in rows);out.append('')
def matrix(mid,singular=False):
    m=matrices[mid]
    if singular:table(m['headers'][:2],[r[:2] for r in m['rows']])
    else:table(m['headers'],m['rows'])

heading('F. Complete forms')
form_answers={
 'F01':(['NEW-U15-PAR-WESAN-NEG-IND-DISPLAY'],
  'There are six person/number positions in each of two tenses. Identical plural forms do not erase those distinctions. Present **ne eom**, **ne eart** and **ne sindon** contain two words; **nis** and the displayed negative preterites are contractions. The table covers the eom/wæs series.',
  'Uncontracted ne with the corresponding positive verb can express valid negation, but this task explicitly requests the selected contractions where available. **Nis** is third singular, not an all-purpose negative form.'),
 'F02':(['NEW-U15-PAR-NABBAN-IND-DISPLAY'],
  'Present: **næbbe**, “I do not have (it)”; **nabbað**, “they do not have (it)”. Preterite: **næfde**, “I did not have (it)”; **næfdon**, “they did not have (it)”. The understood object depends on the context; these forms deny possession.',
  'Keep present **næfst/næfð** distinct from past **næfdest/næfde**. A separate-ne construction may be grammatical but does not supply the requested nabban paradigm.'),
 'F03':(['NEW-U15-PAR-WILLAN-NEG-IND-DISPLAY'],
  'With going as the complement: **nelle**, “I am unwilling/refuse to go”; **nelt**, “you singular are unwilling/refuse to go”; **nolde**, “I was unwilling/refused to go”; **noldest**, “you singular were unwilling/refused to go”. The forms express unwillingness here, rather than merely predicting that no going will occur.',
  'Cook also records the y-series and variation in single/double l. Those are genuine alternatives, but the exercise requests the displayed e-series. Do not use the past **nolde** for every present refusal.'),
 'F04':(['NEW-U15-PAR-NAN-STRONG-NGDA-DISPLAY'],
  '**Nānum** is D singular masculine or neuter, or D plural of any gender. The noun and clause determine which position is intended. A repeated ending is not a unique gender/number label.',
  'The target is the complete strong N/G/D/A system. In clauses, the negative noun phrase can combine with finite ne or a contracted negative verb to express one denial.'),
 'F05':(['NEW-U15-PAR-GEHWA-SINGULAR-NGDA-DISPLAY'],
  '**Gehwā** distributes over persons, **gehwæt** over things. Their potentially numerous referents do not make the pronoun grammatically plural. This defined system has personal and neuter singular columns.',
  'Distinguish personal A **gehwone** from N **gehwā**; G **gehwæs** and D **gehwǣm** serve both columns. No plural is to be invented from an English gloss such as everyone.'),
 'F06':(['NEW-U15-NOM-BOC-DISPLAY','NEW-U15-NOM-TOTH-DISPLAY'],
  '**Bōc** has **bēc** in G/D singular and N/A plural; G/D plural return to **bōca/bōcum**. **Tōð** has **tēð** in D singular and N/A plural, but **tōðes** in G singular and **tōða/tōðum** in G/D plural. The two vowel patterns are not identical.',
  'For example, **bēc** alone has four possible positions, whereas **bōcum** identifies D plural within this table. **Tēð** can be D singular or N/A plural. Sentence function resolves a syncretic spelling; do not assign every front-vowel form the same case.'),
 'F07':(['NEW-U15-NOM-SWEOSTOR-DISPLAY'],
  'The selected table has three distinct surfaces: **sweostor**, **sweostra**, **sweostrum**. Bōc has four: bōc, bēc, bōca, bōcum. **Sweostor** occupies all four singular positions and N/A plural.',
  'Case still follows the phrase’s role: an object sweostor is accusative even though its spelling is also nominative. The number of endings is not the number of grammatical cases. Documented variants remain possible, but this task asks for the selected table.'),
 'F08':(['NEW-U15-NOM-HAETU-DISPLAY','NEW-U15-NOM-HAELU-DISPLAY'],
  'The selected **hǣtu** singular has nominative -u and oblique -e. **Hǣlu** is invariant in the selected singular system. The attested alternatives listed in the lesson remain alternatives; the present form task asks for its selected spellings.',
  'The unassigned plural slots mark a teaching and sense limit. They neither establish count meanings such as separate salvations/heats nor assert that no historical plural ever occurred. The full strengu class reference shows class morphology without assigning those meanings to hǣlu or hǣtu.'),
 'F09':(['NEW-U15-NOM-GEREFA-DISPLAY','NEW-U15-NOM-LEOTHWYRHTA-DISPLAY'],
  'Both nouns have weak masculine endings: nominative singular -a, other singular cases -an, plural N/A -an, G -ena, D -um. In **lēoðwyrhta**, the head is wyrhta and the ending belongs at the end of the whole compound.',
  '**Lēoð-** remains the fixed first element. Do not give it a separate case ending or confuse **lēoðwyrhtena** with the dative plural **lēoðwyrhtum**.'),
}
for code,(mids,explanation,grading) in form_answers.items():
    item('NEW-U15-'+code,code)
    for mid in mids:
        para('**'+matrices[mid]['title'].split(' — ')[0]+'**')
        matrix(mid,singular=code=='F08')
    para(explanation);para(grading)

heading('A. Analysis')
analyses={
'A01':('1. **Nān** and **ne**: “No man comes.” The denial excludes any person’s coming.\n\n2. **Nǣfre** and **ne**: “The king never came.” The denial covers every occasion in the relevant past.\n\n3. **Nān**, **nāwiht** and **ne**: “No man has anything.” The negative expressions reinforce one denial; they do not affirm possession.',
 '“Nobody comes” and “nobody has anything” are idiomatic alternatives. Turning the third clause into a positive statement loses its essential meaning.'),
'A02':('**Ic self gā, and nā ōðer** affirms the speaker’s going and excludes **ōðer**, another person, as the goer. **Nā** negates that contrasted participant. **Ic ne gā** instead denies the speaker’s going: finite **ne** negates the proposition.',
 '“I myself go, and no one else” and “I do not go” preserve the distinction. Do not translate the first clause as the speaker’s refusal or failure to go.'),
'A03':('1. **Hwā cymð?**: interrogative, “Who comes?” Hwā is the nominative singular subject.\n\n2. **Gif hwā cume, ic him bōc sęlle**: indefinite, “If anyone comes, I shall give him a book.” Hwā is the subordinate subject; ic is the main subject.\n\n3. **Swā hwā swā cume, ic him bōc sęlle**: free choice, “Whoever comes, I shall give him a book.” Hwā again supplies the subordinate subject, ic the main subject.',
 '“If someone comes” is possible for the indefinite clause. The repeated swā marks the unrestricted choice in the third; it is not another question asking the person’s identity.'),
'A04':('**Ǣlc mann** treats the men one by one: each has one penny. The head mann is singular and takes **hæfð**. **Ealle ðā męnn** includes the entire group: all the men have food. The head męnn is plural and takes **habbað**.',
 'The two statements do not make the same distribution claim. Collective all does not itself say that each member has exactly one item.'),
'A05':('**Ǣgðer ge … ge** includes both objects: **ðone cyning**, accusative masculine singular, and **his sunu**, accusative masculine singular. His identifies the king as the son’s possessor. The meaning is “I love both the king and his son.”',
 'The relation is inclusive, not an exclusive choice of one object. The two ge elements are paired coordinators here.'),
'A06':('**Man sceal gān** means “One must go” or “People must go”: impersonal man supplies a generic subject, with third-singular **sceal**. **Se mann gǣð**, “The man goes”, identifies a particular person; **gǣð** is also third singular.',
 'The generic use is a nominative-singular subject expression. It introduces no new oblique or plural pronoun paradigm. English “people” in the translation does not change the Old English verb to a plural.'),
'A07':('1. **Ðēos bōc is swā gōd swā sēo bōc**: equality, “This book is as good as that book.” Sēo bōc is the standard after the second swā, with is gōd understood.\n\n2. **Ic lufie lēoht swīðor ðonne ðīestru**: preference, “I love light more than darkness.” Darkness is the contrasted object, accusative like light.\n\n3. **Swā ðēos bōc māre is, swā hēo bętere is**: proportion, “The larger this book is, the better it is.” Each correlated clause has its own subject and comparative predicate.',
 'The proportional statement connects two degrees; it does not call size and goodness equal. In the second clause “rather than” can express the preference, provided the two objects remain clear.'),
'A08':('**Hwā** is nominative, as subject of **cume** within the free-choice clause. **Him** is dative, as recipient with **sęlle** in the main clause. The two forms refer to the same possible person but perform different grammatical jobs.',
 'The explicit main-clause pronoun keeps those jobs separate. Making hwā dative simply because that person later receives the gift would miss the task’s internal-case construction.'),
'A09':('In **ānum uncer**, **ānum** is dative singular because the setting makes the selected person a recipient. **Uncer** is the personal genitive dual, “of us two”, naming the group from which that one is chosen.\n\nIn subject **uncer hūs**, **uncer** is the agreeing possessive, nominative neuter singular, “our house” belonging to the two of us. The dual identifies the possessors, not two houses.',
 'The identical spelling does not erase the distinction between a personal genitive dependent on ānum and a possessive agreeing with hūs.'),
'A10':('1. **Hæfð hē āwiht?** — “Does he have anything?” A question about possession.\n\n2. **Hē nāwiht ne hæfð.** — “He has nothing” or “He does not have anything.” A denial of possession.\n\n3. **Hē hæfð hwæthwega.** — “He has something.” A positive assertion.',
 '**Nāwiht** and finite **ne** express a single negative in the middle clause. The supplied meanings may be consulted; the task does not require memorizing the two supplied indefinite expressions.'),
'A11':('In the story opening, **ān** introduces “a certain man”, an unnamed new participant. In the numerical contrast it means “one man”, as opposed to two. In both settings it agrees with nominative masculine singular **mann**.',
 'Context changes the sense, not the agreement. “A man came” is idiomatic for the first setting; a translation of the second must retain the explicit numerical contrast.'),
'A12':('The ending-bearing stem of **hēafod** is **hēafd-**, as in hēafdes, hēafde, hēafda and hēafdum. Its selected N/A plural is **hēafdu**. The displayed **fōtsceamul-** retains its medial vowel before the endings.',
 'These lexical diagnostics govern the selected forms. Deleting every medial vowel would fail to produce the fōtsceamul table; it is not a general operation licensed by the word’s length.'),
}
for code,(answer,note) in analyses.items():item('NEW-U15-'+code,code);para(answer);para(note)

heading('C. Original composition')
composition_notes={
'C01':'**Nān … ne** gives one denial; **gehwā** is singular “each person”. Bōc and męte are accusative objects. A different grammatical order is possible, but the directions require nān and personal gehwā; a generic plural all would not meet that distributive target.',
'C02':'**Næfde** denies past possession, and **nolde** expresses past unwillingness with plain **gān**. The two meanings must remain separate. Uncontracted ne hæfde/ne wolde can express valid language, but the specified task requires the contractions.',
'C03':'**Ǣnige** and **nāne** agree with accusative feminine singular bōc. The question is not already negative; the reply uses **nān** with finite **ne**. A contracted negative possession verb is also possible in the reply if agreement and the specified nān are preserved.',
'C04':'The directions make the condition potential: **hwā** is indefinite and **hæbbe** present subjunctive. **Him** is the main-clause recipient; the present **sęlle** expresses the promised giving. An indicative condition can be grammatical in a factual setting but would not meet the stated potential-clause target.',
'C05':'The complete **swā hwā swā** expression means whoever. **Gā** is the requested present subjunctive; **him** resumes the person as dative recipient. Omitting the free-choice frame and writing an ordinary question changes the meaning.',
'C06':'**Hwæðer** is nominative as subject of **cume**. **Ðissa twēgra suna** is the genitive group “of these two sons”; **him** separately expresses the main-clause recipient. This is the requested potential clause with internal case, not the specially supplied attracted-case construction in Cook 31.12.',
'C07':'Impersonal **man** takes third-singular **mæg** and plain **gān**: “one can go”. A specific se mann would introduce a particular man. Sceal would express obligation rather than the requested ability.',
'C08':'**Ǣlc sunu … hæfð** is singular and distributive; **ealle ðā suna … habbað** is plural and collective. **Āne** agrees with feminine accusative bōc. “All” does not make the first clause’s one-per-son distribution explicit.',
'C09':'The paired **ǣgðer ge … ge** includes both accusative objects. His sunu is the king’s son. An ordinary and-coordination may preserve the broad meaning but does not demonstrate the required paired construction.',
'C10':'The two **swā** clauses correlate increasing size and goodness. **Māre** and **bętere** are neuter singular with hūs; **hit** resumes it. This is a proportional comparison, not equal-degree as … as.',
'C11':'The first **swā … swā** compares the books’ goodness as equal. **Ðæs cyninges** is the possessor of the third book; **bętere** is its comparative predicate. Inserting ðonne for the equality standard would change the comparison.',
'C12':'**Swīðor** compares preference for the two objects, męte and wīn. The standard is an understood second object of lufað, not a new agent. “More than” and “rather than” express the intended preference here; the direction specifically requests swīðor.',
'C13':'**Ne gā** is a singular negative command; **sęle** a singular affirmative command. **Ðǣm wǣdlan** is the dative recipient and **ðā bōc** the accusative gift. Subject pronoun ðū may be expressed; plural commands would not address the specified one person.',
'C14':'The going is affirmed of **hē self**. **Nā ōðer** excludes another man as the goer; it does not negate gǣð. The stated male referent accounts for self and ōðer in these selected forms.',
'C15':'**Nānum męnn** is the dative recipient, **nāwiht** the thing given, and **ne** finite negation. Together they mean “I give nothing to anyone”. The two specified negative expressions do not cancel each other. Other idiomatic negative phrasings can be valid but do not meet this three-part target.',
'C16':'**Nānes mannes** is the negative genitive possessor of subject sunu. **Ne cymð** agrees with the singular son. The task requires nān inside that genitive phrase; a different placement of no could change the scope or miss the specified construction.',
'C17':'**Næfð** is third-singular negative possession. **Nāna bēc** is accusative feminine plural: no books. Bēc here is not the identical-looking genitive or dative singular. The contracted verb already includes finite negation.',
'C18':'**Gehwone** is the accusative person seen; **gehwæs** is the genitive person whose son is good. Neither the repeated English each nor the common reference licenses nominative gehwā in those two positions.',
'C19':'**Ān mann** introduces an unnamed person rather than insisting on a numerical contrast. **Hē** then maintains that reference. “Sum mann” can also introduce a certain man, but the direction here requires indefinite ān. No English-style indefinite article is needed before the second bōc.',
}
for code,note in composition_notes.items():
    tid='NEW-U15-'+code;item(tid,code,comps[tid]);para(note)

heading('Cook IX.28')
cook_notes={
'28-01':'**Ǣlc ðe … forlǣtt** names the person; the following **him … forgolden bið** resumes that person as a dative recipient in the supplied passive construction. The finite **bið** is last in its clause, as directed. **Mid hundtēontigum** supplies the hundredfold repayment; **hē hæfð** expresses the promised future possession. Brōðor and sweostor are accusative plural here despite their syncretic spellings. Preserve every alternative in the list and the additional eternal life; do not insert the omitted impersonal it or a mechanical shall auxiliary.',
'28-02':'**Sealde** supplies the specified sęllan. **Ǣlcum** is the recipient, **pęning** the payment, and **wið his dæges weorce** the exchange: in return for his day’s work. Dæges is a genitive dependent on dative weorce. A numeral can make the single penny explicit, but confusing the exchange phrase with an opponent changes the sense of wið.',
'28-03':'**Hīe** is the accusative people sent; **on his wīngeard** has the requested directional accusative, into the vineyard. A static dative vineyard would express location rather than the movement specified by into.',
'28-04':'The perception construction has **hīe/ōðre** as an accusative participant with plain **standan**: he saw others stand/standing. **Īdle** agrees with those people; **on strǣte** is the supplied public-place use without an article. English standing does not require a participle when the exercise explicitly selects this infinitive construction.',
'28-05':'**Gāð gē** addresses the plural workers. **On mīnne wīngeard** is directional accusative; **ēow** is the dative recipient with **sęlle**. The required **ðæt riht is** means what is right, with riht as a neuter predicate. Preserve the promise of giving what is right, not a statement that the workers are right.',
'28-06':'**Ęft** means once more. **Ymbe** governs the accusative hour expression; the supplied ordinals **siextan/nigoðan** agree with feminine tīd. **Gelīce** is an adverb, “similarly”, modifying dyde; it is not the plural predicate adjective of 29.1. Different grammatical placement of the adverb is possible without changing either hour.',
'28-07':'The supplied **ðā endleftan tīd** is accusative after ymbe. **Ōðre** is the object of funde and **standende** the explicitly requested present participle describing them. A perception infinitive may be possible elsewhere, but it would not meet this item’s participle control.',
'28-08':'**Standað gē** is a plural indicative question, not an order to stand. **Ealne dæg** is accusative duration, all day; **īdle** describes the plural people addressed. Hēr gives the place. Do not infer a singular verb from the single day.',
'28-09':'The causal clause has negative subject **nān mann**, object **ūs**, and finite **ne hȳrode**. It states one denial: nobody hired us. The preterite follows Cook’s omission of hath. An evidenced equivalent causal conjunction is acceptable, but reversing the negative into nobody failed to hire us is not.',
'28-10':'The supplied **ðā hit ǣfen geworden wæs** presents the evening as having come. **Ðæs wīngeardes** depends on hlāford; **tō his gerēfan** identifies the steward addressed. **Cleopa** and **forgield** are singular commands. The workers are accusative **ðā wyrhtan**; payment has dative **him** and accusative singular **hiera mēde**, their hire. Do not make the recipient accusative merely because modern English says pay them.',
'28-11':'The first **ðā** introduces when; the second refers to those who came. The relative clause ends with **cōmon**, satisfying the stated final-verb control. Main **onfēngon** agrees with plural hīe; distributive **ǣlc his pęning** says that each received his own penny. The bounded payment frame permits accusative pęning. Treating ǣlc as the sole singular subject would lose the plural received they.',
'28-12':'**Wēndon** means supposed/thought and introduces the content clause. **Sceolden** is the selected reported preterite subjunctive plural, expressing the expected receipt; it need not mean moral obligation. **Māre** is substantive neuter, a greater amount, and the object of onfōn. Keep **ðǣr** and the first arrivals; preferential swīðor would not mean more payment.',
'29-01':'**Hīe** is the accusative object made equal, **gelīce** its agreeing plural complement, and **ūs** the dative comparison standard. The relative clause concerns **us**, the speakers who bore the burdens; **bǣron** is first plural in that relation. **Hęfignessa** is the accusative plural burdens, and **on ðisses dæges hǣte** gives this day’s heat. An adverbial similarly would not express the required equal-to-us relation.',
'29-02':'**Nim … gā** are singular commands. **Ðæt ðīn is** is the thing that belongs to the addressee. **Eall swā micel swā** means just as much as; **ðissum** and **ðē** are the two dative recipients under the giving verb, expressed or understood. Do not turn the quantity comparison into one between the recipients’ size.',
'29-03':'**Ne mōt ic …?** asks about permission: “May I not …?” **Dōn** is the plain infinitive after mōt, and **ðæt ic wille** the required free-standing relative content, what I wish. A question about ability with magan would not retain the permission sense.',
'29-04':'**Ne cōme ðū …?** is a past second-singular indicative question. **Tō wyrceanne** is the required inflected infinitive for the work’s purpose; **wið ānum pęninge** is dative exchange, for one penny. Plain wyrcean after tō would miss the inflected-infinitive target. Cōme here is not subjunctive merely because the question is negative.',
'29-05':'One person is described as both **wer** and **wītga**; the finite verb remains singular wæs. **Mihtig** is the masculine predicate, with on worde/on weorce specifying speech and deed. **Beforan Gode and eallum folce** has the dative terms. The earlier taught spelling wītga expresses the unqualified English prophet; the prompt does not require a new spelling variant.',
'29-06':'**Ðæt is se dōm** introduces the judgment, followed by its content. Light came into the world; men preferred darkness to the light. **Ðīestru** is morphologically plural, and **swīðor ðonne** compares preference between accusative objects. **Hiera weorc … wǣron** is plural, with the selected neuter plural **yfel**. Do not make darkness the subject who loved.',
'29-07':'The contrast rejects the purpose of condemnation and asserts the purpose of salvation. In context **ne … ðæt … ac ðæt** does not deny that God sent his Son. Past purpose **dēmde** is subjunctive; **hǣled wǣre** is the corresponding passive purpose, with **ðurh hine** naming mediation. “God did not send him at all” loses the contrast; both purposes must remain explicit.',
'29-08':'**Mēd** is feminine: selected **ēowru** and **miclu** agree with it. **Gē bēoð … bearn** expresses the promised relationship; **ðæs Hēahstan** is the supplied divine title in the genitive. **Ofer ungeðancfulle and yfele** has the newly taught personal objects, the unthankful and evil people, after kind toward. They are not feminine singular reward adjectives. Keep the distinction between promise and the reason given for it.',
'29-09':'**Giefað** is plural imperative. The following supplied impersonal passive **ēow bið giefen** keeps the dative recipients and omits it as directed. An English translation may need “it will be given to you”; that does not require an Old English hit in this controlled response.',
'29-10':'**Nis** is negative third-singular be; **ofer his lārēow** is the accusative standard of rank. The disciple is not above his master. A spatial interpretation of standing over the teacher would miss the intended relation. Uncontracted ne is can be grammatical, although nis is the selected new contraction.',
'29-11':'**Ætīew** is the singular command show; its first vowel remains short in the selected spelling. **Unne** is a supplied second-singular present subjunctive used as a request. Unnan takes dative **ūs** and genitive **ðīnre hǣlu** for what is granted. Do not copy the accusative mildheortnesse frame into the grant clause merely because the two verbs share the same English object order.',
'30-01':'**Ne swęre ðū** is a singular prohibition; the following **ne ðurh** phrases continue it. Each **ðurh** names the oath standard in the accusative. Heaven is masculine (**hē**), earth feminine (**hēo**); Hierusalem is supplied. The great king is **ðæs mǣran cyninges**, genitive dependent on burg. English nor may combine the later prohibitions; it must not remove one of the three standards.',
'30-02':'**Hēafod** and **hǣr** are neuter. In **ān hǣr hwīt oððe blæc wyrcean**, the one hair is the accusative object and the two colors are its agreeing neuter complements. **Ne meaht** denies ability. Masculine ānne/hwītne/blæcne would not agree with this noun; the two occurrences of by/through likewise have different work from object agreement.',
'30-03':'**Sīe** is the supplied present subjunctive wish, “let your speech be …”. **Ēower** refers to plural possessors, while word is singular. The quoted alternatives **hit is, hit nis** contrast affirmation and denial. A second plural possessive does not require a plural verb for the single word/speech.',
'30-04':'**Gē hīerdon** follows the omitted English perfect auxiliary. The passive **cweden wæs** has no inserted it. In the formula, **ēage/tōð** are nominative and **ēagan/tēð** dative after the specified for. The second tēð is dative singular, not automatically plural teeth. Preserve both exchanges.',
'30-05':'**Se ðe …**, resumed by **sē**, identifies the person. **Ān of ðissum lǣstum bebodum** selects one commandment from a dative-plural group. The second relative action has **swā męnn lǣrð**, with its finite verb last as instructed. Main **lǣst hāten** describes the person’s rank, not the size of a commandment. The selected hātan means be called/named; another valid naming verb must still preserve the passive and predicate.',
'30-06':'The two verbs share object **hit**. **Se ðe** is resumed by **sē**; **micel hāten** says that the person will be called great. The original prompt does not require an additional the same. Do not carry least from the preceding item into this one.',
'30-07':'**On ealdum tīdum** is a dative plural time phrase. **Ne sleah ðū** is the singular negative command quoted within the passive report. The selected uncontracted command retains the previously taught short diphthong spelling. Cook’s omitted have and it are not to be reintroduced mechanically into the Old English model.',
'30-08':'**Is hit ðīn eorðe?** asks about the singular addressee’s earth. The prompt says earth, not oath. **Ðīn** agrees with feminine eorðe; hit provides the identifying subject. Plural ēower would fail the explicit singular-your direction.',
'30-09':'**Æt his gewinne** is the supplied source/proceeds use, from his labor. **Ðæt hē mæg** leaves an understood acquisition/action after the modal: what he can [obtain]. It does not ask where he works. Keep the locally supported sense and ellipsis instead of guessing them from the familiar preposition or modal alone.',
'30-10':'**Sēo sunne** is feminine nominative; **his æcer** is accusative singular. **Forbærnde** is the transitive preterite, burned/parched. An idiomatic rendering may express the scorching result, but the field must remain the affected object rather than the thing doing the burning.',
'30-11':'Both parallel clauses use plural **sceoldon** with plain **blōstmian**; preserve their repetition. The bride is feminine, hence selected **fægeru**, and **hiere hām** is the accusative home left. **Sceal** is singular with brȳd. The noun hām is distinct from the earlier homewards adverb; the modal complements remain infinitives, not participles.',
'30-12':'The condition uses ability, **gif hīe magon**, as the prompt says can. Supplied **lǣt hīe libban** is a singular command with accusative participants and a plain infinitive; **būtan mē** means without me. Replacing magon with a wish/volition verb changes the condition.',
'30-13':'**Ne … nǣfre** expresses one never. **Ðā ðe …** is the accusative object of forlǣtt; the relative clause has **on hine** for the person trusted. Do not cancel the negatives or treat this belief-on relation as physical position.',
'31-01':'**Wāt** states present knowledge; **leofað** is the selected present third singular of libban. **Mīn Ālīesend** is the subject of the ðæt-content clause. Preserve the claim that the Redeemer lives, rather than turning it into merely a future hope.',
'31-02':'**On mīnum flǣsce** is a dative setting. **Gesēo** is a present form with the intended future reference. **Ic self** identifies the speaker emphatically; **nā ōðer** excludes another as the seer. It does not negate the speaker’s seeing or mean seeing another god.',
'31-03':'The supplied **wæs lǣred … tō dōnne** is passive teaching with an inflected infinitive. The subject he is also the understood doer. **Godes** is the genitive possessor of accusative **willan**, the thing to be done. Ordinary willa and the modal willan are different lexemes; neither their spelling nor the passive licenses exchanging those roles.',
'31-04':'**Ne lǣd ðū** is a singular prohibition. **On costnunge** gives the temptation entered; **ālīes ūs fram yfele** requests release, with an accusative person and dative source of separation. The supplied yfele is abstract evil. Do not silently turn it into an identified evil person or make the recipient the source of separation.',
'31-05':'**Sīe … gehālgod** is the supplied passive wish, “may your name be hallowed”. **Ðīn nama** is the singular subject. The wording expresses a desired state, not a past report that the name was hallowed. A different grammatical wish order is possible here; the next item alone explicitly requires the verb first.',
'31-06':'**Geweorðe** is the requested prefixed verb, first in the sentence, in its supplied third-singular subjunctive wish use. **Ðīn willa** is the subject. **On eorðan** and **on heofonum** retain the earthly/heavenly settings linked by **swā-swā**. An unprefixed replacement or a noninitial verb would miss an explicit source control.',
'31-07':'**Nān … næs** gives one negative statement. **Engla** is the genitive plural group, of the English; **swā micel swā Ælfred** is an equality standard denied for any king in the statement. The comparison concerns greatness, not numerical quantity, and the title’s historical claim is simply being translated.',
'31-08':'The four predicates retain fighting, judging, translating and being a poet. **Wið ðǣm Dęnum** uses the given people’s dative plural; **his folc** is the object judged; **āwęndednessa** is the translations made. The supplied **of Lǣdene** follows Cook’s glossary spelling with long ǣ. The reading’s exact **Lædene** remains a source spelling of its own. Do not regularize that reading silently to match this composed model.',
'31-09':'The supplied **hātte** is the special was-called form, matching hight. The second clause can leave that same verb understood or repeat it. Keep Osburg as the mother and Æthelwulf as the father; active “called someone” is not the required name relation.',
'31-10':'**Twā and fīftig gēara** is the supplied complete expression for fifty-two years. Its higher-number construction takes genitive plural gēara. The task does not license inferring a new complete higher-numeral paradigm. The meaning is his life’s duration, not his age at the reading lesson in the next item.',
'31-11':'**Bēcrǣdinge** is what he learned. The supplied **æfter ðǣm ðe** introduces the past temporal clause; **twęlf wintra eald** is the supported age expression, with the number and genitive plural years. Preserve after: neither before nor a simple coincident when conveys the same relation.',
'31-12':'**Engliscra lēoða** is genitive plural, the poems contained in the book. Relative **ðe** is the object of **gehēt**, with the mother as subject: the book which she promised. The entire **swā hwæðrum … swā … leornode** is supplied: the recipient form is dative by attraction while the chosen son performs the learning; **hīe** is the feminine book learned. The preterite subjunctive conveys the prospective choice. The regular internal-nominative/resumptive construction practised in C06 can express a defensible alternative if both clauses are fully reconstructed; do not generalize this exceptional dative into a rule for every relative subject.',
'31-13':'**Ānum uncer** is one recipient selected from us two: dative ānum plus the personal genitive dual uncer. **Ðǣm ðe …** further identifies that recipient. The feminine book is **hīe**, object of **ongiett**; the person who understands is the relative subject. The agreeing possessive uncer, “our”, would not supply the stated partitive relation.',
'31-14':'**Asser** is the writer and **Ælfredes bisceop** his appositional description. **Āne bōc** is the accusative object; **ðæs cyninges līfes** is its content genitive, with the king as possessor of the life. The earlier taught bisceop is sufficient for the English bishop. A spatial of-phrase would not demonstrate Cook’s specified genitive relation.',
}
for ex,count in [(28,12),(29,11),(30,13),(31,14)]:
    group='IX' if ex<31 else 'X, XI'
    if ex!=28:heading('Cook '+group+'.'+str(ex))
    for n in range(1,count+1):
        tid=f'EX-IX-{ex}-{n:02}' if ex<31 else f'EX-X-XI-{ex}-{n:02}'
        item(tid,f'Cook {group}.{ex}.{n}',cook[tid]);para(cook_notes[f'{ex}-{n:02}'])

heading('D. Duties of the Rich toward the Poor')
reading_answers={
'D01':('The fault is withholding the speaker’s goods and disregarding the gift entrusted to the rich man. The announced consequence is exclusion from that bounty and poverty in worldly life. The promise is hundredfold repayment of a good deed done in the speaker’s name and eternal heavenly joy in return for gifts to the least. The speaker is the Savior; the initial addressee is the rich man, followed by an embedded gospel saying addressed to a plural audience.',
 'Wlanc also permits proud as a lexical rendering; keep the passage’s wealth and giving context. Do not introduce poor people as the subject of **mann gedēð**: that clause says one/a person does the good deed.'),
'D02':('**Noldest** is negative willan, preterite indicative second singular, governing plain **geðęncean**: “why were you unwilling to consider …?” Inside its content clause **ic wille** states the speaker’s present or continuing intention to repay.',
 'A past question does not force mechanical backshift of a proposition still presented as true. Wille does not become past merely because noldest is past.'),
'D03':('**Swā-hwæt-swā** names the thing given, whatever you give. The immediate recipient is **ānum of mīnum ðǣm lǣstum**, one of the least belonging to the speaker. **Mē** identifies the speaker himself as the recipient of that same gift. **Hit** resumes the thing, not the person receiving it.',
 '“Whatever you give to one of the least of mine, you always give it to me” retains the two recipient descriptions. Supplying brothers as an explanatory gospel allusion is possible, but it is not a separate printed noun in this extract.'),
'D04':('**Ānum** is dative singular, the selected recipient. **Of** governs the dative-plural group **mīnum ðǣm lǣstum**. **Wið ðǣm** is the dative exchange expression, in return for that.',
 'English of does not make the first group genitive in Old English. The second relation concerns repayment, not a person opposed to or standing beside the speaker.'),
'D05':('The Savior said to the rich man: “Why were you so withholding of my goods, which I gave you? Why did you disregard the gift that I gave you? I now remove you from my bounty, which I bestowed on you; then you will be poor in worldly life. Why were you unwilling to consider that I intend to repay each person for a good deed that one does in my name? I repay it to him a hundredfold, as it is declared and stated in my gospel: ‘Whatever you give to one of the least of mine, you always give it to me, and I shall grant you eternal joy in heaven in return for that.’',
 'The assigned opening argument ends here; the outer speech continues beyond it. The unmatched outer quotation follows that boundary. Future “I shall remove/repay” is also defensible for the presents in context. Bounty/distribution, poor/needy and eternal joy/delight are suitable alternatives. Retain the change from rebuke to promise, each recipient, the hundredfold repayment and the gospel quotation.'),
'P01':('The two methods are **word be worde**, word for word, and **andgiet of andgiete**, sense from sense. Various and manifold worldly cares troubled Alfred in mind and body; the troubles that befell his kingdoms are said to be hard to enumerate. After learning and translating the book into English prose, he made it into verse. He asks readers to pray for him and not blame him if they understand it more correctly than he could.',
 'The cares constrain what he could explain; they are not a separate benefit bestowed by the translation. Preserve the sequence from the earlier translation to its later versification.'),
'P02':('In the requested order: **hē** before gebidde = the reader; **hine** after for = Alfred; **him** before ne wīte = Alfred; **hē** after gif = the reader; **hē** after ðonne = Alfred. Thus the reader may understand more correctly than Alfred could.',
 'A repeated masculine pronoun need not keep one referent throughout. Reading every hē as Alfred destroys the comparison and the request addressed to the reader.'),
'P03':('**Ǣgðer ge on mōde ge on līchaman** includes both settings, in mind and in body. In the next sentence **ðā bisga** is the plural subject and **sind** the finite verb. The first following relative clause describes the troubles that befell the kingdoms: its relative is subject of becōmon. The second describes the kingdoms that Alfred had received: its relative is object of underfangen hæfde, with hē as subject.',
 'The two relatives have different antecedents and roles. Do not attach both to the troubles or interpret the kingdoms as the agent that received Alfred.'),
'P04':('**Rihtlicor … ðonne** compares the reader’s more correct understanding with what Alfred could understand; ongietan/understand is recoverable after meahte. **Ne** negates wīte, blame, in the content of the request.',
 '**And him ne wīte** coordinates with the prayer request after ðæt. It is not a separate past assertion that someone did not blame him. “Not find fault with him” is a natural alternative.'),
'P05':('King Alfred was the translator of this book, and translated it from book-Latin into English, as it is now done. At times he set word for word, at times sense from sense, as clearly and intelligibly as he could explain it amid the various and manifold worldly cares that often troubled him both in mind and in body. The troubles that befell in his days the kingdoms he had received are very hard for us to enumerate. Yet, after he had learned this book and translated it from Latin into English prose, he afterwards made it into verse, as it is now done. And now he asks, and entreats in God’s name, each of those who may wish to read this book to pray for him and not blame him if the reader understands it more correctly than Alfred could; for every person must, according to the measure of his understanding and according to his leisure, speak what he speaks and do what he does.',
 'Literary Latin/Latin, translator/interpreter, cares/occupations, and prose/discourse are defensible contextual choices. The translation must retain both methods, the impediments, the later versification, the charitable request and the differing comparison subjects. “He” in the last request may be retained in English if its changing reference remains clear. These are the preface’s statements; the translation does not settle modern questions of authorship.'),
'R02':('The repeated **for** phrases appeal by or for the sake of God’s mercy, the sign of the holy cross, Mary’s virginity, Michael’s obedience, and the saints’ love and merits. In **for ðǣre hālgan rōde tācne**, **tācne** is the dative governed by for; **ðǣre hālgan rōde** is the dependent genitive, of the holy cross.',
 'The syncretic feminine endings do not make rōde the directly governed noun. The exact source **gehīersumnesse** means obedience; translating it as intercession substitutes a different word.'),
'R03':('The first **bęt ðonne** sets the speaker’s desert—what his conduct toward God has earned—as the standard. The second sets his own ability to know or determine what he needs as the standard. **Cunne** is present subjunctive in this petition’s potential comparison.',
 '“Better than I have deserved” and “better than I myself could know how” preserve the difference. Cook’s optative note explains this occurrence; it is not a rule that every comparison takes a subjunctive.'),
'R04':('In the purpose clause, **ic** is the person who is to love **ðē**, the divine addressee. **Mæge** is present subjunctive first singular, governing plain **lufian**; the clause gives the intended purpose of the requested help and teaching.\n\nIn **Sīe ðē lof and wuldor**, the addressee receives the wished-for praise and glory. **Sīe** is the source’s present subjunctive wish form. This is an independent concluding wish, not another subordinate purpose clause.',
 '“So that I may love you” and “May praise and glory be yours” preserve their different functions. Do not make God the actor of the first-person loving merely because he is addressed throughout the prayer.'),
'R05':('Lord, almighty God, Maker and Ruler of all created things, I ask you, by your great mercy, by the sign of the holy cross, by Saint Mary’s virginity, by Saint Michael’s obedience, and by the love of all your saints and their merits, to guide me better than my conduct toward you has deserved. Guide me according to your will and for the benefit of my soul, better than I myself could know how; establish my mind according to your will and for the benefit of my soul; strengthen me against the devil’s temptations; remove from me filthy lust and every unrighteousness; shield me against my adversaries, visible and invisible; and teach me to do your will, so that I may love you inwardly above all things, with pure thought and a pure body. For you are my Creator, my Redeemer, my Help, my Comfort, my Trust and my Hope. May praise and glory be yours now and for ever and ever and ever, world without any end. Amen.',
 'Guide/direct, establish/settle, shield/protect, and benefit/need of my soul are suitable alternatives. Keep all grounds of appeal, the distinction between the initial requested action and six commands, both comparisons, both occurrences of the soul’s need, the purpose and the concluding praise. Mīnre sāwle is genitive dependent on ðearfe in both places; it does not name a separate recipient of the verb.'),
}
for group,title in [('D','Duties of the Rich toward the Poor'),('P','Alfred’s Preface to Boethius'),('R','A Prayer of King Alfred')]:
    if group!='D':heading(group+'. '+title)
    for n in range(1,6):
        code=f'{group}{n:02}';tid='NEW-U15-'+code;item(tid,code)
        if code=='R01':
            table(['Form','Mood and person','Essential meaning'],[
                ['gewissie','Present subjunctive, 2 singular','guide/direct me'],
                ['gewissa','Imperative, 2 singular','guide me'],
                ['gestaðela','Imperative, 2 singular','establish/settle my mind'],
                ['gestranga','Imperative, 2 singular','strengthen me'],
                ['āfierr','Imperative, 2 singular','remove lust and unrighteousness from me'],
                ['gescield','Imperative, 2 singular','shield/protect me'],
                ['tǣc','Imperative, 2 singular','teach me to do your will'],
            ])
            para('The first action is requested in **ðæt ðū mē gewissie** after ic bidde. The six following forms are direct singular commands. Calling every form an imperative would miss the initial subordinate subjunctive; naming only headwords would not give the actual finite forms requested.')
        else:
            answer,note=reading_answers[code];para(answer);para(note)

heading('Sources and grading limits')
para('Cook’s 1895 *Exercises in Old English*, printed pp. 15–18 (one-based PDF 23–26), supplies the 50 numbered English prompts. The solutions are new compositions using the specified forms, established earlier teaching and the lesson’s visible local help. A valid alternative is not rejected merely for differing from a model string; explicit source or original-task directions still define the particular exercise target.')
para('The readings follow Cook’s 1895 second edition of *A First Book in Old English*: the opening argument of *Duties of the Rich toward the Poor*, printed 159.1–12 (PDF 175); the complete *Alfred’s Preface to Boethius*, 162.1–17 (PDF 178); and the complete *A Prayer of King Alfred*, 163.1–18 (PDF 179). Individual lines are editorial counts anchored by the printed marginal line numbers. The learner retains all original source notes separately from modern explanations. The Duties extract does not include the continuation on pp. 160–161.')
para('Complete morphology is limited by the lesson’s stated senses and constructions. Reference forms, supplied phrases and the special attracted-case clause do not silently become independent production requirements. English translation alternatives should preserve the propositions and relations identified above, even when English needs a word that the Old English leaves understood.')
assert len(seen)==len(set(seen))==105 and set(seen)==set(tasks)
assert len(outputs)==len(set(outputs))==322
text=unicodedata.normalize('NFC','\n'.join(out).rstrip()+'\n')
dest.write_text(text,encoding='utf-8',newline='\n')
print('Wrote separate Unit15 key:',len(seen),'tasks;',len(outputs),'output locators;',len(text.split()),'whitespace words.')
