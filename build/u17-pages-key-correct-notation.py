from pathlib import Path

root = Path(__file__).resolve().parents[1]
paths = ['build/u17-pages-key-v1-observations.json', 'build/u17-pages-key-v1-receipt.json', 'build/u17-pages-key-record-v2.py', 'build/u17-pages-key-v2-receipt.json', 'typesetting/ch17/reviews/key.json']
for name in paths:
    path = root / name
    text = path.read_text(encoding='utf-8')
    revised = text.replace('cȳmð', 'cymð')
    if revised != text:
        path.write_text(revised, encoding='utf-8')
print('Corrected reviewer-example notation to the actual printed cymð; document text and image identities unchanged.')
