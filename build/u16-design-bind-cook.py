import copy
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'curriculum/proposals/unit16'

def read(p, default=None):
    path=ROOT/p
    return json.loads(path.read_text(encoding='utf-8-sig')) if path.exists() else default
def save(n,v):
    (DEST/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def norm(s):
    return unicodedata.normalize('NFC',s).casefold()

base=read('lexicon/entries.json')['lemmas']
base_form_ids={f['form_id'] for l in base for f in l['forms']}
base_sense_ids={s['sense_id'] for l in base for s in l['senses']}
forms,senses,owners={}, {}, {}
for packet in [{'lemmas':base},read('curriculum/proposals/unit16/inventory.json')]:
    for l in packet['lemmas']:
        owners[l['lemma_id']]=l
        for f in l['forms']:
            if f['form_id'] not in forms:
                forms[f['form_id']]=(l['lemma_id'],copy.deepcopy(f))
            else:
                forms[f['form_id']][1].setdefault('current_scope',f.get('knowledge_status'))
        for s in l['senses']:
            if s['sense_id'] not in senses:
                senses[s['sense_id']]=(l['lemma_id'],copy.deepcopy(s))
            else:
                senses[s['sense_id']][1].setdefault('current_scope',s.get('knowledge_status'))
by_surface=defaultdict(list)
for fid,(lid,f) in forms.items():
    by_surface[norm(f['form'])].append((lid,f))

def status(rec):
    if rec.get('production_taught_in'):return 'previously_taught'
    rid=rec.get('form_id',rec.get('sense_id'))
    if rid in base_form_ids or rid in base_sense_ids:
        if rec.get('current_scope') in ('new_production','supplied','new_recognition'):return rec['current_scope']
        if rec.get('recognition_taught_in'):return 'prior_recognition'
        return 'supplied'
    return rec.get('current_scope') or rec.get('knowledge_status','unresolved')

# These selections are contextual, not an assertion that a lemma has only one sense.
sense_selection={
 'aefter':'aefter-after-source','an':'an-1','be':'be-u14-concerning-source','beforan':'beforan-before-source',
 'beran':'beran-1','biddan':'biddan-1','blissian':'blissian-u16','cleopian':'cleopian-u15-call',
 'cunnan':'cunnan-u16-acquaintance','cwethan':'cwethan-1','dead':'dead-1','deman':'deman-u15-judge',
 'dom':'dom-1','don':'don-u16-substitute','eall':'eall-all','fleon':'fleon-flee','forgiefan':'forgiefan-u16-forgive',
 'forlaetan':'forlaetan-1','fot':'fot-foot-source','fram':'fram-1','gan':'gan-1','gefyllan':'gefyllan-u16-fulfil',
 'gelimpan':'gelimpan-u16-source','geseon':'geseon-1','geswican':'geswican-cease','habban':'habban-1',
 'halsian':'halsian-u16-conjure','he':'he-1','hieran':'hieran-1','hwa':'hwa-interrogative','hwilc':'hwilc-u13-any',
 'ic':'ic-personal','laedan':'laedan-1','laeran':'laeran-u15-teach','libban':'libban-u16-source',
 'lif':'lif-1','mann':'mann-1','micel':'micel-1','mid':'mid-accompaniment-source','of':'of-u11-source',
 'ofer':'ofer-1','on':'on-1','rihtwis':'rihtwis-1','se':'se-the','secgan':'secgan-1','sellan':'sellan-give',
 'singan':'singan-1','sona':'sona-immediately-source','sothlice':'sothlice-truly','sprecan':'sprecan-1',
 'straet':'straet-1','sum':'sum-some','swa':'swa-u15-free-choice','swithe':'swithe-positive','swithra':'swithra-1',
 'thaet-conjunction':'thaet-conjunction-1','the-relative':'the-relative-which','thonne':'thonne-than',
 'thu':'thu-personal','thurh':'thurh-through','to':'to-destination','twegen':'twegen-1','weg':'weg-1',
 'wel':'wel-positive','weorthan':'weorthan-become','wesan':'wesan-be','wif':'wif-woman','willan':'willan-1',
 'witan':'witan-content','word':'word-1'}
fixed_lemma={'and':'and','ac':'ac','ne':'ne','gif':'gif','on':'on','of':'of','mid':'mid','tō':'to','be':'be',
             'ðe':'the-relative','oððe':'othothe','for-ðon-ðe':'for-thon-the','sang':'singan','hām':'ham','hund':'hund',
             'swilce':'swilce','bęt':'wel','geseah':'geseon','gesēo':'geseon','gesiehst':'geseon','gesāwon':'geseon','gesēoð':'geseon',
             'lǣtt':'laedan','lǣded':'laedan','āgylt':'agyldan'}
sense_selection.update({'magan':'magan-1','healdan':'healdan-u16-keep','weorthan':'weorthan-u16-arise','for-thon-the':'for-thon-the-because','ingan':'ingan-u13'})
surface_specs={}
overrides={}
sense_overrides={}

def morph(code):
    a={}
    for x in code.split('.'):
        if x in ('nom','gen','dat','acc','ins'):a['case']=x
        elif x in ('sg','pl','dual'):a['number']=x
        elif x in ('m','f','n'):a['gender']=x
        elif x in ('1','2','3'):a['person']=int(x)
        elif x in ('pres','pret'):a['tense']={'pres':'present','pret':'preterite'}[x]
        elif x in ('ind','subj','imp'):a['mood']={'ind':'indicative','subj':'subjunctive','imp':'imperative'}[x]
        elif x in ('strong','weak'):a['strength']=x
        elif x=='inf':a['nonfinite']='infinitive'
        elif x=='pp':a['nonfinite']='past_participle'
    return a

def D(surface,lid,code='',sense=None):
    surface_specs[norm(surface)]={'lemma_id':lid,**morph(code)}
    if sense:surface_specs[norm(surface)]['sense_id']=sense
def S(item,index,lid,code='',sense=None):
    for i in ([index] if isinstance(index,int) else index):
        overrides[(item,i)]={'lemma_id':lid,**morph(code)}
        if sense:overrides[(item,i)]['sense_id']=sense

# Personal and possessive surfaces have explicitly selected ordinary case defaults;
# the different functions at particular positions are separately overridden below.
for surface,lid,code in [('ic','ic','nom.sg'),('wē','ic','nom.pl'),('ūs','ic','dat.pl'),('mē','ic','dat.sg'),
 ('ðū','thu','nom.sg'),('gē','thu','nom.pl'),('git','thu','nom.dual'),('ēow','thu','acc.pl'),('ðē','thu','dat.sg'),
 ('unc','ic','dat.dual'),('inc','thu','dat.dual'),('hē','he','nom.sg.m'),('hēo','he','nom.sg.f'),('hīe','he','nom.pl'),
 ('hine','he','acc.sg.m'),('him','he','dat.sg.m'),('hit','he','acc.sg.n'),('his','he','gen.sg.m'),('hiera','he','gen.pl'),('hiere','he','dat.sg.f')]:D(surface,lid,code)
for surface in ('his','hiera'):surface_specs[norm(surface)]['sense_id']='he-possessor'
for surface,lid,code in [('se','se','nom.sg.m'),('sē','se','nom.sg.m'),('sēo','se','nom.sg.f'),('ðone','se','acc.sg.m'),
 ('ðǣre','se','dat.sg.f'),('ðæs','se','gen.sg.m'),('ðǣm','se','dat.sg.m'),('ðā','se','acc.pl'),
 ('ðisne','thes','acc.sg.m'),('ðis','thes','acc.sg.n'),('ðēos','thes','nom.sg.f'),('ðisse','thes','dat.sg.f')]:D(surface,lid,code)
for surface,lid,code in [('grēte','gretan','pres.ind.1.sg'),('rēowon','rowan','pret.ind.3.pl'),('gesāwon','geseon','pret.ind.3.pl'),
 ('ārās','arisan','pret.ind.3.sg'),('bebēad','bebeodan','pret.ind.3.sg'),('cwæð','cwethan','pret.ind.3.sg'),('geswāc','geswican','pret.ind.3.sg'),
 ('wearð','weorthan','pret.ind.3.sg'),('hīerst','hieran','pres.ind.2.sg'),('wāst','witan','pres.ind.2.sg'),('cymð','cuman','pres.ind.3.sg'),
 ('gǣð','gan','pres.ind.3.sg'),('geseah','geseon','pret.ind.3.sg'),('wǣron','wesan','pret.ind.3.pl'),('sægde','secgan','pret.ind.3.sg'),
 ('bēoð','wesan','pres.ind.2.pl'),('forlēton','forlaetan','pret.ind.3.pl'),('ǣswicað','aeswician','pres.ind.3.sg'),('gā','gan','pres.subj.2.sg'),
 ('hæbbe','habban','pres.subj.2.sg'),('sīe','wesan','pres.subj.3.sg'),('is','wesan','pres.ind.3.sg'),('hæfð','habban','pres.ind.3.sg'),
 ('forlīest','forleosan','pres.ind.3.sg'),('forlǣtt','forlaetan','pres.ind.3.sg'),('sēcð','secan','pres.ind.3.sg'),('forwearð','forweorthan','pret.ind.3.sg'),
 ('sęcge','secgan','pres.ind.1.sg'),('blissað','blissian','pres.ind.3.sg'),('cleopað','cleopian','pres.ind.3.sg'),('cwið','cwethan','pres.ind.3.sg'),
 ('fand','findan','pret.ind.1.sg'),('fundon','findan','pret.ind.3.pl'),('nōm','niman','pret.ind.3.sg'),('fōr','faran','pret.ind.3.sg'),
 ('wǣre','wesan','pret.subj.3.sg'),('wæs','wesan','pret.ind.3.sg'),('cleopode','cleopian','pret.ind.3.sg'),('magon','magan','pres.ind.3.pl'),
 ('gīemð','gieman','pres.ind.3.sg'),('wēndon','wenan','pret.ind.3.pl'),('geswīcst','geswican','pres.ind.2.sg'),('finde','findan','pres.subj.3.sg'),
 ('wille','willan','pres.ind.1.sg'),('sægdon','secgan','pret.ind.3.pl'),('willað','willan','pres.ind.1.pl'),('ēodon','gan','pret.ind.3.pl'),
 ('fēngon','fon','pret.ind.3.pl'),('fēde','fedan','pres.subj.3.sg'),('sindon','wesan','pres.ind.3.pl'),('hālsie','halsian','pres.ind.1.sg'),
 ('gesēoð','geseon','pres.ind.2.pl'),('wāt','witan','pres.ind.3.sg'),('lǣrde','laeran','pret.ind.3.sg'),('cunnon','cunnan','pres.ind.2.pl'),
 ('witon','witan','pres.ind.2.pl'),('eom','wesan','pres.ind.1.sg'),('cōm','cuman','pret.ind.1.sg'),('sęnde','sendan','pret.ind.3.sg'),
 ('cūðon','cunnan','pret.ind.2.pl'),('cann','cunnan','pres.ind.1.sg'),('cunne','cunnan','pres.subj.1.sg'),('healde','healdan','pres.ind.1.sg'),
 ('wuldrie','wuldrian','pres.ind.1.sg'),('nis','wesan','pres.ind.3.sg'),('wuldrað','wuldrian','pres.ind.3.sg'),('cweðað','cwethan','pres.ind.2.pl'),
 ('fēng','fon','pret.ind.3.sg'),('cōme','cuman','pret.ind.2.sg'),('plegode','plegian','pret.ind.1.sg'),('dyde','don','pret.ind.3.sg'),
 ('sang','singan','pret.ind.3.sg'),('ðolode','tholian','pret.ind.1.sg'),('wiste','witan','pret.ind.1.sg'),('hīerde','hieran','pret.ind.3.sg'),
 ('mōt','motan','pres.ind.3.sg'),('lǣtt','laedan','pres.ind.3.sg'),('findað','findan','pres.ind.3.pl'),('cumað','cuman','pres.ind.3.pl'),
 ('nēalǣcte','nealaecan','pret.ind.3.sg'),('gesēo','geseon','pres.ind.1.sg'),('ālīest','aliesan','pres.ind.3.sg'),('bewęnde','bewendan','pret.ind.3.sg'),
 ('gesiehst','geseon','pres.ind.2.sg'),('ēode','gan','pret.ind.1.sg'),('sealdest','sellan','pret.ind.2.sg'),('ðwōh','thwean','pret.ind.3.sg'),
 ('cyste','cyssan','pret.ind.3.sg'),('smieredest','smierwan','pret.ind.2.sg'),('smierede','smierwan','pret.ind.3.sg'),('lufode','lufian','pret.ind.3.sg'),
 ('lufað','lufian','pres.ind.3.sg'),('gehēt','gehatan','pret.ind.3.sg'),('bǣde','biddan','pret.subj.3.sg'),('āsęnde','asendan','pret.ind.3.sg'),
 ('behēafdode','beheafdian','pret.ind.3.sg'),('brōhte','bringan','pret.ind.3.sg')]:D(surface,lid,code)
for surface,lid,number in [('geswīc','geswican','sg'),('āceorf','aceorfan','sg'),('weorp','weorpan','sg'),('blissiað','blissian','pl'),
 ('ārīs','arisan','sg'),('nim','niman','sg'),('flēoh','fleon','sg'),('forlǣt','forlaetan','sg'),('ęfthweorf','efthweorfan','sg'),
 ('fōh','fon','sg'),('smiere','smierwan','sg'),('sęllað','sellan','pl'),('dēmað','deman','pl'),('sęle','sellan','sg')]:D(surface,lid,'imp.2.'+number)
for surface,lid in [('gān','gan'),('sęndan','sendan'),('biddan','biddan'),('sittan','sittan'),('cuman','cuman'),('sprecan','sprecan'),('iernan','iernan'),('habban','habban')]:D(surface,lid,'inf')

# Item-specific syntactic case, speech-participant and clause-role decisions.
S('32-01',4,'eall','acc.pl.m.strong')
S('32-02',1,'tha-conjunction');S('32-02',9,'tha-adverb');S('32-02',12,'haelend','acc.sg.m');S('32-02',10,'geseon','pret.ind.3.pl','geseon-perceive-action')
S('32-03',12,'geswican','imp.2.sg')
S('32-04',6,'micel','nom.sg.f.strong');S('32-04',7,'smyltnes','nom.sg.f')
S('32-05',4,'stefn','acc.sg.f')
S('32-06',2,'geseon','pret.ind.3.sg','geseon-perceive-action');S('32-06',3,'twegen','acc.pl.m');S('32-06',4,'brothor','acc.pl.m');S('32-06',8,'se','acc.sg.f');S('32-06',9,'sae','acc.sg.f')
S('32-07',4,'he','dat.pl');S('32-07',5,'cuman','imp.2.pl');S('32-07',10,'don','pres.ind.1.sg','don-u16-cause');S('32-07',11,'thaet-conjunction');S('32-07',14,'mann','gen.pl')
S('32-08',2,'thin-poss','nom.sg.f.strong');S('32-08',3,'hand','nom.sg.f');S('32-08',5,'thin-poss','nom.sg.m.strong');S('32-08',6,'fot','nom.sg.m');S('32-08',7,'thu','acc.sg');S('32-08',16,'god-adjective-comp','nom.sg.n');S('32-08',19,'thaet-conjunction');S('32-08',21,'healt','nom.sg.m.strong');S('32-08',23,'lif','acc.sg.n');S('32-08',25,'thonne');S('32-08',27,'twegen','acc.pl.f');S('32-08',28,'hand','acc.pl.f');S('32-08',30,'twegen','acc.pl.m');S('32-08',31,'fot','acc.pl.m');S('32-08',35,'ece','acc.sg.n.strong');S('32-08',36,'fyr','acc.sg.n');S('32-08',37,'wesan','pres.subj.2.sg','wesan-passive')
S('32-09',2,'hwilc','nom.sg.m.strong');S('32-09',3,'mann','nom.sg.m');S('32-09',9,'an','acc.sg.n');S('32-09',10,'of','','of-u15-source-partitive');S('32-09',11,'se','dat.pl','se-that');S('32-09',15,'se','acc.pl','se-the');S('32-09',25,'se','acc.sg.n','se-free-relative-what-source')
S('32-10',3,'he','nom.sg.n');S('32-10',[5,13],'thaet-conjunction');S('32-10',11,'thu','dat.pl');S('32-10',17,'se','acc.sg.n','se-that')
S('32-11',1,'thonne-conjunction');S('32-11',8,'freond','acc.pl.m');S('32-11',11,'neahgebur','acc.pl.m');S('32-11',20,'min-poss','acc.sg.n.strong');S('32-11',21,'forleosan','acc.sg.n.strong');S('32-11',22,'sceap','acc.sg.n')
S('33-01',3,'se','dat.sg.n');S('33-01',4,'hus','dat.sg.n');S('33-01',8,'se','acc.sg.n');S('33-01',9,'bearn','acc.sg.n');S('33-01',13,'modor','dat.sg.f')
S('33-02',4,'se','acc.sg.n');S('33-02',5,'bearn','acc.sg.n');S('33-02',8,'modor','acc.sg.f');S('33-02',10,'niht','dat.sg.f');S('33-02',15,'land','dat.sg.n');S('33-02',17,'wesan','imp.2.sg');S('33-02',20,'thaet-conjunction');S('33-02',23,'secgan','pres.subj.1.sg')
S('33-03',2,'tha-adverb');S('33-03',6,'se','acc.sg.n');S('33-03',7,'bearn','acc.sg.n');S('33-03',10,'modor','acc.sg.f');S('33-03',12,'niht','dat.sg.f');S('33-03',17,'land','acc.sg.n');S('33-03',18,'thaet-conjunction','','thaet-purpose');S('33-03',20,'wesan','pret.subj.3.sg','wesan-passive');S('33-03',21,'se','nom.sg.n','se-free-relative-what-source');S('33-03',24,'thurh','','thurh-u14-mediated-source');S('33-03',28,'wesan','pret.ind.3.sg','wesan-passive');S('33-03',32,'min-poss','acc.sg.m.strong');S('33-03',33,'sunu','acc.sg.m');S('33-03',34,'cleopian','pret.ind.1.sg')
S('33-04',1,'hwa','gen.sg.n')
S('33-05',4,'se','gen.sg.m')
S('33-06',5,'butan-except');S('33-06',7,'self','gen.sg.m.strong')
S('33-07',3,'thin-poss','gen.sg.n.strong')
S('33-08',1,'wen','nom.sg.f');S('33-08',3,'thaet-conjunction');S('33-08',5,'freond','acc.sg.m')
S('33-09',3,'he','dat.pl')
S('33-10',7,'scip','acc.sg.n');S('33-10',14,'niht','dat.sg.f')
S('34-01',2,'hwa','nom.sg.m','hwa-u14-indefinite-source');S('34-01',5,'wesan','pres.subj.2.sg');S('34-01',8,'ic','acc.sg')
S('34-02',3,'nan','acc.sg.m.strong');S('34-02',5,'findan','pres.subj.2.sg');S('34-02',7,'thu','acc.sg')
S('34-03',2,'min-poss','nom.pl.f.strong');S('34-03',3,'boc','nom.pl.f');S('34-03',5,'begen','dat.pl.m')
S('34-04',1,'begen','nom.pl.m');S('34-04',2,'se','nom.pl');S('34-04',3,'cnapa','nom.pl.m');S('34-04',6,'gelared','nom.pl.m.strong')
S('34-05',3,'begen','nom.pl.m');S('34-05',4,'rihtwis','nom.pl.m.strong')
S('34-06',3,'thu','acc.sg');S('34-06',4,'thurh','','thurh-u15-oath');S('34-06',7,'god','acc.sg.m');S('34-06',8,'thaet-conjunction');S('34-06',11,'secgan','pres.subj.2.sg','secgan-content');S('34-06',14,'wesan','pres.subj.2.sg');S('34-06',15,'crist','nom.sg.m');S('34-06',17,'sunu','nom.sg.m')
S('34-07',2,'thu','dat.pl');S('34-07',5,'thes','dat.sg.n');S('34-07',7,'geseon','pres.ind.2.pl','geseon-perceive-action');S('34-07',8,'mann','gen.sg.m');S('34-07',9,'sunu','acc.sg.m');S('34-07',11,'se','acc.sg.f');S('34-07',12,'swithra','acc.sg.f.weak');S('34-07',13,'hand','acc.sg.f');S('34-07',15,'maegenthrymm','gen.sg.m')
S('34-08',1,'wesan','pres.subj.3.sg');S('34-08',3,'begen','dat.pl.m');S('34-08',4,'aefter','','aefter-according-to-source');S('34-08',5,'incer-poss','dat.sg.m.strong');S('34-08',6,'geleafa','dat.sg.m')
S('34-09',2,'mann','gen.sg.m');S('34-09',3,'sunu','nom.sg.m');S('34-09',5,'to','','to-inflected-infinitive');S('34-09',9,'faeder','gen.sg.m');S('34-09',12,'thonne','','thonne-then-source');S('34-09',16,'be','','be-according-source')
S('34-10',1,'thonne-conjunction');S('34-10',2,'crist','nom.sg.m');S('34-10',4,'thonne','','thonne-then-source');S('34-10',7,'nan','nom.sg.m.strong');S('34-10',8,'mann','nom.sg.m')
S('34-11',1,'haelend','nom.sg.m');S('34-11',2,'cleopian','pret.ind.3.sg','cleopian-u16-cry');S('34-11',7,'tempel','dat.sg.m');S('34-11',10,'ic','acc.sg');S('34-11',25,'self','dat.sg.m.strong');S('34-11',27,'se','nom.sg.m','se-that');S('34-11',29,'soth-citation','nom.sg.m.strong');S('34-11',31,'ic','acc.sg');S('34-11',33,'se','acc.sg.m','se-relative')
S('34-12',12,'thaet-conjunction');S('34-12',18,'wesan','pres.ind.1.sg');S('34-12',19,'thu','dat.pl');S('34-12',20,'gelic','nom.sg.m.strong');S('34-12',29,'spraec','acc.sg.f')
S('34-13',[3,15],'ic','acc.sg');S('34-13',4,'self','acc.sg.m.strong');S('34-13',7,'min-poss','nom.sg.n.strong');S('34-13',8,'wuldor','nom.sg.n');S('34-13',10,'min-poss','nom.sg.m.strong');S('34-13',11,'faeder','nom.sg.m');S('34-13',13,'se','nom.sg.m','se-that');S('34-13',18,'se','dat.sg.m','se-relative');S('34-13',21,'thaet-conjunction');S('34-13',23,'eower-poss','nom.sg.m.strong');S('34-13',24,'god','nom.sg.m')
S('35-01',3,'thothor','acc.sg.m')
S('35-02',1,'hwa','nom.sg.m');S('35-02',4,'blaec','acc.sg.m.weak');S('35-02',5,'thothor','acc.sg.m')
S('35-03',1,'gan','imp.2.sg');S('35-03',3,'weg','gen.sg.m')
S('35-04',5,'wel','','wel-comparative');S('35-04',9,'don','pret.ind.1.sg','don-u16-substitute')
S('35-05',5,'wel','','wel-comparative')
S('35-06',5,'an','acc.sg.f.strong');S('35-06',6,'niht','acc.sg.f');S('35-06',8,'an','acc.sg.m.strong');S('35-06',9,'daeg','acc.sg.m');S('35-06',11,'wesan','pret.ind.1.sg');S('35-06',14,'sae','dat.sg.f')
S('35-07',2,'witan','pret.ind.1.sg','witan-u16-person');S('35-07',3,'sum','acc.sg.m.strong');S('35-07',4,'mann','acc.sg.m');S('35-07',5,'se','nom.sg.m','se-relative');S('35-07',7,'wesan','pret.ind.3.sg','wesan-passive');S('35-07',10,'thridda','acc.sg.m.weak');S('35-07',11,'heofon','acc.sg.m');S('35-07',12,'laedan','pp','laedan-u16-carry');S('35-07',17,'word','acc.pl.n');S('35-07',19,'nan','nom.sg.m.strong');S('35-07',20,'eorthlic','nom.sg.m.strong');S('35-07',21,'mann','nom.sg.m')
S('35-08',3,'nearu','nom.sg.n.strong');S('35-08',5,'se','nom.sg.n');S('35-08',6,'geat','nom.sg.n');S('35-08',9,'weg','nom.sg.m');S('35-08',12,'lif','dat.sg.n');S('35-08',20,'weg','acc.sg.m')
S('35-09',4,'thu','dat.pl');S('35-09',6,'sceap','gen.pl.n');S('35-09',7,'gegierela','dat.pl.m')
S('35-10',1,'tha-conjunction');S('35-10',3,'se','gen.sg.f');S('35-10',4,'burg','gen.sg.f');S('35-10',5,'geat','dat.sg.n');S('35-10',7,'tha-adverb');S('35-10',8,'wesan','pret.ind.3.sg','wesan-passive');S('35-10',10,'dead','nom.sg.m.strong');S('35-10',11,'mann','nom.sg.m')
S('35-11',2,'geseon','pres.ind.1.sg','geseon-perceive-action');S('35-11',3,'maeden','acc.sg.n');S('35-11',5,'se','acc.sg.f');S('35-11',6,'straet','acc.sg.f')
S('35-12',2,'ic','acc.sg');S('35-12',3,'mid','','mid-by-means')
S('35-13',4,'eower-poss','dat.sg.m.strong');S('35-13',5,'ele','dat.sg.m')
S('35-14',3,'sunu','nom.sg.m')
S('36-01',4,'be','','be-according-source');S('36-01',5,'ansien','dat.sg.f');S('36-01',8,'riht','acc.sg.m.strong');S('36-01',9,'dom','acc.sg.m')
S('36-02',1,'tha-adverb');S('36-02',6,'se','dat.sg.n');S('36-02',7,'wif','dat.sg.n');S('36-02',13,'wif','acc.sg.n');S('36-02',17,'thin-poss','dat.sg.n.strong');S('36-02',18,'hus','dat.sg.n');S('36-02',23,'waeter','acc.sg.n');S('36-02',25,'min-poss','dat.pl.m.strong');S('36-02',26,'fot','dat.pl.m');S('36-02',29,'min-poss','acc.pl.m.strong');S('36-02',30,'fot','acc.pl.m');S('36-02',31,'mid','','mid-by-means');S('36-02',32,'he','gen.sg.f','he-possessor')
S('36-03',3,'coss','acc.sg.m');S('36-03',13,'thaet-conjunction');S('36-03',15,'min-poss','acc.pl.m.strong');S('36-03',16,'fot','acc.pl.m')
S('36-04',1,'min-poss','acc.sg.n.strong');S('36-04',2,'heafod','acc.sg.n');S('36-04',[4,12],'mid','','mid-by-means');S('36-04',5,'ele','dat.pl.m');S('36-04',10,'min-poss','acc.pl.m.strong');S('36-04',11,'fot','acc.pl.m');S('36-04',13,'sealf','dat.sg.f')
S('36-05',5,'manig','nom.pl.f.strong');S('36-05',6,'synn','nom.pl.f');S('36-05',8,'wesan','pres.ind.3.pl','wesan-passive');S('36-05',12,'ic','acc.sg')
S('36-06',3,'se','dat.sg.m','se-relative');S('36-06',7,'wesan','pres.ind.3.sg','wesan-passive')
S('36-07',1,'he','nom.sg.n');S('36-07',5,'he','acc.sg.f');S('36-07',7,'wif','dat.sg.n','wif-1')
S('36-08',1,'tha-adverb');S('36-08',4,'mid','','mid-u13-manner-source');S('36-08',5,'ath','dat.sg.m');S('36-08',7,'se','acc.sg.n','se-that');S('36-08',8,'to','','to-inflected-infinitive');S('36-08',11,'hwa','gen.sg.n','hwa-u14-indefinite-source')
S('36-09',1,'tha-adverb');S('36-09',5,'he','gen.sg.f','he-possessor');S('36-09',6,'modor','dat.sg.f');S('36-09',11,'disc','dat.sg.m');S('36-09',13,'se','gen.sg.m');S('36-09',14,'fuluhtere','gen.sg.m');S('36-09',15,'heafod','acc.sg.n')
S('36-10',1,'tha-adverb');S('36-10',8,'se','dat.sg.n')
S('36-11',2,'mann','nom.sg.m','mann-u11-source');S('36-11',5,'heafod','acc.sg.n');S('36-11',7,'disc','dat.sg.m')
S('33-03',26,'witga','acc.sg.m')
S('34-09',15,'aelc','dat.sg.m.strong')
S('34-11',6,'se','dat.sg.n');S('34-11',7,'tempel','dat.sg.n')
# The new composition follows the already selected masculine sǣ system.
S('32-02',14,'se','dat.sg.m');S('32-02',15,'sae','dat.sg.m')
S('32-03',10,'se','dat.sg.m');S('32-03',11,'sae','dat.sg.m')
S('32-06',8,'se','acc.sg.m');S('32-06',9,'sae','acc.sg.m')
S('35-06',13,'thes','dat.sg.m');S('35-06',14,'sae','dat.sg.m')
S('33-01',12,'he','gen.sg.n','he-possessor');S('33-02',7,'he','gen.sg.n','he-possessor');S('33-03',9,'he','gen.sg.n','he-possessor')
S('32-07',6,'aefter','','aefter-u16-follow')
S('32-10',[16,20],'ofer','','ofer-u16-rejoicing');S('32-10',15,'swithe','','swithe-u16-degree')
S('32-06',7,'on','','on-into-goal');S('32-08',[22,34],'on','','on-into-goal')
S('33-03',15,'on','','on-into-goal');S('33-10',6,'on','','on-into-goal')
S('33-02',9,'on','','on-u15-source-during');S('33-03',11,'on','','on-u15-source-during');S('33-10',12,'on','','on-u15-source-during')
S('34-07',10,'on','','on-placement-side-source');S('34-09',7,'on','','on-glory-source')
S('35-13',3,'of','','of-u15-source-partitive')
S('32-08',11,'of-adverb','','of-adverb-u16-off')
S('32-02',4,'swilce','','swilce-u16-sense')
overrides[('32-02',4)]['form_id']='swilce-u16-approximate'
S('36-05',1,'for-thon-the','','for-thon-the-u16-therefore')
S('33-09',7,'on','','on-u16-fishing')
S('36-02',24,'to','','to-u16-body-care')
S('36-07',6,'to','','to-u16-wife-role')
S('35-09',5,'on','','on-u16-clothing')
S('33-10',11,'nawiht','acc.sg','nawiht-u15-nothing')
S('34-13',9,'nawiht','nom.sg.n','nawiht-u16-sense')
D('dēme','deman','imp.2.pl')
S('36-06',1,'laes','acc.sg.n','laes-u16-sense');S('36-06',5,'laes','nom.sg.n','laes-u16-sense')
D('inēode','ingan','pret.ind.1.sg')
for surface,lid,code in [('wind','wind','nom.sg.m'),('nętt','nett','acc.pl.n'),('fisceras','fiscere','nom.pl.m'),('sǣ','sae','dat.sg.f'),
 ('Marian','maria-name','dat.sg.f'),('forlidennesse','forlidennes','acc.sg.f'),('wulfas','wulf','nom.pl.m'),('ęle','ele','dat.sg.m')]:D(surface,lid,code)
for surface,lid in [('æfter','aefter'),('ðonne','thonne'),('ðæt','thaet-conjunction')]:D(surface,lid)

short={'singular':'sg','plural':'pl','masculine':'m','feminine':'f','neuter':'n','nominative':'nom','accusative':'acc','genitive':'gen','dative':'dat','instrumental':'ins'}
short['masculine/feminine']='mf'
def ana(f):
    a=copy.deepcopy(f.get('contextual_analysis') or f.get('analysis',{}))
    if not isinstance(a,dict):
        a=copy.deepcopy(f.get('analysis',{}))
    if not isinstance(a,dict):
        a={'source_description':a}
    if f['form_id']=='hwa-nom-mf-sg':
        a.update({'case':'nom','number':'sg','gender':'mf'})
    descriptive=' '.join(str(a.get(k,'')) for k in ('source_analysis','source_description','contextual_parse'))
    for long, shortname in [('nominative','nom'),('accusative','acc'),('genitive','gen'),('dative','dat'),('instrumental','ins')]:
        if re.search(r'\b'+long+r'\b',descriptive) or re.search(r'\b'+shortname+r'\b',descriptive):a.setdefault('case',shortname)
    for long,shortname in [('singular','sg'),('plural','pl'),('dual','dual')]:
        if re.search(r'\b'+long+r'\b',descriptive) or re.search(r'\b'+shortname+r'\b',descriptive):a.setdefault('number',shortname)
    for long,shortname in [('masculine','m'),('feminine','f'),('neuter','n')]:
        if re.search(r'\b'+long+r'\b',descriptive):a.setdefault('gender',shortname)
    for k,v in list(a.items()):
        if isinstance(v,str):a[k]=short.get(v,v)
    if 'declension' in a and a['declension'] in ('strong','weak'):a.setdefault('strength',a['declension'])
    if 'verb_form' in a:a.setdefault('nonfinite',a['verb_form'])
    if a.get('mood')=='infinitive':a['nonfinite']='infinitive'
    if a.get('participle')=='past':a['nonfinite']='past_participle'
    if a.get('nonfinite')=='past participle':a['nonfinite']='past_participle'
    return a
def match(f,spec):
    a=ana(f)
    for k,v in spec.items():
        if k in ('lemma_id','sense_id','form_id'):continue
        if k=='nonfinite':
            if v=='infinitive' and ('infinitive' in f['form_id'] and 'inflected' not in f['form_id']):continue
            if v=='past_participle' and any(x in f['form_id'] for x in ('participle','-pp-')):continue
        if k=='strength' and a.get(k) is None:continue
        if k=='gender' and a.get(k) is None:continue
        if k=='gender' and a.get(k) in ('all','mf','m/f'):continue
        if a.get(k)!=v:return False
    return True
def priority(lid,f,spec):
    fid=f['form_id']
    canonical='-'.join(str(spec[k]) for k in ('case','number') if k in spec)
    return (0 if f.get('production_taught_in') else 1, 0 if canonical and fid==lid+'-'+canonical else 1,
            1 if 'reference' in fid or 'source' in fid else 0, len(fid),fid)

sequences=[]; errors=[]; decisions=[]
for model in read('sources/audits/unit16-grammar/author-only-cook-models.json')['items']:
    tid=model['source_item_id']; item=tid[-5:]; tokens=[]
    if item=='36-03' and 'inēode' in model['model']:
        for index in (13,15,16):overrides.pop((item,index),None)
        S(item,12,'thaet-conjunction')
        S(item,14,'min-poss','acc.pl.m.strong')
        S(item,15,'fot','acc.pl.m')
    for n,literal in enumerate(model['model'].split(),1):
        surface=literal.strip('.,;:!?‘’“”\"\'()[]')
        key=norm(surface)
        spec=copy.deepcopy(overrides.get((item,n),surface_specs.get(key,{})))
        if 'lemma_id' not in spec and key in fixed_lemma:spec['lemma_id']=fixed_lemma[key]
        if spec.get('lemma_id')=='to':
            spec['form_id']='to-before-inflected-infinitive' if spec.get('sense_id')=='to-inflected-infinitive' else 'to-preposition-dative-invariant'
        candidates=[(lid,f) for lid,f in by_surface[key] if (not spec.get('lemma_id') or lid==spec['lemma_id']) and (not spec.get('form_id') or f['form_id']==spec['form_id']) and match(f,spec)]
        candidates=[(lid,f) for lid,f in candidates if not ('reference' in f['form_id'] or ana(f).get('function')=='citation_only')]
        if not candidates:
            errors.append({'item':item,'token':n,'surface':surface,'problem':'no_matching_form','selector':spec,'available':[{'lemma_id':l,'form_id':f['form_id'],'analysis':ana(f)} for l,f in by_surface[key]][:16]})
            continue
        productive=[x for x in candidates if status(x[1]) in ('previously_taught','new_production')]
        if productive:candidates=productive
        morphs={json.dumps(ana(f),sort_keys=True,ensure_ascii=False) for _,f in candidates}
        if len(morphs)>1 and not spec:
            errors.append({'item':item,'token':n,'surface':surface,'problem':'needs_contextual_selector','available':[{'lemma_id':l,'form_id':f['form_id'],'analysis':ana(f)} for l,f in candidates][:16]})
            continue
        lid,f=sorted(candidates,key=lambda x:priority(x[0],x[1],spec))[0]
        sid=spec.get('sense_id') or sense_selection.get(lid)
        lemma_senses=[s for owner,s in senses.values() if owner==lid]
        if sid is None and len(lemma_senses)==1:sid=lemma_senses[0]['sense_id']
        if sid not in senses or senses[sid][0]!=lid:
            errors.append({'item':item,'token':n,'surface':surface,'problem':'sense_selection','lemma_id':lid,'selected':sid,'available':[s['sense_id'] for s in lemma_senses]})
            continue
        sense=senses[sid][1]
        context=ana(f);context.update({k:v for k,v in spec.items() if k not in ('lemma_id','sense_id','form_id')})
        if f['form_id']=='sendan-infinitive-citation':
            context.update({'nonfinite':'infinitive','infinitive_type':'plain','function':'perceived action of the accusative actor'})
        if f['form_id'] in ('gefyllan-participle-citation','forgiefan-pp-bare-source'):
            context.update({'nonfinite':'past_participle','inflection':'uninflected','function':'predicative past participle in a passive construction'})
        token={'token_index':n,'literal':literal,'surface':surface,'lemma_id':lid,'form_id':f['form_id'],'sense_id':sid,
               'analysis':f['analysis'],'contextual_analysis':context,'form_status':status(f),'sense_status':status(sense),
               'prior_form_production':f.get('production_taught_in'),'prior_sense_production':sense.get('production_taught_in')}
        tokens.append(token)
        decisions.append({'item':item,'token':n,'surface':surface,'form_id':f['form_id'],'sense_id':sid,'context':context,'selector_source':'item' if (item,n) in overrides else 'surface' if key in surface_specs else 'unique_or_same_analysis'})
    sequences.append({'sequence_id':tid+'-MODEL','owner_id':tid,'output_position_id':tid+'-O001','kind':'output','text':model['model'],'tokens':tokens,
        'required_form_ids':sorted({t['form_id'] for t in tokens}),'required_sense_ids':sorted({t['sense_id'] for t in tokens}),
        'status':'contextual_binding_in_progress' if len(tokens)!=len(model['model'].split()) else 'selected_contextual_binding'})
save('author-only-cook-sequence-bindings.json',{'schema_version':1,'chapter':'ch16','visibility':'author_only','status':'contextual_binding_in_progress','sequences':sequences})
save('author-only-cook-binding-review.json',{'schema_version':1,'chapter':'ch16','errors':errors,'decisions':decisions})
scoped=defaultdict(list)
for seq in sequences:
    for t in seq['tokens']:
        for kind in ('form','sense'):
            if t[kind+'_status'] not in ('previously_taught','new_production'):
                scoped[(kind,t[kind+'_id'],t[kind+'_status'])].append(seq['owner_id'][-5:]+':'+str(t['token_index']))
save('cook-support-closure.json',{'schema_version':1,'status':'awaiting_explicit_task_scaffolds','nonproductive_dependencies':[{'kind':k,'id':rid,'status':s,'positions':p} for (k,rid,s),p in scoped.items()]})
print(json.dumps({'sequences':len(sequences),'bound_tokens':sum(len(s['tokens']) for s in sequences),'errors':len(errors)},ensure_ascii=False))
print('\n'.join(e['item']+':'+str(e['token'])+' '+e['surface']+' '+e['problem']+' '+str(e.get('selector',{}))+' '+','.join(x['form_id'] for x in e.get('available',[]) if isinstance(x,dict)) for e in errors))
