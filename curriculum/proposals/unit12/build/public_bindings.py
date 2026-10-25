"""Explicit public token identities; add final new-record aliases only after audit."""
from pathlib import Path
import json,copy
ROOT=Path.cwd();OUT=ROOT/'curriculum/proposals/unit12'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def write(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def prior_status(r):return 'previously_taught' if r.get('production_taught_in') else 'previously_recognition' if r.get('recognition_taught_in') else 'previously_supplied'
lemmas={};forms={};senses={};prior_productive_forms=set();prior_productive_senses=set()
for path in ['lexicon/entries.json','sources/audits/unit12-source/lexical-inventory.json','sources/audits/unit12-grammar/grammar-records.json']:
 if not (ROOT/path).exists():continue
 for l in load(path)['lemmas']:
  old=lemmas.get(l['lemma_id'],{})
  new={**old,**copy.deepcopy(l)}
  for key,ident in [('forms','form_id'),('senses','sense_id')]:
   d={r[ident]:r for r in old.get(key,[])};d.update({r[ident]:copy.deepcopy(r) for r in l.get(key,[])})
   new[key]=list(d.values())
  lemmas[l['lemma_id']]=new
  for f in l.get('forms',[]):
   if path=='lexicon/entries.json' and f.get('production_taught_in'):prior_productive_forms.add(f['form_id'])
   state='previously_taught' if f['form_id'] in prior_productive_forms else prior_status(f) if path=='lexicon/entries.json' else f['knowledge_status']
   forms[f['form_id']]={**copy.deepcopy(f),'lemma_id':l['lemma_id'],'resolved_status':state}
  for s in l.get('senses',[]):
   if path=='lexicon/entries.json' and s.get('production_taught_in'):prior_productive_senses.add(s['sense_id'])
   state='previously_taught' if s['sense_id'] in prior_productive_senses else prior_status(s) if path=='lexicon/entries.json' else s['knowledge_status']
   senses[s['sense_id']]={**copy.deepcopy(s),'lemma_id':l['lemma_id'],'resolved_status':state}

ALIASES={'@when':'tha-conjunction-invariant|tha-when','@then':'tha-adverb-invariant|tha-adverb-1','@have-result-1':'habban-pres-1-sg|habban-perfect','@had-result-1':'habban-pret-1-sg|habban-perfect','@had-result-3':'habban-pret-3-sg|habban-perfect','@had-report-3':'habban-preterite-subj-3-sg|habban-perfect','@went-part':'gewitan-past-participle','@sitting-part':'sittan-present-participle','@gierwed':'gierwan-past-participle'}
SENSE_ALIASES={'@habban-result':'habban-perfect','@wesan-intransitive':'wesan-intransitive-perfect','@wesan-present-participle':'wesan-present-participle'}
DEFAULT_SENSE={'se':'se-the','wesan':'wesan-be','he':'he-1','ic':'ic-personal','thu':'thu-personal','cuman':'cuman-come','sellan':'sellan-give','gewitan':'gewitan-depart','on':'on-1','thaet-conjunction':'thaet-conjunction-1','habban':'habban-1','secgan':'secgan-content','weorthan':'weorthan-1'}
E={
'01':'se-m-nom-sg mann-nom-sg cuman-pret-3-sg and-invariant he-m-nom-sg geseon-pret-3-sg se-n-acc-sg hus-acc-sg',
'02':'se-m-nom-sg mann-nom-sg geseon-pret-3-sg se-n-acc-sg hus-acc-sg the-relative-invariant he-m-gen-sg|he-possessor sunu-nom-sg gewyrcean-pret-3-sg',
'03':'nu-invariant @have-result-1 ic-nom-sg se-n-acc-sg hus-acc-sg gewyrcean-past-participle',
'04':'@when se-m-nom-sg sunu-nom-sg cuman-pret-3-sg @had-result-3 se-m-nom-sg mann-nom-sg se-n-acc-sg hus-acc-sg gewyrcean-past-participle',
'05':'se-m-nom-sg mann-nom-sg bindan-pret-3-sg se-n-acc-sg hors-acc-sg se-n-nom-sg hors-nom-sg weorthan-pret-3-sg|weorthan-1 bindan-participle-citation',
'06':'se-n-nom-sg hors-nom-sg wesan-pret-3-sg|wesan-passive bindan-participle-citation',
'07':'se-m-nom-sg mann-nom-sg wesan-pret-3-sg|@wesan-intransitive @went-part',
'08':'se-m-nom-sg mann-nom-sg wesan-pret-3-sg|@wesan-present-participle @sitting-part',
'09':'he-m-nom-sg secgan-pres-3-sg thaet-conjunction-invariant he-m-nom-sg wesan-present-subj-3-sg her-invariant he-m-nom-sg secgan-pret-3-sg thaet-conjunction-invariant he-m-nom-sg wesan-preterite-subj-3-sg her-invariant',
'10':'he-m-nom-sg secgan-pret-3-sg thaet-conjunction-invariant he-m-nom-sg se-n-acc-sg hus-acc-sg gewyrcean-past-participle @had-report-3',
'11':'he-m-nom-sg secgan-pret-3-sg thaet-conjunction-invariant he-m-nom-sg willan-preterite-subj-3-sg cuman-infinitive-citation',
'12':'he-m-nom-sg cuman-pres-3-sg'
}
A={
'A01':[E['01']], 'A02':[E['02']],
'A03':['ic-nom-sg @have-result-1 se-n-acc-sg hus-acc-sg gewyrcean-past-participle','ic-nom-sg @had-result-1 se-n-acc-sg hus-acc-sg gewyrcean-past-participle'],
'A04':['ic-nom-sg habban-pres-1-sg se-n-acc-sg hus-acc-sg','ic-nom-sg @have-result-1 se-n-acc-sg hus-acc-sg gewyrcean-past-participle'],
'A05':['se-m-nom-sg mann-nom-sg bindan-pret-3-sg se-n-acc-sg hors-acc-sg','se-n-nom-sg hors-nom-sg weorthan-pret-3-sg|weorthan-1 bindan-participle-citation',E['06']],
'A06':[E['07']], 'A07':[E['08']],
'A08':['he-m-nom-sg secgan-pres-3-sg thaet-conjunction-invariant he-m-nom-sg wesan-present-subj-3-sg her-invariant','he-m-nom-sg secgan-pret-3-sg thaet-conjunction-invariant he-m-nom-sg wesan-preterite-subj-3-sg her-invariant'],
'A09':[E['10']], 'A10':[E['11']],
'A11':[E['12'],'he-m-nom-sg willan-pres-3-sg cuman-infinitive-citation']
}
READ='''se-m-nom-sg mann-nom-sg @had-result-3 an-acc-n-sg-strong hus-acc-sg gewyrcean-past-participle
@then cuman-pret-3-sg he-m-gen-sg|he-possessor sunu-nom-sg and-invariant se-m-nom-sg sunu-nom-sg geseon-pret-3-sg se-n-acc-sg hus-acc-sg
se-m-nom-sg faeder-nom-sg cwethan-pret-3-sg nu-invariant @have-result-1 ic-nom-sg se-n-acc-sg hus-acc-sg gewyrcean-past-participle
se-m-nom-sg sunu-nom-sg secgan-pret-3-sg thaet-conjunction-invariant he-m-nom-sg willan-preterite-subj-3-sg faran-infinitive-citation
@when se-m-nom-sg sunu-nom-sg gewitan-pret-3-sg @then sittan-pret-3-sg se-m-nom-sg faeder-nom-sg on-invariant se-n-dat-sg hus-dat-sg-source
@then cuman-pret-3-sg se-m-nom-sg sunu-nom-sg and-invariant he-m-nom-sg sellan-pret-3-sg he-m-gen-sg|he-possessor faeder-dat-sg mete-acc-sg'''

issues=[]
def make_sequence(seqid,text,spec,owner,kind):
 words=text.split();refs=spec.split()
 if len(words)!=len(refs):issues.append({'sequence_id':seqid,'error':'token_count','text_tokens':len(words),'binding_tokens':len(refs)});return None
 tokens=[]
 for i,(literal,ref) in enumerate(zip(words,refs),1):
  ref=ALIASES.get(ref,ref);bits=ref.split('|');fid=ALIASES.get(bits[0],bits[0]);f=forms.get(fid)
  if not f:issues.append({'sequence_id':seqid,'token_index':i,'literal':literal,'missing_form_id':fid});continue
  lid=f['lemma_id'];sid=SENSE_ALIASES.get(bits[1],bits[1]) if len(bits)>1 else DEFAULT_SENSE.get(lid)
  if sid is None:sid=lemmas[lid]['senses'][0]['sense_id']
  s=senses.get(sid);clean=literal.strip('.,:;!?“”"()[]')
  if clean.casefold()!=f['form'].casefold():issues.append({'sequence_id':seqid,'token_index':i,'literal':literal,'form_id':fid,'registered_form':f['form'],'error':'surface_mismatch'})
  if s is None or s['lemma_id']!=lid:issues.append({'sequence_id':seqid,'token_index':i,'literal':literal,'form_id':fid,'sense_id':sid,'error':'missing_or_different_lemma_sense'});continue
  tokens.append({'token_index':i,'literal':literal,'surface':clean,'lemma_id':lid,'form_id':fid,'sense_id':sid,'form':f['form'],'analysis':f['analysis'],'form_status':f['resolved_status'],'sense_status':s['resolved_status']})
 return {'sequence_id':seqid,'owner_id':owner,'kind':kind,'text':text,'tokens':tokens,'required_form_ids':sorted({t['form_id'] for t in tokens}),'required_sense_ids':sorted({t['sense_id'] for t in tokens})}

if __name__=='__main__':
 comp=load('curriculum/proposals/unit12/composition-seed.json');tasks=load('curriculum/proposals/unit12/task-seed.json');seqs=[]
 for e in comp['teaching_examples']:
  seq=make_sequence(e['example_id']+'-INPUT',e['text'],E[e['example_id'][-2:]],e['example_id'],'translated_teaching_example')
  if seq:seqs.append(seq)
 for t in tasks['tasks']:
  code=t['task_id'].removeprefix('NEW-U12-')
  for i,(txt,spec) in enumerate(zip(t['input_texts'],A.get(code,[])),1):
   seq=make_sequence(t['task_id']+f'-INPUT{i}',txt,spec,t['task_id'],'graded_public_input')
   if seq:seqs.append(seq)
 c=comp['new_reading'];seq=make_sequence(c['span_id']+'-INPUT',c['text'],READ,c['span_id'],'controlled_connected_reading')
 if seq:seqs.append(seq)
 write('public-sequence-bindings.json',{'schema_version':1,'chapter':'ch12','status':'closed' if not issues else 'pending_audit_records','sequences':seqs,'issues':issues})
 print(json.dumps({'sequences':len(seqs),'tokens':sum(len(s['tokens']) for s in seqs),'issue_count':len(issues),'issues':issues[:30]},ensure_ascii=False))
