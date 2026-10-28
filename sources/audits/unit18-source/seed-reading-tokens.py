"""Explicit contextual token identities; no headword-based prior grants."""
import json,re
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[2]
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
S=rd(P/'reading-source.json')['source_spans'][0];L={x['lemma_id']:x for x in rd(R/'lexicon/entries.json')['lemmas']}
F={f['form_id']:(l,f) for l in L.values() for f in l.get('forms',[])}
local=rd(P/'local-support.json');N=rd(P/'noun-adjective-paradigms.json');NS=rd(P/'nominal-sense-audit.json')['senses']
TOK=[dict(reading_token_id=f'U18-RWORD-{i:03d}',token_position_one_based=i,surface=re.sub(r'^[“”‘’]+|[.,;:!?“”‘’]+$','',w),source_word_with_punctuation=w) for i,w in enumerate(S['learner_text'].split(),1)]
assert len(TOK)==226
physical=[];pending=None
for line in S['source_lines']:
 words=re.sub(r'\[\d+[a-z]?\]','',line['source_with_note_markers']).split()
 for j,w in enumerate(words):
  unit=dict(word=w,source_line_ids=[line['source_line_id']],printed_pages=[line['printed_page']],pdf_pages_one_based=[line['pdf_page_one_based']])
  if pending:
   unit['word']=(pending['word'] if pending['word'].endswith('swā-') else pending['word'][:-1])+w
   for k in ['source_line_ids','printed_pages','pdf_pages_one_based']:unit[k]=list(dict.fromkeys(pending[k]+unit[k]))
   pending=None
  if j==len(words)-1 and w.endswith('-'):pending=unit
  else:physical.append(unit)
assert pending is None and len(physical)==len(TOK)
for t,p in zip(TOK,physical):
 assert t['surface']==re.sub(r'^[“”‘’]+|[.,;:!?“”‘’]+$','',p['word'])
 t.update({k:p[k] for k in ['source_line_ids','printed_pages','pdf_pages_one_based']})
def compact(x,kind):return {k:x.get(k) for k in (['form_id','form','analysis'] if kind=='form' else ['sense_id','gloss'])+['production_taught_in','recognition_taught_in','supplied_in','coverage_contract']}
def choose(positions,fid,role,sid=None,context=None):
 l,f=F[fid];ss=l.get('senses',[])
 defaults={'se':'se-the','eall':'eall-all','he':'he-1','ic':'ic-personal','mann':'mann-1','swithe':'swithe-positive','the-relative':'the-relative-which','thing':'thing-1','thu':'thu-personal','twegen':'twegen-1','beforan':'beforan-before-source'}
 if sid is None:sid=defaults.get(l['lemma_id'])
 if l['lemma_id']=='he' and fid in ['he-f-gen-sg','he-m-gen-sg']:sid='he-possessor'
 if l['lemma_id']=='aefter':sid='aefter-after-source' if fid=='aefter-initial-u13-source' else 'aefter-according-to-source'
 if sid:s=next(x for x in ss if x['sense_id']==sid)
 elif len(ss)==1:s=ss[0]
 else:s=None
 for i in map(int,positions.split()):
  t=TOK[i-1];assert t['surface'].casefold()==f['form'].casefold(),(i,t['surface'],fid,f['form'])
  t.update(lemma_id=l['lemma_id'],form_id=fid,sense_id=s['sense_id'] if s else None,current_context_analysis=context or f['analysis'],contextual_role_and_meaning=role,form_knowledge_status='previously_taught' if f.get('production_taught_in') or f.get('recognition_taught_in') else 'supplied',sense_knowledge_status='previously_taught' if s and (s.get('production_taught_in') or s.get('recognition_taught_in')) else 'supplied' if s else 'unresolved',prior_form_record=compact(f,'form'),prior_sense_record=compact(s,'sense') if s else None,origin_category='exact source token; identity checked against actual active register',identity_note='Current clause role is stated independently; prior form and sense milestones are preserved separately.',local_help_ids=[])
  if not s:t['sense_candidates']=[compact(x,'sense') for x in ss]
choose('2','mid-thy-u16-reading-surface','when; temporal conjunction in the whole supplied opening clause')
choose('3 26','se-m-gen-sg','genitive masculine singular article')
choose('4','cyning-gen-sg','of the king; genitive singular possessor')
choose('5','dohtor-nom-sg','the daughter; nominative singular subject')
choose('7 42','thaet-conjunction-invariant','that; introduces a content clause','thaet-conjunction-1')
choose('9','on-invariant','in all good accomplishments; dative domain','on-respect')
choose('10','eall-dat-m-pl-strong','all; strong dative masculine plural with cræftum')
choose('11','god-adjective-dat-m-pl-strong','good; strong dative masculine plural with cræftum','god-adjective-1')
choose('13','swa-invariant','so; degree modifying wel','swa-1')
choose('14','wel-positive','well','wel-positive')
choose('17 24 65 102 129 146','tha-adverb-invariant','then; narrative temporal adverb')
choose('19 140','he-f-gen-sg','her; genitive singular, the princess')
choose('22','he-m-gen-sg','his / for him; Apollonius, within supplied love expression')
choose('25','aefter-initial-u13-source','after the close of the feast; temporal dative')
choose('30 197','se-n-nom-sg','nominative neuter singular article with mǣden')
choose('31 198','maeden-nom-sg','girl; nominative singular subject')
choose('33','se-m-dat-sg','dative masculine singular article with cyninge')
choose('34','cyning-dat-sg-source','to the king; dative singular addressee',context={'case':'dat','number':'sg','gender':'m'})
choose('35','leof-nom-m-sg-weak','dear; weak masculine singular direct address to father')
choose('36','faeder-nom-sg','father; direct address, nominative/vocative form')
choose('37 62 175 182','thu-nom-sg','you; nominative singular; addressee changes with the speech')
choose('39 212','ic-dat-sg','to me; first singular dative recipient')
choose('40','lytel-ins-n-sg-strong','a little; instrumental of difference with ǣr')
choose('41','aer-adverb-invariant','earlier, with lȳtle','aer-u13-before')
choose('43 48 73 115','ic-nom-sg','I; first singular nominative')
choose('47 61','swa-hwaet-swa-u15-source-acc-n-sg','whatever; free-choice accusative neuter object')
choose('50','of-invariant-dat-source','from/out of your treasure','of-u11-source')
choose('51','thin-poss-dat-n-sg-strong','your; dative neuter singular with goldhorde')
choose('52','goldhord-dat-sg','treasure; dative singular after of')
choose('54 149','se-m-nom-sg','nominative masculine singular article')
choose('55 177','cyning-nom-sg','king; subject at55, direct address at177')
choose('58','he-f-dat-sg','to her; dative singular princess')
choose('60 199','he-m-dat-sg','to him; dative singular Apollonius')
choose('64 101','he-f-nom-sg','she; nominative singular princess')
choose('66','swithe-positive','very; modifies joyfully')
choose('69 84 90 96 100 120 136 151 156 160 163 168 178 181 202 216','and-invariant','and; coordination')
choose('71','lareow-nom-sg','teacher; direct address, nominative/vocative form')
choose('75','thu-dat-sg','to you; dative singular recipient Apollonius')
choose('77','min-poss-gen-m-sg-strong','my; genitive masculine singular with fæder')
choose('78','faeder-gen-sg','of father; genitive singular with lēafe')
choose('80','twegen-acc-n-pl','two; object quantity twā hund')
choose('81 86','hund-invariant-u09-supplied','hundred, within the supplied quantity; not dog')
choose('82 87','pund-gen-pl','of pounds; genitive plural after the hundreds')
choose('83','gold-gen-sg','of gold; material genitive in the quantity')
choose('85','feower-invariant-count','four; object quantity fēower hund')
choose('89','seolfor-gen-sg','of silver; material genitive in the quantity')
choose('91 158','se-m-acc-sg','accusative masculine singular article')
choose('92','micel-superl-acc-m-sg-weak','greatest; weak accusative masculine singular modifying dǣl')
choose('93','dael-acc-sg-source','part; accusative masculine singular object',context={'case':'acc','number':'sg','gender':'m'})
choose('97','twentig-cardinal-u12-source','twenty, governing the supplied servant phrase')
choose('99','mann-gen-pl','of men; genitive plural after twenty')
choose('103 130','thus-invariant-source','thus; in this way')
choose('106 193','se-all-dat-pl','dative plural article with the enslaved men')
choose('108 195','mann-dat-pl','men; dative plural after tō')
choose('110 207','thes-acc-all-pl','these; accusative neuter plural with ðing',context={'case':'acc','number':'pl','gender':'n','declension':'demonstrative'})
choose('111 208','thing-acc-pl','things; accusative plural object')
choose('112 209','mid-invariant-source','with you; accompaniment','mid-accompaniment-source')
choose('113 210','thu-dat-pl','you; dative plural servants after mid')
choose('114 211','the-relative-invariant','which; accusative plural relative referring to things',context={'case':'acc','number':'pl','gender':'n','function':'relative object'})
choose('118','min-poss-dat-m-sg-strong','my; dative masculine singular with lārēowe')
choose('119','lareow-dat-sg','teacher; dative singular in apposition to Apollonio')
choose('122','innan-u17-preposition','in the chamber; dative location','innan-u17-preposition')
choose('124','beforan-invariant-source','before/in front of my friends; dative complement')
choose('125','min-poss-dat-m-pl-strong','my; dative masculine plural with frēondum')
choose('126','freond-dat-pl','friends; dative plural')
choose('127','thes-nom-n-sg','this; nominative neuter singular subject')
choose('132','aefter-invariant-source','according to the command; dative')
choose('133','se-f-gen-sg','of the; genitive feminine singular article with cwēne')
choose('134','cwen-gen-sg','of the princess; genitive singular','cwen-u17-princess')
choose('137 154','eall-nom-m-pl-strong','all; nominative masculine plural with męnn')
choose('138 152','se-all-nom-pl','nominative plural article with męnn')
choose('139 153','mann-nom-pl','men; nominative plural subject')
choose('143','the-relative-subject-invariant','who; nominative plural relative with delayed antecedent męnn',context={'case':'nom','number':'pl','gender':'m','function':'relative subject'})
choose('144','he-acc-pl','them; accusative plural gifts, not the princess',context={'case':'acc','number':'pl','gender':'f','referent':'giefa'})
choose('159','cyning-acc-sg','the king; accusative singular object')
choose('161','se-f-acc-sg','accusative feminine singular article with cwēne')
choose('165','he-acc-pl','them; king and princess, accusative actor of infinitive',context={'case':'acc','number':'pl','referent':'king and princess','function':'infinitival actor'})
choose('169','ham-invariant','home; directional adverb, not an inflected noun')
choose('171 191','eac-invariant','also','eac-also')
choose('172','swilce-adverb-invariant','likewise, with ēac','swilce-likewise')
choose('176','god-adjective-nom-m-sg-weak','good; weak nominative/vocative masculine singular king','god-u15-kind')
choose('183 214','cwen-nom-sg','princess; direct address at183, subject at214','cwen-u17-princess')
choose('187','thu-nom-pl','you; nominative plural king and princess')
choose('189','he-m-nom-sg','he; Apollonius, nominative singular')
choose('196','the-relative-invariant','whom; accusative plural servants',context={'case':'acc','number':'pl','gender':'m','function':'relative object'})
choose('203','he-dat-pl','to them; dative plural servants, governed by postposed tō')
choose('213','se-f-nom-sg','nominative feminine singular article with cwēn')
choose('218 223','ic-nom-pl','we; nominative plural Apollonius and servants')
choose('220','ure-poss-acc-n-sg-strong','our; accusative neuter singular with giesthūs')
choose('221','giesthus-acc-sg','guesthouse; accusative singular object of seek')
choose('222','thaet-conjunction-invariant','so that; purpose conjunction','thaet-purpose')
choose('225','ic-acc-pl','ourselves; accusative plural reflexive object with geręstan, as Cook177 note2 directs to184b',context={'case':'acc','number':'pl','person':1,'function':'reflexive object with geręstan'})
# New nominal cells have their own explicit sense scope.
for i,lid,fid,role in [(150,'gebeorscipe','gebeorscipe-nom-sg','feast; nominative singular subject'),(166,'gesund','gesund-acc-pl-m-strong','well; accusative plural predicate with infinitival actor hīe'),(188,'gesund','gesund-nom-pl-m-strong','well; nominative plural predicate with gē')]:
 p=next(x for x in N['paradigms'] if x['lemma_id']==lid);f=next(x for x in p['cells'] if x['form_id']==fid);s=next(x for x in NS if x['lemma_id']==lid)
 t=TOK[i-1];assert t['surface']==f['form'];t.update(lemma_id=lid,form_id=fid,sense_id=s['sense_id'],current_context_analysis=f['analysis'],contextual_role_and_meaning=role,form_knowledge_status=f['knowledge_status'],sense_knowledge_status=s['knowledge_status'],local_help_ids=[],prior_form_record=f.get('prior_scope'),prior_sense_record=None,evidence_refs=f['evidence_refs'],origin_category='exact source token; declared rule-derived newly taught cell')
# Local identities take priority over coincidentally identical prior surfaces.
for f in local['forms']:
 for i in f['reading_token_positions_one_based']:
  t=TOK[i-1];assert t['surface'].casefold()==f['surface'].casefold(),(i,t['surface'],f['surface'])
  t.update(lemma_id=f['lemma_id'],form_id=f['form_id'],sense_id=f['sense_id'],current_context_analysis=f['analysis'],contextual_role_and_meaning=f['help_text'],form_knowledge_status='supplied',sense_knowledge_status='supplied',local_help_ids=[f['support_id']],prior_form_record=f['prior_forms'],prior_sense_record=f['prior_senses'],evidence_refs=f['evidence_refs'],origin_category='exact source token with visible local support')
verbs={6:'geseon',15:'wesan',16:'geteon',18:'gefeallan',29:'cwethan',38:'liefan',44:'motan',45:'giefan',49:'willan',56:'cwethan',59:'giefan',63:'willan',68:'utgan',70:'cwethan',74:'giefan',104:'cwethan',109:'beran',116:'behatan',121:'lecgan',128:'weorthan',131:'gedon',142:'herian',145:'geseon',148:'geendian',155:'arisan',157:'gretan',164:'biddan',167:'wesan',170:'gewendan',174:'cwethan',186:'wesan',190:'beseon',200:'forgiefan',201:'habban',204:'cwethan',206:'niman',215:'forgiefan',217:'gan',219:'secan',224:'magan',226:'gerestan'}
for i,lid in verbs.items():TOK[i-1].update(lemma_id=lid,binding_owner='unit18_grammar',external_binding_file='sources/audits/unit18-grammar/reading-verbal-bindings.json',form_knowledge_status='external_binding_pending',sense_knowledge_status='external_binding_pending',current_context_analysis={'part_of_speech':'verb','note':'The verb analyst owns exact finite/nonfinite identity and mood; this source token is not licensed by a matching nominal surface.'},local_help_ids=[])
for t in TOK:
 i=t['token_position_one_based'];t['whole_frame_support_ids']=[h['support_id'] for h in local['reading_phrase_support'] if i in h['reading_token_positions_one_based']]
 t.setdefault('evidence_refs',[f'U18-FB-P{p}' for p in t['printed_pages']])
 if not t.get('lemma_id'):t['form_knowledge_status']='unresolved'
unresolved=[t for t in TOK if not t.get('form_id') and not t.get('binding_owner') or t.get('sense_knowledge_status')=='unresolved']
out=dict(schema_version=1,status='Source/nonverbal audit published for join; verbal records separately owned by grammar analyst',source_span_id=S['source_span_id'],tokenization='226 whitespace words in the declared reflowed text; punctuation removed only for identity matching, capitalization retained. Source physical lines and attached note anchors remain in their separate diplomatic files.',exact_source_word_count=len(TOK),tokens=TOK,local_help_spans=local['reading_phrase_support'],external_whole_frame_support='sources/audits/unit18-grammar/reading-verbal-bindings.json',counts={'total':len(TOK),'verb_tokens':len(verbs),'nonverbal_tokens':len(TOK)-len(verbs),'unresolved_nonverbal':len(unresolved)},unresolved=[{'position':t['token_position_one_based'],'surface':t['surface'],'candidates':t.get('sense_candidates',[])} for t in unresolved])
(P/'reading-token-audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out['counts']));print(json.dumps([{'position':x['position'],'surface':x['surface']} for x in out['unresolved']],ensure_ascii=False))
