"""Bind the independently composed Cook models by exact record identity."""
import copy,json
from collections import Counter
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[2]
def read(path):return json.loads((R/path).read_text(encoding='utf8'))
def write(name,obj):(P/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
FORM={};SENSE={};ORIGIN={};LEMMAS={}
for path in ['lexicon/entries.json','sources/audits/unit14-source/lexical-inventory.json','sources/audits/unit14-source/source-support-records.json','sources/audits/unit14-grammar/grammar-records.json','sources/audits/unit14-grammar/source-support.json']:
 for l in read(path)['lemmas']:
  LEMMAS.setdefault(l['lemma_id'],{})
  for kind,dest in [('forms',FORM),('senses',SENSE)]:
   for rec in l[kind]:
    rid=rec['form_id' if kind=='forms' else 'sense_id'];dest[rid]=(l['lemma_id'],rec);ORIGIN[rid]=path
    if kind=='senses':LEMMAS[l['lemma_id']][rid]=rec
def status(rid,rec):
 if ORIGIN[rid]=='lexicon/entries.json':return 'previously_taught' if rec.get('production_taught_in') or rec.get('recognition_taught_in') else 'supplied'
 return rec['knowledge_status']

DEFAULT={
'dūst':'dust-nom-sg','tō':'to-preposition-dative-invariant','lufode':'lufian-pret-3-sg','god':'god-nom-sg','middangeard':'middangeard-acc-sg','ðæt':'thaet-conjunction-invariant','sealde':'sellan-pret-3-sg','his':'he-m-gen-sg','sunu':'sunu-nom-sg','forweorðe':'forweorthan-pres-subj-3-sg','ðe':'the-relative-invariant','hæbbe':'habban-present-subj-3-sg','ēce':'ece-acc-n-sg-weak','līf':'lif-nom-sg','hǣlend':'haelend-nom-sg','cwæð':'cwethan-pret-3-sg','him':'he-m-dat-sg','weg':'weg-nom-sg','ðǣm':'se-m-dat-sg','fæder':'faeder-nom-sg','būtan':'butan-except-u14-source-1','mē':'ic-dat-sg','sibbe':'sibb-acc-sg','ēow':'thu-dat-pl','mīne':'min-poss-acc-f-sg-strong','ðā':'tha-adverb-invariant','hit':'he-n-nom-sg','cōmon':'cuman-pret-3-pl-source','flōdas':'flod-nom-pl','blēowon':'blawan-pret-3-pl','windas':'wind-nom-pl','āhruron':'ahreosan-pret-3-pl','hūs':'hus-nom-sg','fēoll':'feallan-pret-3-sg','ǣlc':'aelc-nom-n-sg-strong','gōd':'god-adjective-nom-n-sg','trēo':'treo-nom-sg','gōde':'god-adjective-acc-m-pl-strong','wæstmas':'waestm-acc-pl','yfel':'yfel-nom-n-sg-strong','yfele':'yfel-acc-m-pl-strong','wæstm':'waestm-acc-sg','fȳr':'fyr-acc-sg','ēode':'gan-pret-3-sg','munt':'munt-nom-sg','gebǣde':'gebiddan-pret-subj-3-sg','gebæd':'gebiddan-pret-3-sg','wæs':'wesan-pret-3-sg','rēaf':'reaf-nom-sg','hwīt':'hwit-nom-n-sg-strong','cyning':'cyning-nom-sg','eallum':'eall-dat-n-sg','ān':'an-nom-m-sg','ætīewde':'aetiewan-pret-3-sg','dēorwierðu':'deorwierth-acc-n-pl-strong-source','ðing':'thing-acc-pl','seolfor':'seolfor-acc-sg','gold':'gold-acc-sg','wyrtgemang':'wyrtgemang-acc-pl','eall':'eall-acc-n-sg-strong','gemētt':'gemetan-pp-bare-source','sum':'sum-nom-m-sg-strong','welig':'welig-nom-m-sg-strong','mann':'mann-nom-sg','mid':'mid-invariant-source','læg':'licgan-pret-3-sg','hundas':'hund-dog-nom-pl','liccodon':'liccian-pret-3-pl','wunda':'wund-acc-pl','gewāt':'gewitan-pret-3-sg','ęnglas':'engel-nom-pl','bǣron':'beran-pret-3-pl','āhōf':'ahebban-pret-3-sg','ēagan':'eage-acc-pl','geseah':'geseon-pret-3-sg','abraham':'abraham-acc-sg-u14-source','gōdum':'god-goods-dat-pl','ðīnum':'thin-poss-dat-n-sg-strong','ðē':'thu-acc-sg','mīnes':'min-poss-gen-m-sg-strong','sęnde':'sendan-pres-subj-2-sg','hīe':'he-nom-pl','wītgan':'witga-acc-pl','hīerað':'hieran-pres-3-pl','gelīefað':'geliefan-pres-3-pl','ārīse':'arisan-pres-subj-3-sg','habbað':'habban-pres-2-pl','manige':'manig-acc-m-pl-strong','ēowrum':'eower-poss-dat-n-pl-strong'}
OVERRIDES={
'EX-VIII-26-02':{11:'sunu-acc-sg',22:'se-n-acc-sg',24:'lif-acc-sg'},
'EX-VIII-26-03':{18:'faeder-dat-sg',21:'ic-acc-sg'},
'EX-VIII-26-05':{14:'se-n-acc-sg',15:'hus-acc-sg',17:'se-n-nom-sg'},
'EX-VIII-26-08':{4:'munt-acc-sg',10:'tha-conjunction-invariant'},
'EX-VIII-27-01':{3:'he-dat-pl',7:'se-n-acc-sg',10:'se-n-acc-sg',13:'se-all-acc-pl',17:'se-n-nom-sg'},
'EX-VIII-27-07':{3:'abraham-address-u14-source'},
'EX-VIII-27-09':{9:'faeder-gen-sg'},
'EX-VIII-27-10':{3:'se-all-acc-pl'}}
SDEFAULT={
'wesan':'wesan-be','se':'se-the','he':'he-1','ic':'ic-personal','to':'to-destination','on':'on-1','thaet-conjunction':'thaet-conjunction-1','the-relative':'the-relative-which','swa':'swa-1','sellan':'sellan-give','lif':'lif-1','cwethan':'cwethan-1','butan-except':'butan-except-u14-source','thurh':'thurh-u14-mediated-source','cuman':'cuman-come','eall':'eall-all','aelc':'aelc-each','beran':'beran-1','other':'other-other','gan':'gan-1','weorthan':'weorthan-become','an':'an-1','thing':'thing-1','deorwierth':'deorwierth-source','welig':'welig-source','sum':'sum-some','mid':'mid-u14-adornment','aet':'aet-at-source','gewitan':'gewitan-ordinary','hieran':'hieran-1','theah':'theah-although','halsian':'halsian-u13','forlaetan':'forlaetan-u14-leave-to','forweorthan':'forweorthan-1','forceorfan':'forceorfan-u13','weorpan':'weorpan-1','gemetan':'gemetan-find','sendan':'sendan-1','faeder':'faeder-1','eac':'eac-also'}
SOVERRIDES={
'EX-VIII-26-02':{6:'thaet-result',12:'thaet-purpose',17:'on-u14-belief'},
'EX-VIII-26-03':{4:'to-u14-speech-addressee-source',8:'weg-u14-access-source'},
'EX-VIII-26-05':{13:'on-into-goal'},
'EX-VIII-26-06':{5:'beran-produce',12:'beran-produce'},
'EX-VIII-26-07':{7:'beran-produce',10:'on-into-goal',13:'wesan-passive'},
'EX-VIII-26-08':{3:'on-into-goal',5:'thaet-purpose'},
'EX-VIII-26-09':{5:'to-u14-result-source'},
'EX-VIII-26-10':{3:'on-glory-source',8:'wesan-passive'},
'EX-VIII-27-01':{16:'eall-substantive',17:'se-relative',22:'wesan-passive'},
'EX-VIII-27-02':{7:'wesan-passive'},
'EX-VIII-27-08':{8:'on-u14-lifetime-source'},
'EX-VIII-27-11':{4:'on-u14-people-domain-source'}}

models=[];public=[];MISSING={}
SDEFAULT.update({'thu':'thu-personal','habban':'habban-1','forgiefan':'forgiefan-u14-give','gebiddan':'gebiddan-u14-pray','scinan':'scinan-u14-source','swa-swa':'swa-swa-as-source','mann':'mann-1','licgan':'licgan-1','gelimpan':'gelimpan-u14-source','gewitan':'gewitan-depart','geseon':'geseon-1','hwa':'hwa-u14-indefinite-source'})
SOVERRIDES['EX-VIII-27-11'][12]='licgan-u14-source'
for item in read('sources/audits/unit14-source/author-only-cook-working-models.json')['items']:
 iid=item['source_item_id'];rows=[]
 for n,t in enumerate(item['model'].split(),1):
  surface=t.strip('.,;');key=surface.lower()
  fid=OVERRIDES.get(iid,{}).get(n,DEFAULT.get(key))
  if not fid:
   c=[f for f,(l,r) in FORM.items() if r['form'].lower()==key]
   assert len(c)==1,(iid,n,surface,c)
   fid=c[0]
  lid,f=FORM[fid];assert f['form'].lower()==key,(iid,n,surface,fid,f['form'])
  sid=SOVERRIDES.get(iid,{}).get(n,SDEFAULT.get(lid))
  if lid=='he' and key=='his':sid='he-possessor'
  if not sid:
   c=list(LEMMAS[lid])
   if len(c)!=1:MISSING[lid]=(iid,n,c)
   sid=c[0]
  if sid not in SENSE:
   MISSING[lid]=(iid,n,'invalid configured sense',sid,list(LEMMAS[lid]));sid=next(iter(LEMMAS[lid]))
  slid,s=SENSE[sid];assert lid==slid,(iid,n,lid,slid)
  rows.append({'token_index_one_based':n,'token_id':f'{iid}-MODEL-T{n:02d}','surface':surface,'lemma_id':lid,'form_id':fid,'sense_id':sid,'form_status':status(fid,f),'sense_status':status(sid,s),'analysis':copy.deepcopy(f.get('contextual_analysis',f['analysis'])),'gloss':s.get('contextual_gloss',s['gloss']),'evidence_refs':list(dict.fromkeys(f.get('evidence_refs',[])+s.get('evidence_refs',[]))),'form_record_origin':ORIGIN[fid],'sense_record_origin':ORIGIN[sid]})
 models.append({**item,'model_origin':'new_teaching_material: independent composition responding to the exact source prompt, not a quotation from Cook','tokens':rows})
 reqs=[]
 for kind in ['form','sense']:
  for rid in sorted({r[kind+'_id'] for r in rows}):
   row=next(r for r in rows if r[kind+'_id']==rid)
   reqs.append({'kind':kind,'record_id':rid,'lemma_id':row['lemma_id'],'knowledge_status':row[kind+'_status'],'record_origin':row[kind+'_record_origin'],'evidence_refs':row['evidence_refs']})
 public.append({'source_item_id':iid,'required_form_ids':sorted({r['form_id'] for r in rows}),'required_sense_ids':sorted({r['sense_id'] for r in rows}),'requirements':reqs,'model_ref':'author-only-cook-models.json#'+iid,'unresolved':[]})
assert not MISSING,MISSING
write('author-only-cook-models.json',{'schema_version':1,'visibility':'author_only','witness_ref':'author-only-cook-initial-models.json','method':'Initial models composed independently from exact English source prompts. Final strings reconcile exact selected forms, prior scope, current source evidence and coordinated review; each token names its form and sense independently.','items':models,'count':len(models),'token_count':sum(len(x['tokens']) for x in models)})
write('exercises-dependencies.json',{'schema_version':1,'visibility':'public_audit_unordered_dependencies_only','count':len(public),'items':public})
print({'items':len(models),'tokens':sum(len(x['tokens']) for x in models)})
