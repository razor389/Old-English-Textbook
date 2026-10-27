"""One-use integration of reviewed Unit 15 into preserved cumulative records."""
import argparse, copy, hashlib, json
from pathlib import Path
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,x): Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
args=argparse.ArgumentParser()
args.add_argument('--apply',action='store_true')
args=args.parse_args()
c=read('chapters/ch15/coverage.json')
baseline=read('build/unit15-prior-baseline.json')
lex=copy.deepcopy(baseline['lexicon'])
gram=copy.deepcopy(baseline['grammar'])
def union(a,b):
    out=copy.deepcopy(a)
    for x in b:
        if x not in out: out.append(copy.deepcopy(x))
    return out
def integrate(old,new):
    old=copy.deepcopy(old or {})
    out=copy.deepcopy(old)
    out.update(copy.deepcopy(new))
    for name in ['teaching_ids','evidence_refs','used_in_tasks','assessed_in','prerequisite_feature_ids']:
        if name in old or name in new: out[name]=union(old.get(name,[]),new.get(name,[]))
    out['recognition_taught_in']=old.get('recognition_taught_in') or ('ch15' if new['knowledge_status'] in ['new_recognition','new_production'] else None)
    out['production_taught_in']=old.get('production_taught_in') or ('ch15' if new['knowledge_status']=='new_production' else None)
    out['supplied_in']=union(old.get('supplied_in',[]),['ch15'] if new['knowledge_status']=='supplied' else [])
    out['status']='reviewed'
    out['reviewed_in']='ch15'
    out['reviewed_chapters']=union(old.get('reviewed_chapters',[old['reviewed_in']] if old.get('reviewed_in') else []),['ch15'])
    out['review_record']='chapters/ch15/review.md'
    out['coverage_contract']='chapters/ch15/coverage.json'
    out['records_by_chapter']=copy.deepcopy(old.get('records_by_chapter',{}))
    if old and not out['records_by_chapter']:
        out['records_by_chapter'][old['reviewed_in']]=copy.deepcopy(old)
    out['records_by_chapter']['ch15']=copy.deepcopy(new)
    return out
lemmas={l['lemma_id']:l for l in lex['lemmas']}
for proposal in c['lexical_inventory']:
    lid=proposal['lemma_id']
    if lid not in lemmas:
        lemmas[lid]={k:copy.deepcopy(v) for k,v in proposal.items() if k not in ['forms','senses']}
        lemmas[lid].update(forms=[],senses=[])
        lex['lemmas'].append(lemmas[lid])
    lemma=lemmas[lid]
    if lid in {l['lemma_id'] for l in baseline['lexicon']['lemmas']}:
        metadata={k:copy.deepcopy(v) for k,v in lemma.items() if k not in ['forms','senses','metadata_by_chapter']}
        lemma.setdefault('metadata_by_chapter',{}).setdefault('through_ch14',metadata)
    lemma.setdefault('metadata_by_chapter',{})['ch15']={k:copy.deepcopy(v) for k,v in proposal.items() if k not in ['forms','senses']}
    for k,v in proposal.items():
        if k in ['source_spellings','notes'] and isinstance(v,list): lemma[k]=union(lemma.get(k,[]),v)
        elif k not in ['forms','senses']: lemma[k]=copy.deepcopy(v)
    for kind,key in [('forms','form_id'),('senses','sense_id')]:
        indexed={r[key]:r for r in lemma[kind]}
        for rec in proposal[kind]:
            old=indexed.get(rec[key])
            if old and kind=='forms': assert old['form']==rec['form'], (rec[key],old['form'],rec['form'])
            merged=integrate(old,rec)
            if old: lemma[kind][lemma[kind].index(old)]=merged
            else: lemma[kind].append(merged)
features={f['feature_id']:f for f in gram['features']}
for rec in c['grammar_inventory']:
    old=features.get(rec['feature_id'])
    merged=integrate(old,rec)
    if old: gram['features'][gram['features'].index(old)]=merged
    else: gram['features'].append(merged)
# The contract explicitly supplies a few earlier source records again without
# putting them in the new/promoted inventory. Record this exposure as well.
assigned_ids={'form':{f['form_id'] for l in c['lexical_inventory'] for f in l['forms']},
              'sense':{s['sense_id'] for l in c['lexical_inventory'] for s in l['senses']},
              'feature':{f['feature_id'] for f in c['grammar_inventory']}}
reused_supplied={kind:{} for kind in assigned_ids}
reused_taught_in_visible_help={kind:{} for kind in assigned_ids}
prior_records={
    'form':{r['form_id']:r for l in baseline['lexicon']['lemmas'] for r in l['forms']},
    'sense':{r['sense_id']:r for l in baseline['lexicon']['lemmas'] for r in l['senses']},
    'feature':{r['feature_id']:r for r in baseline['grammar']['features']}}
for kind in assigned_ids:
    for task in c['assigned_items']:
        for rid in task.get('supplied_'+kind+'_ids',[]):
            if rid not in assigned_ids[kind]:
                old=prior_records[kind][rid]
                # A complete supplied phrase can contain already taught words.
                # Visible help never demotes those identities or invents a new
                # supplied-only history; its usage remains in the contract.
                target=(reused_taught_in_visible_help if old.get('production_taught_in') or old.get('recognition_taught_in') else reused_supplied)
                target[kind].setdefault(rid,[]).append(task['task_id'])
for kind,records in reused_supplied.items():
    for rid,tasks in records.items():
        if kind=='feature':
            container=gram['features']; key='feature_id'
        else:
            key=kind+'_id'; field='forms' if kind=='form' else 'senses'
            container=next(l[field] for l in lex['lemmas'] if any(r[key]==rid for r in l[field]))
        old=next(r for r in container if r[key]==rid)
        assert not old.get('production_taught_in') and not old.get('recognition_taught_in'),rid
        # Find actual contracted teaching/support records for this reused identity.
        teaching=[r for r in c['teaching_records'] if rid in r.get(kind+'_ids',[])]
        assert teaching,(rid,'reused supplied identity has no contracted support location')
        ev=list(dict.fromkeys(e for r in teaching for e in r.get('evidence_refs',[])))
        assert ev,(rid,'reused supplied support has no evidence')
        rec={key:rid,'knowledge_status':'supplied','evidence_refs':ev,
             'teaching_ids':[r['teaching_id'] for r in teaching],
             'used_in_tasks':tasks,'assessed_in':[],
             'reuse_note':'The canonical Unit15 contract supplies this earlier record again; no recognition or production milestone is added.'}
        for preserved in ['form','analysis','gloss','description','scope_note']:
            if preserved in old:rec[preserved]=copy.deepcopy(old[preserved])
        container[container.index(old)]=integrate(old,rec)
for register in [lex,gram]:
    register['reviewed_chapters']=union(register['reviewed_chapters'],['ch15'])
    register['source_contracts']['ch15']='chapters/ch15/coverage.json'
    register['status']='Units 1–15 reviewed; earliest teaching and supplied-exposure history preserved; no milestones inherited from the archived experiment.'
    for eid,ev in c['evidence_catalog'].items():
        if eid in register['evidence_catalog']: assert register['evidence_catalog'][eid]==ev, ('evidence collision',eid)
        else: register['evidence_catalog'][eid]=copy.deepcopy(ev)
lex.setdefault('form_analysis_reconciliations_by_chapter',{})['ch15']=copy.deepcopy(c['form_identity_reconciliation'])
def flat(register,kind):
    return {r[kind[:-1]+'_id']:r for l in register['lemmas'] for r in l[kind]}
for old,new,key in [(flat(baseline['lexicon'],'forms'),flat(lex,'forms'),'form'),(flat(baseline['lexicon'],'senses'),flat(lex,'senses'),'sense'),({f['feature_id']:f for f in baseline['grammar']['features']},{f['feature_id']:f for f in gram['features']},'feature')]:
    assert set(old)<=set(new)
    for rid,record in old.items():
        after=new[rid]
        for milestone in ['recognition_taught_in','production_taught_in']:
            if record.get(milestone): assert after[milestone]==record[milestone],(rid,milestone)
        for values in ['supplied_in','evidence_refs','teaching_ids','used_in_tasks','assessed_in']:
            assert set(record.get(values,[]))<=set(after.get(values,[])),(rid,values)
        if record.get('reference_only'):
            assert after==record,(rid,'reference-only changed')
        if key=='form':
            assert after.get('analysis')==record.get('analysis'),(rid,'earlier analysis changed')
old_count={'lemmas':len(baseline['lexicon']['lemmas']),'forms':len(flat(baseline['lexicon'],'forms')),'senses':len(flat(baseline['lexicon'],'senses')),'features':len(baseline['grammar']['features'])}
new_count={'lemmas':len(lex['lemmas']),'forms':len(flat(lex,'forms')),'senses':len(flat(lex,'senses')),'features':len(gram['features'])}
metrics={'before':old_count,'after':new_count,'unit15_status_counts':{},'reused_supplied_records':reused_supplied,'reused_taught_in_visible_help':reused_taught_in_visible_help}
for kind,rows in [('forms',list(flat(lex,'forms').values())),('senses',list(flat(lex,'senses').values())),('features',gram['features'])]:
    metrics['unit15_status_counts'][kind]={'new_production':sum(r.get('production_taught_in')=='ch15' for r in rows),'new_recognition_only':sum(r.get('recognition_taught_in')=='ch15' and not r.get('production_taught_in') for r in rows),'supplied_here':sum('ch15' in r.get('supplied_in',[]) for r in rows)}
write('build/unit15-register-metrics.json',metrics)
write('build/unit15-lexicon-merged.json',lex)
write('build/unit15-grammar-merged.json',gram)
if args.apply:
    assert read('lexicon/entries.json') == baseline['lexicon'], 'Active lexicon changed since the frozen baseline; reconcile before integration'
    assert read('curriculum/grammar.json') == baseline['grammar'], 'Active grammar changed since the frozen baseline; reconcile before integration'
    assert c.get('presentation_review', {}).get('status') == 'accepted', 'Every-page presentation acceptance required'
    assert c.get('textual_review',{}).get('status')=='accepted','Independent textual acceptance required'
    write('lexicon/entries.json',lex)
    write('curriculum/grammar.json',gram)
    print('Reviewed registers integrated.')
else: print('Dry run only; active registers unchanged.')
print(json.dumps(metrics,ensure_ascii=False))
