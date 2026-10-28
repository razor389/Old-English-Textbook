"""Fetch fixed registered BT facsimiles; text searches remain finding aids."""
import urllib.request
from pathlib import Path
OUT=Path(__file__).resolve().parent
for n in [478,495,742,746,747,750,751,162,1247,1248,1249]:
    dest=OUT/f'bt_b{n:04}.jpg'
    if dest.exists():continue
    url=f'https://bosworthtoller.com/images-dictionary/bt_b{n:04}.jpg'
    with urllib.request.urlopen(url,timeout=40) as r: data=r.read()
    dest.write_bytes(data)
    print(n,len(data))
