"""Complete context propagation for a scaffold reused by another Cook task."""
import json
from pathlib import Path
def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def write(path,x): Path(path).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
c=read('chapters/ch16/coverage.json')
assert not any(a['amendment_id']=='U16-A07' for a in c['amendments'])
changes=[]; matched=0
for p in read('build/u16-paradigms-context-findings.json')['repairs']:
    for task in c['assigned_items']:
        for seq in task.get('input_sequences',[]):
            if seq.get('source_model_sequence_id')!=p['sequence_id']: continue
            for token in seq['tokens']:
                if token.get('source_model_token_index')!=p['token_index']: continue
                matched+=1
                assert token['surface']==p['expected_surface']
                key=p['contextual_analysis_key']; old=token['contextual_analysis'].get(key)
                if old!=p['proposed_value']:
                    changes.append({'task_id':task['task_id'],'sequence_id':seq['sequence_id'],
                        'token_index':token['token_index'],'field':key,'before':old,'after':p['proposed_value'],
                        'source_model_sequence_id':p['sequence_id'],'source_model_token_index':p['token_index']})
                    token['contextual_analysis'][key]=p['proposed_value']
assert matched==16 and len(changes)==1
assert changes[0]['task_id']=='EX-XII-XIII-33-03'
a={'amendment_id':'U16-A07','date':'2026-10-27','stage':'independent_review',
   'coordinator':'root','reported_by':'unit16_paradigms','finding_id':'U16-PAR-03',
   'reason':'A supplied scaffold reused by33.3 points to the33.2 model; propagate the approved destination context across that explicit cross-task link as well.',
   'changes':changes,'verification':{'all_linked_input_contexts_checked':16,'remaining_discrepancies':0},
   'unchanged':['Every surface, form/sense ID and role','All model strings, prompts, tasks, teaching and counts','Sealed inputs and all previous correction files'],
   'review_status':'requires_independent_verification'}
c['amendments'].append(a); write('chapters/ch16/coverage.json',c)
ledger=read('chapters/ch16/authoring-amendments.json'); ledger['amendments'].append(a); write('chapters/ch16/authoring-amendments.json',ledger)
print('A07: all16 linked input contexts reconciled; one cross-task copy repaired.')
