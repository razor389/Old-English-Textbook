from pathlib import Path
import json,sys
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
mode=sys.argv[1] if len(sys.argv)>1 else 'validation'
if mode=='support':
    d=load('sources/audits/unit13-grammar/source-support.json')
    print(list(d))
    print(json.dumps([(l['lemma_id'],[(f['form_id'],f['form']) for f in l.get('forms',[])],[s['sense_id'] for s in l.get('senses',[])]) for l in d['lemmas']],ensure_ascii=False))
    print(json.dumps(d.get('source_evidence_examples'),ensure_ascii=False))
elif mode=='grammar-help':
    d=load('sources/audits/unit13-grammar/source-support.json')
    print(json.dumps(d.get('local_support'),ensure_ascii=False))
    print(json.dumps(load('sources/audits/unit13-grammar/principal-parts.json'),ensure_ascii=False))
elif mode=='forms':
    wanted=set(sys.argv[2:])
    for p in ['lexicon/entries.json','sources/audits/unit13-grammar/grammar-records.json','sources/audits/unit13-grammar/source-support.json']:
        print(p)
        print(json.dumps([(l['lemma_id'],{k:f.get(k) for k in ['form_id','form','analysis','production_taught_in','recognition_taught_in','knowledge_status','scope_note']}) for l in load(p)['lemmas'] for f in l.get('forms',[]) if f['form'] in wanted],ensure_ascii=False))
elif mode=='validation':
    print(json.dumps(load('curriculum/proposals/unit13/validation.json'),ensure_ascii=False))
elif mode=='schemas':
    for p in ['sources/audits/unit13-source/evidence-catalog.json','sources/audits/unit13-grammar/evidence-catalog.json','curriculum/proposals/unit13/prior-audit.json']:
        d=load(p);print(p,list(d));print(json.dumps(list(d.items())[:2],ensure_ascii=False)[:1000])
        if 'evidence' in d:
            ev=d['evidence'];print(json.dumps(list(ev.items())[:1] if isinstance(ev,dict) else ev[:1],ensure_ascii=False))
        if 'registers' in d:print(json.dumps(d['registers'],ensure_ascii=False))
elif mode=='cook':
    print(json.dumps(load('curriculum/proposals/unit13/author-only-cook-sequence-bindings.json')['issues'],ensure_ascii=False))
elif mode=='cook-support':
    d=load('curriculum/proposals/unit13/author-only-cook-sequence-bindings.json')
    for s in d['sequences']:
        ts=[(t['surface'],t['form_id'],t['form_status'],t['sense_id'],t['sense_status']) for t in s['tokens'] if t['form_status'] not in ['new_production','previously_taught'] or t['sense_status'] not in ['new_production','previously_taught']]
        if ts:print(json.dumps([s['owner_id'],ts],ensure_ascii=False))
elif mode=='tasks':
    print(json.dumps([(t['task_id'],t['prompt'],t['requested_outputs']) for t in load('curriculum/proposals/unit13/task-seed.json')['tasks'][:6]],ensure_ascii=False))
elif mode=='grammar':
    d=load('sources/audits/unit13-grammar/grammar-records.json')
    print(json.dumps([(p['paradigm_id'],p.get('scope'),[(c['form_id'],c['knowledge_status']) for c in p['cells'] if c['knowledge_status']!='new_production']) for p in d['paradigms']],ensure_ascii=False))
    print(json.dumps([l for l in d['lemmas'] if l['lemma_id']=='forceorfan'],ensure_ascii=False))
elif mode=='constructions':
    d=load('sources/audits/unit13-source/construction-requirements.json')
    print(list(d))
    print(json.dumps(d['requirements'][:5],ensure_ascii=False))
    from collections import Counter
    print(Counter(r.get('knowledge_status') for r in d['requirements']))
elif mode=='senses':
    wanted=set(sys.argv[2:])
    for p in ['lexicon/entries.json','sources/audits/unit13-grammar/grammar-records.json','sources/audits/unit13-grammar/source-support.json']:
        print(p)
        print(json.dumps([(l['lemma_id'],[{k:s.get(k) for k in ['sense_id','gloss','production_taught_in','recognition_taught_in','knowledge_status','scope_note']} for s in l.get('senses',[])]) for l in load(p)['lemmas'] if l['lemma_id'] in wanted],ensure_ascii=False))
elif mode=='prior-features':
    needed=set()
    for t in load('curriculum/proposals/unit13/task-plan.json')['tasks']:needed.update(t.get('required_feature_ids',[]))
    print(json.dumps([f for f in load('curriculum/grammar.json')['features'] if f['feature_id'] in needed],ensure_ascii=False))
