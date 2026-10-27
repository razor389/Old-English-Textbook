"""Correct a contextual annotation in the reviewed replacement model only."""
import hashlib
import json
from pathlib import Path

def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
path='chapters/ch15/author-only-model-corrections.json'
d=read(path);s=next(s for s in d['corrected_sequences'] if s['owner_id']=='EX-IX-30-01')
changes=[]
for t in s['tokens']:
    if t['form_id']=='thurh-invariant-eth-source':
        old=t['contextual_analysis'].copy()
        t['contextual_analysis']['function']='preposition governing an accusative oath standard'
        changes.append({'token_index':t['token_index'],'before':old,'after':t['contextual_analysis']})
assert len(changes)==3
d['contextual_annotation_repairs']={'task_id':'EX-IX-30-01','changes':changes,
    'basis':'All three standards in the exact source prompt are things sworn by: heaven, earth and Jerusalem. The oath sense and u15-swerian-thurh frame already identify this use. Original form-record analysis and the frozen original sequence remain historical; contextual_analysis identifies this use.'}
write(path,d)
c=read('chapters/ch15/coverage.json')
c['selected_model_corrections']['sha256']=sha(path)
c['selected_model_corrections']['sha256_normalized_lf']=hashlib.sha256(Path(path).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
next(a for a in c['amendments'] if a['amendment_id']=='U15-AM03')['changes'].append('The three corrected30.1 ðurh tokens explicitly identify accusative oath standards in contextual_analysis; historical form analysis and original model are preserved.')
write('chapters/ch15/coverage.json',c)
r=read('sources/audits/unit15-coordinator/review-amendment-03.json')
r['model_correction_record']=c['selected_model_corrections']
r['contextual_annotation_recheck']=d['contextual_annotation_repairs']
write('sources/audits/unit15-coordinator/review-amendment-03.json',r)
print('Corrected three oath-standard contextual annotations; source history unchanged, canonical identities refreshed.')
