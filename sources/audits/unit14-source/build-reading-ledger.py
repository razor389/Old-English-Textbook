import json,re,copy
from pathlib import Path
P=Path(__file__).resolve().parent
ROOT=P.parents[2]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf8'))
def write(name,obj):(P/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
src=read('sources/audits/unit14-source/reading-source.json')
nom=read('sources/audits/unit14-source/source-support-records.json')
gram=read('sources/audits/unit14-grammar/source-support.json')
FORM={};SENSE={};ORIGIN={}
for path in ['lexicon/entries.json','sources/audits/unit14-source/lexical-inventory.json','sources/audits/unit14-source/source-support-records.json','sources/audits/unit14-grammar/grammar-records.json','sources/audits/unit14-grammar/source-support.json']:
 for l in read(path)['lemmas']:
  for kind,dest in [('forms',FORM),('senses',SENSE)]:
   for r in l[kind]:
    rid=r['form_id' if kind=='forms' else 'sense_id'];dest[rid]=(l['lemma_id'],r);ORIGIN[rid]=path
bindings={x['token_index_one_based']:copy.deepcopy(x) for x in gram['reading_bindings']+nom['reading_nominal_bindings']}
manual={
4:('her-invariant','her-1'),5:('on-invariant','on-1'),6:('woruld-dat-sg','woruld-1'),8:('mid-invariant-source','mid-by-means'),13:('se-all-nom-pl','se-the'),16:('micel-comp-nom-f-pl-weak','micel-comp-1'),18:('se-all-nom-pl','se-the'),22:('swa-invariant','swa-1'),23:('ic-nom-pl','ic-personal'),26:('se-n-dat-sg','se-that'),27:('se-all-acc-pl','se-the'),30:('and-invariant','and-1'),32:('se-n-nom-sg','se-the'),34:('thonne-invariant','thonne-then-source'),35:('the-relative-invariant','the-relative-which'),37:('on-invariant','on-1'),38:('se-m-dat-sg','se-the'),40:('thaet-conjunction-invariant','thaet-result'),41:('he-n-nom-sg','he-1'),43:('up-invariant','up-up'),44:('ofer-invariant','ofer-1'),45:('eall-acc-n-pl-strong','eall-all'),46:('se-all-acc-pl','se-the'),47:('other-acc-n-pl-strong','other-other'),48:('treo-acc-pl','treo-1'),49:('and-invariant','and-1'),51:('he-n-acc-sg','he-1'),52:('thonne-conjunction-invariant','thonne-when'),56:('and-invariant','and-1'),57:('se-m-nom-sg','se-the'),59:('wind-nom-sg','wind-1'),60:('thonne-invariant','thonne-then-source'),62:('he-n-nom-sg','he-1'),65:('and-invariant','and-1'),67:('thonne-invariant','thonne-than'),68:('se-m-nom-sg','se-the'),71:('swa-invariant','swa-1'),73:('eac-invariant','eac-also'),76:('se-all-dat-pl','se-the'),78:('and-invariant','and-1'),80:('thonne-conjunction-invariant','thonne-when'),81:('he-nom-pl','he-1'),84:('up-invariant','up-up'),85:('ofer-invariant','ofer-1'),86:('se-f-acc-sg','se-the'),88:('eorthe-acc-sg','eorthe-1'),89:('he-nom-pl','he-1'),90:('thonne-invariant','thonne-then-source'),94:('and-invariant','and-1'),98:('to-preposition-dative-invariant','to-destination'),99:('eorthe-dat-sg','eorthe-1'),100:('swilce-adverb-invariant','swilce-likewise'),101:('eac-invariant','eac-also'),103:('se-all-dat-pl','se-the'),105:('munt-dat-pl','munt-1'),106:('and-invariant','and-1'),111:('ofer-invariant','ofer-1'),112:('eall-acc-m-sg-strong','eall-all'),113:('middangeard-acc-sg','middangeard-1'),117:('se-m-gen-sg','se-the'),119:('thaet-conjunction-invariant','thaet-conjunction-1'),120:('he-nom-pl','he-1'),123:('mid-invariant-source','mid-by-means'),126:('and-invariant','and-1'),128:('and-invariant','and-1'),129:('mid-invariant-source','mid-by-means'),132:('swa-invariant','swa-1'),133:('se-all-nom-pl','se-the'),136:('her-invariant','her-1'),137:('on-invariant','on-1'),138:('woruld-dat-sg','woruld-1'),140:('and-invariant','and-1'),142:('and-invariant','and-1'),146:('and-invariant','and-1'),147:('thes-gen-f-sg','thes-1'),148:('woruld-gen-sg','woruld-1'),153:('and-invariant','and-1'),154:('thes-nom-all-pl','thes-1'),156:('wundor-nom-pl','wundor-1')}
def status(rid,record):
 if ORIGIN[rid]=='lexicon/entries.json':return 'previously_taught' if record.get('production_taught_in') or record.get('recognition_taught_in') else 'supplied'
 return record['knowledge_status']
for i,(fid,sid) in manual.items():
 assert i not in bindings,(i,'duplicate')
 lid,f=FORM[fid];slid,s=SENSE[sid];assert lid==slid,(i,lid,slid)
 bindings[i]={'token_index_one_based':i,'lemma_id':lid,'form_id':fid,'sense_id':sid,'form':f['form'],'form_status':status(fid,f),'sense_status':status(sid,s),'feature_ids':[]}

pieces=[]
for line in src['source_lines']:
 text=re.sub(r'\[[0-9]+[a-z]?\]','',line['source_with_note_markers'])
 for word in text.split():
  if pieces and pieces[-1]['source_surface'].endswith('-'):
   last=pieces[-1];keep='-' if last['source_surface']=='ðā-' else ''
   last['source_surface']=last['source_surface'][:-1]+keep+word
   last['source_line_ids'].append(line['source_line_id'])
  else:pieces.append({'source_surface':word,'source_line_ids':[line['source_line_id']],'printed_page':line['printed_page'],'pdf_page_one_based':line['pdf_page_one_based'],'editorial_line':line['editorial_line']})
assert len(pieces)==src['word_count']==159
assert ' '.join(p['source_surface'] for p in pieces)==src['learner_text']
missing=sorted(set(range(1,160))-set(bindings))
if missing:raise ValueError(('Unbound token indices',missing))
rows=[]
for i,piece in enumerate(pieces,1):
 b=bindings[i];fid=b['form_id'];sid=b['sense_id'];lid,f=FORM[fid];slid,s=SENSE[sid]
 surface=piece['source_surface'].strip('.,;')
 assert surface.lower()==f['form'].lower(),(i,surface,f['form'])
 assert lid==slid==b['lemma_id'],(i,lid,slid,b['lemma_id'])
 b.update(piece);b['token_id']=f'FB-VIII-DANGERS-T{i:03d}';b['analysis']=copy.deepcopy(f.get('contextual_analysis',f['analysis']));b['gloss']=s.get('contextual_gloss',s['gloss']);b['form_record_origin']=ORIGIN[fid];b['sense_record_origin']=ORIGIN[sid];b['evidence_refs']=list(dict.fromkeys(f.get('evidence_refs',[])+s.get('evidence_refs',[])+['U14-SRC-P'+str(piece['printed_page'])]));
 b['prior_form_scope']={k:f.get(k) for k in ['production_taught_in','recognition_taught_in','supplied_in','coverage_contract']} if ORIGIN[fid]=='lexicon/entries.json' else f.get('prior_scope')
 b['prior_sense_scope']={k:s.get(k) for k in ['production_taught_in','recognition_taught_in','supplied_in','coverage_contract']} if ORIGIN[sid]=='lexicon/entries.json' else s.get('prior_scope')
 rows.append(b)
notes={26:'Dative singular referring back to the opening proposition. Be ðǣm is separate from the accusative object ðā bȳsena.',28:'Accusative plural object shared by both coordinated infinitives.',34:'Discourse-resumptive then; local reading help explains the long suspended sentence.',51:'Reflexive accusative hit: the tree spreads itself.',54:'First of two subjects of gestęnt; wind is the second.',58:'Attributive weak adjective after the article, not a new productive paradigm.',69:'The rest of the forest, per Cook156n11.',87:'The rest of the earth. Original157n1 points to156n12; C05 records the mismatch with relevant156n11.',104:'Exact retained-g source spelling; mixed masculine/feminine coordinated heads share plural dative agreement.',117:'Genitive determiner agreeing with ealdordōmes.',119:'Explanatory content: the punishment consists in being struck; frame locally supplied.',134:'High/exalted human power, distinct from merely physical height.',135:'Conclusion applies the natural examples to human power/eminence.',147:'Genitive feminine singular modifying worulde.',148:'Genitive dependent on subject welan.',149:'Nominative plural subject, not an object.',155:'Weak neuter plural agreement with demonstrative + wundor.'}
for i,n in notes.items():rows[i-1]['contextual_note']=n
write('reading-token-ledger.json',{'schema_version':1,'source_span_id':src['source_span_id'],'tokenization':'Whitespace lexical words; punctuation retained in source_surface; line-broken ðā-ðe and geslægene rejoined. Case-only sentence-initial differences are declared typography.','count':len(rows),'tokens':rows,'unresolved':[]})

helps=[]
for l in nom['lemmas']:
 inds=sorted({i for b in nom['reading_nominal_bindings'] if b['lemma_id']==l['lemma_id'] for i in [b['token_index_one_based']]})
 if not inds:continue
 row={'support_id':'U14-READ-LEX-'+l['lemma_id'].upper(),'kind':'lexical_help','lemma_id':l['lemma_id'],'headword':l['display_headword'],'forms':list(dict.fromkeys(rows[i-1]['source_surface'].strip('.,;') for i in inds)),'glosses':list(dict.fromkeys(rows[i-1]['gloss'] for i in inds)),'token_indices':inds,'form_ids':list(dict.fromkeys(rows[i-1]['form_id'] for i in inds)),'sense_ids':list(dict.fromkeys(rows[i-1]['sense_id'] for i in inds)),'scope':'Printed local help; supplied dependency is not assessed for independent recall.'}
 row['text']='; '.join(row['forms'])+' — '+'; '.join(row['glosses'])
 helps.append(row)
write('reading-support.json',{'schema_version':1,'lexical_help':helps,'grammar_help':gram['reading_support'],'source_apparatus':'reading-apparatus.json','policy':'Every supplied reading dependency must be visible through this lexical list or the linked grammar help. The source apparatus is preserved separately and its questions are explained/reference-only.'})
write('reading-constructions.json',{'schema_version':1,'source_span_id':src['source_span_id'],'constructions':gram['reading_support'],'feature_records':gram['features'],'contextual_notes':notes})
print({'tokens':len(rows),'supplied_form_tokens':sum(r['form_status']=='supplied' for r in rows),'supplied_sense_tokens':sum(r['sense_status']=='supplied' for r in rows),'nominal_help_groups':len(helps)})
