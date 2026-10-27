"""Visible bounded Cook support; no supplied item becomes an independent recall target."""
import json,pathlib,copy
R=pathlib.Path(__file__).resolve().parents[3];O=pathlib.Path(__file__).resolve().parent
L={x['lemma_id']:x for x in json.loads((R/'lexicon/entries.json').read_text(encoding='utf-8-sig'))['lemmas']}
SL=json.loads((R/'sources/audits/unit15-source/source-support-records.json').read_text(encoding='utf-8'))['lemmas']
ALL=copy.deepcopy(L)
for x in SL:
 a=ALL.setdefault(x['lemma_id'],{'lemma_id':x['lemma_id'],'forms':[],'senses':[]})
 for k in ['forms','senses']:
  idk='form_id' if k=='forms' else 'sense_id'
  seen={v[idk] for v in a[k]};a[k].extend(v for v in x[k] if v[idk] not in seen)
D={'schema_version':1,'chapter':'ch15','status':'bounded_source_support_proposal','origin_category':'new_teaching_material','lemmas':[],'features':[],'reading_bindings':[],'cook_support':[],'reading_support':[]}
LM={}
def lem(i,h,pos):
 return LM.setdefault(i,{'lemma_id':i,'display_headword':h,'part_of_speech':pos,'prior_lemma_present':i in L,'forms':[],'senses':[],'scope_note':'Exact displayed support only; no full unassigned system and no unaided recall implied.'})
def form(i,h,pos,fid,surf,analysis,ev):
 old=next((f for f in ALL.get(i,{}).get('forms',[]) if f['form_id']==fid),None)
 f={'form_id':fid,'form':surf,'analysis':old['analysis'] if old else analysis,'knowledge_status':'supplied','teaching_ids':['NEW-U15-LOCAL-HELPS'],'evidence_refs':ev,'scope_note':'Only the exact Cook expression is supplied.'}
 if old:f['prior_scope']={k:old.get(k) for k in ['recognition_taught_in','production_taught_in','supplied_in']}
 lem(i,h,pos)['forms'].append(f);return fid
def sense(i,h,pos,sid,gloss,ev):
 if not any(s['sense_id']==sid for s in lem(i,h,pos)['senses']):lem(i,h,pos)['senses'].append({'sense_id':sid,'gloss':gloss,'knowledge_status':'supplied','teaching_ids':['NEW-U15-LOCAL-HELPS'],'evidence_refs':ev,'scope_note':'Only the displayed expression; no broader syntax assigned.'})
 return sid
def bind(i,fid,sid):
 if (i,fid)==('for','for-invariant'):fid='for-invariant-source-source'
 if (i,fid)==('to','to-invariant'):fid='to-preposition-dative-invariant'
 f=next((f for f in LM.get(i,{}).get('forms',[]) if f['form_id']==fid),None) or next((f for f in ALL[i]['forms'] if f['form_id']==fid),None)
 if f is None:
  # Only an explicit unique invariant may repair a stale guessed identifier.
  fs=ALL[i]['forms']; fs=[v for v in fs if v['form']=={'for':'for','to':'tō'}.get(i,'__missing__')]
  if len(fs)!=1:raise ValueError((i,fid,[(v['form_id'],v['form']) for v in fs]))
  f=fs[0];fid=f['form_id']
 return {'lemma_id':i,'form_id':fid,'sense_id':sid,'form':f['form'],'form_status':'supplied' if not f.get('production_taught_in') else 'previously_taught','sense_status':'supplied'}
def sup(i,title,txt,ids,bindings,ev):
 q={'support_id':i,'feature_id':i,'title':title,'text':txt,'bindings':bindings,'used_in_tasks':ids.split(),'evidence_refs':ev,'knowledge_status':'supplied','display_required':True}
 D['cook_support'].append(q);D['features'].append({'feature_id':i,'title':title,'description':txt,'scope_note':'Exact local help; do not assess unsupported independent recall.','knowledge_status':'supplied','evidence_refs':ev,'teaching_ids':['NEW-U15-LOCAL-HELPS'],'used_in_tasks':ids.split()})

form('nigotha','nigoða','ordinal','nigotha-u15-acc-f-sg-source','nigoðan',{'case':'accusative','gender':'feminine','number':'singular','declension':'weak'},['U15-G-FB46','U15-G-FB48'])
sense('nigotha','nigoða','ordinal','nigotha-u15-source','ninth',['U15-G-FB46'])
form('endlefta','endlefta','ordinal','endlefta-u15-acc-f-sg-source','endleftan',{'case':'accusative','gender':'feminine','number':'singular','declension':'weak'},['U15-G-FB46','U15-G-FB48'])
sense('endlefta','endlefta','ordinal','endlefta-u15-source','eleventh',['U15-G-FB46'])
form('heah','hēah','adjective','heah-u15-highest-gen-source','Hēahstan',{'case':'genitive','gender':'masculine','number':'singular','degree':'superlative','declension':'weak','function':'substantival divine title'},['U15-G-FB43','U15-G-EX16'])
sense('heah','hēah','adjective','heah-u15-highest-title','the Highest, divine title',['U15-G-FB43','U15-G-EX16'])
form('hatan','hātan','verb','hatan-u15-hatte-source','hātte',{'tense':'preterite','person':3,'number':'singular','voice':'lexical passive','function':'special is/was called form'},['U15-G-FB297'])
sense('hatan','hātan','verb','hatan-u15-be-called','be called; be named, special hātte',['U15-G-FB297'])
form('fiftig','fīftig','numeral','fiftig-u15-source','fīftig',{'function':'count numeral in supplied fifty-two construction'},['U15-G-FB46','U15-G-FB48'])
sense('fiftig','fīftig','numeral','fiftig-u15-source-sense','fifty',['U15-G-FB46'])
form('englisc','Englisc','adjective','englisc-u15-source-gen-pl','Engliscra',{'case':'genitive','number':'plural','gender':'neuter','declension':'strong'},['U15-G-EX46','U15-G-FB39'])
sense('englisc','Englisc','adjective','englisc-u15-source-sense','English',['U15-G-EX46'])
form('leornian','leornian','verb','leornian-u15-preterite-subj-3-sg-source','leornode',{'tense':'preterite','mood':'subjunctive','person':3,'number':'singular'},['U15-G-FB74','U15-G-EX18'])
form('yfel','yfel','adjective/substantive','yfel-u15-substantive-dat-source','yfele',{'case':'dative','number':'singular','gender':'neuter','declension':'substantive a-stem','function':'abstract evil'},['U15-G-FB324','U15-G-EX18'])
sense('yfel','yfel','adjective/substantive','yfel-u15-noun-evil-source','evil, substantive noun in fram yfele',['U15-G-FB324','U15-G-EX18'])
for i,h,ca,fid in [('hierusalem','Hierusalem','accusative','hierusalem-u15-source-acc'),('osburg','Osburg','nominative','osburg-u15-source-nom'),('aethelwulf','Æthelwulf','nominative','aethelwulf-u15-source-nom'),('asser','Asser','nominative','asser-u15-source-nom'),('aelfred','Ælfred','genitive','aelfred-u15-source-gen-sg')]:
 surf='Ælfredes' if i=='aelfred' else h
 form(i,h,'proper name',fid,surf,{'case':ca,'number':'singular','scope':'exact supplied name'},['U15-G-EX17' if i=='hierusalem' else 'U15-G-EX18'])
 sense(i,h,'proper name',i+'-u15-source-sense',h,['U15-G-EX17' if i=='hierusalem' else 'U15-G-EX18'])
form('laeden','Lǣden','language name','laeden-u15-glossary-dat-sg','Lǣdene',{'case':'dative','number':'singular','spelling':'selected glossary long ǣ'},['U15-G-FB301'])
sense('laeden','Lǣden','language name','laeden-u15-source-sense','Latin, the language',['U15-G-FB301'])
for i,h,pos,sid,g,ev in [('on','on','preposition','on-u15-source-circumstance','in the circumstance of, here the day’s heat',['U15-G-EX16']),('aet','æt','preposition','aet-u15-proceeds','from; out of the proceeds of work',['U15-G-FB161']),('gewinn','gewinn','noun','gewinn-u15-labour','labour; work',['U15-G-FB161']),('aefter','æfter','preposition/conjunction','aefter-u15-after-clause-source','after, in æfter ðǣm ðe plus a finite clause',['U15-G-EX18','U15-G-FB104'])]:sense(i,h,pos,sid,g,ev)
sense('the-relative','ðe','relative/complementizer','the-u15-after-clause-source','clause marker in the supplied æfter ðǣm ðe temporal conjunction',['U15-G-EX18','U15-G-FB104'])

sup('U15-H-28-01','A hundredfold requital','Use him mid hundtēontigum forgolden bið, “he will be repaid a hundredfold,” with the finite verb last. The initial ǣlc has its own relative clause and is resumed by dative him; this is an impersonal recipient-passive scaffold. Mid hundtēontigum is taken from the checked Duties paragraph, then adapted to this passive. For mīnum naman means for the sake of my name. Neither the numeral phrase nor this resumed construction is a new general production system.','EX-IX-28-01',[bind('hundteontig','hundteontig-u15-source-dat-pl','hundteontig-u15-source-sense'),bind('for','for-invariant','for-u11-source')],['U15-G-FB159','U15-G-FB94','U15-G-FB102','U15-G-EX15'])
sup('U15-H-28-06','The ninth hour','Use nigoðan, the feminine accusative singular weak form of ninth, with tīd. The sixth-hour form siextan is already taught.','EX-IX-28-06',[bind('nigotha','nigotha-u15-acc-f-sg-source','nigotha-u15-source')],['U15-G-FB46','U15-G-FB48'])
sup('U15-H-28-07','The eleventh hour','Use ðā endleftan tīd for the eleventh hour. Endlefta follows Cook’s selected numeral spelling; this exact inflection is supplied.','EX-IX-28-07 EX-IX-28-11',[bind('endlefta','endlefta-u15-acc-f-sg-source','endlefta-u15-source')],['U15-G-FB46','U15-G-FB48'])
sup('U15-H-28-10','Evening and a speech addressee','Use ðā hit ǣfen geworden wæs, when it had become evening. Geworden is supplied from geweorðan; do not manufacture a new full system. Cweðan tō his gerēfan names the person addressed, with tō+dative.','EX-IX-28-10',[bind('geweorthan','geweorthan-past-participle','geweorthan-1'),bind('to','to-invariant','to-u14-speech-addressee-source')],['U15-G-EX15','U15-G-FB102'])
sup('U15-H-29-01','In the heat','On ðisses dæges hǣte means in this day’s heat: on+dative gives the circumstance, while the day is an independent genitive.','EX-IX-29-01',[bind('on','on-invariant','on-u15-source-circumstance')],['U15-G-EX16'])
sup('U15-H-29-07','Through him','The printed spelling ðurh is supplied beside previously taught þurh. Here ðurh hine means through/by way of him. The negation rejects the condemning purpose and contrasts it with saving; it does not deny that the Son was sent.','EX-IX-29-07',[bind('thurh','thurh-invariant-eth-source','thurh-u14-mediated-source')],['U15-G-EX16','U15-G-FB318'])
sup('U15-H-29-08','Of the Highest','Use ðæs Hēahstan as a masculine genitive singular divine title, of the Highest. This exact superlative title is supplied; the entire unused hēah comparison series is not assigned.','EX-IX-29-08',[bind('heah','heah-u15-highest-gen-source','heah-u15-highest-title')],['U15-G-FB43','U15-G-EX16'])
sup('U15-H-30-01','Swearing by a named standard','Use the exact spelling ðurh before the accusative oath standard; it is the supplied spelling of the taught through preposition. Hierusalem is the supplied place-name object.','EX-IX-30-01 EX-IX-30-02',[bind('thurh','thurh-invariant-eth-source','thurh-u15-oath'),bind('hierusalem','hierusalem-u15-source-acc','hierusalem-u15-source-sense')],['U15-G-EX17'])
sup('U15-H-30-05','The resumed subject and one of a set','Cook’s emphatic resumed sē is the supplied long-vowel nominative masculine singular. In ān of ðissum lǣstum bebodum, of+dative selects one from the set. The same long sē may be retained in30.6.','EX-IX-30-05 EX-IX-30-06',[bind('se','se-m-nom-sg-long-u12-source','se-that'),bind('of','of-invariant-dat-source','of-u15-source-partitive')],['U15-G-EX17','U15-G-FB90'])
sup('U15-H-30-07','In old times','On ealdum tīdum means in old times: temporal on takes the dative plural here. This exact supplied temporal expression is distinct from locating an object in a place.','EX-IX-30-07',[bind('on','on-invariant','on-u15-source-during')],['U15-G-EX17'])
sup('U15-H-30-09','Proceeds and an omitted infinitive','Use æt his gewinne for from his labour. In ðæt hē mæg, what he can, a recoverable action such as obtain is left unexpressed. Cook159–161’s argument supplies the actual æt…gewinne…mæge construction; do not add a new independent ellipsis rule or infer a full gewinn paradigm.','EX-IX-30-09',[bind('aet','aet-invariant-source','aet-u15-proceeds'),bind('gewinn','gewinn-dat-sg-source','gewinn-u15-labour')],['U15-G-FB161'])
sup('U15-H-30-12','Let them live','Use lǣt hīe libban, let them live: the accusative hīe is the understood subject of libban. This whole permission construction is scaffolded. Gif hīe magon expresses ability, not unwillingness; a defensible third-person optative translation is also valid language.','EX-IX-30-12',[],['U15-G-EX17','U15-G-FB103'])
sup('U15-H-31-03','A person taught to do something','Use hē wæs lǣred … tō dōnne. The taught person is the subject of the passive and the understood agent of doing. The infinitive’s object Godes willan stays accusative, with Godes genitive. This controlled infinitive frame is supplied.','EX-X-XI-31-03',[],['U15-G-EX17','U15-G-EX18','U15-G-FB101'])
sup('U15-H-31-04','From evil','Use fram yfele, from evil. Here yfele is the dative singular of the substantive noun yfel (Cook’s noun§47 entry), not the ordinary adjective dative yfelum; the exact phrase is supplied.','EX-X-XI-31-04',[bind('yfel','yfel-u15-substantive-dat-source','yfel-u15-noun-evil-source')],['U15-G-FB324','U15-G-EX18'])
sup('U15-H-31-06','May it come about','Use Geweorðe first, as Cook specifies: it is the supplied third-singular present subjunctive of the prefixed verb. Swā-swā means just as; retain the supplied hyphenated source expression.','EX-X-XI-31-06',[bind('geweorthan','geweorthan-pres-subj-3-sg','geweorthan-1'),bind('swa-swa','swa-swa-invariant-source','swa-swa-as-source')],['U15-G-EX18','U15-G-FB314'])
sup('U15-H-31-NAMES','Names and the glossary Latin spelling','The proper names Ælfred, Osburg, Æthelwulf and Asser are supplied; Ælfredes is the genitive needed in31.14. Lǣdene follows the selected glossary’s Lǣden; the actual Preface reading retains its printed Lædene without a long mark. No silent change to that source reading is made.','EX-X-XI-31-07 EX-X-XI-31-08 EX-X-XI-31-09 EX-X-XI-31-13 EX-X-XI-31-14',[bind('aelfred','aelfred-u15-source-nom-sg','aelfred-u15-source-sense'),bind('aelfred','aelfred-u15-source-gen-sg','aelfred-u15-source-sense'),bind('osburg','osburg-u15-source-nom','osburg-u15-source-sense'),bind('aethelwulf','aethelwulf-u15-source-nom','aethelwulf-u15-source-sense'),bind('asser','asser-u15-source-nom','asser-u15-source-sense'),bind('laeden','laeden-u15-glossary-dat-sg','laeden-u15-source-sense')],['U15-G-EX18','U15-G-FB301','U15-G-FB162'])
sup('U15-H-31-09','Hight','Hātte means is/was called, with past time supplied by the context. It is a special passive naming form, not the ordinary active preterite hēt. Use it unchanged in this supported sentence.','EX-X-XI-31-09',[bind('hatan','hatan-u15-hatte-source','hatan-u15-be-called')],['U15-G-FB297'])
sup('U15-H-31-10','Fifty-two years','Use twā and fīftig gēara. The already taught two is combined with supplied fīftig; the numeral expression may govern genitive plural gēara. This one number phrase is supplied, not the full higher-numeral system.','EX-X-XI-31-10',[bind('fiftig','fiftig-u15-source','fiftig-u15-source-sense')],['U15-G-FB46','U15-G-FB48','U15-G-FB90'])
sup('U15-H-31-11','After twelve years of age','Use æfter ðǣm ðe … wæs for after he was…. In twęlf wintra eald, twelve years old, wintra is genitive plural with the numeral and adjective of age. This finite after-clause and age phrase are supplied; twęlf preserves the earlier selected form.','EX-X-XI-31-11',[bind('aefter','aefter-invariant-source','aefter-u15-after-clause-source')],['U15-G-EX18','U15-G-FB90','U15-G-FB91','U15-G-FB104'])
sup('U15-H-31-12','A promise to whichever son','Use Engliscra lēoða, of English poems. The supported recipient expression is swā hwæðrum hiere twēgra suna swā hīe ǣrest leornode. Hwæðrum is dative singular because the whole expression is the recipient of promising, while its understood referent is the learner in the subordinate clause. This case attraction is supplied, not a general production target. Leornode here is prospective preterite subjunctive, identical in spelling to the indicative; it does not claim that he had already learned the book. Original independent free-choice exercises use nominative hwæðer and an explicit resumptive dative.','EX-X-XI-31-12',[bind('englisc','englisc-u15-source-gen-pl','englisc-u15-source-sense'),bind('leornian','leornian-u15-preterite-subj-3-sg-source','leornian-learn')],['U15-G-EX18','U15-G-FB53','U15-G-W240','U15-G-FB74','U15-G-EX46'])
for h in D['cook_support']:
 if h['support_id']=='U15-H-31-11':
  h['bindings'].append(bind('the-relative','the-relative-invariant','the-u15-after-clause-source'))
  h['text']+=' Treat ðe here as the supplied clause marker within the whole after-conjunction; it has no separate subject/object role inside the following clause.'
D['lemmas']=list(LM.values())
(O/'source-support.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(len(D['cook_support']),'visible Cook helps;',len(D['lemmas']),'bounded lemma records')
