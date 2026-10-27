"""Exact visible Unit16 scaffolds; supplied does not mean recall has been taught."""
import json,copy,re
from pathlib import Path
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
L={l['lemma_id']:l for l in json.loads((R/'lexicon/entries.json').read_text(encoding='utf8'))['lemmas']}
G={l['lemma_id']:l for l in json.loads((O/'grammar-records.json').read_text(encoding='utf8'))['lemmas']}
def save(p,d):(O/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
lemmas={};features=[];cook=[];reading=[]
def word(i,head,surface,a,gloss,refs,id=None,sid=None):
    p=L.get(i,{})
    lemmas.setdefault(i,{'lemma_id':i,'display_headword':p.get('display_headword',head),'part_of_speech':'verb','prior_lemma_present':i in L,'forms':[],'senses':[]})
    # New local form identities must not replace an actually taught matching identity.
    candidates=[]
    for f in p.get('forms',[])+G.get(i,{}).get('forms',[]):
        if f['form'].casefold()!=surface.casefold():continue
        qa=f.get('contextual_analysis',f['analysis'])
        ok=True
        for key in ['person','tense','mood','number']:
            if key in a:
                val=qa.get(key)
                if key=='number':val={'sg':'singular','pl':'plural'}.get(val,val)
                if val!=a[key]:ok=False
        if ok:candidates.append(f)
    q=next((f for f in candidates if f.get('production_taught_in') or f.get('knowledge_status')=='new_production'),None)
    if q is None and len(candidates)==1:q=candidates[0]
    if q:
        id=q['form_id'];an=copy.deepcopy(q['analysis']);status='previously_taught' if q.get('production_taught_in') else q.get('knowledge_status','supplied')
    else:
        id=id or f'{i}-u16-source-'+re.sub('[^a-z0-9]+','-',str(len(lemmas[i]['forms'])+1));an=a;status='supplied'
    f={'form_id':id,'form':q['form'] if q else surface,'analysis':an,'contextual_analysis':a,'knowledge_status':status,'evidence_refs':refs,'teaching_ids':[],'scope_note':'Exact contextual support only unless a separate actual prior or new productive identity is explicitly named.'}
    if q and i in L and any(x['form_id']==id for x in p.get('forms',[])):
        f['prior_scope']={k:q.get(k) for k in ['production_taught_in','recognition_taught_in','supplied_in','analysis']}
    if not any(x['form_id']==id for x in lemmas[i]['forms']):lemmas[i]['forms'].append(f)
    sid=sid or i+'-u16-source'
    if not any(x['sense_id']==sid for x in lemmas[i]['senses']):lemmas[i]['senses'].append({'sense_id':sid,'gloss':gloss,'knowledge_status':'supplied','evidence_refs':refs,'scope_note':'Only the explicitly supplied contextual use; no independent recall.'})
    return {'lemma_id':i,'form_id':id,'sense_id':sid,'form':surface,'analysis':a,'knowledge_status':status,'evidence_refs':refs}
def support(item,slug,text,meaning,explanation,refs,bindings=None,status='supplied'):
    fid='u16-support-'+slug
    features.append({'feature_id':fid,'label':slug.replace('-',' '),'description':explanation,'scope_note':'Supply the actual phrase and explanation at the point of use; no independent recall of its exceptional forms/construction.','knowledge_status':status,'evidence_refs':refs,'teaching_ids':[]})
    cook.append({'support_id':'U16-HELP-'+slug.upper(),'source_item_id':'EX-XII-XIII-'+item,'feature_id':fid,'knowledge_status':status,'actual_supplied_text':text,'meaning':meaning,'explanation':explanation,'form_bindings':bindings or [],'evidence_refs':refs})
FB=lambda *ns:['U16-G-FB'+str(n) for n in ns]
support('32-08','better-clause','bętere ðē is ðæt ðū ... gā, ðonne ðū ... hæbbe and ... sīe worpen','It is better for you to go ... than to have ... and be thrown ...','The experiencer is dative ðē; bętere is the actual prior neuter comparative predicate. Keep the explicitly requested ðæt in the first complement and omit it after ðonne. Generic hit earlier resumes whichever of two differently gendered body parts is at issue.','U16-EX-P18 U16-G-FB95 U16-G-FB104'.split())
z=word('gelimpan','gelimpan','gelimpð',{'tense':'present','mood':'indicative','person':3,'number':'singular'},'happen; come about',FB(61,62)+['U16-EX-P18'],id='gelimpan-pres-3-sg-u16-supplied')
support('32-10','gelimpan-clause','gif hit gelimpð ðæt hē hit finde','if it happens that he finds it','The first hit is impersonal; the second hit is the sheep. Gelimpð is supplied; finde is the newly taught present subjunctive. No full gelimpan person paradigm is assigned.',z['evidence_refs'],[z])
z=word('gangan','gangan','gangende',{'nonfinite':'participle','tense':'present','case':'nominative','number':'plural','declension':'strong'},'go; enter in the supplied circumstantial phrase',FB(55,66,100,290)+['U16-EX-P19'],id='gangan-pres-part-nom-pl-u16-supplied')
support('33-01','gangan-participle','intō ðǣm hūse gangende','going into the house','Gangende accompanies the plural actors hīe. The participial phrase is supplied as a whole; it does not assign a new complete gangan finite system.',z['evidence_refs'],[z])
z=word('genyhtsumian','genyhtsumian','genyhtsumien',{'tense':'present','mood':'subjunctive','person':3,'number':'plural'},'suffice; be sufficient for',FB(73,74,167)+['U16-G-EX63'],id='genyhtsumian-pres-subj-3-pl-u16-supplied')
support('34-03','suffice-books','Genyhtsumien mīna bēc unc bǣm.','Let my books suffice for us both.','Adaptation of the exact167.13 genyhtsumien unc bǣm mīne lȳtlan ǣhta. Books is the verified exercise noun, replacing possessions; plural subject and plural optative stay. Unc is dual dative, bǣm dative plural because both has no separate dual.',z['evidence_refs'],[z])
z=word('libban','libban','libbendan',{'nonfinite':'participle','tense':'present','declension':'weak','case':'accusative','gender':'masculine','number':'singular'},'living, in the supplied weak participial adjective',FB(75,100)+['U16-EX-P20'],id='libban-pres-part-weak-acc-m-sg-u16-supplied')
support('34-06','living-god','ðurh ðone libbendan God','by the living God','Libbendan is the exact supplied weak masculine accusative singular participle agreeing with God after ðone. Existing libban finite tables did not teach this attributive cell.',z['evidence_refs'],[z])
support('34-07','right-hand','on ðā swīðran hand Godes mægenðrymmes','at the right hand of God’s majesty','The source explicitly controls on with accusative. Supply the fixed position expression rather than invent a motion meaning for sitting. The selected perception infinitives sittan/cuman denote the perceived ongoing actions; English -ing is not mechanically converted to an OE participle.',['U16-EX-P20']+FB(96,97))
support('34-09','coming-infinitive','is tō cumanne','is to come','Supply this exact wesan + tō-inflected-infinitive construction for impending coming. Cook§200 supplies the general inflected-infinitive framework, not direct evidence of this particular construction. Personally inspected Matthew16.27 (Kemble/Hardwick132, left column) has ys to cumenne; its apparatus gives A cumanne. The new model selects the already taught is/tō/cumanne spellings, separately from the exact source spelling. Actual prior u06-purpose-infinitive only licenses purpose after a coming verb and does not teach this construction. No general future or necessity system is assigned.',['U16-EX-P20','U16-G-MATTHEW132']+FB(106))
z=word('agyldan','āgyldan','āgylt',{'tense':'present','mood':'indicative','person':3,'number':'singular'},'reward; repay', ['U16-G-BT-AGYLDAN','U16-C06-REWARD'],id='agyldan-pres-3-sg-u16-supplied')
support('34-09','reward-clause','ðonne āgylt hē ǣlcum be his āgnum weorce','then he rewards everyone according to his own work','Cook prints āgyltan,113. Preserve that original hint in the source; the declared correction is āgyldan, strongIII (§104). BT30b directly gives hē āgylt and dative reward recipient. Supply the entire clause, without claiming a newly taught whole indicative system.',z['evidence_refs'],[z])
support('35-08','gate-way-agreement','hū nearu is ðæt geat and se weg ðe tō līfe lǣtt','how narrow is the gate and the way that leads to life','Retain the source’s singular formulation, treating gate and way as the combined figurative route. Supply this exact coordination rather than assigning a blanket singular-agreement rule for coordinated subjects. The nearu adjective table is separately audited by the source editor.',['U16-EX-P21']+FB(102))
support('36-03','cessation-kissing','ne geswāc ðæt hēo mīne fēt ne cyste','did not stop kissing my feet','BT879b quotes WS Luke7.45 with both negatives. The second ne belongs to this attested negative cessation construction; it does not mean that she withheld kisses. Supply the whole finite clause, not just geswīcan or a general complement rule.',['U16-G-BT-SIDTHAN','U16-G-BT-GESWICAN','U16-EX-P22'])
support('36-06','less-relative','Lǣs lufað ðǣm ðe lǣs forgiefen is.','The one to whom less is forgiven loves less.','The matrix subject is understood from the attracted dative relative. The relative dative belongs to forgiveness; it must not be generalized into a dative subject of ordinary lufian. The prompt attaches neuter accusative singular specifically to its first Less: this is the adverbial degree accusative. The second lǣs is nominative neuter singular, the smaller amount that is forgiven, and is the passive subject. The entire compressed sentence is supplied.',['U16-EX-P22','U16-G-FB51','U16-G-FB100'])
z=word('aliefan','ālīefan','ālīefð',{'tense':'present','mood':'indicative','person':3,'number':'singular'},'permit; allow, in impersonal permission',FB(275)+['U16-G-BT-ALIEFAN'],id='aliefan-pres-3-sg-u16-supplied')
support('36-07','permission-wife','Hit ne ālīefð ðē hīe tō wīfe habban.','It is not permitted for you to have her as wife.','Impersonal hit with finite ālīefð, dative permitted person ðē, accusative hīe as object of habban, and tō wīfe as the wife-role phrase. Omit the English is; do not add wesan or turn hīe into a dative object.',z['evidence_refs']+['U16-EX-P22'],[z])
support('36-08','promise-freechoice','Ðā gehēt hē mid āðe hiere ðæt tō sęllanne, swā hwæs swā hēo hine bǣde.','Then he promised with an oath to give her whatever she asked him for.','The promise is expressed by prior gehēt plus the intended-action infinitive. Hiere is the recipient of giving, ðæt the accusative thing given. Internally the free-choice request retains biddan’s genitive thing hwæs and accusative person hine; bǣde is preterite subjunctive in the open request. The resumptive ðæt avoids forcing one relative case to serve incompatible clauses.',['U16-EX-P22']+FB(93,103,104,106,292))
z=word('myngian','myngian','myngod',{'nonfinite':'participle','tense':'past','inflection':'uninflected_predicate'},'admonished; prompted',FB(73,74,100)+['U16-G-EX38','U16-EX-P22'],id='myngian-past-part-u16-supplied')
support('36-09','admonished-mother','fram hiere mēder myngod','admonished by her mother','The past participle is supplied uninflected in its predicative attachment to hēo; fram plus dative marks the agent. This does not introduce a complete myngian system.',z['evidence_refs'],[z])
save('source-support.json',{'schema_version':1,'chapter':'ch16','status':'proposal','cook_support':cook,'reading_support':[],'lemmas':list(lemmas.values()),'features':features,'note':'Nominal and indeclinable support supplied by the source packet is complementary, not duplicated here.'})

# Exact reading-only verbal help. Already productive matches retain actual IDs.
lemmas={};features=[]
def rd(line,i,head,surface,analysis,gloss,explanation,id=None,sid=None):
    refs=['U16-G-FB'+line[2:5]]
    z=word(i,head,surface,analysis,gloss,refs,id,sid)
    reading.append({'source_line_id':line,'surface':surface,**z,'actual_supplied_text':surface+' — '+gloss,'explanation':explanation,'knowledge_status':'supplied' if z['knowledge_status'] not in ['previously_taught','new_production'] else z['knowledge_status']})
past=lambda:{'tense':'preterite','mood':'indicative','person':3,'number':'singular'}
pp=lambda:{'nonfinite':'participle','tense':'past','inflection':'base'}
rd('FB168-02','getaecan','getǣcan','getǣht',pp(),'shown; directed','Past participle in passive getǣht wæs; him is the person to whom the route was indicated.')
rd('FB168-03','ingan','ingān','inēode',past(),'went in','Prefixed movement verb; do not split into an unnoticed new finite gān spelling.')
rd('FB168-03','magan','magan','meahte',{'tense':'preterite','mood':'subjunctive','person':3,'number':'singular'},'might; could','Inside the dependent question hwone ... biddan meahte; indicative/subjunctive surface coincides. The selected interpretation is possibility in the thought.')
rd('FB168-05','gesmierwan','gesmierwan','gesmierwed',pp(),'anointed','Exact source prefixed participle and retained w; distinct from selected unprefixed smierwan paradigm. Mid ęle marks the anointing material.')
rd('FB168-06','begyrdan','begyrdan','begyrd',pp(),'girded; clothed around','Passive/predicative participle with mid scīetan, a cloth.')
rd('FB168-07','belimpan','belimpan','belimpende',{'nonfinite':'participle','tense':'present','inflection':'source_context'},'belonging; relating','Tō + dative bæðstęde identifies what the games/equipment relate to; preserve source note6.')
rd('FB168-07','cleopian','cleopian','cleopode',past(),'cried aloud','The new productive cry sense; micelre stefne is a dative of manner/instrument.',sid='cleopian-u16-cry')
rd('FB168-08','gehieran','gehīeran','Gehīere',{'mood':'imperative','person':2,'number':'plural'},'hear; listen','Exact plural command with shortened -e before following gē, not singular by surface alone. The same form recurs later in the line.')
rd('FB168-11','unscrydan','unscrȳdan','unscrȳdde',past(),'undressed; took off','Hine is the person undressed; ðǣm healfan sciccelse is the removed clothing, supplied case frame.')
rd('FB168-13','behealdan','behēaldan','behēold',past(),'observed','Accusative persons observed; no modern behold quotation formula implied.')
rd('FB168-17','ingan','ingān','inēode',past(),'went in','On ðæt bæð gives the entry destination.')
rd('FB168-17','aginnan','āginnan','āgan',past(),'began','StrongIII preterite of āginnan, not āgan own/possess and not āgān depart.')
rd('FB168-17','plegian','plegian','plegian',{'nonfinite':'infinitive','inflection':'plain'},'play','Infinitive after began; wið + dative companions and mid + dative ball are supported locally.',id='plegian-infinitive-u16-source',sid='plegian-u16-play')
rd('FB168-18','gemengan','gemęngan','gemęngde',past(),'joined; mingled','Reflexive hine; on ðæs cyninges plegan continues on169.1. Plegan is an oblique noun governed by on; ðæs cyninges is its genitive possessor. It is not a finite verb.')
rd('FB169-01','iernan','iernan','iernende',{'nonfinite':'participle','tense':'present','case':'nominative','gender':'masculine','number':'singular'},'running','Joined across printed line break iern-/ende; the supplied participle accompanies Apollonius. Do not count the two printed fragments as two words.',id='iernan-present-participle-u16-source',sid='iernan-u16')
rd('FB169-02','gelaeccan','gelǣccan','gelæhte',past(),'caught','Exact source preterite has short æ as printed; preserve lexical spelling and do not silently import a guessed long form.')
rd('FB169-03','geslean','geslēan','geslægene',{'nonfinite':'participle','tense':'past','case':'accusative','gender':'masculine','number':'singular','declension':'source'},'struck','Exact accusative participle agreeing with ðone ðoðor, an evidenced exceptional -e form noted by Cook; do not regularize to a new target.')
rd('FB169-03','gesendan','gesęndan','gesęnde',past(),'sent back','Tō + dative recipient; ongēan is the return direction.')
rd('FB169-03','plegian','plegian','plegiendan',{'nonfinite':'participle','tense':'present','declension':'weak','case':'dative','gender':'masculine','number':'singular'},'playing','Weak dative modifier of cyninge after ðǣm; the finite paradigm does not itself teach this participial cell.',id='plegian-pres-part-weak-dat-m-sg-u16-source',sid='plegian-u16-play')
rd('FB169-04','slean','slēan','slōh',past(),'struck','Exact source singular h spelling; Wright262–263 explicitly gives slōg/slōh. Preserve the earlier selected slōg system and supply this contextual variant.',id='slean-pret-3-sg-h-u16-source')
rd('FB169-05','oncnawan','oncnāwan','oncnēow',past(),'recognized; perceived','Accusative snelnesse, followed by a result/content sequence whose pronoun referents remain genuinely underdetermined in Cook note6.')
rd('FB169-09','herian','hęrian','hęrede',past(),'praised','Accusative hine is the praised person; the exact source spelling remains.')
rd('FB169-10','iernan','iernan','arn',past(),'ran','New productive selected preterite.',sid='iernan-u16')
rd('FB169-10','genealaecan','genēalǣcan','genēalǣcte',past(),'approached','The prefixed verb with tō + dative goal is supplied; do not rename it as the unprefixed nēalǣcan form.')
rd('FB169-11','swingan','swingan','swang',past(),'swung; brandished','Direct object top is the actual OE object. Do not substitute the Latin shoulder/rubbing action.')
rd('FB169-12','thyncan','ðyncan','geðūht',pp(),'seemed','Supply ðǣm cyninge wæs geðūht swilce ... wǣre, it seemed to the king as though ...; dative experiencer and irrealis comparison are explicit.')
rd('FB169-13','gewendan','gewęndan','gewęnd',pp(),'turned; changed back','In swilce hē of ielde tō geoguðe gewęnd wǣre: as though he had been turned from age to youth. Do not mechanically label every wesan+participle a motion perfect.')
rd('FB169-14','thenian','ðēnian','ðēnode',past(),'served; attended','Dative him is the served person; exact source -ode spelling, not a fabricated finite ending from the infinitive.')
rd('FB169-15','utgan','ūtgān','ūtēode',past(),'went out','Prefixed motion verb with of + dative place left.')
rd('FB169-16','gewendan','gewęndan','gewęnde',past(),'turned; went away','Reflexive dative him; ðæs weges is the route genitive, matched by the composition35.3. Pronoun references need discourse reasoning.')
rd('FB170-02','agan-depart','āgān','āgān',pp(),'gone away','Past participle in āgān wæs, had departed. Distinguish unmacroned āgan began at168.17.')
rd('FB170-02','swerian','swęrian','swęrie',{'tense':'present','mood':'indicative','person':1,'number':'singular'},'swear','First-person quoted oath; ðurh + accusative oath standard; the narrated speaker now owns ic.')
rd('FB170-03','bathian','baðian','baðode',{'tense':'preterite','mood':'indicative','person':1,'number':'singular'},'bathed','Reflexive mē and adverbial comparison with dyde; this bath verb is supplied, substitute dōn is newly productive.')
rd('FB170-03','nytan','nytan','nāt',{'tense':'present','mood':'indicative','person':1,'number':'singular','polarity':'negative'},'do not know','Exact contracted negative witan lexeme/form is supplied; no full nytan system was taught earlier or is introduced here.')
rd('FB170-04','beseon','besēon','beseah',past(),'looked; turned his gaze','Reflexive hine and tō + dative person toward whom he turned; supply as a local phrase.')
rd('FB170-05','gewitan-know','gewitan','gewite',{'mood':'imperative','person':2,'number':'singular'},'find out; learn','The preterite-present knowing verb (§126), not strongI gewītan depart; the dependent question has hwæt ... sīe.')
rd('FB170-06','gehiersumian','gehīersumian','gehīersumode',past(),'served; obeyed','Dative mē is the person served; hyphenation gehīer-/sumode is print line division only.')
rd('FB170-09','bewaefan','bewǣfan','bewǣfed',pp(),'wrapped; clothed','Mid + dative garment in the passive/predicative description.')
rd('FB170-09','wendan','węndan','węnde',past(),'turned; returned','Ongēan + tō destination; distinct from wēnan expected despite the similar modern gloss.')
rd('FB170-11','ascian','āscian','āscodest',{'tense':'preterite','mood':'indicative','person':2,'number':'singular'},'asked about','Æfter links to the relative antecedent; exact source spelling preserves -odest.')
rd('FB170-13','forswigian','forswīgian','forswīge',{'tense':'present','mood':'subjunctive','person':3,'number':'singular'},'keep silent about; conceal','Ðēah concessive clause; hit is the thing withheld. Exact source ending is supplied rather than silently generalized to a weak-II table.')
rd('FB170-14','gesweotolian','gesweotolian','gesweotolað',{'tense':'present','mood':'indicative','person':3,'number':'singular'},'reveals; makes clear','Gegierela is the singular subject, hine the person whose condition is revealed.')
rd('FB170-15','secgan','sęcgan','sęge',{'mood':'imperative','person':2,'number':'singular'},'say; tell','Exact source shortened command spelling; the following mixed direct/indirect quotation is explicitly supported by Cook note15, not presented as a regular report transformation.')
save('reading-verbal-support.json',{'schema_version':1,'chapter':'ch16','source_span_id':'FB-XII-APOLLONIUS-GYMNASIUM','status':'proposal_for_source_ledger_reconciliation','items':reading,'lemmas':list(lemmas.values()),'features':features,'source_only_rule':'Reading-only forms and frames stay supplied unless an explicit prior/new productive identity above proves the narrower form and use. No reading-only finite table is implied.'})
print(len(cook),'Cook scaffolds;',len(reading),'reading verbal entries')
