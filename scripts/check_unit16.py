"""Repeatable Unit16 structural/dependency/export checks; independent linguistic review remains required."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import unicodedata

ROOT=Path(__file__).resolve().parents[1]
ERRORS=[]
PRIOR={f'ch{n:02}' for n in range(1,16)}
def require(ok,message):
    if not ok: ERRORS.append(message)
def read(path): return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))
def surf(s): return s.strip('.,:;!?“”‘’"()').casefold()
def identity(path,r):
    p=ROOT/path
    if not p.is_file():return False
    raw=p.read_bytes()
    return hashlib.sha256(raw).hexdigest()==r.get('sha256') or hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest()==r.get('sha256_normalized_lf')
def unique(rows,key):
    out={}
    for r in rows:
        require(r[key] not in out,'Duplicate '+r[key]);out[r[key]]=r
    return out
def main():
    ap=argparse.ArgumentParser(__doc__)
    ap.add_argument('--contract',default='chapters/ch16/coverage.json')
    ap.add_argument('--draft',action='store_true');ap.add_argument('--tex',action='store_true')
    ap.add_argument('--candidate',action='store_true',help='Permit unfinished lifecycle/input hashes only; all content checks still run.')
    args=ap.parse_args();c=read(args.contract);metrics=c['contract_metrics']
    lex=read('lexicon/entries.json');gram=read('curriculum/grammar.json')
    old={'form':{r['form_id']:r for l in lex['lemmas'] for r in l['forms']},'sense':{r['sense_id']:r for l in lex['lemmas'] for r in l['senses']},'feature':{r['feature_id']:r for r in gram['features']}}
    new={'form':unique([r for l in c['lexical_inventory'] for r in l['forms']],'form_id'),'sense':unique([r for l in c['lexical_inventory'] for r in l['senses']],'sense_id'),'feature':unique(c['grammar_inventory'],'feature_id')}
    owners={k:{r[k+'_id']:l['lemma_id'] for ls in [lex['lemmas'],c['lexical_inventory']] for l in ls for r in l[field]} for k,field in [('form','forms'),('sense','senses')]}
    teach=unique(c['teaching_records'],'teaching_id');ev=c['evidence_catalog']
    for register in [lex,gram]:
        for eid,e in register.get('evidence_catalog',{}).items():
            if eid in ev:require(ev[eid]==e,'Earlier evidence altered '+eid)
    def rec(k,rid):return new[k].get(rid,old[k].get(rid))
    def status(k,rid):
        if rid in new[k]:return new[k][rid]['knowledge_status']
        r=old[k].get(rid,{})
        if r.get('production_taught_in') in PRIOR:return 'previously_taught'
        if r.get('recognition_taught_in') in PRIOR:return 'prior_recognition'
        return 'supplied' if r.get('supplied_in') else 'unresolved'
    for k,rows in new.items():
        for rid,r in rows.items():
            require(r.get('knowledge_status') in {'previously_taught','prior_recognition','new_production','new_recognition','supplied'},rid+': invalid status')
            require(bool(r.get('evidence_refs')),rid+': missing evidence')
            require(bool(r.get('teaching_ids')),rid+': missing teaching')
            for eid in r.get('evidence_refs',[]):require(eid in ev,rid+': unknown evidence '+eid)
            for tid in r.get('teaching_ids',[]):require(tid in teach,rid+': unknown teaching '+tid)
    for k,field in [('form','forms'),('sense','senses')]:
        oo={r[k+'_id']:l['lemma_id'] for l in lex['lemmas'] for r in l[field]}
        nn={r[k+'_id']:l['lemma_id'] for l in c['lexical_inventory'] for r in l[field]}
        for rid in oo.keys()&nn.keys():
            require(oo[rid]==nn[rid],rid+': changed existing lemma owner')
            if k=='form':require(old[k][rid]['form']==new[k][rid]['form'],rid+': changed existing form surface')
    for eid,e in ev.items():
        images=list(e.get('images',[]))
        for field in ['image_path','page_image']:
            if isinstance(e.get(field),str):images.append({'path':e[field],'sha256':e.get('image_sha256')})
        if e.get('image'):images+=e['image'] if isinstance(e['image'],list) else [e['image']]
        for im in images:
            path=im.get('path',im.get('image_path')) if isinstance(im,dict) else im
            exists=(ROOT/path).is_file()
            require(exists or (eid=='U02-DUAL' and (ROOT/e['record']).is_file()),eid+': missing image '+path)
            if exists and isinstance(im,dict) and isinstance(im.get('sha256',im.get('image_sha256')),str):require(identity(path,{'sha256':im.get('sha256',im.get('image_sha256'))}),eid+': changed image')
    tasks=unique(c['assigned_items'],'task_id')
    require(len(tasks)==len(c['key_item_ids'])==len(set(c['key_item_ids']))==metrics['tasks'],'Expected contract task/key count')
    require(set(c['key_item_ids'])=={t['key_id'] for t in tasks.values()},'Task/key crosswalk')
    prompts={r['source_item_id']:r['prompt'] for r in read('sources/audits/unit16-source/exercises-prompts.json')['items']}
    require({tid:t['prompt'] for tid,t in tasks.items() if tid.startswith('EX-')}==prompts and len(prompts)==59,'Exact59 Cook prompts')
    position_ids=[]
    for tid,t in tasks.items():
        require(t['dependency_status']=='closed',tid+': dependencies open')
        require(bool(t['output_positions']),tid+': no output positions')
        position_ids.extend(p['output_position_id'] for p in t['output_positions'])
        for k in new:
            required=set(t.get('required_'+k+'_ids',[]))
            supplied=set(t.get('supplied_'+k+'_ids',[]));tested=set(t.get('tested_'+k+'_ids',[]))
            require(supplied|tested<=required,tid+': targets/support outside requirements '+k)
            for rid in required:require(status(k,rid)!='unresolved',tid+': unresolved '+rid)
            allowed={'previously_taught','new_production'}
            if any(word in t['mode'] for word in ['analysis','reading','recognition','comprehension']):allowed|={'prior_recognition','new_recognition'}
            for rid in tested:
                current_allowed=allowed|({'prior_recognition','new_recognition'} if k=='feature' and rid in t.get('metalinguistic_feature_ids',[]) else set())
                require(status(k,rid) in current_allowed,tid+': untaught tested '+rid)
            for pos in t['output_positions']:require(set(pos.get('required_'+k+'_ids',[]))<=required,tid+': output dependency outside task '+k)
    require(len(position_ids)==len(set(position_ids))==metrics['requested_output_positions'],'Requested output positions')
    matrices=unique(c['display_plan']['matrices'],'matrix_id')
    routes=c['display_plan']['paradigm_cell_display_routes']
    cells={(p['paradigm_id'],v.get('cell_id',v.get('form_id'))):v for p in c['paradigms'] for v in p['cells']}
    require(len(cells)==sum(len(p['cells']) for p in c['paradigms'])==metrics['logical_cells'],'Logical cell count/identity')
    require(len(routes)==metrics['literal_routes']==len(cells),'One literal route per logical cell')
    require(len(matrices)==metrics['matrices']==len(c['paradigms']),'Complete matrix/system counts')
    seen=[];components=[];nulls=0
    for r in routes:
        pair=(r['paradigm_id'],r['logical_cell_id']);seen.append(pair)
        require(pair in cells,'Route lacks logical cell '+str(pair))
        m=matrices[r['matrix_id']];ri=r['row_index_zero_based'];ci=r['column_index_zero_based']
        require(m['rows'][ri][ci]==r['surface'],'Route surface differs '+str(pair))
        require(m['cell_logical_ids'][ri][ci]==r['logical_cell_id'],'Route coordinate differs '+str(pair))
        require(m['cell_form_ids'][ri][ci]==r['form_ids'],'Route components differ '+str(pair))
        fs=r['form_ids'];components.extend(fs)
        if not fs:
            nulls+=1;require(r['surface'] in {'—','Unassigned'},'Unassigned cell lacks explicit label')
        else:
            records=[rec('form',fid) for fid in fs]
            require(all(records),'Missing component identity '+str(pair))
            if all(records):require(surf(' '.join(x['form'] for x in records))==surf(r['surface']),'Composite/literal display surface differs '+str(pair))
    require(Counter(seen)==Counter(cells.keys()),'Missing/repeated logical display routes')
    require(nulls==metrics['unassigned_table_slots'],'Unassigned slot count')
    require(len(cells)-nulls==metrics['literal_form_cells'],'Literal form cell count')
    require(len(components)==metrics['component_form_occurrences'],'Component occurrence count')
    require(Counter(components)==Counter(r['form_id'] for r in c['display_plan']['component_form_routes']),'Component route multiset')
    require(metrics['derived_cells']==0,'All assigned systems require literal display')
    routekeys=set(cells)
    for t in tasks.values():
        for pos in t['output_positions']:
            if pos['kind']=='form':
                pair=(pos.get('paradigm_id'),pos.get('cell_id'))
                require(pair in routekeys,t['task_id']+': form output has no actual cell '+str(pair))
    def sequence(seq,label):
        text=seq.get('learner_text',seq.get('text',''));tokens=seq['tokens'];words=text.split()
        require(len(words)==len(tokens),label+': token count differs')
        for word,t in zip(words,tokens):
            if t.get('kind',t.get('token_type'))=='punctuation':continue
            fids=t.get('form_ids',[t.get('form_id')]);sid=t.get('sense_id')
            for fid in fids:
                r=rec('form',fid)
                require(r is not None and surf(r['form'])==surf(word),label+': form surface '+str(fid))
                require(owners['form'].get(fid)==owners['sense'].get(sid)==t.get('lemma_id'),label+': form/sense owner '+word)
    for t in tasks.values():
        for seq in t.get('input_sequences',[]):sequence(seq,t['task_id'])
    passages=c['source_spans']+c['new_material_examples']+c['new_compositions']
    for seq in passages:sequence(seq,seq.get('source_span_id',seq.get('example_id','example')))
    require(len(c['new_material_examples'])==4 and not c['new_compositions'],'Four examples/no new narrative')
    originals=read('sources/audits/unit16-source/reading-source.json')['source_spans']
    require(len(originals)==len(c['source_spans'])==1,'One complete source scene')
    for r,orig in zip(c['source_spans'],originals):require(r['learner_text'].split()==orig['learner_text'].split(),'Exact source passage differs')
    require([len(r['tokens']) for r in c['source_spans']]==[444],'Source444 tokens')
    require(sum(len(r['original_notes']) for r in c['source_spans'])==54,'Original54 notes')
    require(sum(len(r['original_note_anchors']) for r in c['source_spans'])==59,'Original59 note anchors')
    modelpath=ROOT/'curriculum/proposals/unit16/author-only-cook-sequence-bindings.json'
    models={s['owner_id']:s for s in read(modelpath.relative_to(ROOT).as_posix())['sequences']} if modelpath.is_file() else {}
    if c.get('selected_model_corrections'):
        correction_ref=c['selected_model_corrections']
        require(identity(correction_ref['path'],correction_ref),'Selected model correction record changed')
        correction=read(correction_ref['path'])
        require(identity(correction['source'],{'sha256':correction['source_sha256'],'sha256_normalized_lf':correction['source_sha256_normalized_lf']}),'Original model packet changed')
        original_changes={x['task_id']:x for x in correction['corrections']}
        require(len(original_changes)==len(correction['corrected_sequences']),'Correction inventory mismatch')
        for seq in correction['corrected_sequences']:
            tid=seq['owner_id'];change=original_changes[tid]
            require(models[tid]==change['original_sequence'],tid+': original model history differs')
            require(models[tid]['text']==change['original_text'] and seq['text']==change['corrected_text'],tid+': correction text mismatch')
            models[tid]=seq
    require(set(models)==set(prompts),'All59 ordered Cook models bound')
    for tid,s in models.items():
        sequence(s,tid)
        require({t['form_id'] for t in s['tokens']}<=set(tasks[tid]['required_output_form_ids']),tid+': model output forms absent')
        require({t['sense_id'] for t in s['tokens']}<=set(tasks[tid]['required_output_sense_ids']),tid+': model output senses absent')
    dispositions={}
    for n in range(1,17):
        chapter=c if n==16 else read(f'chapters/ch{n:02}/coverage.json')
        for t in chapter['assigned_items']:
            if t['task_id'].startswith('EX-'):dispositions[t['task_id']]='assigned'
        for field,state in [('deferred_source_items','deferred'),('excluded_source_items','excluded')]:
            for r in chapter.get(field,[]):
                if r.get('source_item_id','').startswith('EX-'):dispositions[r['source_item_id']]=state
    require(len(dispositions)==644 and Counter(dispositions.values())=={'assigned':515,'deferred':129},'515/129/0 canonical crosswalk')
    if not args.candidate:
        for r in c['analysis_inputs']:require(identity(r['path'],r),'Frozen input changed '+r['path'])
    for path,digest in c['prior_files'].items():
        if path not in {'lexicon/entries.json','curriculum/grammar.json'}:require(identity(path,{'sha256':digest,'sha256_normalized_lf':c['prior_files_lf_sha256'].get(path)}),'Prior artifact changed '+path)
    if args.draft or args.tex:
        student=(ROOT/'chapters/ch16/student.md').read_text(encoding='utf-8');key=(ROOT/'chapters/ch16/answer-key.md').read_text(encoding='utf-8')
        for label,text in [('student',student),('key',key)]:require(text==unicodedata.normalize('NFC',text),label+': not NFC')
        for teaching_id in teach:
            require('<!-- teaching: '+teaching_id+' -->' in student,'Actual teaching location absent '+teaching_id)
        for mid,m in matrices.items():
            marker='<!-- table: '+mid+' -->';require(student.count(marker)==1,mid+': actual table marker')
            if marker in student:
                block=re.match(r'\s*(\|[^\n]+(?:\n\|[^\n]+)*)',student.split(marker,1)[1]);require(bool(block),mid+': actual table absent')
                if block:
                    rows=[[v.strip().replace('**','') for v in line.strip().strip('|').split('|')] for line in block[1].splitlines()]
                    require([rows[0]]+rows[2:]==[m['headers']]+m['rows'],mid+': actual table differs')
        for tid,t in tasks.items():
            marker='<!-- item: '+tid+' -->';km='<!-- key: '+t['key_id']+' -->'
            require(student.count(marker)==1,tid+': learner item marker');require(key.count(km)==1,tid+': key marker')
            if marker in student:
                tail=student.split(marker,1)[1];prompt=tail.strip().split('\n\n')[0]
                require(prompt==t['prompt'],tid+': actual prompt differs')
                body=tail.split('<!-- item:',1)[0].replace('**','');cursor=0
                for s in t.get('input_sequences',[]):
                    at=body.find(s['text'],cursor);require(at>=0,tid+': ordered input missing');cursor=max(cursor,at+len(s['text']))
            if km in key and tid in models:
                actual=key.split(km,1)[1].strip().split('\n\n',1)[0].replace('**','')
                require(actual==models[tid]['text'],tid+': actual Cook key model differs')
        plain=re.sub(r'\[\^[^\]]+\]','',student).replace('**','')
        for p in passages:
            text=p.get('learner_text',p.get('text',''));require(text in plain,'Actual passage/example missing '+p.get('source_span_id',p.get('example_id','example')))
        for r in c['source_spans']:
            for n in r['original_notes']:require(n.get('text_original',n.get('text',n.get('original_text'))) in student.replace('**',''),'Original note absent')
    if args.tex:
        folder=ROOT/'typesetting/ch16'
        for stem,ids in [('chapter-16',list(tasks)),('answer-key',c['key_item_ids'])]:
            tex=(folder/(stem+'.tex')).read_text(encoding='utf8');pdftext=(folder/'build'/(stem+'.txt')).read_text(encoding='utf8');log=(folder/'build'/(stem+'.log')).read_text(encoding='utf8',errors='replace')
            require((folder/(stem+'.pdf')).is_file(),stem+': missing retained PDF')
            for rid in ids:require(rid in tex,rid+': TeX marker absent')
            for warning in ['Missing character:','Overfull \\hbox','Overfull \\vbox','Underfull \\hbox','Underfull \\vbox','Font shape','Rerun to get','Table widths have changed']:require(warning not in log,stem+': '+warning)
            if stem=='chapter-16':
                chars=lambda s:re.sub(r'\s+','',s.replace('\u00ad','-'))
                for t in tasks.values():require(chars(t['prompt']) in chars(pdftext),t['task_id']+': PDF prompt differs')
    if ERRORS:
        print('\n'.join('ERROR: '+e for e in ERRORS));raise SystemExit(1)
    print(f"Unit16 checks pass:{len(tasks)} tasks,{len(position_ids)} outputs,59 exact Cook prompts,444 reading tokens,54 notes/59 anchors; dependencies/displays/evidence/prior artifacts checked.")
if __name__=='__main__':main()
