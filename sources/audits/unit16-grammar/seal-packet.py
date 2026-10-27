"""Seal this agent's reconciled proposal; never write shared contracts/registers."""
import json,hashlib,copy
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
def read(p):return json.loads((R/p).read_text(encoding='utf8'))
def save(p,d):(O/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
V=read('sources/audits/unit16-grammar/validation.json')
assert V['status']=='pass' and not V['errors'] and not V['warnings'],V
B=read('curriculum/proposals/unit16/author-only-cook-sequence-bindings.json');BS={x['owner_id']:x for x in B['sequences']}
BR=read('curriculum/proposals/unit16/author-only-cook-binding-review.json');assert not BR['errors'],BR['errors']
D=read('sources/audits/unit16-grammar/exercises-verbal-dependencies.json');DS={x['source_item_id']:x for x in D['items']}
M=read('sources/audits/unit16-grammar/author-only-cook-models.json')
N=read('sources/audits/unit16-grammar/grammar-records.json')
old=read('lexicon/entries.json')['lemmas']
forms={f['form_id']:f for l in old for f in l['forms']};senses={s['sense_id']:s for l in old for s in l['senses']}
for packet in [N,read('sources/audits/unit16-grammar/source-support.json'),read('sources/audits/unit16-grammar/reading-verbal-support.json')]:
    for l in packet['lemmas']:
        for f in l['forms']:forms[f['form_id']]=f
        for s in l['senses']:senses[s['sense_id']]=s
variants={
'32-02':'A separately evidenced anterior perfect may be valid in a different composition, but the selected simple preterite is sufficient and taught; do not require a perfect merely because English has had.',
'32-05':'The uncontracted ne wāst is selected. The abandoned nǣtst was neither an assigned negative paradigm cell nor a supported target; no replacement negative-witan table is implied.',
'32-08':'The selected worpen is the prior productive base. A separately evidenced prefixed participle or weak adjective choice cannot silently replace its target identity. The actual supplied better-clause controls are retained.',
'32-11':'First-singular funde is a previously documented unselected alternative; the actual course-selected first-singular cell is fand. The attributive strong neuter forloren is the assigned choice; do not assess its prior malformed weak ending as equivalent.',
'33-03':'Faran fōr expresses unqualified journeyed. A separately evidenced fēran system could also express travel, but it is not introduced here. Actual selected nōm is used rather than silently adopting nam.',
'34-03':'The original167.13 has mīne lȳtlan ǣhta. The exercise requires books; the model selects prior mīna bēc. Do not restore the initial mistaken hooks reading.',
'34-07':'The plain perception infinitives are explicitly licensed. Agreeing participles may belong to other attested constructions, but the abandoned unsupplied participles are not independent targets here.',
'34-09':'Cumenne is directly printed in Matthew16.27; its apparatus A cumanne supports the selected existing course form. Both are linguistic variants, while the model uses cumanne. The reward headword correction is substantive, not an optional spelling change.',
'34-13':'Cook permits the g-containing weak-II spelling series; a documented wuldrige is not the selected wuldrie cell. Keep the requested final reported verb regardless of an admissible spelling variant.',
'35-03':'The selected genitive route is explicitly attested. The initial accusative route proposal is not retained as an unevidenced equivalent.',
'35-04':'A finite comparison can repeat the lexical playing action instead of using dōn, provided the action, tense and agreement remain; this unit specifically practises the evidenced substitute-action option.',
'35-05':'A finite comparison can repeat the singing verb rather than substitute dōn. Retaining narrated nū is a source target; a change to then is not merely a free spelling alternative.',
'35-12':'BT documents smire beside the selected Cook/Wright smiere spelling. Distinguish historical validity from compliance with the selected ie paradigm.',
'35-14':'Frige is the exact supported plural. Frēo is not an interchangeable selected plural merely because it is the dictionary headword.',
'36-01':'Cook55 expressly selects the shortened plural before following gē. Broader historical variability is not denied, but the course target here is dēme gē; the second ordinary command remains dēmað.',
'36-03':'The exact negative cessation clause contains both negatives; omitting or translating the inner ne independently changes the supplied construction. Prior inēode is selected instead of an unsupported separate inn spelling.',
'36-04':'BT records i/y spelling variants such as smirede and smyredest. Selected smieredest must retain second-singular -st, while smierede is third singular; a spelling alternative does not erase this contrast.',
'36-06':'An expanded relative sentence could express the sense, but the source controls a compact attracted-relative pattern. The complete selected pattern is supplied, so the task does not assess unaided invention of case attraction.',
'36-08':'The resumptive accusative ðæt distinguishes the giving object from internally genitive hwæs. A different free-choice construction requires its own evidenced government; English whatever does not make every internal case accusative.',
'36-09':'The primary source has initial I in Iohannes; the model’s J follows the explicitly declared Cook-headword normalization. This is separate from the case analysis.',
'36-10':'The primary source has initial I in Iohannem; the model’s J is declared normalization. Keep the accusative ending; the unchanged dictionary nominative is not the selected object.'}
for m in M['items']:
    i=m['source_item_id'];short=i.removeprefix('EX-XII-XIII-');b=BS[i];d=DS[i]
    assert b['text']==m['model']
    m['tokens']=copy.deepcopy(b['tokens'])
    for t in m['tokens']:
        f=forms.get(t['form_id'],{});s=senses.get(t['sense_id'],{})
        t['grammar_audit_teaching_route_ids']=sorted(set(f.get('teaching_ids',[])+s.get('teaching_ids',[])))
        t['grammar_audit_paradigm_ids']=[p['paradigm_id'] for p in N['paradigms'] if t['form_id'] in {x['form_id']for x in p['forms']}]
    m['required_form_ids']=b['required_form_ids'];m['required_sense_ids']=b['required_sense_ids']
    m['required_feature_ids']=sorted(set(d['new_productive_feature_ids']+[x['feature_id']for x in d['prior_feature_dependencies']]+d['visible_supplied_feature_ids']))
    m['initial_questions']=m.get('initial_questions',m.get('unresolved',[]));m['unresolved']=[]
    m['question_resolution_ref']='sources/audits/unit16-grammar/exercises-verbal-dependencies.json#'+i
    m['control_and_interpretation_audit']=d['interpretation_and_control_audit']
    m['alternative_boundary']=variants.get(short,'The selected response is a verified model, not a claim that every other Old English wording is invalid. Assess any alternative separately for the exact meaning, government, agreement and stated source controls; this audit does not invent an additional full alternative without evidence.')
    if any(t['lemma_id']=='se' and t['surface']=='ðǣm' for t in m['tokens']):m['documented_article_variant']='Cook50 also prints dative ðām. The new model uses actual prior selected ðǣm; the variant is not a change to the original reading.'
    m['review_status']='verbal_and_construction_audit_reconciled_with_exact_token_bindings'
M['status']='sealed_author_only_audit_proposal';M['sealed_binding_source']='curriculum/proposals/unit16/author-only-cook-sequence-bindings.json';M['sealed_binding_sha256']=sha(M['sealed_binding_source'])
save('author-only-cook-models.json',M)
D['status']='sealed_verbal_dependency_decisions';D['models_awaiting_binding_regeneration']=[];save('exercises-verbal-dependencies.json',D)
for name in ['grammar-records.json','source-support.json','reading-verbal-support.json']:
    x=read('sources/audits/unit16-grammar/'+name);x['status']='sealed_audit_proposal';save(name,x)
review={'schema_version':1,'chapter':'ch16','auditor_role':'linguistic/verbal analyst; later fresh review is separate','status':'reconciled','independence_statement':'The frozen initial59 selected models predate the design agent’s bindings. The grammar auditor personally inspected the source prompt images and the primary images named in its evidence catalog, read actual earlier contracts and relevant exact cumulative records, and independently reviewed all final verbal bindings. This is not claimed as blind review of a future answer key.','baseline':{'commit':'e1d94be','lemmas':955,'forms':10470,'senses':1207,'features':950},'checks':[{'scope':'All59 Cook items','result':'Exact prompts and controls preserved; 812 ordered tokens bound; lexical government, person/number/tense/mood and source supports reconciled.'},{'scope':'New verbal systems','result':'30 complete clearly bounded paradigms with208 cells;14 full indicative systems,8 command pairs,2 present-subjunctive systems,4 participial base pairs,2 infinitive pairs. Principal parts and selected stem/ending alternations are explicit; full tables do not grant every construction.'},{'scope':'New form tasks F01–F04','result':'Independently checked all verbal target forms and explanations against the selected systems: strong stem changes, weak spelling/stem contrasts, command numbers, subjunctive numbers and infinitives.'},{'scope':'F05 nominal tasks','result':'Checked exact outputs for consistency with the source editor’s selected nearu/bēgen tables; primary nominal-table audit belongs to the source editor.'},{'scope':'Original A03/C01/C02/C03 and model examples','result':'Reviewed anterior/intended-later viewpoint, dative speech recipient, cunnan personal/skill versus witan content, and action comparison/substitute dōn. No exclusive persons/facts distinction is taught.'},{'scope':'Selected reading168.1–170.16','result':'43 exact verbal support entries supplied to the source editor’s444-token ledger. Reading-only forms remain locally supplied unless a narrower actual prior/new productive identity proves the form and use. Source editor separately records new content-geseon and impersonal-seeming senses.'},{'scope':'Primary evidence','result':'91 locally hashed evidence records; no unresolved grammar evidence references. Matthew132 directly closes is tō cumanne; Cook106 is only the general inflected-infinitive framework.'},{'scope':'Initial witness and repairs','result':'Initial-independent-models.json unchanged;50 explicit amendment records retained. The former37MB unused register duplicate was compacted to a3558-byte identity/count receipt, not treated as primary linguistic evidence.'}],'material_resolutions':['34.3 source reads books, an audit transcription repair, not a Cook error.','34.9 printed āgyltan§113 is retained and explicitly corrected to āgyldan strongIII; only the exact reward clause is supplied.','36.3 exact cessation construction retains both ne; no general arbitrary negative-complement rule is taught.','36.6 first lǣs is adverbial accusative, second is nominative amount/passive subject.','36.1 dēme before gē is newly and narrowly taught; Unit4’s explicit earlier exclusion remains unchanged.','New compositions use the actual prior masculine sǣ and selected nominal/verb variants; original reading variants remain exact.'],'remaining_material_blockers':[],'authoring_boundary':'No learner lesson or answer-key prose has been written by this agent. Authoring awaits the coordinator’s committed coverage contract and explicit assignment.','later_translation_witness_plan':'Before consulting any complete English reading translation, prepare a translation from the actual OE and record that witness. Existing exposure to specific debated clauses is acknowledged; no claim of total blindness is made.'}
if (O/'assessment-role-refresh.json').exists():
    review['pre_contract_assessment_role_refresh']=read('sources/audits/unit16-grammar/assessment-role-refresh.json')
save('review-report.json',review)
files=[p for p in sorted(O.iterdir()) if p.is_file() and p.name not in ['manifest.json']]
manifest={'schema_version':1,'chapter':'ch16','packet':'unit16-grammar','status':'sealed_audit_proposal','sealed_at_utc':datetime.now(timezone.utc).isoformat(),'baseline_commit':'e1d94be','counts':{'cook_items':59,'ordered_model_tokens':812,'paradigms':30,'paradigm_cells':208,'features':50,'cook_scaffolds':14,'reading_verbal_entries':43,'evidence_records':91,'model_amendments':50},'initial_witness':{'path':'sources/audits/unit16-grammar/initial-independent-models.json','sha256':sha('sources/audits/unit16-grammar/initial-independent-models.json'),'preserved':True},'files':[{'path':str(p.relative_to(R)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in files],'external_reconciled_inputs':[{'path':p,'sha256':sha(p)}for p in ['lexicon/entries.json','curriculum/grammar.json','sources/audits/unit16-source/exercises-prompts.json','sources/audits/unit16-source/lexical-inventory.json','sources/audits/unit16-source/exercise-support.json','curriculum/proposals/unit16/author-only-cook-sequence-bindings.json','curriculum/proposals/unit16/author-only-form-models.json','curriculum/proposals/unit16/author-only-form-bindings.json']],'remaining_material_blockers':[],'scope_limit':'Seals this bounded audit proposal, not the still-unwritten chapter or its future independent review. Coordinator owns shared integration and Git/Beads checkpoint.'}
save('manifest.json',manifest)
print('Sealed59 models/812 tokens;30 paradigms/208 cells;91 evidence records; no material grammar blockers.')
