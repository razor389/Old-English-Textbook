"""Evidence metadata and consistency checks for the independent U13 proposal."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parent
def read(p):return json.loads((ROOT/p).read_text(encoding='utf8'))
def write(p,x):(OUT/p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
E=[]
def ev(i,path,source,page,pdf,locator,observation,url=None):
    E.append({'evidence_id':i,'source_id':source,'origin_category':'exact_source','printed_page':page,'pdf_page_one_based':pdf,'locator':locator,'image_path':path,'image_sha256':sha(path),'image_inspected':True,'inspected_by':'unit13_grammar','inspection_method':'Personally viewed the facsimile image; OCR used only to locate it.','observation':observation,**({'source_url':url} if url else {})})
fb={
24:('unit13-grammar/cook_fb_1895_2-p24.png','§§33–35','Dental consonant changes including c+d→ct, d/t+ð→tt/t, and s+ð→st; derivation must retain lexical exceptions.'),
25:('unit11-grammar/cook_fb_1895_2-p25.png','§§35–37','Double consonant simplification and grammatical alternation; final gemination is simplified in selected imperative win.'),
54:('unit02-grammar/cook-fb-p54.png','§§93–94','Four strong stems and their morphological domains.'),
55:('unit02-grammar/cook-fb-p55.png','§95','Complete strong indicative, subjunctive, imperative and nonfinite model; preterite2 singular differs from1/3.'),
60:('unit11-grammar/cook_fb_1895_2-p60.png','§§102–103','Strong II principal stems; bēodan class and present singular mutation.'),
61:('unit11-grammar/cook_fb_1895_2-p61.png','§§103–104','Strong II bīetst/bīet(t); strong III eor pattern and lexical stems.'),
62:('unit11-grammar/cook_fb_1895_2-p62.png','§104','Strong III hweorfan and winnan; present singular mutation and special consonant outcomes.'),
66:('unit12-grammar/cook_fb_1895_2-p66.png','§§108–109','Reduplicating/strong VII healdan, hēold and mutated present; pattern does not license arbitrary lexical prefixes.'),
67:('unit02-grammar/cook-fb-p67.png','§§110–112','Strong VII ondrǣdan class with ē preterite and weak I introduction.'),
68:('unit02-grammar/cook-fb-p68.png','§§112–113','Weak I stem families; geminate and dental formation, participle syncope.'),
69:('unit02-grammar/cook-fb-p69.png','§§113–114','Weak I consonantal outcomes and unmutated preterite group; selected dental participles.'),
70:('unit02-grammar/cook-fb-p70.png','§114','stręcc(e)an and wyrcean belong to lexical irregular weak group; source āstreahte supplies the exact long-prefix spelling.'),
71:('unit02-grammar/cook-fb-p71.png','§116','Herian praise belongs to weakI short i-stems; coupled with neriende model72 this supports selected hęriendra without introducing an unassigned g-variant.'),
72:('unit02-grammar/cook-fb-p72.png','§117','Full weak I model with finite endings and complete command and participle-base pairs.'),
73:('unit02-grammar/cook-fb-p73.png','§§118–119','Full weak II present paradigm; infinitive -ian, -ianne; present participle -iende.'),
74:('unit02-grammar/cook-fb-p74.png','§119 continued','Weak II preterite and past participle, selected -ode/-od; alternatives not automatically assigned.'),
78:('unit11-grammar/cook_fb_1895_2-p78.png','§§133–138','§134 is munan, whereas§133 is sculan. Exercises23.7 forceorfan,134 is an apparent miscitation, preserved in transcript.'),
79:('unit12-grammar/cook_fb_1895_2-p79.png','§§138–140','Wesan commands and dōn anomalous system. Prefix fordōn licensed by its separate lexical entry.'),
80:('unit09-grammar/cook_fb_1895_2-p80.png','§141','Gān indicative/subjunctive/imperative morphology, including suppletive ēode; prefix ingān separately attested.'),
93:('unit12-grammar/cook_fb_1895_2-p93.png','§159b;§161','āxian may take accusative person and genitive thing; dative affected/beneficiary persons.'),
94:('unit13-grammar/cook_fb_1895_2-p94.png','§§162–164','Dative government and indirect-object categories; each new verb frame still needs lexical support.'),
95:('unit11-grammar/cook_fb_1895_2-p95.png','§§165–167','Dative with adjectives and prepositions; not proof of every possible lexical frame.'),
96:('unit12-grammar/cook_fb_1895_2-p96.png','§§168–172','Accusative direct object/cognate object and perception accusative-infinitive, including blissesang ūpāstīgan.'),
97:('unit11-grammar/cook_fb_1895_2-p97.png','§172 continued;§§173–174','oð takes accusative; on static/directional contrast is qualified, not categorical; instrumental general use.'),
99:('unit11-grammar/cook_fb_1895_2-p99.png','§§175–179','Mid often takes dative; instrumental route explicitly ðȳ ilcan wege. No need to rewrite earlier dative-surface nominal identities.'),
100:('unit11-grammar/cook_fb_1895_2-p100.png','§§179–184','Predicative participles may be uninflected; negative concord; lexical reflexive case distinctions.'),
101:('unit11-grammar/cook_fb_1895_2-p101.png','§§184b–188','Accusative reflexive; passive with past participle and wesan/weorðan; simple preterite can translate pluperfect.'),
102:('unit13-grammar/cook_fb_1895_2-p102.png','§§189–191','Agreement, collective phrases and omission. Does not establish one fixed constituent-order rule.'),
103:('unit13-grammar/cook_fb_1895_2-p103.png','§§192–194','Subjunctive uses and content reporting; reporting time is relative and context-sensitive.'),
104:('unit13-grammar/cook_fb_1895_2-p104.png','§§194–196','Commands/content clauses with subjunctive; bebēodan example with dative addressee.'),
105:('unit13-grammar/cook_fb_1895_2-p105.png','§§196–199','Purpose, wishes and imperatives; expressed pronouns possible; questions are not formed by a single universal inversion operation.'),
106:('unit13-grammar/cook_fb_1895_2-p106.png','§§199–201','Plain infinitive, inflected infinitive after adjective (feorr tō gesēceanne), and postposed prepositions in relative clauses.'),
107:('unit13-grammar/cook_fb_1895_2-p107.png','§202','Paired ge…ge is visibly unmarked for length; temporal/causal/concessive homographs require contextual parsing.'),
134:('unit10-source/cook_fb_1895_2-p134.png','lines1–2, editorial count from opening','Mannes Bearn cymð followed by coordinated plural angels with omitted coming predicate corroborates recovery with renewed agreement.'),
141:('unit11-grammar/cook_fb_1895_2-p141.png','lines2–3;note4','Wolde ic sprecan mid ðone… confirms conversational speak-with; note4 expressly labels the accusative after mid exceptional. Productive example selects independently supported normal dative.'),
152:('unit13-source/chad-detail-001.png','lines3–21; notes1–17','Checked all selected text and notes. Source note8 makes fronted voice/song objects of embedded gehīerde; note9a Se sang fixes hē before becōm; note14 marks approximative swā-swā; note17 directs instrumental route.'),
153:('unit13-source/chad-detail-002.png','lines1–9 partial; corroboration16; notes1–13','Checked selected summons and quotation; speaker/addressees and apposition control reference. Separate Æfter ðon hē underðēodde at editorial line16 (after printed15 marker) corroborates pronoun-before-finite after fronting.'),
154:('unit13-grammar/cook_fb_1895_2-p154.png','lines10–11 prostration and ensuing dialogue','Exact āstreahte with accusative reflexive and fore+acc; āxian person+gen thing; hālsige request with ðæt. Source fore is not silently changed to exercise beforan.'),
155:('unit13-grammar/cook_fb_1895_2-p155.png','lines5–6,13,18–19','Lǣdan takes accusative person with accompanying mid phrase; onlīesed is exact passive; Is ðæt hwilc wundor note14 says translate any.'),
274:('unit12-source/cook_fb_1895_2-p274.png','columns a–b','Lexical ǣgðer ge…ge, ǣr adverb before (often pluperfect indication), ǣrest first.'),
276:('unit12-source/cook_fb_1895_2-p276.png','column b','āscian/āxian;āsęndan;āsęttan;āstīgan explicitly ascend/board/descend.'),
277:('unit12-source/cook_fb_1895_2-p277.png','columns a–b','āstręccean prostrate; bebēodan command with strong II reference.'),
278:('unit12-source/cook_fb_1895_2-p278.png','columns a–b','begān pursue/practise/ply; behealdan behold with checked class.'),
280:('unit12-source/cook_fb_1895_2-p280.png','column b','būtan preposition without/outside/except/besides; new without sense is explicit rather than silently inherited from besides.'),
284:('unit12-source/cook_fb_1895_2-p284.png','column b','ęft again/back; ęfthweorfan return, strong III.'),
287:('unit12-source/cook_fb_1895_2-p287.png','columns a–b','fordilgian weakII destroy; fordōn destroy with anomalous-class cross-reference.'),
294:('unit13-source/cook-fb-p294.png','lexical entry gescrȳdan','gescrȳdan weakI clothe; prefix identity is lexical, not generated freely.'),
296:('unit12-source/cook_fb_1895_2-p296.png','lexical entry gewunian','gewunian weakII be wont/use/dwell; frame extension bounded to infinitive of usual action.'),
297:('unit12-source/cook_fb_1895_2-p297.png','lexical entry hālsian','Longā hālsian, weakII conjure/implore/entreat.'),
301:('unit12-source/cook_fb_1895_2-p301.png','columns a–b','ingān§141 distinct from ingangan§109; lǣdan lead/bring/take.'),
306:('unit12-source/cook_fb_1895_2-p306.png','lexical entries nēah,nēalǣcan','nēah adverb at hand; nēalǣcan weakI113 approach; actual source152 confirms nēalǣcton.'),
307:('unit12-source/cook_fb_1895_2-p307.png','lexical entries of,oferwinnan','of from/out; oferwinnan strongIII overcome/conquer/subdue.'),
308:('unit12-source/cook_fb_1895_2-p308.png','lexical entries onlīesan,ondrǣdan','onlīesan release; ondrǣdan§110 fear; accusative person independently corroborated by BT749.'),
311:('unit12-source/cook_fb_1895_2-p311.png','column b, sęllan','sęllan explicitly includes sell as well as give; this supports the new sale sense.'),
317:('unit12-source/cook_fb_1895_2-p317.png','column a','ðǣr there/where; ðanan from there; do not infer relative use from productive adverb there.'),
318:('unit12-source/cook_fb_1895_2-p318.png','column a','ðider thither;ðon sometimes for ðǣm/ðām supports distinct dative source analysis.'),
319:('unit12-source/cook_fb_1895_2-p319.png','column b','under-ðiedan/under-ðēodan source-family lexical entry subjoin/add; exact source153 form is retained without productive paradigm.')
}
fb[324]=('unit13-source/cook-fb-p324.png','columns a–b','wunian dwell/remain; wyrcean work/do/construct/make/build/yield. Distinguish prior work/deed scope from promotion of earlier supplied make sense. Ymbsęllan envelop/beset supports exact source form.')
for p,(path,loc,obs) in fb.items():ev('U13-FB'+str(p),'sources/audits/'+path,'cook_fb_1895_2',p,p+16,loc,obs)
for p,n in [(11,1),(12,2),(13,3)]:ev('U13-EX'+str(p),f'sources/audits/unit13-source/cook-ex-{n:03d}.png','cook_ex_1895',p,p+8,'VII.22–25 original prompts','All original lexical controls and exercise targets checked. 23.7 prints forceorfan,134; 25.7 explicitly says verb last.')
for p,unit,loc,obs in [(16,'unit11-grammar','§26','Grammatical and natural gender reference; no universal gender-only antecedent rule.'),(50,'unit08-grammar','§78','Finite-second means second constituent and is frequently violated. Dependent verb-late is a tendency; coordination and subject pronouns require attention.'),(54,'unit11-grammar','§83','Adverb/conjunction homographs and correlative duplication; semantic and syntactic context govern interpretation.'),(55,'unit11-grammar','§83 continued','When/then, where/there and related correlatives; limited new scope does not promote every family.')]:ev('U13-FULK'+str(p),f'sources/audits/{unit}/fulk-2020-p{p}.png','fulk_2020',p,p+12,loc,obs)
ev('U13-WRIGHT248','sources/audits/unit04-grammar/wright-p248-pdf268.png','wright_oe_1914',248,268,'§476','Dental ending contractions and sibilant outcomes; selected spelling alternatives must be identified, not silently substituted.')
ev('U13-WRIGHT-P294','sources/audits/unit13-source/wright-p294.png','wright_oe_1914',294,314,'§557 continuation before§558','Exact tō-morgen, to-morrow appears among nouns compounded with prepositions; supply only this invariant adverb. Page also distinguishes rest/direction adverbs.')
for p,loc,obs,url in [(303,'column b, for-ceorfan','Exact cut-down sense and strongIII parts; present cirf/cyrf are source variants, while selected ier is Cook-style rule-derived normalization.','https://bosworthtoller.com/11240'),(512,'column a, hatian','Shorta hatian hate, weak preterite ode/ede; distinct from longā hātian become hot.','https://bosworthtoller.com/18225'),(749,'column a lower, on-drǽdan IIb','Fear accusative person without reflexive dative: explicit hine/God/Johannem examples.','https://bosworthtoller.com/24505'),(843,'column a lower, scrýdan I','Accusative clothed person and mid plus garment; mid+dative clothing selected explicitly.','https://bosworthtoller.com/27066')]:ev('U13-BT'+str(p),f'sources/audits/unit13-grammar/bt-main-p{p}.jpg' if p!=843 else 'sources/audits/unit10-grammar/bt-27066-bt_b0843.jpg','bosworth_toller_1898_1921',p,None,loc,obs,url)
for i,r in read('sources/audits/unit13-coordinator/preposition-evidence.json')['evidence'].items():
    img=r['images'][0]
    E.append({'evidence_id':i,'source_id':r['source_id'],'origin_category':'exact_source','printed_page_identity':r['printed_pages'][0],'pdf_page_one_based':None,'locator':r['original_identifier'],'image_path':img['path'],'image_sha256':sha(img['path']),'image_inspected':True,'inspected_by':'unit13_grammar and coordinator independently','inspection_method':'Both agents personally viewed original facsimile; online transcription only located the evidence.','observation':r['claim'],'evidence_limits':r['evidence_limits'],'source_url':r['source_urls'][0]})
write('evidence-catalog.json',{'schema_version':1,'chapter':'ch13','status':'personally_image_checked','conventions':'Cook FB PDF page=printed+16; Exercises PDF page=printed+8; Wright=printed+20; Fulk=printed+12. PDF indexes are one-based. Textual line numbers between printed five-line markers are editorial counts. Dictionary columns are a(left),b(right); no PDF index is asserted for standalone JPEG facsimiles.','evidence':E})
print('catalog:',len(E),'personally inspected page records')
