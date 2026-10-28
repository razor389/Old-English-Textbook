"""Retain the coordinator's actual clause-by-clause precontract readback.

These are author-preparation observations, not independent learner solutions.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
def read(path): return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))
def identity(path):
    raw = (ROOT / path).read_bytes()
    return {'path': path, 'sha256': hashlib.sha256(raw).hexdigest(),
            'sha256_normalized_lf': hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest()}

notes = {
    44: [
        'Jacob addresses his sons: both commands plural; us is the beneficiary and food depends on a quantity expression.',
        'Judah reports the chief’s oath, prohibition and exception; youngest brother remains the object brought with us. Modal permission differs from a prediction.',
        'Keep wilt last in the condition and omit a future auxiliary in the main clause. The bought things have an outer accusative role and a separately governed role in the need-relative.',
        'Keep the plural addressees, ill treatment with wið, the report recipient, and the partitive genitive after more.',
        'Retain both whether clauses, all of us, the answer, the negative knowing clause, willan, the desire’s genitive demonstrative and its expanded content clause.',
        'Retain the boy, both purpose relations, the relative need-frame, return home and the conditional wish of guilt. The two negative constructions have different scopes.',
        'The complete contrary-past arrival clause is supplied. Cook§176 requires the supported adverbial instrumental ōðre sīðe; the earlier ōðre sīð and ordinary-accusative proposals are superseded. Do not imply unrestricted anterior-result syntax.',
        'Keep plural must/do/take/bring, best fruits, vessels, dative recipient, honey and plural acorns. The selected æcernu agrees with the explicitly selected nominal system.',
    ],
    45: [
        'Both commands and the possessive addressees are plural; brother remains singular.',
        'The Lord is subject of a wish; make takes an object and agreeing adjective. Preserve gracious toward, return of the brother, the relative possession and present bereavement with genitive children.',
        'Retain presents, double money, Egyptian land and Joseph as destination. Names and ethnonym routes need explicit support; no invented general foreign-name declension.',
        'The steward is singular addressee; lead and prepare are singular commands. Retain our feast, plural eaters, with me and the complete noon expression.',
        'Follow Cook’s explicit impersonal command-passive target: dative recipient and unexpressed commanded content. Supply the complete frame.',
        'Retain arrival, fear, reciprocal speech, the reason involving money in sacks, passive leading hither, and both intended deprivation and enslavement. No object or possession may disappear.',
        'The request’s addressee is singular; hlystan takes the selected genitive speech complement. Retain earlier presence and the dative beneficiary of buying wheat.',
        'Retain trading, homeward state, opening sacks, finding money therein, and prior giving. English anteriority does not require an invented Old English perfect.',
        'Retain return of money, additional silver, the locally supported stranded instrumental mid with purpose infinitive, and ignorance of the person who put it into the sacks.',
    ],
    46: [
        'Retain the peace wish and plural negative command. The father’s possessive is ēowres with genitive fæder; the first ēower modifies God directly. Preserve treasure in the sacks.',
        'Wash has plural subject; giving has singular subject. Preserve their feet, their donkeys as dative recipients, and fodder as object.',
        'Retain setting forth presents and prospective Joseph-entry under the supplied ongēan ðætte frame; do not insert an English should auxiliary mechanically.',
        'Keep Joseph as recognizer/questioner and both alternative whether clauses: father’s health and continued life.',
        'The singular servant noun and our father are appositional; predicate healthy and still living remain distinct statements.',
        'Retain neuter this as requested, Benjamin, prior mention rather than prediction, dative hearer, and the wish of mercy with dative beneficiary.',
        'Retain Joseph’s command to the steward, plural sacks, wheat filling, each person’s money, and movement into that person’s own sack.',
        'Retain silver as cup material, wheat’s price, the relative giving with two participants, destination in the youngest person’s sack, and the steward’s compliance.',
        'Keep all three journey clauses and the subsequent instructions. Arise/go/catch/ask address the one steward; future catching uses the supplied target mood. Retain the question about requiting good with evil.',
    ],
    47: [
        'The stolen cup is subject of being precious; theft has plural addressees and the lord is dative. Preserve the forstelan hint.',
        'Retain compliance, passive capture, the full money statement and the theft question with both gold and silver. Questioned earlier theft uses the supported past subjunctive.',
        'Retain singular search command, passive wish of killing and the relative possessor located by with. The indefinite relative’s subjunctive is separately supported.',
        'Retain the free-choice with-whomever relation, singular servitude and plural blamelessness; the others are not part of the singular predicate.',
        'Retain search bounds from eldest to youngest, discovery in Benjamin’s sack and return to the city. Prior third-singular funde is valid and explicitly taught in Unit4; the earlier proposed correction was withdrawn.',
        'Retain Judah’s first entry with brothers, destination Joseph and all of them falling together before Joseph.',
        'Preserve Cook’s verb-last control within the question and plural addressees.',
        'The thief is singular and the released addressees plural. Preserve the relative theft and free state while going to the father.',
        'Keep singular past asker, plural asked group, earlier time and the two alternatives father or brother.',
        'Preserve old father, youngest brother with him, and him alone above all of us. Do not add a vowel-length mark to original ænne.',
        'Preserve present commandest; do not backshift its main verb. Keep bringing, seeing and knowing, the be-that phrase and the final report of not being spies.',
    ],
    48: [
        'Retain the oath’s dative father, report of return home, direct quotation with changed pronouns, exception condition and perpetual guilt toward the addressee.',
        'Keep permissive lǣtan with the lad as infinitive subject, going home with brothers, and the speaker’s offered servitude in his place.',
        'Retain negative daring, homeward infinitive, without the lad and preventive lest-clause about the father’s grief.',
        'Retain inability to conceal himself longer, expulsion of all others and the negative purpose excluding a foreign person.',
        'Retain weeping and crying, the instrumental loud voice, the address to brothers, Joseph’s identity and the question of continued life. Source clēopian quantity is preserved and separately supported.',
        'Retain plural fear prohibition with nothing, the impersonal grief wish and sale-content clause; God’s sending for their benefit is explicit, without importing an it-was cleft.',
        'Retain two-year duration, famine over all earth, five further years with source-requested ellipsis and neither plowing nor reaping. Support the whole numeral/ellipsis frame visibly.',
        'Retain quick plural going/telling/bidding, God’s appointment as lord over all Egyptians, and the two requested actions come/dwell in this land.',
        'Dōð swā preserves thus as manner; ðis was superseded. The plural negative-purpose clause remains intact.',
        'Retain both now-see/how and hear/what complements, plural addressees, and the speaker’s speech to them.',
    ],
}
prompts_path = 'sources/audits/unit18-source/exercises-prompts.json'
models_path = 'sources/audits/unit18-grammar/candidate-models.json'
prompts = read(prompts_path)['items']
models = {x['item_id']: x for x in read(models_path)['items']}
assert [len(notes[n]) for n in range(44,49)] == [8,9,9,11,10]
rows = []
for p in prompts:
    sid = p['source_item_id']
    ex, number = map(int, sid.rsplit('-',2)[1:])
    rows.append({'source_item_id': sid, 'exact_prompt': p['prompt'],
                 'candidate_model_at_readback': models[sid]['model'],
                 'coordinator_observation': notes[ex][number-1],
                 'status': 'clause meaning and explicit controls compared; dependency join and independent review still required'})
assert len(rows) == 47
report = {
    'chapter_id': 'ch18', 'reviewer': 'coordinator',
    'stage': 'precontract author preparation',
    'method': 'The coordinator read all47 exact prompts and proposed models, compared clause participants, temporal and modal relations, and original controls, then re-read the changed v6 items. Observations record actual readback; token or marker checks alone did not establish semantic coverage.',
    'input_identities': [identity(prompts_path), identity(models_path)],
    'items': rows,
    'independence_limit': 'The coordinator has read private models and author evidence and is ineligible as the fresh blind reviewer. These comparisons do not certify teaching sufficiency or replace source and independent review.'
}
(ROOT / 'sources/audits/unit18-coordinator/prompt-model-comparison.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Recorded47 actual coordinator prompt/model comparisons; no contract acceptance implied.')
