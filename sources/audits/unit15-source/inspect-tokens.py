import json,pathlib,re,unicodedata
OUT=pathlib.Path(__file__).parent; ROOT=OUT.resolve().parents[2]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
lex=read('lexicon/entries.json'); bysurface={}
for l in lex['lemmas']:
 for f in l['forms']:
  bysurface.setdefault(f['form'].lower(),[]).append({'lemma_id':l['lemma_id'],'form_id':f['form_id'],'analysis':f.get('analysis'),'form_status':'previously_taught' if f.get('production_taught_in') else 'previous_recognition' if f.get('recognition_taught_in') else 'previous_supplied','production_taught_in':f.get('production_taught_in'),'recognition_taught_in':f.get('recognition_taught_in'),'senses':[{'sense_id':s['sense_id'],'gloss':s['gloss'],'production_taught_in':s.get('production_taught_in'),'recognition_taught_in':s.get('recognition_taught_in')} for s in l['senses']]})
rows=[]
for span in read('sources/audits/unit15-source/reading-source.json')['source_spans']:
 print('\nSPAN',span['source_span_id'])
 for n,raw in enumerate(span['learner_text'].split(),1):
  token=raw.strip('.,;:!?“”‘’()');c=bysurface.get(token.lower(),[])
  rows.append({'token_id':span['source_span_id']+f'-T{n:03}','source_span_id':span['source_span_id'],'token_index':n,'source_token':raw,'surface':token,'baseline_candidates':c,'context_status':'pending_contextual_selection'})
  print(n,token,' | '.join(x['form_id']+':'+x['form_status'] for x in c) if c else 'NO SURFACE MATCH')
(OUT/'reading-token-candidates.json').write_text(json.dumps({'schema_version':1,'warning':'Candidates only. A shared spelling does not identify contextual morphology, sense or taught usage.','tokens':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('\nEXISTING NOUNS')
for l in lex['lemmas']:
 if l.get('part_of_speech')=='noun':print(l['lemma_id'],l['display_headword'],'; '.join(s['gloss']+':'+str(s.get('production_taught_in')) for s in l['senses']))
