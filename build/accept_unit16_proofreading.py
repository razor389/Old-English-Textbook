"""Accept only the independently confirmed reversible reference-spacing edit."""
from pathlib import Path
import hashlib,json
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,v): Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
ap='chapters/ch16/presentation-proofreading-amendment.json'
rp='chapters/ch16/reviews/presentation-proofreading.json'
a,r,c=read(ap),read(rp),read('chapters/ch16/coverage.json')
assert r['status']=='pass' and r['reviewer']=='unit16_pages_last'
assert sha(ap)==r['amendment_sha256_at_review']
assert sha('chapters/ch16/student.md')==a['student_after_sha256']==r['student']['actual_after_sha256']
assert r['student']['actual_recovered_before_sha256']==a['student_before_sha256']
assert r['student']['ascii_spaces_added']==8 and r['student']['non_whitespace_changes']==0
s=a['contract_semantic_identity_after']
actual=hashlib.sha256(json.dumps({k:c[k] for k in s['keys']},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
assert actual==s['sha256']==r['contract']['actual_after_semantic_sha256']
assert r['contract']['actual_recovered_before_semantic_sha256']==a['contract_semantic_identity_before']['sha256']
for p,h in a['unchanged_artifacts'].items(): assert sha(p)==h,p
assert c['textual_review']['status']=='proofreading_confirmation_pending'
a['status']='accepted_with_independent_confirmation'
a['non_author_review_sha256']=sha(rp)
write(ap,a)
c['textual_review']['status']='accepted'
c['textual_review']['accepted_artifacts']['student.md']={'sha256':sha('chapters/ch16/student.md'),'sha256_normalized_lf':sha('chapters/ch16/student.md')}
c['textual_review']['accepted_contract_semantic_identity']=s
c['textual_review']['proofreading_addendum']={'record':ap,'sha256':sha(ap),'review':rp,'review_sha256':sha(rp),'status':'accepted','scope':'Eight spaces only; initial linguistic reviews and witnesses preserved.'}
c['textual_review']['identity_scope_note']='Current masters and substantive contract content include independently confirmed A08 spacing corrections. Initial review hashes and the original raw contract identity remain historical, with reversible before/after identities in A08. Subsequent completion metadata does not alter teaching.'
c['initial_textual_acceptance_checkpoint']='effe431'
write('chapters/ch16/coverage.json',c)
co=read('chapters/ch16/coordinator-review.json')
co['accepted_artifacts_before_proofreading']=co['accepted_artifact_identities']
co['accepted_artifact_identities']=[{**x,**({'raw_sha256':sha('chapters/ch16/student.md'),'normalized_lf_sha256':sha('chapters/ch16/student.md')} if x['path']=='chapters/ch16/student.md' else {})} for x in co['accepted_artifact_identities']]
co['presentation_proofreading_acceptance']=c['textual_review']['proofreading_addendum']
write('chapters/ch16/coordinator-review.json',co)
print('A08 accepted after actual independent confirmation; initial reviews preserved.')
