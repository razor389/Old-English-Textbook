"""Faithful prompt transcription from the actually inspected primary images."""
import hashlib
import json
import pathlib
import re
import unicodedata

OUT = pathlib.Path(__file__).parent
raw = {
37: '''Praise ye the Lord from (of) the heavens; praise him in the heights.
Praise ye him, all his angels; praise him, all his powers (mægen).
Praise ye him, sun and moon; praise him, all ye stars and light (lēoht).
Praise him, ye heavens of heavens, and ye waters that are above (ofer, 172) the heavens.
Let them praise [praise they] the name of the Lord; because he spake (gecweðan), and they were made (wyrcean); he commanded, and they were created (p. 190, l. 19).
He hath appointed them for ever and ever; he (om. hath) made (sęttan) a decree (bebod, 47), and (om. it) shall not pass (gewītan).
Praise the Lord from the earth, ye dragons (draca, 53), and all deeps (nēowolnes).
Fire and hail (hægel, 43); snow (snāw, 43) and ice (īs, 47); spirits of the storms (ȳst, 51. b) which fulfil (dōn) his word;
Mountains, and all hills (hyll, 43); fruitful (wæstmbǣre, 59) trees, and all cedars;
(Wild) beasts, and all cattle; serpents, and winged (gefiðred) fowl;
Kings of the earth, and all peoples; princes, and all judges of the earth;
Young (om. men), and maidens (fǣmne); old (om. men), with children;
Let them praise the name of the Lord; for the name of him alone is exalted (ūpāhębban), his glory (wuldor) is above (ofer, 172) the earth and heaven.
He exalteth the horn (horn, 43) of his people, the praise of all his saints (hālga, 53), of the children (bearn) of Israel (Israel), of the people drawing nigh (om. unto) him.''',
38: '''The king made a great ivory (elpenbǣnen, 57. 3) throne, and overlaid (oferwyrcean) it with (mid) the best gold.
There (om.) was a certain queen in those days in the south, called (hātan) Sheba (Saba).
Then she heard the fame (hlīsa) of Solomon (Salomones), and came from the southern (sūðerne, 59) boundaries to Solomon within Jerusalem, and her camels bore southern spices [herbs], and precious gems, and a quantity (unrīm) of gold (154. a).
The queen then (ðā) had speech with (wið) Solomon, and said (om. to) him whatsoever she thought in her heart (verb last).
Solomon then taught her, and told (sęcgean) her the meaning of all the words that (87. d) she asked (āscian) him.
Then the queen saw the wisdom of Solomon, and the great (mǣre) temple that (87. d) he (om. had) built, and the king’s manifold services.
She was so (tō ðan) greatly astonished (ofwundrian, 118), that she had no spirit more (furðor).
She said then to (tō) the king, True is the word that (87. d) I heard in my country concerning thee and thy wisdom (wīsdōm); but I would not believe before I (om. my)self saw (196. b) it (verb last).
Greater (micel, 66) is thy wisdom and thy work than the report (hlīsa) was (wǣre) that I heard.
Blessed (ēadig) are thy vassals and thy servants (ðēowa, 53), that always (simle) stand before (ætforan) thee, and hear thy wisdom.''',
39: '''Blessed (blētsian) be the almighty God, who (87. d) selected thee, and placed (gesęttan) thee over (ofer, 172) the kingdom of the Israelites (Israela), that thou (om. mightest) establish (sęttan) judgments and righteousness.
She gave (forgiefan) the king (om. a) hundred and twenty pounds (154. c) of gold (154. a), and (om. a) multitude of precious spices (wyrt) and of precious stones.
Solomon also gave the queen whatsoever she desired (giernan) of (æt) him; and she returned (gewęndan) again (ongēan) to her country with her retainers.
Solomon then was magnified (mǣrsian, 118) above (ofer, 166) all earthly kings; and all nations (ðēod) desired (gewilnian) to see [that they might see, 194. b] him, and hear his wisdom.
Whosoever buildeth upon (ofer, 166) this foundation (grundweall, 43) gold, or silver, or precious stones, or trees, straw (strēaw, 47) or chaff (ceaf, 47), every one’s (ānes gehwilces) work shall be manifested.
If the building (getimbrung, 51. 3) continues (ðurhwunian, 118), and withstands the fire (164. m), then shall the workman receive (om. a) reward (edlēan, 47) from (æt) God for his work (153. e).
No (183) eye can in this life see, nor any (183) ear (53. 2) hear, nor any (183) man’s heart conceive (āsmēan, 113), the things that God prepares (gearcian, 118) (om. for) those that love him.''',
40: '''The angel saluted Mary, and said that she was (194. b) filled (āfyllan, 113) with God’s grace [gift], and that God was with her (preposition last); and she was blessed (blētsian) among women.
My soul (om. doth) magnify (mǣrsian) the Lord, and my spirit (om. hath) rejoiced in God my Saviour.
For he regarded (gesēon) the humility of his handmaiden (ðīnen, 51. 5); verily (sōðlice), hence forth all generations (cnēoris) shall call (sęcgean) me blessed (ēadig).
For he that (sē ðe) is mighty hath done (om. to) me great things; and holy is his name.
And his mercy is (om. on those) fearing (161) him from (of) generation to (on) generation.
He hath put down (āweorpan) the powerful from (of) (om. their) seat, and lifted up (ūpāhębban) the lowly.
He hath filled the hungering (om. ones) with good (om. things), and the rich (rīce) he hath let go empty.
He hath accepted his servant (cniht) Israel, and remembered his mercy.
As he spake (sprecan) to (tō) our fathers, Abraham and his seed, for ever and ever.
Mary dwelt with her about (swilce) three months, and returned (gewęndan) then to her own house.''',
41: '''God was ever, and ever was his wisdom begotten of (of) him, and the wisdom is his Son, just as mighty as the Father.
The Spirit of God filleth all the circuit of the world, and he maintaineth all things.
He that doeth (wyrcean) my Father’s will, he is my brother, and my mother, and my sister.
We brought (bringan) no thing to this world, nor can we take (lǣdan) any (183) thing hence with us.
Ask (biddan), and (om. it shall) be given you; seek, and ye shall find; knock (cnucian, 118), and it shall be opened (om. to) you.
Our Father, thou which (87. d) art in heaven(s), be thy name hallowed.
Thy kingdom (rīce) come (tōcuman; verb first); thy will befall (geweorðan) on earth as (swā-swā) in heaven(s) (verb first).
Give (sęllan) us to-day our daily (dæghwāmlīc, 55) bread; and forgive (forgiefan) us our debts (gylt, 43), as we forgive (164) our debtors (gyltend, 43. 6).
And lead thou us not into (on, 172) temptation (costnung), but deliver us from evil.
Be it so.
What (hwilc) father will give to his child (164. a) a stone, if it asks (156. b; 159. b) bread of him?
God wrote (āwrītan) the old law (ǣ) with his finger (finger, 43) on the stone tables (tabele, 53).''',
42: '''The young man fell in love with the girl (p. 175, l. 20; cf. mīn lufu befielð on ðē, ‘my love falls on thee,’ ‘I fall in love with thee’).
I heard the voice of harpers harping with their harps; and they sung a new song before the throne, and before the four beasts; and no man could learn that song except the hundred and forty and four thousand.
I saw so great (om. a) company (męnigu), as no man can number (gerīman), of all nations and of every tribe (mǣgð), standing before the throne (ðrymsetl) of God, all clothed (gescrȳdan) with white garments (gegierela), and holding palm-twigs (palmtwīg, 47) in their hands.
And they sang with (om. a) loud (hlūd) voice, Be salvation (om. to) our God which sitteth upon (ofer, 166) his throne.
And all (om. the) angels stood round about [in circuit of] his throne, and bowed (ālūtan, 103) to God, thus saying,
Be (om. to) our God blessing and brightness, wisdom and thanksgiving (ðancung), dignity and strength, for ever and ever.
Foxes (fox, 43) have holes (hol, 47), and the birds of heaven nests (nest, 47); but (sōðlice) the Son of Man hath not where (hwǣr) he (om. may) lay (āhyldan, 113) his head.
The soldiers platted (windan, 104) (om. a) crown of (of) thorns (ðorn, 43), and placed on (172) his head, and a reed (hrēod, 47) in his right (om. hand), and bowed their knee before him, thus saying, Hale be thou, King of the Jews (Iudea).
And they spit (spǣtan, 113) on (on, 172) him, and took (om. a) reed and smote (bēatan) his head.''',
43: '''All [each] flesh is grass, and the glory (wuldor) of the flesh is like [as if] the blossom of herbs.
No man heard (183) his voice in (om. the) streets.
Cry (cleopian), and cease thou not, lift up (āhębban) thy voice like (swā-swā) (om. a) trumpet.
Lady, whither goest thou?
Thou doest ill (yfele).
He did ill, because he censured the princess, the king’s daughter.
They never learned arithmetic well.
You (plur.) will soon know what you do not yet know.
Play (with) ball!
I eat nothing, although other men eat and are merry.
I desire to learn [that I may learn] from you the knowledge that you have.
Choose which of them you (sing.) will.
Within a few hours, two educated and high-born men came toward him.
I woo the illustrious maiden.
We all say that no one here is (194. b) so acceptable to God as he.
At first he thought that he should be slain [that one should slay him].
We all fall at (tō) your (sing.) feet.
I (om. do) not believe that you are (194. b) my wife.
Where is my husband?
I lived eleven years in the land of the Egyptians.'''
}

def pages(ex, item):
    if ex == 37: return [22] if item == 1 else [22,23] if item == 2 else [23]
    if ex == 38: return [23] if item == 1 else [23,24] if item == 2 else [24]
    if ex == 39: return [24] if item == 1 else [24,25] if item == 2 else [25]
    if ex == 40: return [25] if item < 3 else [25,26] if item == 3 else [26]
    if ex == 41: return [26] if item < 8 else [26,27] if item == 8 else [27]
    if ex == 42: return [27] if item <= 7 else [28]
    return [28]

items = []
for ex, block in raw.items():
    for number, prompt in enumerate(block.splitlines(), 1):
        pp = pages(ex, number)
        items.append(dict(source_item_id=f'EX-XII-XIII-{ex:02}-{number:02}', source_id='cook_ex_1895',
            original_group='XII, XIII', original_exercise=ex, original_item=number,
            original_identifier=f'XII, XIII.{ex}.{number}', printed_pages=pp,
            pdf_pages_one_based=[p+8 for p in pp], prompt=unicodedata.normalize('NFC',prompt),
            origin_category='exact source with declared typographic normalization',
            disposition_proposal='assigned', evidence_refs=[f'U17-EX-P{p}' for p in pp],
            source_instruction_refs=['U17-EX37-INSTRUCTION'] if ex==37 else []))
counts={ex:len(block.splitlines()) for ex,block in raw.items()}
assert list(counts.values()) == [14,10,7,10,12,9,20]
data=dict(schema_version=1, source_id='cook_ex_1895',count=len(items),counts_by_exercise=counts,
    status='exact prompt transcription; assignment awaits the coordinator contract',
    verification='All seven course-map page images and all seven fresh 300 dpi primary page images personally viewed. English wording, punctuation, lexical hints, omission controls and references checked.',
    normalization=['Join printed line/page breaks and remove only typographic word-division hyphens.',
        'Collapse typographic spaces before punctuation; preserve lexical to-day, palm-twigs and high-born.',
        'Represent typographic apostrophes and quotation marks with Unicode curly characters; preserve all letters and printed quantities.',
        'Do not encode font weight or italics as linguistic content.'],
    instructions=[dict(instruction_id='U17-EX37-INSTRUCTION',original_exercise=37,
        original_text='[In this exercise, omit the article and the second personal pronoun throughout.]',
        printed_page=22,pdf_page_one_based=30,evidence_refs=['U17-EX-P22'],
        applies_to=[f'EX-XII-XIII-37-{n:02}' for n in range(1,15)])],
    source_anomalies=[],boundary_note='The joint printed heading XII, XIII remains joint. Exercises 44–48 are outside Unit 17. No reader-source derivation is inferred merely from the heading.',items=items)
(OUT/'exercises-prompts.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'count':len(items),'counts':counts},ensure_ascii=False))
