"""Public construction positions bind ordinary records, never invented compound forms."""
from pathlib import Path
import importlib.util,json
ROOT=Path.cwd();OUT=ROOT/'curriculum/proposals/unit12'
spec=importlib.util.spec_from_file_location('u12_bindings',Path(__file__).with_name('public_bindings.py'))
B=importlib.util.module_from_spec(spec);spec.loader.exec_module(B)
subjects={('sg',1):'ic-nom-sg',('sg',2):'thu-nom-sg',('sg',3):'he-m-nom-sg',('pl',1):'ic-nom-pl',('pl',2):'thu-nom-pl',('pl',3):'he-nom-pl'}
english_subjects={('sg',1):'I',('sg',2):'You',('sg',3):'He',('pl',1):'We',('pl',2):'You',('pl',3):'They'}
positions=[]
for number in ['sg','pl']:
 for person in [1,2,3]:
  for tense,short in [('present','pres'),('preterite','pret')]:
   aid=f'habban-{short}-{person}-{number}'
   fids=[subjects[(number,person)],aid,'se-n-acc-sg','hus-acc-sg','gewyrcean-past-participle']
   text=' '.join(B.forms[f]['form'] for f in fids);text=text[0].upper()+text[1:]+'.'
   refs=' '.join(f+'|habban-perfect' if f==aid else f for f in fids)
   ident=f'NEW-U12-HABBAN-PERFECT-IND-{short.upper()}-{person}-{number.upper()}'
   sequence=B.make_sequence(ident,text,refs,'NEW-U12-HABBAN-PERFECT-IND','translated_construction_position')
   english_auxiliary='had' if tense=='preterite' else 'has' if (number,person)==('sg',3) else 'have'
   translation=english_subjects[(number,person)]+' '+english_auxiliary+' built the house.'
   positions.append({'position_id':ident,'mood':'indicative','tense':tense,'person':person,'number':number,'auxiliary_form_id':aid,'fixed_object_form_ids':['se-n-acc-sg','hus-acc-sg'],'participle_form_id':'gewyrcean-past-participle','text':text,'translation':translation,'sequence':sequence})
rows=[]
for number in ['sg','pl']:
 for person in [1,2,3]:
  selected=[p for p in positions if p['person']==person and p['number']==number]
  rows.append([str(person)+' '+('singular' if number=='sg' else 'plural')]+[p['text'] for p in selected])
data={'schema_version':1,'chapter':'ch12','status':'closed' if not B.issues else 'pending_audit_records','patterns':[{'pattern_id':'NEW-U12-HABBAN-PERFECT-IND','title':'Habban + object + past participle: present and preterite indicative','construction_feature_ids':['u12-habban-perfect'],'knowledge_status':'new_production','positions':positions,'headers':['Person / number','Present indicative','Preterite indicative'],'rows':rows,'position_count':12,'new_inflectional_cell_count':0,'scope_note':'These are twelve construction positions, assembled from previously taught indicative auxiliary forms and the newly assigned perfect construction. They are not twelve new inflected words and do not exhaust all moods. The object is accusative; this bounded production pattern uses the uninflected past-participle base.','reported_subjunctive_extension':{'text':'Reported anterior action can use the previously taught preterite subjunctive of habban in this newly taught compound construction. In hē … geworht hæfde, hæfde is assigned as the subjunctive form required by the reported-statement target; its surface is identical to first- and third-person singular indicative hæfde.','auxiliary_form_id':'habban-preterite-subj-3-sg','auxiliary_sense_id':'habban-perfect','feature_ids':['u09-reported-statement','u12-reported-sequence','u12-habban-perfect']}}],'issues':B.issues}
(OUT/'construction-patterns.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'positions':len(positions),'issues':B.issues},ensure_ascii=False))
