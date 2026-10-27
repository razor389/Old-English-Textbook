"""Retain primary evidence and the coordinator's explicit correction decisions."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'sources/audits/unit16-coordinator'
def read(path): return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))
def save(path,data): (ROOT/path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def evidence(path,source,page,pdf,identifier,observation):
    return {'path':path,'sha256':hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),
            'source_id':source,'printed_page':page,'pdf_page_one_based':pdf,
            'original_identifier':identifier,'inspector':'coordinator/root',
            'date':'2026-10-27','method':'Personally viewed through view_image',
            'observation':observation}

records=[
evidence('sources/audits/unit16-coordinator/bt_b0029.jpg','bosworth_toller_1898_1921',29,None,'Main29b: a-gildan; a-giltan',
         'Strong a-gildan/-geldan/-gieldan/-gyldan has geald/guldon/golden and includes reward, repay, requite. Separate weak a-giltan has gilte/gilt and means sin, fail, do wrong.'),
evidence('sources/audits/unit16-coordinator/bt_b0030.jpg','bosworth_toller_1898_1921',30,None,'Main30b: a-gyldan; a-gyltan',
         'a-gyldan expressly gives thu gyltst/he gylt and geald/guldon/golden. Dative recipients occur in repayment examples. Separate a-gyltan/-giltan has gylte/gilte and gylt/gilt, fail in duty or sin.'),
evidence('sources/audits/unit16-coordinator/cook-ex-p60-300.png','cook_ex_1895',60,68,'English–Old English vocabulary: reward; requite',
         'Reward is the noun med; requite is forgieldan(III.104). The vocabulary supplies no independent support for agyltan as the verb reward.'),
evidence('sources/audits/unit04-grammar/cook-p61-pdf77.png','cook_fb_1895_2',61,77,'104: strong class III',
         'Strong gieldan/geald/guldon/golden is explicitly tabulated under104. Prefixing does not turn this into weak class113.'),
evidence('sources/audits/unit02-grammar/cook-fb-p68.png','cook_fb_1895_2',68,84,'113: weak preterits in de/te',
         'Section113 describes weak de/te preterits retaining the stem vowel, with hieran, fyllan, cyssan, settan and sendan among its examples. It cannot describe strong gyldan/geald/guldon/golden.'),
evidence('sources/audits/unit02-grammar/cook-fb-p70.png','cook_fb_1895_2',70,86,'114–115',
         'Viewed while locating113; this page contains the end of114 and beginning of115. It is not cited as the page of113.'),
evidence('sources/audits/unit02-grammar/cook-fb-p71.png','cook_fb_1895_2',71,87,'115–117',
         'Viewed while locating113; this page contains115–117. It is not cited as the page of113.'),
evidence('sources/audits/unit16-grammar/ex-p63.png','cook_ex_1895',63,71,'English–Old English vocabulary: swim',
         'Personally inspected the vocabulary page in the Unit16 model audit; no reward correction is inferred from it.')]
prompts=read('sources/audits/unit16-source/exercises-prompts.json')['items']
original=next(x['prompt'] for x in prompts if x['source_item_id']=='EX-XII-XIII-34-09')
correction={
 'correction_id':'C06','chapter':'ch16','status':'demonstrated_source_hint_error',
 'affected_source_items':['EX-XII-XIII-34-09'],
 'source_id':'cook_ex_1895','printed_page':20,'pdf_page_one_based':28,
 'original_identifier':'XII,XIII.34.9','original_prompt':original,
 'original_hint':'reward (āgyltan, 113)',
 'corrected_guidance':'reward: āgyldan, strong class III (Cook104)',
 'origin_categories':{'original_prompt':'exact source','correction':'documented editorial correction','model':'new teaching material'},
 'decision':'The printed weak headword/class belong to a verb meaning sin or fail in duty. Repay/reward requires the distinct strong gyldan verb. The source English, original hint and original image are all retained; only modern guidance is corrected.',
 'selected_form':'āgylt','analysis':'third-person singular present indicative of strong āgyldan; a valid contracted form, not evidence for weak āgyltan',
 'selected_support':'ðonne āgylt hē ǣlcum be his āgnum weorce',
 'support_scope':'Supply this complete second clause with its dative recipient and phrase meaning. No new complete productive āgyldan paradigm is assigned. Other contracted forms displayed in Unit16 do not automatically teach this verb.',
 'typography':'The prefixed ā spelling follows the printed Cook hint. Dictionary entries are cited as printed with separated prefix; no silent claim of a different dictionary accent convention is made.',
 'historical_cause':'Not established; no conjecture about compositor, author or exemplar is required.',
 'evidence':records[:5],
 'original_image':'sources/audits/unit16-source/exercise-003.png',
 'review_requirement':'Fresh reviewer must distinguish valid strong āgylt from the erroneous weak infinitive/class, and independently check recipient government.',
 'registry_placement':'Separate own correction record; earlier sources/CORRECTIONS.md and all prior-unit artifacts remain unchanged.'}
save('sources/audits/unit16-coordinator/reward-correction.json',correction)
catalog={
 'U16-C06-REWARD':{'source_id':'cook_ex_1895','printed_page':20,'pdf_page_one_based':28,
 'original_identifier':'XII,XIII.34.9; correctionC06','origin_category':'documented editorial correction',
 'record':'sources/audits/unit16-coordinator/reward-correction.json',
 'image':'sources/audits/unit16-source/exercise-003.png',
 'image_sha256':hashlib.sha256((ROOT/'sources/audits/unit16-source/exercise-003.png').read_bytes()).hexdigest(),
 'personally_viewed':True,'inspection_scope':correction['decision'],'supporting_primary_evidence':records[:5]},
 'U16-LATIN-NOTE10':{'source_id':'cook_fb_1895_2','printed_page':169,'pdf_page_one_based':185,
 'original_identifier':'printed169 note10','origin_category':'modern English support for exact source apparatus',
 'image':'sources/audits/unit16-coordinator/cook-fb-p169-600.png',
 'image_sha256':hashlib.sha256((ROOT/'sources/audits/unit16-coordinator/cook-fb-p169-600.png').read_bytes()).hexdigest(),
 'personally_viewed':True,'inspection_scope':'Latin ceroma fricavit eum means rubbing/anointing him with ointment; the printed Latin contains no explicit shoulder or neck noun. Do not introduce either as a certain literal gloss.',
 'lexical_confirmation':{'url':'https://logeion.org/ceroma','source':'Lewis and Short, ceroma; Georges, ceroma','consulted':'2026-10-27','finding':'Ointment used by wrestlers; Georges includes feminine first-declension ceroma, ae and cites Historia Apollonii13.'},
 'teaching_boundary':'Supply an English sense of both Latin parallels; assume no prior Latin. Preserve Cook’s tentative ball interpretation of Old English top and its acknowledged divergence.'}}
save('sources/audits/unit16-coordinator/evidence-catalog.json',catalog)
ledger=read('sources/audits/unit16-coordinator/primary-inspections.json')
known={r['path'] for r in ledger['actual_inspections']}
ledger['actual_inspections']=[{**r,'source_id':'bosworth_toller_1898_1921'} if r.get('source_id')=='bosworth_toller_1898' else r for r in ledger['actual_inspections']]
ledger['actual_inspections'].extend(r for r in records if r['path'] not in known)
save('sources/audits/unit16-coordinator/primary-inspections.json',ledger)
protocol=read('sources/audits/unit16-coordinator/review-independence.json')
protocol['external_help_boundary']='If a task needs external lookup because the actual learner teaching/help omits a dependency, record a dependency gap even if a primary source enables a correct answer. Primary access does not silently cure missing learner support.'
save('sources/audits/unit16-coordinator/review-independence.json',protocol)
print('C06 correction, coordinator evidence catalog, actual inspection ledger and review boundary written.')
