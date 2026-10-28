from pathlib import Path
import json
O=Path('curriculum/proposals/unit18')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
g=read('curriculum/grammar.json');inv=read(O/'inventory.json') if (O/'inventory.json').exists() else {'features':[]}
known={f['feature_id']:f for f in g['features']+inv['features']}
rows={f'{e}.{i}':set() for e,n in [(44,8),(45,9),(46,9),(47,11),(48,10)] for i in range(1,n+1)}
groups={
'u06-imperative-use':'44.1 44.6 44.8 45.1 45.4 46.1 46.7 46.8 46.9 47.3 47.8 48.2 48.6 48.8 48.9',
'u07-quotation-wish':'44.6 45.2 46.1 46.6 47.3 47.4 47.8 48.1 48.2 48.6',
'u07-passive-command-wish':'47.3',
'u07-passive':'45.5 45.6 47.2',
'u07-predicate-participle-variants':'45.2 45.5 45.6 47.2 47.3',
'u02-simple-negation':'44.2 44.5 44.6 46.1 47.11 48.3 48.4 48.6 48.7 48.9',
'u15-negative-concord':'48.4 48.6 48.7',
'u02-clause-coordination':'44.1 44.3 44.5 44.8 45.1 45.3 45.4 45.6 45.7 45.8 45.9 46.2 46.4 46.6 46.7 46.8 46.9 47.2 47.4 47.5 47.6 47.8 47.10 47.11 48.1 48.2 48.5 48.7 48.8 48.10',
'u03-agreement':'44.1 44.2 44.5 44.6 44.7 44.8 45.2 45.3 45.4 45.6 45.7 45.8 45.9 46.1 46.4 46.5 46.6 46.7 46.8 46.9 47.1 47.2 47.4 47.5 47.6 47.8 47.10 47.11 48.1 48.2 48.3 48.4 48.5 48.6 48.7 48.8',
'u03-determiner-conditions':'44.2 44.8 46.7 46.8 47.4 47.5 47.10 48.4',
'u03-ordinal-other':'47.4 48.4',
'u03-possessive-agreement':'44.2 44.5 44.8 45.1 45.2 45.4 45.6 45.7 45.8 45.9 46.1 46.5 46.6 46.8 47.1 47.2 47.4 47.8 47.10 48.1 48.2 48.3 48.5 48.6 48.8',
'u03-possessor-reference':'44.2 44.5 44.8 45.1 45.2 45.4 45.6 45.7 45.8 45.9 46.1 46.5 46.6 46.8 47.1 47.2 47.4 47.8 47.10 48.1 48.2 48.3 48.5 48.6 48.8',
'u02-third-person-possessors':'44.1 45.4 46.2 46.3 46.4 46.6 46.7 46.9 47.2 47.6 48.2 48.5',
'u08-relative-the':'44.3 44.6 45.2 45.6 45.8 46.6 46.8 47.1 47.2 47.3 47.8',
'u08-relative-internal-case':'44.3 44.6 45.2 45.6 45.8 46.6 46.8 47.1 47.2 47.3 47.8',
'u08-relative-demonstrative':'48.7',
'u09-content-that':'44.2 44.4 44.5 47.2 47.11 48.1 48.6 48.8',
'u09-reported-statement':'44.4 44.5 47.2 47.11 48.1 48.8',
'u09-report-reference':'44.2 44.4 44.5 47.9 47.11 48.1 48.8',
'u12-reported-sequence':'44.2 44.4 44.5 46.4 46.9 47.2 47.9 47.11 48.1 48.8',
'u09-dependent-question':'44.5 45.9 46.4 46.9 47.9 48.10',
'u09-dependent-whether':'44.5 46.4 47.9',
'u13-ascian-person-thing':'44.5 46.4 46.9 47.9',
'u08-direct-questions':'46.6 47.2 47.7 48.5',
'u08-interrogative-adverbs':'46.9 47.7 48.10',
'u11-past-when-then':'44.4 45.4 45.6 45.8 46.6 46.9 47.2',
'u11-recurring-when-then':'46.9',
'u07-basic-conditionals':'44.3 44.8',
'u11-contrary-present-condition':'44.7',
'u11-purpose':'44.6 45.2 45.4 45.6 47.11 48.4 48.9',
'u11-negative-purpose':'44.6 48.3 48.9',
'u06-modal-magan':'44.6 45.4 48.4 48.7',
'u06-volition-willan':'44.3 44.5 44.8 46.9 47.7',
'u06-plain-infinitive-complement':'44.2 44.3 44.5 44.6 44.8 45.4 46.9 47.7 48.2 48.3 48.4 48.7',
'u06-purpose-infinitive':'45.9',
'u02-giving-recipient':'45.2 46.1 46.2 46.8',
'u11-bringan-destination':'44.6 44.8 45.9 47.2 47.11 48.1',
'u12-bringan-imperative':'44.8',
'u10-andswarian-dative':'44.5',
'u11-biddan-person':'45.7',
'u11-vocative-personal-adjective':'45.7',
'u13-laedan-person-direction':'44.5 45.4 45.6',
'u02-reflexive-use':'46.1 48.4 48.6',
'u13-ondraedan-acc':'46.1',
'u15-free-choice':'47.4',
'u09-partitive-pronoun':'46.7',
'u15-quantity-partitives':'44.1 44.4 46.7 46.9',
'u10-partitive-group':'44.4 46.7',
'u12-duration-accusative':'48.7',
'u11-butan-dative':'46.9 48.3',
'u09-mid-accompaniment':'44.2 44.3 44.6 45.2 45.4 46.1 47.3 47.4 47.6 47.10 48.2',
'u10-mid-means':'46.7 46.9',
'u10-to-destination':'45.1 45.3 47.5 47.6 47.8 48.1 48.6 48.8',
'on-dative-location':'44.8 45.6 46.1 47.2 47.5 48.8',
'u11-don-placement':'45.9 46.8',
'u05-see-object':'45.4 46.6 47.11 48.3',
'u05-eat':'45.4',
'u12-adrifan-indicative':'48.4',
'u15-man-impersonal':'48.7',
'u16-cleopian-cry':'48.5',
'u13-main-fronting-order':'44.1 44.2 44.8 45.3 45.4 45.6 45.7 45.8 45.9 46.1 46.4 46.5 46.6 46.7 46.9 47.2 47.5 47.9 48.4 48.10',
'u04-findan-exception':'47.5'
}
issues=[]
for fid,items in groups.items():
 if fid not in known:issues.append(fid)
 for item in items.split():rows[item].add(fid)
for f in inv['features']:
 for item in f.get('source_items',[]):
  if item in rows:rows[item].add(f['feature_id'])
# Shared active clause agreement and participant-reference work is stated once;
# lexical government and unusual constructions remain separately named below.
for item in rows:rows[item].update(['u02-active-agreement','u02-pronoun-reference'])
result={'schema_version':1,'chapter':'ch18','status':'explicit_prior_features_and_current_contexts','rows':[{'task_id':f'EX-XII-XIII-{int(k.split(".")[0]):02}-{int(k.split(".")[1]):02}','feature_ids':sorted(v),'scope':'Exact selected prior constructions plus separately evidenced current systems/frames; supplied construction components remain visible and are not independent recall targets.'} for k,v in rows.items()],'unresolved_feature_ids':issues}
(O/'source-feature-bindings.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('47 source feature rows; unknown prior IDs:',issues)
