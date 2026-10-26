"""Private semantic seeds and complete original-task output positions."""
from pathlib import Path
import json,importlib.util
ROOT=Path.cwd();OUT=ROOT/'curriculum/proposals/unit13'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def save(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

answers={
'A01':dict(models=['The bishop greeted the monk.','The bishop greeted the monk.'],analysis='In both, se bisceop is nominative subject, ðone munuc accusative object and grētte the third-singular finite verb. Fronting changes arrangement, not participants.'),
'A02':dict(models=['When the monk came, the bishop then greeted the brothers.'],analysis='Dependent subject se munuc with cōm; main subject se bisceop with grētte. First ðā is temporal when, second correlative then, third accusative-plural article before the object brōðor.'),
'A03':dict(models=['The bishop whom the monk greeted sat in the house.'],analysis='Main sæt has se bisceop as subject; relative grētte has se munuc as subject. Antecedent bisceop is nominative in the main clause, while invariant ðe represents the direct object inside the relative.'),
'A04':dict(models=['The monk greeted the bishop and gave him the food.'],analysis='The monk is the expressed first and understood second subject. The bishop is greeted and receives the food. Him is masculine dative singular; męte is accusative singular as the thing given, although its surface is syncretic with other cases.'),
'A05':dict(models=['It was pleasant.','He was in the house.'],analysis='First hē refers to masculine sang, the song; second to the bishop. Both are masculine singular subjects; context and lexical antecedents select them, not an English human/nonhuman division.'),
'A06':dict(analysis='Both the bishop and the monk are grammatically possible referents. Gender and number do not choose one. Repeating the chosen noun phrase makes the intended reading explicit.',old_english_outputs_from='author-only-sequence-bindings.json'),
'A07':dict(models=['The monk said, “I heard the song. Did you hear it?”'],analysis='Ic is the monk who is speaking; ðū the addressed bishop; hine the masculine song. Hīerdest is second singular preterite indicative. It is not an instruction to obey the bishop.'),
'A08':dict(models=['The monk said that he was in the house.'],analysis='Sægde is main third-singular preterite; ðæt introduces the content through wǣre. The stated context identifies hē as the monk. Wǣre is the reporting preterite subjunctive, with presence simultaneous with the report.'),
'A09':dict(models=['The bishop was in the church, and the brothers were in the house.'],analysis='The repeated lexical copula is recoverable. If expressed, it must be plural wǣron because brōðor is plural; copying singular wæs would not satisfy agreement.',old_english_outputs_from='author-only-sequence-bindings.json'),
'A10':dict(models=['The monk sat in the house.','When the monk sat in the house, the bishop came.'],analysis='The first begins with a fronted main-clause locative phrase; sæt is finite and se munuc subject. The second begins with an entire temporal clause containing sæt and subject se munuc; cōm with se bisceop belongs to the following main clause. On and ðā alone do not identify an actor.'),
'A11':dict(models=['When the monk whom the bishop greeted came, the brothers sang.'],analysis='Outer temporal clause: se munuc ... cōm. Nested relative: ðe se bisceop grētte, with monk as relative object. Main: ðā sungon ðā brōðor. Finite subjects are monk, bishop and brothers respectively. First ðā when, second then, third article; ðe relative object.'),
'A12':dict(analysis='Second position counts complete constituents, not separate written words. Attested ordering varies, including fronted adverbial followed by a pronoun before its finite verb, so neither universal V2 nor universal dependent verb-final order follows. Cook25.7 nevertheless states an explicit final-verb target; grammatical alternatives can be distinguished from compliance with that target.'),
'R01':dict(models=['The bishop sat in the house, and the monk was there. When the monk heard the song, he went to the bishop. The monk said, “I heard the song, which was very pleasant. Did you hear it?” The bishop said, “Go now, and lead the brothers here.” Then the monk went to the church, and came back with the brothers. The bishop saw them and said, “You are my friends. I want to speak with you.” The monk sat with the brothers, and they heard the bishop’s words.']),
'R02':dict(analysis='Hē after ēode is the monk; hine is the masculine song; hīe after geseah is the brothers or the returning party including the monk, with no grammatical basis for excluding the monk categorically. Ic in the final speech is the bishop, ēow his plural addressees. Hine is a grammatical masculine object, not a guarantee of human reference.'),
'R03':dict(analysis='Temporal: Ðā se munuc ðone sang hīerde, finite hīerde, subject monk. Associated main: ðā ēode hē tō ðǣm bisceope, finite ēode, subject hē=monk. Relative: ðe swīðe wynsum wæs, finite wæs, relative subject=song. Coordinated omission: and cōm ęft mid ðǣm brōðrum, finite cōm, understood subject=monk from ēode.'),
'R04':dict(analysis='Hearing precedes inquiry; the bishop then commands, the monk returns, and the bishop makes the final speech. Bishop, monk and brothers are present at the end; the explicit final se munuc sæt mid ðǣm brōðrum establishes the monk with the brothers. The account does not report a yes/no answer to the monk’s question.'),
'S01':dict(models_from='author-only-source-translation-witness.json'),
'S02':dict(analysis='Owini is subject of dyde and main gehīerde; companions of ēodon and dydon; the bishop of wæs; Owini again of parenthetical sægde. First ðā is the opening temporal conjunction, second internal then, and the later ðā before gehīerde is the main-clause correlative. Preserve the coordinated background and parenthetical as-clause; āstīgan is a perceived infinitive, not another finite predicate.'),
'S03':dict(analysis='Both hē becōm and hē in ðe hē ǣr cōm refer to the masculine sang. Its route is from the southeastern heaven to the oratory roof/interior, then back up to heaven by its former route. The exact nēalǣcton plural can continue the paired voice and song; the later masculine singular does not introduce a new human journey.'),
'S04':dict(analysis='Owini listens and directs his attention, hears the return, stays wondering and considers the significance, then responds to the signal by entering. Chad opens the window and makes the signal, then speaks the summons. Hē, se bisceop explicitly marks Chad as the speaker after Owini’s entering.'),
'S05':dict(models=['the oratory in which the bishop was'],analysis='Antecedent is ciricean, the oratory. In is the stranded preposition whose complement relation is carried by the relative; note11 says governed by in. The local help licenses this analysis; independent production of the pattern is not required.'),
'S06':dict(analysis='The fronted objects are Ðā stefne and ðone sang. Their governing verb is embedded gehīerde, not reporting cwæð. Main hē cwæð introduces ðæt hē ǣrest gehīerde ...; note8 explicitly identifies the accusative government. Treat the fronting as the supported source construction, not a general transformation task.'),
'S07':dict(analysis='Chad speaks to Owini. Ūre denotes their shared monastic community, mē is Chad, and ðū is Owini. The seven brothers are to come from the communal church; Owini is expressly to be present as well. Note152.5 distinguishes the local oratory from the church to which the monks went.'),
'S08':dict(analysis='Accept any accurately delimited main/dependent pair with its actual finite verb, subject and initial constituent. The bishop-window main clause has initial ðā then followed by ontȳnde and nominal subject; the relative ðe se bisceop in wæs has late finite wæs. A legitimate differently ordered source example is also acceptable if its clause boundary and dependencies are correct.'),
}
for code in ['C01','C02','C03','C04','C05','C06','C07','C08']:
    answers[code]=dict(old_english_outputs_from='author-only-sequence-bindings.json',analysis='Preserve the stated participant roles and target construction; accept other defensible spelling/word-order variants while distinguishing valid language from exact target compliance.')

pars=load('sources/audits/unit13-source/noun-adjective-paradigms.json')['paradigms']
if (ROOT/'sources/audits/unit13-grammar/grammar-records.json').exists():pars+=load('sources/audits/unit13-grammar/grammar-records.json').get('paradigms',[])
form_records={f['form_id']:f for p in ['lexicon/entries.json','sources/audits/unit13-source/lexical-inventory.json','sources/audits/unit13-grammar/grammar-records.json'] if (ROOT/p).exists() for l in load(p).get('lemmas',[]) for f in l.get('forms',[])}
prior_lex=load('lexicon/entries.json')
began=next(l for l in prior_lex['lemmas'] if l['lemma_id']=='began')
if not any(p['lemma_id']=='began' and p['paradigm_id'].endswith('-IMP') for p in pars):
    pars.append(dict(paradigm_id='NEW-U09-PAR-began-IMP',lemma_id='began',prior_contract='chapters/ch09/coverage.json',cells=[{**f,'knowledge_status':'previously_taught'} for f in began['forms'] if f['form_id'] in ['began-imp-2-sg','began-imp-2-pl']]))
def cells(lemma,filter=None):
    result=[]
    for p in pars:
        if p['lemma_id']!=lemma:continue
        for c in p['cells']:
            c=dict(c)
            if not isinstance(c.get('analysis'),dict):c['analysis']=form_records[c['form_id']].get('analysis',{})
            if filter is None or filter(c,p):result.append(dict(paradigm_id=p['paradigm_id'],**c))
    return result
F={
'F01':[c for l in ['modor','dohtor','brothor'] for c in cells(l)],
'F02':[c for l in ['aex','eagthyrel'] for c in cells(l)],
'F03':[c for l in ['cirice','mynster','wyrttruma'] for c in cells(l,lambda c,p:(c['analysis']['case'],c['analysis']['number']) in [('gen','sg'),('dat','sg'),('nom','pl'),('gen','pl')])],
'F04':cells('swete',lambda c,p:c['analysis'].get('declension')=='strong' and c['analysis']['case']!='ins')+cells('swete-comp',lambda c,p: all(c['analysis'].get(k)==v for k,v in {'case':'nom','number':'sg','gender':'m','declension':'weak'}.items()))+cells('swete-superl',lambda c,p:all(c['analysis'].get(k)==v for k,v in {'case':'nom','number':'sg','gender':'m'}.items())),
'F05':cells('forceorfan',lambda c,p:p['paradigm_id'].endswith('-IND')),
'F06':[c for l in ['winnan','began','behealdan'] for c in cells(l,lambda c,p:p['paradigm_id'].endswith('-IMP'))]+[c for l in ['fordilgian','onliesan'] for c in cells(l,lambda c,p:p['paradigm_id'].endswith('-PART'))]
}
for code,records in F.items():answers[code]=dict(morphological_outputs=[dict(position=i,form_id=c['form_id'],form=c['form'],analysis=c.get('analysis',{}),paradigm_id=c['paradigm_id']) for i,c in enumerate(records,1)],analysis='Use the complete selected systems and explicitly printed stem/ending rules. Documented alternatives remain valid; reference-only cells are not independent production targets.')

seed=load('curriculum/proposals/unit13/task-seed.json')
output=[]
for t in seed['tasks']:
    code=t['task_id'].removeprefix('NEW-U13-')
    assert code in answers,code
    output.append(dict(task_id=t['task_id'],key_id=t['key_id'],requested_outputs=t['requested_outputs'],target=t['target_specification'],**answers[code]))
save('author-only-model-seed.json',dict(schema_version=1,chapter='ch13',private=True,pre_key_excluded=True,status='private_semantic_seeds_pending_final_audit_and_contract',models=output,note='Author preparation only. These are not a published answer key, a frozen independent solution witness, or permission to draft before the contract.'))
print(json.dumps(dict(models=len(output),morphology_output_counts={k:len(v) for k,v in F.items()})))
