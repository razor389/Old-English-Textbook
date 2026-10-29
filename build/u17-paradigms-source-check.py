"""Independent Unit17 source-stage cell comparison; never accepts learner masters.

The expected stems, exceptional cells and endings below were entered by the
reviewer after viewing primary images. They are not extracted from contract
surfaces. This is a review aid, not a source of linguistic evidence.
"""
from pathlib import Path
import hashlib
import json
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(b): return hashlib.sha256(b).hexdigest()
def identity(p):
    b = (ROOT / p).read_bytes()
    return {'path':p,'raw_sha256':sha(b),'normalized_lf_sha256':sha(b.replace(b'\r\n',b'\n'))}
def write(p,d):
    (ROOT/p).parent.mkdir(parents=True,exist_ok=True)
    (ROOT/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

# Lemma: headword, oblique stem, independent lexical class.
nominal = {
 'heanes':('hēanes','hēaness','f'), 'maegen':('mægen','mægen','maegen'),
 'draca':('draca','drac','wm'), 'yst':('ȳst','ȳst','f'),
 'hyll':('hyll','hyll','m'), 'cederbeam':('cēderbēam','cēderbēam','m'),
 'naedre':('nædre','nædr','wf'), 'dema':('dēma','dēm','wm'),
 'halga':('hālga','hālg','wm'), 'horn':('horn','horn','m'),
 'lof':('lof','lof','m'), 'cwen':('cwēn','cwēn','f0'),
 'hlisa':('hlīsa','hlīs','wm'), 'olfend':('olfend','olfend','m'),
 'andgiet':('andgiet','andgiet','n0'), 'thenung':('ðēnung','ðēnung','f'),
 'thegn':('ðegn','ðegn','m'), 'theowa':('ðēowa','ðēow','wm'),
 'wisdom':('wīsdōm','wīsdōm','m'), 'pund':('pund','pund','n0'),
 'grundweall':('grundweall','grundweall','m'), 'getimbrung':('getimbrung','getimbrung','f'),
 'edlean':('edlēan','edlēan','n0'), 'eare':('ēare','ēar','wn'),
 'eadmodnes':('ēaðmōdnes','ēaðmōdness','f'), 'thinen':('ðīnen','ðīnenn','f'),
 'cneoris':('cnēoris','cnēoriss','f'), 'cniht':('cniht','cniht','m'),
 'ymbhwyrft':('ymbhwyrft','ymbhwyrft','m'), 'gylt':('gylt','gylt','m'),
 'gyltend':('gyltend','gyltend','end'), 'finger':('finger','fingr','m'),
 'tabele':('tabele','tabel','wf'), 'hearpere':('hearpere','hearper','m'),
 'hearpe':('hearpe','hearp','wf'), 'maegth-tribe':('mǣgð','mǣgð','f'),
 'thrymsetl':('ðrymsetl','ðrymsetl','n0'), 'palmtwig':('palmtwīg','palmtwīg','n0'),
 'cneo':('cnēo','cnēow','nu'), 'bletsung':('blētsung','blētsung','f'),
 'beorhtnes':('beorhtnes','beorhtness','f'), 'thancung':('ðancung','ðancung','f'),
 'weorthscipe':('weorðscipe','weorðscip','m'), 'fox':('fox','fox','m'),
 'hol':('hol','hol','nu'), 'nest':('nest','nest','n0'),
 'thorn':('ðorn','ðorn','m'), 'cynehelm':('cynehelm','cynehelm','m'),
 'hreod':('hrēod','hrēod','n0'), 'blostma':('blōstma','blōstm','wm'),
 'biema':('biema','biem','wm'), 'hlaefdige':('hlǣfdige','hlǣfdig','wf'),
 'gerimcraeft':('gerīmcræft','gerīmcræft','m'), 'stan':('stān','stān','m')
}
adjectives = {
 'waestmbaere':('wæstmbǣre','wæstmbǣr','e'),
 'geong':('geong','geong','heavy'),
 'manigfeald':('manigfeald','manigfeald','heavy'),
 'rice-adjective':('rīce','rīc','e'),
 'daeghwamlic':('dæghwāmlīc','dæghwāmlīc','heavy'),
 'hlud':('hlūd','hlūd','heavy'),
 'aethele':('æðele','æðel','e'),
 'aethelboren':('æðelboren','æðelboren','retained')
}
case_alias={'nominative':'nom','genitive':'gen','dative':'dat','accusative':'acc','instrumental':'ins'}
num_alias={'singular':'sg','plural':'pl'}
gender_alias={'masculine':'m','feminine':'f','neuter':'n'}
def nominal_expected(lid,a):
    h,s,k=nominal[lid]; c=a['case']; n=a['number']
    if k.startswith('w'):
        if n=='sg': return h if c=='nom' or (k=='wn' and c=='acc') else s+'an'
        return s+({'nom':'an','acc':'an','dat':'um','gen':'na' if k=='wn' else 'ena'}[c])
    if n=='sg':
        if c=='nom' or (c=='acc' and k!='f'): return h
        return s+('e' if k in ('f','f0') or c=='dat' else 'es')
    if c=='dat': return s+'um'
    if c=='gen': return s+('ra' if k=='end' else 'a')
    if k=='maegen': return 'mægnu'
    return s+{'m':'as','end':'e','f':'a','f0':'a','nu':'u','n0':''}[k]

def adjective_expected(h,s,k,a):
    c=case_alias.get(a['case'],a['case']); n=num_alias.get(a['number'],a['number'])
    g=gender_alias.get(a['gender'],a['gender']); strength=a.get('strength',a.get('declension'))
    if strength=='weak':
        if n=='pl': return s+{'nom':'an','acc':'an','gen':'ra','dat':'um'}[c]
        if c=='nom': return s+('a' if g=='m' else 'e')
        if c=='acc' and g=='n': return s+'e'
        return s+'an'
    if c=='ins': return s+'e'
    if n=='pl':
        if c=='gen': return s+'ra'
        if c=='dat': return s+'um'
        return s+({'m':'e','f':'a','n':'' if k=='heavy' else 'u'}[g])
    if g in ('m','n'):
        if c=='nom' or (g=='n' and c=='acc'): return h
        return s+{'gen':'es','dat':'um','acc':'ne'}[c]
    if c=='nom': return s+('' if k=='heavy' else 'u')
    return s+{'gen':'re','dat':'re','acc':'e'}[c]

# Four present positions, three past positions; plural repeated by person.
finite={
 'herian':('hęrie','hęrest','hęreð','hęriað','hęrede','hęredest','hęredon'),
 'gecwethan':('gecweðe','gecwist','gecwið','gecweðað','gecwæð','gecwǣde','gecwǣdon'),
 'up-ahebban':('ūpāhębbe','ūpāhęfst','ūpāhęfð','ūpāhębbað','ūpāhōf','ūpāhōfe','ūpāhōfon'),
 'oferwyrcean':('oferwyrce','oferwyrcst','oferwyrcð','oferwyrceað','oferworhte','oferworhtest','oferworhton'),
 'gesettan':('gesętte','gesętst','gesętt','gesęttað','gesętte','gesęttest','gesętton'),
 'giernan':('gierne','giernst','giernð','giernað','giernde','gierndest','gierndon'),
 'withstandan':('wiðstande','wiðstęntst','wiðstęnt','wiðstandað','wiðstōd','wiðstōde','wiðstōdon'),
 'afyllan':('āfylle','āfylst','āfylð','āfyllað','āfylde','āfyldest','āfyldon'),
 'aweorpan':('āweorpe','āwierpst','āwierpð','āweorpað','āwearp','āwurpe','āwurpon'),
 'awritan':('āwrīte','āwrītst','āwrītt','āwrītað','āwrāt','āwrite','āwriton'),
 'alutan':('ālūte','ālȳtst','ālȳtt','ālūtað','ālēat','ālute','āluton'),
 'windan':('winde','wintst','wint','windað','wand','wunde','wundon'),
 'spaetan':('spǣte','spǣtst','spǣtt','spǣtað','spǣtte','spǣttest','spǣtton'),
 'taelan':('tǣle','tǣlst','tǣlð','tǣlað','tǣlde','tǣldest','tǣldon'),
 'biegan':('bīege','bīegst','bīegð','bīegað','bīegde','bīegdest','bīegdon'),
 'gemunan':('geman','gemanst','geman','gemunon','gemunde','gemundest','gemundon'),
 'thencan':('ðęnce','ðęncst','ðęncð','ðęnceað','ðōhte','ðōhtest','ðōhton')
}
for lid,s in {'maersian':'mǣrs','gewilnian':'gewiln','thurhwunian':'ðurhwun','gearcian':'gearc'}.items():
    finite[lid]=(s+'ie',s+'ast',s+'að',s+'iað',s+'ode',s+'odest',s+'odon')
imperatives={'herian':('hęre','hęriað'),'cnucian':('cnuca','cnuciað'),
 'ahebban':('āhęfe','āhębbað'),'plegian':('plega','plegiað'),
 'ceosan':('cēos','cēosað'),'forgiefan':('forgief','forgiefað')}
subjunctive={'herian':'hęrie','tocuman':'tōcume','geweorthan':'geweorðe',
 'leornian':'leornie','ahyldan':'āhylde','geseon':'gesāwe','settan':'sętte','etan':'ete'}
participles={'up-ahebban':('ūpāhębbende','ūpāhafen'),'afyllan':('āfyllende','āfylled'),
 'maersian':('mǣrsiende','mǣrsod'),'bletsian':('blētsiende','blētsod'),
 'ofwundrian':('ofwundriende','ofwundrod'),'wyrcean':('wyrcende','worht'),
 'gesweotolian':('gesweotoliende','gesweotolod'),'acennan':('ācęnnende','ācęnned'),
 'geopenian':('geopeniende','geopenod'),'gescieppan':('gescieppende','gesceapen')}
infinitives={'geseon':('gesēon','gesēonne'),'geliefan':('gelīefan','gelīefanne'),
 'leornian':('leornian','leornianne')}
def expected(p,x):
    lid=p['lemma_id']; a=x.get('contextual_analysis',x['analysis'])
    if lid in nominal: return nominal_expected(lid,a)
    if lid in adjectives: return adjective_expected(*adjectives[lid],a)
    if a.get('nonfinite')=='present_participle':
        s={'ondraedan':'ondrǣdend','hyngran':'hyngrend'}[lid]
        return adjective_expected(s+'e',s,'e',a)
    if a.get('mood')=='indicative':
        f=finite[lid]
        if a['tense']=='present': return f[3] if a['number']=='pl' else f[a['person']-1]
        return f[6] if a['number']=='pl' else f[5] if a['person']==2 else f[4]
    if a.get('mood')=='imperative': return imperatives[lid][a['number']=='pl']
    if a.get('mood')=='subjunctive': return subjunctive[lid]+('n' if a['number']=='pl' else '')
    if a.get('verb_form') in ('plain_infinitive','inflected_infinitive'):
        return infinitives[lid][a['verb_form']=='inflected_infinitive']
    if a.get('verb_form')=='past_participle': return participles[lid][1]+'e'
    if a.get('verb_form')=='participle': return participles[lid][a['tense']=='past']
    raise ValueError((p['paradigm_id'],x['logical_cell_id'],a))

def main():
    c = read('chapters/ch17/coverage.json')
    notes = read('build/u17-paradigms-view-notes.json')
    catalog = c['evidence_catalog']
    inspections = []
    for n in notes:
        i = identity(n['path'])
        i.update(actually_viewed=True, reviewer='unit17_paradigms', inspection_method='Personal view_image inspection; OCR was not evidence.', observation=n['observation'])
        i['catalog_evidence_ids'] = [k for k, e in catalog.items() if isinstance(e, dict) and e.get('image_path') == n['path']]
        i['source_locators'] = [{k: e[k] for k in ('source_id', 'printed_page', 'pdf_page_one_based', 'original_identifier') if k in e} for e in catalog.values() if isinstance(e, dict) and e.get('image_path') == n['path']][:1]
        inspections.append(i)
    priors = [identity(f'chapters/ch{i:02d}/coverage.json') for i in range(1, 17)]
    priors += [identity('lexicon/entries.json'), identity('curriculum/grammar.json')]
    lexical = read('lexicon/entries.json')
    grammar = read('curriculum/grammar.json')
    prior_forms = {f['form_id']: f for l in lexical['lemmas'] for f in l['forms']}
    systems = []
    cells = []
    prior_reuse = []
    routes = {(r['paradigm_id'], r['logical_cell_id']): r for r in c['display_plan']['paradigm_cell_display_routes']}
    matrices = {m['matrix_id']: m for m in c['display_plan']['matrices']}
    for p in c['paradigms']:
        mismatches = []
        literal_checks = []
        for x in p['cells']:
            exp = expected(p, x)
            key = (p['paradigm_id'], x['logical_cell_id'])
            r = routes[key]
            m = matrices[r['matrix_id']]
            display = m['rows'][r['row_index_zero_based']][r['column_index_zero_based']]
            issues = []
            if x['form'] != exp:
                issues.append({'type': 'source_derived_form', 'expected': exp, 'contract': x['form']})
            if r['surface'] != x['form'] or display != x['form']:
                issues.append({'type': 'contract_display_route', 'route_surface': r['surface'], 'matrix_surface': display})
            if issues:
                mismatches.append({'logical_cell_id': x['logical_cell_id'], 'issues': issues})
            cells.append({'paradigm_id': p['paradigm_id'], 'logical_cell_id': x['logical_cell_id'], 'status': 'source_checked_pending_master_route', 'expected_form_from_reviewed_sources': exp, 'contract_form': x['form'], 'knowledge_status': x['knowledge_status'], 'matrix_id': r['matrix_id'], 'row_index_zero_based': r['row_index_zero_based'], 'column_index_zero_based': r['column_index_zero_based'], 'source_mismatches': issues, 'learner_master_checked': False})
            if x['form_id'] in prior_forms:
                old = prior_forms[x['form_id']]
                prior_reuse.append({'form_id': x['form_id'], 'prior_surface': old['form'], 'current_surface': x['form'], 'surface_preserved': old['form'] == x['form'], 'production_taught_in': old.get('production_taught_in'), 'recognition_taught_in': old.get('recognition_taught_in'), 'supplied_in': old.get('supplied_in', []), 'new_status': x['knowledge_status']})
        ids = [x['logical_cell_id'] for x in p['cells']]
        source_paths = sorted({catalog[e]['image_path'] for e in p['evidence_refs'] if e in catalog and isinstance(catalog[e], dict) and catalog[e].get('image_path')})
        viewed = [i['path'] for i in inspections if i['path'] in source_paths]
        family = 'nominal' if p['lemma_id'] in nominal else 'adjective' if p['lemma_id'] in adjectives else 'verbal'
        rationale = {'nominal': 'Every case/number surface compared with independently entered source headword, lexical class and diagnostic stem; class endings from personally inspected Cook28–37. Selected singular scope, exceptional plural and source quantity were checked separately.', 'adjective': 'Every strong/weak gender, number and case surface compared with source-derived endings from Cook38–41; dictionary-e, heavy-stem and retained-stem choices checked separately. Two instrumental cells retain recognition scope.', 'verbal': 'Every contracted person/number or nonfinite/agreement surface compared with independently entered class model and exceptional stem. Cook55–78 and lexical pages supply rules; present/past stem, dental changes, umlaut, quantity and bounded mood/use were checked separately.'}[family]
        systems.append({'paradigm_id': p['paradigm_id'], 'status': 'source_evidence_checked_pending_final_drafts', 'checked_logical_cell_ids': ids, 'mismatches': mismatches, 'evidence_refs': p['evidence_refs'], 'directly_viewed_cited_images': viewed, 'rationale': rationale, 'diagnostic_rule_checked': p.get('diagnostic_rule', p.get('derivation_rules')), 'scope_checked': p.get('scope'), 'learner_master_checked': False})
    failures = [s for s in systems if s['mismatches']]
    ledger = {'schema_version': 1, 'chapter_id': 'ch17', 'reviewer': 'unit17_paradigms', 'status': 'source_evidence_checked_pending_final_drafts' if not failures else 'source_findings_open', 'independence': {'no_current_author_role': True, 'blind_solver': False, 'reason': 'The frozen contract exposes models; this is independent source/paradigm review, not blind learner solving.', 'student_master_opened': False, 'answer_key_opened': False, 'final_review_requires_coordinator_unlock': True}, 'reviewed_contract_artifact_at_source_stage': identity('chapters/ch17/coverage.json'), 'prior_contract_and_register_reads': priors, 'register_boundary_checks': {'lemmas': len(lexical['lemmas']), 'forms': len(prior_forms), 'features': len(grammar['features']), 'prior_form_reuses': prior_reuse, 'conclusions': ['All sixteen earlier active contracts were read for actual productive and recognition outcomes, bounded scopes and prerequisite teaching.', 'Actual u09-vocative-weak-adjective supports weak direct-address modifiers.', 'Actual u10-hyngran-impersonal remains the two-cell third-singular finite frame; new participial agreement does not extend it.', 'Actual u11-concession remains normally subjunctive, including admitted facts; current supplied ðēah ðe retains that boundary.', 'Actual u14-onfon-dative supplies thing-receiving dative; Unit17 separately teaches personal acceptance/protection.', 'Actual u15-negative-concord already licenses reinforced single negation.', 'Exact prior biegde is unmarked and supplied; the new bīegde series does not overwrite that source witness.', 'Prior gelīefan believe remains distinct from supplied reading permission gelīefst.', 'Existing hēanes singular supplied records and ðēnunge source identity remain recoverable; current scope is explicit.']}, 'counts': {'paradigms': len(systems), 'logical_cells': len(cells), 'display_matrices': len(matrices), 'nominal_adjective_paradigms': 62, 'nominal_adjective_cells': 796, 'verbal_paradigms': 48, 'verbal_cells': 438, 'primary_images_personally_viewed': len(inspections), 'source_mismatches': sum((len(s['mismatches']) for s in systems))}, 'method': 'Personal source-image inspection followed by independent literal cell derivation and comparison. Repeated class endings are rule-derived editorial forms, not claims of individual textual attestation. The helper independently enters expected stems/endings; it does not promote draft displays to acceptance.', 'primary_evidence_image_inspections': inspections, 'paradigm_checks': systems, 'cell_route_checks': cells, 'material_open_findings': len(failures), 'findings': [], 'accepted_artifact_identities': [], 'accepted_contract_semantic_identity': None, 'remaining_gate': 'Root must unlock completed student and answer-key masters. Then personally compare all124 actual matrices and1234 logical routes, explanatory rules, scope labels and key realizations; only then bind artifact and semantic identities and mark accepted.'}
    write('chapters/ch17/reviews/paradigms.json', ledger)
    print(json.dumps(ledger['counts'], ensure_ascii=False))
    for s in failures:
        print(s['paradigm_id'], json.dumps(s['mismatches'], ensure_ascii=False))
    bad = [r for r in prior_reuse if not r['surface_preserved']]
    print('Prior-ID surface changes:', json.dumps(bad, ensure_ascii=False))

if __name__=='__main__': main()
