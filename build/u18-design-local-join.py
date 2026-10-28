from pathlib import Path
import copy
import json
import unicodedata

O=Path('curriculum/proposals/unit18')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def norm(s):return unicodedata.normalize('NFC',s.strip('.,;:!?“”‘’\"()')).casefold()
inv=read(O/'inventory.json');lex=read('lexicon/entries.json');gram=read('curriculum/grammar.json')
local=read('sources/audits/unit18-source/local-support.json');choices=read(O/'author-only-nonverbal-selections.json')
models=read('sources/audits/unit18-grammar/candidate-models.json')['rows']
oldlemmas={l['lemma_id']:l for l in lex['lemmas']};lemmas={l['lemma_id']:l for l in inv['lemmas']}
oldforms={f['form_id']:(l['lemma_id'],f) for l in lex['lemmas'] for f in l['forms']};oldsenses={s['sense_id']:(l['lemma_id'],s) for l in lex['lemmas'] for s in l['senses']}
oldfeatures={f['feature_id']:f for f in gram['features']};issues=[]
source_aliases=[]
def prior(r):return {k:copy.deepcopy(r.get(k)) for k in ['knowledge_status','production_taught_in','recognition_taught_in','supplied_in','status','reviewed_in','coverage_contract']}
def lemma(lid,head,pos):
    if lid not in lemmas:
        old=oldlemmas.get(lid,{})
        lemmas[lid]={'lemma_id':lid,'display_headword':old.get('display_headword',head),'part_of_speech':old.get('part_of_speech',pos),'source_spellings':copy.deepcopy(old.get('source_spellings',[head])),'prior_lemma_present':bool(old),'forms':[],'senses':[],'evidence_refs':[]}
        inv['lemmas'].append(lemmas[lid])
    return lemmas[lid]
def teaching(t):
    existing=next((x for x in inv['teaching_records'] if x['teaching_id']==t['teaching_id']),None)
    if existing:
        for field in ['form_ids','sense_ids','feature_ids','source_items','evidence_refs']:
            if field in t:existing[field]=sorted(set(existing.get(field,[])+t[field]))
    else:inv['teaching_records'].append(t)
def add_form(lid,head,pos,r,tid):
    entity=lemma(lid,head,pos);r=copy.deepcopy(r);r['teaching_ids']=[tid]
    if r['form_id'] in oldforms:
        owner,old=oldforms[r['form_id']];assert owner==lid,(owner,lid)
        assert norm(old['form'])==norm(r['form']),(r,old)
        r['contextual_analysis']=copy.deepcopy(r['analysis']);r['analysis']=copy.deepcopy(old['analysis']);r['form']=old['form'];r['prior_scope']=prior(old)
        r['knowledge_status']='previously_taught' if old.get('production_taught_in') else r['knowledge_status']
        r['prior_metadata_preservation']='Preserve original surface, analysis and all chapter histories; current context and scope are additive.'
    else:r.setdefault('contextual_analysis',copy.deepcopy(r['analysis']));r['prior_scope']=None
    existing=next((f for f in entity['forms'] if f['form_id']==r['form_id']),None)
    if existing:
        assert existing['form']==r['form'],r['form_id']
        existing['evidence_refs']=sorted(set(existing.get('evidence_refs',[])+r.get('evidence_refs',[])))
        existing.setdefault('additional_contexts',[]).append({'analysis':r.get('contextual_analysis',r['analysis']),'teaching_id':tid,'scope_note':r.get('scope_note')})
    else:entity['forms'].append(r)
    entity['evidence_refs']=sorted(set(entity['evidence_refs']+r.get('evidence_refs',[])))
    return r
def add_sense(lid,head,pos,r,tid):
    entity=lemma(lid,head,pos);r=copy.deepcopy(r);r['teaching_ids']=[tid]
    if r['sense_id'] in oldsenses:
        owner,old=oldsenses[r['sense_id']];assert owner==lid,(owner,lid,r['sense_id'])
        r['contextual_gloss']=r['gloss'];r['gloss']=old['gloss'];r['prior_scope']=prior(old)
        r['knowledge_status']='previously_taught' if old.get('production_taught_in') else r['knowledge_status']
    else:r['prior_scope']=None
    existing=next((s for s in entity['senses'] if s['sense_id']==r['sense_id']),None)
    if existing:
        existing['evidence_refs']=sorted(set(existing.get('evidence_refs',[])+r.get('evidence_refs',[])))
        existing.setdefault('additional_contexts',[]).append({'gloss':r.get('contextual_gloss',r['gloss']),'scope_note':r.get('scope_note'),'teaching_id':tid})
    else:entity['senses'].append(r)
    return r
def feature(fid,description,items,ev,span=None,status='supplied',**extra):
    tid='NEW-U18-GRAM-'+fid.upper();r={'feature_id':fid,'description':description,'label':description.split('.')[0],'knowledge_status':status,'teaching_ids':[tid],'source_items':items,'evidence_refs':ev,'scope_note':'Only the explicitly bounded current context; supplied components have no independent recall assessment.',**extra}
    if span:r.update(support_span=span,whole_frame_analysis=description)
    if fid in oldfeatures:
        r['contextual_description']=description;r['description']=oldfeatures[fid].get('description');r['prior_scope']=prior(oldfeatures[fid])
    assert not any(x['feature_id']==fid for x in inv['features']),fid
    inv['features'].append(r);teaching({'teaching_id':tid,'kind':'supplied_whole_frame' if status=='supplied' else 'bounded_construction' if status=='new_production' else 'bounded_interpretation','feature_ids':[fid],'description':description,'knowledge_status':status,'support_span':span,'source_items':items,'evidence_refs':ev,'lesson_placement':'Before the first task using this support, with help remaining visible during the task.'})

for raw in local['forms']:
    r=copy.deepcopy(raw);lid=r['lemma_id'];tid=r['support_id']
    add_form(lid,r['headword'],r['part_of_speech'],{'form_id':r['form_id'],'form':r['form'],'analysis':r['analysis'],'knowledge_status':r['knowledge_status'],'evidence_refs':r['evidence_refs'],'scope_note':r['scope_note'],'source_items':r['source_items']},tid)
    add_sense(lid,r['headword'],r['part_of_speech'],{'sense_id':r['sense_id'],'gloss':r['gloss'],'knowledge_status':r['sense_knowledge_status'],'evidence_refs':r['evidence_refs'],'scope_note':r['scope_note'],'source_items':r['source_items']},tid)
    teaching({'teaching_id':tid,'kind':'visible_local_lexical_help','form_ids':[r['form_id']],'sense_ids':[r['sense_id']],'source_items':r['source_items'],'evidence_refs':r['evidence_refs'],'knowledge_status':'supplied','description':r['help_text'],'scope_note':r['scope_note'],'lesson_placement':'Print immediately with each named task or reading occurrence; no independent recall.'})
for m in models:
    short='.'.join(str(int(x)) for x in m['source_item_id'].split('-')[-2:])
    for i,w in enumerate(m['model'].split(),1):
        matches=[r for r in local['forms'] if short in r['source_items'] and norm(r['form'])==norm(w)]
        if len(matches)==1:
            r=matches[0];choices['rows'][short].setdefault('forms',{})[str(i)]=r['form_id'];choices['rows'][short].setdefault('senses',{})[str(i)]=r['sense_id'];choices['rows'][short].setdefault('contexts',{})[str(i)]=r['analysis']
        elif len(matches)>1:issues.append({'kind':'multiple_local_occurrence_candidates','item':short,'position':i,'form_ids':[x['form_id'] for x in matches]})

for r in local.get('reading_phrase_support',[]):
    if not r.get('source_items'):continue
    feature(r['support_id'],r['help_text'],r['source_items'],r['evidence_refs'],r['phrase'].replace(' / ','; '))
inv['lexical_frames']+=copy.deepcopy([f for f in inv['features'] if f.get('support_span') and f not in inv['lexical_frames']])
inv['unresolved_integration']=[x for x in inv.get('unresolved_integration',[]) if not isinstance(x,str)]+issues
inv['source_proposal_identity_reconciliation']=source_aliases
save(O/'inventory.json',inv);save(O/'author-only-nonverbal-selections.json',choices)
save(O/'local-support-bindings.json',{'schema_version':1,'source':'sources/audits/unit18-source/local-support.json','source_support_ids':[r['support_id'] for r in local['forms']],'identity_reconciliation':source_aliases,'unresolved':issues})
print(json.dumps({'local_forms':len(local['forms']),'lemmas':len(inv['lemmas']),'issues':issues},ensure_ascii=False,indent=2))
