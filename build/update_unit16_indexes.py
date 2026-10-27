"""Update shared indexes only after accepted Unit16 text, exports and registers."""
import json
from pathlib import Path

def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def once(text, old, new):
    assert text.count(old) == 1, (old, text.count(old))
    return text.replace(old, new, 1)

c = read('chapters/ch16/coverage.json')
assert c['textual_review']['status'] == c['presentation_review']['status'] == 'accepted'
assert read('chapters/ch16/register-integration.json')['status'] == 'accepted'
pages = read('typesetting/ch16/page-review.json')
assert pages['status'] == 'PASS' and not pages['unresolved_findings']
lp, kp = pages['page_totals']['learner'], pages['page_totals']['key']
m = c['contract_metrics']
assert m['cook_items'] == 59 and m['source_words'] == [444]
changes = {}

p = 'README.md'; s = Path(p).read_text(encoding='utf-8')
assert '**Unit 16 is complete:**' not in s
s = once(s, '**Units 1–15 are complete**', '**Units 1–16 are complete**')
paragraph = f'**Unit 16 is complete:** [learner PDF](typesetting/ch16/chapter-16.pdf), {lp} pages, and [separate key PDF](typesetting/ch16/answer-key.pdf), {kp} pages. Extended narrative and speech are taught through {m["paradigms"]} complete bounded systems / {m["logical_cells"]} cells and {m["tasks"]} tasks, including all 59 Cook XII, XIII.32–36 prompts. The complete 444-word gymnasium episode from *Apollonius* has local help and all 54 original notes. Fresh independent reviews and non-author inspection of all {lp+kp} pages are complete. See the [review and export record](typesetting/ch16/README.md).\n\n'
changes[p] = once(s, 'The earlier two-chapter experiment', paragraph + 'The earlier two-chapter experiment')

p = 'typesetting/README.md'; s = Path(p).read_text(encoding='utf-8')
assert '[Unit 16 exports]' not in s
changes[p] = once(s, 'Use `chapter-template.tex`', f'The reviewed [Unit 16 exports](ch16/README.md) have **{lp} learner and {kp} key pages**. Every final page has a non-author visual record, complete text/table parity and final file identities.\n\nUse `chapter-template.tex`')

p = 'curriculum/COURSE_PLAN.md'; s = Path(p).read_text(encoding='utf-8')
s = once(s, 'Exercises 1–31 now have full item-level audits; Exercises 32–48 still require them.', 'Exercises 1–36 now have full item-level audits; Exercises 37–48 still require them.')
old_row = next(line for line in s.splitlines() if line.startswith('| 16. '))
new_row = '| 16. Extended narrative and speech | Participants, perception and finite content clauses, relative time, knowing and repeated actions, direct/reported speech and bounded lexical government. Complete new nominal and verbal systems retain their selected senses and uses. | Joint Group XII, XIII, Exercises 32–36: all 59 items, plus 17 original tasks. | The complete 444-word gymnasium episode, Cook 168.1–170.16 / PDF 184–186, with local help and all 54 original notes. |'
s = once(s, old_row, new_row)
s = once(s, 'The current crosswalk is **456 assigned and 188 deferred items**.', 'Through Unit 15 the crosswalk was **456 assigned and 188 deferred items**.')
paragraph = f'The [Unit 16 source audit](../sources/audits/unit16-source/source-audit-report.json), [grammar audit](../sources/audits/unit16-grammar/review-report.json) and [contract](../chapters/ch16/coverage.json) establish all 59 joint XII, XIII.32–36 prompts and the complete gymnasium scene. The {m["paradigms"]} bounded systems / {m["logical_cells"]} cells appear in literal tables. Four translated examples and 17 original tasks practise complete forms, participants, complements, speech, temporal viewpoint and the actual connected reading. Supplied phrases remain distinct from independent recall. All 54 original notes / 59 anchors remain; the following feast is unassigned. [C06](../sources/audits/unit16-coordinator/reward-correction.json) preserves the printed reward hint while supplying the evidenced correction. The current crosswalk is **515 assigned and 129 deferred items**.\n\n'
changes[p] = once(s, 'Active coverage contracts, not this plan', paragraph + 'Active coverage contracts, not this plan')

p = 'curriculum/COOK_MAP.md'; s = Path(p).read_text(encoding='utf-8')
s = once(s, 'The current canonical crosswalk is **456 assigned, 188 deferred and none excluded**', 'Through Unit 15 the canonical crosswalk was **456 assigned, 188 deferred and none excluded**')
s = once(s, 'Exercises **1–31** now have full item-level linguistic audits; Exercises **32–48** remain structurally audited only.', 'Exercises **1–36** now have full item-level linguistic audits; Exercises **37–48** remain structurally audited only.')
paragraph = 'The [Unit 16 contract](../chapters/ch16/coverage.json) assigns all **59 exact joint XII, XIII.32–36 prompts**: 11, 10, 13, 14 and 11 items respectively. Original IDs remain EX-XII-XIII-NN-NN. The current canonical crosswalk is **515 assigned, 129 deferred and none excluded**, totaling all 644 items. The exact 444-word *Incidents in the Gymnasium* reading spans printed 168.1–170.16 / one-based PDF 184–186, ending **cume tō his gereorde.** Individual line numbers are editorial counts anchored by printed marginal numbers. All 54 original notes and 59 anchors remain. Earlier Apollonius excerpts and the following feast are outside this assignment. Seventeen original tasks accompany the source work.\n\n'
changes[p] = once(s, 'All exercise boundaries and terminal item numbers', paragraph + 'All exercise boundaries and terminal item numbers')

p = 'sources/README.md'; s = Path(p).read_text(encoding='utf-8')
s = once(s, 'Exercises 1–31 now have separate item-level audits; Exercises 32–48 still require them.', 'Exercises 1–36 now have separate item-level audits; Exercises 37–48 still require them.')
s = once(s, 'The current crosswalk is 456 assigned / 188 deferred out of 644; Exercises 1–31 have full item-level audits.', 'At the Unit 15 checkpoint the crosswalk was 456 assigned / 188 deferred out of 644; Exercises 1–31 had full item-level audits.')
s += f'\nUnit 16’s [source audit](audits/unit16-source/source-audit-report.json), [grammar audit](audits/unit16-grammar/review-report.json), [design](../curriculum/proposals/unit16/design-audit-report.md) and [coordinator reconciliation](audits/unit16-coordinator/reconciliation.json) establish all 59 Cook XII, XIII.32–36 prompts and the exact 444-word gymnasium scene. The [contract](../chapters/ch16/coverage.json) retains {m["tasks"]} tasks / {m["requested_output_positions"]} requested outputs, {m["paradigms"]} bounded systems / {m["logical_cells"]} cells, four translated examples and all 54 original notes / 59 anchors. [C06](audits/unit16-coordinator/reward-correction.json) preserves the printed āgyltan §113 reward hint and supplies strong āgyldan with contracted āgylt. The registered Matthew edition, printed 132 / PDF 142, corroborates both the reward clause and impending tō cumanne; printed 114 / PDF 124 supplies the John endings with declared initial I→J. The reading retains negative næfde, uncertain reference and top, and mixed invitation wording; the Latin ointment parallel is explained separately in English. [Fresh text review](../chapters/ch16/review.md) and [separate paradigm review](../chapters/ch16/reviews/paradigms.json) resolve material findings. Sealed packets, original witnesses and earlier source records remain unchanged. The current crosswalk is 515 assigned / 129 deferred out of 644; Exercises 1–36 have full item-level audits.\n'
changes[p] = s

p = 'sources/registry.json'; d = read(p)
selected = {r['source_id']: r for r in d['selected_sources']}
selected['cook_ex_1895']['verification'] = 'All 48 exercise boundaries and terminal item counts structurally checked. Exercises 1–36 now have full item-level linguistic audits; Exercises 37–48 still require them. Unit 16 assigns all 59 joint XII, XIII.32–36 prompts. Active coverage contracts govern assignment; older descriptions retain their historical scope.'
selected['cook_ex_1895']['unit16_verification'] = 'All 59 prompts visually checked on printed 18–22 / one-based PDF 26–30, preserving exact English, lexical hints, number, omission and word-order controls. Joint XII, XIII remains one original heading. Books in34.3 and hooked letters in32.6 correct audit transcription. C06 documents the actual printed reward hint error in34.9, preserving its original. Actual learner/key outputs independently reviewed.'
selected['cook_fb_1895_2']['unit16_verification'] = 'Complete exact 444-word Incidents in the Gymnasium, printed168.1–170.16 / PDF184–186, with51 editorially counted lines,54 original notes and59 anchors. The following feast is excluded from this span. Preserve source spelling, negation, uncertain reference/top and mixed speech; modern English help for Latin parallels remains separate. Complete selected nominal/verbal systems and lexical frames have primary-image evidence and independent review.'
audits = ['sources/audits/unit16-source/source-audit-report.json', 'sources/audits/unit16-source/evidence-catalog.json', 'sources/audits/unit16-grammar/review-report.json', 'sources/audits/unit16-grammar/evidence-catalog.json', 'sources/audits/unit16-coordinator/reconciliation.json', 'sources/audits/unit16-coordinator/reward-correction.json', 'chapters/ch16/review.md', 'chapters/ch16/reviews/paradigms.json']
for sid in ['cook_ex_1895', 'cook_fb_1895_2']:
    for path in audits:
        assert Path(path).is_file(), path
        if path not in selected[sid].setdefault('active_audits', []): selected[sid]['active_audits'].append(path)
for source in d['supporting_sources']:
    if source['source_id'] in ['bt_online', 'bosworth_toller_1898_1921']:
        source['unit16_use'] = {'source_record': 'sources/audits/unit16-source/evidence-catalog.json', 'grammar_record': 'sources/audits/unit16-grammar/evidence-catalog.json', 'correction': 'sources/audits/unit16-coordinator/reward-correction.json', 'review': 'chapters/ch16/reviews/paradigms.json', 'scope': 'Inspected primary facsimiles support bounded lexical government and meaning. Main29–30 distinguish strong reward āgyldan/āgylt from weak āgyltan sin/fail; other specified images support the causative, permission and cessation phrases. Transcriptions are finding aids, not substitutes for images.'}
    elif source['source_id'] == 'wright_oe_1914':
        source['unit16_use'] = {'source_record': 'sources/audits/unit16-source/evidence-catalog.json', 'grammar_record': 'sources/audits/unit16-grammar/evidence-catalog.json', 'review': 'chapters/ch16/reviews/paradigms.json', 'scope': 'Primary tables and rules corroborate the long-ja zero plural nętt, full nearu u/o/w system, and selected weak/stem alternations. Complete tables retain their expressly bounded senses and syntax.'}
changes[p] = json.dumps(d, ensure_ascii=False, indent=2)
for path, content in changes.items():
    Path(path).write_text(content.rstrip() + '\n', encoding='utf-8', newline='\n')
print('Updated six shared indexes from accepted Unit16 artifacts.')
