"""Preserve inherited form analyses while making A02 occurrence syntax explicit."""
import hashlib,json
from pathlib import Path
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
c=read('chapters/ch17/coverage.json')
h=read('chapters/ch17/support-amendment-history.json')
assert 'verification_refinements' not in h
changed=[]
for t in c['assigned_items']:
    if 'assessed_output_tokens' not in t:continue
    for place,tokens in [('output',t['assessed_output_tokens'])]+[(s['sequence_id'],s['tokens']) for s in t['input_sequences'] if s.get('amendment_id')=='U17-A02']:
        for token in tokens:
            if token.get('amendment_id')!='U17-A02':continue
            before=json.loads(json.dumps(token))
            rid=token['local_support_id']
            token['reference_route_ids']=list(dict.fromkeys(token.get('reference_route_ids',[])+[rid]))
            if token['literal'].strip(',:;.').casefold()=='cweðende':
                token['contextual_analysis']={**token.get('contextual_analysis',{}),
                    'verb_form':'present_participle','case':'nom','number':'pl','gender':'m',
                    'function':'accompanying speech by the plural angels or soldiers'}
                token['analysis_scope_note']='The inherited form-register analysis is retained as historical representation of this surface/base. This supplied occurrence has the plural subject agreement specified in contextual_analysis; it does not establish a new general production milestone.'
            changed.append({'task_id':t['task_id'],'location':place,'token_index':token['token_index'],
                            'before':before,'after':token})
refinement={'reported_by':'unit17_paradigms','coordinator':'root',
    'reason':'Explicit plural occurrence analysis for accompanying cweðende and direct support-route links for each newly supplied token. Preserve original form analysis and all surfaces.',
    'contract_sha256_before':hashlib.sha256(Path('chapters/ch17/coverage.json').read_bytes()).hexdigest(),
    'changes':changed,'review_status':'requires_independent_verification'}
h['verification_refinements']=[refinement]
note={'record':'chapters/ch17/support-amendment-history.json#verification_refinements',
      'reason':refinement['reason'],'reported_by':'unit17_paradigms'}
next(a for a in c['amendments'] if a['amendment_id']=='U17-A02')['verification_refinements']=[note]
a=read('chapters/ch17/authoring-amendments.json')
next(x for x in a['amendments'] if x['amendment_id']=='U17-A02')['verification_refinements']=[note]
write('chapters/ch17/support-amendment-history.json',h)
write('chapters/ch17/coverage.json',c)
write('chapters/ch17/authoring-amendments.json',a)
print('Recorded',len(changed),'input/output token refinements; all original analyses and surfaces retained.')
