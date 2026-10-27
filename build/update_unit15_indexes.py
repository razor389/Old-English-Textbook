"""One-use shared-index update, gated on reviewed Unit15 completion."""
import json
from pathlib import Path

def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def once(text, old, new):
    assert text.count(old) == 1, (old,text.count(old))
    return text.replace(old,new,1)
c = read('chapters/ch15/coverage.json')
assert c['textual_review']['status'] == c['presentation_review']['status'] == 'accepted'
assert read('chapters/ch15/register-integration.json')['status'] == 'accepted'
pages = read('typesetting/ch15/page-review.json')
assert pages['status'] == 'PASS' and not pages['unresolved_findings']
lp,kp = pages['page_totals']['learner'],pages['page_totals']['key']
assert len(c['assigned_items']) == 105 and len(c['paradigms']) == 69
changes = {}

p='README.md'; s=Path(p).read_text(encoding='utf-8')
assert '**Unit 15 is complete:**' not in s
s=once(s,'**Units 1–14 are complete**','**Units 1–15 are complete**')
paragraph=f'**Unit 15 is complete:** [learner PDF](typesetting/ch15/chapter-15.pdf), {lp} pages, and [separate key PDF](typesetting/ch15/answer-key.pdf), {kp} pages. Negation, quantity and comparison are taught through 69 defined systems / 691 positions, including 16 explicitly unassigned number slots, and 105 tasks. All 50 Cook IX.28–30 and X, XI.31 prompts remain. Three supported readings total 415 words: the opening argument of *Duties of the Rich toward the Poor*, the complete *Alfred’s Preface to Boethius* and *A Prayer of King Alfred*. All 27 original notes remain. Fresh independent reviews and non-author inspection of all {lp+kp} pages are complete. See the [review and export record](typesetting/ch15/README.md).\n\n'
changes[p]=once(s,'The earlier two-chapter experiment',paragraph+'The earlier two-chapter experiment')

p='typesetting/README.md'; s=Path(p).read_text(encoding='utf-8')
assert '[Unit 15 exports]' not in s
changes[p]=once(s,'Use `chapter-template.tex`',f'The reviewed [Unit 15 exports](ch15/README.md) have **{lp} learner and {kp} key pages**. Every final page has a non-author visual record, complete text/table parity and final file identities.\n\nUse `chapter-template.tex`')

p='curriculum/COURSE_PLAN.md'; s=Path(p).read_text(encoding='utf-8')
s=once(s,'Exercises 1–27 now have full item-level audits; Exercises 28–48 still require them.','Exercises 1–31 now have full item-level audits; Exercises 32–48 still require them.')
s=once(s,'| Group IX, Exercises 28–30; joint Group X, XI, Exercise 31. | Duties of the Rich toward the Poor; Alfred\'s preface and prayer as complete short texts or complete checked sections. |','| Group IX, Exercises 28–30; joint Group X, XI, Exercise 31: all 50 items, plus 55 original tasks. | Duties of the Rich toward the Poor, opening argument (159.1–12); complete Alfred preface (162.1–17) and prayer (163.1–18), with local support and all 27 original notes. |')
s=once(s,'Negative, indefinite and proportional families beyond these bounded helps remain Unit 15 work. The current crosswalk is **406 assigned and 238 deferred items**.','At the Unit 14 boundary, further negative, indefinite and proportional families awaited Unit 15. Through Unit 14 the crosswalk was **406 assigned and 238 deferred items**.')
paragraph='The [Unit 15 source audit](../sources/audits/unit15-source/README.md), [grammar audit](../sources/audits/unit15-grammar/report.json) and [contract](../chapters/ch15/coverage.json) establish all 50 IX.28–30 and joint X, XI.31 prompts, together with the three exact readings above. All 69 defined systems appear in literal tables: 691 logical positions, comprising 675 form/expression cells and 16 explicitly unassigned number slots. Complete morphology retains its stated sense and syntax limits. Eight translated examples and 55 original tasks practise negation, indefinite/distributive reference, quantity, comparison and connected discourse. The 114 reading and 36 Cook help groups retain supplied scope. The current crosswalk is **456 assigned and 188 deferred items**.\n\n'
changes[p]=once(s,'Active coverage contracts, not this plan',paragraph+'Active coverage contracts, not this plan')

p='curriculum/COOK_MAP.md'; s=Path(p).read_text(encoding='utf-8')
s=once(s,'The current canonical crosswalk is **406 assigned, 238 deferred and none excluded**','Through Unit 14 the canonical crosswalk was **406 assigned, 238 deferred and none excluded**')
s=once(s,'Exercises **1–27** now have full item-level linguistic audits; Exercises **28–48** remain structurally audited only.','Exercises **1–31** now have full item-level linguistic audits; Exercises **32–48** remain structurally audited only.')
paragraph='The [Unit 15 contract](../chapters/ch15/coverage.json) assigns all **50 exact IX.28–30 and joint X, XI.31 prompts**: 12, 11, 13 and 14 items respectively, resolving their earlier deferrals. Joint-group IDs remain EX-X-XI-31-NN. The current canonical crosswalk is **456 assigned, 188 deferred and none excluded**, totaling all 644 numbered items. The three exact readings are the 103-word Duties opening argument (printed 159.1–12 / PDF 175), the complete 152-word Alfred preface (162.1–17 / PDF 178), and the complete 160-word prayer (163.1–18 / PDF 179). Individual line counts are editorial, anchored by printed marginal numbers. All 27 original notes and 33 anchors remain. The Duties speech continues outside the assigned extract on pp. 160–161. Fifty-five original tasks accompany the source work.\n\n'
changes[p]=once(s,'All exercise boundaries and terminal item numbers',paragraph+'All exercise boundaries and terminal item numbers')

p='sources/README.md'; s=Path(p).read_text(encoding='utf-8')
s=once(s,'Exercises 1–27 now have separate item-level audits; Exercises 28–48 still require them.','Exercises 1–31 now have separate item-level audits; Exercises 32–48 still require them.')
s=once(s,'The current crosswalk is 406 assigned / 238 deferred out of 644; Exercises 1–27 have full item-level audits.','At the Unit 14 checkpoint the crosswalk was 406 assigned / 238 deferred out of 644; Exercises 1–27 had full item-level audits.')
s+='\nUnit 15’s [source audit](audits/unit15-source/README.md), [grammar audit](audits/unit15-grammar/report.json), [design](../curriculum/proposals/unit15/README.md) and [coordinator reconciliation](audits/unit15-coordinator/reconciliation.json) establish all 50 Cook IX.28–30 and joint X, XI.31 prompts and three exact readings totaling415 words. The [contract](../chapters/ch15/coverage.json) retains105 tasks,69 defined systems/691 positions, eight examples,27 original notes/33 anchors,114 reading helps and36 Cook help groups. A600dpi inspection confirms **blōstmian** with m in Cook30.11; the earlier n reading was our transcription error, preserved as withdrawn audit history rather than a Cook erratum. Wright supplies the complete strengu reference paradigm; hǣlu/hǣtu and people names retain explicit number/sense limits. [Fresh text review](../chapters/ch15/review.md) and [separate paradigm review](../chapters/ch15/reviews/paradigms.json) resolve material findings. Sealed packets and blind solutions remain unchanged; canonical amendments document later refinements. The current crosswalk is456 assigned/188 deferred out of644; Exercises1–31 have full item-level audits.\n'
# Keep numeric editorial prose readable.
for old,new in [('totaling415','totaling 415'),('retains105','retains 105'),(',69',', 69'),('systems/691','systems / 691'),(',27',', 27'),('notes/33','notes / 33'),(',114',', 114'),('and36','and 36'),('A600dpi','A 600 dpi'),('Cook30.11','Cook 30.11'),('is456','is 456'),('assigned/188','assigned / 188'),('of644','of 644'),('Exercises1–31','Exercises 1–31')]:
    s=s.replace(old,new)
changes[p]=s

p='sources/registry.json'; d=read(p)
selected={r['source_id']:r for r in d['selected_sources']}
selected['cook_ex_1895']['verification']='All 48 exercise boundaries and terminal item counts structurally checked. Exercises 1–31 now have full item-level linguistic audits; Exercises 32–48 still require them. Unit 15 assigns all 50 IX.28–30 and joint X, XI.31 prompts. Active coverage contracts govern assignment; older descriptions retain their historical scope.'
selected['cook_ex_1895']['unit15_verification']='All 50 prompts visually checked on printed 15–18 / one-based PDF 23–26, preserving exact English, hints, omissions and order controls. Joint X, XI remains a single original group. Cook 30.11 reads blōstmian with m, confirmed at 600 dpi; initial n was an audit transcription error, not a source erratum. Actual learner/key outputs independently reviewed.'
selected['cook_fb_1895_2']['unit15_verification']='Exact 103-word Duties opening argument, printed 159.1–12 / PDF 175 (outer speech continues 160–161); complete 152-word Alfred preface, 162.1–17 / PDF 178; complete 160-word prayer, 163.1–18 / PDF 179. Editorial line counts are anchored by printed marginal numbers. All 27 notes / 33 anchors remain, separately from modern help. Exact source spellings, lengths, vocabulary, grammar and selected complete systems verified against images.'
audit_paths=['sources/audits/unit15-source/README.md','sources/audits/unit15-source/evidence-catalog.json','sources/audits/unit15-grammar/report.json','sources/audits/unit15-grammar/evidence-catalog.json','sources/audits/unit15-coordinator/reconciliation.json','chapters/ch15/review.md','chapters/ch15/reviews/paradigms.json']
for sid in ['cook_ex_1895','cook_fb_1895_2']:
    for path in audit_paths:
        assert Path(path).is_file(),path
        if path not in selected[sid].setdefault('active_audits',[]): selected[sid]['active_audits'].append(path)
for source in d['supporting_sources']:
    if source['source_id'] in ['bt_online','bosworth_toller_1898_1921']:
        source['unit15_use']={'source_record':'sources/audits/unit15-source/evidence-catalog.json','grammar_record':'sources/audits/unit15-grammar/evidence-catalog.json','coordinator_record':'sources/audits/unit15-coordinator/primary-inspections.json','review':'chapters/ch15/reviews/paradigms.json','scope':'Personally inspected facsimiles support lexical quantity, negative and distributive meanings, nominal forms and payment/comparison frames. Main 683a supplies substantive micel; 750b supplies accusative payment with onfōn; Supplement 357a supplies agreeing gelīc with a dative standard; 718b supplies preference swīðe. Web transcriptions served as finding aids; primary image inspections govern.'}
    elif source['source_id']=='wright_oe_1914':
        source['unit15_use']={'evidence':'sources/audits/unit15-source/wright-p184.png','review':'chapters/ch15/reviews/paradigms.json','scope':'Printed 184 §§382–383 supplies the full strengu reference class and variants. Selected hǣlu/hǣtu singular systems do not establish productive count-plural meanings. Pronoun pages 239–240 support bounded family dispositions.'}
changes[p]=json.dumps(d,ensure_ascii=False,indent=2)
for path,content in changes.items():
    Path(path).write_text(content.rstrip()+'\n',encoding='utf-8',newline='\n')
print('Updated six shared indexes from accepted Unit15 artifacts.')
