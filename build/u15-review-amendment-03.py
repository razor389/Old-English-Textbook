"""Canonical corrections from independent task review; sealed proposals stay unchanged."""
import copy
import hashlib
import json
from pathlib import Path

def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def lfsha(p):return hashlib.sha256(Path(p).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
def write(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def replace_once(text,old,new):
    assert text.count(old)==1,(old,text.count(old))
    return text.replace(old,new,1)
assert sha('chapters/ch15/independent-solutions.md')=='2abad21bf90cf8994afbb7e48ec0807b74ab3d1e4cddf80cb30513845ca592fe'
c=read('chapters/ch15/coverage.json');lex=read('lexicon/entries.json');gram=read('curriculum/grammar.json')
assert not any(a['amendment_id']=='U15-AM03' for a in c['amendments'])
tasks={t['task_id']:t for t in c['assigned_items']}
forms={f['form_id']:f for ls in [lex['lemmas'],c['lexical_inventory']] for l in ls for f in l['forms']}
features={f['feature_id']:f for f in gram['features']}
path='curriculum/proposals/unit15/author-only-cook-sequence-bindings.json'
models={s['owner_id']:s for s in read(path)['sequences']}
corrected=[];changes=[]

def token_form(t,fid):
    f=forms[fid];t['form_id']=fid;t['surface']=f['form'];t['analysis']=copy.deepcopy(f['analysis'])
    t['contextual_analysis']=copy.deepcopy(f['analysis'])
    t['form_status']='previously_taught' if f.get('production_taught_in') else f['knowledge_status']

for tid in ['EX-IX-30-01','EX-X-XI-31-13']:
    s=copy.deepcopy(models[tid]);original=copy.deepcopy(s)
    if tid=='EX-IX-30-01':
        i=next(i for i,t in enumerate(s['tokens']) if t['form_id']=='maere-gen-m-sg-weak')
        assert s['tokens'][i-1]['form_id']=='se-m-gen-sg'
        del s['tokens'][i-1];t=s['tokens'][i-1]
        token_form(t,'maere-gen-m-sg-strong');t['literal']='mǣres'
        remove={'maere-gen-m-sg-weak','se-m-gen-sg'};add={'maere-gen-m-sg-strong'}
        basis='Cook30.1 explicitly omits the article before both city and great king. Bare mǣres cyninges uses the complete strong mǣre system already taught in this unit.'
    else:
        t=s['tokens'][2];assert t['form_id']=='he-f-dat-sg' and t['literal']=='hiere,'
        token_form(t,'he-f-acc-sg');t['literal']='hīe,'
        remove={'he-f-dat-sg'};add={'he-f-acc-sg'}
        basis='Actual Unit13 āscian teaching and Cook276b→§159b on93 require the selected accusative person. Hīe replaces unsupported dative hiere; later hīe still refers to the book.'
    s['text']=' '.join(t['literal'] for t in s['tokens'])
    for i,t in enumerate(s['tokens'],1):t['token_index']=i
    s['required_form_ids']=sorted({t['form_id'] for t in s['tokens']})
    s['required_sense_ids']=sorted({t['sense_id'] for t in s['tokens']})
    s['canonical_correction']={'amendment':'U15-AM03','basis':basis,'supersedes_only':original['sequence_id']}
    s['auditor_notes']=[basis]
    corrected.append(s)
    changes.append({'task_id':tid,'original_text':original['text'],'corrected_text':s['text'],
                    'original_sequence':original,'basis':basis,'removed_form_ids':sorted(remove),'added_form_ids':sorted(add)})
    task=tasks[tid]
    for field in ['required_form_ids','required_output_form_ids','tested_form_ids']:
        task[field]=sorted((set(task[field])-remove)|add)
    for pos in task['output_positions']:
        pos['required_form_ids']=sorted((set(pos['required_form_ids'])-remove)|add)
    task['auditor_item_requirements']['token_binding_source']='chapters/ch15/author-only-model-corrections.json#'+s['sequence_id']
    task['canonical_review_resolution']={'amendment':'U15-AM03','basis':basis,'original_audit_preserved':path}

task=tasks['EX-IX-30-01']
oldf,newf='u15-system-maere-weak-ngda','u15-system-maere-strong-ngda'
for field in ['required_feature_ids','tested_feature_ids']:
    task[field]=sorted((set(task[field])-{oldf})|{newf})
for pos in task['output_positions']:
    pos['required_feature_ids']=sorted((set(pos['required_feature_ids'])-{oldf})|{newf})
for field in ['original_controls_and_interpretation','targets']:
    task['auditor_item_requirements'][field]=[v.replace('weak mǣre','strong mǣre after the stated article omissions') for v in task['auditor_item_requirements'][field]]
task['target_specification']+=' Omit both indicated articles; use strong genitive mǣres with bare cyninges.'
task['grading_obligations']['target']=task['target_specification']
task['grading_obligations']['likely_errors']+=' Inserting ðæs before mǣran cyninges violates the second article-omission control; the bare phrase requires strong mǣres.'
for l in c['lexical_inventory']:
    for f in l['forms']:
        if f['form_id'] in ['maere-gen-m-sg-strong','maere-gen-m-sg-weak']:
            for field in ['used_in_tasks','assessed_in']:
                f[field]=[x for x in f.get(field,[]) if x!='EX-IX-30-01']
                if f['form_id'].endswith('strong'):f[field].append('EX-IX-30-01')
for f in c['grammar_inventory']:
    if f['feature_id'] in [oldf,newf]:
        for field in ['used_in_tasks','assessed_in']:
            f[field]=[x for x in f.get(field,[]) if x!='EX-IX-30-01']
            if f['feature_id']==newf:f[field].append('EX-IX-30-01')
        if f['feature_id']==oldf:
            f['scope_note']+=' Complementary productive lexical morphology transfers the explicitly taught Unit3 weak-adjective and e-stem rules, exemplified there by æppelbǣre. No distinct weak-mǣre output is claimed here;30.1 assesses the strong genitive.'

task=tasks['EX-X-XI-31-13'];fid='u13-ascian-person-thing'
for field in ['required_feature_ids','tested_feature_ids']:
    task[field]=sorted(set(task[field])|{fid})
task['output_positions'][0]['required_feature_ids']=sorted(set(task['output_positions'][0]['required_feature_ids'])|{fid})
for field in ['original_controls_and_interpretation','targets']:
    task['auditor_item_requirements'][field]=[v.replace('ask dative','ask an accusative person') for v in task['auditor_item_requirements'][field]]
task['grading_obligations']['likely_errors']+=' Using a dative person with āscian would miss the previously taught accusative-person frame.'
for fid in ['u13-ascian-person-thing','u03-weak-adjectives','u03-e-stem']:
    if not any(f['feature_id']==fid for f in c['prior_requirements']['features']):
        assert features[fid].get('production_taught_in')
        r=copy.deepcopy(features[fid]);r['prior_status']='previously_taught';c['prior_requirements']['features'].append(r)

aid='U15-COOK-NOM-28-04'
helptext='Strǣt here means “public place”, with the earlier feminine declension. Cook’s reference (169) selects the earlier perception construction: use accusative ōðre with the plain infinitive standan. In28.7, by contrast, the printed direction explicitly requests a present participle.'
helptext=helptext.replace('In28.7','In 28.7')
for r in tasks['EX-IX-28-04']['local_support']+c['teaching_records']:
    if r.get('support_id')==aid:
        r['text']=helptext;r['kind']='lexical_and_target_orientation'
        r['evidence_refs']=sorted(set(r['evidence_refs'])|{'U15-G-FB97'}) if 'U15-G-FB97' in c['evidence_catalog'] else r['evidence_refs']

boundary={
 'production_morphology':'The requested forms are productive morphology targets from taught systems. Any expressly supplied help remains available and is not independently recalled. English explanations do not promote untaught Old English forms.',
 'production_composition':'The Old English composition targets independently usable taught forms, senses and constructions. Any explicitly supplied material remains available; its unaided recall is not a target.',
 'recognition_analysis':'Interpret and explain the actual given inputs using taught recognition and any visible supplied help. English analysis does not itself establish productive Old English use.',
 'supported_reading':'Read, interpret and translate the exact source with its visible lexical and construction help. Supplied forms and meanings are not independently recalled; comprehension does not promote every encountered form to production.'
}
boundary_changes=[]
for task in c['assigned_items']:
    if task['task_id'].startswith('NEW-U15-'):
        before=task['assessment_boundary'];task['assessment_boundary']=boundary[task['mode']]
        boundary_changes.append({'task_id':task['task_id'],'mode':task['mode'],'before':before,'after':task['assessment_boundary']})
task=tasks['EX-IX-30-11']
task['grading_obligations']['defensible_alternatives']+=' The isolated should can admit a coherent present expectation/obligation with sculon beside selected modal sceoldon. A subjunctive wish changes modality and is not automatically equivalent.'

correction_path='chapters/ch15/author-only-model-corrections.json'
record={'chapter_id':'ch15','private':True,'pre_key_excluded':True,'amendment_id':'U15-AM03',
        'rule':'Original sealed models remain unchanged. Only the two named selected sequences are superseded; the replacement tokens, dependencies and grading targets are canonical.',
        'source':path,'source_sha256':sha(path),'source_sha256_normalized_lf':lfsha(path),
        'corrections':changes,'corrected_sequences':corrected}
write(correction_path,record)
c['selected_model_corrections']={'path':correction_path,'sha256':sha(correction_path),'sha256_normalized_lf':lfsha(correction_path)}
c['pre_key_review_exclusions'].append(correction_path)
c['amendments'].append({'amendment_id':'U15-AM03','date':'2026-10-27','stage':'after blind checkpoint ecbdc44, independent comparison',
    'reason':'Independent task review found two selected-model errors and unclear target/scope labels.',
    'changes':['30.1 now uses mǣres cyninges, preserving both source article omissions; model tokens, form/system dependencies and direct assessment move to strong mǣre.',
               '31.13 now uses accusative hīe with the actually taught āscian frame; model tokens, dependencies and copied audit targets reconciled.',
               '28.4 makes the earlier §169 perception-infinitive target explicit; its public-place sense is labelled taught, not merely supplied.',
               '30.11 key explains contextual modal choices without mechanically equating English should with past time.',
               'All55 original task assessment boundaries are specialized by mode; tasks, prompts and322 requested outputs remain unchanged.'],
    'model_corrections':correction_path,
    'complementary_weak_maere':'Retained as explicit productive morphology transferred from actual Unit3 weak/e-stem teaching, including æppelbǣre and its tested æppelbǣran. No distinct weak-mǣre output claimed; full table remains visible. The frozen design remains historical evidence.',
    'withdrawn_concern':'Funde in28.7 is valid selected third-singular morphology explicitly taught inUnit4 and corroborated by Wright258. Fand is also valid; no correction required.',
    'boundary_changes':boundary_changes,'review_status':'pending_independent_recheck'})
write('chapters/ch15/coverage.json',c)

p=Path('chapters/ch15/student.md');s=p.read_text(encoding='utf-8')
s=replace_once(s,'Strǣt here means “public place”, with the earlier feminine declension.',helptext)
p.write_text(s,encoding='utf-8',newline='\n')
p=Path('chapters/ch15/answer-key.md');s=p.read_text(encoding='utf-8')
for change in changes:s=replace_once(s,change['original_text'],change['corrected_text'])
s=replace_once(s,'**on strǣte** is the supplied public-place use without an article.','**on strǣte** uses the newly taught public-place sense without an article.')
s=replace_once(s,'The great king is **ðæs mǣran cyninges**, genitive dependent on burg.','The great king is **mǣres cyninges**, genitive dependent on burg. Cook directs omission of both articles: the bare genitive phrase takes strong **mǣres**, not article-led weak ðæs mǣran.')
needle='**Ānum uncer** is one recipient selected from us two:'
s=replace_once(s,needle,'**Hīe** after āscode is the accusative person asked, following the Unit 13 government frame. **Ānum uncer** is one recipient selected from us two:')
needle='The noun hām is distinct from the earlier homewards adverb; the modal complements remain infinitives, not participles.'
s=replace_once(s,needle,needle+' The model takes should as modal ought to, using **sceoldon**. English should is not a mechanical instruction to place the event in the past: a coherent present expectation or obligation can use **sculon**. A subjunctive wish such as **scylen** changes the modality and needs an explicit wish reading.')
p.write_text(s,encoding='utf-8',newline='\n')
report={'amendment_id':'U15-AM03','status':'applied_pending_independent_recheck','blind_checkpoint':'ecbdc44',
    'model_correction_record':c['selected_model_corrections'],
    'primary_image_reinspections':[{'path':p,'raw_sha256':sha(p),'actually_viewed':True,'observer':'root','observation':note} for p,note in [
      ('sources/audits/unit12-grammar/cook_fb_1895_2-p93.png','§159b explicitly marks ðē as accusative with āxian, supporting the taught accusative-person frame.'),
      ('sources/audits/unit12-source/cook_fb_1895_2-p276.png','Column b āscian/āxian cross-refers to §159b.'),
      ('sources/audits/unit15-coordinator/cook-ex17-600.png','30.1 visibly has (om.the) before city and before great king.30.11 has should in both repeated road clauses without a fuller temporal setting.')]],
    'witness_sha256_unchanged':sha('chapters/ch15/independent-solutions.md'),
    'preservation':'No sealed audit/proposal, earlier chapter or blind witness changed.'}
write('sources/audits/unit15-coordinator/review-amendment-03.json',report)
print('Applied AM03:two selected models/dependencies corrected;28.4 guidance,30.11 modal note and55 scope boundaries clarified. All105 prompts/322 outputs preserved.')
