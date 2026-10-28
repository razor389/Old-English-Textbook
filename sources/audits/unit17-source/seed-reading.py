"""Exact bounded performance text and its original apparatus, from viewed images."""
import hashlib
import json
import pathlib
import re
import unicodedata

OUT=pathlib.Path(__file__).parent
ROOT=OUT.parents[2]
lines={174:(7,'''Ðā ēode hēo ūt,[9] and hēt fęccean hiere hearpan. And
sōna swā hēo hearpian ongan, hēo mid wynsumum sange
gemęngde ðǣre hearpan swēg. Ðā ongunnon ealle ðā
męnn hīe hęrian on hiere swēgcræfte; and Apollonius
āna[10] swīgode. Ðā cwæð se cyning: “Apolloni, nū ðū
dēst[11] yfele, for-ðǣm-ðe ealle męnn hęriað mīne dohtor
on hiere swēgcræfte,[12] and ðū āna hīe, swīgende,[12a] tǣlst.[13]”
Apollonius cwæð: “Ēalā, ðū gōda cyning, gif ðū mē
gelīefst,[14] ic sęcge ðæt ic ongiete ðæt sōðlice ðīn dohtor
gefēoll[15] on swēgcræft, ac hēo næfð hine nā wel geleornod;
ac hāt mē[16] nū sęllan ðā hearpan, ðonne wāst[17] ðū nū ðæt
ðū gīet nāst.[17]” Arcestrates se cyning cwæð: “Apolloni,'''),
175:(1,'''ic oncnāwe sōðlice ðæt ðū eart[1] on eallum ðingum wel
gelǣred.”
Ðā hēt se cyning sęllan Apollonie ðā hearpan. Apol-
lonius ðā ūtēode, and hine scrȳdde, and sętte ænne
cynehelm upon his hēafod, and nōm ðā hearpan on his
hand, and inēode, and swā stōd ðæt se cyning and ealle
ðā ymbsittendan wēndon ðæt hē nǣre Apollonius, ac ðæt
hē wǣre Apollines,[2] ðāra hǣðenra god. Ðā wearð stilnes
and swīge[3] geworden innan ðǣre healle. And Apollonius
his hearpenægl genōm, and hē ðā hearpestręngas mid
cræfte āstyrian ongan, and ðǣre hearpan swēg mid wyn-
sumum sange gemęngde.[4] And se cyning self, and ealle
ðe ðǣr andwearde wǣron, micelre stefne cleopedon and
hine hęredon. Æfter ðisum forlēt[5] Apollonius ðā hearpan,
and[6] plegode, and fela fægerra ðinga[7] ðǣr forðtēah,[8] ðe
ðǣm folce ungecnāwen wæs and ungewunelic. And him[9]
eallum ðearle līcode ǣlc ðāra ðinga ðe hē forðtēah.''')}
source_lines=[]
for p,(start,block) in lines.items():
    for n,line in enumerate(block.splitlines(),start):
        source_lines.append(dict(source_line_id=f'FB{p}-{n:02}',printed_page=p,pdf_page_one_based=p+16,
            editorial_line=n,source_with_note_markers=unicodedata.normalize('NFC',line)))
joined=' '.join(x['source_with_note_markers'] for x in source_lines)
text=re.sub(r'\[(\d+[a-z]?)\]','',joined).replace('Apol- lonius','Apollonius').replace('wyn- sumum','wynsumum')
span=dict(source_span_id='FB-XII-APOLLONIUS-MUSIC-PERFORMANCE',title='Apollonius and the music performance',
    source_id='cook_fb_1895_2',original_identifier='Reader XII, A Lesson in Music, opening performance episode',
    origin_category='exact source with declared layout normalization',printed_pages=[174,175],pdf_pages_one_based=[190,191],
    source_lines=source_lines,learner_text=text,word_count=len(text.split()),
    boundaries=dict(start='174.7 Ðā ēode hēo ūt',end='175.17 ðe hē forðtēah.',
        before='The king asks his daughter to fetch her harp and relieve the young man’s sorrow.',
        after='A new paragraph at 175.18 begins the princess’s love and subsequent gifts. This and the later dispersal are unassigned.',
        reason='The selected span contains the complete performance, criticism, demonstration and audience response; it is a bounded episode within the longer printed subsection.'),
    line_convention='Individual line numbers are editorial counts of the physical prose lines, anchored by printed marginal 5/10/15/20. The printed subsection heading is not a prose line.',
    evidence_refs=['U17-FB-P174','U17-FB-P175'])
data=dict(schema_version=1,source_spans=[span],total_word_count=span['word_count'],
    normalizations=['Keep exact linguistic spelling, macrons, punctuation and clause order.',
        'Remove original superscript note cues from the separate learner text; retain every cue and original note in the source/apparatus files.',
        'Join physical line/page breaks; remove only the two word-division hyphens Apol-/lonius and wyn-/sumum.',
        'Use Unicode curly quotation marks and collapse layout spacing around punctuation.'],
    status='source audit; proposed assignment awaits coordinator contract')
(OUT/'reading-source.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

notes={174:{'9':'Not in the Latin.','10':'See 79.','11':'See 140.','12':'Lat. arte musica.',
    '12a':'For swīgiende.','13':'Lat. vituperas.','14':'See 196. d.',
    '15':'Lat. incidit. Translate, has chanced.','16':'See 164. a.','17':'See 126.'},
175:{'1':'See 194, note.','2':'Apollo.','3':'We are reminded of Æn. II. 1, Conticuere omnes.',
    '4':'To this sentence there corresponds in the Latin: —\narripuit plectrum, animumque accommodat arti;\ncum chordis miscetur vox cantu modulata.',
    '5':'Lat. deponens.','6':'The rest of this sentence paraphrases: induit statum comicum et inauditas actiones expressit, deinde tragicum.',
    '7':'See 154. a, b.','8':'Lat. expressit.','9':'See 164. k.'}}
outnotes=[]
for p,ns in notes.items():
    for num,note in ns.items():
        anchors=[]
        for line in source_lines:
            if line['printed_page']!=p:continue
            for m in re.finditer(r'\['+num+r'\]',line['source_with_note_markers']):
                before=line['source_with_note_markers'][:m.start()]
                anchors.append(dict(source_line_id=line['source_line_id'],editorial_line=line['editorial_line'],
                    anchor_text=before.split()[-1],character_offset=m.start()))
        assert anchors,(p,num)
        outnotes.append(dict(apparatus_id=f'FB-U17-{p}-N{num}',source_id='cook_fb_1895_2',printed_page=p,
            pdf_page_one_based=p+16,original_note_number=num,original_text=note,
            origin_category='exact source with declared typographic normalization',anchors=anchors,
            disposition='Retain as original apparatus, separate from modern support. Original questions are not independent tasks unless explicitly assigned.',
            evidence_refs=[f'U17-FB-P{p}']))
(OUT/'reading-apparatus.json').write_text(json.dumps(dict(schema_version=1,notes=outnotes,count=len(outnotes),
    anchor_count=sum(len(n['anchors']) for n in outnotes),normalizations=['Unicode punctuation; joined typographic line-break words; Latin verse lineation retained.']),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

witness=dict(schema_version=1,status='independent initial translation prepared from actual Old English before any chapter key',
    source_span_id=span['source_span_id'],translation=[
    'Then she went out and had her harp fetched. As soon as she began to play the harp, she mingled the sound of the harp with a pleasant song. All the men then began to praise her for her musical skill; Apollonius alone remained silent.',
    'Then the king said: “Apollonius, you now behave badly, because all the men praise my daughter for her musical skill, and you alone, by being silent, criticize her.”',
    'Apollonius said: “Ah, good king, if you permit me, I say that I perceive that your daughter has indeed chanced upon music, but she has not learned it well. But have the harp given to me now; then you will know what you do not yet know.” King Arcestrates said: “Apollonius, I certainly recognize that you are well instructed in everything.”',
    'Then the king had the harp given to Apollonius. Apollonius went out, dressed himself, and put a royal crown on his head, and took the harp in his hand and came in. He stood in such a way that the king and all the people sitting around supposed that he was not Apollonius but Apollo, the god of the heathens. Then silence and stillness fell within the hall.',
    'Apollonius took his plectrum and began to move the harp strings skilfully, and mingled the sound of the harp with a pleasant song. The king himself and all who were present called out in a loud voice and praised him.',
    'After this Apollonius put down the harp and performed, and presented many beautiful things there which were unknown and unfamiliar to the people. Each of the things that he presented pleased them all greatly.'
    ],uncertainties_and_limits=[
    'The initial translation of gefēoll on swēgcræft follows Cook’s explicit has chanced, not a claim of expert mastery.',
    'Plegode and forðtēah express performance/presentation here. Cook’s Latin note expands this as comic and tragic acting; that expansion is separate from what the Old English explicitly says.',
    'Swīgende is the retained source spelling; original note 12a gives swīgiende.',
    'On hiere swēgcræfte is the respect in which she is praised; it is not spatial location.',
    'Ungecnāwen wæs and ungewunelic are singular despite the preceding fela ... ðinga; the rendering preserves the meaning without silently correcting the Old English agreement.'
    ])
(OUT/'author-only-reading-translation-witness.json').write_text(json.dumps(witness,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
context=dict(schema_version=1,origin_category='new teaching material: English context derived from the preceding source',
    text='After a shipwreck, Apollonius has reached the court of King Arcestrates. At the feast the king’s daughter asks about his misfortunes. The king then tells her to fetch her harp and ease the young man’s sorrow.',
    evidence_refs=['U17-FB-P172','U17-FB-P173','U17-FB-P174'],
    limits='English context only. It neither assigns the intervening Old English nor establishes its forms or constructions as taught.')
(OUT/'reading-context.json').write_text(json.dumps(context,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'words':span['word_count'],'lines':len(source_lines),'notes':len(outnotes),'anchors':sum(len(n['anchors']) for n in outnotes)}))
