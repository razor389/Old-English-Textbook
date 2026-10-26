import json
from pathlib import Path
P=Path(__file__).resolve().parent
# Original wording is source evidence. These instructions are not new learner tasks.
DATA={156:[
('1','See 144.','Reference to noun formation; the local danger-noun help supplies the reading.'),
('2','See 114.','The passive participle ymbseald is supplied; this does not assign a new full verbal system.'),
('3','Swā . . . māran, swā . . . swīðran = the greater, the fiercer. Note the tendency to antithesis.','Preserve the proportional meaning; paired comparisons are locally explained.'),
('4','Observe the redundancy.','The two infinitives recognize/understand reinforce the same act. Their object is accusative bȳsena; be ðǣm is separate.'),
('5','See weaxan.','Exact wiexð differs from the earlier selected wiext; supply the source spelling.'),
('6','= so that.','The tree clause states the result of its growth.'),
('6a','See brǣdan (34).','Supply brǣt and its reflexive object; preserve the a-suffixed original note number.'),
('7','See 184. b.','Hit is the tree itself, a reflexive accusative with spreading.'),
('8','Note the alliteration.','Retained observation only; no independent alliteration exercise is assigned.'),
('9','Second subject of gestęnt.','Wind is coordinated with storm, not an object.'),
('10','Frequently the second correlative, in such pairs as ðonne . . . ðonne, ðā . . . ðā, need not be translated; it is frequently followed by an inverted order, as here, the verb preceding its subject. See 202.','Explain the resumptive then and subject/verb order within the supplied reading frame.'),
('11','Se ōðer wudu = the rest of the forest, not the other wood.','Supply the contextual remaining/rest-of sense.'),
('12','Probably here = crag.','Cook qualifies this contextual interpretation of torrum. Keep the qualification and distinguish prior tower.')],
157:[
('1','See p. 156, n. 12.','C05: the exact pointer leads to the note about torrum/crag. The relevant parallel for ōðre as the rest of is p.156 n.11. Preserve the original; do not claim certainty about the cause or intended pointer.'),
('2','This resembles the use of gin in Chaucer, almost as an auxiliary tense-sign, like do in Mod. Eng., the latter not being thus used in OE. In Chaucer it usually occurs as the preterit gan, e.g. in the Clerk’s Tale, 392: “til the sonne gan descende.” See Lounsbury’s History of the English Language. An interesting parallel is to be found in New Testament Greek, as, for example, Acts 1. 1: “The former treatise I made, O Theophilus, concerning all that Jesus began (ἤρξατο) both to do and to teach.” According to Thayer, however (Greek-English Lexicon of the New Testament), there is in its employment always a sense of beginning, in its proper meaning.','Retain historical comparison as reference. The learner help gives onginnað + two coordinated infinitives and permits a natural beginning/falling rendering; no Chaucer or Greek knowledge is assessed.'),
('3','Dependent, like feallan, on onginnað. Give the ind. pret. plur.','Original request retained as reference-only, with the supplied answer hruron, indicative preterite plural. It is not an independent production task and establishes no full hrēosan paradigm.'),
('4','It would be interesting to know from what literary source these illustrations are ultimately derived. They remind one of Shakespeare (Rich. III., 1. 3. 259–260):—\nThey that stand high have many blasts to shake them;\nAnd if they fall, they dash themselves to pieces.\nCf. also 3 Hen. VI., 5. 2. 11–15. No doubt many Elizabethan parallels could be found; I have noted in Chapman, Byron’s Conspiracy, Act 3, Scene 1 (p. 232 of Shepherd’s ed.), and Byron’s Tragedy, Act 5, Scene 1 (Ib., p. 272). Perhaps the Elizabethans may have derived them from Seneca; cf. the Chorus in Act 4 of the Hippolytus, vv. 1123–1143; Hercules Furens 201; Œdipus 8–11. Seneca may have caught a suggestion from Sophocles, though the parallel is somewhat remote; see the latter’s Antigone, vv. 712–717, and Horace, C. II. 10.','The entire source note is retained as literary commentary. Its suggestions are Cook’s, not newly verified assertions about direct borrowing. No external-literature research question is added.'),
('5','See 58. 1.','The source hēagum retains g; its exact form is supplied rather than substituted with prior hēaum.'),
('6','Redundant. What is dūn in Mod. Eng. (24)? Whence is the adverb down derived?','Original questions retained and answered as historical reference: a down is a hill/upland; the adverb developed from a phrase meaning from a hill. Cook’s p.273 ā-dūn entry gives the derivation. No independent etymological production task is assigned.'),
('7','Note the poetical term.','Heofonfȳre is the supplied transparent compound fire from heaven; the learner task may identify its given components.')],
158:[
('1','This suggests Seneca (Œdipus, Act 1, v. 11):—\nImperia sic excelsa Fortunae objacent.','Retained literary comparison only; no Latin translation is required.'),
('2','Pleonastic.','The paired falling verbs reinforce the concluding collapse.'),
('3','Genitive, dependent on welan.','The same note is attached to both ðisse and worulde; both form one genitive phrase dependent on plural subject welan.'),
('4','Cf. Mod. Eng. come to naught.','The whole result idiom is locally supplied; no broad negative system is assigned.')]
}
rows=[]
for page,notes in DATA.items():
 for number,text,explanation in notes:
  rows.append({'apparatus_id':f'FB-VIII-DANGERS-{page}-N{number}','source_id':'cook_fb_1895_2','printed_page':page,'pdf_page_one_based':page+16,'original_note_number':number,'original_text':text,'origin_category':'exact_source','typographic_normalizations':['Joined line-end word divisions; paragraph and poetic line boundaries retained semantically.','Curly quotation marks and en dashes are typographic normalization; lexical wording unchanged.'],'disposition':'retained_source_reference_with_explicit_help; not a new independently assessed task','editorial_explanation':explanation,'evidence_refs':[f'U14-SRC-P{page}']})
src=json.loads((P/'reading-source.json').read_text(encoding='utf8'))
import re
anchors=[]
for line in src['source_lines']:
 for m in re.finditer(r'\[([0-9]+[a-z]?)\]',line['source_with_note_markers']):
  anchors.append({'source_line_id':line['source_line_id'],'apparatus_id':f"FB-VIII-DANGERS-{line['printed_page']}-N{m.group(1)}",'original_note_number':m.group(1),'preceding_text':line['source_with_note_markers'][:m.start()]})
assert len(rows)==24 and len(anchors)==25
obj={'schema_version':1,'scope':'All original notes attached to the selected156.1–158.4 excerpt; notes on the unassigned continuation are not assigned.','count':24,'anchor_occurrences':25,'notes':rows,'anchors':anchors,'source_intro':{'title':'VIII. THE DANGERS OF GREATNESS.','attribution':'(From Wulfstan’s Homilies, No. 49.)','original_context':'[Wulfstan — also known by his Latinized name, Lupus — was Bishop of Worcester and Archbishop of York from 1002 to 1023. This homily is one of those attributed to him, but, according to Napier, with insufficient reason, as a portion of it is found in the Blickling Homilies, the manuscript of which bears the date of 971.]','status':'Historical selected-edition framing preserved as source metadata, not a fresh attribution claim.'}}
(P/'reading-apparatus.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print({'notes':len(rows),'anchors':len(anchors)})
