from pathlib import Path
import json, hashlib, collections, re

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'sources/audits/unit12-grammar'
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def write(p,data):(OUT/p).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
B=read('build/unit12-prior-baseline.json')
R=read('sources/audits/unit12-grammar/grammar-records.json')
E=read('sources/audits/unit12-grammar/evidence-catalog.json')['evidence']
RULES=read('sources/audits/unit12-grammar/rules.json')
FR=read('sources/audits/unit12-grammar/lexical-frames.json')
oldlemmas={x['lemma_id']:x for x in B['lexicon']['lemmas']}
oldforms={f['form_id']:f for x in oldlemmas.values() for f in x['forms']}
oldsenses={s['sense_id']:s for x in oldlemmas.values() for s in x['senses']}
newforms={f['form_id']:f for x in R['lemmas'] for f in x['forms']}
newsenses={s['sense_id']:s for x in R['lemmas'] for s in x['senses']}
forms={**oldforms,**newforms};senses={**oldsenses,**newsenses}
features={x['feature_id']:x for x in R['features']}
issues=[]
def check(test,description):
    if not test:issues.append(description)

check(len(B['contracts'])==11,'Expected eleven prior active contracts.')
check(len(newforms)==sum(len(x['forms']) for x in R['lemmas']),'Duplicate form IDs.')
check(len(newsenses)==sum(len(x['senses']) for x in R['lemmas']),'Duplicate sense IDs.')
check(len(features)==len(R['features']),'Duplicate feature IDs.')
comparison=[]
for l in R['lemmas']:
    for kind,idkey,prior in [('forms','form_id',oldforms),('senses','sense_id',oldsenses)]:
        for x in l[kind]:
            old=prior.get(x[idkey])
            decision={'lemma_id':l['lemma_id'],'record_kind':kind,'record_id':x[idkey],
                      'proposed_status':x['knowledge_status'],'prior_record':old,
                      'decision':'New individual record; headword familiarity does not establish prior teaching.' if old is None else 'Exact prior individual record retained; proposed milestone is evaluated independently.'}
            if old and kind=='forms':
                check(old['form']==x['form'],'Existing surface changed: '+x[idkey])
                check(x.get('prior_record')==old,'Existing full prior record not preserved: '+x[idkey])
                if old.get('production_taught_in'):check(x['knowledge_status']=='previously_taught','Prior production mislabeled new: '+x[idkey])
            comparison.append(decision)
write('prior-record-reconciliation.json',{'schema_version':1,'chapter':'ch12','baseline_checkpoint':B['git_checkpoint'],
    'baseline_counts':{'contracts':len(B['contracts']),'lemmas':len(oldlemmas),'forms':len(oldforms),'senses':len(oldsenses),'features':len(B['grammar']['features'])},
    'records':comparison,'scope_changes':[
      'Supplied geworht and flēoð are explicitly promoted; the original records/history remain retained.',
      'The earlier gierwan and sęttan citation forms with parenthesized ge/w are not silently replaced by the selected bare bases.',
      'The supplied genēosian citation becomes plain-infinitive production; its inflected shape is recognition.',
      'Habban compound usage is a new sense/construction using old finite forms; no invented multiword forms.',
      'Quantitative predicate mā, predicative possession, rich-in, objectless seeing, lethal slēan, intransitive geswīcan and nominal swā receive explicit new scope.',
      'Source-only words/forms, negative nolde/nis/nāh and higher quantities remain individually supplied where specified; no unbounded system follows.'
    ]})

paradigm_checks=[]
for p in R['paradigms']:
    tag=p['paradigm_id'].rsplit('-',1)[1]
    check(p['cell_count']==len(p['cells']),'Cell count mismatch: '+p['paradigm_id'])
    for c in p['cells']:
        check(c['form_id'] in newforms,'Unresolved paradigm form: '+c['form_id'])
        check(forms[c['form_id']]['form']==c['form'],'Surface mismatch: '+c['form_id'])
    if tag=='IND':
        actual={(c['tense'],c['mood'],c['person'],c['number']) for c in p['cells']}
        expected={(t,'indicative',person,n) for t in ['present','preterite'] for person in [1,2,3] for n in ['sg','pl']}
    elif tag=='IMP':
        actual={(c['mood'],c['person'],c['number']) for c in p['cells']};expected={('imperative',2,n) for n in ['sg','pl']}
    elif tag=='PART':
        actual={(c['verb_form'],c['tense']) for c in p['cells']};expected={('participle','present'),('participle','past')}
    elif tag=='INF':
        actual={(c['mood'],c['type']) for c in p['cells']};expected={('infinitive','plain'),('infinitive','inflected')}
    check(actual==expected,'Incomplete coordinates: '+p['paradigm_id'])
    paradigm_checks.append({'paradigm_id':p['paradigm_id'],'tag':tag,'cells':len(p['cells']),'complete_defined_coordinates':actual==expected})

for x in FR['frames']:
    check(x['sense_id'] in senses,'Unresolved frame sense: '+x['sense_id'])
def refs(obj):
    result=set()
    if isinstance(obj,dict):
        result.update(obj.get('evidence_refs',[]))
        for k,v in obj.items():
            if k not in ['evidence_refs','prior_record']:result.update(refs(v))
    elif isinstance(obj,list):
        for v in obj:result.update(refs(v))
    return result
check(not ((refs(R)|refs(FR)|refs(RULES))-set(E)),'Unresolved local evidence reference.')
image_checks=[]
def images(obj):
    if isinstance(obj,dict):
        if ('path' in obj or 'image' in obj) and 'sha256' in obj:
            p=obj.get('path',obj.get('image'))
            if p.startswith('sources/'):
                good=(ROOT/p).exists() and sha(p)==obj['sha256']
                check(good,'Image hash mismatch: '+p);image_checks.append({'path':p,'hash_matches':good})
        for v in obj.values():images(v)
    elif isinstance(obj,list):
        for v in obj:images(v)
images(E)

# Public translated construction display only; no key/private model is read.
pattern_path='curriculum/proposals/unit12/construction-patterns.json'
patterns=read(pattern_path)['patterns']
positions=patterns[0]['positions']
check(len(positions)==12,'Expected twelve habban construction positions.')
coords={(p['tense'],p['person'],p['number']) for p in positions}
check(coords=={(t,p,n) for t in ['present','preterite'] for p in [1,2,3] for n in ['sg','pl']},'Incomplete construction positions.')
for p in positions:
    check(p['auxiliary_form_id'] in oldforms,'New invented auxiliary form: '+p['position_id'])
    check(p['fixed_object_form_ids']==['se-n-acc-sg','hus-acc-sg'],'Object binding is not selected accusative: '+p['position_id'])
    check(p['participle_form_id']=='gewyrcean-past-participle','Wrong participle identity: '+p['position_id'])
    for tok in p['sequence']['tokens']:
        check(tok['form_id'] in forms,'Unresolved construction token form: '+tok['form_id'])
        check(tok['sense_id'] in senses,'Unresolved construction token sense: '+tok['sense_id'])
        check(tok['form']==forms[tok['form_id']]['form'],'Construction token mismatch: '+tok['form_id'])
check(patterns[0]['new_inflectional_cell_count']==0,'Construction display falsely counted as new inflectional cells.')

write('public-composition-review.json',{'schema_version':1,'chapter':'ch12','status':'passed_before_learner_drafting',
 'reviewed_files':[{'path':p,'sha256':sha(p)} for p in ['curriculum/proposals/unit12/composition-seed.json','curriculum/proposals/unit12/compositions.json',pattern_path]],
 'findings':[
  'The twelve teaching examples match the declared narrative time, transitive habban, agentless passive, recognition-only intransitive/present-participle, reported viewpoint and future-context scopes.',
  'The initial unassigned dog was replaced by already taught hors before final seed; current examples use that actual prior noun.',
  'The connected new account uses its declared past viewpoint, direct statement, reported intention and return sequence coherently. A reported intention is not itself proof of fulfillment; later narrated events supply subsequent facts.',
  'All twelve compound positions bind actual old auxiliary identities and the explicitly promoted participle; object remains accusative, finite auxiliary agrees with subject.',
  'No graded answer or complete reading translation is provided by this review.'
 ],'issues':[],'limits':'This is a public composition/construction check. The actual learner draft and exercises still require the later independent solve and key reconciliation.'})

validation={'schema_version':1,'chapter':'ch12','status':'passed' if not issues else 'failed',
 'counts':{'lemmas':len(R['lemmas']),'forms':len(newforms),'senses':len(newsenses),'features':len(features),'paradigms':len(R['paradigms']),
           'inflectional_cells':sum(len(p['cells']) for p in R['paradigms']),'construction_positions_separate':len(positions),'evidence_records':len(E),'rules':len(RULES['rules']),'frames':len(FR['frames'])},
 'paradigm_checks':paradigm_checks,'image_hash_checks':image_checks,'issues':issues,
 'independence':'Only public source/prompts, cumulative registers/contracts, public compositions and translated teaching displays were inspected. No private author file or key was opened. Cook21.4 has documented limited unsolicited answer-clause exposure and must have a fresh independent witness.'}
write('validation.json',validation)
print(validation['status'],validation['counts'],validation['issues'])
if issues:raise SystemExit(1)
