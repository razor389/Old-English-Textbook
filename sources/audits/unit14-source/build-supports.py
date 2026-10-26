"""Exact local nominal/adjectival help; no new complete productive classes."""
import copy,json
from pathlib import Path
P=Path(__file__).resolve().parent
ROOT=P.parents[2]
prior={x['lemma_id']:x for x in json.loads((ROOT/'lexicon/entries.json').read_text(encoding='utf8'))['lemmas']}
L={}
def scope(rec):
 return {k:copy.deepcopy(rec.get(k)) for k in ['knowledge_status','production_taught_in','recognition_taught_in','supplied_in','reviewed_in','coverage_contract']}
def lemma(lid,head,pos):
 if lid not in L: L[lid]={'lemma_id':lid,'display_headword':head,'part_of_speech':pos,'forms':[],'senses':[],'prior_lemma_present':lid in prior,'scope_note':'Exact supplied forms/senses only, locally printed. No full productive paradigm, general foreign-name system, or independent recall is assigned.'}
 return L[lid]
def sense(lid,head,pos,sid,gloss,refs):
 l=lemma(lid,head,pos)
 old=next((s for s in prior.get(lid,{}).get('senses',[]) if s['sense_id']==sid),None)
 r={'sense_id':sid,'gloss':old['gloss'] if old else gloss,'knowledge_status':'supplied','evidence_refs':refs,'teaching_ids':['NEW-U14-SOURCE-HELPS'],'prior_scope':scope(old) if old else None}
 if old and old['gloss']!=gloss:r['contextual_gloss']=gloss
 l['senses'].append(r)
 return sid
def form(lid,head,pos,fid,surface,analysis,refs,indices=(),tasks=(),origin='exact_source',oldid=None):
 l=lemma(lid,head,pos)
 old=next((f for f in prior.get(lid,{}).get('forms',[]) if f['form_id']==(oldid or fid)),None)
 if old: assert old['form']==surface
 r={'form_id':old['form_id'] if old else fid,'form':surface,'analysis':copy.deepcopy(old['analysis']) if old else {'source_analysis':analysis},'knowledge_status':'supplied','evidence_refs':refs,'teaching_ids':['NEW-U14-SOURCE-HELPS'],'prior_scope':scope(old) if old else None,'reading_token_indices':list(indices),'used_in_tasks':list(tasks),'origin_category':origin,'evidence_basis':'Image-checked exact source token and checked citation; any locally composed form is separately declared and derived only within its printed help.'}
 if old:r['contextual_analysis']={'source_analysis':analysis}
 l['forms'].append(r)
 return r['form_id']

# lid, headword, part of speech, gloss, checked vocabulary page, local forms (surface, parse, reading indices).
DATA=[
 ('aeghwilc','ǣghwilc','indefinite adjective','every; each',274,[('ǣghwilc','nominative feminine singular, modifying ār',[1])]),
 ('ar','ār','noun','honour; high office or position',276,[('ār','nominative feminine singular; subject',[3])]),
 ('frecnes','frēcnes','noun','danger; peril',289,[('frēcnessum','dative feminine plural after mid',[9]),('frēcnessa','nominative feminine plural; subject',[19])]),
 ('woruldgethyngth','woruldgeðyngð','noun','worldly honour; worldly dignity',323,[('woruldgeðyngða','nominative feminine plural; subject',[14])]),
 ('bysen','bȳsen','noun','example; illustration',280,[('bȳsena','accusative feminine plural; object of oncnāwan and ongietan; NOT governed by be',[28])]),
 ('wudubearu','wudubearu','noun','forest; grove',323,[('wudubearwe','dative masculine singular after on',[39])]),
 ('wudu','wudu','noun','wood; forest, collectively',323,[('wudu','nominative masculine singular in comparative subject phrase',[70])]),
 ('heaclif','hēaclif','noun','high cliff',281,[('hēaclifum','dative neuter plural after be; transparent hēah + clif compound',[77])]),
 ('dun','dūn','noun','mountain; hill',283,[('dūnum','dative feminine plural after be',[107])]),
 ('wite','wīte','noun','punishment; penalty',323,[('wīte','accusative neuter singular; object of habbað',[115])]),
 ('heofonfyr','heofonfȳr','noun','fire from heaven; heavenly fire',298,[('heofonfȳre','dative neuter singular of instrument after mid',[124])]),
 ('lieg','līeg','noun','thunderbolt; levin (lightning)',303,[('līegum','dative masculine plural of instrument after mid',[130])]),
 ('lor','lor','noun','destruction; ruin',303,[('lore','dative neuter singular in supplied tō lore weorðan',[144])]),
 ('wela','wela','noun','riches; wealth',321,[('welan','nominative masculine plural; subject; depends on genitive ðisse worulde',[149])]),
 ('sorg','sorg','noun','distress; anxiety; trouble; sorrow',313,[('sorge','dative feminine singular in supplied result tō sorge',[152])]),
 ('eorthlic','eorðlic','adjective','earthly',285,[('eorðlican','nominative neuter plural weak, agreeing with wundor after ðās',[155])]),
]
B=[]
for lid,head,pos,gloss,page,forms in DATA:
 refs=[f'U14-FB-P{page}','U14-SRC-P'+str(156 if forms[0][2][0]<=81 else 157 if forms[0][2][0]<=131 else 158)]
 if lid=='heaclif':refs+=['U14-FB-P298']
 sid=sense(lid,head,pos,lid+'-u14-source',gloss,refs)
 for j,(surface,parse,indices) in enumerate(forms,1):
  fid=form(lid,head,pos,lid+f'-u14-source-{j}',surface,parse,refs,indices)
  for i in indices:B.append({'token_index_one_based':i,'lemma_id':lid,'form_id':fid,'sense_id':sid,'form':surface,'form_status':'supplied','sense_status':'supplied','feature_ids':[]})

def add(lid,head,pos,sid,gloss,fid,surface,parse,refs,indices,oldform=False):
 if not any(x['sense_id']==sid for x in L.get(lid,{}).get('senses',[])):sense(lid,head,pos,sid,gloss,refs)
 form(lid,head,pos,fid,surface,parse,refs,indices,oldid=fid if oldform else None)
 for i in indices:B.append({'token_index_one_based':i,'lemma_id':lid,'form_id':fid,'sense_id':sid,'form':surface,'form_status':'supplied','sense_status':'supplied','feature_ids':[]})

add('treo','trēo','noun','treo-1','tree','treo-nom-sg-u14-source','trēow','nominative neuter singular, source -w variant of taught trēo',['U14-FB-P33','U14-SRC-P156'],[33])
# Do not re-register the already productive sense as supplied.
L['treo']['senses']=[];B[-1]['sense_status']='previously_taught'
add('heah','hēah','adjective','heah-u14-exalted-source','high in rank; exalted','heah-nom-f-sg-u14-source','hēah','nominative feminine singular exact source form, modifying ār; prior selected feminine hēa differs',['U14-FB-P298','U14-SRC-P156'],[2])
form('heah','hēah','adjective','heah-dat-pl-u14-source','hēagum','dative plural weak after ðǣm, modifying coordinated muntum and dūnum; source retained g variant',['U14-FB-P298','U14-SRC-P157'],[104])
B.append({'token_index_one_based':104,'lemma_id':'heah','form_id':'heah-dat-pl-u14-source','sense_id':'heah-1','form':'hēagum','form_status':'supplied','sense_status':'previously_taught','feature_ids':[]})
B.append({'token_index_one_based':134,'lemma_id':'heah','form_id':'heah-nom-f-pl-weak','sense_id':'heah-u14-exalted-source','form':'hēan','form_status':'previously_taught','sense_status':'supplied','feature_ids':[]})
sense('swithra','swīðra','adjective','swithra-u14-stronger-source','stronger; fiercer (degree), distinct from earlier right-side sense',['U14-SRC-P156','U14-FB-P315'])
B.append({'token_index_one_based':21,'lemma_id':'swithra','form_id':'swithra-nom-f-pl-weak','sense_id':'swithra-u14-stronger-source','form':'swīðran','form_status':'previously_taught','sense_status':'supplied','feature_ids':[]})
add('storm','storm','noun','storm-u11-source','storm','storm-nom-acc-sg-source','storm','nominative masculine singular, first subject of gestęnt',['U14-SRC-P156','U14-FB-P314'],[54],True)
add('strang','strang','adjective','strang-u14-attributive-source','strong, here attributive with wind','strang-nom-m-sg-weak-u14-source','stranga','nominative masculine singular weak after se',['U14-SRC-P156','U14-FB-P314'],[58])
sense('other','ōðer','adjective','other-u14-rest-source','remaining; the rest of the (forest/earth)',['U14-SRC-P156','U14-SRC-P157'])
for i,fid,surface in [(69,'other-nom-m-sg-strong','ōðer'),(87,'other-acc-f-sg-strong','ōðre')]:B.append({'token_index_one_based':i,'lemma_id':'other','form_id':fid,'sense_id':'other-u14-rest-source','form':surface,'form_status':'previously_taught','sense_status':'supplied','feature_ids':[]})
sense('torr','torr','noun','torr-u14-crag-source','crag, the probable sense here in Cook’s note; earlier tower sense does not license it',['U14-SRC-P156'])
B.append({'token_index_one_based':79,'lemma_id':'torr','form_id':'torr-dat-pl','sense_id':'torr-u14-crag-source','form':'torrum','form_status':'previously_taught','sense_status':'supplied','feature_ids':[]})
add('ealdordom','ealdordōm','noun','ealdordom-primacy-source','chief place; primacy; eminence','ealdordom-gen-sg-u14-source','ealdordōmes','genitive masculine singular dependent on wīte',['U14-SRC-P157','U14-FB-P283'],[118])
add('miht','miht','noun','miht-u14-powers-source','powers; those holding high power or station in the concluding human application','miht-nom-pl-u14-source','mihta','nominative feminine plural; subject of hrēosað, feallað and weorðað',['U14-SRC-P158','U14-FB-P305'],[135])

# Local Cook aids. Foreign names are supplied forms, never a newly productive class.
sid=sense('weg','weg','noun','weg-u14-access-source','way; means of access to the Father in the figurative declaration, not simply a physical road',['U14-EX-P13'])
sid=sense('ancenned','āncęnned','adjective','ancenned-u14-source','only-begotten',['U14-EX-P13'])
form('ancenned','āncęnned','adjective','ancenned-acc-m-sg-weak-u14-source','āncęnnedan','accusative masculine singular weak, agreeing with Sunu after his',['U14-EX-P13'],tasks=['EX-VIII-26-02'],origin='new_teaching_material')
sid=sense('abraham','Abraham','proper_name','abraham-u14-source','Abraham, biblical patriarch',['U14-EX-P14','U14-FB-P38','U14-BT-MAIN-P258B'])
for fid,surf,parse,tasks in [('abraham-gen-sg-u14-source','Abrahames','genitive singular',['EX-VIII-27-05']),('abraham-acc-sg-u14-source','Abraham','accusative singular, uninflected foreign-name route',['EX-VIII-27-06']),('abraham-address-u14-source','Abraham','direct address, uninflected foreign name',['EX-VIII-27-07'])]:
 form('abraham','Abraham','proper_name',fid,surf,parse,['U14-EX-P14','U14-FB-P38','U14-BT-MAIN-P258B'],tasks=tasks,origin='new_teaching_material')
sid=sense('lazarus','Lazarus','proper_name','lazarus-u14-source','Lazarus, the poor man in the parable; plural Lazaruses denotes people like him',['U14-EX-P14','U14-EX-P15','U14-FB-P38','U14-BT-MAIN-P379'])
form('lazarus','Lazarus','proper_name','lazarus-acc-sg-u14-source','Lazarum','accusative singular with Latin ending, directly attested in the cited Luke16.24 quotation',['U14-EX-P14','U14-FB-P38','U14-BT-MAIN-P379'],tasks=['EX-VIII-27-07'])
form('lazarus','Lazarus','proper_name','lazarus-acc-pl-u14-source','Lazaras','accusative plural, naturalized -as; exact Cook prompt help',['U14-EX-P15','U14-FB-P38'],tasks=['EX-VIII-27-11'])

# Transparent base citations printed beside family-analysis tasks only.
for lid,head,gloss,refs in [('hord','hord','hoard; treasure',['U14-BT-MAIN-P552A']),('clif','clif','cliff',['U14-FB-P281']),('ealdor-chief','ealdor','chief; king (not the separate noun life)',['U14-FB-P283'])]:
 sense(lid,head,'noun',lid+'-u14-component-source',gloss,refs)
 form(lid,head,'noun',lid+'-u14-component-citation',head,'citation supplied as a component base, no independent inflectional system',refs,tasks=['NEW-U14-A01','NEW-U14-S05'],origin='exact_source')

obj={'schema_version':1,'baseline_checkpoint':'c2cb7d6','public_scope':'Unordered exact local lexical helps, not a model translation or new productive systems.','lemmas':list(L.values()),'reading_nominal_bindings':sorted(B,key=lambda x:x['token_index_one_based']),'counts':{'lemmas':len(L),'forms':sum(len(l['forms']) for l in L.values()),'senses':sum(len(l['senses']) for l in L.values()),'reading_bindings':len(B)}}
(P/'source-support-records.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(obj['counts'])
