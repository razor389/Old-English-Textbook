"""Record root's actual follow-up inspection of Matthew16.27."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[1]
def read(p):return json.loads((root/p).read_text(encoding='utf-8-sig'))
def save(p,d):(root/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
path='sources/audits/unit16-grammar/matthew-p132-300.png'
row={'path':path,'sha256':hashlib.sha256((root/path).read_bytes()).hexdigest(),
 'source_id':'matthew_kemble_hardwick_1858','printed_page':132,'pdf_page_one_based':142,
 'original_identifier':'Matthew16.27, left/first column and its A apparatus',
 'inspector':'coordinator/root','date':'2026-10-27','method':'Personally viewed through view_image',
 'observation':'Leftcolumn prints mannes Sunu ys to cumenne and then agylt æghwylcum be hys agenum worce. Apparatus at bottom explicitly gives Ch.xvi.v.27,6.A.cumanne and21.A.B.weorce. This corroborates the bounded impending-coming phrase, selected cumanne variant, contracted reward verb and dative recipient. The new model is not presented as an exact quotation of this differently spelled parallel.'}
ledger=read('sources/audits/unit16-coordinator/primary-inspections.json')
assert path not in {r['path'] for r in ledger['actual_inspections']}
ledger['actual_inspections'].append(row)
save('sources/audits/unit16-coordinator/primary-inspections.json',ledger)
correction=read('sources/audits/unit16-coordinator/reward-correction.json')
correction['additional_primary_corroboration']=[row]
save('sources/audits/unit16-coordinator/reward-correction.json',correction)
catalog=read('sources/audits/unit16-coordinator/evidence-catalog.json')
catalog['U16-C06-REWARD']['additional_primary_corroboration']=[row]
save('sources/audits/unit16-coordinator/evidence-catalog.json',catalog)
registry=read('sources/registry.json')
r=next(x for x in registry['supporting_sources'] if x['source_id']==row['source_id'])
r['selected_use']='Bounded primary corroboration for supplied Johannes/Johannem in Cook36.9–10, and the impending-coming phrase and contracted reward verb in34.9. No additional reading assignment or change of the selected Cook editions.'
r['locators']['printed_132_pdf_page_one_based']=142
r['bounded_offset']='For the inspected numbered text pages114 and132, PDF=printed+10. No universal offset is asserted for duplicated/reordered preliminary leaves.'
r['additional_evidence_ids']=['U16-G-MATTHEW132']
save('sources/registry.json',registry)
print('Recorded actual Matthew132 inspection, added C06 corroboration and bounded registry extension.')
