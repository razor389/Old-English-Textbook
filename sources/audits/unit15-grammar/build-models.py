"""Independent source-prompt compositions, reconciled with contextual token identities."""
import json,pathlib,copy,hashlib
R=pathlib.Path(__file__).resolve().parents[3]; O=pathlib.Path(__file__).resolve().parent
P=json.loads((R/'sources/audits/unit15-source/exercises-prompts.json').read_text(encoding='utf-8-sig'))['items']
rows=[
('Ǣlc ðe for mīnum naman his hūs oððe his brōðor oððe his sweostor oððe his fæder oððe his mōdor oððe his wīf oððe his bearn oððe his land forlǣtt, him mid hundtēontigum forgolden bið, and hē hæfð ðǣr-tō-ēacan ēce līf.','each + relative; leave/forsake list; resumed impersonal requital with finite verb last','U15-H-28-01'),
('Hē sealde ǣlcum pęning wið his dæges weorce.','dative each; accusative penny; exchange wið+dative',''),
('Hē sęnde hīe on his wīngeard.','send someone into on+accusative',''),
('Hē geseah ōðre on strǣte īdle standan.','substantival others; object infinitive after perception; idle object agreement',''),
('Ðā cwæð hē, Gāð gē ēac on mīnne wīngeard, and ic ēow sęlle ðæt riht is.','plural command; right neuter predicate in ðæt relative',''),
('Ęft hē ēode ūt ymbe ðā siextan and nigoðan tīd, and gelīce dyde.','temporal ymbe+accusative; coordinated ordinal hours; similarly','U15-H-28-06'),
('Ðā ymbe ðā endleftan tīd hē ēode ūt, and funde ōðre standende.','find+present participle; exact eleventh-hour phrase','U15-H-28-07'),
('Ðā cwæð hē, Hwȳ standað gē hēr ealne dæg īdle?','interrogative; accusative duration; plural predicate adjective',''),
('Ðā cwǣdon hīe, For-ðon-ðe nān mann ūs ne hȳrode.','negative concord; weakII hire preterite',''),
('Sōðlice, ðā hit ǣfen geworden wæs, ðā cwæð ðæs wīngeardes hlāford tō his gerēfan, Cleopa ðā wyrhtan, and forgield him hiera mēde.','evening construction; cleopian/forgieldan commands; recipient dative','U15-H-28-10'),
('Eornostlice, ðā ðā cōmon ðe ymbe ðā endleftan tīd cōmon, ðā onfēngon hīe ǣlc his pęning.','temporal and relative ðā; final relative verb; distributive each share; accusative receipt','U15-H-28-07'),
('And ðā ðe ðǣr ǣrest cōmon wēndon ðæt hīe māre onfōn sceolden.','suppose content clause; sculan past prospective; substantive māre accusative; infinitive onfōn',''),
('Ðū dydest hīe ūs gelīce, ðe bǣron hęfignessa on ðisses dæges hǣte.','make object equal to dative; relative subject we inferred from us; burden plural; heat singular',''),
('Nim ðæt ðīn is, and gā; ic wille ðissum eall swā micel sęllan swā ðē.','substantive possession; just as much; dative comparison with ellipsis of giving',''),
('Ne mōt ic dōn ðæt ic wille?','negative question; permission; substantive relative',''),
('Ne cōme ðū tō mē tō wyrceanne wið ānum pęninge?','negative past question; purpose inflected infinitive; exchange wið+dative',''),
('Hē wæs wer and wītga, mihtig on worde and on weorce beforan Gode and eallum folce.','predicate nouns no article; mighty in respect; before dative',''),
('Ðæt is se dōm, ðæt lēoht on middangeard cōm, and męnn lufodon ðīestru swīðor ðonne ðæt lēoht, for-ðon-ðe hiera weorc yfel wǣron.','content apposition; preference comparison between accusative objects; causal clause',''),
('God ne sęnde his sunu on middangeard ðæt hē middangeard dēmde, ac ðæt middangeard ðurh hine hǣled wǣre.','rejected condemning purpose versus intended saving purpose: negation does not deny sending itself; purpose subjunctive and passive; mediated agency',''),
('Ēowru mēd bið miclu, and gē bēoð ðæs Hēahstan bearn; for-ðon-ðe hē is gōd ofer ungeðancfulle and yfele.','future bēon; feminine reward agrees with possessive and predicate; title Highest; kindness toward accusative substantival adjectives','U15-H-29-08'),
('Giefað, and ēow bið giefen.','plural command; impersonal passive recipient',''),
('Se leornungcniht nis ofer his lārēow.','contracted negative copula; rank above accusative',''),
('Ætīew ūs ðīne mildheortnesse, and unne ūs ðīnre hǣlu.','singular show/grant commands; accusative show object versus genitive grant thing',''),
('Ne swęre ðū ðurh heofon, for-ðon-ðe hē is Godes setl; ne ðurh eorðan, for-ðon-ðe hēo is his fōtsceamul; ne ðurh Hierusalem, for-ðon-ðe hēo is ðæs mǣran cyninges burg.','negative command; oath standard ðurh+accusative; grammatical gender; weak mǣre','U15-H-30-01'),
('Ne swęre ðurh ðīn hēafod, for-ðon-ðe ðū ne meaht ān hǣr hwīt oððe blæc wyrcean.','negative command and ability; neuter hair and agreeing object predicates',''),
('Sīe ēower word swā, Hit is, hit nis.','third-person jussive; speech quotation; explicit thus',''),
('Gē hīerdon ðæt cweden wæs, Ēage for ēagan, and tōð for tēð.','hear content; passive saying; exchange for+dative',''),
('Se ðe tōwierpð ān of ðissum lǣstum bebodum, and swā męnn lǣrð, sē bið lǣst hāten on heofona rīce.','break commandment; least adjective rank; teach verb last; passive name',''),
('Se ðe hit dēð and lǣrð, sē bið micel hāten.','coordinate do and teach; great predicate with passive call',''),
('Gē hīerdon ðæt on ealdum tīdum cweden wæs, Ne sleah ðū.','old times; passive saying; negative kill command',''),
('Is hit ðīn eorðe?','copular question; predicative possessive feminine noun',''),
('Hē hæfð æt his gewinne ðæt hē mæg.','from labour with æt; bounded omitted infinitive after can','U15-H-30-09'),
('Sēo sunne forbærnde his æcer.','parch/scorch transitive weakI preterite',''),
('Ðā wegas sceoldon blōstmian, ðā wegas sceoldon blōstmian; swā fægeru brȳd sceal hiere hām forlǣtan.','exact printed blossom lemma; sculan+plain infinitive; so fair a bride with feminine adjective agreement',''),
('Gif hīe magon, lǣt hīe libban būtan mē.','real condition with ability; let+accusative and plain infinitive; without+dative','U15-H-30-12'),
('Hē ne forlǣtt nǣfre ðā ðe on hine gelīefað.','prior productive never+ne; forsake; believe/trust on+accusative',''),
('Ic wāt sōðlice ðæt mīn Ālīesend leofað.','know content; exact live present variant',''),
('On mīnum flǣsce ic gesēo God, ic self and nā ōðer.','future interpretation of present; emphatic self; constituent nā',''),
('Hē wæs lǣred Godes willan tō dōnne.','passive teaching; taught person controls inflected infinitive','U15-H-31-03'),
('Ne lǣd ðū ūs on costnunge, ac ālīes ūs fram yfele.','negative command; deliver accusative person from dative evil',''),
('Sīe ðīn nama gehālgod.','jussive passive',''),
('Geweorðe ðīn willa on eorðan swā-swā on heofonum.','exact prefixed verb first; jussive befall; manner comparison','U15-H-31-06'),
('Nān cyning Engla næs swā micel swā Ælfred.','negative concord contracted past; genitive ethnonym; equal-degree comparison',''),
('Hē feaht wið ðǣm Dęnum; hē dēmde his folc; hē worhte āwęndednessa of Lǣdene; hē wæs lēoðwyrhta.','fight+wiðdative; judge; translations from language; predicate profession',''),
('His mōdor hātte Osburg, and his fæder Æthelwulf.','special passive name-form, not active hēt; coordinated ellipsis','U15-H-31-09'),
('Hē lifde twā and fīftig gēara.','lived selected prior preterite; supplied numeral and genitive years','U15-H-31-10'),
('Hē leornode bēcrǣdinge æfter ðǣm ðe hē twęlf wintra eald wæs.','learn reading; after finite clause; twelve with genitive years in age phrase','U15-H-31-11'),
('His mōdor hæfde āne bōc Engliscra lēoða, ðe hēo gehēt swā hwæðrum hiere twēgra suna swā hīe ǣrest leornode.','indefinite ān; poem genitive; promise recipient; supplied attracted-case freechoice with prospective past subjunctive','U15-H-31-12'),
('Ælfred āscode hiere, Wilt ðū sōðlice ðā bōc ānum uncer sęllan, ðǣm ðe hīe ǣrest ongiett?','ask dative; future intention; personal genitive dual; explicit resumptive recipient; understand',''),
('Asser, Ælfredes bisceop, wrāt āne bōc ðæs cyninges līfes.','appositive named subject; indefinite book with dependent genitive life','')]
assert len(rows)==len(P)==50
D={'schema_version':1,'status':'source_first_grammar_models_pending_exact_token_binding_and_independent_review','visibility':'author_only','origin_category':'new_teaching_material','model_note':'These are new compositions following Cook prompts and hints, not recovered Cook answer texts. All source prompts remain separately preserved.','items':[]}
for p,(txt,targets,helps) in zip(P,rows):
 D['items'].append({'source_item_id':p['source_item_id'],'model':txt,'tokens':[],'token_binding_status':'pending_designer_exact_binding','grammar_targets':targets.split('; '),'local_help_ids':helps.split() if helps else [],'source_evidence_refs':p['evidence_refs'],'review_status':'candidate_for_independent_review'})
binding_path=R/'curriculum/proposals/unit15/author-only-cook-sequence-bindings.json'
if binding_path.exists():
 bindings=json.loads(binding_path.read_text(encoding='utf-8-sig'))
 by_id={s['owner_id']:s for s in bindings['sequences']}
 if all(m['source_item_id'] in by_id and by_id[m['source_item_id']]['text']==m['model'] for m in D['items']):
  for m in D['items']:
   m['tokens']=copy.deepcopy(by_id[m['source_item_id']]['tokens'])
   m['token_binding_status']='exact_contextual_bindings_reconciled'
   m['review_status']='grammar_audit_and_independent_coordinator_review_reconciled'
  D['status']='audited_proposal_ready_for_contract'
  D['token_binding_provenance']={'path':binding_path.relative_to(R).as_posix(),'sha256':hashlib.sha256(binding_path.read_bytes()).hexdigest(),'note':'Designer bound final compositions after an independent initial composition witness; grammarworker reviewed contextual identities and relative-clause roles.'}
(O/'author-only-cook-models.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('50 models published;',sum(len(m['tokens']) for m in D['items']),'token identities;',D['status'])
