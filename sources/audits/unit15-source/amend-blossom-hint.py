"""Narrow repair after personal600dpi source reinspection; not a Cook erratum."""
import json,pathlib
P=pathlib.Path(__file__).parent
def read(n):return json.loads((P/n).read_text(encoding='utf8'))
def dump(n,x):(P/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
j=read('exercises-prompts.json');item=next(x for x in j['items'] if x['source_item_id']=='EX-IX-30-11')
assert 'blōstnian, 118' in item['prompt'] or 'blōstmian, 118' in item['prompt']
item['prompt']=item['prompt'].replace('blōstnian, 118','blōstmian, 118')
j['verification']='All four selected page images personally inspected first at structural resolution, then against fresh220dpi renders. Exercise30.11 separately reinspected in the actual600dpi page, confirming blōstmian and withdrawing our earlier n reading. Original wording, hints, numbering and joint X, XI heading retained.'
dump('exercises-prompts.json',j)
j=read('source-change-notes.json');c=next(x for x in j['changes'] if x['change_id']=='U15-CN03')
if 'superseded_audit_reading' not in c:c['superseded_audit_reading']=dict(reading='blōstnian(118), with n',description=c['description'],status='withdrawn by U15-CN10; preserved as audit history, not a source variant')
c['description']='The printed blossom hint is blōstmian(118), with m, confirmed by personal600dpi reinspection under U15-CN10. The earlier n judgment is retained below as superseded audit history. The age prompt reads twelve(155) years(154.c) old. No Cook error or source-word emendation is asserted.'
if not any(x['change_id']=='U15-CN10' for x in j['changes']):j['changes'].append(dict(change_id='U15-CN10',category='correction_of_our_audit_not_source_error',affected=['EX-IX-30-11','exercises-prompts.json','exercises-dependencies.json','cook-local-support.json'],supersedes='U15-CN03 earlier n judgment',previous_audit_reading='blōstnian',confirmed_printed_reading='blōstmian',description='The source editor personally viewed the actual Cook printed17/PDF25 page rendered at600dpi, using original image detail. The glyph after t has the two arches of m. The earlier n endorsement, including the fresh220dpi judgment, was wrong and is explicitly withdrawn. Repair only the transcription and dependent hint explanations. This is not a demonstrated Cook error, an inferred variant, or a change of the printed source.',evidence_refs=['U15-EX-P17'],image='sources/audits/unit15-source/exercise-p17-600.png',render_origin='sources/audits/unit15-coordinator/cook-ex17-600.png',inspection_agent='unit15_source'))
dump('source-change-notes.json',j)
p=P/'build-evidence.py';s=p.read_text(encoding='utf8');s=s.replace('30.11 blōstnian,','30.11 blōstmian (m confirmed by personal600dpi reinspection; earlier n audit withdrawn),');p.write_text(s,encoding='utf8')
p=P/'README.md';s=p.read_text(encoding='utf8');s=s.replace('the30.11 hint remains “blōstnian.”','the30.11 hint is “blōstmian,” confirmed by personal600dpi reinspection. The earlier “blōstnian” judgment is preserved and withdrawn in U15-CN10.');s=s.replace('passes35 checks','passes36 checks');p.write_text(s,encoding='utf8')
print(dict(source_item_id=item['source_item_id'],confirmed='blōstmian',history='U15-CN03 superseded reading and U15-CN10'))
