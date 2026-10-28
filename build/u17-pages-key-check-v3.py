from pathlib import Path
import hashlib, json
root = Path(__file__).resolve().parents[1]
sha = lambda p: hashlib.sha256((root/p).read_bytes()).hexdigest()
manifest = json.loads((root/'typesetting/ch17/build/render-manifest-final.json').read_text(encoding='utf-8'))
old = json.loads((root/'build/u17-pages-key-v2-receipt.json').read_text(encoding='utf-8'))
doc = manifest['documents']['key']
assert doc['version'] == 'v3' and doc['pages'] == 45
assert sha(doc['pdf']) == doc['sha256']
assert sha('typesetting/ch17/build/answer-key-v2.pdf') == old['pdf_sha256']
assert sha('typesetting/ch17/build/answer-key-v1.pdf') == old['initial_v1_review']['pdf_sha256']
changed, identical = [], []
for item, prior in zip(doc['images'],old['pages']):
    assert item['page'] == prior['page']
    actual = sha(item['path'])
    assert actual == item['sha256']
    assert sha(prior['image_path']) == prior['image_sha256']
    provenance = prior['personally_viewed_image']
    assert sha(provenance['path']) == provenance['sha256'] == prior['image_sha256']
    if actual == prior['image_sha256']: identical.append(item['page'])
    else: changed.append(item['page'])
assert changed + identical and len(changed) + len(identical) == 45
result = {'version':'v3','pdf_path':doc['pdf'],'pdf_sha256':sha(doc['pdf']),'changed_pages':changed,'byte_identical_to_v2_pages':identical,'key_pages':45,'learner_pages':manifest['documents']['learner']['pages']}
(root/'build/u17-pages-key-v3-identity-check.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
