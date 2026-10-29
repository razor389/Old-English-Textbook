"""Catalogue only personally viewed images; retain actual printed/scan locators."""
import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
def save(p,d):(O/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
records=[]
def image_record(id,source,path,page,observation,pdf=None,section=None):
    assert (R/path).exists(),path
    records.append({'evidence_id':id,'source_id':source,'origin_category':'exact source','origin_scope_note':'New compositions and rule-derived cells are separate from these inspected source images.','images':[{'image_path':path,'image_sha256':sha(path),'printed_page':page,'pdf_page_one_based':pdf,'personally_viewed':True,'actual_view_claim':'The Unit16 grammar auditor personally opened and inspected this exact image in this session. OCR/search was a locator only.','entry_or_section':section,'verification_observations':observation}],'verification_scope':'Supports the stated lexical class, form, or construction. Rule-derived cells are not falsely described as separate attestations.'})
FB={
50:('unit16-grammar','Complete se demonstrative paradigm; dative ðǣm with variant ðām. Existing selected article forms remain unchanged.'),
51:('unit16-grammar','§§85–87 this demonstrative and relative strategies; §87b demonstrative plus ðe. This is not alone evidence for unrestricted case attraction.'),
54:('unit15-grammar','§93 separates present, first/third-singular preterite, plural/second-singular preterite, and participial stems.'),
55:('unit15-grammar','§95 complete strong bindan/fōn finite and nonfinite endings; note shortened plural -e immediately before following subject wē/gē.'),
58:('unit16-grammar','§101 names ðwēan among classVI contracted verbs; distinguishes contracted classes and their different stems.'),
59:('unit14-grammar','§102 classI includes (ā)rīsan and swīcan; contract imperative -h rule is not a rule for every strong verb.'),
60:('unit14-grammar','ClassI s-stem rīsan has rīst; §103 classII includes (for)lēosan and gives s/r alternation by comparison with cēosan.'),
61:('unit15-grammar','§103 second/third-singular forlīest; §104 classIII bindan and eo-r stems, with iernan explicitly under the bindan pattern.'),
62:('unit15-grammar','ClassIII umlaut and consonant contractions; findan usual3sg funde is explicitly noted. Earlier selected1sg fand remains valid.'),
63:('unit15-grammar','ClassV giefan gives giefan, geaf, gēafon, giefen, establishing the checked inherited stems for forgiefan. Niman and cuman principal parts are also printed.'),
64:('unit15-grammar','ClassV biddan and related strong systems; contraction/umlaut in sēon; classVI introduction. Prior selected giefan/forgiefan principal identity remains unchanged.'),
65:('unit14-grammar','§107 explicitly conjugates ðwēan like slēan: slōg/slōgon/slægen and present sliehst/sliehð establish the contracted model.'),
66:('unit14-grammar','§109 gangan is conjugated like bannan; its use alongside gān is separately explained. Only a supplied participle is required here.'),
67:('unit15-grammar','§110 lǣtan/lēt/lēton/lǣten; fōn/fēng/fēngon/fangen. The selected forlǣtan command follows its present stem.'),
68:('unit15-grammar','§113 weakI principal stems hīeran, sęndan, lǣdan, gierwan; -de/-te and consonant-specific subclasses.'),
69:('unit15-grammar','§113 rw/lw verbs follow gierwan; present may retain or lose w. D-stem subclasses and irregular weakI transitions are bounded explicitly.'),
72:('unit15-grammar','Full weakI paradigms hīeran, sęllan, fremman, nęrian: indicative, subjunctive, imperative, infinitives, participles.'),
73:('unit15-grammar','§§118–119 weakII lufian present and imperative; -ie/-ast/-að/-iað and -a command distinguished.'),
74:('unit15-grammar','WeakII preterite -ode/-odest/-odon and -od participle; g/i and past-vowel alternatives are variants, not silently selected cells.'),
75:('unit16-grammar','§122 libban has present participle libbende; §123 sęcgan selected and variant stems, including sęge imperative.'),
76:('unit14-grammar','§126 complete witan and explicit separate negative nytan. Earlier wāt/wāst plus ne does not require importing nytan.'),
88:('unit15-grammar','Elementary syntactic agreement and apposition; source appositions remain distinct from independent inflection lessons.'),
91:('unit15-grammar','§156 genitive complements: biddan request, gīeman govern, wēnan expect; lexical government is not generic object case.'),
92:('unit14-grammar','§156k geswāc his weorces; §157 genitive route ðæs weges; §159 genitive with a second governed case.'),
93:('unit14-grammar','§159b combines accusative person and genitive thing in hine fultumes bǣdon and mildsa biddan wuldres Aldor. Dative roles and reflexive examples follow.'),
94:('unit15-grammar','§§163–164 dative with approach and verbal classes including command/speech; do not infer the same case for every English to.'),
95:('unit14-grammar','§165 dative with suitable/dear/useful and related adjectives; §166 dative prepositions. Named lexical meaning remains separately required.'),
96:('unit16-grammar','§168 accusative objects/cognate accusative; §169 accusative actor of perception infinitive; §170 extent.'),
97:('unit15-grammar','§172 preposition cases and on motion/rest distinction explicitly not universal; §173 object predicates and §174 instruments.'),
100:('unit14-grammar','§179 predicative participles may be uninflected; §183 negative concord; §184a dative reflexives with movement/other particular verbs.'),
101:('unit15-grammar','Passive and tense discussion; English periphrases do not force identical OE auxiliaries.'),
102:('unit15-grammar','§189 coordination can be singular where nouns denote essentially one thing; §190 impersonal subjects may be understood. The gate/way case is supplied locally.'),
103:('unit15-grammar','§193 optative/subjunctive in wishes, concessions and free-choice constructions.'),
104:('unit15-grammar','§194 expectation, report and request; §195 purposes. Report morphology is not a mechanical English backshift rule.'),
105:('unit15-grammar','§196 conditional and indefinite-relative subjunctive uses; §198 infinitives and their complements.'),
106:('unit15-grammar','§200 inflected infinitive and tō; specific lexical selection remains independently audited.'),
167:('unit16-grammar','Lines10–14 expectation Wēn is ðæt, find/miltsie, genyhtsumien unc bǣm mīne lȳtlan ǣhta and on fiscnoð. Books is an exercise adaptation, not the reading noun.'),
168:('unit16-source','Complete gymnasium scene opening: iernan perception, gesmierwed, plural Gehīere,gē, āgan began, playing companions and ball.'),
169:('unit16-source','Næfde is visibly negative; pronoun ambiguity remains. Top is the OE object, not the Latin shoulder. Arn and ðæs weges are explicit.'),
170:('unit16-source','Dōn substitutes for bathing in action comparison; nāt remains locally supplied; note15 explicitly marks mixed direct/indirect invitation.'),
275:('unit15-grammar','Glossary āginnan begin versus āgān depart; ālīefan permit and ālīesan deliver weakI.'),
279:('unit14-grammar','Glossary bewęndan turn (§113,184), blissian rejoice (§118), biddan request/beseech.'),
284:('unit16-source','Glossary ęfthweorfan return strongIII and Egypta/ęle lexical contexts.'),
288:('unit15-grammar','Forlēosan lose and forloren connection; forgiefan give/grant only here. The forgiveness sense is supported by the explicit Cook36.5–6 source prompts, not falsely attributed to this entry.'),
290:('unit14-grammar','Glossary gangan go; related prefixed entries must retain distinct lexeme identities.'),
292:('unit15-grammar','Gefyllan fill/end/finish/accomplish; gelǣred taught/trained/skilled as past participle of lǣran; gehātan promise.'),
296:('unit16-grammar','Gīeman explicitly glossed rule over and referred to§156f, resolving the proposed unnecessary substitution by wealdan.'),
297:('unit15-grammar','Grētan greet/salute/take leave of; hālsian conjure/implore/entreat; Hǣlend Jesus.'),
298:('unit15-grammar','Healdan explicitly hold/observe/maintain/keep/reserve, supporting the new keep-a-saying sense.'),
301:('unit15-grammar','Iernan run/revolve strongIII; lǣdan lead/bring/take/carry, supporting the carried-person passive.'),
309:('unit14-grammar','Plegian play/act weakII; ordinary intransitive play is not inferred only from game-equipment nouns.'),
323:('unit15-grammar','Wuldrian glorify/magnify/celebrate weakII; witan know.'),
}
for p,(owner,obs) in FB.items():image_record('U16-G-FB'+str(p),'cook_fb_1895_2',f'sources/audits/{owner}/fb-p{p}.png',p,obs,p+16)
for p in range(18,23):image_record('U16-EX-P'+str(p),'cook_ex_1895',f'sources/audits/course-map/ex-page{p}.png',p,'Personally read the complete exact English exercise prompt image, including all parenthetic headwords, omissions, section references and word-order controls. The source editor’s item transcription is independently reconciled.',p+8)
for p,owner,obs in [(38,'unit16-grammar','Anoint gesmierwan; admonish myngian; allow ālīefan. The unprefixed smierwan headword is independently controlled by Exercise36.'),(44,'unit16-grammar','Deliver ālīesan weakI.'),(48,'unit16-source','Free frēo explicitly has nominative plural frige; fishing is fiscnoð. These spellings are personally verified against the printed entries.'),(49,'unit15-grammar','Girl mǣden, without g; go includes faran and fēran; give and glosses remain separate from new models.'),(54,'unit16-grammar','Lose forlǣtan/forlēosan and make dōn; glossary is a lexical-class locator, not a universal construction license.'),(59,'unit16-grammar','Rejoice blissian weakII; adjacent entries distinguish other senses.'),(63,'unit16-grammar','Street strǣt (§51b); suffice/be sufficient genyhtsumian weakII; subside gestillan. Selected Geswīc is independently attested by BT.')]:image_record('U16-G-EX'+str(p),'cook_ex_1895',f'sources/audits/{owner}/ex-p{p}.png',p,obs,p+8)
for p,path,obs in [
(174,'sources/audits/unit16-source/wright-p174.png','§355 complete neuter ja-stem cyn(n) table has zero nominative/accusative plural.'),
(175,'sources/audits/unit16-source/wright-p175.png','§356 explicitly lists nett with cyn(n); no invented nettu plural.'),
(258,'sources/audits/unit04-grammar/wright-p258-pdf278.png','§498 iernan, arn, urnon, urnen; findan fand/funde variants; classIII gieldan and ceorfan stems.'),
(262,'sources/audits/unit05-grammar/wright-p262-pdf282.png','ClassVI contracted slēan has singular preterite slōg or slōh; the h variant is explicit, not inferred by modernizing the source.'),
(263,'sources/audits/unit05-grammar/wright-p263-pdf283.png','The same contracted classVI account explicitly includes þwēan, supporting the selected ðwōh singular beside the g plural stem.'),
(270,'sources/audits/unit06-grammar/wright-p270-pdf290.png','§529 gierwan complete present indicative and imperative: gierwe/gierest/giereð/gierwað; giere command.'),
(271,'sources/audits/unit06-grammar/wright-p271-pdf291.png','Gierwan complete preterite and participle; gierede/gieredest/gieredon and gier(w)ed.'),
(274,'sources/audits/unit06-grammar/wright-p274-pdf294.png','§533 explicitly conjugates smierwan like gierwan; no guessed imperative ending needed.')]:image_record('U16-G-WRIGHT'+str(p),'wright_oe_1914',path,p,obs,p+20)
BT=[
('DON',208,'unit06-grammar','Main208b dōn: exact Ic dō ðæt gyt bēoð manna fisceras; separate substitute-action examples.'),
('CUNNAN',174,'unit06-grammar','Main174b cunnan I acquaintance with persons; II skill with infinitive.'),
('GESWICAN',449,'unit16-grammar','Main449a absolute cessation with wind, genitive work and explicit imperative Geswīc. Finite negative cessation clause verified separately.'),
('ALIEFAN',35,'unit16-grammar','Main35b alȳfan/ālīefan permit and impersonal licet construction; dative permitted person.'),
('AESWICIAN',20,'unit16-grammar','Main20a ǣ-swícian weak -ode/-od and offend/stumble example; BT quantity/spelling is not silently substituted for Cook’s headword.'),
('SIDTHAN',879,'unit16-grammar','Main879b siððan II(1) quotes Luke7.45: ne geswāc ðæt hēo mīne fēt ne cyste, with both negatives.'),
('SMIRWAN',889,'unit16-grammar','Main889a/b smirwan variants; smire/smirede/smyredest and anointing with material. Selected ie paradigm follows Cook/Wright, variants remain alternatives.'),
('AGYLDAN',30,'unit16-coordinator','Main30b ā-gyldan gives ðū-gyltst,hē-gylt, preterite geald/guldon; separately weak ā-gyltan means sin/be guilty.'),
('AGYLDAN-PRINCIPALS',29,'unit16-coordinator','Main29b ā-gildan/-gieldan/-gyldan repay/reward, geald/guldon/golden; dative reward recipient.')]
for tag,p,owner,obs in BT:image_record('U16-G-BT-'+tag,'bosworth_toller_1898_1921',f'sources/audits/{owner}/bt_b{p:04d}.jpg',p,obs,section='Main1898; entry noted in observation')
image_record('U16-G-MATTHEW132','matthew_kemble_hardwick_1858','sources/audits/unit16-grammar/matthew-p132-300.png',132,'Left column Matthew16.27 visibly reads mannes Sunu ys to cumenne; the bottom apparatus explicitly gives manuscript A cumanne. This directly supports the bounded impending-coming construction. The same clause has agylt æghwylcum be hys agenum worce, corroborating contracted3sg reward and dative recipient. Source spelling is preserved here; is tō cumanne in the new model selects actual course forms, not an undeclared transcription change.',142,'Matthew16.27, left column and bottom apparatus')
# Prior-learning evidence is the actual cumulative record plus actual contracts, not a stale agent summary.
prior_tags=['ARTICLE','WEORPAN','COMPARATIVE','NIMAN','FARAN','CUMAN','GESEON','PERCEPTION','NOMINAL-SELECTION']
for tag in prior_tags:
    paths = ['lexicon/entries.json', 'curriculum/grammar.json'] + [f'chapters/ch{n:02d}/coverage.json' for n in range(1, 16)]
    records.append({'evidence_id': 'U16-PRIOR-' + tag, 'source_id': 'active_course_through_ch15', 'origin_category': 'new teaching material', 'origin_scope_note': 'Actual earlier active-course teaching records; no Unit16 milestone is inferred from the evidence label.', 'files': [{'path': p, 'sha256': sha(p)} for p in paths], 'verification_scope': 'Read actual source contracts and cumulative records; form/sense/feature IDs, surfaces, analyses and earliest milestones are retained. Exact contextual selections are in the dependency and token ledgers.'})
save('evidence-catalog.json',{'schema_version':1,'chapter':'ch16','auditor':'unit16_grammar','records':records,'unknown_references':[],'no_unviewed_acceptance_claim':True,'external_evidence_refs':['U16-C06-REWARD'],'printed_line_policy':'Reading source line IDs are editorial counts matched to printed marginal anchors; they are not silently claimed as fully printed line numbers.'})
print(len(records),'evidence records')
