import json,pathlib
P=pathlib.Path(__file__).parent;R=P.resolve().parents[2]
def read(p):return json.loads((R/p).read_text(encoding='utf8'))
def dump(n,x):(P/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
L={l['lemma_id']:l for l in read('lexicon/entries.json')['lemmas']};N={l['lemma_id']:l for l in read('sources/audits/unit15-source/lexical-inventory.json')['lemmas']}
for lid,l in N.items():
 if lid in L:L[lid]={**L[lid],**l,'forms':list({f['form_id']:f for f in L[lid]['forms']+l['forms']}.values()),'senses':list({s['sense_id']:s for s in L[lid]['senses']+l['senses']}.values())}
 else:L[lid]=l
# Every overt nominal demand in each original prompt. Final model token order is owned by grammar/design.
DATA={
28:['nama-dat-sg hus-acc-sg brothor-acc-pl sweostor-acc-pl faeder-acc-sg modor-acc-sg wif-acc-sg bearn-acc-pl land-acc-pl lif-acc-sg','pening-acc-sg daeg-gen-sg weorc-dat-sg','wingeard-acc-sg','straet-dat-sg','wingeard-acc-sg','tid-acc-sg','tid-acc-sg','daeg-acc-sg','mann-nom-sg','aefen-nom-sg wingeard-gen-sg hlaford-nom-sg gerefa-dat-sg wyrhta-acc-pl med-acc-sg','tid-acc-sg pening-dat-sg',''],
29:['hefignes-acc-pl daeg-gen-sg haetu-dat-sg','','','pening-dat-sg','wer-nom-sg witga-nom-sg word-dat-sg weorc-dat-sg god-dat-sg folc-dat-sg','dom-nom-sg leoht-nom-sg woruld-acc-sg mann-nom-pl thiestru-acc-pl leoht-acc-sg weorc-nom-pl','god-nom-sg sunu-acc-sg woruld-acc-sg woruld-nom-sg','med-nom-sg bearn-nom-pl','','leornungcniht-nom-sg lareow-acc-sg','mildheortnes-acc-sg haelu-gen-sg'],
30:['heofon-acc-sg god-gen-sg setl-nom-sg eorthe-acc-sg fotsceamul-nom-sg burg-nom-sg cyning-gen-sg','heafod-acc-sg haer-acc-sg','word-nom-sg','eage-nom-sg eage-dat-sg toth-nom-sg toth-dat-sg','bebod-dat-pl mann-acc-pl rice-dat-sg heofon-gen-pl','','tid-dat-pl','eorthe-nom-sg','gedeorf-dat-sg','sunne-nom-sg aecer-acc-sg','weg-nom-pl bryd-nom-sg ham-noun-acc-sg','',''],
31:['aliesend-nom-sg','flaesc-dat-sg god-acc-sg','god-gen-sg willa-acc-sg','costnung-acc-sg','nama-nom-sg','willa-nom-sg eorthe-dat-sg heofon-dat-pl','cyning-nom-sg engle-gen-pl','dene-dat-pl folc-acc-sg awendednes-acc-pl leothwyrhta-nom-sg','modor-nom-sg faeder-nom-sg','gear-gen-pl','becraeding-acc-sg gear-gen-pl','modor-nom-sg boc-acc-sg leoth-gen-pl sunu-gen-pl','boc-acc-sg','bisceop-nom-sg boc-acc-sg cyning-gen-sg lif-gen-sg']}
def norm(x):return {'nominative':'nom','genitive':'gen','dative':'dat','accusative':'acc','singular':'sg','plural':'pl'}.get(x,x)
def cells(lid,case,num):
 out=[]
 for f in L[lid]['forms']:
  a=f.get('contextual_analysis',f.get('analysis',{}));s=' '.join(str(v) for v in a.values()) if isinstance(a,dict) else a;a=a if isinstance(a,dict) else {}
  if (norm(a.get('case'))==case and norm(a.get('number'))==num) or f'-{case}-{num}' in f['form_id'] or case+'-'+num in s:
   out.append(dict(form_id=f['form_id'],form=f['form'],knowledge_status='previously_taught' if f.get('production_taught_in') else f.get('knowledge_status','supplied'),production_taught_in=f.get('production_taught_in'),recognition_taught_in=f.get('recognition_taught_in')))
 return out
prompts=read('sources/audits/unit15-source/exercises-prompts.json')['items'];items=[]
for p in prompts:
 ex=p['original_exercise'];n=p['original_item'];deps=[]
 for slot in DATA[ex][n-1].split():
  lid,case,num=slot.rsplit('-',2);fs=cells(lid,case,num);assert fs,(p['source_item_id'],slot)
  l=L[lid];senses=N[lid]['senses'] if lid in N else [s for s in l['senses'] if s.get('production_taught_in')]
  deps.append(dict(lemma_id=lid,headword=l['display_headword'],case=case,number=num,form_candidates=fs,sense_candidates=[dict(sense_id=s['sense_id'],gloss=s.get('contextual_gloss',s['gloss']),knowledge_status='previously_taught' if s.get('production_taught_in') else s.get('knowledge_status','supplied'),production_taught_in=s.get('production_taught_in')) for s in senses],note='Exact final ordered form/sense binding is in the grammar/design model packet; the present record bounds the source noun requirement.'))
 items.append(dict(source_item_id=p['source_item_id'],original_group=p['original_group'],prompt=p['prompt'],disposition='assigned',evidence_refs=p['evidence_refs'],nominal_requirements=deps,other_dependencies_owner='sources/audits/unit15-grammar; curriculum/proposals/unit15',origin_category='source audit and declared new-composition requirements, not a source Old English quotation'))
notes=[
 ('EX-IX-28-01','Preserve every disjunctive noun phrase, including sisters, and both the hundredfold requital and additional eternal-life clauses. Kinship morphology is not interchangeable: complete sweostor system is now taught; earlier brōðor/mōdor systems remain distinct.'),
 ('EX-IX-28-04','Strǣt has the public-place sense explicitly in Cook’s English glossary59 and Reader vocabulary314. This is a new sense alongside prior street.'),
 ('EX-IX-28-06','Tīd hour is promoted from the previously supplied Unit13 interval sense. Exact sixth/ninth ordinal words and temporal ymbe are handled in the grammar support.'),
 ('EX-IX-28-10','Ǣfen evening and wyrhta workman are prior nouns. Gerēfa steward and wīngeard vineyard have complete new tables; mēd gains the wage/hire sense. The evening-become expression needs separate construction support.'),
 ('EX-IX-29-01','Hęfignessa is accusative plural burdens. Hǣte is the selected dative singular heat after on. The abstract hǣtu/hǣlu discussion must not manufacture plural count uses.'),
 ('EX-IX-29-11','Hǣlu salvation is selected invariant singular; earlier hǣle is a recognized oblique variant. If unnan is used, its grant construction governs genitive of the thing: the possessive must be genitive ðīnre, even though invariant hǣlu looks unchanged.'),
 ('EX-IX-30-01','Use prior setl seat/throne. Preserve the source hint fōtsceamul: complete selected cells retain -sceamul-. Hierusalem is a supplied proper-name form; no full foreign-name declension is inferred.'),
 ('EX-IX-30-02','Hēafod loses unstressed o before endings (hēafd-); hǣr has heavy-neuter zero plural. The final component, not the long first component fōt-, controls retention in fōtsceamul.'),
 ('EX-IX-30-08','The printed word is earth, not oath. There is no source emendation.'),
 ('EX-IX-30-09','Either prior gedeorf labor with an explicitly licensed from relation or the source’s æt ðīnum gewinne frame requires its own final grammar binding. Reader161.5 and note6 directly support æt = from; this is evidence outside the assigned reading span.'),
 ('EX-IX-30-11','Brȳd is feminine; selected accsg brȳde follows Cook51b. Hām here is a noun with accusative object function, distinct from prior adverb hām homewards. Preserve the printed blōstmian hint, matching the selected blossom lemma.'),
 ('EX-X-XI-31-01','Ālīesend is productive as the singular Redeemer title. Its plural morphology is reference only and does not assign a theological plural sense.'),
 ('EX-X-XI-31-08','Dęne and Engle have complete plural-only lexical scope. Lēoðwyrhta is a weak masculine poet; āwęndednes is the -nes translation noun, with doubled ss in inflected forms. Lædene is a supplied dative language name.'),
 ('EX-X-XI-31-11','Bēcrǣding was earlier supplied only; it now has a complete table with productive singular reading and reference-only plurals. The twelve-years-old phrase remains explicitly bounded higher-number syntax.'),
 ('EX-X-XI-31-12','Bōc has bēc in genitive/dative singular and nominative/accusative plural; bōc remains accusative singular. Lēoða is genitive plural poems. Do not make the supplied whichever-of-two clause a blanket productive case-attraction rule.')]
helps=[dict(support_id='U15-COOK-NOM-'+sid.split('-')[-2]+'-'+sid.split('-')[-1],source_item_id=sid,text=t,kind='nominal_orientation',origin_category='new teaching material',evidence_refs=next(x['evidence_refs'] for x in items if x['source_item_id']==sid)) for sid,t in notes]
dump('exercises-dependencies.json',dict(schema_version=1,scope='All50 exact prompts. Nominal source requirements are bounded here; complete verb/adjective/construction requirements and final token bindings are owned by grammar/design and referenced at integration.',count=len(items),items=items))
dump('cook-local-support.json',dict(schema_version=1,nominal_help=helps,grammar_help_owner='sources/audits/unit15-grammar',policy='Nominal notes supplement visible vocabulary and full tables. They do not silently alter an English prompt or authorize unsupported verb systems.'))
print(dict(items=len(items),nominal_requirements=sum(len(x['nominal_requirements']) for x in items),notes=len(helps)))
