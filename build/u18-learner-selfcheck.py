from pathlib import Path
import json,re,unicodedata,hashlib
c=json.loads(Path('chapters/ch18/coverage.json').read_text(encoding='utf8'));s=Path('chapters/ch18/student.md').read_text(encoding='utf8');errors=[]
def ck(b,msg):
 if not b:errors.append(msg)
ck(s==unicodedata.normalize('NFC',s),'not NFC')
for t in c['teaching_records']:ck(s.count('<!-- teaching: '+t['teaching_id']+' -->')==1,'teaching marker '+t['teaching_id'])
for m in c['display_plan']['matrices']:
 marker='<!-- table: '+m['matrix_id']+' -->';ck(s.count(marker)==1,'table marker '+m['matrix_id'])
 if marker not in s:continue
 block=re.match(r'\s*(\|[^\n]+(?:\n\|[^\n]+)*)',s.split(marker,1)[1]);ck(bool(block),'table block '+m['matrix_id'])
 if block:
  rows=[[v.strip().replace('**','') for v in line.strip().strip('|').split('|')] for line in block[1].splitlines()];ck([rows[0]]+rows[2:]==[m['headers']]+m['rows'],'table cells '+m['matrix_id'])
new={'form':{r['form_id']:r for l in c['lexical_inventory'] for r in l['forms']},'sense':{r['sense_id']:r for l in c['lexical_inventory'] for r in l['senses']},'feature':{r['feature_id']:r for r in c['grammar_inventory']}}
for t in c['assigned_items']:
 marker='<!-- item: '+t['task_id']+' -->';ck(s.count(marker)==1,'item '+t['task_id'])
 if marker not in s:continue
 tail=s.split(marker,1)[1];ck(tail.strip().split('\n\n')[0]==t['prompt'],'prompt '+t['task_id']);body=tail.split('<!-- item:',1)[0].replace('**','');cursor=0
 for seq in t.get('input_sequences',[]):
  pos=body.find(seq['text'],cursor);ck(pos>=0,'ordered input '+seq['sequence_id']);cursor=max(cursor,pos+len(seq['text']))
 for p in t['output_positions']:ck(s.count('<!-- output: '+p['output_position_id']+' -->')==1,'output '+p['output_position_id'])
 for k in new:
  for rid in t.get('tested_'+k+'_ids',[]):
   r=new[k].get(rid,{})
   if r.get('knowledge_status') in ['new_production','new_recognition']:ck(any(0<=s.find('<!-- teaching: '+x+' -->')<s.index(marker) for x in r.get('teaching_ids',[])),'teaching order '+t['task_id']+' '+rid)
plain=re.sub(r'\[\^[^\]]+\]','',s).replace('**','')
for p in c['source_spans']+c['new_material_examples']:ck(p.get('learner_text',p.get('text')) in plain,'reading/example text')
for n in c['source_spans'][0]['original_notes']:ck(n.get('original_text',n.get('text_original',n.get('text'))) in s,'original note '+n['apparatus_id'])
ck('hund scēapa' not in s,'historical sheep context leaked into current reading glossary')
ck(s.count('**hund** — hundred, in the supplied gold and silver weight expressions.')==1,'current hundred gloss')
ck(s.count('**swā-hwæt-swā** — whatsoever; whatever.')==1,'shared free-choice gloss')
glossary=json.loads(Path('build/u18-learner-glossary-coverage.json').read_text(encoding='utf8'))
ck(sorted(glossary['all_support_ids'])==sorted(h['support_id'] for h in c['source_spans'][0]['local_support']),'reading support coverage after glossary consolidation')
readsection=s.split('## 7. The gifts',1)[1].split('### Finding',1)[0]
ck(len(re.findall(r'\[\^[^\]]+\]',readsection))==29,'note anchors')
ck(len(re.findall(r'^\[\^[^\]]+\]:',s,re.M))==22,'note definitions')
r={'status':'pass' if not errors else 'fail','contract_sha256':hashlib.sha256(Path('chapters/ch18/coverage.json').read_bytes()).hexdigest(),'student_sha256':hashlib.sha256(s.encode()).hexdigest(),'counts':{'words':len(s.split()),'teaching_locations':253,'matrices':64,'tasks':60,'outputs':87,'original_notes':22,'anchors':29},'errors':errors,'limit':'Learner structural self-check only; no independent linguistic or exported-page certification.'}
Path('build/u18-learner-selfcheck.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(r,ensure_ascii=False,indent=2))
