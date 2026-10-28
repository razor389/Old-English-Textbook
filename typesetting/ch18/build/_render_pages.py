"""One-use Unit 18 raster identity manifest. Rendering is not page inspection."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'typesetting/ch18'
GS = Path('C:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs')
p = argparse.ArgumentParser()
p.add_argument('--version', required=True)
p.add_argument('--document', choices=['learner', 'key', 'both'], default='both')
args = p.parse_args()
c = json.loads((ROOT / 'chapters/ch18/coverage.json').read_text(encoding='utf-8'))
assert c.get('textual_review', {}).get('status') == 'accepted'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rel(path):
    return path.relative_to(ROOT).as_posix()

final = OUT / 'build/render-manifest-final.json'
manifest = json.loads(final.read_text(encoding='utf-8')) if final.exists() else {
    'chapter_id': 'ch18', 'dpi': 150,
    'status': 'rendered_only_not_a_visual_review', 'documents': {}}
for document, stem in [('learner', 'chapter-18'), ('key', 'answer-key')]:
    if args.document not in ['both', document]:
        continue
    folder = OUT / 'build' / f'{document}-{args.version}'
    assert not folder.exists(), 'Use a fresh version; preserve inspected image sets'
    folder.mkdir()
    pdf = OUT / 'build' / (stem + '.pdf')
    log = (OUT / 'build' / (stem + '.log')).read_text(encoding='utf-8', errors='replace')
    pages = int(re.search(r'Output written on .*?\((\d+) pages?', log, re.S)[1])
    subprocess.run([str(GS / 'bin/gswin64c.exe'), '-I' + ';'.join(str(GS / part)
                    for part in ['Resource/Init', 'lib', 'kanji']),
                    '-sDEVICE=png16m', '-r150', '-dTextAlphaBits=4', '-dGraphicsAlphaBits=4',
                    '-dBATCH', '-dNOPAUSE', '-sOutputFile=' + str(folder / 'page-%03d.png'),
                    str(pdf)], check=True)
    images = sorted(folder.glob('page-*.png'))
    assert len(images) == pages, (stem, len(images), pages)
    manifest['documents'][document] = {'pdf': rel(pdf), 'sha256': sha(pdf), 'pages': pages,
        'version': args.version, 'images': [{'page': n, 'path': rel(image), 'sha256': sha(image)}
                                         for n, image in enumerate(images, 1)]}
text = json.dumps(manifest, ensure_ascii=False, indent=2) + '\n'
final.write_text(text, encoding='utf-8', newline='\n')
(OUT / 'build' / f'render-manifest-{args.version}.json').write_text(text, encoding='utf-8', newline='\n')
print({kind: row['pages'] for kind, row in manifest['documents'].items()}, 'rendered; not inspected')
