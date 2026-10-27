"""Ordered source-token dependencies; explicit selector overrides avoid homograph guessing."""
import json,re,pathlib,unicodedata,collections
OUT=pathlib.Path(__file__).parent;ROOT=OUT.parents[2]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
prior=read('lexicon/entries.json')['lemmas'];new=read('sources/audits/unit16-source/lexical-inventory.json')['lemmas']
gram=read('sources/audits/unit16-grammar/grammar-records.json')
gv=read('sources/audits/unit16-grammar/reading-verbal-support.json')
alllem=prior+new+gram.get('lemmas',[])+gv['lemmas'];index=collections.defaultdict(list)
for l in alllem:
 for f in l.get('forms',[]):index[f['form'].casefold()].append((l,f))
reading=read('sources/audits/unit16-source/reading-source.json')['source_spans'][0]
tokens=[]
for line in reading['source_lines']:
 for i,w in enumerate(re.sub(r'\[\d+\]','',line['source_with_note_markers']).split(),1):
  w=w.strip('.,;:!?“”‘’')
  if tokens and tokens[-1]['surface'].endswith('-') and tokens[-1]['surface'] not in ['swā-','ðā-']:
   tokens[-1]['surface']=tokens[-1]['surface'][:-1]+w;tokens[-1]['continuation_line']=line['source_line_id'];continue
  tokens.append({'token_id':f'U16-R-T{len(tokens)+1:03}','source_span_id':reading['source_span_id'],'source_line_id':line['source_line_id'],'printed_page':line['printed_page'],'pdf_page_one_based':line['pdf_page_one_based'],'editorial_line':line['editorial_line'],'line_token_position':i,'surface':w})
assert len(tokens)==444,len(tokens)
gvmap={(x['source_line_id'],x['surface'].casefold()):x for x in gv['items']}
nominal={l['lemma_id']:l for l in new}
def an(f):
 raw=f.get('analysis',{});a=dict(raw) if isinstance(raw,dict) else {'source_analysis':raw};ctx=f.get('contextual_analysis',{});a.update(ctx if isinstance(ctx,dict) else {'contextual_source_analysis':ctx})
 # Earlier contracts sometimes retain source prose instead of structured cases.
 context=str(a.get('source_analysis',''))+' '+f['form_id']
 for k,values in [('case',['nom','gen','dat','acc','ins']),('number',['sg','pl']),('gender',['m','n','f'])]:
  if k not in a:
   for v in values:
    if re.search(r'(?:^|[- ])'+v+r'(?:$|[- ])',context):a[k]=v;break
 return a
def eq(a,key,val):
 v=str(a.get(key,''));return v==val or v.startswith({'nom':'nominative','gen':'genitive','dat':'dative','acc':'accusative','sg':'singular','pl':'plural','m':'masculine','n':'neuter','f':'feminine'}.get(val,'NOT_A_WORD'))
selectors={
 'hē':('he',{'case':'nom','number':'sg','gender':'m'}),'him':('he',{'case':'dat','number':'sg','gender':'m'}),'hine':('he',{'case':'acc','number':'sg','gender':'m'}),'his':('he',{'case':'gen','number':'sg','gender':'m'}),'hiera':('he',{'case':'gen','number':'pl'}),
 'ic':('ic',{'case':'nom','number':'sg'}),'gē':('thu',{'case':'nom','number':'pl'}),'ðū':('thu',{'case':'nom','number':'sg'}),'ēow':('thu',{'case':'dat','number':'pl'}),'ðē':('thu',{'case':'acc','number':'sg'}),
 'se':('se',{'case':'nom','number':'sg','gender':'m'}),'sē':('se',{'case':'nom','number':'sg','gender':'m'}),'ðone':('se',{'case':'acc','number':'sg','gender':'m'}),'ðæs':('se',{'case':'gen','number':'sg','gender':'m'}),'ðǣre':('se',{'case':'gen','number':'sg','gender':'f'}),'ðǣm':('se',{'case':'dat','number':'sg','gender':'m'}),
 'ðisum':('thes',{'case':'dat','number':'pl'}),'ðes':('thes',{'case':'nom','number':'sg','gender':'m'}),'ðe':('the-relative',{}),'ðā':('tha-adverb',{}),
 'wordum':('word',{'case':'dat','number':'pl'}),'weg':('weg',{'case':'acc','number':'sg'}),'ceastre':('ceaster',{'case':'gen','number':'sg'}),'geate':('geat',{'case':'dat','number':'sg'}),'hwone':('hwa',{'case':'acc','number':'sg','gender':'m'}),'līfes':('lif',{'case':'gen','number':'sg'}),
 'ǣnne':('an',{'case':'acc','number':'sg','gender':'m'}),'nacodne':('nacod',{'case':'acc','number':'sg','gender':'m'}),'cnapan':('cnapa',{'case':'acc','number':'sg'}),'strǣte':('straet',{'case':'acc','number':'sg'}),'ęle':('ele',{'case':'dat','number':'sg'}),
 'geongra':('geong',{'case':'gen','number':'pl','gender':'m'}),'manna':('mann',{'case':'gen','number':'pl'}),'handa':('hand',{'case':'dat','number':'sg'}),'micelre':('micel',{'case':'dat','number':'sg','gender':'f'}),'stefne':('stefn',{'case':'dat','number':'sg'}),
 'ānra':('an',{'case':'gen','number':'pl','gender':'m'}),'gehwilcne':('gehwilc',{'case':'acc','number':'sg','gender':'m'}),'weorce':('weorc',{'case':'dat','number':'sg'}),'ealre':('eall',{'case':'gen','number':'sg','gender':'f'}),'cyning':('cyning',{'case':'nom','number':'sg'}),'cyninges':('cyning',{'case':'gen','number':'sg'}),'cyninge':('cyning',{'case':'dat','number':'sg'}),'gefērum':('gefera',{'case':'dat','number':'pl'}),
 'ðoðore':('thothor',{'case':'dat','number':'sg'}),'ðoðor':('thothor',{'case':'acc','number':'sg'}),'god':('god',{'case':'nom','number':'sg'}),'geongan':('geong',{'case':'gen','number':'sg','gender':'m'}),'gelǣredre':('gelared',{'case':'dat','number':'sg','gender':'f'}),'bæð':('baeth',{'case':'acc','number':'sg'}),'bæðe':('baeth',{'case':'dat','number':'sg'}),'weges':('weg',{'case':'gen','number':'sg'}),'mannum':('mann',{'case':'dat','number':'pl'}),'hwilces':('hwilc',{'case':'gen','number':'sg','gender':'m'}),'geonges':('geong',{'case':'gen','number':'sg','gender':'m'}),'mannes':('mann',{'case':'gen','number':'sg'}),'ānum':('an',{'case':'dat','number':'sg','gender':'m'}),'geonga':('geong',{'case':'nom','number':'sg','gender':'m'}),'mann':('mann',{'case':'nom','number':'sg'}),'self':('self',{'case':'nom','number':'sg','gender':'m'}),'gegierela':('gegierela',{'case':'nom','number':'sg'})}
overrides={('FB168-05','ðā'):('se',{'case':'acc','number':'sg','gender':'f'}),('FB170-02','ðā'):('se',{'case':'acc','number':'sg','gender':'f'}),('FB169-15','ðǣre'):('se',{'case':'dat','number':'sg','gender':'f'}),('FB168-12','ðǣm'):('se',{'case':'dat','number':'sg','gender':'n'}),('FB169-13','ðǣm'):('se',{'case':'dat','number':'sg','gender':'n'}),('FB169-15','ðǣm'):('se',{'case':'dat','number':'sg','gender':'n'}),('FB168-11','ðæt'):('se',{'case':'acc','number':'sg','gender':'n'}),('FB168-17','ðæt'):('se',{'case':'acc','number':'sg','gender':'n'}),('FB170-12','ðæt'):('se',{'case':'acc','number':'sg','gender':'n'}),('FB170-06','hwæt'):('hwa',{'case':'nom','number':'sg','gender':'n'}),('FB170-12','hwæt'):('hwa',{'case':'acc','number':'sg','gender':'n'}),('FB169-08','mē'):('ic',{'case':'dat','number':'sg'}),('FB170-03','mē'):('ic',{'case':'acc','number':'sg'}),('FB170-06','mē'):('ic',{'case':'dat','number':'sg'}),('FB168-06','plegan'):('plega',{'case':'acc','number':'sg'}),('FB169-01','plegan'):('plega',{'case':'acc','number':'sg'}),('FB169-07','plegan'):('plega',{'case':'dat','number':'sg'}),('FB168-07','bæðstęde'):('baethstede',{'case':'dat','number':'sg'}),('FB168-10','bæðstęde'):('baethstede',{'case':'nom','number':'sg'})}
unresolved=[]
verb_context={'ēode':(3,'indicative'),'wæs':(3,'indicative'),'becōm':(3,'indicative'),'ðōhte':(3,'indicative'),'geseah':(3,'indicative'),'bær':(3,'indicative'),'cwæð':(3,'indicative'),'is':(3,'indicative'),'gehīerde':(3,'indicative'),'hæfde':(3,'indicative'),'sōhte':(3,'indicative'),'meahte':(3,'indicative'),'cōm':(3,'indicative'),'wolde':(3,'indicative'),'āsęnde':(3,'indicative'),'lēt':(3,'indicative'),'wiste':(3,'indicative'),'næfde':(3,'indicative'),'ðyncð':(3,'indicative'),'wǣre':(3,'subjunctive'),'lǣdde':(3,'indicative'),'dyde':(1,'indicative'),'sīe':(3,'subjunctive'),'wāst':(2,'indicative'),'andswarode':(3,'indicative'),'bitt':(3,'indicative'),'cume':(2,'subjunctive')}
function_senses={'his':'he-possessor','hiera':'he-possessor','wel':'wel-positive','bęt':'wel-comparative','se':'se-the','sē':'se-the','ðone':'se-the','ðæs':'se-the','ðǣre':'se-the','ðǣm':'se-the','swā-swā':'swa-swa-as-source','swilce':'swilce-u16-as-if','ðæs-ðe':'thaes-the-u16-as-seems','æfter':'aefter-after-source','tō':'to-destination','mid':'mid-by-means','on':'on-1','ðurh':'thurh-u15-oath'}
sense_overrides={('FB168-05','sē'):'se-that',('FB168-11','ðæt'):'se-that',('FB170-12','ðæt'):'se-that',('FB169-13','ðǣm'):'se-that',('FB168-17','ðæt'):'se-the',('FB168-07','tō'):'to-u16-belonging',('FB169-07','tō'):'to-u14-speech-addressee-source',('FB170-01','tō'):'to-u14-speech-addressee-source',('FB170-10','tō'):'to-u14-speech-addressee-source',('FB169-13','tō'):'to-u16-rejuvenation',('FB170-08','æfter'):'aefter-u16-seeking',('FB170-11','æfter'):'aefter-u16-seeking',('FB168-01','on'):'on-into-goal',('FB168-13','on'):'on-u16-at-work',('FB169-01','on'):'on-u16-at-work',('FB169-07','on'):'on-u16-at-work',('FB168-17','on'):'on-into-goal',('FB168-16','mid'):'mid-accompaniment-source',('FB169-02','mid'):'mid-u13-manner-source',('FB170-09','mid'):'mid-u13-clothing',('FB169-13','of'):'of-u16-old-age',('FB169-15','be'):'be-u16-grasp'}
for surface,lid in [('ðæt','thaet-conjunction'),('swilce','swilce'),('æfter','aefter'),('mid','mid'),('on','on'),('tō','to'),('be','be'),('of','of'),('bęt','wel'),('wel','wel')]:selectors[surface]=(lid,{})
selectors['mīn']=('min-poss',{'case':'nom','number':'sg','gender':'m'})
overrides[('FB168-12','on')]=('on-adverb',{})
for t in tokens:
 s=t['surface'].casefold();key=(t['source_line_id'],s)
 if key in gvmap:
  x=gvmap[key];t.update({k:x[k] for k in ['lemma_id','form_id','sense_id','analysis','knowledge_status','evidence_refs']});t['scope_rationale']=x['explanation'];t['supply']=x['actual_supplied_text'];continue
 cs=index[s];sel=overrides.get(key,selectors.get(s))
 if sel:
  lid,criteria=sel;cs=[x for x in cs if x[0]['lemma_id']==lid and all(eq(an(x[1]),k,v) for k,v in criteria.items())]
 if s in verb_context:
  person,mood=verb_context[s]
  filtered=[x for x in cs if (an(x[1]).get('person') in [person,str(person)] or re.search('-'+str(person)+'-sg',x[1]['form_id'])) and (mood in str(an(x[1]).get('mood','')) or (mood=='indicative' and 'subj' not in x[1]['form_id']))]
  if filtered:cs=filtered
 if s=='tō':cs=[x for x in cs if x[1]['form_id']=='to-preposition-dative-invariant']
 if not cs:
  unresolved.append({'token_id':t['token_id'],'line':t['source_line_id'],'surface':t['surface'],'selector':sel,'available':[(l['lemma_id'],f['form_id']) for l,f in index[s]][:10]});t['knowledge_status']='unresolved';continue
 # Prefer explicit current supplied/teaching records, then earliest productive actual source record.
 cs.sort(key=lambda x:(0 if x[0] in new else 1,0 if x[1].get('production_taught_in') else 1,x[1]['form_id']))
 l,f=cs[0]; senses=[z for ll in alllem if ll['lemma_id']==l['lemma_id'] for z in ll.get('senses',[])];sid=sense_overrides.get(key,function_senses.get(s));sense=next((x for x in reversed(senses) if x['sense_id']==sid),next((x for x in senses if x.get('production_taught_in')),senses[0]))
 status=f.get('knowledge_status','supplied') if l in new else ('previously_taught' if f.get('production_taught_in') else 'supplied')
 t.update({'lemma_id':l['lemma_id'],'form_id':f['form_id'],'sense_id':sense['sense_id'],'analysis':an(f),'knowledge_status':status,'sense_status':sense.get('knowledge_status') if l in new else ('previously_taught' if sense.get('production_taught_in') else 'supplied'),'evidence_refs':[f'U16-FB-P{t["printed_page"]}']+f.get('evidence_refs',[]),'scope_rationale':'Exact current source supply/production record.' if l in new else 'Actual cumulative form and sense records inspected; prior IDs and source analyses retained. Contextual constructions are separately supported.'})
 t['prior_scope']={k:f.get(k) for k in ['production_taught_in','recognition_taught_in','supplied_in','coverage_contract']}
 if len(cs)>1:t['syncretic_form_candidates']=[f2['form_id'] for l2,f2 in cs if f2['form_id']!=f['form_id']]
# Final manual contextual pass. These overrides are by ordered token, because a
# single line may contain two identical words in different functions.
contextual={
 31:('fultum-u15-source-sense','the explicitly supplied help/support sense in līfes fultumes'),
 85:('apollonius-u16-reading','source-local proper-name reference; earlier gloss to Apollonius was tied to a supplied dative context'),
 133:('theod-u16-region','the expressly supplied region/country sense, distinct from prior people/nation'),
 156:('apollonius-u16-reading','source-local nominative proper-name reference'),
 232:('apollonius-u16-reading','source-local nominative proper-name reference'),
 315:('apollonius-u16-reading','source-local nominative proper-name reference'),
 323:('haelu-u11-source','supplied safety/rescue in the oath; do not substitute productivech15 salvation sense'),
 371:('apollonius-u16-reading','source-local dative proper-name reference within the same declared name support'),
 12:('wesan-passive','auxiliary of getǣht'),33:('geseon-perceive-action','accusative actor plus iernan infinitive'),
 43:('wesan-passive','auxiliary shared by gesmierwed and begyrd'),48:('mid-u16-source-clothing','cloth complement of begyrd'),
 107:('he-1','partitive genitive: each one of them; the later hiera111 is possessive'),
 150:('with-u16-players','dative fellow players, not the earlier accusative opponent frame'),
 176:('ongean-u16-back','adverb back with gesęnde'),184:('ongean-u16-back','source āgēan: adverb back with āsęnde'),
 203:('thaet-u16-uncertain-link','Cook169note6 explicitly leaves this linkage unclear'),205:('witan-content','knowledge stated by following ðæt clause'),
 211:('on-u16-at-work','in the game: on ends169.6 and governs ðǣm plegan at169.7; retain the explicitly supplied activity sense'),
 255:('mid-u13-manner-source','manner: with such great swiftness'),259:('thaet-result','result after swā micelre swiftnesse'),
 262:('wesan-u16-impersonal-seemed','supplied impersonal wæs geðūht, dative experiencer'),271:('wesan-passive','apparent transformation expressed by gewęnd wǣre'),
 317:('wesan-intransitive-perfect','completed departure āgān wæs, not a passive'),331:('thonne-than','comparative complement after bęt'),333:('don-u16-substitute','did so, referring back to bathing'),
 337:('thurh-u16-means','service as means, not an oath standard'),374:('geseon-u16-content','saw that with a finite content clause'),
 377:('wesan-passive','auxiliary of bewǣfed'),378:('mid-u16-source-clothing','cloak complement of bewǣfed'),385:('ongean-u16-back','adverb returned back'),386:('to-destination','destination of returned: to the king'),405:('thurh-u16-means','by what evidence; source note12'),
}
byform={f['form_id']:(l,f) for l in alllem for f in l.get('forms',[])}
bysense={s['sense_id']:s for l in alllem for s in l.get('senses',[])}
priorforms={f['form_id']:f for l in prior for f in l.get('forms',[])}
priorsenses={s['sense_id']:s for l in prior for s in l.get('senses',[])}
currentforms={f['form_id']:f for l in new+gram.get('lemmas',[])+gv['lemmas'] for f in l.get('forms',[])}
currentsenses={s['sense_id']:s for l in new+gram.get('lemmas',[])+gv['lemmas'] for s in l.get('senses',[])}
def selected_status(identity,old,current):
 if identity in old and old[identity].get('production_taught_in'):return 'previously_taught'
 if identity in current:return current[identity].get('knowledge_status','supplied')
 return 'previously_taught' if identity in old and old[identity].get('recognition_taught_in') else 'supplied'
for t in tokens:
 n=int(t['token_id'][-3:])
 if n in contextual:
  sid,why=contextual[n];assert sid in bysense,sid;t['sense_id']=sid;t['contextual_sense_rationale']=why
 if n in [176,385]:
  t['form_id']='ongean-u16-adverb-invariant';t['analysis']=an(byform[t['form_id']][1]);t.pop('syncretic_form_candidates',None)
 if n==331:
  t['lemma_id']='thonne';t['form_id']='thonne-invariant';t['analysis']=an(byform[t['form_id']][1]);t.pop('syncretic_form_candidates',None)
 if 'form_id' in t:
  if t['form_id'] in priorforms:t['registered_analysis']=priorforms[t['form_id']]['analysis']
  if t['lemma_id'] in ['wesan','geseon'] and n not in [262,374]:t['analysis'].pop('context',None)
  if n in contextual:t['contextual_analysis']={**t['analysis'],'source_use':contextual[n][1]}
  if n in [29,238]:
   t['mood_identification_note']='The selected record gives a contextual analysis; this surface does not uniquely distinguish indicative from subjunctive. Do not assess a unique mood from its ending.'
   t['syncretic_mood_alternatives']=['indicative','subjunctive']
  t['knowledge_status']=selected_status(t['form_id'],priorforms,currentforms)
  t['sense_status']=selected_status(t['sense_id'],priorsenses,currentsenses)
  t['prior_sense_scope']={k:priorsenses.get(t['sense_id'],{}).get(k) for k in ['production_taught_in','recognition_taught_in','supplied_in','coverage_contract']}
  if t['sense_status']=='supplied':t['sense_supply']=bysense[t['sense_id']]['gloss']
  if n==317:t['scope_rationale']='Prior ch12 recognition of intransitive perfect, repeated with the exact departure phrase supplied locally; independent productive recall is not claimed.'
dump('reading-token-ledger.json',{'schema_version':1,'status':'source checked; contextual review complete' if not unresolved else 'reconciliation draft','source_span_id':reading['source_span_id'],'token_count':len(tokens),'tokens':tokens,'unresolved':unresolved,'contextual_review':'All444 tokens reviewed in sequence; explicit homograph, preposition, pronoun, person, mood and lexical-sense corrections retained in the generator. Local disputed source syntax remains supplied and identified as uncertain, not silently resolved.','tokenization':'Whitespace words after removing note anchors and punctuation; printed division hyphens joined across169.1–2 and170.6–7. Lexical/correlative hyphens remain.'})
print(json.dumps({'unresolved_count':len(unresolved),'unresolved':unresolved},ensure_ascii=False,indent=1))
