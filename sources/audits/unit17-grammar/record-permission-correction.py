"""Append an explicit semantic correction; preserve exercise models verbatim."""
import hashlib,json,runpy
from pathlib import Path
O=Path(__file__).resolve().parent
def read(n):return json.loads((O/n).read_text(encoding='utf8'))
def digest(n):return hashlib.sha256((O/n).read_bytes()).hexdigest()
before=read('reading-verbal-bindings.json')
assert next(r for r in before['verbal_occurrences']if r['token_position_one_based']==71)['lemma_id']=='geliefan'
models_before=digest('candidate-models.json')
amendments_before={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in O.glob('model-amendments-*.json')}
runpy.run_path(str(O/'build-reading-verbs.py'),run_name='__main__')
runpy.run_path(str(O/'build-evidence-catalog.py'),run_name='__main__')
after=read('reading-verbal-bindings.json')
assert digest('candidate-models.json')==models_before
assert amendments_before=={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in O.glob('model-amendments-*.json')}
correction={'access':'author-only audit; exclude from blind reviewers','correction_id':'U17G-SEMANTIC-CORRECTION-01','trigger':'Coordinator review of the252-token reading ledger identified the stale belief interpretation at token71.','source_locator':'Cook First Book174.14–15/PDF190; note14→196d; glossary303/PDF319 and293/PDF309','evidence_refs':['U17G-FB174','U17G-FB303','U17G-FB293','U17G-FB105'],'evidence_method':'Personally re-inspected cached registered primary images; no network requests and no author translation witness consulted.','decision':'Supply exact gelīefst as permission, with mē the dative person granted permission to speak, understood from ic sęcge. Separate source-local lemma identity from earlier believe. Present indicative2sg remains unchanged.','before_occurrence':next(r for r in before['verbal_occurrences']if r['token_position_one_based']==71),'after_occurrence':next(r for r in after['verbal_occurrences']if r['token_position_one_based']==71),'before_support':next(f for f in before['whole_frame_support']if f['feature_id']=='U17-RSUP-04'),'after_support':next(f for f in after['whole_frame_support']if f['feature_id']=='U17-RSUP-04'),'preservation':{'candidate_models_sha256':models_before,'model_amendments_sha256':amendments_before,'exercise_text_unchanged':True,'reading_source_text_unchanged':True,'reading_token_positions_unchanged':True}}
(O/'semantic-correction-01.json').write_text(json.dumps(correction,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Permission correction recorded; exercise models/amendments unchanged.')
