"""Independent review judgments; not an answer-generation or master-editing script."""

NOTES = {
 'NEW-U17-A01': [
  'King/sægde and man/wǣre are separate subjects and finite predicates; the witness and key both keep gōd as the embedded predicate.',
  'Ðæt introduces reported content, and the stipulated goodness is simultaneous with the past statement, not necessarily anterior.',
  'Both responses reject the inference that wǣre proves the report false; reported mood and truth value remain distinct.'
 ],
 'NEW-U17-A02': [
  'The witness and key translate the comparison of singing as better than the king did, retaining both actors.',
  'Dyde substitutes for singing and agrees with the singular king, independently of the first clause.',
  'Ðā męnn sungon changes the first subject and verb to plural while se cyning dyde remains singular; the actual OE answer matches the target.'
 ],
 'NEW-U17-A03': [
  'Ðone mann is the accusative outer object of geseah, not the relative subject case expressed by an inflected relative.',
  'Invariant ðe has the internal subject role of sang despite the antecedent’s outer accusative; both analyses preserve that distinction.',
  'Ic geseah ðā męnn ðe sungon makes the men plural in the object and relative predicate, leaving the seeing subject singular.'
 ],
 'NEW-U17-A04': [
  'The open tomorrow condition has future reference with present cymð/fare. The witness additionally notes fare’s formal syncretism without changing the contextual indicative analysis.',
  'Cōme/fōre are past subjunctives with the expressly stipulated contrary present reference; neither answer confuses morphology with past time.',
  'The possible future visit versus contrary present setting determines the interpretations; gif alone does not encode either truth assessment.'
 ],
 'NEW-U17-F01': [
  'Ðæs cnihtes bōc supplies singular possessor genitive and singular possessed book; both answers match.',
  'Ðāra cnihta bēc supplies plural genitive possessors and mutated plural books; both answers match.',
  'Ic giefe ðǣm cnihte ðā bōc separates first-singular giver, dative singular recipient, and accusative singular gift.',
  'Wē giefað ðǣm cnihtum ðā bēc changes giver, recipients and gifts to plural with their distinct endings.'
 ],
 'NEW-U17-F02': [
  'Ic geseah ðā cwēn meets the explicitly selected endingless accusative target. Valid cwēne elsewhere is not treated as the requested selection here.',
  'Ic geaf ðǣre cwēne ðā bōc uses dative cwēne for the recipient and the taught giving frame.',
  'Ðǣre cwēne bōc uses genitive cwēne as possessor; the same surface as the dative does not merge the relations.',
  'The witness and key explain the selected zero accusative, syncretic -e obliques and grammatical alternative cwēne without claiming a universal ban on it.'
 ],
 'NEW-U17-F03': [
  'Se fox is on ðǣm hole retains singular fox and locative dative hole.',
  'Ðā foxas sindon on ðǣm holum makes the subject/verb and locative complement plural.',
  'Ðæt nest is on ðǣm trēowe has a neuter singular nest and dative singular tree.',
  'Ðā nest sindon on ðǣm trēowum preserves heavy neuter zero plural nest and the distinct tree dative plural.',
  'Ðā holu sindon miclu applies short-neuter plural -u to holes and the agreeing predicate; no article-triggered weak predicate is invented.'
 ],
 'NEW-U17-F04': [
  'Hęriað is the requested indicative third plural assertion.',
  'Hęriað is also the requested second-plural imperative; the identical spelling does not give identical person/function.',
  'Hęrien is the requested present-subjunctive third plural wish, not a periphrasis of permission.',
  'Both analyses contrast assertion, plural address and wish and identify exactly the first two spellings as syncretic.'
 ],
 'NEW-U17-F05': [
  'Hine ondrǣdendum preserves outer dative plural people and inner accusative singular object of fearing.',
  'Ðā hyngrendan is article plus weak accusative plural substantive participle, not an unsupported finite personal hyngran form.',
  'The dative beneficiary relation does not govern hine; the participle’s fear frame supplies the accusative internally.',
  'The substantive participle names people and carries nominal agreement without independently finite person/tense; this is explicitly taught bounded use.'
 ],
 'NEW-U17-C01': ['The complete sentence matches the key: singular king sees accusative plural men, whose invariant relative controls sungon. An inflected relative would miss the explicit particle target.'],
 'NEW-U17-C02': ['The complete sentence matches the key’s swā … swā equality, with singular gōd/is and plural sindon in their respective clauses.'],
 'NEW-U17-C03': ['The witness matches the open-condition cymð and plural-command giefað; him is dative recipient and bōc accusative gift.'],
 'NEW-U17-C04': ['The witness matches sægð plus present-subjunctive sīe in the requested report. Certainty-indicative language can exist but would miss this task’s stated mood target.'],
 'NEW-U17-A05': [
  'The first image joins all flesh and grass by is, and both responses explain frailty/transience while retaining the nouns.',
  'The second image compares glory with blossom through swilce; both distinguish explicit comparison from the first copular identification.',
  'The witness and key reject Human life is brief as a complete rendering because it drops the two images and their different relations.'
 ],
 'NEW-U17-A06': [
  'Horn remains in the translation while praise context suggests the people’s strength or exaltation; neither response claims a literal animal event.',
  'His sǣde denotes Abraham’s descendants collectively and retains its singular dative form; the possessor is identified correctly.',
  'Both responses separate familiar inflection from contextual and newly taught senses; endings alone do not establish strength or descendants.'
 ],
 'NEW-U17-R01': [
  'Full first division compared against Cook174.7–13: fetching is commissioned, sound and song combine, all praise, Apollonius alone is silent, and the king interprets silence as censure. Witness and key retain every event.',
  'Full second division compared against Cook174.14–175.2: permission, perceived lack of mastery, recipient mē, future knowing and the king’s affirmative acknowledgment are preserved. Witness’s literal now is compatible with the source.',
  'Full third division compared against Cook175.3–17: harp delivery, exit/dress/crown/harp/entrance, mistaken Apollo identity, silence, plectrum/strings/song, praise, acting and universal pleasure all occur. Witness’s crown and performed beautiful things are contextual equivalents of the key’s royal crown and fine performances.'
 ],
 'NEW-U17-R02': [
  'Hēo is the daughter, established by context and compatible feminine singular morphology; neither answer pretends the form supplies a name.',
  'Hine is accusative masculine swēgcræft as the unmastered object; it does not refer to one of the men.',
  'Both hē pronouns in the supposed identities refer to Apollonius, distinct from the plural supposing audience.',
  'Him eallum is the dative plural audience pleased. The witness also correctly notes that him alone is number-syncretic.'
 ],
 'NEW-U17-R03': [
  'Sōna swā supplies immediate temporal linkage of playing and singing, distinct from equality or result.',
  'Gif … gelīefst is the open permission condition, with present indicative and a prospective speech consequence, not belief or counterfactual refusal.',
  'Swā stōd ðæt introduces the result of the performer’s appearance; inner content clauses belong separately to wēndon.',
  'Nǣre/wǣre report what the spectators supposed. The narrator’s continuing Apollonius identification prevents a literal transformation reading; subjunctive itself is not a universal falsehood marker.'
 ],
 'NEW-U17-R04': [
  'Actual note174.12a prints For swīgiende. Both responses retain source swīgende and explain nonfinite accompanying silence.',
  'Ðā ymbsittendan is a weak plural human substantive coordinated with the king as the subject of wēndon.',
  'Both responses preserve singular ungecnāwen wæs and ungewunelic after the collective display. The bounded source explanation does not become a general singular-agreement rule.',
  'Ǣlc ðāra ðinga is the singular subject of līcode; dative plural him eallum supplies experiencers and cannot control its number.'
 ],
 'NEW-U17-R05': [
  'The falling-on image is interpreted through original note174.15 has chanced and local musical help; a physical falling event is excluded.',
  'Plegode and forðtēah describe acting and presenting performances. Original175 notes6/8 support the dramatic sense without adding the Latin as extra OE wording.',
  'Apollines is the source’s Apollo name and a reported predicate identity; it remains distinct from Apollonius, as original175 note2 confirms.'
 ],
 'NEW-U17-R06': [
  'Both responses retain the difference between the king’s social accusation and Apollonius’s technical criticism, with permission and demonstration as his answer.',
  'Both identify skilled harp/song and subsequent dramatic accomplishments, supported by the actual praise and pleasure responses, not merely a vague claim of talent.',
  'Both relate unfamiliar performances to each/all/greatly in the final sentence, preserving novelty with universal positive response.'
 ]
}

COOK = {
37: [
 'Both commands retain the Lord/him, origin of heofonum, location on hēanessum, and global article/second-person omission; the OE answers match.',
 'Commands, angel group and neuter eall … mægnu agree. The frozen witness omits the selected hook in englas; ch10 register has ęnglas. This is a witness orthographic miss, not a model error. Mægen power is now accurately described as taught.',
 'Both commands retain sun, moon, stars and the separately printed light. The model does not silently turn and light into a genitive of light.',
 'Heavens-of-heavens and waters remain plural; the relative has sindon and overt ofer+accusative under Cook172. The global omissions remain intact.',
 'Wish hęrien, command/speech pasts, and both passive plural predicates are present. Witness uses another known causal conjunction and fronted genitive/subject; these do not alter the target. Gecwæð’s ð is retained.',
 'The witness chooses gesętte for established against model sętte; both preserve the perfect-like past meaning. Both copy the supplied compressed decree clause with omitted it and the decree as gewīt’s subject.',
 'Earth origin, dragons and all depths remain. Ealla nēowolnessa agrees in the selected feminine plural; no forbidden articles or second-person subjects are added.',
 'Fire/hail, snow/ice and plural storm spirits are all retained. Witness and key use plural dōð and merely reverse genitive placement. The learner’s former singular storm sentence was a genuine prose defect, repaired under P17-04.',
 'The complete mountain/hill/tree/cedar catalogue remains. Wæstmbǣran is the weak direct-address adjective, while ealle follows its separate strong quantifier system.',
 'Wild beasts, cattle, snakes and feathered birds remain distinct. Neuter eall nīetenu and supplied weak gefiðredan satisfy the selected address patterns.',
 'Kings, all peoples, princes and all judges remain, with both earth genitives. Witness and key vary genitive placement without changing dependence or the global omissions.',
 'Young men/maidens and old men/children remain. The selected weak geongan/ealdan direct-address nominalizations are visibly taught, not inferred from tables alone.',
 'Both retain third-plural wish, his alone, exalted name and glory above earth/heaven. Witness changes permissible causal conjunction and word order; source-global omissions are still met.',
 'The complete dense supplied chain retains horn, people, praise, saints, Israel’s children and the approaching people. Masculine horn, weak hālgena and collective folces/nēalǣcendes are bounded by the supplied frame.'
],
38: [
 'Throne is large and ivory; it is overlaid with best gold by mid+dative. Witness uses known ðrymsetl for model setl; no original lexical cue makes that synonym a target failure.',
 'The key’s Sumu cwēn follows actual ch08 sum-nom-f-sg-strong. Frozen witness Sum cwēn misses the selected short-stem feminine ending and is not silently repaired. Both retain supplied time/south expressions and Saba naming.',
 'Reputation, southern departure, journey to Solomon within Jerusalem, and all three camel loads remain. Witness fram for model of gives the same taught origin; both keep the supplied within-place and gold-quantity phrases.',
 'Both use the supplied conversation-partner wið Salomon and retain final ðōhte. Witness eall ðæt and key swā hwæt swā both render all that she thought without losing a requested word-order control.',
 'Solomon teaches the queen and gives the meaning of all the asked words. Witness’s bare genitive-plus-andgiet order and key’s article/postposed genitive preserve the same object and relative roles.',
 'Queen sees wisdom, great temple and manifold services. Witness worhte and key geworhte are available make/build forms; no source lexeme cue forbids the variation, and all three objects remain.',
 'The supplied degree/result and accusative spirit under negative possession are preserved; witness only varies noncontrolled order in the result clause.',
 'Both retain the true report concerning Solomon/wisdom, former unwillingness, emphatic self and final gesāwe. Witness lande and absence of optional earlier adverbial ǣr do not change the before-clause target.',
 'The complete supplied comparison retains wisdom/work construed together and the explicit wǣre hint. No universal comparative-subjunctive rule is inferred from that copied form.',
 'Both blessed servant groups, continual standing, and hearing of wisdom remain. Plural finite agreement and taught dative ætforan are maintained.'
],
39: [
 'Blessed wish, choosing, appointment over Israel’s realm, and the purpose of judgments/righteousness remain. Witness varies genitive placement but retains overt source over+accusative and omits mightest.',
 'The complete 120-gold phrase and both genitive plural groups are copied as supplied; gold, costly herbs and precious stones all remain. This is not independent numeral production.',
 'Giving all requested things, giernan’s desired object/source frame, and return with attendants remain. Witness geaf/lande versus forgeaf/ēðle is valid meaning-preserving vocabulary variation.',
 'The model and witness OE retain celebrated rank plus all kings’ desire to hear the given wisdom. The clause is desired content under gewilnodon/Cook194b; the learner’s former purpose label and the witness’s inherited purpose wording are corrected in this review, not in the frozen witness.',
 'All six building materials remain under the free-choice construction and each work is revealed. Witness moves wyrcð later but no final-order cue applies; source over+dative foundation remains.',
 'Both survival and resistance to dative fire remain; onfēhð selects dative reward, æt Gode its source, and work is causal genitive. Witness’s adjacent reward-genitive order is valid. Accusative receiving is not condemned universally.',
 'Eye, ear and heart remain three negative coordinated domains of the shared modal, with seeing/hearing/conceiving and God’s preparation for lovers. Witness moves gearcað without losing its recipient or either relative.'
],
40: [
 'Greeting, two reported wǣre clauses and independent final wæs all remain; hiere mid is postposed as required. The witness’s dative betwēox wīfum attempt exposed B17-01; final whole-phrase supply closes it. Witness engel lacks selected ęngel hook.',
 'Soul magnifies and spirit rejoices, with God/Saviour in the explicitly supplied on+dative frame. The separate subjects and past/present choices are preserved.',
 'Humility of the handmaid and all future generations calling her blessed remain. Witness’s known causal conjunction differs from the model; first-singular accusative mē and feminine ēadige are correctly related.',
 'The mighty one does great things for the speaker, followed by holy name. Both simple preterites meet English perfect meaning; witness sē versus model se is a known demonstrative variant.',
 'Mercy’s beneficiaries are dative ondrǣdendum with internal accusative hine, and the complete generation-to-generation expression is supplied. No demonstrative restores omitted on those.',
 'The mighty are brought down from singular setle and the humble exalted. Witness and key retain singular seat; the former learner plural seats wording was repaired under P17-05.',
 'Hungry are filled with good things and rich dismissed empty. Witness īdle and key ǣmtige are both previously productive empty adjectives; no original empty-lexeme cue requires only ǣmtige.',
 'Israel the servant is accepted in the selected dative receiving/protection frame and God remembers mercy. The model’s dative target is taught; it is not a claim that all other receiving government is invalid.',
 'Speech is to forefathers, Abraham and his seed for ever. The descendant sense and Abraham possessor are explicit; the literal seed image remains.',
 'Mary stays with her about three months, then returns home. Witness mid hiere and key hiere mid are both permissible ordering; supplied duration and owned house remain.'
],
41: [
 'God exists ever, his wisdom is ever begotten of him, and that wisdom is his Son, equal in might to the Father. The complete supplied theological relation does not generalize of into an unrestricted passive-agent marker.',
 'Spirit fills the world’s whole circuit and sustains all things. Witness āfylð/worulde and key gefylð/middangeardes preserve both predicates; sustain is separately taught rather than inferred from ordinary hold.',
 'Doing the Father’s will establishes brother, mother and sister relation to the speaker. Every family predicate and the inner relative subject remains.',
 'Nothing brought into the world and nothing taken away remain under coherent negative scope. Witness nāwiht/worulde/mid ūs differs from key nān ðing/middangearde/ūs mid without missing a fixed lexical cue.',
 'Three plural commands ask/seek/knock retain their matching giving/finding/opening consequences. Supplied impersonal passives preserve dative recipients without inventing an object for omitted it shall.',
 'Father-address and heaven location retain the second-singular relative eart agreeing with ðū; name is the singular subject of the passive hallowing wish. Witness and model match.',
 'Kingdom coming and will coming to pass on earth as in heavens remain two wishes with the explicitly directed verbs first. Tōcume retains the source-required prefix and swā-swā retains its exact cue.',
 'Daily bread, forgiveness of debts and comparison with forgiving debtors all remain. Frozen strong dæghwāmlīcne is grammatical and prompt-compliant; weak model dæghwāmlīcan is also valid. B17-05 repairs the invented weak-only target in the explanation.',
 'Negative lead into temptation and deliverance from evil remain. Witness fram and key of both express separation with the dative; earlier taught ālīesan frame directly licenses fram.',
 'Sīe hit swā matches the short independent wish or assent formula, with singular subjunctive and explicit subject; it is not indicative It is so.',
 'The father gives a stone to dative child; inside the condition hit is the child asking, hine the father asked and hlāfes the genitive requested bread. Both answers retain the distinct giving and asking frames.',
 'God writes the old law with his finger on stone tablets: āwrāt retains the required prefix/past stem, finger is instrumental mid+dative, and on+dative marks the tablets’ writing surface.'
],
42: [
 'Complete supplied love-fell-on frame preserves genitive young man, love as subject and maiden as accusative target; exercise befeallan is not silently replaced by source gefēoll.',
 'Voice of harpers/harping, new song, throne/four beasts and entire 144000 exclusion remain. Witness dēorum for nīetenum and repeated beforan are valid alternatives. New song and high numeral expressions are visibly supplied, not recall tests.',
 'Complete supplied company description preserves singular męnigu plus semantic plural people, all nations/every tribe, white garments, palm branches and hands. No unrestricted mixed-number rule is inferred.',
 'Plural singing and singular salvation-wish to dative God remain, with loud voice and source-selected ofer+dative throne. Witness fronts sīe without changing target.',
 'Plural standing, circuit/genitive throne and intransitive āluton to dative God are correct. B17-02 closes the accompanying-speech dependency with visible ðus cweðende. Witness englas lacks the selected hook; other order differences are harmless.',
 'All six coordinated praise qualities, God as recipient and threefold perpetuity formula remain in the exact supplied singular-sīe doxology; no universal singular coordination rule is taught.',
 'Fox holes and heaven’s birds’ nests preserve holu versus nest plural contrast. The supplied negative place frame licenses subjunctive āhylde without adding may.',
 'Plaiting crown, placing it/reed, bending singular knee and singular royal salute all remain. B17-02 supplies the speech accompaniment. Witness Hāl sīe and key Hāl bēo are defensible optative alternatives; no source requirement makes bēo unique.',
 'Spitting on accusative person, taking reed and beating the head remain three plural past actions; beating is not silently strengthened to killing.'
],
43: [
 'The entire supplied flesh/grass and glory/blossom figure is copied with both distinct predications; interpretation does not replace the literal images.',
 'No man heard the voice in streets: nān/ne express one negation, and the source-directed article omission is preserved.',
 'All three singular commands remain and the exact swā-swā bieman comparison is copied; a physical trumpet does not replace voice as object.',
 'Vocative lady and directional hwider with second-singular gǣst preserve addressee and whither, not static where.',
 'Dēst is second-singular present and yfele adverbial bad conduct; no unnecessary adjective agreement is introduced.',
 'Past doing ill is caused by past censure of the princess, identified as the king’s daughter. Witness varies the causal conjunction only. Key now accurately calls the princess sense specifically taught.',
 'Never/well/arithmetic all remain under plural leornodon; witness and key vary order while preserving nǣfre+ne negative concord.',
 'Both know verbs are plural witon, first future from soon and second under not yet. Witness’s free-relative ðæt corresponds to the reading’s ðæt … nāst; key hwæt is also valid. No unsupported nytan paradigm is required.',
 'Plega mid ðoðore matches the play-with-dative frame. Witness explicitly offers plural Plegiað too, correctly distinguished from the model’s selected singular where English leaves number open.',
 'First-singular negative eating contrasts with the exact supplied concessive others eating/merry. Witness nāwiht and key nān ðing preserve the main negation; eten/sīen remain plural subjunctives.',
 'Desired finite first-singular learning content, of ēow source and relative gē habbað all remain; witness changes object/verb order without abandoning the explicit bracketed finite-clause target.',
 'The key’s Cēos hwilc hiera ðū wille is correct. Witness Cēos ðone hiera ðe ðū wille is a valid people-choice rendering with the stated gender assumption, partitive genitive and second-singular subjunctive; the source does not explicitly require hwilc.',
 'Both educated and high-born qualities, two men, plural came and complete within-hours phrase remain. B17-03 supplies him tōgēanes with dative/postposing. Frozen tōgēanes him is also valid ordering, supported by Cook184.7.',
 'Genitive wooing target is met by key ðǣre æðelan fǣmnan and witness ðæs æðelan mǣdenes; the latter is a taught neuter maiden synonym with correct weak agreement.',
 'Speakers, singular negative report, here, dative God and equal comparison remain. B17-04 supplies contiguous Gode swā gecwēme. Witness ne sīe is valid negative concord; bare nān in the model is independently licensed by BT709 nán I(a), so neither is rejected merely for that difference.',
 'At-first supposition retains the supplied active man/hine/slōge, with thinker distinct from grammatical slayer and without asserting a death. Witness’s matrix order varies acceptably.',
 'All first-plural falling and dative plural feet with one addressee’s possessive match; possessor number is not confused with possessed feet number.',
 'Negated belief omits English do, while the wife proposition uses explicitly requested second-singular subjunctive sīe. Witness only varies the embedded predicate order.',
 'Static hwǣr, singular is and newly taught husband sense of wer match; the spousal relation is not lost to generic man.',
 'First-singular lived, eleven-year accusative duration and dative Egyptian-land location match, with the exact ethnonym supplied rather than reconstructed.'
]
}

for ex, rows in COOK.items():
    for n, note in enumerate(rows, 1):
        NOTES[f'EX-XII-XIII-{ex}-{n:02d}'] = [note]

IMAGE_NOTES = {
 'sources/audits/unit17-source/ex-p22.png': (22,30,'Original joint heading and Exercise37 global omission instruction;37.1 and beginning37.2 checked.'),
 'sources/audits/unit17-source/ex-p23.png': (23,31,'37.2–14 and start38 checked; plural spirits in37.8, complete catalogues and horn chain retained.'),
 'sources/audits/unit17-source/ex-p24.png': (24,32,'38 continuation and39 beginning checked, including final-verb controls, self, explicit wǣre and purpose omission.'),
 'sources/audits/unit17-source/ex-p25.png': (25,33,'39.2–7 and40 beginning checked, including194b desired content and40.1 independent blessed clause/postposition.'),
 'sources/audits/unit17-source/ex-p26.png': (26,34,'40 continuation and41.1–8 checked;40.6 singular seat;41.8 has dæghwāmlīc55 but no weak-only instruction.'),
 'sources/audits/unit17-source/ex-p27.png': (27,35,'41 ending and42.1–7 checked, including high number, collective descriptions and unsupplied-original thus saying.'),
 'sources/audits/unit17-source/ex-p28.png': (28,36,'42.8–9 and all43 checked; singular knee, omitted hand, swā-swā, plural/singular addressees, toward/acceptable and eleven years.'),
 'sources/audits/unit17-source/fb-p174.png': (174,190,'Whole assigned174.7–18 personally read, exact spellings and ten original notes checked, including12a and two17 anchors; prior scene viewed as context only.'),
 'sources/audits/unit17-source/fb-p175.png': (175,191,'Whole assigned175.1–17 personally read with nine notes; Apollo, silence result, performances, singular ungecnāwen wæs and dative audience verified.'),
 'sources/audits/unit17-source/fb-p278.png': (278,294,'Glossary be-twēox among/between supplies selected marked vowel; it does not itself supply complement case.'),
 'sources/audits/unit17-source/fb-p291.png': (291,307,'Glossary ge-cwēme pleasing/acceptable and gecweðan inspected; adjective entry alone does not establish its government.'),
 'sources/audits/unit17-source/fb-p316.png': (316,332,'Glossary tō-gēanes towards/to meet inspected; no case label occurs there.'),
 'sources/audits/unit15-grammar/fb-p94.png': (94,110,'§164 dative verb uses including receiving/speaking; no claimed direct evidence for the four missing whole phrases.'),
 'sources/audits/unit14-grammar/fb-p95.png': (95,111,'§164k pleasing and§165 adjective dative relations personally checked; supports184 note5’s explicit direction.'),
 'sources/audits/unit17-source/fb-p96.png': (96,112,'§167–172 inspected; no claim that this page alone establishes accompanying speech.'),
 'sources/audits/unit14-grammar/fb-p106.png': (106,122,'§201 explicitly allows a preposition after its complement, supporting postposed him tōgēanes when combined with lexical184 evidence.'),
 'build/u17-paradigms-fb-p184.png': (184,200,'Personally viewed colleague-rendered original:184.7 tōgēanes ðǣm cyninge;184.9–10 Dianan swā gecwēme;note5 explicitly See165.'),
 'build/u17-paradigms-fb-p186.png': (186,202,'Personally viewed original186.12 betweox ðǣm cyning and ðǣm folce, a dative human group; original unmarked spelling is distinct from glossary normalization.'),
 'build/u17-paradigms-fb-p195.png': (195,211,'Personally viewed195.3–4 God … ðus cweðende. Direct evidence is singular-subject accompaniment; supplied plural42.5/8 is an adaptation using known participial agreement.'),
 'sources/audits/unit03-source/fb-pdf142-p126.png': (126,142,'Personally viewed126.11 And blētsode hīe, ðus cweðende, with God understood; corroborates the earlier supplied construction without promoting its old milestone.'),
 'sources/audits/unit14-grammar/fb-p100.png': (100,116,'§183 multiple negatives strengthen rather than cancel; top continuation of§179 permits uninflected predicate participles.'),
 'sources/audits/unit17-source/fb-p38.png': (38,54,'§55 says weak sometimes after a possessive, otherwise strong; directly supports both41.8 adjective choices.'),
 'sources/audits/unit14-grammar/fb-p63.png': (63,79,'§106 cweðan/cwæð/cwǣdon/cweden directly verifies æ/ð versus ǣ/d stem distinction addressed by P17-01; the new prose preserves it.'),
 'sources/audits/unit17-coordinator/bt-b1082.jpg': (1082,None,'Main dictionary þūsend I(2)(a) directly prints the same-song exception for hundred-and-forty-four thousands, collective ðæt and final-o ðūsendo. The learner declares acute-to-macron normalization and joined line division.'),
 'sources/audits/unit17-coordinator/wright-p49.png': (49,None,'Wright§90 explicitly gives West Saxon nīewe/nīwe with long vowel. This is quantity evidence, not a separately attested nīwne token.'),
 'sources/audits/unit17-coordinator/wright-p213.png': (213,None,'Wright§433 wilde paradigm gives masculine accusative wildne, the stated model for deriving nīwne.'),
 'sources/audits/unit17-coordinator/wright-p214.png': (214,None,'Wright§434 explicitly includes nīewe/nīwe among adjectives declined like wilde; together with§433 this licenses supplied nīwne by rule.'),
 'build/u17-blind-bt-b0709.jpg': (709,None,'Personally downloaded/viewed BT main709, left-column nán I(a), explicitly without other negatives; resolves43.15 bare nān against also-valid ne concord. Acute signs in quoted scan are not silently altered.')
}
