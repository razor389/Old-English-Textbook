"""Author-owned key assembly from frozen models and independently written explanations."""
from pathlib import Path
import hashlib,json,re,unicodedata
ROOT=Path(__file__).resolve().parents[1]
C=json.loads((ROOT/'chapters/ch17/coverage.json').read_text(encoding='utf8'))
TASKS={t['task_id']:t for t in C['assigned_items']}
COOK={s['owner_id']:s['text']for s in json.loads((ROOT/'curriculum/proposals/unit17/author-only-cook-sequence-bindings.json').read_text(encoding='utf8'))['sequences']}
MODELS={}
for name in ['author-only-original-sequence-bindings.json','author-only-form-bindings.json']:
 for s in json.loads((ROOT/'curriculum/proposals/unit17'/name).read_text(encoding='utf8'))['sequences']:
  oid=s['output_position_id']
  if oid in MODELS:assert MODELS[oid]==s['text']
  MODELS[oid]=s['text']
WITNESS=(ROOT/'chapters/ch17/key-author-reading-translation-witness.md').read_text(encoding='utf8')
WP=WITNESS.strip().split('\n\n')

ANSWERS={
'A01':[
"""**Se cyning** is the nominative subject of **sægde**, preterite indicative third singular. **Se mann** is the nominative subject of **wǣre**, preterite subjunctive third singular. The king speaks; the reported goodness belongs to the man.""",
"""**Ðæt** introduces the content of the statement, “that the man was good”; it is a conjunction here. The task places that goodness at the time of the king's past statement. Thus past **wǣre** does not by itself mean that the goodness preceded the statement. Calling ðæt a relative pronoun would give it an unneeded participant role.""",
"""No. The subjunctive marks the embedded report; it does not establish that the man was bad or that the report was false. A translation such as “The king said that the man was good” preserves both the report and the stated simultaneity. An interpretation of earlier goodness or present contrary fact misses the supplied context."""],
'A02':[
"""“The man sang better than the king did.” The man is the better singer in this comparison. “Better than the king sang” expresses the same meaning in English; reversing the two performers does not.""",
"""**Dyde** substitutes for the action “sang.” It is third singular because its own subject is **se cyning**, independently of the first clause's subject. It does not mean that the king performed some unspecified different action.""",
"""**Ðā męnn** and **sungon** replace the first singular subject and verb. The singular **se cyning dyde** stays intact. Pluralizing dyde would change the second performer; retaining sang would leave the first clause without the requested plural agreement."""],
'A03':[
"""**Ðone mann** is accusative singular, the direct object of **geseah**: the person whom I saw. Its role in the seeing clause determines that case.""",
"""Inside the relative clause, **ðe** represents the singer and functions as subject of **sang**. The particle is invariant. Its antecedent's accusative case in the outer clause does not make the relative's internal role accusative.""",
"""The object becomes **ðā męnn** and the relative verb becomes **sungon**. **Ic geseah** remains first singular: the same speaker saw several men. A different defensible order is possible, but changing the speaker to a plural subject changes the task."""],
'A04':[
"""A: “If he comes, I shall go.” **Cymð** is present indicative third singular; **fare** is present indicative first singular in this stated setting. Tomorrow supplies future reference. An indicative condition is possible after gif; no separate future auxiliary is needed.""",
"""B: “If he were coming now, I would go,” or “If he came now, I would go.” **Cōme** is preterite subjunctive third singular and **fōre** preterite subjunctive first singular. Here those past forms express the stipulated contrary-to-fact present situation, not a completed past visit.""",
"""The task's possible visit tomorrow versus contrary-to-fact coming now supplies the time and factual setting. The forms distinguish the two selected constructions, but **gif** alone fixes neither a universal mood nor a time. A translation of B as “If he had come, I would have gone” changes the given time relation."""],
'F01':[
"""**Ðæs cnihtes** is the singular genitive possessor; **bōc** is the singular head. The book does not become genitive merely because its owner is genitive. The assigned sense of cniht is servant.""",
"""**Ðāra cnihta** is genitive plural and **bēc** is the plural head: several servants' books. The changed vowel in bēc belongs to the book paradigm; a regularized plural would miss the selected form.""",
"""**Ic giefe** is first singular present; **ðǣm cnihte** is the dative recipient and **ðā bōc** the accusative thing given. Changing the order of the two objects can preserve the meaning; exchanging their case roles cannot.""",
"""**Wē giefað** is first plural. Both objects change number: dative **ðǣm cnihtum**, accusative **ðā bēc**. Giefað is an assertion with wē here, despite sharing its spelling with a plural command form."""],
'F02':[
"""The queen is the accusative object of seeing: **ðā cwēn**. The endingless cwēn is the explicitly selected accusative. Documented **cwēne** can be a valid accusative alternative, but does not meet this task's endingless-form target.""",
"""**Ðǣre cwēne** is the dative recipient; **ðā bōc** is the accusative gift. The endingless accusative option does not license dropping the dative -e.""",
"""**Ðǣre cwēne** is genitive singular, dependent on **bōc**: the book belongs to the queen. Its spelling matches the preceding dative, while its grammatical function differs.""",
"""**Cwēn** is accusative in the seeing clause even without an ending; **cwēne** is dative as recipient and genitive as possessor. The governing construction and article identify the case. An unchanged ending is not proof of an unchanged grammatical role."""],
'F03':[
"""**Se fox** is nominative masculine singular. **On ðǣm hole** is a dative location, not movement into a hole. **Is** agrees with the single fox.""",
"""**Ðā foxas sindon** gives plural subject and verb; **on ðǣm holum** gives dative plural location. Changing foxas alone would leave the other requested number changes incomplete.""",
"""**Ðæt nest** is the singular subject. The tree is locative dative **trēowe**, with the documented w before the ending. This is a nest located in a tree, not a nest moving toward one.""",
"""Nominative plural **nest** has no overt plural ending; **ðā** and **sindon** make its plural function clear. **Trēowum** is dative plural. An unchanged nest does not justify singular is.""",
"""The short neuter **hol** has nominative plural **holu**, whereas heavy **nest** has a zero ending. Predicate **miclu** is strong neuter plural. An article in the subject does not turn the separate predicate adjective weak."""],
'F04':[
"""Present indicative third plural: several people praise. This is the narrator's assertion, not a wish.""",
"""Second-plural imperative: several listeners are commanded to praise. Its spelling coincides with the indicative answer, but its addressees and function differ.""",
"""Present subjunctive third plural: may they praise. The wish is expressed by the **-en** form; adding a verb meaning “be permitted” would change the construction.""",
"""The first two answers, **hęriað**, are spelled alike. The assertion has third-plural subject reference; the command addresses the second plural. **Hęrien** has the separate subjunctive ending. The supplied infinitive identifies the verb; choosing the finite ending and analysis is the work required."""],
'F05':[
"""The nominalized participle **ondrǣdendum** is dative plural, naming the beneficiaries. **Hine** is accusative singular, the person they fear. No separate people noun or finite fear verb is required.""",
"""**Ðā hyngrendan** is the article plus weak accusative plural participle: the hungry people as direct object. It does not express an impersonal finite “they hunger” construction.""",
"""The whole fear phrase is dative because of its beneficiary role. Within that phrase, **ondrǣdan** governs accusative **hine**. The dependent object does not copy the phrase's outer dative case.""",
"""A participle can be used substantivally for people characterized by an action or condition. It then takes the case, number and strong/weak endings required by that noun phrase. “Present participle” names its form; it does not supply finite person agreement or an independent present-tense assertion."""],
'C01':[
"""The king is the singular subject of **geseah**; **ðā męnn** is its accusative plural object. The invariant **ðe** represents those men as the subject of plural **sungon**. A demonstrative relative can be grammatical elsewhere, but this task requests the invariant particle."""],
'C02':[
"""The two **swā** markers express equal degree: the king is as good as the men. **Gōd** is the singular predicate of the king, while **sindon** agrees with the men in the comparison clause. A comparative meaning “better than” would reverse the requested equality."""],
'C03':[
"""**Cymð** is an indicative in the open future condition. **Giefað** addresses several listeners; **him** is the dative recipient and **ðā bōc** the accusative gift. A singular command would be valid for one listener but would miss the explicit plural target."""],
'C04':[
"""**Se mann** speaks; **se cyning** is the subject of the reported goodness. **Sīe** is present subjunctive third singular, as explicitly requested. An indicative can assert certainty in a reported clause, but would not meet this stated mood target. The report need not be false."""],
'A05':[
"""The first clause identifies **ǣlc flǣsc**, each/all flesh, with **gærs**, grass, through **is**. In context the physical image suggests human frailty and transience. Calling the clause metaphorical does not remove either noun from its translation.""",
"""The second compares the flesh's **wuldor**, glory, with the plants' **blōstma**, blossom, using **swilce**. The first is a copular identification; the second marks an explicit comparison. Both flesh/grass and glory/blossom must remain. No separate hypothetical event is asserted merely by the English help “as if.”""",
"""“Human life is brief” may summarize an implication, but omits both images, the reference to glory, and their different grammatical constructions. A complete translation retains what is said and then may explain its force. Interpretive paraphrase alone does not answer the composition task."""],
'A06':[
"""In 37.14 raising the **horn** can be understood as exalting the people's strength or power in the praise context. This interprets the image while retaining literal horn in the translation; it does not independently establish a replacement dictionary gloss. The clause is not a report about a literal animal.""",
"""In 40.9 **his sǣde** denotes Abraham's offspring or descendants collectively. The possessor is Abraham, not the speaker or God. “His seed” preserves the image; “his descendants” explains the newly taught collective sense. This analysis task keeps the lexical help available.""",
"""Recognizing a noun's case or paradigm does not determine its contextual sense. The same familiar shape could occur in a literal horn or agricultural seed context. Here context guides interpretation of the horn image, while seed requires its newly taught collective meaning and the correct possessor. The task's help remains available; an ending alone establishes none of these choices."""],
'R01':[
'\n\n'.join(WP[2:4])+"\n\n**Points to retain:** she orders the harp fetched; she combines song and harp; Apollonius alone is silent; the king treats that silence as criticism. “Had her harp fetched” is equivalent. Saying that she fetched it herself changes the causative wording.",
'\n\n'.join(WP[4:6])+"\n\n**Points to retain:** **gelīefst** grants permission to speak. **Mē** in the following harp command is the recipient, not the commanded giver. The daughter has chanced upon music but has not mastered it. “Then you will know what you do not yet know” preserves the future consequence; no contrary-to-fact condition is asserted.",
'\n\n'.join(WP[6:8])+"\n\n**Points to retain:** the king has the harp handed to Apollonius; Apollonius dresses and performs; the audience supposes him to be Apollo. The final verbs describe setting down the harp, acting, and presenting performances. “Things” may replace “performances” if their context is clear. The source's singular **ungecnāwen wæs** is retained in analysis even where idiomatic English uses a plural relative."
],
'R02':[
"""**Hēo** is the king's daughter. Its feminine singular form is compatible with that referent, but the preceding context identifies the particular woman. The form alone does not name her.""",
"""**Hine** refers to masculine **swēgcræft**, musical art. It is the accusative object of **geleornod** in the negative perfect: she has not learned it well. Masculine grammatical gender does not make the referent the king or Apollonius.""",
"""Both instances of **hē** refer to Apollonius, the man whom the audience sees. The clauses report their supposed identification: not Apollonius, but Apollo. They do not change the actual referent into a god.""",
"""**Him eallum** refers to all the listeners and is dative plural, the people pleased by the performances. Context supplies the group; the dative construction with **līcode** supplies their experiencer role. They are not its grammatical subject."""],
'R03':[
"""**Sōna swā** introduces “as soon as.” The start of the harp playing is immediately accompanied by the blending of harp sound and song. Here swā is part of the supplied temporal expression, not an assertion that two performers are equally skilled.""",
"""**Gif ðū mē gelīefst** is an open permission condition: “if you permit me [to speak].” **Gelīefst** is present indicative second singular; the following **ic sęcge** states what the speaker will say. It is neither a request to believe a proposition nor a condition assumed contrary to fact.""",
"""In **swā stōd ðæt**, the manner or degree of his stance/appearance leads to a result: the audience takes him for Apollo. This **swā … ðæt** is not the equal-degree **swā … swā** of C02 or the temporal sōna swā at the reading's beginning.""",
"""The two clauses are the contents of **wēndon**, “they supposed”: that he was not Apollonius and that he was Apollo. **Nǣre/wǣre** are past subjunctives in that report. The stated thought explains the mistaken identification; the narrator does not assert an actual transformation."""],
'R04':[
"""Original note 12a says “For **swīgiende**.” Printed **swīgende** is a present participle: remaining silent accompanies the addressee's censure. It is not an independent finite verb. Preserve the edition's swīgende in the source and identify the supplied expansion in analysis.""",
"""**Ðā ymbsittendan** means the people sitting around, the spectators or bystanders. It is a weak nominalized present-participle expression. Together with the king, they supply the plural subject of **wēndon**; no actual people noun need be restored to the text.""",
"""The source construes the display of **fela fægerra ðinga** collectively in the following singular predicate **ungecnāwen wæs and ungewunelic**. Retain that wording and its supplied local explanation. It does not license a universal rule making every plural subject singular, nor does a smoother English plural authorize silently changing the Old English.""",
"""The subject is **ǣlc ðāra ðinga**, each of those things, hence singular **līcode**. **Him eallum** is dative plural, the people to whom each performance was pleasing. Its plurality does not control the verb."""],
'R05':[
"""The image is of falling upon musical art; original note 15 gives the contextual translation “has chanced.” Here the daughter has chanced upon or taken up music without learning it well. Treating **on swēgcræft** as a physical place into which she fell would miss the supplied idiom.""",
"""**Plegode** means acted or performed; **forðtēah** means presented the performances. Original note 6 connects the passage with comic and tragic acting, while note 8 supports the presentation sense. “Played” can work in a clearly theatrical English rendering; playing a ball game or literally drawing objects forward does not express this scene. The Latin note is explanatory evidence, not extra wording to insert into the OE translation.""",
"""**Apollines** identifies Apollo, as original note 2 states. It is the name used in what the spectators suppose. Preserve that reported identification and the source form; do not mistake it for a second occurrence of Apollonius's name or claim that the man really became Apollo."""],
'R06':[
"""The king treats Apollonius's silence as blame and therefore as bad conduct toward his daughter. Apollonius explains a technical judgment: she has encountered music but has not learned it well. He seeks permission to speak and offers a demonstration, rather than denying that his silence conveys criticism.""",
"""He demonstrates skilled harp playing joined with pleasant song, then displays further striking performances after putting down the harp. The listeners respond by shouting praise and taking pleasure in what he presents. Equivalent answers can describe the two kinds of performance in their own words; a bare claim that he is talented does not identify the evidence in the passage.""",
"""The performances are unfamiliar and unusual to the people, yet each greatly pleases all of them. Novelty and approval coexist. “Unknown” does not mean bad or displeasing here, and the final dative experiencers identify the approving audience."""],
}

COOK_NOTES={}

FRONT="""# Unit 17. Answer key

The composition models are new teaching material. The reading translation renders Cook's actual Old English and was prepared independently before comparison with other authorial translations. Each model is one defensible answer: preserve the participants, essential meaning, case relations, agreement, mood and clause connections, together with the task's explicit lexical, number, omission and order controls. A grammatical alternative can miss a stated target. All seven Cook sets retain the original joint group **XII, XIII**.

The supplied phrases and exact dictionary hints remain visible. Copying a given citation is not a test of independent recall; selecting the required ending, person, number or role may still be the task. The complete local numeral expressions, unusual reading frames and figurative supports are not invitations to reconstruct an untaught system unaided. English analytical answers may use equivalent precise terminology.

Except where an order is specified, grammatical rearrangements that preserve the relationships are acceptable. Documented spelling and inflectional variants must be distinguished from mistakes: for example, **ðām** beside selected **ðǣm**, or a licensed feminine plural **-e** beside a selected **-a**. Such variants do not excuse wrong case, person or sense. The selected tables govern tasks that expressly ask for their forms.[^key-sources]
"""

def original(label):
 t=TASKS['NEW-U17-'+label];answers=ANSWERS[label]
 assert len(answers)==len(t['output_positions']),(label,len(answers),len(t['output_positions']))
 out=['### '+label,'<!-- key: '+t['key_id']+' -->','**Task:** '+t['prompt']]
 for s in t.get('input_texts',[]):out.append('**Input:** '+s)
 for p,answer in zip(t['output_positions'],answers):
  oid=p['output_position_id'];out+=['<!-- output: '+oid+' -->','**'+p['label']+'**']
  if oid in MODELS:out.append('**'+MODELS[oid]+'**')
  out.append(answer)
 return '\n\n'.join(out)

def cook(exercise):
 out=['## Cook '+str(exercise)]
 if exercise==37:
  out+=['**Cook\'s instruction:** '+TASKS['EX-XII-XIII-37-01']['source_instructions'][0]['original_text'],
  'This instruction applies to all fourteen items. Retain necessary third-person pronouns such as **hīe** in the praise wishes, but omit an article and an independent second-person subject throughout. The noun catalogues in 37.8–12 continue the address; they need not be converted into fresh finite sentences. Accompanying descriptive adjectives use the selected weak address forms, while **eall** retains its separately taught strong pattern.']
 elif exercise==39:out.append('Items 39.1–4 complete the exchange concerning Solomon. Items 39.5–7 change to the building image and divine reward; they are not further events in the queen\'s visit.')
 elif exercise==40:out.append('Simple preterites can render the English perfect in this passage. Where an English helper is expressly omitted, retain that target. An appropriately formed analytic perfect can be valid elsewhere; its mere resemblance to English is not required here.')
 elif exercise==42:out.append('Keep the complete supplied frames available, especially the genitive harper phrase, the 144,000 exception, the collective company description and the blessing formula. Their unfamiliar components are not separate recall tests.')
 for tid,t in TASKS.items():
  if not tid.startswith('EX-')or t['original_exercise']!=exercise:continue
  short=f"{exercise}.{t['original_item']}";p=t['output_positions'][0]
  out+=['### Cook '+short,'<!-- key: '+t['key_id']+' -->',COOK[tid],
  '<!-- output: '+p['output_position_id']+' -->',"**Cook's prompt:** "+t['prompt'],
  '**Target and explanation:** '+COOK_NOTES[short]]
 return '\n\n'.join(out)

def write():
 assert len(COOK_NOTES)==82
 out=[FRONT.strip(),'## A. Clauses and participants']
 out += [original('A'+f'{i:02}')for i in range(1,5)]
 out += ['## F. Forms and grammatical roles']+[original('F'+f'{i:02}')for i in range(1,6)]
 out += ['## C. Composition']+[original('C'+f'{i:02}')for i in range(1,5)]
 out += [cook(i)for i in range(37,44)]
 out += ['## A. Figurative meaning',original('A05'),original('A06'),'## R. The music performance']
 out += [original('R'+f'{i:02}')for i in range(1,7)]
 out += ["[^key-sources]: Cook, *Exercises in Old English* (1895), XII, XIII.37–43, printed pp. 22–28 (PDF 30–36); *A First Book in Old English*, second edition (1895), especially §§55, 153–166, 183, 188, 194–197 and Reader XII, 174.7–175.17 (PDF 190–191). Individual line references count physical prose lines from the edition's printed marginal anchors. The supplied 144,000 expression is independently attested in Bosworth–Toller, main dictionary p. 1082, **þūsend** I(2)(a), citing *Pastoral Care* 52; its acute length signs are represented by Cook-style macrons. The readings and original note numbers remain those of the selected editions."]
 text=unicodedata.normalize('NFC','\n\n'.join(out)+'\n')
 (ROOT/'chapters/ch17/answer-key.md').write_text(text,encoding='utf8',newline='\n')
 print('Wrote key:',len(text.split()),'whitespace words')

if __name__=='__main__':
 exec((ROOT/'build/u17-key-cook-notes.py').read_text(encoding='utf8'))
 write()
