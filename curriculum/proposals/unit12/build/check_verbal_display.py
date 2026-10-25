"""Independent expected systems checked against literal display coordinates."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[4];OUT=ROOT/'curriculum/proposals/unit12'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
g=load('sources/audits/unit12-grammar/grammar-records.json');d=load('curriculum/proposals/unit12/display-matrices.json')
pars={p['paradigm_id']:p for p in g['paradigms']};matrices={m['matrix_id']:m for m in d['matrices']}
forms={f['form_id']:f for l in g['lemmas'] for f in l.get('forms',[])}
routes={(r['paradigm_id'],r['form_id']):r for r in d['paradigm_cell_display_routes'] if r.get('grammar_display')}
# These expected strings were separately checked against the actual primary
# morphology pages, not extracted from the generated matrix cells.
indicatives={
'adrifan':'ādrīfe ādrīfst ādrīfð ādrīfað ādrīfað ādrīfað ādrāf ādrife ādrāf ādrifon ādrifon ādrifon',
'gehatan':'gehāte gehǣtst gehǣtt gehātað gehātað gehātað gehēt gehēte gehēt gehēton gehēton gehēton',
'fleon':'flēo flīehst flīehð flēoð flēoð flēoð flēah fluge flēah flugon flugon flugon',
'gemetan':'gemēte gemētst gemētt gemētað gemētað gemētað gemētte gemēttest gemētte gemētton gemētton gemētton',
'geopenian':'geopenie geopenast geopenað geopeniað geopeniað geopeniað geopenode geopenodest geopenode geopenodon geopenodon geopenodon',
'gretan':'grēte grētst grētt grētað grētað grētað grētte grēttest grētte grētton grētton grētton',
'cythan':'cȳðe cȳst cȳð cȳðað cȳðað cȳðað cȳðde cȳðdest cȳðde cȳðdon cȳðdon cȳðdon',
'ehtan':'ēhte ēhtst ēht ēhtað ēhtað ēhtað ēhte ēhtest ēhte ēhton ēhton ēhton',
'agan':'āh āhst āh āgon āgon āgon āhte āhtest āhte āhton āhton āhton',
'leornian':'leornie leornast leornað leorniað leorniað leorniað leornode leornodest leornode leornodon leornodon leornodon'}
commands={'sendan':'sęnd sęndað','bringan':'bring bringað','adrifan':'ādrīf ādrīfað','fleon':'flēoh flēoð','gemetan':'gemēt gemētað','geopenian':'geopena geopeniað','weorpan':'weorp weorpað','leornian':'leorna leorniað','risan':'rīs rīsað'}
participles={'gewyrcean':'gewyrcende geworht','gierwan':'gierwende gierwed','settan':'sęttende sętt','gewitan':'gewītende gewiten','sittan':'sittende seten'}
infinitives={'adrifan':'ādrīfan ādrīfanne','geneosian':'genēosian genēosianne'}
expected={**{'NEW-U12-PAR-'+k+'-IND':v.split() for k,v in indicatives.items()},**{'NEW-U12-PAR-'+k+'-IMP':v.split() for k,v in commands.items()},**{'NEW-U12-PAR-'+k+'-PART':v.split() for k,v in participles.items()},**{'NEW-U12-PAR-'+k+'-INF':v.split() for k,v in infinitives.items()}}
errors=[];cells=[]
if set(expected)!=set(pars):errors.append({'system_set_mismatch':{'missing':sorted(set(pars)-set(expected)),'extra':sorted(set(expected)-set(pars))}})
def analysis(c):return {**forms[c['form_id']].get('analysis',{}),**c.get('analysis',{}),**{k:c[k] for k in ['tense','mood','person','number'] if k in c}}
for pid,values in expected.items():
 p=pars[pid];m=matrices[pid]
 if pid.endswith('-IND'):
  ordered=[]
  for tense in ['present','preterite']:
   for number in ['sg','pl']:
    for person in [1,2,3]:
     hits=[c for c in p['cells'] if all(analysis(c).get(k)==v for k,v in {'tense':tense,'number':number,'person':person,'mood':'indicative'}.items())]
     assert len(hits)==1,(pid,tense,number,person);ordered+=hits
 else:ordered=p['cells']
 if len(ordered)!=len(values):errors.append({'cell_count':pid});continue
 for c,wanted in zip(ordered,values):
  route=routes[(pid,c['form_id'])];ri=route['row_index_zero_based'];ci=route['column_index_zero_based'];actual=m['rows'][ri][ci]
  result={'paradigm_id':pid,'form_id':c['form_id'],'analysis':analysis(c),'expected_surface':wanted,'proposal_surface':c['form'],'display_surface':actual,'matrix_id':route['matrix_id'],'row_index_zero_based':ri,'column_index_zero_based':ci,'row_label':route['row_label'],'column_label':route['column_label'],'knowledge_status':c['knowledge_status'],'surface_match':wanted==c['form']==actual,'caption':m['title']}
  if not result['surface_match']:errors.append({'surface_mismatch':result})
  if c['form_id'] not in m['cell_form_ids'][ri][ci]:errors.append({'coordinate_identity_mismatch':result})
  if pid.endswith('-IND'):
   a=analysis(c);expected_row=(0 if a['number']=='sg' else 3)+a['person']-1;expected_col=1 if a['tense']=='present' else 2
   if (ri,ci)!=(expected_row,expected_col):errors.append({'indicative_coordinate_role_mismatch':result})
  cells.append(result)
data={'schema_version':1,'chapter':'ch12','reviewer':'unit12_design','status':'checked' if not errors else 'errors','method':'A separately specified expected surface list for every defined system is checked against the source proposal and its actual visible table coordinate. Primary grammar pages were directly viewed before certifying the expected forms; the source crosscheck records those views individually.','counts':{'systems':len(expected),'indicative_systems':len(indicatives),'command_pairs':len(commands),'participle_pairs':len(participles),'infinitive_pairs':len(infinitives),'checked_cells':len(cells),'literal_cells':len(cells),'construction_positions_excluded':12},'primary_rule_findings':['Cook54§93 assigns strong second-singular preterite to the plural stem; ādrife and fluge therefore do not acquire the first/third-singular long vowel.','Cook58–61 explicitly places flēon in the contracted classII pattern; the contracted present and flīehst/flīehð coexist with flēah/fluge/flugon.','Cook59 makes the contracted classII command long-vowel flēoh, while the inherited slēan command has short-vowel sleah.','Cook67§110 supplies the gehātan-family ē preterite; the ordinary indicative endings and dental present changes supply its twelve selected positions.','Cook68–72 gives the weakI dental patterns, including mētte and ēhte, and the selected gierwed/sętt bases; Cook70 supplies irregular geworht.','Cook24–25 and directly inspected Wright248§476 support selected cȳst/cȳð and checked dental coalescence rather than an arbitrary uniform present suffix.','Cook73–74 supplies the complete weakII present/preterite and command patterns used for geopenian/leornian; the plain and inflected infinitives remain separate precisely bounded systems.','Cook77§127 directly gives āh/āhst/āgon and āhte; twelve indicative positions do not assign its other printed systems.','Every table has a visible lexical caption naming strong, weak, mixed or preterite-present status and the exact system. Recognition participles remain recognition.','The twelve habban clause positions bind existing auxiliaries and are excluded from the152 inflectional cells.'],'image_record':'curriculum/proposals/unit12/source-crosscheck.json','limits':'This is a complete coordinate/surface and morphological-rule crosscheck, not a claim that every derived inflection is separately attested on a page. Dictionary sense/argument frames, reading interpretation, all graded solutions, and final rendered pages require their separate audits/review. The reserved solver has not read private models.','cells':cells,'errors':errors}
(OUT/'verb-display-crosscheck.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'counts':data['counts'],'errors':errors},ensure_ascii=False))
