"""Learner-only parity checks; no independent linguistic review is claimed."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import unicodedata

ROOT=Path(__file__).resolve().parents[1]
c=json.loads((ROOT/'chapters/ch17/coverage.json').read_text(encoding='utf-8'))
s=(ROOT/'chapters/ch17/student.md').read_text(encoding='utf-8')
errors=[]
def require(ok,msg):
    if not ok:errors.append(msg)

require(s==unicodedata.normalize('NFC',s),'Learner text is not NFC')
for t in c['teaching_records']:
    marker='<!-- teaching: '+t['teaching_id']+' -->'
    require(s.count(marker)==1,'Teaching marker count: '+t['teaching_id'])
for m in c['display_plan']['matrices']:
    marker='<!-- table: '+m['matrix_id']+' -->'
    require(s.count(marker)==1,'Table marker count: '+m['matrix_id'])
    if marker not in s:continue
    match=re.match(r'\s*(\|[^\n]+(?:\n\|[^\n]+)*)',s.split(marker,1)[1])
    require(bool(match),'Literal table missing: '+m['matrix_id'])
    if match:
        rows=[[v.strip().replace('**','') for v in row.strip().strip('|').split('|')] for row in match[1].splitlines()]
        require([rows[0]]+rows[2:]==[m['headers']]+m['rows'],'Literal table differs: '+m['matrix_id'])
records={'form':{x['form_id']:x for l in c['lexical_inventory'] for x in l['forms']},
         'sense':{x['sense_id']:x for l in c['lexical_inventory'] for x in l['senses']},
         'feature':{x['feature_id']:x for x in c['grammar_inventory']}}
for t in c['assigned_items']:
    tid=t['task_id'];marker='<!-- item: '+tid+' -->'
    require(s.count(marker)==1,'Task marker count: '+tid)
    if marker not in s:continue
    tail=s.split(marker,1)[1]
    require(tail.strip().split('\n\n',1)[0]==t['prompt'],'Prompt differs: '+tid)
    body=tail.split('<!-- item:',1)[0].replace('**','')
    cursor=0
    for seq in t.get('input_sequences',[]):
        at=body.find(seq['text'],cursor)
        require(at>=0,'Ordered input absent: '+tid+' '+seq['sequence_id']+' '+seq['text'])
        if at>=0:cursor=at+len(seq['text'])
    for p in t['output_positions']:
        marker='<!-- output: '+p['output_position_id']+' -->'
        require(s.count(marker)==1,'Output marker count: '+p['output_position_id'])
        if p.get('label'):
            require(p['label'] in body,'Output label differs: '+p['output_position_id'])
    item_at=s.index('<!-- item: '+tid+' -->')
    for kind in records:
        for rid in t.get('tested_'+kind+'_ids',[]):
            r=records[kind].get(rid,{})
            if r.get('knowledge_status') not in {'new_production','new_recognition'}:continue
            locations=[s.find('<!-- teaching: '+x+' -->') for x in r.get('teaching_ids',[])]
            require(any(0<=x<item_at for x in locations),'New target taught too late: '+tid+' '+rid)
plain=re.sub(r'\[\^[^\]]+\]','',s).replace('**','')
for e in c['new_material_examples']:
    require(e.get('learner_text',e.get('text')) in plain,'Missing example: '+e['example_id'])
    require(e['translation'] in s,'Missing example translation: '+e['example_id'])
for r in c['source_spans']:
    require(r['learner_text'] in plain,'Exact reading differs')
    for n in r['original_notes']:
        require(n['original_text'] in s,'Original note differs: '+n['apparatus_id'])
    between=s.split('<!-- source: '+r['source_span_id']+' -->',1)[1].split('### Finding the cited lines',1)[0]
    labels=re.findall(r'\[\^([^\]]+)\]',between)
    expected=['P'+str(a['printed_page'])+'N'+a['original_note_number'] for a in r['original_note_anchors']]
    require(labels==expected,'Reading anchor order/count differs')
for g in c['source_task_crosswalk']['global_instructions']:
    require(g['original_text'] in s,'Global exercise instruction absent')
visible=re.sub(r'<!--.*?-->','',s,flags=re.S)
require(not re.search(r'\b(?:NEW-U17-|U17-RSUP-|U17-H-|u17-|u11-concession)',visible),'Visible backend identity')
# Confirm the two polysemous cases are routed to the precise reading help.
for tid,heading in [('U17-SUP-THONNE-THEN-CONSEQUENCE','### 174.17–18: giving and knowing'),
                    ('U17-SUP-ON-CHANCED-DOMAIN','### 174.14–16: permission and competence')]:
    at=s.find('<!-- teaching: '+tid+' -->')
    section=s.rfind('### ',0,at)
    require(section>=0 and s[section:].startswith(heading),'Polysemous help at wrong section: '+tid)
report={'status':'pass' if not errors else 'fail','errors':errors,'error_count':len(errors),
        'learner_sha256':hashlib.sha256((ROOT/'chapters/ch17/student.md').read_bytes()).hexdigest(),
        'contract_sha256':hashlib.sha256((ROOT/'chapters/ch17/coverage.json').read_bytes()).hexdigest(),
        'metrics':c['contract_metrics'],
        'visible_whitespace_words':len(visible.split()),
        'scope_limit':'Author self-check of literal displays, markers, teaching order, exact prompts/output labels/input sequences, reading/notes/anchors, and selected sense routes. Independent linguistic and page review remain outstanding.'}
(ROOT/'build/u17-learner-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(report['status'],len(errors),'errors;',len(visible.split()),'visible whitespace words')
for e in errors[:40]:print(e)
raise SystemExit(bool(errors))
