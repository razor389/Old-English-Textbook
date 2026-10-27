"""Resume the saved metadata-only refresh after interrupted sealing."""
import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
record=read(O/'assessment-role-refresh.json')
manifest=read(O/'manifest.json')
validation=read(O/'validation.json')
upstream=record['upstream_binding_path']
assert sha(R/upstream)==record['upstream_binding_sha256']=='816a0898cf8f1e108b0f6aa30f1d308c12d904893d995dad179563a621c2565a'
assert validation['status']=='pass' and not validation['errors'] and not validation['warnings']
assert validation['input_hashes'][upstream]==record['upstream_binding_sha256']
for witness in record['preserved_witnesses']:assert sha(R/witness['path'])==witness['sha256']
lex_path='sources/audits/unit16-source/lexical-inventory.json'
old=next(x for x in manifest['external_reconciled_inputs']if x['path']==lex_path)
assert sha(R/lex_path)==old['sha256']
record['source_inventory_coordination']='The source editor reports nine reading-sense fallback corrections after its final line-boundary check, including on at169.6 continuing into on ðǣm plegan169.7. These do not expand lexical proposal scope. The grammar auditor independently confirms that lexical-inventory.json retains the exact previously reconciled hash.'
record['source_inventory_hash_confirmation']={'path':lex_path,'sha256':old['sha256'],'unchanged_from_pre_refresh_manifest':True}
record['interruption_recovery']='The four-position linguistic-identity comparison and validation were already complete before the interrupted seal. Recovery reuses that saved audit, verifies its upstream hash and preserved witnesses, then copies the current metadata and reseals.'
(O/'assessment-role-refresh.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Saved four-position audit reused; lexical inventory unchanged; coordination updated to nine reading corrections; initial witness and50 amendments unchanged.')
