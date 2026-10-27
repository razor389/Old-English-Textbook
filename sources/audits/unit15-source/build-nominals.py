"""Bounded nominal proposals: literal cells, image-checked citations and rules."""
import json,pathlib,copy,collections
P=pathlib.Path(__file__).parent;R=P.resolve().parents[2]
OLD={l['lemma_id']:l for l in json.loads((R/'lexicon/entries.json').read_text(encoding='utf8'))['lemmas']}
def dump(n,x):(P/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
RULES=[
 ('M43','Strong masculine: uninflected nominative/accusative singular, -es/-e; plural -as/-a/-um/-as.',[28]),
 ('M43-VOWEL','Retain the vowel in the final short-stem element sceamul before endings; the long first element fōt- does not turn the final element into a heavy stem. Full uncontracted cells selected.',[28,29]),
 ('N47','Heavy neuter nominative/accusative singular and plural have no ending; other endings -es/-e/-a/-um. Short final stem bebod- takes plural -u.',[32,33]),
 ('N47-SYNCOPE','hēafod has the syncopated hēafd- stem before endings, with selected nominative/accusative plural hēafdu (§47.1,6).',[28,33]),
 ('F51','Heavy feminine: nominative singular uninflected; oblique singular -e; plural -a/-a/-um/-a. -nes doubles s before endings. Abstract -ung/-ing has the same selected endings; -a oblique singular variants remain recognition alternatives.',[35,36]),
 ('WEAK53','Weak masculine: -a nominative singular, -an other singular and nominative/accusative plural, -ena genitive plural, -um dative plural.',[37]),
 ('ROOT46','tōð follows fōt: dative singular and nominative/accusative plural tēð, genitive singular tōðes, plural genitive tōða and dative tōðum. Cook also admits tōðe and tōðas.',[31,32]),
 ('BOC52','bōc: genitive/dative singular and nominative/accusative plural bēc; genitive plural bōca, dative plural bōcum. Genitive singular bōce follows the explicitly admitted regular -e genitive alternative for this class.',[36]),
 ('SWEOSTOR52','sweostor is unchanged throughout the singular and nominative/accusative plural, with genitive plural sweostra and dative plural sweostrum; no invented umlaut.',[37]),
 ('PEOPLES44','Selected people names Engle and Dęne have plural-only lexical scope: -e nominative/accusative, -a genitive, -um dative. Dęniga/Dęnia genitive plural variants are explicit in §44.2; do not manufacture a singular by backformation.',[30,31]),
 ('END43','Agent noun in -end: selected plural nominative/accusative zero, genitive -ra, dative -um. Cook admits nominative/accusative plural -e and -as variants.',[29]),
 ('ABSTRACT-U','Complete singular selection hǣtu/hǣte and invariant hǣlu; -u/-o/-e oblique variation is recognized. Wright184 §§382–383 explicitly lists both under strengu and warns few such nouns have plurals. BT500b lists hǣlu indeclinable. No plural lexical use assigned.',[297]),
 ('STRENGU-CLASS','Wright184 prints the complete strengu class model: singular nominative strengu/-o, accusative/genitive/dative strenge/-u/-o; plural nominative/accusative strenga/-e/-u/-o, genitive strenga and dative strengum. Select one explicit eight-cell reference column without assigning an independently productive count sense. Earlier ðīestru taught only plural forms and does not establish this complete class.',[])]
rules=[dict(rule_id='U15-NOM-'+i,description=d,evidence_refs=['U15-FB-P'+str(p) for p in ps]+(['U15-WRIGHT-P184','U15-BT-P500B'] if i=='ABSTRACT-U' else ['U15-WRIGHT-P184'] if i=='STRENGU-CLASS' else [])) for i,d,ps in RULES]
# id, head, gender, model, diagnostic stem, gloss, eight literal cells (N G D A), source refs, scope, tasks
D=[
 ('hlaford','hlāford','m','strong43','hlāford','lord; master','hlāford hlāfordes hlāforde hlāford hlāfordas hlāforda hlāfordum hlāfordas',['U15-FB-P299','U15-EX-P16'],'all',['28.10']),
 ('sweostor','sweostor','f','kinship52','sweostr','sister','sweostor sweostor sweostor sweostor sweostor sweostra sweostrum sweostor',['U15-FB-P37','U15-EX-P15'],'all',['28.1']),
 ('wingeard','wīngeard','m','strong43','wīngeard','vineyard','wīngeard wīngeardes wīngearde wīngeard wīngeardas wīngearda wīngeardum wīngeardas',['U15-FB-P322'],'all',['28.3','28.5','28.10']),
 ('gerefa','gerēfa','m','weak53','gerēf','steward; reeve','gerēfa gerēfan gerēfan gerēfan gerēfan gerēfena gerēfum gerēfan',['U15-EX-P16'],'all',['28.10']),
 ('hefignes','hęfignes','f','feminine51-nes','hęfigness','burden','hęfignes hęfignesse hęfignesse hęfignesse hęfignessa hęfignessa hęfignessum hęfignessa',['U15-FB-P298','U15-EX-P41'],'all',['29.1']),
 ('haetu','hǣtu','f','abstract-u','hǣt','heat','hǣtu hǣte hǣte hǣte - - - -',['U15-FB-P297','U15-WRIGHT-P184'],'sg-only',['29.1']),
 ('haelu','hǣlu','f','abstract-u','hǣl','salvation','hǣlu hǣlu hǣlu hǣlu - - - -',['U15-FB-P297','U15-WRIGHT-P184','U15-BT-P500B'],'sg-only',['29.11']),
 ('wer','wer','m','strong43','wer','man (adult male)','wer weres were wer weras wera werum weras',['U15-FB-P322'],'all',['29.5']),
 ('leornungcniht','leornungcniht','m','strong43','leornungcniht','disciple','leornungcniht leornungcnihtes leornungcnihte leornungcniht leornungcnihtas leornungcnihta leornungcnihtum leornungcnihtas',['U15-EX-P16'],'all',['29.10']),
 ('lareow','lārēow','m','strong43','lārēow','master; teacher','lārēow lārēowes lārēowe lārēow lārēowas lārēowa lārēowum lārēowas',['U15-FB-P302','U15-EX-P54'],'all',['29.10']),
 ('fotsceamul','fōtsceamul','m','strong43-retained-vowel','fōtsceamul','footstool','fōtsceamul fōtsceamules fōtsceamule fōtsceamul fōtsceamulas fōtsceamula fōtsceamulum fōtsceamulas',['U15-EX-P17','U15-FB-P28'],'all',['30.1']),
 ('heafod','hēafod','n','neuter47-syncope','hēafd','head','hēafod hēafdes hēafde hēafod hēafdu hēafda hēafdum hēafdu',['U15-FB-P297'],'all',['30.2']),
 ('haer','hǣr','n','neuter47-heavy','hǣr','hair; a hair','hǣr hǣres hǣre hǣr hǣr hǣra hǣrum hǣr',['U15-EX-P17'],'all',['30.2']),
 ('toth','tōð','m','root46','tōð/tēð','tooth','tōð tōðes tēð tōð tēð tōða tōðum tēð',['U15-FB-P32','U15-EX-P17'],'all',['30.4']),
 ('bebod','bebod','n','neuter47-short','bebod','commandment','bebod bebodes bebode bebod bebodu beboda bebodum bebodu',['U15-EX-P17'],'all',['30.5']),
 ('bryd','brȳd','f','feminine51-heavy','brȳd','bride','brȳd brȳde brȳde brȳde brȳda brȳda brȳdum brȳda',['U15-EX-P17'],'all',['30.11']),
 ('ham-noun','hām','m','strong43','hām','home; dwelling','hām hāmes hāme hām hāmas hāma hāmum hāmas',['U15-BT-P506'],'all',['30.11']),
 ('aliesend','ālīesend','m','agent43-end','ālīesend','Redeemer; one who delivers','ālīesend ālīesendes ālīesende ālīesend ālīesend ālīesendra ālīesendum ālīesend',['U15-FB-P275','U15-EX-P59'],'sg',['31.1','FB-XI-ALFRED-PRAYER']),
 ('flaesc','flǣsc','n','neuter47-heavy','flǣsc','flesh','flǣsc flǣsces flǣsce flǣsc flǣsc flǣsca flǣscum flǣsc',['U15-FB-P287','U15-EX-P48'],'sg',['31.2']),
 ('willa','willa','m','weak53','will','will; intention','willa willan willan willan willan willena willum willan',['U15-FB-P322'],'sg',['31.3','31.6','FB-XI-ALFRED-PRAYER']),
 ('costnung','costnung','f','feminine51-ung','costnung','temptation','costnung costnunge costnunge costnunge costnunga costnunga costnungum costnunga',['U15-FB-P281'],'all',['31.4','FB-XI-ALFRED-PRAYER']),
 ('engle','Engle','m','people44','Engl','the English (people)','- - - - Engle Engla Englum Engle',['U15-FB-P285','U15-EX-P46'],'pl-only',['31.7']),
 ('dene','Dęne','m','people44','Dęn','the Danes','- - - - Dęne Dęna Dęnum Dęne',['U15-FB-P30','U15-EX-P18'],'pl-only',['31.8']),
 ('awendednes','āwęndednes','f','feminine51-nes','āwęndedness','translation','āwęndednes āwęndednesse āwęndednesse āwęndednesse āwęndednessa āwęndednessa āwęndednessum āwęndednessa',['U15-FB-P277','U15-EX-P65'],'all',['31.8']),
 ('leothwyrhta','lēoðwyrhta','m','weak53','lēoðwyrht','poet','lēoðwyrhta lēoðwyrhtan lēoðwyrhtan lēoðwyrhtan lēoðwyrhtan lēoðwyrhtena lēoðwyrhtum lēoðwyrhtan',['U15-EX-P18'],'all',['31.8']),
 ('becraeding','bēcrǣding','f','feminine51-ung','bēcrǣding','reading (books)','bēcrǣding bēcrǣdinge bēcrǣdinge bēcrǣdinge bēcrǣdinga bēcrǣdinga bēcrǣdingum bēcrǣdinga',['U15-FB-P277','U15-EX-P59'],'sg',['31.11']),
 ('boc','bōc','f','root52','bōc/bēc','book','bōc bēc bēc bōc bēc bōca bōcum bēc',['U15-FB-P279'],'all',['31.12','31.13','31.14','FB-X-ALFRED-PREFACE']),
 ('leoth','lēoð','n','neuter47-heavy','lēoð','poem; poetry; verse','lēoð lēoðes lēoðe lēoð lēoð lēoða lēoðum lēoð',['U15-FB-P303'],'all',['31.12','FB-X-ALFRED-PREFACE']),
 ('strengu','strengu','f','abstract-u-reference','streng','strength','strengu strenge strenge strenge strenga strenga strengum strenga',['U15-WRIGHT-P184'],'reference',[])]
rulemap={'strong43':['M43'],'strong43-retained-vowel':['M43','M43-VOWEL'],'weak53':['WEAK53'],'neuter47-heavy':['N47'],'neuter47-short':['N47'],'neuter47-syncope':['N47','N47-SYNCOPE'],'feminine51-heavy':['F51'],'feminine51-nes':['F51'],'feminine51-ung':['F51'],'root46':['ROOT46'],'root52':['BOC52'],'kinship52':['SWEOSTOR52'],'people44':['PEOPLES44'],'agent43-end':['END43'],'abstract-u':['ABSTRACT-U'],'abstract-u-reference':['STRENGU-CLASS']}
variants={'toth':{'dative_singular':'tōðe','nominative_accusative_plural':'tōðas'},'boc':{'genitive_singular':'bōce'},'dene':{'genitive_plural':['Dęniga','Dęnia']},'aliesend':{'nominative_accusative_plural':['ālīesende','ālīesendas']},'haelu':{'singular_oblique':['hǣle','hǣlu','hǣlo'],'nominative_singular':['hǣlu','hǣlo']},'haetu':{'singular_oblique':['hǣte','hǣtu','hǣto'],'nominative_singular':['hǣtu','hǣto']},'strengu':{'nominative_singular':['strengu','strengo'],'singular_oblique':['strenge','strengu','strengo'],'nominative_accusative_plural':['strenga','strenge','strengu','strengo']}}
def scope_snapshot(x):return {k:copy.deepcopy(x.get(k)) for k in ['production_taught_in','recognition_taught_in','supplied_in','coverage_contract']}
def norm(v):return {'nominative':'nom','genitive':'gen','dative':'dat','accusative':'acc','singular':'sg','plural':'pl'}.get(v,v)
def matches(f,case,num):
 a=f.get('analysis',{});text=' '.join(str(v) for v in a.values())
 return (norm(a.get('case'))==case and norm(a.get('number'))==num) or case+'-'+num in text or (f'-{case}-{num}' in f['form_id'])
lemmas=[];pars=[]
for lid,head,gender,model,stem,gloss,surfaces,ev,scope,uses in D:
 old=OLD.get(lid);tid='NEW-U15-NOM-'+lid.upper();rid=['U15-NOM-'+x for x in rulemap[model]]
 refs=list(dict.fromkeys(ev+[e for r in rules if r['rule_id'] in rid for e in r['evidence_refs']]))
 tasks=[('EX-IX-' if int(t.split('.')[0])<31 else 'EX-X-XI-')+t.split('.')[0]+'-'+t.split('.')[1].zfill(2) if t[0].isdigit() else t for t in uses]
 note={'all':'Complete singular/plural production in the assigned lexical sense and taught constructions.','sg':'Singular lexical use productive; plural cells are morphological reference only, with no independent plural lexical task.','sg-only':'Complete singular teaching; plural lexical use unassigned. Table explicitly leaves plural cells unassigned because no count sense or lexical plural is established; this does not claim historical absolute defectiveness.','pl-only':'Complete plural teaching of this people name; singular cells unassigned. No singular is manufactured by backformation.','reference':'Complete eight-cell class-reference model from Wright184, recognition only. No independent production or plural count-sense task; Wright spelling retained without inferred Cook diacritics. This complete model, not the unassigned hǣlu/hǣtu plural slots, introduces the class.'}[scope]
 cells=[];forms=[]
 for (num,case),surface in zip([(n,c) for n in ['sg','pl'] for c in ['nom','gen','dat','acc']],surfaces.split()):
  if surface=='-':cells.append(dict(case=case,number=num,form=None,form_id=None,knowledge_status='unassigned',reason=note));continue
  oldf=next((f for f in (old or {}).get('forms',[]) if f['form']==surface and matches(f,case,num)),None)
  status='new_recognition' if scope=='reference' or (scope=='sg' and num=='pl') else 'new_production'
  f=dict(form_id=oldf['form_id'] if oldf else f'{lid}-{case}-{num}',form=surface,analysis=copy.deepcopy(oldf['analysis']) if oldf else dict(case=case,number=num,gender=gender),contextual_analysis=dict(case=case,number=num,gender=gender),knowledge_status=status,teaching_ids=[tid],evidence_refs=refs,evidence_basis='Rule-derived complete-model cell from the cited image-checked lemma and explicit stem/rule; not claimed as an individually attested corpus token.',prior_scope=scope_snapshot(oldf) if oldf else None,scope_note=note)
  forms.append(f);cells.append(f)
 # Preserve earlier supplied hǣle identities as recognized attested variants, rather than replacing them.
 if lid=='haelu':
  for oldf in old['forms']:
   f=copy.deepcopy({k:oldf[k] for k in ['form_id','form','analysis']});f.update(knowledge_status='new_recognition',teaching_ids=[tid],evidence_refs=refs,prior_scope=scope_snapshot(oldf),scope_note='Recognize the earlier -e oblique variant; invariant hǣlu is the selected productive singular.');forms.append(f)
 olds=old['senses'][0] if old and lid in ['wer','willa','becraeding'] else None
 sid=olds['sense_id'] if olds else lid+'-1'
 sense=dict(sense_id=sid,gloss=olds['gloss'] if olds else gloss,contextual_gloss=gloss,knowledge_status='new_recognition' if scope=='reference' else 'new_production',teaching_ids=['NEW-U15-VOC-'+lid.upper()],evidence_refs=refs,scope_note=note,prior_scope=scope_snapshot(olds) if olds else None,used_in_tasks=tasks)
 l=dict(lemma_id=lid,display_headword=head,part_of_speech='noun',gender={'m':'masculine','f':'feminine','n':'neuter'}[gender],declension_model=model,diagnostic_stem=stem,forms=forms,senses=[sense],evidence_refs=refs,rules=rid,scope_note=note,accepted_variants=variants.get(lid,{}),used_in_tasks=tasks,prior_lemma_present=bool(old),origin_category='new teaching material with image-backed lexical citation and explicit rule derivation')
 if lid=='ham-noun':l['identity_note']='Distinct nominal entry from prior adverb ham; prior homewards does not teach accusative noun home.'
 if lid=='fotsceamul':l['identity_note']='Exact prompt spelling fōtsceamul retained; variants fōtsceamel/fōtsceamol attested in BT entry12091. Selected uncontracted stem has source-class/rule evidence, not independently attested every cell.'
 if lid=='aliesend':l['identity_note']='Capitalization Ālīesend in prayer is contextual; lexical headword lower-case. Plural table does not teach a theological plurality of Redeemers.'
 lemmas.append(l);pars.append(dict(paradigm_id=tid,lemma_id=lid,headword=head,model=model,diagnostic_stem=stem,scope=note,cells=cells,rules=rid,accepted_variants=variants.get(lid,{}),evidence_refs=refs))
# Previously productive morphology, newly bounded senses.
for lid,sid,gloss,ev,tasks in [('med','med-hire-u15','hire; wages paid for work',['U15-EX-P16'],['EX-IX-28-10']),('tid','tid-hour-u13-source','hour, a time measure',['U15-FB-P316','U15-EX-P51'],['EX-IX-28-06','EX-IX-28-07','EX-IX-28-11']),('straet','straet-public-place-u15','public place; street as a gathering place',['U15-EX-P59'],['EX-IX-28-04'])]:
 old=OLD[lid];olds=next((s for s in old['senses'] if s['sense_id']==sid),None)
 forms=[dict(form_id=f['form_id'],form=f['form'],analysis=f['analysis'],knowledge_status='previously_taught',prior_scope=scope_snapshot(f),evidence_refs=ev) for f in old['forms']]
 lemmas.append(dict(lemma_id=lid,display_headword=old['display_headword'],part_of_speech='noun',forms=forms,senses=[dict(sense_id=sid,gloss=olds['gloss'] if olds else gloss,contextual_gloss=gloss,knowledge_status='new_production',teaching_ids=['NEW-U15-VOC-'+lid.upper()+'-SENSE'],evidence_refs=ev,prior_scope=scope_snapshot(olds) if olds else None,used_in_tasks=tasks)],evidence_refs=ev,prior_lemma_present=True,scope_note='Existing complete morphology remains prior teaching; only the explicitly described lexical sense is newly productive.',used_in_tasks=tasks))
counts=dict(lemmas=len(lemmas),nominal_systems=len(pars),forms=sum(len(l['forms']) for l in lemmas),sense_records=sum(len(l['senses']) for l in lemmas),form_status_counts=dict(collections.Counter(f['knowledge_status'] for l in lemmas for f in l['forms'])))
dump('lexical-inventory.json',dict(schema_version=1,baseline_checkpoint='9129cda',status='Source-audited bounded nominal proposal; active integration and independent review pending.',lemmas=lemmas,rules=rules,counts=counts))
dump('noun-adjective-paradigms.json',dict(schema_version=1,paradigms=pars,rules=rules,counts=counts,adjective_scope='Owned separately by unit15_grammar. No adjective evidence inferred from these noun records.'))
print(json.dumps(counts))
