import json,re
from pathlib import Path
P=Path(__file__).resolve().parent
R=P.parents[2]
F={};S={}
for path in ['lexicon/entries.json','sources/audits/unit14-source/lexical-inventory.json','sources/audits/unit14-source/source-support-records.json','sources/audits/unit14-grammar/grammar-records.json','sources/audits/unit14-grammar/source-support.json']:
 for l in json.loads((R/path).read_text(encoding='utf8'))['lemmas']:
  for f in l['forms']:F[f['form_id']]=(l['lemma_id'],f)
  for s in l['senses']:S[s['sense_id']]=(l['lemma_id'],s)
items=json.loads((P/'author-only-cook-initial-models.json').read_text(encoding='utf8'))['items']
for item in items:
 i=item['source_item_id'];s=item['model']
 if i=='EX-VIII-26-03':s=s.replace('Sē Hǣlend','Se Hǣlend')
 if i=='EX-VIII-26-05':s=s.replace('Ðā rīnde','Ðā hit rīnde')
 if i=='EX-VIII-26-05':s=s.replace('feoll','fēoll')
 if i=='EX-VIII-26-06':s=s.replace(' yfle ',' yfele ')
 if i in ['EX-VIII-26-06','EX-VIII-26-07']:s=s.replace('bereð','birð')
 if i=='EX-VIII-26-07':s=s.replace(' bið forcorfen',' forcorfen').replace('worpen.','worpen bið.')
 if i=='EX-VIII-26-09':s=s.replace('weorðeð','wierð')
 if i=='EX-VIII-26-10':s=s.replace('næs','ne wæs').replace(' swā ān',' swā-swā ān')
 if i=='EX-VIII-27-02':s=s.replace(' wæs mid',' mid').replace('geglęnged.','geglęnged wæs.')
 if i=='EX-VIII-27-09':s=s.replace('bidde','hālsie')
 if i=='EX-VIII-27-11':s=s.replace('geatum','gatum')
 item['model']=s
 toks=s.split();print(i,len(toks),s)
 for n,t in enumerate(toks,1):
  surf=t.strip('.,;')
  candidates=[fid for fid,(lid,f) in F.items() if f['form'].lower()==surf.lower()]
  if len(candidates)!=1:print(' ',n,surf,','.join(candidates))
(P/'author-only-cook-working-models.json').write_text(json.dumps({'schema_version':1,'visibility':'author_only','items':items},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
