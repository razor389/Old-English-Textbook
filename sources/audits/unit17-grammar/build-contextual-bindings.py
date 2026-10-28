"""Private occurrence analysis, separate from earlier register analyses."""
import json,re,copy,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
L={x['lemma_id']:x for x in json.loads((ROOT/'lexicon/entries.json').read_text(encoding='utf8'))['lemmas']}
S=json.loads((OUT/'verbal-systems.json').read_text(encoding='utf8'))['systems']
NEW=[c for s in S for c in s['cells']]
MODELS=json.loads((OUT/'candidate-models.json').read_text(encoding='utf8'))
def parse(code):
 if code in ['inf','pp','prp']:
  return {'verb_form':{'inf':'plain_infinitive','pp':'past_participle','prp':'present_participle'}[code]}
 if code.startswith('pa:'):
  _,tense,case,gender,number,decl=code.split(':');return {'nonfinite':tense+'_participle','case':case,'gender':gender,'number':number,'declension':decl}
 mood={'ip':'indicative','it':'indicative','sp':'subjunctive','st':'subjunctive','im':'imperative'}[code[:2]]
 a={'mood':mood,'person':int(code[2]),'number':{'s':'singular','p':'plural'}[code[3]]}
 if mood!='imperative':a['tense']='present' if code[:2] in ['ip','sp'] else 'preterite'
 return a
def n(a):
 if not isinstance(a,dict):return a
 d=copy.deepcopy(a)
 if d.get('number') in ['sg','pl']:d['number']={'sg':'singular','pl':'plural'}[d['number']]
 if 'nonfinite' in d:d['verb_form']=d['nonfinite']
 if d.get('verb_form')=='infinitive':d['verb_form']='inflected_infinitive' if d.get('infinitive_type')=='inflected' else 'plain_infinitive'
 if d.get('form')=='infinitive citation':d['verb_form']='plain_infinitive'
 if d.get('verb_form')=='participle':d['verb_form']=d.get('tense','')+'_participle'
 return d
def matches(a,b):
 if not isinstance(a,dict) or not isinstance(b,dict):return False
 aa=n(a);bb=n(b)
 return all(bb.get(k)==v for k,v in aa.items())
def bind(lemma,surface,a,context,task,index,force=None):
 equal=lambda x,y:unicodedata.normalize('NFC',x).casefold()==unicodedata.normalize('NFC',y).casefold()
 old=[f for f in L.get(lemma,{}).get('forms',[]) if equal(f['form'],surface) and matches(a,f['analysis'])]
 taught=[f for f in old if f.get('production_taught_in')]
 new=[f for f in NEW if f['lemma_id']==lemma and equal(f['form'],surface) and matches(a,f['analysis'])]
 choice=taught[0] if taught else new[0] if new else old[0] if old else None
 status='previously_taught' if taught else 'new_production' if new else 'supplied'
 if force:status=force
 fid=choice['form_id'] if choice else f'{lemma}-u17-context-{task.lower().replace(".","-")}-{index}'
 sense=[s for s in L.get(lemma,{}).get('senses',[]) if s.get('production_taught_in')]
 proposed=next((s['sense_proposal'] for s in S if s['lemma_id']==lemma and s.get('sense_proposal')),None)
 return {'source_item_id':task,'token_position_one_based':index,'surface':surface,'lemma_id':lemma,'form_id':fid,'current_context_analysis':a,'contextual_role_and_meaning':context,'form_knowledge_status':status,'prior_form_record':copy.deepcopy(choice) if taught or old and not new else None,'proposed_cell':copy.deepcopy(choice) if new and not taught else None,'prior_productive_senses':copy.deepcopy(sense),'proposed_sense':copy.deepcopy(proposed),'identity_note':'Earlier register analysis is retained unchanged; current contextual person, role, mood and meaning are separate. A familiar form does not itself license this sense or construction.'}
# Surface|lemma|parse|current clause role. Repetitions are resolved in source order.
M={
'37.1':'Hęriað|herian|im2p|Plural addressees praise the Lord;hęriað|herian|im2p|Same plural addressees praise him',
'37.2':'Hęriað|herian|im2p|Angels are addressed;hęriað|herian|im2p|Powers are addressed',
'37.3':'Hęriað|herian|im2p|Sun and moon addressed jointly;hęriað|herian|im2p|Stars and light addressed',
'37.4':'Hęriað|herian|im2p|Heavens and waters addressed;sind|wesan|ip3p|Waters are above heavens',
'37.5':'Hęrien|herian|sp3p|Third-person wish/exhortation with hīe;gecwæð|gecwethan|it3s|God spoke;wǣron|wesan|it3p|Passive auxiliary agreeing with hīe;worhte|wyrcean|pp|Predicate plural past participle made;bebēad|bebeodan|it3s|God commanded absolutely;wǣron|wesan|it3p|Passive auxiliary;gesceapene|gescieppan|pp|Predicate plural past participle created',
'37.6':'sętte|settan|it3s|God appointed them; simple preterite represents English perfect;sętte|settan|it3s|God established a decree;gewīt|gewitan|ip3s|Unexpressed decree-subject will not pass away; present future reference',
'37.7':'Hęriað|herian|im2p|Plural addressees praise God',
'37.8':'dōð|don|ip3p|Storm spirits fulfil his word',
'37.9':'','37.10':'','37.11':'','37.12':'',
'37.13':'Hęrien|herian|sp3p|They are urged to praise;is|wesan|ip3s|Singular name in passive;ūpāhafen|up-ahebban|pp|Name exalted, not literally lifted;is|wesan|ip3s|Glory is above earth and heaven',
'37.14':'ūpāhęfð|up-ahebban|ip3s|God exalts his people’s horn;nēalǣcendes|nealaecan|pa:present:genitive:neuter:singular:strong|Agrees with genitive folces, with dative him as the one approached',
'38.1':'worhte|wyrcean|it3s|King made throne;oferworhte|oferwyrcean|it3s|King overlaid throne with gold',
'38.2':'wæs|wesan|it3s|A queen existed in those days;hāten|hatan|pp|Uninflected predicative naming participle referring to queen',
'38.3':'hīerde|hieran|it3s|Queen heard Solomon’s reputation;cōm|cuman|it3s|Queen came;bǣron|beran|it3p|Camels bore spices, gems, gold',
'38.4':'hæfde|habban|it3s|Queen had speech with Solomon;sægde|secgan|it3s|Queen told him;ðōhte|thencan|it3s|Queen thought whatever in heart; verb-last control',
'38.5':'lǣrde|laeran|it3s|Solomon taught queen;sægde|secgan|it3s|Solomon told meaning to queen;āscode|ascian|it3s|Queen asked him the words/questions',
'38.6':'geseah|geseon|it3s|Queen saw wisdom, temple and services;geworhte|gewyrcean|it3s|King built temple anterior to her seeing',
'38.7':'wæs|wesan|it3s|Queen in astonished state;ofwundrod|ofwundrian|pp|Uninflected predicate participle;astonishment does not license an invented active object frame;næfde|nabban|it3s|Queen had no further spirit',
'38.8':'sægde|secgan|it3s|Queen addressed king;is|wesan|ip3s|Report true;hīerde|hieran|it1s|Queen speaking as I heard;nolde|willan|it1s|Queen’s past unwillingness to believe;gelīefan|geliefan|inf|Complement of nolde;gesāwe|geseon|st1s|Prospective-before past subjunctive; queen saw for herself',
'38.9':'is|wesan|ip3s|Wisdom and work construed together in singular comparison;wǣre|wesan|st3s|Explicit printed wǣre; do not replace with wæs;hīerde|hieran|it1s|Queen heard report',
'38.10':'sind|wesan|ip3p|Vassals and servants are blessed;standað|standan|ip3p|Same people stand before king;hīerað|hieran|ip3p|Same people hear king’s wisdom',
'39.1':'Blētsod|bletsian|pp|Uninflected predicate blessed;sīe|wesan|sp3s|Wish that God be blessed;cēas|ceosan|it3s|God chose king;gesętte|gesettan|it3s|God set king over kingdom;sętte|settan|sp2s|Purpose that king establish judgments and righteousness',
'39.2':'forgeaf|forgiefan|it3s|Queen gave gold and gifts; giving sense, not forgiveness',
'39.3':'forgeaf|forgiefan|it3s|Solomon gave gifts;giernde|giernan|it3s|Queen requested things from him;gewęnde|gewendan|it3s|Queen returned home',
'39.4':'wæs|wesan|it3s|Solomon passive subject;mǣrsod|maersian|pp|Celebrated/exalted above earthly kings;gewilnodon|gewilnian|it3p|Nations desired intended actions;gesāwen|geseon|st3p|Intended seeing under past desire;hīerden|hieran|st3p|Intended hearing under past desire',
'39.5':'wyrcð|wyrcean|ip3s|Whoever builds on foundation;bið|wesan|ip3s|Future passive auxiliary;gesweotolod|gesweotolian|pp|Each one’s work will become manifest',
'39.6':'ðurhwunað|thurhwunian|ip3s|Building endures;wiðstęnt|withstandan|ip3s|Building withstands dative fire;onfēhð|onfon|ip3s|Worker receives dative reward from God',
'39.7':'mæg|magan|ip3s|Eye can see, with coordinated ellipsis for ear and heart;gesēon|geseon|inf|Capability infinitive with eye as actor;hīeran|hieran|inf|Capability infinitive with ear as actor;āsmēan|asmean|inf|Printed citation-reference: heart conceive;gearcað|gearcian|ip3s|God prepares things for dative beneficiaries;lufiað|lufian|ip3p|Beneficiaries love him',
'40.1':'grētte|gretan|it3s|Angel greeted Mary;sægde|secgan|it3s|Angel reported;āfylled|afyllan|pp|Mary filled with gift;wǣre|wesan|st3s|Reported past passive state;wǣre|wesan|st3s|Reported God-with-her state;wæs|wesan|it3s|Narrator asserts she was blessed;blētsod|bletsian|pp|Uninflected predicate referring to Mary',
'40.2':'mǣrsað|maersian|ip3s|Soul magnifies Lord;blissode|blissian|it3s|Spirit rejoiced in God',
'40.3':'geseah|geseon|it3s|God regarded humility;sęcgað|secgan|ip3p|Generations will call Mary blessed, accusative predicate',
'40.4':'is|wesan|ip3s|God is mighty;dyde|don|it3s|God did great things for Mary;is|wesan|ip3s|God’s name is holy',
'40.5':'is|wesan|ip3s|Mercy belongs to/benefits dative fearers;ondrǣdendum|ondraedan|pa:present:dative:masculine:plural:strong|Substantival those fearing; hine is accusative object of fearing, not dative experiencer',
'40.6':'āwearp|aweorpan|it3s|God cast powerful down;ūpāhōf|up-ahebban|it3s|God exalted lowly',
'40.7':'āfylde|afyllan|it3s|God filled hungry people with goods;hyngrendan|hyngran|pa:present:accusative:masculine:plural:weak|Substantival hungry ones after ðā;forlēt|forlaetan|it3s|God let rich depart/left them empty',
'40.8':'onfēng|onfon|it3s|God accepted servant Israel into care; dative cnihte;gemunde|gemunan|it3s|God remembered mercy',
'40.9':'spræc|sprecan|it3s|God spoke to fathers; dative Abraham and seed apposition',
'40.10':'wunode|wunian|it3s|Mary stayed with her;gewęnde|gewendan|it3s|Mary returned to own house',
'41.1':'wæs|wesan|it3s|God existed always;wæs|wesan|it3s|Wisdom’s begetting in continuing state;ācęnned|acennan|pp|Uninflected passive begotten; of-him source phrase local support;is|wesan|ip3s|Wisdom identified as Son',
'41.2':'gefylð|gefyllan|ip3s|Spirit fills world;healt|healdan|ip3s|Spirit maintains all things',
'41.3':'wyrcð|wyrcean|ip3s|Whoever performs Father’s will;is|wesan|ip3s|That person is speaker’s kin',
'41.4':'brōhton|bringan|it1p|We brought nothing;magon|magan|ip1p|We cannot take anything;lǣdan|laedan|inf|We take/carry things away with ourselves',
'41.5':'Biddað|biddan|im2p|Plural askers addressed;bið|wesan|ip3s|Impersonal giving passive with ēow recipient;geseald|sellan|pp|Past participle of sęllan, not a finite verb;sēcað|secan|im2p|Plural command;findað|findan|ip2p|Prediction addressed to plural gē;cnuciað|cnucian|im2p|Plural command knock;bið|wesan|ip3s|Opening passive;geopenod|geopenian|pp|Uninflected passive opened',
'41.6':'eart|wesan|ip2s|Relative thou which art retains addressee2sg;sīe|wesan|sp3s|Wish for name;gehālgod|gehalgian|pp|Name hallowed',
'41.7':'Tōcume|tocuman|sp3s|Kingdom subject of wish; specified prefixed verb first;geweorðe|geweorthan|sp3s|Will subject of wish; verb first',
'41.8':'Sęle|sellan|im2s|Address God singular;forgief|forgiefan|im2s|Forgive our debts;forgiefað|forgiefan|ip1p|We forgive our dative debtors',
'41.9':'lǣd|laedan|im2s|Negative command singular with explicit ðū;ālīes|aliesan|im2s|Deliver us from evil',
'41.10':'Sīe|wesan|sp3s|Independent wish with it subject',
'41.11':'sęlð|sellan|ip3s|Father will give stone, future present;bitt|biddan|ip3s|Child asks person accusative for bread genitive',
'41.12':'āwrāt|awritan|it3s|God wrote law',
'42.1':'befēoll|befeallan|it3s|Love, not young man, is grammatical subject; girl target of on+accusative',
'42.2':'hīerde|hieran|it1s|I heard voice;hearpiendra|hearpian|pa:present:genitive:masculine:plural:strong|Genitive harpers perform harping; whole phrase supplied;sungon|singan|it3p|Harpers sang; reserve voice-person distinction;mihte|magan|it3s|No man had ability;leornian|leornian|inf|Complement learn the song',
'42.3':'geseah|geseon|it1s|I saw company;mæg|magan|ip3s|No man can count;gerīman|geriman|inf|Exact visible reference infinitive;standende|standan|prp|Predicative participle, company’s members standing;gescrȳdde|gescrydan|pp|Plural semantic agreement with company members;healdende|healdan|prp|Same members holding palms; whole dense clause supplied',
'42.4':'sungon|singan|it3p|Company members sang;sīe|wesan|sp3s|Wish assigning salvation to dative God;sitt|sittan|ip3s|God sits above/on throne',
'42.5':'stōdon|standan|it3p|Angels stood;āluton|alutan|it3p|Angels bowed intransitively to dative God;cweðende|cwethan|prp|Accompanying saying with plural angels; uninflected predicate form',
'42.6':'sīe|wesan|sp3s|Doxological wish; blessing/glory cluster treated as one attribution',
'42.7':'habbað|habban|ip3p|Foxes have holes; same verb understood for birds;næfð|nabban|ip3s|Son lacks a place;āhylde|ahyldan|sp3s|Indefinite/virtual locative: where he might lay head; no separate modal',
'42.8':'wundon|windan|it3p|Soldiers plaited crown;sętton|settan|it3p|Soldiers placed crown and reed; object of crown-clause recovered;bīegdon|biegan|it3p|Soldiers bent accusative knee;cweðende|cwethan|prp|Same soldiers saying; predicate uninflected;bēo|wesan|sp2s|Hail/wish addressed to singular king',
'42.9':'spǣtton|spaetan|it3p|Soldiers spat on him;nāmon|niman|it3p|Soldiers took reed;bēoton|beatan|it3p|Soldiers smote head',
'43.1':'is|wesan|ip3s|Flesh identified metaphorically as grass;is|wesan|ip3s|Glory compared to flower',
'43.2':'hīerde|hieran|it3s|No man heard; negative concord',
'43.3':'Cleopa|cleopian|im2s|Singular cry command;geswīc|geswican|im2s|Singular cease-not command;āhęfe|ahebban|im2s|Singular lift command; not present-subjunctive merely because ends-e',
'43.4':'gǣst|gan|ip2s|Lady addressed singular',
'43.5':'dēst|don|ip2s|You do ill; action/manner idiom',
'43.6':'dyde|don|it3s|He did ill;tǣlde|taelan|it3s|He blamed princess',
'43.7':'leornodon|leornian|it3p|They never learned arithmetic well',
'43.8':'witon|witan|ip2p|Plural addressees will soon know;witon|witan|ip2p|Same addressees do not yet know; uncontracted ne witon',
'43.9':'Plega|plegian|im2s|Singular play command; mid instrument',
'43.10':'ete|etan|ip1s|Speaker asserts not eating;eten|etan|sp3p|Concessive other men eat;sīen|wesan|sp3p|Concessive other men merry',
'43.11':'gewilnie|gewilnian|ip1s|Speaker desires;leornie|leornian|sp1s|Same speaker in intended-content clause;habbað|habban|ip2p|Addressees possess knowledge',
'43.12':'Cēos|ceosan|im2s|Singular command choose;wille|willan|sp2s|Indefinite choice relative: whichever you wish',
'43.13':'cōmon|cuman|it3p|Two men came;gelǣrede|laeran|pp|Educated men: attributive strong nominative masculine plural',
'43.14':'gierne|giernan|ip1s|Speaker seeks maiden in marriage; genitive person',
'43.15':'sęcgað|secgan|ip1p|All of us report;sīe|wesan|sp3s|Reported assessment per194b; no one acceptable as him',
'43.16':'wēnde|wenan|it3s|He supposed;slōge|slean|st3s|Indefinite man subject, him object, contemplated slaying not asserted death',
'43.17':'feallað|feallan|ip1p|We fall to addressee’s feet',
'43.18':'gelīefe|geliefan|ip1s|Speaker does not believe;sīe|wesan|sp2s|Reported/denied wife identity; same spelling as3sg but subject2sg',
'43.19':'is|wesan|ip3s|Husband location',
'43.20':'lifde|libban|it1s|Speaker lived eleven years'}
rows=[]
for r in MODELS['rows']:
 short=r['source_item_id'].removeprefix('EX-XII-XIII-').replace('-','.')
 # Remove leading zeros in item for compact canonical map.
 short='.'.join(str(int(x))for x in short.split('.'))
 text=M[short]
 for a,b in [('sind|','sindon|'),('healt|','hielt|'),('geseald|','seald|'),('mihte|','meahte|'),('nāmon|','nōmon|')]:text=text.replace(a,b)
 specs=[x for x in re.split(r';(?=[^;|]+\|[^;|]+\|)',text) if x]
 used=set();rr=[]
 for spec in specs:
  if spec.count('|')!=3:raise ValueError((short,spec))
  surface,lemma,code,context=spec.split('|')
  try:i=next(i for i in range(len(r['tokens'])) if i not in used and r['tokens'][i]==surface)
  except StopIteration:raise ValueError((short,surface,r['model']))
  used.add(i)
  rr.append(bind(lemma,surface,parse(code),context,r['source_item_id'],i+1))
 rows.append({'source_item_id':r['source_item_id'],'model':r['model'],'verbal_occurrences':sorted(rr,key=lambda x:x['token_position_one_based']),'nonverbal_identity_owner':'unit17_source and unit17_design; no bare-surface identity certification here'})
OUT.joinpath('candidate-verbal-bindings.json').write_text(json.dumps({'access':'author-only; exclude from blind reviewers','status':'contextual morphology analyzed; unresolved identity cells are explicitly supplied pending integration','rows':rows,'verbal_occurrence_count':sum(len(r['verbal_occurrences'])for r in rows)},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('items',len(rows),'verbal occurrences',sum(len(r['verbal_occurrences'])for r in rows))
