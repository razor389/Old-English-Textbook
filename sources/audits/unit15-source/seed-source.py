"""Image-checked source transcription. All strings are editorial transcription."""
import json,pathlib,re,hashlib
OUT=pathlib.Path(__file__).parent
ROOT=OUT.resolve().parents[2]
def dump(name,data): (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
prompts={28:[
"Every one that (87. d) forsakes for my name his house, or his brethren, or sisters (52. 3), or father, or mother, or wife, or children, or lands, with a hundredfold (om. it shall) be requited to him (verb last), and he shall have besides eternal life.",
"He gave (sęllan) to each a penny in return for his day’s work.",
"He sent them into (on, 172) his vineyard.",
"He saw others in (om. the) public place standing (169) idle.",
"Then said he, Go ye also into my vineyard, and I will give you what (ðæt) is right.",
"Once more he went out about (ymbe, 172) the sixth and ninth hour, and did similarly.",
"Then about the eleventh hour he went out, and found others standing (pres. part.).",
"Then said he, Why stand ye here all day idle?",
"Then said they, Because no man (om. hath) hired (hȳrian, 118) us.",
"Truly, when even was come [when it was evening become], then said the lord (hlāford) of the vineyard to his steward (gerēfa, 53), Call (cleopian) the workmen, and pay them (164. a) their hire (mēd).",
"Accordingly, when those came that came about the eleventh hour (verb last), then received they each his penny.",
"And those, that there (ðǣr) first came, supposed that they should (sculan) receive more (māre)."],
29:[
"Thou (om. hast) made (dōn) them equal (gelīc) (om. unto) us, which (87. d) (om. have) borne burdens (51. 5) in this day’s heat.",
"Take that is thine, and go (om. thy way); I will give unto this (om. one) just (eall) as much as (om. unto) thee.",
"May I not do what (ðæt) I will?",
"Camest thou not to me to work (wyrcean, 200) for (wið) one penny?",
"He was (om. a) man (wer) and prophet, mighty in speech and in deed (weorc) before (beforan, 166) God and all (om. the) people (folc).",
"That is the judgment, that light (om. is) come into (on, 172) (om. the) world, and men loved darkness (plur.) rather (swīðor) than the light, because their deeds (weorc) were evil.",
"God sent not his son into (om. the) world that he (om. should) condemn the world, but that the world (om. may) be saved (hǣlan, 113) by (ðurh) him.",
"Your reward (om. shall) be great, and ye shall be (om. the) children of the Highest; because he is kind (gōd) unto (ofer, 172) (om. the) unthankful and evil.",
"Give, and (om. it) shall be given you.",
"The disciple (leornungcniht, 43) is not above (ofer, 172) his master (lārēow).",
"Show us thy mercy, and grant us thy salvation."],
30:[
"Swear (thou) not by (ðurh) heaven, because it is God’s throne; nor by earth, because it is his footstool (fōtsceamul, 43); nor by Jerusalem (Hierusalem), because it is (om. the) city of (om. the) great (mǣre) king.",
"Swear not by thy head, because thou canst not make (wyrcean) one hair (hǣr, 47) white or black.",
"Be your (plur.) speech thus, It is, It is not.",
"Ye (om. have) heard that (om. it) was said, Eye for (for, 166) eye, and tooth (46) for tooth.",
"He that breaks (tōweorpan, 104) one of (of, 166) these least commandments (bebod, 47), and teacheth (lǣran) men so (verb last), he (sē) shall be named least in (om. the) kingdom (rīce) of heaven.",
"He that doeth and teacheth it, he shall be called great (micel).",
"Ye (om. have) heard that (om. it) was said in old times (tīd), Kill (thou) not.",
"Is it your (sing.) earth?",
"He has from his labor what he can.",
"The sun parched his field.",
"The roads (weg) should blossom (blōstmian, 118), the roads should bloom, so fair (fæger) (om. a) bride (brȳd, 51. b) shall leave her home (hām).",
"If they can, let them live without me.",
"He never forsakes those that trust in (on) him (172)."],
31:[
"I know truly that my Redeemer liveth.",
"In my flesh I shall see God, I (om. my)self, and not (nā) (om. an)other.",
"He was taught (187) to do God’s will.",
"Lead (thou) us not into temptation, but deliver us from evil.",
"Be thy name hallowed.",
"Thy will befall (geweorðan, verb first) in earth as (swā-swā) in heaven(s).",
"No king of the English was so great as Alfred.",
"He fought with the Danes (44. 2); he judged his people; he made translations from Latin; he was poet (lēoðwyrhta).",
"His mother hight Osburg, and his father Æthelwulf.",
"He lived fifty-two years.",
"He learned reading after he was twelve (155) years (154. c) old.",
"His mother had a book of English poems, which she promised (om. to) whichever of her two sons (om. should) first learn it.",
"Alfred asked her, Wilt thou in fact give that book to one of us two (uncer), (om. to) him who first understands (ongietan) it?",
"Asser, Alfred’s bishop, wrote a book of (153) the king’s life."]}
items=[]
for ex,ps in prompts.items():
 for n,p in enumerate(ps,1):
  group='IX' if ex<31 else 'X, XI'; page=15 if ex==28 and n<10 else 16 if ex in [28,29] else 17 if ex==30 or n<3 else 18
  pages=[15,16] if ex==28 and n==10 else [17,18] if ex==31 and n==3 else [page]
  items.append({'source_item_id':f'EX-{group.replace(", ","-")}-{ex:02}-{n:02}','source_id':'cook_ex_1895','original_group':group,'original_exercise':ex,'original_item':n,'original_identifier':f'{group}.{ex}.{n}','printed_pages':pages,'pdf_pages_one_based':[v+8 for v in pages],'prompt':p,'origin_category':'exact source with declared typographic normalization','disposition_proposal':'assigned','evidence_refs':[f'U15-EX-P{v}' for v in pages]})
dump('exercises-prompts.json',{'schema_version':1,'source_id':'cook_ex_1895','count':len(items),'verification':'All four selected page images personally inspected first at structural resolution, then against fresh 220dpi renders. Original wording, parenthetic and bracketed hints, and the joint X, XI heading retained.','normalization':['Join line/page breaks and remove typographic word-division hyphens.','Represent typographic apostrophes with Unicode right apostrophe; collapse spacing before question marks.'],'source_anomalies':[],'items':items})
readings=[
{'source_span_id':'FB-IX-DUTIES-FIRST-ARGUMENT','title':'Duties of the Rich toward the Poor: first argument','printed_page':159,'identifier':'Reader IX, first paragraph','lines':[
'Se Hǣlend cwæð tō ðǣm wlancan[1]: “For hwȳ wǣre',
'ðū swā fæsthafol mīnra gōda, ðe ic ðē sealde? Tō',
'hwon[2] rēcelēasodest ðū ðǣre giefe, ðe ic ðē geaf? Ic ðē',
'nū āfierre[3] fram mīnre sęlene, ðe ic ðē forgeaf; ðonne',
'bist[3] ðū wǣdla on woruldlīfe. For hwon[2] noldest[4] ðū',
'geðęncean ðæt ic wille[5] forgieldan ǣghwilcum męnn āne',
'gōde dǣd, ðe for mīnum naman mann gedēð? Mid',
'hundtēontigum ic hit him forgielde,[3] swā hit is on',
'mīnum godspelle gecweden and gesǣd,[6] ‘Swā-hwæt-swā[7]',
'gē sęllað ānum of mīnum ðǣm lǣstum,[8] gē hit simle mē',
'sęllað,[9] and ic ēow wið[10] ðǣm gesęlle[3] ēcne drēam[11] on',
'heofonum.’'],
'selection_rationale':'Complete first argumentative paragraph: rebuke for withholding goods, the giver’s future response, and a gospel promise of repayment. The outer speech continues in the following distinct rebuke; this is not the complete speech or complete Reader IX.','unassigned_continuation':'Printed160.1 through Reader IX ending161.20; the next paragraph begins Ðū mann, tō hwon eart ðū mē swā ungeðancfull.'},
{'source_span_id':'FB-X-ALFRED-PREFACE','title':'Alfred’s Preface to Boethius','printed_page':162,'identifier':'Reader X, complete text','lines':[
'Ælfred cyning wæs wealhstōd[1] ðisse bēc, and hīe of',
'Bōclædene[2] on Englisc węnde, swā hēo nū is gedōn.',
'Hwīlum hē sętte word be worde, hwīlum andgiet of',
'andgiete, swā-swā hē hit ðā sweotolost and andgiet-',
'fullicost geręccan meahte for ðǣm mislicum and manig-',
'fealdum woruldbisgum ðe hine oft ǣgðer ge on mōde',
'ge on līchaman bisgodon. Ðā bisga[3] ūs sind swīðe',
'earfoðrīme ðe on his dagum on ðā rīcu becōmon ðe hē',
'underfangen hæfde, and ðēah, ðā hē ðās bōc hæfde',
'geleornod, and of Lædene tō Engliscum spelle gewęnd,',
'ðā geworhte hē hīe eft tō lēoðe, swā-swā hēo nū gedōn',
'is. And nū bitt[4] and for Godes naman hālsað ǣlcne',
'ðāra ðe ðās bōc rǣdan lyste,[5] ðæt hē for hine gebidde,',
'and him ne wīte gif hē[6] hit rihtlicor ongiete ðonne hē[7]',
'meahte; for-ðām-ðe ǣlc mann sceal be his andgietes',
'mǣðe, and be his ǣmettan, sprecan ðæt hē spricð, and',
'dōn ðæt-ðæt hē dēð.'],
'selection_rationale':'Complete short preface: translation method, practical obstacles, later versification, and appeal to readers.','unassigned_continuation':None},
{'source_span_id':'FB-XI-ALFRED-PRAYER','title':'A Prayer of King Alfred','printed_page':163,'identifier':'Reader XI, complete text','lines':[
'Dryhten,[1] ælmihtiga God,[1] Wyrhta and Wealdend ealra',
'gesceafta, ic bidde ðē for ðīnre miclan mildheortnesse,',
'and for ðǣre hālgan rōde tācne,[2] and for Sanctæ Marian',
'mægðhāde, and for Sancti Michaeles gehīersumnesse, and',
'for ealra ðīnra hālgena[3] lufan and hīera earnungum, ðæt',
'ðū mē gewissie[4] bęt ðonne ic āworhte tō ðē; and gewissa',
'mē tō ðīnum willan, and tō mīnre sāwle ðearfe,[5] bęt ðonne',
'ic self cunne[6]; and gestaðela mīn mōd tō ðīnum willan and',
'tō mīnre sāwle ðearfe; and gestranga mē wið ðæs dēofles[3]',
'costnungum; and āfierr fram mē ðā fūlan gālnesse and ǣlce',
'unrihtwīsnesse; and gescield mē wið mīnum wiðerwinnum,',
'gesewenlicum and ungesewenlicum; and tǣc mē ðīnne will-',
'an[7] tō wyrceanne; ðæt ic mæge[8] ðē inweardlīce lufian tō-',
'foran eallum ðingum, mid clǣnum geðance and mid clǣnum',
'līchaman. For-ðon-ðe ðū eart mīn Scieppend,[9] and mīn',
'Ālīesend, mīn Fultum, mīn Frōfor, mīn Trēownes, and',
'mīn Tōhopa. Sīe ðē lof and wuldor nū and ā ā ā, tō',
'worulde būtan ǣghwilcum ęnde. Amen.'],
'selection_rationale':'Complete prayer: request for guidance, sustained imperatives, purpose, grounds, and doxology.','unassigned_continuation':None}]
for r in readings:
 p=r.pop('printed_page'); lines=r.pop('lines'); r.update({'source_id':'cook_fb_1895_2','original_identifier':r.pop('identifier'),'origin_category':'exact source; layout and note-marker removal declared','printed_pages':[p],'pdf_pages_one_based':[p+16],'source_lines':[{'source_line_id':f'FB{p}-{n:02}','printed_page':p,'pdf_page_one_based':p+16,'editorial_line':n,'source_with_note_markers':s} for n,s in enumerate(lines,1)],'line_number_convention':'Editorial count of Old English prose lines from first line on the printed page, anchored by printed marginal multiples of five; no assertion that each individual line number is printed.','evidence_refs':[f'U15-FB-P{p}']})
 r['source_paratext']={159:{'printed_group':'IX.','printed_title':'DUTIES OF THE RICH TOWARD THE POOR.','printed_subtitle':'(From the same Homily as the last.)'},162:{'printed_group':'X.','printed_title':'ALFRED’S PREFACE TO BOETHIUS.','printed_subtitle':'(Prefixed to his translation.)'},163:{'printed_group':'XI.','printed_title':'A PRAYER OF KING ALFRED.','printed_subtitle':'(From the end of his translation of Boethius.)'}}[p]
 text=' '.join(lines); text=re.sub(r'\[\d+\]','',text); text=re.sub(r'(?<=\w)- (?=\w)','',text)
 r['learner_text']=text;r['word_count']=len(text.split());r['start']={'printed_page':p,'editorial_line':1,'text':text.split()[0]};r['end']={'printed_page':p,'editorial_line':len(lines),'text':lines[-1]}
dump('reading-source.json',{'schema_version':1,'source_spans':readings,'total_word_count':sum(r['word_count'] for r in readings),'normalizations':['Remove note cues and join ordinary line/page breaks.','Remove line-end word-division hyphens in andgietfullicost, manigfealdum, willan and tōforan only; retain lexical/correlative hyphens (swā-swā, swā-hwæt-swā, for-ðām-ðe, for-ðon-ðe, ðæt-ðæt).','Retain Cook’s source letters, length marks, capitalizations and punctuation; the Duties outer opening quote remains unmatched in the bounded original because the speech continues. Any learner closing quote must be declared separately.']})
notes={159:[
'From what OE. word is the Mod. Eng. rich derived (see Skeat, Prin., p. 61)? From what OE. meaning is the modern signification derived?',
'Note Wulfstan’s use of tō hwon, for hwon, in the sense of why. See 88.',
'See 188.',
'See 139.',
'Why should not the preterit be used here?',
'Pleonastic.',
'What portion of this is lost, and how is it replaced, in the Mod. Eng. whatsoever?',
'See 66.',
'Cf. the form of this sentence with that on p. 135, l. 14.',
'= in return for. How is this to be reconciled with other senses of wið?',
'Not dream, but joy, bliss.'],162:[
'Wealh- signifies foreign (see walnut), and sometimes servant, orig. Celtic, Celt (cf. Wales, Welsh, Cornwall), from Volcæ, the name of a Celtic tribe (Cæsar, Gallic War, Bk. VII.).',
'Perhaps originally in contrast to the Latin spoken in Britain.',
'See 51. a.',
'Supply hē.',
'See 190.',
'The reader.',
'Alfred.'],163:[
'See 152.',
'Governed by for.',
'See 153. c.',
'See 194. b.',
'See 166.',
'Optative (130).',
'Object of wyrceanne.',
'See 196. d.',
'See 150.']}
apparatus=[]
for p,ns in notes.items():
 for n,t in enumerate(ns,1):
  anchors=[{'source_line_id':l['source_line_id'],'editorial_line':l['editorial_line']} for r in readings for l in r['source_lines'] if l['printed_page']==p for m in re.finditer(r'\['+str(n)+r'\]',l['source_with_note_markers'])]
  apparatus.append({'apparatus_id':f'FB-U15-{p}-N{n}','source_id':'cook_fb_1895_2','printed_page':p,'pdf_page_one_based':p+16,'original_note_number':str(n),'original_text':t,'origin_category':'exact source with declared typographic normalization','anchors':anchors,'disposition':'retained original apparatus; historical questions are source paratext, not independently assigned learner tasks','evidence_refs':[f'U15-FB-P{p}']})
dump('reading-apparatus.json',{'schema_version':1,'notes':apparatus,'count':len(apparatus),'anchor_count':sum(len(x['anchors']) for x in apparatus),'normalizations':['Join printed line divisions and use curly apostrophes.','Typography (italic versus roman and bold source lemmas) is encoded semantically in the content; wording is preserved.']})
catalog={}
for p in range(15,19):
 im=ROOT/f'sources/audits/course-map/ex-page{p}.png';catalog[f'U15-EX-P{p}']={'source_id':'cook_ex_1895','printed_page':p,'pdf_page_one_based':p+8,'original_identifier':f'Exercises page{p}','origin_category':'exact_source','image':im.relative_to(ROOT).as_posix(),'image_sha256':hashlib.sha256(im.read_bytes()).hexdigest(),'personally_viewed':True,'inspection_scope':'Every Unit15 prompt on page, original hints/numbering/group headings.'}
for p,n in [(159,1),(160,2),(161,3),(162,4),(163,5)]:
 im=OUT/f'reader-{n:03}.png';catalog[f'U15-FB-P{p}']={'source_id':'cook_fb_1895_2','printed_page':p,'pdf_page_one_based':p+16,'original_identifier':f'Reader page{p}','origin_category':'exact_source','image':im.relative_to(ROOT).as_posix(),'image_sha256':hashlib.sha256(im.read_bytes()).hexdigest(),'personally_viewed':p in [159,162,163],'inspection_scope':'Exact source and complete attached apparatus.' if p in [159,162,163] else 'Selection-boundary context; low-resolution earlier audit image personally viewed, newly rendered image pending.'}
dump('evidence-catalog.json',catalog)
print(json.dumps({'prompts':len(items),'readings':[(r['source_span_id'],r['word_count']) for r in readings],'notes':len(apparatus),'anchors':sum(len(x['anchors']) for x in apparatus)},ensure_ascii=False))
