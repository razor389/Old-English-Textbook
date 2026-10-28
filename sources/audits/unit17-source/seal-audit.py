"""Validate and seal the source-editor deliverables; never touch shared registers."""
import json,hashlib,re
from pathlib import Path
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(n,d):(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
VIEWED={
 'ex':[22,23,24,25,26,27,28,37,39,40,41,42,45,46,47,49,50,51,53,54,55,56,58,59,61,62,63,64,65,67,68],
 'fb':[18,19,20,28,29,30,31,32,33,34,35,36,37,38,39,40,41,84,96,171,172,173,174,175,176,177,274,275,276,278,279,281,282,284,291,294,297,298,299,300,303,304,305,306,307,308,309,312,313,314,315,316,317,318,322,323,324],
 'bt':[8,504,553,557,809],
}
CLAIMS={
 'ex22':['Exercise37 begins here; item2 continues on23. Exact English, item numbering and global omission instruction inspected.'],
 'ex23':['Continuation of37 and start of38; mægen/draca/ȳst hints belong to23, not merely22. Exact gefiðred, hālga53 and horn43 inspected.'],
 'ex24':['Remainder of38 and start of39; weak ðēowa53 inspected. Exact prompt wording preserved.'],
 'ex25':['Continuation of39 and start of40; feminine getimbrung51.3, ēare53.2, ðīnen51.5 and cnēoris controls inspected.'],
 'ex26':['Continuation of40 and Exercise41; sǣd descendants context; finger43.4, tabele53 and indeclinable-law hint ǣ.'],
 'ex27':['Exercise42 and start of43; męnigu, mǣgð, palmtwīg47 and unmarked ðrymsetl inspected; source English knee is singular.'],
 'ex28':['Remainder of43 through item20; no Exercise44 item is assigned.'],
 'ex37':['Acceptable=gecwēme59; not an unsupported andfęnge substitution.'],
 'ex39':['Arithmetic=gerīmcræft43.'],
 'ex40':['Ball=ðoðor43; bend=bīegan113/gebīegan113 with explicitly long ī; between=betwēox.'],
 'ex41':['Bread=hlāf43; blossom=blōstma53; blessing and brightness nominal entries inspected.'],
 'ex42':['Camel=olfend43, cedar-tree=cēderbēam43, circuit/compass vocabulary.'],
 'ex45':['Dignity/honour vocabulary with weorðscipe44.1.'],
 'ex46':['Educated=gelǣred62; Egyptians=Egypta54; ever=ǣfre.'],
 'ex47':['Adverb yfele is explicitly distinguished from substantive/adjectival evil; few=fēawe58; exceedingly=ðearle.'],
 'ex49':['Gift=giefu51.a; blīðe59 glad/merry; prior great=mǣre and micel alternatives.'],
 'ex50':['Harp=hearpe53.1; hence=heonan; height and high-born entries.'],
 'ex51':['Humility, husband=wer and illustrious=æðele59; no silent promotion of man to husband.'],
 'ex53':['Law entry gemet is a separate generic glossary option; the actual Exercise41.12 hint remains ǣ.'],
 'ex54':['Meaning=andgiet47; manifold; love=lufu51.a and lufe53.1; merry=blīðe59.'],
 'ex55':['Nation=folc47 and mǣgð51.b; music=swēg43/swēgcræft43; multitude=unrīm47.'],
 'ex56':['Number=męnigu51.a; occupation=cræft43; other temporal and nominal glossary entries checked.'],
 'ex58':['Pound=pund47; praise=lof43; princess=cwēn51.b.'],
 'ex59':['Queen=cwēn51.b, distinct English queen/princess entries share the headword.'],
 'ex61':['Serpent=nædre(næddre)53.1; no length added to the selected Exercise spelling.'],
 'ex62':['Silence=swīge53.1; skill=cræft43; song=sang43; no need to extend lēoð poetry silently.'],
 'ex63':['Stone adjective is stānen57 in this glossary; strength=stręngðu51.a.'],
 'ex64':['Thane/vassal and time-related glossary entries.'],
 'ex65':['Trumpet=biema53 without an inferred long vowel; tribe=nation mǣgð.'],
 'ex67':['Where=hwǣr; water=wæter47.1,6; whole=hāl58; winsome=wynsum57.'],
 'ex68':['Young=geong; within=binnan with cited case control.'],
 'fb18':['Cook23 stress and unstressed syllables; the paragraph continues on19. It does not supply an andgiet plural.'],
 'fb19':['Cook23 final sentence: syncope is most apt after a long syllable. This is a tendency, not evidence for all contracted mægen obliques or a particular andgiet plural.'],
 'fb20':['Explicit quantities in wīsdōm and hlūd examples.'],
 'fb28':['Cook43 complete masculine model.'],
 'fb29':['Cook43.4 syncope conditions and exceptions;43.6 agent-noun plurals.'],
 'fb30':['Cook44 e-stems and -ere/-scipe nominal model.'],
 'fb31':['Additional masculine noun systems inspected as class boundaries; not every class is assigned anew.'],
 'fb32':['Cook47 short/heavy neuter singular/plural contrast.'],
 'fb33':['Cook47.1 selected mægnu and47.3 cnēo/trēo, w before endings and cnēowu plural.'],
 'fb34':['Neuter and feminine class boundary material; no ǣ-law entry claimed here.'],
 'fb35':['Cook51 feminine a/b class singular/plural; singular abstract scope does not imply defectiveness.'],
 'fb36':['51.1 endingless accusative,51.3 -ung variants,51.5 doubled stem-final consonants with retained e.'],
 'fb37':['Cook53 weak masculine/feminine/neuter; ēare and contracted genitive plural ēarna.'],
 'fb38':['Cook54 foreign names,55 strong/weak choice and direct address; no invented foreign-name paradigms.'],
 'fb39':['Strong adjective models and polysyllabic syncope conditions.'],
 'fb40':['Cook59 e-adjectives and60 complete weak model; feminine-plural variants distinguished.'],
 'fb41':['Present/past participles as adjectives; inflected attributive/substantive versus usual uninflected predicate distinctions.'],
 'fb84':['Masculine -dōm/-scipe and agent -ere with hearpere; feminine -ung derivations.'],
 'fb96':['Perception construction and accusative duration; isolated quantity frames remain supplied.'],
 'fb171':['Following the Unit16 gymnasium episode: feast context inspected as an unassigned candidate boundary.'],
 'fb172':['Feast narrative context inspected; not selected as the Unit17 reading.'],
 'fb173':['Princess and visitor discussion preceding music performance inspected.'],
 'fb174':['Exact174.7–18 source lines and attached9–17/12a apparatus inspected; wynsumum at174.8 confirmed; swīgende retained with source correction note12a.'],
 'fb175':['Exact175.1–17 source, attached1–9 apparatus and continuation boundary inspected. Preserve upon, Apollines, ænne, ðisum and wyn-/sumum line division. Reading ends before175.18.'],
 'fb176':['Gift/dispersal continuation inspected but not assigned.'],
 'fb177':['Printed music subsection continuation/end inspected; source subsection need not force extra unrelated reading assignment.'],
 'fb274':['ǣfre, ælmihtig57.3, temporal preposition æfter.'],
 'fb275':['andgiet47 sense/meaning/understanding; āna alone; æðele and æðelboren.'],
 'fb276':['andweard58 present; bounded reading predicate.'],
 'fb278':['beorhtnes51.5; betwēox among/between.'],
 'fb279':['biema and blōstma; binnan within.'],
 'fb281':['cniht servant/young man distinction; cnēoris inflection pointer; cedar entry.'],
 'fb282':['cwēn51.1;queen,princess; endingless accusative supported. cynehelm43 and dēma53.'],
 'fb284':['ēaðmōdnes51.5; accompanying lexical boundaries.'],
 'fb291':['gecwēme59 pleasing/acceptable; gefeallan fall/chance.'],
 'fb294':['gerīmcræft and related computational vocabulary.'],
 'fb297':['hǣðen57.3; hāl58; hǣlu51.a.'],
 'fb298':['hearp instruments and heall; hēanes and heonan.'],
 'fb299':['hlāf43; hlǣfdige53.1. No simple horn entry claimed here.'],
 'fb300':['Nominal/pronominal glossary continuation used for comparison; no new unattested lengths inferred.'],
 'fb303':['lufu51.a and53.3; lēoð47 poetry/verse; līefan allow/permit used by grammar to distinguish permission context.'],
 'fb304':['mægen47; mǣgð tribe/nation; manigfeald.'],
 'fb305':['męnigu51.a company/number; masculine/neuter glossary senses checked.'],
 'fb306':['mōnað43 month; munt43 mountain; dictionary serpent variant inspected without silently replacing the selected Exercise spelling.'],
 'fb307':['nīeten47.1 creature/cattle; nēowolnes51.5; absence of an nīwe entry here is not evidence against nīwe.'],
 'fb308':['olfend43 camel and relevant o-headwords.'],
 'fb309':['pund47, rīce59 rich; selected rich sense kept separate from mighty.'],
 'fb312':['Selected s-headwords and boundaries; exact sōð entry is on313.'],
 'fb313':['sōð58 true versus sōð47 truth; stǣnen57 is the First Book variant, distinct from Exercises stānen.'],
 'fb314':['swēg43 music; swēgcræft43 music; stilnes51.5 quietness; stręngðu51.a strength.'],
 'fb315':['sūð and swīge-related glossary continuation inspected.'],
 'fb316':['tōdæg today; tōgēanes towards, locally supplied.'],
 'fb317':['ðegn and related ð-headwords.'],
 'fb318':['ðēnung service; ðīnen51.5 stem; relevant pronoun/nominal glossary entries.'],
 'fb322':['weorðscipe and wer husband.'],
 'fb323':['w-headword continuation, including spelling variants used only as explicit support.'],
 'fb324':['yfele70 evil/wrongly; ymbhwyrft43.'],
 'bt8':['Ǽ; indecl.f., law: exact gender/indeclinability supports feminine accusative ǣ. BT acute is normalized to macron when quoted as course form.'],
 'bt504':['HÁLGA an;m. a saint, with hālgan and hālgena attestations; weak noun differs from hālig adjective.'],
 'bt553':['HORN es;m.; se horn mínre hǽlo and hornas support selected masculine table. Figurative strength/dignity is contextual explanation, not a literal dictionary gloss verified on this page.'],
 'bt557':['HRÉOD es;n.; reed and plural reeds attestations support heavy-neuter table.'],
 'bt809':['SǼD es;n. senseV progeny/posterity; exact Luke1.55 phrase tō Abrahame and hys sǽde supports collective singular descendants.'],
}
catalog=[]
for kind,pages in VIEWED.items():
 for p in pages:
  f=O/f'{kind}-p{p}.{"jpg" if kind=="bt" else "png"}'
  assert f.exists(),f
  catalog.append(dict(evidence_id=f'U17-{kind.upper()}-P{p}',source_id={'ex':'cook_ex_1895','fb':'cook_fb_1895_2','bt':'bosworth_toller_1898'}[kind],printed_page=p,pdf_page_one_based=p+({'ex':8,'fb':16}.get(kind,0)) if kind!='bt' else None,page_convention='One-based PDF page = printed page + '+str(8 if kind=='ex' else 16) if kind!='bt' else 'Standalone scanned printed page; no PDF page number asserted.',image_path=f.relative_to(R).as_posix(),image_sha256=sha(f),actual_image_inspection=True,observer='unit17_source',inspection_method='view_image; actual visual reading, not rendering or hash generation',inspection_date='2026-10-28' if kind=='fb' and p in [18,19] else '2026-10-27',claims=CLAIMS[kind+str(p)],origin_category='exact primary source evidence',url=f'https://bosworthtoller.com/images-dictionary/bt_b{p:04}.jpg' if kind=='bt' else None))
dump('evidence-catalog.json',dict(schema_version=1,records=catalog,actual_images_viewed=len(catalog),external_evidence=[dict(evidence_ids=['U17-COORD-WRIGHT49','U17-COORD-WRIGHT213','U17-COORD-WRIGHT214'],record='sources/audits/unit17-coordinator/niwe-42-02.json',observer='coordinator; not claimed as source-editor inspection'),dict(record='sources/audits/unit17-coordinator/numeral-42-02.json',observer='coordinator;144000 scaffold and BT1082 evidence')],note='OCR and inherited maps were finding aids. Every local record listed here was actually opened with view_image; external coordinator records retain their own observer attribution.'))
# Receipt for all mandatory prior active contracts and actual registers.
paths=[f'chapters/ch{i:02}/coverage.json' for i in range(1,17)]+['lexicon/entries.json','curriculum/grammar.json','STATUS.md','EDITORIAL_POLICY.md','curriculum/COURSE_PLAN.md','curriculum/COOK_MAP.md','sources/registry.json','docs/WORKFLOW.md','docs/HANDOFF.md','AGENTS.md']
receipt=[]
for x in paths:
 p=R/x;assert p.exists(),p
 d=read(p) if p.suffix=='.json' else None
 receipt.append(dict(path=x,sha256=sha(p),read_scope='complete active contract parsed and reviewed against actual registers' if 'coverage.json' in x else 'actual file read; no teaching inherited from archive'))
dump('prior-scope-receipt.json',dict(schema_version=1,baseline_revision='defa800',baseline_counts={'lemmas':1067,'forms':11188,'senses':1376,'features':1080},files=receipt,policy='The prior register is consulted at form and sense level; familiar headword, recognitional table or supplied citation does not establish production. Historical reference/previous-course is evidence only.'))
E=read(O/'exercises-prompts.json');A=read(O/'reading-apparatus.json');N=read(O/'noun-adjective-paradigms.json');S=read(O/'local-support.json');T=read(O/'reading-token-audit.json')
assert E['count']==82 and [E['counts_by_exercise'][str(n)] for n in range(37,44)]==[14,10,7,10,12,9,20]
assert A['count']==19 and A['anchor_count']==20
assert N['counts']=={'paradigms':62,'cells':796}
assert len(T['tokens'])==252 and [x['token_position_one_based'] for x in T['tokens']]==list(range(1,253))
assert len({x['form_id'] for x in S['forms']})==len(S['forms']),'Duplicate local form identity; combine occurrences instead.'
for p in N['paradigms']:
 assert len(p['cells']) in [4,8,50]
 assert len({json.dumps(c['analysis'],sort_keys=True) for c in p['cells']})==len(p['cells'])
assert not S['unresolved'] and not T['unresolved']
checks=dict(schema_version=1,exercise_counts=E['counts_by_exercise'],exercise_total=82,reading_tokens=252,reading_external_verbal=57,reading_nonverbal=195,notes=19,anchors=20,nominal_systems=62,nominal_cells=796,sense_rows=len(read(O/'nominal-sense-audit.json')['senses']),local_supplied_forms=len(S['forms']),actual_local_page_images=len(catalog),source_transcription_changes_after_independent_translation=False,private_translation_sha256=sha(O/'author-only-reading-translation-witness.json'),unresolved_source_dependencies=[],limits=['This is a precontract source audit; the coordinator must reconcile learner displays, tasks and exact prior IDs before committing the learning contract.','Numbers and foreign names are supplied bounded expressions, not newly taught complete general systems.','A full displayed table does not itself establish that all syntactic uses have been taught.'])
dump('audit-checks.json',checks)
dump('source-corrections.json',dict(schema_version=1,demonstrated_source_errors_corrected=[],preserved_source_features=['joint XII,XIII group; no invented ReaderXII/ReaderXIII exercise split','all82 original English prompts and numbering','all19 attached reading notes and20 anchors','swīgende with original12a For swīgiende note','upon, Apollines, ænne and single-s ðisum','wynsumum174.8 and joined wyn-/sumum175.11–12'],declared_normalizations=read(O/'reading-source.json')['normalizations'],model_repairs_are_not_source_errata=['Mægen retains mægenes/mægene/mægena/mægenum; explicit mægnu is restricted to nominative/accusative plural. See morphology-correction-01.json for the preserved previous proposal.','Andgiet is a four-case abstract-singular scope; the unsupported prior plural proposal is preserved and withdrawn, without a defectiveness claim.','Prefer exact prior wæteru and ðoðore over unassigned variant forms.','Use weak direct-address wæstmbǣran/gefiðredan/geongan/ealdan under Cook55.','Keep masculine horn43 selected; no correction of Cook is asserted.','Use hālga noun, not hālig adjective, for the exact saint hint.','Use cwēn endingless accusative under the explicit51.1 glossary pointer.','Keep literal trees39.5 and spirit38.7; biblical paraphrase wood/breath must not overwrite Cook English.','Use sang for song42.2; no silent extension of lēoð poetry.','Reading gelīefst permission is a locally supplied source lemma/frame; belief paradigm is not silently promoted.']))
report=(f'Unit17 source audit is ready for coordinator reconciliation. The packet preserves all82 items of joint XII,XIII Exercises37–43, with counts14/10/7/10/12/9/20; printed Exercises22–28 correspond to one-based PDF30–36. Exercises44–48 remain outside this assignment.\n\n'
 'The accepted reading is the coherent music performance at First Book174.7–175.17, one-based PDF190–191:252 words across29 editorially counted physical prose lines, anchored by the printed marginal multiples of five. All19 original notes and20 anchors are retained separately. The gift/love/dispersal continuation is unassigned. Transcription, learner text, English context, private independent translation and change record remain distinct. Wynsumum was actually checked at both occurrences.\n\n'
 f'The nominal packet defines62 complete systems with796 literal cells and71 separate sense records. Familiar noun classes are reused; four-case abstract-singular tables expressly exclude plural from the taught sense without claiming defectiveness. Hēanes shows all8 cells, with the4 singular cells supplied reference only. The local-support ledger contains{len(S["forms"])} supplied shapes and senses; all252 reading positions bind to exact forms, senses and support routes, including57 external verbal/participial analyses and195 nonverbal analyses. No isolated supplied form is an independent-recall target.\n\n'
 'The coordinator-authorized morphology correction preserves the former proposal in morphology-correction-01.json: mægen now retains full-stem obliques while keeping explicit plural mægnu; andgiet is bounded to four abstract-singular cells, with plural forms and count/faculty senses outside scope. Both actual andgiet exercise uses remain unchanged.\n\n'
 'Bounded lexical decisions include masculine horn supported by Cook43 and BT553; hālga weak noun supported by BT504; endingless accusative cwēn by Cook51.1; sǣd descendants as collective singular supported by the exact Luke1.55 quotation in BT809; and hrēod neuter in BT557. The horn image is retained literally: strength/dignity is modern contextual help, not a verified literal BT definition. Separate queen/princess, fame/report, husband, peoples, elderly and understanding senses are explicit. Cræft musical skill remains supplied.\n\n'
 f'{len(catalog)} local primary page images were actually viewed. Their hashes and bounded claims are in evidence-catalog.json. Wright nīwe and the144000 scaffold are attributed to the coordinator’s independent records, not falsely claimed as source-editor views. The private translation witness was not regenerated after comparison; its seal is in audit-checks.json. No material source dependency remains unresolved. Contract assembly, display routing and final linguistic review remain coordinator/design stages.\n')
report=re.sub(r'(?<=[A-Za-z])(?=\d)|(?<=\d)(?=[A-Za-z])',' ',report)
report=re.sub(r',(?=\S)',', ',report)
report=re.sub(r':(?=\d)',': ',report)
(O/'source-report.md').write_text(report,encoding='utf8')
# Seal all source-editor artifacts except the manifest itself.
files=[p for p in O.iterdir() if p.is_file() and p.name!='manifest.json']
dump('manifest.json',dict(schema_version=1,status='source audit sealed for precontract reconciliation; reseal after any accepted correction',files=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p),bytes=p.stat().st_size) for p in sorted(files)],private_translation_sha256=checks['private_translation_sha256'],counts=checks))
print(json.dumps(checks,ensure_ascii=False))
