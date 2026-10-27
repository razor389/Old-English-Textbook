"""Contextual source-token audit; ambiguity is resolved explicitly, never by first spelling match."""
import json,pathlib,re,copy,collections
P=pathlib.Path(__file__).parent;R=P.resolve().parents[2]
def read(p):return json.loads((R/p).read_text(encoding='utf8'))
def dump(n,x):(P/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
SRC=read('sources/audits/unit15-source/reading-source.json')['source_spans']
PATHS=['lexicon/entries.json','sources/audits/unit15-source/lexical-inventory.json','sources/audits/unit15-grammar/grammar-records-core.json','sources/audits/unit15-grammar/grammar-records-lexical.json','sources/audits/unit15-grammar/grammar-records-families.json']
L={};F={};S={};FO={};SO={}
for path in PATHS:
 for l in read(path)['lemmas']:
  L[l['lemma_id']]=l
  for f in l['forms']:F[f['form_id']]=(l['lemma_id'],f);FO[f['form_id']]=path
  for s in l['senses']:S[s['sense_id']]=(l['lemma_id'],s);SO[s['sense_id']]=path
SUP={};B={};SUPPATH='sources/audits/unit15-source/source-support-records.json'
spanmap={'D':SRC[0],'P':SRC[1],'R':SRC[2]}
def support_lemma(lid,head,pos):
 if lid not in SUP:SUP[lid]=dict(lemma_id=lid,display_headword=head,part_of_speech=pos,forms=[],senses=[],scope_note='Exact source forms and contextual meanings supplied for these reading passages only. No whole productive paradigm or independent recall is inferred.')
 return SUP[lid]
def addsense(lid,head,pos,sid,gloss,ev):
 l=support_lemma(lid,head,pos)
 if sid not in S:
  s=dict(sense_id=sid,gloss=gloss,knowledge_status='supplied',teaching_ids=[],evidence_refs=ev,scope_note=l['scope_note']);l['senses'].append(s);S[sid]=(lid,s);SO[sid]=SUPPATH
 return sid
def addform(lid,head,pos,fid,surface,parse,ev):
 l=support_lemma(lid,head,pos)
 if fid not in F:
  f=dict(form_id=fid,form=surface,analysis={'source_analysis':parse},knowledge_status='supplied',teaching_ids=[],evidence_refs=ev,evidence_basis='Exact inflected token on the personally inspected reading page; headword and meaning checked against cited vocabulary. No additional cells inferred.');l['forms'].append(f);F[fid]=(lid,f);FO[fid]=SUPPATH
 return fid
# Supplied source forms. The token itself is the primary morphological witness.
# span | positions | lemma | citation | POS | cell key | contextual gloss | parse | checked vocabulary pages
DATA='''D|6|wlanc|wlanc|adjective|dat-m-sg-weak|proud; wealthy, here the rich man addressed|substantival weak dative masculine singular|323
D|12|faesthafol|fæsthafol|adjective|nom-m-sg-strong|tenacious; withholding, with genitive of what is held|predicate nominative masculine singular|286
D|21|receleasian|rēcelēasian|verb|pret-2-sg|neglect; despise|preterite indicative second singular; genitive object|309
D|24|giefu|giefu|noun|gen-sg|gift|genitive feminine singular dependent on rēcelēasodest|296
D|32|afierran|āfierran|verb|pres-1-sg|remove; take away|present indicative first singular, future reference|275
D|35|selen|sęlen|noun|dat-sg|bounty; bestowal|dative feminine singular after fram|311
D|45|woruldlif|woruldlīf|noun|dat-sg|worldly life|dative neuter singular after on|323
D|50|gethencean|geðęncean|verb|inf|remember; bear in mind|plain infinitive after noldest|295
D|55|aeghwilc|ǣghwilc|adjective|dat-m-sg|each; every|strong dative masculine singular agreeing with męnn|274
D|59|daed|dǣd|noun|acc-sg|deed|endingless accusative feminine singular|282
D|65|gedon|gedōn|verb|pres-3-sg|do; perform|present indicative third singular|291
D|67|hundteontig|hundtēontig|numeral|dat-pl|a hundredfold; a hundred in return|dative plural after mid in fixed repayment expression|300
D|78|cwethan|cweðan|verb|ge-past-part|said|uninflected ge-prefixed past participle in passive|159
D|80|secgan|sęcgan|verb|ge-past-part|said|uninflected ge-prefixed past participle, pleonastic with gecweden|159
D|81|swa-hwaet-swa|swā-hwæt-swā|pronoun|acc-n-sg|whatsoever; whatever|free-choice relative pronoun, accusative neuter object|314
D|91|simle|simle|adverb|invariant|always|adverb|312
D|99|gesellan|gesęllan|verb|pres-1-sg|give|present indicative first singular, future reference|294
D|101|dream|drēam|noun|acc-sg|joy; bliss|accusative masculine singular|283
P|1|aelfred|Ælfred|proper_noun|nom-sg|Alfred|nominative masculine singular personal name|162
P|4|wealhstod|wealhstōd|noun|nom-sg|interpreter; translator|predicate nominative masculine singular|321
P|10|boclaeden|Bōclæden|noun|dat-sg|book-Latin; Latin|dative neuter singular after of|279
P|12|englisc-language|Englisc|noun|acc-sg|English, the language|accusative language name after on, goal of translation|285
P|13|wendan|węndan|verb|pret-3-sg|translate|preterite indicative third singular|321
P|26|andgiet|andgiet|noun|acc-sg|meaning; sense|accusative neuter singular object of sętte|275
P|28|andgiet|andgiet|noun|dat-sg|meaning; sense|dative neuter singular after of|275
P|33|sweotole|sweotole|adverb|superl|most clearly|superlative adverb|315
P|35|andgietfullice|andgietfullice|adverb|superl|most intelligibly|superlative adverb|276
P|36|gereccan|geręccan|verb|inf|explain; render|plain infinitive after meahte|294
P|40|mislic|mislic|adjective|dat-f-pl-strong|various|strong dative feminine plural|305
P|42|manigfeald|manigfeald|adjective|dat-f-pl-strong|manifold; many|strong dative feminine plural|304
P|43|woruldbisgu|woruldbisgu|noun|dat-pl|worldly occupations; cares|dative feminine plural after for|323
P|54|bisgian|bisgian|verb|pret-3-pl|occupy; trouble|preterite indicative third plural; syncopated source form|279
P|56|bisgu|bisgu|noun|nom-pl|occupations; cares|nominative feminine plural subject|279
P|58|wesan|wesan|verb|sind-pres-3-pl|are|present indicative third plural source variant sind|312
P|60|earfothrime|earfoðrīme|adjective|nom-f-pl|hard to count; innumerable|predicate strong nominative feminine plural|284
P|68|becuman|becuman|verb|pret-3-pl|come upon; befall|preterite indicative third plural|277
P|71|underfon|underfōn|verb|past-part|receive; take charge of|past participle in anterior construction hæfde underfangen|319
P|80|geleornian|geleornian|verb|past-part|learn; study|past participle in hæfde geleornod|292
P|83|laeden|Læden|noun|dat-sg|Latin, the language|dative neuter singular language name after of|301
P|85|englisc|Englisc|adjective|dat-n-sg|English|strong dative neuter singular agreeing with spelle|285
P|86|spell|spell|noun|dat-sg|account; discourse|dative neuter singular after tō|313
P|92|eft|eft|adverb|invariant|again; afterwards|adverb|284
P|114|lystan|lystan|verb|pres-subj-3-sg|please; be a desire to|present subjunctive third singular impersonal; understood experiencer accusative from ǣlcne|303
P|123|witan-blame|wītan|verb|pres-subj-3-sg|blame; censure|present subjunctive third singular, governed request coordinated with gebidde|323
P|127|rihtlice|rihtlīce|adverb|comparative|more correctly|comparative adverb|309
P|128|ongietan|ongietan|verb|pres-subj-3-sg|understand|present subjunctive third singular in condition|308
P|132|for-tham-the|for-ðām-ðe|conjunction|invariant|because|causal conjunction|288
P|138|andgiet|andgiet|noun|gen-sg|understanding|genitive neuter singular dependent on mǣðe|275
P|139|maeth|mǣð|noun|dat-sg|measure; capacity|dative feminine singular after be|304
P|143|aemetta|ǣmetta|noun|dat-sg|leisure; available time|dative masculine singular after be|274
P|150|thaet-thaet|ðæt-ðæt|pronoun|acc-n-sg|that which; what|demonstrative accusative neuter + relative accusative neuter|162
R|2|aelmihtig|ælmihtig|adjective|voc-m-sg-weak|almighty|weak masculine singular in direct address|274
R|6|wealdend|wealdend|noun|voc-sg|Ruler|nominative/vocative masculine singular title|321
R|24|sanctus-latin|Sanctus|foreign_adjective|gen-f-sg|Saint; holy|Latin genitive feminine singular accompanying Marian|163
R|25|maria-name|Maria|proper_noun|gen-context|Mary|source Marian used as genitive; mixed treatment of foreign names, not regular Latin genitive|163,38
R|26|maegthhad|mægðhād|noun|dat-sg|maidenhood; virginity|dative masculine singular after for|304
R|29|sanctus-latin|Sanctus|foreign_adjective|gen-m-sg|Saint; holy|Latin genitive masculine singular|163
R|30|michael-name|Michael|proper_noun|gen-context|Michael|genitive personal name, vernacular -es with Latin Sancti|163,38
R|36|halig|hālig|adjective|gen-pl-substantival|saints; holy ones|substantival genitive plural in -ena|163
R|37|lufe|lufe|noun|dat-sg|love|weak feminine dative singular after for|303
R|39|he|hē|pronoun|hiera-gen-pl|their|third-person genitive plural source spelling hīera|299
R|40|earnung|earnung|noun|dat-pl|merits; good services|dative feminine plural coordinated under for|284
R|44|gewissian|gewissian|verb|pres-subj-2-sg|guide; direct|present subjunctive second singular in requested ðæt clause|296
R|48|awyrcean|āwyrcean|verb|pret-1-sg|do; perform, here deserve by one's conduct|preterite indicative first singular with tō ðē|277
R|52|gewissian|gewissian|verb|imp-2-sg|guide; direct|imperative second singular|296
R|61,78|thearf|ðearf|noun|dat-sg|benefit; good; need|dative feminine singular after tō, with dependent sāwle|317
R|68|gestathelian|gestaðelian|verb|imp-2-sg|establish; make steadfast|imperative second singular source -e- variant|295
R|80|gestrangian|gestrangian|verb|imp-2-sg|strengthen|imperative second singular|295
R|87|afierran|āfierran|verb|imp-2-sg|remove; take away|imperative second singular|275
R|91|ful|fūl|adjective|acc-f-sg-weak|foul|weak accusative feminine singular|289
R|92|galnes|gālnes|noun|acc-sg|lust|accusative feminine singular|290
R|97|gescieldan|gescieldan|verb|imp-2-sg|shield; protect|imperative second singular|294
R|101|witherwinna|wiðerwinna|noun|dat-pl|adversaries|dative masculine plural after wið|323
R|102|gesewenlic|gesewenlic|adjective|dat-m-pl-strong|visible|strong dative masculine plural|294
R|104|ungesewenlic|ungesewenlic|adjective|dat-m-pl-strong|invisible|strong dative masculine plural|319
R|106|taecan|tǣcan|verb|imp-2-sg|teach; show|imperative second singular|316
R|116|inweardlice|inweardlīce|adverb|invariant|fervently; wholeheartedly|adverb|301
R|118|toforan|tōforan|preposition|invariant|before; above all|preposition with dative of comparison or preference|316
R|122|claene|clǣne|adjective|dat-n-sg-strong|pure; clean|strong dative neuter singular agreeing with geðance|281
R|123|gethanc|geðanc|noun|dat-sg|thought; mind|dative neuter singular after mid|295
R|126|claene|clǣne|adjective|dat-m-sg-strong|pure; clean|strong dative masculine singular agreeing with līchaman|281
R|132|scieppend|scieppend|noun|nom-sg|Creator|predicate nominative masculine singular title|311
R|137|fultum|fultum|noun|nom-sg|help; support|predicate nominative masculine singular, address to God|289
R|141|treownes|trēownes|noun|nom-sg|trust; confidence|predicate nominative feminine singular|316
R|144|tohopa|tōhopa|noun|nom-sg|hope|predicate nominative masculine singular|316
R|147|lof|lof|noun|nom-sg|praise|nominative masculine singular subject|303
R|152,153,154|a-ever|ā|adverb|invariant|ever; always|adverb repeated for intensification|163
R|158|aeghwilc|ǣghwilc|adjective|dat-m-sg|any; every|strong dative masculine singular agreeing with ęnde|274
R|159|ende|ęnde|noun|dat-sg|end|dative masculine singular after būtan|285
R|160|amen|Amen|interjection|invariant|Amen|liturgical closing word|163'''
for line in DATA.splitlines():
 code,indices,lid,head,pos,key,gloss,parse,pages=line.split('|');span=spanmap[code]
 ev=list(dict.fromkeys(['U15-FB-P'+str(span['printed_pages'][0])]+['U15-FB-P'+p for p in pages.split(',')]))
 for i in map(int,indices.split(',')):
  surf=span['learner_text'].split()[i-1].strip('.,;:!?“”‘’()')
  fid=addform(lid,head,pos,f'{lid}-u15-source-{key}',surf,parse,ev)
  sid=addsense(lid,head,pos,f'{lid}-u15-source-'+('understanding' if lid=='andgiet' and key=='gen-sg' else 'sense'),gloss,ev)
  B[(code,i)]=(fid,sid)
# Explicit contextual selections for all morphologically ambiguous existing tokens.
CHOICES={
'D':'''2=haelend-nom-sg 3=cwethan-pret-3-sg 4=to-preposition-dative-invariant 5=se-m-dat-sg 8=hwy-invariant 9=wesan-pret-2-sg 13=min-poss-gen-n-pl-strong 14=god-goods-gen-pl 15=the-relative-invariant 17=thu-dat-sg 18=sellan-pret-1-sg 19=to-preposition-dative-invariant 23=se-f-gen-sg 25=the-relative-invariant 27=thu-dat-sg 28=giefan-pret-1-sg 30=thu-acc-sg 34=min-poss-dat-f-sg-strong 36=the-relative-invariant 38=thu-dat-sg 39=forgiefan-pret-1-sg 40=thonne-invariant 48=willan-pret-2-sg-negative 51=thaet-conjunction-invariant 53=willan-pres-1-sg 56=mann-dat-sg 57=an-acc-f-sg-strong 58=god-adjective-acc-f-sg-strong 60=the-relative-invariant 62=min-poss-dat-m-sg-strong 63=nama-dat-sg 64=mann-nom-sg 66=mid-invariant-source 69=he-n-acc-sg 70=he-m-dat-sg 73=he-n-nom-sg 76=min-poss-dat-n-sg-strong 83=sellan-pres-2-pl 84=an-dat-m-sg-strong 86=min-poss-dat-m-pl-strong 87=se-all-dat-pl 88=lytel-superl-dat-m-pl-weak 90=he-n-acc-sg 92=ic-dat-sg 93=sellan-pres-2-pl 96=thu-dat-pl 98=se-n-dat-sg''',
'P':'''2=cyning-nom-sg 3=wesan-pret-3-sg 5=thes-gen-f-sg 6=boc-gen-sg 8=he-f-acc-sg 21=settan-pret-3-sg 22=word-acc-sg 31=he-n-acc-sg 32=tha-adverb-invariant 37=magan-pret-3-sg 39=se-all-dat-pl 44=the-relative-invariant 48=ge-conjunction-source 51=ge-conjunction-source 53=lichama-dat-sg 55=se-all-nom-pl 57=ic-dat-pl 61=the-relative-invariant 63=he-m-gen-sg 66=se-all-acc-pl 67=rice-acc-pl 69=the-relative-invariant 72=habban-pret-3-sg 75=tha-conjunction-invariant 77=thes-acc-f-sg 78=boc-acc-sg 79=habban-pret-3-sg 88=tha-adverb-invariant 89=gewyrcean-pret-3-sg 91=he-f-acc-sg 93=to-preposition-dative-invariant 94=leoth-dat-sg 106=nama-dat-sg 110=the-relative-invariant 111=thes-acc-f-sg 112=boc-acc-sg 115=thaet-conjunction-invariant 119=gebiddan-pres-subj-3-sg 121=he-m-dat-sg 126=he-n-acc-sg 129=thonne-invariant 131=magan-pret-3-sg 133=aelc-nom-m-sg-strong 134=mann-nom-sg 135=sculan-pres-3-sg 137=he-m-gen-sg 142=he-m-gen-sg 145=se-n-acc-sg 149=don-infinitive 84=to-preposition-dative-invariant''',
'R':'''1=dryhten-nom-sg 3=god-nom-sg 7=eall-gen-f-pl-strong 8=gesceaft-gen-pl 10=biddan-pres-1-sg 11=thu-acc-sg 13=thin-poss-dat-f-sg-strong 14=micel-dat-f-sg-weak 15=mildheortnes-dat-sg-source 18=se-f-gen-sg 19=halig-gen-f-sg-weak 20=rod-gen-sg 31=gehiersumnes-dat-sg 34=eall-gen-m-pl-strong 35=thin-poss-gen-m-pl-strong 41=thaet-conjunction-invariant 43=ic-acc-sg 46=thonne-invariant 49=to-preposition-dative-invariant 50=thu-dat-sg 53=ic-acc-sg 54=to-preposition-dative-invariant 55=thin-poss-dat-m-sg-strong 56=willa-dat-sg 58=to-preposition-dative-invariant 59=min-poss-gen-f-sg-strong 60=sawol-gen-sg 63=thonne-invariant 65=self-nom-m-sg-strong 66=cunnan-present-subj-1-sg 69=min-poss-acc-n-sg-strong 71=to-preposition-dative-invariant 72=thin-poss-dat-m-sg-strong 73=willa-dat-sg 75=to-preposition-dative-invariant 76=min-poss-gen-f-sg-strong 77=sawol-gen-sg 81=ic-acc-sg 83=se-m-gen-sg 85=costnung-dat-pl 89=ic-dat-sg 90=se-f-acc-sg 94=aelc-acc-f-sg-strong 95=unrihtwisnes-acc-sg 98=ic-acc-sg 100=min-poss-dat-m-pl-strong 107=ic-dat-sg 109=willa-acc-sg 110=to-before-inflected-infinitive 112=thaet-conjunction-invariant 114=magan-present-subj-1-sg 115=thu-acc-sg 119=eall-dat-n-pl-strong 121=mid-invariant-source 125=mid-invariant-source 127=lichama-dat-sg 131=min-poss-nom-m-sg-strong 134=min-poss-nom-m-sg-strong 135=aliesend-nom-sg 136=min-poss-nom-m-sg-strong 138=min-poss-nom-f-sg-strong 140=min-poss-nom-f-sg-strong 143=min-poss-nom-m-sg-strong 145=wesan-present-subj-3-sg 146=thu-dat-sg 149=wuldor-nom-sg-u13-source 155=to-preposition-dative-invariant 156=woruld-dat-sg 157=butan-invariant'''}
SELECT={(c,int(k)):v for c,text in CHOICES.items() for k,v in (x.split('=') for x in text.split())}
SELECT.update({('D',54):'forgieldan-infinitive',('D',71):'forgieldan-pres-1-sg',('P',47):'aegther-u15-invariant'})
# Sense decisions: same surface or already known lemma never establishes a new sense.
SENSESELECT={
 ('D',88):'lytel-superl-u15-rank',
 ('D',64):'mann-u11-source',
 ('D',54):'forgieldan-u15-pay',('D',71):'forgieldan-u15-pay',('P',47):'aegther-u15-both',
 ('R',111):'wyrcean-work',
 ('P',72):'habban-perfect',('P',79):'habban-perfect',
 ('D',74):'wesan-passive',('P',17):'wesan-passive',('P',99):'wesan-passive',('P',63):'he-possessor',('P',137):'he-possessor',('P',142):'he-possessor',
 ('D',4):'to-u14-speech-addressee-source',('D',7):'for-u15-source-why',('D',19):'to-u15-source-why',('D',20):'hwa-u15-source-why',('D',40):'thonne-then-source',('D',44):'on-u15-source-worldly-life',('D',46):'for-u15-source-why',('D',47):'hwa-u15-source-why',('D',48):'willan-refuse',('D',61):'for-u11-source',('D',72):'swa-comparative-as',('D',75):'on-1',('D',85):'of-u15-source-partitive',('D',97):'with-u15-source-exchange',('D',98):'se-that',
 ('P',9):'of-u11-source',('P',11):'on-into-goal',('P',14):'swa-comparative-as',('P',18):'gedon-u15-source-arrangement',('P',23):'be-u15-source-word-by-word',('P',27):'of-u15-source-correspondence',('P',29):'swa-swa-as-source',('P',38):'for-u15-source-cause',('P',48):'ge-paired-source',('P',49):'on-respect',('P',51):'ge-paired-source',('P',52):'on-respect',('P',62):'on-u15-source-during',('P',65):'on-into-goal',('P',74):'theah-u15-source-nevertheless',('P',82):'of-u11-source',('P',84):'to-u15-source-translation-result',('P',87):'gewendan-u15-source-translate',('P',93):'to-u15-source-translation-result',('P',95):'swa-swa-as-source',('P',98):'gedon-u15-source-arrangement',('P',104):'for-u11-source',('P',117):'for-beneficiary',('P',129):'thonne-than',('P',136):'be-according-source',('P',141):'be-according-source',('P',145):'se-free-relative-what-source',
 ('R',4):'wyrhta-u15-source-maker',('R',10):'biddan-beseech-person',('R',12):'for-u15-source-appeal',('R',17):'for-u15-source-appeal',('R',23):'for-u15-source-appeal',('R',28):'for-u15-source-appeal',('R',33):'for-u15-source-appeal',('R',41):'thaet-conjunction-1',('R',46):'thonne-than',('R',49):'to-u15-source-directed-conduct',('R',54):'to-u15-source-conformity',('R',58):'to-u15-source-benefit',('R',63):'thonne-than',('R',71):'to-u15-source-conformity',('R',75):'to-u15-source-benefit',('R',112):'thaet-purpose',('R',121):'mid-u13-manner-source',('R',125):'mid-u13-manner-source',('R',155):'to-u15-source-eternity',('R',157):'butan-u13-without'}
SENSESELECT.update({('D',97):'with-u15-exchange',('P',128):'ongietan-u15-understand'})
EXTRAS=[
 ('for','for','preposition','why','for what reason; why, in for hwȳ/hwon'),('to','tō','preposition','why','for what purpose; why, in tō hwon'),('hwa','hwā','pronoun','why','what (reason), instrumental hwon in fixed why expressions'),('on','on','preposition','worldly-life','in worldly life, temporal/situational expression'),('of','of','preposition','partitive','of; out of a set, selecting one of the least'),('with','wið','preposition','exchange','in return for, with dative consideration'),('gedon','gedōn','verb','arrangement','made; arranged, describing the present form of the translation'),('be','be','preposition','word-by-word','word by word, literal correspondence in word be worde'),('of','of','preposition','correspondence','from; corresponding to, sense for sense'),('for','for','preposition','cause','because of, with dative of hindering circumstance'),('on','on','preposition','during','during, with dative time'),('theah','ðēah','adverb','nevertheless','nevertheless; yet (independent adverb)'),('to','tō','preposition','translation-result','into; to, result in a new linguistic/literary form'),('gewendan','gewęndan','verb','translate','translate; turn from one language into another'),('wyrhta','wyrhta','noun','maker','Maker; Creator (not the previously taught workman sense)'),('for','for','preposition','appeal','by; for the sake of, naming grounds of appeal in the prayer'),('to','tō','preposition','directed-conduct','towards; in relation to the person to whom conduct is directed'),('to','tō','preposition','conformity','to; in accordance with, a will as the goal of guidance'),('to','tō','preposition','benefit','for; to the benefit of'),('to','tō','preposition','eternity','for ever, in fixed tō worulde')]
for lid,head,pos,key,gloss in EXTRAS:addsense(lid,head,pos,lid+'-u15-source-'+key,gloss,['U15-FB-P159','U15-FB-P162','U15-FB-P163'])
def stat(rec,path):return ('previously_taught' if rec.get('production_taught_in') else 'previous_recognition' if rec.get('recognition_taught_in') else 'supplied') if path=='lexicon/entries.json' else rec.get('knowledge_status','supplied')
def default_sense(lid):
 if lid=='ic':return 'ic-personal'
 if lid=='mann':return 'mann-1'
 if lid in ['word','micel','swithe']:return {'word':'word-1','micel':'micel-1','swithe':'swithe-positive'}[lid]
 if lid=='wel':return 'wel-comparative'
 if lid=='don':return 'don-1'
 if lid=='sprecan':return 'sprecan-1'
 if lid in ['wesan','he','sellan','an']:return {'wesan':'wesan-be','he':'he-1','sellan':'sellan-give','an':'an-1'}[lid]
 ss=[(sid,s) for sid,(l,s) in S.items() if l==lid]
 good=[sid for sid,s in ss if s.get('production_taught_in') or (SO[sid]!='lexicon/entries.json' and s.get('knowledge_status')=='new_production')]
 if len(good)==1:return good[0]
 if len(ss)==1:return ss[0][0]
 # Fixed default is permitted only for contextual senses reviewed below; caller prints ambiguity otherwise.
 DEFAULT={'se':'se-the','swa':'swa-1','to':'to-destination','on':'on-1','for':'for-u11-source','with':'with-against','thaet-conjunction':'thaet-conjunction-1','mid':'mid-by-means','the-relative':'the-relative-which','willan':'willan-1','of':'of-u11-source','biddan':'biddan-1','gewyrcean':'gewyrcean-1','ge-conjunction':'ge-paired-source','gedon':'gedon-do-make','be':'be-according-source','swa-swa':'swa-swa-as-source','thonne':'thonne-then-source','wela':'wela-u14-source','eall':'eall-all','an':'an-one','lice':'lice-1','thing':'thing-1','haelend':'haelend-1','god-adjective':'god-adjective-1','mildheortnes':'mildheortnes-mercy'}
 if lid in DEFAULT:return DEFAULT[lid]
 raise ValueError(('SENSE AMBIGUITY',lid,[(i,s['gloss']) for i,s in ss]))
rows=[];errors=[]
for code,span in spanmap.items():
 # Preserve exact source line provenance while rejoining four typographic split words.
 pieces=[]
 for line in span['source_lines']:
  for word in re.sub(r'\[\d+\]','',line['source_with_note_markers']).split():
   if pieces and pieces[-1]['source_surface'].endswith('-'):
    pieces[-1]['source_surface']=pieces[-1]['source_surface'][:-1]+word;pieces[-1]['source_line_ids'].append(line['source_line_id'])
   else:pieces.append(dict(source_surface=word,source_line_ids=[line['source_line_id']],printed_page=line['printed_page'],editorial_line=line['editorial_line'],pdf_page_one_based=line['pdf_page_one_based']))
 assert ' '.join(x['source_surface'] for x in pieces)==span['learner_text']
 for i,piece in enumerate(pieces,1):
  surf=piece['source_surface'].strip('.,;:!?“”‘’()');key=(code,i)
  if key in B:fid,sid=B[key]
  else:
   candidates=[fid for fid,(l,f) in F.items() if f['form'].lower()==surf.lower()]
   fid=SELECT.get(key)
   if not fid and len(candidates)==1:fid=candidates[0]
   if not fid:errors.append((code,i,surf,candidates));continue
   lid,f=F[fid];sid=SENSESELECT.get(key) or default_sense(lid)
  if key in SENSESELECT:sid=SENSESELECT[key]
  lid,f=F[fid];slid,s=S[sid]
  assert lid==slid,(key,fid,sid,lid,slid)
  assert f['form'].lower()==surf.lower(),(key,surf,fid,f['form'])
  row=dict(token_id=span['source_span_id']+f'-T{i:03}',source_span_id=span['source_span_id'],token_index_one_based=i,lemma_id=lid,form_id=fid,sense_id=sid,form=f['form'],form_status=stat(f,FO[fid]),sense_status=stat(s,SO[sid]),analysis=copy.deepcopy(f.get('contextual_analysis',f.get('analysis'))),gloss=s.get('contextual_gloss',s['gloss']),form_record_origin=FO[fid],sense_record_origin=SO[sid],evidence_refs=list(dict.fromkeys(f.get('evidence_refs',[])+s.get('evidence_refs',[])+['U15-FB-P'+str(piece['printed_page'])])),feature_ids=[])
  row.update(piece)
  for kind,record,path in [('form',f,FO[fid]),('sense',s,SO[sid])]:row['prior_'+kind+'_scope']={k:record.get(k) for k in ['production_taught_in','recognition_taught_in','supplied_in','coverage_contract']} if path=='lexicon/entries.json' else record.get('prior_scope')
  if '-' in surf:row['component_tokens']=[dict(component_index=j,source_component=x,scope_note='Component spelling retained; the full lexical construction is the binding and must not be interpreted as independently taught from components alone.') for j,x in enumerate(surf.split('-'),1)]
  rows.append(row)
if errors:raise ValueError(('UNBOUND FORM AMBIGUITIES',errors))
assert len(rows)==415
# All prior supplied dependencies are explicitly carried forward at exact IDs with fresh local support.
for row in rows:
 for kind,idkey,table,orig in [('forms','form_id',F,FO),('senses','sense_id',S,SO)]:
  if row['form_status' if kind=='forms' else 'sense_status']!='supplied':continue
  rid=row[idkey];lid,rec=table[rid]
  l=support_lemma(lid,L.get(lid,{}).get('display_headword',lid),L.get(lid,{}).get('part_of_speech','source'))
  if not any(x[idkey]==rid for x in l[kind]):
   new={k:copy.deepcopy(v) for k,v in rec.items() if k not in ['records_by_chapter','reviewed_chapters','assessed_in','used_in_tasks']};new['prior_scope']=row['prior_'+('form' if kind=='forms' else 'sense')+'_scope'];new['knowledge_status']='supplied';new['evidence_refs']=row['evidence_refs'];l[kind].append(new)
usedforms={r['form_id'] for r in rows};usedsenses={r['sense_id'] for r in rows}
for l in SUP.values():
 l['forms']=[f for f in l['forms'] if f['form_id'] in usedforms]
 l['senses']=[s for s in l['senses'] if s['sense_id'] in usedsenses]
SUP={k:l for k,l in SUP.items() if l['forms'] or l['senses']}
helps=[]
for lid in sorted({r['lemma_id'] for r in rows if r['form_status']=='supplied' or r['sense_status']=='supplied'}):
 selected=[r for r in rows if r['lemma_id']==lid and (r['form_status']=='supplied' or r['sense_status']=='supplied')]
 hid='U15-READ-LEX-'+lid.upper();forms=list(dict.fromkeys(r['form'] for r in selected));gloss=list(dict.fromkeys(r['gloss'] for r in selected))
 helps.append(dict(support_id=hid,kind='lexical_help',lemma_id=lid,headword=SUP.get(lid,L.get(lid,{})).get('display_headword',lid),forms=forms,glosses=gloss,token_ids=[r['token_id'] for r in selected],form_ids=list(dict.fromkeys(r['form_id'] for r in selected)),sense_ids=list(dict.fromkeys(r['sense_id'] for r in selected)),text='; '.join(forms)+' — '+'; '.join(gloss),scope='Visible local help; these forms/senses are not assessed for independent recall.'))
 for r in selected:r.setdefault('support_ids',[]).append(hid)
dump('source-support-records.json',dict(schema_version=1,lemmas=list(SUP.values()),scope='Supplied exact source records; prior milestones checked against all14 active contracts and actual registers. No productive whole paradigm inferred.',reading_bindings=[dict(source_span_id=r['source_span_id'],token_index_one_based=r['token_index_one_based'],lemma_id=r['lemma_id'],form_id=r['form_id'],sense_id=r['sense_id']) for r in rows if r['form_status']=='supplied' or r['sense_status']=='supplied']))
dump('reading-token-ledger.json',dict(schema_version=1,tokenization='Whitespace source words, punctuation retained; four typographic line divisions rejoined. Source lexical hyphens retained and component spellings recorded.',count=len(rows),span_counts={s['source_span_id']:s['word_count'] for s in SRC},tokens=rows,unresolved=[]))
dump('reading-support.json',dict(schema_version=1,lexical_help=helps,grammar_help=[],source_apparatus='reading-apparatus.json',policy='Every supplied form or contextual sense is exposed in lexical help. Construction orientation is in reading-constructions.json, separately from the complete original apparatus.'))
print(json.dumps(dict(tokens=len(rows),supplied_tokens=sum(r['form_status']=='supplied' or r['sense_status']=='supplied' for r in rows),support_lemmas=len(SUP),help_groups=len(helps))))
