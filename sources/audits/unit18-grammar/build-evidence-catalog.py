import json,re,hashlib
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parents[2]
files=['verbal-systems.json','senses-constructions-support.json','reading-verbal-bindings.json','numeric-control-analysis.json','candidate-verbal-bindings.json']
refs=set()
for fn in files:refs.update(re.findall(r'U18G-[A-Z0-9-]+',(O/fn).read_text(encoding='utf8')))
fb={
12:'§17 i-umlaut table, including ā→ǣ.',
41:'§62 permits uninflected predicative past participles; §61 distinguishes participles from agent nouns.',
45:'§77 irregular adverb comparison, explicitly mā/mǣ more.',
52:'§87d invariant relative ðe; §89a nāhwæðer neither; §89b free-choice forms.',
55:'§95 complete strong finite/nonfinite paradigm; expanded plural/person matrices derive from displayed rows.',
58:'§101 contracted verbs, including ðwēan, and contracted principal-part distinction.',
59:'§102 strongI rīpan class rule; long ī retained in citation/infinitive pair.',
60:'§103 strongII bēodan/bēad/budon/boden; tēon/tēah/tugon/togen.',
63:'§105 strongIV stelan/stæl/stǣlon/stolen and present i; cuman/cumen and niman/nōm exceptions.',
64:'§106 strongV and contracted gesēon, present/stem and umlaut distinctions.',
65:'§107 strongVI, slægen/slagen variants, contraction and swerian.',
66:'§109 reduplicating cnāwan/cnēow/cnēowon/cnāwen.',
67:'Continuation §109, āw types and present umlaut under §94.',
68:'§113 long weakI, explicit lǣdan/lǣdde and -ed participles; stem-class rules.',
69:'WeakI dental and irregular stem rules.',
70:'§114 bringan/brōhte and ðync(e)an/ðūhte irregular stems.',
71:'§115 lęcg(e)an/lęgde(lēde), short weakI; §116 -ian weakI.',
72:'§117 complete weakI finite/nonfinite matrix and short/long-stem contrasts.',
73:'§119 complete weakII present, subjunctive, imperative, infinitive and present participle.',
74:'WeakII preterite and participle, -ige/-ie variation; morphology does not assign extra lexical senses.',
75:'§123 sęcg(e)an explicit present and uncontracted sægde versus sāde; libban variants.',
77:'§131 ðurfan preterite-present and §132 durran; selected irregular stems.',
79:'§138 past wesan including negative nǣre; §139 willan; §140 dōn complete anomalous system.',
80:'§141 gān complete system; first-plural gān subjunctive versus infinitive.',
90:'§153 genitive relations and §154 partitive genitive.',
91:'§156 genitive with verbs, including desire; lexical government checked independently where necessary.',
92:'§156h fear; §158 genitive prepositions; §159 genitive thing with personal dative/accusative.',
93:'§159a reflexive fear example; §160.1 voice instrumental; §161 benefit/reflexive dative.',
94:'§164 dative with speaking, promising, pitying and other verb frames.',
95:'§165 adjective dative and §166.1 agreeing adjective in prepositional phrase.',
96:'§169 accusative actor with infinitive; §170 extent; §172 accusative prepositions begins.',
97:'§172 accusative prepositions continuation; §173 object plus predicate accusative.',
99:'§176 adverbial instrumental time/repetition; §177 deprivation; agreement rules.',
100:'§183 concordant negatives and §184 reflexive datives.',
101:'§184b accusative reflexives; §187 passive; §188 past tense uses.',
102:'§188 habban/wesan perfects; §189 agreement; §190 impersonal construction.',
103:'§192 optative/subjunctive overview and §193 independent wishes.',
104:'§194 reported/content optatives and certainty exception; §195 attraction.',
105:'§196 temporal/conditional/purpose subordination; §197 indefinite relatives; §198 commands; §199 infinitive.',
106:'§199 accusative actor/infinitive and motion-purpose infinitive; §200 inflected infinitive; §201.1 postposed prepositions.',
175:'Assigned reading175.18–21, education/love opening; note10 points to getēon. Earlier lines evidence only, not reassigned.',
176:'Assigned complete reading page, exact commands, permissions, gifts and farewell; original notes retained.',
177:'Assigned reading177.1–2; separately cited177.10 impersonal beboden parallel, outside assigned reading and explicitly used only as exercise45.5 reference.',
295:'Glossary getēon(II103), bring up; play, supporting educational participle context.',
303:'Glossary līefan113 allow, permit, distinct from believe.'}
special_paths={12:'sources/audits/unit05-grammar/cook-p12-pdf28.png',41:'sources/audits/unit17-source/fb-p41.png',58:'sources/audits/unit16-grammar/fb-p58.png',71:'sources/audits/unit15-grammar/fb-p71.png',75:'sources/audits/unit16-grammar/fb-p75.png',96:'sources/audits/unit17-source/fb-p96.png',103:'sources/audits/unit15-grammar/fb-p103.png',175:'sources/audits/unit17-source/fb-p175.png',176:'sources/audits/unit17-source/fb-p176.png',177:'sources/audits/unit17-source/fb-p177.png',303:'sources/audits/unit17-source/fb-p303.png'}
special_paths[90]='sources/audits/unit15-grammar/fb-p90.png'
expaths={29:'course-map/ex-page29.png',30:'course-map/ex-page30.png',31:'unit18-source/ex-p31.png',32:'course-map/ex-page32.png',33:'unit18-source/ex-p33.png',43:'unit16-source/ex-p43.png',44:'unit16-grammar/ex-p44.png',48:'unit16-source/ex-p48.png',49:'unit17-source/ex-p49.png',59:'unit17-source/ex-p59.png',62:'unit17-source/ex-p62.png',64:'unit17-source/ex-p64.png'}
exclaims={29:'All eight Exercise44 prompts and original apparatus; jointXII,XIII heading preserved.',30:'All nine Exercise45 prompts and46.1 continuation; original lexical hints and source-control syntax.',31:'Exercise46 remainder and47 opening; exact “thee” in46.8 and “when you have” in46.9.',32:'Exercise47 continuation and48 opening; present commandest47.11, ænne47.10, dare/without/lest48.3.',33:'Exercise48 continuation; clēopian with ē, ęrian with ogonek, neither89a, omitted be48.7.',43:'Command bēodan/bebēodan/hātan lexical entries.',44:'Despoil berēafian118; desire giernan.',48:'Frighten āfǣran113; source free plural frige; lexical distinctions.',49:'Grieve ofðyncean114 and grief sārnes51b.',59:'Recognize oncnāwanR109; recompense forgieldanIII104.',62:'Silver seolfor47 and seolfren57; slay ofslēanVI107.',64:'Take leave of grētan113; tell sęcgean123; terrify āfǣran.'}
bt={'U18G-BT95':('sources/audits/unit18-grammar/bt_b0095.jpg',95,'main','beþurfan singular/plural present and dental past; exact Genesis43.4/8 relative clause and genitive/other government.'),'U18G-BT1056':('sources/audits/unit18-source/bt-p1056.jpg',1056,'main','þēowian senseII enslave, exact Genesis43.18 accusative-person ðæt hē ūs ðēowige.'),'U18G-BTS81':('sources/audits/unit18-grammar/bt_d0081.jpg',81,'supplement','berēafian, accusative deprived person plus genitive possessions, with other case alternatives separately documented.'),'U18G-BTS240':('sources/audits/unit18-grammar/bt_d0240.jpg',240,'supplement','foresęcgan past mention distinguished from future prediction; person mentioned earlier.'),'U18G-BTS646':('sources/audits/unit18-grammar/bt_d0646.jpg',646,'supplement','nā-hwæþer and contracted nāðer; paired ne-infinitive coordination under mihte.')}
records=[];missing=[]
for eid in sorted(refs):
 if eid in bt:
  path,page,edition,claim=bt[eid];source='bosworth_toller_1898_1921';pdf=None;loc=edition+' volume, printed dictionary page '+str(page)
 elif eid=='U18G-FB176-DETAIL':
  path='sources/audits/unit18-source/fb-p176-command-detail-600dpi.png';page=176;pdf=192;source='cook_fb_1895_2';claim='600dpi exact spelling lęcgeað and ðēowa (no r), personally re-inspected after source correction.';loc='176.4–12 detail'
 elif eid.startswith('U18G-EX'):
  page=int(eid.removeprefix('U18G-EX'));path='sources/audits/'+expaths[page];pdf=page+8;source='cook_ex_1895';claim=exclaims[page];loc='printed'+str(page)
 else:
  suffix=int(eid.removeprefix('U18G-FB'));page=12 if suffix==17 else 91 if suffix==156 else suffix;path=special_paths.get(page,f'sources/audits/unit14-grammar/fb-p{page}.png');pdf=page+16;source='cook_fb_1895_2';claim=fb[page];loc=('§17 on printed12'if suffix==17 else'§156 on printed91'if suffix==156 else'printed'+str(page))
 pp=R/path
 if not pp.exists():missing.append(path);continue
 records.append({'evidence_id':eid,'source_id':source,'printed_page':page,'pdf_page_one_based':pdf,'locator':loc,'image_path':path,'sha256':hashlib.sha256(pp.read_bytes()).hexdigest(),'inspection':'Personally viewed by Unit18 grammar analyst in this audit; inherited image files reused as primary evidence, not as inherited teaching milestones.','claim_scope':claim,'origin_category':'exact primary image evidence; matrices and explanatory prose are separately identified as editorial derivation/adaptation','limitation':'Evidence establishes only the cited letters, forms or rules. Display, lemma familiarity, and source reference do not automatically teach additional senses or constructions.'})
out={'schema_version':1,'evidence_catalog':records,'evidence':records,'counts':{'unique_evidence_records':len(records),'referenced_ids':len(refs)},'missing_images':missing,'source_reference_cautions':['FB17 and FB156 are section aliases, not printed page17/page156.','All PDF positions are one-based, with CookFB printed+16 and CookExercises printed+8. BT image files cite printed dictionary pages; no PDF locator is invented.','Source-only names and nominal/adjective scope use the source-editor evidence catalog; prior productive records preserve their original evidence IDs.','Uninspected downloaded bt_b0085.jpg and unused bt_b0749.jpg are not relied upon for claims.']}
(O/'evidence-catalog.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(out['counts'],missing)
