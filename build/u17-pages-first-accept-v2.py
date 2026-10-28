from pathlib import Path
from datetime import datetime, timezone
import copy, hashlib, json
ROOT = Path(__file__).resolve().parents[1]
observations = json.loads(r'''{
  "35": "Giernan and mǣrsian indicative tables remain complete and legible. The repaired mǣrsian participle heading, formation paragraph, scope paragraph and two-form table now all fit together on this page, with clear ǣ and adequate separation from the folio; U17LF01 is resolved.",
  "36": "Gewilnian, ðurhwunian and wiðstandan each retain their full rule and complete indicative table. Eth, hooked e and ō remain clear; all rows and table rules fit above the footer without a detached introduction.",
  "37": "Gearcian's complete indicative entry is followed by āfyllan's descriptor, indicative table and participle pair on the same page. Ā and ð are intact, headings align, and the last pair is unclipped.",
  "38": "Āweorpan and āwrītan each keep their formation/government explanation with a complete six-row indicative display. Ā/ī/ð render cleanly; the page ends after a full table with generous lower margin.",
  "39": "Ālūtan and windan each retain complete indicative tables below the stem rules. Ū, ȳ, ē, ā and ð are readable; all table columns and lower rules stay within the text block.",
  "40": "Spǣtan, tǣlan and bīegan each have attached descriptors and complete indicative matrices. Long ǣ and ī are clear, no column collides, and the final bīegan row/rule clears the folio.",
  "41": "Gemunan and ðęncean have complete attached indicative entries. Blētsian's participle heading, sense, formation/scope paragraphs and two-form table all stay together at the bottom; hooked e, ē, ō and ð remain readable.",
  "42": "Ofwundrian, wyrcean and gesweotolian each keep the full formation/scope explanation with the two-form participle table. All headings and long forms are readable, rules align, and no entry crosses the page boundary.",
  "43": "Ācęnnan and geopenian each retain complete participle entries, followed by cnucian's complete command pair. Ā, hooked e and ð are clear, with no table clipping or detached heading.",
  "44": "Āhębban, plegian and cēosan each keep complete command pairs with their rules. Tōcuman's descriptor and full six-person present-subjunctive table also fit together below; ā/ē/ō/ð and hooked e remain distinct, and the last row clears the folio.",
  "45": "Geweorðan and leornian retain complete six-row present-subjunctive displays under their explanatory paragraphs. Eth is clear, headers and values align, and the page ends after a full table.",
  "46": "Āhyldan's complete subjunctive table is followed by the repaired ondrǣdan entry: its heading and full formation/scope paragraph now remain with both strong singular and plural matrices. Long ǣ and all gender headings are clear; U17LF02 is resolved.",
  "47": "The ondrǣdan continuation is explicitly labelled Weak and contains both complete matrices. Hyngran then begins with its own heading, sense and full formation/scope rule attached to both strong matrices; no detached introduction or clipped lower row appears.",
  "48": "Hyngran's labelled weak continuation retains both complete matrices. Gesēon's preterite-subjunctive heading, sense and stem rule stay with all six person/number rows. Ē/ā marks, headers and footer are readable, and the page ends after the complete table."
}''')
def sha(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
prior_path = 'build/u17-pages-first-review-v1.json'
prior = json.loads((ROOT/prior_path).read_text(encoding='utf-8'))
assert prior['status']=='needs_revision'
assert [p['page'] for p in prior['pages']]==list(range(1,49))
manifest = json.loads((ROOT/'typesetting/ch17/build/render-manifest-final.json').read_text(encoding='utf-8'))
doc = manifest['documents']['learner']
assert doc['version']=='v2' and doc['pages']==94
assert sha(doc['pdf'])==doc['sha256']=='3e3d7adf2aefdf6044b67c04cc5ed0603069e1e1101507b98c7fa34b6d25cbe2'
assert sha('typesetting/ch17/build/chapter-17-v1.pdf')==prior['pdf_sha256']
pages = []
for n in range(1,49):
    image = doc['images'][n-1]
    image_sha = sha(image['path'])
    assert image_sha == image['sha256']
    if n <= 34:
        previous = prior['pages'][n-1]
        previous_sha = sha(previous['image_path'])
        assert previous['actually_viewed'] is True
        assert previous_sha == previous['image_sha256'] == image_sha
        row = copy.deepcopy(previous)
        row.update({
            'status':'pass',
            'inspection_method':previous['inspection_method']+' Final v2 reuse is authorized only by independently verified actual SHA-256 equality of the old and new image files.',
            'final_identity_verified':True,
            'image_path':image['path'],
            'image_sha256':image_sha,
            'personally_viewed_image':{'path':previous['image_path'],'sha256':previous_sha},
            'byte_identical_reuse':{
                'previously_actually_viewed':True,
                'sha256_equality_verified':True,
                'previously_inspected_image_path':previous['image_path'],
                'previously_inspected_image_sha256':previous_sha,
                'previous_render_version':'v1',
                'final_render_version':'v2'
            }
        })
    else:
        row = {
            'page':n,
            'status':'pass',
            'actually_viewed':True,
            'inspection_method':'Personal full-page visual reinspection of the actual final v2 150-dpi PNG with view_image; no OCR, contact-sheet or hash substitution.',
            'observations':observations[str(n)],
            'final_identity_verified':True,
            'image_path':image['path'],
            'image_sha256':image_sha,
            'personally_viewed_image':{'path':image['path'],'sha256':image_sha}
        }
    pages.append(row)
findings = copy.deepcopy(prior['findings'])
for finding in findings:
    if finding['id']=='U17LF01':
        finding.update({
            'status':'resolved_verified',
            'original_render_version':'v1',
            'resolved_render_version':'v2',
            'resolution_pages':[35,36],
            'resolution':'Personally reinspected final v2 pages 35 and 36. The complete mǣrsian participle heading, formation rule, scope paragraph and two-form table now remain together on page 35. The following entries on page 36 are complete and readable.',
        })
    if finding['id']=='U17LF02':
        finding.update({
            'status':'resolved_verified',
            'original_render_version':'v1',
            'resolved_render_version':'v2',
            'resolution_pages':[46,47],
            'resolution':'Personally reinspected final v2 pages 46 and 47. The ondrǣdan heading and full formation/scope paragraph now stay with both complete strong matrices on page 46. Its complete weak continuation is explicitly labelled on page 47, where the new hyngran introduction also stays with both strong matrices.',
        })
assert all(f['status'] in ('resolved_verified','withdrawn') for f in findings)
project_pages = sum(d['pages'] for d in manifest['documents'].values())
review = {
    'schema_version':1,
    'document':'learner',
    'reviewer':'unit17_pages_first',
    'status':'pass',
    'reviewed_at_utc':datetime.now(timezone.utc).isoformat(),
    'accepted_text_checkpoint':'a137171',
    'pdf_path':doc['pdf'],
    'pdf_sha256':doc['sha256'],
    'render_version':'v2',
    'render_dpi':150,
    'scope':f'Final learner pages 1–48 only: 48 of {doc["pages"]} learner pages, not all {project_pages} learner-plus-key pages. V1 had 141 combined pages; this review does not claim that full scope.',
    'final_scope_counts':{'reviewed_learner_pages':48,'learner_pages':doc['pages'],'combined_project_pages':project_pages},
    'full_project_review_claimed':False,
    'inspection_summary':{
        'pages_1_through_34':'Personally viewed full v1 images reused only after actual old/new SHA-256 equality was independently verified.',
        'pages_35_through_48':'Every changed final v2 full-page image personally reinspected with view_image.',
        'unresolved_material_findings':0
    },
    'findings':findings,
    'pages':pages,
    'review_history':[{
        'render_version':'v1',
        'retained_pdf':{'path':'typesetting/ch17/build/chapter-17-v1.pdf','sha256':sha('typesetting/ch17/build/chapter-17-v1.pdf')},
        'archived_review_json':{'path':prior_path,'sha256':sha(prior_path)},
        'archived_review_markdown':{'path':'build/u17-pages-first-review-v1.md','sha256':sha('build/u17-pages-first-review-v1.md')},
        'original_review':prior
    }]
}
out = ROOT/'typesetting/ch17/reviews'
(out/'learner-first.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
lines=[
    '# Unit 17 learner pages 1–48 — independent final visual review',
    '',
    '**Status: pass.** Final v2 learner pages 1–48 are accepted. Every changed page, 35–48, was personally reinspected as a full 150-dpi PNG with `view_image`. Pages 1–34 reuse personally inspected full v1 images only after actual old/new SHA-256 equality was independently verified for each page.',
    '',
    'Reviewer: `unit17_pages_first`. Accepted text checkpoint: `a137171`.',
    '',
    'Final learner PDF SHA-256: `'+doc['sha256']+'`.',
    '',
    f'This review covers **48 of {doc["pages"]} learner pages**, not the entire **{project_pages}-page learner-plus-key project**. The earlier v1 project had 141 pages. The actual final PDF and all 48 image identities were verified against the final manifest.',
    '',
    'The JSON ledger records each inspection method, actual image hash, concrete page observations, and explicit byte-identical reuse where applicable. It embeds the complete original v1 review and preserves archive identities, so the initial findings and observations remain recoverable.',
    '',
    '## Findings and repair verification',
    '',
    '- **U17LF01 — resolved and visually verified:** the mǣrsian participle heading, formation rule, scope paragraph and two-form table now stay together on final page 35. Final page 36 contains complete following entries.',
    '- **U17LF02 — resolved and visually verified:** the ondrǣdan introduction now stays with both strong matrices on final page 46; its labelled weak continuation is complete on page 47. Hyngran also keeps its introduction with both strong matrices.',
    '- The page 2 word-space query and pages 8/10 column-alignment query were withdrawn after personal lossless-detail inspection of the v1 pages; those images are byte-identical in v2.',
    '',
    'No material finding remains open in this assigned range. Reinspection checked special letters and length marks, alignment, clipping, readable type, headers/folios, sensible page breaks, and introduction-to-table connections.',
    '',
    '## Final page observations',
    '',
    '| Page | Inspection basis | Personal observation |',
    '| --- | --- | --- |'
]
for page in pages:
    basis='Verified byte-identical reuse of personally viewed v1 image' if page['page']<=34 else 'Personally reinspected final v2 full page'
    lines.append('| '+str(page['page'])+' | '+basis+' | '+page['observations'].replace('|','\\|')+' |')
(out/'learner-first.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
loaded=json.loads((out/'learner-first.json').read_text(encoding='utf-8'))
assert [p['page'] for p in loaded['pages']]==list(range(1,49))
for page in loaded['pages']:
    assert page['actually_viewed'] and page['final_identity_verified']
    assert page['status']=='pass' and page['observations'] and page['inspection_method']
    assert sha(page['image_path'])==page['image_sha256']==doc['images'][page['page']-1]['sha256']
    if 'byte_identical_reuse' in page:
        old=page['byte_identical_reuse']
        assert old['previously_actually_viewed'] and old['sha256_equality_verified']
        assert sha(old['previously_inspected_image_path'])==old['previously_inspected_image_sha256']==page['image_sha256']
print(json.dumps({'status':loaded['status'],'final_pages':len(pages),'changed_final_pages_personally_reinspected':14,'verified_identical_reuses':34,'unresolved_material_findings':0,'pdf_sha256':doc['sha256'],'combined_project_pages':project_pages}))
