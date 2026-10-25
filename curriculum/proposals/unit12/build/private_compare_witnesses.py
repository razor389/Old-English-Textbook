"""PRIVATE independent witness reconciliation; never feed this to the reserved solver."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[4];OUT=ROOT/'curriculum/proposals/unit12'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
a_path='curriculum/proposals/unit12/author-only-cook-independent-seed.json'
b_path='sources/audits/unit12-source/author-only-cook-models.json'
a=load(a_path);b=load(b_path);aa={x['task_id']:x for x in a['items']};bb={x['task_id']:x for x in b['items']}
decisions={
'19-01':'Both independently selected æt nīehstan plus geswīcan with genitive rīces. The fixed adverbial expression is local help.',
'19-02':'Both selected possession hæfde with the kingdom and the forty-year duration. The higher numeral is supplied; the duration construction is explicitly assigned.',
'19-03':'Use actual prior hwonne and newly productive bare geworht. Event-focused wurdon is a good canonical choice; wǣron remains a defensible contextual passive. Do not require an unassigned plural participle geworhte.',
'19-04':'Both selected tō-dæg, bist and mid mē; the day adverb and the contextual future use must have their exact records.',
'19-05':'Use taught gewyrcean preterite geworhton, exact supplied Rōmane and Breotone. The designer’s provisional Bretene and the source witness’s unprefixed worhton are replaced by the selected audited identities.',
'19-06':'Use actual ęngel messenger, not fishhook angel or an unmarked substituted spelling; recipient-facing beforan frame is separately assigned.',
'19-07':'Choose singular address throughout: ðū write. The second-singular preterite has short i; wrīte is the long-i present first singular, so the provisional homography claim is false. Plural gē writon can be accepted when the editorial situation explicitly makes the writers plural.',
'19-08':'Use the new productive gehīersumnes sense and select a subjunctive help-clause under the stated196d target, e.g. plural helpen. A grammatical indicative gif clause must be distinguished from compliance with that requested target.',
'19-09':'Both selected Sęnd mē micelne hęre; command, recipient and full army paradigm are explicitly assigned.',
'19-10':'The actual prior frame u11-feohtan-opponent governs accusative: wið mīne fīend. Do not substitute a new dative fighting frame merely because some other prepositional uses admit dative.',
'19-11':'Both selected plural ādrīfað with ēowre fīend; the command pair and enemy paradigm are complete.',
'19-12':'Both selected cęmpan fōron hām. The direction adverb is a new lexical assignment; it is not an accusative home noun guessed from a familiar form.',
'19-13':'Both selected contextual future cymð with dative sciphęre, whose complete hęre-family system is shown.',
'19-14':'Use actual prior command sleah. The public target selects animate all-who, ealle ðā ðe, rather than testing a neuter everything construction. The generic English remains verbatim and the chosen route stays an explicit editorial direction.',
'19-15':'Use independently evidenced welig on dative wæstmum. The designer’s provisional spēdig is not the selected taught lexical route.',
'19-16':'Prefer the explicitly taught bounded negative-concord route ne … nǣfre. The present plural geswīcað has contextual future reference and the new intransitive cease/fail frame.',
'19-17':'Both selected fēower tīda; the actual prior tīd sense already includes season, so no new seasonal sense is inferred without checking.',
'20-01':'Use actual prior dryhtnes, retaining the genitive predicate of possession. The source witness’s Drihtnes is not the selected registered spelling.',
'20-02':'Use the prior article se and masculine hē with the selected sea gender. The new objectless geseon frame and flēon indicative are explicit.',
'20-03':'Both selected future-context flīehð and weak īserne modifying accusative wǣpen. The transitive flee-object frame must be taught separately from intransitive flight.',
'20-04':'Retain every clause. Use actual gesiehð; preserve the original sē ðe hint and explain its relation to the selected model spelling, or locally supply the exact marked form. Nāh is an explicitly supplied negative āgan form. Both niman and the designer’s fōn seizure route need their actual lexical frames checked before selection.',
'20-05':'Use exactly selected gierwed, sętt and geworht, with sumer. Do not add unattested ge- prefixes by analogy or silently substitute sumor. Retain the two possessive predicates and all three active compound clauses; agree the finite auxiliary with ðū, not with its objects.',
'20-06':'Use already taught present-subjunctive hortative syntax, not an unassigned uton construction. Repeat gewyrcen in the second clause: prior dōn placement is narrowly on+accusative and does not establish a new around-frame. The new ābūtan frame takes accusative hīe, not the designer’s provisional dative him. Use actual registered connective spelling and preserve all cities, walls, towers and gates.',
'20-07':'Select the independently evidenced numerical comparison route and the new ādrīfan infinitive. Do not confuse larger size with greater number. Final numerical-comparison evidence is being reconciled by the coordinator.',
'20-08':'Use prior angel fishhook, not ęngel messenger or the designer’s unsupported fiscangul. Keep the first-fish weak ordinal and all four commands. Local inflectional guidance explains the preserved lemma-level ǣrest hint.',
'20-09':'Both selected pęning and masculine accusative ðone with beneficial for + dative. The future visit/event context permits a present gemētst.',
'21-01':'Both preserve past saying and present direct speech with feminine hēo; punctuation is editorial new composition.',
'21-02':'Use actual prior nōm and add the complete bounded rīsan command pair, whose absence was discovered in the actual register. No prefixed ārīsan system is presumed. The addressed noun retains its nominative-shaped weak-noun form.',
'21-03':'Select directly evidenced stānweall rather than introducing the designer’s provisional stone-adjective system. Genitive fōta measures breadth/height; the separate measure sense and higher numeral support are explicit.',
'21-04':'Use grētan with accusative, cȳðan with dative and a prospective report with locally supplied negative preterite subjunctive nolde plus the newly assigned genēosian infinitive. The bounded nǣfre mā … nolde expression conveys one negation, not cancellation. A bare preterite visiting clause can obscure the intended later refusal; the task must not imply an actual completed visit. A fresh unexposed reviewer must independently solve this item because the reserved reviewer disclosed an answer-bearing message.',
'21-05':'Both use substantive weak rihtwīsan and swā … swā with the expressly supplied lēo. The equative frame is newly taught; no unassigned lion declension is demanded.',
'21-06':'Both agree on supplied Bryttas and productive earge. The article can be contextual, not a hidden obligatory addition.',
'21-07':'Both selected fægere fǣmne. The prior weak-adjective address rule is actual u09-vocative-weak-adjective; the full new noun system is shown and hider explicitly promoted.',
'21-08':'Both preserve a genitive relative with antecedent folc and an independent God/subject relation. Use registered dryhten, not an unexplained Drihten spelling.',
'21-09':'Use a registered causal connective for-ðām or for-ðon-ðe. Keep learning-source æt, manner/respect on heortan, finding rest and dative beneficiaries. Ręst repose cites the exercise context explicitly because its vocabulary entry glosses couch/bed.',
'21-10':'The new selected gemang frame is accusative: wulfas, correcting both provisional witnesses’ dative. Word order alone does not alter the sending participants.',
'21-11':'Both select accusative ēow with ēhtan and a contextually prospective present. Local help supplies feminine accusative on ōðre with the city understood; preserve exact original (om. an)other adjacency in the English prompt.',
'21-12':'Both select grēte mīnne ēðel with the taught leave-taking sense and accusative frame; the full ēðel syncope system is assigned.'
}
rows=[]
for tid,x in aa.items():
 y=bb[tid];short=tid.removeprefix('EX-VI-')
 rows.append({'task_id':tid,'designer_independent_model':x['model'],'source_editor_independent_model':y['model'],'identical_surface':x['model']==y['model'],'reconciliation':decisions[short],'status':'canonical_binding_pending'})
final_path='sources/audits/unit12-source/author-only-cook-corrected-models.json'
final={m['task_id']:m for m in load(final_path)['items']}
bound=load('curriculum/proposals/unit12/author-only-cook-sequence-bindings.json')
assert not bound['issues'] and len(bound['sequences'])==38
for row in rows:
 row.update(canonical_model=final[row['task_id']]['model'],status='canonical_model_and_exact_ordered_bindings_reconciled')
source_reading=load('sources/audits/unit12-source/author-only-reading-witness.json')
source_account=load('sources/audits/unit12-source/author-only-composition-witness.json')
designer_readings=load('curriculum/proposals/unit12/author-only-model-seed.json')['translation_witness']
data={'schema_version':1,'chapter':'ch12','access':'PRIVATE: exclude until the corresponding independent solutions are frozen.','status':'all38_independent_witnesses_compared_and_canonical_bindings_reconciled','independence':'Both witnesses existed before either author consulted the other. Their initial strings remain preserved here and in the immutable seed files; corrections are separate decisions.','inputs':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in [a_path,b_path,final_path]},'items':rows,'counts':{'tasks':len(rows),'identical_initial_surfaces':sum(r['identical_surface'] for r in rows),'canonical_bound_tokens':sum(len(s['tokens']) for s in bound['sequences'])},'additional_actual_register_corrections':['Use scēaphierde, forlǣtt, ceastra/ceastre, sindon and ðā-hwīle-ðe; provisional shorter or variant strings did not establish those identities.','The supplied long Sē in20.4 now directly preserves the source cue; the ordinary article later in the same item remains se.'],'reading_comparisons':[{'source_span_id':source_reading['source_span_id'],'designer_translation':designer_readings['picts_scots'],'source_editor_translation':source_reading['translation'],'decision':'Both independent translations preserve the complete event chain, changing actors, prior Roman departure and final crop simile. Accept all they encountered as well as the contextual all whom; no human-only parsing is compulsory. Ordinary oppression/ruin synonyms remain defensible.'},{'composition_id':source_account['composition_id'],'designer_translation':designer_readings['controlled_reading'],'source_editor_translation':source_account['translation'],'decision':'Both independently recover the completed building before arrival, direct speech, intended travel, asserted departure and food-giving return. The selected key keeps one house to make the assigned cardinal ān explicit; natural English a house does not by itself teach a new Old English article sense.'}],'review_exposure':{'task_id':'EX-VI-21-04','fresh_unexposed_solver_required':True,'other_unexposed_tasks':75}}
(OUT/'author-only-witness-reconciliation.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(data['counts']))
