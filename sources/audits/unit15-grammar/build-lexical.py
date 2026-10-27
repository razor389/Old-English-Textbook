"""Literal complete narrowly defined U15 lexical systems, plus governed frames."""
import pathlib
O=pathlib.Path(__file__).resolve().parent
exec((O/'build-records.py').read_text(encoding='utf-8').split('# Complete core')[0])
D['status']='audited_proposal_ready_for_contract'
D['principal_parts']=[]
def pair(i,h,tag,forms,ev,ruleid,scope):
 cs=[]
 for fid,surf,a in forms:
  old=next((f for f in L.get(i,{}).get('forms',[]) if f['form_id']==fid),None)
  cs.append(cell(i,h,fid,surf,old['analysis'] if old else a,ev,prior=old))
 return system(i,h,tag,cs,ruleid,scope,ev)
def imp(i,h,sg,pl,ev,ruleid):
 return pair(i,h,'IMP',[(i+'-imp-2-sg',sg,{'mood':'imperative','person':2,'number':'singular'}),(i+'-imp-2-pl',pl,{'mood':'imperative','person':2,'number':'plural'})],ev,ruleid,'Complete second-person singular/plural command system; negative commands use ne. No other new system implied.')
def inf(i,h,plain,infl,ev,ruleid,oldplain=None,oldinfl=None):
 return pair(i,h,'INF',[(oldplain or i+'-infinitive',plain,{'verb_form':'plain_infinitive'}),(oldinfl or i+'-inflected-infinitive',infl,{'verb_form':'inflected_infinitive'})],ev,ruleid,'Complete selected plain and inflected infinitive pair. Plain after taught modal/perception/permission verb; tō+inflected for the supported purpose. No new finite system implied.')
def part(i,h,pres,past,ev,ruleid,oldpast=None):
 return pair(i,h,'PART',[(i+'-present-participle',pres,{'verb_form':'present_participle','use':'selected base form'}),(oldpast or i+'-past-participle',past,{'verb_form':'past_participle','use':'selected base form'})],ev,ruleid,'Complete present/past participial base pair; present predicative concurrence and past passive use within prior syntax. Full adjectival declension of participles is not newly assigned.')
def pp(i,parts,ev,note):
 D['principal_parts'].append({'lemma_id':i,'parts':parts,'evidence_refs':ev,'scope_note':note,'basis':'Selected lexical principal parts and the cited class rule. Citation here does not make every finite/nonfinite use productive.'})
rule('U15-R-STRONG-III','StrongIII forgieldan has present gield-, past singular geald-, plural guld-, participle gold-. Present2/3 forgieltst/forgielt continue the earlier gieldan selected t cluster. Tōweorpan has weorp-/wearp-/wurp-/worpen; its present2/3 uses umlaut wierp-. Past2singular uses the plural stem plus -e. Singular1/3past bare stem; all pastpl -on. All presentpl -að. Prefixes stay with all stems.',['U15-G-FB54','U15-G-FB55','U15-G-FB61','U15-G-FB62','U15-G-FB288','U15-G-FB316'])
rule('U15-R-STRONG-V','Ongietan follows gietan/giefan classV: ongiet-/ongeat-/ongēat-/ongieten. Present2 ongietst and3 ongiett keep selected t+t assimilation (Cook prints giet(t)); the alternative single t is valid but not the selected cell. Preterite2 uses ongēate, other singular ongeat, plural ongēaton. The infinitive and participle in the principal-parts display are reference only.',['U15-G-FB54','U15-G-FB63','U15-G-FB64','U15-G-FB308'])
rule('U15-R-STRONG-VII','Gehātan follows the prior hātan selected system with ge-: gehāte/gehǣtst/gehǣtt/gehātað; past gehēt/gehēte/gehēton. The ā→ǣ present2/3 and ēpast are both required. Onfōn keeps the contract infinitives onfōn/onfōnne; forlǣtan keeps forlǣtan/forlǣtanne. No negative or subjunctive prefixed system is inferred.',['U15-G-FB54','U15-G-FB55','U15-G-FB67','U15-G-FB292','U15-G-FB308'])
rule('U15-R-STRONG-VI-PART','Standan is classVI, not classIII: standan/stōd/stōdon/standen. Its present base standende keeps the nasal in the present stem; past standen is the selected fourth principal part. Only the participial base pair is newly promoted.',['U15-G-FB55','U15-G-FB65'])
rule('U15-R-WEAK-I','Selected long-stem weakI wēnan,lǣran,forbærnan use present -e,-st,-ð,-að and preterite -de,-dest,-de,-don. Selected participial bases lǣrende/lǣred and hǣlende/hǣled retain full -ed; the frame does not license arbitrary syncopation. Imperative singular has no ending (ætīew, ālīes); plural -að. Plain/inflected wyrcean/wyrceanne preserve earlier selected -ea- before the infinitival ending, rather than silently substituting wyrcan.',['U15-G-FB68','U15-G-FB69','U15-G-FB72','U15-G-FB275','U15-G-FB301','U15-G-FB321','U15-G-EX57'])
rule('U15-R-WEAK-II','Weak II hȳrian follows lufian: present hȳrie, hȳrast, hȳrað, hȳriað; preterite hȳrode, hȳrodest, hȳrode, hȳrodon. The long ȳ is lexical and stays throughout. Commands cleopa/cleopiað distinguish singular -a from plural -iað. The selected pair is blōstmian/blōstmianne; no finite system is assigned.',['U15-G-FB73','U15-G-FB74','U15-G-FB281','U15-G-EX15','U15-G-EX17'])

specs=[
 ('forgieldan','forgieldan',['forgielde','forgieltst','forgielt','forgieldað'],['forgeald','forgulde','forgeald','forguldon'],'U15-R-STRONG-III',['U15-G-FB61','U15-G-FB62','U15-G-FB288'],'forgieldan-u15-pay','pay; requite; recompense'),
 ('hyrian','hȳrian',['hȳrie','hȳrast','hȳrað','hȳriað'],['hȳrode','hȳrodest','hȳrode','hȳrodon'],'U15-R-WEAK-II',['U15-G-FB73','U15-G-FB74','U15-G-EX15'],'hyrian-u15-hire','hire'),
 ('wenan','wēnan',['wēne','wēnst','wēnð','wēnað'],['wēnde','wēndest','wēnde','wēndon'],'U15-R-WEAK-I',['U15-G-FB68','U15-G-FB72','U15-G-FB321'],'wenan-u15-suppose','suppose; expect; think'),
 ('toweorpan','tōweorpan',['tōweorpe','tōwierpst','tōwierpð','tōweorpað'],['tōwearp','tōwurpe','tōwearp','tōwurpon'],'U15-R-STRONG-III',['U15-G-FB61','U15-G-FB62','U15-G-FB316','U15-G-EX17'],'toweorpan-u15-break','break; overthrow, here break a commandment'),
 ('forbaernan','forbærnan',['forbærne','forbærnst','forbærnð','forbærnað'],['forbærnde','forbærndest','forbærnde','forbærndon'],'U15-R-WEAK-I',['U15-G-FB68','U15-G-FB72','U15-G-EX57','U15-G-FB161'],'forbaernan-u15-parch','parch; scorch'),
 ('laeran','lǣran',['lǣre','lǣrst','lǣrð','lǣrað'],['lǣrde','lǣrdest','lǣrde','lǣrdon'],'U15-R-WEAK-I',['U15-G-FB68','U15-G-FB72','U15-G-FB301'],'laeran-u15-teach','teach; instruct'),
 ('ongietan','ongietan',['ongiete','ongietst','ongiett','ongietað'],['ongeat','ongēate','ongeat','ongēaton'],'U15-R-STRONG-V',['U15-G-FB63','U15-G-FB64','U15-G-FB308'],'ongietan-u15-understand','understand; perceive'),
 ('gehatan','gehātan',['gehāte','gehǣtst','gehǣtt','gehātað'],['gehēt','gehēte','gehēt','gehēton'],'U15-R-STRONG-VII',['U15-G-FB67','U15-G-FB292'],'gehatan-promise','promise')]
specs.append(('deman','dēman',['dēme','dēmst','dēmð','dēmað'],['dēmde','dēmdest','dēmde','dēmdon'],'U15-R-WEAK-I',['U15-G-FB72','U15-G-FB282'],'deman-u15-judge','judge'))
for i,h,pr,pa,r,ev,sid,g in specs:
 finite(i,h,'IND',pr,pa,ev,r,'Complete12 present/preterite indicative positions. The selected sense and governed frames are separately stated; citation principal parts do not confer other moods.')
 sense(i,h,sid,g,ev)
cs=[]
for tense,base in [('present','dēme'),('preterite','dēmde')]:
 for num in ['sg','pl']:
  for person in range(1,4):
   cs.append(cell('deman','dēman',f'deman-{tense}-subj-{person}-{num}',base+('n' if num=='pl' else ''),{'tense':tense,'mood':'subjunctive','person':person,'number':'singular' if num=='sg' else 'plural'},['U15-G-FB72','U15-G-FB282']))
system('deman','dēman','SUBJ',cs,'U15-R-WEAK-I','Complete12 present/preterite subjunctive positions, used in the already taught purpose-clause syntax. Present -e/-en, preterite -de/-den.',['U15-G-FB72','U15-G-FB282','U15-G-FB104'])
sense('deman','dēman','deman-u15-condemn','condemn',['U15-G-FB282','U15-G-EX16'],scope='Accusative object; in29.7 the rejected purpose of sending, not denial of sending itself.')
pp('deman',['dēman','dēmde','dēmed'],['U15-G-FB72','U15-G-FB282'],'Reference principal parts; complete indicative and subjunctive systems are assigned.')
imp('forgieldan','forgieldan','forgield','forgieldað',['U15-G-FB55','U15-G-FB288'],'U15-R-STRONG-III')
inf('forgieldan','forgieldan','forgieldan','forgieldanne',['U15-G-FB55','U15-G-FB288'],'U15-R-STRONG-III')
part('forgieldan','forgieldan','forgieldende','forgolden',['U15-G-FB55','U15-G-FB61','U15-G-FB288'],'U15-R-STRONG-III')
part('laeran','lǣran','lǣrende','lǣred',['U15-G-FB72','U15-G-FB301'],'U15-R-WEAK-I')
part('haelan','hǣlan','hǣlende','hǣled',['U15-G-FB72','U15-G-EX16'],'U15-R-WEAK-I')
sense('haelan','hǣlan','haelan-u15-save','save',['U15-G-EX16'],scope='Only complete participial base pair; passive save in the supported purpose clause. No new finite recall required.')
imp('cleopian','cleopian','cleopa','cleopiað',['U15-G-FB73','U15-G-FB281'],'U15-R-WEAK-II')
sense('cleopian','cleopian','cleopian-u15-call','call; summon',['U15-G-FB281'],scope='Command system only; accusative summoned people.')
imp('aliesan','ālīesan','ālīes','ālīesað',['U15-G-FB72','U15-G-FB275'],'U15-R-WEAK-I')
sense('aliesan','ālīesan','aliesan-u15-deliver','deliver; release',['U15-G-FB275'],scope='Command system; person accusative, separation fram+dative.')
imp('aetiewan','ætīewan','ætīew','ætīewað',['U15-G-FB72'],'U15-R-WEAK-I')
inf('wyrcean','wyrcean','wyrcean','wyrceanne',['U15-G-FB69','U15-G-EX16','U15-G-EX17'],'U15-R-WEAK-I',oldplain='wyrcean-infinitive',oldinfl='wyrcean-inflected-infinitive')
inf('onfon','onfōn','onfōn','onfōnne',['U15-G-FB55','U15-G-FB67','U15-G-FB308'],'U15-R-STRONG-VII',oldplain='onfon-infinitive-citation')
inf('forlaetan','forlǣtan','forlǣtan','forlǣtanne',['U15-G-FB55','U15-G-FB67','U15-G-FB288'],'U15-R-STRONG-VII',oldplain='forlaetan-inf')
inf('blostmian','blōstmian','blōstmian','blōstmianne',['U15-G-FB73','U15-G-EX17'],'U15-R-WEAK-II')
sense('blostmian','blōstmian','blostmian-u15-bloom','blossom; bloom',['U15-G-EX17'],scope='Exact printed Cook spelling, infinitive pair only. No new finite forms required.')
part('standan','standan','standende','standen',['U15-G-FB55','U15-G-FB65'],'U15-R-STRONG-VI-PART',oldpast='standan-participle-citation')
part('giefan','giefan','giefende','giefen',['U15-G-FB55','U15-G-FB63'],'U15-R-STRONG-V',oldpast='giefan-participle-citation')
for i,parts,ev in [
 ('forgieldan',['forgieldan','forgeald','forguldon','forgolden'],['U15-G-FB61','U15-G-FB288']),('hyrian',['hȳrian','hȳrode','hȳrod'],['U15-G-FB73','U15-G-FB74','U15-G-EX15']),('wenan',['wēnan','wēnde','wēned'],['U15-G-FB72','U15-G-FB321']),('toweorpan',['tōweorpan','tōwearp','tōwurpon','tōworpen'],['U15-G-FB61','U15-G-FB316']),('forbaernan',['forbærnan','forbærnde','forbærned'],['U15-G-FB72','U15-G-EX57']),('laeran',['lǣran','lǣrde','lǣred'],['U15-G-FB72','U15-G-FB301']),('ongietan',['ongietan','ongeat','ongēaton','ongieten'],['U15-G-FB63','U15-G-FB64','U15-G-FB308']),('gehatan',['gehātan','gehēt','gehēton','gehāten'],['U15-G-FB67','U15-G-FB292']),('cleopian',['cleopian','cleopode','cleopod'],['U15-G-FB73','U15-G-FB74','U15-G-FB281']),('haelan',['hǣlan','hǣlde','hǣled'],['U15-G-FB72','U15-G-EX16']),('aliesan',['ālīesan','ālīesde','ālīesed'],['U15-G-FB72','U15-G-FB275']),('blostmian',['blōstmian','blōstmode','blōstmod'],['U15-G-FB73','U15-G-FB74','U15-G-EX17'])]:pp(i,parts,ev,'Reference principal-parts list. Only the separately enumerated complete systems have productive cells.')

def adj(i,h,kind,ev):
 lemma(i,h,'adjective');cs=[]
 for decl in ['strong','weak']:
  for num in ['sg','pl']:
   for gen in ['m','n','f']:
    if decl=='strong':
     en={('m','sg'):['','es','um','ne'],('n','sg'):['','es','um',''],('f','sg'):['','re','re','e'],('m','pl'):['e','ra','um','e'],('n','pl'):['','ra','um',''],('f','pl'):['a','ra','um','a']}[(gen,num)]
    else:en=['a' if gen=='m' else 'e','an','an','e' if gen=='n' else 'an'] if num=='sg' else ['an','ra','um','an']
    for ca,e in zip(['nom','gen','dat','acc'],en):
     if kind=='e':
      stem=h[:-1]
      if decl=='strong' and ((gen=='f' and num=='sg' and ca=='nom') or (gen=='n' and num=='pl' and ca in ['nom','acc'])):e='u'
      surf=stem+e if e else h
     elif kind=='ig':
      # Selected syncopated pattern, parallel to the previously productive hālig model.
      stem=h[:-2]+'g' if e and e[0] in 'aeiou' else h
      surf=stem+e
     elif kind=='double':surf=(h if not e or e[0] in 'aeiou' else h[:-1])+e
     else:surf=h+e
     a={'case':ca,'gender':gen,'number':num,'declension':decl}
     cs.append(cell(i,h,f'{i}-{ca}-{gen}-{num}-{decl}',surf,a,ev))
  use=cs[-24:]
  system(i,h,decl.upper()+'-NGDA',use,'U15-R-ADJ-'+kind.upper(),'Complete24 NGDA singular/plural positions. Positive degree only; strong/weak choice follows prior teaching. New senses are separately explicit.',ev)
 return cs
rule('U15-R-ADJ-LONG','Riht and gelīc use ordinary long-stem positive adjective NGDA endings. Zero nominative feminine singular and neuter nominative/accusative plural; strong feminine plural -a selected, masculine -e; weak genitive plural -ra. Long ī in gelīc stays.',['U15-G-FB39','U15-G-FB40','U15-G-FB41'])
rule('U15-R-ADJ-E','Mǣre is Cook§59: retain citation -e where no ending is supplied; drop it before another ending, including selected feminine nominative singular mǣru and neuter nominative/accusative plural mǣru. Strong -re/-ra with stem-final r contracts to mǣrre/mǣrra. Weak genitive plural mǣrra.',['U15-G-FB40','U15-G-FB41','U15-G-FB304'])
rule('U15-R-ADJ-IG','Mihtig follows the disyllabic -ig pattern (§57.3): the selected table syncopates i before vowel-initial endings (mihtges, mihtgum, mihtge, mihtgan); retains i before consonantal endings (mihtigne, mihtigre, mihtigra). Select mihtig for strong feminine nominative singular and neuter nominative/accusative plural, parallel to the established hālig pattern. Unsyncopated variants must not be called impossible.',['U15-G-FB39','U15-G-FB305'])
rule('U15-R-ADJ-DOUBLE','Ungeðancfull is explicitly Cook§58.2: retain final ll before vowels (ungeðancfulle, -fullum), but select one l before consonants (ungeðancfulne, -fulre, -fulra). Bare ungeðancfull keeps the lexical double consonant.',['U15-G-FB40','U15-G-EX66'])
for i,h,k,ev,sid,g in [('riht','riht','long',['U15-G-FB39','U15-G-FB40','U15-G-FB41','U15-G-EX15'],'riht-u15-right','right; just'),('gelic','gelīc','long',['U15-G-FB39','U15-G-FB40','U15-G-FB41','U15-G-FB293','U15-G-BT-GELIC'],'gelic-u15-equal','equal; like'),('mihtig','mihtig','ig',['U15-G-FB39','U15-G-FB41','U15-G-FB305'],'mihtig-u15-mighty','mighty; powerful'),('maere','mǣre','e',['U15-G-FB40','U15-G-FB41','U15-G-FB304'],'maere-u15-great','great; renowned'),('ungethancfull','ungeðancfull','double',['U15-G-FB40','U15-G-FB41','U15-G-EX66'],'ungethancfull-u15-unthankful','unthankful')]:
 adj(i,h,k,ev);sense(i,h,sid,g,ev)

# New lexical senses which reuse complete prior morphology.
for i,h,sid,g,ev,scope in [
 ('idel','īdel','idel-u15-idle','idle; not working',['U15-G-EX15'],'Same full prior strong/weak morphology; new employment-context sense.'),
 ('micel-comp','māra','micel-comp-u15-amount','more, a greater amount',['U15-G-BT-MICEL','U15-G-EX16'],'Substantive neuter māre for an amount; here accusative onfōn object. Not the invariant adverb mā.'),
 ('micel','micel','micel-u15-amount','much; an amount',['U15-G-BT-MICEL','U15-G-EX16'],'Substantive neuter micel, quantity rather than physical size.'),
 ('lytel-superl','lǣst','lytel-superl-u15-rank','least in rank or importance',['U15-G-EX17'],'Reuse full prior adjective morphology; persons and commandments.'),
 ('god-adjective','gōd','god-u15-kind','kind; benevolent',['U15-G-EX16'],'Only the taught kindness toward overt accusative group frame.'),
 ('yfel','yfel','yfel-u15-substantive','evil; evil people',['U15-G-EX16','U15-G-EX18'],'Substantival abstract neuter singular or persons masculine plural, with ordinary agreeing case.'),
 ('word','word','word-u15-speech','speech; utterance',['U15-G-EX16','U15-G-EX17'],'Speech/deed contrast and wording quotation; same prior noun morphology.'),
 ('slean','slēan','slean-u15-kill','kill',['U15-G-EX17'],'Bounded negative command; prior strike morphology reused, including selected short-vowel imperative sleah.'),
 ('gelice','gelīce','gelice-u14-source','similarly; in the same way',['U15-G-FB293','U15-G-EX15'],'Promote prior supplied adverb identity.'),
 ('eornostlice','eornostlice','eornostlice-u15-accordingly','accordingly',['U15-G-EX16'],'Discourse connective in the temporal sequence.'),
 ('thaerto-eacan','ðǣr-tō-ēacan','thaerto-eacan-u15-besides','besides; in addition',['U15-G-EX15'],'Existing exact adverbial expression, now productive in bounded coordination.')]:
 lemma(i,h,L.get(i,{}).get('part_of_speech','adverb'))
 # Resolve promotion to existing same-gloss source sense where that exact identity exists.
 if i=='gelice':sid=next((s['sense_id'] for s in L.get(i,{}).get('senses',[]) if 'similar' in s['gloss']),sid)
 if i=='eornostlice':sid=next((s['sense_id'] for s in L.get(i,{}).get('senses',[]) if 'according' in s['gloss']),sid)
 if i=='thaerto-eacan':sid=next((s['sense_id'] for s in L.get(i,{}).get('senses',[]) if 'besides' in s['gloss'] or 'addition' in s['gloss']),sid)
 sense(i,h,sid,g,ev,scope=scope)
 if i in ['gelice','eornostlice','thaerto-eacan']:
  for old in L.get(i,{}).get('forms',[]):cell(i,h,old['form_id'],old['form'],old['analysis'],ev,prior=old)

frames=[
 ('u15-onfon-payment-acc','Receive a payment','Onfōn can take an accusative material payment, as the directly attested onféngon hig syndrige penegas (Mt20.10). Teach this bounded frame for pęning and māre; the Unit14 dative-receive frame remains valid.',['U15-G-BT-ONFON']),
 ('u15-gelic-object-predicate','Make equal to','Dōn takes an accusative object and an agreeing predicate gelīc; the comparison person is dative. Direct source Þū dydest hig gelīce ūs (Mt20.12) supports hīe ūs gelīce.',['U15-G-BT-GELIC']),
 ('u15-wid-exchange','Exchange or payment with wið','Wið+dative expresses payment/return: wið his dæges weorce; wið ānum pęninge. This is distinct from the prior hostile combat use.',['U15-G-EX15','U15-G-EX16','U15-G-FB159']),
 ('u15-forgieldan-payment','Pay or requite','Forgieldan: recipient dative, paid thing accusative. A passive with retained recipient dative is locally scaffolded in28.1.',['U15-G-FB288','U15-G-FB159','U15-G-EX15']),
 ('u15-wenan-content','Suppose a proposition','Wēnan introduces a ðæt-content clause. In this past report sceolden expresses what the workers expected to receive; it is not automatically an obligation.',['U15-G-FB321','U15-G-EX16']),
 ('u15-eall-equative','Exact equality of amount','Eall can strengthen the equative: eall swā micel swā, just as much as. Micel is substantive neuter; the second recipient remains dative under the understood giving verb.',['U15-G-EX16','U15-G-BT-MICEL']),
 ('u15-ofer-kindness-rank','Ofer with persons','Two bounded accusative frames: gōd ofer persons, kind toward; nis ofer a teacher, not above in rank. In29.8 bare strong accusative plural ungeðancfulle/yfele denote unthankful/evil people; this exact personal-object use is newly taught here and is not inherited from prior bare genitive plural or article+weak adjective syntax. Neither ofer frame is a spatial crossing.',['U15-G-EX16']),
 ('u15-swerian-thurh','Swear by','Swęrian with ðurh+accusative names the oath standard. Repeated ne ðurh phrases share the initial negative command.',['U15-G-EX17']),
 ('u15-for-exchange','For in reciprocal replacement','For+dative in eye for eye/tooth for tooth expresses equivalent exchange. The first noun is nominative in the quoted formula.',['U15-G-EX17']),
 ('u15-laeran-objects','Teach people or a thing','Lǣran takes the taught people or taught matter as accusative object in these clauses. Passive teaching plus controlled infinitive remains supplied31.3.',['U15-G-FB301','U15-G-EX17']),
 ('u15-aliesan-separation','Deliver from','Ālīes takes an accusative person; fram+dative names what the person is released from. Yfele is abstract substantive neuter dative.',['U15-G-FB275','U15-G-EX18']),
 ('u15-gehatan-promise','Promise a thing to someone','Gehātan takes an accusative promised thing and dative recipient. The case-attracted free-choice recipient in31.12 is still local scaffold, not independent production.',['U15-G-FB292','U15-G-EX18'])]
for i,t,txt,ev in frames:feature(i,t,txt,ev)
# U12 already teaches gehātan promise with accusative thing/dative recipient.
D['features']=[f for f in D['features'] if f['feature_id']!='u15-gehatan-promise']
sense('don','dōn','don-u15-make','make; render, with agreeing object predicate',['U15-G-BT-GELIC','U15-G-FB97'],scope='Dōn object + predicate gelīc, with dative equality standard; not an inference from ordinary do.')
sense('for','for','for-u15-exchange','for; in exchange for, with dative',['U15-G-EX17'],scope='Reciprocal eye/tooth formula. New bounded prepositional sense, not causal for.')
for i,h,pos,sid,g,ev in [('ut','ūt','adverb','ut-u15-out','out',['U15-G-FB320']),('ymbe','ymbe','preposition','ymbe-u15-about-time','about, of approximate time, with accusative',['U15-G-FB97','U15-G-FB324','U15-G-EX15'])]:
 lemma(i,h,pos);cell(i,h,i+'-invariant',h,{'inflection':'invariant'},ev);sense(i,h,sid,g,ev)
lemma('eall','eall','adjective/adverb');cell('eall','eall','eall-u15-degree-adverb','eall',{'function':'degree_adverb','inflection':'invariant'},['U15-G-FB314','U15-G-EX16']);sense('eall','eall','eall-u15-just','just; exactly, in eall swā',['U15-G-FB314','U15-G-EX16'],scope='Bounded equative degree intensifier; not ordinary nominal agreement.')
for i,h,sid,g,ev in [('with','wið','with-u15-exchange','in exchange or return for, with dative',['U15-G-FB323','U15-G-FB159','U15-G-EX16']),('ofer','ofer','ofer-u15-rank','above in rank, with accusative',['U15-G-EX16']),('ofer','ofer','ofer-u15-toward','toward, in gōd ofer persons, with accusative',['U15-G-EX16']),('thurh','ðurh','thurh-u15-oath','by, naming an oath standard, with accusative',['U15-G-EX17'])]:
 lemma(i,h,'preposition');sense(i,h,sid,g,ev)
# Retain the exact previously supplied identities for now-productive matching cells.
for i,oldid,newid in [('laeran','laeran-pret-3-pl-u12-source','laeran-pret-3-pl'),('ongietan','ongietan-pret-3-pl-u12-source','ongietan-pret-3-pl')]:
 old=next(f for f in L[i]['forms'] if f['form_id']==oldid)
 for f in LM[i]['forms']:
  if f['form_id']==newid:
   f['form_id']=oldid; f['contextual_analysis']=f['analysis']; f['analysis']=old['analysis']; f['prior_scope']={k:old.get(k) for k in ('recognition_taught_in','production_taught_in','supplied_in')}
# Gehātan is a genuine prior Unit12 system, not a new Unit15 teaching claim.
for f in LM['gehatan']['forms']:
 f['knowledge_status']='previously_taught'
 old=next(v for v in L['gehatan']['forms'] if v['form_id']==f['form_id'])
 f['analysis']=old['analysis']
for s in LM['gehatan']['senses']:s['knowledge_status']='previously_taught'
for p in D['paradigms']:
 if p['lemma_id']=='gehatan':p['scope_note']='Review of complete previously productive Unit12 indicative system; no new milestone. New unusual recipient syntax remains separately supplied.'
D['lemmas']=list(LM.values())
(O/'grammar-records-lexical.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(len(D['lemmas']),'lemmas',len(D['paradigms']),'systems',sum(len(x['cells']) for x in D['paradigms']),'cells',len(D['features']),'frames')
