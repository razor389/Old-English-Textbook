import json,re
from pathlib import Path
P=Path(__file__).resolve().parent;d=json.loads((P/'candidate-models.json').read_text(encoding='utf8'));log=[]
changes={
'37-09':[('wæstmbǣru','wæstmbǣran','Weak qualifying adjective in praise-address construction, Cook55 and prior u09-vocative-weak-adjective; strong-u was a real cell but wrong for this selected address.')],
'37-10':[('gefiðrede','gefiðredan','Weak adjective with directly addressed birds; morphology and address selection must be checked separately.')],
'37-12':[('Geonge','Geongan','Weak personal substantive/direct address, Cook55.'),('ealde','ealdan','Weak personal substantive/direct address, Cook55.')],
'42-02':[('nīwe lēoð','nīwne sang','Use prior productive song sense sang; nīwne is locally supplied adjective agreeing with masculine accusative song.'),('ðæt lēoð','ðone sang','Masculine accusative anaphoric object song; do not reuse neuter article after changing noun.'),('būton ðǣm hunde and fēowertig and fēower ðūsendum','būton ðæt hundtēontig and fēowertig and fēower ðūsendo','Coordinator primary BT1082 exact parallel, now personally viewed as well. Preserve entire attested exclusion phrase and ðūsendo; no dative or generalized būton-case claim.')],
'43-15':[('andfęnge','gecwēme','Source editor and personally viewed Ex37 supply acceptable=gecwēme59; use whole local predicate support, not unsupported alternative adjective.')]
}
for r in d['rows']:
 k=r['source_item_id'].removeprefix('EX-XII-XIII-')
 if k not in changes:continue
 old=r['model'];why=[]
 for a,b,w in changes[k]:
  if a not in r['model']:raise ValueError((k,a))
  r['model']=r['model'].replace(a,b);why.append(w)
 r['tokens']=re.findall(r'[A-Za-zĀ-žǢǣȲȳÆæÐðÞþ]+(?:-[A-Za-zĀ-žǢǣȲȳÆæÐðÞþ]+)*',r['model'])
 log.append({'source_item_id':r['source_item_id'],'before':old,'after':r['model'],'reasons':why,'token_count_changed':False})
d['amendment_records'].append('sources/audits/unit17-grammar/model-amendments-09.json')
(P/'candidate-models.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(P/'model-amendments-09.json').write_text(json.dumps({'access':'author-only; exclude from blind reviewers','changes':log},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(len(log))
