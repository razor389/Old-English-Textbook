"""Register the bounded original-edition evidence actually inspected by root."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def read(p): return json.loads((root/p).read_text(encoding='utf-8-sig'))
def save(p,d): (root/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(p): return hashlib.sha256((root/p).read_bytes()).hexdigest()
sid='matthew_kemble_hardwick_1858'
folder='sources/audits/unit16-coordinator/'
page=folder+'matthew-p114-300.png'
url='https://upload.wikimedia.org/wikipedia/commons/a/a0/The_Gospel_according_to_Saint_Matthew_in_Anglo-Saxon_and_Northumbrian_versions_synoptically_arranged%2C_with_collations_of_the_best_manuscripts_%28IA_gospelaccordingt00kembrich%29.pdf'
record={
 'source_id':sid,'title':'The Gospel according to Saint Matthew in Anglo-Saxon and Northumbrian Versions, Synoptically Arranged, with Collations of the Best Manuscripts',
 'editors':['John Mitchell Kemble','Charles Hardwick'],'publisher':'Cambridge: The University Press',
 'year':'[1858]','year_authority':'Internet Archive catalogue; the inspected title leaf does not visibly print a date.',
 'record_url':'https://archive.org/details/gospelaccordingt00kembrich','download_url':url,
 'local_pdf':'sources/cache/matthew_kemble_hardwick_1858.pdf','pdf_sha256':sha('sources/cache/matthew_kemble_hardwick_1858.pdf'),
 'selected_use':'Only the two supplied name forms in Cook XII,XIII.36.9–10. This is primary corroboration, not an additional assigned reading or a change of Cook edition.',
 'column_identity':'Preface iii identifies column1 as Corpus Christi College Cambridge MS140; column2 is Hatton. Select the first/left column on114, not a composite of columns.',
 'locators':{'title_pdf_page_one_based':9,'preface_iii_pdf_page_one_based':5,'printed_114_pdf_page_one_based':124},
 'bounded_offset':'For the inspected numbered text page114, PDF=printed+10. No universal offset is asserted for duplicated/reordered preliminary leaves.',
 'inspection_record':folder+'primary-inspections.json','evidence_id':'U16-MT-P114','accessed':'2026-10-27'}
registry=read('sources/registry.json')
assert sid not in {r['source_id'] for r in registry['supporting_sources']}
registry['supporting_sources'].append(record)
save('sources/registry.json',registry)
catalog=read(folder+'evidence-catalog.json')
catalog['U16-MT-P114']={
 'source_id':sid,'printed_page':114,'pdf_page_one_based':124,'original_identifier':'Matthew14.8,14.10; left/first column',
 'origin_category':'exact source',
 'image':page,'image_sha256':sha(page),'personally_viewed':True,
 'inspection_scope':'Firstcolumn14.8: Iohannes heafod þæs fulluhteres. Firstcolumn14.10: beheafdode Iohannem on þam cwerterne. The genitive Iohannes and accusative Iohannem are directly attested; the rightcolumn variant Iohanne is not silently substituted.',
 'declared_normalization':'Retain the attested endings, writing initial J in Johannes/Johannem solely to follow Cook’s printed Johannes hint. No vowel quantity is inferred and no complete Latin proper-name system is assigned.',
 'affected_items':['EX-XII-XIII-36-09','EX-XII-XIII-36-10'],
 'teaching_scope':'Supply Johannes as the genitive in36.9 and Johannem as the accusative in36.10; identify both roles explicitly.',
 'metadata_authority':record}
save(folder+'evidence-catalog.json',catalog)
ledger=read(folder+'primary-inspections.json')
for name,printed,pdf,observation in [
 ('matthew-title-300.png',None,9,'Title, Cambridge University Press publisher and synoptic-edition identity personally checked; no visible publication year on this leaf.'),
 ('matthew-preface-piii-300.png','iii',5,'Preface explicitly identifies firstcolumn as Corpus Christi College Cambridge140 and secondcolumn as Hatton; Kemble initiated the edition, completed after his1857death.'),
 ('matthew-p114-300.png',114,124,catalog['U16-MT-P114']['inspection_scope'])]:
    p=folder+name
    ledger['actual_inspections'].append({'path':p,'sha256':sha(p),'source_id':sid,'printed_page':printed,
       'pdf_page_one_based':pdf,'inspector':'coordinator/root','date':'2026-10-27',
       'method':'Personally viewed through view_image','observation':observation})
save(folder+'primary-inspections.json',ledger)
print('Registered bounded Matthew primary evidence: supplied genitive Johannes and accusative Johannem.')
