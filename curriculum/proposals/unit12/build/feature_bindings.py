"""Public feature bindings. New audited IDs replace explicit pending names."""
ROLE_IDS={
'foot_paradigm':['@foot_paradigm'],
'new_nominals':['@brycg_paradigm','@here_paradigm'],
'new_indicatives':[],
'new_commands':['u06-imperative-use'],
'participle_pairs':['@participle_pairs'],
'habban_perfect':['@habban_perfect'],
'narrative_time':['u04-past-narration','@temporal_relations'],
'preterite_anterior':['@preterite_anterior'],
'active_passive':['u07-passive','u07-predicate-participle-variants','@voice_comparison'],
'wesan_intransitive':['@wesan_intransitive'],
'wesan_present_participle':['@wesan_present_participle'],
'reported_sequence':['u09-content-that','u09-reported-statement','@reported_sequence'],
'volitional_time':['u06-volition-willan','u06-plain-infinitive-complement','u07-modal-mood-distinction'],
'present_future':['u10-present-future'],
'gierwan_object':['@gierwan_object'],
'controlled_reading':[], 'source_reading':[]}
EXTRA={
'F01':[],'F02':[],'F03':[],'F04':[],'F05':[],'F06':['u02-direct-object'],'F07':[],
'A01':['u06-cuman-intransitive','u05-see-object'],
'A02':['u05-see-object','u02-direct-object','u08-relative-the','u02-third-person-possessors'],
'A03':['u02-direct-object'], 'A04':['u02-direct-object'],
'A05':['u04-direct-objects'], 'A06':['u10-gewitan-departure'],
'A07':['u05-intransitive-posture'],
'A08':[], 'A09':['u02-direct-object'], 'A10':['u06-cuman-intransitive'], 'A11':['u06-cuman-intransitive'],
'C01':['u02-direct-object'], 'C02':['u02-direct-object'],
'C03':['u04-direct-objects'], 'C04':[], 'C05':['u02-direct-object'],
'C06':['u06-cuman-intransitive'], 'C07':['u06-imperative-use'],
'C08':['u06-cuman-intransitive','u02-direct-object'],
'R01':[], 'R02':[], 'R03':['u02-pronoun-reference','u05-direct-quotation'], 'R04':['u02-direct-object'],
'S01':[],'S02':[],'S03':[],'S04':[],'S05':[],'S06':[],'S07':[],'S08':[]}
EXAMPLE_EXTRA={
'01':['u06-cuman-intransitive','u05-see-object'],
'02':['u05-see-object','u02-direct-object','u08-relative-the','u02-third-person-possessors'],
'03':['u02-direct-object'], '04':['u02-direct-object','u06-cuman-intransitive','u11-past-when-then'],
'05':['u04-direct-objects'], '06':['u04-direct-objects'],
'07':['u10-gewitan-departure'], '08':['u05-intransitive-posture'],
'09':[], '10':['u02-direct-object'], '11':['u06-cuman-intransitive'], '12':['u06-cuman-intransitive']}
CONTROLLED_EXTRA=['u02-direct-object','u06-cuman-intransitive','u05-see-object','u05-direct-quotation','u09-content-that','u09-reported-statement','u06-faran-intransitive','u06-plain-infinitive-complement','u06-volition-willan','u10-gewitan-departure','u05-intransitive-posture','on-dative-location','u02-giving-recipient','u02-third-person-possessors','u11-past-when-then','u02-pronoun-reference','u03-cardinal-one']
ALIASES={'@foot_paradigm':['u12-fot-paradigm'],'@brycg_paradigm':['u12-nominal-complete-systems'],'@here_paradigm':['u12-here-paradigm'],'@habban_perfect':['u12-habban-perfect'],'@temporal_relations':['u12-narrative-time'],'@preterite_anterior':['u12-preterite-anterior'],'@voice_comparison':['u12-active-passive'],'@wesan_intransitive':['u12-wesan-intransitive-perfect'],'@wesan_present_participle':['u12-wesan-present-participle'],'@reported_sequence':['u12-reported-sequence']}
ALIASES.update({'@gierwan_object':['u12-gierwan-accusative'],'@participle_pairs':['u12-gewyrcean-participle-bases','u12-gierwan-participle-bases','u12-settan-participle-bases']})
def roles(values):
 result=[]
 for role in values:
  for fid in ROLE_IDS[role]:
   result.extend(ALIASES.get(fid,[fid]))
 return sorted(set(result))
