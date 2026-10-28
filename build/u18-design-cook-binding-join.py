from pathlib import Path
from collections import defaultdict
import copy
import json
import unicodedata

OUT=Path('curriculum/proposals/unit18')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def norm(s):return unicodedata.normalize('NFC',s.strip('.,;:!?“”‘’\"()')).casefold()
def morph(a):
    if not isinstance(a,dict):return {}
    vm={'nominative':'nom','genitive':'gen','dative':'dat','accusative':'acc','instrumental':'ins','singular':'sg','plural':'pl','masculine':'m','feminine':'f','neuter':'n'}
    return {('declension' if k=='strength' else k):vm.get(v,v) if isinstance(v,str) else v for k,v in a.items()}
def state(r):
    if r.get('production_taught_in'):return 'previously_taught'
    if r.get('recognition_taught_in'):return 'prior_recognition'
    return r.get('knowledge_status','unresolved')
lex=read('lexicon/entries.json');inv=read(OUT/'inventory.json')
forms={f['form_id']:(l['lemma_id'],f) for l in lex['lemmas'] for f in l['forms']}
senses={s['sense_id']:(l['lemma_id'],s) for l in lex['lemmas'] for s in l['senses']}
for l in inv['lemmas']:
    forms.update({f['form_id']:(l['lemma_id'],f) for f in l['forms']});senses.update({s['sense_id']:(l['lemma_id'],s) for s in l['senses']})
by_surface=defaultdict(list)
for fid,(lid,f) in forms.items():by_surface[norm(f['form'])].append((lid,f))
choices=read(OUT/'author-only-nonverbal-selections.json')
verbs={r['source_item_id']:{o.get('token_position_one_based',o.get('position')):o for o in r['verbal_occurrences']} for r in read('sources/audits/unit18-grammar/candidate-verbal-bindings.json')['rows']}
models=read('sources/audits/unit18-grammar/candidate-models.json')['rows']
sequences=[]; unresolved=[]
for m in models:
    tid=m['source_item_id'];short='.'.join(str(int(x)) for x in tid.split('-')[-2:]);choice=choices['rows'].get(short,{})
    seq={'sequence_id':tid+'-MODEL','owner_id':tid,'kind':'author_only_output','text':m['model'],'tokens':[],'context_review':choice.get('review'),'dependency_status':'unresolved'}
    for i,word in enumerate(m['model'].split(),1):
        matches=by_surface[norm(word)];spec=choice.get('forms',{}).get(str(i));context=choice.get('contexts',{}).get(str(i));v=verbs.get(tid,{}).get(i)
        sid=choice.get('senses',{}).get(str(i));selected=None;analysis=None
        if v and norm(v['surface'])==norm(word):
            context=v.get('current_context_analysis',v.get('contextual_analysis',v['analysis']))
            if v['form_id'] in forms and norm(forms[v['form_id']][1]['form'])==norm(word):selected=forms[v['form_id']]
            else:
                good=[(l,f) for l,f in matches if l==v['lemma_id'] and all(morph(f.get('contextual_analysis',f['analysis'])).get(k)==val for k,val in morph(context).items())]
                if len(good)==1:selected=good[0]
            if v.get('sense_id'):sid=v['sense_id']
            elif v.get('proposed_sense'):sid=v['proposed_sense']['sense_id']
            if not sid and len(v.get('prior_productive_senses',[]))==1:sid=v['prior_productive_senses'][0]['sense_id']
        elif spec:
            if ':' in spec:
                lid,code=spec.split(':',1);bits=code.split('.');want=dict(zip(['case','number','gender','declension'],bits))
                matches=[(l,f) for l,f in matches if l==lid and all(morph(f.get('contextual_analysis',f['analysis'])).get(k)==val for k,val in want.items())]
                context=context or want
            elif spec in forms:
                selected=forms[spec]
                if norm(selected[1]['form'])!=norm(word):unresolved.append({'task_id':tid,'position':i,'word':word,'kind':'selected_surface_mismatch','selected_form_id':spec});selected=None
            else:matches=[]
        elif norm(word)=='ðe':
            selected=forms['the-relative-invariant']
        elif norm(word)=='mid':
            selected=forms['mid-invariant-source']
        elif norm(word)=='his':
            selected=forms['he-m-gen-sg']
        elif norm(word)=='hwæðer':
            selected=forms['hwaether-conjunction-invariant']
        elif norm(word)=='tō':
            selected=forms['to-preposition-dative-invariant']
        elif norm(word) in choices['default_lemma_choices']:
            matches=[(l,f) for l,f in matches if l==choices['default_lemma_choices'][norm(word)]]
        if selected is None and len(matches)==1:selected=matches[0]
        if selected is None and len(matches)>1:
            # Exact morphology duplicates are retained separately in the registers;
            # prefer an already productive identity only when the contextual analyses agree.
            morphsets={json.dumps(morph(f.get('contextual_analysis',f['analysis'])),sort_keys=True) for l,f in matches}
            if len({l for l,f in matches})==1 and len(morphsets)==1:
                good=[(l,f) for l,f in matches if state(f)=='previously_taught']
                if len(good)==1:selected=good[0]
        if selected:
            lid,f=selected
            if not sid:sid=choices['default_sense_choices'].get(lid)
            if lid=='he' and morph(f.get('contextual_analysis',f['analysis'])).get('case')=='gen' and str(i) not in choice.get('senses',{}):sid='he-possessor'
            ss=[(s_id,s) for s_id,(slid,s) in senses.items() if slid==lid]
            if not sid:
                prod=[(s_id,s) for s_id,s in ss if state(s) in ['previously_taught','new_production']]
                if len(prod)==1:sid=prod[0][0]
                elif len(ss)==1:sid=ss[0][0]
            if sid not in senses or senses[sid][0]!=lid:
                unresolved.append({'task_id':tid,'position':i,'word':word,'kind':'sense','lemma_id':lid,'selected_sense_id':sid,'choices':[(s_id,s.get('contextual_gloss',s['gloss']),state(s)) for s_id,s in ss]});sid=None
            token={'token_index':i,'literal':word,'surface':word.strip('.,;:!?“”‘’\"()'),'lemma_id':lid,'form_id':f['form_id'],'sense_id':sid,
                'analysis':copy.deepcopy(f['analysis']),'contextual_analysis':copy.deepcopy(context or f.get('contextual_analysis',f['analysis'])),
                'form_status':state(f),'sense_status':state(senses[sid][1]) if sid else 'unresolved',
                'context_review_basis':'Explicit grammar occurrence audit' if v else choice.get('review'),
                'assessment_role':'unclassified_until_hint_and_local_help_join'}
            if state(f) not in ['previously_taught','new_production']:unresolved.append({'task_id':tid,'position':i,'word':word,'kind':'form_requires_visible_support_or_promotion','form_id':f['form_id'],'status':state(f)})
            if sid and state(senses[sid][1]) not in ['previously_taught','new_production']:unresolved.append({'task_id':tid,'position':i,'word':word,'kind':'sense_requires_visible_support_or_promotion','sense_id':sid,'status':state(senses[sid][1])})
        else:
            token={'token_index':i,'literal':word,'surface':word.strip('.,;:!?“”‘’\"()'),'form_id':None,'sense_id':None,'status':'unresolved'}
            unresolved.append({'task_id':tid,'position':i,'word':word,'kind':'form','spec':spec,'choices':[(lid,f['form_id'],f.get('contextual_analysis',f['analysis'])) for lid,f in matches]})
        seq['tokens'].append(token)
    sequences.append(seq)
result={'schema_version':1,'chapter':'ch18','visibility':'AUTHOR ONLY. Exclude from fresh blind learner solving.','status':'work_in_progress_contextual_binding; no assessment closure claimed','sequences':sequences,'unresolved':unresolved}
(OUT/'author-only-cook-sequence-bindings.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=defaultdict(int)
for r in unresolved:summary[r['kind']]+=1
print(json.dumps({'rows':len(sequences),'tokens':sum(len(s['tokens']) for s in sequences),'unresolved':dict(summary),'context_reviewed_nonverbal_rows':len(choices['rows'])},indent=2))
