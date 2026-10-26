"""Rebuild the bounded Unit 14 nominal proposals from checked source evidence."""
import copy
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
PRIOR = {x['lemma_id']: x for x in json.loads((ROOT/'lexicon/entries.json').read_text(encoding='utf8'))['lemmas']}

def write(name, value):
    (OUT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf8')

RULES = [
 {'rule_id':'U14-NOM-STRONG-M', 'description':'Complete strong masculine singular/plural: uninflected nominative/accusative singular; -es, -e; plural -as, -a, -um, -as.', 'evidence_refs':['U14-FB-P27','U14-FB-P28']},
 {'rule_id':'U14-NOM-NEUTER-HEAVY', 'description':'Complete strong heavy-stem neuter singular/plural: nominative/accusative singular and plural without ending; -es, -e; plural genitive -a and dative -um. Compounds follow the final nominal component.', 'evidence_refs':['U14-FB-P32','U14-FB-P33']},
 {'rule_id':'U14-NOM-FEMININE', 'description':'Long/heavy feminine model ār: nominative singular uninflected; genitive/dative/accusative -e; plural nominative/accusative/genitive -a, dative -um. The alternate genitive plural -ena is not the selected route.', 'evidence_refs':['U14-FB-P34','U14-FB-P35','U14-FB-P36']},
 {'rule_id':'U14-NOM-NES', 'description':'Feminine -nes doubles s before inflectional endings; the full singular/plural follows the long feminine model.', 'evidence_refs':['U14-FB-P35','U14-FB-P36']},
 {'rule_id':'U14-NOM-WEAK', 'description':'Weak masculine: nominative singular -a; other singular and nominative/accusative plural -an; genitive plural -ena; dative plural -um.', 'evidence_refs':['U14-FB-P37']},
 {'rule_id':'U14-NOM-WEAK-NEUTER', 'description':'Weak neuter ēage has nominative/accusative singular ēage; genitive/dative singular ēagan; nominative/accusative plural ēagan; genitive plural ēagena (also ēagna); dative plural ēagum. Cook §53.2 explicitly gives neuter equality of nominative and accusative.', 'evidence_refs':['U14-FB-P37','U14-LEX-eage']},
 {'rule_id':'U14-NOM-SYNCOPE', 'description':'Wuldor uses the syncopated stem wuldr- before endings, by §§43.4 and 47.6. The selected reference nominative/accusative plural wuldru applies the admitted disyllabic neuter -u route (§47.1); it is a rule-derived reference cell, not a claim of corpus attestation or a new lexical plural meaning.', 'evidence_refs':['U14-FB-P28','U14-FB-P29','U14-FB-P33','U14-LEX-wuldor']},
]

# ID, citation, model, stem, gloss, vocabulary page, used prompts, scope.
DATA = [
 ('dust','dūst','n-heavy','dūst','dust',283,['EX-VIII-26-01'],'sg'),
 ('sothfaestnes','sōðfæstnes','f-nes','sōðfæstness','truth',313,['EX-VIII-26-03'],'sg'),
 ('sibb','sibb','f-heavy','sibb','peace',312,['EX-VIII-26-04'],'sg'),
 ('flod','flōd','m-strong','flōd','flood; stream of water',287,['EX-VIII-26-05'],'all'),
 ('munt','munt','m-strong','munt','mountain',306,['EX-VIII-26-08','EX-VIII-26-09','FB-VIII-DANGERS-OPENING-ARGUMENT'],'all'),
 ('wuldor','wuldor','n-syncopated','wuldr','glory',323,['EX-VIII-26-10'],'sg'),
 ('wyrtgemang','wyrtgemang','n-heavy','wyrtgemang','spice; mixture of spices',324,['EX-VIII-27-01','NEW-U14-F02'],'all'),
 ('goldhord','goldhord','n-heavy','goldhord','treasure; hoard of gold',297,['EX-VIII-27-01','NEW-U14-F02'],'all'),
 ('godwebb','gōdwębb','n-heavy','gōdwębb','purple cloth',296,['EX-VIII-27-02','NEW-U14-F02'],'sg'),
 ('waedla','wǣdla','m-weak','wǣdl','poor or destitute man',320,['EX-VIII-27-03','EX-VIII-27-05','NEW-U14-F01'],'all'),
 ('hund-dog','hund','m-strong','hund','dog',None,['EX-VIII-27-04'],'all'),
 ('wund','wund','f-heavy','wund','wound; sore',None,['EX-VIII-27-04'],'all'),
 ('witga','wītga','m-weak','wītg','prophet',323,['EX-VIII-27-10'],'all'),
 ('thearfa','ðearfa','m-weak','ðearf','poor or needy person',317,['EX-VIII-27-11','NEW-U14-C02'],'all'),
 ('eage','ēage','n-weak','ēag','eye',283,['EX-VIII-27-06','NEW-U14-F01'],'all'),
 ('wic','wīc','n-heavy','wīc','dwelling; abode',322,['EX-VIII-27-05'],'all'),
 ('god-goods','gōd','n-heavy','gōd','goods; good things; property (plural)',296,['EX-VIII-27-08','NEW-U14-A06'],'pl'),
 ('middangeard','middangeard','m-strong','middangeard','world; earth',305,['EX-VIII-26-02','FB-VIII-DANGERS-OPENING-ARGUMENT'],'sg'),
]

def prior_scope(rec):
    return {k:copy.deepcopy(rec.get(k)) for k in ['knowledge_status','production_taught_in','recognition_taught_in','supplied_in','reviewed_in','coverage_contract']}

lemmas=[]
paradigms=[]
for lid,head,model,stem,gloss,page,tasks,scope in DATA:
    gender=model[0]
    refs=['U14-LEX-'+lid]
    rules=[]
    if model=='m-strong':
        surfaces=[head,stem+'es',stem+'e',head,stem+'as',stem+'a',stem+'um',stem+'as']
        rules=['U14-NOM-STRONG-M'];refs+=['U14-FB-P27','U14-FB-P28']
    elif model=='n-heavy':
        surfaces=[head,stem+'es',stem+'e',head,head,stem+'a',stem+'um',head]
        rules=['U14-NOM-NEUTER-HEAVY'];refs+=['U14-FB-P32','U14-FB-P33']
    elif model=='n-syncopated':
        surfaces=[head,stem+'es',stem+'e',head,stem+'u',stem+'a',stem+'um',stem+'u']
        rules=['U14-NOM-NEUTER-HEAVY','U14-NOM-SYNCOPE'];refs+=['U14-FB-P28','U14-FB-P29','U14-FB-P32','U14-FB-P33']
    elif model in ('f-heavy','f-nes'):
        surfaces=[head,stem+'e',stem+'e',stem+'e',stem+'a',stem+'a',stem+'um',stem+'a']
        rules=['U14-NOM-FEMININE']+(['U14-NOM-NES'] if model=='f-nes' else []);refs+=['U14-FB-P35','U14-FB-P36']
    elif model in ('m-weak','n-weak'):
        surfaces=[head,stem+'an',stem+'an',head if model=='n-weak' else stem+'an',stem+'an',stem+'ena',stem+'um',stem+'an']
        rules=['U14-NOM-WEAK']+(['U14-NOM-WEAK-NEUTER'] if model=='n-weak' else []);refs+=['U14-FB-P37']
    else: raise ValueError(model)
    if lid=='wund': refs+=['U14-BT-MAIN-P1281A','U14-BT-SUPP-P570B','U14-EX-P14']
    if lid=='hund-dog': refs+=['U14-BT-SUPP-P570AB','U14-EX-P14']
    old=PRIOR.get(lid)
    old_sense=old['senses'][0] if old else None
    sense_id=old_sense['sense_id'] if old_sense else lid+'-1'
    scope_note={'all':'Ordinary assigned lexical sense; complete singular/plural production within taught constructions.','sg':'Assigned singular sense is productive; all plural cells are morphological recognition/reference only and authorize no independent plural lexical use.','pl':'Assigned plural goods/property sense is productive; all singular cells are morphological recognition/reference only and authorize no independent singular sense.'}[scope]
    cells=[]
    for i,((case,number),surface) in enumerate(zip([(c,n) for n in ['sg','pl'] for c in ['nom','gen','dat','acc']],surfaces)):
        old_form=next((f for f in (old or {}).get('forms',[]) if f['form']==surface and i==0),None)
        analysis={'case':case,'number':number,'gender':gender}
        status='new_production' if scope=='all' or scope==number else 'new_recognition'
        f={'form_id':old_form['form_id'] if old_form else f'{lid}-{case}-{number}','form':surface,
           'analysis':copy.deepcopy(old_form['analysis']) if old_form else analysis,'knowledge_status':status,
           'evidence_refs':refs,'evidence_basis':'Rule-derived cell from the image-checked citation, explicit stem and cited complete model; not represented as a separately attested corpus token.',
           'teaching_ids':['NEW-U14-NOM-'+lid.upper()],
           'scope_note':'Productive morphology within the assigned sense and taught constructions.' if status=='new_production' else 'Morphological recognition/reference only; no independent lexical use is assigned.',
           'prior_scope':prior_scope(old_form) if old_form else None}
        if old_form: f['contextual_analysis']=analysis
        cells.append(f)
    location={'source_id':'cook_fb_1895_2','printed_page':page,'pdf_page_one_based':page+16,'original_identifier':'Vocabulary s.v. '+head} if page else {'source_id':'cook_ex_1895','printed_page':14,'pdf_page_one_based':22,'original_identifier':'VIII.27.4 with corrected nominal class; Bosworth–Toller s.v. '+head}
    sense={'sense_id':sense_id,'gloss':old_sense['gloss'] if old_sense else gloss,'knowledge_status':'new_production','teaching_ids':['NEW-U14-VOC-'+lid.upper()],'evidence_refs':['U14-LEX-'+lid],'scope_note':scope_note,'used_in_tasks':tasks,'prior_scope':prior_scope(old_sense) if old_sense else None}
    lemma={'lemma_id':lid,'display_headword':head,'part_of_speech':'noun','gender':{'m':'masculine','n':'neuter','f':'feminine'}[gender],
      'declension_model':model,'diagnostic_stem':stem,'diagnostic_forms':{'genitive_singular':surfaces[1],'dative_singular':surfaces[2],'nominative_plural':surfaces[4]},
      'source_location':location,'evidence_refs':refs,'rules':rules,'senses':[sense],'forms':cells,'prior_lemma_present':bool(old),'scope_note':scope_note,'used_in_tasks':tasks,
      'accepted_variants':{'genitive_plural':'ēagna (Cook §53.2; valid alternative, not the selected table cell)'} if lid=='eage' else {},
      'source_headword':head,'headword_origin':'exact checked lexical citation; source compound divider omitted when the cited vocabulary prints one',
      'headword_change_note':'Compound joining is declared typography, not inferred vowel length or dialect regularization.'}
    if lid=='hund-dog': lemma['identity_note']='Distinct from existing lemma hund (the numeral hundred); no old numeral records are reused.'
    if lid=='god-goods': lemma['identity_note']='Distinct from god (deity) and god-adjective; no divine or adjectival senses are treated as this nominal plural sense.'
    if lid=='godwebb': lemma['identity_note']='The checked citation is gōd-wębb, with long ō and hook-e. A provisional low-resolution short-o reading was rejected after a 400-dpi reinspection; the final source citation preserves the printed macron.'
    if lid=='dust': lemma['identity_note']='The checked citation is dūst, with long ū. A provisional low-resolution short-u reading was rejected after a 400-dpi reinspection.'
    if lid=='wund': lemma['correction_ref']='C04'
    lemmas.append(lemma)
    paradigms.append({'paradigm_id':'NEW-U14-NOM-'+lid.upper(),'lemma_id':lid,'headword':head,'model':model,'new_class':model=='n-weak','scope':scope_note,'cells':cells,'rules':rules,'accepted_variants':lemma['accepted_variants']})

counts={'lemmas':len(lemmas),'nominal_systems':len(paradigms),'cells':sum(len(x['forms']) for x in lemmas),'form_status_counts':dict(Counter(f['knowledge_status'] for x in lemmas for f in x['forms'])),'reused_form_ids':sum(f['prior_scope'] is not None for x in lemmas for f in x['forms']),'reused_sense_ids':sum(s['prior_scope'] is not None for x in lemmas for s in x['senses'])}
write('lexical-inventory.json',{'schema_version':1,'baseline_checkpoint':'c2cb7d6','status':'Source-audited nominal proposals; integration and review pending.','lemmas':lemmas,'rules':RULES,'counts':counts,'scope_policy':'Complete eight-cell nominal systems. Only ēage introduces a new class; the other models reuse prior morphology but establish these exact lemmas/senses. Reference cells do not license new lexical uses. Existing identities, surfaces and analyses are preserved; added grammatical precision is contextual_analysis.'})
write('noun-adjective-paradigms.json',{'schema_version':1,'paradigms':paradigms,'rules':RULES,'counts':counts,'adjective_scope':'No new productive adjective class. Exact source adjective uses absent from prior teaching are supplied in source-support-records.json.'})
print(json.dumps(counts,ensure_ascii=False))
