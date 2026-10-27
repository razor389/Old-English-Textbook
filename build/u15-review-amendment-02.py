"""Apply the independently identified local-support repair after blind Git freeze."""
import hashlib
import json
from pathlib import Path

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,d): Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha('chapters/ch15/independent-solutions.md')=='2abad21bf90cf8994afbb7e48ec0807b74ab3d1e4cddf80cb30513845ca592fe'
c=read('chapters/ch15/coverage.json')
assert not any(a['amendment_id']=='U15-AM02' for a in c['amendments'])
sid='U15-H-29-09';tid='EX-IX-29-09'
text='Use the supplied frame ēow bið giefen, “it will be given to you (plural).” Ēow is the dative recipient; no hit is expressed. For one addressee, use ðē bið giefen with a singular command. Keep the frame available while composing; its independent recall is not required.'
ev=['U15-EX-P16','U15-G-FB94','U15-G-FB102','U07-C-187-188']
assert all(e in c['evidence_catalog'] for e in ev)
support={'support_id':sid,'feature_id':sid,'title':'Giving to a recipient without an expressed subject',
         'text':text,'bindings':[],'used_in_tasks':[tid],'evidence_refs':ev,
         'knowledge_status':'supplied','origin_category':'new teaching material',
         'evidence_basis':'Bounded new composition using the taught passive formation, dative recipient (Cook §164.a), implicit subject discussion (§190), and Cook29.9’s explicit omission instruction; not a claim that the whole model is an exact quoted Old English source sentence.',
         'display_required':True,'teaching_id':sid,'form_ids':[],'sense_ids':[],'feature_ids':[sid],
         'display_obligation':'Keep this exact construction help visible beside the assigned task and throughout assessment; do not require unaided recall.'}
t=next(t for t in c['assigned_items'] if t['task_id']==tid)
t['local_support'].append(support)
t['required_feature_ids'].append(sid);t['supplied_feature_ids'].append(sid)
t['output_positions'][0]['required_feature_ids'].append(sid)
t['canonical_review_resolution']={'amendment':'U15-AM02','finding':'U15-PAR-F01','scope':'The earlier audit closed the item without its impersonal-passive scaffold. The canonical task now supplies it explicitly; original audit observations remain unchanged.'}
c['grammar_inventory'].append({'feature_id':sid,'title':support['title'],'description':text,
    'scope_note':'Exact local recipient-passive frame for29.9; no new general independent production requirement.',
    'knowledge_status':'supplied','origin_category':'new teaching material','evidence_refs':ev,
    'teaching_ids':[sid],'used_in_tasks':[tid,sid],'assessed_in':[]})
c['teaching_records'].append({**support,'type':'supplied_support','graded':False})
group=next(t for t in c['teaching_records'] if t['teaching_id']=='NEW-U15-LOCAL-HELPS')
group['feature_ids'].append(sid)
group['evidence_refs']=sorted(set(group['evidence_refs']+ev))
c['record_counts_by_scope']['features']['supplied']+=1
c['record_identity_counts']['new_feature_ids']+=1
c['explicit_scope_metrics']['inventory_feature_entries']+=1
c['explicit_scope_metrics']['teaching_records']+=1
c['explicit_scope_metrics']['cook_help_groups']+=1
c['amendments'].append({'amendment_id':'U15-AM02','date':'2026-10-27','stage':'after blind witness checkpoint ecbdc44',
    'reason':'Independent paradigm review found a missing visible supplied construction in29.9 and four misleading key scope labels.',
    'changes':['Added exact local29.9 recipient-passive frame, bound supplied feature and actual teaching marker; original prompt/model unchanged.',
               'Key28.6 distinguishes familiar siextan from supplied nigoðan.',
               'Key29.11 identifies unne as the addressed subjunctive command already taught inUnit10.',
               'Keys30.3 and31.5 identify wishes/passive wishes already taught inUnit7.'],
    'affected_findings':['U15-PAR-F01','U15-PAR-F02','U15-PAR-F03','U15-PAR-F04','U15-PAR-F05'],
    'scope_metrics_after':{'teaching_records':596,'grammar_inventory_records':130,'cook_help_groups':36},
    'frozen_inputs':'Sealed source/grammar/design packets, initial masters at3822d4b and blind witness at ecbdc44 remain recoverable unchanged.',
    'review_status':'pending_independent_recheck'})
write('chapters/ch15/coverage.json',c)
p=Path('chapters/ch15/student.md');s=p.read_text(encoding='utf-8')
anchor='Give, and (om. it) shall be given you.\n\n<!-- output: EX-IX-29-09-O001 -->'
assert s.count(anchor)==1
replacement='Give, and (om. it) shall be given you.\n\n**Modern help — available throughout this item.**\n\n<!-- teaching: NEW-U15-LOCAL-HELPS -->\n\n<!-- teaching: '+sid+' -->\n\n<!-- support: '+sid+' -->\n\n'+text+'\n\n<!-- output: EX-IX-29-09-O001 -->'
p.write_text(s.replace(anchor,replacement),encoding='utf-8',newline='\n')
p=Path('chapters/ch15/answer-key.md');s=p.read_text(encoding='utf-8')
repairs={
    'the supplied ordinals **siextan/nigoðan** agree with feminine tīd':'familiar **siextan** and supplied **nigoðan** agree with feminine tīd',
    '**Unne** is a supplied second-singular present subjunctive used as a request.':'**Unne** is the second-singular present subjunctive used as an addressed request, as taught in Unit 10.',
    '**Sīe** is the supplied present subjunctive wish, “let your speech be …”.':'**Sīe** expresses the present subjunctive wish taught in Unit 7, “let your speech be …”.',
    '**Sīe … gehālgod** is the supplied passive wish, “may your name be hallowed”.':'**Sīe … gehālgod** combines the passive and independent wish taught in Unit 7: “may your name be hallowed”.'
}
for old,new in repairs.items():
    assert s.count(old)==1,old
    s=s.replace(old,new)
p.write_text(s,encoding='utf-8',newline='\n')
report={'amendment_id':'U15-AM02','blind_checkpoint':'ecbdc44','status':'applied_pending_independent_recheck',
        'findings':['U15-PAR-F0'+str(i) for i in range(1,6)],
        'primary_image_reinspection':[{'path':p,'raw_sha256':sha(p),'actually_viewed':True,'observer':'root','date':'2026-10-27','observation':note} for p,note in [
           ('sources/audits/unit15-grammar/fb-p94.png','§164.a gives the dative with giving/imparting; §164.h also records the dative recipient with requital.'),
           ('sources/audits/unit15-grammar/fb-p102.png','§189 note permits an unexpressed subject; §190 explains implied hit in impersonal constructions. This is construction evidence, not a quoted attestation of the new29.9 model.')]],
        'prior_teaching_rechecked':['chapters/ch10/student.md:997–1014, unne addressed subjunctive command and complete system.','chapters/ch07/student.md:246–262 and596–635, subjunctive and passive/participle systems.'],
        'witness_sha256_unchanged':sha('chapters/ch15/independent-solutions.md')}
write('sources/audits/unit15-coordinator/review-amendment-02.json',report)
print('Applied AM02:29.9 supplied frame,596 teaching records,130 features,36 Cook helps; four scope labels repaired. Witness unchanged.')
