"""One-use independent review ledger assembler; expectations transcribed/reasoned by reviewer.

This is not an authoring generator and never changes masters or the coverage contract.
The independently specified lexical stems, endings and analyses below are compared
with BOTH actual learner tables and canonical logical cells before routes are recorded.
"""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(path): return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))
def digest(raw): return hashlib.sha256(raw).hexdigest()
def identity(path):
    raw=(ROOT/path).read_bytes()
    return {'path':path,'raw_sha256':digest(raw),'normalized_lf_sha256':digest(raw.replace(b'\r\n',b'\n'))}
def norm(a):
    aliases={'singular':'sg','plural':'pl','nominative':'nom','genitive':'gen','dative':'dat','accusative':'acc','instrumental':'ins','masculine':'m','feminine':'f','neuter':'n'}
    return {k:aliases.get(v,v) if isinstance(v,str) else v for k,v in a.items()}
def akey(a): return json.dumps(norm(a),sort_keys=True,ensure_ascii=False)
def image(path): return 'sources/audits/'+path
M={}
def add(pid,headers,rows,positions,reason,evidence,scope):
    assert pid not in M
    M[pid]={'headers':headers,'rows':rows,'positions':positions,'reason':reason,'evidence':[image(p) for p in evidence],'scope':scope}
CASES=[('nom','Nominative'),('gen','Genitive'),('dat','Dative'),('acc','Accusative')]
def noun(tag,forms,gender,reason,evidence):
    # forms are reviewer-specified N/G/D/A, first singular then any assigned plural.
    numbers=['sg','pl'] if len(forms)==8 else ['sg']
    rows=[]; pos=[]
    for r,(case,label) in enumerate(CASES):
        row=[label]
        for col,num in enumerate(numbers,1):
            form=forms[(col-1)*4+r];row.append(form)
            pos.append((r,col,form,{'case':case,'number':num,'gender':gender},'new_production'))
        rows.append(row)
    scope='All four cases in '+('both numbers' if len(forms)==8 else 'the explicitly bounded singular')+'; familiar basic noun functions. No unassigned number or advanced construction is inferred.'
    add('NEW-U16-NOM-'+tag,['Case','Singular']+(['Plural'] if len(forms)==8 else []),rows,pos,reason,evidence,scope)
def masc(tag,stem,evidence,extra='',singular=False):
    forms=[stem,stem+'es',stem+'e',stem]
    if not singular:forms += [stem+'as',stem+'a',stem+'um',stem+'as']
    noun(tag,forms,'m','Strong masculine stem '+stem+'; singular zero/-es/-e/zero and plural -as/-a/-um/-as. '+extra,['unit01-source/nominal-3.png']+evidence)
masc('NEAHGEBUR','nēahgebūr',['unit16-source/exercise-002.png'])
masc('THOTHOR','ðoðor',['unit01-source/nominal-4.png','unit16-source/fb-p318.png'],'Short first syllable licenses retained medial o; no invented ðoðr- stem.')
masc('COSS','coss',['unit16-source/exercise-005.png'])
masc('DISC','disc',['unit16-source/exercise-005.png'])
masc('ATH','āð',['unit16-source/exercise-005.png'])
masc('TEAR','tēar',['unit16-source/fb-p315.png'])
masc('MAEGENTHRYMM','mægenðrymm',['unit16-source/ex-p49.png','unit16-source/fb-p318.png'],'The majesty sense is bounded to singular.',True)
noun('FULUHTERE',['fuluhtere','fuluhteres','fuluhtere','fuluhtere'],'m','The -ere class retains final e in dative singular and adds only -s in the genitive; Baptist title is explicitly singular.',['unit01-source/nominal-5.png','unit16-source/exercise-005.png'])
for tag,stem in [('CNAPA','cnap'),('GEGIERELA','gegierel')]:
    noun(tag,[stem+'a',stem+'an',stem+'an',stem+'an',stem+'an',stem+'ena',stem+'um',stem+'an'],'m','Weak masculine '+stem+'- has nominative singular -a, other singular and nominative/accusative plural -an, genitive plural -ena, dative plural -um.',['unit01-source/nominal-12.png','unit16-source/fb-p292.png' if tag=='GEGIERELA' else 'unit16-source/fb-p168.png'])
for tag,stem in [('FURLANG','furlang'),('NETT','nętt')]:
    noun(tag,[stem,stem+'es',stem+'e',stem,stem,stem+'a',stem+'um',stem],'n','Neuter zero nominative/accusative in both numbers, -es/-e singular obliques and -a/-um plural obliques. '+('Heavy furlang follows word.' if tag=='FURLANG' else 'Nett expressly follows cyn(n), Wright356; zero plural is lexical ja-stem behavior, not a universal geminate rule.'),['unit16-source/fb-p32.png','unit16-source/exercise-001.png']+(['unit16-source/wright-p174.png','unit16-source/wright-p175.png'] if tag=='NETT' else []))
noun('TEMPEL',['tempel','temples','temple','tempel','templu','templa','templum','templu'],'n','Tempel syncopates to templ- before every ending; -u survives in nominative/accusative plural.',['unit16-source/fb-p33.png','unit16-source/fb-p315.png'])
noun('MAEDEN',['mǣden','mǣdenes','mǣdene','mǣden','mǣden','mǣdena','mǣdenum','mǣden'],'n','The selected -en neuter retains medial e throughout; heavy full stem has zero nominative/accusative plural. Do not import templ-/wolcn- syncope.',['unit16-source/fb-p33.png','unit16-source/ex-p49.png'])
noun('WOLCEN',['wolcen','wolcnes','wolcne','wolcen','wolcnu','wolcna','wolcnum','wolcnu'],'n','Wolcen uses wolcn- with vowel endings, including nominative/accusative plural -u; differs from selected mǣden.',['unit16-source/fb-p33.png','unit16-source/ex-p43.png'])
for tag,stem,plural in [('STEFN','stefn',True),('SPRAEC','sprǣc',True),('ANSIEN','ansīen',False),('SEALF','sealf',False),('WEN','wēn',False),('SMYLTNES','smyltnes',False)]:
    oblique='smyltness' if tag=='SMYLTNES' else stem
    forms=[stem,oblique+'e',oblique+'e',stem if tag=='WEN' else oblique+'e']
    if plural:forms += [oblique+'a',oblique+'a',oblique+'um',oblique+'a']
    note='Strong feminine singular -e in genitive/dative and ordinarily accusative; assigned plural has -a/-a/-um/-a. '
    if tag=='WEN':note+='Lexically specified §51.1 exception retains wēn in accusative singular.'
    if tag=='SMYLTNES':note+='-nes doubles s before endings under §51.5.'
    evidence=['unit01-source/nominal-10.png']
    evidence += {'STEFN':['unit16-source/ex-p66.png'],'SPRAEC':['unit16-source/exercise-003.png'],'ANSIEN':['unit16-source/ex-p43.png'],'SEALF':['unit16-source/exercise-005.png'],'WEN':['unit16-source/fb-p321.png'],'SMYLTNES':['unit01-source/nominal-11.png','unit16-source/ex-p42.png']}[tag]
    noun(tag,forms,'f',note,evidence)

def adjective(tag,stem,heavy=False,alternating=False):
    cols=[('m','sg'),('f','sg'),('n','sg'),('m','pl'),('f','pl'),('n','pl')]
    endings={
      ('strong','nom'):['','' if heavy else 'u','','e','a','' if heavy else 'u'],
      ('strong','gen'):['es','re','es','ra','ra','ra'],
      ('strong','dat'):['um','re','um','um','um','um'],
      ('strong','acc'):['ne','e','','e','a','' if heavy else 'u'],
      ('strong','ins'):['e',None,'e',None,None,None],
      ('weak','nom'):['a','e','e','an','an','an'],
      ('weak','gen'):['an','an','an','ra','ra','ra'],
      ('weak','dat'):['an','an','an','um','um','um'],
      ('weak','acc'):['an','an','e','an','an','an']}
    rows=[];positions=[]
    labels=dict(CASES);labels['ins']='Instrumental'
    for r,((strength,case),ends) in enumerate(endings.items()):
        row=[strength.title()+' '+labels[case].lower()]
        for col,((gender,num),ending) in enumerate(zip(cols,ends),1):
            if ending is None:form='—'
            elif alternating:
                form='nearu' if ending in ['','u'] else ('nearo' if ending in ['ne','re','ra'] else 'nearw')+ending
            else:form=stem+ending
            row.append(form)
            if ending is not None:positions.append((r,col,form,{'case':case,'number':num,'gender':gender,'strength':strength},'new_recognition' if case=='ins' else 'new_production'))
        rows.append(row)
    note='Independently reconstructed every gender/number/case in strong and weak series, including weak neuter nominative/accusative singular -e, common plural -an/-ra/-um, and masculine/neuter singular instrumental -e. '
    note += 'Heavy healt has zero feminine nominative singular and neuter nominative/accusative plural.' if heavy else 'Uncontracted '+stem+'- retains the full stem and -u in feminine nominative singular and neuter nominative/accusative plural, permitted by Cook57.3.'
    evidence=['unit16-source/fb-p39.png','unit16-source/fb-p40.png','unit16-source/fb-p41.png']
    if alternating:
        note='The full strong/weak ending matrix is independently reconstructed. Nearu remains in zero/-u positions; nearw- precedes vowel endings and nearo- precedes -ne/-re/-ra, including WEAK genitive plural nearora. Instrumentals nearwe are recognition only.'
        evidence += ['unit16-source/wright-p215.png']
    add('NEW-U16-ADJ-'+tag,['Series / case','M sg','F sg','N sg','M pl','F pl','N pl'],rows,positions,note,evidence,'48 productive cells; two masculine/neuter singular instrumental cells recognition only. Dashes are nonapplicable positions, not assigned or derivable cells. Basic attributive/predicate uses; supplied reading participles remain separate.')
adjective('HEALT','healt',True)
adjective('GELARED','gelǣred')
adjective('EORTHLIC','eorðlic')
adjective('NEARU','nearu',alternating=True)
rows=[];positions=[]
for r,(case,label) in enumerate(CASES):
    forms=['bēgen','bā','bā'] if case in ['nom','acc'] else ['bēgra']*3 if case=='gen' else ['bǣm']*3
    rows.append([label]+forms)
    for col,(gender,form) in enumerate(zip(['m','f','n'],forms),1):positions.append((r,col,form,{'case':case,'number':'pl','gender':gender},'new_production'))
add('NEW-U16-NOM-BEGEN',['Case','M plural','F plural','N plural'],rows,positions,'Bēgen follows twēgen: masculine bēgen, feminine/neuter bā, genitive bēgra, dative bǣm. Twelve separate assignments, no singular or separate dual. Neuter bū and dative bām are valid alternatives.',['unit16-source/fb-p48.png','unit16-grammar/fb-p167.png'],'Productive plural-only both; modifier and apposition, including unc/inc bǣm. Dual pronouns do not require an invented dual bēgen paradigm.')

def indicative(tag,pres,past,reason,evidence):
    # Each reviewer vector specifies 1sg,2sg,3sg,and common plural.
    rows=[];positions=[]
    for r,(person,num) in enumerate([(1,'sg'),(2,'sg'),(3,'sg'),(1,'pl'),(2,'pl'),(3,'pl')]):
        row=[f'{person} {num}']
        for col,(tense,vector) in enumerate([('present',pres),('preterite',past)],1):
            form=vector[person-1 if num=='sg' else 3];row.append(form)
            positions.append((r,col,form,{'tense':tense,'mood':'indicative','person':person,'number':num},'new_production'))
        rows.append(row)
    add('NEW-U16-PAR-'+tag+'-IND',['Person / number','Present','Preterite'],rows,positions,reason,evidence,'Complete twelve-position present/preterite indicative for the stated sense/frame; homographic persons remain separate assignments. Other moods and nonfinite uses are only productive when separately taught.')
for tag,stem,lex in [('AESWICIAN','ǣswic','unit16-grammar/bt_b0020.jpg'),('BLISSIAN','bliss','unit14-grammar/fb-p279.png'),('WULDRIAN','wuldr','unit15-grammar/fb-p323.png'),('PLEGIAN','pleg','unit14-grammar/fb-p309.png'),('BEHEAFDIAN','behēafd','unit16-source/exercise-005.png'),('CLEOPIAN','cleop','unit16-source/fb-p168.png')]:
    indicative(tag,[stem+'ie',stem+'ast',stem+'að',stem+'iað'],[stem+'ode',stem+'odest',stem+'ode',stem+'odon'],'Weak-II stem '+stem+'-: checked -ie/-ast/-að/-iað present and -ode/-odest/-ode/-odon past; neither optional g nor unselected past-vowel variants enter targets. Lexical sense/frame is separately stated.',['unit15-grammar/fb-p73.png','unit15-grammar/fb-p74.png',lex])
indicative('ARISAN',['ārīse','ārīst','ārīst','ārīsað'],['ārās','ārise','ārās','ārison'],'Strong I: present ī, contracted second/third singular -st, past first/third ā and second singular/plural i. Prefix ā- retained. Prior subjunctive does not itself establish these indicative cells.',['unit15-grammar/fb-p54.png','unit15-grammar/fb-p55.png','unit14-grammar/fb-p59.png','unit14-grammar/fb-p60.png'])
indicative('ACEORFAN',['āceorfe','ācierfst','ācierfð','āceorfað'],['ācearf','ācurfe','ācearf','ācurfon'],'Strong III: present eo except mutation to ie in second/third singular; past first/third ea and second/plural u. Prefix ā- retained; plural persons share surface but not assignment.',['unit15-grammar/fb-p54.png','unit15-grammar/fb-p55.png','unit15-grammar/fb-p61.png','unit15-grammar/fb-p62.png','unit04-grammar/wright-p258-pdf278.png'])
indicative('FORLEOSAN',['forlēose','forlīest','forlīest','forlēosað'],['forlēas','forlure','forlēas','forluron'],'Strong II: ēo/īe present, contracted second/third singular, ēa first/third past and u second/plural, with s changing to r in second/plural past; lexical loss takes accusative.',['unit15-grammar/fb-p54.png','unit15-grammar/fb-p55.png','unit14-grammar/fb-p60.png','unit15-grammar/fb-p61.png','unit15-grammar/fb-p288.png'])
indicative('IERNAN',['ierne','iernst','iernð','iernað'],['arn','urne','arn','urnon'],'Strong III exceptional present iern-; past arn first/third singular, urn- second/plural. Checked against Wright and lexical run sense, not a regular weak guess.',['unit15-grammar/fb-p54.png','unit15-grammar/fb-p55.png','unit04-grammar/wright-p258-pdf278.png','unit16-source/fb-p301.png'])
indicative('THWEAN',['ðwēa','ðwiehst','ðwiehð','ðwēað'],['ðwōh','ðwōge','ðwōh','ðwōgon'],'Contracted strong VI: ðwēa-/ðwieh- present and ðwōh singular1/3 versus ðwōg- second/plural past. A valid singular g variant is distinguished from selected h; material/liquid frame is explicit.',['unit14-grammar/fb-p65.png','unit05-grammar/wright-p262-pdf282.png','unit05-grammar/wright-p263-pdf283.png','unit16-source/exercise-005.png'])
indicative('BEWENDAN',['bewęnde','bewęntst','bewęnt','bewęndað'],['bewęnde','bewęndest','bewęnde','bewęndon'],'Weak I dental stem: second singular -ntst, third -nt; past dental simplification yields bewęnde rather than *bewęndde. Homographic first/third past and first present require context; reflexive dative is a bounded construction.',['unit15-grammar/fb-p69.png','unit15-grammar/fb-p72.png','unit14-grammar/fb-p279.png','unit14-grammar/fb-p100.png'])
indicative('SMIERWAN',['smierwe','smierest','smiereð','smierwað'],['smierede','smieredest','smierede','smieredon'],'Weak I rw subclass as gierwan: w in present1/plural, absent in second/third and selected past smiered-. Consistent ie selection; BT i/y variants remain valid language.',['unit15-grammar/fb-p68.png','unit15-grammar/fb-p69.png','unit06-grammar/wright-p270-pdf290.png','unit06-grammar/wright-p271-pdf291.png','unit06-grammar/wright-p274-pdf294.png','unit16-grammar/bt_b0889.jpg'])
indicative('ALIESAN',['ālīese','ālīest','ālīest','ālīesað'],['ālīesde','ālīesdest','ālīesde','ālīesdon'],'Long weak-I ālīes- stem: selected contracted -st second/third present; past -de/-dest/-don. Weak deliver is distinct from strong lose forlēosan and impersonal permit ālīefan.',['unit15-grammar/fb-p68.png','unit15-grammar/fb-p72.png','unit16-grammar/ex-p44.png'])

def pair(tag,kind,forms,reason,evidence):
    if kind=='IMP':labels=['imperative, 2, sg','imperative, 2, pl'];analyses=[{'mood':'imperative','person':2,'number':n} for n in ['sg','pl']]
    elif kind=='PART':labels=['participle, present','participle, past'];analyses=[{'nonfinite':'participle','tense':t,'inflection':'base'} for t in ['present','past']]
    else:labels=['infinitive','infinitive, dat'];analyses=[{'nonfinite':'infinitive','inflection':'plain'},{'nonfinite':'infinitive','inflection':'inflected','case':'dat'}]
    rows=[[label,form] for label,form in zip(labels,forms)]
    positions=[(r,1,form,analyses[r],'new_production') for r,form in enumerate(forms)]
    scope={'IMP':'Both ordinary second-person numbers; no complete new finite tense system is silently assigned. Shortened plural before following pronoun is separately taught for dēme gē.', 'PART':'Both participial bases; basic passive/predicative and separately taught attributive uses only, not every participial construction.','INF':'Plain and inflected infinitive; tō remains separate, and syntax follows the taught purpose/perception frames.'}[kind]
    add('NEW-U16-PAR-'+tag+'-'+kind,['Position','Form'],rows,positions,reason,evidence,scope)
for tag,forms,extra,evidence in [
 ('ACEORFAN',['āceorf','āceorfað'],'Strong present eo stem, not mutated indicative ie.',['unit15-grammar/fb-p61.png']),
 ('BLISSIAN',['blissa','blissiað'],'Weak-II -a versus -iað.',['unit15-grammar/fb-p73.png']),
 ('SMIERWAN',['smiere','smierwað'],'Rw-subclass singular loses w; plural retains it.',['unit06-grammar/wright-p270-pdf290.png','unit06-grammar/wright-p274-pdf294.png']),
 ('ARISAN',['ārīs','ārīsað'],'Class-I ī retained in both commands.',['unit14-grammar/fb-p59.png']),
 ('FORLAETAN',['forlǣt','forlǣtað'],'Lǣtan present stem, not preterite lēt-.',['unit15-grammar/fb-p67.png','unit15-grammar/fb-p288.png']),
 ('GESWICAN',['geswīc','geswīcað'],'Class-I present ī; cessation/work frame separately governed.',['unit14-grammar/fb-p59.png','unit16-grammar/bt_b0449.jpg']),
 ('EFTHWEORFAN',['ęfthweorf','ęfthweorfað'],'StrongIII return present eo, retained prefix ęft-.',['unit16-source/fb-p284.png']),
 ('DEMAN',['dēm','dēmað'],'Long weak-I bare singular; dēme gē is a separately conditioned plural alternative.',['unit15-grammar/fb-p72.png','unit06-grammar/wright-p270-pdf290.png'])]:
    pair(tag,'IMP',forms,'Independent command pair: '+extra,['unit15-grammar/fb-p55.png']+evidence)
for tag,stem,evidence in [('FINDAN','find',['unit15-grammar/fb-p62.png','unit15-grammar/fb-p104.png','unit15-grammar/fb-p105.png']),('FEDAN','fēd',['unit15-grammar/fb-p72.png','unit06-grammar/wright-p271-pdf291.png','unit15-grammar/fb-p105.png'])]:
    rows=[];positions=[]
    for r,(person,num) in enumerate([(1,'sg'),(2,'sg'),(3,'sg'),(1,'pl'),(2,'pl'),(3,'pl')]):
        form=stem+('e' if num=='sg' else 'en');rows.append([f'{person} {num}',form]);positions.append((r,1,form,{'tense':'present','mood':'subjunctive','person':person,'number':num},'new_production'))
    add('NEW-U16-PAR-'+tag+'-PRES-SUBJ',['Person / number','Present'],rows,positions,'Unmutated present stem '+stem+'- plus singular -e or plural -en. All three persons in each number remain distinct logical positions despite homography.',['unit15-grammar/fb-p55.png']+evidence,'Complete six-position present subjunctive; hypothesis/expectation/indefinite relative uses taught explicitly, no universal dependent-clause rule.')
for tag,forms,note,evidence in [
 ('FORLEOSAN',['forlēosende','forloren'],'Present ēos-, strong past or- with s/r alternation; strong neuter accusative forloren modifies scēap in32.11.',['unit14-grammar/fb-p60.png','unit15-grammar/fb-p288.png']),
 ('LAEDAN',['lǣdende','lǣded'],'Regular weak-I -ende / selected uncontracted -ed, permitting ordinary passive carry/lead sense.',['unit15-grammar/fb-p68.png','unit16-source/fb-p301.png']),
 ('GEFYLLAN',['gefyllende','gefylled'],'Present and weak past participial bases retain ll; fulfil-prediction sense is explicitly taught, distinct from physical fill.',['unit15-grammar/fb-p68.png','unit16-source/fb-p292.png','unit16-source/exercise-002.png']),
 ('FORGIEFAN',['forgiefende','forgiefen'],'Class-V -giefen past participle; forgiveness frame retains dative person while sin becomes nominative passive subject.',['unit15-grammar/fb-p63.png','unit16-source/exercise-005.png'])]:
    pair(tag,'PART',forms,note,['unit15-grammar/fb-p54.png','unit15-grammar/fb-p55.png','unit14-grammar/fb-p100.png']+evidence)
pair('IERNAN','INF',['iernan','iernanne'],'Iern- present stem plus plain -an or inflected -anne; perception actor is accusative.',['unit15-grammar/fb-p55.png','unit15-grammar/fb-p106.png','unit16-source/fb-p168.png'])
pair('SENDAN','INF',['sęndan','sęndanne'],'Sęnd- present stem plus plain -an or inflected -anne; visible infinitive hint in32.6 is a reference cue, not unaided spelling recall.',['unit15-grammar/fb-p55.png','unit15-grammar/fb-p106.png','unit16-source/exercise-001.png'])

def literal_table(student,mid):
    marker='<!-- table: '+mid+' -->'
    assert student.count(marker)==1,(mid,'marker count')
    before,after=student.split(marker)
    lines=after.splitlines(); start=next(i for i,v in enumerate(lines) if v.startswith('|'))
    table=[]
    for line in lines[start:]:
        if not line.startswith('|'):break
        table.append([p.strip() for p in line.strip().strip('|').split('|')])
    assert len(table)>=3
    assert all(re.fullmatch(r':?-+:?',v) for v in table[1])
    firstline=before.count('\n')+1+start
    return table[0],table[2:],firstline

def main():
    args=argparse.ArgumentParser();args.add_argument('--accept',action='store_true');args.add_argument('--prose-verified',action='store_true');opt=args.parse_args()
    c=read('chapters/ch16/coverage.json');student=(ROOT/'chapters/ch16/student.md').read_text(encoding='utf-8');key=(ROOT/'chapters/ch16/answer-key.md').read_text(encoding='utf-8')
    inspections=read('build/u16-paradigms-image-notes.json')
    for record in inspections:record['raw_sha256']=identity(record['path'])['raw_sha256']
    viewed={r['path'] for r in inspections}
    paradigms={p['paradigm_id']:p for p in c['paradigms']}
    assert set(M)==set(paradigms) and len(M)==56
    checks=[];routes=[];unassigned=0;nonapplicable=[]
    for pid,e in M.items():
        assert set(e['evidence'])<=viewed,(pid,'evidence not actually viewed')
        p=paradigms[pid];mid=pid+'-DISPLAY';headers,rows,line=literal_table(student,mid)
        assert headers==e['headers'],(pid,'header',headers,e['headers'])
        assert rows==e['rows'],(pid,'literal table differs from independent reconstruction',rows,e['rows'])
        display=next(m for m in c['display_plan']['matrices'] if m['matrix_id']==mid)
        assert display['headers']==headers and display['rows']==rows
        expected={akey(a):(r,col,form,a,status) for r,col,form,a,status in e['positions']}
        actual={akey(cell.get('contextual_analysis',cell['analysis'])):cell for cell in p['cells']}
        assert len(actual)==len(p['cells'])==len(expected),(pid,'duplicate or missing analysis')
        assert set(actual)==set(expected),(pid,'analyses',set(actual)^set(expected))
        ids=[]
        for ak,(r,col,form,analysis,status) in expected.items():
            cell=actual[ak];cid=cell.get('cell_id',cell.get('form_id'));ids.append(cid)
            assert cell['form']==form,(pid,cid,'form')
            assert cell['knowledge_status']==status,(pid,cid,'scope')
            assert display['cell_logical_ids'][r][col]==cid,(pid,cid,'route')
            assert display['cell_knowledge_statuses'][r][col]==status
            assert set(display['cell_form_ids'][r][col])==set(cell.get('form_ids',[cell['form_id']]))
            routes.append({'paradigm_id':pid,'logical_cell_id':cid,'status':'accepted','form':form,'analysis':analysis,'knowledge_status':status,'learner_location':{'path':'chapters/ch16/student.md','matrix_id':mid,'markdown_line':line+2+r,'row_label':rows[r][0],'column_label':headers[col]},'independent_expected_form':form,'evidence':e['evidence'],'reason':e['reason']+' Exact case/person/number/mood/series assignment and literal display checked; '+('recognition only, with no independent production task' if status=='new_recognition' else 'productive within the stated basic scope')+'.'})
        for r,row in enumerate(rows):
            for col,value in enumerate(row[1:],1):
                if value=='—':
                    assert display['cell_logical_ids'][r][col] is None and display['cell_form_ids'][r][col]==[]
                    unassigned+=1
                    nonapplicable.append({'matrix_id':mid,'data_row_zero_based':r,'column_zero_based_including_label':col,'row_label':row[0],'column_label':headers[col],'status':'not_applicable','logical_cell_id':None})
        checks.append({'paradigm_id':pid,'status':'accepted','checked_logical_cell_ids':ids,'mismatches':[],'independent_language_check':e['reason'],'scope_check':e['scope'],'primary_evidence':e['evidence'],'literal_display_checked':True})
    assert len(routes)==564 and unassigned==16
    assert Counter(r['knowledge_status'] for r in routes)=={'new_production':556,'new_recognition':8}
    assert len(c['assigned_items'])==76 and sum(len(t['output_positions']) for t in c['assigned_items'])==179
    # Validate the explicit override without rewriting or treating the sealed source as current.
    active_override=c['selected_model_corrections']['path']
    amended=read(active_override);sealed=read(amended['source'])
    historical_a03=read('chapters/ch16/model-binding-amendments.json')
    assert identity(amended['source'])['raw_sha256']==historical_a03['source_sha256']
    originals={s['sequence_id']:s for s in sealed['sequences']};effective=dict(originals);text_changes=[]
    for s in amended['corrected_sequences']:
        original_text=originals[s['sequence_id']]['text']
        if s['text']!=original_text:
            assert s['sequence_id']=='EX-XII-XIII-34-06-MODEL'
            assert s['text']==original_text.replace('sęcge gif ðū sīe','sęcge hwæðer ðū sīe',1)
            text_changes.append({'sequence_id':s['sequence_id'],'original_text':original_text,'accepted_current_text':s['text'],'reason':'Explicit A06 scope repair: invariant hwæðer whether was actually taught and assessed in ch09; conditional gif alone did not establish its interrogative sense. Fulk p286 independently confirms the conjunction. All other model text is unchanged.'})
        effective[s['sequence_id']]=s
    assert len(effective)==59 and sum(len(s['tokens']) for s in effective.values())==812
    if text_changes:
        changed=effective['EX-XII-XIII-34-06-MODEL'];token=changed['tokens'][11]
        assert changed['text'] in key
        assert token['lemma_id']=='hwaether-conjunction' and token['form_id']=='hwaether-conjunction-invariant' and token['sense_id']=='hwaether-whether'
        assert token['prior_form_production']==token['prior_sense_production']=='ch09'
        assert token['assessment_role']=='independent_production'
    given=[]
    for s in effective.values():
        task=s['owner_id'];marker='<!-- item: '+task+' -->';assert marker in student
        chunk=student.split(marker,1)[1].split('<!-- item:',1)[0]
        for t in s['tokens']:
            if t.get('assessment_role')=='given_dictionary_form_position_identification_not_unaided_recall':
                ref=t['given_reference'];assert ref['exact_parenthesis'] in chunk,(task,ref)
                assert t['surface'].casefold()==ref['hint_text'].casefold(),(task,t['surface'],ref['hint_text'])
                given.append({'task_id':task,'token_index':t['token_index'],'surface':t['surface'],'exact_visible_hint':ref['exact_parenthesis']})
    assert len(given)==38
    roles=Counter(t['assessment_role'] for s in effective.values() for t in s['tokens'])
    assert roles=={'independent_production':603,'supplied_position_not_unaided_recall':171,'given_dictionary_form_position_identification_not_unaided_recall':38}
    nett=next(t for t in effective['EX-XII-XIII-32-06-MODEL']['tokens'] if t['surface']=='nętt')
    assert norm(nett['contextual_analysis'])['number']=='sg'
    lifecycle={'status','review_status','completion','amendments','textual_review','presentation_review','contract_checkpoint','complete_drafts_checkpoint','independent_solutions_checkpoint','accepted_text_checkpoint'}
    semantic_keys=sorted(set(c)-lifecycle)
    semantic={'keys':semantic_keys,'sha256':digest(json.dumps({k:c[k] for k in semantic_keys},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8'))}
    artifacts=[identity('chapters/ch16/'+name) for name in ['student.md','answer-key.md']]
    findings=[
      {'finding_id':'U16-PAR-01','status':'open','severity':'material','location':'chapters/ch16/student.md:274, Strong feminine nouns; NEW-U16-NOM-WEN governing rules','observed_problem':'The blanket other-singular-cases -e statement contradicts the correct accusative wēn table and Cook lexical exception.','source_evidence':['sources/audits/unit16-source/fb-p321.png','sources/audits/unit01-source/nominal-10.png'],'source_locator':'Cook p.321 s.v. wēn (51.1), p.35 §51.1','suggested_repair':'State ordinary genitive/dative/accusative -e and explicitly except wēn accusative singular; correct any current rule that treats this as ordinary51b. Preserve the table.'},
      {'finding_id':'U16-PAR-02','status':'open','severity':'material','location':'chapters/ch16/student.md:448, nearu paragraph','observed_problem':'The weak forms use nearw- is unqualified, although the correct weak genitive plural is nearora.','source_evidence':['sources/audits/unit16-source/wright-p215.png','sources/audits/unit16-source/fb-p41.png'],'source_locator':'Wright p.215 §§435–436 and Cook p.41 §60 weak genitive plural -ra','suggested_repair':'Add the weak genitive plural nearora exception to the nearw- statement; preserve all table forms.'},
      {'finding_id':'U16-PAR-03','status':'open','severity':'material_metadata','location':'chapters/ch16/model-binding-amendments.json effective model contextual analyses; exact coordinates in build/u16-paradigms-context-findings.json','observed_problem':'Current contextual_analysis inherits source-specific labels that contradict the actual token: speech-addressee tō for destination/body-care/wife-role, mediator ðurh for an oath, proportional swā for free-choice, indefinite Hwā for an interrogative, and ēstas object-relative labels for current subject/route/recipient relatives. Nearby inherited context labels are also corrected in the grouped proposal.','source_evidence':['sources/audits/unit16-source/exercise-001.png','sources/audits/unit16-source/exercise-002.png','sources/audits/unit16-source/exercise-003.png','sources/audits/unit16-source/exercise-004.png','sources/audits/unit16-source/exercise-005.png','sources/audits/unit14-grammar/fb-p93.png','sources/audits/unit15-grammar/fb-p104.png','sources/audits/unit15-grammar/fb-p105.png','sources/audits/unit15-grammar/fb-p106.png'],'source_locator':'Original prompts32–36 and their actual current model strings; contextual grammar follows the explicitly taught/supplied constructions.','suggested_repair':'Override only the 37 specified current contextual fields. Preserve raw historical analysis, sealed packet, all model text, forms, senses, roles and tasks.'}]
    context_repairs=read('build/u16-paradigms-context-findings.json')['repairs']
    actual_context_repairs=[]
    input_mirror_checks=[]
    for repair in context_repairs:
        token=next(t for t in effective[repair['sequence_id']]['tokens'] if t['token_index']==repair['token_index'])
        assert token['surface']==repair['expected_surface']
        value=token['contextual_analysis'][repair['contextual_analysis_key']]
        actual_context_repairs.append({**repair,'actual_current_value':value,'status':'verified' if value==repair['proposed_value'] else 'pending'})
        for task in c['assigned_items']:
            for seq in task.get('input_sequences',[]):
                if seq.get('source_model_sequence_id')!=repair['sequence_id']:continue
                for inp in seq.get('tokens',[]):
                    if inp.get('source_model_token_index')!=repair['token_index']:continue
                    current=inp['contextual_analysis'][repair['contextual_analysis_key']]
                    input_mirror_checks.append({'task_id':task['task_id'],'input_sequence_id':seq['sequence_id'],'input_token_index':inp['token_index'],'source_model_sequence_id':repair['sequence_id'],'source_model_token_index':repair['token_index'],'surface':inp['surface'],'key':repair['contextual_analysis_key'],'expected_value':repair['proposed_value'],'actual_value':current,'status':'verified' if current==repair['proposed_value'] else 'pending'})
    if opt.accept or opt.prose_verified:
        # Human reviewer must have read the actual repair before requesting --accept.
        assert 'Their other singular cases have -e' not in student
        assert re.search(r'wēn.{0,220}accusative|accusative.{0,220}wēn',student,re.I)
        assert 'The weak forms use nearw-.' not in student
        assert 'nearora' in student
        for f in findings[:2]:
            f['status']='resolved_verified'
            f['resolution']='Verified the actual repaired learner wording and current canonical rule after A04; correct literal tables and all564 routes remain unchanged.'
    if opt.accept:
        assert all(r['status']=='verified' for r in actual_context_repairs)
        assert all(r['status']=='verified' for r in input_mirror_checks)
        assert len(input_mirror_checks)==16 and len(text_changes)==1
        findings[2]['status']='resolved_verified'
        findings[2]['resolution']='Verified all37 repaired model contextual fields and every linked supplied-input mirror against the actual clauses. A05 preserves all model strings; the separate declared A06 hwæðer repair is recorded below. All812 token positions and assessment-role counts remain unchanged.'
    open_findings=[f['finding_id'] for f in findings if f['status']=='open']
    ledger={
      'schema_version':'1.0','chapter_id':'ch16','reviewer':'unit16_paradigms','status':'accepted' if opt.accept else 'pending_material_repairs',
      'independence':{'no_current_author_role':True,'role':'Fresh non-author paradigm/scope reviewer; key comparison permitted. This is separate from the blind all-task solver.','no_shared_file_edits':True,'inspection_method':'Personally opened every listed primary image with view_image; independently reconstructed the morphology and reviewed learner rules/scopes. Computation only compares these reviewer expectations with literal learner tables and canonical coordinates.'},
      'counts':{'paradigms':56,'logical_cells':564,'productive_cells':556,'recognition_only_cells':8,'missing_assigned_logical_cells':0,'unassigned_logical_cells':0,'derived_only_cells':0,'nonapplicable_dashes':16,'tasks':76,'requested_output_positions':179,'primary_images_actually_viewed':len(inspections),'material_open_findings':len(open_findings)},
      'nonapplicable_visual_positions':nonapplicable,
      'paradigm_checks':checks,'cell_route_checks':routes,'material_open_findings':open_findings,'findings':findings,
      'primary_evidence_image_inspections':inspections,
      'reviewed_artifact_identities':artifacts,'reviewed_contract_semantic_identity':semantic,
      'accepted_artifact_identities':artifacts if opt.accept else [],'accepted_contract_semantic_identity':semantic if opt.accept else {},
      'prior_scope_checks':{
        'actual_files_read':[identity(f'chapters/ch{i:02d}/coverage.json') for i in range(1,16)]+[identity('lexicon/entries.json'),identity('curriculum/grammar.json')],
        'findan':'Actual ch04 NEW-U04-PAR-findan and cumulative lexicon select fand first singular and funde third singular. Cook p.62 expressly supports third-singular funde; Wright p.258 also permits funde in first singular. Learner906 preserves selected forms and key32.11 accepts funde as valid alternative. No correction required.',
        'arisan':'Actual ch14 taught complete subjunctive systems, not the new indicative/imperative systems; unit16 explicitly adds the latter.',
        'cleopian':'Actual ch15 command pair and summon-person frame do not license all indicative cells or cry-out sense; unit16 now explicitly supplies the full indicative and new cry frame.',
        'aliesan':'Prior command pair/reference principal parts did not constitute full indicative teaching; this unit supplies all twelve indicative assignments.',
        'nominal_and_verbal_reuse':'The actual earlier contracts establish noun/adjective and strong/weak patterns; present chapter still explicitly selects each new lexeme, stem, sense and productive position. Earlier source/reference occurrences are not silently promoted.'},
      'form_task_and_alternative_checks':[
        'F01–F05 keys checked against independent paradigms: nearu reference cell is visible, bēgen with sunu uses the earlier u-stem forms, and requested cases/number determine target forms.',
        'Full adjective tables include recognition-only instrumental cells, but no F-task asks their unaided production. Dashes are not derivable empty cells.',
        'Selected smierwan ie forms, h/g ðwēan variants, findan fand/funde, bā/bū and bǣm/bām alternatives are distinguished from source validity; spelling variants are not silently mixed in selected tables.',
        'The ordinary plural command dēmað is displayed while immediately following gē permits dēme; source Gehīere gē is supplied rather than wrongly parsed singular.',
        'A01–A03 finite clause exercises correctly distinguish accusative infinitive actor from nominative finite subject, past report time relationships, pronoun ambiguity, and mood homography.',
        'C01–C03 checks preserve speech-level referents, personal cunnan versus ability infinitive versus witan content, and plural dydon replacing a previously expressed action.'
      ],
      'sense_and_construction_checks':[
        'Ǣswician moral offend takes accusative person; āceorfan takes thing cut and separate of particle. Disjunctive singular body-part subject takes singular verb.',
        'Blissian intransitive with mid companion or explicitly taught ofer accusative; wuldrian accusative person/reflexive; plegian intransitive play, with reading wið/mid frames locally supplied; cleopian cry aloud distinct from prior summon.',
        'Iernan run is productive intransitive and plain perception infinitive; reading iernende is separately supplied. Bewęndan reflexive dative is bounded; ðwēan/smierwan take accusative patient and mid material.',
        'Cunnan acquaintance and ability frames checked on BT174; witan personal object required by Cook35.7 prevents a false persons/facts split. Dōn finite causative checked on BT208; action substitution checked on Cook170note4.',
        'Gefyllan fulfil-utterance, forgiefan forgiveness with dative person, hālsian oath-request and healdan keep-saying are explicit new senses/frames; displayed morphology alone does not establish these uses.',
        'Wēnan and biddan lexical genitives checked in Cook156/159; wēn is ðæt expectation checked on p167. Genitive route and time/degree/cognate accusatives remain exact taught functions.',
        'Supplied special constructions remain available: numerical/partitive phrases, foreign names, impending is tō cumanne, fixed right-hand accusative, singular gate/way coordination, double-negative cessation, attracted relative in36.6, impersonal permission, promise/free-choice clause.',
        'Reading support preserves source oddities and uncertainty: geslægene ending, nested pronouns and negative næfde, top and swang versus Latin anointing, dative reflexives, homographic moods, forswīge and mixed direct/reported speech. No generalized morphology is inferred from these local forms.'
      ],
      'amendment_verification':{
        'A01':'Verified new productive play/run/cry senses against actual displays, vocabulary frames and images; obsolete source-only labels do not control current teaching.',
        'A02':'Verified no shoulder/neck claim in actual Latin note; learner route help gives the construction without supplying35.3 answer; personal-relative help correctly refers to man/person rather than stale mountain/hill wording.',
        'A03':'Verified explicit current override of sealed model metadata: all59 model strings unchanged;32.6 singular net; destination tō contextual functions, and38 visible exact hints correctly classified as reference cues.',
        'A04':'Actual student274 and448 repaired; wēn rules agree in paradigm, display and teaching record; the correct tables are unchanged.',
        'A05':'All37 corrected contextual fields in24 tasks verified against independently specified clause functions. Original raw analyses and original A03 packet are preserved.',
        'A06':'Current final overlay selects ch09 hwæðer whether in34.6, with actual prior form/sense and u09-dependent-whether feature; final key model and explanatory note agree. Fulk p286 was personally inspected. No new productive milestone. Linked supplied-input checks below include the cross-task reuse of the33.2 Egypt phrase in33.3; all16 must pass before acceptance.',
        'A07':'Independently caught and verified the additional cross-task mirror:33.3 U16-CSUP-04-INPUT-02 token1 tō is linked to33.2 MODEL token13. Its destination function now agrees with that source model; all16 linked mirrors, including this reuse, are correct.',
        'input_snapshot_comparison':read('build/u16-paradigms-input-mirror-check.json'),
        'given_reference_checks':given,'current_contextual_field_checks':actual_context_repairs,'linked_supplied_input_context_checks':input_mirror_checks,'declared_model_text_changes':text_changes,'effective_model_roles':dict(roles),'source_packet_identity':identity(amended['source']),'historical_A03_override_identity':identity('chapters/ch16/model-binding-amendments.json'),'current_override_identity':identity(active_override),
        'source_corrections':'Independently inspected Matthew114 left column and BT29–30/Matthew132: Johannes genitive/Johannem accusative with declared I→J; āgyldan reward strongIII and valid contracted āgylt versus weak āgyltan sin.'},
      'scope_limit':'Text and paradigm review only; exported-page visual inspection and register integration are separate completion gates. Pending ledger cannot be treated as acceptance; final acceptance is tied to actual current hashes.'}
    dest=ROOT/'chapters/ch16/reviews/paradigms.json';dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'status':ledger['status'],'paradigms':len(checks),'cells':len(routes),'images':len(inspections),'open_findings':ledger['material_open_findings'],'ledger':str(dest)},ensure_ascii=False))

if __name__=='__main__':main()
