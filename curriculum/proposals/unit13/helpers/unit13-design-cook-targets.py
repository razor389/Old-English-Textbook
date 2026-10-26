"""Public grammatical targets, with no ordered Old English answers."""
from pathlib import Path
import json
P=Path('curriculum/proposals/unit13')
targets={
22:[
'Nominal predicate and dependent genitive; use the newly assigned abstract and kinship senses.',
'Proper-name subject and a nested royal genitive; preserve the instruction to omit the English definite article before daughter. Names remain locally supplied.',
'Dependent possessor, adjective agreement with a neuter head, and agentless passive; use the specified destruction verb.',
'Singular command and means phrase with plural hands; retain the explicit singular addressee.',
'Singular command with the newly audited pursue-study frame and agreeing possessive.',
'Ordinary present go with the church as destination.',
'Plural departure command and a relative clause whose personal antecedent determines second-person plural agreement.',
'A direct question asking a name; do not mistake the interrogative for an object merely because it begins the sentence.',
'Command hātan with an accusative commanded party and a plain infinitive; distinguish destination and the person referred to.',
'The newly selected descending sense and its source and destination phrases; retain plural heavens.',
'The bounded customary-action construction with a visiting infinitive and accusative person.',
'Volition with an asking infinitive, accusative person and genitive thing; preserve the first-adverb and singular addressee controls.',
'Volition with leading an accusative person and an accompanying first-person pronoun.',
'Reflexive prostration with the new verb. The selected placement construction has beforan with an accusative landmark; a defensible static beforan with dative remains valid Old English and is distinguished from this stated target.',
'A stated third-day expression, feminine adjective agreement, agentless release and separation from the body.',
],
23:[
'Superlative window and church genitive, with separately supported dimensions and two/four-foot measures.',
'Gradual approach of a singular song, with weak adjective under its article.',
'Entreaty content with its own subject and a dependent name-question; preserve the bracketed that-clause target.',
'Coordinated past actions, a possessive object, four parts, and dative distribution to each soldier; preserve thus and the omitted-to control.',
'A dependent genitive and ordinary static standing beside the cross, using the directly attested wið with accusative landmark. Do not explain this case by a generic motion rule.',
'The explicitly taught substantival many use with a plural finite verb and an accusative writing.',
'An instrumental means phrase and the specified strong cutting verb; identify the direct object independently of initial position.',
'The specified placement passive and local root-phrase frame; retain the complete trees genitive.',
'Taking an accusative axe with a hand-goal expression; distinguish the hand’s possessor from its case.',
'The newly taught selling sense of sęllan, a recipient and five count objects.',
'Singular abstract infirmity with a bodily adjective and correctly agreeing grievous predicate.',
'Masculine companionship, its second-person possessor and a pleasant predicate.',
'A question with anticipatory reference and the specifically supported wonder/concession frame.',
],
24:[
'Substantival relative and main personal correlate; preserve the sitting clause and supported midst expression.',
'Plural nominal predication with the newly audited without-body phrase.',
'Past seeing with an accusative perceived actor and falling infinitive; preserve the until/limit target.',
'Substantival relative, explicit same correlate and passive clothing with the explicitly taught mid plus dative garment frame.',
'Fronted neuter-plural objects with a following saying predicate and a postposed substantival relative subject.',
'A fear command, accusative personal relative, capability and the locally supported both-soul-and-body destruction frame.',
'Negative worthiness and its supported entering-content clause; preserve the singular addressee and attested under plus accusative roof-entry frame. Supporting quotations with other entering verbs establish the prepositional frame without silently granting those lexemes.',
'Fronted predicate adjective with a feminine reward and a plural-possessor adjective; retain plural heavens.',
'A long conditional with a nested relative and two temporal viewpoints, followed by the much-more conclusion and locally supplied little-faith address.',
'Comparative nominal predication with coordinated soul/body topics and an understood repeated comparison predicate.',
'Plural behold-command and a separate feeding clause; distinguish plural addressees from the singular father.',
'A direct modal question with alternative eating/drinking infinitives and shared first-plural subject.',
],
25:[
'A subject relative, nested object relatives and a main question; recover every pronoun’s function and preserve negation.',
'A dependent genitive with the newly taught departure sense and nearness predicate.',
'A past action with a locally supplied indefinite/partitive expression, followed by a simultaneous while-clause and town destination.',
'A complete command of be with accompanying plural brothers.',
'An opening command and accusative plural windows governed by a house genitive.',
'Coordinated plural commands, a substantive dative relative and a purpose clause; personal references remain distinct across the long sentence.',
'Personal predication and an indicative condition containing an object relative. The nearest scope of the prompt’s final “verb last” direction is the relative containing I command you: put its finite verb last. The conditional dōð may precede that relative or follow it; neither arrangement creates a universal dependent-clause rule.',
'Past plural singing with a superlative song and the locally supported pleasant-to-hear description; preserve the accusative control.',
'A church genitive with singular roof, copula and agreeing high predicate.',
'The complete locally supplied angelic-company phrase, including the exact participial genitive-plural construction and initial then.',
'The complete locally supplied optative acclamation, preserving glory, highest places, earthly peace and the good-will genitive.',
'A return verb with a supported route expression and relative reference to an earlier arrival; preserve the omitted-by control.',
]}
rows=[dict(task_id=f'EX-VII-{exercise:02}-{i:02}',target_specification=target) for exercise,items in targets.items() for i,target in enumerate(items,1)]
assert len(rows)==52
(P/'cook-targets.json').write_text(json.dumps(dict(schema_version=1,chapter='ch13',status='public_target_design_pending_evidence_join',targets=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(len(rows))
