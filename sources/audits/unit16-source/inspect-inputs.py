"""Read immutable current teaching inputs; render only the source work assigned here."""
import hashlib, json, pathlib, subprocess
ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = pathlib.Path(__file__).parent
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
contracts=[]
for n in range(1,16):
    p=f'chapters/ch{n:02}/coverage.json'; c=read(p)
    contracts.append({'path':p,'sha256':sha(p),'status':c.get('status'),'title':c.get('title'),'bounded_scope':c.get('bounded_scope'),'productive_outcomes':c.get('productive_outcomes'),'recognition_outcomes':c.get('recognition_outcomes'),'assigned_count':len(c.get('assigned_items',[]))})
lex=read('lexicon/entries.json'); grammar=read('curriculum/grammar.json'); registry=read('sources/registry.json')
record={'baseline':'e1d94be968e89ecfc4918ed58d850702e5d0e57e','method':'All fifteen contracts and both actual cumulative registers parsed in full. Specific prior teaching claims will cite actual form/sense/construction records, not this orientation.','contracts':contracts,'registers':[{'path':p,'sha256':sha(p)} for p in ['lexicon/entries.json','curriculum/grammar.json']],'counts':{'lemmas':len(lex['lemmas']),'forms':sum(len(l.get('forms',[])) for l in lex['lemmas']),'senses':sum(len(l.get('senses',[])) for l in lex['lemmas']),'features':len(grammar['features'])},'source_caches':registry['local_cache']}
(OUT/'prior-scope-audit.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record,ensure_ascii=False,indent=2))
GS=pathlib.Path('C:/Users/Ross/AppData/Local/texlive/2026/tlpkg/tlgs')
def render(pdf,first,last,stem,dpi):
    subprocess.run([str(GS/'bin/gswin64c.exe'),'-I'+';'.join(str(GS/d) for d in ('Resource/Init','lib','kanji')),'-q','-sDEVICE=png16m',f'-r{dpi}',f'-dFirstPage={first}',f'-dLastPage={last}','-dBATCH','-dNOPAUSE',f'-sOutputFile={OUT.as_posix()}/{stem}-%03d.png',str(ROOT/pdf)],check=True)
render('sources/cache/cook_ex_1895.pdf',26,30,'exercise',300)
render('sources/cache/cook_fb_1895_2.pdf',180,190,'reader',200)
