"""Exact reading positions and contextual verbal analysis, with whole support."""
from pathlib import Path
import json,re,copy
O=Path(__file__).resolve().parent;ROOT=O.parents[2]
# Reuse the locally defined matcher without rerunning the model-output mutation.
ns={}
prefix=(O/'build-contextual-bindings.py').read_text(encoding='utf8').split('# Surface|lemma|parse|current clause role.')[0]
ns['__file__']=str(O/'build-contextual-bindings.py');exec(prefix,ns)
bind=ns['bind'];parse=ns['parse'];L=ns['L']
R=json.loads((ROOT/'sources/audits/unit17-source/reading-source.json').read_text(encoding='utf8'))['source_spans'][0]
T=re.findall(r'[A-Za-zĀ-žǢǣȲȳÆæÐðÞþ]+(?:-[A-Za-zĀ-žǢǣȲȳÆæÐðÞþ]+)*',R['learner_text']);assert len(T)==252
# token position, lemma, explicit morphology, current contextual role, sense scope
data=[
(2,'gan','it3s','Princess went out','prior'),
(6,'hatan','it3s','Princess ordered harp fetched; infinitive agent left unexpressed','prior'),
(7,'feccean','inf','Fetching of princess’s harp, with object hiere hearpan','supply:fetch'),
(14,'hearpian','inf','Princess’s harp playing begins','supply:play harp'),
(15,'onginnan','it3s','Princess began playing, governing hearpian','prior'),
(20,'gemengan','it3s','Princess mixed harp sound with pleasant song','supply:mix sound with song'),
(25,'onginnan','it3p','All men began praising; plural actors','prior'),
(30,'herian','inf','Praise princess for her musical skill, after ongunnon','new:praise'),
(37,'swigian','it3s','Apollonius alone was silent','supply:be silent'),
(39,'cwethan','it3s','King speaks directly','prior'),
(45,'don','ip2s','King addresses Apollonius: you behave ill','prior'),
(50,'herian','ip3p','All men praise king’s daughter','new:praise'),
(60,'swigian','prp','Silence accompanies Apollonius’s blame; exact swīgende retained, note12a gives swīgiende','supply:being silent'),
(61,'taelan','ip2s','Apollonius censures her by silence; hīe direct object','new:blame'),
(63,'cwethan','it3s','Apollonius speaks directly','prior'),
(71,'geliefan-permit','ip2s','Conditional if the king permits Apollonius to speak; mē is the dative person granted permission, and the speaking is understood from ic sęcge','supply:permit; allow'),
(73,'secgan','ip1s','Apollonius says nested content','prior'),
(76,'ongietan','ip1s','Apollonius perceives/understands the inner content','prior'),
(81,'gefeallan','it3s','Princess has chanced upon music; source note15 explicitly supplies idiomatic sense','supply:chance upon'),
(86,'nabban','ip3s','Princess has not mastered it; negative auxiliary in perfect','prior'),
(90,'geleornian','pp','Music has not been learned well; hine points to masculine swēgcræft','supply:learn; master'),
(92,'hatan','im2s','Apollonius commands king to have harp given','prior'),
(95,'sellan','inf','Give harp to dative mē; recipient is not the implied giving agent','prior'),
(99,'witan','ip2s','King will know; present future reference','prior'),
(105,'nytan','ip2s','King does not yet know; contracted negative nāst','supply:not know'),
(109,'cwethan','it3s','King speaks','prior'),
(112,'oncnawan','ip1s','King acknowledges/recognizes Apollonius’s education','supply:recognize; acknowledge'),
(116,'wesan','ip2s','Asserted certainty in reported content, not automatic subjunctive; note194','prior'),
(121,'gelared','pp','Well taught/educated state of Apollonius in all things; prior lexical adjective, not a newly assigned participle','prior'),
(123,'hatan','it3s','King ordered harp given','prior'),
(126,'sellan','inf','Give harp to dative Apollonie','prior'),
(132,'utgan','it3s','Apollonius went out, prefixed lexical form','supply:go out'),
(135,'scrydan','it3s','Apollonius dressed himself; hine reflexive accusative','supply:dress oneself'),
(137,'settan','it3s','Put crown on his head','prior'),
(144,'niman','it3s','Took harp into hand; exact nōm','prior'),
(151,'ingan','it3s','Entered; exact prefixed inēode','prior'),
(154,'standan','it3s','Stood so that audience inferred godlike identity','prior'),
(161,'ymbsittan','pa:present:nominative:masculine:plural:weak','Substantival surrounding sitters/spectators, with ealle ðā','supply:people sitting around'),
(162,'wenan','it3p','King and spectators supposed mistaken identity','prior'),
(165,'wesan','st3s','They supposed he was not Apollonius; negative past subjunctive','supply:negative copula nǣre in reported supposition'),
(170,'wesan','st3s','They supposed he was Apollo; imagined reported identity','prior'),
(176,'weorthan','it3s','Silence and quiet came about; singular whole-result expression','supply:resultative come about'),
(180,'geweorthan','pp','Become/come-to-pass resultative, not transitive passive','supply:become; come about'),
(188,'geniman','it3s','Apollonius took his plectrum','supply:take'),
(195,'astyrian','inf','Move/stir harp strings with skill, complement of began','supply:move; set in motion'),
(196,'onginnan','it3s','Apollonius began moving strings','prior'),
(204,'gemengan','it3s','Apollonius mixed harp sound with pleasant song','supply:mix sound with song'),
(214,'wesan','it3p','Relative attendees were present','prior'),
(217,'cleopian','it3p','All shouted with loud voice; actual cleopedon retains source spelling','prior'),
(220,'herian','it3p','All praised Apollonius','new:praise'),
(223,'forlaetan','it3s','Set aside/put down harp, as note5 Latin deponens confirms','supply:set aside'),
(228,'plegian','it3s','Acted/performed, not merely played a ball game; note6 theatrical paraphrase','supply:act; perform'),
(234,'forthteon','it3s','Presented/performed many fine things, not literally pulled objects out','supply:present; perform'),
(238,'ungecnawen','pp','Unfamiliar/unknown to audience; preserve singular predicate after collective fela phrase','supply:unknown'),
(239,'wesan','it3s','Singular source wæs preserved with unknown/unusual predicate','prior'),
(246,'lician','it3s','Each performance pleased all people; dative experiencers him eallum','supply:please'),
(252,'forthteon','it3s','Relative object refers to each performance he presented','supply:present; perform')]
F=[]
def frame(id,start,end,analysis):
 F.append({'feature_id':id,'token_start_one_based':start,'token_end_one_based':end,'exact_span':' '.join(T[start-1:end]),'knowledge_status':'supplied','whole_frame_analysis':analysis,'evidence_refs':['U17G-FB174'if start<107 else'U17G-FB175'],'origin_category':'exact source span with new private grammatical analysis'})
frame('U17-RSUP-01',6,9,'Hēt governs fetching infinitive, with an unexpressed performer; hiere is possessive, the harp is the thing fetched. Supply fęccean and the complete commission frame.')
frame('U17-RSUP-02',11,33,'Sōna swā marks as soon as; hearpian is infinitive under began. Gemęngde joins accusative harp-sound and mid/dative song. Hęrian on hiere swēgcræfte praises her with respect to musical skill, not physical location.')
frame('U17-RSUP-03',35,61,'Apollonius alone remained silent; swīgende accompanies the addressed2sg censure in the quotation. Exact source form is retained and note12a explicitly supplies swīgiende. No new full swīgian system or generalized instrumental participle is tested.')
frame('U17-RSUP-04',68,90,'Gif ðū mē gelīefst means if you permit me [to speak]; mē is the dative person granted permission and the permitted speaking is understood from the following ic sęcge, I will say. Gelīefst is present indicative2sg, as the original note14 directs to196d; no infinitive is printed or inserted in the source. Cook303 explicitly gives līefan allow,permit; the reading supplies its exact prefixed occurrence. Keep this source-local permission verb separate from the earlier believe sense. The nested content says the daughter has chanced upon music, but has not learned it well. Gefēoll on swēgcræft is the source’s idiom, not literal physical falling; masculine hine resumes swēgcræft.')
F[-1]['evidence_refs']+=['U17G-FB303','U17G-FB293','U17G-FB105']
frame('U17-RSUP-05',92,105,'Hāt governs the act of giving, with mē as dative recipient, as source note164a directs; do not construe it as order me to give. Wāst and nāst are2sg affirmative and contracted-negative know; future knowledge is expressed with present wāst. Nāst is supplied, not a new nytan paradigm.')
frame('U17-RSUP-06',111,121,'King acknowledges that the addressee is well educated. Eart is asserted indicative: note194 explicitly directs the certainty exception. The dictionary recognition sense and full content frame are supplied.')
frame('U17-RSUP-07',123,151,'The king has the harp given to dative Apollonie. Apollonius goes out, dresses himself with reflexive hine, puts on crown, takes harp in hand, and enters. Exact prefixed/source forms remain local support; common root or prefix does not grant new senses.')
frame('U17-RSUP-08',153,174,'Result clause: his stance made king and surrounding spectators suppose he was Apollo, not Apollonius. Ymbsittendan is weak nominalized plural; wēndon agrees with king+spectators. Nǣre/wǣre are past subjunctives in reported mistaken supposition. Source Apollo name is supplied, not silently corrected to an OE nominative.')
frame('U17-RSUP-09',175,183,'Wearð … geworden presents silence/quiet coming about as a whole result. It is not a transitive passive. Preserve singular wearð and supplied resultative idiom.')
frame('U17-RSUP-10',184,204,'Genōm takes plectrum accusative; āstyrian ongan governs moving harp strings with skill. The same mixing frame joins harp sound and song. Neither ge- nor ā- alone proves these specific senses.')
frame('U17-RSUP-11',205,220,'King himself and all present people are plural actors shouting and praising. Micelre stefne is dative/instrumental of manner; no mid occurs in the exact source. Hęredon refers to the applause for Apollonius.')
frame('U17-RSUP-12',221,252,'Forlēt means set aside the harp (note5), plegode means performed/acted (note6), and forðtēah presented performances (note8). Fela governs genitive plural fine things; preserve singular ungecnāwen wæs and ungewunelic in the relative without inventing a universal agreement rule. Him eallum are dative people pleased; ǣlc of those things is singular subject of līcode.')
rows=[]
for i,lemma,code,role,scope in data:
 analysis=parse(code)
 if i==121:analysis={'case':'nom','number':'sg','gender':'m','strength':'strong'}
 rec=bind(lemma,T[i-1],analysis,role,'FB-XII-APOLLONIUS-MUSIC-PERFORMANCE',i)
 rec['reading_token_id']=f'U17-RWORD-{i:03}'
 rec['whole_frame_support_ids']=[f['feature_id']for f in F if f['token_start_one_based']<=i<=f['token_end_one_based']]
 if scope.startswith('supply:'):
  rec['sense_id']=f'{lemma}-u17-reading';rec['sense_knowledge_status']='supplied';rec['contextual_gloss']=scope.split(':',1)[1]
 elif scope.startswith('new:'):
  rec['sense_id']='herian-u17-selected'if lemma=='herian'else'taelan-u17-selected';rec['sense_knowledge_status']='new_production';rec['contextual_gloss']=scope.split(':',1)[1]
 else:
  old=[s for s in L.get(lemma,{}).get('senses',[])if s.get('production_taught_in')]
  if not old:
   rec['sense_id']=f'{lemma}-u17-reading';rec['sense_knowledge_status']='supplied'
  else:rec['sense_id']=old[0]['sense_id'];rec['sense_knowledge_status']='previously_taught';rec['actual_prior_sense']=copy.deepcopy(old[0])
 selected_prior={6:'hatan-command',92:'hatan-command',123:'hatan-command',73:'secgan-content',217:'cleopian-u16-cry'}
 if i in selected_prior:
  actual=next(s for s in L[lemma]['senses']if s['sense_id']==selected_prior[i])
  rec['sense_id']=actual['sense_id'];rec['sense_knowledge_status']='previously_taught';rec['actual_prior_sense']=copy.deepcopy(actual)
  rec['current_frame_scope']='The actual source-local frame is supplied by the whole-frame support; the earlier sense record is not rewritten.'
 if i==30:rec['form_id']='herian-u17-inf-reference';rec['form_knowledge_status']='supplied';rec['visible_reference']=True
 if i==71:
  rec['form_id']='geliefan-permit-u17-source-pres-2-sg';rec['form_knowledge_status']='supplied'
  rec['sense_id']='geliefan-permit-u17-source-sense';rec['sense_knowledge_status']='supplied'
  rec['evidence_refs']=['U17G-FB174','U17G-FB303','U17G-FB293','U17G-FB105']
  rec['selected_sense_record']={'sense_id':rec['sense_id'],'gloss':'permit; allow','knowledge_status':'supplied','scope':'Exact permission clause at174.14–15; no independent productive permission paradigm or complement rule.','evidence_refs':rec['evidence_refs']}
  rec['supplied_lemma_proposal']={'lemma_id':'geliefan-permit','display_headword':'gelīefst (permission)','part_of_speech':'verb','origin_category':'exact source form; declared source-local lexical identity','scope_note':'Exact prefixed present2sg occurrence supplied at174.15. Cook303 gives the underlying permission verb līefan113; Cook293 ge-līefan believe remains a separate earlier teaching record. The exact source form, not a new independently recalled infinitive, is the display reference.'}
  rec['identity_note']='Supplied permission homograph; do not reuse the earlier believe lemma/form milestone merely because gelīefst has the same spelling. Morphology is present indicative2sg; mē is the dative permitted person.'
 rec['support_route_complete']=bool(rec['whole_frame_support_ids'])or rec['form_knowledge_status']!='supplied'
 rows.append(rec)
out={'schema_version':1,'access':'author-only grammar/source analysis; excluded from blind reviewers','source_span_id':R['source_span_id'],'exact_source_word_count':252,'tokenization':'Unicode word strings; retain internal hyphens and length marks; 1-based positions in source learner_text, no textual normalization.','verbal_occurrences':rows,'whole_frame_support':F,'counts':{'verbal_occurrences':len(rows),'whole_support_frames':len(F)},'unresolved_routes':[r['reading_token_id']for r in rows if not r['support_route_complete']]}
(O/'reading-verbal-bindings.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(out['counts'],out['unresolved_routes'])
