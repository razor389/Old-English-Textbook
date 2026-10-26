"""Exact local helps, independently of the productive finite-system proposal."""
import build_records as m
PRODUCTIVE={s['sense_id']:s for l in m.D['lemmas'] for s in l['senses']}
m.D={'schema_version':1,'chapter':'ch13','status':'independent_audit_proposal','baseline':'e17fc5f','lemmas':[],'features':[],'local_support':[],'source_evidence_examples':[]};m.L={}
def add(i,h,t,parse,sid,g,ev,fid=None,pos='verb'):
    old=m.OLDF.get(fid); old_s=m.OLDS.get(sid)
    s=m.sense(i,h,sid,g,ev,'Exact source or explicitly scaffolded expression only; no independent lexical recall.','new_production' if old_s and old_s.get('production_taught_in') else 'supplied',pos)
    if sid in PRODUCTIVE:
        m.L[i]['senses']=[x for x in m.L[i]['senses'] if x['sense_id']!=sid]
    f=m.form(i,h,t,{'source_analysis':parse},ev,fid or i+'-u13-source-'+str(len(m.L[i]['forms'])+1),'new_production' if old and old.get('production_taught_in') else 'supplied',scope='Exact locally supported form; no complete new verbal or nominal system is implied.',pos=pos)
    return {'lemma_id':i,'form_id':f['form_id'],'sense_id':s}
rows=[
('hwaethwugu','hwæthwugu','hwæthwugu','neuter indefinite substantive, something','hwaethwugu-u13-source','something; hwæthwugu swilces, something of that sort','152.3',None,'indefinite'),
('ute','ūte','ūte','invariant adverb','ute-u13-source','outside','152.3,153.6',None,'adverb'),
('gelomlice','gelōmlice','gelōmlice','invariant adverb','gelomlice-u13-source','frequently; regularly','152.5',None,'adverb'),
('semninga','sęmninga','sęmninga','invariant adverb','semninga-u13-source','suddenly','152.7',None,'adverb'),
('se','se','ðon','neuter demonstrative dative singular source variant after æfter','se-u13-after-that','that, in temporal æfter ðon: after that','152.8,153.16','se-dat-n-sg-result-source','demonstrative'),
('singan','singan','singendra','substantival genitive plural present participle','singan-u13-singing-source','of people singing','152.9',None,'verb'),
('blissian','blissian','blissiendra','substantival genitive plural present participle','blissian-u13-source','of people rejoicing','152.9',None,'verb'),
('thanan','ðanan','ðanan','invariant adverb','thanan-u13-source','thence; from there','152.12',None,'adverb'),
('ingangan','ingangan','ingangende','present participle, uninflected predicative form','ingangan-u13-source','going in; entering','152.14',None,'verb'),
('ymbsellan','ymbsęllan','ymbsealde','preterite indicative third singular','ymbsellan-u13-source','surrounded; enveloped','152.15',None,'verb'),
('geornlice','geornlice','geornlice','invariant adverb','geornlice-u13-source','earnestly; attentively','152.16',None,'adverb'),
('athenian','āðęnian','āðęnede','preterite indicative third singular','athenian-u13-attend','directed; stretched (his mind toward the things heard)','152.16',None,'verb'),
('upastigan','ūpāstīgan','ūpāstīgan','plain infinitive in accusative-and-infinitive perception construction','upastigan-u13-source','rise up; ascend','152.18',None,'verb'),
('efthweorfan','ęfthweorfan','ęfthweorfan','plain infinitive in perception construction','efthweorfan-u13','return; turn back','152.21','efthweorfan-infinitive-u13-source','verb'),
('wundrian','wundrian','wundriende','present participle, uninflected supplementary predication','wundrian-u13-source','wondering','153.1',None,'verb'),
('wafian','wafian','wafiende','present participle, uninflected supplementary predication','wafian-u13-source','amazed; in astonishment','153.1',None,'verb'),
('thencan','ðęncan','ðōhte','preterite indicative third singular','thencan-u13-source','thought','153.2',None,'verb'),
('smeagan','smēagan','smēade','preterite indicative third singular','smeagan-u13-source','pondered; considered','153.2',None,'verb'),
('ontynan','ontȳnan','ontȳnde','preterite indicative third singular','ontynan-u13-source','opened','153.4',None,'verb'),
('slean','slēan','slōg','preterite indicative third singular','slean-u13-signal','made a signal, in slōg tācen','153.5','slean-pret-3-sg','verb'),
('gan','gān','Gang','singular imperative, exact source initial capital and gang variant','gan-u13-gang-source','go!','153.7',None,'verb'),
('hrathe','hraðe','hraðe','invariant adverb','hrathe-u13-source','quickly','153.7',None,'adverb'),
('mid','mid','mid','adverbial use without expressed object','mid-u13-along-source','along; with them, in mid wes','153.9','mid-adverb-u13-source','adverb'),
('in','in','in','adverb, direction inward','in-u13-inward-source','in; inward','153.6–7','in-adverb-u13-source','adverb'),
('mid','mid','mid','preposition with dative manner noun','mid-u13-manner-source','with; in the manner of the accompanying quality or mental disposition','152.20,153.2','mid-invariant-source','preposition'),
('swa-swa','swā-swā','swā-swā','adverbial approximation before measure','swa-swa-u13-approximately','about; approximately (Latin quasi in source note)','152.17','swa-swa-invariant-source','adverb'),
('sculan','sculan','sceolden','preterite subjunctive third plural in embedded question','sculan-u13-interpretive-source','should; might, asking what the events were to mean','153.3','sculan-preterite-subj-3-pl','verb'),
('in','in','in','preposition plus accusative direction within attention idiom','in-u13-directed-source','towards; onto, in directed his mind towards these things','152.16','in-acc-u13-source','preposition'),
('to','tō','tō','postposed preposition governing dative addressee him','to-u13-addressee-source','to (a speech addressee), postposed in cwæð him tō','153.7','to-preposition-dative-invariant','preposition'),
('to','tō','tō','preposition within explicitly supplied result-position phrase','to-u13-at-root-source','at/to the root, in bounded tō ðæs trēowes wyrttruman','Exercises23.8','to-preposition-dative-invariant','preposition'),
('hwaethwega','hwæthwega','hwæthwega','indefinite substantive, something','hwaethwega-u13-source','something; local indefinite support only','Exercises25.3',None,'indefinite'),
('to-morgen','tō-morgen','tō-morgen','invariant temporal adverb','to-morgen-u13-source','tomorrow','Exercises24.9','to-morgen-invariant-source','adverb'),
('herian','hęrian','hęriendra','substantival genitive plural present participle within supplied phrase','herian-u13-praising-source','of people praising','Exercises25.10',None,'verb'),
('cwethan','cweðan','cweðendra','substantival genitive plural present participle within supplied phrase','cwethan-u13-saying-source','of people saying','Exercises25.10',None,'verb'),
]
bindings=[]
for i,h,t,p,s,g,loc,f,pos in rows:
    ev=[('U13-EX12' if loc.startswith(('Exercises23','Exercises24')) else 'U13-EX13')] if loc.startswith('Exercises') else ['U13-FB152','U13-FB153']
    if i=='to-morgen':ev.append('U13-WRIGHT-P294')
    x=add(i,h,t,p,s,g,ev,f,pos);x.update(surface=t,locator=loc,help=g);bindings.append(x)
    if i in ['herian','cwethan'] and loc=='Exercises25.10':
        r=next(z for z in m.L[i]['forms'] if z['form_id']==x['form_id'])
        r.update(origin_category='new_teaching_material',evidence_basis='Supplied composition form derived from checked participle base plus previously taught strong genitive plural ending; not an exact Old English quotation.',evidence_refs=['U13-FB71','U13-FB72','U13-FB102'] if i=='herian' else ['U13-FB55','U13-FB102'])
m.D['local_support']=bindings
# Existing source-supported identities retained with their original histories.
for i,h,t,p,s,g,f,pos in [
('aefter','æfter','æfter','preposition governing dative','aefter-after-source','after, temporal with dative','aefter-invariant-source','preposition'),
('an','ān','āna','weak nominative masculine singular in predicative alone expression','an-alone','alone','an-nom-m-sg-weak-alone-source','adjective'),
('swa-swa','swā-swā','swā-swā','comparative conjunction','swa-swa-as-source','just as','swa-swa-invariant-source','conjunction'),
('in','in','in','preposition, including postposed in relative clause','in-u11-source','in, with dative location','in-invariant-dat-source','preposition')]:add(i,h,t,p,s,g,['U13-FB152','U13-FB153','U13-FB106'],f,pos)
frag=[]
frag.append(add('aefter','æfter','Æfter','source-capitalized temporal preposition','aefter-after-source','after',['U13-FB153'],'aefter-initial-u13-source','preposition'))
frag.append(add('se','se','ðon','neuter dative demonstrative after temporal æfter','se-u13-after-that','that',['U13-FB153'],'se-dat-n-sg-result-source','demonstrative'))
frag.append(add('he','hē','hē','nominative masculine singular subject','he-1','he (Chad)',['U13-FB153'],'he-m-nom-sg','pronoun'))
frag.append(add('undertheodan','underðēodan','underðēodde','preterite indicative third singular','undertheodan-u13-added-source','added; subjoined (to his speech)',['U13-FB153'],'undertheodan-pret-3-sg-u13-source','verb'))
for n,(x,surface) in enumerate(zip(frag,['Æfter','ðon','hē','underðēodde']),1):x.update(token_index=n,surface=surface,knowledge_status='previously_taught' if n==3 else 'supplied')
m.D['source_evidence_examples']=[{'example_id':'NEW-U13-SOURCE-ORDER-FRAGMENT','origin_category':'exact_source','source_id':'cook_fb_1895_2','printed_page':153,'pdf_page':169,'printed_lines':'16','text':'Æfter ðon hē underðēodde','translation':'After that he added','local_support':'This complete fragment is supplied as corroborative evidence outside the assigned continuous reading. Æfter ðon means after that; hē is Chad; underðēodde means added to his speech (Cook note13: Latin subjunxit). Identify its order only; no independent translation or lexical recall is required. The fronted temporal phrase is followed by subject pronoun, then finite verb.','tokens':frag,'required_form_ids':[x['form_id'] for x in frag],'required_sense_ids':[x['sense_id'] for x in frag],'required_feature_ids':['u13-pronoun-position-limits'],'evidence_refs':['U13-FB153','U13-FULK50']}]
m.D['features']=[{'feature_id':'u13-source-local-idioms','knowledge_status':'supplied','scope_note':'Full local help accompanies source-only participial genitives, approximative swā-swā, attention idiom, signal idiom, modal embedded question, preposition stranding, in/mid adverbs and exact nonfinite variants. Recognizing their role in a scaffolded clause is not independent recall.','evidence_refs':['U13-FB152','U13-FB153','U13-FB106']}, {'feature_id':'u13-bounded-formula-support','knowledge_status':'supplied','scope_note':'Cook25.10–11 praising/saying genitives and doxology,24.9 little-faith address,25.3 hwæthwega and24.7 negative-copula/worthy-content expression receive complete local phrase help. No productive genitive participle declension or -hwega family is inferred.','evidence_refs':['U13-EX12','U13-EX13']}, {'feature_id':'u13-source-after-that','knowledge_status':'supplied','scope_note':'æfter ðon source dative demonstrative retained, including supplied corroboration fragment. Do not relabel existing instrumental cells as dative or change historical analysis of the earlier result-connective record.','evidence_refs':['U13-FB152','U13-FB153']}]
m.D['source_evidence_examples'][0].pop('printed_lines')
m.D['source_evidence_examples'][0].update(editorial_line_count=16,line_count_convention='Line16 is counted from the adjacent printed15 marker; the scan does not print16 beside that line.')
m.D['features'][1]['scope_note']='Cook25.10–11 praising/saying genitives and doxology,24.9 little-faith address,25.3 hwæthwega and23.8 at-root expression receive complete local phrase help. No productive genitive participle declension or -hwega family is inferred. Worthy+ðæt is separately bounded productive syntax; uncontracted ne eom reuses taught words.'
m.D['features'].append({'feature_id':'u13-to-at-root-support','knowledge_status':'supplied','scope_note':'Supply the complete local expression tō ðæs trēowes wyrttruman for Cook23.8, at/to the root of the tree. Do not infer a general static tō rule from this phrase.','evidence_refs':['U13-EX12','U13-FB95']})
source_tokens=m.json.loads((m.ROOT/'sources/audits/unit13-source/reading-tokens.json').read_text(encoding='utf8'))['tokens']
for help_record in m.D['local_support']:
    if help_record['locator'].startswith('Exercises'):continue
    matches=[t for t in source_tokens if t['surface'].strip('.,;:“”!?').casefold()==help_record['surface'].casefold()]
    # Homographs may have distinct local senses; retain all exact occurrences as cross-references.
    locs=[]
    for t in matches:
        for loc in t['source_locators']:
            if loc not in locs:locs.append(loc)
    if locs:
        help_record['source_locators']=locs
        help_record['source_token_ids']=[t['token_id'] for t in matches]
        help_record['locator']='; '.join(str(x['printed_page'])+'.'+str(x['editorial_line']) for x in locs)
        help_record['locator_convention']='Editorial line counts copied from the source editor’s exact token map; printed five-line markers anchor the count.'
m.write('source-support.json',m.D)
print('Written exact support:',len(m.D['lemmas']),'lemmas,',sum(len(l['forms']) for l in m.D['lemmas']),'forms')
