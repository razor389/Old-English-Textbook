from pathlib import Path
import json, hashlib, copy

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'sources/audits/unit12-grammar'
def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def write(name,data): (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
E={}
def evidence(ident,sid,pages,loc,claim,paths,limits='',offset=None,url=None):
    rec={'source_id':sid,'printed_pages':pages,'original_identifier':loc,'claim':claim,
         'evidence_limits':limits or 'Only the expressly described morphology or construction is supported; related systems are not automatically assigned.',
         'origin_category':'exact_source','verification':'Original page images directly inspected by unit12_grammar; OCR used only as a finding aid.',
         'images':[{'path':p,'sha256':sha(p),'actually_viewed':True,'viewed_by':'unit12_grammar','inspection_date':'2026-10-25'} for p in paths]}
    if offset is not None:
        rec['pdf_pages_one_based']=[p+offset for p in pages]
        rec['locator_convention']=f'Printed page + {offset} = one-based PDF page; section identifiers are original, not editorial line counts.'
    else:rec['locator_convention']='Original dictionary facsimiles; a/b identify left/right printed columns; no PDF page asserted.'
    if url:rec['record_url']=url
    E[ident]=rec
def cook(ident,pages,loc,claim,limits=''):
    paths=[]
    for p in pages:
        own=f'sources/audits/unit12-grammar/cook_fb_1895_2-p{p}.png'
        old=f'sources/audits/unit11-grammar/cook_fb_1895_2-p{p}.png'
        paths.append(own if (ROOT/own).exists() else old)
    evidence(ident,'cook_fb_1895_2',pages,loc,claim,paths,limits,16)
def bt(ident,entry,page,component,loc,claim,limits=''):
    part='b' if component=='main' else 'd'
    evidence(ident,'bosworth_toller_1898_1921',[page],f'{component} {page}, {loc}',claim,
             [f'sources/audits/unit12-grammar/bt-{entry}-bt_{part}{page:04d}.jpg'],limits,url=f'https://bosworthtoller.com/{entry}')

cook('U12-G-FB-STRONG',[54,55],'§§93–95','Complete strong-verb present/preterite endings, stem distribution, infinitive, participles and commands. Explicit plural person cells may share one printed plural form.')
cook('U12-G-FB-DENTALS',[24,25],'§§33–35','Dental interactions and consonant simplification; d/t plus ð gives tt/t. This rule is not misapplied to claim cȳðan has a d-stem.')
cook('U12-G-FB-I',[58,59],'§§100–102','Class I stem distribution and contraction background; supports ādrīfan/rīsan/gewītan patterns with their checked lexical identities.')
cook('U12-G-FB-II',[60,61],'§103 and contract/consonant notes','Class II ablaut and flēon contraction; selected īe in second/third present singular, flēah/flugon and long contracted imperative flēoh.')
cook('U12-G-FB-III',[61,62],'§104','Class III weorpan stem system and ordinary strong command formation.')
cook('U12-G-FB-IV-V',[63,64],'§§105–106, especially sittan with biddan','Sittan shares the class V system of biddan; seten follows its past-participial base pattern. Present sittende uses the unchanged present stem.')
cook('U12-G-FB-VII',[67],'§110','Hātan hēt hēton hāten and prescribed present umlaut; gehātan retains the lexical prefix in the selected derivative system.')
cook('U12-G-FB-WI',[68,69,72],'§§113,117','Weak I complete endings and explicit exceptional principal parts: sęttan, sęndan, ēhtan, mētan, gierwan. Gier(w)ed permits selected gierwed; past ēhte and sętt are preserved.')
cook('U12-G-FB-WII',[73,74],'§§118–120','Weak II present -ie/-ast/-að/-iað, dental preterite in -ode and imperative -a/-iað. Complete clearly defined systems are derived from this pattern and checked headwords.')
cook('U12-G-FB-BRINGAN',[70],'§114','Bringan has the weak preterite brōhte; the present-stem command uses bring-.')
cook('U12-G-FB-WYRCEAN',[70],'§114','Wyrcean worhte (ge)worht; prefixed gewyrcean gives selected geworht, not a regularized *gewyrc(e)d.')
cook('U12-G-FB-AGAN',[76,77],'§§125,127','Āgan present āh/āhst/āgon and preterite āhte; nāgan is its negative counterpart. Unit scope is the complete positive indicative and one supplied negative third singular, not all listed moods.')
cook('U12-G-FB-PARTICIPLES',[54,55,100],'§§93–95,179','Present/past participle base morphology and predicative uninflected participles. Displaying bases does not establish full adjective declensions or free progressive/perfect syntax.')
cook('U12-G-FB-TENSE',[101,102],'§§186–188','Only two independent tenses; context determines future, perfect and pluperfect translations. Habban plus transitive past participle and be with intransitive past participle are explicitly described.')
cook('U12-G-FB-MOOD',[103,104],'§§192–196','Contextual indicative/subjunctive uses in reported and dependent clauses; no automatic English backshift doctrine is asserted.')
cook('U12-G-FB-READING',[145,146],'Picts and Scots, selected passage; p146 notes3 and11','Selected source includes wæs onweg gewiten, reported promise/conditional, past sequence and active narration where Latin had a passive. Notes preserve distinctions among the three successive ðā forms.','Selected span ends at and hīe mid ealle foriermdon. Line numbers in our transcription are explicitly editorial, not printed line labels.')
cook('U12-G-FB-PREPOSITIONS',[96,97],'§172','On commonly marks rest with dative and motion with accusative; this is a constructional distinction with documented limits, not an exceptionless semantic shortcut.')
cook('U12-G-FB-DURATION',[96],'§170','Accusative extent/duration of time; supports bounded forty-years requirement without promoting the entire higher numeral system.')
cook('U12-G-FB-MEASURE',[90],'§154c','Numerals with genitive measures, including eahta fōta, support the assigned dimensional quantity construction.')
cook('U12-G-FB-DATIVE',[93,94],'§§160–161,164','General dative of benefit or interest, with original Old English examples; Cook21.9 beneficiary with find rest is a declared application of this general syntax.','This is not a claim that these pages contain an exact gemētan plus rest lexical example.')
cook('U12-G-FB-NEGATION',[100],'§183','Negative words/constructions may reinforce a single negative meaning; bounded nǣfre with preverbal negation is explicitly distinguished from a general negative-family assignment.')
for ident,page,loc,claim in [
 ('U12-G-LEX-ADRIFAN',273,'ādrīfan','Class I expel/drive out lexical identity.'),
 ('U12-G-LEX-GEMETAN',293,'gemētan','Weak I find lexical identity; not unlengthened gemetan measure.'),
 ('U12-G-LEX-GEOPENIAN',293,'geopenian','Weak II open lexical identity.'),
 ('U12-G-LEX-GENEOSIAN',293,'genēosian','Weak II visit lexical identity.')]:cook(ident,[page],'Glossary, '+loc,claim)
E['U12-G-LEX-SLEAN']=copy.deepcopy(E['U12-G-FB-READING'])
E['U12-G-LEX-SLEAN']['claim']='The selected passage uses slōgon of the killing of the Britons; this supports the explicit kill/slay extension beyond earlier strike.'

for ident,pages,loc,claim in [
 ('U12-G-FULK-TENSE',[31,32,33],'§§48–52','Two inflected tenses; contextual past/anterior/future interpretation, compound perfects, and limited be plus present participle. Willan retains volition. Fulk spelling is not silently substituted for Cook.'),
 ('U12-G-FULK-MOOD',[28,29],'§§45–46','Reported mood and dependent-clause interpretation depend on viewpoint; a subjunctive does not imply that a proposition is false.')]:
    paths=[f'sources/audits/unit12-grammar/fulk-2020-p{p}.png' if p>=31 else f'sources/audits/unit11-grammar/fulk-2020-p{p}.png' for p in pages]
    evidence(ident,'fulk-2020',pages,loc,claim,paths,offset=12)
evidence('U12-G-WRIGHT-DENTALS','wright_oe_1914',[248],'§476','Regular loss of þ before -st, with analogical retention also documented, and þ+þ coalescence. Selected cȳst/cȳð are derived from checked cȳðan, not claimed as separate printed lexical attestations.',
         ['sources/audits/unit12-grammar/wright_oe_1914-p248.png'],offset=20)
for ex,ps in [(19,[9,10]),(20,[10]),(21,[10,11])]:
    evidence(f'U12-G-EX{ex}','cook_ex_1895',ps,f'Group VI Exercise {ex}',
             'Exact original English prompts and explicit grammatical controls establish required scope; they are not themselves an Old English model answer.',
             [f'sources/audits/course-map/ex-page{p:02d}.png' for p in ps],offset=8)

bt('U12-G-BT-GEHATAN',14611,398,'main','gehātan','Promise with accusative thing and dative recipient; selected hēt preterite is documented.')
E['U12-G-BT-GEHATAN']['additional_evidence']={'source_id':'bosworth_toller_1898_1921','original_identifier':'Supplement338b, gehātan IV','images':[{'path':'sources/audits/unit12-grammar/bt-48229-bt_d0338.jpg','sha256':sha('sources/audits/unit12-grammar/bt-48229-bt_d0338.jpg'),'actually_viewed':True,'viewed_by':'unit12_grammar'}]}
bt('U12-G-BT-FLEON',45203,224,'supplement','flēon I–II','Distinct intransitive flight and transitive avoiding/fleeing accusative persons or things. Main292 supplies principal forms; Cook supplies selected īe spelling.')
E['U12-G-BT-FLEON']['additional_evidence']={'source_id':'bosworth_toller_1898_1921','original_identifier':'Main292a, flēon','images':[{'path':'sources/audits/unit12-grammar/bt-10921-bt_b0292.jpg','sha256':sha('sources/audits/unit12-grammar/bt-10921-bt_b0292.jpg'),'actually_viewed':True,'viewed_by':'unit12_grammar'}]}
bt('U12-G-BT-GRETAN',17502,489,'main','weak grētan,II','Take leave of an accusative person; Cook21.12 explicitly extends the farewell object to native land. Weak grētan is distinct from strong weep.','The place-object extension is declared editorial application to Cook21.12, not a claim that the cited person example has a place object.')
bt('U12-G-BT-CYTHAN',7294,191,'main','cȳðan','Past cȳðde/cȳdde and 2sg variants; third present cȳþ. Accusative announced thing and dative recipient are directly illustrated; dictionary accents are normalized to course macrons.')
bt('U12-G-BT-EHTAN',9159,244,'main','ēhtan','Both genitive and accusative government; the exact Matthew10.23 example uses accusative eow. Header gives ēht/ēhte/ēhton.')
bt('U12-G-BT-LEORNIAN',21483,634,'main','leornian','Learn with accusative thing, and learn from æt+dative person; the Matthew11.29 source example directly supports the objectless learning-from phrase.')
bt('U12-G-BT-GESWICAN',49917,422,'supplement','geswīcan I,IV–V','Intransitive cessation and failure include things, not merely transitive/genitive cessation. Cook19.16 seasonal subjects are a bounded application.')
bt('U12-G-BT-WRITAN',36660,1275,'main','wrītan III–IV','Write letters/text, taking the written object in accusative; letter-writing sense is distinct from physical incision.')
bt('U12-G-BT-SENDAN',27430,862,'main','sendan I–II','Accusative sent person or thing, with dative recipient explicitly illustrated; no implied promotion of every complement.')
bt('U12-G-BT-WELIG',35019,1186,'main','welig adjective,(1)–(3)','Rich persons/places and productive things; swā welig on wæstmum directly supports rich-in resources, allowing an explicit bounded harvest application.')
bt('U12-G-BT-BEFORAN',3398,77,'main','beforan preposition,I–II','Before with dative and accusative is distinguished; Cook19.6 explicitly selects dative through§166. Extending before to sending is bounded, not a general rule from motion alone.')
bt('U12-G-BT-ABUTAN',121,4,'main','ābūtan preposition','Around/about governs accusative; separate adverb entry is not used to infer government.')
bt('U12-G-BT-GEMANG',15160,414,'main','gemang preposition,II','Selected accusative among, including the exact sending sheep among wolves example. Dative is also documented separately.')
bt('U12-G-BT-FOR',45383,231,'supplement','for,A with dative,III(8)','Dative for on behalf of/in support of; combines with the earlier giving construction in the assigned beneficiary use.')
bt('U12-G-BT-SWA',29493,940,'main','swā IV(2)(b),V(1)(a),V(11)','Degree comparison uses two separated swā tokens; contracted comparisons allow an understood predicate. Does not promote the unrelated hyphenated source form.')
bt('U12-G-BT-MA',22005,653,'main','mā adverb','More/further, including negated future continuation and no longer; bounded never-more use is separate from quantitative predicate mā.')

# Import coordinator evidence with its original inspector provenance intact.
for ident,rec in read('sources/audits/unit12-coordinator/habban-agreement-evidence.json')['evidence'].items():
    E[ident]=copy.deepcopy(rec)
    E[ident]['independent_grammar_inspection']='Unit12 grammar analyst also directly inspected the decisive main497a / supplement493a image; other images retain coordinator-only inspection attribution.'
extensions=read('sources/audits/unit12-coordinator/construction-extension-evidence.json')['records']
for rec in extensions:
    out=copy.deepcopy(rec);ident=out.pop('evidence_id');E[ident]=out
E['U12-G-PREDICATE-POSSESSION']={'source_id':'bosworth_toller_1898_1921','origin_category':'new_teaching_material',
    'original_identifier':'Composite checked predicate-possession evidence: main255b and1059b–1060a',
    'evidence_refs':['U12-ROOT-BT-PREDICATE-GENITIVE','U12-ROOT-BT-PREDICATE-POSSESSIVE'],
    'claim':'Predicative genitive marks the owner; predicative possessive adjectives retain agreement with the possessed entity.',
    'verification':'Coordinator image-checked primary records retained with their original inspector attribution.'}
E['U12-G-QUANTITY-COMPARISON']=copy.deepcopy(E['U12-ROOT-BT-QUANTITATIVE-MA'])
E['U12-G-QUANTITY-COMPARISON']['independent_grammar_inspection']='The same main653 facsimile was independently inspected as bt-22005-bt_b0653.jpg; quantitative entry is distinct from the adjacent adverb entry.'

records=read('sources/audits/unit12-grammar/grammar-records.json')
frames=read('sources/audits/unit12-grammar/lexical-frames.json')
def refs(obj):
    result=set()
    if isinstance(obj,dict):
        result.update(obj.get('evidence_refs',[]))
        for k,v in obj.items():
            if k not in ['prior_record','evidence_refs']: result.update(refs(v))
    elif isinstance(obj,list):
        for v in obj: result.update(refs(v))
    return result
missing=sorted((refs(records)|refs(frames))-set(E))
if missing:raise ValueError('Missing evidence: '+repr(missing))
write('evidence-catalog.json',{'schema_version':1,'chapter':'ch12','status':'image_checked_evidence_complete','evidence':E,
      'normalization':'Cook selected spelling and length marks remain authoritative for the course; BT accents may be converted to macrons only in declared teaching selections. Source transcription remains separate.',
      'independence':'No private model or key opened. Limited answer-clause exposure for Cook21.4 occurred in an unsolicited source-agent message during construction discussion and was disclosed immediately; the other tasks remain reserved for independent solving.'})

morph=[
 ('U12-R-STRONG-SYSTEMS','Strong indicative systems','The present singular uses -e, -st, -ð and plural -að, subject to stated stem/dental changes. Preterite first/third singular share the selected singular stem; second singular uses the plural stem with -e; all plural persons use -on. Ādrīfan has ī/ā/i; gehātan retains ge- and selects hā-/hēt-, with hǣt- in second/third present singular. Flēon is contracted: flēo-, flīeh-, flēah-, flug- are explicitly distributed, not mechanically generated from the citation.',STR if False else ['U12-G-FB-STRONG','U12-G-FB-I','U12-G-FB-II','U12-G-FB-VII']),
 ('U12-R-WEAK-I','Weak I selected systems','Gemētan and grētan retain ē; t before the third-singular dental yields selected -tt, and the preterite is -tte/-ttest/-tton. Ēhtan has ēht in third present singular and ēhte/-est/-on in the preterite, not an invented doubled dental. Cȳðan selects cȳst and cȳð after regular dental interaction; cȳðde/-dest/-don is selected, with attested cȳdde variants recognized. These are complete present/preterite indicative systems only.',['U12-G-FB-WI','U12-G-FB-DENTALS','U12-G-BT-CYTHAN','U12-G-WRIGHT-DENTALS']),
 ('U12-R-WEAK-II','Weak II selected systems','Geopenian and leornian have -ie, -ast, -að, -iað in the present, and -ode, -odest, -ode, -odon in the preterite. The plural form serves all persons; each person/number coordinate is still displayed.',['U12-G-FB-WII']),
 ('U12-R-AGAN','Āgan positive indicative','Āh/āhst/āh and plural āgon form the present; āhte/āhtest/āhte and plural āhton form the preterite. These cells are the full defined positive indicative. Supplied nāh does not establish a negative paradigm.',['U12-G-FB-AGAN']),
 ('U12-R-COMMANDS','Nine complete direct-command pairs','Both singular and plural are provided for sęndan, bringan, ādrīfan, flēon, gemētan, geopenian, weorpan, leornian and rīsan. Strong long stems and long weak I stems use the selected bare singular; contracted flēon has flēoh; weak II uses -a singular and -iað plural. The commands do not imply newly productive subjunctives.',['U12-G-FB-STRONG','U12-G-FB-II','U12-G-FB-WI','U12-G-FB-WII']),
 ('U12-R-PARTICIPLE-BASES','Five complete base pairs with unequal learning scope','Gewyrcean/gewyrcende/geworht, gierwan/gierwende/gierwed and sęttan/sęttende/sętt have productive present and past bases; their larger syntactic uses remain separately bounded. Gewītan/gewītende/gewiten and sittan/sittende/seten are recognition/reference pairs. A displayed participle base is not a complete adjectival declension or an unrestricted perfect/progressive system.',['U12-G-FB-PARTICIPLES','U12-G-FB-WYRCEAN','U12-G-FB-WI','U12-G-FB-IV-V']),
 ('U12-R-INFINITIVES','Two complete plain/inflected shape pairs','Ādrīfan/ādrīfanne and genēosian/genēosianne show both shapes. Plain infinitives are productive only with the already taught specified modals; inflected shapes are recognition/reference.',['U12-G-FB-STRONG','U12-G-FB-WII']),
 ('U12-R-COMPOUND-DISPLAY','Twelve construction positions, not twelve inflectional cells','The complete present and preterite habban construction display has six person/number positions for each tense and binds prior finite auxiliary forms, prior accusative ðæt hūs and new productive geworht. Count these as construction examples separately; do not fabricate multiword lexical forms. The finite auxiliary agrees with the subject; the object is the participle patient.',['U12-G-FB-TENSE','U12-ROOT-BT-HABBAN-AGREEMENT','U12-ROOT-BT-HABBAN-SUPPLEMENT'])
]
rules=[{'rule_id':i,'title':title,'rule':rule,'evidence_refs':ev,'origin_category':'new_teaching_material','knowledge_status':'new_production'} for i,title,rule,ev in morph]
rules += [{'rule_id':'U12-R-'+x['feature_id'][4:].upper(),'feature_id':x['feature_id'],'rule':x['description'],
           'scope_and_limits':x.get('scope_note',''),'knowledge_status':x['knowledge_status'],
           'evidence_refs':x['evidence_refs'],'origin_category':'new_teaching_material'} for x in records['features']]
write('rules.json',{'schema_version':1,'chapter':'ch12','status':'audited_scope_proposal_pending_contract','rules':rules,
      'principle':'Complete morphology and productive syntax are distinct assignments. Prior learning is established by the actual baseline records, not by headword familiarity or archived course milestones.'})
print({'evidence_records':len(E),'rules':len(rules),'missing_refs':missing})
