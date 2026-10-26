"""Build the bounded Unit 13 grammatical proposal; never edit active registers."""
import json, hashlib, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
B=json.loads((ROOT/'build/unit13-prior-baseline.json').read_text(encoding='utf8'))
OLD={x['lemma_id']:x for x in B['lexicon']['lemmas']}
OLDF={f['form_id']:f for l in OLD.values() for f in l['forms']}
OLDS={s['sense_id']:s for l in OLD.values() for s in l['senses']}
OLDG={f['feature_id']:f for f in B['grammar']['features']}
D={'schema_version':1,'chapter':'ch13','status':'independent_audit_proposal_pending_coordinator_contract','baseline':'e17fc5f','origin_category':'new_teaching_material','lemmas':[],'paradigms':[],'features':[],'rules':[]}
L={}; RULES={}; FRAMES=[]
def write(name,obj):
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def lemma(i,h,pos='verb'):
    if i not in L:
        L[i]={'lemma_id':i,'display_headword':h,'part_of_speech':pos,'prior_lemma_present':i in OLD,'origin_category':'new_teaching_material','scope_note':'Only explicitly listed systems, senses and constructions are proposed. Citation headwords and source-only variants do not establish production.','forms':[],'senses':[]}
        if i in OLD:
            L[i]['prior_record_ref']='lexicon/entries.json#'+i
            L[i]['display_headword']=OLD[i]['display_headword']
            L[i]['part_of_speech']=OLD[i]['part_of_speech']
        D['lemmas'].append(L[i])
    return L[i]
def sense(i,h,sid,gloss,ev,scope='',status='new_production',pos='verb'):
    l=lemma(i,h,pos); old=OLDS.get(sid)
    s={'sense_id':sid,'gloss':gloss,'knowledge_status':('previously_taught' if old and old.get('production_taught_in') and status=='new_production' else status),'evidence_refs':ev,'scope_note':scope,'teaching_ids':['NEW-U13-VOC-'+i.upper()]}
    if old:
        s['prior_record']=old
        if old.get('gloss')!=gloss:
            s['contextual_gloss']=gloss
            s['gloss']=old['gloss']
    if not any(x['sense_id']==sid for x in l['senses']):l['senses'].append(s)
    return sid
def form(i,h,text,analysis,ev,fid=None,status='new_production',rule=None,scope='',pos='verb'):
    l=lemma(i,h,pos); match=None
    if fid in OLDF:match=OLDF[fid]
    elif i in OLD:
        for f in OLD[i]['forms']:
            if f['form']!=text:continue
            a=f.get('analysis',{}); blob=json.dumps(a)
            if not isinstance(a,dict):a={}
            if all(a.get(k)==v for k,v in analysis.items()) or (analysis.get('nonfinite')=='infinitive' and 'infinitive' in (blob+' '+f['form_id']) and 'inflected' not in blob):match=f;break
    if match:fid=match['form_id']
    fid=fid or (i+'-u13-'+str(len(l['forms'])+1))
    f={'form_id':fid,'form':text,'analysis':analysis,'knowledge_status':('previously_taught' if match and match.get('production_taught_in') and status=='new_production' else status),'evidence_refs':ev,'origin_category':'declared_normalization' if rule else 'exact_source','evidence_basis':'derived_from_checked_lexeme_and_explicit_rule' if rule else 'exact_image_checked_source','scope_note':scope or 'Morphological production within the expressly taught lexical frames only.','teaching_ids':['NEW-U13-PAR-'+i.upper()]}
    if rule:f['rule_id']=rule
    if match:
        f['prior_record']=match
        if match.get('analysis')!=analysis:
            f['contextual_analysis']=analysis
            f['analysis']=match.get('analysis')
    if not any(x['form_id']==fid for x in l['forms']):l['forms'].append(f)
    return f
def rule(i,text,ev,scope):
    r={'rule_id':i,'statement':text,'evidence_refs':ev,'lexical_scope':scope};RULES[i]=r;D['rules'].append(r)
def paradigm(i,h,kind,cells,ev,rid,scope):
    pid='NEW-U13-PAR-'+i.upper()+'-'+kind
    fs=[form(i,h,t,a,ev,i+'-'+suffix,rule=rid,scope=scope) for suffix,t,a in cells]
    p={'paradigm_id':pid,'lemma_id':i,'system':kind,'scope_note':scope,'evidence_refs':ev,'rule_id':rid,'teaching_id':pid,'display_route':'NEW-U13-DISPLAY-'+i.upper()+'-'+kind,'diagnostic_route':'NEW-U13-CHECK-'+i.upper()+'-'+kind,'cells':[{k:v for k,v in f.items() if k not in ['prior_record','teaching_ids']} for f in fs]}
    D['paradigms'].append(p);return p
def finite(i,h,pres,pret,ev,rid,mood='indicative'):
    cells=[]
    for tense,vs in [('present',pres),('preterite',pret)]:
        for n in ['singular','plural']:
            for person in [1,2,3]:
                t=vs[person-1] if n=='singular' else vs[3]
                cells.append((('pres' if tense=='present' else 'pret')+'-'+('subj-' if mood=='subjunctive' else '')+str(person)+'-'+('sg' if n=='singular' else 'pl'),t,{'tense':tense,'mood':mood,'person':person,'number':n}))
    return paradigm(i,h,'SUBJ' if mood=='subjunctive' else 'IND',cells,ev,rid,'Complete present and preterite '+mood+', all three persons in each number. Production is limited to the attached lexical frames; no other mood/nonfinite system is inferred.')
def imp(i,h,sg,pl,ev,rid):
    return paradigm(i,h,'IMP',[(f'imp-2-{short}',t,{'mood':'imperative','person':2,'number':n}) for short,n,t in [('sg','singular',sg),('pl','plural',pl)]],ev,rid,'Complete second-person singular/plural imperative; commands and prohibitions in taught lexical frames.')
def inf(i,h,plain,ger,ev,rid):
    return paradigm(i,h,'INF',[('infinitive',plain,{'nonfinite':'infinitive','inflection':'uninflected'}),('inflected-infinitive',ger,{'nonfinite':'infinitive','inflection':'inflected','case':'dative'})],ev,rid,'Complete plain/inflected infinitive pair. The plain infinitive is productive with taught modal/willan constructions; tō plus inflected infinitive only in previously taught or explicitly listed functions.')
def part(i,h,pres,past,ev,rid):
    return paradigm(i,h,'PART',[('present-participle-base',pres,{'nonfinite':'participle','tense':'present','inflection':'base'}),('past-participle-base',past,{'nonfinite':'participle','tense':'past','inflection':'base'})],ev,rid,'Complete present/past participle base pair. Base formation is productive; only the past base is used in taught uninflected predicative passives. No attributive participle declension or independent use of every present participle is licensed.')
rule('U13-R-WII','Selected long-form weak II: -ie, -ast, -að, -iað; preterite -ode, -odest, -ode, -odon. Infinitive -ian, inflected -ianne, present participle -iende, past -od. Alternative -ige/-ade formations remain outside this selected system.',['U13-FB73','U13-FB74'],['fordilgian','gewunian','ascian','halsian','wunian','hatian'])
rule('U13-R-WI','Weak I has selected present stems and dental preterite; syncope and consonant outcomes are stated per lexical row. Full singular/plural indicative endings follow §117.',['U13-FB68','U13-FB69','U13-FB72','U13-FB24','U13-WRIGHT248'],['onliesan','nealaecan','asettan','gescrydan','asendan','laedan'])
rule('U13-R-STRECCAN','The selected āstręccean system has geminate/ungeminated present alternation and unmutated preterite āstreahte. Past is not mechanically generated from the mutated infinitive. Source154 verifies āstreahte; §114 supports the lexical class.',['U13-FB70','U13-FB154','U13-FB277','U13-FB24','U13-FB25'],['astreccean'])
rule('U13-R-III','Strong III four stems govern present, past1/3 singular, past2 singular/plural, and past participle. Selected mutations eor→ier before 2/3 singular endings follow Cook; forceorfan ier is declared Cook-style normalization of BT cirf/cyrf variants. n+st simplifies to -nst, nn+ð to -nð.',['U13-FB54','U13-FB55','U13-FB61','U13-FB62','U13-FB24','U13-BT303'],['forceorfan','oferwinnan','efthweorfan','winnan'])
rule('U13-R-VII','Strong VII lexical pasts hēold and ondrēd are learned with their stems. Dental-ending simplifications in present follow Wright§476; imperative singular drops doubled/final consonant as appropriate.',['U13-FB66','U13-FB67','U13-FB24','U13-WRIGHT248'],['behealdan','ondraedan'])
rule('U13-R-II','Strong II bēod/bēad/bud/bod; present2/3 singular bīetst/bīett follows checked Cook§103. Only attested bebēodan prefix identity is licensed.',['U13-FB60','U13-FB61','U13-FB277'],['bebeodan'])
rule('U13-R-ANOMALOUS','Lexically attested fordōn and ingān take the checked dōn/gān finite morphology with their prefixes. ingangan/ingangende is a separately supplied lexical variant, not a regular ingān participle.',['U13-FB79','U13-FB80','U13-FB287','U13-FB301'],['fordon','ingan'])
rule('U13-R-INF','Selected plain infinitive plus -ne after its final n gives the inflected infinitive -anne/-enne (including -ianne). Promote a prior citation form only through the explicit pair.',['U13-FB55','U13-FB72','U13-FB73','U13-FB106'],['ascian','fordon','laedan','sprecan'])

specs=[
('fordilgian','fordilgian','destroy; annihilate','fordilg','U13-FB287'),('gewunian','gewunian','be accustomed; be wont','gewun','U13-FB296'),('ascian','āscian','ask a person about something','āsc','U13-FB276'),('halsian','hālsian','entreat; implore','hāls','U13-FB297'),('wunian','wunian','dwell; remain','wun','U13-FB73'),('hatian','hatian','hate','hat','U13-BT512')]
for i,h,g,st,e in specs:
    ev=[e,'U13-FB73','U13-FB74'];sense(i,h,i+'-u13',g,ev)
    finite(i,h,[st+'ie',st+'ast',st+'að',st+'iað'],[st+'ode',st+'odest',st+'ode',st+'odon'],ev,'U13-R-WII')
verbrows=[
('astreccean','āstręccean','prostrate (oneself)',['āstręcce','āstręcst','āstręcð','āstręcceað'],['āstreahte','āstreahtest','āstreahte','āstreahton'],'U13-R-STRECCAN',['U13-FB277','U13-FB154','U13-FB70']),
('onliesan','onlīesan','release',['onlīese','onlīest','onlīest','onlīesað'],['onlīesde','onlīesdest','onlīesde','onlīesdon'],'U13-R-WI',['U13-FB308','U13-FB155','U13-FB72']),
('nealaecan','nēalǣcan','approach; draw near',['nēalǣce','nēalǣcst','nēalǣcð','nēalǣcað'],['nēalǣcte','nēalǣctest','nēalǣcte','nēalǣcton'],'U13-R-WI',['U13-FB306','U13-FB152','U13-FB24']),
('forceorfan','forceorfan','cut down; cut off',['forceorfe','forcierfst','forcierfð','forceorfað'],['forcearf','forcurfe','forcearf','forcurfon'],'U13-R-III',['U13-BT303','U13-FB61','U13-FB62']),
('asettan','āsęttan','set; place',['āsętte','āsętst','āsętt','āsęttað'],['āsętte','āsęttest','āsętte','āsętton'],'U13-R-WI',['U13-FB276','U13-FB68','U13-FB72']),
('oferwinnan','oferwinnan','overcome; conquer',['oferwinne','oferwinst','oferwinð','oferwinnað'],['oferwann','oferwunne','oferwann','oferwunnon'],'U13-R-III',['U13-FB307','U13-FB62']),
('gescrydan','gescrȳdan','clothe',['gescrȳde','gescrȳtst','gescrȳt','gescrȳdað'],['gescrȳdde','gescrȳddest','gescrȳdde','gescrȳddon'],'U13-R-WI',['U13-FB294','U13-FB69','U13-WRIGHT248']),
('ondraedan','ondrǣdan','fear',['ondrǣde','ondrǣtst','ondrǣt','ondrǣdað'],['ondrēd','ondrēde','ondrēd','ondrēdon'],'U13-R-VII',['U13-FB67','U13-FB308','U13-BT749']),
('fordon','fordōn','destroy',['fordō','fordēst','fordēð','fordōð'],['fordyde','fordydest','fordyde','fordydon'],'U13-R-ANOMALOUS',['U13-FB287','U13-FB79']),
('ingan','ingān','enter; go in',['ingā','ingǣst','ingǣð','ingāð'],['inēode','inēodest','inēode','inēodon'],'U13-R-ANOMALOUS',['U13-FB301','U13-FB80']),
('asendan','āsęndan','send',['āsęnde','āsęntst','āsęnt','āsęndað'],['āsęnde','āsęndest','āsęnde','āsęndon'],'U13-R-WI',['U13-FB276','U13-FB69','U13-WRIGHT248']),
('behealdan','behealdan','behold; look at',['behealde','behieltst','behielt','behealdað'],['behēold','behēolde','behēold','behēoldon'],'U13-R-VII',['U13-FB278','U13-FB66']),
('bebeodan','bebēodan','command; instruct',['bebēode','bebīetst','bebīett','bebēodað'],['bebēad','bebude','bebēad','bebudon'],'U13-R-II',['U13-FB277','U13-FB60','U13-FB61']),
('efthweorfan','ęfthweorfan','return; turn back',['ęfthweorfe','ęfthwierfst','ęfthwierfð','ęfthweorfað'],['ęfthwearf','ęfthwurfe','ęfthwearf','ęfthwurfon'],'U13-R-III',['U13-FB284','U13-FB62'])]
for i,h,g,p,t,r,ev in verbrows:
    sense(i,h,'oferwinnan-u12-source' if i=='oferwinnan' else i+'-u13',g,ev)
    finite(i,h,p,t,ev,r)
finite('ingan','ingān',['ingā']*3+['ingān'],['inēode']*3+['inēoden'],['U13-FB80','U13-FB301'],'U13-R-ANOMALOUS','subjunctive')
for args in [('winnan','winnan','win','winnað',['U13-FB62','U13-FB25'],'U13-R-III'),('behealdan','behealdan','beheald','behealdað',['U13-FB278','U13-FB66'],'U13-R-VII'),('ondraedan','ondrǣdan','ondrǣd','ondrǣdað',['U13-FB67','U13-BT749'],'U13-R-VII'),('laedan','lǣdan','lǣd','lǣdað',['U13-FB72','U13-FB301'],'U13-R-WI')]:imp(*args)
for args in [('ascian','āscian','āscian','āscianne',['U13-FB276','U13-FB73'],'U13-R-INF'),('fordon','fordōn','fordōn','fordōnne',['U13-FB79','U13-FB287'],'U13-R-INF'),('laedan','lǣdan','lǣdan','lǣdanne',['U13-FB301','U13-FB72'],'U13-R-INF'),('sprecan','sprecan','sprecan','sprecanne',['U13-FB55','U13-FB141'],'U13-R-INF')]:inf(*args)
for args in [('fordilgian','fordilgian','fordilgiende','fordilgod',['U13-FB287','U13-FB73','U13-FB74'],'U13-R-WII'),('onliesan','onlīesan','onlīesende','onlīesed',['U13-FB308','U13-FB155','U13-FB72'],'U13-R-WI'),('asettan','āsęttan','āsęttende','āsętt',['U13-FB276','U13-FB68','U13-FB72'],'U13-R-WI'),('gescrydan','gescrȳdan','gescrȳdende','gescrȳd',['U13-FB294','U13-FB69','U13-FB72'],'U13-R-WI'),('asendan','āsęndan','āsęndende','āsęnd',['U13-FB276','U13-FB69','U13-FB72'],'U13-R-WI')]:part(*args)

def feature(i,title,scope,ev,status='new_production',prior=None):
    f={'feature_id':i,'title':title,'knowledge_status':status,'scope_note':scope,'evidence_refs':ev,'teaching_ids':['NEW-U13-GRAM-'+i.upper()],'prior_feature_refs':prior or []};D['features'].append(f);return f
def frame(i,lemmaids,text,ev,tasks=None,status='new_production'):
    f=feature(i,text,text,ev,status);FRAMES.append({'frame_id':i,'feature_id':i,'lemma_ids':lemmaids,'construction':text,'knowledge_status':status,'evidence_refs':ev,'used_in_tasks':tasks or []});return f
feature('u13-clause-role-parsing','Clause roles and finite predicates','Identify complete clauses, finite predicate, expressed/understood subject and governed complements by morphology, agreement and frame; order is corroboration, not the sole criterion.',['U13-FULK50','U13-FB102'],prior=['u11-clause-roles-order'])
feature('u13-main-fronting-order','Main-clause fronting','Subject-initial and fronted main clauses; second constituent is not second written word. Finite-second is an evidenced tendency, with actual exceptions; no automatic transformation.',['U13-FULK50','U13-FB152'])
feature('u13-pronoun-position-limits','Pronoun position and limits','A subject pronoun may precede the finite verb after a fronted adverbial: exact Æfter ðon hē underðēodde. Neither pronouns nor fronting impose an exceptionless placement rule.',['U13-FULK50','U13-FB153'])
feature('u13-reference-resolution-ambiguity','Sustained reference and ambiguity','Recover antecedents through agreement, syntax, discourse and meaning. Masculine sang can be referred to by hē/hine; identical masculine candidates can remain ambiguous. Do not choose nearest noun mechanically.',['U13-FULK16','U13-FB152','U13-FB153'])
feature('u13-coordination-predicate-recovery','Coordination and predicate recovery','Recover a shared subject or repeated lexical predicate only where the clauses support it. Restore finite agreement with the second expressed subject: singular wæs becomes plural wǣron. Cook134.1–2 independently has singular cymð and omitted plural coming.',['U13-FB134','U13-FB102','U13-FULK50'],prior=['u10-coordinated-predicate-ellipsis'])
feature('u13-quoted-reference','Person in reported and quoted speech','Within direct quotation, first and second person refer to current speaker and addressees. In indirect report, contextual third-person reference can be explicit or ambiguous; mood does not identify the antecedent.',['U13-FB153','U13-FB103','U13-FB104'])
feature('u13-long-sentence-analysis','Long-sentence analysis','Find boundaries and finite predicates before resolving reference; keep embedded clauses and coordinated material separate; return to apposition and source notes where necessary.',['U13-FB152','U13-FB153','U13-FULK54'])
feature('u13-supported-long-fronting','Long fronting in the source','Recognition only with explicit help: Cook152.8–9 Ðā stefne and ðone sang are accusatives governed by embedded gehīerde, as note8 says. Do not teach them as ordinary objects of cwæð or license free long extraction.',['U13-FB152'],'new_recognition')
feature('u13-dependent-order-tendencies','Dependent clause order','Dependent finite predicates often occur late/end, but need not be last. Cook25.7 expressly asks verb last for that item; this is a target constraint, not a general validity test.',['U13-FULK50','U13-EX13'],prior=['u08-clause-order'])
feature('u13-correlative-clause-reference','Correlative and homographic clause markers','Reuse taught temporal/causal relatives and correlatives. Distinguish temporal conjunction ðā, main adverb ðā, and demonstrative/article ðā by construction, agreement and context; paired when/then can clarify. No universal inversion diagnostic.',['U13-FULK54','U13-FULK55','U13-FB107','U13-FB152'])
feature('u13-negation-question-order','Negation and questions in clause analysis','Reuse ne plus finite, negative concord, interrogative-word and finite-initial yes/no questions; existing forms/moods only. This reinforces earlier systems and does not silently add contracted negative copulas.',['U13-FULK50','U13-FB100','U13-FB105'])

frames=[
('u13-fordilgian-acc',['fordilgian'],'Destroy accusative entity; corresponding patient passive.',['U13-FB287','U13-FB101'],['EX-VII-22-01']),
('u13-gewunian-inf',['gewunian','gen eosian'],'Be accustomed to a plain infinitive; controlled subject shared.',['U13-FB296','U13-FB106'],['EX-VII-22-11']),
('u13-ascian-person-thing',['ascian'],'Ask an accusative person about a genitive thing, or ask a bounded indirect question; not a double accusative.',['U13-FB93','U13-FB154'],['EX-VII-22-12','EX-VII-22-13']),
('u13-astreccean-reflexive',['astreccean'],'Prostrate oneself: accusative reflexive coreferential with subject.',['U13-FB154','U13-FB100'],['EX-VII-22-14']),
('u13-onliesan-acc-passive',['onliesan'],'Release an accusative entity; passive uninflected onlīesed with wesan.',['U13-FB155','U13-FB101'],['EX-VII-22-15']),
('u13-nealaecan-to-dat',['nealaecan'],'Approach a goal marked by tō plus dative.',['U13-FB152','U13-FB306'],['EX-VII-23-02']),
('u13-halsian-request',['halsian'],'Entreat accusative person; requested content may be ðæt plus subjunctive.',['U13-FB154','U13-FB104'],['EX-VII-23-03']),
('u13-forceorfan-acc',['forceorfan'],'Cut down an accusative tree/entity.',['U13-BT303'],['EX-VII-23-07']),
('u13-asettan-acc-passive',['asettan'],'Place/set accusative entity; corresponding uninflected predicative passive.',['U13-FB276','U13-FB101'],['EX-VII-23-08']),
('u13-wunian-location',['wunian'],'Dwell/remain with ordinary static location or no complement.',['U13-FB153','U13-FB73'],['EX-VII-24-03']),
('u13-oferwinnan-acc',['oferwinnan'],'Overcome/conquer an accusative person or force.',['U13-FB307'],['EX-VII-24-04']),
('u13-gescrydan-clothing',['gescrydan'],'Clothe an accusative person; passive with clothing marked by mid+dative. This is a bounded lexical extension from the checked scrȳdan clothing frame, not a general rule for all dress verbs.',['U13-FB294','U13-FB101','U13-BT843'],['EX-VII-24-04','EX-VII-24-09']),
('u13-ondraedan-acc',['ondraedan'],'Fear accusative person/entity, with optional coreferential dative; no forced English-style reflexive.',['U13-BT749','U13-FB308'],['EX-VII-24-05','EX-VII-24-06']),
('u13-fordon-acc',['fordon'],'Destroy accusative entities; plain infinitive after taught modal.',['U13-FB287','U13-FB106'],['EX-VII-24-06']),
('u13-ingan-under',['ingan'],'Enter/go in; supplied worthy-content construction takes pres subjunctive ingā. Direction under a roof uses the explicitly supported local prepositional expression.',['U13-FB301','U13-FB80','U13-FB104'],['EX-VII-24-07']),
('u13-asendan-person',['asendan'],'Send accusative person/entity; corresponding patient passive.',['U13-FB276','U13-FB101'],['EX-VII-25-01']),
('u13-behealdan-acc',['behealdan'],'Behold/look at accusative object.',['U13-FB278'],['EX-VII-25-04']),
('u13-hatian-acc',['hatian'],'Hate accusative person.',['U13-BT512'],['EX-VII-25-06']),
('u13-bebeodan-content',['bebeodan'],'Command dative addressee; ðæt content with subjunctive under the taught command frame, or a licensed relative containing the command.',['U13-FB104','U13-FB154','U13-FB277'],['EX-VII-25-07']),
('u13-efthweorfan-return',['efthweorfan'],'Return intransitively; explicit route adjunct may specify way.',['U13-FB284','U13-FB152'],['EX-VII-25-12']),
('u13-laedan-person-direction',['laedan'],'Lead/bring/take accusative person, optionally with accompanying person (mid+dative) and direction adverb hider.',['U13-FB301','U13-FB155','U13-FB153'],['NEW-U13-READING']),
('u13-sprecan-conversation-mid',['sprecan','mid'],'Speak with a person: mid+dative marks interlocutor. Source141 confirms lexical conversation but its mid+acc is explicitly exceptional and is not generalized.',['U13-FB141','U13-FB95','U13-FB99'],['NEW-U13-EXAMPLE08','NEW-U13-READING']),
('u13-began-study',['began'],'Pursue/practise accusative study/activity using existing begān finite and imperative systems.',['U13-FB278'],['EX-VII-22-04']),
('u13-astigan-descent',['astigan'],'Descend intransitively; of+dative marks source. This is an explicit new sense alongside earlier boarding.',['U13-FB276','U13-FB152'],['EX-VII-22-10','FB-VII-CHAD-MUSIC-SUMMONS']),
('u13-sellan-sale',['sellan'],'Sell accusative possession (distinct from prior give sense).',['U13-FB93'],['EX-VII-23-10']),
('u13-wyrcean-making',['wyrcean'],'Make/do accusative thing; practise an accusative abstract wrongdoing. Distinguish prior physical labour from this transitive scope.',['U13-FB93','U13-FB296'],['EX-VII-22-07']),
('u13-instrumental-route',['weg','ilca','se'],'By the same way: ðȳ instrumental determiner plus existing dative-surface ilcan wege in adverbial route function. Reuse dative forms; this does not add an unassigned adjective paradigm.',['U13-FB99','U13-FB152'],['EX-VII-25-12']),
('u13-pleasant-infinitive',['wynsum','hieran'],'Pleasant to hear: tō plus inflected infinitive after evaluative adjective, bounded to this expression.',['U13-FB106'],['EX-VII-25-08']),
('u13-ge-paired',['ge-conjunction'],'Paired ge ... ge coordinates parallel constituents, both ... and; optional previously supplied ǣgðer requires its explicit support.',['U13-FB107'],['EX-VII-24-06']),
]
task_corrections={'u13-fordilgian-acc':['EX-VII-22-03'],'u13-ascian-person-thing':['EX-VII-22-12'],'u13-wunian-location':['EX-VII-24-01'],'u13-ondraedan-acc':['EX-VII-24-06'],'u13-asendan-person':['EX-VII-24-09'],'u13-behealdan-acc':['EX-VII-24-11'],'u13-began-study':['EX-VII-22-05'],'u13-laedan-person-direction':['EX-VII-22-13','NEW-U13-READING'],'u13-wyrcean-making':['EX-VII-22-07','EX-VII-23-04']}
for args in frames:
    args=list(args)
    args[1]=[x.replace('gen eosian','geneosian') for x in args[1]]
    if args[0] in task_corrections:args[4]=task_corrections[args[0]]
    frame(*args)
frame('u13-beforan-positioning-acc',['beforan','astreccean'],'Beforan plus accusative in movement/positioning before a person; static dative is a valid alternative construal and not a language error. Cook172 target and prostration frame are considered separately.',['U13-C-BT-BEFORAN','U13-FB154','U13-EX11'],['EX-VII-22-14'])
frame('u13-with-proximity-acc',['with','standan'],'Wið plus accusative for static proximity, as stand beside; this accusative does not indicate motion.',['U13-C-BT-WID','U13-EX12'],['EX-VII-23-05'])
frame('u13-under-direction-acc',['under','ingan'],'Under plus accusative for entering beneath a roof; separate from already taught static under+dative.',['U13-C-BT-UNDER'],['EX-VII-24-07'])
frame('u13-worthy-content',['wierthe','ingan'],'Wierðe worthy with ðæt plus present subjunctive for the proposed entry; bounded adjective-content frame corroborated by exact primary roof-entry example.',['U13-C-BT-UNDER'],['EX-VII-24-07'])
for f in FRAMES:
    if f['frame_id']=='u13-gescrydan-clothing':
        f['evidence_refs'].append('U13-C-BT-GESCRYDAN')
        f['construction']='Clothe accusative person with garment marked mid+dative; exact prefixed ge-scrýdan also attested. Passive retains mid+dative.'
        next(x for x in D['features'] if x['feature_id']==f['feature_id']).update(scope_note=f['construction'],evidence_refs=f['evidence_refs'])
    if f['frame_id']=='u13-sellan-sale':
        f['evidence_refs']=['U13-FB311','U13-FB96']
        next(x for x in D['features'] if x['feature_id']==f['feature_id'])['evidence_refs']=f['evidence_refs']
    if f['frame_id']=='u13-wyrcean-making':
        f['evidence_refs']=['U13-FB324','U13-FB93']
        next(x for x in D['features'] if x['feature_id']==f['feature_id'])['evidence_refs']=f['evidence_refs']

extensions=[('laedan','lǣdan','laedan-u13-bring','lead; bring; take a person',['U13-FB301','U13-FB155'],'Person accusative with direction adverb or accompanying phrase.'),('sprecan','sprecan','sprecan-u13-converse','speak with someone',['U13-FB141'],'Conversation mid+dative; source exceptional accusative is not promoted.'),('began','begān','began-u13-study','pursue; practise study',['U13-FB278'],'Accusative study/activity.'),('astigan','āstīgan','astigan-u13-descend','descend',['U13-FB276','U13-FB152'],'Intransitive descent; of+dative departure.'),('sellan','sęllan','sellan-u13-sell','sell',['U13-FB93'],'Accusative possession; transfer by sale distinct from earlier give.'),('wyrcean','wyrcean','wyrcean-u13-do-practise','make; do; practise',['U13-FB93','U13-FB296'],'Transitive concrete or bounded abstract object; do unrighteousness.')]
for args in extensions:sense(*args)
L['wyrcean']['senses']=[s for s in L['wyrcean']['senses'] if s['sense_id']!='wyrcean-u13-do-practise']
sense('wyrcean','wyrcean','wyrcean-make','make',['U13-FB324','U13-FB93'],'Promote the actual earlier supplied make sense for finite transitive production; infinitive syntax is not enlarged.')
sense('wyrcean','wyrcean','wyrcean-work','work; perform',['U13-FB324'],'Reuse earlier accusative work/deed scope, including unrighteousness as the deed performed.')
for l in D['lemmas']:
    for s in l['senses']:
        if s['sense_id']=='sellan-u13-sell':s['evidence_refs']=['U13-FB311','U13-FB96']
        if s['sense_id']=='wyrcean-u13-do-practise':s['evidence_refs']=['U13-FB324','U13-FB93']
sense('beforan','be-foran','beforan-u13-positioning','before, into a position in front of; accusative landmark',['U13-C-BT-BEFORAN'],'Bounded movement/positioning before person; ordinary static dative remains a valid alternative.',pos='preposition')
sense('with','wið','with-u13-proximity','by; beside; at, with accusative landmark',['U13-C-BT-WID'],'Static proximity with standan; no claim that all wið takes accusative.',pos='preposition')
sense('under','under','under-u13-direction','under, with directional accusative',['U13-C-BT-UNDER'],'Move/enter under roof; static dative scope remains distinct.',pos='preposition')
sense('mid','mid','mid-u13-clothing','with (a garment), clothing complement',['U13-BT843','U13-C-BT-GESCRYDAN'],'Dative garment complement of scrȳdan/gescrȳdan only.',pos='preposition')
sense('hwilc','hwilc','hwilc-u13-any','any; some (indefinite adjective)',['U13-FB155'],'Indefinite any in a question or conditional; uses the previously complete productive adjective forms.',pos='adjective')
frame('u13-hwilc-indefinite',['hwilc'],'Indefinite hwilc any in any wonder and if any person; distinguish interrogative which.',['U13-FB155','U13-FB153'],['EX-VII-23-13','FB-VII-CHAD-MUSIC-SUMMONS'])
frame('u13-don-well-dative',['don','wel'],'Do well to a dative person: extend the prior beneficiary frame to wel plus dōn without expressed deed object.',['U13-FB106','U13-FB94'],['EX-VII-25-06'])
frame('u13-singan-song',['singan','sang'],'Sing accusative song, a bounded cognate-object extension.',['U13-FB96','U13-EX13'],['EX-VII-25-08'])
closed=[
('thaer','ðǣr','adverb','thaer-there','there','thaer-invariant-source',['U13-FB317','U13-FB153']),('eft','ęft','adverb','eft-u13-again-back','again; back','eft-invariant',['U13-FB284','U13-FB152']),('of','of','preposition','of-u11-source','out of; from, governing dative','of-invariant-dat-source',['U13-FB307','U13-FB152']),('mid','mid','preposition','mid-u13-interlocutor','with an interlocutor, governing dative','mid-invariant-source',['U13-FB141','U13-FB99']),('butan','būtan','preposition','butan-u13-without','without, governing dative','butan-invariant',['U13-FB280','U13-FB95']),('oth-preposition','oð','preposition','oth-u13-until','up to; until, governing accusative','oth-preposition-invariant',['U13-FB97','U13-FB152']),('thider','ðider','adverb','thider-u13-thither','thither; to that place','thider-invariant',['U13-FB318']),('aer-adverb','ǣr','adverb','aer-u13-before','before; earlier','aer-adverb-invariant',['U13-FB274','U13-FB152']),('aerest','ǣrest','adverb','aerest-u13-first','first; at first','aerest-invariant',['U13-FB274','U13-FB152']),('styccemaelum','styccemǣlum','adverb','styccemaelum-u13','little by little','styccemaelum-invariant',['U13-FB152']),('neah-adverb','nēah','adverb','neah-u13-nigh','near; at hand','neah-adverb-invariant',['U13-FB306']),('othothe','oððe','conjunction','othothe-u13-or','or','othothe-invariant',['U13-FULK50','U13-FB152']),('ge-conjunction','ge','conjunction','ge-u13-both-and','both ... and (paired ge ... ge)','ge-conjunction-source',['U13-FB107','U13-FB274'])]
for i,h,pos,sid,g,fid,ev in closed:
    if sid=='ge-u13-both-and':sid='ge-paired-source'
    sense(i,h,sid,g,ev,pos=pos)
    form(i,h,h,{'invariant':True,'function':pos},ev,fid,scope='Only the explicitly listed sense and construction are productive.',pos=pos)
PPS=[]
for i,h,pp,ev in [('forceorfan','forceorfan','forcorfen',['U13-BT303','U13-FB61','U13-FB62'])]:
    sid=i+'-u13'; refs=[]
    for fid,t,a in [(i+'-infinitive-citation',h,{'nonfinite':'infinitive','function':'citation'}),(i+'-participle-citation',pp,{'nonfinite':'participle','tense':'past','function':'citation'})]:
        f=form(i,h,t,a,ev,fid,status='supplied',scope='Printed principal-part citation for deriving the finite system. No independent nonfinite recall or use is assigned.')
        refs.append({'form_id':f['form_id'],'sense_id':sid,'form':t,'knowledge_status':'supplied'})
    PPS.append({'lemma_id':i,'citations':[refs[0],{'form_id':i+'-pret-3-sg','sense_id':sid,'form':'forcearf','knowledge_status':'new_production'},{'form_id':i+'-pret-3-pl','sense_id':sid,'form':'forcurfon','knowledge_status':'new_production'},refs[1]],'scope':'All four parts are printed for reference. Explain finite distribution from them; nonfinite citations are supplied.','evidence_refs':ev})
for p in D['paradigms']:
    suffix={'IND':'indicative','SUBJ':'subjunctive','IMP':'imperative','INF':'infinitive-pair','PART':'participle-bases'}[p['system']]
    p['feature_id']='u13-'+p['lemma_id']+'-'+suffix
    f=feature(p['feature_id'],p['lemma_id']+' '+suffix,p['scope_note'],p['evidence_refs'])
    f.update(paradigm_id=p['paradigm_id'],form_ids=[c['form_id'] for c in p['cells']],rule_id=p['rule_id'])
lexical_notes={
 'astreccean':'āstręcc- in first singular/plural; simplify before -st/-ð. Select -eað plural with the e-infinitive spelling. Unmutated and spirantized past āstreaht- is lexical, confirmed by exact āstreahte.',
 'onliesan':'s+st and s+ð both give st. Past stem onlīesd-. Past participle onlīesed is exact155.13.',
 'nealaecan':'Past stem nēalǣct- from c+d; no substitution of a hypothetical -h- past. Source plural nēalǣcton corroborates.',
 'asettan':'Present geminate tt; selected sętst/sętt. Past āsętt- gives first/third singular āsętte, identical to present first singular; labels carry the distinction.',
 'gescrydan':'Present d becomes t before -st/-ð; past dental dd. Selected uninflected past participle gescrȳd simplifies final gemination; source gescrȳdd is a documented variant.',
 'asendan':'Present final d devoices before -st/-ð. In past -ndd- simplifies to -nd-, giving āsęnde; past participle selected āsęnd.',
 'forceorfan':'ceorf/cearf/curf/corf; selected present singular cierf is rule-derived under Cook mutation. BT explicitly attests cirf/cyrf variants; all are not separately assigned.',
 'oferwinnan':'winn/wann/wunn/wunn; winst and winð simplify clusters. Only this attested compound is licensed.',
 'efthweorfan':'hweorf/hwearf/hwurf/hworf with present singular hwierf; exact source infinitive remains separately supplied.',
 'behealdan':'heald/hēold; selected mutated present h i e l forms behieltst/behielt, with dental contraction. Present stem has short ea.',
 'bebeodan':'bēod/bēad/bud/bod; mutated dental present bīetst/bīett. Preterite2 singular and plural use bud-.',
 'ondraedan':'Selected strongVII preterite ondrēd, second singular ondrēde, plural ondrēdon; present dental ondrǣtst/ondrǣt.',
 'fordon':'Prefix for- plus the separately attested dōn paradigm, including dēst/dēð and dyde. No general prefix-formation rule.',
 'ingan':'Prefix in- plus attested gān, including suppletive inēode. Subjunctive present ingā/ingān, past inēode/inēoden. ingangan is a different supplied variant identity.'}
for i,h,g,st,e in specs:lexical_notes[i]='Selected weakII stem '+st+'; apply all printed weakII endings. Long vowels in āsc/hāls are lexical. No -ige/-ade alternative is tested.'
for l in D['lemmas']:
    if l['lemma_id'] in lexical_notes:l['derivation_note']=lexical_notes[l['lemma_id']]
write('grammar-records.json',D)
write('principal-parts.json',{'chapter':'ch13','scope':'Citation-only support for finite derivation; nonfinite use requires an assigned separate system.','rows':PPS})
write('lexical-frames.json',{'schema_version':1,'chapter':'ch13','status':D['status'],'frames':FRAMES})
write('rules.json',{'chapter':'ch13','rules':D['rules']})
write('display-routes.json',{'chapter':'ch13','routes':[{'paradigm_id':p['paradigm_id'],'display_id':p['display_route'],'diagnostic_id':p['diagnostic_route'],'heading':p['lemma_id']+' — '+p['system'],'visible_metadata':['tense','mood','person','number'] if p['system'] in ['IND','SUBJ'] else ['nonfinite','tense','inflection'] if p['system'] in ['PART','INF'] else ['mood','person','number'],'form_ids':[c['form_id'] for c in p['cells']],'cell_count':len(p['cells']),'route':'Print every cell with the lexical principal parts and rule; diagnostic reconstructs selected cells across persons/numbers, then all remaining cells are explicitly supplied in the table.'} for p in D['paradigms']]})
print('Written incremental grammar proposal:',len(D['lemmas']),'lemmas,',len(D['paradigms']),'systems,',sum(len(p['cells']) for p in D['paradigms']),'paradigm cells,',len(D['features']),'features')
