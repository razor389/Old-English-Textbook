"""One-use consolidation of identified non-author Unit 17 page reviews."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, shutil

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'typesetting/ch17'
def read(path): return json.loads((ROOT/path).read_text(encoding='utf-8'))
def sha(path): return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def lfsha(path): return hashlib.sha256((ROOT/path).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
def identity(path): return {'path':path,'sha256':sha(path),'sha256_normalized_lf':lfsha(path)}
c = read('chapters/ch17/coverage.json')
assert c['textual_review']['status'] == 'accepted'
assert c.get('accepted_text_checkpoint'), 'Accepted text checkpoint required'
semantic=c['textual_review']['accepted_contract_semantic_identity']
payload=json.dumps({k:c[k] for k in semantic['keys']},ensure_ascii=False,sort_keys=True,separators=(',',':'))
assert hashlib.sha256(payload.encode('utf-8')).hexdigest()==semantic['sha256'],'Reviewed contract content changed'
for name, expected in c['textual_review']['accepted_artifacts'].items():
    path='chapters/ch17/'+name
    assert sha(path)==expected['sha256'] or lfsha(path)==expected['sha256_normalized_lf'],path
manifest=read('typesetting/ch17/build/render-manifest-final.json')
ledger_paths=['typesetting/ch17/reviews/learner-first.json','typesetting/ch17/reviews/learner-last.json','typesetting/ch17/reviews/key.json']
ledgers=[read(p) for p in ledger_paths]
documents=[]
resolved=[]
for kind, stem in [('learner','chapter-17'),('key','answer-key')]:
    expected=manifest['documents'][kind]
    expected_count=expected['pages']
    assert expected_count > 0
    assert sha(expected['pdf'])==expected['sha256']
    rows=[]
    for ledger_path, ledger in zip(ledger_paths,ledgers):
        if ledger['document']!=kind: continue
        assert ledger['status'].lower() in ['pass','accepted'],ledger_path
        assert ledger['pdf_sha256']==expected['sha256'],ledger_path
        author='unit17_design' if kind=='learner' else 'unit17_grammar'
        reviewer_name=ledger['reviewer'].rsplit('/',1)[-1]
        assert reviewer_name != author,('author reviewed own export',ledger_path)
        for finding in ledger.get('findings',[]):
            assert finding['status'] in ['resolved','resolved_verified','withdrawn'],finding
            resolved.append({'ledger':ledger_path,**finding})
        for page in ledger['pages']:
            assert page['status'].lower() in ['pass','accepted'],page
            assert page.get('actually_viewed') is True and page.get('inspection_method'),page
            assert page.get('observations') and page.get('final_identity_verified') is True,page
            image=expected['images'][page['page']-1]
            assert page['image_path']==image['path'],page
            assert sha(page['image_path'])==page['image_sha256']==image['sha256'],page
            if 'byte_identical_reuse' in page:
                old=page['byte_identical_reuse']
                assert old['previously_actually_viewed'] and old['sha256_equality_verified'],page
                assert sha(old['previously_inspected_image_path'])==old['previously_inspected_image_sha256']==page['image_sha256'],page
            if 'personally_viewed_image' in page:
                old=page['personally_viewed_image']
                assert sha(old['path'])==old['sha256']==page['image_sha256'],page
            rows.append({'reviewer':ledger['reviewer'],'ledger':ledger_path,**page})
    rows.sort(key=lambda x:x['page'])
    assert [x['page'] for x in rows]==list(range(1,expected_count+1)),kind
    retained='typesetting/ch17/'+stem+'.pdf'
    shutil.copyfile(ROOT/expected['pdf'],ROOT/retained)
    assert sha(retained)==sha(expected['pdf'])
    documents.append({'kind':kind,'path':retained,'sha256':sha(retained),'build_path':expected['pdf'],'pages':expected_count,'render_dpi':150,'page_review_records':rows})
parity=read('typesetting/ch17/content-parity.json')
for doc in parity['documents']:
    assert sha(doc['master'])==doc['master_sha256'],doc['master']
    assert sha(doc['tex'])==doc['tex_sha256'],doc['tex']
    assert all(doc[k]=='PASS' for k in ['paragraph_and_cell_parity','pdf_complete_paragraph_character_parity','title_parity'])
bad=['Missing character:','Overfull \\hbox','Overfull \\vbox','Underfull \\hbox','Underfull \\vbox','Font shape','Rerun to get','Table widths have changed','Fatal error','! LaTeX Error']
logs=[]
for stem in ['chapter-17','answer-key']:
    path='typesetting/ch17/build/'+stem+'.log'
    raw=(ROOT/path).read_text(encoding='utf-8',errors='replace')
    diagnostics=[token for token in bad if token in raw]
    assert not diagnostics,(stem,diagnostics)
    logs.append({'path':path,'sha256':sha(path),'diagnostics':diagnostics,'checked_diagnostics':bad,'output_line':re.search(r'Output written on [^\n]+',raw)[0]})
report={
    'schema_version':1,'chapter_id':'ch17','status':'PASS','accepted_at_utc':datetime.now(timezone.utc).isoformat(),
    'presentation_aggregator':'coordinator',
    'aggregation_method':'Reconciled three non-author ledgers against every final PDF/image identity, full content parity and clean logs. Every final page has a recorded visual inspection or an explicit verified identity with a directly inspected image. The individual ledgers record the actual inspection and any repair history. The coordinator aggregates those records rather than claiming personal inspection of every page.',
    'accepted_text_checkpoint':c['accepted_text_checkpoint'],
    'accepted_text_identities':[identity('chapters/ch17/'+n) for n in c['textual_review']['accepted_artifacts']],
    'page_totals':{**{d['kind']:d['pages'] for d in documents},'total':sum(d['pages'] for d in documents)},
    'every_final_page_visually_inspected_by_non_author':True,'page_coverage_complete_without_overlap':True,
    'reviewer_ledgers':[identity(p) for p in ledger_paths],
    'documents':documents,'resolved_findings':resolved,'unresolved_findings':[],
    'content_parity':{'identity':identity('typesetting/ch17/content-parity.json'),'counts':{k:sum(d[k] for d in parity['documents']) for k in ['paragraph_heading_list_blocks','original_tables','original_table_cells_including_headers','all_editorial_comments_preserved']},'documents':parity['documents']},
    'compilation_logs':logs,'masters_unchanged_since_textual_acceptance':True,'frozen_solutions_unchanged':True,'build_and_retained_pdf_bytes_identical':True,
    'scope_limit':'Accepts only the identified Unit17 complete exports and presentation. Register integration and final Beads/checkpoint closure are separate.'
}
(OUT/'page-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS:',sum(d['pages'] for d in documents),'final pages, complete parity, unchanged accepted masters and clean logs. Retained both complete PDFs.')
