from pathlib import Path
import copy,json,re
O=Path('curriculum/proposals/unit18')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(n,d):(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
L=read('lexicon/entries.json');G=read('curriculum/grammar.json')
F={f['form_id']:(l,f) for l in L['lemmas'] for f in l['forms']}
S={s['sense_id']:(l,s) for l in L['lemmas'] for s in l['senses']}
FEATURES={f['feature_id']:f for f in G['features']}
PRIOR_READ_FRAME=next(f for f in read('chapters/ch09/coverage.json')['lexical_frames'] if f['frame_id']=='u09-frame-raedan')
tasks=[];seqs=[];models=[];examples=[]
def seq(sid,text,pairs,features,kind='input'):
    words=re.findall(r"[^\W\d_]+(?:[-’'][^\W\d_]+)*",text,re.UNICODE)
    assert len(words)==len(pairs),(sid,words,pairs)
    tokens=[]
    for i,(word,(fid,ss)) in enumerate(zip(words,pairs),1):
        l,f=F[fid];ll,s=S[ss]
        assert l['lemma_id']==ll['lemma_id'],(sid,fid,ss)
        assert word.casefold()==f['form'].casefold(),(sid,word,f['form'])
        assert f.get('production_taught_in'),(sid,fid,'form not productive')
        assert s.get('production_taught_in'),(sid,ss,'sense not productive')
        tokens.append({'token_index':i,'literal':word,'surface':f['form'],'lemma_id':l['lemma_id'],'form_id':fid,'sense_id':ss,'analysis':copy.deepcopy(f['analysis']),'form_status':'previously_taught','sense_status':'previously_taught','form_production_taught_in':f['production_taught_in'],'sense_production_taught_in':s['production_taught_in'],'evidence_refs':sorted(set(f.get('evidence_refs',[])+s.get('evidence_refs',[])))})
    for tok in tokens:
        if tok['lemma_id']=='the-relative':
            tok['contextual_analysis']={'invariant_relative_particle':True,'internal_role':'subject' if '-A03-' in sid else 'direct_object','scope':'Contextual role of this occurrence; retain original register analysis unchanged.'}
        elif tok['lemma_id']=='thaet-conjunction':
            tok['contextual_analysis']={'invariant':True,'function':'finite content conjunction'}
        if kind=='visible_lexical_reference':
            tok['contextual_analysis']={'function':'visible dictionary or grammatical reference','independent_syntactic_use':False}
            tok['assessment_role']='visible_reference_position'
            tok['independent_recall_assessment']=False
    for ff in features:assert FEATURES[ff].get('production_taught_in'),(sid,ff,'feature not productive')
    row={'sequence_id':sid,'text':text,'kind':kind,'origin_category':'new teaching material','tokens':tokens,'feature_ids':features,'dependency_status':'closed_against_actual_prior_register','prior_feature_records':[{k:FEATURES[ff].get(k) for k in ['feature_id','production_taught_in','evidence_refs','scope_note','description']} for ff in features]}
    row['prior_lexical_frame_records']=[{'contract':'chapters/ch09/coverage.json','record':copy.deepcopy(PRIOR_READ_FRAME)}] if any(t['lemma_id']=='raedan' for t in tokens) else []
    seqs.append(row)
    return row
def task(tid,kind,prompt,inputs,outs,features,stage=1,**extra):
    outputs=[]
    for i,(label,model,meaning,error,*oseq) in enumerate(outs,1):
        oid=f'{tid}-O{i:03}'
        sq=oseq[0] if oseq else None
        outputs.append({'output_position_id':oid,'label':label,'response_language':'Old English' if sq else 'English','target':meaning,'essential_meaning':meaning,'alternatives_policy':'Accept equivalent grammatical wording preserving the proposition and explicit target. An English analysis may use equivalent precise terminology.','error_diagnosis':error,'output_sequence_id':sq['sequence_id'] if sq else None})
        models.append({'output_position_id':oid,'model':model,'target':meaning,'essential_meaning':meaning,'alternatives':'Accept defensible variants preserving every stated relation and the explicit target.','error_diagnosis':error,'output_sequence':sq})
    tasks.append({'task_id':tid,'key_id':'KEY-'+tid,'kind':kind,'origin_category':'new teaching material','prompt':prompt,'input_sequence_ids':[s['sequence_id'] for s in inputs],'input_texts':[s['text'] for s in inputs],'requested_outputs':outputs,'feature_ids':features,'stage':stage,'dependency_status':'closed_against_actual_prior_register' if not extra.get('source_span_id') else 'awaits_exact_reading_join','supplied_help_rule':'All source-specific supplied words and whole constructions remain visible; no supplied recall is assessed.',**extra})
se=('se-m-nom-sg','se-the');cyn=('cyning-nom-sg','cyning-source');man=('mann-nom-sg','mann-1')
datman=[('se-m-dat-sg','se-the'),('mann-dat-sg','mann-1')]
book=[('se-f-acc-sg','se-the'),('boc-acc-sg','boc-1')]
he=('he-m-nom-sg','he-1');ic=('ic-nom-sg','ic-personal')
rel=('the-relative-invariant','the-relative-which')
that=('thaet-conjunction-invariant','thaet-conjunction-1')
giv=('sellan-pret-3-sg','sellan-give')
features_roles=['article-agreement','u02-active-agreement','u02-giving-recipient','u02-pronoun-reference']
# Two translated examples are pedagogical inputs, not exercises or an extra narrative.
e1=seq('NEW-U18-EXAMPLE-01','Se mann ðe se cyning geseah, sang.',[se,man,rel,se,cyn,('geseon-pret-3-sg','geseon-1'),('singan-pret-3-sg','singan-1')],['article-agreement','u02-active-agreement','u08-relative-the','u08-relative-internal-case','u05-see-object','u04-intransitive-actions'],'worked_example')
examples.append({'example_id':e1['sequence_id'],'sequence_id':e1['sequence_id'],'teaching_id':e1['sequence_id']+'-TEACHING','text':e1['text'],'translation':'The man whom the king saw sang.','teaching_point':'The man is subject of sang, while the relative represents the object of geseah; the king is the relative clause subject.','grading':'ungraded translated teaching example','origin_category':'new teaching material'})
e2=seq('NEW-U18-EXAMPLE-02','Se cyning hēt ðone mann ðǣm cnihte ðā bōc sęllan.',[se,cyn,('hatan-pret-3-sg','hatan-command'),('se-m-acc-sg','se-the'),('mann-acc-sg','mann-1'),('se-m-dat-sg','se-the'),('cniht-dat-sg','cniht-u17-servant')]+book+[('sellan-infinitive-citation','sellan-give')],['article-agreement','u02-active-agreement','u09-command-infinitive','u02-giving-recipient','u06-infinitive-government'],'worked_example')
examples.append({'example_id':e2['sequence_id'],'sequence_id':e2['sequence_id'],'teaching_id':e2['sequence_id']+'-TEACHING','text':e2['text'],'translation':'The king ordered the man to give the servant the book.','teaching_point':'The accusative man performs the infinitive; the servant is its dative recipient and the book its accusative object.','grading':'ungraded translated teaching example','origin_category':'new teaching material'})

a1=seq('NEW-U18-A01-INPUT','Se cyning sealde ðǣm męnn ðā bōc. Hē hīe rǣdde.',[se,cyn,giv]+datman+book+[he,('he-f-acc-sg','he-1'),('raedan-pret-3-sg','raedan-1')],features_roles+['u13-reference-resolution-ambiguity'])
a1out=seq('NEW-U18-A01-OUTPUT','Se mann hīe rǣdde.',[se,man,('he-f-acc-sg','he-1'),('raedan-pret-3-sg','raedan-1')],['article-agreement','u02-active-agreement','u02-pronoun-reference','u13-reference-resolution-ambiguity'],'author_only_output')
task('NEW-U18-A01','reference_analysis','Analyse the two sentences. No further context identifies the reader.',[a1],[
('Identify the giver, recipient and thing given.','The king gives the book to the man. Cyning is nominative, męnn dative singular, and bōc accusative singular.','Keep agent, recipient and object distinct.','Do not interpret męnn as plural merely because the spelling is also a plural form.'),
('Give the referent and case of hīe.','Hīe refers to the feminine singular book and is accusative object of rǣdde.','Resolve the inanimate feminine pronoun from agreement and syntax.','Do not force hīe to mean they or a female person.'),
('Which named people can hē refer to? Explain what the forms establish.','Either the king or the man can be meant. Both are masculine singular; morphology and the supplied context do not settle which is the reader.','Recognize genuine ambiguity rather than applying a nearest-noun rule.','Do not treat the nearest preceding person as a grammatical requirement.'),
('Rewrite only the second sentence so that the recipient is explicitly the reader.',a1out['text'],'Identify the man explicitly as reader while keeping the book pronominal.','Do not make the king the explicitly stated reader.',a1out)],features_roles+['u13-reference-resolution-ambiguity'])

a2=seq('NEW-U18-A02-INPUT','Se cyning cwæð: “Ic geseah ðone mann.”',[se,cyn,('cwethan-pret-3-sg','cwethan-1'),ic,('geseon-pret-1-sg','geseon-1'),('se-m-acc-sg','se-the'),('mann-acc-sg','mann-1')],['article-agreement','u02-active-agreement','u05-direct-quotation','u05-see-object','u13-quoted-reference'])
a2out=seq('NEW-U18-A02-OUTPUT','Se cyning sægde ðæt hē ðone mann gesāwe.',[se,cyn,('secgan-pret-3-sg','secgan-content'),that,he,('se-m-acc-sg','se-the'),('mann-acc-sg','mann-1'),('geseon-u17-preterite-subj-3-sg','geseon-1')],['article-agreement','u02-active-agreement','u09-content-that','u09-reported-statement','u09-report-reference','u12-reported-sequence','u05-see-object'],'author_only_output')
task('NEW-U18-A02','reported_speech','Convert this direct statement into a report. Retain the king as the person who saw the man; use sęcgan with a ðæt clause and a preterite subjunctive in that clause.',[a2],[
('Identify the referent of ic and the time of the seeing relative to the quoted statement.','Ic is the king. The quoted preterite places the seeing before his act of speaking.','Recover the quoted speaker and relative temporal viewpoint.','Do not assign ic to the current narrator.'),
('Write the complete reported statement.',a2out['text'],'Use third-person reference to the king, reported content and the requested preterite subjunctive.','An indicative may be valid reporting but does not meet the explicit subjunctive target.',a2out),
('Explain whether the chosen subjunctive proves that the king’s statement is false.','It does not. The mood marks the reported content in this target construction, without itself establishing truth or falsity.','Distinguish reporting mood from truth value.','Do not translate a report as contrary to fact solely because its verb is subjunctive.')],['u05-direct-quotation','u13-quoted-reference','u09-content-that','u09-reported-statement','u09-report-reference','u12-reported-sequence'])

a3=seq('NEW-U18-A03-INPUT','Ðā męnn ðe ðone cyning gesāwon, sungon.',[('se-all-nom-pl','se-the'),('mann-nom-pl','mann-1'),rel,('se-m-acc-sg','se-the'),('cyning-acc-sg','cyning-source'),('geseon-pret-3-pl','geseon-1'),('singan-pret-3-pl','singan-1')],['article-agreement','u02-active-agreement','u08-relative-the','u08-relative-internal-case','u05-see-object','u04-intransitive-actions'])
a3out=seq('NEW-U18-A03-OUTPUT','Se mann ðe ðone cyning geseah, sang.',[se,man,rel,('se-m-acc-sg','se-the'),('cyning-acc-sg','cyning-source'),('geseon-pret-3-sg','geseon-1'),('singan-pret-3-sg','singan-1')],a3['feature_ids'],'author_only_output')
task('NEW-U18-A03','relative_number','Analyse the sentence, then replace the men by the man and keep the king singular.',[a3],[
('Translate the complete sentence.','The men who saw the king sang.','Preserve the men as both seers and singers and the king as object.','Do not make the king the subject of gesāwon.'),
('Identify the role represented by ðe and explain the agreement of both finite verbs.','Ðe represents the men as subject of the relative clause; gesāwon and sungon are both third-person plural because their respective subjects refer to the men.','Keep the relative clause and main clause agreement relations explicit.','Do not determine agreement from the nearer singular cyning.'),
('Write the complete singular version.',a3out['text'],'Change the article, noun and both finite verbs; preserve the king as singular object.','Do not leave either finite verb plural.',a3out)],a3['feature_ids'])

c1=seq('NEW-U18-C01-OUTPUT','Se mann ðe se cyning geseah, sealde ðǣm cnihte ðā bōc.',[se,man,rel,se,cyn,('geseon-pret-3-sg','geseon-1'),giv,('se-m-dat-sg','se-the'),('cniht-dat-sg','cniht-u17-servant')]+book,['article-agreement','u02-active-agreement','u08-relative-the','u08-relative-internal-case','u05-see-object','u02-giving-recipient'],'author_only_output')
task('NEW-U18-C01','controlled_composition','Translate: The man whom the king saw gave the servant the book. Use ðe and sęllan.',[],[
('Write one complete Old English sentence.',c1['text'],'The man gives; the king sees that man; the servant receives the book.','Do not confuse the relative object with the main subject or the recipient with the object.',c1)],c1['feature_ids'],2)
c2=seq('NEW-U18-C02-OUTPUT','Se cyning hēt ðā męnn ðǣm cnihte ðā bēc sęllan.',[se,cyn,('hatan-pret-3-sg','hatan-command'),('se-all-acc-pl','se-the'),('mann-acc-pl','mann-1'),('se-m-dat-sg','se-the'),('cniht-dat-sg','cniht-u17-servant'),('se-all-acc-pl','se-the'),('boc-acc-pl','boc-1'),('sellan-infinitive-citation','sellan-give')],e2['feature_ids'],'author_only_output')
task('NEW-U18-C02','controlled_composition','Translate: The king ordered the men to give the servant the books. Use hātan and a plain infinitive of sęllan.',[],[
('Write one complete Old English sentence.',c2['text'],'Keep the king as commander, the men as instructed actors, the servant as recipient and books as objects.','Do not use nominative męnn as a finite-clause subject or give the infinitive a plural ending.',c2)],c2['feature_ids'],2)

RID='FB-XII-APOLLONIUS-LOVE-GIFTS-DEPARTURE'
reading_specs=[
('R01','Translate the complete assigned passage in the following three consecutive divisions. All local help and original notes remain available.',[
('Translate 175.18–176.2, through goldhorde.','The daughter sees that Apollonius is thoroughly educated in all excellent accomplishments; she falls in love with him. After the drinking feast she reminds her father that he recently permitted her to give Apollonius whatever she wished from his treasure.','Preserve seeing and education, her reaction, the time phrase, permission, donor, recipient, free choice and the source of the gift.','Do not make Apollonius love the daughter or turn the earlier permission into a new command.'),
('Translate 176.3–176.13, through gesāwon.','The king tells her to give him whatever she wishes. Gladly she goes out and announces a gift by her father’s permission: two hundred pounds of gold, four hundred pounds’ weight of silver, the greatest part of costly clothing and twenty slave men. She orders these men to carry the things promised to her teacher and place them in the chamber before her friends. Her command is carried out; all the men who saw praise her gifts.','Preserve every gift, quantity, material, permission, instruction, promise and narrated result, including the relative clause’s actual antecedent.','Do not omit the servants, merge the two weight phrases, or make the gifts the subject of gesāwon.'),
('Translate from Ðā sōðlice geęndode in 176.13 through 177.2 geręstan.','The banquet ends. All the men rise, salute the king and princess, wish them well and return home. Apollonius also wishes health to the good king, pitier of the poor, and the princess, lover of learning. Looking toward the slave men whom the maiden had given him, he tells them to take the gifts and proposes going to their guesthouse so that they may rest.','Preserve the two departures or intended movements, the addressees of each speech, the prior gift and the final purpose.','Do not replace the proposed journey by a narrated arrival or make the servant-directed commands address the king.')]),
('R02','For each cited form, name the referent and explain its grammatical role. Keep the whole passage available.',[
('Explain hiere and his in 175.20.','Hiere is the daughter as possessor of mōd; his refers to Apollonius in the expression for love toward him. The whole expression means that she fell in love with him.','Keep the two possessors and the direction of affection distinct, applying the supplied expression.','Do not interpret his as the daughter’s own love or infer an unexpressed change of subject.'),
('Identify the speaker and addressee of ic and ðē in 176.5.','The princess is ic, the giver; Apollonius is ðē, the dative recipient of giefan.','Recover person and dative recipient within direct speech.','Do not preserve the earlier king as the speaker of this new quotation.'),
('Distinguish him in 176.19 from him in 176.20.','The first is singular Apollonius, recipient of the slave men whom the maiden had given him. The second is plural, the slave men addressed by Apollonius. Context and clause roles resolve identical dative spellings.','Resolve two syncretic pronouns by clause roles and discourse.','Do not assign both forms the same referent solely because they have the same spelling.')]),
('R03','Parse the following selected source expressions and explain their functions. Supplied lexical and quantity explanations remain visible.',[
('Compare the grammatical subjects of geseah 175.18 and gefēoll 175.20.','Geseah has the king’s daughter as subject; gefēoll has hiere mōd as grammatical subject. The meaning of the latter supplied expression is that she fell in love.','Separate literal grammatical subject from an idiomatic English rendering.','Do not make hiere alone the nominative subject of gefēoll.'),
('Explain the relationships expressed by punda and goldes in 176.6.','Punda is genitive plural of the counted weight-unit after twā hund; goldes is genitive singular naming the material measured. The complete supplied phrase means two hundred pounds of gold.','Apply the visible quantity analysis and distinguish counted units from material.','Do not infer that both genitives have the same semantic dependency or introduce an independent high-numeral recall test.'),
('Use original note 13 to explain ðe hīe gesāwon in 176.13 and the role of giefa.','The relative refers back to męnn despite intervening words; it represents the men as subject of gesāwon. Hīe is accusative plural, the gifts as object of seeing. Giefa is accusative plural, the gifts praised, with hiere as possessor.','Explain separation of antecedent and relative and distinguish subject from object with the source note visible.','The note already supplies the antecedent; the task asks how the complete structure works.'),
('Compare the case, number and agreement of gesunde in 176.16 and 176.18.','In 176.16 gesunde is accusative plural, agreeing with the infinitival subject hīe, the king and princess. In 176.18 it is nominative plural, agreeing with gē in the direct subjunctive wish. The identical surfaces participate in different clause structures; both expressions wish the addressees well or bid them farewell.','Apply the supplied farewell expressions and distinguish accusative plural from nominative plural predicate agreement.','Do not make gesunde an adverb merely because idiomatic English uses well.')]),
('R04','Describe the clause relations in the following spans using the complete source and its local support.',[
('Analyse the opening sentence 175.18–20: identify the temporal frame, the seeing-content clause and the main event.','Mid-ðȳ-ðe introduces the temporal frame with the daughter as perceiver; ðæt introduces the content of what she sees, Apollonius’s education; ðā introduces the ensuing main event, her falling in love.','Distinguish temporal subordination, embedded content and the main event.','Do not label every subordinate clause a relative or flatten the three relations into coordination.'),
('Compare ðæt ic mōste 176.1 with swā-hwæt-swā176.2 and 176.3–4.','The first is the supplied permission-content construction. Swā-hwæt-swā introduces the freely chosen thing she may give; its object role is internal to the free-choice clause.','Apply the visibly supplied permission frame and prior free-choice analysis without treating their introductory forms as interchangeable.','Do not interpret swā-hwæt-swā as a direct question.'),
('Analyse the final ðæt clause 177.2 and explain how it relates to gān wē sēcean.','The final clause gives the purpose of the proposed journey to the guesthouse: so that they can rest. Gān wē is the locally supplied first-person plural exhortation, with sēcean; the goal is prospective.','Distinguish a proposal, its infinitival action and its purpose.','Do not treat the purpose as an accomplished event or infer a general future-tense auxiliary.')]),
('R05','Explain the passage’s sequence from the actual statements, distinguishing completed actions from proposals.',[
('What authority does the princess give for her gifts, and who selects them?','She invokes the king’s earlier permission; he renews permission to give whatever she wishes. She herself announces the particular gifts.','Distinguish authorization from the selection and announcement of gifts.','Do not attribute each specified gift directly to a royal command.'),
('What does the final speech establish about Apollonius’s next action, and what remains unnarrated at this boundary?','He instructs the slave men to take the gifts and proposes going to their guesthouse to rest. This excerpt does not narrate their arrival or sleeping.','Separate intended action from completed narrative and respect the selected boundary.','Do not import the following Apollonius as Teacher episode into the answer.')])
]
for suffix,prompt,outs in reading_specs:
    task('NEW-U18-'+suffix,'supported_reading',prompt,[],outs,[],6,source_span_id=RID,assessment_scope='Supported translation and analysis; no source-only form, sense or frame is tested for unaided recall.')
reading_translation_models=['Truly, when the king’s daughter saw that Apollonius was so well trained in all excellent accomplishments, her heart fell in love with him. Then, after the end of the drinking feast, the maiden said to the king: “Dear father, a little while ago you allowed me to give Apollonius whatever I wished from your treasury.”', 'King Arcestrates said to her: “Give him whatever you wish.” Then she went out very happily and said: “Master Apollonius, with my father’s permission I give you two hundred pounds of gold and four hundred pounds’ weight of silver, and the greatest part of costly clothing, and twenty slave men.” And then she spoke thus to the slave men: “Carry with you these things which I promised Apollonius, my teacher, and place them inside the chamber before my friends.” This was then done in this way, according to the princess’s command; and all the men who saw them praised her gifts.', 'Then indeed the banquet ended, and all the men arose, greeted the king and the princess, wished them well and went home. Apollonius also said: “You good king, who has compassion on the poor, and you princess, lover of learning, farewell!” He also looked toward the slave men whom the maiden had given him and said to them: “Take with you these things which the princess gave me, and let us go and seek our guesthouse so that we may rest.”']
for number,text in enumerate(reading_translation_models,1):
    next(m for m in models if m['output_position_id']==f'NEW-U18-R01-O{number:03}')['model']=text

# Old English lexical controls embedded in original prompts are explicit inputs.
hint_specs=[
('NEW-U18-A02','sęcgan',[('secgan-infinitive-citation','secgan-content')]),
('NEW-U18-A02','ðæt',[('thaet-conjunction-invariant','thaet-conjunction-1')]),
('NEW-U18-C01','ðe',[('the-relative-invariant','the-relative-which')]),
('NEW-U18-C01','sęllan',[('sellan-infinitive-citation','sellan-give')]),
('NEW-U18-C02','hātan',[('hatan-infinitive-citation','hatan-command')]),
('NEW-U18-C02','sęllan',[('sellan-infinitive-citation','sellan-give')])
]
for number,(owner,text,pairs) in enumerate(hint_specs,1):
    sq=seq(owner+'-LEXICAL-REFERENCE-'+str(number),text,pairs,[],'visible_lexical_reference')
    t=next(t for t in tasks if t['task_id']==owner)
    t['input_sequence_ids'].append(sq['sequence_id'])
    t.setdefault('visible_lexical_reference_ids',[]).append(sq['sequence_id'])
    sq['owner_id']=owner
save('task-seed.json',{'schema_version':1,'chapter':'ch18','status':'prior-dependent tasks closed; reading and new form joins pending','tasks':tasks})
save('compositions.json',{'schema_version':1,'chapter':'ch18','status':'two translated examples; no new connected narrative','examples':examples,'teaching_examples':examples,'new_connected_compositions':[]})
save('original-prior-bindings.json',{'schema_version':1,'chapter':'ch18','sequences':[s for s in seqs if s['kind']!='author_only_output']})
save('author-only-original-models.json',{'schema_version':1,'chapter':'ch18','access':'AUTHOR ONLY. Withhold from a fresh blind solver until solutions are frozen.','models':models,'output_sequences':[s for s in seqs if s['kind']=='author_only_output']})
print(json.dumps({'tasks':len(tasks),'outputs':sum(len(t['requested_outputs']) for t in tasks),'examples':len(examples),'prior_bound_sequences':len(seqs),'prior_bound_tokens':sum(len(s['tokens']) for s in seqs)},indent=2))
