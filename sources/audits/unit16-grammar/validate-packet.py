"""Deterministic identity/evidence closure; does not purport to prove linguistic truth."""
import json,hashlib,re
from pathlib import Path
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf8'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
errors=[];warnings=[]
L=read(R/'lexicon/entries.json')['lemmas'];G=read(R/'curriculum/grammar.json')['features']
PF={f['form_id']:(l['lemma_id'],f) for l in L for f in l['forms']}
PS={s['sense_id']:(l['lemma_id'],s) for l in L for s in l['senses']}
C=read(O/'evidence-catalog.json');CE={x['evidence_id']:x for x in C['records']}
allowed=set(CE)|set(C['external_evidence_refs']);unknown=set()
products=['grammar-records.json','principal-parts.json','lexical-frames.json','source-support.json','reading-verbal-support.json','author-only-cook-models.json','model-amendments.json','exercises-verbal-dependencies.json']
def walk(x):
    if isinstance(x,dict):
        for k,v in x.items():
            if k in ['evidence_refs','source_evidence_refs']:
                for ref in v:
                    if ref.startswith('U16-') and ref not in allowed:unknown.add(ref)
            if k=='origin_category' and v not in ['exact source','declared normalization','adaptation of a specific passage','new teaching material']:
                errors.append(['origin_category',v])
            walk(v)
    elif isinstance(x,list):
        for v in x:walk(v)
for name in products:walk(read(O/name))
for ref in sorted(unknown):errors.append(['missing_evidence',ref])
for record in C['records']:
    for image in record.get('images',[]):
        p=R/image['image_path']
        if not p.exists() or digest(p)!=image['image_sha256']:errors.append(['image_hash',record['evidence_id'],image['image_path']])
        if image.get('personally_viewed') is not True:errors.append(['unviewed_image_claim',record['evidence_id']])
N=read(O/'grammar-records.json');S=read(O/'source-support.json');RV=read(O/'reading-verbal-support.json')
for packet in [N,S,RV]:
    for l in packet['lemmas']:
        for f in l['forms']:
            if f['form_id'] in PF:
                pl,p=PF[f['form_id']]
                if l['lemma_id']!=pl or f['form']!=p['form'] or f['analysis']!=p['analysis']:errors.append(['prior_form_changed',f['form_id']])
                if f['knowledge_status']=='previously_taught' and not p.get('production_taught_in'):errors.append(['unsupported_prior_production',f['form_id']])
        for s in l['senses']:
            if s['sense_id'] in PS and s.get('prior_scope'):
                pl,p=PS[s['sense_id']]
                if l['lemma_id']!=pl or s['gloss']!=p['gloss']:errors.append(['prior_sense_changed',s['sense_id']])
    for kind,idkey in [('features','feature_id')]:
        ids=[x[idkey] for x in packet.get(kind,[])]
        if len(ids)!=len(set(ids)):errors.append(['duplicate_feature',packet.get('chapter')])
for p in N['paradigms']:
    ids=[x['form_id'] for x in p['forms']]
    if len(ids)!=len(set(ids)):errors.append(['duplicate_paradigm_cell',p['paradigm_id']])
    expected=12 if p['paradigm_id'].endswith('-IND') else 6 if p['paradigm_id'].endswith('-PRES-SUBJ') else 2
    if len(ids)!=expected:errors.append(['incomplete_bounded_paradigm',p['paradigm_id'],len(ids),expected])
M=read(O/'author-only-cook-models.json');P={x['source_item_id']:x for x in read(R/'sources/audits/unit16-source/exercises-prompts.json')['items']}
B=read(R/'curriculum/proposals/unit16/author-only-cook-sequence-bindings.json');BS={x['owner_id']:x for x in B['sequences']}
if len(M['items'])!=59 or {x['source_item_id']for x in M['items']}!=set(P):errors.append(['source_crosswalk'])
tokens=0;stale=[]
for m in M['items']:
    i=m['source_item_id'];q=BS.get(i,{})
    if m['source_prompt']!=P[i]['prompt']:errors.append(['prompt_changed',i])
    if q.get('text')!=m['model']:stale.append(i)
    else:
        ts=q.get('tokens',[]);tokens+=len(ts)
        if [t['token_index']for t in ts]!=list(range(1,len(ts)+1)):errors.append(['token_order',i])
        if ' '.join(t['literal']for t in ts)!=m['model']:errors.append(['token_reconstruction',i])
        for t in ts:
            if not all(t.get(k) for k in ['lemma_id','form_id','sense_id']):errors.append(['unbound_token',i,t.get('token_index')])
if stale:warnings.append({'models_awaiting_final_binding':stale})
C['unknown_references']=sorted(unknown)
(O/'evidence-catalog.json').write_text(json.dumps(C,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
out={'schema_version':1,'chapter':'ch16','status':'pass' if not errors and not warnings else 'pending_reconciliation' if not errors else 'fail','limits':'Checks exact source/record identities, bounded table completeness and reference closure. Linguistic interpretation remains separately reviewed against the actual images.','source_items':len(M['items']),'new_bounded_paradigms':len(N['paradigms']),'paradigm_cells':sum(len(p['forms'])for p in N['paradigms']),'evidence_records':len(C['records']),'ordered_tokens_on_current_models':tokens,'errors':errors,'warnings':warnings,'input_hashes':{str(p.relative_to(R)).replace('\\','/'):digest(p) for p in [R/'lexicon/entries.json',R/'curriculum/grammar.json',O/'initial-independent-models.json',R/'curriculum/proposals/unit16/author-only-cook-sequence-bindings.json']}}
(O/'validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({k:out[k]for k in ['status','errors','warnings','ordered_tokens_on_current_models']},ensure_ascii=False))
