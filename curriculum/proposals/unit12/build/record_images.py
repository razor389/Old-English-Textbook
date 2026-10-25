from pathlib import Path
import json,hashlib
OUT=Path('curriculum/proposals/unit12')
rows=[
('sources/audits/course-map/ex-page09.png','cook_ex_1895',9,17,'VI.19.1–11','Directly read all first11 Exercise19 prompts; At length, kingdom forty years, built passive, build pret. control, beforan166, singular Come, plural written-you context and help196d retained.'),
('sources/audits/course-map/ex-page10.png','cook_ex_1895',10,18,'VI.19.12–17; VI.20.1–9; VI.21.1–8 opening','Directly read the remaining Exercise19 prompts, all9 Exercise20 prompts and Exercise21 opening. The long shepherd sentence and three-clause have-perfect prompt remain complete; gemētan, geswīcan, ābūtan172, gīet, ǣrest and geopenian controls verified visually.'),
('sources/audits/course-map/ex-page11.png','cook_ex_1895',11,19,'VI.21.8 continuation–12','Directly checked continuing whose-God sentence and final4 prompts: æt, ēaðmōd, gemētan, ręst51b, gemang172, ēhtan and motion on controls remain. Unit13 Exercise22 starts after this boundary and is not assigned.'),
('sources/audits/unit12-source/cook_fb_1895_2-p145-detail.png','cook_fb_1895_2',145,161,'Editorial prose lines1–7','Directly inspected all selected prose and all six attached original notes. Text begins Ðā ongunnon twā ðēoda. Confirmed hooked hęrgian/onsęndon, quantities hīe/ǣhta/hīendon/gehēton/hīernesse/singāle and the line-break continuation at meahten. The continuation of p144 note10 above note1 is not attached to the selected span.'),
('sources/audits/unit12-source/cook_fb_1895_2-p146-detail.png','cook_fb_1895_2',146,162,'Editorial prose lines1–11, ending before And hīe ðā eft','Directly inspected all selected prose and attached notes1–15. Confirmed exact Rōmanisca, hęre, ongēaton, ādrifon, onweg gewiten, the three ðā functions per note11 and all final attack verbs. Note3 explicitly compares active Old English and passive Latin; note8 sends reflexive him to §184a. The assigned span ends at foriermdon., before the second appeal.')]
rows.append(('sources/audits/unit12-source/cook_ex_1895-p10.png','cook_ex_1895',10,18,'VI.20.6 gīet detail recheck','Directly viewed this larger retained image after the initial structural image; the hint is gīet with macron over i, not giēt. Source transcript preserves it.'))
for pp,loc,obs in [
 (28,'§43','Directly inspected the complete ordinary masculine pattern and stem-ending rules; lexical diagnostic stems are required alongside shared endings.'),
 (29,'§43.4','Directly inspected ēðel with genitive ēðles and the selected syncopated oblique stem; the syncope cannot be guessed merely from a modern-looking headword.'),
 (30,'§44','Directly inspected hęre and the printed optional -g-/-ig- oblique spellings, including hęr(i)ges. A chosen teaching pattern must state its variants, not flatten them silently.'),
 (31,'§46 opening','Directly inspected the introduction to the root-noun vowel alternation; the following fōt table supplies the assigned cells.'),
 (32,'§46 fōt','Directly inspected fōt/fōtes/fēt (fōte)/fōt and fēt/fōta/fōtum/fēt, with occasional fōtas noted separately. The dative-singular and plural variants must retain their stated cell scope.'),
 (33,'§48 neuter disyllables','Directly inspected the ending-bearing syncope of neuter wǣp(e)n/wǣpnu and the surrounding selected neuter patterns.'),
 (34,'§48–49 continuation','Directly inspected the neuter continuation and lexical stem exceptions; no unattested blanket stem rule is inferred.'),
 (35,'§50–51','Directly inspected the full strong-feminine pattern and the qualified endingless accusative alternatives.'),
 (36,'§51 continuation','Directly inspected disyllabic feminine syncope and -nes/-ness- formation; complete lexical diagnostics are needed for derived models.')]:
 rows.append((f'sources/audits/unit12-source/cook_fb_1895_2-p{pp}.png','cook_fb_1895_2',pp,pp+16,loc,obs))
for pp,loc,obs in [
 (24,'§§33–35','Directly inspected dental devoicing, coalescence and consonant simplification rules used in the selected present and preterite surfaces.'),
 (25,'§§35–37','Directly inspected geminate simplification and grammatical consonant alternation, keeping lexical selection distinct from a blanket spelling rule.'),
 (53,'§§90–92','Directly inspected the grammatical classification of verbs and the distinction between a present stem and independently selected strong stems.'),
 (54,'§§92–94','Directly inspected the four strong stems and the explicit assignment of second-singular indicative preterite to the plural stem.'),
 (55,'§95','Directly inspected complete strong and contracted finite paradigms, command pairs and nonfinite bases, including the restricted reduced plural before a following subject pronoun.'),
 (57,'§100','Directly inspected the introduction to contracted verbs and the h-loss mechanism underlying their selected present forms.'),
 (58,'§101','Directly inspected the explicit classII placement of flēon and the contracted tēon model, without conflating flee with fly.'),
 (59,'§§101–102','Directly inspected the contracted singular command rule: long vowel in classII, short vowel in classVI sleah; also strongI stems, including rīsan and wrītan.'),
 (60,'§§102–103','Directly inspected strongI present diagnostics and strongII four-stem alternation, with flēon explicitly assigned to the tēon pattern.'),
 (61,'§§103–104','Directly inspected contracted classII present flīehst/flīehð derivation through the tēon pattern, and strongIII weorpan stem membership.'),
 (68,'§§112–113','Directly inspected the weakI dental patterns mētte, ēhte, gier(w)ed and sętt; no unsourced ge- prefix or replacement stem is added.'),
 (69,'§§113–114','Directly inspected the named t/d and gierwan families plus the irregular weak preterite/participle rules.'),
 (70,'§114','Directly inspected wyrcean/worhte/(ge)worht and bringan’s mixed dental preterite family.'),
 (71,'§§115–117','Directly inspected the weakI subclass boundaries and introduction to the complete weakI patterns.'),
 (72,'§117','Directly inspected complete weakI present/preterite, singular/plural commands and participle bases.'),
 (73,'§§118–119','Directly inspected the complete weakII present and command patterns, including -ie/-ast/-að/-iað and singular -a/plural -iað.'),
 (74,'§§119–121','Directly inspected weakII -ode/-odest/-odon and the habban indicative/subjunctive bases reused by the construction display.')]:
 rows.append((f'sources/audits/unit11-grammar/cook_fb_1895_2-p{pp}.png','cook_fb_1895_2',pp,pp+16,loc,obs))
rows.extend([
 ('sources/audits/unit12-grammar/cook_fb_1895_2-p67.png','cook_fb_1895_2',67,83,'§110','Directly inspected hātan/hēt/hēton/hāten and the independently defined reduplicating ē-preterite family used by gehātan.'),
 ('sources/audits/unit12-grammar/cook_fb_1895_2-p77.png','cook_fb_1895_2',77,93,'§127','Directly inspected āh/āhst/āgon and āhte, with negative nāgan noted separately. Only the newly selected indicative and local negative help are assigned.'),
 ('sources/audits/unit12-grammar/wright_oe_1914-p248.png','wright_oe_1914',248,268,'§476','Directly inspected thorn/dental loss before -st and coalescence of thorn+thorn, corroborating selected cȳst/cȳð; the registry confirms printed/PDF offset20.')])
rows.extend([
 ('sources/audits/unit11-grammar/cook_fb_1895_2-p101.png','cook_fb_1895_2',101,117,'§§186–188','Directly inspected the two simple tense forms, passive auxiliaries and contextual past/future relations. The old description of modern-like future auxiliaries is qualified in the design rather than adopted without restriction.'),
 ('sources/audits/unit12-grammar/cook_fb_1895_2-p102.png','cook_fb_1895_2',102,118,'§188 continuation','Directly inspected the bounded habban/transitive and wesan/intransitive participial constructions and the source examples.'),
 ('sources/audits/unit12-grammar/fulk-2020-p32.png','fulk_2020',32,44,'§§49–50','Directly inspected the developing perfect-like constructions, the ordinary preterite expressing earlier past relations, and the contextual range of be plus present participle; no exact modern progressive category is imposed.'),
 ('sources/audits/unit12-grammar/fulk-2020-p33.png','fulk_2020',33,45,'§§51–52','Directly inspected contextual interpretation of the simple tenses and the future/habitual uses of bēon; future reference is not treated as an exclusive mechanical form-to-meaning code.')])
for pp,loc,obs in [
 (37,'§53','Directly inspected the complete masculine/feminine weak noun patterns, including -ena genitive plural and -um dative plural, and the explicit heorte class membership.'),
 (39,'§57.3; §58','Directly inspected disyllabic adjective endings, optional ēadig syncope before vowel endings, the occasional endingless feminine/neuter positions, and long-adjective loss of -u.'),
 (40,'§§58–60','Directly inspected the long strong paradigm, qualified h-loss/consonant rules, adjective -e behavior and introduction to weak adjective inflection.'),
 (41,'§§60–62','Directly inspected the complete weak adjective table, regular -ra genitive plural, and the distinct finite/predicate roles of participles. Uninflected predicate bases are not finite forms.'),
 (285,'Vocabulary ēðel','Directly verified ēðel, native land/country, with §43.4 morphology reference; also observed the separate ęngel spelling rather than confusing it with fishhook angel.'),
 (286,'Vocabulary fǣmne and fēond','Directly verified fǣmne with long æ and weak-noun §53 reference, and fēond with §46.3 reference.'),
 (289,'Vocabulary fōt','Directly verified long ō in fōt and the root-declension §46 reference.'),
 (296,'Vocabulary gewrit and gīet','Directly verified gewrit as writing/letter/document and gīet as yet/still; alternate gīt/gȳt spellings are lexical variants, not silently substituted source text.'),
 (301,'Vocabulary īsern','Directly verified the distinct noun īsern (§47) and adjective īsern (§57); the adjective has the assigned disyllabic pattern.'),
 (309,'Vocabulary pęning and ręst','Directly verified pęning with hooked e and masculine §43. Ręst is glossed couch/bed here; its repose meaning requires the separate exercise-context evidence, which was requested explicitly from the source editor.'),
 (310,'Vocabulary Rōmane, sǣdtīma and sāwol','Directly verified Rōmane with long ō, weak sǣd-tīma seedtime, and sāw(o)l with explicit §51.4 syncope reference.'),
 (320,'Vocabulary wǣpen','Directly verified wǣpen and the §47.1 plural/arms reference; the selected inflection remains independently supported by the grammatical table.')]:
 rows.append((f'sources/audits/unit12-source/cook_fb_1895_2-p{pp}.png','cook_fb_1895_2',pp,pp+16,loc,obs))
data={'schema_version':1,'chapter':'ch12','reviewer':'unit12_design','method':'Each recorded image was directly viewed in full via view_image; transcription was compared after that inspection. OCR and rendering alone do not certify this record.','images':[{'path':p,'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest(),'source_id':s,'printed_page':pp,'pdf_page_one_based':pdf,'original_identifier':loc,'visually_inspected':True,'observations':obs} for p,s,pp,pdf,loc,obs in rows],'limits':'Independent prompt/source boundary and key-text crosscheck; detailed word-level lexical evidence remains the source editor’s audit. Private translation was independently prepared before consulting other authors’ private witnesses.'}
(OUT/'source-crosscheck.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Recorded',len(rows),'actual viewed page images')
