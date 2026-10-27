"""Document the four metadata-only assessment-role repairs before contract freeze."""
import json,hashlib
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
p=R/'curriculum/proposals/unit16/author-only-cook-sequence-bindings.json'
expected_sha='816a0898cf8f1e108b0f6aa30f1d308c12d904893d995dad179563a621c2565a'
assert sha(p)==expected_sha
old=read(O/'author-only-cook-models.json');new=read(p);bs={x['owner_id']:x for x in new['sequences']}
expected={('EX-XII-XIII-33-03',15),('EX-XII-XIII-33-10',6),('EX-XII-XIII-34-07',18),('EX-XII-XIII-36-02',5)}
changes=[]
for m in old['items']:
    b=bs[m['source_item_id']]
    assert m['model']==b['text'] and len(m['tokens'])==len(b['tokens'])
    for a,z in zip(m['tokens'],b['tokens']):
        keys={k for k in set(a)|set(z) if not k.startswith('grammar_audit_') and a.get(k)!=z.get(k)}
        if not keys:continue
        assert keys=={'assessment_role','support_ids'},(m['source_item_id'],a['token_index'],keys)
        assert a['assessment_role']=='supplied_position_not_unaided_recall' and z['assessment_role']=='independent_production'
        assert z['form_status'] in ['previously_taught','new_production'] and z['sense_status'] in ['previously_taught','new_production']
        changes.append({'source_item_id':m['source_item_id'],'token_index':a['token_index'],'surface':a['surface'],'lemma_id':z['lemma_id'],'form_id':z['form_id'],'sense_id':z['sense_id'],'form_status':z['form_status'],'sense_status':z['sense_status'],'prior_form_production':z.get('prior_form_production'),'prior_sense_production':z.get('prior_sense_production'),'old_assessment_role':a['assessment_role'],'new_assessment_role':z['assessment_role'],'removed_inapplicable_support_ids':a['support_ids'],'linguistic_identity_and_analysis_unchanged':True})
assert {(x['source_item_id'],x['token_index'])for x in changes}==expected
out={'schema_version':1,'chapter':'ch16','origin_category':'new teaching material','record_id':'U16-G-ASSESSMENT-ROLE-REFRESH-01','recorded_at_utc':datetime.now(timezone.utc).isoformat(),'reason':'The aggregate binder had allowed a supplied form scope and a supplied sense scope to cross-contaminate distinct contextual uses. Four previously/newly taught prepositions were therefore incorrectly tagged as visibly supplied. The exact phrase-support assignments are now corrected.','upstream_binding_path':str(p.relative_to(R)).replace('\\','/'),'upstream_binding_sha256':expected_sha,'changed_positions':changes,'unchanged_scope':{'cook_models':59,'ordered_tokens':812,'model_text':True,'all_lemma_form_sense_ids':True,'all_linguistic_analyses':True,'source_prompts':True,'linguistic_amendment_count':50},'preserved_witnesses':[{'path':str(q.relative_to(R)).replace('\\','/'),'sha256':sha(q)}for q in [O/'initial-independent-models.json',O/'model-amendments.json']],'source_inventory_coordination':'The source editor is separately correcting eight reading-sense fallback selections. This does not expand the lexical proposal scope; the lexical-inventory hash is checked separately at final manifest refresh.','status':'independently_confirmed_metadata_only'}
(O/'assessment-role-refresh.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'confirmed_positions':changes,'upstream_sha256':expected_sha},ensure_ascii=False))
