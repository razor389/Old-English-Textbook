"""Repeated source-packet integrity check after editorial repairs."""
import collections,hashlib,json,re
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[2]
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(n,x):(P/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
e=rd(P/'exercises-prompts.json');h=rd(P/'exercise-hints.json');r=rd(P/'reading-source.json');a=rd(P/'reading-apparatus.json');n=rd(P/'noun-adjective-paradigms.json');s=rd(P/'nominal-sense-audit.json');l=rd(P/'local-support.json');t=rd(P/'reading-token-audit.json');catalog=rd(P/'evidence-catalog.json')
assert len(e['items'])==47
expected=[f'EX-XII-XIII-{ex}-{i:02d}' for ex,c in [(44,8),(45,9),(46,9),(47,11),(48,10)] for i in range(1,c+1)]
assert [x['source_item_id'] for x in e['items']]==expected
assert len(h['records'])==154
assert len(a['notes'])==22 and sum(len(x['anchors']) for x in a['notes'])==29
span=r['source_spans'][0];assert len(span['source_lines'])==26 and len(span['learner_text'].split())==226
assert len(t['tokens'])==226 and not t['unresolved']
assert t['tokens'][224]['form_id']=='ic-acc-pl'
assert all(x.get('form_id') or x.get('binding_owner')=='unit18_grammar' for x in t['tokens'])
assert n['counts']['paradigms']==26 and n['counts']['cells']==470
assert len({f['form_id'] for p in n['paradigms'] for f in p['cells']})==470
assert len(l['forms'])==66 and len(l['reading_phrase_support'])==18
assert len({x['form_id'] for x in l['forms']})==66
sensegloss=collections.defaultdict(set)
for f in l['forms']:sensegloss[f['sense_id']].add(f['gloss'])
assert not {k:v for k,v in sensegloss.items() if len(v)>1}
ids={x['evidence_id'] for x in catalog['records']};assert len(ids)==len(catalog['records'])
def refs(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k=='evidence_refs':yield from v
   else:yield from refs(v)
 elif isinstance(x,list):
  for v in x:yield from refs(v)
missing=set()
for x in [e,h,r,a,n,s,l,t]:missing|={i for i in refs(x) if i.startswith('U18-') and i not in ids}
assert not missing,missing
for x in catalog['records']:assert digest(R/x['image_path'])==x['image_sha256']
old=rd(P/'pre-correction-reading-source.json');capture=rd(R/'sources/audits/unit18-coordinator/captured-precorrection-reading-data.json')['observed_pre_correction_data'];assert old==capture
def repair(x):
 if isinstance(x,str):return x.replace('lęcgað','lęcgeað').replace('ðēowra','ðēowa')
 if isinstance(x,list):return [repair(v) for v in x]
 if isinstance(x,dict):return {k:repair(v) for k,v in x.items()}
 return x
assert repair(old)==r
olda=rd(P/'pre-correction-reading-apparatus.json');fixed=repair(olda)
for x in fixed['notes']:
 if x['apparatus_id']=='FB-U18-176-N10':
  for anchor in x['anchors']:anchor['character_offset']-=1
assert fixed==a
oldus=rd(P/'pre-us-correction-reading-token-audit.json');assert oldus['tokens'][224]['form_id']=='ic-dat-pl'
oldposs=rd(P/'pre-eowre-correction-local-support.json');assert any('ēowre ðearfe'in x['help_text'] for x in oldposs['forms'])
assert not any('ēowre ðearfe'in x['help_text'] for x in l['forms'])
queries=[
 ('reading-spelling','The initial audit lęcgað and ðēowra were incorrect. Personally inspected600dpi source prints lęcgeað and ðēowa. The inverse witness equals the coordinator’s earlier captured semantic JSON; the two replacements recover the current source.','transcription-checks.json'),
 ('reading-us-case','Initial token225 analysis/form route was dative. Root comparison and personal184b inspection show geręste hine is accusative reflexive;177N2 points there. Current225 is actual prior ic-acc-pl. The actual previous audit bytes remain preserved; no old register record was overwritten.','pre-us-correction-reading-token-audit.json'),
 ('eower-dative','Initial benefit help paired dative ðearfe with unsupported selected ēowre. Actual prior dative feminine singular is ēowerre. Grammar modelv10 and local help use for ēowerre ðearfe; no existing accusative/instrumental ēowre form was relabeled.','pre-eowre-correction-local-support.json'),
 ('theowa-manna','Source genitive plural ðēowa manna and dative plural ðēowum mannum remain wholly supplied. BT1053 supports strong noun þeów; BT1054’s adjective quotation actually has þeówra with r. Root’s initial contrary fullpage observation was withdrawn after the personally inspected crop. Strong-noun/appositional analysis remains contextual inference, not a uniquely proven historical classification.','bt-p1054-adjective-detail.png'),
 ('sith-instrumental','Cook44.7 hint sīð176 supplies a lemma, not an uninflected accusative. Section176 and Crawford43.10 oþre siðe establish the adverbial instrumental phrase. The selected sīðe instrumental has its own supplied identity, separate from sith-dat-sg.','local-support.json'),
 ('false-prior-withdrawal','An early message incorrectly suggested actual prior status for feoh, earmlice and betweonan. Full actual-register lookup found none. That claim is withdrawn: feoh now has a complete selected mass-singular table; earmlice and betwēonan him have explicit local supply.','prior-scope-receipt.json'),
 ('feoh-quantity','Preserve printed unmarked feoh from Cook hint and47.5, with printed fēos and rule-supported fēo after h-loss. This is not a historical-short-vowel claim and does not condemn independently evidenced fēoh.','noun-adjective-paradigms.json'),
 ('aecern-plural','Cook gives unmarked æcern; BT plural evidence is supplemented by the exact O.æcernu variant in Crawford190 apparatus43.11. No macron is inferred.','crawford1922-p190.png'),
 ('source-names','Iacob and Iosep nominative spellings are routed to actual Cook hints; Iudas also occurs in Crawford190/194, Iosepe and Egypta lande in191, Beniamines sacce in194, and Iosep nominative in195. The packet does not claim all name forms occur on every cited page or invent full foreign-name declensions.','local-support.json'),
 ('silver-cup','Earlier proposed læfel seolfres was withdrawn because the checked quantity genitive did not establish a manufactured-material cup construction. Select visible seolfrenne læfel from CookEx62 seolfren57 plus the already taught strong accusative ending; no complete new adjective class is introduced.','local-support.json'),
 ('butan-functions','Use the printed Cook280 būtan separately for spatial outside, absence and negative-condition conjunction. The earlier supplied būton exclusion marker did not by itself establish a finite unless clause. Grammar modelv9/v10 selects būtan; distinct supplied conjunction identity retained.','local-support.json'),
 ('leaf-permission','Exercises57 gives lēaf47 for permission; FirstBook302 gives lēaf51.b for permission and a separate47 leaf. The source dative lēafe is identical. Follow the reading’s own glossary for contextual feminine analysis and disclose the disagreement; do not independently test gender.','local-support.json'),
 ('lord-mark','The isolated mark after lord in47.1 is treated as a print/scan anomaly of undetermined origin, not a demonstrated linguistic Cook error. Diplomatic prompt/image retained and typographic removal declared.','exercises-prompts.json'),
]
dump('query-resolutions.json',dict(schema_version=1,status='resolved with explicit local scope; no material source query left open',records=[dict(query_id='U18-Q-'+k,status='resolved',resolution=v,artifact=f) for k,v,f in queries],unresolved=[]))
vg=R/'sources/audits/unit18-grammar/reading-verbal-bindings.json';verbs=rd(vg) if vg.exists() else None
if verbs:
 assert len(verbs['verbal_occurrences'])==41 and not verbs['unresolved_routes']
 for v in verbs['verbal_occurrences']:assert t['tokens'][v['token_position_one_based']-1]['surface']==v['surface']
report=dict(schema_version=1,source_editor='unit18_source',proposed_gate_status='source evidence ready for coordinator reconciliation and canonical contract',scope='47 exact Cook English composition prompts plus separately selected original Apollonius prose; no OE Joseph reading assigned',counts=dict(exercises=5,prompts=47,hint_records=154,reading_words=226,physical_reading_lines=26,original_notes=22,original_note_anchors=29,nominal_paradigms=26,nominal_cells=470,nominal_senses=27,local_forms=66,local_phrases=18,reading_nonverbal_tokens=185,external_verbal_tokens=41,actual_image_receipts=len(catalog['records'])),source_sets={'exercises':expected,'reading':span['source_span_id'],'reading_locator':'Cook FirstBook175.18–177.2 / one-based PDF191–193'},validation={'exact_complete_item_sequence':True,'all_hint_records_retained':True,'all_original_note_anchors_present':True,'reconstructed_source_equals_earlier_captured_data':True,'reversible_transcription_repairs':True,'all_selected_nominal_cells_literal_and_unique':True,'local_sense_ids_do_not_conflate_distinct_glosses':True,'source_nonverbal_token_routes_unresolved':0,'all_referenced_own_evidence_ids_resolve':True,'image_hashes_match_actual_inspection_receipts':True,'external_41_verbal_routes_present_and_surface_match':bool(verbs)},remaining_coordinator_work=['Reconcile with design/grammar final joins and commit canonical learning contract before learner/key prose.','Keep all supplied forms/whole phrases visible; independent recall is limited to declared production/recognition scope.','The independent review, chapter render, registers, Beads export and Git checkpoint are coordinator stages, not certified by this source audit.'],source_registry={'proposal':'sources/audits/unit18-source/source-registry-proposal.json','coordinator_confirmed_cache':'sources/cache/crawford_heptateuch_1922.pdf','pdf_sha256':'3235a08e7a1625df8acb1983d9f996d2d60f794e2353ada661d0408ff4334a5f','pdf_size_bytes':28967646,'assignment_status':'corroboration only'},unresolved_source_queries=[])
dump('source-gate-report.json',report)
manifest=[]
for p in sorted(P.iterdir()):
 if p.is_file() and p.name!='manifest.json':manifest.append(dict(path=p.relative_to(R).as_posix(),size_bytes=p.stat().st_size,sha256=digest(p)))
dump('manifest.json',dict(schema_version=1,scope='Exclusive unit18-source files only; snapshots and exact originals are retained',files=manifest,file_count=len(manifest),report='source-gate-report.json'))
print(json.dumps(report['counts']));print('All source packet integrity checks passed.')
