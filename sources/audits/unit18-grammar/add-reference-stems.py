"""Bounded diagnostic citation records; do not grant extra productive cells."""
import json
from pathlib import Path
O=Path(__file__).resolve().parent;p=O/'verbal-systems.json';d=json.loads(p.read_text(encoding='utf8'))
for s in d['systems']:
 ds=[]
 for c in s['cells']:
  a=c['analysis'];key=(a.get('tense'),a.get('mood'),a.get('verb_form'))
  if a.get('person',1)!=1 and not(a.get('person')==3 and s['lemma_id']=='ofthyncean'):continue
  if a.get('mood')=='indicative'and a.get('number')=='sg'and a.get('person')==1:label=a['tense']+' indicative first singular'
  elif a.get('mood')=='indicative'and a.get('number')=='pl'and a.get('person')==1:label=a['tense']+' indicative plural'
  elif a.get('mood')=='subjunctive':label=a['tense']+' subjunctive '+a['number']
  elif a.get('verb_form'):label=a.get('tense','')+' '+a['verb_form']
  elif s['lemma_id']=='ofthyncean':label=a['tense']+' '+a['mood']+' impersonal third singular'
  else:continue
  if not any(x['form']==c['form']and x['label']==label.strip()for x in ds):ds.append({'form':c['form'],'label':label.strip(),'evidence_refs':s['evidence_refs'],'status':'reference to independently displayed literal cell','productive_form_id':c['form_id']})
 if not ds:
  ds=[{'form':c['form'],'label':'imperative '+c['analysis']['number'],'evidence_refs':s['evidence_refs'],'status':'reference to independently displayed literal cell','productive_form_id':c['form_id']}for c in s['cells']]
 s['principal_parts']=ds
 s['citation_reference']={'infinitive':s['headword'],'diagnostic_stems':ds,'status':'supplied_reference','evidence_refs':s['evidence_refs'],'limitation':'This bounded citation records only the headword and source-checked diagnostic forms actually needed for the selected system. It is not an unassigned full principal-part or finite paradigm. A headword or a citation outside a separately displayed productive cell is visible reference only.'}
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('reference records',len(d['systems']))
