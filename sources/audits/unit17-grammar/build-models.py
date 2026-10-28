"""PRIVATE AUTHOR AUDIT. Candidate sequences, not a learner answer key.

Initial models are independent working hypotheses. Exact controls, morphology,
senses and evidence are reconciled before these can become contract inputs.
"""
import json, re
from pathlib import Path
OUT=Path(__file__).resolve().parent
MODELS={
37:[
'Hęriað Drihten of heofonum; hęriað hine on hēahnessum.',
'Hęriað hine, ealle his ęnglas; hęriað hine, ealle his mægnu.',
'Hęriað hine, sunne and mōna; hęriað hine, ealle steorran and lēoht.',
'Hęriað hine, heofonas heofona, and wætru ðe ofer heofonum sind.',
'Hęrien hīe naman Drihtnes, for ðām ðe hē gecwæð and hīe wǣron worhte; hē bebēad and hīe wǣron gesceapene.',
'Hē gesętte hīe ā and ēcelīce; hē sętte bebod and ne gewīt.',
'Hęriað Drihten of eorðan, dracan and ealle nēowolnessa.',
'Fȳr and hægel, snāw and īs; gāstas ysta ðe his word dōð.',
'Muntas and ealle hyllas; wæstmbǣre trēowu and ealle cederas.',
'Dēor and eall nīeten; wyrmas and gefiðere fugolas.',
'Cyningas eorðan and ealle folc; ealdormęnn and ealle dēman eorðan;',
'Geonge and fæmnan; ealde mid bearnum;',
'Hęrien hīe naman Drihtnes; for ðām ðe his nama āna is ūpāhęfen; his wuldor is ofer eorðan and heofonum.',
'Hē ūpāhęfð horn his folces, lof ealra his hālgena, bearna Israēles, folces him nēalǣcendes.'
],
38:[
'Se cyning worhte micel elpenbǣnen setl and oferwrēah hit mid ðām bętstan golde.',
'Sum cwēn wæs on ðām dagum be sūðan, hāten Saba.',
'Ðā hīerde hēo Salomones hlīsan and cōm of ðām sūðernum gemǣrum tō Salomone binnan Hierusalem, and hire olfendas bǣron sūðerne wyrta and dēorwyrðe gimmstanas and unrīm goldes.',
'Sēo cwēn hæfde ðā sprǣce wið Salomon and sægde him swā hwæt swā hēo on hire heortan ðōhte.',
'Salomon hīe ðā lǣrde and sægde hire ðæt gemet ealra ðāra worda ðe hēo hine āscode.',
'Ðā geseah sēo cwēn Salomones wīsdōm and ðæt mǣre templ ðe hē getimbrode and ðæs cyninges mænigfealde ðēnunge.',
'Hēo wæs tō ðām swīðe ofwundrod, ðæt hēo nānne gāst furðor næfde.',
'Hēo sægde ðā tō ðām cyninge: Sōð is ðæt word ðe ic on mīnum ēðle be ðē and ðīnum wīsdōme hīerde; ac ic nolde ǣr gelīefan ǣr ic hit gesāwe.',
'Māra is ðīn wīsdōm and ðīn weorc ðonne se hlīsa wǣre ðe ic hīerde.',
'Ēadige sind ðīne ðegnas and ðīne ðēowas, ðe simle ætforan ðē standað and ðīnne wīsdōm hīerað.'
],
39:[
'Blētsod sīe se ælmihtiga God, ðe ðē gecēas and ðē ofer ðǣm rīce Israēla gesętte, ðæt ðū dōmas and rihtwīsnesse sęttest.',
'Hēo forgeaf ðām cyninge hund and twēntig punda goldes and męnigeo dēorwyrðra wyrta and dēorwyrðra stāna.',
'Salomon ēac forgeaf ðǣre cwēne swā hwæs swā hēo æt him giernde; and hēo gewęnde ongēan tō hire ēðle mid hire ðegnum.',
'Salomon wæs ðā mǣrsod ofer ealle eorðlice cyningas; and ealle ðēoda gewilnodon ðæt hīe hine gesāwen and his wīsdōm gehīerden.',
'Swā hwā swā ofer ðis grundweall timbrað gold oððe seolfor oððe dēorwyrðe stānas oððe trēowu, strēaw oððe ceaf, ǣlces gewilces weorc bið geswutelod.',
'Gif ðæt getimbrung ðurhwunað and ðām fȳre wiðstęnt, ðonne onfēhð se wyrhta edlēan æt Gode for his weorce.',
'Ne gesiehð ēage on ðis līf, ne gehīerð ēare, ne āsmēað mannes heorte ðā ðing ðe God gegearcode ðām ðe hine lufiað.'
],
40:[
'Se ęngel grētte Marian and sægde ðæt hēo mid Godes gife āfylled wǣre, and ðæt God hire mid wǣre; and hēo wæs blētsod betwēox wīfum.',
'Mīn sāwol mǣrsað Drihten, and mīn gāst blissode on Gode mīnum Hǣlende.',
'For ðām ðe hē geseah his ðīnenne ēaðmōdnesse; sōðlīce, heonanforð ealle cnēorissa mē ēadige sęcgað.',
'For ðām ðe se ðe mihtig is hæfð mē micele ðing gedōn; and hālig is his nama.',
'And his mildheortnes is him ondrǣdendum of cnēorisse on cnēorisse.',
'Hē hæfð ðā mihtigan of setle āworpen and ðā ēaðmōdan ūpāhęfen.',
'Hē hæfð ðā hyngrendan mid gōdum āfylled, and ðā rīcan hæfð hē ǣmtige forlǣten.',
'Hē hæfð his cniht Israel onfangen and his mildheortnesse gemund.',
'Swā hē spræc tō ūrum fæderum, Abrahame and his sǣde, ā on ēcnysse.',
'Maria wunode hire mid swilce ðrīe mōnaðas and gewęnde ðā tō hire āgnum hūse.'
],
41:[
'God wæs ǣfre, and ǣfre wæs his wīsdōm of him ācęnned; and se wīsdōm is his Sunu, efenswā mihtig swā se Fæder.',
'Godes Gāst gefylð ealne ymbhwyrft middangeardes, and hē healt ealle ðing.',
'Se ðe mīnes Fæder willan wyrcð, hē is mīn brōðor and mīn mōdor and mīn sweostor.',
'Wē nān ðing tō middangearde brōhton, ne magon wē ǣnig ðing heonon ūs mid lǣdan.',
'Biddað, and ēow bið geseald; sēcað, and gē findað; cnuciað, and ēow bið geopenod.',
'Ūre Fæder, ðū ðe eart on heofonum, sīe ðīn nama gehālgod.',
'Cume ðīn rīce; geweorðe ðīn willa on eorðan swā-swā on heofonum.',
'Sęle ūs tōdæg ūrne dæghwāmlīcan hlāf; and forgief ūs ūre gyltas, swā wē ūrum gyltendum forgiefað.',
'And ne lǣd ðū ūs on costnunge, ac ālīes ūs of yfele.',
'Sīe hit swā.',
'Hwilc fæder sęlð his bearne stān, gif hit hine hlāfes bitt?',
'God āwrāt ðā ealdan ǣ mid his fingre on ðām stǣnenum tabulum.'
],
42:[
'Ðæs geongan mannes lufu gefeoll on ðā fæmnan.',
'Ic hīerde ðāra hearpera stefne mid heora hearpum hearpiendra; and hīe sungon nīwe lēoð beforan ðām ðrȳmsetle and ðām fēower nīetenum; and nān mann ne mihte ðæt lēoð leornian būton ðām hunde and fēowertig and fēower ðūsendum.',
'Ic geseah swā micele męnigeo swā nān mann gerīman ne mæg, of eallum ðēodum and of ǣlcre mǣgðe, standende beforan ðām ðrȳmsetle, ealle mid hwītum gegierelum gescrȳdde and palmwīga on heora handum healdende.',
'And hīe sungon mid hlūdre stefne: Hǣlu sīe ūrum Gode, ðe ofer his ðrȳmsetle sitt.',
'And ealle ðā ęnglas stōdon ymb ðæt ðrȳmsetl and Gode āluton, ðus cwęðende:',
'Ūrum Gode sīe blētsung and beorhtnes, wīsdōm and ðancung, weorðscipe and stręngðu, ā on ēcnysse.',
'Foxas habbað holu, and heofones fugolas nest; ac sōðlīce Mannes Sunu næfð hwǣr hē his hēafod āhylde.',
'Ðā cęmpan wundon cynehelm of ðornum and sętton on his hēafod and hrēod on his swīðran, and būgon heora cnēow beforan him, ðus cwęðende: Hāl bēo ðū, Iūdēa cyning!',
'And hīe spǣtton on hine and nāmon hrēod and bēoton his hēafod.'
],
43:[
'Ǣlc flǣsc is gærs, and eall ðæs flǣsces wuldor is swā ðǣra wyrta blōstma.',
'Nān mann ne hīerde his stefne on strǣtum.',
'Cleopa and ne geswīc ðū; āhęfe ðīne stefne swā-swā bȳman.',
'Hlǣfdige, hwider gǣst ðū?',
'Ðū dēst yfele.',
'Hē dyde yfele, for ðām ðe hē tǣlde ðā cwēne, ðæs cyninges dohtor.',
'Hīe nǣfre gerīmcræft wel leornodon.',
'Gē witon sōna hwæt gē gīet ne witon.',
'Plega mid clīewene!',
'Ic nān ðing ne ete, ðēah ðe ōðre męnn eten and blīðe sīen.',
'Ic gewilnie ðæt ic of ēow ðæt andgiet leornie ðe gē habbað.',
'Cēos hwilc heora ðū wille.',
'Binnan fēawum tīdum cōmon twēgen gelǣrede and æþelborene męnn him tōgēanes.',
'Ic gierne ðǣre æðelan fæmnan.',
'Wē ealle sęcgað ðæt nān mann hēr Gode swā andfęnge sīe swā hē.',
'Ǣrest hē wēnde ðæt hine man slōge.',
'Wē ealle feallað tō ðīnum fōtum.',
'Ic ne gelīefe ðæt ðū mīn wīf sīe.',
'Hwǣr is mīn wer?',
'Ic lifde endleofan gēar on Ægypta lande.'
]}
rows=[]
for ex,models in MODELS.items():
    for item,model in enumerate(models,1):
        rows.append({'source_item_id':f'EX-XII-XIII-{ex:02}-{item:02}',
        'model':model,'origin_category':'new teaching material','stage':'provisional independent audit hypothesis',
        'tokens':re.findall(r"[A-Za-zÆæÐðÞþǢǣĒēĪīŌōŪūȲȳĀāĘęǢǣǼǽ]+(?:-[A-Za-zÆæÐðÞþǢǣĒēĪīŌōŪūȲȳĀāĘę]+)*",model),
        'controls_checked':False,'morphology_checked':False,'sense_frames_checked':False})
doc={'schema_version':1,'chapter':'ch17','access':'author-only; exclude from blind reviewers',
 'warning':'Provisional independent models for dependency discovery. Not authoritative answers; unresolved lexical and morphology choices require the accompanying audit and primary-image evidence.',
 'source_group':'XII, XIII','rows':rows,'count':len(rows)}
assert len(rows)==82
for name in ['initial-independent-models.json','candidate-models.json']:
    p=OUT/name
    if name=='initial-independent-models.json' and p.exists():continue
    p.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(len(rows),'candidate sequences written')
