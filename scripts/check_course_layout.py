"""Independently verify the accepted course-table revision.

Run: python scripts/check_course_layout.py [--report build/course-layout-check.json]

This checker imports neither table authoring implementation. The acceptance record
binds current master text and logical matrices; retained TeX is decoded afresh so
formatting-only repairs do not invalidate a previously reviewed matrix.
"""
from collections import Counter
import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []


def check(ok, message):
    if not ok:
        ERRORS.append(message)


def sha(text):
    return hashlib.sha256(text.encode('utf8')).hexdigest()


def plain(text):
    text=re.sub(r'<!--.*?-->','',text)
    return ' '.join(text.replace('**', '').replace(r'\*', '*').split())


def parse_md(text):
    results = []
    lines = text.splitlines(keepends=True)
    offset = 0
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith('|') and i + 1 < len(lines) and re.match(r'^\s*\|[- :|]+\|\s*$', lines[i+1]):
            start = offset
            block = []
            while i < len(lines) and lines[i].lstrip().startswith('|'):
                block.append(lines[i]);offset += len(lines[i]);i += 1
            rows = [[cell.strip() for cell in re.split(r'(?<!\\)\|', row.strip()[1:-1])] for row in block]
            results.append({'headers': rows[0], 'rows': rows[2:], 'start': start, 'end': offset, 'raw': ''.join(block)})
        else:
            offset += len(lines[i]);i += 1
    return results


def matrix(block):
    return [block['headers'], *block['rows']]


def target_value(record, target):
    b = record['output_blocks'][target['block']]
    if target.get('caption'):
        value = b['caption']
    else:
        value = matrix(b)[target['row']][target['column']]
    if 'slice' in target:
        value = value[slice(*target['slice'])]
    return value


def features(label, command=False, gender_label=False):
    label = plain(label).lower().replace('–', '-')
    if gender_label:
        for short,full in [('m','masculine'),('n','neuter'),('f','feminine')]:
            label=re.sub(r'^'+short+r'(?=\.?\s)',full,label)
    result = {}
    for val, pattern in [('n',r'\b(?:nominative|nom|n)\b'),('g',r'\b(?:genitive|gen|g)\b'),('d',r'\b(?:dative|dat|d)\b'),('a',r'\b(?:accusative|acc|a)\b'),('i',r'\b(?:instrumental|instr)\b')]:
        if re.search(pattern, label):result['case'] = (val,);break
    if re.search(r'\b(singular|sg\.?|one person)\b', label):result['number'] = ('sg',)
    if re.search(r'\b(plural|pl\.?|two or more)\b', label):result['number'] = ('pl',)
    if 'dual' in label:result['number'] = ('du',)
    pronouns={
        'ic':((1,),('sg',)),
        'ðū':((2,),('sg',)),
        'hē / hēo / hit':((3,),('sg',)),
        'wē / gē / hīe':((1,2,3),('pl',)),
    }
    if label in pronouns:result.update(zip(('person','number'),pronouns[label]))
    gs=[]
    for name, code in [('masculine','m'),('neuter','n'),('feminine','f')]:
        if name in label:gs.append(code)
    if 'all genders' in label:gs=['m','n','f']
    if gs:result['gender'] = tuple(gs)
    if re.search(r'1-3|1\s*[,/]\s*2\s*(?:[,/]|and)\s*3|all (?:three )?persons|all (?:singular|plural|sg|pl)', label):result['person']=(1,2,3)
    elif '1/3' in label:result['person']=(1,3)
    else:
        for word,n in [('first',1),('second',2),('third',3)]:
            if re.search(r'\b'+word+r'\b',label):result['person']=(n,)
        pm=re.search(r'(?:^|\s)([123])(?:st|nd|rd)?(?:\s|,|$)',label)
        if pm:result['person']=(int(pm[1]),)
    if command and 'number' in result and 'person' not in result:result['person']=(2,)
    if 'preterite' in label:result['tense']=('preterite',)
    elif 'present' in label:result['tense']=('present',)
    if 'reference' in label:result['scope']=('reference',)
    for mood in ['indicative','subjunctive','imperative']:
        if mood in label:result['mood']=(mood,)
    if re.search(r'\bstrong\b',label):result['series']=('strong',)
    if re.search(r'\bweak\b',label):result['series']=('weak',)
    return result


def semantic_cells(headers, rows, *, kind, caption=None, old=False):
    """Derive grammatical coordinates from visible axes, not supplied cell maps."""
    out=Counter()
    command = kind.startswith('command_')
    h0 = plain(headers[0]).lower()
    case_columns = len(headers)>1 and all(features(h).get('case') for h in headers[1:])
    number_case = h0 == 'number' and len(headers)>1 and plain(headers[1]).lower()=='case'
    verb_comparison = h0 in {'verb','lemma','verb label'}
    tense_rows = h0 == 'tense'
    no_row_descriptor = kind in {'command_pair_person_rows','present_subjunctive_number_rows'} and old
    person_rows = any(w in h0 for w in ['person','number','addressee']) and not number_case and not case_columns and not (kind=='noun_number_columns' and old)
    adjective = kind in {'adjective_number_panels','gender_number_panels','gender_order_and_case_labels','complete_key_declension_case_rows'}
    source_tense = ''
    inherited_tenses={}
    for c,h in enumerate(headers):
        f=features(h,command,adjective)
        if 'tense' in f:source_tense=f['tense'][0]
        inherited_tenses[c]=source_tense
    for r,row in enumerate(rows):
        for c,value in enumerate(row):
            if (not no_row_descriptor and c == 0) or (number_case and c==1):continue
            f={k:val for k,val in features(headers[0],command).items() if k in ['mood']}
            lemma=''
            if no_row_descriptor:
                f.update(features(headers[c],command))
            elif case_columns:
                f.update(features(row[0],command));f.update(features(headers[c],command))
            elif number_case:
                f.update(features(row[0],command));f.update(features(row[1],command));f.update(features(headers[c],command,adjective))
            elif verb_comparison:
                lemma=row[0]
                f.update(features(headers[c],command))
                if inherited_tenses[c]:f['tense']=(inherited_tenses[c],)
            elif tense_rows:
                f.update(features(row[0],command));f.update(features(headers[c],command,adjective))
            else:
                f.update(features(row[0],command));f.update(features(headers[c],command,adjective))
                if kind in {'paired_lemma_indicatives','paired_lemma_subjunctives'}:
                    if ' · ' in headers[c]:lemma=headers[c].split(' · ',1)[0]
                    else:lemma=caption or ''
                elif kind in {'single_tense_comparison_transpose','command_comparison_person_rows'}:
                    lemma=headers[c]
                elif kind=='noun_number_columns':
                    if old:lemma=headers[c]
                    elif caption:lemma=caption
                    else:lemma=re.sub(r'\s+(?:singular|plural)(?:\b.*)?$','',headers[c],flags=re.I)
            if kind=='pronoun_case_rows' and not old and caption:
                f.update(features(caption))
            if kind in {'paired_lemma_subjunctives','present_subjunctive_number_rows','subjunctive_number_rows','subjunctive_person_labels'}:
                f.setdefault('person',(1,2,3))
                f.setdefault('mood',('subjunctive',))
            if kind.startswith('command_'):
                f.setdefault('person',(2,))
                f.setdefault('mood',('imperative',))
            if kind=='noun_number_columns' and old:
                f.update(features(row[0]))
            dims=['case','number','gender','person','tense','scope','series','mood']
            for vals in itertools.product(*(f.get(k,('',)) for k in dims)):
                out[(lemma,*vals,value)] += 1
    return out


def tex_plain(text):
    text=re.sub(r'(?m)%[^\n]*','',text).strip()
    text=text.replace(r'\allowbreak{}','').replace(r'\newline',' ')
    text=text.replace(r'\&','&').replace(r'\%','%').replace(r'\_','_').replace(r'\#','#')
    # All table-body commands inventoried: textbf and the two spacing commands.
    while re.search(r'\\textbf\{[^{}]*\}',text):
        text=re.sub(r'\\textbf\{([^{}]*)\}',r'\1',text)
    check(not re.search(r'\\[A-Za-z]+',text),'Unparsed TeX cell command: '+text[:100])
    return ' '.join(text.split())


def decode_tex(text):
    result=[]
    pat=re.compile(r'\\begin\{(tabular|longtable)\}\{[^\n]*\}\n(.*?)\\end\{\1\}',re.S)
    for match in pat.finditer(text):
        body=match[2]
        head=body.split(r'\toprule',1)[1].split(r'\midrule',1)[0].strip()
        if match[1]=='longtable':data=body.split(r'\endlastfoot',1)[1]
        else:data=body.split(r'\midrule',1)[1]
        data=data.split(r'\bottomrule',1)[0]
        rawrows=[head,*[s for s in re.split(r'(?<!\\)\\\\(?:\[[^\]]*\])?',data) if s.strip()]]
        decoded=[]
        for row in rawrows:
            row=re.sub(r'\\\\\s*$','',row.strip())
            decoded.append([tex_plain(v) for v in re.split(r'(?<!\\)&',row)])
        result.append(decoded)
    return result


def audit_style(record):
    """Find obvious complete paradigms without relying on author classifications."""
    findings=[]
    for doc in record['documents']:
        for table in doc['tables']:
            for block in table['output_blocks']:
                hs=block['headers'];rows=block['rows'];labels=[row[0] for row in rows]
                fs=[features(label) for label in labels]
                ref={'path':doc['path'],'original_table':table['original_index_zero_based']+1}
                plural=[row for row,f in zip(rows,fs) if f.get('number')==('pl',) and f.get('person') in [(1,),(2,),(3,)]]
                if len(plural)==3 and len({tuple(row[1:]) for row in plural})==1:
                    findings.append({**ref,'finding':'Repeated identical plural rows','labels':[row[0] for row in plural]})
                finite=all('person' in f and 'number' in f for f in fs) and bool(rows) and 'person' in hs[0].lower()
                if finite and not all(re.match(r'^[123](?:–3)? (?:sg|pl)\.(?::.*)?$',label) for label in labels):
                    findings.append({**ref,'finding':'Noncanonical finite row labels','labels':labels})
                if hs[:1]==['Verb'] and hs[1:]==['Present singular','Present plural','Preterite singular','Preterite plural']:
                    findings.append({**ref,'finding':'Complete subjunctive matrix has verb row axis'})
                if hs[:1]==['Verb'] and len(hs)==3 and all('second' in h.lower() for h in hs[1:]):
                    findings.append({**ref,'finding':'Complete imperative comparison has verb row axis'})
                if len(rows)==2 and all(re.search(r'command|imperative',label,re.I) for label in labels):
                    findings.append({**ref,'finding':'Command label aliases','labels':labels})
                if hs[:1]==['Case']:
                    aliases=[h for h in hs[1:] if re.match(r'^(?:neuter|masculine|feminine|common)\b',h) or re.search(r'\b(?:sg|pl)\.?$',h)]
                    if aliases:findings.append({**ref,'finding':'Nominal header aliases','headers':aliases})
    return findings


def verify_frozen_content(baseline, review):
    def digest(value):return sha(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')))
    exceptions={(e['path'],e['field']):e for e in review['bounded_semantic_exceptions']}
    checks=[];source_ids=[]
    for chapter,fields in baseline['chapters'].items():
        path=f'chapters/{chapter}/coverage.json'
        data=json.loads((ROOT/path).read_text(encoding='utf8'))
        for field,expected in fields.items():
            actual=digest(data[field]);exception=exceptions.get((path,field))
            approved=exception['approved_current_sha256'] if exception else expected
            if exception:check(exception['baseline_sha256']==expected,path+': metadata exception baseline')
            check(actual==approved,path+': frozen '+field)
            checks.append({'path':path,'field':field,'semantic_sha256':actual,'baseline_sha256':expected,**({'bounded_metadata_amendment':exception['description']} if exception else {})})
        source_ids.extend(item['task_id'] for item in data['assigned_items'] if item['task_id'].startswith('EX-'))
    for path,info in baseline['registers'].items():
        data=json.loads((ROOT/path).read_text(encoding='utf8'))[info['key']]
        actual=digest(data);check(actual==info['semantic_sha256'],path+': frozen '+info['key'])
        check(len(data)==info['count'],path+': register item count')
        checks.append({'path':path,'field':info['key'],'count':len(data),'semantic_sha256':actual})
    check(len(source_ids)==644 and len(set(source_ids))==644,'Cook item assignment count or uniqueness')
    return {'checks':checks,'cook_item_count':len(source_ids),'distinct_cook_item_count':len(set(source_ids))}


def logical_mapping_digest(doc):
    tables=[]
    for t in doc['tables']:
        tables.append({key:t[key] for key in ['original_index_zero_based','kind','changed','original','revised','original_headers','original_rows','output_blocks','mapping']})
    value={'path':doc['path'],'tables':tables,'prose_changes':doc.get('prose_changes',[])}
    return sha(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')))


def negative_controls(record):
    """Verify that the independent semantic comparison detects plausible damage."""
    indexed={(d['path'],t['original_index_zero_based']+1):t for d in record['documents'] for t in d['tables']}
    results=[]
    def probe(name,path,number,change):
        table=indexed[(path,number)]
        before=semantic_cells(table['original_headers'],table['original_rows'],kind=table['kind'],old=True)
        blocks=copy.deepcopy(table['output_blocks']);change(blocks)
        after=Counter()
        for b in blocks:after.update(semantic_cells(b['headers'],b['rows'],kind=table['kind'],caption=b.get('caption')))
        detected=before!=after;check(detected,'Negative control failed: '+name)
        results.append({'mutation':name,'detected':detected})
    probe('altered vowel length','chapters/ch01/student.md',15,lambda bs:bs[0]['rows'][0].__setitem__(1,'ēom'))
    probe('swapped gender headings','chapters/ch03/student.md',2,lambda bs:bs[0].__setitem__('headers',[bs[0]['headers'][0],bs[0]['headers'][2],bs[0]['headers'][1],bs[0]['headers'][3]]))
    probe('dual relabelled plural','chapters/ch02/student.md',1,lambda bs:bs[0]['headers'].__setitem__(2,bs[0]['headers'][2].replace('Dual','Plural')))
    probe('reference-only scope deleted','chapters/ch03/student.md',19,lambda bs:bs[1].__setitem__('headers',[h.replace(': reference only','') for h in bs[1]['headers']]))
    probe('imperative plural broadened to all persons','chapters/ch08/student.md',35,lambda bs:bs[0]['rows'][1].__setitem__(0,'1–3 pl.'))
    probe('lemma association changed','chapters/ch02/student.md',2,lambda bs:bs[0]['headers'].__setitem__(1,'incorrect lemma · Present'))
    probe('subjunctive labelled indicative','chapters/ch08/answer-key.md',10,lambda bs:bs[0]['headers'].__setitem__(1,bs[0]['headers'][1].replace('subjunctive','indicative')))
    probe('weak preterite third-singular row omitted','chapters/ch02/student.md',2,lambda bs:bs[0]['rows'].pop(2))
    probe('numbered plural response relabelled all persons','chapters/ch15/student.md',71,lambda bs:bs[0]['rows'][3].__setitem__(0,'1–3 pl.'))
    return results


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path,help='Optional JSON report path.')
    args=parser.parse_args()
    record=json.loads((ROOT/'docs/revisions/table-layout/tables.json').read_text(encoding='utf8'))
    baseline=json.loads((ROOT/'docs/revisions/table-layout/baseline.json').read_text(encoding='utf8'))
    review=json.loads((ROOT/'docs/revisions/table-layout/table-review.json').read_text(encoding='utf8'))
    approved={d['path']:d for d in review['documents']}
    check(set(approved)=={d['path'] for d in record['documents']},'Accepted document coverage')
    check(len(record['documents'])==36,'Course master count')
    summary=[];counts=Counter();semantic_failures=[];tex_pending=[]
    for doc in record['documents']:
        name=doc['path'];current=(ROOT/name).read_text(encoding='utf8')
        actual=parse_md(current)
        expected=[b for t in doc['tables'] for b in t['output_blocks']]
        check(len(actual)==len(expected),name+': current table count')
        for i,(a,b) in enumerate(zip(actual,expected)):
            check(matrix(a)==matrix(b),f'{name} current matrix {i}')
        accepted=approved[name]
        check(sha(current)==accepted['sha256_normalized_lf'],name+': accepted master hash')
        check(sha(current)==doc['current_master_sha256_normalized_lf'],name+': manifest master hash')
        check(logical_mapping_digest(doc)==accepted['logical_mapping_sha256'],name+': accepted logical mapping')
        check(doc['original_sha256_normalized_lf']==baseline['files'][name]['sha256_normalized_lf'],name+': baseline identity')
        for i,t in enumerate(doc['tables']):
            label=f'{name} T{i+1:02} {t["kind"]}'
            om=[t['original_headers'],*t['original_rows']]
            original_tables=parse_md(t['original'])
            check(len(original_tables)==1 and matrix(original_tables[0])==om,label+': original literal matrix')
            check(sha(t['original'])==t['original_sha256'],label+': original table hash')
            check(sha(t['revised'])==t['revised_sha256'],label+': revised table hash')
            indexed={tuple(m['source']):m for m in t['mapping']}
            allcoords={(r,c) for r,row in enumerate(om) for c in range(len(row))}
            check(set(indexed)==allcoords and len(indexed)==len(t['mapping']),label+': source mapping coverage/uniqueness')
            for coord,m in indexed.items():
                r,c=coord;v=om[r][c]
                check(v==m['original_value'],label+': mapping source differs')
                check(bool(m['targets']),label+': missing destination')
                for dest in m['targets']:
                    tv=target_value(t,dest)
                    if dest['how']=='exact':check(tv==v,label+f': altered exact value {coord}')
                if m['role']=='literal':
                    check(any(x['how']=='exact' for x in m['targets']),label+f': literal lacks exact destination {coord}')
            for bidx,b in enumerate(t['output_blocks']):
                for r,row in enumerate(matrix(b)):
                    for c,v in enumerate(row):
                        origins=[m for m in t['mapping'] if any(not x.get('caption') and x['block']==bidx and x['row']==r and x['column']==c for x in m['targets'])]
                        if r>0 and c>0:check(bool(origins),label+f': unsupported output body cell {bidx}/{r}/{c}')
            if t['changed']:
                before=semantic_cells(t['original_headers'],t['original_rows'],kind=t['kind'],old=True)
                after=Counter()
                for b in t['output_blocks']:after.update(semantic_cells(b['headers'],b['rows'],kind=t['kind'],caption=b.get('caption')))
                if before!=after:
                    semantic_failures.append({'document':name,'table':i+1,'kind':t['kind'],'missing':list((before-after).items())[:4],'extra':list((after-before).items())[:4]})
            else:check(len(t['output_blocks'])==1 and matrix(t['output_blocks'][0])==om,label+': unchanged table differs')
            if t['kind']=='identical_plural_rows':
                plural=[row for row in t['original_rows'] if features(row[0]).get('number')==('pl',)]
                check(len(plural)==3 and len({tuple(row[1:]) for row in plural})==1,label+': unequal plural inputs')
            if t['kind'].startswith('protected_'):
                check(len(t['output_blocks'])==1 and len(t['output_blocks'][0]['rows'])==len(t['original_rows']),label+': protected rows lost')
                check([x[1:] for x in t['output_blocks'][0]['rows']]==[x[1:] for x in t['original_rows']],label+': protected values changed')
            counts[t['kind']]+=1;counts['source_cells']+=len(allcoords)
        # Independent TeX decode is bound to actual retained bytes.
        tex=(ROOT/doc['tex_path']).read_text(encoding='utf8')
        prose_tex=tex.replace(r'\allowbreak{}','').replace(r'\newline',' ')
        while re.search(r'\\(?:textbf|textit|emph)\{[^{}]*\}',prose_tex):
            prose_tex=re.sub(r'\\(?:textbf|textit|emph)\{([^{}]*)\}',r'\1',prose_tex)
        prose_tex=' '.join(prose_tex.replace(r'\S{}','§').split())
        for change in doc.get('prose_changes',[]):
            check(plain(change['after']) in prose_tex,name+': changed prose absent from actual TeX '+plain(change['after'])[:50])
        groups=list(re.finditer(r'(?m)^% mdtable:(T\d+):begin\n(.*?)^% mdtable:\1:end',tex,re.S))
        check(len(groups)==len(doc['tables']),name+': actual TeX groups')
        rendergroups=doc['rendering']['tables']
        for i,(g,t) in enumerate(zip(groups,doc['tables'])):
            physical=decode_tex(g[2]);rg=rendergroups[i]
            captions=list(re.finditer(r'(?m)^% course-caption:(T\d+):(\d+):begin\n(.*?)^% course-caption:\1:\2:end',g[2],re.S))
            wanted_captions={bidx:plain(b['caption']) for bidx,b in enumerate(t['output_blocks']) if b.get('caption')}
            actual_captions={int(c[2]):tex_plain(c[3].replace(r'\par','').replace(r'\nobreak','')) for c in captions}
            check(actual_captions==wanted_captions,name+f': actual TeX captions T{i+1}')
            if 'panels' in rg:
                panels=rg['panels'];check(len(physical)==len(panels),name+f': TeX T{i+1} physical panels')
                covered=set()
                for actualtex,panel in zip(physical,panels):
                    outidx=panel['output_table_index_zero_based'];cols=panel['source_columns_zero_based']
                    b=t['output_blocks'][outidx]
                    expectedtex=[[plain(row[c]) for c in cols] for row in matrix(b)]
                    check(actualtex==expectedtex,name+f': decoded TeX T{i+1}/{outidx} differs')
                    covered.update((outidx,r,c) for r,row in enumerate(matrix(b)) for c in cols)
                required={(bidx,r,c) for bidx,b in enumerate(t['output_blocks']) for r,row in enumerate(matrix(b)) for c in range(len(row))}
                check(covered==required,name+f': missing physical TeX coverage T{i+1}')
            elif len(physical)==1 and physical[0]==[[plain(v) for v in row] for row in matrix(t['output_blocks'][0])]:pass
            elif name=='chapters/ch01/student.md' and i==15:
                b=t['output_blocks'][0]
                exp=[['Noun; gender','Meaning','Diagnostic forms','Pattern; limit']]
                for row in b['rows']:
                    v=list(map(plain,row));exp.append([v[0]+' ('+v[1]+')',v[2],'G sg '+v[3]+' N pl '+v[4],v[5]])
                check(physical==[exp],name+': independently reconstructed six-to-four vocabulary')
            elif name=='chapters/ch13/student.md' and i==16:
                m=matrix(t['output_blocks'][0]);exp=[[[plain(row[c]) for c in cols] for row in m] for cols in [[0,1,5],[0,2,3,4]]]
                check(physical==exp,name+': independently reconstructed nominal diagnostics')
            else:tex_pending.append({'document':name,'table':i+1,'parity':rg.get('original_matrix_to_tex_parity'),'expected':matrix(t['output_blocks'][0]),'actual':physical})
        summary.append({'path':name,'sha256_normalized_lf':sha(current),'tex_path':doc['tex_path'],'tex_sha256_normalized_lf':sha(tex),'original_groups':len(doc['tables']),'current_tables':len(actual)})
    frozen=verify_frozen_content(baseline,review)
    style_findings=audit_style(record)
    controls=negative_controls(record)
    passed=not (ERRORS or semantic_failures or tex_pending or style_findings)
    result={'status':'pass' if passed else 'fail','counts':dict(counts),'errors':ERRORS,'semantic_comparison_exceptions':semantic_failures,'tex_reflow_exceptions':tex_pending,'style_findings':style_findings,'negative_controls':controls,'frozen_content':frozen,'documents':summary}
    if args.report:
        dest=args.report if args.report.is_absolute() else ROOT/args.report
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'status':result['status'],'documents':len(summary),'source_cells':counts['source_cells'],'cook_items':frozen['cook_item_count'],'errors':ERRORS,'semantic_exceptions':semantic_failures,'tex_reflow_exceptions':tex_pending,'style_findings':style_findings},ensure_ascii=False,indent=2))
    return 0 if passed else 1



if __name__=='__main__':raise SystemExit(main())
