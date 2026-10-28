"""252 exact source positions; contextual analyses never replace prior metadata."""
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf8'))
L={l['lemma_id']:l for l in read(R/'lexicon/entries.json')['lemmas']}
S=read(O/'local-support.json')['forms']; P=read(O/'noun-adjective-paradigms.json')['paradigms']; SS=read(O/'nominal-sense-audit.json')['senses']
G=read(R/'sources/audits/unit17-grammar/reading-verbal-bindings.json'); span=read(O/'reading-source.json')['source_spans'][0]
T=re.findall(r'[^\W\d_]+(?:-[^\W\d_]+)*',span['learner_text']);ROWS={}
def short(x,kind):
 keys=['form_id','form','analysis','production_taught_in','recognition_taught_in','supplied_in','coverage_contract'] if kind=='form' else ['sense_id','gloss','production_taught_in','recognition_taught_in','supplied_in','coverage_contract']
 return {k:x.get(k) for k in keys if k in x}
def norm(a):
 if not isinstance(a,dict):return {}
 m={'nominative':'nom','genitive':'gen','dative':'dat','accusative':'acc','singular':'sg','plural':'pl','masculine':'m','feminine':'f','neuter':'n'}
 return {('strength' if k=='declension' else k):m.get(v,v) if isinstance(v,str) else v for k,v in a.items()}
def setrow(i,lid,fid,sid,analysis,fs,ss,helpids,role,priorform=None,priorsense=None,origin='previous active register; exact source token'):
 ROWS[i]=dict(reading_token_id=f'U17-RWORD-{i:03}',token_position_one_based=i,surface=T[i-1],lemma_id=lid,form_id=fid,sense_id=sid,current_context_analysis=analysis,contextual_role_and_meaning=role,form_knowledge_status=fs,sense_knowledge_status=ss,local_help_ids=helpids,prior_form_record=short(priorform,'form') if priorform else None,prior_sense_record=short(priorsense,'sense') if priorsense else None,origin_category=origin,evidence_refs=['U17-FB-P174' if i<=110 else 'U17-FB-P175'],identity_note='Actual prior analysis/status is retained separately. Current syntactic context is additive, not a retroactive reinterpretation of a prior form.')
def b(positions,lid,fid=None,a=None,sid=None,role=''):
 for i in positions:
  l=L[lid]; hits=[f for f in l['forms'] if f['form_id']==fid] if fid else [f for f in l['forms'] if f['form'].casefold()==T[i-1].casefold() and all(norm(f.get('analysis')).get(k)==v for k,v in (a or {}).items())]
  if not hits:raise ValueError((i,T[i-1],lid,fid,a))
  f=hits[0]
  sh=[s for s in l['senses'] if s['sense_id']==sid] if sid else [s for s in l['senses'] if s.get('production_taught_in')]
  if not sh:sh=l['senses']
  s=sh[0]
  setrow(i,lid,f['form_id'],s['sense_id'],a or norm(f.get('analysis')) or {'contextual_analysis':f.get('analysis')},'previously_taught' if f.get('production_taught_in') else 'supplied','previously_taught' if s.get('production_taught_in') else 'supplied',[],role or s['gloss'],f,s)
def local(positions,lid,tag):
 h=next(x for x in S if x['lemma_id']==lid and (x['form_id'].endswith(tag) or x['support_id'].endswith(tag.upper())))
 for i in positions:
  assert h['surface'].casefold()==T[i-1].casefold(),(i,h['surface'],T[i-1])
  pf=next((f for f in L.get(lid,{}).get('forms',[]) if f['form_id']==h['form_id']),None)
  ps=next((s for s in L.get(lid,{}).get('senses',[]) if s['sense_id']==h['sense_id']),None)
  setrow(i,lid,h['form_id'],h['sense_id'],h['analysis'],'previously_taught' if pf and pf.get('production_taught_in') else 'supplied','supplied',[h['support_id']],h['help_text'],pf,ps,origin='exact source; supplied modern analysis and meaning')
def prod(positions,lid,case,number):
 p=next(x for x in P if x['lemma_id']==lid);f=next(x for x in p['cells'] if x['analysis']['case']==case and x['analysis']['number']==number);s=next(x for x in SS if x['lemma_id']==lid)
 for i in positions:
  assert f['form']==T[i-1],(i,f['form'],T[i-1])
  setrow(i,lid,f['form_id'],s['sense_id'],f['analysis'],f['knowledge_status'],s['knowledge_status'],[p['paradigm_id']],s['gloss'],origin='exact source; proposed complete Unit17 nominal display')
# Grammar owns these57 analyses and their12 whole-clause supports.
for v in G['verbal_occurrences']:
 i=v['token_position_one_based'];assert v['surface']==T[i-1]
 setrow(i,v['lemma_id'],v['form_id'],v['sense_id'],v['current_context_analysis'],v['form_knowledge_status'],v['sense_knowledge_status'],v.get('whole_frame_support_ids',[]),v['contextual_role_and_meaning'],v.get('prior_form_record'),v.get('actual_prior_sense'),origin='exact source; grammar agent verbal/participial analysis')
 ROWS[i]['external_binding']='sources/audits/unit17-grammar/reading-verbal-bindings.json#'+v['reading_token_id']
# Invariant forms whose contextual meaning remains within actual prior teaching.
for surface,lid,fid in [('and','and','and-invariant'),('ac','ac','ac-invariant'),('nū','nu','nu-invariant'),('ūt','ut','ut-invariant'),('sōðlice','sothlice','sothlice-invariant'),('nā','na','na-invariant'),('wel','wel','wel-positive'),('gif','gif','gif-invariant'),('Ēalā','eala','eala-invariant'),('ðǣr','thaer','thaer-invariant-source'),('mid','mid','mid-invariant-source'),('on','on','on-invariant'),('sōna','sona','sona-invariant-source'),('swā','swa','swa-invariant')]:
 b([i for i,t in enumerate(T,1) if t.casefold()==surface.casefold() and i not in ROWS],lid,fid)
b([1,24,38,122,131,175],'tha-adverb','tha-adverb-invariant',role='then; narrative temporal adverb')
b([3,13,16,85],'he','he-f-nom-sg',role='she, the princess')
b([8,32,54],'he','he-f-gen-sg',role='her, referring to the princess; genitive possessive')
b([29,59],'he','he-f-acc-sg',role='her, the princess as object')
b([164,169,190,251],'he','he-m-nom-sg',role='he, Apollonius')
b([87,134,219],'he','he-m-acc-sg',role='masculine singular object:87 refers to swēgcræft;134 reflexively to Apollonius;219 to Apollonius')
b([141,148,186],'he','he-m-gen-sg',role='his, Apollonius; genitive possessive')
b([44,57,65,69,100,103,115],'thu','thu-nom-sg',role='you, singular addressee')
b([72,75,111],'ic','ic-nom-sg',role='I, the current speaker')
b([70,93],'ic','ic-dat-sg',role='to me: permission/recipient in the separately supported verb frame')
b([243],'he','he-dat-pl',role='to them all, experiencers of līcode')
b([40,107,124,156,206],'se','se-m-nom-sg',role='the, masculine nominative singular with cyning')
b([27,160],'se','se-all-nom-pl',a={'case':'nom','number':'pl','gender':'m'},role='the, masculine plural with men/those seated around')
b([96,128,145,225],'se','se-f-acc-sg',role='the harp, feminine accusative singular')
b([191],'se','se-all-acc-pl',a={'case':'acc','number':'pl','gender':'m'},role='the strings, masculine accusative plural')
b([21,198],'se','se-f-gen-sg',role='of the harp, feminine genitive singular')
b([182],'se','se-f-dat-sg',role='the hall, feminine dative singular')
b([172],'se','se-all-gen-pl',a={'case':'gen','number':'pl','gender':'m'},role='of the heathens')
b([248],'se','se-all-gen-pl',a={'case':'gen','number':'pl','gender':'n'},role='of those things')
b([236],'se','se-n-dat-sg',role='the people, neuter collective singular')
b([74,77,114,155,163,168],'thaet-conjunction','thaet-conjunction-invariant',role='that, introducing the separately analysed content/result clause')
b([102],'se','se-n-acc-sg',sid='se-free-relative-what-source',role='that which / what you do not yet know; demonstrative object with understood relative relation')
b([26,48,159,210],'eall','eall-nom-m-pl-strong',role='all, nominative masculine plural')
b([118],'eall','eall-dat-n-pl-strong',role='all matters, dative neuter plural')
b([244],'eall','eall-dat-m-pl-strong',role='all of them, dative masculine plural')
b([28,49],'mann','mann-nom-pl',role='men, nominative plural')
b([41,108,125,157,207],'cyning','cyning-nom-sg',role='king, subject or apposition')
b([67],'cyning','cyning-nom-sg',a={'case':'nom','number':'sg','gender':'m','function':'direct address'},role='king, directly addressed')
b([51],'min-poss','min-poss-acc-f-sg-strong',role='my, agreeing with daughter')
b([52],'dohtor','dohtor-acc-sg',role='daughter, object of praise/blame')
b([80],'dohtor','dohtor-nom-sg',role='daughter, subject of chanced')
b([79],'thin-poss','thin-poss-nom-f-sg-strong',role='your, agreeing with daughter')
b([66],'god-adjective','god-adjective-nom-m-sg-weak',role='good, weak singular in direct address')
b([18,202],'wynsum','wynsum-dat-m-sg-strong',role='pleasant, agreeing with dative singular song; exact source wynsumum')
b([19,203],'sang','sang-dat-sg',role='song, accompaniment to the harp music')
b([119],'thing','thing-dat-pl',role='matters; fields of accomplishment',sid='thing-matters')
b([142],'heafod','heafod-acc-sg',role='head, destination of crown placement')
b([149],'hand','hand-acc-sg',role='hand, destination in took the harp into his hand')
b([208],'self','self-nom-m-sg-strong',role='the king himself')
b([216],'stefn','stefn-dat-sg',role='voice, dative in the supplied manner phrase micelre stefne')
b([221],'aefter','aefter-invariant-source',role='after, temporal preposition with dative',sid='aefter-after-source')
b([230],'fela','fela-invariant',role='many, with genitive plural; supported collective construction')
b([231],'faeger','faeger-gen-n-pl-strong',role='fine/beautiful, genitive plural positive; not comparative')
b([232,249],'thing','thing-gen-pl',role='things performed, genitive neuter plural')
b([237],'folc','folc-dat-sg-source',role='the people, dative collective singular',sid='folc-source')
b([247],'aelc','aelc-nom-n-sg-strong',role='each one, nominative neuter singular governing partitive genitive')
b([211,235],'the-relative','the-relative-subject-invariant',a={'inflection':'invariant','function':'subject relative'},role='who/which; supplied relative-clause role with explicit antecedent')
b([250],'the-relative','the-relative-invariant',a={'inflection':'invariant','function':'object relative'},role='which he performed, object of forðtēah')
# Exact source names and isolated forms are explicitly supplied.
for poss,lid,tag in [([23,200],'sweg','acc-sg'),([33,55],'swegcraeft','dat-sg'),([83],'swegcraeft','acc-sg'),([36,58],'an','alone-source'),([46],'yfele-adverb','invariant'),([47],'for-tham-the','source-invariant'),([138],'an','source-acc-m-sg'),([140],'upon','invariant'),([173],'haethen','gen-pl'),([174],'god','common-nom-sg'),([177],'stilnes','nom-sg'),([179],'swige','nom-sg'),([181],'innan','preposition'),([183],'heall','dat-sg'),([187],'hearpenaegl','acc-sg'),([192],'hearpestreng','acc-pl'),([194],'craeft','dat-sg'),([213],'andweard','nom-m-pl'),([215],'micel','dat-f-sg-strong'),([222],'thes','dat-n-sg-source'),([241],'ungewunelic','nom-n-sg'),([245],'thearle','invariant'),([35,62,130,166,185,224],'apollonius','reading-nom'),([42,110],'apollonius','reading-voc'),([127],'apollonius','reading-dat'),([106],'arcestrates','reading-nom'),([171],'apollines','reading-nom')]:local(poss,lid,tag)
prod([9,97,129,146,226],'hearpe','acc','sg');prod([22,199],'hearpe','gen','sg');prod([139],'cynehelm','acc','sg')
# Remaining invariant adverb IDs are selected from their actual unique surface records.
for i,lid in [(98,'thonne'),(104,'giet')]:
 if i not in ROWS:b([i],lid)
# Sense selection overrides the mechanical invariant surface lookup.
b([31,53,117],'on','on-invariant',sid='on-respect',role='in/with respect to a quality or domain, with dative: musical skill or fields of accomplishment')
b([147],'on','on-invariant',sid='on-into-goal',role='into his hand, destination of taking; accusative hand')
b([17,201],'mid','mid-invariant-source',sid='mid-accompaniment-source',role='with an accompanying pleasant song')
b([193],'mid','mid-invariant-source',sid='mid-u13-manner-source',role='with skill; supplied manner expression mid cræfte')
local([98],'thonne','THEN-CONSEQUENCE');local([11],'sona','TEMPORAL-CORRELATIVE');local([12],'swa','TEMPORAL-CORRELATIVE');local([82],'on','CHANCED-DOMAIN')
for i in range(11,16):ROWS[i]['local_help_ids'].append('U17-READ-SONA-SWA')
for i in range(81,84):ROWS[i]['local_help_ids'].append('U17-READ-ON-MUSIC')
missing=[(i,t) for i,t in enumerate(T,1) if i not in ROWS]
assert not missing,missing
assert len(T)==252 and len(ROWS)==252
for h in S:
 h['reading_token_positions_one_based']=[i for i,r in ROWS.items() if h['support_id'] in r['local_help_ids']]
support=read(O/'local-support.json');support['forms']=S
(O/'local-support.json').write_text(json.dumps(support,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
for i,row in ROWS.items():
 row['whole_frame_support_ids']=[h['feature_id'] for h in G['whole_frame_support'] if h['token_start_one_based']<=i<=h['token_end_one_based']]
data=dict(schema_version=1,status='complete exact-position source analysis; grammar-owned verbal records joined by explicit IDs',source_span_id=span['source_span_id'],tokenization=G['tokenization'],exact_source_word_count=252,tokens=[ROWS[i] for i in sorted(ROWS)],local_help_spans=[dict(support_id=h['support_id'],token_positions_one_based=h['reading_token_positions_one_based'],help_text=h['help_text']) for h in S if h['reading_token_positions_one_based']]+support['reading_phrase_support'],external_whole_frame_support=G['whole_frame_support'],counts={'tokens':252,'verbal_or_participial_external':len(G['verbal_occurrences']),'nonverbal':252-len(G['verbal_occurrences']),'missing':0},unresolved=[])
(O/'reading-token-audit.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(data['counts'])
