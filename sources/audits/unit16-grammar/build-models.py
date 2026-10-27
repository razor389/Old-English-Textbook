"""Independent new compositions under all 59 exact Cook prompt controls.

This is an author-only audit witness, not learner/key prose or source text.
"""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[3]
O=Path(__file__).resolve().parent
P=json.loads((R/'sources/audits/unit16-source/exercises-prompts.json').read_text(encoding='utf-8-sig'))['items']
ROWS=[
('Ic grēte ēow ealle.', 'farewell sense; accusative persons; agreeing all', ''),
('Ðā hīe rēowon swilce twēntig furlanga oððe ðrītig, ðā gesāwon hīe Hǣlend uppan ðǣre sǣ gān.', 'prior rowing relative to seeing; swilce approximation; genitive measure after tens; perception infinitive gān last', 'simple preterite expresses contextual anteriority; no mechanical English perfect'),
('Hē ārās and bebēad ðām winde, and cwæð tō ðǣre sǣ, Gestille.', 'command dative wind; to sea dative; singular subside command', 'intransitive gestillan command frame to verify'),
('Se wind geswāc, and wearð micel smyltnes.', 'intransitive ceased; weorðan came about; no indefinite article', ''),
('Ðū hīerst his stefne, and ðū nǣtst hwanon hē cymð, ne hwider hē gǣð.', 'hear voice; contracted negative know; paired indirect questions', ''),
('Hē geseah twēgen brōðor hiera nett on ðā sǣ sęndan; hīe wǣron fisceras.', 'see object infinitive; plural brethren with one shared net; on accusative direction', ''),
('And hē sægde him, Cumað æfter mē, and ic dō ðæt git manna fisceras sīen; and hīe sōna forlēt-on hiera nettu.', 'said dative; come after dative; no will; dōn finite result clause; dual git with plural finite verb and predicate; immediately left', 'REMOVE temporary hyphen forlēt-on; finite-result construction needs lexical evidence'),
('Gif ðīn hand oððe ðīn fōt ðē ǣswicað, āceorf hit of, and weorp fram ðē; betere ðē is ðæt ðū healt on līf gā, ðonne ðū twā handa and twēgen fēt hæbbe and on ēce fȳr sīe geworpen.', 'conditional injury; cut it off; cast object omitted; dative better; main that retained; than without that; hypothetical competing states; passive cast', 'ǣswician person case and coordinated hand/foot pronoun reference need verification'),
('Gif hwilc mann hæfð hund scēapa and forlīest ān of ðām, ne forlǣtt hē ðā nigon and hundnigontig on muntum and gǣð and sēcð ðæt ðe forwearð?', 'conditional indefinite hwilc; hundred genitive; loss one of those; negative question without do; genitive shared sheep; relative perished', ''),
('And gif hit gelimpð ðæt hē hit finde, sōðlice ic ēow sęcge ðæt hē swīðor ofer ðæt blissað ðonne ofer ðā nigon and hundnigontig.', 'happen content; rejoicing comparison over accusative; explicit than phrase', ''),
('Ðonne hē hām cymð, hē cleopað his frīend and his nēahgebūras tōgædere and cwið, Blissiað mid mē, for-ðon-ðe ic mīn forlorene scēap funde.', 'home adverb; summons; plural rejoice; no have; lost sheep agrees', 'past participle adjectival inflection to verify'),
('And, intō ðām hūse gangende, hīe fundon ðæt cild mid Marian his mēder.', 'same-subject going participle; intō dative; Marian dative with appositive mother', ''),
('Ārīs, and nim ðæt cild and his mōdor on niht, and flēoh tō Egypta lande, and bēo ðǣr oð ðæt ic ðē sęcge.', 'singular command chain; by night; Egyptian genitive; destination dative; prospective until with final verb', ''),
('Hē ðā ārās and nam ðæt cild and his mōdor on niht and fērde on Egypta land, ðæt gefylled wǣre ðæt fram Drihtne ðurh ðone wītgan cweden wæs, Of Egyptum ic mīnne sunu cleopode.', 'executed command; motion on accusative; purpose past subjunctive passive without might; relative subject; fram Lord and mediated ðurh prophet; no have', ''),
('Hwæs magon hīe biddan?', 'genitive thing requested; modal can', ''),
('Sēo sunne gīemð ðæs dæges.', 'gīeman genitive rule over', ''),
('Hīe ne wēndon nāhtes būtan dēaðes selfes.', 'expect genitive; negative concord; except complement shares governing case', 'verify genitive nāhtes and exceptive construction'),
('Ðū geswīcst ðīnes weorces.', 'future present; cease genitive', ''),
('Wēn is ðæt hē frēond finde.', 'possibility subject clause and present subjunctive', ''),
('Hē sægde him, Ic wille gān on fiscnað; hīe sægdon, And wē willað gān mid ðē.', 'direct speech; willan intention and infinitive; fishing pursuit', ''),
('Hīe ēodon ūt and ēodon on scip and ne fēngon nāwiht on ðǣre nihte.', 'went out; boarded bare ship; caught nothing negative concord; on time dative', ''),
('Swā hwā swā ðū sīe, ne forlǣt mē.', 'free choice hypothetical copula; negative command', ''),
('Gif ðū nānne ne finde ðe ðē fēde, węnd hider.', 'hypothetical condition; indefinite relative prospective subjunctive; return command', ''),
('Genōgien mīne hōcas unc bām.', 'suffice third plural wish; dual dative both of us; hooks', 'source p167.13 governs selected exact suffice model'),
('Bēgen ðā cnapan sindon wel gelǣrede.', 'both masculine; educated passive participle agreement', 'lǣran versus gelǣran lexical participle to verify'),
('Hīe wǣron bēgen rihtwīse beforan Gode.', 'both predicate adjective masculine plural; before dative', ''),
('Ic halsige ðē ðurh ðone libbendan God ðæt ðū ūs sęcge gif ðū sīe Crist, Godes Sunu.', 'conjure person; ðurh oath; living weak participle; tell us; dependent yes/no; title without article', ''),
('Ic ēow sęcge, Æfter ðissum gē gesēoð Mannes Sunu on ðā swīðran hand Godes mægenðrymmes sittende and on heofones wolcnum cumende.', 'after these no things; future vision; object participles; on accusative right-hand idiom; cloud plural without article', 'right-hand idiom and majesty noun pending nominal audit'),
('Sīe inc bām æfter incrum gelēafan.', 'impersonal wish; dual dative both; dual possessive agreeing faith', ''),
('Sōðlice Mannes Sunu is tō cumenne on his Fæder wuldre, and ðonne āgylt hē ǣlcum be his āgnum weorce.', 'be plus inflected infinitive intended future; no shall; reward dative; according to dative', ''),
('Ðonne Crist cymð, ðonne nāt nān mann hwanon hē is.', 'when then correlation; contracted negative know; indirect question', ''),
('Hǣlend cleopode and lǣrde on ðām temple and cwæð, Mē gē cunnon, and gē witon hwanon ic eom; and ic ne cōm of mē selfum, ac sē is sōð ðe mē sęnde, ðone gē ne cunnon.', 'cry teach speech; person knowledge versus fact question; reflexive source from self; relative subject and accusative person', ''),
('Gē hine ne cūðon; ic hine cann, and gif ic sęcge ðæt ic hine ne cunne, ic bēo ēow gelīc; ac ic hine cann, and ic healde his sprǣce.', 'preterite known; reported hypothetical knowledge with final verb; no shall; like dative; keep saying', ''),
('Gif ic mē selfne wuldrige, nis mīn wuldor nāwiht; mīn Fæder is sē ðe mē wuldrað, be ðām gē cweðað ðæt hē ēower God sīe.', 'reflexive glorify; verb-first negative apodosis; father no anticipatory it; concerning relative; reported subjunctive', ''),
('Fōh ðisne ðoðor.', 'singular catch command; masculine ball', 'ball lexical decision belongs source analyst'),
('Hwā fēng ðone blacan ðoðor?', 'subject who; caught strong preterite; weak black', ''),
('Gā ðone weg ðe ðū cōme.', 'route accusative; relative route and second-singular past', ''),
('Ic ne plegode nǣfre bęter ðonne ic tō-dæg dyde.', 'negative concord; play comparison; substitute do; today', ''),
('Hēo ne sang nǣfre bęter ðonne hēo nū dyde.', 'negative concord; singing comparison; substitute do; now at narrated time', ''),
('Ðrīwa ic ðolode forlidennesse; āne niht and ānne dæg ic wæs on ðissere sǣ.', 'thrice; suffered shipwreck; accusative duration; this sea dative', ''),
('Ic wiste sumne mann sē ðe wæs ōð ðone ðriddan heofon lǣded and ðǣr hīerde ðā word ðe nān eorðlic mann ne mōt sprecan.', 'know person with witan; relative passive; until third heaven accusative; word relative; may not speak', 'verify witan person and lǣdan unprefixed participle'),
('Ēalā, hū nearu is ðæt geat and se weg ðe tō līfe lǣtt, and swīðe fēawe sindon ðe ðone weg findað.', 'narrow gate and way; relative final verb; substantive few with relative; omitted there', 'singular agreement for paired gate/way supplied or explicitly taught'),
('Hīe cumað tō ēow on scēapa gegierelum, ac innan hīe sindon wulfas.', 'toward dative; sheep genitive; clothing locative; within adverb; predicate wolves', ''),
('Ðā hē ðǣre burge geate nēalǣhte, ðā wæs ðǣr dēad mann boren.', 'approach dative; genitive city; then there distinct; passive carrying', ''),
('Ic gesēo mǣgden geond ðā strǣt iernan.', 'perception accusative and infinitive; along street accusative', ''),
('Smire mē mid ęle.', 'anoint accusative person with instrumental phrase', ''),
('Sęllað ūs of ēowrum ęle.', 'plural give; dative recipients; of partitive substance dative', ''),
('Gif se Sunu ēow ālīest, gē bēoð sōðlice frēo.', 'deliver; contextual later state no shall; indeed; predicate free plural', ''),
('Ne dēmað gē be ansīene, ac dēmað rihtne dōm.', 'negative plural command; appearance dative; cognate accusative judgement', ''),
('Ðā bewęnde hē hine tō ðām wīfe and cwæð, Gesihst ðū ðis wīf? Ic ēode intō ðīnum hūse; ðū ne sealdest mē wæter tō mīnum fōtum; ðēos ðwōh mīne fēt mid hiere tēarum.', 'reflexive turn; see woman; enter intō dative; gave not; water purpose; this no one or hath; wash feet with tears', 'female demonstrative human reference after neuter wīf explicitly bound'),
('Ðū mē coss ne sealdest; ðēos, siððan ic inn ēode, ne geswāc ðæt hēo mīne fēt cyste.', 'gave final; no indefinite article; this without one; since entered; cease not plus finite kiss clause without hath', 'cease+finite clause requires checked local scaffold'),
('Mīn hēafod ðū mid ęlum ne smirede; ðēos smirede mīne fēt mid sealfe.', 'head fronted; oils plural; no didst; anoint simple past; ointment dative', ''),
('For-ðon ic ðē sęcge, Manega synna hiere sindon forgiefene, for-ðon-ðe hēo mē swīðe lufode.', 'therefore say recipient; sins forgiven recipient; loved finite last; degree much', ''),
('Lǣs lufað ðǣm ðe lǣs forgiefen is.', 'less accusative degree; dative relative recipient with unexpressed matrix subject; passive less', 'attracted dative construction needs explicit bounded support'),
('Hit ne ālīefð ðē hīe tō wīfe habban.', 'impersonal permission no is; dative person; have her as wife', 'active impersonal spelling and construction pending lexical image'),
('Ðā gehēt hē mid āðe hiere ðæt tō sęllanne, swā hwæs swā hēo hine bǣde.', 'promise dative recipient; oath; giving intended thing; request person accusative and thing genitive; prospective past subjunctive no should', 'safe resumptive accusative ðæt plus internally genitive free-choice; evidence required'),
('Ðā cwæð hēo, fram hiere mēder myngod, Sęle mē on disce Johannes ðæs fuluhteres hēafod.', 'passive admonished subject supplement; agent fram; give command; dish; Baptist appositive genitive', 'Johannes case spelling and myngod agreement pending nominal audit'),
('Ðā āsęnde hē and behēafdode Johannem on ðām cwearterne.', 'send absolute; behead accusative John; prison locative', 'proper-name declension pending nominal audit'),
('And man brōhte his hēafod on disce.', 'generic man one; brought direct object; in dish', ''),
]
assert len(ROWS)==len(P)==59
D={'schema_version':1,'chapter':'ch16','status':'independent_initial_compositions_pending_primary_reconciliation','visibility':'author_only','origin_category':'new teaching material','source_text_separate':True,'items':[]}
for p,(text,targets,uncertainty) in zip(P,ROWS):
    D['items'].append({'source_item_id':p['source_item_id'],'source_prompt':p['prompt'],'model':text,'grammar_targets':targets.split('; '),'source_evidence_refs':p['evidence_refs'],'tokens':[],'unresolved':([uncertainty] if uncertainty else []),'review_status':'candidate awaiting exact lexical and construction verification'})
(O/'author-only-cook-models.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Published',len(D['items']),'independent initial models; no claim of final acceptance.')
