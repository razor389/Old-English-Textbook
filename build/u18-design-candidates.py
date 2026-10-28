from pathlib import Path
from collections import defaultdict
import json,unicodedata
O=Path('curriculum/proposals/unit18')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def norm(s):return unicodedata.normalize('NFC',s.strip('.,;:!?“”‘’"()')).casefold()
L=read('lexicon/entries.json')
entries={l['lemma_id']:l for l in L['lemmas']}
F={f['form_id']:(l['lemma_id'],f) for l in L['lemmas'] for f in l['forms']}
S={s['sense_id']:(l['lemma_id'],s) for l in L['lemmas'] for s in l['senses']}
for path,key in [('sources/audits/unit18-source/noun-adjective-paradigms.json','paradigms'),('sources/audits/unit18-grammar/verbal-systems.json','systems')]:
    for p in read(path)[key]:
        F.update({f['form_id']:(p['lemma_id'],f) for f in p['cells']})
        if p.get('sense_proposal'):S[p['sense_proposal']['sense_id']]=(p['lemma_id'],p['sense_proposal'])
for s in read('sources/audits/unit18-source/nominal-sense-audit.json')['senses']:S[s['sense_id']]=(s['lemma_id'],s)
if (O/'inventory.json').exists():
    I=read(O/'inventory.json')
    for l in I['lemmas']:
        entries[l['lemma_id']]=l
        F.update({f['form_id']:(l['lemma_id'],f) for f in l['forms']})
        S.update({s['sense_id']:(l['lemma_id'],s) for s in l['senses']})
surf=defaultdict(list)
for fid,(lid,f) in F.items():surf[norm(f['form'])].append((lid,f))
vb={}
vp=Path('sources/audits/unit18-grammar/candidate-verbal-bindings.json')
if vp.exists():
    packet=read(vp)
    for row in packet.get('rows',packet.get('items',[])):
        vb[row.get('source_item_id',row.get('item_id'))]={v.get('token_position_one_based',v.get('position')):v for v in row['verbal_occurrences']}
def status(r):
    if r.get('production_taught_in'):return 'previously_taught'
    if r.get('recognition_taught_in'):return 'prior_recognition'
    return r.get('knowledge_status','supplied' if r.get('supplied_in') else 'unresolved')
packet=read('sources/audits/unit18-grammar/candidate-models.json')
rows=[];missing={}
for row in packet.get('rows',packet.get('items',[])):
    tid=row.get('source_item_id',row.get('item_id'));tokens=[]
    for i,w in enumerate(row['model'].split(),1):
        if i in vb.get(tid,{}):
            v=vb[tid][i]
            assert norm(v['surface'])==norm(w),(tid,i,w,v)
            tokens.append({'position':i,'word':w,'verbal_binding':v});continue
        cs=[]
        for lid,f in surf[norm(w)]:
            cs.append({'lemma_id':lid,'form_id':f['form_id'],'analysis':f.get('contextual_analysis',f['analysis']),'status':status(f),'senses':[{'sense_id':sid,'gloss':s.get('contextual_gloss',s['gloss']),'status':status(s)} for sid,(ls,s) in S.items() if ls==lid]})
        tokens.append({'position':i,'word':w,'candidates':cs})
        if not cs:missing.setdefault(norm(w),[]).append(tid)
    rows.append({'source_item_id':tid,'model':row['model'],'tokens':tokens})
(O/'author-only-cook-identity-candidates.json').write_text(json.dumps({'visibility':'AUTHOR ONLY; finding aid, not certification','rows':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'models':len(rows),'tokens':sum(len(r['tokens']) for r in rows),'unmatched_surfaces':missing},ensure_ascii=False,indent=2))
