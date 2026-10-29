"""Read every active prerequisite contract and the actual teaching registers."""
import hashlib,json,pathlib,subprocess
ROOT=pathlib.Path(__file__).resolve().parents[3]
OUT=pathlib.Path(__file__).parent
def read(p):
    return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p):
    return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
contracts=[]
for n in range(1,15):
    p=f'chapters/ch{n:02}/coverage.json'; c=read(p)
    contracts.append({'path':p,'sha256':sha(p),'title':c.get('title'),'status':c.get('status'),'keys':list(c),'assigned_count':len(c.get('assigned_items',[])),'bounded_scope':c.get('bounded_scope',[]),'productive_outcomes':c.get('productive_outcomes',[]),'recognition_outcomes':c.get('recognition_outcomes',[])})
lex=read('lexicon/entries.json'); grammar=read('curriculum/grammar.json'); registry=read('sources/registry.json')
rec={'baseline':'9129cda','method':'All fourteen JSON contracts and both cumulative registers parsed in full; actual individual form/sense/feature milestones determine prior status.','contracts':contracts,'registers':[{'path':p,'sha256':sha(p)} for p in ['lexicon/entries.json','curriculum/grammar.json']],'counts':{'lemmas':len(lex['lemmas']),'forms':sum(len(l.get('forms',[])) for l in lex['lemmas']),'senses':sum(len(l.get('senses',[])) for l in lex['lemmas']),'features':len(grammar['features'])},'negative_indefinite_features':[f for f in grammar['features'] if any(k in json.dumps(f,ensure_ascii=False).lower() for k in ['negativ','indefinit','proportion','distribut'])],'source_caches':registry['local_cache']}
(OUT/'prior-scope-audit.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'counts':rec['counts'],'contracts':[{'path':x['path'],'title':x['title'],'assigned':x['assigned_count']} for x in contracts],'prior_features':[(x['feature_id'],x.get('production_taught_in'),x.get('recognition_taught_in'),x.get('description')) for x in rec['negative_indefinite_features']]},ensure_ascii=False,indent=2))
GS=pathlib.Path('C:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs')
subprocess.run([str(GS/'bin/gswin64c.exe'),'-I'+';'.join(str(GS/d) for d in ('Resource/Init','lib','kanji')),'-q','-sDEVICE=png16m','-r170','-dFirstPage=175','-dLastPage=179','-dBATCH','-dNOPAUSE',f'-sOutputFile={OUT.as_posix()}/reader-%03d.png',str(ROOT/'sources/cache/cook_fb_1895_2.pdf')],check=True)
