"""Record coordinator observations made by personally viewing these facsimiles.

This records views already performed. It does not infer inspection from existence.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
target = ROOT / 'sources/audits/unit18-coordinator/primary-inspections.json'
data = json.loads(target.read_text(encoding='utf-8-sig'))
observations = [
    ('sources/audits/unit17-source/fb-p32.png', 32,
     'Cook, A First Book in Old English, selected1895 second edition',
     'Personally re-read the strong-neuter class rule and complete hof/word singular-plural tables; these support the already-established class framework used by the new lexical tables.'),
    ('sources/audits/unit17-source/fb-p33.png', 33,
     'Cook, A First Book in Old English, selected1895 second edition',
     'Personally read47.5: unmarked feoh, money/fee, genitive fēos, with reference to43.3 for loss of h. The source itself marks the oblique vowel while leaving the headword unmarked. Also read47.4 fæt versus fatu/fata/fatum.'),
    ('sources/audits/unit18-source/fb-p99.png', 99,
     'Cook, A First Book in Old English, selected1895 second edition',
     'Personally read176 adverbial instrumental, including number of times, and178 instrumental of difference. These support the supplied ōðre sīðe and lȳtle ǣr analyses; no unassigned general production scope follows.'),
    ('sources/audits/unit18-source/bt-p1053.jpg', 1053,
     'Bosworth–Toller Dictionary',
     'Personally read the masculine strong noun þeów, genitive -es, and weak alternative þeówa. This supports a separate strong servant noun paradigm; it does not by itself determine the historical analysis of Cook’s ðēowa manna.'),
    ('sources/audits/unit18-source/bt-p1054.jpg', 1054,
     'Bosworth–Toller Dictionary',
     'Initial full-page observation incorrectly read the quoted adjective as lacking r. Personal close-crop reinspection, prompted by the source editor, clearly shows mīnra þeówra manna WITH r. That earlier observation is withdrawn. The dictionary supports the distinction between selected strong-noun and adjective paradigms; the contextual history of Cook’s r-less phrase remains a bounded inference.'),
    ('sources/audits/unit18-grammar/bt_b0095.jpg', 95,
     'Bosworth–Toller Dictionary',
     'Personally read be-þurfan: present singular þearf/þearft, plural þurfon, dental preterite þorfte, and genitive or accusative government. The entry quotes We bicgaþ ða þing ðe we beþurfon from Genesis43.4,8. The selected genitive frame is supported, but is not claimed to be the only attested government.'),
    ('sources/audits/unit18-grammar/bt_d0240.jpg', 240,
     'Bosworth–Toller Supplement',
     'Personally read fore-secgan I with reference to the past and II referring to the future. This supports the past-mention sense required by Exercise46.6; a bare English gloss foretell would mislead.'),
    ('sources/audits/unit18-source/crawford1922-p190.png', 190,
     'Crawford1922, Old English Heptateuch',
     'Personally read Genesis43.10 oþre siðe, with final e on both words, and the surrounding arrival clause. This corroborates the supplied time phrase; it does not make the entire current composition an exact transcription. Nearby43.4/8 also attest the need-relative.'),
    ('sources/audits/unit18-source/crawford1922-p191.png', 191,
     'Crawford1922, Old English Heptateuch',
     'Personally read Genesis43.15 to Egypta lande to Iosepe. This corroborates the supplied ethnonym and name forms; the edition’s spelling and absence of editorial macrons remain distinct from the new Cook-controlled composition.'),
    ('sources/audits/unit18-source/crawford1922-p194.png', 194,
     'Crawford1922, Old English Heptateuch',
     'Personally read Genesis44.12 on Beniamines sacce, with the genitive name ending clearly present. The same clause prints he funde; this agrees with the separately documented earlier findan variant. These are corroborating excerpts, not an assigned new reading.'),
    ('sources/audits/unit18-source/crawford1922-p195.png', 195,
     'Crawford1922, Old English Heptateuch',
     'Personally read Genesis44.33 Læt þone cnapan faran ham ... ic beo þin þeowa for hine. The permissive frame and substitution for+accusative support the supplied48.2 construction. The page also has nominative Iosep in44.17. The current Cook-controlled model remains a declared new composition.'),
]
data['coordinator_additional_facsimile_views'] = [
    {'image_path': p, 'image_sha256': hashlib.sha256((ROOT / p).read_bytes()).hexdigest(),
     'source_work': work, 'printed_page': page, 'actually_viewed': True,
     'inspection_method': 'Personal view_image inspection of the complete facsimile page.',
     'observations': note}
    for p, page, work, note in observations
]
target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
crop = 'sources/audits/unit18-source/bt-p1054-adjective-detail.png'
data['coordinator_observation_corrections'] = [{
    'location': 'Bosworth–Toller1054 adjective entry quotation',
    'initial_incorrect_observation': 'The quotation has ðēowa manna without r.',
    'corrected_observation': 'The quotation reads mīnra þeówra manna, with r.',
    'trigger': 'The source editor challenged the coordinator’s full-page reading with a close crop.',
    'method': 'The coordinator personally viewed the retained close crop and withdrew the earlier claim.',
    'image_path': crop,
    'image_sha256': hashlib.sha256((ROOT / crop).read_bytes()).hexdigest(),
    'scope': 'A correction of the coordinator’s observation, not a source erratum or a change to Cook’s reading.'
}]
target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Recorded', len(observations), 'additional actual coordinator facsimile inspections and the separately identified close-crop correction; the Crawford title inspection is retained in its registry entry.')
