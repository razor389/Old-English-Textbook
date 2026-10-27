"""Acquire the original Matthew edition solely to check two supplied name forms."""
from pathlib import Path
import hashlib
import urllib.request
root=Path(__file__).resolve().parents[1]
url='https://upload.wikimedia.org/wikipedia/commons/a/a0/The_Gospel_according_to_Saint_Matthew_in_Anglo-Saxon_and_Northumbrian_versions_synoptically_arranged%2C_with_collations_of_the_best_manuscripts_%28IA_gospelaccordingt00kembrich%29.pdf'
path=root/'sources/cache/matthew_kemble_hardwick_1858.pdf'
if not path.exists():
    request=urllib.request.Request(url,headers={'User-Agent':'OldEnglishCourseSourceAudit/1.0'})
    with urllib.request.urlopen(request,timeout=60) as response:
        data=response.read()
    assert data.startswith(b'%PDF'), 'Expected primary facsimile PDF'
    path.write_bytes(data)
print(path.relative_to(root).as_posix(),path.stat().st_size,hashlib.sha256(path.read_bytes()).hexdigest())
