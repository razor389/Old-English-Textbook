from pathlib import Path
from collections import Counter
import json,re,unicodedata
C=json.loads(Path('chapters/ch18/coverage.json').read_text(encoding='utf8'))
T={t['teaching_id']:t for t in C['teaching_records']}
L={l['lemma_id']:l for l in C['lexical_inventory']}
F={f['feature_id']:f for f in C['grammar_inventory']}
S={s['sense_id']:(l,s) for l in C['lexical_inventory'] for s in l['senses']}
M=C['display_plan']['matrices'];seen=set();out=[];routes=[]
def add(s=''):out.append(s)
def marks(ids,place):
 for tid in ids:
  if tid in T and tid not in seen:
   add('<!-- teaching: '+tid+' -->\n');seen.add(tid);routes.append({'teaching_id':tid,'location':place})
def fm(fid,place):
 if fid in F:marks(F[fid].get('teaching_ids',[]),place)
def hm(fids,sids,place):
 for t in T.values():
  if t['kind'] in ['visible_local_lexical_help','bounded_lexical_sense'] and set(t.get('sense_ids',[]))&set(sids):
   if t['kind']=='bounded_lexical_sense' or not fids or set(t.get('form_ids',[]))&set(fids):marks([t['teaching_id']],place)
def analysis(a):
 vals=[];names={'nom':'nominative','gen':'genitive','dat':'dative','acc':'accusative','ins':'instrumental','voc':'direct address','sg':'singular','pl':'plural','m':'masculine','f':'feminine','n':'neuter','pres':'present','pret':'preterite','ind':'indicative','subj':'subjunctive','imp':'imperative'}
 for k in ['mood','tense','person','case','gender','number','declension','verb_form','infinitive_type']:
  v=a.get(k)
  if v is None:continue
  v={1:'first person',2:'second person',3:'third person'}.get(v,str(v)) if k=='person' else names.get(str(v),str(v)).replace('_',' ')
  if v not in vals:vals.append(v)
 if a.get('government'):vals.append('governs '+names.get(a['government'],a['government']))
 return ', '.join(vals)
def table(m):
 add('<!-- table: '+m['matrix_id']+' -->\n');add('| '+' | '.join(m['headers'])+' |');add('| '+' | '.join(['---']*len(m['headers']))+' |')
 for row in m['rows']:add('| '+' | '.join(row)+' |')
 add()
def vocabulary(lid,place):
 l=L[lid]
 for s in l['senses']:
  if s['knowledge_status'] in ['new_production','new_recognition'] and any(t not in seen for t in s.get('teaching_ids',[])):
   marks(s['teaching_ids'],place);add('**'+l['display_headword']+'** — '+s.get('contextual_gloss',s['gloss'])+'.\n')
def clean(s):
 s=s.replace('newly productive','taught for production').replace('newly taught','newly presented').replace('selected ordinary frame','selected ordinary construction').replace('independent recall is claimed','independent recall is required')
 s=re.sub(r'(?<=[A-Za-z])(?=\d)', ' ',s)
 s=re.sub(r'(?<=\d)(?=[A-Za-z])',' ',s)
 s=s.replace('needs no English to','needs no separate tō').replace('Supply these reference links explicitly','Keep the people and gifts distinct')
 s=s.replace('actual prior ','earlier ').replace('weakII','weak class II').replace('weakI ','weak class I ')
 s=s.replace('The nominal/source packet supplies the exact silver-adjective form with evidence; no independent adjective system is inferred','The exact silver adjective is supplied; its remaining forms are not assigned here')
 s=s.replace('Keep the earlier cleopian records unchanged; the marked source variant is not silently substituted into earlier paradigms','This marked source variant is supplied locally; retain the earlier spelling in its own paradigm')
 s=s.replace('The name phrase is supplied by the nominal/source packet','The exact name phrase is supplied')
 s=s.replace('not the lexical identity here','a different verb here').replace('without an unassigned intransitive habban perfect','without adding a habban perfect')
 s=s.replace('Our model is a declared lexical adaptation with bēodan:','The supplied expression uses bēodan:')
 s=s.replace('omit the English to as instructed rather than adding an unsolicited ofer','use the bare dative for the people, following the instruction to omit a separate equivalent of English to')
 s=re.sub(r'BT Supplement 646[^.]*\.', '',s)
 s=re.sub(r'(?<=[.;])(?=\d{2}\.)',' ',s)
 s=re.sub(r' {2,}',' ',s)
 return s
noun={
'sacc':'Masculine; stem sacc-. Use the ordinary strong masculine endings.',
'assa':'Masculine; weak stem ass-. All oblique singular cases and nominative/accusative plural are assan; genitive plural is assena and dative plural assum.',
'hunig':'Neuter; stem hunig-. Retain the medial vowel before endings. This table gives the complete singular of the mass meaning honey.',
'aecern':'Neuter; stem æcern-. The selected nominative/accusative plural is æcernu. Retain the medial vowel in the other cases: final rn makes the second syllable heavy. Preserve unmarked æ.',
'hwaete':'Masculine; stem hwǣt-. Nominative and accusative singular retain final -e. This table gives the complete singular of wheat.',
'laefel':'Masculine; stem læfel-. Retain medial e before endings because the first syllable is short. Preserve unmarked æ.',
'sceawere':'Masculine; stem scēawer-. Replace the dictionary form’s final e with the required ending; nominative/accusative plural is scēaweras.',
'elcung':'Feminine; stem ęlcung-. This table selects -e in the oblique singular. The -ung class also admits -a variants. Only abstract singular delay is required.',
'gebeorscipe':'Masculine; stem gebēorscip-. Nominative and accusative singular retain -e; the plural follows the ordinary strong masculine pattern.',
'sarnes':'Feminine; oblique stem sārness-. Double final s and retain the preceding e: sārnesse. Only abstract singular grief is required.',
'ealdor-chief':'Masculine; ealdor has the oblique stem ealdr-. Lose the unstressed vowel before an ending: ealdres, ealdre, ealdras.',
'thearf':'Feminine; stem ðearf-. This unit uses the abstract singular benefit or good; the oblique singular is ðearfe.',
'theow-servant':'Masculine; strong stem ðēow-. Distinguish this noun from the earlier weak ðēowa. Its selected genitive plural is ðēowa, while the weak noun has ðēowena. The complete phrase in the reading has local help.',
'hunger':'Masculine; hunger has the oblique stem hungr-. Retain hunger without an ending; use hungres and hungre before endings. This table gives the mass singular famine or hunger.',
'sith':'Masculine; stem sīð-. These are the four ordinary cases. The second-time expression in 44.7 is instrumental and is supplied separately; its noun is not dative merely because both end in -e.',
'lac':'Neuter; stem lāc-. The long vowel makes the stem heavy, so nominative/accusative plural has no ending.',
'faet':'Neuter; retain æ throughout the singular and use a throughout the plural: fatu, fata, fatum. The short stem takes -u in nominative/accusative plural.',
'weorth-price':'Neuter; stem weorð-. The table gives the complete singular of price or value.',
'feoh':'Neuter; money. Final h disappears before endings: genitive fēos and selected dative fēo. The source prints feoh without a macron before h; preserve that spelling. An absent printed macron does not assert that the historical vowel was short.'}
adj={
'scyldig':'Use the uncontracted stem scyldig-. Strong feminine nominative singular and neuter nominative/accusative plural retain -u; contraction is a documented alternative.',
'twifeald':'The heavy stem twīfeald- takes no -u in strong feminine nominative singular or neuter nominative/accusative plural.',
'gesund':'The heavy stem gesund- takes no -u in strong feminine nominative singular or neuter nominative/accusative plural.',
'hal':'The heavy stem hāl- takes no -u in strong feminine nominative singular or neuter nominative/accusative plural. The meaning here is health.',
'agen':'Use āgn- before vowel-initial endings but āgen- before consonantal endings: compare āgnes, āgnum, āgna, āgnu with āgenne, āgenre, āgenra.',
'claene':'Use clǣn- before endings. Retain dictionary -e where no other ending is present. In the accusation, the sense is blameless or free from guilt.',
'eltheodig':'Use the uncontracted stem ęlðēodig-. Strong feminine nominative singular and neuter nominative/accusative plural retain -u.'}
verb={
'bethurfan':'This preterite-present has present singular beðearf, beðearft, beðearf and plural beðurfon. The dental preterite uses beðorfte- in the singular and beðorft- in the plural. The complete indicative is assigned; the headword alone does not introduce an infinitive construction or subjunctive.',
'oncnawan':'The present stem oncnāw- changes ā to ǣ in the second and third singular. Preterite oncnēow- adds -e in the second singular; first and third singular have no ending. The recognized person is accusative.',
'undon':'Retain un- with the irregular dōn stems: undō, undēst, undēð, undōð; preterite undyde, undydest, undydon. The accusative object is the tied container opened.',
'lecgean':'The short weak verb has lęcge, lęgest, lęgeð and plural lęcgeað. The doubled consonant is absent in the second and third singular. Present cg alternates with preterite g: lęgde, lęgdest, lęgdon. These tables select the uncontracted past; lēde/lēdon are documented variants. The reading’s imperative lęcgeað is separately supplied.',
'foresecgean':'Add fore- to the irregular sęcgan pattern. Select plural foresęcgeað, second/third singular foresægst and foresægð, and preterite foresægde, foresægdest, foresægdon. Retain unmarked æ before gd; contracted sāde is a separate alternative. Here the verb means mention earlier, not predict the future.',
'forstelan':'Strong class IV alternates e, æ, ǣ, o. Present second and third singular have i: forstilst, forstilð. Preterite first/third singular is forstæl, second singular forstǣle, and plural forstǣlon. Keep lexical for-; unprefixed stelan is listed separately.',
'ceapian':'Weak class II has present -ie, -ast, -að, -iað and preterite -ode, -odest, -odon. Retain ēa. The complete infinitive pair is cēapian/cēapianne; the special buying-purpose construction remains supplied.',
'gedon':'Present subjunctive is gedō in all singular persons and gedōn in all plural persons. The causative construction takes an accusative person and an agreeing adjective.',
'agiefan':'Retain ā- with unchanged gief-. Present subjunctive singular ends in -e and plural in -en. The returned person is accusative and the recipient dative.',
'hlystan':'Long weak hlyst- takes present subjunctive -e/-en. Speech or content heeded is genitive.',
'gemiltsian':'This extends the familiar weak class II verb to present subjunctive -ie/-ien. The person receiving mercy remains dative.',
'geseon':'The contracted present subjunctive is gesēo in the singular and gesēon in the plural. Only this mood and tense are added here.',
'wunian':'The familiar weak class II verb adds present subjunctive -ie/-ien. Dwelling in a place uses on with dative.',
'bringan':'Present subjunctive is bringe/bringen; preterite subjunctive brōhte/brōhten. The irregular dental past changes g to h before the dental group. Each tense has one form for all three persons within a number.',
'laedan':'The weak dental past has dd: lǣdde/lǣdden. These are the preterite subjunctive singular and plural in all persons, used under a past report of desire.',
'stelan':'The preterite subjunctive uses the long-vowel plural stem stǣl- in both numbers: stǣle/stǣlen. Its use in the accusation concerns earlier theft.',
'gearcian':'Weak class II commands have singular -a and plural -iað; these extend the earlier indicative system.',
'ascian':'Weak class II commands have singular -a and plural -iað. Retain initial ā.',
'diernan':'The pair gives plain and inflected infinitives. Select -anne here; -enne is a documented alternative. A modal takes the plain form; the inflected form still requires a licensed construction.',
'erian':'The pair gives plain and inflected infinitives, with selected -ianne. The modal construction takes the plain form. Retain printed ę.',
'ripan':'The pair gives plain and inflected infinitives, with selected -anne. The modal construction takes the plain form. Retain ī.',
'giernan':'The pair extends the earlier finite system to plain and inflected infinitives, with selected -anne. The genitive and desired-content complements are explained separately.',
'afaeran':'The long weak stem gives present āfǣrende and uncontracted past āfǣred. The base past participle can remain uninflected in the supplied predicate with plural subject.',
'beodan':'Strong class II gives present bēodende and past boden. The selected new sense is command, distinct from offering. The impersonal command passive remains supplied as a whole.',
'ofslean':'The contracted verb gives present ofslēande and past ofslægen; ofslagen is a documented alternative. Retain of-. These participles do not introduce a finite system.',
'ofthyncean':'This complete impersonal system is limited to third singular: present indicative ofðyncð, present subjunctive ofðynce, and past ofðūhte in both moods. The experiencer is dative and does not trigger personal or plural agreement. A cause/content clause gives what grieves that person.'}
add('# Unit 18. Independent prose consolidation\n')
add('A connected narrative changes speakers, refers back across clauses, and presents some actions as wishes, instructions or reports. Identify each clause’s participants and time relation before joining it to the whole.\n')
add('The final numbered Cook exercises form a sustained Joseph composition sequence. The original Old English reading continues the banquet scene with the princess’s gifts and the farewells. These are separate texts. The two translated examples and lettered tasks are new teaching material.\n')
marks(['NEW-U18-DICTIONARY-REFERENCES','NEW-U18-VERBAL-CONTEXT-HELP'],'Reference and supplied forms')
add('**Forms and help.** A dictionary form identifies a word; it may still need inflection. The complete tables teach their named systems and stated meanings. Diagnostic stems are references to those systems, not assignments of unlisted moods. An expression labelled **Supplied** remains visible during the task: use its unfamiliar forms with the explanation given. Its independent recall is not required. In verb tables, 1, 2 and 3 denote person.\n')
add('## 1. Clauses, reference and reporting\n')
add('A noun phrase takes its case from its own clause. A relative expression can have a different role from its antecedent. The particle ðe has no visible case ending; identify its verb and complements to establish its role.\n')
for e in C['new_material_examples']:
 marks([e['teaching_id']],'Cumulative translated example');add('**'+e['text']+'**\n');add(e['translation']+'\n');add(e['teaching_point']+'\n')
add('A third-person pronoun follows its referent’s grammatical gender, including that of an inanimate noun. Agreement can exclude a referent without selecting a unique person. There is no general nearest-noun rule.\n')
add('In direct speech, ic identifies the current speaker. A report revises that reference to fit its reporting clause. A preterite subjunctive under a past report does not itself prove the report false. Establish earlier, simultaneous or prospective time from the whole statement.\n')
add('With hātan and an infinitive, the accusative actor is the person ordered to act. A dative recipient of that action is a separate complement.\n')
add('## 2. Nouns and adjectives\n')
add('Choose case from the phrase’s function: nominative subject, accusative direct object, genitive possessor or licensed complement, dative recipient or licensed complement. A preposition or particular verb can determine the case.\n')
add('Strong masculine nouns normally have genitive singular -es, dative -e, nominative/accusative plural -as, genitive plural -a and dative plural -um. Strong neuters share -es, -e, -a and -um; nominative and accusative agree, with plural -u or no ending according to the stem. The selected feminine oblique singular ends in -e. Stem changes and weak assa are given individually.\n')
add('A singular-only table gives all four cases of the stated mass or abstract meaning, using a familiar class. It does not claim that no plural is possible in other senses.\n')
for p in C['paradigms']:
 if p['part_of_speech'] not in ['noun','adjective']:continue
 lid=p['lemma_id']
 if lid=='scyldig':
  add('### Strong and weak adjectives\n');add('Adjectives agree in gender, number and case. Use the strong pattern in its familiar undetermined uses and the weak pattern after the determiners that require it. The tables give every ordinary case in all three genders and both numbers. Strong masculine and neuter instrumental singular cells are recognition only; they introduce no new instrumental production.\n')
 add('### '+p['headword']+'\n');vocabulary(lid,p['headword']+' vocabulary')
 marks(sorted({x for cell in p['cells'] for x in cell.get('teaching_ids',[]) if x in T and T[x]['kind']=='complete_bounded_paradigm'}),p['headword']+' nominal system')
 add((noun if p['part_of_speech']=='noun' else adj)[lid]+'\n')
 ms=[m for m in M if p['paradigm_id'] in m['paradigm_ids']]
 for m in ms:
  if len(ms)>1:add('**'+m['title']+'**\n')
  table(m)
add('## 3. Verbal systems\n')
add('Each heading states the complete system added or reviewed. Indicative tables distinguish present and preterite. Subjunctive tables give all persons of the named tense; identical forms do not remove person distinctions. Commands distinguish singular and plural addressees. Infinitive and participle pairs add no unlisted finite forms.\n')
add('A modal takes a plain infinitive. The inflected infinitive requires its stated construction, commonly with tō. A base past participle may occur in the specified passive or result predicate without a new adjective declension. Meaning and complementation remain separate from the form.\n')
scopes={'indicative12':'present and preterite indicative','indicative12-infinitive2':'indicative and infinitives','present-subjunctive6':'present subjunctive','preterite-subjunctive6':'preterite subjunctive','subjunctive12':'present and preterite subjunctive','imperative2':'singular and plural commands','infinitive2':'plain and inflected infinitives','participle2':'present and past base participles','impersonal4':'third-singular impersonal system'}
for p in C['paradigms']:
 if p['part_of_speech']!='verb':continue
 lid=p['lemma_id'];code=p.get('system_scope_code',p['paradigm_id'].split('-',2)[-1]);name=scopes.get(code,code)
 add('### '+p['headword']+': '+name+'\n');vocabulary(lid,p['headword']+' meaning')
 marks(sorted({x for cell in p['cells'] for x in cell.get('teaching_ids',[]) if x in T and T[x]['kind']=='complete_bounded_paradigm'}),p['headword']+' '+name)
 if lid=='theowian':rule='Weak class II present subjunctive has -ie in the singular and -ien in the plural. The selected sense is enslave, with an accusative person. The source’s -ige variant is the same ending.'
 elif lid=='bereafian':rule='Weak class II gives present subjunctive -ie/-ien. The deprivation complement is explained below.' if 'subjunctive' in code else 'Weak class II gives present -iende and past -od. Retain ēa. These are base participles; the deprivation complement is taught separately.'
 else:rule=verb[lid]
 add(rule+'\n')
 cite=p.get('citation_reference',{})
 if cite.get('diagnostic_stems'):add('**Diagnostic forms:** '+'; '.join(x['form']+' ('+x['label']+')' for x in cite['diagnostic_stems'])+'.\n')
 ms=[m for m in M if p['paradigm_id'] in m['paradigm_ids']]
 for m in ms:
  if len(ms)>1:add('**'+m['title']+'**\n')
  table(m)
add('## 4. Meanings and complements\n')
for lid in L:vocabulary(lid,'Additional productive meanings')
for f in C['grammar_inventory']:
 if f['knowledge_status'] not in ['new_production','new_recognition']:continue
 add('### '+f.get('label',f['feature_id'])+'\n');fm(f['feature_id'],'Meanings and complements')
 body=f['description']
 body=re.sub(r'BT(?: Supplement)?\s*\d+[^.]*\.(?:\s*\d+[^.]*\.)?', '',body)
 body=body.replace('The two case frames are not interchangeable.','Keep the recipient distinct from those present at the oath.')
 body=body.replace('ætforan us','ætforan ūs')
 if f['feature_id']=='u18-bethurfan-genitive-relative':body='Beðurfan takes a genitive of the thing needed in the selected construction: hwǣtes, of wheat. In ðā ðing ðe wē beðurfon, the things are accusative outside the relative because they are bought. Inside it, invariant ðe represents the genitive complement required by beðurfan. Its unchanged spelling does not transfer the outer accusative into the relative. Other government is attested; the genitive is the target here.'
 if f['feature_id']=='u18-bereafian-deprivation':body='Berēafian takes an accusative person and genitive possessions in the selected active construction. In the passive, the deprived person becomes nominative while the possessions remain genitive. In 45.6, assena and ðinga are genitive plurals; selfe agrees with accusative ūs in the following clause. Dative and instrumental alternatives are attested elsewhere, but the local target is genitive.'
 if f['feature_id']=='u18-giernan-propositional-desire':body='After giernan, genitive ðæs points forward to a ðæt clause explaining the desired action. The demonstrative is inflected; the following ðæt is a conjunction. In the past report, lǣdden is first-plural preterite subjunctive, describing the action then desired.'
 if f['feature_id']=='u18-ondraedan-genitive':body='Ondrǣdan can take a reflexive dative and a genitive feared thing. In 48.6, ēow names the people themselves and nānes ðinges the feared entity. In 46.1 the reflexive dative occurs without an expressed feared thing. The unchanged spelling of ēow does not make it accusative. This construction supplements the earlier accusative frame.'
 if f['feature_id']=='u18-ofthyncean-impersonal':body='Ofðyncean remains third singular with a dative experiencer and a cause/content ðæt clause. Present subjunctive ofðynce means let it not grieve in the negative wish. English it needs no separate Old English pronoun here. A plural experiencer does not make the verb plural.'

 body=body.replace('in the model','in the translation').replace('Our ðēowie','The selected ðēowie')
 add(clean(body).strip()+'\n')
add('The earlier preterite singular funde of findan remains valid; the alternative fand does not invalidate it. Retain the selected spelling unless using an independently justified alternative.\n')
def task(t):
 tid=t['task_id'];cook=tid.startswith('EX-');short='.'.join(str(int(x)) for x in tid.split('-')[-2:]) if cook else tid.split('-')[-1]
 add('### '+('Cook '+short if cook else short)+'\n');add('<!-- item: '+tid+' -->\n');add(t['prompt']+'\n')
 hs={h['support_id']:h for h in t.get('local_support',[])}
 for seq in t.get('input_sequences',[]):
  sid=seq['sequence_id'];kind=seq['kind'];text=seq['text']
  if kind=='input':add(text+'\n')
  elif kind=='visible_lexical_reference':add('**Reference:** '+text+'.\n')
  elif kind=='visible_source_hint':add('**Hint:** '+text+'.\n')
  else:
   h=hs.get(sid,{})
   if h.get('feature_id'):fm(h['feature_id'],tid+' supplied construction')
   hm([x.get('form_id') for x in seq['tokens']],[x.get('sense_id') for x in seq['tokens']],tid+' supplied word')
   meaning=h.get('meaning_and_analysis',h.get('meaning',''))
   if isinstance(meaning,list):meaning=' '.join(meaning)
   meaning=meaning.replace('paired here with samod','').strip(' ;,.')
   parse=analysis(h.get('analysis',{}))
   add('**Supplied:** '+text+' — '+clean(meaning)+(('; '+parse) if parse and not h.get('feature_id') else '')+'.\n')
 for r in t.get('source_control_records',[]):
  exp=[x for x in r.get('explanatory_content',[]) if not x.startswith(('The exact lexical or phrase hint ','The class/form reference is resolved','Reuse the actual earlier complete system','The source locator is retained exactly'))]
  if any('nominal packet' in x for x in exp):
   head=r.get('hint_text','the noun')
   exp=['The number refers to the noun’s declension. Use the complete '+head+' table in section 2 and its stated stem rule.']
   if head=='gerēfa':exp=['Gerēfa follows the earlier weak masculine pattern: nominative singular -a; other singular cases and nominative/accusative plural -an; genitive plural -ena; dative plural -um.']
  if r['reference_id']=='U18-HINT-45-07-05':exp=['Ūs is the benefactive/reflexive dative: we bought wheat for ourselves. It refers to the buying subject, while wheat is the accusative thing purchased. Retain the phrase; the prompt gives no omission instruction.']
  if exp:add('**'+r['literal_source_text']+'** '+clean(' '.join(exp))+'\n')
 for i,p in enumerate(t['output_positions'],1):
  add('<!-- output: '+p['output_position_id']+' -->\n')
  if not cook:add(str(i)+'. '+p['label']+'\n')
add('## 5. Cumulative analysis and controlled composition\n')
add('Use the stated earlier or newly taught forms. Keep any explicitly supplied reference visible. Explain roles from the actual sentence; do not supply an unstated referent or event.\n')
for t in C['assigned_items']:
 if t['task_id'].startswith('NEW-U18-') and not t['task_id'].startswith('NEW-U18-R'):task(t)
add('## 6. Cook: the Joseph sequence\n');marks(['NEW-U18-SOURCE-HINTS'],'Cook source controls')
add('Translate every numbered prompt into Old English. Parentheses and brackets are Cook’s original controls: a lexical hint selects a word, om. requests omission of a separate word, and an order or number instruction applies where marked. The numbered grammar references are explained beside their prompts. English wording is retained exactly, including commandest in 47.11. Modern hints and supplied expressions remain available during composition. Preserve every participant, clause and time relation.\n')
for n,heading in {44:'The return is proposed',45:'The brothers return to Egypt',46:'The welcome and the cup',47:'The accusation and the plea',48:'Recognition and invitation'}.items():
 add('## Cook '+str(n)+'. '+heading+'\n')
 for t in C['assigned_items']:
  if t['task_id'].startswith('EX-') and int(t['task_id'].split('-')[-2])==n:task(t)
add('## 7. The gifts and the end of the banquet\n')
reading=C['source_spans'][0]
add('The king’s daughter has heard and watched Apollonius. The continuation moves through her gifts, their delivery and the farewells. The exact passage is Cook 175.18–177.2, ending before the following teacher scene. Read it with the original notes and modern help below.\n')
raw=[]
for line in reading['source_lines']:
 s=re.sub(r'\[([0-9]+[a-z]?)\]',lambda m:'[^P'+str(line['printed_page'])+'N'+m[1]+']',line['source_with_note_markers'])
 raw.extend(s.split())
def bare(s):return re.sub(r'\[\^[^\]]+\]','',s)
noted=[];i=0
for want in reading['learner_text'].split():
 word=raw[i];i+=1
 while bare(word)!=want:
  assert bare(word).endswith('-') and i<len(raw),(word,want)
  nxt=raw[i];i+=1;choices=[word+nxt,word[:-1]+nxt]
  viable=[x for x in choices if want.startswith(bare(x)) or bare(x)==want]
  assert viable,(word,nxt,want)
  word=viable[0]
 noted.append(word)
assert i==len(raw)
notedtext=' '.join(noted);assert bare(notedtext)==reading['learner_text']
assert len(re.findall(r'\[\^[^\]]+\]',notedtext))==29
add(notedtext+'\n')
add('### Finding the cited lines\n')
add('These locators retain the source’s physical line divisions, including divided words. The running text joins those words.\n')
add('| Page and line | Beginning of the printed line |');add('| --- | --- |')
for line in reading['source_lines']:
 s=re.sub(r'\[[0-9]+[a-z]?\]','',line['source_with_note_markers'])
 add('| '+str(line['printed_page'])+'.'+str(line['editorial_line'])+' | '+' '.join(s.split()[:5])+' … |')
add();add('### Modern help for the reading\n')
add('The explanations supply unfamiliar senses and whole constructions. Where an original note already identifies a referent, the later question asks for an explanation with that aid visible. Source spelling is retained.\n')
rhelp={
'01':('175.18–20: seeing and falling in love','The daughter sees that a fact holds; indicative wæs belongs to the content clause. Wæs getogen means was educated or accomplished in good skills. In the following idiom, singular mōd is the subject of gefēoll, hiere its possessor, and on his lufe the state into which her mind falls: she falls in love with him.'),
'02':('175.20–176.2: the earlier permission','Līefdest means permitted, with mē as dative person permitted. Ðæt ic mōste giefan is naturally translated by permitted me to give. The free-choice object swā-hwæt-swā means whatever; wolde is first-singular preterite subjunctive and leaves giving understood. Of with dative identifies the treasury from which she may take the gift.'),
'03':('176.3–4: renewed permission','Gief is a singular command to the daughter, with him as recipient. Wille is second-singular present subjunctive within whatever you wish. Its spelling also occurs in other persons and moods; this context fixes the use.'),
'04':('176.4: going out','Hēo … ūtēode means she went out. Swīðe blīðe means very gladly. The exact prefixed preterite is supplied.'),
'05':('176.5–8: the gifts','Giefe is first-singular present indicative; ðē is the recipient. Be mīnes fæder lēafe means with my father’s permission. The following quantities all name what she gives. Their complete weight and servant expressions are supplied below.'),
'06':('176.9–11: the instructions','Berað and lęcgeað are plural commands to the enslaved men: carry the gifts along and place them in the chamber before her friends. In the promise relative, behēt is first-singular preterite, ðe represents the promised things, and Apollonio mīnum lārēowe is the dative recipient. The source lęcgeað is imperative despite matching the newly learned indicative plural in spelling.'),
'07':('176.12: the command is carried out','Ðis wearð … gedōn means this was done. Gedōn is a past participle in the singular passive event, not a present subjunctive plural of the same spelling. The action follows the princess’s command.'),
'08':('176.12–13: praise and a separated relative','All the men who saw the gifts praised her gifts. Original note13 explicitly identifies męnn as antecedent of ðe. The relative is subject of its clause; hīe is accusative plural, the gifts. The relative stands after the main clause’s object, separated from its own antecedent. Both finite verbs have plural subjects.'),
'09':('176.13–16: the guests leave','Geęndode is intransitive: the banquet ended. The men rose, took leave of king and princess, wished them well and returned home. In bǣdon hīe gesunde bēon, hīe is the accusative actor of bēon and gesunde its agreeing accusative plural predicate. This complete farewell wish is supplied.'),
'10':('176.16–18: Apollonius’s farewell','The king and princess are addressed separately and then resumed together by plural gē. Bēon is second-plural present subjunctive, may you be; gesunde is nominative plural agreeing with gē. The agent nouns and their genitive complements are supplied below.'),
'11':('176.18–20: the servants','Beseah tō means looked toward, with a dative target. In the relative, the maiden is subject, the enslaved men the object represented by ðe, and singular him the recipient Apollonius. Forgiefen hæfde is active past perfect. The later him is plural and refers to the servants; tō follows the verb but still belongs to that dative addressee.'),
'12':('177.1–2: the proposed departure','Nimað is a plural command to take the gifts along. Gān wē is a first-plural subjunctive exhortation, let us go; supplied sēcean states the purpose of going. In the gift relative, the princess is subject and mē recipient. Final ðæt expresses purpose, with plural mægen and accusative reflexive ūs before geręstan. The words propose seeking the guesthouse and resting; they do not narrate a completed arrival.')}
for no,(heading,body) in rhelp.items():
 add('### '+heading+'\n');fm('U18-RSUP-'+no,heading);add(clean(body)+'\n')
add('### Supplied expressions and exact word help\n')
glossary_groups=[];shared_glosses={}
for original in reading['local_support']:
 h=dict(original);h['learner_support_ids']=[h['support_id']]
 if h.get('exact_help_text') in ['hund','swā-hwæt-swā']:
  key=json.dumps({k:h.get(k) for k in ['exact_help_text','form_id','sense_id','meaning','analysis']},ensure_ascii=False,sort_keys=True)
  if key in shared_glosses:
   shared_glosses[key]['learner_support_ids'].append(h['support_id']);continue
  shared_glosses[key]=h
 glossary_groups.append(h)
assert sorted(x for h in glossary_groups for x in h['learner_support_ids'])==sorted(h['support_id'] for h in reading['local_support'])
Path('build/u18-learner-glossary-coverage.json').write_text(json.dumps({'source_support_count':len(reading['local_support']),'display_groups':len(glossary_groups),'shared_glosses':[{'text':h['exact_help_text'],'form_id':h['form_id'],'sense_id':h['sense_id'],'support_ids':h['learner_support_ids']} for h in glossary_groups if len(h['learner_support_ids'])>1],'all_support_ids':[x for h in glossary_groups for x in h['learner_support_ids']]},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
for h in glossary_groups:
 if h.get('feature_id','').startswith('U18-RSUP'):continue
 fid=h.get('feature_id')
 if fid:fm(fid,'Reading supplied expression')
 hm([h['form_id']] if h.get('form_id') else [],[h['sense_id']] if h.get('sense_id') else [],'Reading exact word help')
 text=h.get('exact_help_text',h.get('exact_span',h.get('phrase','')))
 meaning=h.get('meaning_and_analysis',h.get('meaning',h.get('help_text','')))
 if h.get('support_id')=='U18-HELP-SERVANTS':meaning='Twenty enslaved men; to the enslaved men. Preserve ðēowa without r. The selected local explanation treats ðēowa and manna as appositional genitive plurals, and ðēowum and mannum as appositional datives. The phrase’s meaning and case are supplied without requiring independent historical classification.'
 if h.get('support_id')=='U18-HELP-FINAL-PLAN':meaning='Let us go seek our guesthouse, so that we may rest. Gān wē is an exhortation, ðæt marks purpose, and ūs is accusative reflexive with geręstan.'
 if h.get('support_id')=='U18-HELP-QUANTITIES':meaning='Two hundred pounds of gold and four hundred pounds by weight of silver. Hund means hundred. Punda is genitive plural after the hundreds; goldes and seolfres are material genitives. Gewihte is a dative expression of measure: by weight.'
 if text=='hund' and h.get('sense_id')=='hund-hundred-source':meaning='hundred, in the supplied gold and silver weight expressions'
 parse=analysis(h.get('analysis',{}))
 add('**'+text+'** — '+clean(str(meaning)).rstrip('.')+(('; '+parse) if parse and not fid else '')+'.\n')
add('### Reading tasks\n')
add('Keep the complete text, original notes and modern help available. Translate the whole assigned passage; the analysis questions explain the supplied relations without testing recall of unfamiliar source forms.\n')
for t in C['assigned_items']:
 if t['task_id'].startswith('NEW-U18-R'):task(t)
add('## Source and editorial notes\n')
add('The English prompts are Cook, Exercises in Old English, joint Group XII, XIII, Exercises 44–48, printed pages 29–33 (PDF pages 37–41). The original prose is Cook, A First Book in Old English, second edition, Reader XII, printed 175.18–177.2 (PDF 191–193). Modern explanations and lettered tasks are separate teaching material. Note numbers restart by printed page; P175, P176 and P177 identify the page.\n')
add('Preserve the selected spellings, including unmarked æcern, læfel and feoh, reading lęcgeað, and ðēowa without added r. The strong servant noun and the acorn plural have separately checked dictionary and manuscript-edition support. Derived paradigm cells apply the given stem and ending rules; their display does not assert that every cell occurs in the passage.\n')
add('The note on getogen raises an etymological question about modern wanton; here getogen means educated or accomplished. The hǣse note points to modern behest; hǣs here means command. These historical prompts are not additional exercises. The Beowulf comparison describes the company rising and one man greeting another and wishing him health; it illustrates farewell without assigning a poetry reading.\n')
add('The Latin notes mean a little earlier (176 note 1), teacher or master (note 5), enslaved people (note 10), dining room (note 11), saying farewell (note 15), and farewell or be well (note 17). Note 2 recommends an English infinitive for the finite Old English permission clause. Note 4 observes that the going-out detail is absent from the Latin. Note 9 records a manuscript adjective variant; the learner text retains Cook’s edited dēorwurðes. The other numbered grammatical references are explained in the modern reading help.\n')
for n in reading['original_notes']:
 label='P'+str(n['printed_page'])+'N'+str(n['original_note_number'])
 add('[^'+label+']: '+n.get('original_text',n.get('text_original',n.get('text','')))+'\n')
text=unicodedata.normalize('NFC','\n'.join(out))
Path('chapters/ch18/student.md').write_text(text,encoding='utf8')
missing=[t for tid,t in T.items() if tid not in seen]
Path('build/u18-learner-teaching-routes.json').write_text(json.dumps({'routes':routes,'unplaced':missing},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'characters':len(text),'words':len(text.split()),'teaching_markers':len(seen),'unplaced_count':len(missing),'unplaced':[t['teaching_id'] for t in missing]},ensure_ascii=False,indent=2))
