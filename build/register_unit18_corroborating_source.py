"""Centrally register the checked Crawford corroboration, without assigning it."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
def read(path): return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))
def sha(path): return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
proposal_path = 'sources/audits/unit18-source/source-registry-proposal.json'
p = read(proposal_path)
registry = read('sources/registry.json')
assert p['source_id'] not in {s['source_id'] for s in registry['supporting_sources']}
assert sha(p['retrieved_pdf_path']) == p['pdf_sha256']
assert (ROOT / p['retrieved_pdf_path']).stat().st_size == p['pdf_size_bytes']
destination = ROOT / p['proposed_local_pdf']
assert not destination.exists(), 'Do not replace an existing selected source silently'
shutil.copyfile(ROOT / p['retrieved_pdf_path'], destination)
assert sha(p['proposed_local_pdf']) == p['pdf_sha256']
entry = {k:v for k,v in p.items() if k not in ['registry_action','proposed_local_pdf','retrieved_pdf_path']}
entry['local_pdf'] = p['proposed_local_pdf']
entry['proposal_record'] = proposal_path
entry['coordinator_title_inspection'] = {
    'image_path': 'sources/audits/unit18-source/crawford1922-title.png',
    'image_sha256': sha('sources/audits/unit18-source/crawford1922-title.png'),
    'pdf_page_one_based': 9,
    'actually_viewed': True,
    'observations': 'The coordinator personally read the printed title, editor S.J.Crawford, London publication for EETS by Humphrey Milford/Oxford University Press, and printed1922 date.'
}
entry['assignment_status'] = 'Supporting evidence only; no learner reading or exercise assigned from this edition.'
registry['supporting_sources'].append(entry)
registry['local_cache'].append({'path': entry['local_pdf'], 'bytes': p['pdf_size_bytes'], 'sha256': p['pdf_sha256']})
(ROOT / 'sources/registry.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Registered Crawford1922 corroboration and verified central cached copy; selected Cook assignments unchanged.')
