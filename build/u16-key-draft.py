"""Author Unit16 key from the committed task contract and separately written answers."""
import json,runpy,unicodedata,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text(encoding='utf8'))
C=read('chapters/ch16/coverage.json');tasks={x['task_id']:x for x in C['assigned_items']}
FM={x['task_id']:x for x in read('curriculum/proposals/unit16/author-only-form-models.json')['tasks']}
CM={x['source_item_id']:x for x in read('sources/audits/unit16-grammar/author-only-cook-models.json')['items']}
# Declared post-contract corrections leave the sealed original model packet intact.
if C.get('selected_model_corrections'):
    for seq in read(C['selected_model_corrections']['path'])['corrected_sequences']:
        CM[seq['owner_id']]['model']=seq['text']
COOK=runpy.run_path(str(R/'build/u16-key-cook-notes.py'))['COOK']
parts=[]
def put(s=''):parts.append(s)
def begin(tid,title=None):
    put('### '+(title or tid.removeprefix('NEW-U16-')));put();put('<!-- key: '+tasks[tid]['key_item_id']+' -->');put()
def answer(tid,n,text):
    p=tasks[tid]['output_positions'][n-1]
    put('<!-- output: '+p['output_position_id']+' -->');put();put('**'+str(n)+'. '+p['label']+'.** '+text);put()
put('# Unit 16. Answer key');put()
put('The Old English composition models are new teaching material. The reading translation renders Cook’s actual Old English. A model is one defensible answer: preserve the meaning, case relations, agreement, viewpoint and clause connections, while also observing each task’s stated lexical, number and word-order targets. An otherwise valid alternative can miss a requested target.');put()
put('The exact local helps remain available. A supplied phrase is not a test of unaided recall, even when some of its words have been taught. The form tasks use the selected tables; dictionary-given **iernan** and **nearu** are reference inputs, not extra vocabulary-recall tests. Accurate English explanations may differ in wording. N = nominative, G = genitive, D = dative, A = accusative.');put()
put('Except where the exercise fixes an order, grammatical rearrangements that preserve the relationships are acceptable. Cook also attests such variants as dative **ðām** beside the selected **ðǣm**. A spelling variant must be evidenced; it does not excuse a wrong case, person or tense. Distinguish ordinary negative concord from the specially supplied cessation clause in36.3.');put()
put('## F. Forms and phrases');put()
gloss={
'F01':{1:'you cut off (present, singular)',2:'you cut off (past, singular)',3:'they cut off (past)',5:'he loses',6:'you lost (singular)',7:'they lost',9:'he washes',10:'you washed (singular)',11:'they washed',13:'he runs',14:'he ran',15:'they ran'},
'F02':{1:'I anoint',2:'you anoint (singular)',3:'she anointed',4:'I turn',5:'he turned',6:'they played',7:'they beheaded',8:'fulfilled',9:'forgiven'},
'F03':{1:'cut off, addressed to one',2:'cut off, addressed to several',3:'rejoice, addressed to one',4:'rejoice, addressed to several',5:'anoint, addressed to one',6:'anoint, addressed to several',7:'arise, addressed to one',8:'arise, addressed to several',9:'leave, addressed to one',10:'leave, addressed to several',11:'cease, addressed to one',12:'cease, addressed to several',13:'return, addressed to one',14:'return, addressed to several'},
'F04':{1:'that he find',2:'that they find',3:'that he feed',4:'that they feed',5:'to run, plain form',6:'to run, inflected form; give no separate tō here'},
'F05':{1:'narrow, N masculine singular',2:'narrow, A masculine singular',3:'narrow, G masculine singular',4:'narrow, D masculine plural',5:'both sons, A plural',6:'of both sons, G plural',7:'to both sons, D plural'}}
explanations={
('F01',4):'The present second singular has **ie** in **ācierf-**; the preterite second singular and plural use **ācurf-**, with **u**. Add second-singular **-e** or plural **-on** to that past stem. Keep the prefix **ā-** in every form.',
('F01',8):'The present third singular has **īe** and the contracted ending **-st**: **forlīest**. The preterite second singular and plural have **u** and **r**, hence **forlur-e**, **forlur-on**. Carrying present **s** into these past positions misses the stem alternation.',
('F01',12):'The present third singular has **ðwieh-** plus **-ð**. Preterite second singular and plural have **ðwōg-**; their endings are **-e**, **-on**. The selected first/third singular **ðwōh** has **h**, so it cannot simply be used as the stem for all past positions.',
('F01',16):'The selected stems are present **iern-**, singular preterite **arn**, and plural preterite **urn-**. Thus the requested third singular is **iernð**, the past third singular **arn**, and the past plural **urnon**. Neither past stem is formed by merely adding an ending to **iernan**.',
('F02',10):'The selected present first singular retains **w**: **smierwe**. The present second singular and preterite omit it: **smierest**, **smierede**. All three retain the selected **ie** spelling. The distribution is part of this checked paradigm, not a reason to remove every w from every form.',
('F02',11):'**Bewęnde** represents both present first singular and preterite first/third singular. The two requested answers therefore coincide in spelling while differing in tense and person. A subject and context can distinguish them; the ending alone cannot.',
('F05',8):'The masculine nominative singular ends in **-u**. The selected accusative has **-o-** before **-ne**: **nearone**. Before **-es** and **-um** the stem appears as **nearw-**: **nearwes**, **nearwum**. Do not build all four forms from an unchanged nearu-.',
('F05',9):'**Bēgen** has plural forms, although its meaning refers to two. **Bēgen**, **bēgra**, **bǣm** agree with the plural forms of **sunu**. It has no separate dual declension; with a dual personal pronoun such as **unc**, the appropriate form of both is still plural.'}
fnotes={
'F01':'These are the requested indicative positions, not a list of interchangeable principal parts. In particular, **ācurfe**, **forlure** and **ðwōge** are second singular; the corresponding **-on** forms answer they. The English present/past ambiguity of cut does not make the Old English forms interchangeable.',
'F02':'**Gefylled** and **forgiefen** are past participles, not finite past verbs. Their uninflected use is requested here. In a finite anointing clause, a second-singular past would require **smieredest**, whereas the requested she form is **smierede**. Documented i/y variants of smierwan are valid spellings but differ from the selected ie series.',
'F03':'The singular commands do not all have the same ending: compare **blissa**, **smiere** and **ārīs**. The plural follows the selected present stem, including **smierwað** with w. These are ordinary command pairs; the separately taught shortened plural before following gē is not requested here.',
'F04':'Present subjunctive singular **-e** contrasts with plural **-en**. Do not substitute indicative third-singular or plural endings. The infinitives have **-an** and **-anne**; neither is a present participle. In the last answer tō is already specified by the question, so the requested form is **iernanne** alone.',
'F05':'The three phrases require no article. **Suna** is syncretic: in the first phrase it is accusative plural, in the second genitive plural. **Bēgen** versus **bēgra** makes that case contrast visible. **Bǣm sunum** has dative plural agreement in both words.'}
for k in ['F01','F02','F03','F04','F05']:
    tid='NEW-U16-'+k;begin(tid)
    for n,o in enumerate(FM[tid]['outputs'],1):
        text=explanations.get((k,n))
        if text is None:text='**'+o['model']+'** — '+gloss[k][n]+'.'
        answer(tid,n,text)
    put(fnotes[k]);put()

original={
'A01':[
'**The king went.** Hē can refer back to the king, the subject of the first sentence.',
'**The son went.** Hē can instead refer to the king’s son. Both candidates are masculine singular; proximity to the pronoun alone does not settle the reference.',
'**Se cyning ēode.** Only the pronoun has been replaced; the action and tense remain unchanged.',
'**Se sunu ēode.** The explicit nominative subject selects the son. The two readings and their corresponding rewrites may be presented in the opposite order.'],
'A02':[
'“The king saw the son go.” “Saw the son walking” also conveys the perceived action; it need not introduce an Old English progressive construction.',
'“The king knew that the son went.” “Had gone” is defensible if an anterior context is stated, but it is not forced by the spelling ēode alone.',
'**Ðone sunu** is accusative masculine singular. It denotes the actor of the plain infinitive **gān** in the perception construction: the son, not the king, does the going.',
'**Se sunu** is nominative masculine singular, the subject of finite **ēode** inside the **ðæt** content clause. The subject’s case is determined within that clause.',
'**Gān** is a nonfinite plain infinitive. **Ēode** is a finite third-singular preterite of gān here; indicative and subjunctive share that spelling. A factual indicative or contextual report-subjunctive analysis is possible, provided the answer acknowledges that the surface alone does not distinguish them.'],
'A03':[
'“He said that the king was there.” The king’s presence is simultaneous with the saying, as the specified context requires.',
'**Sægde:** sęcgan, third-singular preterite indicative. **Wǣre:** wesan, third-singular preterite subjunctive in the reported clause. The subject se cyning rules out the homographic second-singular indicative analysis of wǣre.',
'There is **no infinitive or participle**. Both sægde and wǣre are finite.',
'The content is a finite **ðæt** clause with reported **wǣre**. Its past form is interpreted from the past saying viewpoint; the context places the presence at that same time. It does not mean that the king had already ceased to be there. English backshift alone cannot determine the relative time.',
'“He said that the king had made the ship.” The making is complete before the saying viewpoint.',
'**Sægde:** third-singular preterite indicative of sęcgan. **Hæfde:** third-singular preterite of habban, finite auxiliary in the content clause. The model selects the report subjunctive; its indicative spelling is identical, so a factual-indicative interpretation is also defensible with that limit explained.',
'**Geworht** is the uninflected past participle of **gewyrcean**. It combines with finite **hæfde** and accusative patient **ðæt scip**. It is not itself a finite verb.',
'The transitive **habban + past participle** group presents the making as complete at the past viewpoint. That complete group, together with the stated context, supports anterior “had made.” Calling both verbs simply past would miss the relation between them; this is not a passive with the ship as subject.',
'“He said that the king intended to sing.” “Would sing” is acceptable if it retains the intended later action rather than asserting its eventual fulfillment.',
'**Sægde:** third-singular preterite indicative of sęcgan. **Wolde:** third-singular preterite of willan, finite volitional verb in the content clause. The selected report-subjunctive analysis shares its spelling with the indicative; a contextual indicative report is possible if that syncretism is acknowledged.',
'**Singan** is the plain infinitive complement of **wolde**. Its understood actor is the king.',
'**Willan + plain infinitive** expresses volition or intention. In the stated context, singing is still intended and lies after the saying. Neither wolde nor the English word would proves that the singing happened. This contrasts with simultaneous wǣre in sentence1 and completed geworht hæfde in sentence2.'],
'C01':[
'**Se cyning sægde his suna: ‘Sęle mē ðā bōc.’**\n\nThe king said to his son, “Give me the book.” **His suna** is the dative speech recipient; **sęle** is a singular command. **Mē** is the recipient of giving and **ðā bōc** its accusative object.',
'**Se sunu sealde him ðā bōc.**\n\nThe son gave the book to the king. **Sealde** narrates the completed action; **him** remains dative. An explicit **ðǣm cyninge** would remove reference ambiguity, but would replace the recipient pronoun that the next part asks you to explain.',
'Quoted **mē** and narrative **him** both denote the king. The first is first person because the king is speaking; the second is third person because the narrator is describing him. Changing the pronoun’s person need not change its referent.'],
'C02':[
'**Ic cann ðone mann.** — “I know that man.” The personal object is accusative, and cunnan means acquaintance here. Another evidenced knowing verb could be valid language, but the prompt specifically requests cunnan.',
'**Ic cann singan.** — “I know how to sing.” The plain infinitive supplies the learned skill; no separate translation of English how is required in this frame.',
'**Ic wāt ðæt hē hēr is.** — “I know that he is here.” Witan takes a finite content clause; **hē** is its nominative subject. The model presents the content factually with indicative is. A subjunctive needs an appropriate contextual interpretation, not an automatic rule that every dependent clause must have one.',
'The first complement is an **accusative person**, the second a **plain infinitive**, and the third a **finite ðæt clause**. These examples contrast particular senses and constructions. They do not establish a universal persons-versus-facts division: witan can also take a personal object, as in Cook35.7.'],
'C03':[
'**Ðā męnn plegodon wel; se cyning plegode bęt ðonne hīe dydon.**\n\n“The men played well; the king played better than they did.” **Plegodon** and **dydon** are plural; **plegode** is singular. **Bęt** compares the playing, and ðonne introduces its comparison clause.',
'**Dydon** stands for **played** and agrees with **hīe**, the men. Its subject is not the singular king. Repeating **plegodon** could make a grammatical comparison, but would miss the expressly requested substitute-dōn target. This use does not create modern English do-support.'],
'R02':[
'The boy announces that the baths are open, and Apollonius hears him: **Se bæðstęde is open** (168.9–10), followed by Apollonius taking off his half-cloak and entering (168.11–12). His earlier concern is finding help to live on; the king has not yet invited him.',
'Apollonius joins the ball game, catches and returns the ball with speed, and does not let it fall (168.18–169.5). The king notices **ðæs geongan snelnesse**, the young man’s agility. Merely saying that they played omits the evidence of skill that attracts attention.',
'The king tells his companions to go away and says **ðes cniht … is mīn gelīca**, “this young man … is my equal” (169.7–8). Distinguish this clear direct statement from the preceding clause whose pronoun reference Cook calls unclear.',
'The messenger concludes that Apollonius is **forliden mann**, a shipwrecked man (170.10–11). He has seen him wrapped in a dirty cloak; he says **his gegierela hine gesweotolað**, “his clothing reveals him” (170.13–14). He infers the condition from clothing, rather than reporting a confession or learning the man’s name.',
'The king orders his messenger to go quickly and convey an invitation to Apollonius to come to the king’s meal (170.14–16). The messenger is to deliver the request; the text does not yet narrate Apollonius accepting or attending the feast.'],
'R03':[
'**Hine** is accusative masculine singular and refers to the **ball**, ðoðor; Cook’s note3 confirms this. It is the actor of **feallan** in the construction “he never let it fall.” Grammatical masculine does not make its referent a man.',
'**Him** is dative singular and refers to the **king**, the person Apollonius serves with **ðēnode**. The verb’s recipient/service frame and the scene establish its role; it is not an accusative object merely because English says served him.',
'The **hē** immediately before hine lǣdde is nominative singular, **Apollonius**, subject of the leading action. Cook’s note14 identifies him explicitly. It is distinct from the king who has just come out of the bath.',
'**Hine** is accusative masculine singular, the **king**, direct object of lǣdde. Cook’s note15 names the king. Apollonius leads the king by the hand, not the reverse.',
'**Him** is a dative reflexive referring to **Apollonius**, the subject who then turns away. It belongs to **gewęnde**, as the local help and §184a indicate. It does not introduce another person to whom Apollonius went.',
'The **hē** after ðæt is nominative masculine singular, **Apollonius**, subject of **wæs … bewǣfed**. The preceding observer is the messenger. Cook’s note8 and the clothing report distinguish the two referents; the masculine ending alone would not.'],
'R04':[
'**Ðe him getǣht wæs** is a relative clause identifying **ðone weg**, the road that had been shown to him. It is not the main action of walking.',
'The passive group is **getǣht wæs**: **wæs**, third-singular preterite indicative of wesan, is finite; **getǣht** is the past participle. The relative’s subject is the road, and **him** is the dative person to whom it was shown.',
'**Ōð-ðæt hē becōm** is a temporal endpoint clause: the walking continues until he reaches the gate.',
'**Becōm** is third-singular preterite indicative of becuman. The completed arrival supplies the endpoint; do not call it subjunctive merely because it is subordinate.',
'**Hwone hē biddan meahte** is a dependent question giving the content of his thought: whom he might ask. **Hwone** denotes the person asked, not the subject of could.',
'The group is **biddan meahte**. **Meahte** is third-singular preterite of magan, selected here as subjunctive possibility in the dependent question; the indicative has the same surface. **Biddan** is a plain infinitive, not a second finite verb.',
'**Ðæt se cyning hine hęrede** is the content of what Apollonius heard: that the king praised him. The surrounding when-clause contains the hearing.',
'**Hęrede** is third-singular preterite of hęrian, selected here as indicative in the heard content. Its subjunctive spelling is identical. The answer should identify the king as its subject and avoid pretending that the ending by itself proves mood.',
'**Hwæt se geonga mann sīe** is the dependent question governed by **gewite**, “find out.” Here hwæt asks what the man is or what his condition is; the messenger responds with his shipwrecked condition.',
'**Sīe** is third-singular present subjunctive of wesan. The subject is **se geonga mann**. It is finite, whereas gewite is the separate imperative governing the question.',
'**Ðēah hē hit self forswīge** is a concessive clause: even if he himself keeps it silent. It concedes possible silence while asserting that the clothing still reveals him.',
'**Forswīge** is third-singular present subjunctive of forswīgian in the supplied source construction. **Hē** is the subject and **hit** the concealed matter; **self** reinforces the subject rather than supplying another finite verb.'],
'R05':[
'The **king, Arcestrates**, is the outer speaker, introduced by **Ðā cwæð se cyning**.',
'His **messenger**, the man who has just returned with the report, is the immediate addressee of singular **Gā** and **sęge**. Apollonius is elsewhere at this point.',
'**Him** denotes **Apollonius**, the dative recipient of the message after sęge.',
'**Se cyning** inside the proposed message denotes **the same king, Arcestrates**. The king gives the messenger wording that names him in the third person.',
'Inner **ðē** and **ðū** both denote **Apollonius**, the person who will hear the invitation. **Ðē** is the accusative person whom the king asks; **ðū** is nominative subject of **cume**. Their referent is not the messenger merely because the king is currently addressing him.',
'The outer **sęge him ðæt** begins a report, but what follows is quoted wording with second-person address: **se cyning bitt ðē ðæt ðū cume tō his gereorde**. Cook’s note15 calls this a mixture of direct and indirect construction. Preserve that mixture when explaining the source; a smooth indirect paraphrase can explain its meaning but cannot replace the wording being analysed. **Cume** is present subjunctive in the request; English can render the request with “asks you to come.”'],
'R06':[
'“The king then recognized the young man’s agility, so that he knew that he had no equal in that game.” This preserves the repeated pronouns and the negative **næfde** rather than silently deciding all their referents.',
'Original note6 says the clause is unclear. Its Latin parallel has the king knowing that he himself had no equal; the Old English’s sequence and repeated hē/his leave room for discussion, including a reading in which the young man is the one without an equal. A proposed reading should name its referents and acknowledge that limit. Dropping ne from næfde, or changing the whole clause to “he had found his equal,” is not a translation of the printed wording.',
'“With a skilled hand he swung the top—apparently the ball—with such great speed that it seemed to the king as though he had been changed from old age back to youth.” The king experiences the seeming return to youth; Apollonius performs the action.',
'Original note10 says that the Old English departs from the Latin. The English help for the Latin describes rubbing/anointing the king with ointment so rapidly that he seemed young again. Cook only tentatively identifies **top** with **ðoðor**. Translate **swang ðone top**, mark the uncertain object, and do not substitute the ointment action for the Old English event.']}
put('## A. Reference, clause structure and time');put()
for k in ['A01','A02','A03']:
    tid='NEW-U16-'+k;begin(tid)
    for n,text in enumerate(original[k],1):answer(tid,n,text)
    if k=='A01':put('The explicit noun phrases must be nominative subjects. A nearest-noun rule would erase the real ambiguity; replacing more than hē would also miss the restricted rewriting task.');put()
put('## C. Short compositions');put()
for k in ['C01','C02','C03']:
    tid='NEW-U16-'+k;begin(tid)
    for n,text in enumerate(original[k],1):answer(tid,n,text)

for exercise,count in [(32,11),(33,10),(34,13),(35,14),(36,11)]:
    put(f'## Cook XII, XIII.{exercise}');put()
    for n in range(1,count+1):
        tid=f'EX-XII-XIII-{exercise}-{n:02d}';short=f'{exercise}-{n:02d}'
        begin(tid,f'Cook XII, XIII.{exercise}.{n}')
        put(CM[tid]['model']);put()
        put('<!-- output: '+tasks[tid]['output_positions'][0]['output_position_id']+' -->');put()
        meaning,note=COOK[short]
        put('**Meaning:** '+meaning);put();put(note);put()

put('## R. The gymnasium scene');put()
begin('NEW-U16-R01')
witness=(R/'chapters/ch16/author-translation-witness.md').read_text(encoding='utf8')
translation=witness.split('## Translation\n\n',1)[1].split('\n\n## Decisions',1)[0]
# Root identified the grammatical singular plega after the witness was preserved.
translation=translation.replace('equipment for young men’s games belonging to the baths','equipment for young men’s play belonging to the baths')
answer('NEW-U16-R01',1,translation)
put('This model retains every stage from arrival to invitation. **Plegan** at168.6 is grammatical accusative singular; “equipment for young men’s play” is a contextual rendering, not a claim that the Old English noun is plural. “Bath,” “baths” or “bathing place” can render the facility without changing the action.');put()
put('The pronouns in the ball exchange are interpreted from the game sequence. At 169.5–7, however, the model deliberately leaves “he knew that he had no equal” unresolved; **næfde** must stay negative. At 169.11–13, **top** is retained with Cook’s tentative ball interpretation. “Our common safety,” “common welfare” or a carefully explained religious rendering may express the oath at 170.2; none should add an event. See R06 for the two substantial textual uncertainties.');put()
put('The final invitation is intentionally awkward in English because the source combines an outer report with quoted second-person address. A fluent paraphrase may explain the intended message, but a complete translation should acknowledge the actual mixture rather than conceal it. The following feast is not part of this reading.');put()
for k in ['R02','R03','R04','R05','R06']:
    tid='NEW-U16-'+k;begin(tid)
    for n,text in enumerate(original[k],1):answer(tid,n,text)
text=unicodedata.normalize('NFC','\n'.join(parts).rstrip()+'\n')
text=re.sub(r'\b(Cook|sentence|note|at|in)(?=\d)',r'\1 ',text).replace('strongIII','strong III')
(R/'chapters/ch16/answer-key.md').write_text(text,encoding='utf8')
print('Wrote Unit16 answer key:',len(text),'characters')
