"""Render the Unit 15 learner master from its committed contract and authored prose.

This scratch helper writes only chapters/ch15/student.md and u15-learner-* reports.
It never updates the contract, registers, proposals, or audit packets.
"""
from pathlib import Path
import json
import re
import unicodedata
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
C = json.loads((ROOT / 'chapters/ch15/coverage.json').read_text(encoding='utf-8'))
LEX = {x['lemma_id']: x for x in C['lexical_inventory']}
PAR = {x['paradigm_id']: x for x in C['paradigms']}
MAT = {p: m for m in C['display_plan']['matrices'] for p in m['paradigm_ids']}
TASK = {x['task_id']: x for x in C['assigned_items']}
FEATURE = {x['feature_id']: x for x in C['grammar_inventory']}
RECORD = {x['teaching_id']: x for x in C['teaching_records']}
OUT = []
LOCATIONS = []
SEEN_MARKERS = set()
SEEN_MATRICES = set()
SEEN_TASKS = set()
SEEN_SUPPORT = defaultdict(list)
TAUGHT_SENSES = set()
TAUGHT_FORMS = set()
TAUGHT_FEATURES = set()


def add(text):
    if text and text.strip():
        OUT.append(text.strip())


def bind(location, *, ids=(), forms=(), senses=(), features=()):
    """Attach only bounded-record markers whose actual content is present here."""
    forms, senses, features = set(forms), set(senses), set(features)
    found = set(ids)
    for tid, r in RECORD.items():
        if r['type'] != 'bounded_teaching_record':
            continue
        if (forms.intersection(r.get('form_ids', [])) or
                senses.intersection(r.get('sense_ids', [])) or
                features.intersection(r.get('feature_ids', []))):
            found.add(tid)
    for tid in sorted(found):
        assert tid in RECORD, tid
        add(f'<!-- teaching: {tid} -->')
    SEEN_MARKERS.update(found)
    TAUGHT_FORMS.update(forms)
    TAUGHT_SENSES.update(senses)
    TAUGHT_FEATURES.update(features)
    LOCATIONS.append({'location': location, 'teaching_ids': sorted(found),
                      'form_ids': sorted(forms), 'sense_ids': sorted(senses),
                      'feature_ids': sorted(features)})


def para(text, features=(), forms=(), senses=(), ids=(), location=None):
    bind(location or text[:90], features=features, forms=forms, senses=senses, ids=ids)
    add(text)


def table(headers, rows):
    def row(values):
        return '| ' + ' | '.join(str(v) for v in values) + ' |'
    return '\n'.join([row(headers), row(['---'] * len(headers))] + [row(r) for r in rows])


def matrix(pid, title=None):
    m = MAT[pid]
    assert m['matrix_id'] not in SEEN_MATRICES, m['matrix_id']
    forms = {f for row in m['cell_form_ids'] for cell in row for f in cell}
    features = [f['feature_id'] for f in C['grammar_inventory'] if f.get('paradigm_id') == pid]
    bind('matrix ' + pid, forms=forms, features=features,
         ids=[pid] if pid in RECORD else [])
    if title:
        add('**' + title + '**')
    add('<!-- table: ' + m['matrix_id'] + ' -->\n\n' + table(m['headers'], m['rows']))
    SEEN_MATRICES.add(m['matrix_id'])


GENDER = {'m': 'masculine', 'f': 'feminine', 'n': 'neuter',
          'masculine': 'masculine', 'feminine': 'feminine', 'neuter': 'neuter'}
SENSE_GLOSS = {'wer-u11-source': 'man', 'tid-hour-u13-source': 'hour',
               'becraeding-u13-source': 'reading; reading books'}


def vocab(lid, extra='', include_forms=False, heading=None):
    l = LEX[lid]
    senses = [s for s in l.get('senses', []) if s.get('knowledge_status') != 'supplied']
    assert senses, lid
    glosses = [SENSE_GLOSS.get(s['sense_id'], s['gloss']) for s in senses]
    forms = [f['form_id'] for f in l.get('forms', [])
             if f.get('knowledge_status') != 'supplied'] if include_forms else []
    bind('vocabulary ' + lid, senses=[s['sense_id'] for s in senses], forms=forms)
    gender = GENDER.get(l.get('gender'), '')
    label = '**' + (heading or l['display_headword']) + '** — '
    if gender:
        label += gender + '; '
    add(label + '; '.join(glosses) + ('. ' + extra if extra else '.'))


def noun(lid, extra=''):
    p = next(p for p in C['paradigms'] if p['lemma_id'] == lid and p['paradigm_id'].startswith('NEW-U15-NOM-'))
    suffix = 'Stem **' + p['diagnostic_stem'].rstrip('-') + '-**.'
    if extra:
        suffix += ' ' + extra
    vocab(lid, suffix)
    matrix(p['paradigm_id'])


add('''# Unit 15. Negation, quantity and comparison in discourse

A negative clause can contain more than one negative word without becoming affirmative. Quantity words distinguish an individual from a group, while comparison can express equality, preference or a proportional change. This unit brings these distinctions into connected arguments and requests.

Sections 1–5 give the vocabulary, complete defined systems and constructions needed by the practice. The eight translated examples and the lettered exercises are new teaching material. Cook IX.28–30 and X, XI.31 retain their complete original prompts. The three readings preserve Cook’s Old English and original notes; modern helps are identified separately.

**Scope and notation.** Learn the forms for use in the meanings and constructions stated. A reference table supplies forms for recognition, without requiring their independent recall. Supplied expressions remain available during their exercises and readings. “Unassigned” means that no form or use in that position is required here; it does not assert that a historical form was impossible. In verbal tables, 1, 2 and 3 denote person. Preserve vowel length and the distinction between e and ę.''')

add('''## 1. Nouns and their meanings

The tables give nominative, genitive, dative and accusative in both numbers. Unless a number is marked as reference or unassigned, both numbers may be used. Endings that coincide still have distinct grammatical functions: the sentence determines the case. The lexical meaning, gender and stem belong to the whole word.[^nouns]

### Strong masculine nouns

The nominative and accusative singular have no ending. The other singular endings are genitive -es and dative -e. The plural endings are nominative/accusative -as, genitive -a and dative -um.''')
for lid in ['hlaford', 'wingeard', 'wer', 'leornungcniht', 'lareow', 'ham-noun']:
    noun(lid, 'This is the noun “home; dwelling”, distinct from the directional adverb hām.' if lid == 'ham-noun' else '')
add('''Fōtsceamul retains the vowel of its final element -sceamul- before endings. The long vowel in the first element fōt- does not require the loss of that later vowel.''')
noun('fotsceamul')

add('''### Strong neuter nouns

Heavy stems have no ending in nominative and accusative, singular or plural. Genitive and dative singular take -es and -e; genitive and dative plural take -a and -um. Bebod has a short final stem and takes nominative/accusative plural -u.''')
for lid in ['haer', 'leoth', 'bebod']:
    noun(lid)
add('''Hēafod loses the unstressed o before an ending: the ending-bearing stem is hēafd-. Its selected nominative/accusative plural is hēafdu. Compare fōtsceamul above: medial vowels are not all deleted by one general rule.''')
noun('heafod')
noun('flaesc', '**Plural reference:** the plural forms show the morphology; use the singular for the assigned meaning “flesh”.')

add('''### Strong feminine nouns

These long-stem nouns have no nominative singular ending. The other singular cases take -e. The plural has nominative/accusative and genitive -a, dative -um. Nouns in -nes double s before an ending. The -ung and -ing nouns use the same selected endings; oblique singular forms in -a are recognized alternatives.''')
for lid in ['bryd', 'hefignes', 'awendednes', 'costnung']:
    noun(lid)
noun('becraeding', '**Plural reference:** the meaning practised here is singular “reading”.')

add('''### Weak masculine nouns

The nominative singular ends in -a. The other singular cases and nominative/accusative plural end in -an; genitive plural takes -ena and dative plural -um. In lēoðwyrhta the final element is the noun head, and the ending follows the whole stem.''')
for lid in ['gerefa', 'leothwyrhta']:
    noun(lid)
noun('willa', '**Plural reference:** the assigned use is singular “will; disposition”.')

add('''### Root and kinship nouns

Learn the vowel changes with their case positions. Bōc has bēc in genitive and dative singular and nominative and accusative plural. Tōð has tēð in dative singular and nominative and accusative plural. Recognize genitive singular bōce, dative singular tōðe and nominative/accusative plural tōðas as alternatives to the selected forms below.''')
noun('boc')
noun('toth')
add('''Sweostor is unchanged throughout the singular and in nominative/accusative plural. Only genitive plural sweostra and dative plural sweostrum have different surfaces. Its pattern must be learned separately from the earlier brōðor and mōdor.''')
noun('sweostor')

add('''### Abstract nouns in -u

Hǣtu uses hǣte in the selected oblique singular cases. Hǣlu is unchanged throughout the selected singular. Oblique variants in -u, -o and -e occur, and nominative -o occurs beside -u. Learn the selected singular forms; no plural count meaning is assigned to either word.[^abstracts]''')
noun('haetu', '**Plural unassigned.**')
noun('haelu', '**Plural unassigned.**')
add('''The complete class model strengu follows. It is **for recognition only in both numbers**. Its spelling is retained from Wright. Besides the selected forms, recognize nominative singular strengo, oblique singular strengu/strengo, and nominative/accusative plural strenge/strengu/strengo. The availability of a class pattern does not supply a count meaning for every abstract noun.''')
noun('strengu', '**Singular and plural reference only.**')

add('''### People names and an agent noun

Engle and Dęne name peoples in the plural. They take nominative/accusative -e, genitive -a and dative -um. No singular is assigned. Dęniga and Dęnia are recognized genitive plural alternatives.''')
noun('engle', '**Singular unassigned.**')
noun('dene', '**Singular unassigned.**')
add('''The agent noun ālīesend has singular -es and -e as above. Its selected plural has unchanged nominative/accusative, genitive -ra and dative -um. Nominative/accusative plural forms in -e and -as are recognized alternatives. The plural is morphological reference; the assigned title “Redeemer” is singular.''')
noun('aliesend', '**Plural reference.**')

add('''### Additional senses of familiar nouns

Keep the earlier declensions. These meanings are needed in the following exercises.''')
vocab('med', include_forms=True)
vocab('tid', include_forms=True)
vocab('straet', include_forms=True)
vocab('word', include_forms=True)

add('''## 2. Negation

### Finite negation and contractions''')
para('''Place ne before the finite verb to deny a proposition. Some common verbs have contracted negative forms. The following complete table covers **the present indicative eom/eart/is/sindon and the preterite indicative wæs/wǣre/wǣron only**. It does not replace every form of bēon/wesan. Ne eom, ne eart and ne sindon remain two words; nis and the negative preterites are contracted. Separate ne with the ordinary positive form is also valid.[^negation]''', features=['u15-negative-copula'])
matrix('NEW-U15-PAR-WESAN-NEG-IND', 'Negative be-series: indicative')
vocab('nabban')
para('''The complete negative possession series is now available for use. Distinguish first singular næbbe from second and third singular næfst, næfð; the present plural has bb again. A present form denies present possession; a preterite form denies past possession.''', features=['u15-nabban-indicative'])
matrix('NEW-U15-PAR-NABBAN-IND', 'Nabban: indicative')
vocab('willan')
para('''Negative willan expresses refusal or unwillingness and governs a plain infinitive. The present and preterite distinguish the time of that unwillingness; English “would not” may need a past refusal, not a future form. These are indicative forms. A supplied subjunctive nolde encountered earlier does not thereby acquire every use of this table.''', features=['u15-negative-willan'])
matrix('NEW-U15-PAR-WILLAN-NEG-IND', 'Negative willan: indicative')

add('### Nān and negative concord')
vocab('nan')
para('''Nān agrees with its noun or stands alone for “no one”. It has the strong long-stem adjective endings in the four cases below. Keep long ā; note masculine accusative singular nānne, feminine plural nāna and neuter nominative/accusative plural nān. Only this strong four-case system is required here.''')
matrix('NEW-U15-PAR-NAN-STRONG-NGDA', 'Nān: strong declension')
para('''Nān, nāwiht and nǣfre can accompany finite ne or a contracted negative verb. They express **one denial**. This is negative concord: adding a second negative does not turn the clause into an affirmation. Determine what is denied from the roles of the negative expressions, not by counting them.''', features=['u15-negative-concord'])
vocab('nawiht', 'Use the selected accusative nāwiht as the thing denied: “nothing”. Other cases are not assigned by this form.', include_forms=True)
vocab('na', include_forms=True)
para('''Nā can deny one contrasted participant rather than the whole finite assertion. In ic self and nā ōðer, it excludes “another”; the assertion about “I myself” can remain affirmative. Distinguish this constituent use from finite ne. For a negative command, put ne before the imperative; the familiar affirmative command form remains.''', features=['u15-constituent-na'])

add('''## 3. Indefinite reference, groups and comparison

### An unnamed person and each member of a group''')
vocab('an', 'Use the earlier singular strong agreement forms.', include_forms=True)
para('''Context distinguishes cardinal “one” from indefinite “a certain”. Both agree with the same singular noun. An indefinite use does not create a plural cardinal meaning.''', features=['u15-an-indefinite'])
vocab('hwa', 'The earlier personal/neuter case forms are unchanged.', include_forms=True)
para('''Hwā/hwæt can ask “who?/what?” or refer indefinitely to “anyone/anything” in an appropriate condition or concession. The clause and its setting decide the function. English “any” cannot be replaced mechanically with hwā in every construction. Use the earlier ǣnig when an agreeing “any” is required.''', features=['u15-hwa-indefinite'])
vocab('gehwa')
para('''Gehwā refers to each person; gehwæt to everything. Both are singular, even when they distribute over many members. The genitive can identify the group; the distributive itself takes the case required by its own role. There is one personal column, without separate masculine and feminine forms, and no plural. The selected dative is gehwǣm, and the personal accusative is gehwone.[^pronouns]''', features=['u15-gehwa-distributive'])
matrix('NEW-U15-PAR-GEHWA-SINGULAR-NGDA', 'Gehwā/gehwæt: singular')
vocab('mann', 'Only nominative singular man is used in this impersonal function.', include_forms=True)
para('''Impersonal man means “one; people in general” and takes a third-person singular verb. Do not give it the oblique or plural forms of the ordinary count noun mann. The count noun still refers to an individual man and retains its earlier declension.''', features=['u15-man-impersonal'])
para('''Ǣlc distributes a singular share to each member; eall can gather the members as a plural whole. An explicit plural subject can retain a plural verb while ǣlc his pęning distributes one penny to each person. A genitive after a selection word identifies the whole group; it does not determine the selecting word’s case.''', features=['u15-quantity-partitives'])
vocab('ic', 'Personal genitive uncer means “of us two”. Its form is fixed by the partitive relation; it is distinct from the earlier agreeing possessive uncer, “our (two people’s)”.', include_forms=True, heading='uncer')

add('### Free choice and paired coordination')
vocab('hwaether', include_forms=True)
vocab('swa', include_forms=True)
para('''Swā hwā swā means “whoever”; swā hwæt swā means “whatever”. Swā hwæðer swā selects “whichever of two”. Give the pronoun the case needed within its clause. A pronoun in the main clause can resume the same referent in a different case, such as a subject within the choice clause and a dative recipient in the main clause. A possible or contingent event may take the subjunctive; free choice does not mechanically require one mood. Cook’s exceptional attracted dative in 31.12 is supplied with that item.''', features=['u15-free-choice'])
vocab('aegther', include_forms=True)
para('''Ǣgðer ge … ge means “both … and”. It includes both coordinated constituents. Here ǣgðer is an invariant coordinator; this expression does not require the separate inflectional family meaning “either”.''', features=['u15-either-both-coordination'])

add('### Equality, preference and proportion')
para('''In equality, swā … swā accompanies a positive adjective: “as … as”. In a proportional comparison, each swā clause contains a comparative: “the more …, the more …”. Each clause retains its own subject, verb and adjective agreement. A proportional relation does not assert equal degree.''', features=['u15-proportional-swa'])
vocab('swithe', 'The positive swīðe “very; greatly” is familiar. Learn comparative swīðor for preference; superlative swīðost is for recognition.')
matrix('NEW-U15-PAR-SWITHE-DEGREES', 'Swīðe: degrees of the adverb')
para('''Swīðor … ðonne compares preference: “more/rather … than”. The compared expressions retain the cases required by their verb. With lufian, both the preferred object and the alternative are accusative; neither becomes nominative merely by following ðonne.''', features=['u15-rather-than'])
vocab('micel', 'Use the earlier neuter forms substantivally for an amount.', include_forms=True)
vocab('micel-comp', 'The neuter substantive māre means “more; a greater amount”.', include_forms=True, heading='māre')
vocab('eall', 'This adverbial use is invariant and distinct from agreeing “all”.', include_forms=True)
para('''Eall strengthens an equative in eall swā micel swā, “just as much as”. Micel denotes the amount. When the comparison leaves “give” understood, the second recipient remains dative, just as the first recipient does.''', features=['u15-eall-equative'])

add('''**Reference limits.** Āwiht “anything” and hwæthwega “something” are supplied as exact objects in A10; they are not models for a new case system. The variants ōht and nōht, and the further family citations nǣnig, āhwæðer, nāhwæðer, ǣghwæðer, āhwā, ǣghwā and swā hwilc swā, require no new recall here. The earlier scope of other indefinite families remains unchanged. Instrumental degree expressions are reference material, and the possessive sīn is not introduced.''')

add('''## 4. Additional verbs

The following systems supply the forms required by the exercises. Each indicative table is complete for present and preterite, all three persons, singular and plural. Other moods and nonfinite forms are defined separately. A principal part identifies a stem; its citation alone does not require every possible use.[^verbs]

### Strong indicative systems''')
vocab('forgieldan', 'Strong III; present forgield-, preterite singular forgeald-, preterite plural forguld-, past participle forgolden.')
para('''The second- and third-singular present forms forgieltst and forgielt use the selected t cluster. The preterite second singular uses the plural stem plus -e; first and third singular have the bare singular stem. All present plurals end in -að and preterite plurals in -on. The prefix remains attached throughout.''')
matrix('NEW-U15-PAR-FORGIELDAN-IND', 'Forgieldan: indicative')
vocab('toweorpan', 'Strong III; present tōweorp-, preterite singular tōwearp-, preterite plural tōwurp-, past participle tōworpen.')
add('''The second- and third-singular present stem is tōwierp-. The preterite follows the same person/number distribution as forgieldan.''')
matrix('NEW-U15-PAR-TOWEORPAN-IND', 'Tōweorpan: indicative')
vocab('ongietan', 'Strong V; present ongiet-, preterite singular ongeat-, preterite plural ongēat-, past participle ongieten.')
add('''Second singular ongietst and third singular ongiett retain the selected t-cluster spellings. Third singular ongiet is a recognized alternative. Preterite second singular ongēate takes the plural stem; first and third singular have ongeat. The principal-part infinitive and past participle are reference citations; the complete new system here is indicative.''')
matrix('NEW-U15-PAR-ONGIETAN-IND', 'Ongietan: indicative')
vocab('gehatan', 'Strong VII. This indicative is a review of the earlier system.')
add('''Gehātan keeps its prefix and the familiar hātan stem changes: ā becomes ǣ in the second- and third-singular present, while the preterite has ē. This review does not add a new prefixed negative or subjunctive system.''')
matrix('NEW-U15-PAR-GEHATAN-IND', 'Gehātan: indicative review')

add('''### Weak indicative systems

The long-stem weak I verbs below use present -e, -st, -ð, -að and preterite -de, -dest, -de, -don. The repeated plural ending serves all three persons. Dēman also has the complete subjunctive shown separately.''')
for lid in ['wenan', 'forbaernan', 'laeran', 'deman']:
    vocab(lid, 'Weak I.')
    matrix('NEW-U15-PAR-' + lid.upper() + '-IND', LEX[lid]['display_headword'].capitalize() + ': indicative')
add('''The subjunctive singular has one form for all three persons; the plural has -n. Dēme can therefore be indicative first singular or present subjunctive singular; the clause and its function decide. Use the earlier distinctions among assertion, purpose and wish.''')
matrix('NEW-U15-PAR-DEMAN-SUBJ', 'Dēman: subjunctive')
vocab('hyrian', 'Weak II. Keep the long ȳ throughout.')
add('''Hȳrian follows lufian: present singular hȳrie, hȳrast, hȳrað, plural hȳriað; the preterite uses hȳrod- and the ordinary weak endings. Distinguish third-singular -að from plural -iað.''')
matrix('NEW-U15-PAR-HYRIAN-IND', 'Hȳrian: indicative')

add('''### Commands

Each table gives the complete second-person singular/plural command pair. Forgieldan has the strong singular stem without an ending. The weak I singulars ālīes and ætīew also have no ending; their plurals take -að. Weak II cleopa has singular -a and plural cleopiað.''')
matrix('NEW-U15-PAR-FORGIELDAN-IMP', 'Forgieldan: imperative')
vocab('cleopian', 'Weak II; only the command pair is newly required for use.')
matrix('NEW-U15-PAR-CLEOPIAN-IMP', 'Cleopian: imperative')
vocab('aliesan', 'Weak I; only the command pair is newly required for use.')
matrix('NEW-U15-PAR-ALIESAN-IMP', 'Ālīesan: imperative')
add('''**ætīewan** — show; the earlier verb, now with its complete command pair. Retain short initial æ in ætīew.''')
matrix('NEW-U15-PAR-AETIEWAN-IMP', 'Ætīewan: imperative')

add('''### Infinitives

These are complete pairs of plain and inflected infinitives. Use the plain form after the taught modal verbs. The inflected infinitive follows tō in the uses already learned; particular difficult frames are supplied locally. The pair does not introduce a finite system for the verb.''')
matrix('NEW-U15-PAR-FORGIELDAN-INF', 'Forgieldan: infinitives')
add('''**wyrcean** — work; do. The selected pair retains ea before the inflected ending.''')
matrix('NEW-U15-PAR-WYRCEAN-INF', 'Wyrcean: infinitives')
add('''**onfōn** — receive; keep the contracted stem in both infinitives.''')
matrix('NEW-U15-PAR-ONFON-INF', 'Onfōn: infinitives')
add('''**forlǣtan** — forsake; leave. Keep the long ǣ in both infinitives.''')
matrix('NEW-U15-PAR-FORLAETAN-INF', 'Forlǣtan: infinitives')
vocab('blostmian', 'Weak II; only the infinitive pair is required for use here.')
matrix('NEW-U15-PAR-BLOSTMIAN-INF', 'Blōstmian: infinitives')

add('''### Participial bases

Each pair gives the present and past participial base, without adding a complete adjective declension. The present participle can express an accompanying activity in the earlier predicative construction; the past participle can enter the earlier passive. Keep full -ed in lǣred and hǣled. Standan is strong VI: its present base standende retains n, and its past base is standen.''')
matrix('NEW-U15-PAR-FORGIELDAN-PART', 'Forgieldan: participial bases')
matrix('NEW-U15-PAR-LAERAN-PART', 'Lǣran: participial bases')
vocab('haelan', 'Weak I; the participial bases are required, not a new finite system.')
matrix('NEW-U15-PAR-HAELAN-PART', 'Hǣlan: participial bases')
add('''**standan** — stand. **giefan** — give. Their meanings are familiar; the following complete base pairs supply the forms needed here.''')
matrix('NEW-U15-PAR-STANDAN-PART', 'Standan: participial bases')
matrix('NEW-U15-PAR-GIEFAN-PART', 'Giefan: participial bases')

add('''### Principal parts for reference

For strong verbs the order is infinitive, preterite singular, preterite plural, past participle. Weak verbs have infinitive, preterite singular and past participle. This list is available for reference. Only forms in a separately defined system above, or already learned earlier, require independent use; the remaining citation forms are supplied.''')
pp_forms = [p['form_id'] for r in C['principal_parts']['records'] for p in r['parts']]
bind('principal parts reference', ids=['NEW-U15-PRINCIPAL-PARTS'], forms=pp_forms)
pp_rows = []
for r in C['principal_parts']['records']:
    parts = [p['form'] for p in r['parts']]
    if len(parts) == 4:
        pp_rows.append([parts[0], 'strong', parts[1], parts[2], parts[3]])
    else:
        pp_rows.append([parts[0], 'weak', parts[1], '—', parts[2]])
add(table(['Infinitive', 'Type', 'Preterite singular', 'Preterite plural', 'Past participle'], pp_rows))

add('''## 5. Adjectives, meanings and government

### Complete adjective systems

Each adjective has complete strong and weak tables for the four cases, both numbers and all three genders. Use strong forms in the familiar indefinite and predicative constructions, weak forms after the definite determiner as previously learned. No instrumental system is added.[^adjectives]

Riht and gelīc follow the ordinary long-stem pattern: strong feminine nominative singular and neuter nominative/accusative plural have no ending. The selected strong feminine plural has -a, masculine plural -e. Weak genitive plural has -ra.''')
for lid in ['riht', 'gelic']:
    vocab(lid)
    for kind in ['STRONG', 'WEAK']:
        matrix('NEW-U15-PAR-' + lid.upper() + '-' + kind + '-NGDA', LEX[lid]['display_headword'].capitalize() + ': ' + kind.lower())
vocab('mihtig')
add('''The selected forms lose i before a vowel-initial ending: mihtges, mihtgum, mihtge, mihtgan. They retain i before a consonantal ending: mihtigne, mihtigre, mihtigra. Strong feminine nominative singular and neuter nominative/accusative plural are mihtig, parallel to the earlier hālig. Unsyncopated forms are recognized variants.''')
for kind in ['STRONG', 'WEAK']:
    matrix('NEW-U15-PAR-MIHTIG-' + kind + '-NGDA', 'Mihtig: ' + kind.lower())
vocab('maere')
add('''Mǣre keeps its final e where there is no added ending and drops it before another ending. Note strong feminine nominative singular and neuter nominative/accusative plural mǣru. Stem-final r with -re/-ra gives mǣrre/mǣrra; weak genitive plural is also mǣrra.''')
for kind in ['STRONG', 'WEAK']:
    matrix('NEW-U15-PAR-MAERE-' + kind + '-NGDA', 'Mǣre: ' + kind.lower())
vocab('ungethancfull')
add('''Ungeðancfull retains ll in the bare form and before vowel-initial endings, as in ungeðancfulle and ungeðancfullum. Before consonantal endings the selected forms have one l: ungeðancfulne, ungeðancfulre, ungeðancfulra.''')
for kind in ['STRONG', 'WEAK']:
    matrix('NEW-U15-PAR-UNGETHANCFULL-' + kind + '-NGDA', 'Ungeðancfull: ' + kind.lower())

add('''### Additional vocabulary

Retain the earlier inflections of the familiar words below. Their stated senses are needed here; the adverbs do not agree with a noun.''')
for lid in ['idel', 'lytel-superl', 'god-adjective', 'yfel', 'slean', 'gelice',
            'eornostlice', 'thaerto-eacan', 'don', 'ut', 'ymbe', 'with', 'for', 'ofer', 'thurh']:
    extra = ''
    if lid == 'thurh':
        extra = 'The spelling ðurh is supplied beside the earlier þurh.'
    elif lid == 'ymbe':
        extra = 'Use accusative for the approximate time, including an hour.'
    vocab(lid, extra, include_forms=True)

add('### Government and clause relations')
para('''**Payment and exchange.** Forgieldan takes the person paid in the dative and the thing paid in the accusative. Onfōn can take an accusative material payment, including pęning and substantive māre. This payment construction stands alongside the earlier dative use of “receive”. Wið with the dative gives payment or return; for with the dative gives equivalent exchange, as in an eye-for-eye formula. The first noun in that quoted formula is nominative.''', features=['u15-forgieldan-payment', 'u15-onfon-payment-acc', 'u15-wid-exchange', 'u15-for-exchange'])
para('''**Making equal.** Dōn takes an accusative object and an agreeing predicate gelīc. The person used as the comparison standard is dative. Distinguish the object’s agreement from the comparison person’s case.''', features=['u15-gelic-object-predicate'])
para('''**Content after wēnan.** Wēnan can introduce a ðæt clause giving the thought or expectation. In a past report, sceolden, the preterite subjunctive plural of sculan, may express an expected outcome, “that they would receive”, rather than a duty.''', features=['u15-wenan-content'])
para('''**Kindness and rank.** Gōd ofer with the accusative means “kind toward” people. The bare strong accusative plurals ungeðancfulle and yfele can denote “unthankful people” and “evil people” in this use. Ofer with an accusative teacher or master can also mean “above” in rank. Neither use requires physical movement across something.''', features=['u15-ofer-kindness-rank'])
para('''**An oath.** Swęrian with ðurh plus accusative names what one swears by. When a negative command is followed by several ne ðurh phrases, each phrase shares that command; the repeated ne does not create several positive assertions.''', features=['u15-swerian-thurh'])
para('''**Teaching and deliverance.** Lǣran takes an accusative person or the accusative matter taught. Ālīes takes the person delivered in the accusative; fram with the dative names what the person is delivered from. The passive teaching expression in Cook 31.3 and the exact substantive dative yfele, “evil”, in 31.4 remain supplied there.''', features=['u15-laeran-objects', 'u15-aliesan-separation'])

add('''### Translated examples — new teaching material

These examples distinguish meanings and constructions; they are not exercises.''')
for n, ex in enumerate(C['new_material_examples'], 1):
    bind('translated example ' + str(n), ids=[ex['teaching_id']],
         forms=ex.get('required_form_ids', []), senses=ex.get('required_sense_ids', []),
         features=ex.get('feature_ids', []))
    add(f'**{n}.** {ex["text"]}\n\n{ex["translation"]}')
    add(ex['pedagogical_purpose'])


# The following replacements remove production-history prose from the modern
# helps while preserving their forms, senses, government, and task limits.
HELP_TEXT = {
    'U15-COOK-NOM-28-01': 'Keep every alternative, including sisters, and both promised results. Sweostor has its own table; retain the distinct earlier brōðor and mōdor patterns.',
    'U15-H-28-01': 'Use him mid hundtēontigum forgolden bið, “he will be repaid a hundredfold”, with the finite verb last. The initial ǣlc has its own relative clause and is resumed by dative him, the recipient in this supplied passive construction. Mid hundtēontigum means “with a hundredfold”. For mīnum naman means “for the sake of my name”. Keep this whole construction available as help.',
    'U15-COOK-NOM-28-04': 'Strǣt here means “public place”, with the earlier feminine declension.',
    'U15-COOK-NOM-28-06': 'Tīd means “hour”. Temporal ymbe takes accusative for the approximate time.',
    'U15-H-28-06': 'Use supplied nigoðan, the feminine accusative singular weak form of “ninth”, with tīd. Siextan, “sixth”, is already familiar.',
    'U15-H-28-07': 'Use the supplied expression ðā endleftan tīd, “the eleventh hour”, with the feminine accusative singular weak ordinal.',
    'U15-COOK-NOM-28-10': 'Ǣfen means “evening”; wyrhta, “workman”; gerēfa, “steward”; wīngeard, “vineyard”; mēd here, “hire; wages”.',
    'U15-H-28-10': 'Use ðā hit ǣfen geworden wæs, “when it had become evening”. Geworden is the supplied past participle of geweorðan. With cweðan, tō his gerēfan names the person addressed: tō takes dative.',
    'U15-COOK-NOM-29-01': 'Hęfignessa is accusative plural “burdens”; hǣte is the selected dative singular “heat”.',
    'U15-H-29-01': 'On ðisses dæges hǣte means “in this day’s heat”: on with dative gives the circumstance; ðisses dæges is a dependent genitive.',
    'U15-H-29-07': 'Use the supplied spelling ðurh beside the familiar þurh. Here ðurh hine means “through/by way of him”. Negation rejects the condemning purpose and contrasts it with saving; it does not deny that the Son was sent.',
    'U15-H-29-08': 'Use ðæs Hēahstan, “of the Highest”, as a supplied masculine genitive singular divine title. No further superlative forms of hēah are required.',
    'U15-COOK-NOM-29-11': 'Hǣlu, “salvation”, is unchanged through the selected singular. Unnan governs genitive of the thing granted, so use genitive ðīnre with it even though hǣlu shows no separate genitive ending. Hǣle is a recognized oblique alternative.',
    'U15-COOK-NOM-30-01': 'Setl means “seat; throne”. Fōtsceamul retains -sceamul- in its inflected stem.',
    'U15-H-30-01': 'Use the supplied spelling ðurh before each accusative oath standard. Hierusalem is the supplied place name; its other cases are not required.',
    'U15-COOK-NOM-30-02': 'Hēafod uses hēafd- before endings. Hǣr is neuter and has no nominative/accusative plural ending. Fōtsceamul, by contrast, retains its medial vowel.',
    'U15-H-30-05': 'The emphatic resumed sē is a supplied long-vowel nominative masculine singular. In ān of ðissum lǣstum bebodum, “one of these least commandments”, of takes dative to identify the group. The same long sē may be used in 30.6.',
    'U15-H-30-07': 'Use the supplied on ealdum tīdum, “in old times”, with temporal on and dative plural.',
    'U15-COOK-NOM-30-08': 'Eorðe, “earth”, is feminine. Its possessive must agree with the noun that it modifies.',
    'U15-COOK-NOM-30-09': 'Gewinne, “labour”, is a supplied noun form in the expression æt his gewinne.',
    'U15-H-30-09': 'Use æt his gewinne, “from his labour”. In the supported ðæt hē mæg, “what he can”, an action such as “obtain” is understood. Retain this supplied expression without deriving further forms of gewinn.',
    'U15-COOK-NOM-30-11': 'Brȳd is feminine; the selected accusative singular is brȳde. Hām is the noun “home”, here an accusative object, rather than the directional adverb. Use the given infinitive blōstmian for “blossom”.',
    'U15-H-30-12': 'Use the supplied permission construction lǣt hīe libban, “let them live”: accusative hīe is the understood subject of libban. Gif hīe magon expresses ability. A third-person optative is also a valid way to express the request.',
    'U15-COOK-NOM-31-01': 'Use ālīesend as the singular title “Redeemer”. Its displayed plurals remain reference forms.',
    'U15-H-31-03': 'Use hē wæs lǣred … tō dōnne. The person taught is the passive subject and the understood doer of the infinitive. Godes willan is the infinitive’s accusative object, with dependent genitive Godes. This whole passive-and-infinitive frame is supplied.',
    'U15-H-31-04': 'Use fram yfele, “from evil”. Yfele is a supplied substantive noun in the dative singular, not the ordinary adjective dative yfelum.',
    'U15-H-31-06': 'Begin with supplied Geweorðe, the third-singular present subjunctive of the prefixed verb. Swā-swā means “just as”; retain this supplied hyphenated expression.',
    'U15-H-31-NAMES': 'The names Ælfred, Osburg, Æthelwulf and Asser are supplied; Ælfredes is the genitive for 31.14. Use supplied dative Lǣdene for “Latin”, following Cook’s glossary Lǣden. The Preface reading below retains its printed Lædene without a length mark.',
    'U15-COOK-NOM-31-08': 'Dęne and Engle name peoples in the plural. Lēoðwyrhta is a weak masculine noun, “poet”. Āwęndednes means “translation” and doubles s before endings. The language-name dative is supplied separately.',
    'U15-H-31-09': 'Supplied hātte means “is/was called”; context supplies past time here. It is a special passive naming form, not the active preterite hēt.',
    'U15-H-31-10': 'Use the supplied number phrase twā and fīftig gēara, “fifty-two years”. Fīftig means “fifty”; gēara is genitive plural governed by this numeral expression. No further higher numerals are required.',
    'U15-COOK-NOM-31-11': 'Bēcrǣding means “reading”. Use its singular; the displayed plurals are for reference.',
    'U15-H-31-11': 'Use æfter ðǣm ðe … wæs for “after he was …”. Here ðe belongs to the supplied after-conjunction and has no separate subject or object role. In twęlf wintra eald, “twelve years old”, wintra is genitive plural with the numeral and adjective of age. Keep both expressions available as help.',
    'U15-COOK-NOM-31-12': 'Bōc is accusative singular “book”; bēc belongs to other cases in its table. Lēoða is genitive plural “poems”.',
    'U15-H-31-12': 'Use Engliscra lēoða, “of English poems”. The supplied recipient expression is swā hwæðrum hiere twēgra suna swā hīe ǣrest leornode. Hwæðrum is dative because the whole expression is the recipient of the promise; the same person is understood as the learner in the subordinate clause. Leornode is prospective preterite subjunctive, identical in spelling to the indicative; the learning is still to occur. This case attraction is supplied. In the independent free-choice exercises, keep the internal subject nominative and resume it with an explicit dative recipient.',
    'U15-READ-P-HINDRANCES': 'The two superlative adverbs mean “most clearly and most intelligibly”. For with dative introduces the worldly cares that constrained how clearly Alfred could explain it. Ǣgðer ge … ge means “both … and”; on mōde/on līchaman identify mind and body. Sind means “are”. The relative after Ðā bisga refers to the cares, which are the subject of becōmon.',
}


def support(s, owner, tokens=None):
    sid = s['support_id']
    forms, senses = s.get('form_ids', []), s.get('sense_ids', [])
    selected = []
    if tokens is not None and s.get('kind') == 'lexical_help':
        selected = [t for t in tokens if t['token_id'] in s.get('token_ids', [])]
        assert selected, (owner, sid)
        forms = sorted({t['form_id'] for t in selected})
        senses = sorted({t['sense_id'] for t in selected})
    bind('help ' + sid + ' for ' + owner,
         ids=[s.get('teaching_id', sid)], forms=forms, senses=senses,
         features=s.get('feature_ids', []))
    add('<!-- support: ' + sid + ' -->')
    if selected:
        # A source form can recur with several functions; retain each local
        # meaning, but do not import a different passage's contextual gloss.
        pieces = []
        seen = set()
        for t in selected:
            form = t.get('form', t['surface'])
            gloss = t['gloss']
            a = t.get('contextual_analysis') or t['analysis']
            if isinstance(a, str):
                a = {'source_analysis': a}
            analysis = a.get('source_analysis', '')
            if analysis:
                analysis = re.sub(r' agreeing with .*', '', analysis)
                analysis = analysis.replace('source -e- variant', '').replace('source spelling hīera', '')
                analysis = analysis.replace('source Marian used as genitive; mixed treatment of foreign names, not regular Latin genitive', 'genitive form of a foreign name')
                analysis = analysis.replace('source form ', '')
            else:
                order = ['declension', 'tense', 'mood', 'verb_form', 'person', 'case', 'number', 'gender']
                labels = []
                for key in order:
                    if key not in a or a[key] is None:
                        continue
                    value = str(a[key])
                    value = {'nom': 'nominative', 'gen': 'genitive', 'dat': 'dative', 'acc': 'accusative',
                             'sg': 'singular', 'pl': 'plural', 'm': 'masculine', 'f': 'feminine',
                             'n': 'neuter', '1': 'first person', '2': 'second person', '3': 'third person'}.get(value, value)
                    labels.append(value.replace('_', ' '))
                analysis = ' '.join(labels)
            analysis = re.sub(r'\s+', ' ', analysis).strip()
            if form == 'gewęnd':
                analysis = 'past participle'
            analysis = analysis.replace('; syncopated source form', '; syncopated form')
            analysis = analysis.replace(' source variant sind', '')
            key = (form, gloss, analysis)
            if key in seen:
                continue
            seen.add(key)
            # Ordinary word meanings are given first; the local parse follows.
            piece = '**' + form + '** — ' + gloss
            if analysis and analysis not in ['invariant', 'adverb', 'preposition', 'conjunction']:
                piece += ' (' + analysis + ')'
            pieces.append(piece + '.')
        add(' '.join(pieces))
    else:
        help_text = HELP_TEXT.get(sid, s['text'])
        help_text = re.sub(r'\bnote(\d)', r'note \1', help_text)
        help_text = re.sub(r'\bnotes(\d)', r'notes \1', help_text)
        add(help_text)
    SEEN_SUPPORT[sid].append(owner)


def output_marker(p):
    return '<!-- output: ' + p['output_position_id'] + ' -->'


RESPONSE_LABELS = {
    'F01': ['why twelve positions remain distinct; where ne stays separate'],
    'F02': ['meaning of present first singular', 'meaning of present third plural', 'meaning of preterite first singular', 'meaning of preterite third plural'],
    'F03': ['meaning of present first singular', 'meaning of present second singular', 'meaning of preterite first singular', 'meaning of preterite second singular'],
    'F04': ['how the sentence identifies the form’s case, number and gender'],
    'F05': ['reason no plural column is needed'],
    'F06': ['positions with vowel changes', 'forms whose cases need context'],
    'F07': ['contrast with bōc', 'reason a sentence still requires case analysis'],
    'F08': ['selected singular patterns', 'meaning and limits of the unassigned plural cells'],
    'F09': ['relation of the compound’s structure to its inflection'],
    'A01': ['clause 1: negative words', 'clause 1: proposition denied', 'clause 2: negative words', 'clause 2: proposition denied', 'clause 3: negative words', 'clause 3: proposition denied'],
    'A02': ['first clause: scope of negation', 'first clause: contrasting participant', 'second clause: scope of negation'],
    'A03': ['clause 1: function of hwā', 'clause 1: meaning', 'clause 1: subject', 'clause 2: function of hwā', 'clause 2: meaning', 'clause 2: subject', 'clause 3: function of hwā', 'clause 3: meaning', 'clause 3: subject'],
    'A04': ['clause 1: quantifier meaning', 'clause 1: subject head and verb agreement', 'clause 2: quantifier meaning', 'clause 2: subject head and verb agreement'],
    'A05': ['meaning of the construction', 'first coordinated constituent', 'second coordinated constituent', 'whether just one is selected'],
    'A06': ['clause 1: subject and reference', 'clause 1: verb number', 'clause 2: subject and reference', 'clause 2: verb number', 'reason this does not supply a new plural pronoun'],
    'A07': ['comparison 1: meaning', 'comparison 1: standard or related clause', 'comparison 2: meaning', 'comparison 2: standard or related clause', 'comparison 3: meaning', 'comparison 3: standard or related clause'],
    'A08': ['subject of cume and its case', 'recipient of the book and its case', 'function of the explicit main-clause pronoun'],
    'A09': ['first uncer: function', 'second uncer: function', 'ānum: role and case', 'number of the group'],
    'A10': ['clause 1: meaning and statement type', 'clause 2: meaning and statement type', 'clause 3: meaning and statement type', 'how the two negatives work together'],
    'A11': ['ān in the first setting', 'ān in the second setting', 'reason for the same agreement'],
    'A12': ['hēafod: stem before endings', 'hēafod: nominative/accusative plural', 'fōtsceamul: stem before endings', 'why deleting every medial vowel would fail'],
    'D01': ['fault', 'consequence', 'promise', 'speaker and addressee'],
    'D02': ['noldest and its infinitive', 'tense of wille in this context'],
    'D03': ['thing given', 'immediate recipient', 'recipient identified by the speaker', 'resuming pronoun'],
    'D04': ['case relations in the first phrase', 'case relation and meaning in wið ðǣm'],
    'P01': ['first translation method', 'second translation method', 'obstacles', 'later change', 'request to readers'],
    'P02': ['hē before gebidde', 'hine after for', 'him before ne wīte', 'hē after gif', 'hē after ðonne', 'contrast between the comparison subjects'],
    'P03': ['meaning and coordination in the first expression', 'main subject and finite verb', 'first relative clause', 'second relative clause'],
    'P04': ['comparison and understood words', 'function of ne and relation of its clause to the request'],
    'R02': ['meaning of the for phrases', 'case relations in ðǣre hālgan rōde tācne'],
    'R03': ['first comparison standard', 'second comparison standard', 'explanation of cunne'],
    'R04': ['first clause: actor/addressee', 'first clause: mood', 'first clause: function', 'second clause: actor/addressee', 'second clause: mood', 'second clause: function'],
}


def response_labels(t):
    key = t['task_id'].removeprefix('NEW-U15-')
    labels = RESPONSE_LABELS[key]
    assert len(labels) == len([p for p in t['output_positions'] if p['kind'] != 'form']), key
    return labels


def form_response(t):
    positions = t['output_positions']
    by_matrix = {}
    for n, p in enumerate(positions, 1):
        if p['kind'] != 'form':
            continue
        d = p['display_route']
        by_matrix.setdefault(d['matrix_id'], []).append((n, p))
    lookup = {m['matrix_id']: m for m in C['display_plan']['matrices']}
    for mid, pairs in by_matrix.items():
        m = lookup[mid]
        used_cols = sorted({p['display_route']['column_index_zero_based'] for _, p in pairs})
        used_rows = sorted({p['display_route']['row_index_zero_based'] for _, p in pairs})
        cell = {(p['display_route']['row_index_zero_based'], p['display_route']['column_index_zero_based']): n for n, p in pairs}
        pid = m['paradigm_ids'][0]
        l = LEX.get(PAR[pid]['lemma_id'], {})
        add('**Response grid: ' + l.get('display_headword', PAR[pid]['lemma_id']) + '**')
        add('\n'.join(output_marker(p) for _, p in pairs))
        rows = [[m['rows'][ri][0]] + [f'({cell[ri, ci]}) ____' if (ri, ci) in cell else '—' for ci in used_cols] for ri in used_rows]
        add(table([m['headers'][0]] + [m['headers'][ci] for ci in used_cols], rows))
    explanations = [(n, p) for n, p in enumerate(positions, 1) if p['kind'] != 'form']
    if explanations:
        add('\n'.join(output_marker(p) for _, p in explanations))
        add('**Then explain:** ' + '; '.join(f'({n}) {label}' for (n, p), label in zip(explanations, response_labels(t))) + '.')


def short_label(tid):
    if tid.startswith('EX-'):
        if tid.startswith('EX-X-XI-'):
            ex, item = tid.split('-')[-2:]
            return 'Cook X, XI.' + ex + '.' + str(int(item))
        group, ex, item = tid.split('-')[1:]
        return 'Cook ' + group + '.' + ex + '.' + str(int(item))
    return tid.removeprefix('NEW-U15-')


def task(tid, shared_support=None):
    assert tid not in SEEN_TASKS, tid
    t = TASK[tid]
    SEEN_TASKS.add(tid)
    add('**' + short_label(tid) + '**')
    add('<!-- item: ' + tid + ' -->\n\n' + t['prompt'])
    if shared_support is not None:
        assert {s['support_id'] for s in t.get('local_support', [])} <= set(shared_support)
        for s in t.get('local_support', []):
            SEEN_SUPPORT[s['support_id']].append(tid + ' (shared reading help)')
    elif t.get('local_support'):
        add('**Modern help — available throughout this item.**')
        for s in t['local_support']:
            support(s, tid)
    for i, seq in enumerate(t.get('input_sequences', []), 1):
        add(f'({i}) {seq["text"]}')
    if tid.startswith('NEW-U15-F'):
        form_response(t)
    elif len(t['output_positions']) > 1:
        positions = t['output_positions']
        if tid == 'NEW-U15-R01':
            add('\n'.join(output_marker(p) for p in positions))
            rows = []
            for ri, label in enumerate(['Opening requested action', 'First direct command', 'Second direct command', 'Third direct command', 'Fourth direct command', 'Fifth direct command', 'Sixth direct command']):
                rows.append([label] + [f'({ri * 3 + ci + 1}) ____' for ci in range(3)])
            add(table(['Requested action', 'Finite form', 'Mood', 'Meaning'], rows))
        else:
            add('\n'.join(output_marker(p) for p in positions))
            add('**Responses, in order:** ' + '; '.join(f'({i}) {label}' for i, label in enumerate(response_labels(t), 1)) + '.')
    else:
        add(output_marker(t['output_positions'][0]))


add('''## 6. Practice — new teaching material

The form grids identify each requested position even when several answers have the same spelling. Give English explanations for the analysis questions and Old English for composition. In composition, the directions specify the construction being practised. A different grammatical expression may convey the meaning without meeting that particular direction. Keep all supplied help visible.''')
for stage in C['study_sequence'][:4]:
    add('### ' + str(stage['stage']) + '. ' + stage['title'])
    for tid in stage['practice']:
        task(tid)
add('### 5. Noun systems and commands')
for tid in ['NEW-U15-F06', 'NEW-U15-F07', 'NEW-U15-F08', 'NEW-U15-F09', 'NEW-U15-A12', 'NEW-U15-C13']:
    task(tid)

add('''## 7. Cook’s exercises

The prompts, parentheses, references and translation controls below are Cook’s original material. Translate every item into Old English. Modern help is separate and remains available; it supplies unusual forms or constructions without requiring their unaided recall. Numbers in Cook’s parentheses refer to his grammar or earlier exercises.[^exercises]''')
for group, prefix in [('IX.28', 'EX-IX-28-'), ('IX.29', 'EX-IX-29-'), ('IX.30', 'EX-IX-30-'), ('X, XI.31', 'EX-X-XI-31-')]:
    add('### Cook ' + group)
    for t in C['assigned_items']:
        if t['task_id'].startswith(prefix):
            task(t['task_id'])


add('''## 8. Readings

The Old English passages and the numbered original notes are exact source material, with declared typographic normalization. Modern vocabulary and construction helps precede each passage and remain available for all five tasks on it. Original note numbers are prefixed D, P or R here only to distinguish the three sets. Cook’s grammatical references and historical questions are retained as apparatus; answer only the tasks explicitly assigned below.''')
para('''Attend to each passage’s movement: a rebuke becomes a promise, an account of translation becomes a request to readers, and an appeal becomes a series of commands and a concluding wish. Distinguish rhetorical questions, assertions, purposes and petitions.''', features=['u15-source-argument'])

READING_TITLES = [
    ('D', 'Duties of the rich toward the poor: the opening argument', 'Cook, First Book, printed p. 159 (PDF p. 175). This is the complete first argument, including its embedded gospel saying. The Savior’s outer speech continues on pp. 160–161; its opening quotation mark is intentionally left unmatched in this selection.'),
    ('P', 'Alfred’s preface to Boethius', 'Cook, First Book, printed p. 162 (PDF p. 178). The complete preface.'),
    ('R', 'A prayer of King Alfred', 'Cook, First Book, printed p. 163 (PDF p. 179). The complete prayer.'),
]
for span, (code, title, locator) in zip(C['source_spans'], READING_TITLES):
    sid = span['source_span_id']
    add('### ' + code + '. ' + title)
    add(locator)
    add('**Modern vocabulary — supplied for this reading.** Forms are glossed in their local senses; the parses identify the forms encountered, not complete new paradigms.')
    for s in span['local_support']:
        if s['kind'] == 'lexical_help':
            support(s, sid, tokens=span['tokens'])
    add('**Modern construction help.**')
    for s in span['local_support']:
        if s['kind'] != 'lexical_help':
            support(s, sid)
    add('**Cook’s text**')
    source_title = span['source_paratext']
    add(source_title['printed_group'] + ' ' + source_title['printed_title'] + '\n\n' + source_title['printed_subtitle'])
    bind('source reading ' + sid, ids=[span['teaching_id']])
    raw = ' '.join(line['source_with_note_markers'] for line in span['source_lines'])
    # Preserve lexical hyphens, joining only the printed line-wrap divisions
    # already resolved in the contract's exact learner transcription.
    raw = re.sub(r'(\w+)- (\w+)', lambda m: m.group(1) + ('' if m.group(1) + m.group(2) in span['learner_text'] else '-') + m.group(2), raw)
    assert re.sub(r'\[\d+\]', '', raw) == span['learner_text'], sid
    marked = re.sub(r'\[(\d+)\]', lambda m: '[^' + code + m.group(1) + ']', raw)
    add('<!-- passage: ' + sid + ' -->')
    add(marked)
    add('**Original notes — Cook.**')
    for note in span['original_notes']:
        add('[^' + code + note['original_note_number'] + ']: ' + note['original_text'])
    add('**Tasks ' + code + '01–' + code + '05 — new teaching material.** Keep the modern vocabulary, construction helps and original notes available for every task.')
    shared = [s['support_id'] for s in span['local_support']]
    for n in range(1, 6):
        task(f'NEW-U15-{code}{n:02d}', shared_support=shared)

add('''## 9. Sources and selected forms

[^nouns]: Cook, A First Book in Old English, 2nd ed., pp. 28–37, especially §§43–53. Tables give selected complete models; stated alternatives remain valid.

[^abstracts]: Wright, Old English Grammar, p. 184, §§382–383, supplies the complete strengu class and its variants. Bosworth–Toller, p. 500b, treats hǣlu as indeclinable. These facts support the selected singular tables without assigning plural count uses.

[^negation]: Cook, First Book, pp. 23, 74, 78–79 and 100. The selected negative indicative forms combine the positive systems with the stated contractions; the multiword entries remain ordinary ne plus a verb.

[^pronouns]: Cook, First Book, pp. 52–53; Wright, Old English Grammar, pp. 239–240. Further indefinite and free-choice families are acknowledged only within the limits stated above.

[^verbs]: Cook, First Book, pp. 54–74 and the cited lexical entries. The class patterns determine endings and stem distribution; each newly required system is printed in full above.

[^adjectives]: Cook, First Book, pp. 39–41, §§57–59. The selected -ig syncopation and double-consonant spellings do not exclude the stated historical alternatives.

[^exercises]: Cook, Exercises in Old English (1895), IX.28–30 and X, XI.31, printed pp. 15–18 (PDF pp. 23–26). The preserved source prompts are distinct from the modern directions and helps.''')


missing_markers = sorted(set(RECORD) - SEEN_MARKERS)
missing_matrices = sorted({m['matrix_id'] for m in C['display_plan']['matrices']} - SEEN_MATRICES)
missing_tasks = sorted(set(TASK) - SEEN_TASKS)
required_support = {s['support_id'] for owner in C['assigned_items'] + C['source_spans'] for s in owner.get('local_support', [])}
missing_support = sorted(required_support - set(SEEN_SUPPORT))
text = unicodedata.normalize('NFC', '\n\n'.join(OUT).rstrip() + '\n')
(ROOT / 'chapters/ch15/student.md').write_text(text, encoding='utf-8', newline='\n')
report = {
    'role': 'lesson_author_not_independent_reviewer',
    'contract_amendments': [a.get('amendment_id', a.get('id')) for a in C.get('amendments', [])],
    'counts': {'teaching_records': len(SEEN_MARKERS), 'matrices': len(SEEN_MATRICES),
               'tasks': len(SEEN_TASKS), 'support_records': len(SEEN_SUPPORT),
               'words_with_markup': len(text.split())},
    'missing_teaching_records': missing_markers,
    'missing_matrices': missing_matrices,
    'missing_tasks': missing_tasks,
    'missing_support': missing_support,
    'locations': LOCATIONS,
    'support_locations': dict(SEEN_SUPPORT),
    'covered_forms': sorted(TAUGHT_FORMS),
    'covered_senses': sorted(TAUGHT_SENSES),
    'covered_features': sorted(TAUGHT_FEATURES),
}
(ROOT / 'build/u15-learner-generation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: v for k, v in report.items() if k in ['counts', 'missing_teaching_records', 'missing_matrices', 'missing_tasks', 'missing_support']}, ensure_ascii=False, indent=2))



