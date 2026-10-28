"""Reproducible Unit18 nominal evidence; never writes cumulative registers."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
LEX=json.loads((ROOT/'lexicon/entries.json').read_text(encoding='utf-8'))
LEMMAS={x['lemma_id']:x for x in LEX['lemmas']}
CASES=['nom','gen','dat','acc']
PAR=[]
SENSE=[]

def dump(name,x): (OUT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def norm(a):
 if not isinstance(a,dict):return {}
 m={'nominative':'nom','genitive':'gen','dative':'dat','accusative':'acc','instrumental':'ins','singular':'sg','plural':'pl','masculine':'m','feminine':'f','neuter':'n'}
 return {('strength' if k=='declension' else k):m.get(v,v) if isinstance(v,str) else v for k,v in a.items()}
def prior(lid,form,a):
 wanted=norm(a); hits=[]
 for f in LEMMAS.get(lid,{}).get('forms',[]):
  aa=norm(f.get('analysis'))
  if lid=='claene' and f['form_id'] in ['claene-u15-source-dat-n-sg-strong','claene-u15-source-dat-m-sg-strong']:
   aa=dict(case='dat',number='sg',gender='n' if '-n-' in f['form_id'] else 'm',strength='strong')
  if f['form'].casefold()==form.casefold() and all(aa.get(k)==v for k,v in wanted.items()):hits.append(f)
 if not hits:return None
 f=sorted(hits,key=lambda x:(not bool(x.get('production_taught_in')),not bool(x.get('recognition_taught_in'))))[0]
 return {k:f.get(k) for k in ['form_id','form','analysis','production_taught_in','recognition_taught_in','supplied_in','coverage_contract']}
def cell(lid,form,a,pid,refs,scope,status='new_production'):
 p=prior(lid,form,a)
 fid=f"{lid}-{a['case']}-{a['number']}"+(f"-{a['gender']}-{a['strength']}" if 'strength' in a else '')
 if p:fid=p['form_id']
 if p and p.get('production_taught_in'):status='previously_taught'
 return dict(form_id=fid,form=form,analysis=a,contextual_analysis=a,knowledge_status=status,
   teaching_ids=[] if status=='previously_taught' else [pid],evidence_refs=refs,
   evidence_basis='Rule-derived literal cell from the image-checked headword, diagnostic stem and cited class rule; not a claim that every displayed form is independently attested.',prior_scope=p,scope_note=scope)
def sense(lid,head,gloss,items,refs,pid,scope,sid=None):
 old=LEMMAS.get(lid,{}).get('senses',[]);sid=sid or lid+'-u18-sense';p=next((x for x in old if x['sense_id']==sid),None)
 SENSE.append(dict(lemma_id=lid,headword=head,sense_id=sid,gloss=gloss,knowledge_status='previously_taught' if p and p.get('production_taught_in') else 'new_production',prior_senses=[{k:s.get(k) for k in ['sense_id','gloss','production_taught_in','recognition_taught_in','supplied_in']} for s in old],source_items=items.split(),evidence_refs=refs,teaching_ids=[pid],scope=scope))
def noun(lid,head,gender,model,stem,gloss,items,ev,number='both',overrides=None,diagnostic='',sid=None):
 pid='NEW-U18-NOM-'+lid.upper();refs=ev.split()+(['U18-FB-P37'] if model.startswith('53') else ['U18-FB-P35','U18-FB-P36'] if model.startswith('51') else ['U18-FB-P32','U18-FB-P33'] if model.startswith('47') else ['U18-FB-P28','U18-FB-P29','U18-FB-P30'])
 if model.startswith('53'):fs=[head,stem+'an',stem+'an',stem+'an',stem+'an',stem+'ena',stem+'um',stem+'an']
 elif model.startswith('51'):fs=[head,stem+'e',stem+'e',stem+'e',stem+'a',stem+'a',stem+'um',stem+'a']
 elif model.startswith('47'):
  pl=stem+('u' if model=='47-short' else '')
  fs=[head,stem+'es',stem+'e',head,pl,stem+'a',stem+'um',pl]
 elif model.startswith('44'):fs=[head,stem+'es',head,head,stem+'as',stem+'a',stem+'um',stem+'as']
 else:fs=[head,stem+'es',stem+'e',head,stem+'as',stem+'a',stem+'um',stem+'as']
 for k,v in (overrides or {}).items():fs[k]=v
 scope=('Complete nominative/genitive/dative/accusative singular and plural of the stated count or individuated sense, with familiar basic uses only.' if number=='both' else 'Complete four-case singular of this mass or abstract sense, reusing an already taught noun class. Plural forms and count senses are outside this assignment; this is not a defective-noun claim or a new noun-class introduction.')
 cs=[cell(lid,f,dict(case=CASES[i%4],number='sg' if i<4 else 'pl',gender=gender),pid,refs,scope) for i,f in enumerate(fs[:8 if number=='both' else 4])]
 PAR.append(dict(paradigm_id=pid,lemma_id=lid,headword=head,part_of_speech='noun',model='Cook '+model,diagnostic_stem=stem,diagnostic_rule=diagnostic or 'Keep the printed headword and vowel quantities; add the displayed class endings to the diagnostic stem.',number_scope=number,scope=scope,cells=cs,evidence_refs=refs,source_items=items.split()))
 sense(lid,head,gloss,items,refs,pid,scope,sid)

noun('sacc','sacc','m','43','sacc','sack','45.6 45.8 45.9 46.1 46.7 46.8 47.2 47.5','U18-EX-P30 U18-EX-P31')
noun('assa','assa','m','53','ass','ass; donkey','45.6 46.2','U18-EX-P39',diagnostic='Cook explicitly gives assa53. All oblique singular and nominative/accusative plural assan; genitive plural assena, dative plural assum. Do not use a strong ass or genitive plural assa.')
noun('hunig','hunig','n','47','hunig','honey','44.8','U18-EX-P29',number='sg',diagnostic='The first syllable is short; retain hunig- under43.4/47.6. Honey is the selected mass singular sense.')
noun('aecern','æcern','n','47','æcern','acorn','44.8','U18-EX-P29 U18-BT-P9 U18-CRAWFORD1922-P190',overrides={4:'æcernu',7:'æcernu'},diagnostic='Preserve Cook’s unmarked æcern; do not infer a macron. BT9 gives æcern/æcirn es;n. and an attested -u plural in Genesis43.11. Crawford1922 p190 apparatus43.11 explicitly prints O. æcernu, corroborating the exact selected plural spelling, while the main text has æcyrnu. Retain æcern- in oblique forms; the final rn makes the second syllable heavy.')
noun('hwaete','hwǣte','m','44','hwǣt','wheat','45.7 46.7 46.8','U18-EX-P30',number='sg')
noun('laefel','læfel','m','43','læfel','cup','46.8 47.1 47.5 47.8','U18-EX-P31',diagnostic='First syllable short: retain læfel- in all ending-bearing forms under43.4. Preserve Cook’s unmarked æ; neither lāfel nor lǣfel is silently substituted.')
noun('sceawere','scēawere','m','44.1','scēawer','spy','47.11','U18-EX-P32',diagnostic='The hint gives scēawere44. The -ere noun loses dictionary e before endings: scēaweres, scēaweras, scēawera, scēawerum.')
noun('elcung','ęlcung','f','51.3','ęlcung','delay','44.7','U18-EX-P44 U18-EX-P58',number='sg',diagnostic='Select ordinary -e oblique singular;51.3 also records -a variants for -ung nouns. No new plural delay sense is assigned.')
noun('gebeorscipe','gebēorscipe','m','44.1','gebēorscip','feast; banquet','45.4 FB176.14','U18-EX-P47 U18-FB-P290')
noun('sarnes','sārnes','f','51.5','sārness','grief','48.3','U18-EX-P49 U18-EX-P66',number='sg',diagnostic='Double final s and retain preceding e in every oblique form: sārnesse, not sārnese or sārnse;51.5.')
noun('ealdor-chief','ealdor','m','43.4a','ealdr','chief; ruler','44.2','U18-EX-P42',diagnostic='Heavy first syllable and light second syllable: ealdor but ealdres/ealdre/ealdras. The earlier component citation did not teach this full noun system.',sid='ealdor-chief-u14-component-source')
noun('thearf','ðearf','f','51.b','ðearf','benefit; good','48.6','U18-EX-P40 U18-EX-P58',number='sg',sid='thearf-u15-source-sense')
noun('theow-servant','ðēow','m','43','ðēow','servant; enslaved person','46.5 47.4 47.8 48.2','U18-EX-P31 U18-BT-P1053',diagnostic='Distinct strong masculine noun þeów es;m. in BT1053. Normalize BT thorn/acute to course eth/macron, corroborated by Cook’s ðēow hint. The selected strong-noun genitive plural is ðēowa. Distinguish the earlier weak-noun selected genitive ðēowena and the regular adjective-table genitive ðēowra; this comparison does not exhaust historical variants or uniquely determine the reading phrase’s category.')
noun('hunger','hunger','m','43.4a','hungr','famine; hunger','48.7','U18-EX-P47 U18-EX-P63',number='sg',diagnostic='The selected Cook glossary headword is hunger, not hungor.43.4a licenses hungres/hungre with syncope; retain hunger in nominative/accusative singular.')
noun('sith','sīð','m','43','sīð','time; occasion','44.7','U18-EX-P29 U18-FB-P312 U18-FB-P99 U18-CRAWFORD1922-P190',diagnostic='The hint sīð176 supplies a lemma and points to the adverbial instrumental. Supply the entire ōðre sīðe phrase: adjective and noun instrumental masculine singular in an adverbial number-of-times expression. The instrumental noun occurrence has its own supplied identity and is not relabeled from the dative table cell. It is not ordinary accusative ōðre sīð, and no independent instrumental production is licensed. The noun is distinct from the earlier compound sīðfæt.')
noun('lac','lāc','n','47','lāc','gift; present','44.8 45.3 46.3','U18-EX-P49 U18-EX-P58',diagnostic='Long ā gives the heavy neuter endingless nominative/accusative plural lāc.')
noun('faet','fæt','n','47-short','fæt','vessel; container','44.8','U18-EX-P51 U18-EX-P66',overrides={4:'fatu',5:'fata',6:'fatum',7:'fatu'},diagnostic='Cook47.4: keep æ in the singular; use a throughout the plural before back-vowel endings: fatu/fata/fatum/fatu. The prior compound sīðfæt supplies neither this neuter identity nor this container sense.')
noun('weorth-price','weorð','n','47','weorð','price; value','46.8','U18-EX-P31',number='sg')
noun('feoh','feoh','n','47.5','fēo','money','45.3 45.8 45.9 46.1 46.7 46.8 47.2','U18-EX-P30 U18-FB-P33 U18-FB-P29',number='sg',overrides={1:'fēos',2:'fēo'},diagnostic='Cook47.5 prints unmarked feoh, genitive fēos, and refers to43.3 for h-loss before endings. Select contracted fēo in the dative. Preserve unmarked feoh before final h and the printed long vowel after loss; do not silently regularize to fēoh. Absence of a printed macron is not a claim that the historical vowel was short or that independently evidenced fēoh is invalid. This is the mass money sense of the already taught neuter and h-loss patterns, not a new class with an omitted plural.')

def adjective(lid,head,stem,kind,gloss,items,ev,sid=None):
 pid='NEW-U18-ADJ-'+lid.upper();refs=ev.split()+['U18-FB-P38','U18-FB-P39','U18-FB-P40','U18-FB-P41']
 scope='Complete strong and weak positive adjective: all three genders, singular and plural, nominative/genitive/dative/accusative. Masculine and neuter strong instrumental singular are separately recognition only; displaying them grants no new instrumental construction.'
 cs=[]
 def inflect(end):
  base=('āgn' if lid=='agen' and end and end[0] in 'aeou' else stem)
  return base+end if end else head
 for st in ['strong','weak']:
  for num in ['sg','pl']:
   for gen in ['m','n','f']:
    u=kind in ['e','polysyllable','syncope']
    if st=='weak':es=([('a' if gen=='m' else 'e'),'an','an',('e' if gen=='n' else 'an')] if num=='sg' else ['an','ra','um','an'])
    elif num=='pl':es=[{'m':'e','n':'u' if u else '', 'f':'a'}[gen],'ra','um',{'m':'e','n':'u' if u else '','f':'a'}[gen]]
    elif gen=='m':es=['','es','um','ne']
    elif gen=='n':es=['','es','um','']
    else:es=['u' if u else '', 're','re','e']
    for case,end in zip(CASES,es):cs.append(cell(lid,inflect(end),dict(case=case,number=num,gender=gen,strength=st),pid,refs,scope))
 for gen in ['m','n']:cs.append(cell(lid,inflect('e'),dict(case='ins',number='sg',gender=gen,strength='strong'),pid,refs,scope,'new_recognition'))
 diag=('Retain dictionary -e only where no other ending is present; otherwise use the explicit stem.' if kind=='e' else 'Select syncopated āgn- before vowel-initial endings, but retain āgen- before consonantal endings: āgnes, āgnum, āgna, āgnu; āgenne, āgenre, āgenra. Cook57.3 permits syncope. Existing supplied āgnum confirms the selected stem; other cells are declared rule-derived.' if kind=='syncope' else 'Select uncontracted polysyllabic stem and ordinary -u cells under57.3; the source permits contraction but no contracted alternatives are silently inserted.' if kind=='polysyllable' else 'Heavy adjective stem under58: no -u in strong feminine nominative singular or neuter nominative/accusative plural.')
 PAR.append(dict(paradigm_id=pid,lemma_id=lid,headword=head,part_of_speech='adjective',model='Cook '+('59' if kind=='e' else '57.3' if kind in ['polysyllable','syncope'] else '58')+'; weak60',diagnostic_stem=stem,diagnostic_rule=diag,scope=scope,number_scope='both',cells=cs,evidence_refs=refs,source_items=items.split()))
 sense(lid,head,gloss,items,refs,pid,scope,sid)

adjective('scyldig','scyldig','scyldig','polysyllable','guilty; culpable','44.6 48.1','U18-EX-P29 U18-EX-P33')
adjective('twifeald','twīfeald','twīfeald','heavy','double; twofold','45.3','U18-EX-P30')
adjective('gesund','gesund','gesund','heavy','well; in good health','46.5 FB176.16 FB176.18','U18-EX-P31 U18-EX-P67')
adjective('hal','hāl','hāl','heavy','hale; healthy','46.4','U18-EX-P50',sid='hal-u18-health')
adjective('agen','āgen','āgen','syncope','own','46.7','U18-EX-P57',sid='agen-u16-sense')
adjective('claene','clǣne','clǣn','e','clean; pure; blameless','47.4','U18-EX-P32',sid='claene-u18-blameless')
adjective('eltheodig','ęlðēodig','ęlðēodig','polysyllable','foreign','48.4','U18-EX-P48',sid='eltheodig-u18-foreign')
sense('glaed','glæd','gracious; favourably disposed toward someone with wið','45.2',['U18-EX-P29','U18-EX-P30'],'NEW-U18-VOC-GLAED-GRACIOUS','Reuse the actual prior complete short-stem adjective system, including æ/a alternation. This is a new contextual sense, not an inference from earlier glad.','glaed-u18-gracious')

rules=[dict(rule_id='U18-NOM-RULE-SCOPE',text='Every class is already taught. New count nouns receive eight complete literal cells; selected mass/abstract nouns receive all four singular cells with their plural explicitly outside the assigned sense. No isolated needed case substitutes for a stated system.'),dict(rule_id='U18-NOM-RULE-EVIDENCE',text='Headword spelling and class evidence are source-specific. Complete tables are declared rule-derived; OCR, headword familiarity and prior display do not certify individual forms or senses.'),dict(rule_id='U18-NOM-RULE-PRIOR',text='Read actual prior entries before promotion. Preserve source-analysis strings and historical metadata separately; clǣnum records are matched using their explicit original gender description, and Hāl differs only in capitalization. The current cell analysis does not overwrite prior chapter history.'),dict(rule_id='U18-NOM-RULE-DISTINCT',text='Keep strong noun theow-servant, adjective theow and weak noun theowa as distinct identities; also keep ealdor-chief separate from life, and weorth-price separate from verbs or adjective senses.'),dict(rule_id='U18-NOM-RULE-READING',text='The exact source reading retains ðēowa manna and ðēowum mannum. Its whole expression is supplied with a bounded analysis; these noun tables do not automatically grant the construction.'),dict(rule_id='U18-NOM-RULE-ALTERNATIVES',text='Selected stem and endings define the displayed course table. Cook-recognized -ung oblique -a, feminine plural -e, adjective contractions and other independently evidenced variants are not errors solely because a different variant was selected; they do not count as independently taught unless explicitly recorded.')]
assert len({p['lemma_id'] for p in PAR})==len(PAR)
assert all(len(p['cells'])==(50 if p['part_of_speech']=='adjective' else 8 if p['number_scope']=='both' else 4) for p in PAR)
dump('noun-adjective-paradigms.json',dict(schema_version=1,status='proposed complete nominal systems; primary images checked; coordinator contract required',paradigms=PAR,counts=dict(paradigms=len(PAR),cells=sum(len(p['cells']) for p in PAR),nouns=sum(p['part_of_speech']=='noun' for p in PAR),adjectives=sum(p['part_of_speech']=='adjective' for p in PAR)),rules=rules))
dump('nominal-sense-audit.json',dict(schema_version=1,status='proposed exact nominal senses, checked against actual active register',senses=SENSE,count=len(SENSE)))
print(json.dumps({'paradigms':len(PAR),'cells':sum(len(p['cells']) for p in PAR),'senses':len(SENSE)}))
