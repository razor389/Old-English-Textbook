"""Explicit amendments to private initial hypotheses; preserve the witness."""
import json,re
from pathlib import Path
OUT=Path(__file__).resolve().parent
changes={
'37-01':('Hęriað Drihten of heofonum; hęriað hine on hēanessum.','Checked noun hēanes, not invented hēahnes.'),
'37-02':('Hęriað hine, ealle his ęnglas; hęriað hine, eall his mægnu.','Neuter plural eall agreement.'),
'37-04':('Hęriað hine, heofonas heofona, and wætru ðe ofer heofonas sind.','Explicit §172 target requires accusative after ofer.'),
'37-06':('Hē sętte hīe ā ā ā; hē sętte bebod and ne gewīt.','Use checked Ex48 duration expression; no untaught prefixed appoint form.'),
'37-08':('Fȳr and hægel, snāw and īs; gāstas ȳsta ðe his word dōð;','Preserve exact printed longȳ.'),
'37-09':('Muntas and ealle hyllas; wæstmbǣru trēowu and ealle cēderbēamas;','Neuter plural strong adjective; evidenced cedar headword.'),
'37-10':('Dēor and eall nīeten; wyrmas and gefiðrede fugolas;','Exact hint gefiðred; inflect masculine plural.'),
'37-11':('Cyningas eorðan and eall folc; ealdormęnn and ealle dēman eorðan;','Neuter plural eall agreement.'),
'37-12':('Geonge and fǣmnan; ealde mid bearnum;','Source quantity for fǣmne.'),
'37-13':('Hęrien hīe naman Drihtnes; for ðām ðe his ānes nama is ūpāhafen; his wuldor is ofer eorðan and heofon.','Of him alone is genitive; classVI past participle hafen; §172 accusative.'),
'37-14':('Hē ūpāhęfð horn his folces, lof ealra his hālgena, bearna Israeles, folces him nēalǣcendes.','Preserve Israel quantity; weak hālga target; complete participial genitive phrase locally supplied.'),
'38-01':('Se cyning worhte micel elpenbǣnen setl and oferworhte hit mid ðām bętstan golde.','Exact lexical hint oferwyrcean, not oferwrēon.'),
'38-03':('Ðā hīerde hēo Salomones hlīsan and cōm of ðām sūðernum gemǣrum tō Salomone binnan Hierusalem, and hire olfendas bǣron sūðerne wyrta and dēorwierðe gimmas and unrīm goldes.','Select attested precious-gem lexemes; source proper-name phrase supplied.'),
'38-06':('Ðā geseah sēo cwēn Salomones wīsdōm and ðæt mǣre tempel ðe hē geworhte and ðæs cyninges manigfealde ðēnunga.','Use prior productive gewyrcean build; tempel headword; retain plural services.'),
'38-07':('Hēo wæs tō ðan swīðe ofwundrod, ðæt hēo nānne gāst furðor næfde.','Preserve exact tō ðan source hint.'),
'38-08':('Hēo sægde ðā tō ðām cyninge: Sōð is ðæt word ðe ic on mīnum ēðle be ðē and ðīnum wīsdōme hīerde; ac ic nolde ǣr gelīefan ǣr ic self hit gesāwe.','Omit my only, retain self; prescribed preterite subjunctive saw stays final.'),
'38-10':('Ēadige sind ðīne ðegnas and ðīne ðēowan, ðe simle ætforan ðē standað and ðīnne wīsdōm hīerað.','Exact weak noun ðēowa target, rather than strong ðēow.'),
'39-01':('Blētsod sīe se ælmihtiga God, ðe ðē cēas and ðē ofer ðæt rīce Israela gesętte, ðæt ðū dōmas and rihtwīsnesse sętte.','Prior cēosan avoids unsupported prefix; §172 accusative; purpose second singular subjunctive sętte, not indicative sęttest.'),
'39-03':('Salomon ēac forgeaf ðǣre cwēne eall ðæt ðe hēo æt him giernde; and hēo gewęnde ongēan tō hire ēðle mid hire ðegnum.','External direct object eall ðæt; invariant relative ðe internally represents genitive wanted thing without productive case attraction.'),
'39-04':('Salomon wæs ðā mǣrsod ofer eallum eorðlicum cyningum; and ealle ðēoda gewilnodon ðæt hīe hine gesāwen and his wīsdōm hīerden.','Explicit §166 dative; coordinated unprefixed hearing verb from prior repertoire.'),
'39-05':('Swā hwā swā ofer ðissum grundwealle wyrcð gold oððe seolfor oððe dēorwierðe stānas oððe trēowu, strēaw oððe ceaf, ānes gehwilces weorc bið gesweotolod.','Explicit §166 dative and ānes gehwilces; prior wyrcean build sense evidenced Ex41; evidenced manifestation lemma.'),
'39-06':('Gif sēo getimbrung ðurhwunað and ðām fȳre wiðstęnt, ðonne onfēhð se wyrhta edlēan æt Gode his weorces.','Feminine getimbrung; §153e genitive price/value/reward frame, not new for phrase.'),
'39-07':('Nān ēage ne mæg on ðissum līfe gesēon, ne nān ēare hīeran, ne nānes mannes heorte āsmēan ðā ðing ðe God gearcað ðām ðe hine lufiað.','Retain modal can, all negative participants and present prepares; āsmēan is given infinitive reference, not an independent conjugation demand.'),
'40-04':('For ðām ðe se ðe mihtig is dyde mē micele ðing; and hālig is his nama.','Use ordinary preterite for completed deed; no unnecessary unassigned gedōn auxiliary construction.'),
'40-05':('And his mildheortnes is hine ondrǣdendum of cnēorisse on cnēorisse.','God is accusative object of fear; participle dative plural identifies beneficiaries.'),
'40-06':('Hē āwearp ðā mihtigan of setle and ūpāhōf ðā ēaðmōdan.','Simple past conveys completed actions; no extra āweorpan participle system.'),
'40-07':('Hē āfylde ðā hyngrendan mid gōdum, and ðā rīcan hē forlēt ǣmtige.','Simple past; accusative plural weak hungry and predicate empty retain own analyses.'),
'40-08':('Hē onfēng his cniht Israel and gemunde his mildheortnesse.','Simple past avoids unsupported gemund participle; remember past belongs to explicit gemunan system or whole supplied frame.'),
'40-09':('Swā hē spræc tō ūrum fæderum, Abrahame and his sǣde, ā ā ā.','Use checked everlasting expression.'),
'41-04':('Wē nān ðing tō ðissum middangearde ne brōhton, ne magon wē ǣnig ðing heonon ūs mid lǣdan.','Retain this and full negative concord.'),
'41-07':('Tōcume ðīn rīce; geweorðe ðīn willa on eorðan swā-swā on heofonum.','Preserve explicit prefixed tōcuman hint and both verb-first controls.'),
'41-12':('God āwrāt ðā ealdan ǣ mid his fingre on ðām stānenum tabelum.','Stone adjective supported separately; exact tabele weak plural.'),
'42-01':('Ðæs geongan mannes lufu befeoll on ðæt mǣden.','Prompt hint uses befeallan, not gefeallan; follow young-man subject via genitive possessor of love.'),
'42-03':('Ic geseah swā micele męnigu swā nān mann gerīman ne mæg, of eallum ðēodum and of ǣlcre mǣgðe, standende beforan Godes ðrymsetle, ealle mid hwītum gegierelum gescrȳdde and palmtwīg on heora handum healdende.','Retain God, exact headword quantities and palm-twig spelling; referential agreement supplied for collective company.'),
'42-04':('And hīe sungon mid hlūdre stefne: Hǣlu sīe ūrum Gode, ðe ofer his ðrymsetle sitt.','Exact throne spelling, §166 dative.'),
'42-05':('And ealle ęnglas stōdon on ymbhwyrfte his ðrymsetles and Gode āluton, ðus cweðende:','Omit article as required; retain his and exact in-circuit-of paraphrase target; correct unmutated participle stem.'),
'42-06':('Ūrum Gode sīe blētsung and beorhtnes, wīsdōm and ðancung, weorðscipe and stręngðu, ā ā ā.','Checked everlasting expression.'),
'42-07':('Foxas habbað holu, and heofones fugolas nest; sōðlīce Mannes Sunu næfð hwǣr hē his hēafod āhylde.','Use exact adversative sōðlīce target without adding an unnecessary ac.'),
'42-08':('Ðā cęmpan wundon cynehelm of ðornum and sętton on his hēafod and hrēod on his swīðran, and bīegdon heora cnēow beforan him, ðus cweðende: Hāl bēo ðū, Iudea cyning!','Transitive bow knee uses bīegan; exact Iudea hint and cweðende stem.'),
'43-01':('Ǣlc flǣsc is gærs, and ðæs flǣsces wuldor is swilce ðǣra wyrta blōstma.','No invented all before glory; follow bracketed as-if with swilce.'),
'43-03':('Cleopa and ne geswīc ðū; āhęfe ðīne stefne swā-swā bieman.','Checked trumpet headword biema.'),
'43-06':('Hē dyde yfele, for ðām ðe hē tǣlde ðā cwēn, ðæs cyninges dohtor.','Checked princess sense; selected endingless feminine accusative.'),
'43-07':('Hīe nǣfre gerīmcræft wel ne leornodon.','Negative concord with never.'),
'43-13':('Binnan fēawum tīdum cōmon twēgen gelǣrede and æðelborene męnn him tōgēanes.','Course eth spelling retained; high-born and temporal within senses separately assigned.')
}
doc=json.loads((OUT/'candidate-models.json').read_text(encoding='utf-8'))
amends=[]
for r in doc['rows']:
    k=r['source_item_id'][-5:]
    if k in changes:
        new,why=changes[k]
        if new!=r['model']:
            amends.append({'source_item_id':r['source_item_id'],'before':r['model'],'after':new,'reason':why})
        r['model']=new
    r['tokens']=re.findall(r'[A-Za-zÆæÐðÞþǢǣĒēĪīŌōŪūȲȳĀāĘęǼǽ]+(?:-[A-Za-zÆæÐðÞþǢǣĒēĪīŌōŪūȲȳĀāĘę]+)*',r['model'])
    r['stage']='amended audit candidate; precise evidence/status binding in progress'
doc['amendment_record']='sources/audits/unit17-grammar/model-amendments-01.json'
(OUT/'candidate-models.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'model-amendments-01.json').write_text(json.dumps({'schema_version':1,'preserved_initial':'initial-independent-models.json','amendments':amends},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('amended',len(amends))
