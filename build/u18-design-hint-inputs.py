from pathlib import Path
from collections import defaultdict
import copy
import hashlib
import json
import re
import unicodedata

OUT=Path('curriculum/proposals/unit18')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def norm(s):return unicodedata.normalize('NFC',s).casefold()
lex=read('lexicon/entries.json');inv=read(OUT/'inventory.json')
lemmas={l['lemma_id']:l for l in lex['lemmas']}
form_ids={f['form_id']:(l['lemma_id'],f) for l in lex['lemmas'] for f in l['forms']}
for l in inv['lemmas']:
    lemmas[l['lemma_id']]=l;form_ids.update({f['form_id']:(l['lemma_id'],f) for f in l['forms']})
headwords=defaultdict(set)
for l in lex['lemmas']+inv['lemmas']:
    for head in [l.get('display_headword','')]+l.get('source_spellings',[]):
        if isinstance(head,str):headwords[norm(head)].add(l['lemma_id'])
for p in inv['paradigms']:headwords[norm(p.get('headword',''))].add(p['lemma_id'])
models={s['owner_id']:s for s in read(OUT/'author-only-cook-sequence-bindings.json')['sequences']}
source=read('sources/audits/unit18-source/exercises-prompts.json')
prompts={r['source_item_id']:r for r in source['items']}
controls=read(OUT/'input-reference-records.json')['records']
aliases={'sęcgean':'secgan','sęcgan':'secgan','mugan':'magan','ofslēan':'ofslean','ðā':'tha-conjunction','Iacob':'iacob','Iudas':'iudas','Iosep':'iosep','beðurfan':'bethurfan','foresęcgean':'foresecgean','lęcgean':'lecgean','ęrian':'erian','clēopian':'cleopian','ðēow':'theow-servant','weorð':'weorth-price'}
per_item={}
records=[];sequences=[];hint_lemmas={};pending=[]
def slug(s):
    t=s.translate(str.maketrans({'æ':'ae','ǣ':'ae','ð':'th','þ':'th','ę':'e','œ':'oe'}))
    return ''.join(c for c in unicodedata.normalize('NFD',t).casefold() if unicodedata.category(c)!='Mn')
def hint_token(refid,tid,index,word,lid,sid):
    matching=[(fid,f) for fid,(owner,f) in form_ids.items() if owner==lid and norm(f['form'])==norm(word)]
    model_ids={t.get('form_id') for t in models[tid]['tokens'] if t.get('lemma_id')==lid and norm(t.get('surface',''))==norm(word)}
    matching_model=[(fid,f) for fid,f in matching if fid in model_ids]
    selected=matching_model[0] if len(matching_model)==1 else matching[0] if len(matching)==1 else None
    if selected is None:
        canonical=[]
        for fid,f in matching:
            a=f.get('contextual_analysis',f.get('analysis',{}))
            if not isinstance(a,dict):continue
            if a.get('case') in ['nom','nominative'] and a.get('number') in ['sg','singular'] and a.get('gender') in ['m','masculine',None] and a.get('declension',a.get('strength')) in [None,'strong']:canonical.append((fid,f))
            elif any('infinitive' in str(a.get(key,'')) for key in ['nonfinite','verb_form']):canonical.append((fid,f))
        if len(canonical)==1:selected=canonical[0]
    if selected:
        fid,f=selected
        return {'token_index':index,'literal':word,'surface':word,'lemma_id':lid,'form_id':fid,'sense_id':sid,'analysis':copy.deepcopy(f['analysis']),
            'contextual_analysis':{'function':'exact_source_hint_reference','independent_syntactic_use':False},
            'form_status':'previously_taught' if f.get('production_taught_in') else f.get('knowledge_status','supplied'),
            'reference_position_status':'supplied','sense_status':'visible_reference_meaning','assessment_role':'visible_reference_position','independent_recall_assessment':False}
    fid=lid+'-u18-hint-reference-'+hashlib.sha256(word.encode()).hexdigest()[:8]
    lemma=hint_lemmas.setdefault(lid,{'lemma_id':lid,'display_headword':lemmas.get(lid,{}).get('display_headword',word),'part_of_speech':lemmas.get(lid,{}).get('part_of_speech','reference_pending_classification'),'forms':[],'senses':[]})
    if not any(f['form_id']==fid for f in lemma['forms']):
        lemma['forms'].append({'form_id':fid,'form':word,'analysis':{'function':'exact_source_hint_reference','independent_syntactic_use':False},'knowledge_status':'supplied','teaching_ids':['NEW-U18-SOURCE-HINTS'],
            'evidence_refs':prompts[tid]['evidence_refs'],'scope_note':'Exact visible Cook hint string only. Its appearance supplies a reference position, not unaided recall or a new inflectional system.','source_hint_refs':[refid]})
    return {'token_index':index,'literal':word,'surface':word,'lemma_id':lid,'form_id':fid,'sense_id':sid,'analysis':{'function':'exact_source_hint_reference'},'form_status':'supplied','sense_status':'visible_supplied_reference_meaning','assessment_role':'visible_reference_position','independent_recall_assessment':False}
for original in controls:
    r=copy.deepcopy(original);tid=r['task_id'];inside=r['literal_source_text'][1:-1].strip();head=inside.split(',',1)[0].split(';',1)[0].strip()
    r['learner_visible_route']={'kind':'exact_prompt_span','task_id':tid,'character_start_zero_based':r['character_start_zero_based'],'character_end_exclusive':r['character_end_exclusive'],'literal':r['literal_source_text']}
    r['knowledge_status']='supplied';r['independent_recall_assessment']=False
    if r['literal_source_text'].startswith('['):r['role']='visible English target wording';r['required_form_ids']=[]
    elif inside in ['s','our','neut.'] or re.match(r'^(om\.|verb |preposition |plur\.|sing\.)',inside,re.I):r['role']='visible English omission, order, number or meaning instruction';r['required_form_ids']=[]
    elif re.match(r'^(?:p\.|\d)',inside):r['role']='visible original grammar/source locator';r['required_form_ids']=[];r['explanation_route']='sources/audits/unit18-grammar/numeric-control-analysis.json; join by original control before contract'
    else:
        head='ǣr' if inside.startswith('see ǣr') else head
        words=head.split();bound=[]
        for index,word in enumerate(words,1):
            lids=sorted(headwords[norm(word)])
            alias=aliases.get(word)
            if alias not in lemmas:alias=None
            lid=per_item.get((tid,head)) or alias or (lids[0] if len(lids)==1 else None)

            if not lid:
                candidates={t.get('lemma_id') for t in models[tid]['tokens'] if norm(t.get('surface',''))==norm(word) and t.get('lemma_id')}
                if len(candidates)==1:lid=next(iter(candidates))
            if not lid:
                pending.append({'reference_id':r['reference_id'],'kind':'headword_lemma','head':head,'word':word,'candidate_lemmas':lids});continue
            senses=sorted({t['sense_id'] for t in models[tid]['tokens'] if t.get('lemma_id')==lid and t.get('sense_id')})
            sid=senses[0] if len(senses)==1 else None

            if not sid:pending.append({'reference_id':r['reference_id'],'kind':'hint_sense','lemma_id':lid,'word':word,'candidate_senses':senses})
            bound.append(hint_token(r['reference_id'],tid,index,word,lid,sid))
        r['role']='visible exact Old English lexical or phrase hint';r['hint_text']=head
        r['required_form_ids']=[t['form_id'] for t in bound];r['required_sense_ids']=sorted({t['sense_id'] for t in bound if t.get('sense_id')})
        r['dependency_status']='bound' if len(bound)==len(words) and all(t.get('sense_id') for t in bound) else 'awaits_exact_hint_identity_join'
        if bound:
            seq={'sequence_id':r['reference_id']+'-INPUT','owner_id':tid,'kind':'visible_source_hint','text':head,'tokens':bound,'source_control_id':r['reference_id'],'independent_recall_assessment':False}
            sequences.append(seq);r['input_sequence_id']=seq['sequence_id']
    records.append(r)
result={'schema_version':1,'chapter':'ch18','status':'exact_source_controls_classified; pending_identity_join_explicit','records':records,'lemmas':list(hint_lemmas.values()),'features':[],
    'sequences':sequences,'unresolved':pending,'counts':{'original_controls':len(records),'hint_input_sequences':len(sequences),'hint_form_records':sum(len(l['forms']) for l in hint_lemmas.values()),'pending':len(pending)}}
(OUT/'source-hint-inventory.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result['counts'],indent=2));print(json.dumps(pending,ensure_ascii=False,indent=2))
