"""Source transcription and original apparatus, independently read from page images."""
import json,pathlib,re,hashlib
OUT=pathlib.Path(__file__).parent;ROOT=OUT.resolve().parents[2]
def dump(name,obj): (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines={168:[
'Æfter ðisum wordum hē ēode on ðone weg ðe him',
'getǣht[1] wæs, ōð-ðæt hē becōm tō ðǣre ceastre geate, and',
'ðǣr inēode. Mid-ðȳ-ðe hē ðōhte hwone hē biddan meahte',
'līfes fultumes,[2] ðā geseah hē ǣnne nacodne cnapan geond',
'ðā strǣte iernan. Sē wæs mid[3] ęle gesmierwed, and mid',
'scīetan begyrd, and bær geongra[4] manna[4] plegan[4] on handa,',
'tō ðǣm bæðstęde[5] belimpende.[6] And cleopode[7] micelre',
'stefne,[8] and cwæð: “Gehīere,[9] gē ceasterwaran[10]! Gehīere,',
'gē ęlðēodige,[11] frige and ðēowe, æðele and unæðele! Se',
'bæðstęde is open.”',
'Ðā-ðā Apollonius ðæt gehīerde, hē hine unscrȳdde ðǣm[12]',
'healfan sciccelse ðe hē on hæfde, and ēode intō ðǣm ðwēale.[13]',
'And mid-ðȳ-ðe hē behēold hiera ānra[14] gehwilcne on hiera',
'weorce, hē sōhte his gelīcan,[15] ac hē ne meahte hine ðǣr',
'findan on ðǣm flocce. Ðā fǣringa cōm Arcestrates, ealre',
'ðǣre ðēode[16] cyning,[17] mid micelre męnige his manna,[18] and',
'inēode on ðæt bæð. Ðā āgan se cyning plegian wið[19] his',
'gefērum mid ðoðore.[20] And Apollonius hine[21] gemęngde,[21]'],169:[
'swā-swā God wolde, on ðæs cyninges plegan, and, iern-',
'ende, ðone ðoðor gelæhte,[1] and, mid swiftre hrædnesse',
'geslægene,[2] ongēan gesęnde tō ðǣm plegiendan cyninge.',
'Ęft hē āgēan āsęnde; hē hrædlīce slōh, swā hē hine[3]',
'nǣfre feallan ne lēt. Se cyning ðā oncnēow ðæs geongan',
'snelnesse,[4] ðæt hē wiste[5] ðæt hē næfde his gelīcan on',
'ðǣm plegan.[6] Ðā cwæð hē tō his gefērum: “Gāð ēow',
'heonan; ðes cniht, ðæs-ðe mē ðyncð,[7] is mīn gelīca.”',
'Ðā-ðā Apollonius gehīerde ðæt se cyning hine hęrede,',
'hē arn hrædlīce, and genēalǣcte tō ðǣm cyninge, and',
'mid gelǣredre[8] handa[9] hē swang[10] ðone top mid swā',
'micelre swiftnesse ðæt ðǣm cyninge wæs geðūht swilce',
'hē of ielde tō geoguðe gewęnd wǣre. And, æfter ðǣm,',
'on his cynesętle hē him[11] gecwēmlīce[12] ðēnode[13]; and,',
'ðā-ðā hē ūtēode of ðǣm bæðe, hē[14] hine[15] lǣdde be ðǣre',
'handa, and him[16] ðā siððan ðanan gewęnde, ðæs weges[17]',
'ðe hē ǣr cōm.'],170:[
'Ðā cwæð se cyning tō his mannum,[1] siððan Apollonius',
'āgān[2] wæs: “Ic swęrie ðurh ðā gemǣnan hǣle[3] ðæt ic',
'mē nǣfre bęt ne baðode ðonne ic dyde[4] tō-dæg, nāt ic',
'ðurh[5] hwilces geonges mannes ðēnunge.[6] Ðā beseah hē',
'hine tō ānum his manna, and cwæð: “Gā, and gewite',
'hwæt[7] se geonga mann sīe, ðe mē tō-dæg swā wel gehīer-',
'sumode.”',
'Se mann ðā ēode æfter Apollonio. Mid-ðȳ-ðe hē geseah',
'ðæt hē[8] wæs mid horgum[9] sciccelse bewǣfed, ðā węnde',
'hē ongēan tō ðǣm cyninge, and cwæð: “Se geonga mann',
'ðe[10] ðū æfter āscodest is forliden[11] mann.[11]” Ðā cwæð se',
'cyning: “Ðurh[12] hwæt[12] wāst[13] ðū ðæt?” Se mann him',
'andswarode, and cwæð: “Ðēah hē hit self forswīge,[14] his',
'gegierela hine gesweotolað.” Ðā cwæð se cyning: “Gā',
'hrædlīce, and sęge him ðæt[15] ‘se cyning bitt ðē ðæt ðū',
'cume[16] tō his gereorde.’”']}
source_lines=[]
for p,ls in lines.items():
 for n,text in enumerate(ls,1):source_lines.append({'source_line_id':f'FB{p}-{n:02}','printed_page':p,'pdf_page_one_based':p+16,'editorial_line':n,'source_with_note_markers':text})
paragraphs=[[(168,1),(168,10)],[(168,11),(169,8)],[(169,9),(169,17)],[(170,1),(170,7)],[(170,8),(170,16)]]
texts=[]
for start,end in paragraphs:
 ls=[x['source_with_note_markers'] for x in source_lines if start<=(x['printed_page'],x['editorial_line'])<=end]
 text=re.sub(r'\[\d+\]','',' '.join(ls));text=re.sub(r'(?<=\w)- (?=\w)','',text);texts.append(text)
reading={'source_span_id':'FB-XII-APOLLONIUS-GYMNASIUM','title':'The Incidents in the Gymnasium','source_id':'cook_fb_1895_2','original_identifier':'Reader XII, subsection The Incidents in the Gymnasium, complete','origin_category':'exact source with declared layout normalization','printed_pages':[168,169,170],'pdf_pages_one_based':[184,185,186],'source_lines':source_lines,'learner_paragraphs':texts,'learner_text':'\n\n'.join(texts),'word_count':sum(len(t.split()) for t in texts),'line_number_convention':'Editorial count of Old English text lines from the first prose line on each printed page, anchored by printed marginal multiples of five. Individual line numbers are not all printed.','start':{'printed_page':168,'editorial_line':1,'text':'Æfter ðisum wordum'},'end':{'printed_page':170,'editorial_line':16,'text':'cume tō his gereorde.’”'},'prior_overlap':'None. Unit4 storm-to-shore and Unit6 fisherman gift/direction selections precede this scene; neither is reassigned here.','selection_rationale':'A complete source-titled scene: arrival and public announcement, game and royal recognition, departure, inquiry and identification, invitation. The following feast is outside the assignment.','source_paratext':{'printed_title':'The Incidents in the Gymnasium.','running_head':'APOLLONIUS OF TYRE.','original_reader_section':'XII'},'evidence_refs':['U16-FB-P168','U16-FB-P169','U16-FB-P170']}
dump('reading-source.json',{'schema_version':1,'source_spans':[reading],'total_word_count':reading['word_count'],'normalizations':['Remove original note cues from learner text; preserve separately with exact anchors.','Join ordinary printed line and page breaks; remove only the division hyphens in iernende (169.1–2) and gehīersumode (170.6–7).','Retain lexical/correlative hyphens and Cook’s letters, quantities, capitalization and punctuation, including the mixed quoted invitation.','Represent quotation marks typographically in Unicode; collapse spacing before punctuation.'],'status':'image-checked transcription; open to independent reconciliation before sealing'})
notes={168:[
'See 187.',
'MS. fultum. See 159. b.',
'See 174.',
'Lat. lusus juvenales.',
'Lat. gymnasium.',
'Modifies plegan.',
'See 20.',
'See 160. 1. This word is the Chaucerian steven.',
'See 95, note.',
'This is a compound word, formed of a Latin and an English element. Which is Latin, and what is its form in that language?',
'Lat. peregrini. See 152.',
'See 162.',
'Lat. lavacrum.',
'See 154. b.',
'Lat. parem, Eng. peer.',
'Lat. regionis.',
'See 151.',
'Lat. famularum. See 154. a.',
'Why not mid?',
'This curious word is very rare in Old English.',
'Lat. miscuit se. See 184. b.'],169:[
'See 114.',
'Lat. subtili velocitate percussam. The OE. participle is a little awkward.',
'The ball.',
'Lat. velocitatem.',
'See 126. What is the latest English quotation that you can find for this word?',
'This clause is not very clear. The Latin has: et quia sciebat se (i.e. Archistrates) in pilæ lusu neminem parem habere, ad suos ait, famuli, recedite; hic enim juvenis, etc.',
'Lat. ut suspicor. See 157. 1 and 164. l. What Mod. Eng. word comes from mē ðyncð?',
'Lat. docta.',
'See 51. 3.',
'Here the English departs from the Latin: ceroma fricavit eum tanta subtilitate, ut de sene juvenem redderet. Top would seem to signify the same as ðoðor.',
'See 164. e.',
'Lat. gratissime.',
'See 28.',
'Apollonius.',
'Archistrates.',
'See 184. a.',
'See 157.'],170:[
'Lat. amicos.',
'How is the sense of Mod. Eng. ago related to that of this word?',
'This phrase shows Christian influence.',
'Note this use of dōn to replace a verb of specific meaning.',
'Governs ðēnunge.',
'See 28.',
'How does this, as here used, differ in meaning from hwā?',
'Apollonius.',
'Lat. sordido.',
'Governed by æfter. See 87. c and 201. 1.',
'Lat. naufragus.',
'Lat. unde.',
'See 126.',
'See 196. e.',
'Confusion of two constructions, the direct and the indirect.',
'Lat. ut venias. Translate by the infinitive, as often in such cases.']}
apparatus=[]
for p,ns in notes.items():
 for n,text in enumerate(ns,1):
  anchors=[]
  for line in source_lines:
   if line['printed_page']==p:
    for m in re.finditer(r'\['+str(n)+r'\]',line['source_with_note_markers']):
     prefix=line['source_with_note_markers'][:m.start()]; anchor=re.search(r'([^\s\[\]]+)$',prefix).group(1)
     anchors.append({'source_line_id':line['source_line_id'],'editorial_line':line['editorial_line'],'anchor_text':anchor,'character_offset':m.start()})
  apparatus.append({'apparatus_id':f'FB-U16-{p}-N{n}','source_id':'cook_fb_1895_2','printed_page':p,'pdf_page_one_based':p+16,'original_note_number':str(n),'original_text':text,'origin_category':'exact source with declared typographic normalization','anchors':anchors,'disposition':'Retained original apparatus, separate from modern support. Questions are source paratext unless a task explicitly assigns them.','evidence_refs':[f'U16-FB-P{p}']})
dump('reading-apparatus.json',{'schema_version':1,'notes':apparatus,'count':len(apparatus),'anchor_count':sum(len(n['anchors']) for n in apparatus),'normalizations':['Join printed line divisions; original italics and bold are represented semantically as source content.','Retain original Latin spellings and source questions, including Archistrates beside text Arcestrates.']})
catalog=json.loads((OUT/'evidence-catalog.json').read_text())
for p in [168,169,170]:
 im=OUT/f'fb-p{p}.png';catalog[f'U16-FB-P{p}']={'source_id':'cook_fb_1895_2','printed_page':p,'pdf_page_one_based':p+16,'original_identifier':f'Reader XII, p{p}','origin_category':'exact source','image':im.relative_to(ROOT).as_posix(),'image_sha256':hashlib.sha256(im.read_bytes()).hexdigest(),'personally_viewed':True,'inspection_scope':'Every assigned text line and all original notes/anchors; source-specific spellings, macrons, and punctuation checked at300dpi. The feast opening on170 is outside the assignment.'}
dump('evidence-catalog.json',catalog)
dump('source-change-notes.json',{'schema_version':1,'changes':[{'change_id':'U16-T01','kind':'audit transcription repair; not source erratum','affected_source_items':['EX-XII-XIII-32-06'],'before':['sendan','nett'],'after':['sęndan','nętt'],'evidence':'600dpi ex-p18 image confirms the hooked vowels. Original source is unchanged.'}],'source_peculiarities':[{'id':'U16-P01','locator':'168 note2','original':'MS. fultum','edited_text':'fultumes','treatment':'Preserve Cook’s text and manuscript note; no new editorial emendation.'},{'id':'U16-P02','locator':'169.3 note2','original':'geslægene','treatment':'Preserve awkward printed participle and supply the whole phrase; no silent regularization.'},{'id':'U16-P03','locator':'169.5–7 note6','treatment':'Preserve the unclear nested knowledge/equal clause; support the plausible narrative reading without claiming unique pronoun resolution.'},{'id':'U16-P04','locator':'169.11 note10','original':'top','treatment':'Retain source and Cook’s tentative ball interpretation and Latin divergence; do not replace with Latin massage wording.'},{'id':'U16-P05','locator':'170.15–16 note15','treatment':'Preserve the mixed direct/reported invitation and original quotation punctuation; provide complete local explanation.'},{'id':'U16-P06','locator':'168.16 note18','original':'famularum','treatment':'Retain printed Latin word even though a masculine servant group could invite another Latin form; no silent correction.'}]})
changes=json.loads((OUT/'source-change-notes.json').read_text())
changes['changes'].append({'change_id':'U16-T02','kind':'audit transcription repair; not source erratum','affected_source_items':['EX-XII-XIII-34-03'],'before':'Let my hooks be sufficient for both of us','after':'Let my books be sufficient for both of us','evidence':'Original-resolution exercise-003.png and 600dpi close-ex-p20.png; closed lower bowl matches b in be and both on the same line. The original source is unchanged.'})
changes['changes'].append({'change_id':'U16-T03','kind':'audit transcription repair; not source erratum','locator':'168.2','before':'oð-ðæt','after':'ōð-ðæt','evidence':'600dpi close-fb-p168.png personally inspected; source has macron over o. Both occurrences of hiera in168.13 are unmarked and are retained.'})
changes['source_peculiarities'].append({'id':'U16-P07','locator':'170.2–4','treatment':'Source opens a double quotation at Ic swęrie but prints no closing quotation before Ðā beseah. Exact transcription retains it; any modern learner punctuation repair must be separately declared.'})
dump('source-change-notes.json',changes)
print({'words':reading['word_count'],'lines':len(source_lines),'notes':len(apparatus),'anchors':sum(len(n['anchors']) for n in apparatus)})
