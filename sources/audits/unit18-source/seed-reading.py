"""Primary transcription of the inspected love/gifts/banquet-departure episode."""
import json
import pathlib
import re
import unicodedata

OUT = pathlib.Path(__file__).parent
lines = {
175: (18, '''Sōðlice, mid-ðȳ-ðe ðæs cyninges dohtor geseah ðæt Apol-
lonius on eallum gōdum cræftum swā wel wæs getogen,[10]
ðā gefēoll hiere mōd on his lufe. Ðā, æfter ðæs bēorscipes
geęndunge, cwæð ðæt mǣden tō ðǣm cyninge: “Lēofa[11]'''),
176: (1, '''fæder, ðū līefdest mē, lȳtle[1] ǣr,[1] ðæt[2] ic[2] mōste[2] giefan
Apollonio swā-hwæt-swā ic wolde of ðīnum goldhorde.”
Arcestrates se cyning cwæð tō hiere: “Gief him swā-
hwæt-swā ðū wille.[3]” Hēo ðā swīðe blīðe ūtēode,[4] and
cwæð: “Lārēow[5] Apolloni, ic giefe ðē, be mīnes fæder
lēafe, twā hund punda[6] goldes,[7] and fēower hund punda[6]
gewihte[8] seolfres,[7] and ðone mǣstan dǣl dēorwurðes[9]
rēafes, and twēntig ðēowa[10] manna.[10]” And hēo ðā ðus
cwæð tō ðǣm ðēowum mannum: “Berað ðās ðing mid
ēow, ðe ic behēt Apollonio mīnum lārēowe, and lęcgeað
innan būre[11] beforan mīnum frēondum.” Ðis wearð ðā
ðus gedōn, æfter ðǣre cwēne hǣse[12]; and ealle ðā męnn
hiere giefa hęredon ðe[13] hīe gesāwon. Ðā sōðlice geęnd-
ode se gebēorscipe, and ðā męnn ealle ārison,[14] and
grētton ðone cyning and ðā cwēne, and bǣdon hīe
gesunde bēon,[15] and hām gewęndon. Ēac swilce Apol-
lonius cwæð: “Ðū gōda cyning, and earmra[16] gemiltsiend,
and ðū cwēn, lāre[16] lufiend, bēon gē gesunde.[17]” Hē
beseah ēac tō ðǣm ðēowum mannum, ðe ðæt mǣden him
forgiefen hæfde,[18] and him cwæð tō: “Nimað ðās ðing mid'''),
177: (1, '''ēow, ðe mē sēo cwēn forgeaf, and gān[1] wē sēcean ūre
giesthūs, ðæt wē mægen ūs[2] geręstan.”'''),
}
source_lines = []
for p, (start, block) in lines.items():
    for n, line in enumerate(block.splitlines(), start):
        source_lines.append(dict(source_line_id=f'FB{p}-{n:02}', printed_page=p,
            pdf_page_one_based=p+16, editorial_line=n,
            source_with_note_markers=unicodedata.normalize('NFC', line)))
joined = ' '.join(x['source_with_note_markers'] for x in source_lines)
text = re.sub(r'\[(\d+[a-z]?)\]', '', joined)
for a, b in [('Apol- lonius', 'Apollonius'), ('swā- hwæt-swā', 'swā-hwæt-swā'), ('geęnd- ode', 'geęndode')]:
    text = text.replace(a, b)
span = dict(source_span_id='FB-XII-APOLLONIUS-LOVE-GIFTS-DEPARTURE',
    title='The princess’s gifts and the end of the banquet', source_id='cook_fb_1895_2',
    original_identifier='Reader XII, A Lesson in Music, closing love/gifts and banquet-departure episode',
    origin_category='exact source with declared layout normalization', printed_pages=[175,176,177],
    pdf_pages_one_based=[191,192,193], source_lines=source_lines, learner_text=text, word_count=len(text.split()),
    boundaries=dict(start='175.18 Sōðlice, mid-ðȳ-ðe', end='177.2 ðæt wē mægen ūs geręstan.',
        before='The music demonstration and audience approval, ending ðe hē forðtēah., were assigned in Unit17.',
        after='The printed heading Apollonius as Teacher and the princess’s arrangements for his lodging begin the next episode; they remain unassigned.',
        reason='Complete connected love/gifts/banquet-departure episode, closing at the printed subsection boundary.'),
    line_convention='Individual line numbers are editorial counts of physical prose lines anchored by printed marginal 5/10/15/20. Headings are not prose lines.',
    evidence_refs=['U18-FB-P175','U18-FB-P176','U18-FB-P177'])
data = dict(schema_version=1, source_spans=[span], total_word_count=span['word_count'],
    normalizations=['Keep exact linguistic spelling, macrons, punctuation and clause order.',
        'Separate original superscript note cues from learner text; retain all cues and original notes in source/apparatus records.',
        'Join physical line/page breaks; join typographic Apol-/lonius and geęnd-/ode. Rejoin the line-broken lexical swā-hwæt-swā without removing its lexical hyphens.',
        'Use Unicode curly quotation marks and collapse layout spacing before punctuation.'],
    status='source audit; assignment awaits coordinator contract')
(OUT/'reading-source.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

notes = {
175: {'10':'See getēon. What relation has getogen to Mod. Eng. wanton?', '11':'See 55.'},
176: {'1':'Lat. paulo ante. See 178.', '2':'Translate by the infinitive sign, to. The OE. follows the Latin.',
    '3':'See 197.', '4':'Not in Latin.', '5':'Lat. magister.', '6':'See 154. c.',
    '7':'See 153. f.', '8':'See 174.', '9':'MS. deorwurðan.', '10':'Lat. servos.',
    '11':'Lat. triclinio.', '12':'See the derivation of Mod. Eng. behest.', '13':'Refers to męnn.',
    '14':'So in Beowulf (653–655):\n“Werod eall ārās; grētte ðā . . .\nguma ōðerne, . . . and him hǣl\nābēad.”',
    '15':'Lat. vale dicentes.', '16':'See 153. d.', '17':'Lat. valete.', '18':'See 188.'},
177: {'1':'See 193. a.', '2':'See 184. b.'},
}
outnotes = []
for p, ns in notes.items():
    for num, note in ns.items():
        anchors=[]
        for line in source_lines:
            if line['printed_page'] != p: continue
            for m in re.finditer(r'\['+num+r'\]',line['source_with_note_markers']):
                before = line['source_with_note_markers'][:m.start()]
                anchors.append(dict(source_line_id=line['source_line_id'],editorial_line=line['editorial_line'],
                    anchor_text=before.split()[-1],character_offset=m.start()))
        assert anchors,(p,num)
        outnotes.append(dict(apparatus_id=f'FB-U18-{p}-N{num}',source_id='cook_fb_1895_2',printed_page=p,
            pdf_page_one_based=p+16,original_note_number=num,original_text=note,
            origin_category='exact source with declared typographic normalization',anchors=anchors,
            disposition='Retain original apparatus separately from modern support. The etymological question and Beowulf comparison are source notes, not independent learner tasks or poetry assignment.',
            evidence_refs=[f'U18-FB-P{p}']))
(OUT/'reading-apparatus.json').write_text(json.dumps(dict(schema_version=1,notes=outnotes,count=len(outnotes),
    anchor_count=sum(len(n['anchors']) for n in outnotes),normalizations=['Unicode punctuation; joined layout word divisions; original quoted verse lineation retained.']),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

witness = dict(schema_version=1,status='independent initial translation from actual Old English, before chapter key',
    source_span_id=span['source_span_id'], origin_category='new editorial translation; not Cook’s source English',
    translation=[
    'Indeed, when the king’s daughter saw that Apollonius was so well educated in all good accomplishments, her heart fell in love with him. Then, after the conclusion of the banquet, the maiden said to the king: “Dear father, you allowed me a little while ago to give Apollonius whatever I wished from your treasury.”',
    'King Arcestrates said to her: “Give him whatever you wish.” She then went out very gladly, and said: “Master Apollonius, by my father’s permission I give you two hundred pounds of gold, and four hundred pounds by weight of silver, and the greatest part of the precious clothing, and twenty slaves.”',
    'And she then said this to the slaves: “Carry with you these things which I promised Apollonius my teacher, and put them in the chamber before my friends.” This was then done in accordance with the princess’s command; and all the men who saw her gifts praised them.',
    'Then the banquet ended, and all the men rose and greeted the king and the princess, wished them well, and went home. Apollonius likewise said: “Good king, benefactor of the poor, and you, princess, lover of learning, farewell.”',
    'He also looked towards the slaves whom the maiden had given him, and said to them: “Take with you these things which the princess gave me, and let us go to seek our guesthouse, so that we may rest.”'
    ], uncertainties_and_limits=[
        'The temporal repetition of the banquet’s conclusion in the source is retained; no event is silently omitted or reordered.',
        'Getogen is educated/trained here; it is not literal physical dragging.',
        'Cwēn in this passage denotes the king’s daughter/princess; she is not a different queen.',
        'Gewihte is the actual dative singular phrase by weight, qualifying the amount of silver.',
        'Cook’s note13 makes męnn the antecedent of ðe; hīe in hīe gesāwon is the plural object giefa, not the woman as subject.',
        'Bǣdon hīe gesunde bēon and bēon gē gesunde are literal wishes that the addressees be well; their discourse function is farewell.',
        'Gān is the exhortative plural subjunctive, let us go; sēcean is the dependent infinitive.',
        'Forgiefen hæfde identifies the gift as earlier than the look and instruction; no modern perfect rule is inferred from this single passage.',
        'Būr is translated chamber; original note11 supplies the Latin dining-room setting without changing the Old English lexical text.'
    ])
(OUT/'author-only-reading-translation-witness.json').write_text(json.dumps(witness,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
context = dict(schema_version=1,origin_category='new teaching material: English context derived from preceding source',
    text='Apollonius, a shipwrecked prince, is a guest at King Arcestrates’s banquet. After the king’s daughter plays and sings, Apollonius demonstrates his own skill and wins the admiration of everyone present.',
    evidence_refs=['U18-FB-P175'],limits='English context only; no additional Old English narrative or teaching milestone is assigned.')
(OUT/'reading-context.json').write_text(json.dumps(context,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'words':span['word_count'],'lines':len(source_lines),'notes':len(outnotes),'anchors':sum(len(n['anchors']) for n in outnotes)}))
