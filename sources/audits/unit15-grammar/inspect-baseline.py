import hashlib, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = pathlib.Path(__file__).resolve().parent

def read(path):
    b=(ROOT/path).read_bytes()
    return json.loads(b.decode('utf-8-sig')), hashlib.sha256(b).hexdigest()

def compact_record(x):
    keys=('feature_id','form_id','sense_id','form','gloss','description','analysis','recognition_taught_in','production_taught_in','supplied_in','knowledge_status','scope_note','scope','evidence_refs')
    return {k:x[k] for k in keys if k in x}

contracts=[]
for i in range(1,15):
    path=f'chapters/ch{i:02}/coverage.json'
    x,h=read(path)
    contracts.append({'path':path,'sha256':h,'parsed_entire_document':True,'chapter_id':x['chapter_id'],'status':x['status'],'productive_outcomes':x['productive_outcomes'],'recognition_outcomes':x['recognition_outcomes'],'bounded_scope':x['bounded_scope'],'teaching_record_count':len(x['teaching_records']),'paradigm_count':len(x['paradigms']),'assigned_item_count':len(x['assigned_items'])})
l,lh=read('lexicon/entries.json')
g,gh=read('curriculum/grammar.json')
r,rh=read('sources/registry.json')
keywords=re.compile(r'negat|compar|quant|indefin|distribut|partitiv|proport|except|concess|relative|correlat|gehw|ǣg|ǣnig|ān |nān|āwiht|nāwiht|nāht|nōht|seld|swið|mann|man impers|swā',re.I)
features=[compact_record(x) for x in g['features'] if keywords.search(json.dumps(x,ensure_ascii=False))]
summary={'baseline_revision':'9129cda','contracts':contracts,'registers':{'lexicon':{'path':'lexicon/entries.json','sha256':lh,'lemmas':len(l['lemmas']),'forms':sum(len(x['forms']) for x in l['lemmas']),'senses':sum(len(x['senses']) for x in l['lemmas'])},'grammar':{'path':'curriculum/grammar.json','sha256':gh,'features':len(g['features'])}},'registry_sha256':rh,'selected_editions':[{k:x[k] for k in ('source_id','author','authors','title','edition','publication_year','archive_identifier','pdf_url') if k in x} for x in r['selected_sources']+r['supporting_sources']],'relevant_features':features,'interpretation':'Whole current files are parsed; the topical extraction supports human review of relevant scope. Prior supplied exposure is never treated as prior teaching.'}
(OUT/'prior-scope-audit.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('CONTRACTS')
for x in contracts:
    print(x['chapter_id'],'assigned',x['assigned_item_count'],'paradigms',x['paradigm_count'])
    print('PRODUCTIVE',json.dumps(x['productive_outcomes'],ensure_ascii=False))
    print('BOUNDARY',json.dumps(x['bounded_scope'],ensure_ascii=False))
print('REGISTERS',summary['registers'])
print('FEATURES')
for x in features:
    print(x['feature_id'], '|',x.get('description'),'| P',x.get('production_taught_in'),'R',x.get('recognition_taught_in'),'|',x.get('scope_note',''))
