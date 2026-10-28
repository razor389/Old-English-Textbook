from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
root = Path(__file__).resolve().parents[1]
sha = lambda p: hashlib.sha256((root/p).read_bytes()).hexdigest()
notes = json.loads(r'''{"8":"F05's final analytical question and answer remain together at the top. Section C and the complete C01/C02 task, model and explanation groups follow. The page now ends cleanly after C02; no C03 heading or task is stranded at the foot. Old English glyphs, macrons, header and footer are clear.","9":"The complete C03 block now begins the page: heading, task, requested-output instruction, Gif hē cymð model and full explanation stay together. C04 remains complete beneath it with clear item spacing and intact sægð/sīe/gōd glyphs and marks. K17-P03 is visibly resolved; no new orphan or clipping appears."}''')
manifest = json.loads((root/'typesetting/ch17/build/render-manifest-final.json').read_text(encoding='utf-8'))
old = json.loads((root/'build/u17-pages-key-v2-receipt.json').read_text(encoding='utf-8'))
original = old['initial_v1_review']
doc = manifest['documents']['key']
assert doc['version'] == 'v3' and doc['pages'] == 45
assert sha(doc['pdf']) == doc['sha256'] == 'a16eec4e7eafd929c427507e3b430986256a0d126d1b6c497fcb2cd25daeae42'
assert [p['page'] for p in old['pages']] == list(range(1,46))
assert [p['page'] for p in original['pages']] == list(range(1,46))
retained_prior = [
    {'version':'v1','path':'typesetting/ch17/build/answer-key-v1.pdf','sha256':original['pdf_sha256']},
    {'version':'v2','path':'typesetting/ch17/build/answer-key-v2.pdf','sha256':old['pdf_sha256']}
]
for identity in retained_prior: assert sha(identity['path']) == identity['sha256']
directly_viewed_paths = {p['image_path'] for p in original['pages'] if p['actually_viewed']}
directly_viewed_paths.update(p['image_path'] for p in old['pages'] if p['page'] in [6,7,8,9,44,45] and p['actually_viewed'])
pages, changed = [], []
reuse_versions = {'v1':[],'v2':[]}
for item, prior in zip(doc['images'],old['pages']):
    n = item['page']
    assert n == prior['page']
    current_sha = sha(item['path'])
    assert current_sha == item['sha256']
    assert sha(prior['image_path']) == prior['image_sha256']
    page = {'page':n,'status':'pass','actually_viewed':True,
            'final_identity_verified':True,'image_path':item['path'],'image_sha256':current_sha}
    if current_sha != prior['image_sha256']:
        changed.append(n)
        page['inspection_method'] = "Direct personal visual inspection of this complete final v3 150-dpi page with view_image(detail='original')."
        page['observations'] = notes[str(n)]
        page['personally_viewed_image'] = {'path':item['path'],'sha256':current_sha}
    else:
        provenance = prior['personally_viewed_image']
        assert provenance['path'] in directly_viewed_paths
        assert sha(provenance['path']) == provenance['sha256'] == current_sha
        version = 'v1' if '/key-v1/' in provenance['path'] else 'v2'
        reuse_versions[version].append(n)
        page['inspection_method'] = f"Personally viewed the complete {version} 150-dpi page with view_image(detail='original'); actual current and directly inspected image SHA-256 values verify byte-identical final reuse."
        page['observations'] = prior['observations']
        page['personally_viewed_image'] = dict(provenance)
        page['byte_identical_reuse'] = {
            'previously_actually_viewed':True,'sha256_equality_verified':True,
            'previously_inspected_image_path':provenance['path'],
            'previously_inspected_image_sha256':provenance['sha256'],
            'previously_inspected_render':version
        }
    assert page['observations'] and page['inspection_method']
    pages.append(page)
assert changed == [8,9]
assert len(reuse_versions['v1']) == 39 and reuse_versions['v2'] == [6,7,44,45]
assert [p['page'] for p in pages] == list(range(1,46))
findings = json.loads(json.dumps(old['findings']))
for finding in findings:
    if finding['id'] == 'K17-P03':
        finding['status'] = 'resolved_verified'
        finding['resolution'] = 'Personally inspected final v3 pages 8 and 9: page 8 ends after complete C02; all of C03 (P125–P129) begins page 9 with task, requested output, model and explanation together. C04 remains complete below it.'
        finding['history'] = [{'render':'v2','status':'open','pages':[8,9]},
                              {'render':'v3','status':'resolved_verified','personally_reinspected_pages':[8,9]}]
    else:
        finding['final_identity_confirmation'] = 'Final v3 page images are byte-identical to the personally inspected v2 repair images.'
assert all(f['status']=='resolved_verified' for f in findings)
report = {
    'schema_version':1,'chapter_id':'ch17','document':'key','reviewer':'unit17_pages_key',
    'status':'pass','version':'v3','accepted_at_utc':datetime.now(timezone.utc).isoformat(),
    'accepted_text_checkpoint':'a137171','pdf_path':doc['pdf'],'pdf_sha256':sha(doc['pdf']),
    'render_dpi':150,'page_count':45,
    'scope':'Accepts presentation of these 45 answer-key pages only. The final learner PDF has 94 pages and the combined export has 139; no personal inspection of learner pages is claimed.',
    'inspection_summary':{
        'v1_pages_personally_viewed':list(range(1,46)),
        'v2_pages_personally_viewed':[6,7,8,9,44,45],
        'v3_pages_personally_viewed':changed,
        'final_pages_reused_from_direct_v1_views':reuse_versions['v1'],
        'final_pages_reused_from_direct_v2_views':reuse_versions['v2'],
        'every_final_page_has_direct_visual_provenance':True,
        'actual_final_pdf_and_image_hashes_verified':True
    },
    'findings':findings,'unresolved_findings':[],'pages':pages,
    'retained_prior_pdfs':retained_prior,
    'initial_v1_review':original,
    'intermediate_v2_review':{k:v for k,v in old.items() if k!='initial_v1_review'},
    'receipt_identities':[
        {'path':'build/u17-pages-key-v1-receipt.json','sha256':sha('build/u17-pages-key-v1-receipt.json')},
        {'path':'build/u17-pages-key-v2-receipt.json','sha256':sha('build/u17-pages-key-v2-receipt.json')}
    ]
}
serialized = json.dumps(report,ensure_ascii=False,indent=2)+'\n'
(root/'typesetting/ch17/reviews/key.json').write_text(serialized,encoding='utf-8')
(root/'build/u17-pages-key-v3-receipt.json').write_text(serialized,encoding='utf-8')
(root/'typesetting/ch17/reviews/key.md').write_text("# Unit 17 answer-key page review\n\nReviewer: `unit17_pages_key`, a fresh non-author presentation reviewer. Status: **PASS** for key v3, all **45 pages**.\n\nI personally inspected all 45 full-page v1 images, the six changed v2 pages (6–9, 44–45), and the two changed v3 pages (8–9), using `view_image` at original resolution for the supplied 150-dpi images. For final v3, 39 pages are verified byte-identical to images I personally viewed in v1, and four to images I personally viewed in v2. The two remaining pages were directly inspected in v3. Every actual final image hash matches the manifest and its recorded direct-view identity.\n\nThe final PDF SHA-256 is `a16eec4e7eafd929c427507e3b430986256a0d126d1b6c497fcb2cd25daeae42`. The [page ledger](key.json) records every final page exactly once, its concrete observations and actual image hash, explicit reuse provenance where applicable, and the complete v1/v2 review history. The retained v1 and v2 PDFs were also verified against their original review hashes.\n\nAll reported adjustments are resolved:\n\n- **K17-P01:** F04's imperative prompt, `hęriað` model and explanation (P094–P096) now remain together on page 6.\n- **K17-P02:** the optional R05 Apollo question and short answer (P543–P544) now remain together on page 44; R06 starts on page 45.\n- **K17-P03:** C03's complete heading, task, model and explanation (P125–P129) now begin page 9, with page 8 ending after C02.\n\nThe Cook item models, original English prompts and explanations remain attached and readable. The complete reading translation retains all three divisions and their retention notes; its third division continues cleanly from page 41 to page 42. No unresolved clipping, missing special character, orphan heading, detached task/model, unreadable typography or header/footer defect remains.\n\nThis accepts only my **45 answer-key pages**. The final learner PDF has 94 pages, making 139 pages in the combined export; I do not claim personal inspection of those learner pages or the whole export. Accepted text, contracts, registers and other reviewers' files were not edited.\n",encoding='utf-8')
print('PASS: all 45 final key pages, actual PDF/image identities, direct visual provenance, and all three resolved findings.')
print('Direct final views: 8,9. Verified direct-view reuse: 39 v1 pages and four v2 pages.')
print('PDF SHA256:', report['pdf_sha256'])
