"""Write only the blind review artifacts, after the reviewer's final manual readback.

The expected identities deliberately prevent silently accepting a later master.
Do not rerun against changed masters without a new substantive review.
"""
import hashlib, importlib.util, json, re
from pathlib import Path

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def sha(raw):
    return hashlib.sha256(raw).hexdigest()
def receipt(path):
    raw = Path(path).read_bytes()
    return {'path':path,'raw_sha256':sha(raw),'normalized_lf_sha256':sha(raw.replace(b'\r\n',b'\n')),'bytes':len(raw)}
def write(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')

spec = importlib.util.spec_from_file_location('review_data','build/u17-blind-review-data.py')
data = importlib.util.module_from_spec(spec)
spec.loader.exec_module(data)
c = read('chapters/ch17/coverage.json')
intake = read('chapters/ch17/reviews/blind-intake.json')
s = Path('chapters/ch17/student.md').read_text(encoding='utf-8')
k = Path('chapters/ch17/answer-key.md').read_text(encoding='utf-8')
w = Path('chapters/ch17/independent-solutions.md').read_text(encoding='utf-8')
expected = {
 'chapters/ch17/student.md':'f387f880e0423dd8c6adddf9765cba7b05d10bbe3850fc8593045fcfeec9d05a',
 'chapters/ch17/answer-key.md':'c6710364dde62f50c01f7bfeab57fd6ed813dddaa13d6860cfd55e75b5b2a81d',
 'chapters/ch17/independent-solutions.md':'32d031c180ea67429cf2772ffc1e009596f82eb8c1851c8c8a93375d88985a36',
 'chapters/ch17/reviews/blind-intake.json':'52754b181033b985ed404d9d247f4a605bdda5777550ac0a63338ab89c0ea9c1',
 'chapters/ch17/coverage.json':'c950af9623d38584c23730bc6c7ae1d4fc685fcc22015bf6ae0e47e0fb405056',
}
for path, digest in expected.items():
    assert receipt(path)['raw_sha256'] == digest, 'Changed after final manual readback: '+path

# The earlier curriculum and actual registers still equal the blind intake.
prior_preservation = []
for old in intake['earlier_active_contracts'] + intake['actual_registers']:
    now = receipt(old['path'])
    assert now['raw_sha256'] == old['sha256'], old['path']
    prior_preservation.append(now)

task_ids = re.findall(r'<!-- item: ([^ ]+) -->',s)
contract_tasks = {t['task_id']:t for t in c['assigned_items']}
assert set(task_ids) == set(contract_tasks)
tasks = [contract_tasks[tid] for tid in task_ids]
outputs = [o['output_position_id'] for t in tasks for o in t['output_positions']]
assert len(task_ids) == 103 and len(outputs) == 146
assert set(data.NOTES) == set(task_ids)
assert all(len(data.NOTES[t['task_id']]) == len(t['output_positions']) for t in tasks)
for text in [s,w]:
    assert re.findall(r'<!-- item: ([^ ]+) -->',text) == task_ids
    assert re.findall(r'<!-- output: ([^ ]+) -->',text) == outputs
assert re.findall(r'<!-- key: KEY-([^ ]+) -->',k) == task_ids
assert re.findall(r'<!-- output: ([^ ]+) -->',k) == outputs

models = {m.group(1):m.group(2).strip() for m in re.finditer(r'<!-- key: KEY-(EX-[^ ]+) -->(.*?)<!-- output:',k,re.S)}
frozen_models = read('sources/audits/unit17-grammar/candidate-models.json')['rows']
assert len(models) == len(frozen_models) == 82
for row in frozen_models:
    assert models[row['source_item_id']] == row['model'],row['source_item_id']
for t in tasks:
    if t['task_id'].startswith('EX-'):
        assert t['prompt'] in s and "**Cook's prompt:** "+t['prompt'] in k,t['task_id']

# All 235 original controls are exact substrings at their recorded prompt positions.
by_task = {t['task_id']:t for t in tasks}
controls = c['source_task_crosswalk']['original_controls']
assert len(controls) == 235
for ctrl in controls:
    prompt = by_task[ctrl['task_id']]['prompt']
    assert prompt[ctrl['character_start_zero_based']:ctrl['character_end_exclusive']] == ctrl['literal_source_text'],ctrl['reference_id']

# The model packet remains immutable; five explicit contract overlays take precedence.
model_bindings = read('curriculum/proposals/unit17/author-only-cook-sequence-bindings.json')['sequences']
bindings = {row['owner_id']:row for row in model_bindings}
token_count = 0
amended_output_count = 0
token_route_summary = []
for tid, model in models.items():
    t = by_task[tid]
    out = t['output_positions'][0]
    toks = t.get('assessed_output_tokens',bindings[tid]['tokens'])
    assert ' '.join(x['literal'] for x in toks) == model,tid
    for token in toks:
        pos = token['token_index']
        for kind, refkey in [('form','reference_output_positions'),('sense','reference_sense_output_positions')]:
            rid = token[kind+'_id']
            assert rid in out['required_output_'+kind+'_ids'],(tid,pos,kind)
            role = token.get(kind+'_assessment_role',token['assessment_role'])
            if role == 'independent_production':
                assert rid in out['tested_'+kind+'_ids'],(tid,pos,kind,'test')
                assert pos not in out.get(refkey,[]),(tid,pos,kind,'reference conflict')
            elif role == 'visible_reference_position':
                assert pos in out.get(refkey,[]),(tid,pos,kind,'reference missing')
        if token.get('amendment_id') == 'U17-A02':
            amended_output_count += 1
            assert token['independent_recall_assessment'] is False
            assert token['reference_route_ids']
            if token['surface'].rstrip(':') == 'cweðende':
                assert token['contextual_analysis']['number'] == 'pl'
    token_count += len(toks)
    token_route_summary.append({'task_id':tid,'model_tokens_checked':len(toks),'canonical_overlay':bool(t.get('assessed_output_tokens')),'status':'verified'})
assert amended_output_count == 11

amendment_checks = []
amendment = next(a for a in c['amendments'] if a['amendment_id']=='U17-A02')
for change in amendment['changes']:
    t = by_task[change['task_id']]
    help_row = next(x for x in t['local_support'] if x['support_id']==change['support_id'])
    assert help_row['exact_help_text'] == change['exact_help_text']
    assert change['exact_help_text']+' — '+change['meaning_and_analysis'] in s
    feature = next(x for x in c['grammar_inventory'] if x['feature_id']==change['feature_id'])
    assert feature['knowledge_status'] == 'supplied'
    seq = next(x for x in t['input_sequences'] if x['sequence_id']==change['support_id'])
    assert seq['text'] == change['exact_help_text']
    for token in seq['tokens']:
        assert token['independent_recall_assessment'] is False
        assert change['support_id'] in token['reference_route_ids']
    out = t['output_positions'][0]
    assert change['feature_id'] in out['supplied_feature_ids']
    assert change['feature_id'] not in out['tested_feature_ids']
    assert set(change['reference_positions']) <= set(out['reference_output_positions'])
    assert set(change['reference_positions']) <= set(out['reference_sense_output_positions'])
    amendment_checks.append({'task_id':t['task_id'],'feature_id':change['feature_id'],'help':change['exact_help_text'],'reference_positions':change['reference_positions'],'input_token_count':len(seq['tokens']),'status':'verified'})
assert len(amendment_checks)==5

# Reading text and apparatus identity after only the declared presentation operations.
r = c['source_spans'][0]
a=s.index('<!-- source: FB-XII-APOLLONIUS-MUSIC-PERFORMANCE -->')
b=s.index('### Finding the cited lines',a)
st=re.sub(r'<!--.*?-->','',s[a:b])
st=re.sub(r'\[\^[^]]+\]','',st)
assert ' '.join(st.split())==' '.join(r['learner_text'].split())
notes={m.group(1):' '.join(m.group(2).split()) for m in re.finditer(r'^\[\^(P\d+N[^]]+)\]:[ \t]*(.*?)(?=\n[ \t]*\n|\Z)',s,re.M|re.S)}
assert len(notes)==19
for n in r['original_notes']:
    label=f"P{n['printed_page']}N{n['original_note_number']}"
    assert notes[label]==' '.join(n['original_text'].split()),label
anchors=re.findall(r'\[\^(P\d+N[^]]+)\]',s[a:b])
assert len(anchors)==20 and anchors.count('P174N17')==2

deps = read('build/u17-blind-dependency-check.json')
assert deps['status']=='pass' and not deps['errors']
assert deps['contract_raw_sha256']==expected['chapters/ch17/coverage.json']

def blocks(text):
    matches=list(re.finditer(r'<!-- output: ([^ ]+) -->',text))
    return {m.group(1):text[m.end():matches[i+1].start() if i+1<len(matches) else len(text)].strip() for i,m in enumerate(matches)}
wb,kb=blocks(w),blocks(k)
task_reviews=[]
output_reviews=[]
for t in tasks:
    tid=t['task_id']
    task_reviews.append({'task_id':tid,'status':'accepted','key_id':t['key_id'],
      'output_position_ids':[o['output_position_id'] for o in t['output_positions']],
      'review_basis':data.NOTES[tid],
      'source_control_ids':[x['reference_id'] for x in t.get('source_control_records',[])],
      'visible_support_ids':[x['support_id'] for x in t.get('local_support',[])],
      'assessment_note':'Acceptance concerns the task, final model, explanation and support; an explicitly recorded witness error is not erased or graded as correct.'})
    for i,o in enumerate(t['output_positions']):
        oid=o['output_position_id']
        output_reviews.append({'output_position_id':oid,'task_id':tid,'status':'accepted',
          'requested_response_language':o['response_language'],'target':o['target'],
          'comparison':data.NOTES[tid][i],
          'witness_response_block_sha256':sha(wb[oid].encode('utf-8')),
          'key_response_block_sha256':sha(kb[oid].encode('utf-8')),
          'tested_form_ids':o.get('tested_form_ids',[]),'tested_sense_ids':o.get('tested_sense_ids',[]),
          'tested_feature_ids':o.get('tested_feature_ids',[]),'supplied_feature_ids':o.get('supplied_feature_ids',[])})

findings=[
 {'finding_id':'B17-01','severity':'material','status':'resolved_verified','tasks':['EX-XII-XIII-40-01'],
  'problem':'Visible betwēox help omitted its dative complement although the witness needed that government.',
  'resolution':'U17-A02 supplies betwēox wīfum and its dative explanation; both components are reference positions in this task.',
  'evidence':['Cook186.12; glossary278','actual ch09 supplied accusative phrases do not establish general productive government'],
  'verification':'Final learner, key, four supplied feature/role layers, input/output tokens and primary images reread.'},
 {'finding_id':'B17-02','severity':'material','status':'resolved_verified','tasks':['EX-XII-XIII-42-05','EX-XII-XIII-42-08'],
  'problem':'The productive cweðende base did not grant independently productive accompanying speech, which earlier u07 explicitly kept supplied.',
  'resolution':'Both tasks now print ðus cweðende with its accompanying speech function. A supplied feature, teaching record and complete references are present; occurrence analysis explicitly gives plural angels/soldiers.',
  'evidence':['Cook195.3–4 and126.11 directly attest the expression with singular God','Cook100§179 and existing participial agreement support the declared plural application'],
  'verification':'No promotion of the historical construction; old form analysis is retained separately from new plural occurrence analysis.'},
 {'finding_id':'B17-03','severity':'material','status':'resolved_verified','tasks':['EX-XII-XIII-43-13'],
  'problem':'Headword tōgēanes did not tell the learner its dative complement or the selected postposition.',
  'resolution':'Complete him tōgēanes with explicit dative and postposition is visible and locally reference-only.',
  'evidence':['Cook184.7 tōgēanes ðǣm cyninge','Cook106§201 postposition; glossary316'],
  'verification':'The witness’s alternative order remains valid language; no new global government milestone is inferred.'},
 {'finding_id':'B17-04','severity':'material','status':'resolved_verified','tasks':['EX-XII-XIII-43-15'],
  'problem':'The key claimed a supplied acceptable-to frame, but visible help gave only the adjective and not dative God.',
  'resolution':'Contiguous Gode swā gecwēme, its dative relation and predicate analysis are now supplied as one frame with all three reference positions.',
  'evidence':['Cook184.9–10 Dianan swā gecwēme and note5 See165','Cook95§165; glossary291'],
  'verification':'Final help, feature, expanded teaching record and both token routes verified.'},
 {'finding_id':'B17-05','severity':'material','status':'resolved_verified','tasks':['EX-XII-XIII-41-08'],
  'problem':'The key called its weak adjective an indicated choice, although the original/visible prompt does not require weak.',
  'resolution':'Key now explicitly accepts strong ūrne dæghwāmlīcne hlāf alongside its weak model, both prompt-compliant.',
  'evidence':['Cook Exercises26.41.8','Cook38§55 sometimes weak after possessive','actual ch03 contract and teaching'],
  'verification':'Final key paragraph read directly; the blind strong answer is a valid alternative, not an error.'},
 {'finding_id':'B17-06','severity':'verification_concern','status':'adjudicated','tasks':['EX-XII-XIII-43-15'],
  'problem':'Witness adds ne before sīe whereas the model uses bare nān.',
  'resolution':'Both are defensible. BT709 nán I(a) expressly attests use without other negatives; the final key explicitly allows the earlier negative-concord pattern too.',
  'evidence':['https://bosworthtoller.com/23433','build/u17-blind-bt-b0709.jpg'],
  'verification':'Post-unlock primary dictionary text lookup and personal page-image inspection; this is not retroactive learner support.'},
 {'finding_id':'P17-01','severity':'material','status':'resolved_verified','problem':'Overgeneralized gecweðan preterite alternation.',
  'resolution':'Final prose distinguishes gecwæð æ/ð from gecwǣde/gecwǣdon ǣ/d; table remains correct. Cook63 personally viewed.'},
 {'finding_id':'P17-02','severity':'material','status':'resolved_verified','problem':'Mægen powers and cwēn princess described globally as supplied.',
  'resolution':'Final key calls the senses taught while local source hints remain reference positions where actually given.'},
 {'finding_id':'P17-03','severity':'material','status':'resolved_verified','problem':'39.4 desired content called purpose.',
  'resolution':'Final learner states the clause expresses what all nations desired and cites194b. It no longer exposes the assessed finite gewilnodon.'},
 {'finding_id':'P17-04','severity':'material','status':'resolved_verified','problem':'37.8 singular storm prose contradicted plural source spirits.',
  'resolution':'Final learner names the spirits of the storms as actors. It no longer exposes assessed dōð.'},
 {'finding_id':'P17-05','severity':'minor','status':'resolved_verified','problem':'40.6 local help pluralized seat.',
  'resolution':'Final learner says seat; original prompt and model retain singular setle.'},
 {'finding_id':'P17-followup-reference-leaks','severity':'material','status':'resolved_verified','problem':'Intermediate P17 prose repairs printed assessed dōð and gewilnodon locally.',
  'resolution':'Both finite answers removed from the final learner help, while the corrected plural/content explanations remain and independent-production bindings remain unchanged.'},
]

image_receipts=[]
for path,(printed,pdf,observation) in data.IMAGE_NOTES.items():
    rec=receipt(path)
    rec.update({'printed_page':printed,'pdf_page_one_based':pdf,'actually_viewed':True,'phase':'after_explicit_comparison_unlock',
      'observations':observation,
      'scan_convention':'Cook printed page plus16 = one-based PDF page' if pdf is not None else 'Image identified by printed page; no independently claimed PDF index'})
    image_receipts.append(rec)

mutable={'status','review_status','completion','amendments','textual_review','presentation_review','contract_checkpoint','complete_drafts_checkpoint','independent_solutions_checkpoint','accepted_text_checkpoint'}
semantic_keys=sorted(set(c)-mutable)
semantic=sha(json.dumps({key:c[key] for key in semantic_keys},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8'))
artifacts=[receipt(path) for path in ['chapters/ch17/student.md','chapters/ch17/answer-key.md','chapters/ch17/independent-solutions.md']]
ledger={
 'schema_version':1,'chapter_id':'ch17','status':'accepted_pre_export','reviewer':'unit17_blind',
 'counts':{'tasks':103,'requested_output_positions':146,'attempted_before_key':146,'cook_items_and_models':82,'complete_reading_divisions':3,
   'original_reading_notes':19,'original_reading_note_anchors':20,'material_open_findings':0,'primary_images_personally_viewed':len(image_receipts),
   'assessed_record_routes_checked':deps['tested_routes_checked'],'cook_model_tokens_checked':token_count},
 'independence':{'blind_solutions_checkpoint':'ed28a8e','no_current_author_role':True,'all_tasks_solved_before_key_access':True,
   'coordinator_explicit_unlock_received':True,'unchanged_witness_preserved':True,'blind_intake_preserved':True,
   'blind_learner_raw_sha256':intake['learner']['sha256'],'blind_intake_identity':receipt('chapters/ch17/reviews/blind-intake.json'),
   'access_attestation':intake['access_attestation'],
   'phase_distinction':'Only after root explicitly reported full response readback and the unchanged ed28a8e checkpoint did this reviewer access the key, current contract, packets, other reviews and primary evidence. No author role, Beads write or Git mutation was performed.',
   'post_unlock_external_lookup':['https://bosworthtoller.com/23433','https://bosworthtoller.com/images-dictionary/bt_b0709.jpg']},
 'accepted_artifact_identities':artifacts,
 'accepted_contract_semantic_identity':{'keys':semantic_keys,'sha256':semantic},
 'accepted_contract_raw_identity':receipt('chapters/ch17/coverage.json'),
 'task_reviews':task_reviews,'output_position_reviews':output_reviews,'findings':findings,
 'primary_evidence_image_inspections':image_receipts,
 'amendment_reviews':[{'amendment_id':'U17-A01','status':'verified','detail':'Space before174.8 is present; task and source content unchanged.'},
   {'amendment_id':'U17-A02','status':'verified','detail':'Four supplied features, five task applications,420 teaching records,11 output/11 input reference tokens; direct plural contextual analyses and unchanged prior milestones verified.','applications':amendment_checks}],
 'source_and_dependency_review':{'original_cook_controls_verified':len(controls),'all82_original_prompt_and_model_strings_preserved':True,
   'reading_text_exact_after_declared_presentation':True,'all19_original_notes_exact_after_whitespace_normalization':True,'twenty_anchors_including_both174N17':True,
   'assessment_route_check':'build/u17-blind-dependency-check.json','recognition_boundary':'The27 English interpretation positions may assess the new recognition feature with visible inputs; they do not grant independent OE production.',
   'model_token_route_checks':token_route_summary,'earlier_contract_and_register_receipts':prior_preservation,
   'audit_limits':'Automated identity/milestone checks supplement, rather than replace, the independently solved responses, the item-specific linguistic comparisons and the personally viewed source evidence.'},
 'witness_differences':{'selected_morphology_correction':['38.2: frozen Sum cwēn should be selected Sumu cwēn.'],
   'selected_orthography_corrections':['37.2 and42.5: frozen englas omits selected hook in ęnglas.','40.1: frozen engel omits selected hook in ęngel.'],
   'analysis_correction':['39.4: frozen desired-content/purpose wording is narrowed here to desired content.'],
   'defensible_alternatives':'Other significant differences are adjudicated at their actual output positions, including daily-bread strong/weak, direct/preposed tōgēanes, ne concord, choice relatives, maiden synonyms and source-controlled versus optional ordering.'},
 'final_reread':'All final changed learner/key passages, the five canonical token overlays, both amendments and the substantive contract were reread after the final repair-induced hints were removed. Accepted identities above are the actual resulting files.',
 'scope_limit':'Textual acceptance only. Export parity, every-page visual inspection, cumulative register integration and coordinator completion remain separate gates.'
}
write('chapters/ch17/review-ledger.json',ledger)

md = f'''# Unit 17 independent textual review

Accepted before export by `unit17_blind`, a fresh non-author. All **103 tasks and146 requested outputs**, including all82 Cook compositions and the complete three-part reading translation, have individualized comparisons in [review-ledger.json](review-ledger.json). No material finding remains open. This accepts the final teaching, tasks and key; it does not certify the exports or register integration.

The original [independent solutions](independent-solutions.md) and [blind intake](reviews/blind-intake.json) remain unchanged. All actual responses were written before current-key/contract/audit access. Root read them in full and froze them at `ed28a8e` before explicitly unlocking comparison. The initial learner hash was `{intake['learner']['sha256']}`. No Beads command or Git mutation was performed by this reviewer.

## Findings and verified repairs

| Finding | Actual final resolution |
| --- | --- |
| B17-01,40.1 | Complete **betwēox wīfum**, dative complement and task-only reference positions now supplied. Earlier ch09 accusative phrase exposure did not teach this government. |
| B17-02,42.5/8 | Complete **ðus cweðende** now supplied in both tasks. Plural occurrence analysis is explicit; the historical form record and earlier supplied construction milestone remain unchanged. |
| B17-03,43.13 | Complete **him tōgēanes**, dative complement and postposition now supplied. |
| B17-04,43.15 | Complete contiguous **Gode swā gecwēme**, dative person and predicate agreement now supplied. |
| B17-05,41.8 | Key accepts both strong **dæghwāmlīcne** and its weak model **dæghwāmlīcan**; the prompt did not mandate weak. |
| P17-01–05 | Final prose correctly limits gecweðan’s æ/ð versus ǣ/d alternation; calls powers/princess senses taught; calls39.4 desired content; retains plural storm spirits and singular seat. |
| Subsequent hint check | Intermediate answers dōð and gewilnodon were removed from local help. Their independent-production status remains valid. |

The four support repairs are bounded applications of direct source evidence, not new general production milestones. I personally viewed Cook186.12 for **betweox** plus the dative group;184.7 for **tōgēanes** plus dative;184.9–10 and note5/§165 for **gecwēme**;195.3–4 and126.11 for accompanying **ðus cweðende**. The latter source subjects are singular. Applying the supplied expression to plural angels/soldiers uses the already evidenced participial agreement; it is not claimed as a verbatim plural attestation. Cook106§201 supports postposition. All11 amended output tokens and11 input copies have direct reference routes and exclude independent recall.

The43.15 model’s bare **nān** and the witness’s **ne sīe** were separately adjudicated. [Bosworth–Toller, nán](https://bosworthtoller.com/23433), main page709 I(a), expressly records use without another negative. I personally viewed the downloaded scan. The final key also accepts negative concord. This lookup occurred after unlock and is not retroactive learner support.

## Witness comparison and source fidelity

The frozen witness is not silently corrected. In38.2 its **Sum cwēn** misses the selected **Sumu** ending. Its angel forms in37.2,40.1 and42.5 omit the selected **ę** hook. Its39.4 explanatory purpose wording is corrected here to desired content. These are distinct from the supported alternatives recorded at each output: strong daily-bread adjective, word order without an explicit control, permitted synonyms, choice-relative formulations, preposed **tōgēanes**, and negative concord.

All82 original prompts,235 original controls and all82 model strings were reconciled. All14 Exercise37 items retain the global omission instruction, without suppressing needed third-person wish subjects. The complete252-word reading matches the contract after only note-anchor removal and whitespace normalization. All19 original notes and20 anchors, including both174 note17 anchors, remain. The three full translations preserve causative fetching/giving, musical-art antecedence, the reported Apollo identity, intransitive silence result, performance senses, collective source agreement and each/all/greatly in the final response.

The actual sixteen prior contracts and cumulative registers still match their blind-intake hashes. The independent dependency check resolves2069 assessed record references. Its27 recognition-feature routes occur in English interpretation tasks with visible help, not independent Old English production. Full model-token routes were checked at all82 compositions; semantic absence of a needed construction was assessed through the blind solve and manual review, not inferred from successful ID joins. U17-A01’s spacing and U17-A02’s support/assessment changes are verified. The separate paradigm reviewer owns the all-cell evidence for110 systems/124 displays/1234 cells; this review does not relabel that work as its own.

## Accepted identities

| Artifact | Raw SHA-256; LF-normalized bytes have the same identity |
| --- | --- |
| student.md | `{artifacts[0]['raw_sha256']}` |
| answer-key.md | `{artifacts[1]['raw_sha256']}` |
| independent-solutions.md | `{artifacts[2]['raw_sha256']}` |

The substantive contract identity is `{semantic}`. Its exact key set and original raw identity are recorded in the ledger, excluding only the coordinator’s mutable completion/review metadata. The ledger also records{len(image_receipts)} actual page-image inspections with raw hashes, locators and specific observations. These receipts include direct exercise22–28 and reading174–175 inspection, supplementary government evidence, Cook38/63/100/106, and the checked144000/nīwne supports.

Export parity, every-page visual inspection and register integration remain to be completed by the coordinator’s later stages.
'''
for before, after in [
 ('and146','and 146'),('all82','all 82'),('calls39.4','calls 39.4'),('Cook186','Cook 186'),
 (';184','; 184'),('note5','note 5'),(';195','; 195'),('and126','and 126'),('Cook106§201','Cook 106 §201'),
 ('All11','All 11'),('and11','and 11'),('The43.15','The 43.15'),('page709','page 709'),
 ('In38.2','In 38.2'),('in37.2,40.1 and42.5','in 37.2, 40.1 and 42.5'),('Its39.4','Its 39.4'),
 ('All82','All 82'),('prompts,235','prompts, 235'),('All14','All 14'),('Exercise37','Exercise 37'),
 ('complete252','complete 252'),('All19','All 19'),('and20','and 20'),('both174 note17','both 174 note 17'),
 ('resolves2069','resolves 2,069'),('Its27','Its 27'),('for110 systems/124 displays/1234 cells','for 110 systems, 124 displays and 1,234 cells'),
 ('records28','records 28'),('exercise22','exercise 22'),('reading174','reading 174'),('Cook38/63/100/106','Cook 38/63/100/106'),
 ('checked144000','checked 144,000'),('B17-01,40.1','B17-01, 40.1'),('B17-02,42.5/8','B17-02, 42.5/8'),
 ('B17-03,43.13','B17-03, 43.13'),('B17-04,43.15','B17-04, 43.15'),('B17-05,41.8','B17-05, 41.8')
]:
    md = md.replace(before, after)
Path('chapters/ch17/review.md').write_text(md,encoding='utf-8',newline='\n')
print(json.dumps({'status':ledger['status'],'tasks':len(task_reviews),'outputs':len(output_reviews),'material_open_findings':0,
 'source_images':len(image_receipts),'model_tokens_checked':token_count,'contract_semantic_sha256':semantic,
 'review_md_sha256':receipt('chapters/ch17/review.md')['raw_sha256'],'review_ledger_sha256':receipt('chapters/ch17/review-ledger.json')['raw_sha256']},indent=2))
