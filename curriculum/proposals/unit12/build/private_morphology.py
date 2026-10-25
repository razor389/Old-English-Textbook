"""PRIVATE: morphology models selected from independently audited complete systems."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[4];OUT=ROOT/'curriculum/proposals/unit12'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
n=load('sources/audits/unit12-source/noun-adjective-paradigms.json')
g=load('sources/audits/unit12-grammar/grammar-records.json')
pars={p['paradigm_id']:p for p in n['paradigms']+g['paradigms']}
forms={f['form_id']:{**f,'lemma_id':l['lemma_id']} for package in [load('lexicon/entries.json'),load('sources/audits/unit12-source/lexical-inventory.json'),g] for l in package['lemmas'] for f in l.get('forms',[])}
seeds=load('curriculum/proposals/unit12/task-seed.json')['tasks'];models=load('curriculum/proposals/unit12/author-only-model-seed.json')
existing={m['task_id']:m for m in models['models']}
morphology_senses={'fot':'fot-foot-source','brycg':'brycg-1','here':'here-1','fleon':'fleon-flee','gretan':'gretan-take-leave','gemetan':'gemetan-find','adrifan':'adrifan-expel','geopenian':'geopenian-open','cythan':'cythan-announce','gierwan':'gierwan-1','settan':'settan-1','gewyrcean':'gewyrcean-1'}
groups={
 'F01':[('fōt','NEW-U12-NOM-FOT',None)],
 'F02':[('brycg','NEW-U12-NOM-BRYCG',None),('hęre','NEW-U12-NOM-HERE',None)],
 'F03':[('flēon','NEW-U12-PAR-fleon-IND',None),('grētan','NEW-U12-PAR-gretan-IND',None)],
 'F04':[],
 'F05':[(lid,'NEW-U12-PAR-'+lid+'-IMP',None) for lid in ['fleon','adrifan','gemetan','geopenian']],
 'F07':[(lid,'NEW-U12-PAR-'+lid+'-PART',None) for lid in ['gierwan','settan','gewyrcean']]
}
queries=[{'tense':'present','person':2,'number':'sg'},{'tense':'present','person':3,'number':'sg'},{'tense':'preterite','person':2,'number':'sg'},{'tense':'preterite','person':3,'number':'pl'}]
def analysis(c):return {**forms[c['form_id']].get('analysis',{}),**c.get('analysis',{}),**{k:c[k] for k in ['tense','mood','person','number'] if k in c}}
for lid in ['gemetan','adrifan','geopenian','cythan']:
 p=pars['NEW-U12-PAR-'+lid+'-IND'];selected=[]
 for q in queries:
  hits=[c for c in p['cells'] if all(analysis(c).get(k)==v for k,v in q.items())]
  assert len(hits)==1,(lid,q,hits)
  selected.append(hits[0])
 groups['F04'].append((lid,None,selected))
notes={
 'F01':'Fōt has the inherited vowel alternation in its selected dative singular and nominative/accusative plural; genitive and dative plural retain fōt-. Do not apply one vowel throughout every cell.',
 'F02':'Give all four cases in both numbers. Keep brycg’s checked stem and hęre’s independently specified oblique and plural forms; a familiar ending does not establish an unattested stem.',
 'F03':'Each complete indicative system has six present and six preterite positions. Distinguish contracted strong flēon from weak grētan and preserve the independently checked stems.',
 'F04':'The four requested positions expose present stem alternation, the strong second-singular/plural preterite stem, and the respective weak preterite formations. Select cells by person, number and tense before writing them.',
 'F05':'A singular command addresses one person; its plural counterpart addresses several. Use each verb’s checked command stem, without adding an indicative third-singular ending.',
 'F07':'These are present- and past-participle bases, not finite personal forms. Each retains its separately checked lexical stem; these six bases do not by themselves license an unassigned adjective declension.'
}
for code,gg in groups.items():
 tid='NEW-U12-'+code;sub=[];allcells=[]
 for label,pid,chosen in gg:
  cells=pars[pid]['cells'] if pid else chosen
  for c in cells:
   f=forms[c['form_id']]
   assert f.get('production_taught_in') or f.get('knowledge_status') in ['new_production','previously_taught'],(tid,c)
  sub.append({'label':label,'paradigm_id':pid,'forms':[{'form_id':c['form_id'],'form':c['form'],'analysis':analysis(c)} for c in cells]});allcells+=cells
 seed=next(t for t in seeds if t['task_id']==tid)
 existing[tid]={'task_id':tid,'model':'; '.join(s['label']+': '+', '.join(f['form'] for f in s['forms']) for s in sub),'morphology_groups':sub,'required_output_form_ids':sorted({c['form_id'] for c in allcells}),'required_output_sense_ids':sorted({morphology_senses[forms[c['form_id']]['lemma_id']] for c in allcells}),'target':seed['target_specification'],'explanation':notes[code],'alternatives':'Accept only documented variants within their stated lexical and morphological cells.','diagnosis':notes[code],'status':'complete_morphology_model'}
pattern=load('curriculum/proposals/unit12/construction-patterns.json')['patterns'][0]
assert len(pattern['positions'])==12
tid='NEW-U12-F06';seed=next(t for t in seeds if t['task_id']==tid)
existing[tid]={'task_id':tid,'model':' '.join(p['text'] for p in pattern['positions']),'construction_groups':[{'label':pattern['title'],'pattern_id':pattern['pattern_id'],'positions':pattern['positions']}],'required_output_form_ids':sorted({fid for p in pattern['positions'] for fid in p['sequence']['required_form_ids']}),'required_output_sense_ids':sorted({sid for p in pattern['positions'] for sid in p['sequence']['required_sense_ids']}),'target':seed['target_specification'],'explanation':'The auxiliary is finite and changes for person, number and tense. The accusative object ðæt hūs and uninflected participle geworht stay fixed. These are twelve indicative construction positions, not twelve additional inflectional forms.','alternatives':'The target requires the stated indicative positions and fixed object/participle. Other grammatical clauses or moods do not complete that requested table.','diagnosis':'Do not inflect the participle for person or number, replace the accusative object with a passive subject, or confuse a preterite auxiliary with a present auxiliary.','status':'complete_construction_model'}
models['models']=[existing[t['task_id']] for t in seeds]
(OUT/'author-only-model-seed.json').write_text(json.dumps(models,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'completed_morphology_tasks':6,'completed_construction_tasks':1,'inflectional_outputs':sum(len(existing['NEW-U12-'+code]['required_output_form_ids']) for code in groups),'construction_positions':12},ensure_ascii=False))
