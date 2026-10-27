"""Build auditable, literal U15 records; never mutates the active registers."""
import copy, hashlib, json, pathlib
R=pathlib.Path(__file__).resolve().parents[3]; O=pathlib.Path(__file__).resolve().parent
L={x['lemma_id']:x for x in json.loads((R/'lexicon/entries.json').read_text(encoding='utf-8-sig'))['lemmas']}
D={'schema_version':1,'chapter':'ch15','baseline':'9129cda','status':'independent_audit_proposal_pending_coordinator_contract','origin_category':'new_teaching_material','lemmas':[],'paradigms':[],'features':[],'rules':[]}
LM={}
def lemma(i,h,pos='verb'):
    if i not in LM:
        LM[i]={'lemma_id':i,'display_headword':h,'part_of_speech':pos,'prior_lemma_present':i in L,'forms':[],'senses':[]}
    return LM[i]
def sense(i,h,sid,gloss,ev,status='new_production',scope=''):
    lemma(i,h).setdefault('senses',[]).append({'sense_id':sid,'gloss':gloss,'knowledge_status':status,'evidence_refs':ev,'scope_note':scope,'teaching_ids':['NEW-U15-VOC-'+i.upper()]})
def cell(i,h,fid,surf,a,ev,status='new_production',prior=None):
    q={'form_id':fid,'form':surf,'analysis':a,'knowledge_status':status,'evidence_refs':ev,'origin_category':'new_teaching_material','evidence_basis':'rule-derived completion from personally inspected primary images; not an assertion of separate attestation of this cell'}
    if prior is not None:q['prior_scope']={k:prior.get(k) for k in ('recognition_taught_in','production_taught_in','supplied_in','analysis')}
    if not any(x['form_id']==fid for x in lemma(i,h)['forms']):LM[i]['forms'].append(q)
    return q
def system(i,h,tag,cells,rule,scope,ev):
    pid='NEW-U15-PAR-'+i.upper()+'-'+tag
    for c in cells:
        c.setdefault('teaching_ids',[]).append(pid)
        c['scope_note']=scope
    D['paradigms'].append({'paradigm_id':pid,'lemma_id':i,'system':tag,'teaching_id':pid,'rule_id':rule,'scope_note':scope,'evidence_refs':ev,'display_route':pid+'-DISPLAY','cells':cells})
    return pid
def feature(i,title,txt,ev,status='new_production',prior=()):
    D['features'].append({'feature_id':i,'title':title,'description':txt,'scope_note':txt,'knowledge_status':status,'evidence_refs':ev,'teaching_ids':['NEW-U15-GRAM-'+i.upper()],'prior_feature_refs':list(prior)})
def rule(i,txt,ev):D['rules'].append({'rule_id':i,'statement':txt,'evidence_refs':ev})
def finite(i,h,tag,present,past,ev,ruleid,scope,polarity=None):
    cs=[]
    for tn,st,series in [('present','pres',present),('preterite','pret',past)]:
        for n,ps in [('singular',range(1,4)),('plural',range(1,4))]:
            for p in ps:
                ix=p-1 if n=='singular' else 3
                suffix='-negative' if polarity else ''
                fid=f'{i}-{st}-{p}-'+('sg' if n=='singular' else 'pl')+suffix
                a={'tense':tn,'mood':'indicative','person':p,'number':n}
                if polarity:a['polarity']=polarity
                old=next((f for f in L.get(i,{}).get('forms',[]) if f['form_id']==fid),None)
                cs.append(cell(i,h,fid,series[ix],a,ev,prior=old))
    return system(i,h,tag,cs,ruleid,scope,ev)

# Complete core negative/indefinite systems.
nev=['U15-G-FB78','U15-G-FB79','U15-G-FB100']
rule('U15-R-NEG','Ne precedes a finite verb. The selected negative copula combines uncontracted ne eom/ne eart/ne sindon with nis and the contracted preterite næs/nǣre/nǣron. These alternatives form one complete twelve-position indicative construction table. An uncontracted cell contains two existing words, not a new multiword inflected verb. Negative willan selects Cook’s e-vowel alternatives nelle/nelt/nele/nellað and nolde/noldest/noldon. Other spellings are valid source variants, not extra selected recall targets.',nev)
ws=[]
for tn,st,seq in [('present','pres',['ne eom','ne eart','nis','ne sindon']),('preterite','pret',['næs','nǣre','næs','nǣron'])]:
    for n,ps in [('singular',range(1,4)),('plural',range(1,4))]:
        for p in ps:
            surf=seq[p-1 if n=='singular' else 3]; a={'tense':tn,'mood':'indicative','person':p,'number':n,'polarity':'negative'}
            if surf.startswith('ne '):
                ws.append({'cell_id':f'wesan-negative-{st}-{p}-{n}','display':surf,'analysis':a,'knowledge_status':'new_production','components':[{'lemma_id':'ne','form_id':'ne-invariant','form':'ne'},{'lemma_id':'wesan','form_id':f'wesan-{st}-{p}-'+('sg' if n=='singular' else 'pl'),'form':surf[3:]}],'evidence_refs':nev,'evidence_basis':'two-word construction from prior forms with a newly explicit negative-copula scope; not a new inflected word'})
            else:
                fid='wesan-nis-source' if surf=='nis' else f'wesan-{st}-{p}-'+('sg' if n=='singular' else 'pl')+'-negative'
                old=next((f for f in L['wesan']['forms'] if f['form_id']==fid),None)
                c=cell('wesan','wesan',fid,surf,old['analysis'] if old else a,nev,prior=old)
                c['contextual_analysis']=a;ws.append(c)
system('wesan','wesan','NEG-IND',ws,'U15-R-NEG','Complete negative present eom-series and preterite wæs-series indicative. Plain ne+form remains grammatical. No neom/neart or negative bēo paradigm is asserted.',nev)
ns=[]
for old in L['nabban']['forms']:
    if old['analysis'].get('mood')!='indicative':continue
    ns.append(cell('nabban','nabban',old['form_id'],old['form'],old['analysis'],['U15-G-FB74'],prior=old))
system('nabban','nabban','IND',ns,'U15-R-NABBAN','Promote the twelve previously recognition-only contracted negative habban indicative forms for ordinary possession. No new subjunctive/imperative/infinitive follows.','U15-G-FB74'.split())
rule('U15-R-NABBAN','Cook’s habban table and ne+h contraction (§29), with the already checked Unit2 negative cells, give næbbe, næfst, næfð, nabbað; preterite næfde, næfdest, næfde, næfdon. The negative cells are rule-derived, not separately printed in a full negative table. Do not conflate first-singular bb with other singular f. Retain the earlier form identities and recognition histories.',['U15-G-FB23','U15-G-FB74'])
sense('nabban','nabban','nabban-1','have not',['U15-G-FB74'],scope='Ordinary possession, with the same selected object construction as habban.')
finite('willan','willan','NEG-IND',['nelle','nelt','nele','nellað'],['nolde','noldest','nolde','noldon'],['U15-G-FB79'],'U15-R-NEG','Contracted negative indicative of willan: unwillingness/refusal plus the taught plain infinitive. Past unwillingness need not mean a past counterfactual. The old supplied subjunctive nolde remains a different mood record.',polarity='negative')
sense('willan','willan','willan-refuse','be unwilling; refuse (with ne)',['U15-G-FB79','U15-G-FB159'],status='previously_taught',scope='Reuse the actual Unit9 productive sense. Unit15 newly teaches contracted indicative morphology; negated willan is not an automatic future negative.')
lemma('nan','nān','indefinite')
cs=[]
endings={('m','sg'):['','es','um','ne'],('n','sg'):['','es','um',''],('f','sg'):['','re','re','e'],('m','pl'):['e','ra','um','e'],('n','pl'):['','ra','um',''],('f','pl'):['a','ra','um','a']}
for (gen,num),ends in endings.items():
    for ca,en in zip(['nom','gen','dat','acc'],ends):
        fid=f'nan-{ca}-{gen}-{num}-strong'
        old=None
        if (ca,gen,num)==('nom','m','sg'):fid='nan-u14-nom-m-sg-source';old=L['nan']['forms'][0]
        a={'case':{'nom':'nominative','gen':'genitive','dat':'dative','acc':'accusative'}[ca],'gender':{'m':'masculine','f':'feminine','n':'neuter'}[gen],'number':{'sg':'singular','pl':'plural'}[num],'declension':'strong'}
        surf='nān'+en
        if (ca,gen,num)==('acc','m','sg'):surf='nānne'
        cs.append(cell('nan','nān',fid,surf,old['analysis'] if old else a,['U15-G-FB52','U15-G-FB39','U15-G-FB40'],prior=old))
system('nan','nān','STRONG-NGDA',cs,'U15-R-NAN','Complete strong NGDA singular/plural. Attributive no and singular substantive no one; plural none where a plural group is contextually recoverable. The case is governed by its actual clause role. No weak paradigm is invented.',['U15-G-FB52','U15-G-FB39','U15-G-FB40'])
sense('nan','nān','nan-u14-source','no; no one',['U15-G-FB52','U15-G-FB100'],scope='Promotes the exact U14 supplied lexical sense; full negative concord explicitly taught now.')
rule('U15-R-NAN','Nān follows strong long-stem adjective NGDA endings, with nominative/accusative neuter plural nān and feminine plural nāna, masculine accusative singular nānne. Long ā remains. No invented weak system or general negative spelling rule.',['U15-G-FB52','U15-G-FB39','U15-G-FB40'])
lemma('gehwa','gehwā / gehwæt','pronoun');cs=[]
for old in L['gehwa']['forms']:cs.append(cell('gehwa','gehwā / gehwæt',old['form_id'],old['form'],old['analysis'],['U15-G-FB52','U15-G-FB53','U15-G-W240'],prior=old))
system('gehwa','gehwā / gehwæt','SINGULAR-NGDA',cs,'U15-R-GEHWA','Eight complete singular common-person/neuter NGDA positions. Promote the exact earlier recognition cells for ordinary each one/everything; no plural is created.',['U15-G-FB52','U15-G-FB53','U15-G-W240'])
sense('gehwa','gehwā / gehwæt','gehwa-each-reference','each one; everyone / everything',['U15-G-FB53','U15-G-W240'],scope='Earlier recognition sense promoted, using singular agreement. A plural genitive may specify the group.')
rule('U15-R-GEHWA','Gehwā compounds the singular interrogative hwā/hwæt. Select prior gehwǣm (not silently substitute hwām). Accusative persons gehwone versus things gehwæt. No distinct feminine morphology or plural.',['U15-G-FB52','U15-G-FB53','U15-G-W239','U15-G-W240'])

feature('u15-negative-concord','General negative concord','Nān/nāwiht and preverbal ne or a negative contraction combine to express one negation; earlier nǣfre+ne is the bounded prerequisite. Nān can be an agreeing determiner or stand alone. A negative expression is not cancelled by a second negative.', ['U15-G-FB52','U15-G-FB100'],prior=['u12-negative-concord-bounded'])
feature('u15-negative-copula','Negative copula indicative','Use the complete twelve-position selected negative copula table in ordinary nominal/adjectival clauses; uncontracted ne plus the positive form remains a valid alternative.',['U15-G-FB78','U15-G-FB79','U15-G-FB100'])
feature('u15-nabban-indicative','Negative possession','Use all twelve prior recognition-only nabban indicative forms for ordinary negative possession; keep their supplied and recognition history.',['U15-G-FB74'])
feature('u15-negative-willan','Negative volition','Use the complete contracted negative willan indicative with a taught plain infinitive for refusal/unwillingness; distinguish tense from the English wording would not.',['U15-G-FB79','U15-G-FB159'])
feature('u15-constituent-na','Constituent negation','Nā can negate a contrasted constituent, as ic self and nā ōðer; the finite assertion need not itself be negative. Distinguish from preverbal ne and from negative concord.',['U15-G-EX17','U15-G-EX18'])
feature('u15-an-indefinite','Indefinite ān','Ān with a singular noun can mean a/certain, separately from cardinal one. Reuse the already productive singular strong forms; plural cardinal-one reference cells receive no new automatic production.',['U15-G-FB52','U15-G-FB275'])
feature('u15-hwa-indefinite','Indefinite personal reference','Hwā/hwæt can have indefinite anyone/anything reference in an appropriate condition or concession. Familiar interrogative morphology is reused; English any is not a license for unrestricted distribution.',['U15-G-FB53','U15-G-W240'])
feature('u15-gehwa-distributive','Each one','Gehwā/gehwæt is singular and distributes across a recoverable group; the genitive can name that group. Retain the actual syntactic case of the distributive.',['U15-G-FB53','U15-G-W240'])
feature('u15-man-impersonal','Impersonal man','Man is a defective nominative-singular subject meaning one/people in general, with a third-singular finite verb. Do not invent oblique or plural forms in this function or identify it with every use of count noun mann.',['U15-G-FB53','U15-G-W240'])
feature('u15-free-choice','Free-choice relatives','Swā hwā swā and swā hwæt swā mean whoever/whatever. The case follows the pronoun’s function in the supported clause, and a resumptive pronoun can carry a different main-clause role. Swā hwæðer swā selects between two. Prospective or contingent examples may have subjunctive; the form alone does not mechanically impose one mood. The attracted dative construction of Cook31.12 remains explicitly supplied.',['U15-G-FB53','U15-G-W240','U15-G-FB159'])
feature('u15-proportional-swa','Proportional comparison','Paired swā clauses containing comparatives can correlate two changes: the greater…, the greater…. Distinguish this from equal-degree swā…swā with a positive adjective. The two clause subjects and comparative agreement remain independent.',['U15-G-FB156','U15-G-FB157'],prior=['u12-equative-swa-swa'])
feature('u15-either-both-coordination','Both…and','Ǣgðer ge…ge strengthens paired coordination: both…and. The invariant coordinator does not assign an entire unused inflected either-pronoun family.',['U15-G-FB162'],prior=['u13-ge-paired'])
feature('u15-quantity-partitives','Quantity and distribution','Distinguish agreeing quantitative adjectives from a genitive specifying the whole group. In ǣlc his pęning, each distributes a singular share across plural people; the finite verb may agree with the explicit plural subject. Personal uncer can specify of us two after ān.',['U15-G-EX16','U15-G-EX18','U15-G-FB275','U15-G-FB94'])
feature('u15-rather-than','Preference comparison','Swīðor…ðonne compares the degree of preference between two objects or actions. In loving darkness rather than light, both compared noun phrases have the accusative role belonging to love; do not impose Unit3’s nominative copular standard.',['U15-G-EX16','U15-G-BT-SWITHE'],prior=['u03-comparison-thonne','u11-verbal-comparison-ma'])
feature('u15-source-argument','Argument through questions and prayer','Recognize the supported reading’s rhetorical questions, grounds for action, repeated requests, and differences between an asserted statement, a prayer, and a prospective purpose. This is scaffolded source analysis, not unrestricted composition.',['U15-G-FB159','U15-G-FB162','U15-G-FB163'],'new_recognition')

D['lemmas']=list(LM.values())
(O/'grammar-records-core.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('core',len(D['paradigms']),'systems',sum(len(x['cells']) for x in D['paradigms']),'cells',len(D['features']),'features')
