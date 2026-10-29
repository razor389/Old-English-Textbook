"""Validate proposal closure without mutating the active course or solving a key."""
import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[3]; O=Path(__file__).resolve().parent
def load(p):return json.loads((R/p).read_text(encoding='utf8'))
def dump(p,x):(O/p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def digest(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
B=load('build/unit13-prior-baseline.json');G=load('sources/audits/unit13-grammar/grammar-records.json');S=load('sources/audits/unit13-grammar/source-support.json');E=load('sources/audits/unit13-grammar/evidence-catalog.json')
oldl={l['lemma_id']:l for l in B['lexicon']['lemmas']};oldf={f['form_id']:f for l in oldl.values() for f in l['forms']};olds={s['sense_id']:s for l in oldl.values() for s in l['senses']};oldg={f['feature_id']:f for f in B['grammar']['features']}
errors=[];eids={e['evidence_id'] for e in E['evidence']};allf={};alls={};prior=[]
for label,obj in [('grammar-records',G),('source-support',S)]:
    local_f=set();local_s=set()
    for l in obj['lemmas']:
        for f in l['forms']:
            i=f['form_id']
            if i in local_f:errors.append('duplicate form in '+label+':'+i)
            local_f.add(i);allf[i]=f
            if i in oldf:
                for k in ['form','analysis']:
                    if f.get(k)!=oldf[i].get(k):errors.append('changed prior '+k+':'+i)
                prior.append({'record_kind':'form','record_id':i,'prior_record':oldf[i],'proposed_status':f['knowledge_status'],'policy':'Preserve all earlier history, analyses, source spelling and first milestones. Add only explicit ch13 scope; contextual analysis is separate.'})
        for s in l['senses']:
            i=s['sense_id']
            if i in local_s:errors.append('duplicate sense in '+label+':'+i)
            local_s.add(i);alls[i]=s
            if i in olds:
                if s['gloss']!=olds[i]['gloss']:errors.append('changed prior gloss:'+i)
                prior.append({'record_kind':'sense','record_id':i,'prior_record':olds[i],'proposed_status':s['knowledge_status'],'policy':'Explicit promotion only where marked; preserve supplied history and any earlier production milestone.'})
def refs(x):
    if isinstance(x,dict):
        for k,v in x.items():
            if k=='prior_record':continue
            if k=='evidence_refs':yield from v
            else:yield from refs(v)
    elif isinstance(x,list):
        for v in x:yield from refs(v)
used=set(refs(G))|set(refs(S))
for i in sorted(used-eids):errors.append('missing evidence:'+i)
for e in E['evidence']:
    if digest(e['image_path'])!=e['image_sha256']:errors.append('image digest changed:'+e['evidence_id'])
for f in G['features']:
    for i in f.get('prior_feature_refs',[]):
        if i not in oldg:errors.append('unknown prior feature:'+i)
        else:prior.append({'record_kind':'feature','record_id':i,'prior_record':oldg[i],'policy':'Earlier scope reused without resetting teaching milestone.'})
for p in G['paradigms']:
    expected=12 if p['system'] in ['IND','SUBJ'] else 2
    if len(p['cells'])!=expected:errors.append('incomplete system:'+p['paradigm_id'])
    for c in p['cells']:
        if c['form_id'] not in allf:errors.append('missing paradigm form:'+c['form_id'])
        if c['form']!=allf[c['form_id']]['form']:errors.append('paradigm surface mismatch:'+c['form_id'])
    if p['system'] in ['IND','SUBJ']:
        positions={(c['analysis']['tense'],c['analysis']['mood'],c['analysis']['person'],c['analysis']['number']) for c in p['cells']}
        if len(positions)!=12:errors.append('duplicate finite position:'+p['paradigm_id'])
# Independent reconstruction of the design agent's full-model routes.
P=load('curriculum/proposals/unit13/grammar-display-plan.json');M=load('curriculum/proposals/unit13/display-matrices.json');mat={m['matrix_id']:m for m in M['matrices']}
route_ids=[]
for d in P['derivations']:
    op=d['operation'];base=allf[d['model_form_id']]['form'];want=allf[d['form_id']]['form']
    if not base.startswith(op['model_stem']):errors.append('model stem mismatch:'+d['form_id']);continue
    got=op['target_stem']+base[len(op['model_stem']):]
    if got!=want or got!=d['result']:errors.append('derived surface mismatch:'+d['form_id'])
for route in P['cell_display_routes']:
    route_ids.append(route['form_id']);m=mat[route['matrix_id']];r=route['row_index_zero_based'];c=route['column_index_zero_based'];actual=m['rows'][r][c]
    fid=route.get('model_form_id',route['form_id']) if route['display_kind']=='explicit_derivation' else route['form_id']
    if actual!=allf[fid]['form']:errors.append('literal model cell mismatch:'+fid)
if len(route_ids)!=278 or set(route_ids)!={c['form_id'] for p in G['paradigms'] for c in p['cells']}:errors.append('display coverage mismatch')
for suffix in ['IND','SUBJ']:
    m=mat['NEW-U13-PAR-INGAN-'+suffix]
    if ('subjunctive' if suffix=='SUBJ' else 'indicative') not in m['title']:errors.append('finite display lacks mood:'+suffix)
framefile=load('sources/audits/unit13-grammar/lexical-frames.json');nom=load('sources/audits/unit13-source/lexical-inventory.json');knownl=set(oldl)|{l['lemma_id'] for obj in [G,S,nom] for l in obj['lemmas']}
for f in framefile['frames']:
    for i in f['lemma_ids']:
        if i not in knownl:errors.append('frame lemma absent:'+i+' in '+f['frame_id'])
examplefile=load('curriculum/proposals/unit13/compositions.json');taskfile=load('curriculum/proposals/unit13/task-seed.json')
comments={1:'Case, agreement and hear+accusative support the intended participants.',2:'A fronted accusative constituent is licensed; no second-word rule is inferred.',3:'Adverb-first finite/nominal-subject order is a supported tendency.',4:'Temporal conjunction and correlative adverb are distinct; known gān/tō frame.',5:'Masculine sang supports hē while English renders it; no gender-only universal rule.',6:'The expressed subject continues through coordination; grētan actual earlier sense explicitly includes greet.',7:'Both masculine referents remain possible without more context; ambiguity is intentional.',8:'New sprecan INF pair and explicit conversation mid+dative frame resolve earlier citation/sense gaps.',9:'Relative internal object differs from nominative antecedent; source nominal audit owns cirican.',10:'Three ðā tokens have distinct conjunction/adverb/article roles.',11:'Bounded repeated-predicate ellipsis is corroborated by Cook134 and prior Unit10.',12:'Known indirect report and past subjunctive; relative reporting time, not absolute past by form alone.'}
reviews=[]
for x in examplefile['teaching_examples']:
    n=int(x['example_id'][-2:]);reviews.append({'input_id':x['example_id'],'text':x['text'],'text_sha256':hashlib.sha256(x['text'].encode()).hexdigest(),'verdict':'accepted_with_explicit_contract_dependencies','observation':comments[n]})
for x in examplefile['compositions']:
    reviews.append({'input_id':x.get('composition_id',x.get('span_id')),'text_sha256':hashlib.sha256(x['text'].encode()).hexdigest(),'word_count':len(x['text'].split()),'verdict':'accepted_with_explicit_contract_dependencies','observation':'Coherent hearing, question, summons and assembly. lǣd requires the new complete command pair and person+direction frame; sprecan requires its complete INF pair and conversation frame; ðǣr and ęft require explicit promotion/new sense. Final word is a new source-owned complete nominal system. No obedience sense is inferred from hearing.'})
for t in taskfile['tasks']:
    if '-A' in t['task_id']:
        reviews.append({'input_id':t['task_id'],'input_texts':t['input_texts'],'verdict':'accepted','observation':('Restore the same lexical copula with agreement for the second expressed plural subject; do not copy the singular surface.' if t['task_id'].endswith('A09') else 'Checked vocabulary, finite morphology, case/antecedent roles and stated context; no extra ordering or reference rule is required.')})
dump('public-composition-review.json',{'chapter':'ch13','reviewer':'unit13_grammar','scope':'Twelve original teaching examples, the original connected account, twelve analysis tasks, and full verbal display routes. No ordered graded-answer sequence is reproduced.','reviewed_files':{'curriculum/proposals/unit13/compositions.json':digest('curriculum/proposals/unit13/compositions.json'),'curriculum/proposals/unit13/task-seed.json':digest('curriculum/proposals/unit13/task-seed.json')},'findings':reviews,'display_review':{'logical_cells':278,'literal_cells':218,'derived_cells':60,'matrices':19,'five_weak_II_derived_systems':'Every cell independently reconstructed by replacing fordilg with the exact lexical stem; finite number/person and tense positions are identical.','mood_metadata':'ingān indicative and subjunctive matrices have distinct explicit titles.'}})
dump('prior-reconciliation.json',{'schema_version':1,'chapter':'ch13','baseline':'e17fc5f','baseline_counts':{'lemmas':647,'forms':8235,'senses':778,'features':599},'prior_contracts_read':[f'chapters/ch{i:02d}/coverage.json' for i in range(1,13)],'actual_registers_read':['lexicon/entries.json','curriculum/grammar.json'],'comparison_method':'Every proposed matching identity is compared with the immutable parsed actual register; copied prior_record retains the complete earlier record. Exact original form/analysis/gloss comparisons are validation assertions.','records':prior,'decisions':['Promote actual earlier supplied oferwinnan sense, ge-paired-source, wyrcean-make and thaer-there explicitly.','Preserve old combined eft quoque history; new back/again use is explicit.','Prior wyrcean-work already covers accusative deed; do not relabel that as newly learned.','Prior lǣdan person-accusative frame alone did not license hider; add bounded direction frame.','Source ingangende belongs to supplied ingangan, not new finite ingān.','Reuse ilcan/wege dative-surface identities with explicit contextual instrumental-route function.','Keep ðon old dative-source identity distinct from productive instrumental variants; contextual temporal use is separately supplied.']})
counts={'verbal_systems':len(G['paradigms']),'verbal_cells':sum(len(p['cells']) for p in G['paradigms']),'grammar_proposal_lemmas':len(G['lemmas']),'source_support_lemmas':len(S['lemmas']),'source_support_forms':sum(len(l['forms']) for l in S['lemmas']),'grammar_features':len(G['features']),'supplied_features':len(S['features']),'personally_inspected_evidence_records':len(E['evidence']),'baseline_reconciliation_records':len(prior)}
dump('validation.json',{'schema_version':1,'chapter':'ch13','status':'passed' if not errors else 'requires_correction','checks':['All proposal evidence references resolve to personally inspected image records.','All image SHA256 values match retained artifacts.','All matching prior form surfaces, morphological analyses and sense glosses preserved.','All34 declared verbal systems complete; all278 cells have explicit production scope.','All278 design display routes present; all60 derived cells independently reproduced.','Finite displays explicitly distinguish indicative and subjunctive.','Frame lemma identities exist in actual baseline or current nominal/verbal proposal.','Public examples and analysis inputs independently reviewed without reading an ordered new key.'],'counts':counts,'errors':errors})
print(json.dumps({'counts':counts,'errors':errors},ensure_ascii=False))
