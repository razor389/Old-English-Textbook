import json,re,hashlib
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parents[2]
def load(p):return json.loads(p.read_text(encoding='utf8'))
M=load(O/'candidate-models.json');B=load(O/'candidate-verbal-bindings.json');V=load(O/'verbal-systems.json');S=load(O/'senses-constructions-support.json');Q=load(O/'reading-verbal-bindings.json');N=load(O/'numeric-control-analysis.json');E=load(O/'evidence-catalog.json')
L={l['lemma_id']:l for l in load(R/'lexicon/entries.json')['lemmas']};P={(lid,f['form_id']):f for lid,l in L.items()for f in l['forms']}
errors=[];models={r['source_item_id']:r for r in M['rows']};counts={}
assert len(M['rows'])==47
for ex in range(44,49):counts[ex]=sum(r['exercise']==ex for r in M['rows'])
assert list(counts.values())==[8,9,9,11,10]
for row in B['rows']:
 assert row['model']==models[row['source_item_id']]['model']
 ts=re.findall(r'[^\W\d_]+(?:-[^\W\d_]+)*',row['model'])
 for v in row['verbal_occurrences']:
  assert ts[v['token_position_one_based']-1]==v['surface']
  assert v['sense_id']and v['sense_id']!='UNRESOLVED'
  if v['form_knowledge_status']=='previously_taught':assert v['analysis']==P[(v['lemma_id'],v['form_id'])]['analysis'],v['form_id']
rt=load(R/'sources/audits/unit18-source/reading-source.json')['source_spans'][0]['learner_text'];ts=re.findall(r'[^\W\d_]+(?:-[^\W\d_]+)*',rt);assert len(ts)==226
for v in Q['verbal_occurrences']:
 assert ts[v['token_position_one_based']-1]==v['surface']
 assert v['sense_id']and v['sense_id']!='UNRESOLVED'
 if v['form_knowledge_status']=='previously_taught':assert v['analysis']==P[(v['lemma_id'],v['form_id'])]['analysis'],v['form_id']
for s in V['systems']:
 assert s['display_cell_count']==len(s['cells'])
 assert s['citation_reference']['status']=='supplied_reference'
 assert all(c['analysis']and c['form']for c in s['cells'])
assert sum(len(s['cells'])for s in V['systems'])==182
assert len({c['form_id']for s in V['systems']for c in s['cells']})==182
assert not B['issues']and not Q['unresolved_routes']and not N['unresolved']and not E['missing_images']
assert len(N['numeric_controls'])==45
for e in E['evidence_catalog']:
 assert hashlib.sha256((R/e['image_path']).read_bytes()).hexdigest()==e['sha256']
out={'status':'pass','model_version':M['model_version'],'checks':{'complete_cook_items':47,'exercise_counts':counts,'model_verbal_occurrences':sum(len(r['verbal_occurrences'])for r in B['rows']),'reading_words':226,'reading_verbal_occurrences':len(Q['verbal_occurrences']),'verbal_systems':len(V['systems']),'literal_unique_new_productive_cells':182,'composition_sense_proposals':len(S['sense_proposals']),'new_productive_construction_features':len(S['features']),'composition_supplied_whole_frames':len(S['whole_frame_support']),'reading_supplied_whole_frames':len(Q['whole_frame_support']),'numeric_controls_explained':45,'image_evidence_records':len(E['evidence_catalog']),'prior_form_analyses':'all retained byte-equivalent as parsed JSON dictionaries; contextual parses are separate','token_positions':'all exact','unresolved_routes':0},'limitations':['This checks declared scope/identities and exact token joins, not linguistic truth by itself. Primary-page inspection and independent review remain distinct.','No active registers, chapters, contracts, Beads or Git were written by this worker.']}
(O/'packet-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps(out,ensure_ascii=False))
