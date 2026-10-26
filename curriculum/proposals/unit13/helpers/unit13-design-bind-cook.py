"""Private Cook output identities, resolved from actual forms and explicit roles."""
from pathlib import Path
import json,re,copy
ROOT=Path.cwd();OUT=ROOT/'curriculum/proposals/unit13'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def save(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def state(r):return 'previously_taught' if r.get('production_taught_in') else 'previously_recognition' if r.get('recognition_taught_in') else 'previously_supplied'
L={};F={};S={};baseline=set();prior_records={}
for path in ['lexicon/entries.json','sources/audits/unit13-source/lexical-inventory.json','sources/audits/unit13-source/source-support-records.json','sources/audits/unit13-grammar/grammar-records.json','sources/audits/unit13-grammar/source-support.json']:
    if not (ROOT/path).exists():continue
    for l in load(path).get('lemmas',[]):
        lid=l['lemma_id'];old=L.get(lid,{})
        merged={**old,**copy.deepcopy(l)}
        for key,idkey,d in [('forms','form_id',F),('senses','sense_id',S)]:
            records={x[idkey]:x for x in old.get(key,[])}
            for r in l.get(key,[]):
                r=copy.deepcopy(r)
                rid=r[idkey]
                if path=='lexicon/entries.json':prior_records[rid]=copy.deepcopy(r)
                elif rid in prior_records:
                    for field in ['form','analysis'] if key=='forms' else ['gloss']:
                        if field in r and field in prior_records[rid] and r[field]!=prior_records[rid][field]:
                            r['unit13_contextual_'+field]=r[field];r[field]=copy.deepcopy(prior_records[rid][field])
                if path=='lexicon/entries.json' and r.get('production_taught_in'):baseline.add(rid)
                st='previously_taught' if rid in baseline else state(r) if path=='lexicon/entries.json' else r.get('knowledge_status','supplied')
                if rid in d and d[rid]['resolved_status']=='new_production' and st=='supplied':st='new_production'
                records[rid]=copy.deepcopy(r);d[rid]={**copy.deepcopy(r),'lemma_id':lid,'resolved_status':st}
            merged[key]=list(records.values())
        L[lid]=merged

# Every position below names its lexical identity and intended syntactic analysis.
# Model strings are independently authored source-editor proposals, not English prompts.
SPEC={
'22-01':'idelnes:ns wesan:pi3s synn:gs modor:ns',
'22-02':'aethelthryth:ns wesan:ti3s eastengle:gp cyning:gs dohtor:ns',
'22-03':'se:mgs bisceop:gs faeger:nnsW mynster:ns wesan:ti3s/wesan-passive fordilgian:pastpart',
'22-04':'winnan:imps mid/mid-by-means thin-poss:fdpS hand:dp',
'22-05':'began:imps/began-u13-study thin-poss:fasS leornung:as',
'22-06':'he:mns gan:pi3s to/to-destination cirice:ds',
'22-07':'gewitan:impp fram ic:ds thu:np the-relative wyrcean:pi2p/wyrcean-work unrihtwisnes:as',
'22-08':'hwa:nns wesan:pi3s thin-poss:mnsS nama:ns',
'22-09':'hatan:imps ure-poss:mapS thrie:map freond:ap thider to/to-destination he:mds gan:inf',
'22-10':'se:mns sang:ns astigan:pi3s/astigan-u13-descend of/of-u11-source heofon:dp to/to-destination eorthe:ds',
'22-11':'ic:ns gewunian:pi1s se:mas bisceop:as geneosian:inf',
'22-12':'ic:ns willan:pi1s aerest-adverb thu:as ascian:inf an:ngsS thing:gs',
'22-13':'ic:ns willan:pi1s he:mas mid/mid-accompaniment-source ic:ds laedan:inf/laedan-u13-bring',
'22-14':'se:mns maessepreost:ns astreccan:ti3s he:mas beforan/beforan-u13-positioning se:mas bisceop:as',
'22-15':'on/on-sabbath-temporal se:mas thridda:masW daeg:as wesan:ti3s/wesan-passive se:fns halig:fnsW sawol:ns of se:mds lichama:ds onliesan:pastpart',
'23-01':'se:nns micel-superl:nnsW eagthyrel:ns se:fgs cirice:gs wesan:pi3s twegen:mgp fot:gp brad:nnsS and feower fot:gp heah:nnsS',
'23-02':'styccemaelum nealaecan:ti3s se:mns swete:mnsW sang:ns',
'23-03':'ic:ns halsian:pi1s thu:as thaet-conjunction thu:ns ic:ds secgan:ps2s/secgan-content hwa:nns se:mgs engel:gs nama:ns wesan:ps3s',
'23-04':'se:mnp cempa:np niman:ti3p he:mgs/he-possessor hraegl:as and wyrcean:ti3p/wyrcean-make feower dael:ap aelc:mdsS cempa:ds an:masS dael:as swa/swa-1 don:ti3p se:mnp cempa:np',
'23-05':'se:mgs haelend:gs modor:ns standan:ti3s/standan-ordinary with/with-u13-proximity se:fas rod:as',
'23-06':'manig:mnpS raedan:pi3p thes:nas gewrit:as',
'23-07':'mid/mid-by-means he:mgs/he-possessor lytel:mdsW adesa:ds forceorfan:ti3s he:mns se:nas treo:as',
'23-08':'se:fns aex:ns wesan:pi3s/wesan-passive to/to-u13-at-root-source se:ngp treo:gp wyrttruma:ds asettan:pastpart',
'23-09':'he:mns niman:ti3s aex:as on he:mgs/he-possessor hand:as',
'23-10':'sellan:imps/sellan-u13-sell ic:ds fif adesa:ap',
'23-11':'he:mgs/he-possessor lichamlic:fnsS untrymnes:ns wesan:ti3s swithe hefig:fnsS',
'23-12':'thin-poss:mnsS geferscipe:ns wesan:pi3s swithe wynsum:mnsS',
'23-13':'wesan:pi3s he:nns aenig:nnsS wundor:ns theah god:gs geleafa:ns weaxan:ts3s',
'24-01':'se:mns/se-relative the-relative on/on-1 se:nds cynesetl:ds sittan:pi3s he:mns wunian:pi3s tomiddes/tomiddes-midst he:dp',
'24-02':'engel:np wesan:pi3p gast:np butan/butan-u13-without lichama:ds',
'24-03':'ic:ns geseon:ti1s/geseon-perceive-action steorra:as of heofon:ds oth eorthe:as feallan:inf',
'24-04':'se:mns/se-relative the-relative oferwinnan:pi3s se:mns ilca:mnsW wesan:pi3s/wesan-passive mid/mid-u13-clothing hwit:ndsS hraegl:ds gescrydan:pastpart',
'24-05':'thes:nap thing:ap cwethan:pi3s se:mns/se-relative the-relative halig:mnsS wesan:pi3s',
'24-06':'ondraedan:impp se:mas/se-relative the-relative magan:pi3s fordon:inf ge/ge-paired-source sawol:as ge/ge-paired-source lichama:as on hell:ds',
'24-07':'ic:ns ne wesan:pi1s wierthe:mnsS thaet-conjunction thu:ns under/under-u13-direction min-poss:masS hrof:as ingan:ps2s',
'24-08':'micel:fnsS wesan:pi3s eower-poss:fnsS med:ns on/on-1 heofon:dp',
'24-09':'gif god:ns swa/swa-1 gescrydan:pi3s aecer:gs graes:as the-relative todag wesan:pi3s and tomorgen wesan:pi3s/wesan-passive on ofen:as asendan:pastpart micel:nisS ma he:mns gescrydan:pi3s thu:ap thu:np lytel:mgsS geleafa:gs',
'24-10':'god-adjective-comp:fnsW wesan:pi3s se:fns sawol:ns thonne mete:ns and se:mns lichama:ns thonne he:mgs/he-possessor hraegl:ns',
'24-11':'behealdan:impp heofon:gs fugol:ap eower-poss:mnsS heofonlic:mnsW faeder:ns fedan:pi3s he:ap',
'24-12':'hwa:nas sculan:pi1p ic:np etan:inf oththe hwa:nas drincan:inf',
'25-01':'se:mns/se-relative the-relative ne lufian:pi3s he:mgs/he-possessor brothor:as se:mas/se-relative the-relative he:mns geseon:pi3s hu magan:pi3s he:mns god:as lufian:inf se:mas/se-relative the-relative he:mns ne geseon:pi3s',
'25-02':'min-poss:fgsS forthfor:gs tid:ns wesan:pi3s neah',
'25-03':'he:mns don:ti3s hwaethwega swilc:ngsS tha-hwile-the he:mgs/he-possessor gefera:np to/to-destination burg:ds gan:ti3p',
'25-04':'wesan:imps mid/mid-accompaniment-source se:mdp brothor:dp',
'25-05':'geopenian:imps se:ngs hus:gs eagthyrel:ap',
'25-06':'lufian:impp eower-poss:mapS feond:ap don:impp se:mdp wel the-relative thu:ap hatian:pi3p thaet-conjunction/thaet-purpose thu:np wesan:ps2p eower-poss:mgsS faeder:gs bearn:np se:mns/se-relative the-relative on/on-1 heofon:dp wesan:pi3s',
'25-07':'thu:np wesan:pi2p min-poss:mnpS freond:np gif thu:np se:nap thing:ap don:pi2p the-relative ic:ns thu:dp bebeodan:pi1s',
'25-08':'se:mnp fugol:np singan:ti3p se:mas swete-superl:masW sang:as wynsum:masS to/to-inflected-infinitive hieran:inflected',
'25-09':'se:fgs cirice:gs hrof:ns wesan:pi3s swithe heah:mnsS',
'25-10':'tha-adverb wesan:ti3s semninga mid/mid-accompaniment-source se:mds engel:ds getael:ns heofonlic:ngsS weorod:gs herian:prespart god:as and thus cwethan:prespart/cwethan-u13-saying-source',
'25-11':'god:ds wesan:ps3s wuldor:ns on heanes:dp/heanes-heights-u13-source and on eorthe:ds sibb:ns mann:dp god-adjective:mgsS willa:gs',
'25-12':'he:mns efthweorfan:ti3s se:mis ilca:misW weg:ds the-relative he:mns aer cuman:ti3s',
}
DEFAULT={'se':'se-the','wesan':'wesan-be','he':'he-1','ic':'ic-personal','thu':'thu-personal','to':'to-destination','on':'on-1','hieran':'hieran-1','geseon':'geseon-1','secgan':'secgan-content','mid':'mid-accompaniment-source','willan':'willan-1','sellan':'sellan-give'}
ALIASES={'thrie':'thrie','cynesetl':'setl','hraegl':'reaf','graes':'gaers','aerest-adverb':'aerest','astreccan':'astreccean','oth':'oth-preposition','ge':'ge-conjunction','oththe':'othothe','neah':'neah-adverb','aer':'aer-adverb','todag':'to-daeg','tomorgen':'to-morgen'}
NORMAL={'nominative':'nom','genitive':'gen','dative':'dat','accusative':'acc','instrumental':'ins','singular':'sg','plural':'pl','masculine':'m','feminine':'f','neuter':'n'}
def norm(v):return NORMAL.get(v,v)
def wanted(tag):
    if not tag:return {}
    v=re.fullmatch(r'([pt])([is])([123])([sp])',tag)
    if v:return dict(tense='present' if v[1]=='p' else 'preterite',mood='indicative' if v[2]=='i' else 'subjunctive',person=int(v[3]),number='sg' if v[4]=='s' else 'pl')
    if tag in ['imps','impp']:return dict(mood='imperative',person=2,number='sg' if tag=='imps' else 'pl')
    if tag in ['inf','inflected','pastpart','prespart']:return {'special':tag}
    n=re.fullmatch(r'([mfn]?)([ngdai])([sp])([SW]?)',tag)
    if not n:raise ValueError(tag)
    d=dict(case={'n':'nom','g':'gen','d':'dat','a':'acc','i':'ins'}[n[2]],number='sg' if n[3]=='s' else 'pl')
    if n[1]:d['gender']=n[1]
    if n[4]:d['declension']='strong' if n[4]=='S' else 'weak'
    return d
def match(f,w):
    original=f.get('analysis',{})
    a={k:norm(v) for k,v in original.items()} if isinstance(original,dict) else {}
    contextual=f.get('unit13_contextual_analysis')
    if isinstance(contextual,dict):a.update({k:norm(v) for k,v in contextual.items()})
    if 'special' in w:
        tag=w['special'];fid=f['form_id']
        if tag=='inf':return ('infinitive' in fid or a.get('mood')=='infinitive') and 'inflected' not in fid
        if tag=='inflected':return 'inflected' in fid or a.get('verb_form')=='inflected_infinitive'
        if tag=='pastpart':return 'past-participle' in fid or 'pastpart' in fid or ('participle' in fid and 'pres' not in fid) or (a.get('verb_form')=='participle' and a.get('tense')=='past')
        if tag=='prespart':return 'prespart' in fid or 'present-participle' in fid or (a.get('verb_form')=='participle' and a.get('tense')=='present')
    return all(a.get(k)==v or (k=='gender' and a.get(k)=='all' and v in ['m','f','n']) for k,v in w.items())

def resolve(literal,spec,owner,index):
    clean=literal.strip('.,:;!?“”"()[]');left,*stail=spec.split('/');lid,*tail=left.split(':');lid=ALIASES.get(lid,lid);tag=tail[0] if tail else '';w=wanted(tag)
    candidates=[f for f in F.values() if f['lemma_id']==lid and f['form'].casefold()==clean.casefold()]
    exact=[f for f in candidates if match(f,w)]
    if owner=='EX-VII-25-12' and lid=='ilca':
        exact=[f for f in candidates if f['form_id']=='ilca-dat-m-sg-weak']
    if lid=='to':
        wanted_id='to-before-inflected-infinitive' if stail and stail[0]=='to-inflected-infinitive' else 'to-preposition-dative-invariant'
        exact=[f for f in exact if f['form_id']==wanted_id]
    # A unique supplied exact token may carry a source_analysis rather than structured fields.
    if not exact and len(candidates)==1 and candidates[0]['resolved_status'] in ['supplied','previously_supplied']:
        exact=candidates
    if not exact:
        issues.append(dict(owner=owner,token_index=index,literal=literal,specification=spec,error='no_matching_identity',candidates=[dict(form_id=f['form_id'],analysis=f.get('analysis'),status=f['resolved_status']) for f in candidates]));return None
    exact.sort(key=lambda f:(f['resolved_status'] not in ['previously_taught','new_production'],f['form_id'] not in baseline))
    if len(exact)>1 and exact[0]['resolved_status']==exact[1]['resolved_status']:
        issues.append(dict(owner=owner,token_index=index,literal=literal,specification=spec,error='ambiguous_identity',candidates=[f['form_id'] for f in exact]));return None
    f=exact[0];sid=stail[0] if stail else DEFAULT.get(lid)
    if sid is None:sid=L[lid]['senses'][0]['sense_id']
    s=S.get(sid)
    if not s or s['lemma_id']!=lid:
        issues.append(dict(owner=owner,token_index=index,literal=literal,error='sense_identity',lemma_id=lid,sense_id=sid,available=[s['sense_id'] for s in L[lid]['senses']]));return None
    return dict(token_index=index,literal=literal,surface=clean,lemma_id=lid,form_id=f['form_id'],sense_id=sid,form=f['form'],analysis=f.get('analysis',{}),contextual_analysis=w,form_status=f['resolved_status'],sense_status=s['resolved_status'])

issues=[];sequences=[]
models=load('sources/audits/unit13-source/author-only-cook-models.json')['items']
for m in models:
    owner=m['task_id'];code=owner.removeprefix('EX-VII-');text=m['model'];words=text.split();spec=SPEC[code].split()
    if len(words)!=len(spec):issues.append(dict(owner=owner,error='token_count',words=len(words),bindings=len(spec)));continue
    tokens=[]
    for i,(word,hint) in enumerate(zip(words,spec),1):
        token=resolve(word,hint,owner,i)
        if token:tokens.append(token)
    sequences.append(dict(sequence_id=owner+'-MODEL',owner_id=owner,kind='private_cook_model',text=text,tokens=tokens,required_form_ids=sorted({t['form_id'] for t in tokens}),required_sense_ids=sorted({t['sense_id'] for t in tokens})))
save('author-only-cook-sequence-bindings.json',dict(schema_version=1,chapter='ch13',private=True,pre_key_excluded=True,status='closed' if not issues else 'pending_record_reconciliation',source_models='sources/audits/unit13-source/author-only-cook-models.json',sequences=sequences,issues=issues))
print(json.dumps(dict(sequences=len(sequences),tokens=sum(len(s['tokens']) for s in sequences),issues=len(issues),sample=issues[:12]),ensure_ascii=False))
