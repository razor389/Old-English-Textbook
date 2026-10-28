"""Reconcile the operative correction overlay with its final visible support routes."""
import copy,hashlib,json
from pathlib import Path
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def union(a,b):return list(dict.fromkeys(a+b))
c=read('chapters/ch18/coverage.json');assert not c.get('textual_review')
history=read('chapters/ch18/support-amendment-history.json');assert 'assessment_route_followup' not in history
path='chapters/ch18/selected-model-corrections.json';overlay=read(path)
record={'reported_by':'unit18_blind','reason':'The operative corrected_sequences retained draft independent-assessment annotations even though final canonical tokens supplied those positions. Reconcile every operative route; preserve original_sequence and the initial correction stage.','overlay_sha256_before':sha(path),'initial_corrected_sequences':copy.deepcopy(overlay['corrected_sequences']),'changed_tokens':[]}
tasks={t['task_id']:t for t in c['assigned_items']}
for tid,task in tasks.items():
    supports=[h for h in task.get('local_support',[]) if h.get('amendment_id')=='U18-A05']
    if not supports:continue
    for token in task['assessed_output_tokens']:
        routes=[h['support_id'] for h in supports if token['token_index'] in h['output_token_positions_one_based']]
        if routes:
            for field in ['reference_route_ids','sense_reference_route_ids']:
                token[field]=union(token.get(field,[]),routes)
            record['changed_tokens'].append({'task_id':tid,'position':token['token_index'],'routes':routes})
    for seq in task['input_sequences']:
        if seq.get('amendment_id')!='U18-A05':continue
        for token in seq['tokens']:
            for field in ['reference_route_ids','sense_reference_route_ids']:
                token[field]=union(token.get(field,[]),[seq['sequence_id']])
for seq in overlay['corrected_sequences']:
    seq['tokens']=copy.deepcopy(tasks[seq['owner_id']]['assessed_output_tokens'])
    seq['assessment_scope']='Operative final assessment annotations match canonical assessed_output_tokens and visible local-help routes; preserved original_sequence remains historical.'
write(path,overlay)
b=Path(path).read_bytes();c['selected_model_corrections']={'path':path,'sha256':hashlib.sha256(b).hexdigest(),'sha256_normalized_lf':hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest()}
record['overlay_sha256_after']=sha(path);history['assessment_route_followup']=record
write('chapters/ch18/support-amendment-history.json',history);write('chapters/ch18/coverage.json',c)
# Keep the one-use preparation aid aligned with the actual root inspection claim.
p=Path('build/prepare_unit18_support_spec.py');s=p.read_text(encoding='utf-8')
s=s.replace("'inspected_by':['root','unit18_grammar','unit18_blind']","'inspected_by':['root']")
p.write_text(s,encoding='utf-8',newline='\n')
assert sha('chapters/ch18/independent-solutions.md')==read('chapters/ch18/blind-freeze.json')['identity']['raw_sha256']
print('Final canonical and corrected-model assessment routes reconciled; original sequences and initial overlay retained.')
