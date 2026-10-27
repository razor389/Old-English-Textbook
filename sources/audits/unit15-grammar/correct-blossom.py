from pathlib import Path
import json,hashlib
O=Path(__file__).resolve().parent;R=O.parents[2]
for n in ['build-lexical.py','build-models.py']:
 p=O/n;t=p.read_text(encoding='utf-8')
 t=t.replace('blostnian','blostmian').replace('blōstnian','blōstmian').replace('blōstnode','blōstmode').replace('blōstnod','blōstmod')
 t=t.replace('Cook’s printed blōstmian is retained literally; its paired infinitives are blōstmian/blōstmianne, not a silently corrected blōstmian.','The original600dpi prompt reads blōstmian; the earlier audit reading blōstnian was mistaken. The complete selected pair is blōstmian/blōstmianne; no finite system is assigned.')
 t=t.replace('blōstnianne','blōstmianne')
 p.write_text(t,encoding='utf-8')
p=R/'sources/audits/unit15-coordinator/cook-ex17-600.png'
(O/'transcription-corrections.json').write_text(json.dumps({'schema_version':1,'corrections':[{'item_id':'EX-IX-30-11','earlier_auditor_reading':'blōstnian','correct_source_reading':'blōstmian','kind':'auditor_transcription_error_corrected','basis':'Personally viewed original600dpi image: m has two humps. This is not an error attributed to Cook and not a normalization away from the printed prompt.','image_path':str(p.relative_to(R)).replace('\\','/'),'image_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'identifier_replacement':'blostnian-* -> blostmian-*; no former n-form was integrated into the active registers.'}]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
