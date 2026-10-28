from pathlib import Path
import hashlib, json

root = Path(__file__).resolve().parents[1]
notes = json.loads((root / 'build/u17-pages-key-v1-observations.json').read_text(encoding='utf-8'))
manifest = json.loads((root / 'typesetting/ch17/build/render-manifest-final.json').read_text(encoding='utf-8'))
doc = manifest['documents']['key']
sha = lambda p: hashlib.sha256((root / p).read_bytes()).hexdigest()
assert doc['version'] == 'v1' and doc['pages'] == 45
pdf_sha = sha(doc['pdf'])
assert pdf_sha == doc['sha256']
pages = []
for item in doc['images']:
    n = item['page']
    actual_sha = sha(item['path'])
    assert actual_sha == item['sha256'], item['path']
    pages.append({'page': n, 'status': 'needs_repair' if n in [6,7] else 'pass', 'actually_viewed': True, 'inspection_method': notes['inspection_method'], 'observations': notes['observations'][str(n)], 'final_identity_verified': True, 'image_path': item['path'], 'image_sha256': actual_sha})
assert [p['page'] for p in pages] == list(range(1,46))
receipt = {k:v for k,v in notes.items() if k != 'observations'}
receipt.update({'status': 'needs_repair', 'pdf_path': doc['pdf'], 'pdf_sha256': pdf_sha, 'pages': pages})
path = root / 'build/u17-pages-key-v1-receipt.json'
path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print('Recorded 45 personally viewed v1 pages; actual PDF and all image hashes match manifest.')
print('PDF SHA256:', pdf_sha)
tex_path = root / 'typesetting/ch17/answer-key.tex'
if not tex_path.exists():
    candidates = list((root / 'typesetting/ch17').rglob('answer-key.tex'))
    assert len(candidates) == 1, candidates
    tex_path = candidates[0]
lines = tex_path.read_text(encoding='utf-8').splitlines()
for idx,line in enumerate(lines):
    if 'A speaker commands several listeners' in line or 'Explain the function of Apollines' in line:
        print(str(tex_path.relative_to(root)), idx+1)
        for nearby in lines[max(0,idx-3):idx+7]: print(nearby)
