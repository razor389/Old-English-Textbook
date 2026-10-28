import json
from pathlib import Path
R=Path.cwd();L=json.loads((R/'lexicon/entries.json').read_text(encoding='utf8'))['lemmas'];want='sendan cuman bycgan secgan willan habban libban andswarian motan magan dur(r)an duran beodan geseon thurf(an) thurfan agiefan aflaeran afaeran afyrht beræafian bereafian theowian incuman c(e)apian ceapian ofthyncan ofthyncean bringan laedan gefyllan settan ascian gemiltsian forleosan lecgean forstelan stelan ofslean diernan erian ripan oncnawan undon gedon hlystan gelaeccan fōn fon naðor nawther naþer'.split()
for x in L:
 if x['lemma_id'] in want or any(z in x['display_headword']for z in ['fǣr','fēred','fyrht','ðync','ðēow']):
  print(x['lemma_id'],x['display_headword'],[(s['sense_id'],s['gloss'],s.get('production_taught_in'))for s in x['senses']])
  for f in x['forms']:
   a=f['analysis'];
   if isinstance(a,dict)and(a.get('person',3)in[1,3])and a.get('number','sg')in['sg','singular']:
    print(' ',f['form_id'],f['form'],a,f.get('production_taught_in'))
print('CANDIDATEIMAGEPATHS')
A=R/'sources/audits';images=[p for p in A.glob('unit*/*.png')if 'ex' in p.name]
for n in [37,38,39,40,41,42,43,44,45,46,47,48,49,50,53,54,59,60,62,63,64,66,67,68,69]:
 matches=[p for p in images if p.name in [f'ex-p{n}.png',f'ex-pdf{n+8}-p{n}.png',f'cook-ex-p{n}.png']]
 print(n, matches[-1].relative_to(R)if matches else 'MISSING')
