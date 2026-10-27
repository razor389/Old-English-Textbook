"""Record actual manual image views; rendering alone does not count as inspection."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
rows = []

def add(path, source, printed, pdf, observation):
    raw = (ROOT / path).read_bytes()
    rows.append(dict(path=path, sha256=hashlib.sha256(raw).hexdigest(),
                     source_id=source, printed_page=printed, pdf_page_one_based=pdf,
                     inspector='coordinator/root', date='2026-10-27',
                     method='Personally viewed through view_image at original detail',
                     observation=observation))

for n in range(18, 23):
    add(f'sources/audits/course-map/ex-page{n}.png', 'cook_ex_1895', n, n+8,
        'Initial complete prompt/page boundary inspection. Fine letters were subsequently rechecked on higher-resolution images; this low-resolution view alone does not certify them.')
add('sources/audits/course-map/fb-contents02.png','cook_fb_1895_2',None,None,
    'Actual contents: XII Apollonius begins164; Gymnasium168; Feast170; XIII Six Days Creation189. The joint exercise heading is not evidence for a Cook reader Gospel section.')
for n, folder, dpi in [(165,'unit04-source',400),(166,'unit04-source',400),(167,'unit06-source',600)]:
    add(f'sources/audits/{folder}/fb-pdf{n+16}-p{n}-{dpi}dpi.png','cook_fb_1895_2',n,n+16,
        'Read preceding narrative and original apparatus to establish context and avoid reassigning earlier units. Fisherman scene begins166.13 and ends167; earlier gift extract overlaps the rejected full-fisherman candidate.')
observations = {
18:'Joint XII,XIII heading;32.1–6 begin here. grētan,swilce,furlang,gān,uppan and verb-last controls retained;32.6 continues on19.',
19:'32.7 explicitly make that ye(dual)are, with dōn;32.8 all comparison clauses and omissions;32.9–11 lost sheep;33.1–3 command/execution/prophecy extends to20.',
20:'34.3 unequivocally BOOKS, matching b in be/both on same line. Earlier source-agent hooks reading rejected.33.3 ending,33.4–10 and34.1–11 controls checked, including āgyltan and cunnan/witan.',
21:'34.11–13 retain all speaker/reference and word-order instructions.35.10 prints then(ðā), carried(beran), not gān; short e in beran.35.7 retains both relative clauses and may(not)speak.',
22:'36.2 bewęndan184.a;36.3 verb-last and bracketed finite kiss clause;36.6 dative relative;36.7 om.is;36.8 om.should;36.9 fuluhtere44.1. The special omission instruction belongs only to37.'}
for i,n in enumerate(range(18,23),1):
    add(f'sources/audits/unit16-source/exercise-{i:03d}.png','cook_ex_1895',n,n+8,observations[n])
for n, note in [(168,'Full scene starts Æfter ðisum wordum; source notes1–21, public announcement, bath/game and joined-sentence page boundary checked.'),
                (169,'Full action sequence and notes1–17 checked. Awkward geslægene, unclear knowledge/equal clause, tentative top meaning, explicit subjects in notes14–15. Initial root næfde misreading corrected after600dpi view.'),
                (170,'Assignment ends line16 with royal invitation before Feast heading. Substitute dōn note4; mixed speech note15; missing close quote after opening oath preserved with editorial explanation.')]:
    add(f'sources/audits/unit16-coordinator/cook-fb-p{n}-300.png','cook_fb_1895_2',n,n+16,note)
add('sources/audits/unit16-coordinator/cook-fb-p169-600.png','cook_fb_1895_2',169,185,
    'Decisive recheck:169.6 is næfde. Corrects root initial hæfde/positive translation; source editor negative transcript is correct. All text and both note columns visible; ambiguity does not permit dropping negation.')
out = ROOT / 'sources/audits/unit16-coordinator/primary-inspections.json'
assert not out.exists(), 'Initial inspection ledger already recorded; append later inspections explicitly'
out.write_text(json.dumps({'schema_version':1,'chapter':'ch16','actual_inspections':rows,
    'limitation':'Only these personally viewed images are certified. Other rendered candidate pages are not claimed as inspected. These are source views, not final exported-page acceptance.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(len(rows),'actual source inspections recorded')
