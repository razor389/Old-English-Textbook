"""Reviewer-owned comparison ledger; never writes the frozen solutions or masters."""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
def read_json(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))

def read_text(path):
    return (ROOT / path).read_text(encoding='utf-8-sig')

contract = read_json('chapters/ch15/coverage.json')
witness = read_text('chapters/ch15/independent-solutions.md')
student = read_text('chapters/ch15/student.md')
key = read_text('chapters/ch15/answer-key.md')
answers = {}
for m in re.finditer(r'<!-- output: (.*?) -->\s*(.*?)(?=<!-- (?:output|item):|\n## |\Z)', witness, re.S):
    assert m.group(1) not in answers
    answers[m.group(1)] = m.group(2).strip()
assert len(answers) == 322 and all(answers.values())
assert hashlib.sha256((ROOT / 'chapters/ch15/independent-solutions.md').read_bytes()).hexdigest() == '2abad21bf90cf8994afbb7e48ec0807b74ab3d1e4cddf80cb30513845ca592fe'
tasks = {t['task_id']: t for t in contract['assigned_items']}

if len(sys.argv) > 1 and sys.argv[1] == 'show':
    prefixes = sys.argv[2:]
    for t in contract['assigned_items']:
        if any(t['task_id'].startswith(p) for p in prefixes):
            print(t['task_id'], t['mode'])
            for o in t['output_positions']:
                print(o['output_position_id'], o['kind'], o.get('label', ''), '|', answers[o['output_position_id']])
                if o['kind'] == 'form':
                    print('CONTRACT:', o.get('lemma_id'), o.get('analysis_selector'), o['display_route']['surface'])
    sys.exit(0)

# These judgments were written after personally comparing the completed blind
# answers with the actual prompts, key, canonical contract and inspected evidence.
# This script assembles the record; it does not infer grammatical acceptance.
rationales = {}
conclusions = {}
def add(short, rationale, output_conclusions=None):
    tid = short if short.startswith('EX-') else 'NEW-U15-' + short
    assert tid in tasks and tid not in rationales
    rationales[tid] = rationale
    if output_conclusions is not None:
        nonforms = [o for o in tasks[tid]['output_positions'] if o['kind'] != 'form']
        assert len(nonforms) == len(output_conclusions), (tid, len(nonforms), len(output_conclusions))
        for o, conclusion in zip(nonforms, output_conclusions):
            conclusions[o['output_position_id']] = conclusion
    elif len(tasks[tid]['output_positions']) == 1:
        conclusions[tasks[tid]['output_positions'][0]['output_position_id']] = rationale

add('F01', 'All twelve negative-copula positions match the actual selected present/preterite indicative system. The explanation preserves separate ne where taught and the contractions nis/næs/nǣre/nǣron; repeated plural spellings retain distinct person positions. Cook78–79 and100 corroborate the negative system. No subjunctive or universal contracted present is inferred.', [
    'The witness counts twelve grammatical positions and correctly distinguishes the five present positions with separate ne from nis and the six contracted preterite positions. This answers the explanation rather than merely counting distinct spellings.'
])
add('F02', 'All twelve nabban forms match the selected negative-possession paradigm, including næfst/næfð, nabbað and the weak preterite series. Four requested meanings distinguish present from past and first singular from third plural. Cook74 with the negative contraction discussion on23 supports the pattern.', [
    'Næbbe with ic is present first-singular denial of possession; the witness supplies that meaning without turning it into unwillingness.',
    'Nabbað with hīe is present third-plural denial of possession; the plural meaning is explicit despite the shared plural ending.',
    'Næfde with ic is preterite first-singular denial of possession; past time is retained.',
    'Næfdon with hīe is preterite third-plural denial of possession; both the past and plural values are retained.'
])
add('F03', 'All twelve selected negative willan forms match; nelle/nelt/nele/nellað and nolde/noldest/noldon are not confused with negative possession. Four translations preserve volition and tense. The selected e-series is legitimate alongside documented variants, but a selected-series task need not accept every variant as compliance. Cook79 supplies the system.', [
    'Ic nelle gān is present first-singular unwillingness or refusal to go; the witness preserves volitional meaning and the plain infinitive.',
    'Ðū nelt gān addresses one person and expresses present refusal; the witness retains both person and volition.',
    'Ic nolde gān expresses past refusal by the speaker; it is not merely a mechanical future-in-the-past.',
    'Ðū noldest gān expresses past refusal by one addressee; the witness keeps the distinctive second-singular preterite.'
])
add('F04', 'All twenty-four four-case strong nān positions agree with the visible selected table. Masculine accusative nānne, feminine -re obliques, selected feminine plural nāna and neuter endingless forms are all retained. Cook52 states strong nān and Cook39–40 supplies the adjective endings. The explanation distinguishes agreement from syncretism.', [
    'The witness correctly derives gender/number from the head noun and case from construction. Its account of nānum covers masculine/neuter dative singular and all dative plurals within this expressly four-case table; it does not collapse them into one grammatical cell.'
])
add('F05', 'All eight personal/neuter singular gehwā positions match the selected hwā-derived forms. Personal gehwone is distinguished from neuter gehwæt. Cook52–53 and Wright240 support the compound and singular distribution. Neither the task nor the key invents plural cells or distinct personal masculine/feminine declensions.', [
    'The witness correctly explains distributive personal reference and neuter everything, with singular grammar in both columns; many possible referents do not create a plural paradigm.'
])
add('F06', 'Both complete eight-position root-noun paradigms match: bōc/bēc/bōca/bōcum and tōð/tōðes/tēð/tōða/tōðum. The explanations identify the different umlaut distributions and each syncretic surface. Cook31–32 and36 support the root patterns and recorded alternatives, without promoting alternatives to the selected-cell target.', [
    'The witness locates bōc umlaut in genitive/dative singular and nominative/accusative plural, and tōð umlaut in dative singular and nominative/accusative plural; the two systems are not treated as identical.',
    'The witness correctly counts four bēc cells and three tēð cells, alongside the two uninflected nominative/accusative singular cells. It identifies the distinct plural genitives/datives and tōðes rather than treating a repeated surface as one case.'
])
add('F07', 'The full sweostor paradigm matches the selected system: unchanged sweostor except sweostra and sweostrum. Cook37 explicitly gives this exception. Both explanations distinguish distinct spellings from case/number positions; the comparison with bōc is accurate.', [
    'Three selected sweostor surfaces are correctly contrasted with the four selected bōc surfaces; this is a spelling count, not a reduction in grammatical positions.',
    'The witness correctly assigns unchanged sweostor to all singular cases and plural nominative/accusative, requiring syntax, agreement and context to choose the intended cell.'
])
add('F08', 'All eight assigned singular positions are correct: hǣtu/hǣte and invariant hǣlu. Wright184 corroborates the feminine abstract class and its variants; the BT500b hǣlu entry explicitly supports indeclinability. The key and witness correctly leave plural meanings unassigned rather than claiming historical nonexistence.', [
    'The witness distinguishes selected hǣtu nominative -u and oblique -e from unchanged hǣlu in every assigned singular case.',
    'The witness correctly treats the plural blanks as an instructional/sense boundary, not as evidence that historical plural forms could never occur. No count-plural production is assessed.'
])
add('F09', 'All sixteen weak masculine gerēfa/lēoðwyrhta positions agree with the actual table and key. Cook37 provides the weak -a/-an/-ena/-um system; the exercise scans supply the lexical heads. The compound explanation inflects the complete final head and does not separately inflect lēoð-.', [
    'The witness correctly makes wyrhta the weak masculine head and attaches the inflection after lēoðwyrht-. The first compound member receives no separate case ending.'
])

add('A01', 'All six outputs distinguish the actual negative expressions from the single proposition denied in each clause. Negative concord is interpreted as one denial, including the subject/object quantifiers in the third clause; the key supplies complete meanings. Cook100 §183 confirms the construction.', [
    'Nān and finite ne are both identified in the first clause.',
    'The first clause denies the coming of any man; it is not a double-negative affirmation.',
    'Nǣfre and finite ne are both identified in the second clause.',
    'The second clause denies any occasion of the king’s coming, preserving never and past tense.',
    'Nān, nāwiht and finite ne are all identified in the third clause; none is silently omitted.',
    'The third clause denies any possession by any man. The witness explicitly avoids the weaker not-all interpretation and the false positive reading.'
])
add('A02', 'Three outputs correctly distinguish constituent nā from finite ne. The first assertion remains affirmative with self and a contrasted excluded person; the second negates going. The same distinction is required by source31.2.', [
    'Nā scopes over the contrasted participant and leaves the assertion that the speaker goes affirmative.',
    'Ōðer is correctly identified as the excluded participant, contrasted with ic self.',
    'Ne negates the finite proposition ic gā; the witness correctly translates the second clause as not going.'
])
add('A03', 'The nine outputs correctly identify interrogative, contingent indefinite and free-choice hwā, give their meanings, and separate subordinate subjects from the main subject/recipient. The actual examples and visible construction teaching supply the distinction; an English analysis is not a new productive paradigm.', [
    'The first hwā is correctly classified as interrogative.',
    'Who comes? preserves the direct question and present event.',
    'Hwā is correctly identified as nominative subject of cymð.',
    'The second hwā is correctly classified as an indefinite within the possible if-clause.',
    'The second translation preserves the condition, possible visitor, gift and resumed recipient; the future English rendering of present sęlle is legitimate.',
    'The witness separates subordinate hwā/cume from main ic/sęlle, rather than taking both verbs with one subject.',
    'The third hwā belongs to swā hwā swā and expresses open free choice.',
    'Whoever comes preserves the third clause’s free-choice force and the promised book.',
    'The witness identifies hwā as internal subject, ic as main subject and him as main dative recipient, preserving the two constructions.'
])
add('A04', 'All four outputs correctly contrast distributive singular ǣlc with collective plural ealle and identify the actual subject heads/finite agreement. The witness does not infer plural agreement merely from the number of people distributed over.', [
    'Ǣlc distributes a penny to each individual man, preserving the singular distributive meaning.',
    'Mann is the singular nominative head and hæfð has third-singular agreement.',
    'Ealle quantifies the plural men as a group; the possession of food is retained.',
    'Męnn is the plural nominative head and habbað has plural agreement in this third-person context.'
])
add('A05', 'Four answers identify inclusive both-and, each accusative object, and the absence of an exclusive either-or choice. The finite predicate and the son’s possession are preserved.', [
    'Ǣgðer ge … ge contributes both … and and includes both objects of loving.',
    'Ðone cyning is correctly identified as the first accusative object.',
    'His sunu is correctly identified as the second accusative object, with his retained.',
    'Both participants are included; the witness correctly rejects an exclusive choice of one.'
])
add('A06', 'Five answers preserve the contrast between defective impersonal man and ordinary count mann. Both given finite verbs are singular, but that shared agreement does not erase the reference contrast. Cook53 §89e confirms impersonal nominative singular man.', [
    'Impersonal man denotes people in general and is the subject of the first clause.',
    'Sceal is correctly recognized as third-person singular.',
    'Se mann refers to a particular man and is the nominative singular subject of the second clause.',
    'Gǣð is correctly recognized as third-person singular.',
    'The witness does not construct oblique or plural impersonal-pronoun cells from generic reference; it keeps the ordinary noun’s inflection separate.'
])
add('A07', 'All six outputs distinguish equal degree, preference and proportional correlation. The standards retain their original syntactic roles; the feminine pronoun in the third sentence refers to bōc. The analyses match the actual inputs rather than importing one universal swā meaning.', [
    'The first comparison is equality in goodness between this and that book.',
    'Sēo bōc is the equal-degree standard, with its copular predicate understood.',
    'The second comparison expresses preference for light over darkness, not relative brightness.',
    'Ðīestru retains the accusative object role parallel to lēoht; ðonne does not assign it nominative case.',
    'The third comparison expresses correlated increases in size and quality, preserving the larger … the better relation.',
    'Swā hēo bętere is correlates with the size clause, and hēo refers to feminine bōc. The witness correctly rejects equal size and goodness.'
])
add('A08', 'Three answers correctly analyze the ordinary resumed free-choice pattern. Hwā’s nominative is set by its own clause and him’s dative by main-clause giving; source31.12’s separately supplied attraction is not imposed here.', [
    'Hwā is nominative as subject of cume within its own clause.',
    'Him is dative as recipient of the book in the main clause.',
    'Resumption allows the same referent to occupy two case-governed roles; the subordinate subject need not become dative.'
])
add('A09', 'Four answers distinguish personal genitive dual uncer in ānum uncer from the agreeing possessive uncer in uncer hūs. The external recipient remains dative and only one of the two is selected. Earlier pronoun teaching and Cook90 partitive genitive support the analysis.', [
    'Uncer after ānum is correctly interpreted as the personal genitive of us two, defining the selected group.',
    'Uncer with hūs is the agreeing possessive our, nominative neuter singular in this clause; it is not the same syntactic use as the partitive.',
    'Ānum is dative because the selected person receives the gift.',
    'The group has exactly two members, but the gift’s selected recipient is one; dual and singular roles are kept separate.'
])
add('A10', 'Four answers preserve anything in an open question, nothing under negation, and something in an affirmative clause. The middle ne/nāwiht combination is one denial, not a positive assertion.', [
    'Does he have anything? correctly preserves the information-seeking question.',
    'He has nothing correctly denies possession in the middle clause.',
    'He has something correctly asserts possession in the last clause.',
    'Nāwiht specifies no thing possessed and ne negates the finite assertion; their concord does not cancel the denial.'
])
add('A11', 'Three answers distinguish the indefinite introduction from the cardinal contrast without inventing different morphology. Both ān forms agree with nominative masculine singular mann.', [
    'The story-opening ān introduces an unnamed/certain man and need not assert an exact numerical contrast.',
    'The contrasted ān is cardinal one rather than two.',
    'Both forms have the same strong nominative masculine singular agreement; discourse, not a different ending, selects the sense.'
])
add('A12', 'Four outputs match the actual displayed lexical patterns: hēafd-/hēafdu versus retained fōtsceamul-. Cook33 explicitly names hēafdu and the syncope; the exercise source supplies fōtsceamul. The diagnosis properly treats stem behavior as lexical rather than deleting all medial vowels.', [
    'Hēafd- is the correct ending-bearing stem of hēafod.',
    'Hēafdu is the selected nominative/accusative plural, matching the learner table, key and Cook33.',
    'Fōtsceamul- is the retained stem in the actual displayed paradigm.',
    'The witness correctly contrasts the two patterns and identifies fōtsceaml- as the erroneous result of blanket deletion. It does not infer an unrestricted sound rule from one noun.'
])

add('C01', 'Nān mann ne hæfð bōc; gehwā hæfð męte preserves both propositions, negative concord and singular distributive gehwā. Both clauses use taught possession syntax; no hidden alternative lexical target is imposed.')
add('C02', 'Ic næfde ðā bōc, and ic nolde gān meets the explicit contracted-preterite targets for possession and volition. The book and refusal to go are both retained; an uncontracted alternative would be grammatical but would miss this stated control.')
add('C03', 'The witness’s question uses ǣnige with feminine accusative bōc; its answer uses nāne and finite ne. Both are correct, and the reply’s object-before-verb order differs harmlessly from the model while preserving the actual lexical targets.')
add('C04', 'Gif hwā bōc hæbbe, ic him pęning sęlle uses indefinite hwā, the requested potential present subjunctive, the possessed book, a resumptive dative recipient and a penny given. Indicative conditions may be valid in other contexts, but this target is explicit and met.')
add('C05', 'Swā hwā swā gā, ic him pęning sęlle meets the free-choice frame and present subjunctive target, with dative resumption and the complete promise. The analysis does not replace whoever with a merely factual condition.')
add('C06', 'Swā hwæðer ðissa twēgra suna swā ǣrest cume, ic him ðā bōc sęlle correctly preserves the two-son group, internal nominative subject, first arrival, present subjunctive and explicit main dative. It does not import the separately supplied source-specific attraction of31.12.')
add('C07', 'Man mæg gān uses the requested impersonal subject, singular ordinary-ability magan and plain infinitive. It preserves one can go without adding a plural impersonal paradigm.')
add('C08', 'Ǣlc sunu hæfð āne bōc; ealle ðā suna habbað męte correctly contrasts distributive singular and quantified plural. Āne agrees with feminine accusative bōc; both finite verbs agree with their actual subjects.')
add('C09', 'Ic gesēo ǣgðer ge ðone cyning ge his sunu includes both accusative objects in the requested inclusive construction. The possession relation his sunu and the seeing predicate are retained.')
add('C10', 'Swā ðæt hūs māre is, swā hit bętere is gives the requested proportional comparison. Both comparatives fit the neuter singular house and hit resumes it; this is not the equality construction.')
add('C11', 'Ðēos bōc is swā gōd swā sēo bōc, ac ðæs cyninges bōc is bętere preserves this/that, equal goodness and the king’s better book. The feminine nominative comparative and dependent genitive are correct.')
add('C12', 'Hē lufað męte swīðor ðonne wīn preserves preference and the requested swīðor construction. Męte and wīn are parallel accusative objects, so the standard is not falsely recast as a subject.')
add('C13', 'Ne gā; sęle ðǣm ðearfan ðā bōc preserves the singular prohibition and affirmative command with accusative book/dative poor recipient. The key’s wǣdlan and witness’s ðearfan are both taught weak nouns for the poor person; no lexical selection in this prompt excludes the latter. Unit14 explicitly teaches ðearfa and its dative.')
add('C14', 'Hē self gǣð, and nā ōðer keeps the man’s going affirmative and excludes another person through constituent nā. Self agrees with the masculine subject; finite ne would change the requested proposition.')
add('C15', 'Ic nāwiht nānum ne sęlle retains all three explicit negative targets, the accusative thing given and dative recipient, expressing one denial. Substantival nānum is licensed by the unit’s nān as no one; the key’s added męnn is not a hidden requirement.')
add('C16', 'Nānes mannes sunu ne cymð correctly places the negative dependent genitive within the subject noun phrase and finite ne in the clause. The son is singular subject, not an object of denial.')
add('C17', 'Se cyning næfð nāna bēc uses the requested contracted possession form and selected feminine accusative plural nāna with bēc. The root-noun plural is correct; a valid uncontracted ne hæfð would not satisfy this particular stated target.')
add('C18', 'Se cyning gesiehð gehwone; gehwæs sunu is gōd uses personal accusative gehwone as the first direct object and genitive gehwæs as the second clause’s dependent possessor. Both explicit targets and complete propositions are retained.')
add('C19', 'Ān mann cōm, and hē hæfde bōc correctly introduces an unnamed man and continues with past possession. Bare bōc is valid for an indefinite book; the prompt does not require an exact numerical contrast or an additional ān.')

add('D01', 'The four summaries follow the actual103-word Duties selection: misuse of entrusted goods, withdrawal/pauperhood, hundredfold recompense and eternal bliss, with the Savior and rich man distinguished from the embedded plural audience. No later unassigned passage is needed. The personally viewed Cook159 image confirms the bounded argument and its notes.', [
    'The witness identifies withholding/neglect of the Savior’s entrusted goods and failure to remember the promised recompense. This captures the two rebukes without inventing an unrelated fault.',
    'Withdrawal from the Savior’s bounty and consequent pauperhood in worldly life are both retained. Prospective English will is appropriate to the local present forms and supplied source note.',
    'The witness retains hundredfold repayment, identification of aid to the least with aid to the Savior, and eternal bliss in heaven. Bliss correctly renders drēam here.',
    'The outer addressee is the rich man; the embedded gospel saying addresses plural gē/ēow. The witness does not treat all second-person forms as one unchanged number.'
])
add('D02', 'Both answers correctly analyze negative volition with its plain infinitive and the continuing present intention inside the remembered proposition. The key does not demand English tense backshift merely because the question is past.', [
    'Noldest is preterite indicative second-singular negative willan, governing geðęncean. Refused/would not remember preserves volition rather than reducing it to simple non-occurrence.',
    'Ic wille states the speaker’s continuing intention to repay; the witness correctly rejects compulsory past backshift of the embedded promise.'
])
add('D03', 'All four requested roles in the quoted saying are correctly separated: free-choice object, immediate least-one recipient, the Savior as ultimate recipient, and resumed hit. The actual Cook159 wording, including both sęllað clauses, is retained.', [
    'Swā-hwæt-swā is the accusative neuter free-choice thing given, not the subject or recipient.',
    'Ānum of mīnum ðǣm lǣstum identifies the immediate dative recipient selected from the least ones.',
    'Mē identifies the Savior as the person to whom the gift is also given.',
    'Hit resumes the given thing as the second clause’s accusative object; it does not refer to the poor recipient.'
])
add('D04', 'The two answers distinguish partitive selection with of plus dative from reciprocal reward with wið plus dative. Partitive meaning does not automatically make the of phrase a genitive; all actual case forms are accounted for.', [
    'Ānum is dative singular recipient and of governs the dative plural mīnum ðǣm lǣstum. The witness correctly identifies substantival least ones and rejects a genitive parse based only on meaning.',
    'Wið ðǣm means in return for that gift/deed and governs dative singular. It describes exchange rather than selection from a group.'
])
add('D05', 'The independent complete translation preserves every clause of the103-word source: both rebukes, removal from bounty and pauperhood, refusal to remember, good deed for the Savior’s name, hundredfold repayment, both gospel reporting participles, gift to a least one as gift to the Savior, and eternal bliss in heaven. Its future English for prospective presents is supported. The source’s outer speech remains deliberately open; no closing continuation is fabricated. Comparison with the actual key and Cook159 image found no essential omission.')

add('P01', 'Five answers accurately outline both translation methods, Alfred’s mental/bodily and political obstacles, anterior study/translation followed by verse, and the charitable request to readers. The complete152-word Cook162 selection supplies all facts; the witness does not confuse the modern exercise author with Alfred.', [
    'Word be worde is verbal correspondence, word for word; the witness preserves the first method.',
    'Andgiet of andgiete is sense correspondence, sense for sense; it is not another label for identical wording.',
    'The worldly cares are various/manifold and affect both mind and body; the witness also retains the hard-to-count troubles of the governed kingdoms.',
    'Study and Latin-to-English discourse/prose translation precede the subsequent versification. The witness preserves this temporal sequence.',
    'The reader is asked to pray for Alfred and refrain from blame if understanding more correctly; the witness includes the stated limitations of understanding and leisure.'
])
add('P02', 'All five pronominal referents and the comparison contrast are correct. Cook162 notes6–7 explicitly distinguish the reader’s hē from Alfred’s hē; identical spelling does not give a single referent throughout.', [
    'Hē before gebidde is the prospective reader who is asked to pray.',
    'Hine after for is Alfred, the person prayed for.',
    'Him before ne wīte is Alfred, the person not to be blamed.',
    'Hē after gif is the reader whose understanding may be more correct.',
    'Hē after ðonne is Alfred, whose capacity forms the comparison standard.',
    'The witness explicitly contrasts reader and Alfred across the two hē tokens and recovers understanding/rendering as the compared capacity; it does not compare one person with himself.'
])
add('P03', 'Four analyses correctly identify the inclusive on-phrases, main plural cares/sind, and the two different relative antecedents. The care clause’s subject and the kingdom clause’s object are kept distinct; anterior underfangen hæfde remains a supplied reading construction.', [
    'Ǣgðer ge … ge coordinates on mōde and on līchaman, including both spheres of affliction; neither phrase is omitted.',
    'Ðā bisga is the plural nominative subject of sind; ūs is dative and swīðe earfoðrīme the predicate. The main subject is not the intervening kingdoms.',
    'The first relative refers to the cares, with ðe subject of plural becōmon and on ðā rīcu the goal. His days are retained.',
    'The second relative refers to the kingdoms, with ðe object of underfangen and hē/Alfred subject of hæfde. The witness correctly distinguishes it from the preceding relative.'
])
add('P04', 'Both outputs preserve the comparison’s elided predicate and the negative requested content. The key correctly treats ne wīte as part of what the reader is asked to do, rather than as an already factual report.', [
    'Rihtlicor compares correctness of understanding the book; understand it is recovered after ðonne hē meahte. The witness does not turn it into a moral comparison.',
    'Ne negates wīte within the requested subjunctive content coordinated with praying. The witness retains the request and does not assert that blame has already ceased.'
])
add('P05', 'The independent152-word-source translation covers Alfred’s identification, Latin-to-English transfer, both methods, clearness/intelligibility, mental/bodily cares, hard-to-count kingdoms, study and prior prose/discourse translation, subsequent verse, the request for prayer/no blame, the two different hē referents, and the final speaking/doing limits of understanding and leisure. Prose is a justified contextual rendering of spelle against lēoð, with discourse expressly acknowledged. The actual Cook162 image and key confirm completeness; source Lædene is not silently rewritten merely because a lexical lemma has quantity marking.')

add('R01', 'All21 outputs separately identify the opening subjunctive request and six imperative commands, then retain the essential meaning of each. The Cook163 image confirms gewissie versus gewissa, gestaðela, gestranga, āfierr, gescield and tǣc; no seventh imperative is invented. Supplied exact reading forms remain recognition/comprehension support.', [
    'Gewissie is the exact opening requested form; it is not replaced by the following imperative gewissa.',
    'Gewissie is correctly parsed as present subjunctive second singular in the requested ðæt clause.',
    'The opening petition requests guidance better than the speaker’s conduct towards God has deserved.',
    'Gewissa is the exact following guide command.',
    'Gewissa is correctly parsed as second-singular imperative.',
    'The guidance is according to God’s will, for the soul’s benefit and beyond the speaker’s own knowledge; all three components are retained.',
    'Gestaðela is the exact establish command; its medial vowel is preserved.',
    'Gestaðela is correctly parsed as second-singular imperative.',
    'The mind is to be made steadfast according to God’s will and for the soul’s benefit; the witness retains the repeated benefit phrase.',
    'Gestranga is the exact strengthen command.',
    'Gestranga is correctly parsed as second-singular imperative.',
    'The strengthening is against the devil’s temptations, with the correct adversarial relation.',
    'Āfierr is the exact remove command, with its quantity and consonant spelling retained.',
    'Āfierr is correctly parsed as second-singular imperative.',
    'The petition removes foul lust and all/every unrighteousness from the speaker; neither object is omitted.',
    'Gescield is the exact protection command.',
    'Gescield is correctly parsed as second-singular imperative.',
    'The speaker asks protection from both visible and invisible adversaries; the witness keeps both descriptions.',
    'Tǣc is the exact teach command.',
    'Tǣc is correctly parsed as second-singular imperative.',
    'Teach me to do your will preserves the person taught and the governed act, including will as the object of doing.'
])
add('R02', 'Both answers preserve all grounds of entreaty and correctly distinguish the preposition’s dative noun from its dependent genitive. Cook163 specifically reads Michael’s gehīersumnesse, obedience; replacing that with an inherited devotional gloss such as intercession would be wrong here.', [
    'The witness includes mercy, cross-sign, Mary’s virginity, Michael’s obedience, and the saints’ love and merits. These are the grounds of entreaty introduced by for, not extra requested actions.',
    'For governs dative tācne; ðǣre hālgan rōde is a dependent genitive singular. The witness does not directly govern rōde with the preposition merely because it follows nearby.'
])
add('R03', 'Three answers correctly distinguish deserved treatment from the speaker’s own knowledge as the two comparison standards. The supplied contextual subjunctive cunne is recognized accurately, without asserting a universal rule that all comparisons take that mood.', [
    'Ic āworhte tō ðē states the speaker’s conduct/desert towards God as the first comparison standard; the request exceeds that desert.',
    'Ic self cunne is the speaker’s own possible knowledge as the second comparison standard; the requested guidance goes beyond it.',
    'Cunne is first-singular present subjunctive, not past indicative. The witness correctly labels know how to direct myself as an interpretive recovery rather than an extra written verb.'
])
add('R04', 'All six outputs distinguish the purpose clause from the final independent wish, including actor/addressee, mood and function. Cook163 prints singular sīe with the joined praise/glory conception; Cook102–103 supports agreement and optative interpretation. The witness does not treat God as subject of an imperative to love.', [
    'Ic is the praying speaker who would love, and ðē is God as loved addressee; the two roles are not reversed.',
    'Mæge is present subjunctive first singular with plain infinitive lufian.',
    'The clause gives the purpose of the teaching/guidance: that the speaker may love God fervently above all things.',
    'Lof and wuldor are the praise/glory wished to God; ðē is dative recipient. God is not the grammatical subject of a second-person command.',
    'Sīe is the actual singular present subjunctive used optatively, matching the source rather than being silently regularized to plural.',
    'The closing clause is an independent doxological wish for praise and glory now and forever, not another subordinate purpose clause.'
])
add('R05', 'The independent complete translation covers every component of the160-word Cook163 prayer: invocation and maker/ruler titles; every ground of entreaty including Michael’s obedience; the opening requested guidance and both comparison standards; all six commands; the soul’s benefit twice; temptations, lust/unrighteousness, visible/invisible adversaries; purpose and pure thought/body; all six closing divine descriptions; independent praise/glory wish, three repeated ever terms and eternity without end; Amen. The actual key and personally inspected image confirm completeness and the long personal ðē/relative ðe distinction. No claim of independent productive recall is made for the reading’s supplied forms.')

add('EX-IX-28-01', 'The blind answer preserves all eight relinquished alternatives, their intended numbers, for mīnum naman, and both promised results. Its supplied dative-resumption/passive clause retains final bið as Cook directs; alternate ordering of the final possession clause is grammatical. The long prompt and continuation were checked across printed15–16. The source’s sisters control and the learned sweostor plural are retained; supplied hundtēontigum/repayment syntax is not an unaided-recall test.')
add('EX-IX-28-02', 'The witness’s gehwǣm is a defensible taught distributive alternative to the key’s ǣlcum, explicitly allowed in the contract. Hē sealde, the penny and wið his dæges weorce preserve payment to each for a day’s work, with genitive dæges dependent on dative weorce. Difference of quantifier spelling is not an error.')
add('EX-IX-28-03', 'Hē sęnde hīe on his wīngeard preserves past sending, the plural object and movement into the vineyard. On has its directional accusative; no unsupported passive or wrong person is introduced.')
add('EX-IX-28-04', 'The frozen standende version is grammatical as a perception-plus-participle description and preserves essential meaning, but misses Cook’s §169 accusative-plus-infinitive target. Cook96 and the contrast with28.7’s explicit pres.part. control confirm the intended standan. AM03 now makes this target locally explicit without altering the source prompt. The accepted model is Hē geseah ōðre on strǣte īdle standan. The public-place sense is correctly labelled taught, and article omission is retained. This corrects the review record, not the frozen witness.')
add('EX-IX-28-05', 'The witness retains then said, the plural command, also, movement into my vineyard, and the promised giving of what is right. Supplied ðæt riht is is used as instructed rather than replaced by interrogative hwæt. Present sęlle validly carries the prospective promise; direct speech remains direct.')
add('EX-IX-28-06', 'The witness’s V2 order and final gelīce are acceptable alternatives to the model. Both the sixth and ninth hours, renewed departure and doing similarly remain. AM02 now correctly identifies sixth as familiar and ninth as supplied. Ymbe takes the accusative hour phrase and gelīce is adverbial here, unlike the adjective in29.1.')
add('EX-IX-28-07', 'The witness’s fand and the key’s funde are both valid third-singular preterites, as actual Unit4 explicitly teaches and the personally viewed Wright258 page confirms. My initial objection to funde is withdrawn. The eleventh-hour phrase, going out, others and explicitly requested present participle standende are all retained; constituent order differences do not alter them.')
add('EX-IX-28-08', 'The witness preserves then said, why, plural address, standing here, all-day duration and plural predicate idle. Ealne dæg is the duration accusative and īdle agrees with the people. It follows the complete prompt rather than merely reproducing standan.')
add('EX-IX-28-09', 'The witness retains plural past speaking and because no one hired us. Nān mann with finite ne gives negative concord, ūs is the hired accusative people and the supplied hȳrode has the required past sense. Neither the cause nor the negative is lost.')
add('EX-IX-28-10', 'The complete evening/supervisor/pay sequence is preserved, including the supplied anterior evening construction, vineyard owner, dative gerēfan after tō, singular commands cleopa/forgield and plural workers/payees. Hier(a) mēde retains their wage rather than changing the owner or recipient. The prompt crosses printed15–16 and was checked as one item.')
add('EX-IX-28-11', 'The witness preserves both temporal clauses and the eleventh hour, leaves the relative verb cōmon last as directed, and distributes each penny while plural hīe governs onfēngon. Repeated ðā/cōmon is source-controlled, not an accidental duplicate to delete. The supplied receiving/distribution structure remains available.')
add('EX-IX-28-12', 'The witness preserves the first arrivals’ expectation of receiving more. Māre is the received amount; onfōn stays infinitival and supplied sceolden gives the anticipated outcome inside the past report. It does not recast should as a moral duty or omit the first-arrival relative.')
add('EX-IX-29-01', 'The witness makes hīe the accusative people rendered equal, gelīce their plural predicate, and ūs the dative standard. The relative refers to us and retains burdens and this day’s heat; hǣte is correctly oblique. Its alternate relative verb placement is valid and does not change the supplied result-complement construction.')
add('EX-IX-29-02', 'The witness retains both singular commands, that which is yours, this recipient and the as-much-as comparison with you. Present sęlle is a taught prospective promise and is a defensible alternative to the key’s wille plus infinitive. Ðissum and ðē remain dative recipients; the shared giving is understood in the standard.')
add('EX-IX-29-03', 'Ne mōt ic dōn ðæt ic wille preserves the negative permission question and the object clause. The witness explicitly distinguishes permission mōtan from ability magan; the same surface English may does not license a loss of the intended permission sense.')
add('EX-IX-29-04', 'Ne cōme ðū tō mē tō wyrceanne wið ānum pęninge preserves the negative past question, singular addressee, coming to the speaker and work for one penny. The second-singular strong preterite cōme is not confused with an imperative; supplied inflected infinitive and dative remuneration are retained.')
add('EX-IX-29-05', 'The witness preserves man and prophet, mighty in word and deed, and before God and all people. The two predicates and both spheres of might are present; the prepositional datives and quantified folce match the taught/supplied frames.')
add('EX-IX-29-06', 'The witness’s taught feminine woruld is a valid alternative to the key’s masculine middangeard. It preserves the judgment/content clause, light’s arrival, men’s preference for darkness and the reason that their deeds were evil. Swīðor compares the two objects of loving; yfel is the selected neuter plural predicate with weorc.')
add('EX-IX-29-07', 'The witness preserves sending the Son and contrasts the rejected condemning purpose with the saving purpose. Its feminine woruld consistently controls ðā/sēo; uninflected predicative hǣled is legitimate, as Cook100 explicitly permits. Dēmde and wǣre are the supplied past subjunctive purposes, and ðurh hine retains mediation. The negative does not erase the occurrence of sending.')
add('EX-IX-29-08', 'The key is correct with Ēowru mēd bið miclu. My frozen Ēower with feminine nominative singular mēd misses the selected agreement taught explicitly in Unit3; correct it here to Ēowru, with supported unsyncopated ēoweru also a documented alternative. The rest preserves large reward, children of the Highest, and goodness over unthankful/evil people. Miclu agrees with mēd; both substantival objects after ofer are accusative plural. The witness is not silently repaired.')
add('EX-IX-29-09', 'The blind plural Giefað, and ēow bið giefen matches the key and source omission of it. AM02 supplies this exact recipient-passive frame visibly, binds its feature and says its independent recall is not assessed. A consistently singular Gief, and ðē bið giefen is also defensible because the English leaves number open; that option is now explicitly supported. Adding hit would miss the omission control.')
add('EX-IX-29-10', 'Se leornungcniht nis ofer his lārēow retains disciple, teacher, possession and negative above relation. The contracted copula is correct, and the comparison/prepositional sense is locally taught. No plural or participial substitution is needed.')
add('EX-IX-29-11', 'The witness and key retain singular thy, two addressed requests, mercy and salvation. Ætīew governs the accusative mercy with dative ūs; unne governs dative ūs plus genitive ðīnre hǣlu. AM02 correctly labels addressed subjunctive unne as prior Unit10 teaching. The unchanged noun hǣlu remains genitive by construction; its surface does not license an accusative analysis.')
add('EX-IX-30-01', 'The blind mǣres cyninges correctly preserves Cook’s two explicit article omissions. AM03 replaces the old key’s article-led ðæs mǣran, changes selected model/form/system bindings to strong genitive mǣres and removes stale article requirements. The omission-controlled answer retains all three oath standards, each causal reason, correct heofon/eorðe pronominal gender and supplied Jerusalem. Optional overt ðū is not essential to a singular command. Cook17 and39–40 were personally checked; valid definite weak language is distinguished from compliance with this prompt.')
add('EX-IX-30-02', 'The witness preserves the prohibition against swearing by one’s head and the inability to make one hair white or black. Both color alternatives and the one-hair object remain; hēafod/ān hǣr are accusative and meaht takes plain wyrcean. Finite ne is retained in both the prohibition and its reason.')
add('EX-IX-30-03', 'The witness’s previously taught ðus is a valid alternative to the key’s swā for thus. Sīe is the prior singular subjunctive wish, word is singular despite plural possessors ēower, and both quoted hit is/hit nis alternatives remain. AM02 removes the misleading claim that this wish must be newly supplied.')
add('EX-IX-30-04', 'The witness preserves plural hearing, passive reporting and both eye/eye and tooth/tooth exchange pairs. It correctly distinguishes nominative quotation heads from dative objects after for, including tēð as dative singular rather than plural merely from its spelling.')
add('EX-IX-30-05', 'The witness retains whoever breaks one of the least commandments and teaches men so, the resumed subject, being called least and the heavenly kingdom. Ān is accusative neuter; of governs the dative plural group. The teaching clause ends in lǣrð as explicitly directed. Supplied hāten does not become an unsupported full productive verb system.')
add('EX-IX-30-06', 'The witness preserves both doing and teaching, resumes the person with sē and gives the requested passive naming as great. It does not omit the auxiliary or mistake hāten for active called; the actual source says he shall be called, as checked on printed17.')
add('EX-IX-30-07', 'The witness retains plural hearing, ancient times, passive reporting and the singular prohibition Ne sleah. Omitting an optional overt ðū does not change the addressee or the source’s omission of English shalt. The two clauses remain distinct.')
add('EX-IX-30-08', 'Is hit ðīn eorðe translates the actual printed earth, not an inherited misreading. The question and singular addressee remain, and endingless ðīn is the correct selected feminine nominative singular with long-stem agreement. Surface absence of -u does not mean absence of agreement.')
add('EX-IX-30-09', 'The witness retains possession/receipt at his labor and the supplied free-relative content ðæt hē mæg. It does not invent a verb meaning earn from English or replace the supplied relation with a different object structure.')
add('EX-IX-30-10', 'The key’s Sēo sunne forbærnde his æcer is correct and uses the actual taught field noun. My frozen feld is outside the fourteen-unit plus Unit15 productive vocabulary and lacks a local supplied form; this is a scope miss, not a claim that feld is impossible Old English. The correction is recorded separately as æcer; past burning, sun subject and possessive field object are otherwise retained.')
add('EX-IX-30-11', 'Both repeated road clauses, supplied blōstmian, feminine fægeru brȳd, singular sceal and accusative hiere hām are preserved. The model’s sceoldon is defensible modal ought to and does not entail past time or counterfactuality. The witness’s sculon is defensible under its expressly stated present expectation/obligation reading, though not an interchangeable spelling; its initial reservation overstated the restriction on sceoldon. AM03 now explains the contextual choice. Scylen would require a wish reading. No hidden tense target appears in the printed prompt.')
add('EX-IX-30-12', 'The witness preserves the actual if they can condition and supplied lǣt hīe libban permission construction, with plural ability and without me. A subjunctive libben hīe is possible as an optative alternative but changes the construction; the recorded answer follows the given help. The source’s If was personally confirmed on printed17.')
add('EX-IX-30-13', 'The witness preserves never, leaving/abandoning and the people who trust in him. Nǣfre and finite ne form negative concord; the relative uses the already taught gelīefan on plus accusative confidence/belief-in frame, rather than an invented untaught verb. Its object placement differs harmlessly from the model; the trust sense is contextual, not assumed for every occurrence of a familiar lemma.')
add('EX-X-XI-31-01', 'Ic wāt sōðlice ðæt mīn Ālīesend leofað preserves the speaker’s certain knowledge, the Redeemer’s identity and present living. The nominalized redeemer and its possession are retained; living is not converted to a past event.')
add('EX-X-XI-31-02', 'The witness preserves in my flesh, seeing God, first-person self emphasis and exclusion of another observer. Present gesēo is legitimate prospective English shall see, and nā scopes over the contrasted participant rather than negating seeing. This directly applies the unit’s taught constituent-negation distinction.')
add('EX-X-XI-31-03', 'Hē wæs lǣred Godes willan tō dōnne preserves past passive teaching and the supplied infinitive complement. Godes is dependent genitive; willan is the accusative weak-noun object of doing, not a modal verb. The exact supported complement remains available rather than being silently promoted to broad independent recall.')
add('EX-X-XI-31-04', 'The witness preserves both addressed commands and their contrast: do not lead us into temptation, but deliver us from evil. Ālīes and lǣd address one person, ūs remains the object, directional on and source fram retain the required cases, and supplied yfele is not reanalyzed as an unrelated plural.')
add('EX-X-XI-31-05', 'Sīe ðīn nama gehālgod is a singular passive wish, preserving hallowing of the addressee’s name. AM02 correctly identifies the passive and independent wish as prior Unit7 teaching. The answer is not a report of a past completed act, and no unwritten verb-first control from31.6 is imposed here.')
add('EX-X-XI-31-06', 'Geweorðe ðīn willa on eorðan swā-swā on heofonum obeys the explicit verb-first instruction and expresses the wish with the requested earth/heaven comparison. Willa remains the weak masculine nominative subject; the locative case phrases are correct.')
add('EX-X-XI-31-07', 'The witness preserves no English king, past negation and equality comparison with Alfred. Engla is the partitive people-name genitive, nān and næs express one denial, and swā micel swā retains the as-great-as relation. The supplied proper name is not an independent lexical-recall test.')
add('EX-X-XI-31-08', 'All four predicates survive: fighting the Danes, judging his people, making translations from Latin and being a poet. Bare Dęnum is a defensible ethnonym plural without the model’s optional determiner; wið still has the appropriate dative. The witness’s taught geworhte is a valid make/accomplish alternative to worhte. The plural translations, Latin source and weak poet noun are correct; spelling alternatives are not mistaken for omitted content.')
add('EX-X-XI-31-09', 'The witness preserves the supplied naming form hātte and both parents/names, with the verb understood in the coordinated father clause. Osburg and Æthelwulf match the printed source; hātte is not confused with active hēt. This item does not license unsupplied productive naming forms.')
add('EX-X-XI-31-10', 'Hē lifde twā and fīftig gēara preserves lived and fifty-two years, including the supplied compound numeral construction and its genitive year phrase. The source does not say merely fifty or twelve; the full number was checked on printed18.')
add('EX-X-XI-31-11', 'The witness preserves learning to read after being twelve winters/years old. Bēcrǣdinge uses the taught reading noun; æfter ðǣm ðe introduces the temporal clause and twęlf wintra eald retains the age expression. The two past predicates are not collapsed into a nominal age alone.')
add('EX-X-XI-31-12', 'The witness preserves the mother’s book of English lays, her promise, either of the two sons and first learning it. Bare bōc is valid indefinite usage; inflected relative ðā is a taught alternative to invariant ðe. Supplied attracted hwæðrum is retained and not generalized from the ordinary internally nominative free-choice pattern; leornode has the supplied prospective subjunctive interpretation. Hīe refers to the feminine book, not one of the sons.')
add('EX-X-XI-31-13', 'The frozen hīe after āscode correctly follows actual Unit13’s accusative-person āscian frame. Cook276b points to159b, and the personally viewed Cook93 example explicitly labels ðē accusative; AM03 corrects the old key’s unsupported hiere and all selected dependencies. The rest preserves direct singular address, the book, giving to one of us two, appositional dative ðǣm, and the first understander. Personal genitive dual uncer supplies the partitive group; later hīe is the book as object of ongiett. No universal ban on every historical dative ask construction is claimed.')
add('EX-X-XI-31-14', 'The witness preserves Asser, appositional Alfred’s bishop, past writing and the book about the king’s life. Bare bōc is a valid indefinite alternative to the key’s āne bōc. The nested genitives ðæs cyninges līfes preserve the source’s content-genitive control153; the author or subject of the life is not reversed.')

evidence_observations = {
    'sources/audits/unit15-source/exercise-001.png': 'Cook Exercises printed15/PDF23: inspected the actual28 prompts, the eight alternatives of28.1, sisters52.3,28.4 standing(169), and28.7 standing(pres.part.); these last two controls deliberately differ.',
    'sources/audits/unit15-source/exercise-002.png': 'Cook Exercises printed16/PDF24: inspected the continuation of28, all29 prompts and controls, including original sęllan/hȳrian, singular thy in29.11 and omit it in29.9.',
    'sources/audits/unit15-source/exercise-003.png': 'Cook Exercises printed17/PDF25: inspected every30 prompt and beginning of31; confirmed both article omissions in30.1, earth in30.8, blōstmian in30.11, If they can in30.12 and he shall be called in30.6.',
    'sources/audits/unit15-source/exercise-004.png': 'Cook Exercises printed18/PDF26: inspected continuation of31.3 through31.14, including Æthelwulf, fifty-two, uncer, content-genitive153 and the verb-first Geweorðan control. Following32 is outside this review.',
    'sources/audits/unit15-source/reader-001.png': 'Cook First Book printed159/PDF175: personally read the complete103-word first Duties argument and its eleven notes with repeated anchors. Confirmed prospective188, the two gospel reporting participles, eternal bliss and the intentionally unclosed outer speech.',
    'sources/audits/unit15-source/reader-004.png': 'Cook First Book printed162/PDF178: personally read all152 words and seven notes of the Preface. Confirmed Lædene as printed, the repeated ðæt frame, supplied subject of bitt, and notes distinguishing reader hē from Alfred hē.',
    'sources/audits/unit15-source/reader-005.png': 'Cook First Book printed163/PDF179: personally read all160 words and nine notes of the Prayer. Confirmed gehīersumnesse, gewissie versus six commands, gestaðela, singular Sīe, three ā repetitions, willan as object of wyrceanne and ǣghwilcum agreeing with ęnde.',
    'sources/audits/unit15-source/cook-fb-p276.png': 'Cook First Book printed276, right column: āscian/āxian has quantity ā, weak-II118 and a specific159.b cross-reference, directing the case-government check to93.',
    'sources/audits/unit15-grammar/fb-p61.png': 'Cook First Book printed61: inspected ClassIII strong stems including gieldan/geald/guldon/golden and weorpan/wearp/wurpon/worpen. This generic table alone does not decide the exceptional third-singular findan question.',
    'sources/audits/unit04-grammar/wright-p257-pdf277.png': 'Wright printed257/PDF277: inspected the general ClassIII nasal stem series as background to the following page’s explicit findan exception.',
    'sources/audits/unit04-grammar/wright-p258-pdf278.png': 'Wright printed258/PDF278: the note explicitly says funde, formally second singular, is also used in first and third singular beside fand. This directly withdraws the proposed objection to key28.7.',
    'sources/audits/unit15-grammar/fb-p90.png': 'Cook First Book printed90: inspected the genitive discussion, including partitive154; it supports personal-genitive selection but is not the159.b āscian evidence.',
    'sources/audits/unit14-grammar/fb-p93.png': 'Cook First Book printed93:159.b explicitly prints ðē(acc.) hlāfes āxan, separating accusative person from genitive thing. The following dative discussion does not turn this selected ask frame into dative person.',
    'sources/audits/unit15-grammar/fb-p102.png': 'Cook First Book printed102: inspected agreement189 and impersonal190, including singular agreement for a coordinated conception; this supports retaining source Sīe rather than silently regularizing it.',
    'sources/audits/unit15-grammar/fb-p101.png': 'Cook First Book printed101: passive187 and prospective present188 support the unit’s periphrastic passive and future English translations of contextually prospective presents.',
    'sources/audits/unit15-grammar/fb-p74.png': 'Cook First Book printed74: habban/nabban121 supplies the irregular positive series and negative formation reference; inspected hæbbe/hæfst/hæfð/habbað and the weak preterite pattern.',
    'sources/audits/unit14-grammar/fb-p78.png': 'Cook First Book printed78: inspected sculan133, magan135, mōtan137 and wesan138, preserving distinctions among the finite systems and their indicative/optative forms.',
    'sources/audits/unit14-grammar/fb-p79.png': 'Cook First Book printed79: inspected negative wesan preterites and willan139 including negative e/y and consonant variants. It supports the selected negative series without making variants errors of language.',
    'sources/audits/unit14-grammar/fb-p100.png': 'Cook First Book printed100: the opening note explicitly permits uninflected predicative participles;181 treats substantival adjectives and183 negative concord. This supports feminine woruld with uninflected hǣled in the blind29.7 alternative.',
    'sources/audits/unit15-grammar/fb-p23.png': 'Cook First Book printed23: inspected contraction of ne with habban, h-loss and næfde, and āscian/āxian metathesis32. These are distinct phenomena rather than unsupported spelling regularization.',
    'sources/audits/unit14-grammar/fb-p52.png': 'Cook First Book printed52: inspected personal/neuter hwā/hwæt forms88 and strong nān/indefinite compounds89; personal versus neuter and strong agreement are explicit.',
    'sources/audits/unit06-grammar/cook-p53-pdf69.png': 'Cook First Book printed53/PDF69:89c makes hwā compounds follow the interrogative,89d supplies free choice, and89e identifies impersonal man as nominative singular. No full impersonal plural/oblique system is supplied.',
    'sources/audits/unit08-grammar/wright_oe_1914-p240.png': 'Wright printed240: inspected gehwā each/everyone and the swā hwā/hwæt/hwæðer patterns; the personal indefinite is not presented as a separate plural paradigm.',
    'sources/audits/unit15-grammar/fb-p39.png': 'Cook First Book printed39: inspected strong adjective obliques, long-stem loss of-u and the disyllabic stem discussion. This supports the selected adjective outputs and strong genitive in repaired30.1.',
    'sources/audits/unit15-source/cook-fb-p31.png': 'Cook First Book printed31: inspected plural people-name Engle, the sunu table and the root masculine tōð classification with mutated dative/nominative-accusative plural behavior.',
    'sources/audits/unit15-source/cook-fb-p36.png': 'Cook First Book printed36: bōc is among the root feminines; the gōs paradigm gives the inflectional pattern and notes the genitive alternative. Inspected kinship material on the same page.',
    'sources/audits/unit15-source/cook-fb-p37.png': 'Cook First Book printed37: sweostor is explicitly unchanged except genitive/dative plural; the following weak noun table supplies -a/-an/-ena/-um, corroborating gerēfa and lēoðwyrhta.',
    'sources/audits/unit15-grammar/fb-p40.png': 'Cook First Book printed40: inspected the long-stem and e-adjective paradigm, including grēne-type strong genitive-e stem behavior. This supports mǣres after the omitted article, distinct from weak mǣran.',
    'sources/audits/unit15-source/cook-fb-p32.png': 'Cook First Book printed32: inspected the full fōt root pattern, the documented tōðas alternative and the neuter endings. The recorded alternative does not replace a task’s expressly selected tēð cell.',
    'sources/audits/unit15-source/wright-p184.png': 'Wright printed184: inspected complete strengu-type declension and variants, with hǣtu/hǣlu listed. The note says few such nouns occur in plural; it does not prove that no historical plural exists.',
    'sources/audits/unit15-source/bt-main-p500.jpg': 'Bosworth–Toller printed500, right column: hǽlu/hǽlo is explicitly feminine indeclinable with health/safety/salvation senses, supporting the selected unchanged singular system.',
    'sources/audits/unit15-grammar/fb-p38.png': 'Cook First Book printed38: inspected strong/weak adjective selection55 and the beginning of the disyllabic adjective rules. Article-controlled weak selection is distinct from the bare strong phrase required by30.1.',
    'sources/audits/unit15-grammar/fb-p48.png': 'Cook First Book printed48: inspected two genitive twēg(r)a, numeral genitive patterns with-tig, ordinal weak80 and personal pronoun beginnings; these support two-member selection and numeral phrases.',
    'sources/audits/unit09-grammar/cook_fb_1895_2-p96.png': 'Cook First Book printed96:169 expressly gives subject accusative with an infinitive and a geseah … gān example. This resolves the intended28.4 target, unlike28.7’s separately printed participle requirement.',
    'sources/audits/unit15-grammar/fb-p103.png': 'Cook First Book printed103: inspected independent optatives192–193 and content194, supporting the distinction between wished clauses and requested subordinate content without making all clauses imperatives.',
    'sources/audits/unit15-source/cook-fb-p33.png': 'Cook First Book printed33:47.6 explicitly gives hēafod with nominative plural hēafdu rather than usual hēafodu, illustrating syncope; the surrounding paragraph warns that neuter plural syncope is not uniform.',
    'sources/audits/unit15-source/cook-fb-p288.png': 'Cook First Book printed288: inspected for-gieldan/for-gildan as strongIII104 with recompense/pay/give senses, and the separate for-lǣtan entry. These lexical classes/senses support the source exercise reading rather than supplying a full extra production system.',
    'sources/audits/unit15-source/cook-fb-p297.png': 'Cook First Book printed297: inspected hǣlu, hǣtu and hēafod entries with their grammar cross-references, and hām as home. The entries distinguish noun hām from a previously encountered directional adverb.',
    'sources/audits/unit15-source/cook-fb-p289.png': 'Cook First Book printed289: inspected the fōt cross-reference and fultum help/support entry. This page does not contain a fōtsceamul paradigm; none is falsely attributed to it.'
}

findings = [
    {'finding_id':'U15-BLIND-F01','status':'resolved_verified','task_ids':['EX-IX-28-04'],
     'finding':'The intended §169 infinitive target was only an opaque parenthetical reference; the blind participle preserved meaning but missed that target.',
     'resolution':'AM03 now gives explicit local guidance to use accusative ōðre with plain standan, preserves the original prompt, and correctly labels public-place as a taught sense. The frozen attempt remains untouched.',
     'evidence':['sources/audits/unit15-source/exercise-001.png','sources/audits/unit09-grammar/cook_fb_1895_2-p96.png']},
    {'finding_id':'U15-BLIND-F02','status':'resolved_verified','task_ids':['EX-IX-30-01'],
     'finding':'Initial key ðæs mǣran cyninges violated the source direction to omit the article before great king.',
     'resolution':'AM03 replaces it with mǣres cyninges, updates the selected model and strong-form dependencies, and removes obsolete article requirements. Both original omissions and all oath clauses remain. The old definite phrase is valid language but fails this controlled prompt.',
     'evidence':['sources/audits/unit15-source/exercise-003.png','sources/audits/unit15-grammar/fb-p39.png','sources/audits/unit15-grammar/fb-p40.png']},
    {'finding_id':'U15-BLIND-F03','status':'resolved_verified','task_ids':['EX-X-XI-31-13'],
     'finding':'Initial key hiere after āscode did not follow the actual prior accusative-person frame, and copied canonical targets still said dative.',
     'resolution':'AM03 now has hīe, binds he-f-acc-sg and u13-ascian-person-thing, and reconciles the selected model/canonical requirement copies. Actual Unit13 and Cook276b→159b on93 independently support this selected accusative. No general prohibition across every historical ask construction is asserted.',
     'evidence':['chapters/ch13/student.md','sources/audits/unit15-source/cook-fb-p276.png','sources/audits/unit14-grammar/fb-p93.png']},
    {'finding_id':'U15-BLIND-F04','status':'withdrawn','task_ids':['EX-IX-28-07'],
     'finding':'I initially suspected that key funde could only be second singular and should be replaced by the blind fand.',
     'resolution':'Actual Unit4 explicitly selects third-singular funde and permits fand; personally inspecting Wright258 confirmed funde in first/third singular beside fand. The initial suspicion was wrong. Both alternatives are grammatical here, and the key requires no correction.',
     'evidence':['chapters/ch04/student.md','sources/audits/unit04-grammar/wright-p258-pdf278.png']},
    {'finding_id':'U15-BLIND-F05','status':'resolved_verified','task_ids':[t for t in tasks if t.startswith('NEW-U15-')],
     'finding':'A blanket assessment-boundary sentence described every original task as supplied non-recall work, contradicting F/C productive targets.',
     'resolution':'All55 original boundaries now distinguish productive morphology, productive composition, recognition analysis and supported reading. Supplied help remains available without erasing the explicitly taught productive targets.'},
    {'finding_id':'U15-BLIND-F06','status':'adjudicated','task_ids':['EX-IX-30-11'],
     'finding':'The isolated English should did not settle a unique modal reading; the blind reservation over-narrowed sceoldon to past/counterfactual contexts.',
     'resolution':'The key’s sceoldon is defensible modal ought to without necessary past-time reference. The blind sculon remains defensible under its stated present expectation/obligation reading; the two are not merely spelling variants. Scylen would need an explicit wish reading. AM03 records that distinction while retaining the repeated clauses and original prompt.',
     'evidence':['sources/audits/unit15-source/exercise-003.png','sources/audits/unit14-grammar/fb-p78.png','chapters/ch06/student.md','chapters/ch07/student.md','chapters/ch09/student.md']},
    {'finding_id':'U15-BLIND-F07','status':'resolved_verified','task_ids':['EX-IX-29-09'],
     'origin':'Separate paradigm review finding, independently rechecked here; not claimed as this reviewer’s original discovery.',
     'finding':'The recipient-passive construction needed visible supplied help rather than merely a private dependency label.',
     'resolution':'AM02 supplies ēow bið giefen, its dative recipient/no-hit explanation, the singular counterpart and the explicit non-recall boundary, with actual teaching marker and bound feature. The blind answer matches the supported model.',
     'evidence':['chapters/ch15/student.md','sources/audits/unit15-source/exercise-002.png']},
    {'finding_id':'U15-BLIND-F08','status':'resolved_verified','task_ids':['EX-IX-28-06','EX-IX-29-11','EX-IX-30-03','EX-X-XI-31-05'],
     'origin':'Separate paradigm review findings, independently rechecked here.',
     'finding':'Four key comments labelled already taught material as supplied: sixth ordinal, addressed unne, independent sīe wish and passive wish.',
     'resolution':'AM02 correctly distinguishes familiar siextan from supplied nigoðan, cites Unit10 for unne and Unit7 for the wishes/passive wish. No extra independent-recall claim is introduced.'},
    {'finding_id':'U15-BLIND-F09','status':'adjudicated','task_ids':['EX-IX-29-08'],
     'finding':'My frozen Ēower mēd misses the selected feminine nominative singular possessive agreement.',
     'resolution':'The key’s Ēowru mēd is correct, with supported unsyncopated ēoweru an alternative in actual Unit3. The review records the correction; the witness remains unchanged. This is a selected agreement error, not proof that every historical uninflected-looking ēower usage is impossible.',
     'evidence':['chapters/ch03/student.md']},
    {'finding_id':'U15-BLIND-F10','status':'adjudicated','task_ids':['EX-IX-30-10'],
     'finding':'My frozen feld is not part of the actual taught/supplied productive inventory for this task.',
     'resolution':'Use the key’s taught æcer: Sēo sunne forbærnde his æcer. The scope miss is recorded without claiming feld is impossible Old English or rewriting the witness.',
     'evidence':['lexicon/entries.json','chapters/ch15/student.md']},
    {'finding_id':'U15-BLIND-F11','status':'resolved_verified','task_ids':['EX-IX-30-01'],
     'finding':'The replacement canonical model retained an inherited contextual label calling ðurh a personal-mediator frame at the oath-standard tokens.',
     'resolution':'The coordinator changed all three contextual functions to accusative oath standard, refreshed the correction-record hash and removed stale current-task article/weak-form usage links. The learner/key text did not need further change.'}
]

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def identity(path):
    raw = (ROOT / path).read_bytes()
    return {'path':path,'raw_sha256':sha(raw),'normalized_lf_sha256':sha(raw.replace(b'\r\n',b'\n'))}

assert len(rationales) == 105 and set(rationales) == set(tasks)
student_ids = re.findall(r'<!-- item: (.*?) -->', student)
witness_ids = re.findall(r'<!-- item: (.*?) -->', witness)
assert student_ids == witness_ids and len(student_ids) == len(set(student_ids)) == 105
assert set(student_ids) == set(tasks)
expected = [o['output_position_id'] for t in tasks.values() for o in t['output_positions']]
assert len(expected) == len(set(expected)) == 322 and set(expected) == set(answers)
assert re.findall(r'<!-- output: (.*?) -->', student) == list(answers)
key_output_ids = re.findall(r'<!-- output: (.*?) -->', key)
assert len(key_output_ids) == len(set(key_output_ids)) == 322 and set(key_output_ids) == set(expected)
key_ids = re.findall(r'<!-- key: (.*?) -->', key)
assert len(key_ids) == len(set(key_ids)) == 105 and set(key_ids) == {t['key_id'] for t in tasks.values()}

form_system_notes = {
    'F01':'This is the selected negative indicative copula; the separately written ne is retained where the course selects it.',
    'F02':'This is selected negative possession, not a willan form; the irregular present and weak preterite are kept distinct.',
    'F03':'This is the selected negative-volition indicative series; the e-series and preterite nol- are retained.',
    'F04':'This is the requested selected strong nān agreement cell; repeated spellings do not erase its gender/case/number.',
    'F05':'This is the assigned singular personal/neuter gehwā cell; no plural system is inferred.',
    'F06':'The requested root-noun cell retains the selected stem vowel and ending, including the bōc/tōð difference in genitive singular.',
    'F07':'The selected sweostor paradigm changes only in genitive/dative plural; this cell retains its own grammatical identity.',
    'F08':'Only the assigned singular abstract-noun system is assessed; hǣtu has selected oblique-e while hǣlu is unchanged.',
    'F09':'The whole weak masculine stem receives the selected ending; the compound’s first member is not separately inflected.'
}
expanded = {'sg':'singular','pl':'plural','nom':'nominative','gen':'genitive','dat':'dative','acc':'accusative','m':'masculine','f':'feminine','n':'neuter','mf':'personal common gender'}
form_count = 0
for tid, t in tasks.items():
    start = key.index('<!-- key: ' + t['key_id'] + ' -->')
    end = key.find('<!-- key:', start + 1)
    key_section = key[start:end if end >= 0 else len(key)]
    for o in t['output_positions']:
        if o['kind'] != 'form':
            continue
        form_count += 1
        oid = o['output_position_id']
        surface = o['display_route']['surface']
        assert answers[oid] == surface, (oid, answers[oid], surface)
        assert surface in key_section, (oid, 'form absent from actual key section')
        selector = ', '.join(k + '=' + str(expanded.get(v, v)) for k,v in o['analysis_selector'].items())
        conclusions[oid] = f"{surface} correctly answers {o['lemma_id']} ({selector}), matching the actual selected learner/key cell. " + form_system_notes[tid.rsplit('-',1)[-1]]
assert form_count == 116
assert len(conclusions) == 322 and set(conclusions) == set(expected)

dispositions = {
    'EX-IX-28-04':'grammatically_valid_but_misses_source_target',
    'EX-IX-29-08':'corrected_in_review_only',
    'EX-IX-30-10':'scope_correction_in_review_only',
    'EX-IX-30-11':'contextually_adjudicated_alternative',
}
for tid in [
    'NEW-U15-C03','NEW-U15-C13','NEW-U15-C15','NEW-U15-C19',
    'EX-IX-28-01','EX-IX-28-02','EX-IX-28-06','EX-IX-28-07',
    'EX-IX-29-01','EX-IX-29-02','EX-IX-29-06','EX-IX-29-07',
    'EX-IX-30-01','EX-IX-30-03','EX-IX-30-07','EX-IX-30-13',
    'EX-X-XI-31-08','EX-X-XI-31-12','EX-X-XI-31-14']:
    dispositions[tid] = 'valid_alternative_or_order'
corrections = {
    'EX-IX-28-04':'Hē geseah ōðre on strǣte īdle standan.',
    'EX-IX-29-08':'Ēowru mēd bið miclu, and gē bēoð ðæs Hēahstan bearn, for-ðon-ðe hē is gōd ofer ungeðancfulle and yfele.',
    'EX-IX-30-10':'Sēo sunne forbærnde his æcer.'
}
output_reviews = []
for tid in student_ids:
    for o in tasks[tid]['output_positions']:
        oid = o['output_position_id']
        row = {
            'output_position_id':oid,'task_id':tid,'status':'accepted',
            'output_kind':o['kind'],'blind_answer':answers[oid],
            'blind_answer_disposition':dispositions.get(tid,'concordant'),
            'conclusion':conclusions[oid],
            'scope':tasks[tid].get('assessment_boundary','Supported Cook composition: assess the taught forms, meanings and explicit source controls; retain visible supplied material without assessing its unaided recall.')
        }
        if 'label' in o:
            row['requested_response'] = o['label']
        if o['kind'] == 'form':
            row['analysis_selector'] = o['analysis_selector']
            row['selected_surface'] = o['display_route']['surface']
            row['form_ids'] = o['form_ids']
        if tid in corrections:
            row['review_correction_not_applied_to_witness'] = corrections[tid]
        output_reviews.append(row)

mutable = {'status','review_status','completion','amendments','textual_review','presentation_review','contract_checkpoint','complete_drafts_checkpoint','independent_solutions_checkpoint','accepted_text_checkpoint'}
semantic_keys = sorted(set(contract) - mutable)
semantic_payload = json.dumps({k:contract[k] for k in semantic_keys},ensure_ascii=False,sort_keys=True,separators=(',',':'))
images = []
for path, observation in evidence_observations.items():
    images.append({'path':path,'raw_sha256':sha((ROOT/path).read_bytes()),'actually_viewed':True,'concrete_observations':observation})
artifacts = [identity('chapters/ch15/' + n) for n in ['student.md','answer-key.md','independent-solutions.md']]
counts = {
    'material_open_findings':0,
    'actual_tasks':105,'task_reviews':105,'cook_tasks':50,'original_tasks':55,
    'actual_output_positions':322,'output_position_reviews':322,'morphology_output_positions':116,
    'morphology_tasks':9,'morphology_explanation_outputs':18,'analysis_tasks':12,'analysis_outputs':55,
    'original_composition_tasks':19,'reading_tasks':15,'reading_output_positions':64,
    'reading_analysis_outputs':61,'full_reading_translations':3,'reading_spans':3,
    'source_words':415,'source_words_by_span':[103,152,160],'source_notes':27,'source_note_anchors':33,
    'primary_evidence_images_actually_viewed':len(images),
    'canonical_teaching_records':len(contract['teaching_records']),
    'canonical_grammar_inventory_records':len(contract['grammar_inventory']),
    'findings':len(findings),'frozen_witness_outputs_changed':0
}
ledger = {
    'schema_version':1,'chapter_id':'ch15','reviewer':'unit15_blind','status':'accepted_pre_export',
    'review_date':'2026-10-27',
    'independence':{
        'blind_solutions_checkpoint':'ecbdc44','complete_drafts_checkpoint':'3822d4b','contract_checkpoint':'ff7f7c8',
        'no_current_author_role':True,'all_tasks_solved_before_key_access':True,
        'all_requested_outputs_attempted_before_key_access':True,
        'coordinator_verified_and_committed_witness_before_explicit_unlock':True,
        'explicit_comparison_unlock_received':True,'no_contact_with_paradigm_reviewer':True,
        'witness_never_edited_after_freeze':True,
        'blind_witness_raw_sha256':'2abad21bf90cf8994afbb7e48ec0807b74ab3d1e4cddf80cb30513845ca592fe',
        'blind_learner_raw_sha256':'6caabca8c79ff4ce94beb1ce5c059b0f6cda65427b434bb11a042971b2e0df33',
        'protocol':'sources/audits/unit15-coordinator/review-independence.json',
        'phase_boundary':'The actual learner tasks were all attempted using the permitted learner masters/registers before key, contract, current audits, model witnesses or token-map access. Parent explicitly unlocked comparison only after ecbdc44. Subsequent corrections are separate and do not rewrite that evidence.'
    },
    'acceptance_scope':'Final repaired learner/key text and substantive canonical coverage content, before PDF exports. Accepted status refers to the task/key/contract after review; blind-answer dispositions separately preserve misses and alternatives. This record is not a claim that every initial answer was correct, nor a substitute for final every-page export inspection or cumulative-register integration.',
    'method':[
        'Compared each actual prompt and every requested output with its frozen independent answer, actual key and canonical target/scope, distinguishing essential meaning from selected controls.',
        'Personally read primary exercise and reading page images, then targeted grammar/lexical images for source-sensitive claims; file hashes identify inspected evidence and are not the inspection itself.',
        'Rechecked actual earlier learner teaching for funde/fand, possessive ēowru, āscian government, modal systems and composition alternatives rather than accepting copied current metadata as proof.',
        'The116 requested morphology forms were checked individually against their selected cells and actual key sections. The separately assigned full691-cell paradigm audit is not claimed as this reviewer’s work.',
        'Automated set/order/count/hash checks supplement the manual linguistic review. The assembly script does not infer acceptance from string equality and does not regenerate the frozen witness.'
    ],
    'counts':counts,
    'findings':findings,
    'amendment_rechecks':[
        {'amendment_id':'U15-AM01','status':'verified','conclusion':'The readable row labels preserve the shown forms and output tasks. Prayer ǣghwilcum belongs with ęnde, confirmed directly on Cook163; the contextual correction does not alter the source or forms.'},
        {'amendment_id':'U15-AM02','status':'verified','conclusion':'The exact29.9 supplied frame is visible with an actual marker and bound feature; four key labels correctly identify prior teaching. Final counts are596 teaching records,130 grammar records and36 Cook-help groups.'},
        {'amendment_id':'U15-AM03','status':'verified','conclusion':'Strong mǣres and accusative hīe repair the source-controlled selected models; actual task requirements and canonical replacements agree.28.4 target/help and sense label,30.11 modal note,55 mode-specific boundaries and the three oath-standard contexts are reconciled. Weak mǣre remains a taught transferred system without a falsely claimed direct output.'}
    ],
    'task_reviews':[{'task_id':tid,'status':'accepted','output_position_count':len(tasks[tid]['output_positions']),'rationale':rationales[tid]} for tid in student_ids],
    'output_position_reviews':output_reviews,
    'accepted_artifact_identities':artifacts,
    'accepted_contract_semantic_identity':{'keys':semantic_keys,'sha256':sha(semantic_payload.encode('utf-8')),'serialization':'UTF-8 JSON; ensure_ascii=False; sort_keys=True; compact separators comma/colon; exactly the listed substantive top-level keys.'},
    'accepted_contract_artifact_at_review':identity('chapters/ch15/coverage.json'),
    'accepted_selected_model_correction_identity':identity('chapters/ch15/author-only-model-corrections.json'),
    'primary_evidence_image_inspections':images,
    'remaining_gates':['Produce complete learner and key exports, reconcile export parity and inspect every exported page/special character.','Integrate accepted scope into cumulative registers, update project status/handoff, export Beads and create the coordinator’s recoverable local checkpoint.']
}

report = '''# Unit 15 — independent textual review

Accepted before export, with no material open findings. The final repaired learner master, answer key and substantive coverage contract are identified in [review-ledger.json](review-ledger.json). The review covers all **105 actual tasks and 322 requested output positions**, including **116 morphology forms**, all50 Cook items, all19 new compositions and all15 reading tasks. All three complete independent translations cover the actual103-,152- and160-word selections (415 words total).

The original blind answers remain frozen in [independent-solutions.md](independent-solutions.md), committed by the coordinator at `ecbdc44` before explicit comparison access. Their raw SHA256 remains `2abad21bf90cf8994afbb7e48ec0807b74ab3d1e4cddf80cb30513845ca592fe`, including the final blank line. I did not author current lesson/key material, consult excluded current models before the solve, or communicate with the paradigm reviewer. The coordinator’s explicit unlock, rather than elapsed time or file availability, began comparison. The ledger retains every initial answer alongside an individual conclusion; an accepted final task does not mean that every blind answer was correct.

## Corrections verified in the final materials

- **30.1:** Cook’s printed17 explicitly omits both articles in “city of great king.” The initial `ðæs mǣran cyninges` missed that control. The final key has **mǣres cyninges**, matching the blind answer’s strong genitive. AM03 updates the selected model, form/system dependencies and stale article links. The three `ðurh` contexts now correctly describe accusative oath standards. A definite weak phrase is good Old English in an appropriate context, but does not satisfy this prompt.
- **31.13:** Actual Unit13 teaches `āscian` with an accusative person and genitive thing. I personally checked Cook276b’s159.b reference and Cook93’s explicitly labelled `ðē (acc.) hlāfes āxan`. The final key has **āscode hīe**, and the canonical dependencies now bind the accusative form and prior government feature. The old `hiere` was unsupported by this selected frame; the judgment is not a universal ban across all historical constructions translated “ask.” The later `hīe` remains the book, object of `ongiett`.
- **28.4:** The original `(169)` points to the perception construction with an accusative subject and plain infinitive, confirmed by Cook96. My blind **standende** conveyed the scene grammatically but missed that source target. The final local help now explicitly requests **ōðre … standan**, contrasts28.7’s printed participle direction, and preserves the original prompt. The key correctly calls the public-place sense taught. The accepted controlled response is `Hē geseah ōðre on strǣte īdle standan.`
- **29.9:** I independently rechecked the separate paradigm reviewer’s finding and AM02 repair. The learner now has the exact supplied **ēow bið giefen** frame, recipient/no-`hit` explanation, singular counterpart and non-recall boundary, with an actual teaching marker and bound feature. Both a consistent plural command and a consistent singular command are possible where English does not fix number.
- **Scope descriptions:** AM02 corrects the key’s labels for familiar `siextan`, Unit10’s addressed `unne`, and Unit7’s independent/passive wishes. AM03 makes all55 original assessment boundaries match their actual modes: taught forms/compositions remain productive targets; supplied support is not unaided recall; English analysis and reading comprehension do not promote every encountered form to production. The final contract has596 teaching records,130 grammar records and36 Cook-help groups.

## Alternatives and reviewer corrections

**Funde/fand in28.7:** I initially questioned the key’s `funde`; that objection is withdrawn. Actual Unit4 explicitly selects third-singular `funde` and permits `fand`. The personally inspected Wright258 note confirms first- and third-singular `funde` beside `fand`. Both answers are grammatical here. The review preserves this reversal instead of silently removing it.

**Modal choice in30.11:** The key’s `sceoldon` is defensible “ought to” and need not report a past event or a counterfactual. My blind reservation was too restrictive on that point. My `sculon` remains defensible under its stated present expectation/obligation reading, but is not an interchangeable spelling. `Scylen` would need a wish reading. The final key now explains the contextual difference; the source gives no unique tense control. Both repeated road clauses, `blōstmian`, feminine `fægeru brȳd`, singular `sceal` and noun `hām` remain required.

Two further corrections belong to my blind answers, not to the key:

- **29.8:** Replace my `Ēower mēd` with the selected **Ēowru mēd**. Actual Unit3 explicitly supplies feminine nominative singular `ēowru`, with `ēoweru` a supported alternative. The final key’s agreement is right; the rest of my sentence preserves the requested reward, children of the Highest and goodness to unthankful/evil people.
- **30.10:** Replace my out-of-scope `feld` with taught **æcer**: `Sēo sunne forbærnde his æcer.` This is a productive-vocabulary boundary, not a claim that `feld` is impossible Old English.

Other differences were judged by the prompt rather than by string equality. Accepted alternatives include distributive `gehwǣm` beside `ǣlcum` in28.2; prospective present `sęlle` beside `wille` plus infinitive in29.2; taught feminine `woruld` beside masculine `middangeard` in29.6–7, with consistent agreement and permitted uninflected predicative `hǣled`; prior `ðus` in30.3; ordinary constituent-order differences; and optional overt subjects where the imperative already fixes person. In the new compositions, prior `ðearfan` is a valid poor-person noun beside `wǣdlan` inC13, and substantival dative `nānum` satisfies C15 without an obligatory added `męnn`. In31.8, bare ethnonym `Dęnum` and prior `geworhte` preserve the four requested predicates. Bare indefinite `bōc` is valid in31.12/14, and prior inflected relative `ðā` is a defensible alternative in31.12 while the supplied attracted `hwæðrum` remains intact. These decisions are attached to their individual output records.

## Complete output and reading review

All116 requested morphology forms match the actual selected learner/key cells, with each coordinate preserved even when spellings repeat. The eighteen accompanying explanations correctly distinguish syncretism, singular-only/assigned-sense boundaries and compound inflection. The separate full691-cell paradigm review remains a distinct reviewer’s work; this record does not claim it by proxy.

All55 analysis outputs and19 new compositions were compared with their actual grammatical controls and taught/supplied scope. All50 complete Cook answers were checked against the page-image prompts, including item continuations, omissions, named vocabulary, person/number and prescribed word order. No difficult source clause or alternative in a long item was dropped. The ledger explicitly distinguishes grammatical alternatives from failure to meet a visible control.

The three full translations were composed independently from the actual Old English before key access. Comparison found no essential omission. The Duties translation retains both rebukes, pauperhood, hundredfold recompense, giving to the least as giving to the Savior, and eternal bliss; the bounded source’s outer quotation remains open. The Preface retains both translation methods, mental/bodily cares, kingdoms, study and prior prose/discourse translation, subsequent verse, the request for prayer/no blame, the different reader/Alfred pronouns, and the closing limits of understanding/leisure. The Prayer retains all grounds of entreaty—including Michael’s **obedience**—the opening requested subjunctive, all six commands, both comparison standards, the soul’s benefit twice, visible/invisible adversaries, the purpose and pure thought/body, all six concluding descriptions, and the three repeated “ever” terms with the final eternity phrase. The61 reading-analysis outputs identify the actual participants, cases, scopes and moods separately.

I personally viewed the exercise and reading scans and the targeted grammar/lexical images listed with concrete observations and hashes in the ledger. Hash checks identify those images; they do not substitute for visual inspection. Source-sensitive checks included actual `earth`, `If they can`, article omissions, `(169)` versus `(pres.part.)`, `gehīersumnesse`, `gestaðela`, `Sīe`, and the source distinction between personal `ðē` and relative `ðe`. AM01’s correction of `ǣghwilcum` to agree with `ęnde` is also confirmed by the prayer image.

## Acceptance identities and limits

'''
for a in artifacts:
    report += f"- `{a['path']}` — raw `{a['raw_sha256']}`; normalized LF `{a['normalized_lf_sha256']}`.\n"
report += f"\nSubstantive contract SHA256: `{ledger['accepted_contract_semantic_identity']['sha256']}`. The ledger lists every included top-level key and excludes only the agreed completion/review/checkpoint metadata fields. The final selected-model correction artifact is also identified there.\n\n"
report += 'All eleven findings are resolved, adjudicated or withdrawn. The acceptance is **pre-export**: complete learner/key PDFs, export parity, every-page visual inspection, cumulative-register integration and the coordinator’s final status/Beads/Git checkpoint remain separate gates. No later unit is reviewed or drafted here.\n'

if len(sys.argv) > 1 and sys.argv[1] == 'write':
    (ROOT/'chapters/ch15/review-ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    (ROOT/'chapters/ch15/review.md').write_text(report,encoding='utf-8',newline='\n')
    print(json.dumps({'written':['chapters/ch15/review.md','chapters/ch15/review-ledger.json'],'counts':counts,'artifacts':artifacts,'contract_semantic_sha256':ledger['accepted_contract_semantic_identity']['sha256']},ensure_ascii=False,indent=2))
else:
    print(json.dumps({'ready':True,'counts':counts,'contract_semantic_sha256':ledger['accepted_contract_semantic_identity']['sha256']},ensure_ascii=False,indent=2))
