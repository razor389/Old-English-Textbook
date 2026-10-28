from pathlib import Path
import copy,hashlib,json
O=Path('curriculum/proposals/unit18')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
srcpath=Path('sources/audits/unit18-source/exercises-prompts.json')
src=read(srcpath); hints=read('sources/audits/unit18-source/exercise-hints.json')
errors={
44:[
'Keep the sons as plural addressees and us as beneficiary; do not turn the amount of food into a count of food items.',
'Preserve both the negative permission and its exception, including the youngest brother and accompaniment; do not make Judah the person swearing the earlier oath.',
'Keep the finite verb last in the conditional clause as directed; omit the future auxiliary while retaining future reference. The relative has its own need-government.',
'Keep the persons addressed, ill treatment and earlier report distinct; do not confuse the quantifier more with an adjective agreeing with brethren.',
'Do not omit all, either indirect question, the negative knowledge, the desire or the genitive demonstrative before its following content clause.',
'Retain the singular command, both purposes, the negative perish, the exception and the first-person wish of guilt. Do not replace the wish with a factual confession.',
'Preserve the contrary condition and unreal completed arrival; do not translate the delay as an actual absence or omit the second-time expression.',
'Preserve conditional necessity, the command to do as they choose, source-partitive fruits, vessels, recipient, honey and acorns; do not omit an item of the gifts.'
],
45:[
'Both commands address the brothers. Keep their brother singular and the destination person distinct from the carried companion.',
'Preserve the wish, causative adjective, recipient of the restored brother, identifying relative and the separate lament; do not equate grammar of the causative with the adjective’s lexical sense.',
'Retain presents, double money, travel destination and Joseph; do not silently regularize the exact twīfeald hint or count money as several animals.',
'Keep seeing and speaking in sequence, plural men as the objects to be led in, feast as prepared object and the purpose of eating at noon.',
'In the source’s commanded-him rephrasing, the person commanded is dative. Do not make him an accusative passive subject.',
'Preserve arrival, fear, mutual speech, the causal money phrase, the found-in-sacks relative, passive bringing, both possessions taken and the threatened enslaving of the speakers.',
'Preserve the address, explicit request for hearing, earlier visit, wheat and dative selves as beneficiaries. Do not read the personal reflexive as a direct object.',
'Retain completed trading, homeward state, opening sacks, discovery, therein and the earlier giving; do not invent a second source of the money.',
'Retain brought-back money and other silver, the instrumental/trading relation and ignorance of who put the money into their sacks.',
],
46:[
'Distinguish the peace wish from the plural negative command; retain both named relations to God and the location of treasure in the sacks.',
'Do not switch the washers of the feet or the giver of fodder; distinguish the possessors from the recipient animals.',
'Retain presentation of the gifts and the anticipated entry; the source ongēan ðætte needs its own temporal meaning and supplied scope.',
'Joseph recognizes them, then asks two questions about their father. Do not let a form of know stand in for the new recognition sense without evidence.',
'Retain servant in apposition to our father, health and still living, with each possessor/addressee correctly identified.',
'Keep Joseph as seer and speaker, Benjamin as brother and the boy as the neuter demonstrative’s identification; retain the earlier telling and the blessing wish.',
'Preserve command recipient, all sacks, wheat and the instruction to put each person’s money in his own sack; do not assign the same possessor to every sack.',
'Retain the silver cup, wheat price, the wheat’s relative clause, youngest person’s sack and the reported execution. Do not omit either object placed into the sack.',
'Retain morning, travel, outside-city sense, distance already travelled, command sequence, anticipated catching, question and reversal of good and evil.',
],
47:[
'Keep the stolen cup as relative object, plural ye as thieves in the accusation, and the lord as the person to whom it was precious.',
'Preserve commanded action, passive catching, returned money and its origin, the rhetorical question and both gold and silver; omit only the expressly omitted auxiliary.',
'Preserve the singular search command, passive killing wish and the person with whom the thing is found. The finding relative has its own internal prepositional role.',
'Keep free-choice possessor and resumed servant identity distinct, and preserve the separate innocence wish for the others.',
'Retain search from oldest to youngest, discovery in Benjamin’s sack and the return to the city. Do not replace the source endpoints by invented ages.',
'Keep Judah first, his brothers accompanying him, Joseph as destination/addressee and all as participants in the final prostration.',
'Preserve the direct question and final finite verb as directed; do not omit the willingness/motive expressed by would.',
'The stolen-cup relative identifies the one who is to remain a servant. Keep the separate plural command allowing the others to return free to their father.',
'Retain Judah’s quoted second-person question about the speakers’ possession of father or brother; do not make Judah ask a new question here.',
'Retain old father, youngest brother, accompaniment, the particular brother as sole favored object and the comparison above us all. Preserve the exact unmarked ænne hint.',
'The exact prompt says present commandest. Preserve that source wording and distinguish any explicitly justified contextual alternative; retain commanded bringing, purpose of seeing and the conclusion that the speakers are not spies.',
],
48:[
'Preserve the oath’s recipient and reported promise, then the quoted exception and everlasting guilt wish toward the father; do not merge the two times or add a forbidden English-style future auxiliary.',
'Retain the vocative, permission for the lad and brothers to go, and the speaker’s substitution as servant for the lad.',
'Preserve fear/daring negation, absence of the lad and the prevented event of seeing the father’s grief.',
'Retain inability to conceal himself, the comparative longer, the expulsion of every other person and its negative purpose; do not reverse who is excluded.',
'Keep weeping and loud crying separate, then speech to brothers, Joseph’s identification and the question whether their father still lives.',
'Preserve the prohibition, impersonal grief expression, sale into this kingdom, divine sending, benefit to the brothers and destination. Do not turn the reassurance into denial that a sale occurred.',
'Retain two past famine years and five still expected, the source’s omitted be and implicit years, and the paired negative plough/reap clause. Do not claim the five years have already elapsed.',
'Retain plural commands to go, tell and bid, all Egyptians as the domain of lordship, and both coming and dwelling in the command content.',
'Retain the plural instruction and the negative purpose of avoiding perishing.',
'Keep the two perception statements and their respective embedded questions: how things stand with Joseph and what he says to the brothers.'
]}
rows=[]
for item in src['items']:
    e,n=item['original_exercise'],item['original_item'];tid=item['source_item_id']
    row=copy.deepcopy(item)
    row.update(task_id=tid,key_id='KEY-'+tid,key_item_id='KEY-'+tid,proposed_disposition='assigned',pedagogical_group=item['semantic_and_construction_demands'],
        requested_outputs=[{'output_position_id':tid+'-O001','kind':'complete_translation','response_language':'Old English','label':'Translate the complete numbered prompt, retaining its original controls.','target':item['semantic_and_construction_demands'],'essential_meaning':item['prompt'],'alternatives_policy':'Accept evidenced grammatical alternatives preserving every proposition and participant. Report compliance with an explicit lexical, order, number, omission or bracketed target separately from linguistic validity.','error_diagnosis':errors[e][n-1]}],
        dependency_status='awaits exact model identities and complete teaching/support joins',
        exact_prompt_ref=srcpath.as_posix()+'#/items/'+str(len(rows)),
        supplied_reference_rule='All exact original hints and whole local help remain visible. Their forms and meanings are reference input; unaided recall of supplied content is not tested.')
    rows.append(row)
controls=[{'reference_id':h['hint_id'],'task_id':h['source_item_id'],'literal_source_text':h['exact_text'],'character_start_zero_based':h['character_start'],'character_end_exclusive':h['character_end'],'source_kind':h['kind'],'evidence_refs':h['evidence_refs'],'independent_recall_assessment':False} for h in hints['records']]
for c in controls:
    prompt=next(i['prompt'] for i in src['items'] if i['source_item_id']==c['task_id'])
    assert prompt[c['character_start_zero_based']:c['character_end_exclusive']]==c['literal_source_text'],c
assert len(rows)==47 and len(controls)==154
def save(n,d):(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
save('source-task-crosswalk.json',{'schema_version':1,'chapter':'ch18','status':'all exact prompts and response contracts; dependency joins pending','canonical_assignment_rule':'Only the active coordinator coverage contract assigns these records; proposal retains every complete set with no redistribution or omission.','source_input':{'path':srcpath.as_posix(),'sha256':hashlib.sha256(srcpath.read_bytes()).hexdigest()},'instructions':src['instructions'],'cook_items':rows,'counts':src['counts_by_exercise'],'source_only_statement':'The Joseph material is an English composition sequence, not a separate attested Old English Joseph reading.'})
save('input-reference-records.json',{'schema_version':1,'chapter':'ch18','status':'exact source-control spans before linguistic binding','records':controls,'count':len(controls)})
print(json.dumps({'cook_items':len(rows),'outputs':len(rows),'source_controls':len(controls)},indent=2))
