"""Reproduce this worker's image-checked source transcriptions; no shared writes."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def write(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8')

prompts = {
    26: [
        'Thou art dust, and thou returnest (gewendan) to dust.',
        'So much (swīðe) loved God (om. the) world (middangeard), that he gave (sęllan) his only-begotten (āncęnned) Son, that no one (om. may) perish (196. f) that (87. d) believeth in (on, 172) him, but have (196. f) the eternal life.',
        'Jesus said (cweðan) to him, I am way, and truth, and life; no one (nān) cometh (183) to the Father, except by (ðurh) me.',
        'Peace I leave (om. with) you (164. a); my peace I give (forgiefan) you.',
        'Then rained it, and there (ðǣr) came floods, and blew winds, and fell (āhrēosan) on that house; and the house fell (feallan).',
        'So every good tree beareth (beran) good fruits (wǣstm), and every evil tree beareth evil fruits.',
        'Every tree that (87. d) beareth not good fruit (sing.) is cut down (forceorfan, 104) and cast into (om. the) fire (verb last).',
        'He went into (on, 172) a mountain, that he (om. might) pray (gebiddan, 184. b); and when (ðā) he prayed (184. b), his raiment was white (hwīt), shining.',
        'The mountain, falling, (be)cometh to naught.',
        'The king, in all his glory (wuldor), was not adorned like (swā-swā) one of these.',
    ],
    27: [
        'He showed (ætīewan) them his precious things,—the silver, and the gold, and the spices, and all that was found (gemētan) in his treasures.',
        'A certain rich man was adorned (geglęngan) with purple (verb last).',
        'Then (ðā) lay a certain poor man at his gate.',
        'No man gave (om. unto) him; but dogs (hund, 43) came and licked (liccian, 118) his sores (wund, 43).',
        'Then happened it that the poor man departed (gewītan); and angels bore him to Abraham’s (54) dwelling.',
        'Then lifted (āhebban) he his eyes up, and saw Abraham afar off [from afar].',
        'O father Abraham, have compassion on me, and send Lazarus.',
        'O son, remember that thou didst receive goods in thy life.',
        'I beseech thee that thou send him to my father’s house.',
        'If they hear not the prophets, they (om. will) not believe, though any one (hwā) arise from death (verb last).',
        'Provide for yourselves (184. a) friends (156. n) in (on) God’s poor (ðearfa). Ye have many Lazaruses (Lazaras) now lying at your gates.',
    ],
}
items = []
for exercise, ss in prompts.items():
    for n, prompt in enumerate(ss, 1):
        pages = ([13] if n == 1 else [13, 14] if n == 2 else [14]) if exercise == 26 else ([14] if n < 7 else [14, 15] if n == 7 else [15])
        items.append({'source_item_id': f'EX-VIII-{exercise:02}-{n:02}', 'source_id': 'cook_ex_1895', 'original_group': 'VIII', 'original_exercise': exercise, 'original_item': n, 'original_identifier': f'VIII.{exercise}.{n}', 'printed_pages': pages, 'pdf_pages_one_based': [p+8 for p in pages], 'prompt': prompt, 'origin_category': 'exact source with declared typographic normalization', 'disposition_proposal': 'assigned', 'source_image_refs': [f'sources/audits/unit14-source/cook-ex-{p-12:03}.png' for p in pages], 'evidence_refs': [f'U14-EX-P{p}' for p in pages]})
write('exercises-prompts.json', {'schema_version': 1, 'source_id': 'cook_ex_1895', 'count': len(items), 'verification': 'Personally inspected selected primary page images, printed13–15 / PDF21–23. OCR used only as finding aid.', 'normalization': ['Join line/page breaks; remove line-end division hyphens in forceorfan, shining, Abraham.', 'Represent typographic apostrophes with Unicode right apostrophe; collapse spacing before punctuation.', 'Represent continuous em dash with em dash; retain printed brackets, controls, lexical spellings and section letters.'], 'items': items})

lines = {
156: [
 'Ǣghwilc hēah ār, hēr on worulde, bið mid frēcnessum[1]',
 'ymbseald[2]; efne swā[3] ðā woruldgeðyngða bēoð māran, swā',
 'ðā frēcnessa bēoð swīðran. Swā wē magon, be ðǣm, ðā',
 'bȳsena oncnāwan and ongietan.[4] Ðæt trēow, ðonne, ðe',
 'wiexð[5] on ðǣm wudubearwe, ðæt[6] hit hlīfað ūp ofer eall',
 'ðā ōðru trēowu and brǣt[6a] hit,[7] ðonne sęmninga storm[8]',
 'gestęnt, and se stranga wind,[9] ðonne[10] bið hit swīðlicor',
 'gewǣged and geswęnged ðonne se ōðer wudu.[11] Swā bið',
 'ēac gelīce be ðǣm hēaclifum and torrum,[12] ðonne hīe',
],
157: [
 'hlīfiað feorr ūp ofer ðā ōðre[1] eorðan, hīe ðonne sęmninga',
 'feallan onginnað,[2] and full ðearlice hrēosan[3] tō eorðan.',
 'Swilce[4] ēac be ðǣm hēagum[5] muntum and dūnum,[6] ðā-',
 'ðe hēah standað ofer ealne middangeard, ðā-hwæðre wīte',
 'habbað ðæs ealdordōmes, ðæt hīe bēoð geneahhe mid',
 'heofonfȳre[7] geðrēade and geðrǣste, and mid līegum ge-',
],
158: [
 'slægene. Swā ðā hēan mihta[1] hēr on worulde hrēosað,',
 'and feallað,[2] and tō lore weorðað, and ðisse[3] worulde[3]',
 'welan weorðað tō sorge, and ðās eorðlican wundor',
 'weorðað tō nāhte.[4]',
]}
# Correct literal keyboard entry against the inspected page before publication.
records = []
for p, ss in lines.items():
    for n, s in enumerate(ss, 1):
        records.append({'source_line_id': f'FB156-158-{p}-{n:02}', 'printed_page': p, 'pdf_page_one_based': p+16, 'editorial_line': n, 'source_with_note_markers': s, 'line_number_convention': 'Editorial prose-line count from first Old English line on page; printed marginal5 anchors pp156–157; p158 boundary ends immediately before printed5.'})
text = ' '.join(re.sub(r'\[[0-9]+[a-z]?\]', '', r['source_with_note_markers']) for r in records).replace('ðā- ðe','ðā-ðe').replace('ge- slægene','geslægene')
write('reading-source.json', {'schema_version': 1, 'source_span_id': 'FB-VIII-DANGERS-OPENING-ARGUMENT', 'source_id': 'cook_fb_1895_2', 'original_identifier': 'Reader VIII, The Dangers of Greatness, opening argument', 'origin_category': 'exact source; declared removal of layout/apparatus markers only', 'title': 'The Dangers of Greatness', 'printed_pages': [156,157,158], 'pdf_pages_one_based': [172,173,174], 'start': {'printed_page':156,'editorial_line':1,'text':'Ǣghwilc hēah ār'}, 'end': {'printed_page':158,'editorial_line':4,'text':'weorðað tō nāhte.'}, 'word_count': len(text.split()), 'source_lines': records, 'learner_text': text, 'selection_rationale': 'Complete first argument: opening thesis about danger with high station; connected tree, cliff and mountain examples; explicit return to human power, wealth and earthly wonders. The following paragraph begins a distinct luxury/death argument and is unassigned.', 'unassigned_continuation': 'Printed158.5 through the end of ReaderVIII; begins Ðēah wē ðisse worulde wlęnca tilien swīðe.', 'source_image_refs': [f'sources/audits/unit14-source/dangers-{n:03}.png' for n in (1,2,3)], 'evidence_refs': ['U14-SRC-P156','U14-SRC-P157','U14-SRC-P158'], 'normalizations': [{'kind':'layout','change':'Remove page headers, printed marginal numbers, footnote cues and line/page breaks; join two divided words ðā- / ðe and ge- / slægene. Retain the lexical hyphen in ðā-ðe.'}, {'kind':'typography','change':'Superscript source notes are represented in the source-line field by bracketed editorial markers; these markers are omitted from learner text.'}], 'linguistic_changes': []})
write('author-only-reading-witness.json', {'audience':'author only; withhold until independent solver freezes answers', 'independence':'Prepared directly from the inspected selected Old English, before consulting other translators or any prior-course answer key.', 'source_span_id':'FB-VIII-DANGERS-OPENING-ARGUMENT', 'translation':'Every high honour here in the world is surrounded by dangers; just as worldly distinctions are greater, so the dangers are stronger. Thus we can recognize and understand the examples from this. The tree, then, which grows in the woodland so that it towers up above all the other trees and spreads itself out—when suddenly a storm arises, and the strong wind, then it is shaken and battered more violently than the rest of the forest. It is likewise also with the high cliffs and crags: when they tower far up above the rest of the earth, they then suddenly begin to fall and crash very violently to the earth. Likewise also with the high mountains and hills, which stand high above the whole world: nevertheless they suffer the punishment of their eminence, in that they are often chastised and afflicted by heavenly fire, and struck by flames. So the high powers here in the world collapse and fall and come to ruin, and the riches of this world turn to sorrow, and these earthly wonders come to nothing.', 'translation_notes':['ār here is high dignity/honour, not grace or mercy.', 'The tree sentence has a left-dislocated topic with later resumptive hit. The English dash is a translation aid, not source punctuation.', 'brǣt hit is reflexive spreading itself; do not make the storm the actor.', 'The storms illustrate risk attached to height, then the text transfers the comparison to worldly power.', 'torr here probably means a crag according to Cook156note12, not the productive earlier tower sense.', 'wīte habban ðæs ealdordōmes: suffer punishment on account of their eminence; the following ðæt explains it.', 'The literal repeated collapse/fall is preserved though Cook calls feallað pleonastic.', 'mihta can be rendered powers or potentates; the personification is contextual, not a unique new referential identity.']})
print(f'{len(items)} Cook items; {len(text.split())} reading words; {len(records)} source lines')
