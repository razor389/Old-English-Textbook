"""Assemble the Unit 17 learner master from the committed contract and authored prose.

This helper writes only chapters/ch17/student.md and build/u17-learner-*.
The contract and all source/proposal packets are read-only inputs.
"""
from pathlib import Path
from collections import defaultdict
import json
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
C = json.loads((ROOT / 'chapters/ch17/coverage.json').read_text(encoding='utf-8'))
TEACH = {t['teaching_id']: t for t in C['teaching_records']}
LEX = {l['lemma_id']: l for l in C['lexical_inventory']}
FORMS = {r['form_id']: r for l in C['lexical_inventory'] for r in l['forms']}
SENSES = {r['sense_id']: r for l in C['lexical_inventory'] for r in l['senses']}
MATRICES = {m['matrix_id']: m for m in C['display_plan']['matrices']}
TASKS = {t['task_id']: t for t in C['assigned_items']}
P = {p['paradigm_id']: p for p in C['paradigms']}
OUT, EMITTED = [], set()

def put(text=''):
    OUT.append(text.strip() + '\n\n')

def mark(tid):
    if tid in TEACH and tid not in EMITTED:
        put('<!-- teaching: ' + tid + ' -->')
        EMITTED.add(tid)

def mark_records(form_ids=(), sense_ids=(), feature_ids=()):
    current_forms, current_senses = set(form_ids), set(sense_ids)
    def eligible(tid):
        if tid not in TEACH:
            return False
        t=TEACH[tid]
        if t['kind'] in {'complete_bounded_paradigm','visible_whole_frame_verbal_help',
                         'visible_dictionary_references','visible_exact_source_controls'}:
            return False
        if t.get('form_ids') and not set(t['form_ids']) & current_forms:
            return False
        if t.get('sense_ids') and not set(t['sense_ids']) & current_senses:
            return False
        return True
    for fid in form_ids:
        for tid in FORMS.get(fid, {}).get('teaching_ids', []):
            if eligible(tid):
                mark(tid)
    for sid in sense_ids:
        for tid in SENSES.get(sid, {}).get('teaching_ids', []):
            if eligible(tid):
                mark(tid)
    for t in C['teaching_records']:
        if set(t.get('feature_ids', [])) & set(feature_ids):
            mark(t['teaching_id'])

def clean(s):
    """Typography only for new explanatory prose, never exact prompts or tables."""
    s = s or ''
    s = re.sub(r'(?i)\bCook\s*§?\s*(\d+)', r'Cook §\1', s)
    s = re.sub(r'\b(in|of|with|under|before|after|from|and|the|selected|source|printed|note|complete|supplied)(?=\d)', r'\1 ', s)
    s = re.sub(r'(?<=\d)(?=[A-Za-z])', ' ', s)
    s = re.sub(r'\b([123])\s*sg\b', lambda m: {'1':'first','2':'second','3':'third'}[m[1]]+' singular', s)
    s = re.sub(r'\b([123])\s*pl\b', lambda m: {'1':'first','2':'second','3':'third'}[m[1]]+' plural', s)
    s = s.replace('144000', '144,000').replace('120pounds', '120 pounds')
    return s

def matrix(mid):
    m = MATRICES[mid]
    put('<!-- table: ' + mid + ' -->')
    rows = [m['headers'], ['---'] * len(m['headers'])] + m['rows']
    put('\n'.join('| ' + ' | '.join(r) + ' |' for r in rows))

def vocab(lemma_id, supplied=False):
    records = [t for t in C['teaching_records'] if t.get('lemma_id') == lemma_id
               and t['kind'] == 'bounded_lexical_sense'
               and (t.get('knowledge_status') == 'supplied') == supplied
               and t['teaching_id'] not in EMITTED]
    if not records:
        return False
    for t in records:
        mark(t['teaching_id'])
    glosses = list(dict.fromkeys(clean(t.get('contextual_gloss') or t['gloss']) for t in records))
    word = LEX[lemma_id]['display_headword']
    put('**' + word + '** — ' + '; '.join(glosses) + ('. Supplied reference only.' if supplied else '.'))
    return True

NOUN_NOTES = {
    'heanes': 'Use the plural for heights or the highest places. The singular column gives reference forms only; singular height is not required from memory here. The stem is hēaness-, with doubled s before every ending and with e retained.',
    'maegen': 'Retain the full stem mægen- in mægenes, mægene, mægena and mægenum. The exceptional nominative/accusative plural is mægnu. In the praise catalogue the plural denotes heavenly powers; the singular denotes power or strength.',
    'naedre': 'The selected spelling is nædre, with short æ and one d. The source also gives næddre. Add the weak feminine endings to nædr-.',
    'halga': 'This is a weak masculine noun, saint or holy one. Its genitive plural is hālgena. Keep it distinct from the adjective hālig and its genitive plural hālgra.',
    'horn': 'This table selects masculine horn, plural hornas. In Cook 37.14 the horn represents strength or dignity; retain the image when translating.',
    'cwen': 'The selected accusative singular is endingless cwēn; the genitive and dative have cwēne. The ordinary-class accusative cwēne is also a defensible variant, but the contrast exercise explicitly asks for cwēn. Queen and princess are separately assigned contextual meanings.',
    'hlisa': 'Fame is ordinarily singular in this passage. A report or account can be treated as an individual item. The complete table serves those stated meanings; context determines which is intended.',
    'olfend': 'Retain e in the stem olfend-. The final letters -end do not make this an agent noun of the gyltend pattern.',
    'andgiet': 'Learn the four singular cases for meaning and understanding. These are abstract uses of a familiar neuter class. Plural forms and separate count meanings are outside this unit; the absence of a plural column does not mean that the word has no plural.',
    'thenung': 'The selected singular oblique ending is -e. Nouns in -ung can also have -a in the dative, and sometimes in the genitive and accusative; retain such a form when it is given in a source.',
    'theowa': 'This is weak ðēowa, with nominative/accusative plural ðēowan. Do not substitute the plural of the separate strong form ðēow.',
    'wisdom': 'Retain both lengths in wīsdōm. The final member follows the familiar masculine dōm pattern; only abstract singular wisdom is used here.',
    'getimbrung': 'The noun is feminine. A pronoun resuming the building must agree with that grammatical gender.',
    'eare': 'This weak neuter has ēare in both nominative and accusative singular. The other singular cases end in -an. Its genitive plural contracts to ēarna; the dative plural is ēarum.',
    'eadmodnes': 'Use ēaðmōdness- before the endings, with doubled s and retained e. Only abstract singular humility is assigned.',
    'thinen': 'The oblique stem is ðīnenn-, with doubled n and retained e: ðīnenne. The nominative singular conceals the doubling.',
    'cneoris': 'Use cnēoriss- before endings: cnēorisse, cnēorissa and cnēorissum. The assigned meaning is generation.',
    'cniht': 'The meaning required here is servant. It is distinct from the earlier occurrence meaning youth; familiarity with the word in that passage did not supply this new meaning.',
    'gylt': 'Retain debt in translating the prayer. Its moral force comes from the prayer’s context; an ordinary noun ending does not by itself express that interpretation.',
    'gyltend': 'This masculine agent noun has selected nominative/accusative plural gyltende and genitive plural gyltendra. An endingless nominative/accusative plural is also recorded. The selected pattern is not the ordinary -as plural.',
    'finger': 'The second-syllable vowel disappears before an ending: finger, but fingres and fingre. Use the oblique stem fingr-.',
    'tabele': 'The weak feminine stem is tabel-. Retain e in the dative plural tabelum.',
    'hearpere': 'The final -e of the headword gives way to endings on hearper-. The genitive plural is hearpera, as in the familiar masculine -ere class.',
    'weorthscipe': 'This masculine -e noun retains -e in the nominative, dative and accusative singular. The genitive has -es on weorðscip-. Only singular honour or dignity is assigned here.',
    'maegth-tribe': 'Long ǣ distinguishes mǣgð, tribe or nation, from short-vowel mægð, maiden. Keep both the length and this noun’s feminine pattern.',
    'thrymsetl': 'Retain the source spelling ðrymsetl. The final stem setl is heavy, so the nominative/accusative plural has no -u.',
    'palmtwig': 'Long ī makes palmtwīg a heavy neuter. The nominative/accusative plural is palmtwīg.',
    'cneo': 'The endingless singular cnēo has cnēow- before endings. Its nominative/accusative plural is cnēowu.',
    'hol': 'The short vowel and single final consonant give the light neuter pattern: nominative/accusative plural holu.',
    'nest': 'The final consonant cluster makes the stem heavy. The nominative/accusative plural is nest.',
    'hreod': 'Long ēo makes hrēod a heavy neuter. Its nominative/accusative plural is endingless.',
    'biema': 'Retain the source spelling biema, without adding a length mark. It follows the weak masculine pattern.',
    'stan': 'The full stone paradigm is available for the gifts, building materials and bread-or-stone contrast.',
}

VERB_NOTES = {
    'herian': 'This weak verb follows the nęrian type. The present has hęrie, hęrest and hęreð, with -i- in plural hęriað. The preterite stem is hęred-. The command is singular hęre, plural hęriað; the present subjunctive is singular hęrie, plural hęrien. Thus hęriað can be a statement or a command, whereas hęrien expresses a plural wish in the praise exercise.',
    'gecwethan': 'The present second and third singular have i. The preterite contrasts singular æ with ǣ in the second singular and plural, and changes ð to d. Retain the lexical prefix ge-.',
    'up-ahebban': 'The present stem has doubled bb, but the second and third singular are ūpāhęfst and ūpāhęfð. The preterite has hōf and the past participle hafen, with ūpā- retained. Raising can be physical or, in the explicitly taught exaltation sense, an increase in standing.',
    'oferwyrcean': 'The selected present uses -ean and plural -eað. The weak preterite has worht-. Retain ofer- throughout. The thing overlaid is accusative; the covering material follows mid with the dative.',
    'gesettan': 'Retain tt before a vowel. The selected present second singular has -tst and third singular -tt. The weak dental preterite merges with the final t; it does not add a separate -tde sequence.',
    'giernan': 'This long-stem weak verb has present -st and -ð and a preterite in -de. The thing desired or person sought in marriage is genitive. Æt with the dative names the person from whom something is requested.',
    'maersian': 'The weak -ian pattern has present singular -ie, -ast, -að and plural -iað; its preterite uses -ode, -odest, -odon. The participles have -iende and -od. In the passive, mǣrsod means celebrated or exalted.',
    'gewilnian': 'Use the weak -ian endings: present -ie, -ast, -að, -iað; preterite -ode, -odest, -odon. A following ðæt clause can express what is desired.',
    'thurhwunian': 'Use the weak -ian endings: present -ie, -ast, -að, -iað; preterite -ode, -odest, -odon. The meaning is remaining or lasting.',
    'withstandan': 'The present second and third singular have stęntst and stęnt. The preterite has stōd and stōdon, without the present stem’s n. The thing resisted is dative.',
    'gearcian': 'The verb is unprefixed gearcian. Use the weak -ian endings: present -ie, -ast, -að, -iað; preterite -ode, -odest, -odon. The things prepared are accusative and their beneficiaries dative.',
    'afyllan': 'Double ll before a vowel, but use single l in āfylst, āfylð and āfylde. The selected past participle is āfylled; contracted āfyld is also recorded. The filled entity is accusative in an active clause and nominative in a passive; mid with the dative names the contents.',
    'aweorpan': 'The strong stems alternate eo, ea, u, o. Present second and third singular have ie; the preterite second singular uses the same u-stem as the plural. The displaced person is accusative and of with the dative gives the source.',
    'awritan': 'The strong vowel sequence is ī, ā, i, i. Present second singular has -tst and the selected third singular -tt; a source variant has single -t. There is no new vowel mutation in these two present forms.',
    'alutan': 'The strong stems alternate ū, ēa, u, o. Present second and third singular change ū to ȳ and have -tst and selected -tt; single -t is also recorded. The actor bows; dative Gode names the one bowed to.',
    'windan': 'The strong stems alternate i, a, u, u. Stem d becomes t before the second- and third-singular present endings. The thing plaited is accusative; of with the dative names its material.',
    'spaetan': 'Retain long ǣ. The t-stem has selected present third singular -tt and weak preterite -tte, -ttest, -tton. In the exercise, on takes the accusative person spat upon.',
    'taelan': 'This long-stem weak verb has a preterite in -de. The person blamed is accusative. In the reading, tǣlst is second singular present indicative.',
    'biegan': 'Use the selected long-diphthong stem bīeg- with weak endings. This transitive verb takes the bent knee as an accusative object. Keep it distinct from the intransitive bowing verb.',
    'gemunan': 'This preterite-present verb has present first/third singular geman, second singular gemanst and plural gemunon. Its dental preterite uses gemund-. The thing remembered is accusative.',
    'thencan': 'The selected headword variant is ðęncean. Its weak preterite ðōht- changes the vowel and replaces c before the dental ending. In the Sheba exchange, a free-choice expression gives what the queen had thought.',
}

GRAMMAR = {
    'NEW-U17-GRAM-U17-PARTICIPLE-HUMAN-NOMINALIZATION': ('Participles naming people', 'A present participle can describe people without an expressed noun. Its ending gives the phrase’s role in the surrounding clause, while the verb inside the participle retains its own complements. In hine ondrǣdendum, the dative plural names the beneficiaries of mercy; accusative hine names the person feared. In ðā hyngrendan, the article and weak accusative plural identify hungry people as a direct object. These are nonfinite descriptions, not present-tense assertions. Learn these human uses of ondrǣdende and hyngrende; no personal finite conjugation of hyngran is added.'),
    'NEW-U17-GRAM-U17-PREDICATE-PARTICIPLE-PLURAL': ('Past participles in a predicate', 'A past participle with a form of be can remain uninflected or take the strong masculine agreement endings, regardless of the subject’s gender. The selected plural predicates in Cook 37.5 are worhte and gesceapene. They belong with wǣron; they are not finite weak preterites. The uninflected bases worht and gesceapen are also possible with plural subjects. The two small displays in the preceding section distinguish the base from the selected agreeing plural.'),
    'NEW-U17-GRAM-U17-HERIAN-OBJECT': ('Praise: statement, command and wish', 'Hęrian takes the praised person or thing in the accusative. A plural command addresses the beings named in the catalogue; a third-person wish has hīe as subject and hęrien as verb. The identical indicative and imperative form hęriað does not make their functions identical.'),
    'NEW-U17-GRAM-U17-GIERNAN-REQUEST-WOO': ('Requesting and seeking in marriage', 'Giernan governs a genitive of the requested thing or marriage partner. Æt with the dative gives the person asked. In Cook 39.3, keep the outer accusative role of eall ðæt separate from the role represented by invariant ðe in its relative clause. In Cook 43.14, seeking the maiden in marriage requires her genitive form.'),
    'NEW-U17-GRAM-U17-FILLING-MATERIAL': ('Contents and covering', 'Āfyllan takes the filled entity in the accusative and its contents after mid with the dative. In a passive, the filled entity becomes the nominative subject. Oferwyrcean has a similar case arrangement for a different act: the throne is overlaid with gold. Learn each verb’s meaning together with its complements.'),
    'NEW-U17-GRAM-U17-ONFON-PERSON-DATIVE': ('Receiving a thing or a person', 'The selected onfōn construction takes the dative: edlēane for a received reward, and his cnihte Israel for the servant accepted into care. Accusative receiving constructions exist elsewhere; these exercises specifically practise the dative frame.'),
    'NEW-U17-GRAM-U17-SECGAN-PREDICATE': ('Calling someone blessed', 'Sęcgan can take an object and an adjective that agrees with it: the generations call Mary blessed. In Cook 40.3, mē is the first-person singular object, ēadige its feminine accusative singular predicate, and sęcgað agrees with the plural generations. The present verb has future reference in the prediction.'),
    'NEW-U17-GRAM-U17-VERB-LEXICAL-EXTENSIONS': ('New meanings of familiar verbs', 'Dōn can mean fulfil or carry out a word or command; healdan can mean sustain all things; sęcgan can mean call or declare someone to be something. Learn those meanings explicitly. Wyrcean retains the familiar work or perform sense with the Father’s will and the make or build sense with a foundation.'),
    'NEW-U17-GRAM-U17-VIRTUAL-RELATIVE': ('Indefinite relatives and the subjunctive', 'A relative clause can describe an indefinite or possible situation: the one you wish to choose, or a place where one might lay one’s head. Such clauses can take the subjunctive. Wille in Cook 43.12 is second singular present subjunctive; āhylde in Cook 42.7 is third singular present subjunctive. The construction does not make every relative subjunctive, and English may need not be translated by an extra modal.'),
    'NEW-U17-GRAM-U17-LEORNIAN-SOURCE': ('Learning from someone', 'Of with the dative can name the person from whom one learns in Cook 43.11. Gewilnian introduces the desired content with ðæt. The embedded ic takes first singular leornie, while plural gē takes habbað. The separate clauses keep their own subjects and agreement.'),
    'NEW-U17-GRAM-U17-PLEGIAN-INSTRUMENT': ('Playing with an object', 'Plegian in the ordinary play sense takes mid with the dative instrument. The ball exercise therefore uses the familiar dative ðoðore. The reading’s act or perform sense is supplied separately.'),
    'NEW-U17-GRAM-U17-TEMPORAL-BEFORE': ('Before a past event', 'In Cook 38.8, nolde expresses a former unwillingness to believe. The seeing is still prospective from that earlier viewpoint: the before-clause uses first singular past subjunctive gesāwe. Its spelling alone does not make it second singular indicative. Retain self and follow the requested final position of the verb.'),
    'NEW-U17-GRAM-U15-NEGATIVE-CONCORD': ('Negative concord', 'Preverbal ne can combine with nān or another negative word to express one negation. In the coordinated eye, ear and heart sentence, the first mæg can govern the following infinitives as well. Identify the subject of each part; repeated negative words do not make it affirmative. Use the ordinary ne witon for we do not know. The reading’s contracted nāst is supplied separately.'),
    'NEW-U17-GRAM-U17-PAST-TENSE-SELECTION': ('Choosing a past tense', 'The simple preterite can correspond to English simple past, present perfect or past perfect when the context establishes the time relation. Cook §188 explicitly permits this range. An English has or had therefore does not always require a separate auxiliary in Old English. Follow an explicit omission instruction; elsewhere choose a construction whose exact forms and intended time relation you know.'),
    'NEW-U17-GRAM-U17-GENITIVE-REWARD-CAUSE': ('The grounds for a reward', 'A genitive dependent on a reward can express its grounds: his weorces, for his work. In Cook 39.6, edlēane is dative because it is received with onfōn; the work-genitive depends on the reward, and æt Gode gives its source.'),
    'NEW-U17-GRAM-U17-PERSONAL-ADJECTIVE-GROUPS': ('Adjectives naming people', 'The selected adjectives geong, eald, mihtig, ēaðmōd and rīce can name young, old, powerful, humble and rich people. Use weak masculine plural forms in the assigned address and object expressions. Geongan and ealdan address people without an expressed men or article under Cook 37’s instruction. Ðā mihtgan, ðā ēaðmōdan and ðā rīcan are accusative plural objects. These people meanings are distinct from merely describing a noun; this unit assigns these particular plural uses, not an unrestricted noun declension.'),
}

def teach_grammar(tid):
    title, text = GRAMMAR[tid]
    put('### ' + title)
    mark(tid)
    if tid.endswith('PERSONAL-ADJECTIVE-GROUPS'):
        mark('NEW-U17-VOC-MIHTIG-U17-POWERFUL-PEOPLE')
        mark('NEW-U17-VOC-EADMOD-U17-HUMBLE-PEOPLE')
    put(text)

def pretty_analysis(a):
    conv = {'nom':'nominative','gen':'genitive','dat':'dative','acc':'accusative','voc':'vocative',
            'sg':'singular','pl':'plural','m':'masculine','n':'neuter','f':'feminine',
            'present_participle':'present participle','past_participle':'past participle',
            'infinitive':'infinitive','imp':'imperative','pres':'present','pret':'preterite'}
    parts = []
    for key in ['nonfinite','mood','tense','person','case','gender','number','declension','strength']:
        if key in a:
            value = a[key]
            if key == 'person':
                value = {1:'first person',2:'second person',3:'third person'}.get(value,str(value))
            else:
                value = conv.get(str(value),str(value).replace('_',' '))
            if value not in parts:
                parts.append(value)
    return ', '.join(parts)

def source_markers(t, support=None):
    if support:
        mark_records([support['form_id']] if support.get('form_id') else [],
                     [support['sense_id']] if support.get('sense_id') else [],
                     [support['feature_id']] if support.get('feature_id') else [])
        sid = support.get('support_id','')
        mark(sid)
    short = f"{t['original_exercise']}.{t['original_item']}"
    for r in C['teaching_records']:
        if short in r.get('source_items',[]) and r['kind'] in {
            'supplied_whole_frame','visible_bounded_context_sense','visible_exact_expression_reference'}:
            mark(r['teaching_id'])

CONTROL_NOTES = {
    '37.5': '“Praise they” calls for a third-person wish with an expressed subject. Cook’s page 190, line 19 begins the said/made example; commanded/created follows on line 20. Use the passive auxiliary with the appropriate predicate participles.',
    '37.6': 'Omit a separate word for hath. In the final coordinated predicate, the decree is the understood subject; God is not the thing that passes away. The supplied present gewīt has future reference.',
    '37.8': 'The storm fulfils his word. Keep that meaning of dōn distinct from a general act of making.',
    '37.9': 'The described trees are addressed directly; use the weak plural adjective form. The quantifier all keeps its own agreement.',
    '37.10': '“(Wild) beasts” specifies the intended animal sense. The winged birds are directly addressed and take a weak plural adjective.',
    '37.12': 'Omit men but retain the people meant by young and old. Their weak masculine plural adjectives carry the direct address.',
    '38.2': 'Omit the English dummy there. The complete time and south expressions below remain available.',
    '38.3': 'Use the bracketed herbs meaning. Cook §154.a concerns the partitive genitive after a quantity: goldes depends on unrīm. The feminine accusative plural adjective for southern follows its taught inflection; its dictionary form in the hint is not automatically the answer form.',
    '38.4': 'Omit a separate to with the following object and put the finite verb last in the specified dependent clause. The supplied conversation frame gives wið its local meaning.',
    '38.5': 'Cook §87.d points to invariant relative ðe. Work out its clause role from the verb and antecedent; its shape does not show a case ending.',
    '38.6': 'Use invariant relative ðe and retain the complete list of what the queen saw. Omit the separately marked had.',
    '38.8': 'Keep self while omitting my. Cook §196.b supports the past subjunctive in the before-clause, viewed from the earlier unwillingness. Put that finite verb last.',
    '38.9': 'The printed wǣre is supplied exactly. It belongs to the report in the comparison; it does not agree with wisdom and works. The whole expression below construes wisdom and its work together.',
    '39.1': 'Use the relative particle for “which”. In the that-clause, omit a separate mightest and express the intended purpose with the subjunctive.',
    '39.2': 'Cook §154.c concerns a genitive after a higher numeral; §154.a concerns quantity plus genitive. Both complete quantity expressions are supplied below. Omit the marked indefinite articles.',
    '39.3': 'The requested thing is genitive with giernan; æt with the dative marks the person asked. Keep the main object’s role separate from that of the relative clause.',
    '39.4': 'The bracket replaces the infinitive “to see” with a purpose clause, “that they might see”; use the appropriate subjunctive. The rank comparison after ofer is dative as Cook §166 directs.',
    '39.6': 'Cook §164.m calls for the dative thing resisted. The received reward is also dative in the selected onfōn frame. Under §153.e the work is a genitive dependent on reward, expressing its grounds.',
    '39.7': 'Cook §183 calls for negative concord. Keep the subjects eye, ear and heart distinct; the first mæg can govern all three following infinitives. Ēare is singular weak neuter (§53.2). The beneficiaries are dative without a separate for.',
    '40.1': 'Cook §194.b calls for the subjunctive in the reported content. Use the bracketed gift meaning and put the specified preposition after its complement; its government is unchanged.',
    '40.2': 'Omit separate hath and doth. The supplied rejoice-in expression gives on its local relation to the source of joy.',
    '40.3': 'The plural generations are the subject of call. The first-person object has its own agreeing feminine predicate adjective.',
    '40.5': 'Cook §161 marks the dative beneficiaries. Omit on those, but retain the people through the participle. Their fearing still takes accusative him. The generation-to-generation expression is supplied as a whole.',
    '40.6': 'The mighty and the humble are weak masculine plural adjectives naming people. Omit the marked their without deleting the seats.',
    '40.7': 'The hungry and the rich name people without added ones. Good things uses the familiar plural noun for goods; omit a separate things.',
    '41.4': 'Cook §183 calls for negative concord. Retain the specified negative relation through both parts of the sentence.',
    '41.5': 'Use plural commands. The supplied impersonal passive expressions take dative addressees; do not insert the omitted it shall.',
    '41.6': 'Use the indicated plural heavens. In “thou who art”, invariant ðe leaves the verb second singular with the addressed thou.',
    '41.7': 'Put the finite verbs first as directed. The wishes are expressed by present subjunctives. The exact swā-swā comparison remains visible reference help.',
    '41.8': 'Use a singular command to the addressee. Debts are the thing forgiven; the debtors are dative people forgiven (§164). Preserve the requested forgiveness relation.',
    '41.11': 'The recipient of give is dative (§164.a). Ask has an accusative person asked and a genitive thing requested (§156.b; §159.b); the child is the subject of that clause.',
    '42.1': 'The exact quotation supplies the idiom: love is the subject, and on introduces the girl toward whom it is directed. The supplied past expression retains this structure.',
    '42.2': 'The voice is singular; the harpers are plural. Both the nested harper phrase and the entire exclusion of the 144,000 remain supplied. Retain nīwne sang and the later ðone sang with their visible support.',
    '42.3': 'The supplied expression keeps the grammatical singular company and the following descriptions of its many members. The participles describe perceived people; they do not become separate progressive finite verbs.',
    '42.5': 'Omit the marked article and retain the supplied “in circuit of” arrangement. Possessive his is not an article.',
    '42.6': 'The entire singular attribution of blessing and praise is supplied. It is a local formula, not a rule that every coordinated subject takes a singular verb.',
    '42.7': 'Omit a separate may. The subjunctive in the indefinite relative clause expresses a place where one might lay one’s head.',
    '42.8': 'Cook §172 specifies accusative complements in the marked on phrases, including placement on the head and spitting upon a person. Do not reduce all these meanings to one physical-motion rule. Omit the marked hand.',
    '42.9': 'Keep the actions coordinated and identify their subject before choosing each past form.',
    '43.1': 'The bracketed each and as if are part of the target. Preserve both images, then distinguish a copular identification from an elliptical comparison.',
    '43.2': 'Use negative concord (§183) and omit the marked article.',
    '43.3': 'Use the command to the stated addressee. The supplied swā-swā phrase is an elliptical comparison; it does not make an actual trumpet the object being lifted.',
    '43.8': 'The addressees are plural. Express their not knowing with ordinary ne and the appropriate finite form of witan.',
    '43.9': 'The parenthetic with calls for mid with the dative instrument. Use the familiar ball paradigm.',
    '43.10': 'The supplied although-clause has plural present subjunctives. Its meaning is “eat and are merry”, a concession rather than a wish.',
    '43.11': 'The bracket calls for a finite desired-content clause. Its first-person subject and the following plural you keep separate agreement; of with the dative names the source of learning.',
    '43.12': 'Address one person. The relative clause is indefinite: the one you wish to choose. Use the appropriate subjunctive.',
    '43.15': 'The denied content takes the selected present subjunctive under Cook §194.b. Keep the local pleasing expression supplied.',
    '43.16': 'The bracket supplies an active paraphrase: an indefinite person might slay him. Preserve the distinction between that grammatical subject and the man who held the expectation.',
    '43.17': 'The possessor addressed by your is singular. We is the subject of fall and requires a plural indicative verb; the sentence is a statement, not a command.',
    '43.18': 'Omit the English supporting do. The reported content takes second singular present subjunctive with thou under Cook §194.b.',
}

SUPPORT_NOTES = {
 'U17-H-37-06': 'He established a decree, and it will not pass away. The second predicate has the understood decree as subject. Keep the omitted it unexpressed and preserve the future reference of present gewīt.',
 'U17-H-37-14': 'The horn of his people, the praise of all his saints, of the children of Israel, of a people approaching him. Horn is the accusative thing exalted and represents strength or dignity; lof is appositional praise. The successive genitives identify the people concerned. Hālgena belongs to the noun hālga; folces is singular collective, nēalǣcendes agrees with it, and him is the dative person approached. Use the complete phrase as supplied.',
 'U17-H-38-09': 'Your wisdom and your work are greater than the report I heard. In this supplied arrangement, singular Māra is construes wisdom and its work together. The exact wǣre is third singular past subjunctive in the comparison, referring to the report. Keep that given form available; a defensible plural arrangement of the main clause can also be grammatical.',
 'U17-H-41-01': 'His wisdom was always begotten of him. The complete theological relation is supplied: of him gives the origin in this expression. It does not establish a general passive-agent use of of.',
 'U17-H-41-05': 'It will be given to you; it will be opened to you. These supplied impersonal passive expressions have dative plural addressees and a singular finite bið with future reference.',
 'U17-H-42-01': 'The young man fell in love with the girl: literally, the young man’s love fell upon the girl. Love is the nominative subject, the young man its genitive possessor, and the girl the accusative complement of on. Use the whole supplied past expression; the quoted present befielð in the prompt remains reference help.',
 'U17-H-42-02-PART': 'The voice of the harpers harping with their harps. Stefne is the accusative voice heard. Hearpera and hearpiendra are genitive plural; mid governs dative plural hearpum. The following they refers to the harpers. This complete nested description is supplied.',
 'U17-H-42-03': 'So great a company as no man can number, from all nations and every tribe, standing before God’s throne, all clothed in white garments and holding palm branches in their hands. Męnigu is grammatically feminine singular, while the later plural expressions describe its members. Standende and healdende are nonfinite descriptions, and gescrȳdde is a plural predicate past participle. Keep the whole supplied expression; this particular shift from collective to members is not a general agreement rule.',
 'U17-H-42-06': 'To our God be blessing and brightness, wisdom and thanksgiving, honour and strength, for ever. The recipient is dative and sīe is the singular optative. The whole coordinated formula, including ā ā ā, is supplied.',
 'U17-H-43-01': 'Every flesh is grass, and the glory of the flesh is as the blossom of plants. Retain the flesh/grass identification and the separate glory/blossom comparison. Swilce introduces an elliptical comparison here; no separate finite counterfactual verb is required.',
 'U17-H-43-03': 'As a trumpet: the accusative comparison imagines lifting a trumpet. It supplies a standard for the voice being raised, rather than an actual second object of the command. Retain the exact given swā-swā.',
 'U17-H-43-16': 'That someone should slay him. Man is an indefinite singular subject, and hine is the man who had the expectation. Past subjunctive slōge expresses the contemplated act; it does not assert that he died.',
 'U17-H-38-04': 'The queen then had speech with Solomon. Wið identifies the conversational partner. This supplied arrangement selects accusative Salomon; dative Salomone is also supported for this conversation frame.',
 'U17-H-39-04': 'Solomon was then celebrated above all earthly kings. Ofer here expresses rank and takes the explicitly requested dative complement. Keep that local case choice separate from the accusative rank construction encountered earlier.',
 'U17-H-40-02': 'My spirit rejoiced in God my Saviour. On with the dative names the source or object of joy in this supplied expression.',
 'U17-H-40-05': 'From generation to generation. Both cnēorisse forms are dative singular; of marks the starting generation and on the succeeding extent. Use the whole supplied temporal expression.',
 'U17-H-42-02-NUMBER': 'Except the one hundred and forty-four thousand. This entire exclusion phrase is supplied, including collective ðæt and final-o ðūsendo. It is not a dative chain. The number’s internal arrangement and unfamiliar forms require no independent recall.',
 'U17-H-43-10': 'Although other people eat and are merry. Eten and sīen are third plural present subjunctives in the concessive clause. Ðe belongs to the connective ðēah ðe; it is not a relative who or which. The complete clause remains supplied.',
 'U17-H-39-07': 'Nor can any man’s heart conceive: the earlier mæg also governs this last infinitive. The heart is the final subject, and the things mentioned are its shared object. The exact printed āsmēan and this frame are supplied.',
 'u17-supplied-days': 'In those days; a complete dative plural time expression.',
 'u17-supplied-south': 'In the south. Preserve the short vowel of be and use the complete expression.',
 'u17-supplied-degree-result': 'So greatly astonished. Tō ðan gives the degree and the following ðæt clause its result. Keep the exact supplied ðan.',
 'u17-supplied-120-gold': 'One hundred and twenty pounds of gold. Punda is genitive plural after the higher numeral; goldes is genitive singular naming the material. Use the complete quantity phrase.',
 'u17-supplied-within-place': 'Within Jerusalem. The foreign place form and the complete prepositional expression are supplied.',
 'u17-supplied-within-time': 'Within a few hours. The adjective and time noun are dative plural; keep the whole expression available.',
 'u17-supplied-three-months': 'About three months. Swilce gives approximation and mōnaðas is accusative plural of duration; use this complete supplied phrase.',
 'u17-supplied-unrim-gold': 'An immense quantity of gold. Genitive singular goldes depends on the quantity noun unrīm.',
 'u17-supplied-menigu-quantity': 'A great quantity of costly herbs and precious stones. The quantity noun is accusative singular, followed by both groups in the genitive plural. The complete phrase is supplied.',
}

def supplied_gloss(s, short):
    exact=s.get('exact_help_text','').strip('.,;:')
    contextual={
        ('39.2','hund'):'hundred, within the complete supplied quantity of gold',
        ('39.7','āsmēan'):'conceive; plain infinitive under the shared mæg, with the heart as subject',
        ('40.1','giefe'):'gift of grace; divine favour',
        ('42.1','befēoll'):'fell upon, with love as the subject and the girl as its goal',
        ('42.2','hearpiendra'):'harping; describing the harpers',
        ('42.3','gerīman'):'number; plain infinitive under mæg',
        ('42.3','gescrȳdde'):'clothed; plural predicate past participle describing the company’s members',
        ('42.3','healdende'):'holding; present participle describing the company’s members',
    }
    return contextual.get((short,exact),clean(s.get('meaning',s.get('help_text',''))))

def task(tid):
    t = TASKS[tid]
    cook = tid.startswith('EX-')
    label = 'Cook ' + str(t['original_exercise']) + '.' + str(t['original_item']) if cook else tid.replace('NEW-U17-','')
    put('### ' + label)
    put('<!-- item: ' + tid + ' -->')
    put(t['prompt'])
    if cook:
        short = f"{t['original_exercise']}.{t['original_item']}"
        source_markers(t)
        if short == '43.10':
            mark('NEW-U17-VOC-THE-U17-CONCESSIVE-MARKER')
        if short in CONTROL_NOTES:
            put('**Construction.** ' + CONTROL_NOTES[short])
        # The exact original prompt already supplies all hint sequences in order.
        hint_seqs = [s for s in t.get('input_sequences',[]) if s.get('kind') == 'visible_source_hint']
        for seq in hint_seqs:
            for tok in seq.get('tokens',[]):
                mark_records([tok.get('form_id')],[tok.get('sense_id')])
        # Exact support order is also the contract's visible-input order.
        for s in t.get('local_support',[]):
            source_markers(t,s)
            exact = s.get('exact_help_text',s.get('exact_span',''))
            if s.get('feature_id') == 'U17-H-41-05':
                explanation = ('It will be opened to you.' if 'geopenod' in exact else 'It will be given to you.')+' The addressees are dative plural; singular bið has future reference in this supplied impersonal passive.'
            elif s.get('feature_id') in SUPPORT_NOTES:
                explanation = SUPPORT_NOTES[s['feature_id']]
            elif s.get('meaning_and_analysis'):
                explanation = clean(s['meaning_and_analysis'])
            else:
                explanation = supplied_gloss(s,short)
                analysis = pretty_analysis(s.get('analysis',{}))
                if analysis:
                    explanation += ('; ' if explanation else '') + analysis
            put('**Supplied:** ' + exact + (' — ' + explanation.rstrip('.') + '.' if explanation else '.'))
            for seq in t.get('input_sequences',[]):
                if seq['sequence_id'] == s.get('support_id'):
                    for tok in seq.get('tokens',[]):
                        mark_records([tok.get('form_id')],[tok.get('sense_id')])
        # Each source task requests one whole translation; its prompt is that position.
        put('<!-- output: '+t['output_positions'][0]['output_position_id']+' -->')
        put('Write one complete Old English translation, keeping the printed controls and the supplied expressions available.')
    else:
        for si,seq in enumerate(t.get('input_sequences',[])):
            for tok in seq.get('tokens',[]):
                mark_records([tok.get('form_id')],[tok.get('sense_id')])
            put(('**'+chr(65+si)+'.** ' if tid=='NEW-U17-A04' else '')+seq['text'])
        for n,p in enumerate(t['output_positions'],1):
            put('<!-- output: '+p['output_position_id']+' -->')
            put(str(n) + '. ' + p['label'])

def noun_paradigm(p):
    pid, lid = p['paradigm_id'], p['lemma_id']
    put('### ' + p['headword'])
    vocab(lid)
    if lid == 'heanes':
        vocab(lid,True)
    mark(pid)
    gender = p['cells'][0]['analysis'].get('gender')
    stem = p.get('diagnostic_stem')
    g = {'m':'Masculine','n':'Neuter','f':'Feminine'}[gender]
    put(g + '; stem **' + stem + '-**. ' + NOUN_NOTES.get(lid,'Add the endings of the stated pattern to this stem, preserving its vowel length.'))
    if len(p['cells']) == 4 and lid not in {'andgiet','wisdom','eadmodnes'}:
        put('This table gives the complete singular for the stated abstract or mass meaning. The familiar noun class is reused; plural meanings and forms are not assigned here.')
    for mid in TEACH[pid]['matrix_ids']:
        matrix(mid)

def adjective_paradigm(p):
    lid, pid = p['lemma_id'],p['paradigm_id']
    put('### ' + p['headword'])
    vocab(lid)
    mark(pid)
    stem = p['diagnostic_stem']
    if lid == 'aethelboren':
        note = 'Use the retained stem æðelboren- throughout this selected table. Do not remove a vowel merely by analogy with a different word.'
    elif '59' in p['model']:
        note = 'The headword ends in -e; replace that -e with an overt ending on **' + stem + '-**. The displayed strong forms select feminine nominative singular and neuter nominative/accusative plural -u, and feminine plural -a. The source also permits -e in those positions.'
    else:
        note = 'The stem **' + stem + '-** is heavy. Strong feminine nominative singular and neuter nominative/accusative plural therefore have no added -u.'
    put(note)
    for mid in TEACH[pid]['matrix_ids']:
        m = MATRICES[mid]
        put('**' + ('Strong' if '-STRONG-' in mid else 'Weak') + '.**')
        matrix(mid)

def verb_paradigm(p):
    pid,lid = p['paradigm_id'],p['lemma_id']
    scope = p['scope']
    titles = {'indicative12':'Present and preterite indicative',
              'indicative12-participle-pair2':'Indicative and participles',
              'indicative12-imperative2-present-subjunctive6':'Indicative, commands and present subjunctive',
              'participle-pair2':'Present and past participles',
              'imperative2':'Singular and plural commands',
              'present-subjunctive6':'Present subjunctive',
              'preterite-subjunctive6':'Preterite subjunctive',
              'infinitive-pair2':'Plain and inflected infinitives',
              'selected singular/base and plural-e predicate realization':'Base and plural predicate participle'}
    title = titles.get(scope,'Present participle: strong and weak agreement')
    put('### ' + p['headword'] + ': ' + title.lower())
    vocab(lid)
    mark(pid)
    if scope.startswith('indicative'):
        put(VERB_NOTES[lid])
    elif scope == 'participle-pair2':
        notes = {
            'maersian':'The present participle has -iende and the past participle -od. The latter is used in the passive description celebrated or exalted.',
            'wyrcean':'The present participle uses the present stem; the past participle is worht, with the same changed stem as the weak preterite.',
            'gescieppan':'Retain the lexical ge-. The present participle uses the present stem, while gesceapen has ea and single p.',
            'acennan':'The present participle keeps the present stem with nn; the past participle has -ed. The begetting expression below is supplied in full.',
        }
        put(notes.get(lid,'The present participle has -iende and the past participle -od in this weak -ian pattern.'))
        put('This display assigns the complete present/past formation pair. It does not add other finite moods or an unrestricted attributive declension; the past form is used in the stated passive frame.')
    elif scope == 'imperative2':
        notes = {'cnucian':'The weak -ian command has singular -a and plural -iað.',
                 'ahebban':'The strong j-present has singular āhęfe and plural āhębbað.',
                 'plegian':'The weak -ian command has singular -a and plural -iað. The assigned ordinary sense is play, including playing with a ball.',
                 'ceosan':'Use the unmutated present stem in the singular command and add -að for the plural.',
                 'forgiefan':'Use the unmutated present stem for the singular command and -að for the plural. In the prayer, the meaning is forgive, with the familiar thing/person case distinction.'}
        put(notes[lid] + ' Only this complete command pair is added here.')
    elif scope in {'present-subjunctive6','preterite-subjunctive6'}:
        if scope.startswith('preterite'):
            put('Build the past subjunctive on the plural preterite stem gesāw-. All three singular persons have -e and all three plural persons -en. This system supplies the before-clause’s first singular gesāwe.')
        else:
            put('All three singular persons use -e and all three plural persons -en on the present stem; there is no indicative second/third-singular vowel change. With leornian, retain i in leornie and leornien.' if lid == 'leornian' else 'All three singular persons use -e and all three plural persons -en on the present stem, without an indicative second/third-singular vowel change. Only this tense of the subjunctive is added here.')
    elif scope == 'infinitive-pair2':
        put('The pair distinguishes the plain infinitive from the inflected infinitive. The selected series uses -anne, with -ianne in leornianne and -onne after contracted gesēon. The alternative -enne series also exists. The modal constructions here require the plain infinitive; this table adds no new purpose-clause use.')
    elif scope.startswith('selected'):
        put('The base is selected for singular predicates and the -e form for the plural predicate in Cook 37.5. The uninflected base is also permitted with a plural predicate. These are selected alternatives, not a complete attributive declension.')
    else:
        put('Remove final -e from the participle before adding an overt adjective ending. The strong table follows the grēne type: selected feminine nominative singular and neuter nominative/accusative plural -u, and feminine plural -a; the corresponding -e variants are also recorded. The weak forms follow the ordinary weak adjective pattern. The new independent use is describing or naming the specified human groups; no complete personal finite hyngran system is assigned.')
    for mid in TEACH[pid]['matrix_ids']:
        m = MATRICES[mid]
        caption = m['title'].split('—',1)[-1].strip()
        if len(TEACH[pid]['matrix_ids']) > 1:
            put('**' + caption[0].upper() + caption[1:] + '.**')
        matrix(mid)

put('# Unit 17. Connected exposition, praise and figurative language')
put('A connected passage uses familiar clauses for different purposes: to report what happened, compare people or actions, praise, request, and interpret an event. Keep the grammar of each clause distinct from the meaning supplied by its setting. A word can retain its ordinary inflection while taking a new contextual sense.')
put('Work through the clause review first, then study the new systems in manageable groups before the form and composition practice. Cook’s complete joint Group XII, XIII, Exercises 37–43 follow. The final reading contains a complete musical performance, criticism, demonstration and audience response. The four translated examples and the lettered tasks are new teaching material.')
put('**How to use the help.** A dictionary form gives a word and meaning; you may still need to form the required inflection. A complete expression labelled **Supplied** stays available while you answer and requires no independent recall of its unfamiliar parts. A familiar form does not automatically supply a new meaning. Reference-only and recognition forms are identified with their tables. In verb tables, 1, 2 and 3 denote person; singular and plural address remain distinct.')

put('## 1. Follow the clauses')
put('First identify each finite verb, its subject and its complements. Then identify how the clauses are joined. A relative expression can represent a different role inside its clause from the role of its antecedent outside. A content clause reports a proposition. A comparison can repeat an earlier action with dōn. A condition establishes a setting for the following statement or command.')
mark('NEW-U17-GRAM-U17-LITERAL-CONTEXTUAL-INTERPRETATION')
put('Interpretation comes after this grammatical account. Distinguish an ordinary word meaning, a supplied idiom, and an image whose force depends on context. A complete translation retains the participants and relations as well as the image; an explanation of the image’s point cannot replace the translated sentence.')
for e in C['new_material_examples']:
    mark(e['example_id']+'-TEACHING')
    put('**' + e['text'] + '**')
    put(e['translation'])
    put(e['teaching_point'])
put('A subjunctive in a report does not by itself say that the report is false. A past form can be simultaneous with a past statement; anteriority needs further evidence. In a condition, establish time and the speaker’s view of its possibility from the whole context. In an equal comparison, swā … swā gives the two sides; in an unequal comparison, identify what the comparative modifies and the standard introduced by ðonne.')
for tid in ['NEW-U17-A01','NEW-U17-A02','NEW-U17-A03','NEW-U17-A04']:
    task(tid)

put('## 2. Nouns and adjectives')
put('Choose case from the word’s work in the clause. A subject is nominative, an ordinary direct object accusative, a noun-dependent possessor genitive, and a recipient or governed complement takes its licensed case. A preposition or a particular verb can change the expected choice. Each table below gives all four cases for its stated number and meaning.')
nominals = [p for p in C['paradigms'] if p.get('part_of_speech') == 'noun']
groups = [
 ('Strong masculine nouns',lambda p:p['cells'][0]['analysis']['gender']=='m' and not p['model'].startswith('Cook 53'),
  'The ordinary masculine pattern has a bare nominative/accusative singular, genitive -es and dative -e; the plural has nominative/accusative -as, genitive -a and dative -um. The -e and agent-noun patterns and any changed stems are explained individually.'),
 ('Strong neuter nouns',lambda p:p['cells'][0]['analysis']['gender']=='n' and not p['model'].startswith('Cook 53'),
  'Nominative and accusative are alike in each number. The singular genitive has -es and dative -e; the plural genitive has -a and dative -um. A light stem normally has nominative/accusative plural -u, while a heavy stem normally has no ending. Learn the stated compound and exceptional stems with the table.'),
 ('Strong feminine nouns',lambda p:p['cells'][0]['analysis']['gender']=='f' and not p['model'].startswith('Cook 53'),
  'The selected pattern has nominative singular without an added ending and genitive, dative and accusative singular -e. Plural nominative, genitive and accusative have -a; dative has -um. The endingless accusative of cwēn and the doubled consonants of the -nes and related stems require particular attention.'),
 ('Weak nouns',lambda p:p['model'].startswith('Cook 53'),
  'Weak masculines normally have nominative singular -a, other singular cases -an, plural nominative/accusative -an, genitive -ena and dative -um. Weak feminines have nominative singular -e and otherwise the same endings. The weak neuter ēare keeps -e also in the accusative singular and has a contracted genitive plural.'),
]
for title,pred,intro in groups:
    put('### ' + title)
    put(intro)
    for p in nominals:
        if pred(p):
            noun_paradigm(p)
put('### Strong and weak adjectives')
put('An adjective agrees with its noun in gender, number and case. Use the familiar strong and weak choice: an article or comparable definite determiner normally calls for weak inflection, while a predicative adjective is normally strong. Direct address also favours weak forms; the praise catalogue uses this pattern even while its global instruction removes the article. The selected personal uses are explained after the tables.')
put('The columns are masculine, neuter and feminine, first singular and then plural. Strong instrumental singular forms in the masculine and neuter columns are for recognition; their display adds no new instrumental construction. A dash is an inapplicable display position. Weak genitive plural -ra is the selected form. These tables print one consistent set of source-licensed forms; a documented alternative is not automatically ungrammatical.')
for p in C['paradigms']:
    if p.get('part_of_speech') == 'adjective':
        adjective_paradigm(p)
teach_grammar('NEW-U17-GRAM-U17-PERSONAL-ADJECTIVE-GROUPS')

put('## 3. Verbs and nonfinite forms')
put('Each heading states exactly which verbal system is being learned. A complete indicative table gives all three persons in both numbers for the present and preterite. A command pair gives singular and plural; a subjunctive table gives all persons in its named tense. A two-form nonfinite display gives the stated pair, rather than an unprinted finite conjugation.')
mark('NEW-U17-DICTIONARY-REFERENCES')
put('**Dictionary references:** hęrian, praise; ondrǣdan, fear; hyngran, be hungry. These citation forms remain visible. A citation identifies the word; it does not by itself teach a new infinitival construction. The independent forms are the ones printed in the bounded systems below.')
put('Strong verbs change their stem vowels in the preterite; the second singular preterite normally shares the plural stem. Weak verbs use a dental preterite, whose spelling can merge with the last consonant of the stem. Present subjunctives generally have singular -e and plural -en; weak -ian verbs retain i in that pattern. Learn an exceptional stem together with its endings.')
verbs = [p for p in C['paradigms'] if p.get('part_of_speech') not in {'noun','adjective'}]
for p in verbs:
    verb_paradigm(p)

put('## 4. Meanings and complements')
put('The following meanings extend familiar words. Use their previously learned forms only in the constructions now stated. The new noun and adjective tables above already give their own meanings; the additional distinctions here prevent a familiar spelling from hiding a new lexical task.')
for l in C['lexical_inventory']:
    vocab(l['lemma_id'])
for tid in GRAMMAR:
    if tid not in EMITTED:
        teach_grammar(tid)
put('For sǣd in the promise to Abraham, the descendants are expressed collectively. The assigned dative sǣde is singular. Folc can denote distinct peoples in the plural catalogue, while the collective people in the dense horn passage remains singular. Wer now also means husband. Keep these contextual meanings separate from the earlier plant seed, people and man meanings.')

put('## 5. Form contrasts and composition')
put('Complete each requested response. The form contrasts test case, number and clause function in meaningful expressions. Keep supplied dictionary forms available, but choose the required endings from the tables and explanations. In the compositions, preserve every participant and the stated clause relationship.')
for code in ['F01','F02','F03','F04','F05','C01','C02','C03','C04']:
    task('NEW-U17-'+code)

put('## 6. Cook: connected composition')
mark('NEW-U17-SOURCE-HINTS')
mark('NEW-U17-VERBAL-CONTEXT-HELP')
put('Translate the complete English prompts. Parenthetic Old English is visible lexical or phrase help; a headword may require inflection, while an exact supplied expression is used as given. Parenthetic numbers refer to Cook’s grammar: the relevant constructions are explained here, so the locator is not a substitute for instruction. An omission control removes the specified English word from the Old English wording, while preserving its intended relation. Brackets supply the requested paraphrase. Distinguish a grammatical alternative from compliance with an explicit word, order, number or omission target.')
put('All supplied expressions and meanings remain available during these exercises. Copying an exact given form is a reference response. When the hint gives a headword but the task requires a different inflection, its lexical meaning is still given; the new ending is the part you must choose.')
set_intros = {
37:('Praise and enumeration','The catalogue alternates addressed beings with statements and wishes about them. Track who is addressed, who acts, and who receives praise. A list can leave a governing verb understood from its setting; keep the listed items complete.'),
38:('The queen’s visit','Follow the sequence of hearing, arrival, conversation, observation and judgment. Comparison and reporting clauses keep their own subjects and times.'),
39:('Praise, gifts and a change of subject','The first four items continue praise and reciprocal gifts. Items 5–7 turn to building and to what eye, ear and heart can apprehend; they are a change of material, not a continuation of the queen’s visit.'),
40:('Blessing and reversal','The prayer moves between praise, remembered acts, descriptions of people and a promise to descendants. Keep the beneficiaries, objects and predicates distinct.'),
41:('Petitions and explanation','Identify each addressee, the requested act and its recipients. The asking and receiving constructions have their own case patterns.'),
42:('Vision and figurative description','The longer vision sentences contain nested descriptions and source-specific number expressions. Their complete supplied phrases remain available. Separate the finite clauses from participles that describe perceived people.'),
43:('Mixed composition','Apply the same distinctions to comparisons, requests, reports and descriptions. The change of subject does not change the need to identify each clause’s participants and complements.'),
}
for ex in range(37,44):
    title,intro=set_intros[ex]
    put('## Cook ' + str(ex) + '. ' + title)
    put(intro)
    if ex == 37:
        for inst in C['source_task_crosswalk']['global_instructions']:
            text=inst.get('original_text',inst.get('text',inst.get('instruction',inst.get('exact_text',inst.get('instruction_text')))))
            if text:
                put(text)
        put('This applies to all fourteen items: omit the article and second-person pronoun. It does not remove a third-person subject needed for “let them praise”.')
    for t in C['assigned_items']:
        if t.get('original_exercise') == ex:
            task(t['task_id'])

put('## 7. Interpreting the images')
put('Keep the wording of the completed translations beside the following questions. Explain the effect of an image after identifying its literal grammatical structure. Do not replace an entire translated clause with a general statement of its message.')
task('NEW-U17-A05')
task('NEW-U17-A06')

put('## 8. A musical performance')
READ = C['source_spans'][0]
put(READ['context']['text'])
put('The reading is from Cook’s First Book, Reader XII, printed pages 174–175, lines 174.7–175.17 (scan pages 190–191). It begins when the daughter goes out and ends with the audience’s approval. The line references count the physical prose lines, anchored by the original marginal numbers. The text preserves the source’s spelling; line-end word divisions are joined and the original note numbers are identified by page. All help remains available during the reading tasks.')
put('<!-- source: ' + READ['source_span_id'] + ' -->')
source_parts=[]
for line in READ['source_lines']:
    page=line['printed_page']
    annotated=re.sub(r'\[([0-9]+[a-z]?)\]',lambda m:'[^P'+str(page)+'N'+m[1]+']',line['source_with_note_markers'])
    source_parts.append(annotated)
annotated=' '.join(source_parts).replace('Apol- lonius','Apollonius').replace('wyn- sumum','wynsumum')
assert re.sub(r'\[\^[^\]]+\]','',annotated)==READ['learner_text']
put(annotated)

put('### Finding the cited lines')
put('The passage is set continuously above. These short openings locate the physical source lines used by the questions; words divided at a line end are printed complete here.')
locators=[]
for line in READ['source_lines']:
    raw=re.sub(r'\[[^\]]+\]','',line['source_with_note_markers'])
    if raw.startswith('lonius '):raw='Apollonius '+raw[len('lonius '):]
    if raw.startswith('sumum '):raw='wynsumum '+raw[len('sumum '):]
    opening=' '.join(raw.split()[:4]).strip(' ,;:')
    locators.append(str(line['printed_page'])+'.'+str(line['editorial_line'])+' — '+opening)
put('\n'.join('- '+s for s in locators))

READ_NOTES = [
 ('174.7: the harp is fetched', 'The daughter goes out and has her harp fetched. Hēt governs fęccean, fetch, with the performer of the fetching left unexpressed; hiere gives the harp’s possessor. Do not make the daughter herself the necessary performer of fetch.',1),
 ('174.8–10: playing, singing and praise', 'Sōna swā means as soon as and introduces the complete time clause. Hearpian is the infinitive after began. Gemęngde means mixed: the harp’s sound is accusative and the song follows mid with the dative. On hiere swēgcræfte means with respect to her musical skill. The men’s praise concerns that skill.',2),
 ('174.11–13: silence and blame', 'Āna means alone. Swīgode means remained silent; the source participle swīgende is explained by Cook’s note 12a as swīgiende, being silent. It accompanies the addressed you in the accusation. Dēst yfele means you do wrong: dēst is second singular present indicative of dōn, and yfele is an adverb. Tǣlst means you blame or censure. Keep the source spelling of the participle.',3),
 ('174.14–16: permission and competence', 'Gif ðū mē gelīefst means if you permit me to speak. Gelīefst is second singular present indicative; mē is the dative person granted permission. Speaking is understood from the following ic sęcge, I will say; no speaking-infinitive occurs in the printed clause. This is the permission verb, distinct from believe. Ic ongiete introduces what Apollonius perceives. Gefēoll on swēgcræft means has chanced upon musical skill: on has an accusative complement in this supplied idiom. Masculine hine resumes swēgcræft, and næfð … nā wel geleornod says she has not learned or mastered it well.',4),
 ('174.17–18: giving and knowing', 'Hāt mē nū sęllan ðā hearpan asks for the harp to be given to the speaker. Mē is the dative recipient of giving, as original note 16 directs; it is not the person commanded to give. Ðonne means then in the consequence. Wāst is you know and nāst is the contracted you do not know; the latter is supplied here without a new conjugation. The present wāst refers to the knowledge that will follow. Ðæt ðū gīet nāst means what you do not yet know.',5),
 ('175.1–2: the king’s acknowledgment', 'Oncnāwe means acknowledge or recognize. The king’s content clause asserts that the addressee is well educated, using indicative eart. Original note 1 points to the certainty exception; the presence of ðæt does not mechanically demand a subjunctive. On eallum ðingum means in all matters, and gelǣred is the familiar adjective learned or educated.',6),
 ('175.3–6: preparing the demonstration', 'The king has the harp given to dative Apollonie. Apollonius then goes out (ūtēode), dresses himself (hine scrȳdde), puts a crown upon his head, takes the harp into his hand and enters (inēode). The supplied source form ænne is masculine accusative singular; retain its unmarked vowel. Upon his hēafod and on his hand describe the destinations of placement and taking.',7),
 ('175.6–8: appearance and supposition', 'Swā … ðæt introduces a result: he stood in such a way that the king and those sitting around supposed something about him. Ðā ymbsittendan is a weak plural description naming those people. The coordinated subject takes plural wēndon. The two content clauses have past subjunctives nǣre and wǣre; they present the spectators’ supposition. Apollines is the source’s name-form for Apollo, the god of the heathens. Preserve it without confusing him with Apollonius.',8),
 ('175.8–9: silence', 'Wearð … geworden presents quietness and silence coming about as a whole result; it is not a transitive passive. Retain singular wearð in this supplied expression. Stilnes and swīge are feminine nouns, and innan ðǣre healle means within the hall, with a dative complement.',9),
 ('175.10–12: the performance', 'Genōm means took; the object is his hearpenægl, his plectrum or string-plucking implement. Āstyrian ongan means began to set in motion, with the harp strings as accusative object. Mid cræfte means skilfully, with skill. Gemęngde again combines harp sound with song. These supplied senses explain the performance without creating new finite systems for all its verbs.',10),
 ('175.12–14: the response', 'The king himself and all those present are the plural actors of cleopedon, cried out, and hęredon, praised. The invariant relative ðe represents the people who were present. Micelre stefne means with a loud voice; it is a dative expression of manner without a printed mid. Hine is the person praised.',11),
 ('175.14–17: further accomplishments', 'Forlēt means set aside the harp; plegode means acted or performed; forðtēah means presented or performed the accomplishments. These performance meanings remain supplied. Fela governs genitive plural fægerra ðinga. The following relative construes what was unfamiliar collectively and has singular ungecnāwen wæs and ungewunelic; preserve this source construction without making it a general rule for agreement. In the last sentence, ǣlc is singular subject of līcode, pleased, and him eallum gives the dative people pleased. Ðāra ðinga is the partitive genitive after each; ðearle means greatly.',12),
]
put('### Modern help for the reading')
put('The following explanations supply the unfamiliar constructions and contextual meanings. Consult them throughout the reading and its questions. The original notes are retained separately at the end; their Latin parallels require no Latin exercise.')
for title,explanation,number in READ_NOTES:
    put('### '+title)
    fid='U17-RSUP-'+str(number).zfill(2)
    mark('NEW-U17-GRAM-'+fid)
    frame=next(s for s in READ['local_support'] if s['support_id']==fid)
    lo,hi=frame['token_start_one_based'],frame['token_end_one_based']
    for tok in READ['tokens'][lo-1:hi]:
        mark_records([tok['form_id']],[tok['sense_id']])
    if number==2:
        mark('NEW-U17-GRAM-U17-READ-SONA-SWA')
        mark('U17-SUP-SONA-TEMPORAL-CORRELATIVE')
        mark('U17-SUP-SWA-TEMPORAL-CORRELATIVE')
    if number==4:
        mark('NEW-U17-GRAM-U17-READ-ON-MUSIC')
    put(explanation)

put('### Exact word help')
put('These exact source forms can be consulted. The noun and verb endings below identify their particular occurrence; they do not require an additional complete paradigm from memory.')
seen_lex=set()
for s in READ['local_support']:
    if not s.get('form_id'):
        continue
    pair=(s['form_id'],s['sense_id'])
    if pair in seen_lex:
        continue
    seen_lex.add(pair)
    mark_records([s['form_id']],[s['sense_id']])
    word=s['exact_help_text']
    read_gloss={
        'fęccean':'fetch; plain infinitive after hēt',
        'hearpian':'play the harp; plain infinitive after began',
        'hęrian':'praise; plain infinitive after began',
        'swīgende':'being silent; the supplied present participle',
        'geleornod':'learned; mastered; past participle',
        'nǣre':'was not, in the reported supposition',
        'wearð':'came about, with geworden in the supplied result expression',
        'geworden':'come about; past participle in the supplied result expression',
        'āstyrian':'move; set in motion; plain infinitive after began',
        'ungecnāwen':'unknown; singular predicate in the supplied collective expression',
    }
    explanation=read_gloss.get(word,clean(s.get('meaning','')))
    analysis=pretty_analysis(s.get('analysis',{}))
    if analysis:
        explanation += '; '+analysis
    put('**'+word+'** — '+explanation.rstrip('.')+'.')
put('**Names:** Apollonius is the visitor; Apolloni addresses him, and Apollonie is the dative form for the recipient. Arcestrates is the king. Apollines is Apollo, the god. These exact name-forms are supplied.')
put('**Source distinctions:** for-ðǣm-ðe means because, with the source’s internal hyphens and ǣ. Āna means alone, rather than cardinal one. The lowercase common noun god names a deity here. Hǣðenra names the heathens in the genitive plural after ðāra. Mid cræfte describes manner, whereas mid wynsumum sange supplies the accompanying song. Æfter ðisum means after this, with the source’s single s.')

put('### Reading tasks')
put('Keep the exact passage, the original notes and all modern help open. These questions ask you to relate the supplied forms to one another and to the episode’s argument; they do not test independent recall of source-only forms.')
for code in ['R01','R02','R03','R04','R05','R06']:
    task('NEW-U17-'+code)

put('## Source and editorial notes')
put('The English exercises are Cook, Exercises in Old English, joint Group XII, XIII, Exercises 37–43, printed pages 22–28 (scan pages 30–36). All original prompts and controls are retained. The Old English reading is Cook, A First Book in Old English, second edition, Reader XII, printed pages 174–175. Original reading note numbers restart on page 175; P174 and P175 below identify their page. The modern explanations and the lettered exercises are separate teaching material.')
put('The supplied exclusion phrase for the 144,000 follows the parallel recorded by Bosworth–Toller under þūsend, printed page 1082. Acute length marks are presented as macrons and a divided word is joined; final-o ðūsendo is retained. The supplied nīwne follows the long nīwe adjective’s wilde pattern described by Wright, pages 49, 213–214. In the although-expression, the dictionary’s ðēah-ðe is spaced as ðēah ðe. These limited presentation choices do not change the original English prompts or the reading text.')
for n in READ['original_notes']:
    label='P'+str(n['printed_page'])+'N'+n['original_note_number']
    put('[^'+label+']: '+n['original_text'])
put('The short Latin glosses identify musical art (174 note 12), censure (174 note 13), chancing upon something (174 note 15), setting aside (175 note 5), and representing or performing (175 note 8). The allusion in 175 note 3 recalls everyone falling silent. The verse in note 4 describes taking the plectrum and mingling song with the strings; note 6 names comic and tragic performance. They illuminate the Old English scene without replacing its actual wording.')

def finish():
    text=unicodedata.normalize('NFC',''.join(OUT).rstrip()+'\n')
    (ROOT/'chapters/ch17/student.md').write_text(text,encoding='utf-8',newline='\n')
    print('Wrote learner master:',len(text.split()),'whitespace words;',len(EMITTED),'teaching records.')
    remaining=[t for t in TEACH if t not in EMITTED]
    (ROOT/'build/u17-learner-unrouted.json').write_text(json.dumps([TEACH[t] for t in remaining],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Teaching records still to route:',len(remaining))

if __name__=='__main__':
    finish()
