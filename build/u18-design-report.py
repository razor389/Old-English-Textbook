from pathlib import Path
import json
O=Path('curriculum/proposals/unit18')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
v=read(O/'validation.json');inv=read(O/'inventory.json');plan=read(O/'task-plan.json');out=read(O/'outcomes.json')
assert v['status']=='pass', 'A failed validation cannot be reported as a final proposal.'
out['status']='complete design proposal; ready for coordinator reconciliation, not canonical'
out['pending_inputs']=[]
out['remaining_coordinator_gates']=['Reconcile independent source and grammar evidence; commit the canonical coverage contract before prose.','Draft the learner lesson and answer key from the committed contract.','Freeze fresh independent learner solutions before model/key review; resolve linguistic findings.','Inspect every exported page and special character; integrate active registers and final source assignment status.']
save(O/'outcomes.json',out)
c=v['counts'];scope=inv['record_counts_by_scope'];models=read('sources/audits/unit18-grammar/candidate-models.json')
report=f'''# Unit 18 curriculum proposal

The proposal is ready for coordinator reconciliation. Its dependency audit passes with zero unresolved records. This is an author-preparation packet; it does not authorize lesson or key prose before the canonical coverage contract is committed.

The baseline is `0eda27783a3830fbd10bebef3702e27c15ff837c`. All seventeen active contracts and the actual cumulative registers were loaded before design: 1,197 lemmas, 12,557 forms, 1,573 senses and 1,143 features. See [the prior audit](prior-audit.json).

## Assigned source and purpose

All 47 original Cook joint XII, XIII items in Exercises 44–48 remain assigned, in the original 8/9/9/11/10 distribution. Their English prompts, original identifiers, 154 hints and bracketed controls remain exact. The 45 numeric controls have individual explanations and actual teaching or support routes. No difficult item is silently omitted or deferred.

This English Joseph sequence supplies sustained composition. It is not evidence of an Old English Joseph reading in the selected Cook reader. The separately assigned original prose is Cook 175.18–177.2, PDF 191–193: all 26 physical lines, 226 words, 22 original notes and 29 anchors. It closes before “Apollonius as Teacher.” I personally inspected the selected source images and joined the independent source editor’s exact transcription and apparatus; later high-resolution corrections are preserved in that editor’s evidence packet.

The unit practices complete-clause translation and composition, selective parsing, participant reference and clause structure. It makes no claim of general graduation, whole-reader mastery or mastery of poetry. No arbitrary vocabulary quota or additional original narrative is imposed.

## Requested work

The [task plan](task-plan.json) has {c['tasks']} task groups and {c['requested_output_positions']} requested answer positions: 47 source compositions plus 13 original task groups with 40 answers. All answer positions have a target, essential meaning, defensible-alternative policy, useful error diagnosis, exact dependency routes and a private model with explanation. Public task labels contain no answers.

| Group | Purpose | Requested answers |
|---|---|---:|
| A01–A03 | Reference, reporting and relative-clause analysis with controlled transformations | 10 |
| C01–C02 | Two concise cumulative compositions using actual prior productive language | 2 |
| F01–F03 | Case, number, tense and lexical-government contrasts | 13 |
| R01–R05 | Complete prose translation, reference, parsing, clause relations and discourse limits | 15 |
| Cook 44–48 | Complete sustained Joseph composition sequence | 47 |

The form work requires ten meaningful Old English sentences and three explanations. Two translated cumulative examples precede the relevant tasks. There is no newly composed connected reading. The whole prose translation is divided at complete discourse boundaries; the third division begins with the new sentence in 176.13, not in the middle of the following printed line.

## Teaching and visible support

The [inventory](inventory.json) contains {c['lemmas']} involved lemmas, {c['forms']} form records, {c['senses']} sense records and {c['features']} feature records. These are proposal records, including reused prior identities and supplied references; they are not all new teaching. The explicit statuses are:

| Record type | Previously taught | New production | New recognition | Prior recognition | Supplied |
|---|---:|---:|---:|---:|---:|
'''
for kind in ['form','sense','feature']:
 d=scope[kind];report+='| '+kind+' | '+' | '.join(str(d.get(k,0)) for k in ['previously_taught','new_production','new_recognition','prior_recognition','supplied'])+' |\n'
report+=f'''
There are {c['paradigms']} defined systems and {c['paradigm_cells']} literal cells, routed once each to {c['matrices']} display matrices. The independent nominal packet contributes 26 systems and 470 cells; the verbal packet contributes 29 bounded systems and 182 cells. Complete nominal classes and adjective systems are displayed, including explicit singular-only scope for selected mass-noun senses. Seven new verbal indicative systems are complete; the other verbal assignments are complete, explicitly bounded mood, command, infinitive or participial systems. Their diagnostic stems and citation references are visible references, not grants of unassigned moods or syntactic uses. Adjective instrumental cells remain recognition only.

The exact morphology, sense and construction statuses are separate. A familiar lemma, copied hint, displayed cell or source-only occurrence never establishes unrestricted independent production. Existing stored surfaces, analyses and meanings are preserved, including capitalization-only contextual comparison of stored Hāl and model hāl. Every supplied output position has visible local help; it is not assessed for independent recall. The [literal display routes](display-matrices.json), [source controls](source-hint-inventory.json), [local support routes](source-support-routes.json) and [reading bindings](reading-bindings.json) make those boundaries auditable.

## Material reconciliations

The selected 47 private models are exactly the independent grammar packet’s `{models['model_version']}` text, with {c['cook_model_tokens']} bound tokens. Superseded hypotheses and transparent amendments remain in the independent evidence packet. In particular:

- The genitive complement of beðurfan is explicit inside the invariant relative in 44.3 and 44.6; the accusative head’s case is not copied into the relative’s internal role.
- The contrary condition and anterior intransitive wesan/participle result in 44.7 are supplied as a whole construction. Its second-time expression has the source-checked instrumental identity, not a relabelled dative or an inferred accusative.
- Conditional būtan, spatial būtan, comparison ofer and the selected causal, beneficial and substitution uses of for have separate contextual routes. The dative possessive in 48.6 uses the actual taught form; no earlier accusative record is relabelled.
- The earlier findan past singular funde remains valid under the actual Unit 4 exception. A temporary error diagnosis was withdrawn after primary evidence was checked; Unit 18 makes no corrective claim against that earlier teaching.
- The exact reading preserves ðēowa manna without an invented r, lęcgeað and the source vowel marks. The servant phrase remains locally explained; cwēn refers to the princess in this passage.
- Note 176.13 visibly gives the relative antecedent. The related task asks learners to explain the separation and the roles of the people and gifts; it does not pretend the antecedent must be independently discovered.
- The two gesund(e) passages have distinct agreement environments. Final ūs is accusative reflexive under Cook 177 note 2 and §184b, with the actual accusative identity. The final proposal to go and rest is not translated as a completed arrival.

## Validation and handoff

[Validation](validation.json) passes: exact source prompt and control crosswalks, all {c['cook_model_tokens']} Cook model tokens, all {c['source_words']} reading tokens, {c['original_oe_output_tokens']} original output tokens, input references, record ownership, unchanged earlier identities, complete response contracts, visible support routes and the literal cell/display bijection are checked. This certifies structural dependency closure, not linguistic truth by itself.

The coordinator still owns source reconciliation, the canonical contract checkpoint, lesson/key authorization, fresh independent solving, full paradigm review, exported-page inspection, registers, Beads and Git. A fresh solver must not read this proposal’s private model files or the canonical author-only contract before freezing solutions. Independent source and coordinator reading translations remain separate witnesses; I prepared the proposal’s whole translation from the actual Old English without consulting those witnesses.

The source editor and grammar analyst own their evidence packets. All design writes remain under `curriculum/proposals/unit18/` and `build/u18-design-*`; no Beads, Git, shared register, source index or chapter prose was changed by this worker.
'''
(O/'REPORT.md').write_text(report,encoding='utf8')
roles={
 'inventory.json':'Reconciled lexical, grammatical, reading and teaching proposal; coordinator integration input.',
 'task-plan.json':'All requested task and response contracts with exact dependencies.',
 'display-matrices.json':'Literal displays and one-to-one routes for every assigned paradigm cell.',
 'validation.json':'Structural audit receipt; source evidence and independent linguistic review remain separate.',
 'outcomes.json':'Bounded curricular outcomes, sequence and remaining coordinator gates.',
 'REPORT.md':'Human handoff and scope/status report.',
 'read_prior.py':'Reproducible baseline active-contract/register inspection.',
}
files=[]
for p in sorted(O.iterdir()):
 if not p.is_file() or p.name=='file-manifest.json':continue
 files.append({'path':p.as_posix(),'purpose':roles.get(p.name,'Supporting joined design evidence or private author-preparation record; follow references from inventory/task plan.'),'review_visibility':'Exclude from fresh blind solving until solutions are frozen.','canonical':False})
save(O/'file-manifest.json',{'schema_version':1,'chapter':'ch18','status':'complete proposal manifest','files':files,'generator':'build/u18-design-run.py','generator_scope':'Design artifacts only; no shared contract, register or chapter prose mutation.'})
print('final report, outcomes and file manifest written')
