"""Author audit: literal bounded systems; does not write active registers."""
import json,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parent
L={x['lemma_id']:x for x in json.loads((ROOT/'lexicon/entries.json').read_text(encoding='utf8'))['lemmas']}
systems=[]
def norm(a):
 if not isinstance(a,dict):return {}
 d=copy.deepcopy(a)
 for k in ['use','function','citation_notation']:d.pop(k,None)
 if d.get('number') in ['singular','plural']:d['number']={'singular':'sg','plural':'pl'}[d['number']]
 return d
def cell(lemma,surface,analysis,suffix,status='new_production'):
 matches=[f for f in L.get(lemma,{}).get('forms',[]) if f['form']==surface and norm(f['analysis'])==norm(analysis)]
 prior=next((f for f in matches if f.get('production_taught_in')),matches[0] if matches else None)
 return {'lemma_id':lemma,'form_id':prior['form_id'] if prior else f'{lemma}-u17-{suffix}','form':surface,'analysis':analysis,'knowledge_status':'previously_taught' if prior and prior.get('production_taught_in') else status,'prior_record':copy.deepcopy(prior),'proposed_teaching_id':f'NEW-U17-VERB-{lemma.upper()}'}
def system(lemma,head,kind,pres=None,pret=None,imp=None,subj=None,parts=None,pp=None,evidence=None,rules=None,sense=None,items=None,subj_tense='present',infs=None):
 s={'system_id':f'u17-{lemma}-{kind}','lemma_id':lemma,'headword':head,'scope':kind,'origin_category':'new teaching material derived from specified source rules','evidence_refs':evidence or [],'derivation_rules':rules or [],'cells':[],'prior_senses':copy.deepcopy(L.get(lemma,{}).get('senses',[])),'source_items':items or []}
 if sense:s['sense_proposal']={'sense_id':f'{lemma}-u17-selected','gloss':sense,'knowledge_status':'new_production','scope':'Only the elementary uses and explicitly described frames in this audit.'}
 for tense,vals in [('present',pres),('preterite',pret)]:
  if vals:
   assert len(vals)==6
   for i,v in enumerate(vals):
    p=i%3+1;n='sg' if i<3 else 'pl'
    s['cells'].append(cell(lemma,v,{'tense':tense,'mood':'indicative','person':p,'number':n},f'{"pres" if tense=="present" else "pret"}-{p}-{n}'))
 if imp:
  for n,v in zip(['sg','pl'],imp):s['cells'].append(cell(lemma,v,{'mood':'imperative','person':2,'number':n},f'imp-2-{n}'))
 if subj:
  for n,v in zip(['sg','pl'],subj):
   for p in [1,2,3]:s['cells'].append(cell(lemma,v,{'tense':subj_tense,'mood':'subjunctive','person':p,'number':n},f'{subj_tense}-subj-{p}-{n}'))
 if infs:
  for typ,v in zip(['plain','inflected'],infs):s['cells'].append(cell(lemma,v,{'verb_form':typ+'_infinitive'},f'{typ}-infinitive'))
 if parts:
  for tense,v in zip(['present','past'],parts):s['cells'].append(cell(lemma,v,{'verb_form':'participle','tense':tense,'agreement':'base'},f'{tense}-participle'))
 s['citation_reference']={'infinitive':head,'past_participle':pp,'status':'supplied_reference','limitation':'Citation positions are visible reference only unless a separate literal productive cell or exact task support assigns their use.'}
 s['productive_cell_count']=sum(c['knowledge_status']=='new_production' for c in s['cells']);s['display_cell_count']=len(s['cells'])
 systems.append(s);return s
def ind(a,b,c,d,e,f,g,h):return [a,b,c,d,d,d],[e,f,g,h,h,h]
def weak2(lemma,head,gloss,items,extra=None):
 stem=head[:-3];pr,pt=ind(stem+'ie',stem+'ast',stem+'að',stem+'iað',stem+'ode',stem+'odest',stem+'ode',stem+'odon')
 return system(lemma,head,'indicative12',pr,pt,pp=stem+'od',sense=gloss,items=items,evidence=['U17G-FB73','U17G-EX-PROMPTS'],rules=['Cook§118: present -ie/-ast/-að/-iað; preterite -ode/-odest/-odon; no indicative2/3sg i.',*(extra or [])])
def supplied_ref(lemma,head,form,analysis,scope,ev,items):
 return {'lemma_id':lemma,'headword':head,'form_id':f'{lemma}-u17-reference','form':form,'analysis':analysis,'knowledge_status':'supplied','support_scope':scope,'evidence_refs':ev,'source_items':items}
# Each finite indicative has all three persons in both numbers and both tenses.
pr,pt=ind('hęrie','hęrest','hęreð','hęriað','hęrede','hęredest','hęrede','hęredon')
system('herian','hęrian','indicative12-imperative2-present-subjunctive6',pr,pt,imp=['hęre','hęriað'],subj=['hęrie','hęrien'],pp='hęred',sense='praise',items=['37.1–5','37.7','37.13','FB174.10–13','FB175.14'],evidence=['U17G-FB71','U17G-FB72','U17G-EX58','U17G-FB174','U17G-FB175'],rules=['Cook§116 explicitly includes hęrian with nęrian. Keep present1sg/subjunctive hęrie, plural subjunctive hęrien; imperative singular hęre.','Retain -i- in present plural indicative/imperative hęriað, but not pret hęrede.'])
pr,pt=ind('gecweðe','gecwist','gecwið','gecweðað','gecwæð','gecwǣde','gecwæð','gecwǣdon')
system('gecwethan','gecweðan','indicative12',pr,pt,pp='gecweden',sense='speak; say',items=['37.5'],evidence=['U17G-FB63','U17G-FB64','U17G-FB190','U17G-EX-PROMPTS'],rules=['Cook§106 cweðan: present i in2/3sg; preterite singular æ versus2sg/plural ǣ; grammatical ð/d alternation. Prefix ge- belongs to the specified lexeme.'])
pr,pt=ind('ūpāhębbe','ūpāhęfst','ūpāhęfð','ūpāhębbað','ūpāhōf','ūpāhōfe','ūpāhōf','ūpāhōfon')
system('up-ahebban','ūpāhębban','indicative12-participle-pair2',pr,pt,parts=['ūpāhębbende','ūpāhafen'],pp='ūpāhafen',sense='raise; exalt',items=['37.13–14','40.6'],evidence=['U17G-FB65','U17G-EX-PROMPTS'],rules=['Cook§107 hębban: geminated present, hęfst/hęfð, preterite hōf, past participle hafen. Prefix ūpā- retained.','Exaltation sense is explicitly taught separately from physical raising; horn image remains source-local supported.'])
pr,pt=ind('oferwyrce','oferwyrcst','oferwyrcð','oferwyrceað','oferworhte','oferworhtest','oferworhte','oferworhton')
system('oferwyrcean','oferwyrcean','indicative12',pr,pt,pp='oferworht',sense='overlay; cover with a worked covering',items=['38.1'],evidence=['U17G-FB69','U17G-FB70','U17G-EX-PROMPTS'],rules=['Cook§114 wyrcean/worhte; select the -ean spelling already productive for wyrcean, with present plural -eað. Prefix ofer- remains in every cell.','Accusative covered thing + mid/dative material, directly specified by38.1.'])
pr,pt=ind('gesętte','gesętst','gesętt','gesęttað','gesętte','gesęttest','gesętte','gesętton')
system('gesettan','gesęttan','indicative12',pr,pt,pp='gesętt',sense='set; place; establish',items=['39.1'],evidence=['U17G-FB68','U17G-FB69','U17G-EX-PROMPTS'],rules=['Cook§113 sęttan retains tt before vowels; selected indicative2sg sętst and3sg sętt. Dental preterite merges with final stem t; no *gesęttde.'])
pr,pt=ind('gierne','giernst','giernð','giernað','giernde','gierndest','giernde','gierndon')
system('giernan','giernan','indicative12',pr,pt,pp='gierned',sense='desire; request; ask for; seek in marriage',items=['39.3','43.14'],evidence=['U17G-FB68','U17G-FB296','U17G-BT495','U17G-EX68'],rules=['Cook113 long syllable weakI: selected syncopated present -st/-ð and past -de.','Genitive thing/person desired; æt +dative person from whom asked. Wooing sense independently attested FB296 and Ex68, not inferred from desire alone.'])
weak2('maersian','mǣrsian','make great; magnify; glorify',['39.4','40.2'])
system('maersian','mǣrsian','participle-pair2',parts=['mǣrsiende','mǣrsod'],pp='mǣrsod',evidence=['U17G-FB73','U17G-EX-PROMPTS'],rules=['Cook118 present -iende, past -od. Passive mǣrsod in39.4 describes being celebrated/exalted above kings.'])
weak2('gewilnian','gewilnian','desire; wish',['39.4','43.11'])
weak2('thurhwunian','ðurhwunian','remain; endure; last',['39.6'])
pr,pt=ind('wiðstande','wiðstęntst','wiðstęnt','wiðstandað','wiðstōd','wiðstōde','wiðstōd','wiðstōdon')
system('withstandan','wiðstandan','indicative12',pr,pt,pp='wiðstanden',sense='withstand; resist',items=['39.6'],evidence=['U17G-FB65','U17G-FB95','U17G-EX68'],rules=['Cook107 standan: present2/3 stęntst/stęnt, past stōd/stōdon; stem n absent from past. Dative opposed thing as164m and39.6.'])
weak2('gearcian','gearcian','prepare',['39.7'],['Use unprefixed gearcian specified in39.7; do not silently replace with gegearcian. Accusative prepared things and dative beneficiaries.'])
pr,pt=ind('āfylle','āfylst','āfylð','āfyllað','āfylde','āfyldest','āfylde','āfyldon')
system('afyllan','āfyllan','indicative12-participle-pair2',pr,pt,parts=['āfyllende','āfylled'],pp='āfylled',sense='fill',items=['40.1','40.7'],evidence=['U17G-FB68','U17G-FB69','U17G-EX-PROMPTS'],rules=['Cook113 fyllan: double ll before vowel, single l in fylst/fylð and fylde; past participle fylled (contracted fyld is a source-recognized alternative).','Accusative filled entity + mid/dative contents. Ordinary passive āfylled wǣre in reported speech.'])
pr,pt=ind('āweorpe','āwierpst','āwierpð','āweorpað','āwearp','āwurpe','āwearp','āwurpon')
system('aweorpan','āweorpan','indicative12',pr,pt,pp='āworpen',sense='cast down; cast away',items=['40.6'],evidence=['U17G-FB61','U17G-FB62','U17G-EX42'],rules=['Cook104 weorpan: eo/ea/u/o, present2/3 ie; past2sg uses plural u stem. Accusative displaced persons; of/dative source.'])
pr,pt=ind('āwrīte','āwrītst','āwrītt','āwrītað','āwrāt','āwrite','āwrāt','āwriton')
system('awritan','āwrītan','indicative12',pr,pt,pp='āwriten',sense='write',items=['41.12'],evidence=['U17G-FB59','U17G-EX68'],rules=['Cook102 ī/ā/i/i; present2sg -tst,3sg selected -tt (single-t source variant also permitted); no vowel mutation in present2/3sg.'])
pr,pt=ind('ālūte','ālȳtst','ālȳtt','ālūtað','ālēat','ālute','ālēat','āluton')
system('alutan','ālūtan','indicative12',pr,pt,pp='āloten',sense='bow; incline oneself',items=['42.5'],evidence=['U17G-FB60','U17G-FB61','U17G-EX-PROMPTS'],rules=['Cook103 ū/ēa/u/o; present2/3 ū→ȳ; t stem gives -tst/-tt (single-t3sg is a documented variant).','Intransitive actor bows, with dative Gode. Not the transitive knee-bending verb of42.8.'])
pr,pt=ind('winde','wintst','wint','windað','wand','wunde','wand','wundon')
system('windan','windan','indicative12',pr,pt,pp='wunden',sense='wind; plait',items=['42.8'],evidence=['U17G-FB61','U17G-FB62','U17G-EX-PROMPTS'],rules=['Cook104 -ind- follows bindan: i/a/u/u, d→t before -st/-ð. Accusative thing plaited; of/dative material.'])
pr,pt=ind('spǣte','spǣtst','spǣtt','spǣtað','spǣtte','spǣttest','spǣtte','spǣtton')
system('spaetan','spǣtan','indicative12',pr,pt,pp='spǣt',sense='spit',items=['42.9'],evidence=['U17G-FB68','U17G-FB69','U17G-EX-PROMPTS'],rules=['Cook113 t-stem weakI: preterite -tte/-ttest/-tton; retain the explicitly marked ǣ. Present3sg selected -tt; no *spǣtð.','On+accusative marks the person spat upon, as the prompt172 directs.'])
pr,pt=ind('tǣle','tǣlst','tǣlð','tǣlað','tǣlde','tǣldest','tǣlde','tǣldon')
system('taelan','tǣlan','indicative12',pr,pt,pp='tǣled',sense='blame; censure',items=['43.6','FB174.13'],evidence=['U17G-FB68','U17G-FB69','U17G-EX42','U17G-FB174'],rules=['Cook113 long-stem weakI, past -de. Accusative person blamed. Source tǣlst is indicative2sg.'])
pr,pt=ind('bīege','bīegst','bīegð','bīegað','bīegde','bīegdest','bīegde','bīegdon')
system('biegan','bīegan','indicative12',pr,pt,pp='bīeged',sense='bend',items=['42.8'],evidence=['U17G-FB68','U17G-FB69','U17G-EX-PROMPTS'],rules=['Regular weakI selected bīeg- long-diphthong spelling; earlier exact source biegde remains separately recorded with its original unmarked quantity.','Transitive accusative knee is bent. Do not substitute intransitive būgan as though it had the same frame.'])
pr,pt=ind('geman','gemanst','geman','gemunon','gemunde','gemundest','gemunde','gemundon')
system('gemunan','gemunan','indicative12',pr,pt,pp='gemunen',sense='remember',items=['40.8'],evidence=['U17G-FB78','U17G-EX59'],rules=['Cook134 munan with lexical ge- as explicitly listed under remember Ex59: present1/3 man,2manst,plural munon; dental past munde.','Accusative thing remembered. No future/volitional meaning is transferred from unprefixed munan.'])
pr,pt=ind('ðęnce','ðęncst','ðęncð','ðęnceað','ðōhte','ðōhtest','ðōhte','ðōhton')
system('thencan','ðęncean','indicative12',pr,pt,pp='ðōht',sense='think',items=['38.4'],evidence=['U17G-FB69','U17G-FB70'],rules=['Cook114 þenc(e)an gives þōhte/þōht: c disappears before h+dental past; present uses the selected -ean variant. Prior lemma spelling ðęncan is preserved as its canonical identity; ðęncean is a declared source-listed headword variant.','Free-choice swā hwæt swā is object of thinking; on/dative heart is figurative location supplied by38.4.'])
# Bounded extensions do not reassign entire finite systems.
for lemma,head,parts,ev in [
 ('bletsian','blētsian',['blētsiende','blētsod'],['U17G-FB73','U17G-EX41']),
 ('ofwundrian','ofwundrian',['ofwundriende','ofwundrod'],['U17G-FB73','U17G-EX-PROMPTS']),
 ('wyrcean','wyrcean',['wyrcende','worht'],['U17G-FB70','U17G-FB190']),
 ('gesweotolian','gesweotolian',['gesweotoliende','gesweotolod'],['U17G-FB73','U17G-EX54']),
 ('acennan','ācęnnan',['ācęnnende','ācęnned'],['U17G-FB68','U17G-EX-PROMPTS']),
 ('geopenian','geopenian',['geopeniende','geopenod'],['U17G-FB73','U17G-EX-PROMPTS'])]:
 system(lemma,head,'participle-pair2',parts=parts,pp=parts[1],evidence=ev,rules=['Complete present/past formation pair only. The selected tasks use the past participle in the already bounded passive construction; no additional finite mood or new active lexical frame follows from this display.'])
for lemma,head,imp,ev in [('cnucian','cnucian',['cnuca','cnuciað'],['U17G-FB73','U17G-EX-PROMPTS']),('ahebban','āhębban',['āhęfe','āhębbað'],['U17G-FB65']),('plegian','plegian',['plega','plegiað'],['U17G-FB73']),('ceosan','cēosan',['cēos','cēosað'],['U17G-FB60','U17G-FB56'])]:
 system(lemma,head,'imperative2',imp=imp,evidence=ev,rules=['Complete singular/plural command pair; no other finite system assigned here. Keep strong j-present singular āhęfe and weakII singular -a distinct.'])
for lemma,head,subj,ev in [('tocuman','tōcuman',['tōcume','tōcumen'],['U17G-FB63','U17G-FB56','U17G-EX-PROMPTS']),('geweorthan','geweorðan',['geweorðe','geweorðen'],['U17G-FB62','U17G-FB56','U17G-EX-PROMPTS']),('leornian','leornian',['leornie','leornien'],['U17G-FB73']),('ahyldan','āhyldan',['āhylde','āhylden'],['U17G-FB72','U17G-EX-PROMPTS'])]:
 system(lemma,head,'present-subjunctive6',subj=subj,evidence=ev,rules=['All three persons singular and plural; singular -e/plural -en on the present stem. No preterite subjunctive or indicative extension follows from this display.'])
# Fully defined attributive declension, independently source checked against61+59/60.
pattern=[f for f in L['bindan']['forms'] if isinstance(f['analysis'],dict) and f['analysis'].get('nonfinite')=='present_participle' and f['analysis'].get('declension') in ['strong','weak']]
assert len(pattern)==48
for lemma,head,base in [('ondraedan','ondrǣdan','ondrǣdende'),('hyngran','hyngran','hyngrende')]:
 s={'system_id':f'u17-{lemma}-present-participle-agreement48','lemma_id':lemma,'headword':head,'scope':'present-participle full NGDA strong/weak, all three genders, singular/plural','origin_category':'new teaching material derived from specified source rules','evidence_refs':['U17G-FB38','U17G-FB39','U17G-FB40','U17G-FB41','U17G-FB71','U17G-FB100'],'derivation_rules':['Cook61: present participles follow59 grēne; weak follows60. Remove final-e before overt endings.','Select strong feminine singular -u, neuter plural -u, feminine plural -a; source -e alternatives are recognized, not unmarked required substitutions.','Nominalized human use in40.5/7 is productive; assigning the full morphology does not teach unrelated nonhuman nominal senses.','Hyngrende is a participle; no complete personal finite hyngran system is inferred from this nominalization.'],'cells':[]}
 for f in pattern:
  surface=f['form'].replace('bindend',base[:-1]);a=copy.deepcopy(f['analysis']);a['use']='adjectival agreement; human nominalization separately taught'
  s['cells'].append(cell(lemma,surface,a,f['form_id'].removeprefix('bindan-')))
 s['display_cell_count']=48;s['productive_cell_count']=48;systems.append(s)
system('geseon','gesēon','preterite-subjunctive6',subj=['gesāwe','gesāwen'],subj_tense='preterite',evidence=['U17G-FB55','U17G-FB64'],rules=['Cook95 uses plural preterite stem in both numbers of the past subjunctive;106 explicitly gives sāwon for sēon, hence prefixed gesāwe/gesāwen. Present subjunctive is not additionally assigned.'],items=['38.8','39.4'])
for lemma,head,forms in [('settan','sęttan',['sętte','sętten']),('etan','etan',['ete','eten'])]:
 system(lemma,head,'present-subjunctive6',subj=forms,evidence=['U17G-FB55','U17G-FB64','U17G-FB72'],rules=['Complete singular/plural present subjunctive for all3persons; no indicative2/3sg mutation. Only this tense is newly assigned.'])
system('forgiefan','forgiefan','imperative2',imp=['forgief','forgiefað'],evidence=['U17G-FB55','U17G-FB64','U17G-EX-PROMPTS'],rules=['Complete two-person command-number pair. Prior give and forgive senses remain separate;41.8 uses forgiveness.'])
for lemma,head,forms in [('geseon','gesēon',['gesēon','gesēonne']),('geliefan','gelīefan',['gelīefan','gelīefanne']),('leornian','leornian',['leornian','leornianne'])]:
 system(lemma,head,'infinitive-pair2',infs=forms,evidence=['U17G-FB55','U17G-FB106'],rules=['Plain and inflected infinitive pair. Select prior course -anne series, including -ianne; contracted -on gives -onne. Alternative -enne remains a documented form, not the selected recall target.','Independent task use here is ordinary modal infinitive; displaying the inflected form does not add new purpose or gerund syntax.'])
system('gescieppan','gescieppan','participle-pair2',parts=['gescieppende','gesceapen'],pp='gesceapen',evidence=['U17G-FB65','U17G-FB190'],rules=['Cook107 scieppan/sceōp/sceōpon/sceapen, with the specified lexical ge-. Present -ende attaches to the present stem; past participle uses ea and single p. Earlier citation alone did not assign productive past participle.'],items=['37.5'])
for lemma,head,base,plural in [('wyrcean','wyrcean','worht','worhte'),('gescieppan','gescieppan','gesceapen','gesceapene')]:
 s={'system_id':f'u17-{lemma}-past-predicate2','lemma_id':lemma,'headword':head,'scope':'selected singular/base and plural-e predicate realization','origin_category':'new teaching material derived from specified source rules','evidence_refs':['U17G-FB41','U17G-FB190'],'derivation_rules':['Display the uninflected base selected for singular and the inflected-e plural used37.5. Uninflected bases are also permissible for plural predicates under62; this is a selected teaching realization, not an exclusion of that valid alternative.'],'cells':[cell(lemma,base,{'verb_form':'participle','tense':'past','agreement':'base'},'past-participle'),cell(lemma,plural,{'verb_form':'past_participle','agreement':'predicate_plural_strong_masculine_like','number':'plural'},'past-participle-predicate-plural')],'display_cell_count':2,'productive_cell_count':2}
 systems.append(s)
for s in systems:
 if 'U17G-FB56'in s['evidence_refs']and'U17G-FB55'not in s['evidence_refs']:s['evidence_refs'].append('U17G-FB55')
 if s['lemma_id']=='biegan':s['evidence_refs'].append('U17G-EX40')
refs=[supplied_ref('asmean','āsmēan','āsmēan',{'verb_form':'plain_infinitive'},'The exact dictionary form is printed in39.7. It is a visible lexical reference under mæg, not an independent-recall finite system.',['U17G-EX-PROMPTS'],['39.7']),supplied_ref('geriman','gerīman','gerīman',{'verb_form':'plain_infinitive'},'Exact printed reference in42.3, within supplied dense whole clause. No complete new finite system assigned.',['U17G-EX-PROMPTS'],['42.3'])]
result={'schema_version':1,'status':'precontract proposal; no active register mutation','access':'author-only morphology and dependency audit','baseline':'defa800','systems':systems,'reference_only':refs,'counts':{'systems':len(systems),'display_cells':sum(len(s['cells'])for s in systems),'new_production_cell_appearances':sum(s['productive_cell_count']for s in systems),'unique_form_ids':len({c['form_id']for s in systems for c in s['cells']})}}
(OUT/'verbal-systems.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(result['counts'])
