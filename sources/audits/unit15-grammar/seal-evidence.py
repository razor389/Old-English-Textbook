"""Evidence catalogue: only page images actually viewed by this grammar auditor."""
import json,pathlib,hashlib,re
R=pathlib.Path(__file__).resolve().parents[3];O=pathlib.Path(__file__).resolve().parent
def load(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def write(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
names=['grammar-records-core.json','grammar-records-families.json','grammar-records-lexical.json','source-support.json','principal-parts.json','pronoun-dispositions.json','lexical-frames.json']
refs=set()
def walk(x):
 if isinstance(x,dict):
  refs.update(x.get('evidence_refs',[]))
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
for n in names:walk(load('sources/audits/unit15-grammar/'+n))
viewed={22,23,39,40,41,43,44,45,46,47,48,52,53,54,55,56,61,62,63,64,65,67,68,69,72,73,74,78,79,80,90,91,94,97,100,101,102,103,104,156,157,159,161,162,163,275,281,282,283,288,292,293,297,298,299,301,302,304,305,306,307,308,314,316,317,318,319,320,321,323,324}
fbpaths={52:'sources/audits/unit14-grammar/fb-p52.png',53:'sources/audits/unit06-grammar/cook-p53-pdf69.png',65:'sources/audits/unit14-grammar/fb-p65.png',78:'sources/audits/unit14-grammar/fb-p78.png',79:'sources/audits/unit14-grammar/fb-p79.png',100:'sources/audits/unit14-grammar/fb-p100.png',156:'sources/audits/unit14-grammar/fb-p156.png',157:'sources/audits/unit14-grammar/fb-p157.png',159:'sources/audits/unit15-source/reader-001.png',161:'sources/audits/unit15-source/reader-003.png',162:'sources/audits/unit15-source/reader-004.png',163:'sources/audits/unit15-source/reader-005.png'}
loc={23:'§29, loss of h after ne',39:'§57.3 and §58, adjective stem/ending rules',40:'§58.2 and §59, long/double-consonant and e-adjectives',41:'§60 weak adjective table and §61 participles',43:'§§65–69 comparison, hēahra/hēahsta note',46:'§78 numeral/ordinal list',48:'§§79–81; numeral government and ordinal declension',52:'§§88–89a,b interrogative and indefinite families',53:'§89c–e indefinite hwā, free-choice swā and impersonal man',54:'§§90–94 principal stems and their distribution',55:'§95 strong conjugation table',61:'§104 classIII stem series',62:'§104 classIII umlaut and consonantal adjustments',63:'§106 classV stem series',64:'§106 gietan and present t-stem forms',65:'§107 classVI standan, slēan, swęrian',67:'§110 classVII; §111 weakI',68:'§113 weakI',69:'§114 weakI stem exceptions',72:'§117 selected weakI complete table',73:'§§118–119 weakII present systems',74:'§119 weakII past; §121 habban/nabban',78:'§138 present copula and nis',79:'§138 past negative copula; §139 willan negatives',90:'§154 partitive genitive and §155 age/quality definition',91:'§§155–156 genitive with adjectives/verbs',94:'§§163–164 equality, recipients and receive',97:'§§172–174 preposition cases and object predicates',100:'§§181–184 substantive adjectives and negative concord',101:'§§186–188 passive and tense',102:'§§189–191 agreement, impersonals, indicative',103:'§§192–194 subjunctive, independent wishes',104:'§§194–196 subordinate and adverbial subjunctive',156:'Dangers first paragraph and note3, swā comparatives = the… the',157:'Dangers continuation, proportional/contextual examples',159:'Duties first complete argument/paragraph, including mid hundtēontigum and forgieldan',161:'Duties continuation, lines4–6 æt þīnum gewinne…mæge; lines15–16 forbærnð',162:'Complete Alfred Preface, paired ǣgðer ge…ge and exact Lædene',163:'Complete Alfred Prayer; not an exercise-model source',275:'s.v. ālīesan; ān indefinite; āht',281:'s.v. cleopian',282:'s.v. dēman (113), doom/condemn',288:'s.v. forgieldan and forlǣtan',292:'s.v. gehātan and related vocabulary',293:'s.v. gelīc, gelīce',297:'s.v. hātan, explicit hātte is/was called',301:'s.v. īdel, lǣran, Lǣden',304:'s.v. mǣre, man, mā/māra',305:'s.v. micel, mihtig',314:'s.v. swā and eall swā; swā-hwæðer/swā-hwæt/swā-swā',316:'s.v. tōweorpan',317:'s.v. ðǣr-tō-ēacan',318:'s.v. ðurh',320:'s.v. ūt',321:'s.v. wēnan',323:'s.v. wið, in return for',324:'s.v. wyrcean, yfel adjective and separate noun§47, ymb(e)'}
registry=load('sources/registry.json');sources={s['source_id']:s for s in registry['selected_sources']+registry['supporting_sources']}
pdfs={'cook_ex_1895':'sources/cache/cook_ex_1895.pdf','cook_fb_1895_2':'sources/cache/cook_fb_1895_2.pdf','wright_oe_1914':'sources/cache/wright_oe_1914.pdf'}
def img(path,printed,pdf=None,entry=None):
 q={'image_path':path,'image_sha256':sha(path),'printed_page':printed,'personally_viewed':True,'actual_view_claim':'The grammar auditor opened and visually inspected this exact image in this session; OCR was used only to locate relevant pages.'}
 if pdf:q['pdf_page_one_based']=pdf;q['pdf_index_zero_based']=pdf-1
 if entry:q['entry_or_section']=entry
 return q
records=[];unknown=[]
for rid in sorted(refs):
 if m:=re.fullmatch('U15-G-FB([0-9]+)',rid):
  p=int(m[1])
  if p not in viewed:unknown.append({'id':rid,'reason':'no actual-view record'});continue
  path=fbpaths.get(p,f'sources/audits/unit15-grammar/fb-p{p}.png');sid='cook_fb_1895_2'
  ims=[img(path,p,p+16,loc.get(p,'personally inspected printed page'))]
 elif m:=re.fullmatch('U15-G-EX([0-9]+)',rid):
  p=int(m[1]);sid='cook_ex_1895'
  if p==17:path='sources/audits/unit15-coordinator/cook-ex17-600.png'
  elif p in [15,16,18]:path=f'sources/audits/course-map/ex-page{p}.png'
  elif p in [46,57,66]:path=f'sources/audits/unit15-grammar/ex-p{p}.png'
  else:unknown.append({'id':rid,'reason':'no actual-view record'});continue
  ims=[img(path,p,p+8,'IX.28–30 and joint X,XI.31' if p<19 else 'English–Old English glossary; cited headword')]
 elif rid in ['U15-G-W239','U15-G-W240']:
  p=int(rid[-3:]);sid='wright_oe_1914';ims=[img(f'sources/audits/unit08-grammar/wright_oe_1914-p{p}.png',p,p+20,'§§470–471 interrogatives and indefinites')]
 elif rid.startswith('U15-G-BT-'):
  sid='bosworth_toller_1898_1921'
  d={'U15-G-BT-GELIC':[('bt_d0357.jpg',357,'Supplement s.v. gelīc IV(1): make them equal to us, Mt20.12')],'U15-G-BT-MICEL':[('bt_b0682.jpg',682,'Main s.v. micel begins columnb'),('bt_b0683.jpg',683,'Main s.v. micel IV(a,b), substantive neuter amount, with/without genitive, columna')],'U15-G-BT-ONFON':[('bt_b0750.jpg',750,'Main s.v. on-fōn, heading gen/dat/acc and II(a), Mt20.10 syndrige penegas, columnb')],'U15-G-BT-SWITHE':[('bt_b0959.jpg',959,'Main s.v. swīðe begins columnb'),('bt_b0960.jpg',960,'Main s.v. swīðe continuation and degree uses, columna'),('bt_d0718.jpg',718,'Supplement s.v. swīðe IV, comparative preference rather, columnb')]}.get(rid)
  if d is None:unknown.append({'id':rid,'reason':'unknown BT reference'});continue
  ims=[img('sources/audits/unit15-grammar/'+n,p,entry=e) for n,p,e in d]
 else:unknown.append({'id':rid,'reason':'unmapped evidence id'});continue
 source=sources[sid]
 q={'evidence_id':rid,'source_id':sid,'selected_edition':source.get('edition') or ('Main1898; Supplement1921' if sid.startswith('bosworth') else '1895 selected scan'),'title':source['title'],'origin_category':'exact source evidence; generated cells and Cook answers separately declared new teaching material','images':ims,'verification_scope':'Supports only the stated rule/entry/construction. Derived paradigm cells are not claimed separately attested.'}
 if sid in pdfs:q['pdf_path']=pdfs[sid];q['pdf_sha256']=sha(pdfs[sid]);q['page_convention']='One-based PDF page equals printed page + '+str({'cook_ex_1895':8,'cook_fb_1895_2':16,'wright_oe_1914':20}[sid])+'.'
 else:q['image_origin']='https://bosworthtoller.com/images-dictionary/';q['page_convention']='Original printed dictionary page; b=1898 main, d=1921 supplement. Entry locator replaces a PDF page.'
 records.append(q)
write('evidence-catalog.json',{'schema_version':1,'chapter':'ch15','auditor':'unit15_grammar','records':records,'unknown_references':unknown,'no_unviewed_acceptance_claim':'Downloaded but uninspected pages, optional cancelled downloads, and OCR transcriptions are excluded from positive image-view claims.'})
print('Evidence:',len(records),'records;',len(unknown),'unresolved refs',unknown)
