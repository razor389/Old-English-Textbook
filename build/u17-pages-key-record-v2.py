from pathlib import Path
import hashlib, json, sys
sys.stdout.reconfigure(encoding='utf-8')
root = Path(__file__).resolve().parents[1]
notes = json.loads(r'''{"observations":{"6":"F03's remaining four prompt/model/explanation groups are intact. F04 now retains both the first indicative response and the complete imperative prompt, hęriað model and explanation on this page. K17-P01 is visibly resolved; glyphs and footer clear.","7":"F04 resumes at a complete subjunctive question with hęrien and its explanation, then the comparison question. F05's first two participial models and the two-relations answer remain complete and attached. No new prompt/model detachment or clipping.","8":"F05's last analytical answer, section C, C01 and C02 are complete. C03's heading and two-line Task occur at the foot of the page, while its requested-output line, model and explanation start page 9. This new task/model detachment is K17-P03.","9":"The page begins with C03's requested-output line, complete Gif hē cymð model and explanation, detached from its Task on page 8 (K17-P03). C04 remains complete and legible with all macrons and Old English glyphs intact.","44":"R04's remaining answers and all three R05 questions/answers are readable. The full Apollo question and answer now stay together at the foot of this page; the previous two-line continuation on page 45 is removed. Final answer line clears the footer.","45":"R06 starts cleanly with its heading and task and retains all three complete interpretive question/answer divisions. The complete source note follows, including the legible þūsend headword. No R05 continuation, clipping, orphan heading or footer collision."},"findings":[{"id":"K17-P01","status":"resolved_verified","severity":"material","reported_render":"v1","pages":[6,7],"location":"F04 imperative prompt/model/explanation, P094–P096","description":"The v1 imperative prompt ended page 6 while its model and explanation began page 7.","resolution":"Personally inspected v2 page 6: the prompt, hęriað model and complete explanation are now together; page 7 begins at the following complete question.","history":[{"render":"v1","status":"open"},{"render":"v2","status":"resolved_verified","personally_reinspected_pages":[6,7]}]},{"id":"K17-P02","status":"resolved_verified","severity":"minor_optional","reported_render":"v1","pages":[44,45],"location":"R05 Apollo question/answer, P543–P544","description":"The readable but short v1 Apollo answer divided two lines onto each of pages 44 and 45.","resolution":"Personally inspected v2 pages 44 and 45: prompt and full answer are together on page 44, and page 45 starts at R06.","history":[{"render":"v1","status":"reported_nonblocking"},{"render":"v2","status":"resolved_verified","personally_reinspected_pages":[44,45]}]},{"id":"K17-P03","status":"open","severity":"material","reported_render":"v2","pages":[8,9],"location":"C03 heading/task and requested-output/model/explanation","description":"The v2 C03 heading and Task are stranded at the foot of page 8; the output instruction, model and explanation begin page 9.","requested_repair":"Keep the complete short C03 block together, preferably at the top of page 9."}]}''')
old = json.loads((root / 'build/u17-pages-key-v1-receipt.json').read_text(encoding='utf-8'))
sha = lambda p: hashlib.sha256((root / p).read_bytes()).hexdigest()
expected_pdf = 'e3611d374e3e2ba79a48b9f2e7f62ec8f11fd9bd874c208528bfbddaa6a6e828'
pdf_candidates = ['typesetting/ch17/build/answer-key-v2.pdf', 'typesetting/ch17/build/answer-key.pdf']
pdf = next((p for p in pdf_candidates if (root/p).exists() and sha(p) == expected_pdf), None)
assert pdf, 'No actual v2 PDF matches its expected identity'
old_pdf = 'typesetting/ch17/build/answer-key-v1.pdf'
assert sha(old_pdf) == old['pdf_sha256']
manifest = json.loads((root / 'typesetting/ch17/build/render-manifest-final.json').read_text(encoding='utf-8'))
manifest_doc = manifest['documents']['key']
if manifest_doc['version'] == 'v2':
    assert manifest_doc['pages'] == 45 and manifest_doc['sha256'] == expected_pdf
changed = []
pages = []
for prior in old['pages']:
    n = prior['page']
    old_sha = sha(prior['image_path'])
    assert old_sha == prior['image_sha256'] and prior['actually_viewed']
    image_path = f'typesetting/ch17/build/key-v2/page-{n:03d}.png'
    actual_sha = sha(image_path)
    if manifest_doc['version'] == 'v2':
        identity = manifest_doc['images'][n-1]
        assert identity['page'] == n and identity['path'] == image_path and identity['sha256'] == actual_sha
    page = {'page': n, 'status': 'needs_repair' if n in [8,9] else 'pass',
            'actually_viewed': True, 'final_identity_verified': True,
            'image_path': image_path, 'image_sha256': actual_sha}
    if actual_sha != old_sha:
        changed.append(n)
        page['inspection_method'] = "Direct personal visual inspection of the complete v2 150-dpi page with view_image(detail='original')."
        page['observations'] = notes['observations'][str(n)]
        page['personally_viewed_image'] = {'path': image_path, 'sha256': actual_sha}
    else:
        page['inspection_method'] = "Direct personal full-page view of v1 with view_image(detail='original'); actual old/new SHA-256 values verify that the v2 image is byte-identical."
        page['observations'] = prior['observations']
        page['byte_identical_reuse'] = {'previously_actually_viewed': True, 'sha256_equality_verified': True,
            'previously_inspected_image_path': prior['image_path'],
            'previously_inspected_image_sha256': old_sha}
        page['personally_viewed_image'] = {'path': prior['image_path'], 'sha256': old_sha}
    pages.append(page)
assert changed == [6,7,8,9,44,45]
assert [p['page'] for p in pages] == list(range(1,46))
report = {'schema_version': 1, 'chapter_id': 'ch17', 'document': 'key',
    'reviewer': 'unit17_pages_key', 'status': 'needs_repair', 'version': 'v2',
    'pdf_path': pdf, 'pdf_sha256': sha(pdf), 'pages': pages,
    'scope': '45 answer-key pages only; no personal inspection claim for the 96 learner pages or complete 141-page export.',
    'inspection_summary': {'v1_pages_personally_viewed': list(range(1,46)), 'v2_pages_personally_viewed': changed, 'v2_pages_verified_byte_identical': [p['page'] for p in pages if 'byte_identical_reuse' in p]},
    'findings': notes['findings'], 'initial_v1_review': old,
    'retained_v1_pdf': {'path': old_pdf, 'sha256': sha(old_pdf)}}
serialized = json.dumps(report, ensure_ascii=False, indent=2)+'\n'
(root / 'build/u17-pages-key-v2-receipt.json').write_text(serialized, encoding='utf-8')
(root / 'typesetting/ch17/reviews/key.json').write_text(serialized, encoding='utf-8')
print('V2 receipt saved: six changed pages personally viewed; all 39 other actual image hashes equal v1.')
print('PDF SHA256:', sha(pdf))
print('K17-P01 and K17-P02 resolved; K17-P03 remains open on pages 8-9.')
lines = (root / 'typesetting/ch17/answer-key.tex').read_text(encoding='utf-8').splitlines()
start = next(i for i,s in enumerate(lines) if r'\subsection*{C03}' in s)
end = next(i for i in range(start+1,len(lines)) if r'\subsection*{C04}' in lines[i])
for i in range(start-3,end-1): print(f'{i+1}: {lines[i]}')
