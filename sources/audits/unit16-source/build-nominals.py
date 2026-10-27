"""Image-evidenced Unit16 nominal proposals; no shared register mutation."""
import json,pathlib,hashlib
OUT=pathlib.Path(__file__).parent; ROOT=OUT.parents[2]
def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(n,d): (OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
prior={x['lemma_id']:x for x in read('lexicon/entries.json')['lemmas']}
lemmas=[]; paradigms=[]
def scope(x):
 return {k:x.get(k) for k in ['knowledge_status','production_taught_in','recognition_taught_in','supplied_in','teaching_ids','coverage_contract']}
def lemma(lid,head,pos,gloss,ev,sid=None,status='new_production',note=''):
 old=prior.get(lid); sid=sid or lid+'-u16-sense'
 old_s=next((s for s in old.get('senses',[]) if s['sense_id']==sid),None) if old else None
 l={'lemma_id':lid,'display_headword':head,'part_of_speech':pos,'source_spellings':[head], 'prior_lemma':bool(old),'forms':[], 'senses':[{'sense_id':sid,'gloss':gloss,'knowledge_status':status,'teaching_ids':['NEW-U16-VOC-'+lid.upper()],'evidence_refs':ev,'prior_scope':scope(old_s) if old_s else None,'scope_note':note}], 'scope_note':note,'evidence_refs':ev}
 lemmas.append(l);return l
def cell(l,surf,a,pid,ev,status='new_production',fid=None):
 old=prior.get(l['lemma_id'],{}); oldf=next((f for f in old.get('forms',[]) if f['form_id']==fid),None) if fid else None
 if not fid: fid=l['lemma_id']+'-'+a['case']+'-'+a['number']+(('-'+a['gender']+'-'+a['strength']) if 'strength' in a else '')
 if not oldf: oldf=next((f for f in old.get('forms',[]) if f['form_id']==fid),None)
 f={'form_id':fid,'form':surf,'analysis':oldf['analysis'] if oldf else a,'contextual_analysis':a,'knowledge_status':status,'teaching_ids':[pid],'evidence_refs':ev,'evidence_basis':'Transparent derivation from the cited image-checked headword, explicit stem, and shared paradigm rule; individual corpus attestation is not claimed.', 'prior_scope':scope(oldf) if oldf else None,'scope_note':l['scope_note']}
 l['forms'].append(f);return f
def noun(lid,head,gender,gloss,model,stem,ev,sg,pl=None,sid=None,reuse=None,note=''):
 pid='NEW-U16-NOM-'+lid.upper(); note=note or 'Complete singular/plural production of this count-noun sense by the verified familiar class; basic subject, object, possession and prepositional uses only.'
 l=lemma(lid,head,'noun',gloss,ev,sid,note=note);l['gender']=gender;l['declension_model']=model
 cells=[]
 for number,forms in [('sg',sg),('pl',pl)]:
  if forms:
   for case,s in zip(['nom','gen','dat','acc'],forms): cells.append(cell(l,s,{'case':case,'number':number,'gender':gender},pid,ev,fid=(reuse or {}).get((case,number))))
 p={'paradigm_id':pid,'lemma_id':lid,'headword':head,'model':model,'diagnostic_stem':stem,'scope':note,'cells':cells,'evidence_refs':ev,'basic_uses':['subject nominative','direct-object accusative when the verb licenses it','adnominal genitive','case selected by an already taught preposition or licensed recipient'], 'number_scope':{'sg':'production','pl':'production' if pl else 'not assigned: the selected mass/abstract/title sense supplies no count plural; familiar class morphology is available in the shared model, not asserted as a new lexical sense'}}
 paradigms.append(p);return l
def m43(lid,h,gl,ev,stem=None,sgonly=False,sid=None,reuse=None,note=''):
 st=stem or h; return noun(lid,h,'m',gl,'Cook43; prior MASC',st,ev,[h,st+'es',st+'e',h],None if sgonly else [st+'as',st+'a',st+'um',st+'as'],sid,reuse,note)
def n47(lid,h,gl,ev,st=None,plural=None):
 st=st or h; return noun(lid,h,'n',gl,'Cook47; prior strong neuter',st,ev,[h,st+'es',st+'e',h],[plural or h,st+'a',st+'um',plural or h])
def f51(lid,h,gl,ev,st=None,sgonly=False,sid=None,reuse=None,acc=None):
 st=st or h;return noun(lid,h,'f',gl,'Cook51.b /51.5; prior strong feminine',st,ev,[h,st+'e',st+'e',acc or st+'e'],None if sgonly else [st+'a',st+'a',st+'um',st+'a'],sid,reuse,'Singular production of the assigned abstract or mass sense; no count plural is claimed.' if sgonly else '')
def weakm(lid,h,gl,ev):
 st=h[:-1];return noun(lid,h,'m',gl,'Cook53; prior weak masculine',st,ev,[h,st+'an',st+'an',st+'an'],[st+'an',st+'ena',st+'um',st+'an'])
n47('furlang','furlang','furlong',['U16-EX-P18','U16-FB-P32'])
n47('nett','nętt','net',['U16-EX-P18','U16-FB-P32','U16-WRIGHT-P174','U16-WRIGHT-P175'])
f51('smyltnes','smyltnes','calm; calmness',['U16-EX-P42','U16-FB-P35','U16-FB-P36'],st='smyltness',sgonly=True)
f51('stefn','stefn','voice',['U16-EX-P66','U16-FB-P35','U16-FB-P168'],sid='stefn-u13-source',reuse={('acc','sg'):'stefn-acc-sg-u13-source'})
m43('neahgebur','nēahgebūr','neighbour',['U16-EX-P19','U16-FB-P28'])
weakm('cnapa','cnapa','boy',['U16-FB-P168','U16-EX-P20','U16-FB-P37'])
m43('thothor','ðoðor','ball',['U16-EX-P40','U16-FB-P318','U16-FB-P28','U16-FB-P29','U16-FB-P168'],note='Complete familiar strong masculine derivation. Cook168 note20 calls the word very rare; production is confined to Cook35.1–2 and the ball-reading context. Short first syllable retains the medial o before endings under43.4.d.')
weakm('gegierela','gegierela','garment; clothing',['U16-EX-P49','U16-FB-P292','U16-FB-P37'])
f51('ansien','ansīen','appearance',['U16-EX-P22','U16-FB-P35'],sgonly=True)
m43('coss','coss','kiss',['U16-EX-P22','U16-FB-P28'])
f51('sealf','sealf','ointment',['U16-EX-P22','U16-FB-P35'],sgonly=True)
m43('disc','disc','dish',['U16-EX-P22','U16-FB-P28'])
m43('ath','āð','oath',['U16-EX-P22','U16-FB-P28'])
noun('fuluhtere','fuluhtere','m','baptizer; Baptist as John’s title','Cook44.1; prior masculine -ere','fuluhter',['U16-EX-P22','U16-FB-P30'],['fuluhtere','fuluhteres','fuluhtere','fuluhtere'],None,note='Singular title use in Johannes ðæs fuluhteres. No count plural of the proper-title sense is asserted; prior44.1 model explains the forms.')
m43('tear','tēar','tear',['U16-FB-P315','U16-FB-P28'])
n47('tempel','tempel','temple',['U16-EX-P64','U16-FB-P315','U16-FB-P33'],st='templ',plural='templu')
n47('maeden','mǣden','girl; maiden',['U16-EX-P49','U16-FB-P33'],st='mǣden',plural='mǣden')
n47('wolcen','wolcen','cloud',['U16-EX-P43','U16-FB-P33'],st='wolcn',plural='wolcnu')
m43('maegenthrymm','mægenðrymm','majesty; glory',['U16-EX-P49','U16-FB-P318','U16-FB-P28'],sgonly=True,sid='maegenthrymm-source',reuse={('dat','sg'):'maegenthrymm-dat-sg-source'},note='Singular abstract glory/majesty sense promoted from suppliedch10; no count plural is asserted. Preserve existing mægenðrymme source form and analysis.')
f51('wen','wēn','expectation; chance, especially wēn is ðæt',['U16-FB-P321','U16-FB-P35'],sgonly=True,acc='wēn')
f51('spraec','sprǣc','saying; speech',['U16-EX-P21','U16-FB-P313','U16-FB-P35'])

# Complete adjectives. Prior Unit7 regular model endings; new nearu pattern is checked against Wright435–436.
def adjective(lid,h,gl,ev,kind='heavy',sid=None):
 pid='NEW-U16-ADJ-'+lid.upper();l=lemma(lid,h,'adjective',gl,ev,sid,note='Complete strong/weak positive adjective morphology; basic attributive and predicate uses. Instrumental singular is recognition only; no new advanced syntax follows from displaying its cell.')
 cells=[]
 for strength in ['strong','weak']:
  for number in ['sg','pl']:
   for gender in ['m','n','f']:
    for case in ['nom','gen','dat','acc']:
     if strength=='weak':
      ending=('a' if gender=='m' else 'e') if number=='sg' and case=='nom' else ('e' if number=='sg' and gender=='n' and case=='acc' else ('ra' if number=='pl' and case=='gen' else ('um' if number=='pl' and case=='dat' else 'an')))
     elif number=='pl': ending={'nom':{'m':'e','n':'' if kind=='heavy' else 'u','f':'a'}[gender],'acc':{'m':'e','n':'' if kind=='heavy' else 'u','f':'a'}[gender],'gen':'ra','dat':'um'}[case]
     elif gender=='f': ending={'nom':'' if kind=='heavy' else 'u','gen':'re','dat':'re','acc':'e'}[case]
     else: ending={'nom':'','gen':'es','dat':'um','acc':'ne' if gender=='m' else ''}[case]
     if kind=='u':
      if strength=='strong' and (case=='nom' and number=='sg' or gender=='n' and case in ['nom','acc']): surf=h
      elif ending in ['ne','re','ra']:surf=h[:-1]+'o'+ending
      else:surf=h[:-1]+'w'+ending
     else: surf=h+ending
     a={'case':case,'number':number,'gender':gender,'strength':strength};fid=None
     if lid=='eorthlic' and a=={'case':'nom','number':'pl','gender':'n','strength':'weak'}:fid='eorthlic-u14-source-1'
     cells.append(cell(l,surf,a,pid,ev,fid=fid))
 for gender in ['m','n']: cells.append(cell(l,(h[:-1]+'we' if kind=='u' else h+'e'),{'case':'ins','number':'sg','gender':gender,'strength':'strong'},pid,ev,'new_recognition'))
 paradigms.append({'paradigm_id':pid,'lemma_id':lid,'headword':h,'model':'Wright435–436 nearu' if kind=='u' else 'Cook57–62 regular adjective','diagnostic_stem':h[:-1]+'w-/near(o)-' if kind=='u' else h,'scope':l['scope_note'],'cells':cells,'evidence_refs':ev,'rules':['Uncontracted disyllabic stem selected for transparent regular model; Cook57.3 permits syncopation but does not make it the sole form.'] if kind=='short' else (['nearu in uninflected positions; nearw- before vowels; nearo- before consonantal ne/re/ra, as Wright’s gearu table explicitly states.'] if kind=='u' else ['Long/heavy adjective has zero feminine nominative singular and neuter nominative/accusative plural.'])})
 return l
adjective('healt','healt','halt; lame',['U16-EX-P18','U16-FB-P40','U16-FB-P41'])
adjective('gelared','gelǣred','educated; trained; skilled',['U16-EX-P20','U16-FB-P292','U16-FB-P39','U16-FB-P41'],'short')
adjective('eorthlic','eorðlic','earthly',['U16-EX-P46','U16-FB-P39','U16-FB-P41'],'short','eorthlic-u14-source')
adjective('nearu','nearu','narrow',['U16-EX-P21','U16-FB-P39','U16-WRIGHT-P215','U16-FB-P41'],'u')

ev=['U16-FB-P48','U16-EX-P20'];pid='NEW-U16-NOM-BEGEN'
l=lemma('begen','bēgen','numeral','both',ev,note='Complete plural-only both system, declined as twēgen under Cook79. No singular is meaningful; bā/bū neuter and bǣm/bām dative are source-licensed alternatives. Ordinary modifier and appositive uses, including unc bǣm/inc bǣm, are assigned.')
cells=[]
for gender in ['m','n','f']:
 for case in ['nom','gen','dat','acc']:
  surf=('bēgen' if gender=='m' else 'bā') if case in ['nom','acc'] else ('bēgra' if case=='gen' else 'bǣm')
  f=cell(l,surf,{'case':case,'number':'pl','gender':gender},pid,ev,fid='begen-'+case+'-pl-'+gender)
  f['accepted_variants']=['bū'] if gender=='n' and case in ['nom','acc'] else (['bēga'] if case=='gen' else (['bām'] if case=='dat' else []));cells.append(f)
paradigms.append({'paradigm_id':pid,'lemma_id':'begen','headword':'bēgen','model':'Cook79 as twēgen','scope':l['scope_note'],'cells':cells,'evidence_refs':ev,'singular':'Not applicable to both; no fictitious singular cells.'})

# Local support means no independent recall or whole new paradigm is claimed.
def supplied(lid,h,pos,gl,forms,ev,sid=None,note=''):
 l=lemma(lid,h,pos,gl,ev,sid,'supplied',note or 'Only the exact assigned form and contextual sense are supplied; no independent recall or wider paradigm is inferred.')
 for fid,surf,a in forms:
  f=cell(l,surf,a,'NEW-U16-SUP-'+lid.upper(),ev,'supplied',fid);f['evidence_basis']='Exact source form or explicitly declared rule-supported local supply, as distinguished in the contextual analysis.'
 return l
supplied('freo','frēo','adjective','free',[('freo-u16-pl-frige','frige',{'case':'nom','number':'pl','gender':'m','context':'Cook explicitly supplies exceptional nominative plural frige; also direct address in168.9'})],['U16-EX-P48','U16-FB-P168'],note='Exact irregular plural frige supplied in35.14 and reading168.9. No unsupported frēo plural target; no whole paradigm promoted.')
supplied('feawe','fēawe','adjective','few people',[('feawe-u16-nom-m-pl','fēawe',{'case':'nom','number':'pl','gender':'m','context':'substantive subject of sindon and antecedent of relative in35.8'})],['U16-FB-P286','U16-EX-P21'])
supplied('ele','ęle','noun','oil',[('ele-dat-pl','ęlum',{'case':'dat','number':'pl','gender':'m'})],['U16-EX-P22','U16-FB-P30'],sid='ele-1',note='Prior singular productionch09 remains prior; plural was recognitionch09. Exact plural ęlum is supplied for the prompt’s oils; no new count-oil sense or independent plural recall is claimed.')
supplied('maria-name','Maria','proper_noun','Mary',[('maria-name-u16-dat-context','Marian',{'case':'dat','number':'sg','gender':'f','context':'declared local weak-feminine adaptation allowed by Cook53.1/54, after mid; distinct from prior genitive source analysis'})],['U16-EX-P19','U16-FB-P37','U16-FB-P38'],sid='maria-name-u15-source-sense')
supplied('egypta','Egypta','proper_noun','Egyptians; country-name phrases Egypta land and of Egyptum',[('egypta-u16-gen-pl','Egypta',{'case':'gen','number':'pl','gender':'m','context':'local place expression Egypta land; country expressed as land of Egyptians'}),('egypta-u16-dat-pl','Egyptum',{'case':'dat','number':'pl','gender':'m','context':'local of Egyptum; mixed foreign-name treatment under54'})],['U16-EX-P19','U16-EX-P46','U16-FB-P284','U16-FB-P38'])
supplied('fiscnoth','fiscnoð','noun','fishing',[('fiscnoth-u16-acc-sg','fiscnoð',{'case':'acc','number':'sg','gender':'m','context':'exact source on fiscnoð; phrase supplied in33.9'})],['U16-FB-P167'])

supplied('agen','āgen','adjective','own',[('agen-u16-dat-n-sg','āgnum',{'case':'dat','number':'sg','gender':'n','strength':'strong','context':'supplied entire reward clause34.9; syncopated disyllabic adjective under57.3'})],['U16-EX-P57','U16-FB-P39'])
supplied('johannes-name','Johannes','proper_noun','John',[('johannes-name-u16-gen-context','Johannes',{'case':'gen','number':'sg','gender':'m','context':'WS Matthew14.8 Iohannes; declared initial I→J to follow Cook’s given headword'}),('johannes-name-u16-acc-context','Johannem',{'case':'acc','number':'sg','gender':'m','context':'WS Matthew14.10 Iohannem; declared initial I→J to follow Cook’s given headword'})],['U16-EX-P22','U16-FB-P38','U16-MT-P114'])
for lid,h,gl,ev in [
 ('hwanon','hwanon','whence; from where',['U16-FB-P300']),('hwider','hwider','whither; to where',['U16-EX-P67']),
 ('togaedere','tōgædere','together',['U16-FB-P316']),('geond','geond','along; through, with accusative',['U16-FB-P168']),
 ('innan','innan','within; inside',['U16-FB-P301']),
 ('siththan','siððan','since; after, as a conjunction; afterwards as an adverb',['U16-EX-P22','U16-FB-P169','U16-FB-P170']),
 ('thriwa','ðrīwa','thrice; three times',['U16-EX-P21'])]:
 l=lemma(lid,h,'preposition' if lid=='geond' else 'adverb',gl,ev)
 l['forms']=[{'form_id':lid+'-u16-invariant','form':h,'analysis':{'part_of_speech':l['part_of_speech'],'inflection':'invariant'},'knowledge_status':'new_production','teaching_ids':['NEW-U16-VOC-'+lid.upper()],'evidence_refs':ev,'evidence_basis':'Exact image-checked vocabulary or prompt hint and contextual use.','scope_note':gl}]
supplied('uppan','uppan','preposition','upon; on top of',[('uppan-u16-invariant','uppan',{'part_of_speech':'preposition','inflection':'invariant','context':'exact supplied uppan ðǣre sǣ32.2; dative under166'})],['U16-EX-P18'])
supplied('thritig','ðrītig','numeral','thirty',[('thritig-u16-invariant','ðrītig',{'part_of_speech':'numeral','inflection':'uninflected in32.2','context':'supplied quantity phrase; no complete new tens system claimed'})],['U16-EX-P18','U16-FB-P48','U16-FB-P318'])
supplied('hundnigontig','hundnigontig','numeral','ninety',[('hundnigontig-u16-invariant','hundnigontig',{'part_of_speech':'numeral','inflection':'uninflected in32.9–10','context':'supplied nigon and hundnigontig; no complete new tens system claimed'})],['U16-EX-P18','U16-EX-P19','U16-FB-P48'])
supplied('naht','nāht','noun','nothing; naught',[('naht-u16-gen-sg','nāhtes',{'case':'gen','number':'sg','gender':'n','context':'selected genitive with wēnan in33.6; whole exception phrase supplied'})],['U16-EX-P19','U16-FB-P306'],sid='naht-u14-source')
supplied('oth','ōð','preposition','as far as; up to',[('oth-u16-invariant','ōð',{'part_of_speech':'preposition','inflection':'invariant','context':'supplied ōð ðone ðriddan heofon, accusative goal, in35.7'})],['U16-EX-P21','U16-EX-P66'])
supplied('swilce','swilce','adverb','about; approximately',[('swilce-u16-approximate','swilce',{'part_of_speech':'adverb','inflection':'invariant','context':'swilce twēntig furlanga oððe ðrītig; approximation, not an automatic extension of prior as-if conjunction'})],['U16-EX-P18'])

def a(case,number,gender,**kw):return {'case':case,'number':number,'gender':gender,**kw}
def readingword(lid,h,gl,forms,page,lexpage=None,sid=None,pos='noun'):
 ev=[f'U16-FB-P{page}']+([f'U16-FB-P{lexpage}'] if lexpage else [])
 old=prior.get(lid,{})
 sid=sid or (old['senses'][0]['sense_id'] if old.get('senses') and old['senses'][0].get('gloss')==gl else lid+'-u16-reading')
 fs=[]
 for surf,an in forms:
  fid=None
  for f in old.get('forms',[]):
   aa=f.get('analysis',{});aa=aa if isinstance(aa,dict) else {'source_analysis':aa};con=aa.get('contextual_parse',aa.get('source_analysis',''))
   if f['form'].casefold()==surf.casefold() and ((str(aa.get('case','')).startswith(an['case']) and str(aa.get('number','')).startswith(an['number'])) or (an['case']+'-'+an['number'] in con)):
    fid=f['form_id'];break
  fs.append((fid or lid+'-u16-source-'+an['case']+'-'+an['number']+('-'+an['strength'] if lid=='geong' else ''),surf,an))
 return supplied(lid,h,pos,gl,fs,ev,sid,note='Exact reading forms and contextual meaning only; supplied without independent recall or a new complete paradigm. Contextual renderings are not unrestricted new dictionary senses.')
readingword('fultum','fultum','help; support',[('fultumes',a('gen','sg','m'))],168,sid='fultum-u15-source-sense')
readingword('sciete','scīete','linen cloth',[('scīetan',a('dat','sg','f'))],168,311)
readingword('baethstede','bæðstęde','bathing place; here gymnasium',[('bæðstęde',a('dat','sg','m')),('bæðstęde',a('nom','sg','m'))],168)
readingword('ceasterwaran','ceasterwaran','townspeople; citizens',[('ceasterwaran',a('nom','pl','m',function='direct address'))],168)
readingword('eltheodig','ęlðēodig','foreign people; strangers',[('ęlðēodige',a('nom','pl','m',function='substantive direct address'))],168,pos='adjective')
readingword('theow','ðēow','unfree; enslaved people',[('ðēowe',a('nom','pl','m',function='substantive direct address'))],168,318,pos='adjective')
readingword('aethele','æðele','noble people',[('æðele',a('nom','pl','m',function='substantive direct address'))],168,pos='adjective')
readingword('unaethele','unæðele','people not noble',[('unæðele',a('nom','pl','m',function='substantive direct address'))],168,pos='adjective')
readingword('open','open','open',[('open',a('nom','sg','m',strength='strong',function='predicate'))],168,pos='adjective')
readingword('healf','healf','half',[('healfan',a('dat','sg','m',strength='weak'))],168,298,sid='healf-half-source',pos='adjective')
readingword('sciccels','sciccels','cloak',[('sciccelse',a('dat','sg','m'))],168,311)
readingword('thweal','ðwēal','bath; bathing place',[('ðwēale',a('dat','sg','n'))],168)
readingword('gelica','gelīca','equal; peer',[('gelīcan',a('acc','sg','m')),('gelīca',a('nom','sg','m'))],168,292)
readingword('flocc','flocc','group; company',[('flocce',a('dat','sg','m'))],168)
readingword('menigu','męnigu','company; crowd',[('męnige',a('dat','sg','f'))],168,305)
readingword('theod','ðēod','region; country',[('ðēode',a('gen','sg','f'))],168,318,sid='theod-u16-region')
readingword('plega','plega','play; game',[('plegan',a('acc','sg','m',context='168.6 literal youthful games; equipment is an explanatory contextual rendering')),('plegan',a('dat','sg','m',context='169.1/7 game'))],168)
readingword('hraednes','hrædnes','speed; quickness',[('hrædnesse',a('dat','sg','f'))],169)
readingword('snelnes','snelnes','skill; agility',[('snelnesse',a('acc','sg','f'))],169)
readingword('swiftnes','swiftnes','swiftness',[('swiftnesse',a('dat','sg','f'))],169,315)
readingword('swift','swift','swift',[('swiftre',a('dat','sg','f',strength='strong'))],169,315,pos='adjective')
readingword('cniht','cniht','young man; youth',[('cniht',a('nom','sg','m'))],169)
readingword('top','top','ball?, as Cook tentatively interprets it',[('top',a('acc','sg','m',context='uncertain object noun in the OE wording; Latin describes rubbing with ointment instead'))],169)
readingword('ieldu','ieldu','age; old age',[('ielde',a('dat','sg','f'))],169,301)
readingword('geoguth','geoguð','youth',[('geoguðe',a('dat','sg','f'))],169)
readingword('cynesetl','cynesętl','royal seat; throne',[('cynesętle',a('dat','sg','n'))],169)
readingword('gemaene','gemǣne','common; shared',[('gemǣnan',a('acc','sg','f',strength='weak'))],170,pos='adjective')
readingword('haelu','hǣlu','safety; rescue',[('hǣle',a('acc','sg','f',context='by the common safety, in the source oath; welfare is a contextual alternative'))],170,297,sid='haelu-u11-source')
readingword('thenung','ðēnung','service; attendance',[('ðēnunge',a('acc','sg','f'))],170,318)
readingword('horg','horg','dirty; filthy',[('horgum',a('dat','sg','m',strength='strong'))],170,pos='adjective')
readingword('gereord','gereord','meal; banquet',[('gereorde',a('dat','sg','n'))],170)
readingword('apollonius','Apollonius','Apollonius',[('Apollonius',a('nom','sg','m')),('Apollonio',a('dat','sg','m'))],170,pos='proper_noun')
readingword('arcestrates','Arcestrates','Arcestrates, king of the region',[('Arcestrates',a('nom','sg','m'))],168,pos='proper_noun')
readingword('geong','geong','young',[('geongra',a('gen','pl','m',strength='strong')),('geongan',a('gen','sg','m',strength='weak',context='substantive young man')),('geonges',a('gen','sg','m',strength='strong'))],168,pos='adjective')
readingword('an','ān','one',[('ǣnne',a('acc','sg','m',context='source spelling distinct from prior selected ānne'))],168,pos='numeral')
readingword('thes','ðes','this; these',[('ðisum',a('dat','pl','n',context='single-s source spelling corresponding to prior ðissum'))],168,pos='demonstrative')
readingword('forliden','forliden','shipwrecked',[('forliden',a('nom','sg','m',strength='strong',context='adjectival participle describing the man; no general new verbal paradigm'))],170,288,pos='adjective')
for lid,h,surf,gl,ev,sid in [
 ('oth-thaet','oð-ðæt','ōð-ðæt','until',['U16-FB-P168','U16-EX-P66'],'oth-thaet-until'),
 ('mid-thy','mid-ðȳ','mid-ðȳ-ðe','when; while',['U16-FB-P168','U16-FB-P305'],'mid-thy-when'),
 ('tha-conjunction','ðā','ðā-ðā','when; factual past time',['U16-FB-P168','U16-EX-P67'],'tha-when'),
 ('faeringa','fǣringa','fǣringa','suddenly',['U16-FB-P168','U16-FB-P286'],None),
 ('ongean','ongēan','āgēan','back; again',['U16-FB-P169'],'ongean-u16-back'),
 ('hraedlice','hrædlīce','hrædlīce','quickly',['U16-FB-P169','U16-FB-P300'],None),
 ('heonan','heonan','heonan','hence; from here',['U16-FB-P169','U16-FB-P298'],None),
 ('gecwemlice','gecwēmlīce','gecwēmlīce','pleasantly; agreeably',['U16-FB-P169'],None)]:
 supplied(lid,h,'conjunction' if lid in ['oth-thaet','mid-thy','tha-conjunction'] else 'adverb',gl,[(lid+'-u16-reading-surface',surf,{'part_of_speech':'conjunction' if lid in ['oth-thaet','mid-thy','tha-conjunction'] else 'adverb','inflection':'invariant'})],ev,sid)
supplied('twentig','twēntig','numeral','twenty',[('twentig-cardinal-u12-source','twēntig',{'inflection':'uninflected in the supplied quantity phrase'})],['U16-EX-P18','U16-FB-P48'],sid='twentig-u12-source')
supplied('hund','hund','numeral','hundred, in the supplied hund scēapa phrase',[('hund-invariant-u09-supplied','hund',{'inflection':'invariant in supplied hundred expression'})],['U16-EX-P18','U16-FB-P48','U16-FB-P300'],sid='hund-hundred-source')
supplied('soth-citation','sōð','adjective','true',[('soth-u16-predicate-nom-m-sg','sōð',a('nom','sg','m',strength='strong',context='exact predicate in34.11; prior citation alone is not full productive adjective teaching'))],['U16-EX-P20','U16-FB-P313'],sid='soth-citation-1')
l=lemma('dom','dōm','noun','judgment; a judgment made in judging', ['U16-EX-P22'],'dom-u16-judgment',note='New ordinary-judgment sense extends prior Day-of-Judgment/fate uses. Reuse actual singular morphology; do not extend abstract plurals to independent recall.')
cell(l,'dōm',a('acc','sg','m'),'NEW-U16-VOC-DOM',['U16-EX-P22'],fid='dom-acc-sg')

# New ordinary uses of previously supplied invariant prepositions are separately declared.
def existing_function(lid,sid,gl,ev,status='new_production',surf=None,fid=None):
 old=prior[lid];h=old['display_headword'];of=next((f for f in old['forms'] if f['form']==(surf or h)),old['forms'][0]);surf=surf or of['form'];fid=fid or of['form_id']
 if lid=='to':of=next(f for f in old['forms'] if f['form_id']=='to-preposition-dative-invariant');fid=of['form_id']
 l=lemma(lid,h,old['part_of_speech'],gl,ev,sid,status,'Only the named construction and sense are assigned; other homographic uses retain their earlier scope.')
 f={'form_id':fid,'form':surf,'analysis':of['analysis'],'knowledge_status':status,'teaching_ids':['NEW-U16-VOC-'+lid.upper()],'evidence_refs':ev,'prior_scope':scope(of),'scope_note':l['scope_note']};l['forms'].append(f)
existing_function('aefter','aefter-after-source','after, temporal with dative',['U16-EX-P20','U16-FB-P168'])
existing_function('aefter','aefter-according-to-source','according to, with dative',['U16-EX-P20'])
existing_function('sona','sona-immediately-source','immediately; at once',['U16-EX-P19','U16-FB-P313'])
existing_function('into','into-destination-source','into; destination expressed with dative after intō',['U16-EX-P19','U16-EX-P22','U16-FB-P301'],surf='intō')
existing_function('on','on-u16-fishing','in the fishing activity, in supplied on fiscnoð',['U16-FB-P167','U16-EX-P19'],'supplied')
existing_function('to','to-u16-body-care','for the care of a body part, in supplied wæter tō mīnum fōtum',['U16-EX-P22'],'supplied',surf='tō')
existing_function('to','to-u16-wife-role','as wife; in the role of wife, in supplied tō wīfe',['U16-EX-P22'],'supplied',surf='tō')
existing_function('on','on-u16-clothing','in; wearing clothing, in supplied on scēapa gegierelum',['U16-EX-P21'],'supplied')
existing_function('of','of-u15-source-partitive','of; from a portion of a whole, in the supplied phrases ān of ðǣm and of ēowrum ęle',['U16-EX-P18','U16-EX-P21'],'supplied')
existing_function('be','be-according-source','according to, with dative',['U16-EX-P22'])
existing_function('be','be-u14-concerning-source','concerning; about, with dative',['U16-EX-P21'])
existing_function('thurh','thurh-through','through',['U16-FB-P318'],surf='ðurh')
existing_function('thurh','thurh-u14-mediated-source','through; by way of a person',['U16-EX-P19','U16-FB-P318'],surf='ðurh')
existing_function('for-thon-the','for-thon-the-u16-therefore','therefore; for that reason (adverbial consequence, distinct from because)',['U16-EX-P22','U16-EX-P67'],surf='for-ðon',fid='for-thon-the-invariant-short-source-source')
existing_function('swilce','swilce-u16-as-if','as if, introducing the source comparison of apparent rejuvenation',['U16-FB-P169','U16-FB-P315'],'supplied',surf='swilce')
existing_function('thaes-the','thaes-the-u16-as-seems','as, in the exact parenthesis ðæs-ðe mē ðyncð',['U16-FB-P169'],'supplied',surf='ðæs-ðe')
existing_function('aefter','aefter-u16-seeking','after; in search of; about the person sought or inquired after',['U16-FB-P170'],'supplied')
existing_function('on','on-u16-at-work','at work; engaged in an activity, in exact source phrases',['U16-FB-P168','U16-FB-P169'],'supplied')
existing_function('to','to-u16-belonging','to, complement of belonging',['U16-FB-P168'],'supplied',surf='tō')
existing_function('to','to-u16-rejuvenation','to, a resulting state of youth',['U16-FB-P169'],'supplied',surf='tō')
existing_function('be','be-u16-grasp','by, the body part by which a person is led',['U16-FB-P169'],'supplied')
existing_function('of','of-u16-old-age','from, the state of old age in the supplied rejuvenation comparison',['U16-FB-P169'],'supplied')
supplied('on-adverb','on','adverb','on, in the relative clause referring to the cloak he wore',[('on-adverb-u16-source','on',{'part_of_speech':'adverb','inflection':'invariant','context':'ðe hē on hæfde; keep entire clothing expression supplied'})],['U16-FB-P168'])
supplied('laes','lǣs','degree_word','less; a smaller amount',[('laes-u16-acc-n-sg','lǣs',a('acc','sg','n',context='degree accusative modifying lufað, as expressly directed by Cook36.6')),('laes-u16-nom-n-sg','lǣs',a('nom','sg','n',context='smaller amount as subject of forgiefen is in the supplied36.6 clause'))],['U16-EX-P22'])
supplied('nawiht','nāwiht','indefinite_pronoun','nothing; naught',[('nawiht-u16-nom-n-sg','nāwiht',a('nom','sg','n',context='predicate in nis mīn wuldor nāwiht; prior accusative source form preserved separately'))],['U16-EX-P21'])
supplied('ongean','ongēan','adverb','back; again',[('ongean-u16-adverb-invariant','ongēan',{'part_of_speech':'adverb','inflection':'invariant','context':'back with sending and returning; distinct from the prior preposition against'})],['U16-FB-P169','U16-FB-P170'],sid='ongean-u16-back')
existing_function('thurh','thurh-u16-means','through; by means of service, or by evidence in the exact source question Ðurh hwæt',['U16-FB-P170','U16-FB-P318'],'supplied',surf='ðurh')
existing_function('with','with-u16-players','with; against fellow players, with dative in the exact source playing frame',['U16-FB-P168'],'supplied',surf='wið')
existing_function('mid','mid-u16-source-clothing','with a cloth or cloak: exact complements of begyrd and bewǣfed, beyond the earlier bounded gescrȳdan frame',['U16-FB-P168','U16-FB-P170'],'supplied',surf='mid')
existing_function('thaet-conjunction','thaet-u16-uncertain-link','that: source169.6 linkage expressly uncertain in Cook note6; retain the clause without requiring a unique content/result classification',['U16-FB-P169'],'supplied',surf='ðæt')
# These two finite source forms retain their actual IDs; only the bounded source sense is new.
supplied('geseon','gesēon','verb','see that a stated circumstance holds',[('geseon-pret-3-sg','geseah',{'tense':'preterite','mood':'indicative','person':3,'number':'sg','context':'170.8–9 finite ðæt content complement; not accusative-plus-infinitive'})],['U16-FB-P170'],sid='geseon-u16-content')
supplied('wesan','wesan','verb','in the impersonal source expression it seemed to the king',[('wesan-pret-3-sg','wæs',{'tense':'preterite','mood':'indicative','person':3,'number':'sg','context':'wæs geðūht with dative experiencer, supplied as a complete expression'})],['U16-FB-P169'],sid='wesan-u16-impersonal-seemed')

# Combine proposals for the same actual lemma without losing per-sense scopes.
merged={}
for l in lemmas:
 if l['lemma_id'] not in merged:merged[l['lemma_id']]=l;continue
 dest=merged[l['lemma_id']]
 for k,ik in [('forms','form_id'),('senses','sense_id')]:
  have={x[ik]:x for x in dest[k]}
  for x in l[k]:
   if x[ik] not in have:dest[k].append(x);have[x[ik]]=x
   elif x.get('knowledge_status')=='new_production':have[x[ik]].update(x)
 dest['source_spellings']=list(dict.fromkeys(dest['source_spellings']+l['source_spellings']));dest['evidence_refs']=list(dict.fromkeys(dest['evidence_refs']+l['evidence_refs']))
lemmas=list(merged.values())

dump('lexical-inventory.json',{'schema_version':1,'status':'source reconciled; ready for canonical integration','baseline':'e1d94be968e89ecfc4918ed58d850702e5d0e57e','lemmas':lemmas,'boundary':'Verbal paradigms belong to unit16-grammar; two narrow reading senses reuse existing finite IDs. Shared integration belongs to root/design.'})
dump('noun-adjective-paradigms.json',{'schema_version':1,'status':'source reconciled; assigned positions mapped in exercises-dependencies and reading-token-ledger','paradigms':paradigms,'counts':{'paradigms':len(paradigms),'cells':sum(len(p['cells']) for p in paradigms)},'rules':['Nouns of a previously taught class are explicitly derived from verified shared models; a complete paradigm does not grant unassigned senses or syntax.','Mass/abstract/proper-title sense inventories do not invent count plurals.','All old IDs and source analyses are preserved; contextual analyses may add a task-specific interpretation without erasing earlier records.']})
print({'lemmas':len(lemmas),'paradigms':len(paradigms),'cells':sum(len(p['cells']) for p in paradigms)})
