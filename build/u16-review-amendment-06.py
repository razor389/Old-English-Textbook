"""Use the taught whether-question route and reconcile linked input contexts."""
import copy,hashlib,json
from pathlib import Path
def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def write(path,x): Path(path).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def identity(path):
    raw=Path(path).read_bytes()
    return {'path':path,'sha256':hashlib.sha256(raw).hexdigest(),'sha256_normalized_lf':hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest()}
c=read('chapters/ch16/coverage.json')
assert not any(a['amendment_id']=='U16-A06' for a in c['amendments'])
previous_ref=c['selected_model_corrections']; previous=read(previous_ref['path'])
assert previous_ref==identity(previous_ref['path'])
source=previous['source']; base={s['owner_id']:s for s in read(source)['sequences']}
models=copy.deepcopy(base)
for s in previous['corrected_sequences']: models[s['owner_id']]=copy.deepcopy(s)
tid='EX-XII-XIII-34-06'; task=next(t for t in c['assigned_items'] if t['task_id']==tid)
seq=models[tid]; old_seq=copy.deepcopy(seq)
token=seq['tokens'][11]
assert token['surface']==token['literal']=='gif' and token['form_id']=='gif-invariant'
lex=read('lexicon/entries.json'); gram=read('curriculum/grammar.json')
oldlemma=next(l for l in lex['lemmas'] if l['lemma_id']=='hwaether-conjunction')
form=next(f for f in oldlemma['forms'] if f['form_id']=='hwaether-conjunction-invariant')
sense=next(s for s in oldlemma['senses'] if s['sense_id']=='hwaether-whether')
feature=next(g for g in gram['features'] if g['feature_id']=='u09-dependent-whether')
assert all(r['production_taught_in']=='ch09' for r in [form,sense,feature])
assert form['form']=='hwæðer'
token.update(literal='hwæðer',surface='hwæðer',lemma_id='hwaether-conjunction',
    form_id=form['form_id'],sense_id=sense['sense_id'],analysis=copy.deepcopy(form['analysis']),
    contextual_analysis={'invariant':True,'function':'conjunction introducing the dependent yes/no question after sęcge'},
    prior_form_production='ch09',prior_sense_production='ch09')
words=seq['text'].split(); assert words[11]=='gif'; words[11]='hwæðer'; seq['text']=' '.join(words)
for kind,oldid,newid in [('form','gif-invariant',form['form_id']),('sense','gif-if',sense['sense_id'])]:
    for holder in [seq,task,*task['output_positions']]:
        for name in ['required_'+kind+'_ids','required_output_'+kind+'_ids','tested_'+kind+'_ids']:
            if name in holder:
                assert oldid in holder[name],(kind,name)
                holder[name]=sorted({newid if x==oldid else x for x in holder[name]})
    oldrec=next(r for l in c['lexical_inventory'] for r in l[kind+'s'] if r[kind+'_id']==oldid)
    for name in ['used_in_tasks','assessed_in']:
        if tid in oldrec.get(name,[]): oldrec[name].remove(tid)
for holder in [task,*task['output_positions']]:
    holder['required_feature_ids']=sorted(set(holder.get('required_feature_ids',[])+[feature['feature_id']]))
    holder['tested_feature_ids']=sorted(set(holder.get('tested_feature_ids',[])+[feature['feature_id']]))
before_note=task['grading_obligations']['interpretation_and_control_audit']
assert 'gif introduces the whether-content' in before_note
task['grading_obligations']['interpretation_and_control_audit']=before_note.replace('gif introduces the whether-content','previously taught hwæðer introduces the dependent whether-question')
recall=next(t for t in c['teaching_records'] if t['teaching_id']=='NEW-U16-PRIOR-RECALL')
newlemma=copy.deepcopy(oldlemma)
newlemma['prior_lemma']=True; newlemma['prior_lemma_present']=True
newlemma['scope_note']='Reuse of the previously productive ch09 dependent-question conjunction; distinct from the inflected choice-of-two pronoun. No new gif-whether sense is assigned.'
for kind,record in [('form',form),('sense',sense),('feature',feature)]:
    r=copy.deepcopy(record)
    r.update(knowledge_status='previously_taught',teaching_ids=['NEW-U16-PRIOR-RECALL'],
        used_in_tasks=[tid],assessed_in=[tid],
        prior_scope={'production_taught_in':'ch09','recognition_taught_in':'ch09','coverage_contract':'chapters/ch09/coverage.json'})
    if kind=='feature': c['grammar_inventory'].append(r)
    else: newlemma[kind+'s']=[r]
    idkey=kind+'_id'
    recall[kind+'_ids']=sorted(set(recall.get(kind+'_ids',[])+[r[idkey]]))
    c['prior_requirements'][kind+'_ids']=sorted(set(c['prior_requirements'][kind+'_ids']+[r[idkey]]))
    recall['evidence_refs']=sorted(set(recall.get('evidence_refs',[])+r['evidence_refs']))
    for eid in r['evidence_refs']:
        e=lex.get('evidence_catalog',{}).get(eid,gram.get('evidence_catalog',{}).get(eid))
        assert e is not None
        if eid in c['evidence_catalog']: assert c['evidence_catalog'][eid]==e
        else: c['evidence_catalog'][eid]=copy.deepcopy(e)
c['lexical_inventory'].append(newlemma)
for key in ['lemmas','forms','senses','features']: c['explicit_scope_metrics'][key]+=1

# A05 also governs exact supplied-input copies linked to those model positions.
mirrors=[]
for p in read('build/u16-paradigms-context-findings.json')['repairs']:
    current_task=next(t for t in c['assigned_items'] if t['task_id']==p['task_id'])
    for input_seq in current_task.get('input_sequences',[]):
        if input_seq.get('source_model_sequence_id')!=p['sequence_id']: continue
        for t in input_seq['tokens']:
            if t.get('source_model_token_index')!=p['token_index']: continue
            assert t['surface']==p['expected_surface']
            key=p['contextual_analysis_key']; old=t['contextual_analysis'].get(key)
            if old==p['proposed_value']: continue
            mirrors.append({'task_id':p['task_id'],'sequence_id':input_seq['sequence_id'],
                'token_index':t['token_index'],'source_model_token_index':p['token_index'],
                'field':key,'before':old,'after':p['proposed_value']})
            t['contextual_analysis'][key]=p['proposed_value']
affected=sorted(t for t in models if models[t]!=base[t])
path='chapters/ch16/model-binding-final-amendments.json'
record={
 'chapter_id':'ch16','amendment_id':'U16-A06','status':'applied_after_independent_findings',
 'source':source,'source_sha256':identity(source)['sha256'],'source_sha256_normalized_lf':identity(source)['sha256_normalized_lf'],
 'previous_correction_record':previous_ref,
 'reason':'Select previously taught hwæðer for34.6 dependent whether-question; the former gif-if binding did not teach that sense.',
 'changed_model':{'task_id':tid,'before':old_seq,'after':seq},
 'corrections':[{'task_id':t,'original_sequence':base[t],'original_text':base[t]['text'],'corrected_text':models[t]['text']} for t in affected],
 'corrected_sequences':[models[t] for t in affected],
 'linked_input_context_corrections':mirrors,
 'counts':{'all_sequences':59,'all_tokens':812,'cumulative_override_sequences':len(affected),
     'model_words_replaced_here':1,'linked_input_context_fields':len(mirrors)},
 'scope':'One replacement with already productive ch09 knowledge; no new milestone, task, paradigm or learner help is needed. All unchanged A03/A05 overrides remain in force.'}
write(path,record); c['selected_model_corrections']=identity(path)
amendment={
 'amendment_id':'U16-A06','date':'2026-10-27','stage':'independent_review','coordinator':'root',
 'reported_by':['unit16_blind','unit16_paradigms'],'original_contract_checkpoint':'543e214',
 'complete_drafts_checkpoint':'9b75319','blind_solutions_checkpoint':'1bf0e8e',
 'reason':record['reason'],'correction_record':c['selected_model_corrections'],
 'previous_correction_record':previous_ref,'counts':record['counts'],
 'prior_teaching':{'chapter':'ch09','learner_location':'chapters/ch09/student.md:73',
    'form_id':form['form_id'],'sense_id':sense['sense_id'],'feature_id':feature['feature_id'],
    'evidence_refs':feature['evidence_refs']},
 'input_context_note':'Mirror the37 approved A05 contextual descriptions into the exact linked supplied-input tokens where applicable; retain every original text, ID and assessment role.',
 'linked_input_context_corrections':mirrors,
 'unchanged':['Exact original Cook English and source reading/apparatus','All task/output counts and paradigm cells',
    'All new productive/recognition milestones','Sealed base packet, historical A03/A05 correction records and frozen blind witness'],
 'review_status':'requires_independent_verification'}
c['amendments'].append(amendment); write('chapters/ch16/coverage.json',c)
ledger=read('chapters/ch16/authoring-amendments.json'); ledger['amendments'].append(amendment); write('chapters/ch16/authoring-amendments.json',ledger)
print(record['counts']); print(seq['text'])
