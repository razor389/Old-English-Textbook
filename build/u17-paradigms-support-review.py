"""Record supplemental, personally inspected evidence for four supplied frames."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))

def identity(path):
    data = (ROOT / path).read_bytes()
    return {'path': path, 'raw_sha256': hashlib.sha256(data).hexdigest(),
            'normalized_lf_sha256': hashlib.sha256(data.replace(b'\r\n', b'\n').replace(b'\r', b'\n')).hexdigest()}

views = [
    ('sources/audits/unit17-source/fb-p278.png', 278,
     ['U17-FB-P278'], 'Vocabulary has be-twēox, among, between. It witnesses selected quantity and meaning but does not state government.'),
    ('sources/audits/unit17-source/fb-p316.png', 316,
     ['U17-FB-P316'], 'Vocabulary has tō-gēanes, towards, to meet. It does not state government or require postposition.'),
    ('sources/audits/unit17-source/fb-p291.png', 291,
     ['U17-FB-P291'], 'Vocabulary has ge-cwēme (59), pleasing, acceptable. It witnesses the adjective but does not alone establish the dative complement.'),
    ('build/u17-paradigms-fb-p184.png', 184,
     ['U17P-FB184'], 'Line7 cōm tōgēanes ðǣm cyninge has an unequivocal dative target. Lines9–10 nǣre nān Dianan swā gecwēme swā hēo have a deity as the target of pleasing; note5 on gecwēme explicitly says See165, the dative-adjective rule.'),
    ('sources/audits/unit06-grammar/bt_b0085.jpg', None,
     [], 'Bosworth–Toller printed85 covers beó-módor through beorg-hleóð. Inspected during the betwēox search; it supplies no betwēox evidence and is not cited in the linguistic conclusion.'),
    ('sources/audits/unit17-source/fb-p96.png', 96,
     ['U17-FB-P96'], 'Page continues dative absolute and gives §§168–172. It does not establish the four lexical frames; it is not substituted for direct lexical evidence.'),
    ('build/u17-paradigms-fb-p187.png', 187,
     [], 'Page has the fisherman reward and end of Apollonius. No requested betwēox or accompanying cweðende example occurs; the relevant feast example is on186.'),
    ('build/u17-paradigms-fb-p196.png', 196,
     [], 'Page describes sixth-day animals and has finite gecwæð. The sought accompanying cweðende blessing is on195, not196.'),
    ('sources/audits/unit14-grammar/fb-p95.png', 95,
     ['U17G-FB95', 'U14-G-FB95'], '§165 explicitly assigns dative complements to dear/useful/obedient and related adjectives, with Gode ðone lēofan fæder among examples. §166 says dative is common with prepositions but is not lexical proof for an arbitrary preposition.'),
    ('sources/audits/unit14-grammar/fb-p106.png', 106,
     ['U17G-FB106', 'U14-G-FB106'], '§201.1 explicitly permits a preposition to follow its object. This supports placement him tōgēanes when combined with the same-lexeme dative evidence on184.'),
    ('build/u17-paradigms-fb-p186.png', 186,
     ['U17P-FB186'], 'Line12 has betweox ðǣm cyning and ðǣm folce in the prepared feast. Both demonstratives and folce are dative despite the bare printed cyning. The source prints unmarked betweox here; the selected long betwēox is independently witnessed on278. This is between/among human participants, not a general assertion of invariant dative government.'),
    ('build/u17-paradigms-fb-p195.png', 195,
     ['U17P-FB195'], 'Lines3–4 have God hīe geblētsode ðā, ðus cweðende tō ðǣm fiscum, followed by direct speech. Cweðende accompanies the same subject’s finite blessing. The source subject is singular; a plural exercise application must be declared as such.'),
    ('sources/audits/unit03-source/fb-pdf142-p126.png', 126,
     ['U07-C-READ126'], 'Editorial line11, between printed10 and15, has And blētsode hīe, ðus cweðende, followed by Weaxað. The understood subject remains God. Note17 directs the reader to cweðan. This is the actual earlier Unit7 supplied accompanying construction.')
]
inspections = []
for path, page, refs, observation in views:
    row = identity(path)
    row.update({'actually_viewed': True, 'reviewer': 'unit17_paradigms',
                'inspection_method': 'Personal view_image inspection; OCR was a locator only.',
                'inspection_phase': 'post-witness-unlock supplied-frame investigation',
                'observation': observation, 'catalog_evidence_ids': refs})
    if page is not None:
        row['source_locators'] = [{'source_id': 'cook_fb_1895_2', 'printed_page': page,
                                   'pdf_page_one_based': page + 16}]
    else:
        row['source_locators'] = [{'source_id': 'bosworth_toller_main', 'printed_page': 85}]
    inspections.append(row)

boundary = []
terms = ['betweox', 'betwēox', 'togeanes', 'tōgēanes', 'gecweme', 'gecwēme',
         'cweðende', 'accompanying-participle']
for n in range(1, 17):
    path = f'chapters/ch{n:02d}/coverage.json'
    contract = read(path)
    rows = []
    for row in contract.get('grammar_inventory', []):
        if any(t in row.get('description', '') + ' ' + row.get('feature_id', '') for t in terms):
            rows.append({k: row.get(k) for k in ['feature_id', 'description', 'knowledge_status', 'scope_note', 'evidence_refs']})
    for row in contract.get('lexical_inventory', []):
        if row.get('lemma_id') in {'betweox', 'togeanes', 'gecweme'}:
            rows.append({k: row.get(k) for k in ['lemma_id', 'senses', 'scope_note']})
    boundary.append({'contract_identity': identity(path), 'relevant_explicit_records': rows})

checks = [
    {
        'construction': 'betwēox wīfum', 'items': ['EX-XII-XIII-40-01'],
        'status': 'support_gap_confirmed_pending_final_repair_review',
        'prior_boundary': 'Only Unit9 supplied betweox-among-source in exact accusative phrases. No independent case-government milestone exists in the sixteen prior contracts or actual registers.',
        'current_gap': 'The learner supplies betwēox and its meaning but no case or whole governed phrase.',
        'recommendation': 'Supply betwēox wīfum, among women; identify wīfum as dative plural. Keep this phrase supplied and do not claim betwēox always governs the dative.',
        'evidence_refs': ['U17P-FB186', 'U17-FB-P278'],
        'derivation_boundary': 'A bounded new phrase applying the directly witnessed dative human-group frame to independently known wīf morphology; not a verbatim quotation of betwēox wīfum from Cook186.'
    },
    {
        'construction': 'ðus cweðende', 'items': ['EX-XII-XIII-42-05', 'EX-XII-XIII-42-08'],
        'status': 'support_gap_confirmed_pending_final_repair_review',
        'prior_boundary': 'u06-source-participle and u07-source-accompanying-participle are supplied; u07-participle-formation explicitly preserves that syntactic limit even while cweðende is a productive form.',
        'current_gap': 'Current Unit17 productive human nominalization and two -ende agreement systems do not teach accompanying speech. Neither local exercise help currently supplies the expression.',
        'recommendation': 'Print the whole phrase at both tasks: saying thus. Explain that cweðende describes the angels/soldiers while they perform the finite actions and introduces their words; it is not another finite past-tense verb.',
        'evidence_refs': ['U17P-FB195', 'U07-C-READ126', 'U17G-FB41'],
        'derivation_boundary': 'The direct source examples have singular God as subject. Plural reference in the two exercise applications uses ordinary participial agreement; the supplied expression itself is unchanged.'
    },
    {
        'construction': 'him tōgēanes', 'items': ['EX-XII-XIII-43-13'],
        'status': 'support_gap_confirmed_pending_final_repair_review',
        'prior_boundary': 'No prior productive or supplied tōgēanes lemma/frame appears in the active lexical inventory or registers.',
        'current_gap': 'The learner supplies only the word and meaning. Its dative complement and the selected postposed realization are not visible.',
        'recommendation': 'Supply him tōgēanes, towards him/to meet him; identify him as dative singular and tōgēanes as following its complement. No general new postposition system is required.',
        'evidence_refs': ['U17P-FB184', 'U17G-FB106', 'U17-FB-P316'],
        'derivation_boundary': 'A declared application of cōm tōgēanes ðǣm cyninge on184 plus §201.1 permitted postposition, not a false quotation of him tōgēanes from that passage.'
    },
    {
        'construction': 'Gode gecwēme', 'items': ['EX-XII-XIII-43-15'],
        'status': 'support_gap_confirmed_pending_final_repair_review',
        'prior_boundary': 'No prior gecwēme lemma or frame is independently assigned. A general dative relation or a different adjective does not supply this lexical government.',
        'current_gap': 'The learner supplies nominative masculine singular gecwēme but leaves the target of pleasing without visible case support.',
        'recommendation': 'Supply Gode gecwēme, pleasing/acceptable to God; explain Gode as dative singular naming the one to whom the person is pleasing. Keep the adjective form and this frame supplied.',
        'evidence_refs': ['U17P-FB184', 'U17G-FB95', 'U17-FB-P291'],
        'derivation_boundary': 'A declared application of the same adjective with Dianan on184, whose note5 explicitly refers to §165, replacing the deity complement with familiar Gode.'
    }
]
report = {
    'reviewer': 'unit17_paradigms',
    'status': 'four_support_gaps_confirmed_bounded_supplies_recommended',
    'independence': 'Performed after the blind witness was frozen at ed28a8e and comparison access was unlocked. Direct page images and actual prior records were inspected independently; findings were then shared with the blind reviewer and coordinator.',
    'primary_evidence_image_inspections': inspections,
    'prior_contract_boundary_checks': boundary,
    'actual_register_identities': [identity('lexicon/entries.json'), identity('curriculum/grammar.json')],
    'construction_checks': checks,
    'source_locator_note': 'Cook second edition printed page +16 gives one-based PDF page. Individual prose line counts are editorial counts anchored by printed marginal5/10/15 numbers, not separately printed line labels.',
    'no_master_contract_or_register_edits': True,
    'remaining_gate': 'Coordinator reconciles the supplied constructions and task bindings, then author repairs are reread and final artifact identities checked. This support report does not accept unfinished amendments.'
}
out = ROOT / 'build/u17-paradigms-support-review.json'
out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')

ledger = read('chapters/ch17/reviews/paradigms.json')
ledger['supplemental_support_review'] = identity('build/u17-paradigms-support-review.json')
ledger['corroborated_supplied_construction_gaps'] = checks
by_path = {x['path']: x for x in ledger['primary_evidence_image_inspections']}
for row in inspections:
    if row['path'] not in by_path:
        ledger['primary_evidence_image_inspections'].append(row)
    else:
        prior = by_path[row['path']]
        assert prior['raw_sha256'] == row['raw_sha256']
        prior.setdefault('later_personal_inspections', []).append({k: row[k] for k in ['inspection_phase', 'observation']})
ledger['counts']['primary_images_personally_viewed'] = len(ledger['primary_evidence_image_inspections'])
ledger['remaining_gate'] = 'Five wording findings await author-repair reread; four corroborated supplied-construction gaps await coordinator amendment and final visible-support verification. All 110 systems, 124 matrices and1234 cells remain checked; no cell change is proposed. Final acceptance remains pending.'
(ROOT / 'chapters/ch17/reviews/paradigms.json').write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')

md_path = ROOT / 'chapters/ch17/reviews/paradigms.md'
md = md_path.read_text(encoding='utf-8')
md += """

After the blind witness was frozen at `ed28a8e` and comparison access was unlocked, this reviewer independently corroborated four learner-support gaps. The complete evidence and prior-teaching checks are in [the supplied-frame report](../../../build/u17-paradigms-support-review.json). All sixteen earlier contracts and both actual registers retain the narrow prior limits: Unit9 **betweox** was supplied in exact accusative phrases; Unit6/7 accompanying **cweðende** remained supplied; neither **tōgēanes** nor **gecwēme** had an earlier productive frame. Unit17's participial nominalization does not independently teach accompanying speech.

The recommendation is four whole-phrase supplies: **betwēox wīfum** at40.1, **ðus cweðende** at42.5/8, **him tōgēanes** at43.13, and **Gode gecwēme** at43.15, each with its local relation explained. Cook184 line7 directly witnesses **tōgēanes ðǣm cyninge**; lines9–10 and note5 explicitly bind **gecwēme** with **Dianan** to the dative-adjective rule. Cook186 line12 has **betweox ðǣm cyning and ðǣm folce**. Cook195 lines3–4 and earlier Cook126 line11 directly witness **ðus cweðende** accompanying God's blessing and introducing speech. The proposed exercise phrases are bounded grammatical applications of these witnessed frames, not falsely claimed verbatim quotations. The singular source subjects for **cweðende** remain recorded explicitly; the supplied exercise references are plural.

Every additional image actually opened, including unsuccessful locator pages, is recorded with its raw hash and concrete observation. No master, contract or register was edited by this reviewer. Final acceptance still requires the coordinator's reconciled amendment and verification of the actual repaired learner/key files.
"""
md_path.write_text(md, encoding='utf-8', newline='\n')
print(json.dumps({'supplemental_images_actually_viewed': len(inspections),
                  'distinct_images_in_main_ledger': ledger['counts']['primary_images_personally_viewed'],
                  'support_gaps': len(checks), 'status': report['status']}))
