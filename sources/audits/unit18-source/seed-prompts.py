"""Exact Cook XII,XIII.44–48 English prompts; compare fresh primary images."""
import json
import pathlib
import re
import unicodedata

OUT = pathlib.Path(__file__).parent
blocks = {
44: '''Jacob (Iacob) said to his sons, Go and buy us a certain amount of food (męte).
Then said Judah (Iudas), The chief of the land swore oaths before us that we should not (mōtan) come before him, except we bring our youngest brother with us.
If thou wilt send him with us (verb last), we (om. will) go together and buy the things that (87. d) we need (beðurfan, 131).
Ye dealt ill (earmlice) with (wið) me, when ye said to him that ye had more (77) brethren (154).
The man asked (āscian) us all whether our father was living [lived] and whether we had brethren, and we answered him; we knew not that he would (willan) desire (giernan) that (156. a), that we should bring (lǣdan, 194. b) our brother thither.
Judah said, Send the boy with me, that we may (mugan) buy the things that we need, that we perish (forweorðan) not; except I bring him back home, may I be (193. a) guilty (scyldig).
Were it not for this delay [if this delay were not], we had [were, 188] come (om. a) second time (sīð, 176).
Then said Jacob, If ye needs (nīede, 176) must do so, do as ye will; take of (of) your best fruits in vessels, and carry (bringan) presents (om. to) the man, honey (hunig, 47) and acorns (æcern, 47).''',
45: '''Take your (plur.) brother and go to the man.
And my Lord make (gedōn) him gracious (glæd) toward (wið) you, that he may give (āgiefan, 196. f) you your brother, whom he hath with him; I am now bereft [despoiled] of my children (156).
Then they took the presents and double (twīfeald) money (feoh, 47), and went to the land of the Egyptians to Joseph (Iosep).
When he saw them, then said he to (tō) his steward (gerēfa, 53), Lead in these men, and prepare our feast, that they may (mugan) eat with me at noon (tō middes dæges, 158; 166. 1).
And he did as he was commanded [was commanded him; cf. p. 177, l. 10].
When they were there (ðǣr), then they became greatly frightened, and said to one another (betwēonan him), Because of (for) the money that we found in our sacks (sacc, 43), we (om. have) been led (62) in hither, that he may despoil us of our asses, and of our things, and enslave us (our)selves.
Then said they to (tō) the steward, O sir, we pray (biddan) thee that thou hear (hlystan, 156) our speech; we were here a while ago and bought wheat (hwǣte, 44) for ourselves (161; 184. a).
When we had trafficked (cēapian) and were on the way home (hāmweard wǣron), then we undid (undōn) our sacks; then we found the money therein which we had given (see ǣr, adv.).
Now we have brought it back, and also other silver to traffic with [with to traffic]; and we know not who put (dōn) it into (on, 172) our sacks.''',
46: '''Then said the steward, Peace be with you, fear (ondrǣdan, 184) ye not; your God and your father’s God (om. hath) given you treasure in your sacks.
And they washed (101) their feet, and he gave their asses provender [fodder].
They set (lęcgean) forth their presents, against that (ongēan ðætte) Joseph (om. should) enter.
Then Joseph recognized them, and asked them whether their father was hale, or whether he was living [lived].
Then said they, Thy servant (ðēow) our father is well (gesund); he is yet alive [liveth yet].
When Joseph saw his brother Benjamin, then said he, Is this (neut.) the lad, (om. of) whom (87. d) ye told me before (foresęcgean)? And he said, God have compassion on thee, my son.
Then Joseph commanded (bēodan, 164) his steward, and said, Fill their sacks with wheat, and put the money of each of them into (on, 172) his own sack.
And take my silver cup (læfel, 43), and the price (weorð, 47) of the wheat, which he gave thee, and put into the sack of the youngest; and he did so.
In (om. the) morning, as (ðā) they journeyed, and they were without (om. the) city, and had gone (faran) some part of the way, then said Joseph to (tō) his steward, Arise and go after these men, and when you have (196. b) overtaken [caught] them, then ask them why they would (willan) requite good with (mid) evil.''',
47: '''The cup, which ye stole (forstelan, 105), was very precious to my lord (hlāford).
He did as was commanded him, and when they were overtaken [caught], they said, The money that we found in our sacks we brought to thee from our country; thinkest (wēnan) thou that we (om. have) stolen (stelan) thy lord’s gold or his silver?
Look for [seek out] it; and let him be slain (ofslēan) with whom thou findest (195) it.
Then said he, With whomsoever I find it, let him be my servant, and let the others be blameless (clǣne).
And he sought from (fram) the eldest unto [until] the youngest; and he found the cup in Benjamin’s sack; and they turned back to the city.
And Judah went in first (fyrmest) with his brethren to Joseph, and they fell all together before Joseph.
And he said to (tō) them, Why would ye do so (verb last)?
Let him be my servant who stole the cup, and go ye free to your father.
Then said Judah, Thou askedst us before whether we had father or brother.
And we said, We have (om. an) old father, and he hath with him our youngest brother, and he loveth him alone (ænne) above (ofer) us all.
And thou commandest us that we (om. should) bring him to thee, that thou (om. mightest) see him, and know by (be) that that we were not spies (scēawere, 44).''',
48: '''And I swore oaths (om. to) my father that I (om. would) bring him home again to (tō) him, and said, Except I bring him again back to thee, let me be ever guilty (scyldig) toward (wið) thee.
My lord, let (lǣtan) the lad go home with his brethren, and (om. let) me be thy servant instead of (for, 172) him.
I dare not go home without the lad, lest I see my father’s grief.
Then could (mugan) not Joseph conceal (diernan, 113) himself longer, but he drove all the others out, that no foreign man (om. should) be among them.
And he wept and cried (clēopian) with a loud (hlūd) voice (160. 1); and he said to (tō) his brethren, I am Joseph; (om. doth) our father live yet (nū gīet)?
Fear ye (184) nothing, nor (om. let) it grieve (190) you that ye sold (sęllan) me into this kingdom; indeed (om. it was) for your benefit God sent me into the land of the Egyptians.
Now two years has been [was] famine over (172) all (om. the) earth, and (om. there) yet shall (om. be) five, in which one can (mugan) neither (89. a) plow (ęrian, 116) nor reap (rīpan, 102).
Go quickly to my father and tell him that God has set me as a (tō) lord (om. to) all (om. the) Egyptians; bid (bēodan) him (164) that he come to me and dwell in this land.
Do thus, that ye perish not.
Now ye see how it is with me, and ye hear what I say (sprecan) to (tō) you.''',
}
demands = {
44: [
('Direct plural commands after past speech; beneficiary us; partitive food amount.', 'Jacob; sons; go/buy; amount; food'),
('Narrative inversion; oath and finite content; negative permission; except-condition with youngest brother.', 'Judah; ruler; country; oath; appear before; youngest'),
('Conditional willingness; explicit final verb; relative thing-object and need-government; omit English future auxiliary.', 'send; accompany; together; buy; need'),
('Past main action; temporal/report clause; comparison/quantity more with plural brethren.', 'treat badly; wið addressee; more brothers'),
('Two coordinated indirect questions; reporting and ignorance; desire with genitive demonstrative and following content clause.', 'ask all; live; brothers; answer; know; desire; bring thither'),
('Singular command; two purpose clauses; negative perish; except-condition and first-person self-imprecation.', 'send boy; buy; need; perish; return home; guilty'),
('Unreal past condition and anterior come-construction; accusative occasion second time.', 'delay; second; occasion; come'),
('Conditional necessity; free-choice manner; partitive source after of; direct and recipient objects.', 'needs; best fruits; vessels; carry; presents; honey; acorns')],
45: [
('Plural commands with singular shared brother and directional recipient.', 'take; your plural; brother; go'),
('Optative make with object predicate; wið recipients; purpose giving; relative possessive clause; deprivation genitive.', 'Lord; gracious; give back; brother; bereft; children'),
('Coordinated past actions; adjective agreement with money; Egyptian territory and named goal.', 'take; presents; double; money; Egyptians; Joseph'),
('Temporal ðā correlation and nested direct commands/purpose; exact noon expression.', 'see; steward; lead in; prepare feast; eat; noon'),
('Comparative manner clause and impersonal passive with dative person; exact parallel177.10.', 'do; command; him as recipient not subject'),
('Temporal correlation; becoming frightened; reciprocal speech; causal money phrase; passive lead and purpose deprivation/enslavement.', 'there; frightened; reciprocal; sacks; lead in; asses; possessions; enslave'),
('Respectful address; request finite content; listen with governed object; past purchase and benefactive reflexive.', 'pray; listen; speech; earlier; wheat; ourselves'),
('Anterior trading and state heading home; opening sacks; earlier payment; ǣr controls sequence.', 'trade; homeward; undo; sacks; therein; pay'),
('Restored money and added silver; infinitive purpose with stranded instrumental relation; indirect question.', 'bring back; silver; trade with; know; put into')],
46: [
('Greeting wish; negative plural command and reflexive fear; compound possessor; omit hath.', 'peace; fear; father’s God; give; treasure; sacks'),
('Coordinated past actions; feet plural; recipient asses and direct fodder.', 'wash; feet; asses; fodder'),
('Set forth presents; prospective ongēan ðætte clause, omit should; retain lęcgean hint.', 'set; presents; enter'),
('Recognition plus alternative indirect questions with adjective and lexical live.', 'recognize; hale; live; father'),
('Honorific servant; predicative healthy; lexical live with gīet.', 'servant; healthy; alive'),
('Temporal seeing; neuter demonstrative with male lad; direct-object relative; optative mercy with dative recipient.', 'Benjamin; lad; tell before; mercy; son'),
('Command recipient; plural sacks with genitive contents; distributive possessors and own sack; on goal.', 'command; steward; fill; wheat; money; each; own'),
('Elliptical command object; material silver-cup phrase; price with dependent wheat; relative giving; youngest substantive.', 'cup; silver; wheat price; take; put'),
('Temporal journey; static outside and anterior progress; pursuit command; prospective temporal caught-clause; indirect why question.', 'morning; outside city; part of road; arise; follow; overtake; requite good with evil')],
47: [
('Fronted cup and past theft relative; precious with dative standard.', 'cup; steal; precious; lord'),
('Dative impersonal command; passive catching; object money fronting with relative; return from country; supposition content.', 'command; catch; money; sack; country; think; gold; silver; steal'),
('Seek imperative; passive death wish; indefinite/conditional relative with find.', 'seek; slay; with whom; find'),
('Free-choice with whomsoever; first-person finding; third-person jussives with servant and blameless predicates.', 'find; servant; others; blameless'),
('Range from eldest until youngest; finding within sack; return to city.', 'seek; eldest; youngest; Benjamin’s; sack; turn back'),
('Entry in first position; accompaniment; collective falling before person.', 'Judah; first; brethren; Joseph; fall together'),
('Past report and direct question with modal willingness; explicit final lexical verb.', 'say; why; will; do so'),
('Identifying theft relative; servant jussive; plural dismissal with free predicate.', 'servant; steal; cup; go free; father'),
('Past speech; recalled prior asking; indirect whether alternatives.', 'ask before; father; brother'),
('Reported direct speech with present have; omit indefinite article; youngest brother; singular alone and comparative overtopping.', 'old father; youngest; love; him alone; above all'),
('Source literal present commandest; command content and purpose; discernment from evidence; negative spies predicate.', 'command; bring; see; know by that; spies')],
48: [
('Oath with dative father; future-in-past without would; embedded quoted except-condition and continuing guilt wish.', 'swear; father; bring home; again; ever guilty; toward'),
('Let plus accusative and infinitive; coordinated first-person predicate without repeated let; substitution for.', 'lord; lad; go home; brethren; servant instead'),
('Negative dare with infinitive; without person; apprehensive lest-clause.', 'dare; return home; lad; see; father’s grief'),
('Negative ability with reflexive concealment; longer comparative; expulsion and purpose no foreign man.', 'can; conceal; longer; drive out; others; foreign'),
('Past crying; instrumental/manner voice; reported identity and direct yes/no question; omit do-support.', 'weep; cry; loud voice; Joseph; father; live yet'),
('Negative fear and grief commands; finite cause/content; sale into realm; explanatory benefactive providence.', 'fear; grieve; sell; kingdom; benefit; God; send'),
('Elapsed and prospective duration; source omit be under shall; locative scope and impersonal one; neither/nor agriculture.', 'two/five years; famine; earth; can; plow; reap'),
('Plural message command; appointment as lord; dative Egyptians; command content with coming/dwelling.', 'quickly; father; God; set as lord; Egyptians; bid; come; dwell'),
('Plural do command with negative purpose clause.', 'do thus; perish'),
('Present perceiving and indirect manner; relative speech-object; addressee tō.', 'now; see; how things stand; hear; say')],
}
page_map = {
44: [[29]]*8,
45: [[29],[29,30]]+[[30]]*7,
46: [[30],[30,31]]+[[31]]*7,
47: [[31],[31,32]]+[[32]]*9,
48: [[32],[32],[32],[32,33]]+[[33]]*6,
}
items=[]
hint_records=[]
for ex,block in blocks.items():
    rows=block.splitlines()
    assert len(rows)==len(demands[ex])==len(page_map[ex])
    for n,(prompt,pages,(construction,lexical)) in enumerate(zip(rows,page_map[ex],demands[ex]),1):
        sid=f'EX-XII-XIII-{ex:02}-{n:02}'
        hint_ids=[]
        for j,m in enumerate(re.finditer(r'\([^)]*\)|\[[^]]*\]',prompt),1):
            hid=f'U18-HINT-{ex:02}-{n:02}-{j:02}'
            hint_ids.append(hid)
            raw=m.group()
            kind='literal bracketed rephrasing' if raw.startswith('[') else 'original parenthetical hint'
            if 'om.' in raw:kind='English omission control'
            elif 'verb last' in raw:kind='explicit word-order control'
            elif any(s in raw for s in ['plur.','neut.']):kind='number/gender control'
            hint_records.append(dict(hint_id=hid,source_item_id=sid,exact_text=raw,kind=kind,
                character_start=m.start(),character_end=m.end(),printed_pages=pages,
                evidence_refs=[f'U18-EX-P{p}' for p in pages],
                support_scope='Retain as original supplied source instruction; hinted form is not independent productive mastery without an explicit teaching record.'))
        items.append(dict(source_item_id=sid,source_id='cook_ex_1895',original_group='XII, XIII',
            original_exercise=ex,original_item=n,original_identifier=f'XII, XIII.{ex}.{n}',
            printed_pages=pages,pdf_pages_one_based=[p+8 for p in pages],
            prompt=unicodedata.normalize('NFC',prompt),origin_category='exact source with declared typographic normalization',
            disposition_proposal='assigned',evidence_refs=[f'U18-EX-P{p}' for p in pages],
            source_instruction_refs=hint_ids,semantic_and_construction_demands=construction,
            lexical_sense_demands=lexical.split('; '),
            dependency_status='Reconcile actual forms, senses and constructions against current registers and grammar/source packets; no mastery inferred from familiarity of a headword.'))
data=dict(schema_version=1,source_id='cook_ex_1895',count=len(items),
    counts_by_exercise={str(ex):len(block.splitlines()) for ex,block in blocks.items()},
    status='Exact image-checked source transcription; assignment awaits coordinator contract.',
    verification='All five course-map images and all five fresh300dpi primary page images29–33 personally viewed. Page32 additionally viewed at original resolution. English, numbers, lexical hints, letters, length marks, omission controls, brackets and references checked.',
    normalization=['Join printed line/page breaks and remove only typographic word-division hyphens.',
        'Collapse typographic spaces before punctuation; retain all lexical hyphens.',
        'Represent typographic apostrophes and quotation marks with Unicode curly characters; preserve letters and printed quantities.',
        'Do not encode font weight or italics as linguistic content.',
        '47.1: omit the isolated apostrophe-like print/scan anomaly between lord and its opening hint-parenthesis; preserve the mark in the anomaly record and primary image. No linguistic character or instruction is removed. Its physical origin is not asserted.'],
    instructions=[],source_anomalies=[
        dict(source_item_id='EX-XII-XIII-47-11',observation='The source prints present commandest, not commandedst. Preserve that wording in the prompt and explain any contextual translation choice explicitly.'),
        dict(source_item_id='EX-XII-XIII-47-01',observation='The facsimile has an isolated apostrophe-like print/scan anomaly immediately after lord, before (hlāford). No quotation is opened and no word contains it. The declared prompt normalization removes that mark; the source image retains it. The available evidence does not distinguish a printing artifact from a scan artifact; no linguistic Cook error is asserted.',image_path='sources/audits/unit18-source/ex-p31.png'),
        dict(source_item_id='EX-XII-XIII-45-03',observation='Exact hint twīfeald has long ī. Do not silently substitute twēfeald.'),
        dict(source_item_id='EX-XII-XIII-47-10',observation='Exact hint ænne has unmarked æ. Do not infer or add a length mark.'),
        dict(source_item_id='EX-XII-XIII-48-07',observation='The exact neither reference is89.a, not83.a.')],
    boundary_note='This is a sustained English Joseph composition sequence. It is not an Old English Joseph reading from Cook’s reader. The heading remains joint XII, XIII.',items=items)
(OUT/'exercises-prompts.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'exercise-hints.json').write_text(json.dumps(dict(schema_version=1,count=len(hint_records),records=hint_records,
    source_note='Original hints and bracketed rephrasings remain literal; modern supplied frames require separate declared records.'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'prompts':len(items),'hints':len(hint_records),'by_exercise':data['counts_by_exercise']}))
