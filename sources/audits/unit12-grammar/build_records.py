from pathlib import Path
import json, copy

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'sources/audits/unit12-grammar'
B = json.loads((ROOT / 'build/unit12-prior-baseline.json').read_text(encoding='utf-8'))
OLD = {x['lemma_id']: x for x in B['lexicon']['lemmas']}
L, F, P, FR = {}, [], [], []

def lemma(i, h=None, pos='verb'):
    if i not in L:
        L[i] = {'lemma_id': i, 'display_headword': h or OLD[i]['display_headword'],
                'part_of_speech': pos, 'forms': [], 'senses': [],
                'origin_category': 'new_teaching_material',
                'scope_note': 'Only the individually listed forms, senses and constructions establish the proposed Unit 12 scope.'}
        if i in OLD:
            L[i]['prior_record_ref'] = {'baseline': 'build/unit12-prior-baseline.json', 'lemma_id': i,
                                       'prior_form_count': len(OLD[i]['forms'])}
    return L[i]

def previous(i, kind, idkey, ident):
    return next((x for x in OLD.get(i, {}).get(kind, []) if x[idkey] == ident), None)

def form(i, ident, text, analysis, ev, status='new_production', scope=''):
    r = {'form_id': ident, 'form': text, 'analysis': analysis, 'knowledge_status': status,
         'evidence_refs': ev, 'origin_category': 'declared_normalization',
         'evidence_basis': 'Image-checked lexical stem plus image-checked inflection rule; derived cells are not claimed individually attested.',
         'scope_note': scope}
    old = previous(i, 'forms', 'form_id', ident)
    if old:
        r.update(prior_record=copy.deepcopy(old), prior_status=old.get('knowledge_status'))
        if old.get('production_taught_in') and status == 'new_production': r['knowledge_status'] = 'previously_taught'
    if any(x['form_id'] == ident for x in L[i]['forms']):
        raise ValueError('duplicate proposed form ' + ident)
    L[i]['forms'].append(r)
    return r

def sense(i, ident, gloss, ev, status='new_production', scope=''):
    r = {'sense_id': ident, 'gloss': gloss, 'knowledge_status': status, 'evidence_refs': ev,
         'origin_category': 'new_teaching_material', 'scope_note': scope}
    old = previous(i, 'senses', 'sense_id', ident)
    if old: r.update(prior_record=copy.deepcopy(old), prior_status=old.get('knowledge_status'))
    L[i]['senses'].append(r)
    return r

def feature(i, desc, ev, scope='', status='new_production'):
    F.append({'feature_id': i, 'description': desc, 'knowledge_status': status,
              'evidence_refs': ev, 'scope_note': scope})

def frame(i, s, gloss, rule, ev, status='new_production'):
    FR.append({'frame_id': 'U12-FRAME-' + s, 'lemma_id': i, 'sense_id': s, 'gloss': gloss,
               'knowledge_status': status, 'frame_and_boundary': rule, 'evidence_refs': ev})

def par(i, tag, cells, ev, scope):
    P.append({'paradigm_id': 'NEW-U12-PAR-' + i + '-' + tag, 'lemma_id': i,
              'title': L[i]['display_headword'] + ': ' + tag, 'scope': scope,
              'origin_category': 'new_teaching_material', 'evidence_refs': ev,
              'cell_count': len(cells),
              'cells': [{'form_id': f['form_id'], 'form': f['form'], 'knowledge_status': f['knowledge_status'], **f['analysis']} for f in cells]})

WI = ['U12-G-FB-WI', 'U12-G-FB-DENTALS']
WII = ['U12-G-FB-WII']
STR = ['U12-G-FB-STRONG']
verbs = [
 ('adrifan','ādrīfan',['ādrīfe','ādrīfst','ādrīfð','ādrīfað'],['ādrāf','ādrife','ādrāf','ādrifon'],STR+['U12-G-FB-I','U12-G-LEX-ADRIFAN'],'adrifan-expel','drive out; expel','Accusative person or group expelled; previously taught fram+dative may identify the source of departure.'),
 ('gehatan','gehātan',['gehāte','gehǣtst','gehǣtt','gehātað'],['gehēt','gehēte','gehēt','gehēton'],STR+['U12-G-FB-VII','U12-G-BT-GEHATAN'],'gehatan-promise','promise','Accusative thing promised and optionally dative recipient. No general promise-clause or calling/commanding sense is inferred.'),
 ('fleon','flēon',['flēo','flīehst','flīehð','flēoð'],['flēah','fluge','flēah','flugon'],STR+['U12-G-FB-II','U12-G-BT-FLEON'],'fleon-flee','flee; flee from; avoid','Intransitive flight, or accusative person/thing avoided. This verb is distinct from flēogan, fly.'),
 ('gemetan','gemētan',['gemēte','gemētst','gemētt','gemētað'],['gemētte','gemēttest','gemētte','gemētton'],WI+['U12-G-LEX-GEMETAN'],'gemetan-find','find; meet','Accusative person or thing found. The preterite gemētte is not the past participle gemētt.'),
 ('geopenian','geopenian',['geopenie','geopenast','geopenað','geopeniað'],['geopenode','geopenodest','geopenode','geopenodon'],WII+['U12-G-LEX-GEOPENIAN'],'geopenian-open','open','Accusative thing opened, including mouth or eyes; no reflexive/intransitive system is silently established.'),
 ('gretan','grētan',['grēte','grētst','grētt','grētað'],['grētte','grēttest','grētte','grētton'],WI+['U12-G-BT-GRETAN','U12-G-EX21'],'gretan-take-leave','greet; take leave of','Accusative person greeted or taken leave of, extended explicitly to the native-land object required in Cook21.12. Weak grētan is distinct from the strong homonym meaning weep.'),
 ('cythan','cȳðan',['cȳðe','cȳst','cȳð','cȳðað'],['cȳðde','cȳðdest','cȳðde','cȳðdon'],WI+['U12-G-BT-CYTHAN','U12-G-WRIGHT-DENTALS'],'cythan-announce','make known; announce','Accusative thing announced or a ðæt content clause; optionally dative recipient. Selected cȳst follows regular dental loss before -st, cȳð the coalescence of two dentals. Past cȳdde is an attested alternative to selected cȳðde.'),
 ('ehtan','ēhtan',['ēhte','ēhtst','ēht','ēhtað'],['ēhte','ēhtest','ēhte','ēhton'],WI+['U12-G-BT-EHTAN'],'ehtan-persecute','pursue; persecute','Selected accusative person pursued/persecuted, directly evidenced in Matthew 10.23. Genitive government is also attested and may be accepted if its forms are supported.'),
 ('agan','āgan',['āh','āhst','āh','āgon'],['āhte','āhtest','āhte','āhton'],['U12-G-FB-AGAN'],'agan-possess','have; possess','Accusative possession. This is the positive present/preterite indicative only; no imperative, subjunctive, nonfinite or negative system is implied.'),
 ('leornian','leornian',['leornie','leornast','leornað','leorniað'],['leornode','leornodest','leornode','leornodon'],WII+['U12-G-BT-LEORNIAN'],'leornian-learn','learn','Accusative thing learned when expressed; æt+dative identifies the person from whom one learns. Objectless learn from me is independently evidenced.')
]
for i,h,pr,pa,ev,si,gl,rule in verbs:
    lemma(i,h); cells=[]
    for tense,short,arr in [('present','pres',pr),('preterite','pret',pa)]:
        for num in ['sg','pl']:
            for person in [1,2,3]:
                ident = f'{i}-{short}-{person}-{num}'
                if i == 'fleon' and short == 'pres' and person == 3 and num == 'pl': ident = 'fleon-pres-3-pl-source'
                cells.append(form(i,ident,arr[person-1] if num=='sg' else arr[3],
                                  {'tense':tense,'mood':'indicative','person':person,'number':num},ev,scope=rule))
    par(i,'IND',cells,ev,'Complete present and preterite indicative: all three persons, singular and plural. Other moods/nonfinite systems require separate records.')
    sense(i,si,gl,ev,scope=rule); frame(i,si,gl,rule,ev)
    feature('u12-'+i+'-indicative','Complete defined '+h+' present/preterite indicative system.',ev,rule)
    form(i,i+'-inf-citation',h,{'mood':'infinitive','type':'plain'},ev,status='supplied',scope='Vocabulary citation only, unless separately promoted in the defined infinitive pair.')

commands = [
 ('sendan','sęndan','sęnd','sęndað',WI),('bringan','bringan','bring','bringað',WI+['U12-G-FB-BRINGAN']),
 ('adrifan','ādrīfan','ādrīf','ādrīfað',STR+['U12-G-FB-I']),
 ('fleon','flēon','flēoh','flēoð',STR+['U12-G-FB-II']),
 ('gemetan','gemētan','gemēt','gemētað',WI),('geopenian','geopenian','geopena','geopeniað',WII),
 ('weorpan','weorpan','weorp','weorpað',STR+['U12-G-FB-III']),('leornian','leornian','leorna','leorniað',WII),
 ('risan','rīsan','rīs','rīsað',STR+['U12-G-FB-I'])
]
for i,h,sg,pl,ev in commands:
    lemma(i,h)
    cells=[form(i,f'{i}-imp-2-{n}',v,{'mood':'imperative','person':2,'number':n},ev) for n,v in [('sg',sg),('pl',pl)]]
    par(i,'IMP',cells,ev,'Both directly addressed command forms, singular and plural; no unlisted subjunctive cells inferred.')
    feature('u12-'+i+'-imperative','Both '+h+' direct commands.',ev)

parts = [
 ('gewyrcean','gewyrcean','gewyrcende','geworht','gewyrcean-past-participle','new_production',WI+['U12-G-FB-WYRCEAN']),
 ('gierwan','gierwan','gierwende','gierwed','gierwan-past-participle','new_production',WI),
 ('settan','sęttan','sęttende','sętt','settan-past-participle','new_production',WI),
 ('gewitan','gewītan','gewītende','gewiten','gewitan-past-participle','new_recognition',STR+['U12-G-FB-I','U12-G-FB-READING']),
 ('sittan','sittan','sittende','seten','sittan-participle-citation','new_recognition',STR+['U12-G-FB-IV-V'])
]
for i,h,pr,pa,pa_id,status,ev in parts:
    lemma(i,h); ev=ev+['U12-G-FB-PARTICIPLES']
    cells=[form(i,i+'-present-participle',pr,{'verb_form':'participle','tense':'present','agreement':'base'},ev,status=status,
                scope='Base morphology only; productive perfect/periphrastic syntax requires its explicitly separate construction milestone.'),
           form(i,pa_id,pa,{'verb_form':'participle','tense':'past','agreement':'base'},ev,status=status,
                scope='Selected bare base. Prior citation record, where present, is retained. No full new adjectival declension is inferred.')]
    par(i,'PART',cells,ev,'Both participle bases; '+('production of base morphology' if status=='new_production' else 'recognition/reference morphology')+' only. Syntax is restricted to separately listed constructions.')
    feature('u12-'+i+'-participle-bases','Both '+h+' participle bases.',ev,'Morphology and productive syntax remain separate.',status)

for i,h,inflected,ev,oldid in [
 ('adrifan','ādrīfan','ādrīfanne',STR+['U12-G-FB-I'],'adrifan-inf-citation'),
 ('geneosian','genēosian','genēosianne',WII+['U12-G-LEX-GENEOSIAN'],'geneosian-infinitive-citation')]:
    lemma(i,h)
    if i=='adrifan':
        a=next(x for x in L[i]['forms'] if x['form_id']==oldid); a.update(knowledge_status='new_production',scope_note='Plain infinitive with prior magan; no new infinitival complement family.')
    else: a=form(i,oldid,h,{'mood':'infinitive','type':'plain'},ev,scope='Plain infinitive after volitional willan; previous supplied citation is promoted explicitly.')
    b=form(i,i+'-inflected-infinitive',inflected,{'mood':'infinitive','type':'inflected'},ev,status='new_recognition',scope='Reference morphology; no new tō-infinitive construction is taught.')
    par(i,'INF',[a,b],ev,'Plain infinitive production in the specified modal construction; inflected infinitive recognition only.')
    feature('u12-'+i+'-modal-infinitive','Plain '+h+' in the assigned modal construction.',ev)

TIME=['U12-G-FB-TENSE','U12-G-FULK-TENSE']
PERF=TIME+['U12-ROOT-BT-HABBAN-AGREEMENT','U12-ROOT-BT-HABBAN-SUPPLEMENT']
core = [
 ('u12-narrative-time','Interpret narrative temporal relations from context, clause relations and lexical meaning.',TIME,'The two inflected tenses do not map one-to-one to modern English simple/progressive/perfect categories; prior present-for-future remains in force.','new_production'),
 ('u12-preterite-anterior','A simple preterite can express action earlier than another past viewpoint.',TIME,'Relative anteriority can be made explicit in translation without inventing an Old English compound form.','new_production'),
 ('u12-habban-perfect','Finite habban with a selected transitive past participle expresses a completed action or present/past result.',PERF,'The auxiliary agrees with the subject, while the accusative object is the patient of the participle. Selected bare participles are productive. Object-agreeing alternatives are recognized/accepted only within independently supported inflection; no arbitrary causative or intransitive have-perfect is introduced.','new_production'),
 ('u12-wesan-intransitive-perfect','Recognize wesan with an intransitive past participle, specifically gewiten.',TIME+['U12-G-FB-READING'],'The subject is the departing participant; the phrase is not passive merely because it contains be. Recognize the contextual completed-departure meaning; no unrestricted productive system.','new_recognition'),
 ('u12-wesan-present-participle','Recognize wesan with a present participle, specifically sittende.',TIME,'Context may motivate simple, progressive or durative English. A simple finite Old English verb may also receive progressive English. No obligatory modern progressive category is inferred.','new_recognition'),
 ('u12-active-passive','Compare an active transitive clause with a supported agentless passive and distinguish event from resulting state.',TIME+['U12-G-FB-PARTICIPLES'],'Retains prior u07-passive: a passive subject is the affected entity; converting to agentless passive omits any named active agent. Wearð may focus on coming into the condition, wæs on a state or contextually an event. No mechanical became/was rule or fram-agent production.','new_production'),
 ('u12-reported-sequence','Express simultaneous, anterior and intended-later time relative to a reporting viewpoint.',TIME+['U12-G-FB-MOOD','U12-G-FULK-MOOD'],'Prior report subjunctives provide simultaneous sīe/wǣre; anterior hæfde plus selected participle is new. Hæfde is syncretic and context identifies the report function. Wolde plus infinitive retains volition/intention and does not guarantee later realization. Indicative reports may be defensible; no automatic backshift or subjunctive=false.','new_production')
]
for i,d,ev,scope,st in core: feature(i,d,ev,scope,st)
for i,si,gl,ev,st,rule in [
 ('habban','habban-perfect','auxiliary of completed action/result with a transitive participle',PERF,'new_production',core[2][3]),
 ('wesan','wesan-intransitive-perfect','auxiliary with an intransitive past participle',TIME+['U12-G-FB-READING'],'new_recognition',core[3][3]),
 ('wesan','wesan-present-participle','auxiliary with a present participle',TIME,'new_recognition',core[4][3])]:
    lemma(i); sense(i,si,gl,ev,status=st,scope=rule); frame(i,si,gl,rule,ev,st)

extensions = [
 ('geswican','geswican-fail','fail; cease','Intransitive cease/fail without an expressed genitive object, including seedtime and harvest ceasing or failing in Cook19.16. Earlier genitive cessation remains available for ceasing from rule.',['U12-G-EX19','U12-G-BT-GESWICAN'],'u12-geswican-intransitive'),
 ('slean','slean-kill','slay; kill','Accusative person killed; distinguishes this lethal sense from previously taught strike/smite.',['U12-G-FB-READING','U12-G-LEX-SLEAN'],'u12-slean-kill'),
 ('geseon','geseon-objectless','see; perceive without an expressed object','Seeing is asserted absolutely in the bounded temporal clauses of Cook20.2; no accusative object must be invented.',['U12-G-EX20'],'u12-geseon-objectless'),
 ('on','on-respect','in; with respect to a quality or domain','On+dative with rich/lowly predicates; not physical motion into the noun.',['U12-G-BT-WELIG','U12-G-EX21'],'u12-on-respect'),
 ('beforan','beforan-before-motion','before; ahead of a person','Beforan+dative marks the person before whom someone is sent; extends earlier static location explicitly.',['U12-G-EX19','U12-G-BT-BEFORAN'],'u12-beforan-motion')
]
for i,si,gl,rule,ev,ft in extensions:
    lemma(i,pos=OLD[i]['part_of_speech']); sense(i,si,gl,ev,scope=rule); frame(i,si,gl,rule,ev); feature(ft,rule,ev)

for i,si,ft,gl,rule,ev in [
 ('gierwan','gierwan-1','u12-gierwan-accusative','prepare','Accusative thing prepared; with the selected past participle, habban retains that accusative patient.',WI+['U12-G-EX20']),
 ('writan','writan-1','u12-writan-accusative','write','Accusative text or letter written; prior morphology does not itself establish this lexical frame.',['U12-G-EX19','U12-G-BT-WRITAN']),
 ('sendan','sendan-1','u12-sendan-recipient','send','Accusative person/thing sent and dative recipient; beforan+dative is a separate ahead-of frame.',['U12-G-EX19','U12-G-BT-SENDAN']),
 ('weorpan','weorpan-1','u12-weorpan-accusative','throw; cast','Accusative thing thrown, including the assigned hook.',['U12-G-EX20','U12-G-FB-III']),
 ('welig','welig-rich-in','u12-welig-on-dative','rich in','Welig on+dative identifies the thing or resource in which a person, place or productive event is rich; includes harvest rich in fruit.',['U12-G-BT-WELIG'])]:
    lemma(i,pos=OLD[i]['part_of_speech']); frame(i,si,gl,rule,ev); feature(ft,rule,ev)

particles = [
 ('abutan','ābūtan','preposition','abutan-invariant','abutan-around','around; about','u12-abutan-accusative','Ābūtan+accusative, surrounding a person/thing or building around it.',['U12-G-BT-ABUTAN']),
 ('gemang','gemang','preposition','gemang-invariant','gemang-among','among','u12-gemang-accusative','Selected accusative after sending among a group; the directly attested sheep/wolves passage supports this precise use. Dative location is also attested but is not the selected productive frame.',['U12-G-BT-GEMANG']),
 ('aet','æt','preposition','aet-invariant-source','aet-source','from, with learn','u12-aet-learning-source','Æt+dative marks the person from whom one learns, as in leornian æt a person.',['U12-G-BT-LEORNIAN']),
 ('for','for','preposition','for-invariant-source-source','for-beneficiary','for; on behalf of','u12-for-beneficiary','For+dative identifies the beneficiary in the assigned payment/giving expression; not every for-case or causal use.',['U12-G-EX20','U12-G-BT-FOR'])
]
for i,h,pos,fi,si,gl,ft,rule,ev in particles:
    lemma(i,h,pos); form(i,fi,h,{'invariant':True,'function':pos},ev); sense(i,si,gl,ev,scope=rule); frame(i,si,gl,rule,ev); feature(ft,rule,ev)

for ft,d,ev,scope in [
 ('u12-duration-accusative','Accusative quantity of time expresses duration.',['U12-G-FB-DURATION','U12-G-EX19'],'The supplied forty-years phrase is explicitly local support; this does not establish all numeral systems.'),
 ('u12-extent-genitive','A numeral plus genitive measure noun can state breadth or height.',['U12-G-FB-MEASURE','U12-G-EX21'],'The measure noun fōt is separately taught in full; the twenty-feet quantity remains supplied local support.'),
 ('u12-negative-concord-bounded','Nǣfre and preverbal ne reinforce one negative meaning.',['U12-G-FB-NEGATION','U12-G-EX19','U12-G-EX21'],'Bounded never/never again constructions only; nǣfre mā means never more/again. Do not teach a general negative-pronoun family by implication.'),
 ('u12-predicate-possession','Predicative genitive identifies a possessor; predicative possessive adjectives agree with what is possessed.',['U12-G-EX20','U12-G-PREDICATE-POSSESSION'],'Distinguish an owner in genitive from ðīn in the gender/number of dæg or niht. Earlier attributive forms are reused with an explicit new syntax milestone.'),
 ('u12-more-numerous','Quantitative predicative mā means more in number with a plural subject.',['U12-G-EX20','U12-G-QUANTITY-COMPARISON'],'Selected indeclinable mā plus prior ðonne comparison standard; distinct from earlier adverbial amount of doing. No new māran comparative-adjective system is required.'),
 ('u12-on-elliptic-city','On+accusative with adjectival ōðer may have an understood city noun.',['U12-G-EX21','U12-G-FB-PREPOSITIONS'],'Supplied local on ōðre [ceastre] analysis, using the actual prior ceaster system; no unrestricted nominal ellipsis production is inferred.')
]: feature(ft,d,ev,scope,status='supplied' if ft=='u12-on-elliptic-city' else 'new_production')

lemma('ma',pos='adverb')
sense('welig','welig-rich-in','rich in; abounding in',['U12-G-BT-WELIG'],scope='On+dative names the resource; extends prior person-wealthy scope explicitly to places and productive events, including a harvest rich in fruit.')
sense('ma','ma-again','more; again in never more', ['U12-G-EX21','U12-G-BT-MA'],scope='Bounded nǣfre mā, never more/again; distinct from comparative amount of doing.')
sense('ma','ma-more-numerous','more in number', ['U12-G-QUANTITY-COMPARISON'],scope='Indeclinable quantitative predicate with plural subject and a ðonne comparison standard; explicitly distinct from the prior adverbial use.')
frame('ma','ma-more-numerous','more in number','Plural subject + finite be + indeclinable mā, optionally compared with a nominative standard after ðonne.',['U12-G-QUANTITY-COMPARISON'])
lemma('swa',pos='adverb')
sense('swa','swa-equative-degree','as, marking an equal degree',['U12-G-BT-SWA','U12-G-EX21'],scope='The first single-token swā before the compared adjective. Does not alter the unrelated historical hyphenated swā-swā source record.')
sense('swa','swa-equative-standard','as, introducing a comparison standard',['U12-G-BT-SWA','U12-G-EX21'],scope='The second single-token swā after the adjective; the nominative standard is understood as the subject of be. Explicit extension beyond the earlier finite comparative clause.')
feature('u12-equative-swa-swa','Two separated swā tokens express equality of degree.',['U12-G-BT-SWA','U12-G-EX21'],'First swā is degree; second swā introduces the standard. Bind each to the actual prior swa-invariant form and its new sense; do not invent a compound form spanning the intervening adjective.')
sense('swa','swa-predicative-as','as; like in a predicative comparison',['U12-G-BT-GEMANG','U12-G-EX21'],scope='Bounded comparison of the accusative persons sent with sheep; the comparative nominal refers to the object, not an unrelated nominative subject.')
feature('u12-swa-predicative-comparison','Swā plus a nominal compares the persons sent to sheep.',['U12-G-BT-GEMANG','U12-G-EX21'],'Explicit bounded extension beyond the prior finite comparative clause.')
feature('u12-source-reported-condition','Recognize the selected past reported condition and possibility in the Picts and Scots passage.',['U12-G-FB-READING','U12-G-FB-MOOD'],'Source-specific gif ... gefultumoden and ðæt ... meahten are supplied/analyzed in context. This does not promote a complete new conditional or modal subjunctive system.',status='new_recognition')
feature('u12-gemetan-beneficiary','Finding accusative rest may include the dative beneficiaries.',['U12-G-EX21','U12-G-FB-DATIVE'],'Declared application of Cook160–161 general dative-of-benefit syntax to the bounded Cook21.9 requirement; not a separately quoted dictionary valency witness. It does not require a preposition translating English unto.')
lemma('nagan','nāgan')
form('nagan','nagan-pres-3-sg-local','nāh',{'tense':'present','mood':'indicative','person':3,'number':'sg'},['U12-G-FB-AGAN'],status='supplied',scope='Local contracted negative of āgan for Cook20.4; no full negative system.')
sense('nagan','nagan-local','does not have; does not possess',['U12-G-FB-AGAN'],status='supplied',scope='Only the supplied local third singular nāh.')
feature('u12-negative-agan-local','Supplied nāh for the negative possession clause in Cook20.4.',['U12-G-FB-AGAN'],'Reuse already supplied nis for the other local negative clause; full negative systems are not production.',status='supplied')

data={'schema_version':1,'chapter':'ch12','status':'audited_scope_proposal_pending_coordinator_reconciliation',
      'origin_category':'new_teaching_material','lemmas':list(L.values()),'features':F,'paradigms':P,
      'integration_warning':'Coordinator contract establishes teaching. No private models or answer key consulted. Construction patterns are counted separately from lexical forms and inflectional paradigm cells.'}
for name,obj in [('grammar-records.json',data),('lexical-frames.json',{'schema_version':1,'chapter':'ch12','status':data['status'],'frames':FR})]:
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print({'lemmas':len(L),'forms':sum(len(x['forms']) for x in L.values()),'senses':sum(len(x['senses']) for x in L.values()),'features':len(F),'paradigms':len(P),'paradigm_cells':sum(x['cell_count'] for x in P),'frames':len(FR)})
