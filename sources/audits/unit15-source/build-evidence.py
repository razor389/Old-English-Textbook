"""Seal inspected primary pages, with bounded claims rather than hash-only evidence."""
import json,pathlib,hashlib,shutil,collections
P=pathlib.Path(__file__).parent;R=P.resolve().parents[2]
def read(n):return json.loads((P/n).read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(n,x):(P/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
registry=json.loads((R/'sources/registry.json').read_text(encoding='utf8'))
caches={x['path']:x for x in registry['local_cache']}
uses=collections.defaultdict(set)
def walk(x,context=''):
 if isinstance(x,dict):
  label=next((str(x[k]) for k in ['rule_id','form_id','sense_id','source_item_id','support_id','source_span_id','lemma_id'] if k in x),context)
  for e in x.get('evidence_refs',[]):uses[e].add(label)
  for v in x.values():walk(v,label)
 elif isinstance(x,list):
  for v in x:walk(v,context)
for n in ['exercises-prompts.json','reading-source.json','reading-apparatus.json','lexical-inventory.json','source-support-records.json','reading-constructions.json']:walk(read(n),n)
FB={
28:('§43, strong masculine nouns; vowel retention/syncope','Strong masculine literal endings; stem-vowel conditions distinguish a short final element from a heavy one.'),
29:('§43 continuation, agent nouns in -end','Agent-noun plural zero/-e/-as and genitive -ra; selected reference cells explicitly distinguished from independently attested tokens.'),
30:('§44, names of peoples','Dęne and Engle belong to plural people names; Dęne genitive alternatives are stated.'),
31:('§44 continuation and §46 root nouns','Plural people-name endings and the root-noun framework.'),
32:('§46 continuation; §47 neuter nouns','Tōð has tēð with admitted tōðe/tōðas alternatives; heavy neuters have zero nominative/accusative plural.'),
33:('§47 continuation','Neuter -u versus zero plurals and hēafod/hēafdu with hēafd- before endings; not a license to syncopate every compound.'),
35:('§51, strong feminine nouns','Strong feminine case endings, including the selected oblique -e and plural -a/-um pattern.'),
36:('§51 continuation and §52 irregular feminines','-nes inflected -ness-; bōc belongs to the stated umlaut-feminine group, with a regular non-umlauted -e genitive alternative admitted for this class.'),
37:('§52.3 kinship noun; §53 weak nouns','Complete sweostor singular, sweostor/sweostra/sweostrum plural; weak masculine -a/-an/-ena/-um. Bōc and its class alternatives are on36.'),
38:('§55, foreign proper names','Foreign-name case forms may combine Latin and vernacular treatment; no uniform productive Latin paradigm inferred from Marian/Michaeles.'),
159:('Reader IX opening paragraph, editorial lines1–12; notes1–11','Exact selected 103-word argument and all eleven attached notes. Personal ðē retains its macron. Note3 reads188. Outer quotation continues beyond this paragraph.'),
160:('Reader IX continuation, opening through page end','Boundary control only: the following paragraph starts Ðū mann, tō hwon eart ðū mē swā ungeðancfull. Its text is unassigned in this unit.'),
161:('Reader IX continuation, especially editorial line5 and note6','Boundary and lexical-frame control only. Hafa æt ðīnum gewinne ðæt ðū mæge, and æt ðīnum geswince; note6 identifies æt as from. Lines15–16 attest the sun scorching fields. Not part of the assigned reading.'),
162:('Reader X complete, editorial lines1–17; notes1–7','Exact 152-word preface, title/subtitle and all seven notes. Notes6–7 distinguish reader from Alfred; source hyphens versus line-division hyphens retained separately.'),
163:('Reader XI complete, editorial lines1–18; notes1–9','Exact 160-word prayer, title/subtitle and all nine notes. Gehīersumnesse, gestaðela and Sīe are confirmed at400dpi; note8 reads196.d.'),
274:('Vocabulary: ǣghwilc, ǣgðer, ælmihtig, ǣmetta','Lexical headwords and contextual meanings for each/every, paired both, almighty and leisure.'),
275:('Vocabulary: āfierran, ālīesend, andgiet','Remove; Redeemer; understanding/sense. The derivative andgietfullice continues on276 and is cited there.'),
276:('Vocabulary: andgietfullice','Adverb clearly/intelligibly, supporting the reading’s attested superlative andgietfullicost.'),
277:('Vocabulary: āwęndednes, āwyrcean, bēcrǣding, becuman','Translation; do/perform; reading; come/befall. Meanings are applied to exact source tokens, not a fabricated full verb paradigm.'),
279:('Vocabulary: bisgian, bisgu, bōc, Bōclæden','Trouble/occupy; occupations; book; book-Latin. Bōclæden class47 is neuter; bōc paradigm is checked against §52.'),
281:('Vocabulary: clǣne, costnung','Pure/clean and temptation, with their stated class references.'),
282:('Vocabulary: dǣd','Deed and the attested endingless accusative dǣd in the selected source.'),
283:('Vocabulary: drēam','Joy/bliss, corroborated by the explicit warning in159n11 against translating dream.'),
284:('Vocabulary: earfoðrīme, earnung, eft','Hard to count; merits/services; again/afterwards.'),
285:('Vocabulary: Engle, Englisc, ęnde','English people, English language/adjective and end. The people-name plural is distinct from the language name.'),
286:('Vocabulary: fæsthafol','Holding fast/tenacious, interpreted with genitive goods in the personally checked sentence.'),
287:('Vocabulary: flǣsc; for-bærnan','Flesh is class47; scorch/parch is independently available for the sun-field sentence. No unassigned full verbal system inferred here.'),
288:('Vocabulary: forgieldan; for-ðām-ðe','Repay/recompense and causal because. Exact source infinitive and present forgielde are separately bound.'),
289:('Vocabulary: fūl, fultum','Foul and help/support; the prayer’s nominal predicate is not a finite verb.'),
290:('Vocabulary: gālnes','Lust, with feminine -nes morphology.'),
291:('Vocabulary: gedōn','Do/make; exact source gedēð and the translation’s resulting arrangement are distinguished by context.'),
292:('Vocabulary: geleornian','Learn/study, supporting the source participle geleornod in the anterior construction.'),
294:('Vocabulary: geręccan, gescieldan, gesęllan, gesewenlic','Explain/render; protect; give; visible. Only the reading’s exact forms are supplied by this packet.'),
295:('Vocabulary: gestaðolian/-staðelian, gestrangian, geðanc, geðęncean','Establish; strengthen; thought; remember. Reading gestaðela preserves the printed -e- variant.'),
296:('Vocabulary: gewissian, giefu','Guide and gift, applied to the precise source constructions.'),
297:('Vocabulary: hǣlu, hǣtu, hēafod','Salvation, heat and head. The abstract-u alternatives are bounded with Wright184 and BT500b; hēafod stem behavior is checked in §47.'),
298:('Vocabulary: hęfignes','Burden; complete feminine -nes system has explicit class/rule evidence.'),
299:('Vocabulary: hīera/hiere, hlāford','Third-person genitive plural variant hīera and masculine hlāford lord/master.'),
300:('Vocabulary: hundtēontig','A hundred(fold), with the source’s mid hundtēontigum interpreted as repayment in a hundredfold.'),
301:('Vocabulary: inweardlīce, Læden','Fervently/ardently; Latin with class47 neuter. The exact reading form Lædene is dative singular.'),
302:('Vocabulary: lārēow','Teacher/master, masculine class43.'),
303:('Vocabulary: lēoð, lof, lufe, lystan','Poem/verse, praise, weak noun love, impersonal please. Lyste is interpreted contextually in the prospective reader clause.'),
304:('Vocabulary: mǣð, mægðhād, manigfeald','Measure/capacity, maidenhood and manifold.'),
305:('Vocabulary: mislic','Various; reading datplmislicum has exact source evidence.'),
308:('Vocabulary: ongietan','Understand, with subjunctive ongiete supplied for the conditional reading clause.'),
309:('Vocabulary: rēcelēasian, rihtlīce','Neglect/despise and rightly; more correctly rihtlicor is the exact source comparative.'),
311:('Vocabulary: scieppend, sęlen','Creator and gift/bestowal; source sęlene refers to what the speaker bestowed.'),
312:('Vocabulary: simle, sind','Always and plural are; sind is retained as a source variant.'),
313:('Vocabulary: spell','Account/discourse, the dative result phrase tō Engliscum spelle.'),
314:('Vocabulary: strǣt, swā-hwæt-swā','Public place and whatsoever, explicitly supporting the new gathering-place sense and the bounded free-choice relative.'),
315:('Vocabulary: sweotole','Clearly, supporting the exact source superlative sweotolost.'),
316:('Vocabulary: tǣcan, tīd, tōforan, tōhopa, trēownes','Teach/show; hour; before/above; hope; trust. No hereafter sense is imported into worldly life.'),
317:('Vocabulary: ðearf','Need; profit, benefit, selecting benefit in tō mīnre sāwle ðearfe.'),
319:('Vocabulary: underfōn, ungesewenlic','Receive/take charge of and invisible; source participle/adjective cases are separately analyzed.'),
321:('Vocabulary: wealdend, wealhstōd, węndan','Ruler, translator/interpreter and translate; distinctions between actor and action maintained.'),
322:('Vocabulary: wer, willa, wīngeard','Adult man, will/intention and vineyard, with the stated declension classes.'),
323:('Vocabulary: wītan, wiðerwinna, wlanc, woruldbisgu, woruldlīf','Blame; adversary; proud/wealthy; worldly cares; worldly life. Wītan blame is distinct from wīte punishment; worldly life is not silently translated as the afterlife.')}
EX={15:('Group IX, Exercise28 items1–10 opening','All exact English wording, hints and original numbering; item10 continues on16.'),16:('Group IX, Exercise28 item10 continuation–12 and Exercise29 items1–11','All exact English wording and hints; burdens reference is51.5 and29.11 begins Show us.'),17:('Group IX, Exercise30 items1–13; joint X, XI Exercise31 items1–3 opening','All exact prompts;30.6 has he shall be called,30.8 earth,30.11 blōstmian (m confirmed by personal600dpi reinspection; earlier n audit withdrawn),30.12 If they can. Joint heading X, XI retained.'),18:('Joint X, XI Exercise31 item3 continuation–14','All exact prompts and hints, including31.11 twelve(155), years(154.c).'),41:('English glossary, burden','Hęfignes selected for burden, confirmed with Reader vocabulary298.'),46:('English glossary, English','Engle people-name plural distinguished from Englisc language/adjective.'),48:('English glossary, flesh','Flǣsc as the noun flesh.'),51:('English glossary, hour','Tīd hour, separately promoted from its earlier source-only sense.'),54:('English glossary, master','Lārēow teacher/master, corroborated by Reader vocabulary302.'),59:('English glossary, public place; reading; Redeemer','Strǣt public place, bēcrǣding reading and ālīesend Redeemer.'),65:('English glossary, translation','Āwęndednes translation and the complete feminine -nes system.')}
ev=[]
def add(eid,sid,page,pdf,identifier,claim,image,cache=None,url=None):
 rec=dict(evidence_id=eid,source_id=sid,printed_page=page,pdf_page_one_based=pdf,original_identifier=identifier,origin_category='exact_source',claim=claim,image=image.relative_to(R).as_posix(),image_sha256=sha(image),personally_viewed=True,inspection_agent='unit15_source',inspection_date='2026-10-26',used_by=sorted(uses[eid]),limitations='This page supports the stated lemma, source token or rule; a derived table cell is not asserted to be an individually attested corpus form.')
 if cache:rec.update(source_cache=cache,source_sha256=caches[cache]['sha256']);assert sha(R/cache)==caches[cache]['sha256']
 if url:rec['image_url']=url
 ev.append(rec)
for page,(identifier,claim) in FB.items():
 if page in [159,162,163]:im=P/f'reader-p{page}-400.png'
 elif page in [160,161]:im=P/f'reader-{page-158:03}.png'
 else:
  im=P/f'cook-fb-p{page}.png';shutil.copyfile(R/f'build/u15-source-fb-p{page}.png',im)
 add(f'U15-FB-P{page}','cook_fb_1895_2',page,page+16,identifier,claim,im,'sources/cache/cook_fb_1895_2.pdf')
for page,(identifier,claim) in EX.items():
 if page==17:im=P/'exercise-p17-600.png'
 elif page in range(15,19):im=P/f'exercise-{page-14:03}.png'
 else:
  im=P/f'cook-ex-p{page}.png';shutil.copyfile(R/f'build/u15-source-ex-p{page}.png',im)
 add(f'U15-EX-P{page}','cook_ex_1895',page,page+8,identifier,claim,im,'sources/cache/cook_ex_1895.pdf')
im=P/'wright-p184.png';shutil.copyfile(R/'build/u15-source-wright184.png',im)
add('U15-WRIGHT-P184','wright_oe_1914',184,204,'§382 continuation and §383, strengu-class abstract nouns','Hǣlu and hǣtu are expressly listed; -u/-o and oblique -e variation is described. Few nouns in this class have a plural. This evidence justifies the bounded singular selections and does not establish absolute historical defectiveness.',im,'sources/cache/wright_oe_1914.pdf')
add('U15-BT-P500B','bosworth_toller_1898_1921','Main500b',None,'s.v. hǽlu, hǽlo','Entry explicitly labels the noun indeclinable feminine and gives health, safety, salvation. Cook-style macrons replace dictionary acute quantity marks only in new teaching material.',P/'bt-main-p500.jpg',url='https://bosworthtoller.com/images-dictionary/bt_b0500.jpg')
add('U15-BT-P506','bosworth_toller_1898_1921','Main506a–b',None,'s.v. hám, beginning at bottom of a and continuing in b','Masculine noun hám with genitive -es; home/house/abode and attested plural forms support a nominal system distinct from the prior directional adverb.',P/'bt_b0506.jpg',url='https://bosworthtoller.com/images-dictionary/bt_b0506.jpg')
own={x['evidence_id'] for x in ev};missing={x for x in uses if (x.startswith('U15-FB-') or x.startswith('U15-EX-') or x.startswith('U15-BT-') or x.startswith('U15-WRIGHT-')) and x not in own};assert not missing,missing
external=sorted(x for x in uses if x not in own)
dump('evidence-catalog.json',dict(schema_version=1,baseline_checkpoint='9129cda',policy='Every claimed primary image personally inspected. OCR is a finding aid only. Earlier evidence IDs remain attached to unchanged prior records and resolve in the active earlier evidence catalogs; this packet does not claim fresh inspection of those older images. Grammar-worker IDs remain owned by its catalog.',evidence=ev,count=len(ev),external_evidence_refs=external))
dump('source-inputs.json',dict(schema_version=1,baseline_checkpoint='9129cda',sources=[dict(path=p,sha256=caches[p]['sha256'],bytes=caches[p]['bytes']) for p in ['sources/cache/cook_ex_1895.pdf','sources/cache/cook_fb_1895_2.pdf','sources/cache/wright_oe_1914.pdf']],facsimile_images=[x for x in ev if x['source_id']=='bosworth_toller_1898_1921'],page_conventions={'CookExercises':'Printed Arabic page+8 = one-based PDF page.','CookFirstBook':'Printed Arabic page+16 = one-based PDF page.','Wright':'Printed184 = one-based PDF204.','BT':'Independent printed-page facsimiles; a/b indicate columns, no invented local PDF locator.','reading_lines':'Editorial line counts anchored by printed marginal multiples of five; no claim all numbers appear in print.'}))
print(dict(evidence_records=len(ev),external_evidence_refs=len(external)))
