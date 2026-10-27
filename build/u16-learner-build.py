"""Render the committed Unit16 literals within the authored learner exposition."""
import hashlib
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
C = json.loads((ROOT / 'chapters/ch16/coverage.json').read_text(encoding='utf-8'))
LEX = {x['lemma_id']: x for x in C['lexical_inventory']}
FORMS = {f['form_id']: (l, f) for l in LEX.values() for f in l['forms']}
SENSES = {s['sense_id']: (l, s) for l in LEX.values() for s in l['senses']}
TEACH = {x['teaching_id']: x for x in C['teaching_records']}
PAR = {x['paradigm_id']: x for x in C['paradigms']}
MATS = {x['paradigm_ids'][0]: x for x in C['display_plan']['matrices']}
TASKS = {x['task_id']: x for x in C['assigned_items']}
EXAMPLES = {x['example_id']: x for x in C['new_material_examples']}
R = C['source_spans'][0]
out = []
marked = set()
rendered_tables = []

def emit(text=''):
    out.append(text.strip())

def mark(*ids):
    for tid in ids:
        if tid in TEACH and tid not in marked:
            emit('<!-- teaching: ' + tid + ' -->')
            marked.add(tid)

def lexical_markers(lid):
    if lid not in LEX:
        return
    for row in LEX[lid]['forms'] + LEX[lid]['senses']:
        for tid in row.get('teaching_ids', []):
            if tid.startswith(('NEW-U16-VOC-', 'NEW-U16-SUP-')) or tid.startswith('u16-'):
                mark(tid)

def table(pid):
    p, m = PAR[pid], MATS[pid]
    mark(pid)
    emit('<!-- table: ' + m['matrix_id'] + ' -->')
    lines = ['| ' + ' | '.join(m['headers']) + ' |', '| ' + ' | '.join('---' for _ in m['headers']) + ' |']
    lines += ['| ' + ' | '.join(row) + ' |' for row in m['rows']]
    emit('\n'.join(lines))
    rendered_tables.append(m['matrix_id'])

def headword(lid):
    l = LEX[lid]
    return l.get('display_headword', l.get('lemma', l.get('headword', lid)))

def new_gloss(lid):
    return '; '.join(s.get('contextual_gloss', s['gloss']) for s in LEX[lid]['senses'] if s['knowledge_status'] == 'new_production')

def example(n):
    e = EXAMPLES[f'NEW-U16-EXAMPLE-{n:02d}']
    mark(e['example_id'])
    emit('<!-- example: ' + e['example_id'] + ' -->')
    emit(e['text'])
    emit(e['translation'])

def analysis(a):
    words = []
    names = {'nom':'nominative', 'gen':'genitive', 'dat':'dative', 'acc':'accusative',
        'ins':'instrumental', 'inst':'instrumental', 'sg':'singular', 'pl':'plural',
        'm':'masculine', 'f':'feminine', 'n':'neuter', 'pres':'present', 'pret':'preterite',
        'subj':'subjunctive', 'ind':'indicative', 'imp':'imperative'}
    if a.get('person'):
        words.append({1:'first person',2:'second person',3:'third person'}.get(a['person'], str(a['person']) + ' person'))
    for key in ['tense', 'mood', 'nonfinite', 'case', 'number', 'gender', 'declension']:
        if key in a:
            v = str(a[key]); words.append(names.get(v, v))
    if not words and a.get('inflection') == 'invariant':
        words = ['invariable']
    if not words and a.get('inflection') == 'citation':
        words = ['dictionary form']
    return ', '.join(words)

emit('# Unit 16. Extended narrative and speech')
emit('A longer narrative combines events, perceptions, reports and quoted speech. The form of each clause establishes its own participants; context connects those participants across the passage. A change of speaker can change the reference of I, you, here and now without changing the people or events described.')
emit('The vocabulary and complete systems below prepare the original exercises and Cook’s complete joint Group XII, XIII, Exercises 32–36. The final reading follows Apollonius through a game at the public baths and the invitation that results from it. The four translated examples and the lettered exercises are new material.')
emit('**Scope.** Learn the productive forms for the meanings and constructions stated. A **reference** form may be consulted; it does not require unaided recall. **Recognition** forms are identified where they occur. **Supplied help** remains available during the corresponding task. In verb tables, 1, 2 and 3 denote person; singular you and plural you remain distinct. Preserve vowel length and the distinction between e and ę.')
mark('NEW-U16-PRIOR-RECALL')
emit('The previously learned case functions, strong and weak adjective choice, personal and dual pronouns, direct quotation, finite content clauses, perception with an infinitive, relative clauses, passives and perfect constructions remain in use. A familiar form does not make every meaning or complement of its verb familiar. The new extensions are stated explicitly below.')

emit('## 1. Nouns, adjectives and both')
emit('Use the nominative for a subject and the accusative for a direct object when the verb takes one. An adnominal genitive expresses possession or another noun-dependent relation. A recipient or a preposition takes its own licensed case. These ordinary uses apply to the nouns below; a special government pattern must be learned separately. Identical endings do not remove the distinction between grammatical positions.[^nominal]')

nominal_groups = [
    ('Strong masculine nouns', ['neahgebur','thothor','coss','disc','ath','tear','maegenthrymm'],
     'The nominative and accusative singular have the bare stem; the genitive adds -es and the dative -e. The plural has nominative/accusative -as, genitive -a and dative -um.'),
    ('The masculine title in -ere', ['fuluhtere'],
     'The singular retains -e in the nominative, accusative and dative; the genitive ends in -es. Here fuluhtere is learned in the singular title “Baptist”.'),
    ('Weak masculine nouns', ['cnapa','gegierela'],
     'The nominative singular ends in -a. The other singular cases and the nominative/accusative plural end in -an; the genitive plural has -ena and the dative plural -um.'),
    ('Strong neuter nouns', ['furlang','nett','tempel','maeden','wolcen'],
     'Nominative and accusative coincide in each number. The singular genitive and dative use -es and -e; the plural genitive and dative use -a and -um. Learn the nominative/accusative plural with the noun. Furlang and nętt have no ending in those plural positions.'),
    ('Strong feminine nouns', ['smyltnes','stefn','ansien','sealf','wen','spraec'],
     'The selected nouns have no ending in the nominative singular. Their other singular cases have -e; the plural, where assigned, has nominative/accusative -a, genitive -a and dative -um. Smyltnes doubles its final s before an ending.')]
special_nouns = {
    'thothor':'The medial o remains before endings. This rare word is learned for the ball exercises and the gymnasium scene.',
    'tempel':'Use templ- before the displayed vowel endings.',
    'wolcen':'Use wolcn- before the displayed vowel endings.',
    'maeden':'Retain mǣden- in the selected forms.',
    'nett':'The zero nominative/accusative plural belongs to this noun’s class; it is not inferred merely from the written double consonant.'}
for title, lids, introduction in nominal_groups:
    emit('### ' + title)
    emit(introduction)
    for lid in lids:
        lexical_markers(lid)
        p = next(p for p in PAR.values() if p['lemma_id'] == lid and p['paradigm_id'].startswith('NEW-U16-NOM-'))
        gender = {'m':'masculine','f':'feminine','n':'neuter'}[LEX[lid]['gender']]
        emit(f"**{headword(lid)}** — {gender}; {new_gloss(lid)}. Stem **{p['diagnostic_stem']}-**.")
        if lid in special_nouns:
            emit(special_nouns[lid])
        if p.get('number_scope', {}).get('pl') != 'production':
            emit('Only the singular is learned for this meaning. No count-plural sense is assigned here.')
        table(p['paradigm_id'])

emit('### Adjectives')
emit('The following tables give the complete strong and weak positive forms. Use the strong or weak series under the conditions already learned, with agreement in case, number and gender. In ordinary predicate use the adjective also agrees with its subject. The strong instrumental singular forms are for recognition only; their appearance here introduces no new instrumental construction. The other displayed positions are productive.[^adjectives]')
adj_notes = {
    'healt':'The heavy stem takes no -u in the strong feminine nominative singular or neuter nominative/accusative plural.',
    'gelared':'The selected forms keep the full gelǣred- stem before endings. Shorter contracted variants do not replace this table.',
    'eorthlic':'The selected forms keep the full eorðlic- stem before endings.',
    'nearu':'Learn the alternating stems together: nearu in the selected nominative singular forms; nearw- before vowel endings; nearo- before consonantal -ne, -re and -ra. Thus the case ending can select a different visible stem. The weak forms use nearw-.'}
for lid in ['healt','gelared','eorthlic','nearu']:
    lexical_markers(lid)
    emit(f'**{headword(lid)}** — {new_gloss(lid)}.')
    emit(adj_notes[lid])
    table('NEW-U16-ADJ-' + lid.upper())

emit('### Both')
lexical_markers('begen')
emit('**bēgen** — both. Its case and gender follow the noun or pronoun to which it refers. It has a plural declension, although it denotes two: it is not a dual inflection. It can accompany a noun or stand in apposition to a pronoun; **unc bǣm** means “to us both” and **inc bǣm**, “to you both”. The dative **bām** is also valid; neuter **bū** is an alternative to **bā**. The table selects one spelling for each position.')
table('NEW-U16-NOM-BEGEN')
lexical_markers('dom')
emit('**dōm** — judgment; a judgment made in judging. Use the previously learned singular forms, including accusative **dōm**. This ordinary judgment sense is additional to the earlier religious and fate-related uses; no new abstract plural is required.')

emit('## 2. Verbal systems and their basic uses')
mark('NEW-U16-GRAMMAR')
emit('Each indicative table gives all six person-and-number positions in the present and preterite. The basic uses beside it state the objects and complements licensed here. A present can refer to a future event when the context supplies that viewpoint; English will does not by itself require willan. Commands, subjunctives and nonfinite forms are treated separately.[^verbs]')

mark('NEW-U16-PRINCIPAL-PARTS')
emit('### Principal parts for reference')
emit('These dictionary forms show the stems from which the selected systems are formed. They remain available for reference. Productive finite forms are given in the complete tables that follow; productive nonfinite forms are identified in their own tables.')
pp_rows = []
for pp in C['principal_parts']['items']:
    pp_rows.append('| ' + pp['headword'] + ' | ' + pp['verb_class'] + ' | ' + '; '.join(pp['selected_principal_parts']) + ' |')
emit('| Verb | Class | Principal parts: reference |\n| --- | --- | --- |\n' + '\n'.join(pp_rows))

verb_prose = {
    'aeswician':('ǣswician — offend; cause someone to stumble. The person affected is accusative. In the exercise, hand or foot is a disjunctive singular subject and takes a singular verb; the meaning is moral offence, not simply physical injury.', 'Weak II. The selected present endings are -ie, -ast, -að, -iað; the preterite uses -ode, -odest, -odon. Keep ǣswic- before these endings.'),
    'blissian':('blissian — rejoice, intransitive. A companion may be introduced by mid with the dative. Ofer with the accusative introduces what one rejoices over; this use is explained again with comparison below.', 'Weak II. Add the same selected endings to bliss-.'),
    'wuldrian':('wuldrian — glorify, with an accusative person. A masculine speaker glorifying himself uses the accusative reflexive phrase mē selfne.', 'Weak II. Add the selected endings to wuldr-.'),
    'plegian':('plegian — play, intransitive. It can be modified by time and manner adverbs. The reading’s expressions for fellow players and the ball receive their own local help.', 'Weak II. The selected stems are plegi- in the plural present and pleg- before -ode/-odon. Keep the selected spelling throughout the table.'),
    'beheafdian':('behēafdian — behead, with an accusative person.', 'Weak II. Retain the prefix and behēafd- stem in the selected forms.'),
    'cleopian':('cleopian — cry aloud. The use here can introduce quoted words. The command forms are already familiar; the complete indicative is now learned.', 'Weak II, with the same selected present and preterite endings as the preceding verbs.'),
    'arisan':('ārīsan — arise; get up, intransitive. This indicative system supplements the previously learned subjunctive.', 'Strong I: ī / ā / i / i. Present -s plus -st or -ð gives the selected -st in both second and third singular. Preterite second singular uses the plural stem.'),
    'aceorfan':('āceorfan — cut off, with an accusative object. The separate particle of can reinforce “off”; it has no governed noun after it in that use.', 'Strong III: eo / ea / u / o. The second and third singular present have ie. The second singular preterite has the u-stem of the plural. Retain ā- throughout.'),
    'forleosan':('forlēosan — lose, with an accusative thing lost. Its participle can describe that thing as lost.', 'Strong II: ēo / ēa / u / o. The preterite plural and past participle also change s to r. Both second and third singular present are forlīest; preterite second singular uses forlur-.'),
    'iernan':('iernan — run, intransitive. An accusative actor with its plain infinitive can follow a verb of perception, as in the construction recalled below.', 'Strong III. The selected stems are iern-, arn, urn- and urnen. Retain the position of r and the present ie spelling; do not replace it with a later irn- or yrn- series.'),
    'thwean':('ðwēan — wash, with an accusative thing or body part. A possessor or recipient may retain the case independently required by the clause.', 'Contracted strong VI, like slēan. The contracted present alternates ēa and ie. The selected preterite singular has h, while the second singular and plural have g; the past participle is ðwegen.'),
    'bewendan':('bewęndan — turn. In the subject-directed movement used here, dative him can refer back to the subject: the subject turns toward someone. This particular dative reflexive does not make all reflexives dative.', 'Weak I with a d-stem, like sęndan. The present contracts to -ntst and -nt. The dental preterite contracts to bewęnde: present first singular and preterite first/third singular therefore coincide in spelling.'),
    'smierwan':('smierwan — anoint. The body part or person anointed is accusative; mid with the dative introduces the substance used.', 'Weak I, like gierwan. Retain w in present first singular and plural; omit it in second/third singular and in the preterite. The selected series has ie, including smierede; the singular command is smiere.'),
    'aliesan':('ālīesan — release; deliver, with an accusative person or thing. The meaning and commands continue the preceding unit; the indicative is now complete.', 'Weak I. Continue the selected ālīesan, ālīesde, ālīesed system. In the second and third singular present, contraction after s gives -st. Do not substitute a strong-verb system.')}
weak_order = ['aeswician','blissian','wuldrian','plegian','beheafdian','cleopian']
strong_order = ['arisan','aceorfan','forleosan','iernan','thwean']
other_order = ['bewendan','smierwan','aliesan']
for title, lids in [('Weak verbs in -ian', weak_order), ('Strong and contracted verbs', strong_order), ('Further weak verbs', other_order)]:
    emit('### ' + title)
    if lids == strong_order:
        emit('The ordinary strong present has singular endings -e, -st, -ð and plural -að. The preterite first and third singular have no added ending; second singular has -e on the plural stem, and all plural persons have -on. The stem changes and contractions stated below modify these ordinary combinations.')
    elif lids == other_order:
        emit('The ordinary weak-I present uses -e, -st, -ð and plural -að, with the contractions shown below. Its dental preterite stem takes singular -e, -est, -e and plural -on. Learn the selected dental stem from the reference principal part and the complete preterite column.')
    for lid in lids:
        lexical_markers(lid)
        emit('**' + verb_prose[lid][0].split(' — ',1)[0] + '** — ' + verb_prose[lid][0].split(' — ',1)[1])
        emit(verb_prose[lid][1])
        table('NEW-U16-PAR-' + lid.upper() + '-IND')

emit('### Commands')
emit('The first form addresses one person; the second addresses more than one. Use ne before a negative command. The bare-stem commands preserve their own stem changes; weak-II blissian instead has singular blissa, and smierwan has singular smiere. These are commands, not present indicative forms inferred from a matching spelling.')
for lid in ['aceorfan','blissian','smierwan','arisan','forlaetan','geswican','efthweorfan','deman']:
    lexical_markers(lid)
    if lid == 'forlaetan':
        emit('**forlǣtan** — leave; let go, with the previously learned objects and sense.')
    elif lid == 'geswican':
        emit('**geswīcan** — cease. It may be used without an expressed complement, including with a wind as subject or in an addressed command. Its genitive complement remains a separate use.')
    elif lid == 'efthweorfan':
        emit('**ęfthweorfan** — return; turn back. Retain the prefix in both commands.')
    elif lid == 'deman':
        emit('**dēman** — judge. A judgment itself may be expressed as an accusative object, as in the instruction to judge a right judgment.')
    table('NEW-U16-PAR-' + lid.upper() + '-IMP')
    if lid == 'deman':
        emit('**Immediately before gē**, use the shortened plural command **dēme gē**. Without that following pronoun the ordinary plural remains **dēmað**. This positional exception is required in the first clause of Cook 36.1; it does not replace the ordinary pair or introduce a new general command table.[^commands]')

emit('### Present subjunctives: expectation and an unspecified provider')
emit('Findan “find” and fēdan “feed” retain their previously learned indicative systems. The complete present subjunctive has -e in every singular person and -en in every plural person. The six positions remain distinct even when the forms coincide.')
for lid in ['findan','fedan']:
    table('NEW-U16-PAR-' + lid.upper() + '-PRES-SUBJ')
emit('**Wēn is ðæt** with a present subjunctive expresses the bounded expectation “perhaps; there is a prospect that …”. In the hypothetical conditional “if you find no one”, use **finde**; a relative clause identifying a possible, as-yet-unfound provider uses **fēde**. These choices concern the status of the situation, not a mechanical conversion of an English future.')
emit('Keep the previously selected preterites of findan distinct: first singular **fand**, third singular **funde**. A spelling shared with another person or mood must be interpreted from its clause.')

emit('### Participles and infinitives')
emit('The following pairs give the productive participial bases. These present participles add -ende to the present stem and describe ongoing action. Learn each past-participle stem and prefix as shown. The past participle can enter the previously learned passive or perfect constructions; in a passive, the affected participant is the subject. These bases do not themselves supply every possible adjective inflection.')
part_prose = {
    'forleosan':'Forlēosan retains the r-stem in its past participle. In the strong neuter accusative singular, **forloren** can modify a lost thing; this exact attributive position is also learned here.',
    'laedan':'Lǣdan here includes “carry; take a person”. A passive makes the person carried its subject. The endpoint in the assigned carrying event uses ōð with the accusative.',
    'gefyllan':'Gefyllan here means “fulfil a spoken prediction”. That prediction is accusative in an active clause and becomes the subject in a passive. This is distinct from physically filling a container.',
    'forgiefan':'Forgiefan here means “forgive”: the sin or offence is accusative, the person forgiven dative. In a passive the sin becomes nominative and the person remains dative. The uninflected past participle is **forgiefen** in the assigned predicative use.'}
for lid in ['forleosan','laedan','gefyllan','forgiefan']:
    lexical_markers(lid)
    emit(part_prose[lid])
    table('NEW-U16-PAR-' + lid.upper() + '-PART')
emit('The plain infinitive and the inflected infinitive after tō are separate forms. A perception construction takes the plain infinitive and an accusative actor. The previously learned purpose construction takes tō and the inflected form. A new meaning such as “is to come” still requires separate local help; it does not follow merely from knowing the ending.')
for lid in ['iernan','sendan']:
    table('NEW-U16-PAR-' + lid.upper() + '-INF')

emit('## 3. Clause structure, government and viewpoint')
emit('### Reference and finite content')
emit('A pronoun does not automatically refer to the nearest noun. Establish the speaker, addressee and continuing participant from the whole passage. A pronoun’s ending can establish its role without uniquely establishing its referent. When a new composition requires an unambiguous reference, an explicit noun phrase can resolve it.')
example(1)
emit('The quotation uses the father’s I and here. The report uses third-person hē and, under the stated change of reporting place, ðǣr. The subjunctive wǣre belongs to reported content; it does not mean that every English past verb must be replaced by an Old English subjunctive.')
example(2)
emit('With perception and a plain infinitive, the actor of the perceived action is accusative. A finite ðæt-clause has its own nominative subject and finite verb. Some finite spellings can represent more than one mood; identify only what the ending and context together warrant.')
emit('An earlier speech event does not make every situation in its content earlier still. A reported state can be simultaneous with the saying; habban with a past participle can mark an already completed event; willan with an infinitive can express an intention whose action is still ahead. Interpret the whole verb group and the stated context. Directly quoted now or today retains the quoted speaker’s viewpoint.')

emit('### Knowing, action comparison and causation')
lexical_markers('cunnan'); lexical_markers('witan')
emit('**Cunnan** can mean “know; be acquainted with” a person and take that person in the accusative. Its earlier use with a plain infinitive expresses knowing how to do something. **Witan** can introduce factual content or a question, but can also take a personal accusative object. Thus the contrast is useful without making persons and facts an exclusive division between the two verbs.[^knowing]')
example(3)
lexical_markers('don')
emit('**Dōn** can repeat an action already expressed. In an action comparison, **bęt** “better” modifies the action and **ðonne** introduces the comparison clause. Dōn then carries the tense, person and number of its own subject. It is not an auxiliary inserted to imitate modern English questions or negatives.')
example(4)
emit('A separate causative pattern is **dōn + ðæt + finite clause**, “cause that; make it be that”. The subject inside that clause remains nominative. With dual **git**, use a plural finite verb, such as **bēoð**; a noun describing both participants is plural. Do not turn the dual subject into an accusative object of dōn in this pattern.')

emit('### Government and lexical meaning')
emit('A case after a verb belongs to that verb’s construction. It is not determined by the nearest English preposition.')
emit('**Biddan** takes the requested thing in the genitive; the person asked can simultaneously be accusative. Interrogative **hwæs** asks for that requested thing. **Gīeman** “take care of” and **geswīcan** “cease from” retain their learned genitive government. **Wēnan** “expect” now also takes a genitive thing expected, including a genitive negative or a coordinated exception. Its earlier finite content-clause use does not replace this pattern.')
lexical_markers('halsian')
emit('**Hālsian** “conjure; solemnly charge” takes the person charged in the accusative. **Ðurh** with an accusative names the oath standard, and a requested **ðæt**-clause follows. An uncertain embedded identification uses a subjunctive. This person is not an ordinary dative recipient.')
lexical_markers('healdan'); lexical_markers('weorthan')
emit('**Healdan** now includes “keep; observe” a saying, with accusative sprǣc. **Weorðan** can mean “arise; come about” with an event as its subject. If a calm comes about and no participle is present, this is an intransitive lexical use, not the passive auxiliary.')
emit('With **bewęndan**, the dative reflexive can identify the person who turns toward someone. With **gān**, the genitive route pattern **ðæs weges ðe …** means “by the way by which …”. Neither construction should be generalized to every motion verb. In Cook 36.10, **āsęndan** has no expressed patient: understand “sent someone”, followed by the coordinated action.')
lexical_markers('ofer'); lexical_markers('swithe'); lexical_markers('of-adverb')
emit('With **blissian**, **ofer + accusative** names the object of rejoicing. **Swīðor** here compares its degree, “more”, and **ðonne** introduces the second object of comparison, with its own ofer phrase. It is not the earlier “rather” meaning. The separate particle **of**, “off”, has no following governed complement; prepositional **of** still governs the dative in its own uses.')

emit('### Direction, relation and time words')
function_rows = [
    ('hwanon','hwanon','whence; from where','Interrogative adverb of origin.'),
    ('hwider','hwider','whither; to where','Interrogative adverb of destination.'),
    ('togaedere','tōgædere','together','Adverb.'),
    ('geond','geond','along; through','Preposition with accusative.'),
    ('innan','innan','within; inside','Adverb in the assigned use.'),
    ('siththan','siððan','since; after; afterwards','As a conjunction, introduces a temporal clause; as an adverb, means afterwards.'),
    ('thriwa','ðrīwa','thrice; three times','Adverb.'),
    ('sona','sōna','immediately; at once','Adverb; a complete as-soon-as construction is separately supplied where required.'),
    ('aefter','æfter','after; following; according to','Dative in the three stated uses: time after an event, following a person, or conformity to something.'),
    ('into','intō','into','Destination with dative in this selected use.'),
    ('be','be','according to; concerning','Dative in both senses. The reading’s “by the hand” receives separate local help.'),
    ('thurh','ðurh','through; by way of a person','Accusative for the mediating person. Oath use is separately identified; source-local means or evidence receives help.'),
    ('for-thon-the','for-ðon','therefore; for that reason','Adverbial consequence here. Do not expand it into a because-clause merely from the related longer expression.')]
for lid, _, _, _ in function_rows:
    lexical_markers(lid)
emit('| Word | Meaning | Use |\n| --- | --- | --- |\n' + '\n'.join('| ' + ' | '.join(row[1:]) + ' |' for row in function_rows))
emit('The following exercises reuse the previously learned masculine **sǣ**. Preserve the appropriate masculine article or demonstrative with it. **Bōc** retains its learned feminine plural **bēc**. Source variants in the reading are supplied locally and do not replace the forms learned for new composition.')

emit('## 4. Form and clause practice')
mark('NEW-U16-DIRECTION-HEADWORDS')
emit('The dictionary forms printed with the form exercises are given references. Produce the requested inflections from the learned systems. If a requested position has the same form as its given headword, identify that position; it is not a test of recalling an unseen word. Explain the requested contrasts in English.')

def word_help(bindings, title='Supplied words', owner=None):
    if not bindings:
        return
    rows = []
    seen = set()
    for b in bindings:
        pair = (b['form_id'], b['sense_id'])
        if pair in seen:
            continue
        seen.add(pair)
        lexical_markers(b['lemma_id'])
        role = analysis(b.get('analysis', {}))
        gloss = b['gloss']
        if owner and owner.startswith('NEW-U16-F'):
            role = 'given dictionary form'
        if b['form'] == 'becōm' and owner == 'reading':
            role = 'third singular preterite indicative'
        if b['form'] == 'meahte' and owner == 'reading':
            role = 'third singular preterite; indicative or subjunctive in form'
        if b['form'] == 'hęrede' and owner == 'reading':
            role = 'third singular preterite; indicative reading here, with the same subjunctive spelling possible'
        if owner == 'EX-XII-XIII-35-07' and b['form'] == 'sē':
            gloss = 'who; the one who, referring to the man'
        if b['sense_id'] == 'thaet-u16-uncertain-link':
            gloss = 'that; the precise linkage at 169.6 remains uncertain (P169N6)'
        if b['sense_id'] == 'mid-u16-source-clothing':
            gloss = 'with a cloth or cloak, accompanying girded or wrapped'
        if b['form'] == 'geslægene' and owner == 'reading':
            role = 'past participle, masculine accusative singular; exceptional ending (P169N2)'
        rows.append(f"| {b['form']} | {gloss} | {role or 'as used here'} |")
    emit('**' + title + '.** These forms and meanings remain available for this task.')
    emit('| Form | Meaning | Role |\n| --- | --- | --- |\n' + '\n'.join(rows))

COOK_EXPLANATIONS = {
    'U16-CSUP-01':'About twenty furlongs or thirty; upon the sea. The supplied numerical phrase takes genitive furlanga; the prepositional phrase has the dative.',
    'U16-CSUP-02':'A hundred sheep; ninety-nine; one of those. These numerical and partitive expressions remain supplied.',
    'U16-CSUP-03':'With Mary his mother. Marian is the supplied weak-feminine form after mid here; the earlier genitive use of the name had a different function.',
    'U16-CSUP-04':'Land of the Egyptians; to their land; from the Egyptians. These foreign-name forms and their place-reference uses remain supplied.',
    'U16-CSUP-17':'True: supplied nominative masculine singular in predicate use. No complete new adjective system is required.',
    'U16-CSUP-19':'Nothing; naught. Here nāwiht is nominative in the predicate after nis, unlike its earlier accusative object use.',
    'U16-CSUP-14':'With oils. The plural dative ęlum remains supplied.',
    'U16-CSUP-12':'This woman. The feminine pronoun refers to the woman as a person, although wīf is grammatically neuter. Retain this supplied reference in the exchange.',
    'U16-CSUP-16':'John: Johannes is genitive and Johannem accusative. The endings are retained from the attested forms; initial J follows Cook’s headword. See the note on names above.',
    'U16-HELP-BETTER-CLAUSE':'The experiencer is dative ðē; bętere is the familiar neuter comparative predicate. Keep the requested ðæt in the first complement and omit it after ðonne. Earlier hit resumes whichever of the differently gendered body parts is at issue.',
    'U16-HELP-COMING-INFINITIVE':'This supplied wesan + tō + inflected-infinitive phrase expresses impending coming. Knowing the ordinary purpose infinitive does not by itself establish this use. Retain the complete expression here.',
    'U16-HELP-REWARD-CLAUSE':'Āgylt is the contracted third singular of strong āgyldan, and ǣlcum is the dative recipient. The whole clause remains supplied; see the correction above.',
    'U16-HELP-GATE-WAY-AGREEMENT':'This wording treats gate and way as a combined figurative route and retains a singular predicate. Use this supplied coordination here; it is not a general singular-agreement rule for coordinated subjects.',
    'U16-HELP-SUFFICE-BOOKS':'The verb is plural optative, agreeing with bēc. Unc is dual dative; bǣm is dative plural because both has no separate dual form. This whole sentence remains supplied.',
    'U16-HELP-LIVING-GOD':'Libbendan is the supplied weak masculine accusative singular participle agreeing with God after ðone. The finite forms of libban do not supply this adjective position.',
    'U16-HELP-RIGHT-HAND':'On has an accusative in this fixed position expression; it does not express motion by the seated person. The perceived ongoing actions use plain infinitives sittan and cuman. English -ing does not automatically require an Old English participle.',
    'U16-HELP-CESSATION-KISSING':'Both negatives belong to this attested cessation construction: the second ne does not mean that she withheld kisses. Keep the complete finite clause supplied here.',
    'U16-HELP-PROMISE-FREECHOICE':'Gehēt introduces the promise and the intended-action infinitive. Hiere is the recipient of giving, ðæt the accusative thing given. Within the free-choice request, biddan takes genitive hwæs and accusative hine; bǣde is preterite subjunctive in the open request. The resumptive ðæt lets each clause retain its own case requirement.'}

def local_support(task):
    for h in task.get('local_support', []):
        if h.get('bindings'):
            word_help(h['bindings'], owner=task['task_id'])
            continue
        text = h.get('actual_supplied_text')
        if text:
            emit('**Supplied help:** ' + text)
        for field in ['meaning','explanation']:
            if h.get(field):
                emit(COOK_EXPLANATIONS.get(h.get('support_id'),h[field]) if field == 'explanation' else h[field])
        if not text and h.get('text'):
            emit(h['text'])

def task(tid):
    t = TASKS[tid]
    code = 'Cook XII, XIII.' + '.'.join(str(int(x)) for x in tid.split('-')[-2:]) if tid.startswith('EX-') else tid.split('-')[-1]
    emit('**' + code + '**')
    emit('<!-- item: ' + tid + ' -->')
    emit(t['prompt'])
    if not tid.startswith('EX-'):
        if t['input_sequences']:
            for n, seq in enumerate(t['input_sequences'], 1):
                emit(f'({n}) ' + seq['text'])
        if tid.startswith('NEW-U16-R'):
            for item in t.get('inputs', []):
                if isinstance(item, dict) and item.get('anchors'):
                    emit('Selected passages: ' + '; '.join(item['anchors']) + '.')
            excerpts = {
                'NEW-U16-R03':['FB169-04','FB169-14','FB169-15','FB169-16','FB170-09'],
                'NEW-U16-R05':['FB170-14','FB170-15','FB170-16'],
                'NEW-U16-R06':['FB169-05','FB169-06','FB169-07','FB169-11','FB169-12','FB169-13']}
            if tid in excerpts:
                emit('Source wording for the cited locations:')
                for line in R['source_lines']:
                    if line['source_line_id'] in excerpts[tid]:
                        source_text = re.sub(r'\[\d+\]', '', line['source_with_note_markers'])
                        emit(line['source_line_id'].replace('FB','').replace('-','.') + ': ' + source_text)
        else:
            local_support(t)
    else:
        local_support(t)
    if tid.startswith('EX-'):
        for p in t['output_positions']:
            emit('<!-- output: ' + p['output_position_id'] + ' -->')
        return
    for n, p in enumerate(t['output_positions'], 1):
        emit('<!-- output: ' + p['output_position_id'] + ' -->')
        emit(f"({n}) {p['label']}: ____________________")

for tid in [f'NEW-U16-F{n:02d}' for n in range(1,6)] + [f'NEW-U16-A{n:02d}' for n in range(1,4)]:
    task(tid)
emit('## 5. New compositions')
emit('Translate every clause and identify the requested relations. Keep a grammatical alternative distinct from compliance with an explicitly requested verb or construction.')
for n in range(1,4):
    task(f'NEW-U16-C{n:02d}')

emit('## 6. Cook: Group XII, XIII, Exercises 32–36')
mark('NEW-U16-COOK-SUPPORT')
emit('Translate the complete original prompts. Parenthesized words, omissions, number instructions and order directions belong to Cook’s exercises. The modern helps below are additional and remain available; a supplied expression does not require independent recall. Cook’s paragraph numbers refer to his grammar, but the material needed here is stated in this unit.[^cook]')
emit('**Source correction for 34.9.** Cook prints “reward (āgyltan, 113)”. The verb meaning “repay; reward” is strong **āgyldan**, belonging with §104; **āgylt** is a valid contracted third singular. The complete reward clause is supplied with the item. No additional full conjugation is required. The original prompt is retained.[^reward]')
emit('**Names in 36.9–10.** The supplied **Johannes** is genitive and **Johannem** accusative. Their endings are directly attested with initial I; initial J is used here to follow Cook’s headword. These name forms remain supplied.[^john]')
for ex, count in [(32,11),(33,10),(34,13),(35,14),(36,11)]:
    emit('### Exercise ' + str(ex))
    for n in range(1,count+1):
        task(f'EX-XII-XIII-{ex:02d}-{n:02d}')

emit('## 7. The Incidents in the Gymnasium')
mark('NEW-U16-READING-SUPPORT')
emit('Apollonius has survived a shipwreck. A fisherman has shared clothing with him and shown him the road to the city. This scene begins as he follows that road; it ends with the king’s invitation. The following feast is outside the passage.')
emit('The text is Cook’s complete scene at printed pages 168.1–170.16. A locator such as 169.6 means printed page 169, editorially counted line 6, anchored by the edition’s printed line numbers. P169N6 instead means original note 6 on page 169. Original notes and modern help are kept separate; a question in an original note is not an additional exercise.[^reading]')
emit('### Supplied vocabulary and constructions')
emit('The following help is local to this reading. Retain the learned productive systems where they apply; the additional forms, spellings, meanings and constructions listed here may be consulted throughout the reading tasks.')

# One common glossary makes every R-task lexical help available without six copies.
reading_bindings = next(h['bindings'] for h in TASKS['NEW-U16-R01']['local_support'] if h.get('bindings'))
word_help(reading_bindings, 'Reading forms and meanings', owner='reading')
emit('**Further verbal help.** The following notes identify the action or construction in the exact source form.')
for v in R['verbal_glossary']:
    lexical_markers(v['lemma_id'])
    loc = v['source_line_id'].replace('FB','').replace('-', '.')
    verbal_notes = {
        ('168.03','inēode'):'The prefixed form means went in; its finite verb is part of the word.',
        ('168.07','cleopode'):'Preterite third singular of cleopian in the cry-aloud sense. Micelre stefne expresses the manner or means, “with a loud voice”.',
        ('169.01','iernende'):'The supplied present participle accompanies Apollonius. The printed division iern-/ende is joined in the reading.',
        ('169.04','slōh'):'The supplied h spelling is a valid singular variant of the previously selected slōg.',
        ('169.03','geslægene'):'The participial phrase refers to the accusative ðone ðoðor. Retain the unusual printed -e, to which Cook draws attention in P169N2.',
        ('169.09','hęrede'):'Hine is the person praised. The selected indicative interpretation fits the known event, but the third-singular preterite subjunctive has the same spelling; the ending alone does not distinguish them.',
        ('169.10','arn'):'Third singular preterite of iernan, as in the learned table.',
        ('169.11','swang'):'Its direct object is top, tentatively “ball”. The Latin parallel describes rubbing or anointing with ointment; retain the actual Old English action rather than replacing it by that parallel.',
        ('170.03','nāt'):'The supplied contracted negative means “I do not know”. Only this local form of nytan is required.',
        ('170.02','āgān'):'Past participle in āgān wæs, “had gone away”. Its second vowel is long; the second vowel of āgan “began” at 168.17 is short.',
        ('169.14','ðēnode'):'The dative him is the person served. Retain the source’s -ode spelling.'}
    explanation = verbal_notes.get((loc,v['surface']),v['explanation'])
    explanation = re.sub(r'\b(?:Cook |source )?note(\d+)\b', lambda m: 'P' + loc.split('.')[0] + 'N' + m[1], explanation)
    explanation = explanation.replace('StrongIII', 'Strong III').replace('strongI ', 'strong I ')
    emit('**' + loc + '. ' + v['actual_supplied_text'] + '.** ' + explanation)
for h in R['modern_support']:
    locs = ', '.join(x.replace('FB','').replace('-', '.') for x in h['source_line_ids'])
    reading_notes = {
        'U16-RSUP-15':'The genitive names the route followed, as in the pattern taught above; the relative ðe identifies that route. Retain the past-time reference of the source wording.',
        'U16-RSUP-17':'An oath by the common safety or welfare. Hǣle is feminine accusative singular, here in the safety/rescue sense. No possessive “our” is printed.',
        'U16-RSUP-14':'Use P169N11 and P169N14–P169N16 for the pronoun chain. The later him is reflexive; the by-the-hand phrase specifies how one person leads another.',
        'U16-RSUP-12':'Retain the Old English action with top, tentatively a ball. Cook’s Latin parallel describes rubbing or anointing with ointment and its rejuvenating effect; it names no shoulder or neck. Wǣre belongs to the imagined transformation comparison.'}
    explanation = reading_notes.get(h['support_id'],h['actual_supplied_text'])
    explanation = re.sub(r'\b(?:Cook |source )?note(\d+)\b', lambda m: 'P' + h['source_line_ids'][0][2:5] + 'N' + m[1], explanation)
    emit('**' + locs + ': ' + h['source_phrase'] + '.** ' + explanation)
emit('**The Latin parallels in English.** Original P169N6 compares the difficult knowledge/equal clause with a Latin account in which the king has long known his own skill to be without an equal. This parallel helps explain Cook’s concern but does not settle every Old English pronoun or cancel **næfde**. Original P169N10 quotes a Latin account of rubbing or anointing with an ointment used by wrestlers; it does not name a shoulder or neck. Keep the Old English **swang ðone top** and the note’s tentative interpretation distinct from that Latin action. No Latin translation is required.')
emit('**Quotation punctuation.** The edition begins a quotation at 170.2 but does not print its expected closing mark before the next narrated action. The final invitation also mixes quoted and reported wording. The text below retains those signs and constructions; they are not silently regularized.')

emit('### Source text')
emit('<!-- passage: ' + R['source_span_id'] + ' -->')
annotated_lines = []
for line in R['source_lines']:
    page = line['printed_page']
    annotated = re.sub(r'\[(\d+)\]', lambda m: '[^P' + str(page) + 'N' + m[1] + ']', line['source_with_note_markers'])
    annotated_lines.append(annotated)
annotated_words = '\n'.join(annotated_lines).replace('-\n', '').replace('\n', ' ').split()
assert len(annotated_words) == 444
cursor = 0
for paragraph in R['learner_paragraphs']:
    length = len(paragraph.split())
    rendered = ' '.join(annotated_words[cursor:cursor+length])
    assert re.sub(r'\[\^[^\]]+\]', '', rendered) == paragraph
    emit(rendered)
    cursor += length
assert cursor == 444
emit('### Original notes')
for note in R['original_notes']:
    emit('[^' + note['display_id'] + ']: ' + note['original_text'])

emit('### Reading tasks')
emit('Use the whole text, the original notes and the supplied modern help for all six tasks. A supported interpretation should preserve the actual negative and clause structure while acknowledging a genuine uncertainty. The line excerpts below are locating aids; interpret the complete clause in the continuous reading.')
for n in range(1,7):
    task(f'NEW-U16-R{n:02d}')

emit('## Sources and editorial notes')
emit('[^nominal]: Cook, *A First Book in Old English*, §§43–53, with the noun entries in *Exercises in Old English*, pp. 18–22. For nętt, Wright, *Old English Grammar*, §§355–356 explicitly assigns nett to the cyn(n) type. The limited singular meanings are teaching limits, not claims of historical defectiveness.')
emit('[^adjectives]: Cook §§57–62 and 79; Wright §§435–436 for the u/o/w alternation of nearu. The tables retain the selected complete uncontracted systems where alternatives are possible.')
emit('[^verbs]: Cook §§95–116 and the cited vocabulary entries; Wright pp. 262–263 for contracted slēan/ðwēan preterites and pp. 270–274 for the gierwan/smierwan pattern. The selected spellings are teaching forms; attested alternatives are not thereby declared ungrammatical.')
emit('[^commands]: Cook §95, note: the plural command has the shortened form before a following subject pronoun. Here the additional productive position is specifically dēme gē.')
emit('[^knowing]: Bosworth–Toller, s.v. cunnan, distinguishes acquaintance with a person from the infinitival ability construction; personal-object witan is also attested and is expressly requested by Cook 35.7.')
emit('[^cook]: Cook, *Exercises in Old English* (1895), joint Group XII, XIII, pp. 18–22, Exercises 32–36. All 59 numbered prompts and their controls are retained.')
emit('[^reward]: The printed hint in 34.9 confuses weak āgyltan with strong āgyldan “repay; reward”. Cook’s strong-verb treatment, Bosworth–Toller s.v. ā-gildan, and the West Saxon Matthew 16.27 support the correction and contracted āgylt. The English prompt itself is unchanged.')
emit('[^john]: The West Saxon Gospels, Matthew 14.8 and 14.10, printed p. 114, have genitive Iohannes and accusative Iohannem. Initial I → J is the only declared normalization in the supplied name forms.')
emit('[^reading]: Cook, *A First Book in Old English*, second edition (1895), pp. 168–170, “The Incidents in the Gymnasium”; one-based PDF pp. 184–186. All 54 original notes and 59 anchors are retained. Modern help interprets the exact reading without replacing it by its Latin parallels. For ceroma, the Latin lexicon meaning is wrestlers’ ointment.')

missing = sorted(set(TEACH) - marked)
if missing:
    # Report a real missing location; never append anonymous markers to pass a check.
    raise RuntimeError('Teaching locations still need prose: ' + ', '.join(missing))
assert len(rendered_tables) == len(set(rendered_tables)) == 56
text = unicodedata.normalize('NFC', '\n\n'.join(out) + '\n')
(ROOT / 'chapters/ch16/student.md').write_text(text, encoding='utf-8', newline='\n')
print(json.dumps({'student_words': len(text.split()), 'teaching_locations': len(marked), 'tables': len(rendered_tables), 'bytes': len(text.encode('utf-8'))}))
