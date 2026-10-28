from pathlib import Path
import copy,json
O=Path('curriculum/proposals/unit18')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(n,d):(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
L=read('lexicon/entries.json');N=read('sources/audits/unit18-source/noun-adjective-paradigms.json');V=read('sources/audits/unit18-grammar/verbal-systems.json')
F={f['form_id']:(l['lemma_id'],f) for l in L['lemmas'] for f in l['forms']};S={s['sense_id']:(l['lemma_id'],s) for l in L['lemmas'] for s in l['senses']}
for p in N['paradigms']+V['systems']:
 for f in p['cells']:F[f['form_id']]=(p['lemma_id'],f)
for s in read('sources/audits/unit18-source/nominal-sense-audit.json')['senses']:S[s['sense_id']]=(s['lemma_id'],s)
for p in V['systems']:
 if p.get('sense_proposal'):S[p['sense_proposal']['sense_id']]=(p['lemma_id'],p['sense_proposal'])
alias={}
if (O/'inventory.json').exists():
 I=read(O/'inventory.json');alias=I.get('form_id_aliases',{})
 for l in I['lemmas']:
  F.update({f['form_id']:(l['lemma_id'],f) for f in l['forms']});S.update({s['sense_id']:(l['lemma_id'],s) for s in l['senses']})
def state(r):return 'previously_taught' if r.get('production_taught_in') else r.get('knowledge_status','unresolved')
seqs=[];models=[];tasks=[]
def sequence(tid,n,text,pairs,features):
 toks=[]
 assert len(text.split())==len(pairs)
 for i,(w,(fid,sid)) in enumerate(zip(text.split(),pairs),1):
  fid=alias.get(fid,fid);lid,f=F[fid];slid,s=S[sid];assert lid==slid
  assert w.strip('.,;:!?').casefold()==f['form'].casefold(),(w,f)
  assert state(f) in ['previously_taught','new_production'],(fid,state(f))
  assert state(s) in ['previously_taught','new_production'],(sid,state(s))
  toks.append({'token_index':i,'literal':w,'surface':f['form'],'lemma_id':lid,'form_id':fid,'sense_id':sid,'analysis':copy.deepcopy(f['analysis']),'contextual_analysis':copy.deepcopy(f.get('contextual_analysis',f['analysis'])),'form_status':state(f),'sense_status':state(s),'assessment_role':'independent_production','form_assessment_role':'independent_production','sense_assessment_role':'independent_production','independent_recall_assessment':True})
 sq={'sequence_id':f'{tid}-OUTPUT-{n:03}','output_position_id':f'{tid}-O{n:03}','owner_id':tid,'text':text,'tokens':toks,'kind':'author_only_output','origin_category':'new teaching material','feature_ids':features,'dependency_status':'closed_forms_and_senses'};seqs.append(sq);return sq

def task(tid,prompt,specs,analysis,features):
 outs=[]
 for n,(label,text,pairs,meaning,error) in enumerate(specs,1):
  sq=sequence(tid,n,text,pairs,features);oid=sq['output_position_id'];outs.append({'output_position_id':oid,'label':label,'response_language':'Old English','target':meaning,'essential_meaning':meaning,'alternatives_policy':'Accept grammatical variants preserving all stated roles, time, number and the explicitly selected lexical systems.','error_diagnosis':error,'output_sequence_id':sq['sequence_id']});models.append({'output_position_id':oid,'model':text,'target':meaning,'essential_meaning':meaning,'alternatives':'Accept other taught grammatical word orders preserving all roles, time and number; the specified lexical systems remain the target.','error_diagnosis':error,'output_sequence':sq})
 n=len(outs)+1;label,model,meaning,error=analysis;oid=f'{tid}-O{n:03}';outs.append({'output_position_id':oid,'label':label,'response_language':'English','target':meaning,'essential_meaning':meaning,'alternatives_policy':'Accept grammatical variants preserving all stated roles, time, number and the explicitly selected lexical systems.','error_diagnosis':error,'output_sequence_id':None});models.append({'output_position_id':oid,'model':model,'target':meaning,'essential_meaning':meaning,'alternatives':'Equivalent precise grammatical explanations are accepted.','error_diagnosis':error,'output_sequence':None})
 tasks.append({'task_id':tid,'key_id':'KEY-'+tid,'kind':'morphology_in_context','origin_category':'new teaching material','prompt':prompt,'input_sequence_ids':[],'input_texts':[],'requested_outputs':outs,'feature_ids':features,'stage':3,'mode':'analysis_and_production','dependency_status':'forms_and_senses_closed; construction_join_pending','assessment_scope':'Use the systems taught immediately beforehand. No model or inflected target form is printed in the prompt; complete sentences test agreement and government, and the final explanation tests the contrast.'})
se=('se-m-nom-sg','se-the');tha=('se-all-nom-pl','se-the');thane=('se-m-acc-sg','se-the');thapl=('se-all-acc-pl','se-the');thdat=('se-all-dat-pl','se-the');mann=('mann-nom-sg','mann-1');men=('mann-nom-pl','mann-1');king=('cyning-acc-sg','cyning-source');wheat=('hwaete-acc-sg','hwaete-u18-sense')
base=['article-agreement','u02-active-agreement']
task('NEW-U18-F01','Translate each sentence, then explain the selected ending contrast. Use the newly taught words for ass, sack and wheat.',[
 ('The ass has the sack.','Se assa hæfð ðone sacc.',[se,('assa-nom-sg','assa-u18-sense'),('habban-pres-3-sg','habban-1'),thane,('sacc-acc-sg','sacc-u18-sense')],'Singular ass is subject; sack is accusative possession.','Do not use oblique assan as the nominative singular.'),
 ('The asses have the sacks.','Ðā assan habbað ðā saccas.',[tha,('assa-nom-pl','assa-u18-sense'),('habban-pres-3-pl','habban-1'),thapl,('sacc-acc-pl','sacc-u18-sense')],'Plural subjects and objects with plural finite agreement.','Do not apply strong masculine -as to the weak ass noun.'),
 ('The men give wheat to the asses.','Ðā męnn sęllað ðǣm assum hwǣte.',[tha,men,('sellan-pres-3-pl','sellan-give'),thdat,('assa-dat-pl','assa-u18-sense'),wheat],'Men give; asses are dative recipients; wheat is a mass singular object.','Do not make the recipients accusative or invent a count plural for the selected wheat sense.'),
 ('The wheat is in the sacks.','Se hwǣte is on ðǣm saccum.',[se,('hwaete-nom-sg','hwaete-u18-sense'),('wesan-pres-3-sg','wesan-be'),('on-invariant','on-1'),thdat,('sacc-dat-pl','sacc-u18-sense')],'Mass singular wheat controls singular is; static location takes dative plural sacks.','Do not let plural sacks govern the copula.')],
 ('Compare the plural noun endings in the first three translations and the location phrase.','Assan is weak nominative plural; saccas is strong accusative plural. Both classes have dative plural -um: assum as recipient and saccum after static on. Wheat retains the selected mass singular.','Distinguish the two noun patterns while applying ordinary number, recipient and location functions.','A common dative plural ending does not make the entire declensions identical.'),base+['u02-giving-recipient','on-dative-location'])
task('NEW-U18-F02','Translate the two sentences using the newly taught verb meaning need. Then explain the governed noun.',[
 ('The man needs wheat.','Se mann beðearf hwǣtes.',[se,mann,('bethurfan-u18-present-indicative-3-sg','bethurfan-u18-selected'),('hwaete-gen-sg','hwaete-u18-sense')],'Present singular need with a genitive thing needed.','Do not substitute an accusative object merely because English has no preposition.'),
 ('The men needed wheat.','Ðā męnn beðorfton hwǣtes.',[tha,men,('bethurfan-u18-preterite-indicative-3-pl','bethurfan-u18-selected'),('hwaete-gen-sg','hwaete-u18-sense')],'Preterite plural need with the same genitive mass noun.','Do not use the present plural beðurfon to express this completed past need.')],
 ('Identify the tense and number of each finite verb, and explain the case of wheat in both sentences.','Beðearf is present indicative third singular; beðorfton is preterite indicative third plural. Hwǣtes is genitive singular governed by need in both, independent of the subject’s number.','Separate finite agreement/tense from lexical genitive government.','The genitive complement does not agree in number with the subject.'),base+['u18-bethurfan-genitive-relative'])
task('NEW-U18-F03','Translate the four sentences using the newly taught verbs meaning recognize and undo/open. Then explain the roles and number changes.',[
 ('I recognize the king.','Ic oncnāwe ðone cyning.',[('ic-nom-sg','ic-personal'),('oncnawan-u18-present-indicative-1-sg','oncnawan-u18-selected'),thane,king],'First singular present recognition and accusative person.','Do not substitute a past form for the present.'),
 ('We recognized the king.','Wē oncnēowon ðone cyning.',[('ic-nom-pl','ic-personal'),('oncnawan-u18-preterite-indicative-1-pl','oncnawan-u18-selected'),thane,king],'First plural preterite recognition and unchanged singular object.','Do not pluralize the king when the recognizing subject changes number.'),
 ('The man opens the sack.','Se mann undēð ðone sacc.',[se,mann,('undon-u18-present-indicative-3-sg','undon-u18-selected'),thane,('sacc-acc-sg','sacc-u18-sense')],'Third singular present undo/open and accusative sack.','Do not use the infinitive where the sentence requires a finite verb.'),
 ('The men opened the sacks.','Ðā męnn undydon ðā saccas.',[tha,men,('undon-u18-preterite-indicative-3-pl','undon-u18-selected'),thapl,('sacc-acc-pl','sacc-u18-sense')],'Third plural preterite open with plural accusative sacks.','Do not retain singular article/object or present tense.')],
 ('Identify the direct objects and explain which words change when the subject, object or tense changes.','The king is the singular accusative object of both recognition clauses. Sack and sacks are accusative objects of undo/open. The finite verb changes for subject person/number and tense; object number determines its article and noun, not the verb’s person.','Track independent agreement domains and accusative objects across finite stem changes.','Do not derive finite agreement from a nearer object.'),base+['u18-oncnawan-object','u18-undon-object'])
save('form-task-plan.json',{'schema_version':1,'chapter':'ch18','tasks':tasks,'counts':{'tasks':len(tasks),'outputs':sum(len(t['requested_outputs']) for t in tasks)}})
save('author-only-form-models.json',{'schema_version':1,'visibility':'AUTHOR ONLY. Exclude from blind solving.','models':models})
save('author-only-form-bindings.json',{'schema_version':1,'visibility':'AUTHOR ONLY. Exclude from blind solving.','sequences':seqs})
save('form-input-bindings.json',{'schema_version':1,'sequences':[],'scope':'English prompts contain no Old English lexical or inflected reference inputs.'})
print(json.dumps({'tasks':len(tasks),'outputs':len(models),'Old_English_outputs':len(seqs),'bound_tokens':sum(len(s['tokens']) for s in seqs)}))
