import json, urllib.request
from pathlib import Path
O=Path('sources/audits/unit18-grammar')
L={x['lemma_id']:x for x in json.load(open('lexicon/entries.json',encoding='utf8'))['lemmas']}
for name in ['bycgan','gefyllan','settan','ingan','beraefian','gedon','liefan','libban','hlystan','wunian','cuman','beodan','geendian','get eon','geteon','beseon','behatan','forgiefan']:
 x=L.get(name)
 if not x: print(name,'ABSENT');continue
 fs=[{k:f.get(k) for k in ['form_id','form','analysis','production_taught_in','recognition_taught_in']} for f in x['forms'] if isinstance(f.get('analysis'),dict) and (f.get('analysis',{}).get('mood')!='indicative' or f.get('analysis',{}).get('person')==3)]
 print(json.dumps({'lemma':name,'senses':[{k:s.get(k)for k in ['sense_id','gloss','production_taught_in']}for s in x['senses']],'forms':fs},ensure_ascii=False))
for code in ['b0095','d0240','b0749','b0085']:
 p=O/('bt_'+code+'.jpg')
 if not p.exists():
  try:p.write_bytes(urllib.request.urlopen('https://bosworthtoller.com/images-dictionary/bt_'+code+'.jpg',timeout=50).read())
  except Exception as e:print(code,type(e).__name__,str(e));continue
 print('EVIDENCE_FILE',p,p.stat().st_size)
