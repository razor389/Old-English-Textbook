"""Reproducible precontract nominal audit. Never mutates active registers."""
import json, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
LEX=json.loads((ROOT/'lexicon/entries.json').read_text(encoding='utf-8'))
LEMMAS={x['lemma_id']:x for x in LEX['lemmas']}
CASES=['nom','gen','dat','acc']
def dump(name,x): (OUT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def norm(a):
 if not isinstance(a,dict):return {}
 m={'nominative':'nom','genitive':'gen','dative':'dat','accusative':'acc','instrumental':'ins','singular':'sg','plural':'pl','masculine':'m','feminine':'f','neuter':'n'}
 return {('strength' if k=='declension' else k):m.get(v,v) if isinstance(v,str) else v for k,v in a.items()}
def prior(lid,form,a):
 wanted=norm(a)
 hits=[]
 for f in LEMMAS.get(lid,{}).get('forms',[]):
  aa=norm(f.get('analysis'))
  if f['form']==form and all(aa.get(k)==v for k,v in wanted.items()):hits.append(f)
 # Retain original source IDs only where the actual registered analysis is explicit.
 if hits:
  f=sorted(hits,key=lambda f:(not bool(f.get('production_taught_in')),not bool(f.get('recognition_taught_in'))))[0]
  return {k:f.get(k) for k in ['form_id','form','analysis','production_taught_in','recognition_taught_in','supplied_in']}
 return None
def cell(lid,form,a,pid,evidence,scope,status='new_production'):
 p=prior(lid,form,a)
 fid=f"{lid}-{a['case']}-{a['number']}"+(f"-{a['gender']}-{a['strength']}" if 'strength' in a else '')
 if p:fid=p['form_id']
 if p and p.get('production_taught_in'):status='previously_taught'
 return dict(form_id=fid,form=form,analysis=a,knowledge_status=status,teaching_ids=[] if status=='previously_taught' else [pid],evidence_refs=evidence,evidence_basis='Derived from the image-checked headword, stated diagnostic stem and cited class rule; not a claim that every cell is individually attested in this passage.',prior_scope=p,scope_note=scope)
PAR=[]
SENSE=[]
def noun(lid,head,gender,model,stem,gloss,items,ev,number='both',overrides=None,diagnostic='',sense_id=None):
 pid='NEW-U17-NOM-'+lid.upper()
 refs=ev.split()+(['U17-FB-P37'] if model.startswith('53') else ['U17-FB-P35','U17-FB-P36'] if model.startswith('51') else ['U17-FB-P32','U17-FB-P33'] if model.startswith('47') else ['U17-FB-P28','U17-FB-P29','U17-FB-P30'])
 if model.startswith('53'):
  forms=[head,stem+'an',stem+'an',head if gender=='n' else stem+'an',stem+'an',stem+'ena',stem+'um',stem+'an']
 elif model.startswith('51'):
  forms=[head,stem+'e',stem+'e',stem+'e',stem+'a',stem+'a',stem+'um',stem+'a']
 elif model.startswith('47'):
  plu=stem+('u' if model in ['47-short','47-syncope'] else '')
  forms=[head,stem+'es',stem+'e',head,plu,stem+'a',stem+'um',plu]
 elif model.startswith('44'):
  forms=[head,stem+'es',head,head,stem+'as',stem+'a',stem+'um',stem+'as']
 else:
  forms=[head,stem+'es',stem+'e',head,stem+'as',stem+'a',stem+'um',stem+'as']
 if overrides:
  for k,v in overrides.items():forms[k]=v
 scope=('Complete nominative, genitive, dative and accusative singular/plural of the stated count or individuated sense; familiar basic uses only.' if number=='both' else 'Reuse of a previously taught noun class: complete four-case singular of this stated mass/abstract sense. The plural lies outside the taught sense and this assignment; this is not a claim that the noun lacks a plural or an introduction of a new noun class.')
 cells=[]
 for i,f in enumerate(forms[:8 if number=='both' else 4]):
  cells.append(cell(lid,f,{'case':CASES[i%4],'number':'sg' if i<4 else 'pl','gender':gender},pid,refs,scope))
 PAR.append(dict(paradigm_id=pid,lemma_id=lid,headword=head,part_of_speech='noun',model='Cook '+model,diagnostic_stem=stem,diagnostic_rule=diagnostic or 'Add the displayed class endings to this stem; retain all printed vowel quantities.',scope=scope,number_scope=number,cells=cells,evidence_refs=refs,source_items=items.split()))
 old=LEMMAS.get(lid,{}).get('senses',[])
 chosen=sense_id or lid+'-u17-sense'
 oldmatch=next((s for s in old if s['sense_id']==chosen),None)
 SENSE.append(dict(lemma_id=lid,headword=head,sense_id=chosen,gloss=gloss,knowledge_status='previously_taught' if oldmatch and oldmatch.get('production_taught_in') else 'new_production',prior_senses=[{k:s.get(k) for k in ['sense_id','gloss','production_taught_in','recognition_taught_in','supplied_in']} for s in old],source_items=items.split(),evidence_refs=refs,teaching_ids=[pid],scope=scope))

# Exact class numbers are those printed in the exercise hint or image-checked glossary.
noun('heanes','hēanes','f','51.5','hēaness','heights; highest places','37.1','U17-EX-P50 U17-FB-P298',diagnostic='Double final s in every ending-bearing form; retain e. The source headword is hēanes, not hēahnes. The singular sense retains its separate original register ID.',sense_id='heanes-heights-u13-source')
noun('maegen','mægen','n','47','mægen','power; strength; in37.2 heavenly powers','37.2','U17-EX-P22 U17-FB-P304 U17-FB-P29',overrides={4:'mægnu',7:'mægnu'},diagnostic='Retain mægen- in genitive/dative singular and plural: mægenes, mægene, mægena, mægenum. Cook47.1 explicitly selects the exceptional nominative/accusative plural mægnu; that plural does not authorize an all-ending mægn- stem. Later contracted obliques require separately identified evidence and are outside this selected table.',sense_id='maegen-u17-power')
noun('draca','draca','m','53','drac','dragon','37.7','U17-EX-P22')
noun('yst','ȳst','f','51.b','ȳst','storm','37.8','U17-EX-P22')
noun('hyll','hyll','m','43','hyll','hill','37.9','U17-EX-P23')
noun('cederbeam','cēderbēam','m','43','cēderbēam','cedar; cedar tree','37.9','U17-EX-P42 U17-FB-P281')
noun('naedre','nædre','f','53.1','nædr','serpent','37.10','U17-EX-P61',diagnostic='The English–Old English glossary explicitly gives nædre (næddre),53.1. Select nædre consistently; do not add a length mark. The alternative doubled d is recognized, not silently mixed into this table.')
noun('dema','dēma','m','53','dēm','judge','37.11','U17-FB-P282')
noun('halga','hālga','m','53','hālg','saint; holy one','37.14','U17-EX-P23 U17-BT-P504',diagnostic='The hint specifies weak noun hālga53. Printed BT504 independently gives hālga an;m. and hālgena. Genitive plural hālgena differs from adjectival hālgra; do not silently replace the noun with hālig.')
noun('horn','horn','m','43','horn','horn; figuratively strength or dignity in37.14','37.14','U17-EX-P23 U17-BT-P553',diagnostic='Selected masculine follows the explicit Cook43 hint and BT553 es;m., including se horn and hornas. Neuter is an attested alternative outside this selected table. The figurative explanation is contextual modern help, not an instruction to replace horn by a different noun.')
noun('lof','lof','m','43','lof','praise','37.14','U17-EX-P58',number='sg',sense_id='lof-u15-source-sense')
noun('cwen','cwēn','f','51.1','cwēn','queen','38.2 38.4 38.5 38.6 39.2 39.3','U17-FB-P282 U17-EX-P58',overrides={3:'cwēn'},diagnostic='FB282 explicitly assigns51.1, permitting endingless accusative singular cwēn. Ex58 assigns general51.b; cwēne is the ordinary-class variant and must be explained if selected.',sense_id='cwen-u17-queen')
noun('hlisa','hlīsa','m','53','hlīs','fame','38.3','U17-EX-P23',diagnostic='Weak masculine. Fame is singular; separately assigned reports can be individuated. Full number table does not license every abstract/count use without context.',sense_id='hlisa-u17-fame')
noun('olfend','olfend','m','43','olfend','camel','38.3','U17-EX-P42 U17-FB-P308',diagnostic='Retain e: olfend belongs to ordinary43, not the agent-noun subclass43.6 merely because its letters end in end.')
noun('andgiet','andgiet','n','47','andgiet','meaning; sense','38.5','U17-EX-P54 U17-FB-P275',number='sg',diagnostic='The already-taught neuter class is reused for the four abstract-singular cells andgiet, andgietes, andgiete, andgiet. Both assigned uses are singular. All plural forms and count/faculty senses are outside this assignment; no defective-noun claim is made. The earlier proposed zero nominative/accusative plural lacked specific evidence and is withdrawn.',sense_id='andgiet-u15-source-sense')
noun('thenung','ðēnung','f','51.3','ðēnung','service; attendance; service performed','38.6','U17-FB-P318',sense_id='thenung-u16-reading',diagnostic='Ordinary -e singular is selected. Cook51.3 also permits -a in the dative and sometimes genitive/accusative of -ung nouns; preserve a source variant if encountered.')
noun('thegn','ðegn','m','43','ðegn','vassal; retainer; thane','38.10 39.3','U17-FB-P317 U17-EX-P64')
noun('theowa','ðēowa','m','53','ðēow','servant','38.10','U17-EX-P24',diagnostic='Original hint specifies weak ðēowa53: nominative plural ðēowan, not strong ðēowas.')
noun('wisdom','wīsdōm','m','43','wīsdōm','wisdom','38.6 38.8 38.9 38.10 39.4 41.1 42.6','U17-FB-P20 U17-FB-P84 U17-EX-P24',number='sg',diagnostic='FB20 explicitly prints wīsdōm with both lengths; FB143 identifies masculine -dōm compounds. Inflect the compound by the familiar dōm class43.')
noun('pund','pund','n','47','pund','pound; source weight measure','39.2','U17-EX-P58 U17-FB-P309')
noun('grundweall','grundweall','m','43','grundweall','foundation','39.5','U17-EX-P25')
noun('getimbrung','getimbrung','f','51.3','getimbrung','building; structure built','39.6','U17-EX-P25',diagnostic='The noun is feminine. In39.6 use a feminine resumptive subject, not a masculine pronoun inferred from English building.')
noun('edlean','edlēan','n','47','edlēan','reward; recompense','39.6','U17-EX-P25')
noun('eare','ēare','n','53.2','ēar','ear','39.7','U17-EX-P25 U17-FB-P37',overrides={3:'ēare',5:'ēarna'},diagnostic='Weak neuter: nominative/accusative singular ēare; other singular ēaran; plural ēaran, ēarna, ēarum, ēaran. Genitive plural contracts.')
noun('eadmodnes','ēaðmōdnes','f','51.5','ēaðmōdness','humility','40.3','U17-EX-P51 U17-FB-P284',number='sg',diagnostic='Double s in the oblique stem; no syncope of the preceding e.')
noun('thinen','ðīnen','f','51.5','ðīnenn','handmaiden','40.3','U17-EX-P25 U17-FB-P318',diagnostic='Cook51.5 explicitly applies: double n and retain e, hence ðīnenne, not ðīnene or ðīnnes.')
noun('cneoris','cnēoris','f','51.5','cnēoriss','generation','40.3 40.5','U17-EX-P25 U17-FB-P281',diagnostic='The glossary explicitly says like51.5: cnēorisse, cnēorissa, cnēorissum. Do not infer a one-s stem from the nominative. Glossary tribe/nation is not an additional productive grant.')
noun('cniht','cniht','m','43','cniht','servant','40.8','U17-EX-P26 U17-FB-P281',sense_id='cniht-u17-servant')
noun('ymbhwyrft','ymbhwyrft','m','43','ymbhwyrft','circuit; compass; orbit','41.2 42.5','U17-FB-P324 U17-EX-P42',sense_id='ymbhwyrft-u13-source')
noun('gylt','gylt','m','43','gylt','debt, including the prayer’s figurative moral debt','41.8','U17-EX-P26',diagnostic='Keep the literal source English debts. Moral wrongdoing is a contextual explanation of the prayer, not an unrestricted separately taught offence sense.')
noun('gyltend','gyltend','m','43.6','gyltend','debtor','41.8','U17-EX-P26',overrides={4:'gyltende',5:'gyltendra',7:'gyltende'},diagnostic='Agent noun43.6: select plural nominative/accusative -e, genitive -ra, dative -um. Endingless plural is a source-listed alternative; -as is rare, not the selected table.')
noun('finger','finger','m','43.4','fingr','finger','41.12','U17-EX-P26',diagnostic='Initial syllable heavy, final syllable light: syncopate before endings by43.4; nominative/accusative singular finger, genitive fingres, dative fingre.')
noun('tabele','tabele','f','53.1','tabel','tablet; table of the law','41.12','U17-EX-P26',diagnostic='Weak feminine tabele: retain tabel- throughout the oblique forms; dative plural tabelum, not tabulum.')
noun('hearpere','hearpere','m','44.1','hearper','harper','42.2','U17-FB-P84',diagnostic='FB143 explicitly gives hearpere. Agent nouns in -ere follow44.1: genitive plural hearpera, not hearperena.')
noun('hearpe','hearpe','f','53.1','hearp','harp','42.2 FB174.7-175.17','U17-FB-P298 U17-EX-P50')
noun('maegth-tribe','mǣgð','f','51.b','mǣgð','tribe; nation','42.3','U17-FB-P304 U17-EX-P65',diagnostic='Long ǣ distinguishes this noun from mægð, maiden, an umlaut feminine. Preserve the length and the source long-stem class. Province is not granted as a new productive sense.')
noun('thrymsetl','ðrymsetl','n','47','ðrymsetl','throne; throne of glory','42.2 42.3 42.4 42.5','U17-EX-P27',diagnostic='Preserve unmarked y in the hint. Final component setl has a heavy stem, so plural nominative/accusative ðrymsetl, not -u.')
noun('palmtwig','palmtwīg','n','47','palmtwīg','palm twig; palm branch','42.3','U17-EX-P27',diagnostic='The hint explicitly marks long ī. This makes a heavy neuter: nominative/accusative plural palmtwīg, not palmtwīgu.')
noun('cneo','cnēo','n','47.3','cnēow','knee','42.8','U17-FB-P33',overrides={0:'cnēo',3:'cnēo',4:'cnēowu',7:'cnēowu'},diagnostic='Cook47.3 gives cnēo, with w before endings and nominative/accusative plural cnēowu. Prior exposure supplied only the plural object knees.',sense_id='cneo-u17-knee')
noun('bletsung','blētsung','f','51.3','blētsung','blessing','42.6','U17-EX-P41',number='sg')
noun('beorhtnes','beorhtnes','f','51.5','beorhtness','brightness','42.6','U17-EX-P41',number='sg')
noun('thancung','ðancung','f','51.3','ðancung','thanksgiving','42.6','U17-EX-P27 U17-FB-P84',number='sg',diagnostic='The hint supplies the headword; FB144 identifies feminine -ung and51.3 supplies the inflection. Singular abstract scope only.')
noun('weorthscipe','weorðscipe','m','44.1','weorðscip','honour; dignity','42.6','U17-EX-P45 U17-FB-P322',number='sg')
noun('fox','fox','m','43','fox','fox','42.7','U17-EX-P27')
noun('hol','hol','n','47-short','hol','hole','42.7','U17-EX-P27',diagnostic='Short heavy distinction: hol has short vowel plus a single consonant; nominative/accusative plural holu.')
noun('nest','nest','n','47','nest','nest','42.7','U17-EX-P27',diagnostic='The consonant cluster st makes a heavy stem; nominative/accusative plural nest, not nestu.')
noun('thorn','ðorn','m','43','ðorn','thorn','42.8','U17-EX-P27')
noun('cynehelm','cynehelm','m','43','cynehelm','crown','42.8 FB175.5','U17-FB-P282')
noun('hreod','hrēod','n','47','hrēod','reed','42.8 42.9','U17-BT-P557',diagnostic='Personally inspected BT557 gives HRÉOD es;n. and a plural reeds example. Acute length in BT is declared normalized to the course macron; long ēo makes a heavy neuter with endingless nominative/accusative plural.')
noun('blostma','blōstma','m','53','blōstm','blossom','43.1','U17-EX-P41 U17-FB-P279')
noun('biema','biema','m','53','biem','trumpet; clarion','43.3','U17-EX-P65 U17-FB-P279',diagnostic='Retain source biema without an inferred vowel length; do not normalize to bȳme.')
noun('hlaefdige','hlǣfdige','f','53.1','hlǣfdig','lady','43.4','U17-FB-P299')
noun('gerimcraeft','gerīmcræft','m','43','gerīmcræft','arithmetic; computation','43.7','U17-EX-P39 U17-FB-P294',number='sg')
noun('stan','stān','m','43','stān','stone','39.2 39.5 41.11','U17-EX-P63 U17-FB-P28',sense_id='stan-u11-source')

def adjective(lid,head,stem,kind,gloss,items,ev,sense_id=None):
 pid='NEW-U17-ADJ-'+lid.upper(); refs=ev.split()+['U17-FB-P38','U17-FB-P39','U17-FB-P40','U17-FB-P41']
 scope='Complete strong and weak positive adjective: all three genders, singular and plural, nominative/genitive/dative/accusative. Separate masculine/neuter strong instrumental singular is recognition only; its display does not license new instrumental uses.'
 cells=[]
 for strength in ['strong','weak']:
  for number in ['sg','pl']:
   for gender in ['m','n','f']:
    if strength=='weak':endings=([('a' if gender=='m' else 'e'),'an','an',('e' if gender=='n' else 'an')] if number=='sg' else ['an','ra','um','an'])
    elif number=='pl':endings=[{'m':'e','n':('u' if kind in ['e','polysyllable'] else ''),'f':'a'}[gender],'ra','um',{'m':'e','n':('u' if kind in ['e','polysyllable'] else ''),'f':'a'}[gender]]
    elif gender=='m':endings=['','es','um','ne']
    elif gender=='n':endings=['','es','um','']
    else:endings=[('u' if kind in ['e','polysyllable'] else ''),'re','re','e']
    for case,end in zip(CASES,endings):
     f=stem+end if end else head
     a=dict(case=case,number=number,gender=gender,strength=strength)
     cells.append(cell(lid,f,a,pid,refs,scope))
 for gender in ['m','n']:cells.append(cell(lid,stem+'e',dict(case='ins',number='sg',gender=gender,strength='strong'),pid,refs,scope,'new_recognition'))
 PAR.append(dict(paradigm_id=pid,lemma_id=lid,headword=head,part_of_speech='adjective',model='Cook '+('59' if kind=='e' else '57.3, selected uncontracted forms' if kind=='polysyllable' else '58')+'; weak60',diagnostic_stem=stem,diagnostic_rule=('Keep the dictionary -e only when no other ending is present; use the explicit stem for every ending.' if kind=='e' else 'The table selects the retained stem throughout; contracted alternatives require separate evidence and are not silently substituted.' if kind=='polysyllable' else 'Heavy stem: no -u in strong feminine nominative singular or neuter nominative/accusative plural.'),scope=scope,cells=cells,evidence_refs=refs,source_items=items.split()))
 old=LEMMAS.get(lid,{}).get('senses',[]); sid=sense_id or lid+'-u17-sense'; os=next((s for s in old if s['sense_id']==sid),None)
 SENSE.append(dict(lemma_id=lid,headword=head,sense_id=sid,gloss=gloss,knowledge_status='previously_taught' if os and os.get('production_taught_in') else 'new_production',prior_senses=[{k:s.get(k) for k in ['sense_id','gloss','production_taught_in','recognition_taught_in','supplied_in']} for s in old],source_items=items.split(),evidence_refs=refs,teaching_ids=[pid],scope=scope))

adjective('waestmbaere','wæstmbǣre','wæstmbǣr','e','fruitful','37.9','U17-EX-P23')
adjective('geong','geong','geong','heavy','young; substantivally young people','37.12','U17-EX-P68',sense_id='geong-young-source')
adjective('manigfeald','manigfeald','manigfeald','heavy','manifold; numerous and varied','38.6','U17-EX-P54 U17-FB-P304',sense_id='manigfeald-u15-source-sense')
adjective('rice-adjective','rīce','rīc','e','rich; substantivally rich people','40.7','U17-FB-P309 U17-EX-P26')
adjective('daeghwamlic','dæghwāmlīc','dæghwāmlīc','heavy','daily','41.8','U17-EX-P26')
adjective('hlud','hlūd','hlūd','heavy','loud','42.4','U17-EX-P27 U17-FB-P20')
adjective('aethele','æðele','æðel','e','noble; illustrious','43.14','U17-EX-P51',sense_id='aethele-u17-noble')
adjective('aethelboren','æðelboren','æðelboren','polysyllable','high-born','43.13','U17-EX-P50')

# Sense promotion is deliberately separate from form teaching.
def sense(lid,sid,gloss,items,ev,scope):
 l=LEMMAS[lid]
 SENSE.append(dict(lemma_id=lid,headword=l['display_headword'],sense_id=sid,gloss=gloss,knowledge_status='new_production',prior_senses=[{k:s.get(k) for k in ['sense_id','gloss','production_taught_in','recognition_taught_in','supplied_in']} for s in l['senses']],source_items=items.split(),evidence_refs=ev.split(),teaching_ids=['NEW-U17-SENSE-'+lid.upper()],scope=scope,forms_status='Use existing productive cells only; no new morphology is inferred from this sense promotion.'))
sense('heanes','heanes-u13-source','height; highest point','','U17-EX-P50 U17-FB-P298','Supplied singular reference cells complete the declared display; no singular task or new productive singular sense is assigned. Preserve this existing supplied sense and its original history.')
SENSE[-1]['knowledge_status']='supplied'; SENSE[-1]['teaching_ids']=['U17-REF-HEANES-SINGULAR']
for p in PAR:
 if p['lemma_id']=='heanes':
  p['scope']='Full eight-cell reference display; only plural heights is assigned for production. All four singular cells and the singular sense remain supplied reference, without independent recall.'
  p['number_scope']='both_displayed_plural_productive'
  for c in p['cells']:
   if c['analysis']['number']=='sg':c.update(knowledge_status='supplied',teaching_ids=['U17-REF-HEANES-SINGULAR'],scope_note='Supplied singular reference only; no independent singular use assigned.')
sense('saed','saed-u17-descendants','seed; offspring; descendants collectively','40.9','U17-EX-P26 U17-BT-P809','Collective singular, specifically dative singular sǣde referring to Abraham’s descendants. BT809 sense V explicitly gives progeny/posterity and the Luke1.55 phrase to Abrahame and hys sǽde. Do not translate it as a grammatical plural or seed for sowing.')
sense('folc','folc-u17-peoples','peoples; distinct peoples or national groups','37.11','U17-EX-P23','Count plural groups, distinct from the prior collective-singular sense. Use existing eight-case morphology; the nominal address is nominative neuter plural eall folc.')
sense('eald','eald-u17-elderly','old people; the elderly','37.12','U17-EX-P23 U17-FB-P38','Human substantive use of the adjective. Direct address selects weak masculine plural ealdan under the already-taught address rule; do not infer a new noun declension.')
sense('andgiet','andgiet-u15-source-understanding','understanding','43.11','U17-FB-P275','Promote only the abstract-singular understanding sense in the explicit task; retain the distinct abstract-singular meaning/sense entry used in38.5. All plural forms and count/faculty senses remain outside scope; this is not a defective-noun claim.')
SENSE[-1]['forms_status']='Use the complete four-case abstract-singular andgiet display, reusing the previously taught neuter class; no plural or extra morphology.'
sense('wer','wer-u17-husband','husband','43.19','U17-EX-P51 U17-FB-P322','Marital relationship, distinct from the already productive man. Existing eight forms suffice.')
sense('craeft','craeft-u17-skill','skill; accomplishment','FB175.11','U17-FB-P175','Supplied recognition of the exact phrase mid cræfte, by skill. Prior craft/occupation is not automatically this performance sense; no independent production assigned.')
SENSE[-1]['knowledge_status']='supplied'; SENSE[-1]['teaching_ids']=['U17-READ-HELP-CRA EFT'.replace(' ','')]
for lid,sid,gloss,items,ev in [('cwen','cwen-u17-princess','princess','43.6','U17-EX-P58 U17-FB-P282'),('hlisa','hlisa-u17-report','report; account heard','38.9','U17-EX-P24')]:
 base=next(s for s in SENSE if s['lemma_id']==lid)
 SENSE.append({**base,'sense_id':sid,'gloss':gloss,'source_items':items.split(),'evidence_refs':ev.split(),'scope':'Separate contextual sense sharing the complete noun table; no new morphology.'})

# Item pointers are drawn from the exact transcription, not a guessed page split.
ITEMS={f"{x['original_exercise']}.{x['original_item']}":x for x in json.loads((OUT/'exercises-prompts.json').read_text(encoding='utf-8'))['items']}
for row in PAR+SENSE:
 refs=[r for r in row['evidence_refs'] if r not in [f'U17-EX-P{x}' for x in range(22,29)]]
 for item in row['source_items']:
  if item in ITEMS:refs.extend(ITEMS[item]['evidence_refs'])
 row['evidence_refs']=list(dict.fromkeys(refs))
 if 'cells' in row:
  for c in row['cells']:c['evidence_refs']=row['evidence_refs']

rules=[
 dict(rule_id='U17-NOM-R01',rule='Masculine consonant stems43: singular zero/es/e/zero; plural as/a/um/as. Do not infer gender or class merely from an English translation.',evidence_refs=['U17-FB-P28']),
 dict(rule_id='U17-NOM-R02',rule='Syncope43.4 requires a heavy initial and light second syllable in the stated model; compare ēðel→ēðles with hęngest retaining e. Noun classes and explicitly listed exceptions outrank a mechanical spelling rule.',evidence_refs=['U17-FB-P29']),
 dict(rule_id='U17-NOM-R03',rule='Neuter47 nominative/accusative plural takes u for the stated short monosyllabic model, zero for the heavy model. Disyllables and compounds need their own diagnostic statement rather than automatic assignment from a final spelling. Cook47.1 explicitly lists mægnu in nominative/accusative plural; the selected table retains mægen- in all oblique forms. Final long vowels/diphthongs and consonant clusters matter, including palmtwīg and nest.',evidence_refs=['U17-FB-P29','U17-FB-P32','U17-FB-P33']),
 dict(rule_id='U17-NOM-R04',rule='Feminine51.5 -nes/-en/-el/-et doubles the final consonant in oblique forms and retains e. Explicit examples and glossary assignments govern cnēoris and ðīnen.',evidence_refs=['U17-FB-P36','U17-FB-P281','U17-FB-P318']),
 dict(rule_id='U17-NOM-R05',rule='Weak53 m-a/f-e: oblique singular an, plural an/ena/um/an. Weak neuter ēare keeps e in nominative/accusative singular and has genitive plural ēarna.',evidence_refs=['U17-FB-P37']),
 dict(rule_id='U17-NOM-R06',rule='Strong/weak adjective choice is a syntactic choice. Substantival use is separately identified; familiar adjective forms do not automatically teach a new lexical meaning or new participial government.',evidence_refs=['U17-FB-P38','U17-FB-P41']),
 dict(rule_id='U17-NOM-R07',rule='Tables are complete only within their named number/sense and case scope. Singular-only teaching is an assignment boundary, never an assertion that the word is defective. Supplied source forms must be visible at the task and cannot be independent-recall targets.',evidence_refs=['EDITORIAL_POLICY.md']),
 dict(rule_id='U17-NOM-R08',rule='Direct-address adjectives take weak forms under Cook55 and prior u09-vocative-weak-adjective. Thus the selected address forms are wæstmbǣran, gefiðredan, geongan and ealdan. Eall has its separately taught quantifier pattern; its presence does not make every neighboring modifier strong.',evidence_refs=['U17-FB-P38','chapters/ch09/coverage.json']),
]
dump('noun-adjective-paradigms.json',dict(schema_version=1,status='precontract proposed teaching; primary evidence checked; root must reconcile contract',paradigms=PAR,counts={'paradigms':len(PAR),'cells':sum(len(p['cells']) for p in PAR)},rules=rules))
dump('nominal-sense-audit.json',dict(schema_version=1,status='precontract proposed productive sense inventory; source-only sense below is explicitly recognition/supplied in final reconciliation',senses=SENSE))
print(len(PAR),'paradigms',sum(len(p['cells']) for p in PAR),'cells',len(SENSE),'senses')
