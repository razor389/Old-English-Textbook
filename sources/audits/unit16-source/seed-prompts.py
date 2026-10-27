"""Exact English prompt transcription from personally inspected 300 dpi page images."""
import hashlib,json,pathlib
OUT=pathlib.Path(__file__).parent
ROOT=OUT.resolve().parents[2]
prompts={32:[
'I bid you all farewell (grētan).',
'When they had rowed about (swilce) twenty furlongs (furlang, 47), or thirty, then saw they Jesus walking (gān) on (uppan, 166) the sea (verb last).',
'He arose and commanded (bebēodan) the wind (164. b), and said (cweðan) to the sea, Subside.',
'The wind ceased (geswīcan), and there was (weorðan) (om. a) great calm.',
'Thou hearest his voice, and thou knowest not whence he cometh, nor whither he goeth.',
'He saw two brethren casting (sęndan) their net (nętt, 47) into (on, 172) the sea; they were fishers.',
'And he said (sęcgean) to them (164. b), Come after (æfter, 166) me, and I (om. will) make (dōn) that ye (dual) are fishers of men (153. d); and they immediately left their nets.',
'If thy hand or thy foot offend (ǣswician, 118) thee, cut it (āceorfan, 104) off (of), and cast (om. it) from thee; (om. it) is better (om. for) thee (165) that thou go halt (healt, 58) into life, than (om. that) thou have two hands and two feet, and be cast into everlasting fire.',
'If any (hwilc) man hath (om. a) hundred sheep (154. c), and loseth (forlēosan) one of (of, 166) them [those], (om. doth) he not leave the nine and ninety in the mountains, and goeth and seeketh (sēcean) the one that (87. d) was perishing (forwearð)?',
'And if it happeneth that he finds it, truly I say (sęcgean) to you that he rejoiceth more (swīðor) over (ofer, 172) that one than over the nine and ninety.',
'When he cometh home (hām), he calleth (cleopian) together his friends and his neighbors (nēahgebūr, 43), and saith (cweðan), Rejoice with me, because I (om. have) found my lost sheep.'
],33:[
'And, going (gangan) into (intō, 166) the house, they found the child with Mary (Maria, 53) his mother.',
'Arise, and take (niman) the child and his mother by night, and flee to (tō, 166) (om. the) land of the Egyptians, and be there until (that) I tell thee (verb last).',
'He arose then, and took the child and his mother by night, and journeyed into (on, 172) the land of the Egyptians; that it (om. might) be fulfilled (gefyllan) which (87. a) was spoken (cweðan) of (fram, 166) (om. the) Lord by (ðurh, 172) the prophet, From (of, 166) (om. the) Egyptians (om. have) I called (cleopian) my son.',
'What can they ask for [request; 156. b]?',
'The sun rules over the day (156. f).',
'They expected nothing but [except] death itself (156. g).',
'Thou wilt cease from thy work (156. k).',
'Perhaps he will find a friend (194. a).',
'He said to them, I will (139) go a fishing; they said, And we will go with thee.',
'They went out (ūt), and went into (om. a) ship, and caught nothing (183) in (on) that night.'
],34:[
'Whoever you are (193. c), forsake me not.',
'If you find nobody (196. d) that will feed you, return hither.',
'Let my books be sufficient for both of us (see p. 167, l. 13).',
'Both the boys are well educated.',
'They were both righteous before (beforan, 166) God.',
'I conjure thee by (ðurh) the living God, that thou tell us if thou be Christ, (om. the) Son of God.',
'I tell you, After these (om. things), ye shall see the Son of Man sitting on (on, 172) the right hand of (om. the) majesty of God, and coming in (om. the) clouds of heaven.',
'Be (om. it unto) you two (dual, 81) according to (æfter) your faith.',
'Truly the Son of Man is to come (200) in (on, 166) his Father’s glory (wuldor), and then (ðonne) (om. shall) reward (āgyltan, 113) every one (164) according to (be) his own work.',
'When (ðonne) Christ cometh, then knoweth no man whence he is.',
'Jesus cried (cleopian) and taught (lǣran) in the temple, and said, Me ye know (cunnan), and ye know (witan) whence I am; and I came not from myself [me self], but he is true that (87. d) sent me, whom (87. a) ye know not.',
'Ye have not known (pret.) him; I know him, and if I say that I know (194) him not (verb last), I (om. shall) be like (om. unto) you (165); but I know him, and I keep (healdan) his saying (sprǣc).',
'If I glorify myself, my glory is (183) naught (verb first); my Father (om. it) is, that (87. d) glorifieth me, concerning whom (87. a) ye say (cweðan) that he is (194) your God.'
],35:[
'Catch this ball.',
'Who caught the black ball?',
'Go the way that (87. d) you came.',
'I never played better than I did to-day.',
'She never sang better than she did now.',
'Thrice (ðrīwa) I suffered shipwreck; a night (170) and a day I was in this sea.',
'I knew (witan) a certain man that (87. d) was carried (lǣdan) unto (ōð, 172) the third heaven, and there (ðǣr) heard the words that no earthly man may (not) speak (sprecan).',
'O, how narrow (nearu, 57. 5) is the gate and the way that (87. d) leads to life (verb last), and very few (om. there) are that find the way.',
'They come to (tō, 166) you in sheep’s garments (gegierela), but within (innan) they are wolves.',
'When he came nigh (nēalǣcan) to the gate (163) of the city, then (ðā) was there (ðǣr) a dead man carried (beran).',
'I see a girl running (169) along (172) the street.',
'Anoint me with oil.',
'Give (sęllan) us of (of, 166) your oil.',
'If the Son delivers you, ye (om. shall) indeed be free.'
],36:[
'Judge ye not according to (be) appearance (ansīen, 51. b), but judge right judgment (168. 1).',
'Then turned (bewęndan, 184. a) he to the woman, and said, Seest thou this woman? I went into (intō) thy house, thou gavest me not water for (tō) my feet; this (om. one hath) washed (101. VI.) my feet with (mid) her tears.',
'Thou gavest (verb last) me not (om. a) kiss (coss, 43); this (om. one), since (siððan) I entered, (om. hath) ceased not to kiss [that she kissed] my feet.',
'My head thou with oils (om. didst) not anoint (smierwan, 113); this one anointed my feet with ointment (sealf, 51. b).',
'Therefore I say (sęcgean) to thee (164. b), Many sins are forgiven (forgiefan) her, because she loved (verb last) me much (swīðe).',
'Less (neut. acc. sing.) loveth (om. to) whom (87. b) less forgiven is.',
'It (om. is) not permitted (ālīefan) thee to have her to wife.',
'Then he promised with (mid) oath (āð, 43) to give (sęllan) her whatsoever she (om. should) ask (biddan) him.',
'Then, admonished (myngian) by (fram) her mother, she said, Give me in a dish (disc, 43) the head of John (Johannes) the Baptist (fuluhtere, 44. 1).',
'Then he sent (āsęndan), and beheaded (behēafdian, 118) John in the prison.',
'And one brought his head in a dish.'
]}
items=[]
for ex, rows in prompts.items():
    for n, prompt in enumerate(rows,1):
        page=18 if ex==32 and n<=6 else 19 if ex==32 or ex==33 and n<=3 else 20 if ex==33 or ex==34 and n<=11 else 21 if ex in [34,35] else 22
        pages=[18,19] if ex==32 and n==6 else [19,20] if ex==33 and n==3 else [20,21] if ex==34 and n==11 else [page]
        items.append({'source_item_id':f'EX-XII-XIII-{ex:02}-{n:02}','source_id':'cook_ex_1895','original_group':'XII, XIII','original_exercise':ex,'original_item':n,'original_identifier':f'XII, XIII.{ex}.{n}','printed_pages':pages,'pdf_pages_one_based':[p+8 for p in pages],'prompt':prompt,'origin_category':'exact source with declared typographic normalization','disposition_proposal':'assigned','evidence_refs':[f'U16-EX-P{p}' for p in pages]})
record={'schema_version':1,'source_id':'cook_ex_1895','count':len(items),'verification':'All five original page images personally viewed at course-map resolution and every prompt rechecked at fresh 300dpi. All hints, square-bracket paraphrases, omissions, number and word-order controls retained.','normalization':['Join printed line and page breaks; remove only typographic word-division hyphens.','Collapse spacing before punctuation; retain lexical to-day and all source punctuation.','Use Unicode apostrophes and æ/ð/ę and printed macrons; no silent linguistic normalization.'],'source_anomalies':[],'boundary_note':'The instruction to omit articles and second-person pronouns belongs to Exercise37, outside this assignment. Group XII, XIII is joint; it does not by itself establish a derivation from either reader section.','items':items}
(OUT/'exercises-prompts.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
catalog={}
for p in range(18,23):
    im=OUT/f'exercise-{p-17:03}.png'
    catalog[f'U16-EX-P{p}']={'source_id':'cook_ex_1895','printed_page':p,'pdf_page_one_based':p+8,'original_identifier':f'Exercises page {p}','origin_category':'exact source','image':im.relative_to(ROOT).as_posix(),'image_sha256':hashlib.sha256(im.read_bytes()).hexdigest(),'personally_viewed':True,'inspection_scope':'Every assigned prompt, parenthetic hint, omission and target control; joint group heading on p18; Exercise37 instruction excluded on p22.'}
(OUT/'evidence-catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print({ex:len(rows) for ex,rows in prompts.items()})
