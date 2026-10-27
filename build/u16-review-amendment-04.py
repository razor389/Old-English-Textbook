"""Post-freeze record of independently verified wēn/nearu rule clarifications."""
import argparse,hashlib,json
from pathlib import Path
ap=argparse.ArgumentParser(__doc__)
ap.add_argument('--solutions-checkpoint',required=True)
a=ap.parse_args()
def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def write(path,value): Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
freeze=read('chapters/ch16/blind-freeze.json')
assert hashlib.sha256(Path('chapters/ch16/independent-solutions.md').read_bytes()).hexdigest()==freeze['identity']['raw_sha256']
assert len(a.solutions_checkpoint)>=7
c=read('chapters/ch16/coverage.json')
assert not any(x['amendment_id']=='U16-A04' for x in c['amendments'])
new_rule='Selected singular: nominative/accusative wēn; genitive/dative wēne. The accusative retains no -e, as allowed by Cook §51.1 and specifically identified by the vocabulary entry on p.321.'
changes=[]
old_model='Cook51.b /51.5; prior strong feminine'
new_model='Cook51.b with the §51.1 accusative exception; vocabulary p.321; prior strong feminine'
def repair(value,path=''):
    if isinstance(value,dict):
        for key,child in value.items():
            if key in ['records_by_chapter','metadata_by_chapter','prior_record','amendments']: continue
            here=path+'/'+key
            if child==old_model:
                # Restrict the class-locator repair to the wēn record itself.
                if value.get('lemma_id')=='wen' or value.get('paradigm_id')=='NEW-U16-NOM-WEN':
                    changes.append({'path':here,'before':child,'after':new_model})
                    value[key]=new_model
            else: repair(child,here)
    elif isinstance(value,list):
        for i,child in enumerate(value): repair(child,path+'/'+str(i))
repair(c)
for field,rows,idkey,target in [
    ('display_plan/matrices',c['display_plan']['matrices'],'matrix_id','NEW-U16-NOM-WEN-DISPLAY'),
    ('paradigms',c['paradigms'],'paradigm_id','NEW-U16-NOM-WEN'),
    ('teaching_records',c['teaching_records'],'teaching_id','NEW-U16-NOM-WEN')]:
    index=next(i for i,x in enumerate(rows) if x[idkey]==target)
    row=rows[index]; before=list(row.get('rules',[]))
    assert new_rule not in before
    row['rules']=before+[new_rule]
    changes.append({'path':'/'+field+'/'+str(index)+'/rules','before':before,'after':row['rules']})
assert len(changes)>=4
amendment={
 'amendment_id':'U16-A04','date':'2026-10-27','stage':'independent_review',
 'original_contract_checkpoint':'543e214','complete_drafts_checkpoint':'9b75319',
 'blind_solutions_checkpoint':a.solutions_checkpoint,'coordinator':'root',
 'reported_by':'unit16_paradigms',
 'reason':'The displayed forms were correct, but two author-written generalizations omitted their exceptions. Make wēn accusative singular and nearu weak genitive plural explicit; clarify the existing wēn source locator and rule without changing any form or teaching boundary.',
 'primary_evidence':[
   {'evidence_id':'U16-FB-P321','locator':'Cook vocabulary p.321, wēn → §51.1'},
   {'evidence_id':'U16-FB-P35','locator':'Cook p.35 §51.1, omitted accusative -e'},
   {'locator':'Wright p.215 §§435–436, nearo- before consonantal endings'},
   {'locator':'Cook pp.40–41 §60, weak genitive plural -ra'}],
 'primary_inspection_record':'chapters/ch16/reviews/paradigms.json',
 'canonical_changes':changes,
 'learner_prose_repairs':[
  {'before':'The selected nouns have no ending in the nominative singular. Their other singular cases have -e; the plural, where assigned, has nominative/accusative -a, genitive -a and dative -um. Smyltnes doubles its final s before an ending.',
   'after':'The selected nouns have no ending in the nominative singular. Their genitive and dative singular have -e. The accusative singular also has -e, except wēn, whose accusative is wēn. The plural, where assigned, has nominative/accusative -a, genitive -a and dative -um. Smyltnes doubles its final s before an ending.'},
  {'before':'Learn the alternating stems together: nearu in the selected nominative singular forms; nearw- before vowel endings; nearo- before consonantal -ne, -re and -ra. Thus the case ending can select a different visible stem. The weak forms use nearw-.',
   'after':'Learn the alternating stems together: nearu in the strong nominative singular, neuter accusative singular and neuter nominative/accusative plural; nearw- before vowel endings; nearo- before consonantal -ne, -re and -ra. The weak forms use nearw- except for genitive plural nearora.'}],
 'unchanged':['All literal table cells, form/sense/feature identities and productive boundaries',
   'Every actual task, output, model, source passage and note',
   'The initial blind witness and all author/source witnesses',
   'Sealed source/design packets and prior per-chapter records'],
 'review_status':'requires_independent_verification'}
c['amendments'].append(amendment)
write('chapters/ch16/coverage.json',c)
ledger=read('chapters/ch16/authoring-amendments.json')
ledger['amendments'].append(amendment)
write('chapters/ch16/authoring-amendments.json',ledger)
print('Recorded A04 with',len(changes),'canonical rule/locator changes; author must apply the two prose repairs separately.')
