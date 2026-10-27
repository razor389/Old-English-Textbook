"""Retrieve two fixed primary dictionary page images for the reward-hint audit."""
from pathlib import Path
import hashlib
import urllib.request

root=Path(__file__).resolve().parents[1]
folder=root/'sources/audits/unit16-coordinator'
for page in [29,30]:
    name=f'bt_b{page:04d}.jpg'
    destination=folder/name
    url='https://bosworthtoller.com/images-dictionary/'+name
    if destination.exists():
        print('Already retained:',name)
        continue
    raw=urllib.request.urlopen(url,timeout=30).read()
    assert raw.startswith(b'\xff\xd8'), 'Expected original JPEG page'
    destination.write_bytes(raw)
    print(name,hashlib.sha256(raw).hexdigest(),'downloaded, not yet inspected')
