"""Bind public inputs and privately selected outputs to individually resolved records."""
from pathlib import Path
import copy, json
ROOT = Path.cwd()
OUT = ROOT / 'curriculum/proposals/unit13'
def load(path): return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))
def save(name,value): (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def prior_state(r): return 'previously_taught' if r.get('production_taught_in') else 'previously_recognition' if r.get('recognition_taught_in') else 'previously_supplied'

lemmas={};forms={};senses={};prior_forms={};prior_senses={}
for path in ['lexicon/entries.json','sources/audits/unit13-source/lexical-inventory.json','sources/audits/unit13-grammar/grammar-records.json']:
    if not (ROOT/path).exists(): continue
    for lemma in load(path).get('lemmas',[]):
        lid=lemma['lemma_id']; old=lemmas.get(lid,{})
        merged={**copy.deepcopy(old),**copy.deepcopy(lemma)}
        for kind,key,destination,baseline in [('forms','form_id',forms,prior_forms),('senses','sense_id',senses,prior_senses)]:
            records={x[key]:copy.deepcopy(x) for x in old.get(kind,[])}
            for record in lemma.get(kind,[]):
                rid=record[key]; r=copy.deepcopy(record)
                if path=='lexicon/entries.json': baseline[rid]=copy.deepcopy(record)
                state=prior_state(record) if path=='lexicon/entries.json' else record.get('knowledge_status','unresolved')
                if rid in baseline and baseline[rid].get('production_taught_in'): state='previously_taught'
                records[rid]=r; destination[rid]={**r,'lemma_id':lid,'resolved_status':state}
            merged[kind]=list(records.values())
        lemmas[lid]=merged

ALIASES={
 '@when':'tha-conjunction-invariant|tha-when', '@then':'tha-adverb-invariant|tha-adverb-1',
 '@mid':'mid-invariant-source|mid-accompaniment-source', '@midconv':'mid-invariant-source|mid-u13-interlocutor',
 '@to':'to-preposition-dative-invariant|to-destination', '@there':'thaer-invariant-source|thaer-there',
 '@again':'eft-invariant|eft-u13-again-back', '@my':'min-poss-nom-m-pl-strong',
 '@brothers-nom':'brothor-nom-pl','@brothers-acc':'brothor-acc-pl','@brothers-dat':'brothor-dat-pl',
 '@friends-nom':'freond-nom-pl', '@lead-command':'laedan-imp-2-sg|laedan-u13-bring', '@speak-inf':'sprecan-infinitive-citation|sprecan-u13-converse',
}
DEFAULT_SENSE={'se':'se-the','wesan':'wesan-be','he':'he-1','ic':'ic-personal','thu':'thu-personal','cuman':'cuman-come','sellan':'sellan-give','on':'on-1','thaet-conjunction':'thaet-conjunction-1','habban':'habban-1','secgan':'secgan-content','hieran':'hieran-1','gretan':'gretan-take-leave'}

E={
'01':'se-m-nom-sg munuc-nom-sg hieran-pret-3-sg se-m-acc-sg sang-acc-sg',
'02':'se-m-acc-sg sang-acc-sg hieran-pret-3-sg se-m-nom-sg munuc-nom-sg',
'03':'@then hieran-pret-3-sg se-m-nom-sg munuc-nom-sg se-m-acc-sg sang-acc-sg',
'04':'@when he-m-nom-sg se-m-acc-sg sang-acc-sg hieran-pret-3-sg @then gan-pret-3-sg he-m-nom-sg @to se-m-dat-sg bisceop-dat-sg',
'05':'se-m-nom-sg sang-nom-sg wesan-pret-3-sg swete-nom-m-sg-strong he-m-nom-sg wesan-pret-3-sg eac-invariant wynsum-nom-m-sg-strong',
'06':'se-m-nom-sg bisceop-nom-sg geseon-pret-3-sg se-m-acc-sg munuc-acc-sg and-invariant gretan-pret-3-sg he-m-acc-sg',
'07':'se-m-nom-sg bisceop-nom-sg geseon-pret-3-sg se-m-acc-sg munuc-acc-sg he-m-nom-sg wesan-pret-3-sg on-invariant se-n-dat-sg hus-dat-sg-source',
'08':'se-m-nom-sg bisceop-nom-sg cwethan-pret-3-sg ic-nom-sg willan-pres-1-sg @midconv thu-dat-pl @speak-inf',
'09':'se-m-nom-sg munuc-nom-sg the-relative-invariant se-m-nom-sg bisceop-nom-sg gretan-pret-3-sg gan-pret-3-sg @to se-f-dat-sg cirice-dat-sg',
'10':'@when se-m-nom-sg bisceop-nom-sg cuman-pret-3-sg @then singan-pret-3-pl se-all-nom-pl @brothers-nom',
'11':'se-m-nom-sg bisceop-nom-sg wesan-pret-3-sg on-invariant se-n-dat-sg hus-dat-sg-source and-invariant se-m-nom-sg munuc-nom-sg on-invariant se-f-dat-sg cirice-dat-sg',
'12':'he-m-nom-sg secgan-pret-3-sg thaet-conjunction-invariant se-m-nom-sg sang-nom-sg swete-nom-m-sg-strong wesan-preterite-subj-3-sg',
}
A={
'A01':['se-m-nom-sg bisceop-nom-sg gretan-pret-3-sg se-m-acc-sg munuc-acc-sg','se-m-acc-sg munuc-acc-sg gretan-pret-3-sg se-m-nom-sg bisceop-nom-sg'],
'A02':['@when se-m-nom-sg munuc-nom-sg cuman-pret-3-sg @then gretan-pret-3-sg se-m-nom-sg bisceop-nom-sg se-all-acc-pl @brothers-acc'],
'A03':['se-m-nom-sg bisceop-nom-sg the-relative-invariant se-m-nom-sg munuc-nom-sg gretan-pret-3-sg sittan-pret-3-sg on-invariant se-n-dat-sg hus-dat-sg-source'],
'A04':['se-m-nom-sg munuc-nom-sg gretan-pret-3-sg se-m-acc-sg bisceop-acc-sg and-invariant sellan-pret-3-sg he-m-dat-sg se-m-acc-sg mete-acc-sg'],
'A05':['se-m-nom-sg sang-nom-sg wesan-pret-3-sg swete-nom-m-sg-strong he-m-nom-sg wesan-pret-3-sg wynsum-nom-m-sg-strong','se-m-nom-sg bisceop-nom-sg cuman-pret-3-sg he-m-nom-sg wesan-pret-3-sg on-invariant se-n-dat-sg hus-dat-sg-source'],
'A06':['se-m-nom-sg bisceop-nom-sg geseon-pret-3-sg se-m-acc-sg munuc-acc-sg he-m-nom-sg sittan-pret-3-sg on-invariant se-n-dat-sg hus-dat-sg-source'],
'A07':['se-m-nom-sg munuc-nom-sg cwethan-pret-3-sg ic-nom-sg hieran-pret-1-sg se-m-acc-sg sang-acc-sg hieran-pret-2-sg thu-nom-sg he-m-acc-sg'],
'A08':['se-m-nom-sg munuc-nom-sg secgan-pret-3-sg thaet-conjunction-invariant he-m-nom-sg on-invariant se-n-dat-sg hus-dat-sg-source wesan-preterite-subj-3-sg'],
'A09':['se-m-nom-sg bisceop-nom-sg wesan-pret-3-sg on-invariant se-f-dat-sg cirice-dat-sg and-invariant se-all-nom-pl @brothers-nom on-invariant se-n-dat-sg hus-dat-sg-source'],
'A10':['on-invariant se-n-dat-sg hus-dat-sg-source sittan-pret-3-sg se-m-nom-sg munuc-nom-sg','@when se-m-nom-sg munuc-nom-sg on-invariant se-n-dat-sg hus-dat-sg-source sittan-pret-3-sg @then cuman-pret-3-sg se-m-nom-sg bisceop-nom-sg'],
'A11':['@when se-m-nom-sg munuc-nom-sg the-relative-invariant se-m-nom-sg bisceop-nom-sg gretan-pret-3-sg cuman-pret-3-sg @then singan-pret-3-pl se-all-nom-pl @brothers-nom'],
}
READ='''se-m-nom-sg bisceop-nom-sg sittan-pret-3-sg on-invariant se-n-dat-sg hus-dat-sg-source and-invariant se-m-nom-sg munuc-nom-sg wesan-pret-3-sg @there
@when se-m-nom-sg munuc-nom-sg se-m-acc-sg sang-acc-sg hieran-pret-3-sg @then gan-pret-3-sg he-m-nom-sg @to se-m-dat-sg bisceop-dat-sg
se-m-nom-sg munuc-nom-sg cwethan-pret-3-sg ic-nom-sg hieran-pret-1-sg se-m-acc-sg sang-acc-sg the-relative-invariant swithe-positive wynsum-nom-m-sg-strong wesan-pret-3-sg hieran-pret-2-sg thu-nom-sg he-m-acc-sg
se-m-nom-sg bisceop-nom-sg cwethan-pret-3-sg gan-imp-2-sg nu-invariant and-invariant @lead-command se-all-acc-pl @brothers-acc hider-invariant-source
@then gan-pret-3-sg se-m-nom-sg munuc-nom-sg @to se-f-dat-sg cirice-dat-sg and-invariant cuman-pret-3-sg @again @mid se-all-dat-pl @brothers-dat
se-m-nom-sg bisceop-nom-sg geseon-pret-3-sg he-acc-pl and-invariant cwethan-pret-3-sg thu-nom-pl wesan-pres-2-pl @my @friends-nom ic-nom-sg willan-pres-1-sg @midconv thu-dat-pl @speak-inf
se-m-nom-sg munuc-nom-sg sittan-pret-3-sg @mid se-all-dat-pl @brothers-dat and-invariant he-nom-pl hieran-pret-3-pl se-m-gen-sg bisceop-gen-sg word-acc-pl'''

# Private ordered output strings stay in the author-only file, not the public task plan.
PRIVATE={
'A06':[
 ('Se bisceop sæt on ðǣm hūse.','se-m-nom-sg bisceop-nom-sg sittan-pret-3-sg on-invariant se-n-dat-sg hus-dat-sg-source'),
 ('Se munuc sæt on ðǣm hūse.','se-m-nom-sg munuc-nom-sg sittan-pret-3-sg on-invariant se-n-dat-sg hus-dat-sg-source')],
'A09':[('Ðā brōðor wǣron on ðǣm hūse.','se-all-nom-pl @brothers-nom wesan-pret-3-pl on-invariant se-n-dat-sg hus-dat-sg-source')],
'C01':[
 ('Ðā brōðor hīerdon ðone sang.','se-all-nom-pl @brothers-nom hieran-pret-3-pl se-m-acc-sg sang-acc-sg'),
 ('Ðone sang hīerdon ðā brōðor.','se-m-acc-sg sang-acc-sg hieran-pret-3-pl se-all-nom-pl @brothers-nom')],
'C02':[('Ðā grētte se bisceop ðā brōðor.','@then gretan-pret-3-sg se-m-nom-sg bisceop-nom-sg se-all-acc-pl @brothers-acc')],
'C03':[('Ðā ðā brōðor cōmon, ðā sang se bisceop.','@when se-all-nom-pl @brothers-nom cuman-pret-3-pl-source @then singan-pret-3-sg se-m-nom-sg bisceop-nom-sg')],
'C04':[('Ðā brōðor, ðe se bisceop grētte, ēodon tō ðǣre cirican.','se-all-nom-pl @brothers-nom the-relative-invariant se-m-nom-sg bisceop-nom-sg gretan-pret-3-sg gan-pret-3-pl @to se-f-dat-sg cirice-dat-sg')],
'C05':[('Se bisceop grētte ðone munuc. Ðā ēode se munuc tō ðǣre cirican.','se-m-nom-sg bisceop-nom-sg gretan-pret-3-sg se-m-acc-sg munuc-acc-sg @then gan-pret-3-sg se-m-nom-sg munuc-nom-sg @to se-f-dat-sg cirice-dat-sg')],
'C06':[('Se munuc cwæð: “Ic wille mid ēow sprecan.”','se-m-nom-sg munuc-nom-sg cwethan-pret-3-sg ic-nom-sg willan-pres-1-sg @midconv thu-dat-pl @speak-inf')],
'C07':[('Se munuc geseah ðone bisceop and grētte hine.','se-m-nom-sg munuc-nom-sg geseon-pret-3-sg se-m-acc-sg bisceop-acc-sg and-invariant gretan-pret-3-sg he-m-acc-sg')],
'C08':[('Ðā se bisceop, ðe se munuc grētte, cōm, ðā sungon ðā brōðor.','@when se-m-nom-sg bisceop-nom-sg the-relative-invariant se-m-nom-sg munuc-nom-sg gretan-pret-3-sg cuman-pret-3-sg @then singan-pret-3-pl se-all-nom-pl @brothers-nom')],
}

issues=[]
def sequence(seqid,text,spec,owner,kind):
    words=text.split();refs=spec.split()
    if len(words)!=len(refs):
        issues.append(dict(sequence_id=seqid,error='token_count',words=len(words),bindings=len(refs)))
        return None
    tokens=[]
    for i,(literal,ref) in enumerate(zip(words,refs),1):
        ref=ALIASES.get(ref,ref); fid,*tail=ref.split('|'); f=forms.get(fid)
        if not f:
            issues.append(dict(sequence_id=seqid,token_index=i,literal=literal,missing_form_id=fid));continue
        lid=f['lemma_id'];sid=tail[0] if tail else DEFAULT_SENSE.get(lid)
        if sid is None: sid=lemmas[lid]['senses'][0]['sense_id']
        s=senses.get(sid);clean=literal.strip('.,:;!?“”"()[]')
        if clean.casefold()!=f['form'].casefold(): issues.append(dict(sequence_id=seqid,token_index=i,error='surface_mismatch',literal=literal,form_id=fid,registered=f['form']))
        if not s or s['lemma_id']!=lid:
            issues.append(dict(sequence_id=seqid,token_index=i,error='sense_identity',sense_id=sid,lemma_id=lid));continue
        tokens.append(dict(token_index=i,literal=literal,surface=clean,lemma_id=lid,form_id=fid,sense_id=sid,form=f['form'],analysis=f['analysis'],form_status=f['resolved_status'],sense_status=s['resolved_status']))
    return dict(sequence_id=seqid,owner_id=owner,kind=kind,text=text,tokens=tokens,required_form_ids=sorted({t['form_id'] for t in tokens}),required_sense_ids=sorted({t['sense_id'] for t in tokens}))

if __name__=='__main__':
    comps=load('curriculum/proposals/unit13/composition-seed.json');seed=load('curriculum/proposals/unit13/task-seed.json');public=[];private=[]
    for e in comps['teaching_examples']:
        if e['example_id'][-2:] not in E: continue
        s=sequence(e['example_id']+'-INPUT',e['text'],E[e['example_id'][-2:]],e['example_id'],'translated_teaching_example')
        if s:public.append(s)
    for t in seed['tasks']:
        for i,(text,spec) in enumerate(zip(t['input_texts'],A.get(t['task_id'].removeprefix('NEW-U13-'),[])),1):
            s=sequence(t['task_id']+f'-INPUT{i}',text,spec,t['task_id'],'graded_public_input')
            if s:public.append(s)
    r=comps['new_reading'];s=sequence(r['span_id']+'-INPUT',r['text'],READ,r['span_id'],'controlled_connected_reading')
    if s:public.append(s)
    public_issues=copy.deepcopy(issues);issues.clear()
    for code,pairs in PRIVATE.items():
        for i,(text,spec) in enumerate(pairs,1):
            owner='NEW-U13-'+code;s=sequence(owner+f'-OUTPUT{i}',text,spec,owner,'required_old_english_output')
            if s:private.append(s)
    save('public-sequence-bindings.json',dict(schema_version=1,chapter='ch13',status='closed' if not public_issues else 'pending_audit_records',sequences=public,issues=public_issues))
    save('author-only-sequence-bindings.json',dict(schema_version=1,chapter='ch13',status='closed' if not issues else 'pending_audit_records',private=True,pre_key_excluded=True,sequences=private,issues=issues))
    print(json.dumps(dict(public_sequences=len(public),public_tokens=sum(len(s['tokens']) for s in public),public_issues=len(public_issues),private_sequences=len(private),private_issues=len(issues),issues_sample=(public_issues+issues)[:15]),ensure_ascii=False))
