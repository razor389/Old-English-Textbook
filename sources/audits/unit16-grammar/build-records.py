"""Unit16 bounded verbal records from actual registers and inspected primary images.

This writes proposals only. It never changes prior records or teaching milestones.
"""
import json, hashlib, copy
from pathlib import Path
R=Path(__file__).resolve().parents[3]; O=Path(__file__).resolve().parent
L={x['lemma_id']:x for x in json.loads((R/'lexicon/entries.json').read_text(encoding='utf8'))['lemmas']}
def save(name,obj):
    def normalize(x):
        if isinstance(x,dict):
            if x.get('origin_category')=='new_teaching_material':x['origin_category']='new teaching material'
            for v in x.values():normalize(v)
        elif isinstance(x,list):
            for v in x:normalize(v)
    normalize(obj)
    (O/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
lemmas={}; features=[]; paradigms=[]; principals=[]; frames=[]
def lemma(i,head=None):
    if i not in lemmas:
        p=L.get(i,{})
        lemmas[i]={'lemma_id':i,'display_headword':head or p.get('display_headword'), 'part_of_speech':'verb','prior_lemma_present':i in L,'forms':[],'senses':[],'source_spellings':p.get('source_spellings',[])}
    return lemmas[i]
def prior_meta(x): return {k:x.get(k) for k in ['recognition_taught_in','production_taught_in','supplied_in','analysis','gloss','coverage_contract'] if k in x}
def form(i,id,surface,analysis,refs,status='new_production',teaching=None,note=''):
    q=next((x for x in L.get(i,{}).get('forms',[]) if x['form_id']==id),None)
    z={'form_id':id,'form':surface,'analysis':analysis,'knowledge_status':status,'evidence_refs':refs,'origin_category':'new_teaching_material','evidence_basis':'selected rule-derived form from an inspected paradigm and inspected lexical class; not a claim that every person is independently attested','teaching_ids':[teaching] if teaching else [],'scope_note':note}
    if q:
        assert q['form']==surface,(id,q['form'],surface)
        z['analysis']=copy.deepcopy(q['analysis']);z['contextual_analysis']=analysis;z['prior_scope']=prior_meta(q)
        if q.get('production_taught_in'): z['knowledge_status']='previously_taught'
    old=next((x for x in lemma(i)['forms'] if x['form_id']==id),None)
    if not old: lemma(i)['forms'].append(z)
    return old or z
def sense(i,id,gloss,refs,feature=None,status='new_production'):
    p=next((s for s in L.get(i,{}).get('senses',[]) if s['sense_id']==id),None)
    z={'sense_id':id,'gloss':gloss,'knowledge_status':status,'evidence_refs':refs,'teaching_ids':[feature] if feature else []}
    if p:
        z['gloss']=p['gloss']; z['contextual_gloss']=gloss;z['prior_scope']=prior_meta(p)
        if p.get('production_taught_in'):z['knowledge_status']='previously_taught'
    if not any(s['sense_id']==id for s in lemma(i)['senses']):lemma(i)['senses'].append(z)
    return z
def feat(id,label,scope,refs,status='new_production',tasks=None):
    x={'feature_id':id,'label':label,'description':scope,'scope_note':scope,'knowledge_status':status,'teaching_ids':['NEW-U16-GRAMMAR'],'evidence_refs':refs,'origin_category':'new_teaching_material','used_in_tasks':tasks or []}
    features.append(x);return x
def lexical(i,head,gloss,construction,refs,sid=None,fid=None,tasks=None):
    lemma(i,head);sid=sid or i+'-u16';fid=fid or 'u16-'+i+'-frame'
    sense(i,sid,gloss,refs,fid)
    feat(fid,head+': '+gloss,construction,refs,tasks=tasks)
    frames.append({'lemma_id':i,'sense_id':sid,'feature_id':fid,'construction':construction,'evidence_refs':refs,'knowledge_status':'new_production','scope_limit':'Only this stated frame; a displayed conjugation does not teach every construction.'})
def indicative(i,head,pres,past,cls,rule,refs,pp,inf=None):
    lemma(i,head);pid='NEW-U16-PAR-'+i.upper()+'-IND'; cells=[]
    for tense,forms in [('present',pres),('preterite',past)]:
        assert len(forms)==6
        for (person,number),surface in zip([(1,'singular'),(2,'singular'),(3,'singular'),(1,'plural'),(2,'plural'),(3,'plural')],forms):
            id=f'{i}-'+('pres' if tense=='present' else 'pret')+f'-{person}-'+('sg' if number=='singular' else 'pl')
            a={'tense':tense,'mood':'indicative','person':person,'number':number}
            f=form(i,id,surface,a,refs,teaching=pid,note='Complete present and preterite indicative; elementary uses are separately bounded by the lexical-frame record.')
            cells.append({'form_id':id,'form':surface,'analysis':a,'knowledge_status':f['knowledge_status'],'evidence_refs':refs})
    paradigms.append({'paradigm_id':pid,'lemma_id':i,'label':head+' present and preterite indicative','verb_class':cls,'completeness':'12 person/number/tense positions, singular and plural; homographic positions remain distinct','teaching_scope':'new_production','forms':cells,'rules_and_exceptions':[rule],'evidence_refs':refs,'shared_model_basis':{'already_taught_pattern':cls,'application':'Ending pattern is reused, but this lexeme and every selected stem/form are explicitly introduced here.'}})
    feat('u16-'+i+'-indicative',head+' complete indicative',rule+' Only indicative morphology is granted by this table; consult the separate frame for uses.',refs)
    parts=[head,past[0],past[3],pp] if cls.startswith('strong') else [head,past[0],pp]
    ids=[]
    for n,s in enumerate(parts,1):
        prior=next((f for f in L.get(i,{}).get('forms',[]) if f['form']==s and ('reference' in f['form_id'] or 'citation' in f['form_id'])),None)
        id=prior['form_id'] if prior else f'{i}-u16-principal-part-{n}-reference'
        a={'verb_form':'principal_part','position':n,'function':'citation_only'}
        f=form(i,id,s,a,refs,status='supplied',teaching='NEW-U16-PRINCIPAL-PARTS',note='Reference display only. The independently assigned finite/nonfinite form identity, if any, is separate.')
        ids.append(id)
    principals.append({'lemma_id':i,'headword':head,'verb_class':cls,'selected_principal_parts':parts,'form_ids':ids,'evidence_refs':refs,'rule':rule,'status':'reference display; productive finite forms listed separately'})
def command(i,sg,pl,refs):
    pid='NEW-U16-PAR-'+i.upper()+'-IMP';cells=[]
    for number,s in [('singular',sg),('plural',pl)]:
        id=f'{i}-imp-2-'+('sg' if number=='singular' else 'pl');a={'mood':'imperative','person':2,'number':number}
        z=form(i,id,s,a,refs,teaching=pid,note='Complete ordinary second-person singular/plural command pair, including ordinary negative command with ne.')
        cells.append({'form_id':id,'form':s,'analysis':a,'knowledge_status':z['knowledge_status'],'evidence_refs':refs})
    paradigms.append({'paradigm_id':pid,'lemma_id':i,'label':lemma(i)['display_headword']+' command pair','completeness':'both ordinary second-person numbers','teaching_scope':'new_production','forms':cells,'rules_and_exceptions':['Use the attested present stem; singular ending is selected for this verb, not guessed from English. Plural follows the selected present plural stem.'],'evidence_refs':refs})
def subj(i,sg,pl,refs):
    pid='NEW-U16-PAR-'+i.upper()+'-PRES-SUBJ';cells=[]
    for number,s in [('singular',sg),('plural',pl)]:
        for person in [1,2,3]:
            id=f'{i}-pres-subj-{person}-'+('sg' if number=='singular' else 'pl');a={'tense':'present','mood':'subjunctive','person':person,'number':number}
            form(i,id,s,a,refs,teaching=pid,note='Complete present subjunctive morphology; only the explicitly assigned expectation/indefinite-relative uses are extended.')
            cells.append({'form_id':id,'form':s,'analysis':a,'knowledge_status':'new_production','evidence_refs':refs})
    paradigms.append({'paradigm_id':pid,'lemma_id':i,'label':lemma(i)['display_headword']+' present subjunctive','completeness':'all six present subjunctive person/number positions','teaching_scope':'new_production','forms':cells,'rules_and_exceptions':['Present stem + e throughout singular, + en throughout plural; no present-indicative second/third-singular stem change.'],'evidence_refs':refs})
def parts(i,pres,past,refs,pastid=None):
    pid='NEW-U16-PAR-'+i.upper()+'-PART';cells=[]
    for tense,s,id in [('present',pres,i+'-present-participle-base'),('past',past,pastid or i+'-past-participle-base')]:
        a={'nonfinite':'participle','tense':tense,'inflection':'base'}
        z=form(i,id,s,a,refs,teaching=pid,note='Complete present/past base pair; attributive inflection follows already taught adjective patterns only where explicitly assigned. Predicative past participle may remain uninflected.')
        cells.append({'form_id':id,'form':s,'analysis':a,'knowledge_status':z['knowledge_status'],'evidence_refs':refs})
    paradigms.append({'paradigm_id':pid,'lemma_id':i,'label':lemma(i)['display_headword']+' participial bases','completeness':'present and past bases','teaching_scope':'new_production','forms':cells,'rules_and_exceptions':['Present -ende; past from the checked principal part, not from the present stem alone. This is not a license for every participial construction.'],'evidence_refs':refs})

FB=lambda *ns:['U16-G-FB'+str(n) for n in ns]
I=FB(54,55);W=FB(68,69,72);W2=FB(73,74)
def weak2(i,h,root,gloss,frame,refs,sid=None,fid=None):
    lexical(i,h,gloss,frame,refs,sid,fid)
    indicative(i,h,[root+'ie',root+'ast',root+'að']+[root+'iað']*3,[root+'ode',root+'odest',root+'ode']+[root+'odon']*3,'weak II','Selected -ie/-ast/-að/-iað present; -ode/-odest/-odon past; infinitive -ian and participle -od. The optional g and alternative past vowels are not selected targets.',W2+refs,root+'od')
weak2('aeswician','ǣswician','ǣswic','offend; cause to stumble','Accusative person offended; disjunctive singular subject hand or foot takes singular finite verb. The ethical/metaphorical meaning is supplied by the source, not physical injury.',['U16-EX-P18','U16-G-BT-AESWICIAN'])
weak2('blissian','blissian','bliss','rejoice','Ordinary intransitive rejoice; mid + dative companion; in32.10 ofer + accusative object of rejoicing is explicitly taught.',['U16-EX-P18','U16-EX-P19']+FB(279))
weak2('wuldrian','wuldrian','wuldr','glorify','Accusative person; self-directed glorification uses the accusative reflexive phrase mē selfne.',['U16-EX-P20']+FB(323))
weak2('plegian','plegian','pleg','play','Ordinary intransitive play, with time and manner adverbs; the assigned action comparison may repeat this action with dōn. Reading wið + participant and mid + instrument are locally supported, not generalized by this frame.',FB(309,168,170),'plegian-u16-play','u16-plegian-play')
weak2('beheafdian','behēafdian','behēafd','behead','Accusative person; active preterite narrates the commanded action without imposing an otherwise unexpressed causative paraphrase.',['U16-EX-P22'])
# Previous command/arise-subjunctive milestones are preserved; only missing systems are new.
lemma('cleopian');sense('cleopian','cleopian-u15-call','call; summon',FB(73,74))
indicative('cleopian','cleopian',['cleopie','cleopast','cleopað']+['cleopiað']*3,['cleopode','cleopodest','cleopode']+['cleopodon']*3,'weak II','Same complete weak-II ending selection as lufian; prior commands remain ch15. The full indicative is newly taught.',W2+['U16-EX-P19','U16-EX-P20'],'cleopod')
lexical('cleopian','cleopian','cry aloud','Intransitive cry out followed by direct words; distinguish from the prior accusative summon frame.',FB(168)+['U16-EX-P20'],'cleopian-u16-cry','u16-cleopian-cry')
lemma('arisan');sense('arisan','arisan-u14-arise','arise',FB(59,60))
indicative('arisan','ārīsan',['ārīse','ārīst','ārīst']+['ārīsað']*3,['ārās','ārise','ārās']+['ārison']*3,'strong I','ī/ā/i/i; s+st and s+ð give selected -st in both2sg and3sg. Preterite2sg has the plural stem. Prior complete subjunctive remains ch14.',I+FB(59,60),'ārisen')
lexical('aceorfan','āceorfan','cut off','Accusative thing cut; of is the separately written off particle in the assigned command, not a preposition requiring another object.',['U16-EX-P18']+FB(61,62))
indicative('aceorfan','āceorfan',['āceorfe','ācierfst','ācierfð']+['āceorfað']*3,['ācearf','ācurfe','ācearf']+['ācurfon']*3,'strong III','eo/ea/u/o; present2sg/3sg ie mutation, past2sg from u plural stem. Prefix ā- remains unchanged; shared prior forceorfan pattern does not erase this lexeme identity.',I+FB(61,62)+['U16-EX-P18'],'ācorfen')
lexical('forleosan','forlēosan','lose','Accusative thing lost. Attributive forloren32.11 is strong neuter accusative singular modifying scēap, not an invented weak ending.',['U16-EX-P18']+FB(60,61))
indicative('forleosan','forlēosan',['forlēose','forlīest','forlīest']+['forlēosað']*3,['forlēas','forlure','forlēas']+['forluron']*3,'strong II','ēo/ēa/u/o with grammatical s/r alternation in plural preterite and participle; present2sg/3sg both forlīest. Past2sg uses forlur-.',I+FB(60,61),'forloren')
lexical('iernan','iernan','run','Ordinary intransitive run. In perception constructions the accusative actor runs; geond + accusative marks the street traversed.',FB(61,168,301)+['U16-EX-P21'])
indicative('iernan','iernan',['ierne','iernst','iernð']+['iernað']*3,['arn','urne','arn']+['urnon']*3,'strong III','Selected ie/ a / u / u stems: iern-, arn, urn-, urnen. Keep the metathesized r in every selected stem. The present uses the Cook ie series rather than importing later irn/yrn spellings.',I+FB(61,301,168,169)+['U16-G-WRIGHT258'],'urnen')
lexical('thwean','ðwēan','wash','Accusative body part washed; mid + dative washing liquid. The woman is the subject, the feet the patient.',['U16-EX-P22']+FB(65))
indicative('thwean','ðwēan',['ðwēa','ðwiehst','ðwiehð']+['ðwēað']*3,['ðwōh','ðwōge','ðwōh']+['ðwōgon']*3,'strong VI contracted','Cook explicitly places ðwēan with slēan: contracted present ēa/ie; preterite singular h versus plural/2sg g; past participle ðwegen. Wright262–263 explicitly gives slōg/slōh and similarly þwēan, licensing the selected h variant. Do not construct an uncontracted thwēan-stem indicative.',I+FB(58,65)+['U16-G-WRIGHT262','U16-G-WRIGHT263'],'ðwegen')
lexical('bewendan','bewęndan','turn','Transitive turn; selected self-turning movement is expressed by the subject plus the dative reflexive him and tō + dative goal. The dative reflexive is explicitly bounded, not a universal reflexive rule.',FB(68,69,100,279)+['U16-EX-P22'])
indicative('bewendan','bewęndan',['bewęnde','bewęntst','bewęnt']+['bewęndað']*3,['bewęnde','bewęndest','bewęnde']+['bewęndon']*3,'weak I','Consonant+d model as sęndan: present contraction -ntst/-nt; past d-stem plus dental ending contracts, giving bewęnde. Present1sg and past1/3sg are homographic.',W+FB(279),'bewęnd')
lexical('smierwan','smierwan','anoint','Accusative person/body part anointed; mid + dative oil/ointment. Select consistent ie forms; independently attested i/y variants are documented alternatives, not silently mixed target cells.',['U16-EX-P22','U16-G-EX38','U16-G-BT-SMIRWAN','U16-G-WRIGHT274'])
indicative('smierwan','smierwan',['smierwe','smierest','smiereð']+['smierwað']*3,['smierede','smieredest','smierede']+['smieredon']*3,'weak I rw','Wright explicitly assigns smierwan to gierwan: w retained in1sg/plural present, lost in2sg/3sg and past; complete ending selection from Wright270–271, with imperative smiere. BT attests smire/smirede and smyredest variants; these do not alter the selected ie table.',W+['U16-G-WRIGHT270','U16-G-WRIGHT271','U16-G-WRIGHT274','U16-G-BT-SMIRWAN'],'smiered')
lemma('aliesan');sense('aliesan','aliesan-u15-deliver','deliver; release',['U16-G-EX44'])
indicative('aliesan','ālīesan',['ālīese','ālīest','ālīest']+['ālīesað']*3,['ālīesde','ālīesdest','ālīesde']+['ālīesdon']*3,'weak I','Continue the actual ch15 selected ālīesan/ālīesde/ālīesed principal parts: no silent change to a strong verb or to a different spelling. s+st/ð selects -st; prior command pair retains ch15.',W+['U16-G-EX44'],'ālīesed')
for i,sg,pl,refs in [
 ('aceorfan','āceorf','āceorfað',I+FB(61)),('blissian','blissa','blissiað',W2+FB(279)),
 ('smierwan','smiere','smierwað',['U16-G-WRIGHT270','U16-G-WRIGHT274']),('arisan','ārīs','ārīsað',I+FB(59,60)),
 ('forlaetan','forlǣt','forlǣtað',I+FB(67)),('geswican','geswīc','geswīcað',I+FB(59)+['U16-G-BT-GESWICAN']),
 ('efthweorfan','ęfthweorf','ęfthweorfað',I+FB(61,62,284)),('deman','dēm','dēmað',W+['U16-G-WRIGHT270','U16-EX-P22'])]: command(i,sg,pl,refs)
subj('findan','finde','finden',I+FB(61,62,104,105,167))
subj('fedan','fēde','fēden',W+FB(105))
parts('forleosan','forlēosende','forloren',I+FB(60,61,100))
form('forleosan','forleosan-pp-strong-acc-n-sg','forloren',{'nonfinite':'participle','tense':'past','declension':'strong','case':'accusative','gender':'neuter','number':'singular'},I+FB(60,61,100),teaching='NEW-U16-GRAMMAR',note='Exact attributed cell in mīn forloren scēap: strong neuter accusative singular -∅, explicitly derived through the already taught Unit7 strong-participle adjective pattern. The base-pair table does not by itself grant all adjective cells.')
parts('laedan','lǣdende','lǣded',W+FB(100,301))
parts('gefyllan','gefyllende','gefylled',W+FB(100),pastid='gefyllan-participle-citation')
parts('forgiefan','forgiefende','forgiefen',I+FB(63,64,100,288),pastid='forgiefan-pp-bare-source')
pid='NEW-U16-PAR-IERNAN-INF';cells=[]
for id,s,a in [('iernan-infinitive','iernan',{'nonfinite':'infinitive','inflection':'plain'}),('iernan-inflected-infinitive','iernanne',{'nonfinite':'infinitive','inflection':'inflected','case':'dative'})]:
    form('iernan',id,s,a,I+FB(106,168),teaching=pid,note='Complete plain/inflected infinitive pair; only prior elementary infinitive uses and the assigned perception frame apply.')
    cells.append({'form_id':id,'form':s,'analysis':a,'knowledge_status':'new_production','evidence_refs':I+FB(106,168)})
paradigms.append({'paradigm_id':pid,'lemma_id':'iernan','label':'iernan infinitive pair','completeness':'plain and inflected infinitive','teaching_scope':'new_production','forms':cells,'rules_and_exceptions':['Plain -an, inflected -anne; tō is a separate word.'],'evidence_refs':I+FB(106,168)})
pid='NEW-U16-PAR-SENDAN-INF';cells=[]
for id,s,a in [('sendan-infinitive-citation','sęndan',{'nonfinite':'infinitive','inflection':'plain'}),('sendan-inflected-infinitive','sęndanne',{'nonfinite':'infinitive','inflection':'inflected','case':'dative'})]:
    z=form('sendan',id,s,a,W+FB(96,106),teaching=pid,note='Complete plain/inflected pair. The plain form is used after perception with an accusative actor in32.6; prior finite teaching did not establish this infinitive recall.')
    cells.append({'form_id':id,'form':s,'analysis':a,'knowledge_status':z['knowledge_status'],'evidence_refs':W+FB(96,106)})
paradigms.append({'paradigm_id':pid,'lemma_id':'sendan','label':'sęndan infinitive pair','completeness':'plain and inflected infinitive','teaching_scope':'new_production','forms':cells,'rules_and_exceptions':['Plain -an, inflected -anne; tō is a separate word.'],'evidence_refs':W+FB(96,106)})
# New ordinary lexical frames in otherwise familiar verbs.
lexical('cunnan','cunnan','know; be acquainted with a person','Accusative person known. Compare the already taught cunnan + plain infinitive skill frame; do not teach an exclusive persons/facts partition, since witan can also have a personal object.',['U16-G-BT-CUNNAN','U16-EX-P20'],'cunnan-u16-acquaintance','u16-cunnan-person')
lexical('witan','witan','know a person','Accusative personal object as expressly required by Cook35.7; this does not replace the prior fact/question-content sense.',['U16-EX-P21']+FB(323),'witan-u16-person','u16-witan-person')
lexical('don','dōn','do the already mentioned action','Finite dōn repeats the lexical action in the comparison; it carries its own tense, person and number. It does not create modern English do-support.',['U16-G-BT-DON']+FB(170),'don-u16-substitute','u16-don-substitute')
lexical('don','dōn','cause that; make it be that','dōn + finite ðæt clause: the embedded subject is nominative git and the plural indicative bēoð agrees with dual git. Fishers is a nominative plural predicate; the person is not a direct accusative object of dōn in this selected frame.',['U16-G-BT-DON','U16-EX-P18'],'don-u16-cause','u16-don-finite-result')
lexical('gefyllan','gefyllan','fulfil a spoken prediction','Accusative utterance/prediction in active use; passive subject in the assigned purpose clause. Distinct from physically fill and accomplish a work.',['U16-EX-P19']+FB(292),'gefyllan-u16-fulfil','u16-gefyllan-utterance')
lexical('forgiefan','forgiefan','forgive','Accusative sin/offence and dative person in active use; the sin is the nominative subject of the passive, and the person remains dative. This new sense is not inferred from prior give/grant.',['U16-EX-P22']+FB(288),'forgiefan-u16-forgive','u16-forgiefan-forgive')
lexical('halsian','hālsian','conjure; solemnly charge','Accusative person + ðurh and accusative oath standard + requested ðæt clause; embedded uncertainty uses subjunctive sīe. This is not the ordinary beneficiary dative.',['U16-EX-P20']+FB(297,104),'halsian-u16-conjure','u16-halsian-oath')
feat('u16-adverbial-action-comparison','Adverbial comparison of actions','Comparative bęt qualifies the action; ðonne introduces a finite comparison clause with repeated verb or substitute dōn. Keep distinct subject agreement in each clause; the prior copular subject-comparison lesson did not cover this extension. Narrated nū/tō-dæg retain the specified speaker viewpoint.',FB(170)+['U16-G-BT-DON','U16-EX-P21'])
feat('u16-expectation-findan','Expectation with a finite subjunctive','Wēn is ðæt + present subjunctive gives the bounded perhaps/expectation pattern. No rule mechanically changes English will into willan.',FB(104,167)+['U16-EX-P19'])
feat('u16-indefinite-relative-fedan','Unspecified antecedent and intended feeding','In34.2, negative nānne and the hypothetical conditional permit present subjunctive finde; the relative ðe ðē fēde identifies an as-yet-unfound possible provider. Do not put the indicative feeding statement into an indiscriminate tense-backshift rule.',FB(105,167)+['U16-EX-P20'])
feat('u16-genitive-route','Genitive of the route followed','Use the genitive route ðæs weges with gān and the relative identifying that route; this is the exact pattern at169.16–17 and Cook§157.',FB(92,169)+['U16-EX-P21'])
feat('u16-bewendan-reflexive','Dative reflexive with turn','The selected subject-directed movement bewęnde hē him tō ... contains the dative reflexive him, specifically licensed by Cook§184a. It does not make every reflexive dative.',FB(100,279)+['U16-EX-P22'])
feat('u16-geswican-absolute','Absolute cease','Geswīcan may be absolute with a wind subject and may form an addressed command Geswīc. The prior genitive cessation frame remains distinct.',['U16-G-BT-GESWICAN','U16-EX-P18'])
feat('u16-asendan-absolute','Send without an expressed patient','The source36.10 expressly leaves the sending patient unexpressed; understand sent (someone), followed by the coordinated action. Only this bounded absolute application is assigned.',['U16-EX-P22'])
feat('u16-laedan-passive-carry','Lǣdan in a passive carrying event','A person is the patient of passive lǣdan, followed by an accusative endpoint with ōð. Keep distinct from intransitive movement.',['U16-EX-P21']+FB(301,101))
sense('laedan','laedan-u16-carry','carry; take a person',['U16-EX-P21']+FB(301),'u16-laedan-passive-carry')
lexical('healdan','healdan','keep; observe a saying','Accusative sprǣc as what one keeps/observes; distinguish the old physical hold sense.',['U16-EX-P20']+FB(298),'healdan-u16-keep','u16-healdan-keep')
lexical('weorthan','weorðan','arise; come about','Intransitive event with nominative smyltnes: a calm came about. No past participle is present, so this is not the previously taught passive auxiliary.',['U16-EX-P18'],'weorthan-u16-arise','u16-weorthan-arise')
def function_word(i,head,pos,surface,sid,gloss,fid,scope,refs):
    lemma(i,head)['part_of_speech']=pos
    q=next((f for f in L.get(i,{}).get('forms',[]) if f['form']==surface),None)
    id=q['form_id'] if q else i+'-invariant'
    a=q['analysis'] if q else {'inflection':'invariant'}
    form(i,id,surface,a,refs,teaching='NEW-U16-GRAMMAR',note=scope)
    sense(i,sid,gloss,refs,fid);feat(fid,gloss,scope,refs)
    frames.append({'lemma_id':i,'sense_id':sid,'feature_id':fid,'construction':scope,'evidence_refs':refs,'knowledge_status':'new_production','scope_limit':'Only the stated sense and construction; other uses remain separately classified.'})
function_word('aefter','æfter','preposition','æfter','aefter-u16-follow','after; following a person','u16-aefter-follow','Motion following a person: Cumað æfter mē. The following person is dative. The source-only temporal/according-to senses are not silently promoted with this new sense.',['U16-EX-P18']+FB(95))
function_word('of-adverb','of','adverb','of','of-adverb-u16-off','off','u16-of-particle','Of is an off particle in āceorf hit of. It has no following governed complement; distinguish the existing preposition of + dative.',['U16-EX-P18'])
function_word('ofer','ofer','preposition','ofer','ofer-u16-rejoicing','over; about, object of rejoicing','u16-ofer-rejoicing','Blissian ofer + accusative introduces what one rejoices over. In32.10 both compared objects retain ofer with accusative. This extends the old spatial/authority senses only in this bounded emotional frame.',['U16-EX-P18'])
function_word('swithe','swīðe','adverb','swīðor','swithe-u16-degree','more, degree of an action or feeling','u16-degree-comparison','Swīðor compares degree of rejoicing in32.10, followed by ðonne plus the second ofer phrase. This is not the prior rather/preference sense and not a superlative.', ['U16-EX-P18']+FB(104))
feat('u16-wenan-genitive','Expect with a genitive object','Wēnan expect takes a genitive thing expected, here nāhtes and the coordinated exception dēaðes selfes. The earlier full indicative and finite content clause did not itself teach this government.',FB(91)+['U16-EX-P19'])
frames.append({'lemma_id':'wenan','sense_id':'wenan-u15-suppose','feature_id':'u16-wenan-genitive','knowledge_status':'new_production','construction':'Genitive thing expected; semantic expect sense retains its actual ch15 milestone.','evidence_refs':FB(91)+['U16-EX-P19']})
feat('u16-biddan-requested-thing','Request with genitive thing','Biddan takes the requested thing in genitive, as Hwæs ... biddan? The person asked may simultaneously stand in accusative, as hine with genitive hwæs. Preserve the earlier simple personal-entreaty milestone; it did not teach this combined government.',FB(91,93)+['U16-EX-P19','U16-EX-P22'])
frames.append({'lemma_id':'biddan','sense_id':'biddan-1','feature_id':'u16-biddan-requested-thing','knowledge_status':'new_production','construction':'Genitive thing requested, optionally accusative person asked. Existing request sense retains its prior milestone.','evidence_refs':FB(91,93)})
form('deman','deman-imp-2-pl-before-ge','dēme',{'mood':'imperative','person':2,'number':'plural','position':'immediately before following subject gē'},FB(55,72),teaching='NEW-U16-GRAMMAR',note='Explicit positional variant in Ne dēme gē. It is still a plural command, not a first-person indicative; ordinary dēmað remains elsewhere.')
feat('u16-deman-command-before-ge','Shortened plural command before gē','Cook§95note gives plural -e immediately before a following subject pronoun. The productive extension is specifically dēme gē in36.1, paired with ordinary dēmað in its second clause. Source Gehīere,gē receives its own exact supplied form.',FB(55,168)+['U16-EX-P22'])

save('grammar-records.json',{'schema_version':1,'chapter':'ch16','baseline':'e1d94be','status':'proposal_pending_token_reconciliation','origin_category':'new_teaching_material','lemmas':list(lemmas.values()),'features':features,'paradigms':paradigms})
save('principal-parts.json',{'schema_version':1,'items':principals})
save('lexical-frames.json',{'schema_version':1,'frames':frames})
print(len(lemmas),'verbal lemmas;',len(paradigms),'complete bounded paradigms;',sum(len(p['forms']) for p in paradigms),'cells;',len(features),'features')
