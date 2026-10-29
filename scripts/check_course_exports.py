"""Check all course master prose and actual exported PDF text independently.

Run: python scripts/check_course_exports.py --report build/course-export-check.json
Requires Xpdf pdftotext; --pdftotext can specify its executable.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import unicodedata

import check_course_layout as tables

ROOT=Path(__file__).resolve().parents[1]


def norm(value):
    return ' '.join(unicodedata.normalize('NFC',value).split())


def chars(value):
    return re.sub(r'\s+','',unicodedata.normalize('NFC',value)).replace('\u00ad','-')


def quote_projection(value):
    return value.translate(str.maketrans({'’':"'",'‘':"'",'“':'"','”':'"'}))


def group(value,pos):
    if value[pos]!='{':raise ValueError('Expected TeX group: '+value[pos:pos+50])
    start=pos+1;depth=1;pos+=1
    while depth:
        if value[pos]=='\\':pos+=2;continue
        if value[pos]=='{':depth+=1
        elif value[pos]=='}':depth-=1
        pos+=1
    return value[start:pos-1],pos


def texplain(value):
    """Decode only inventoried text/layout commands; fail on an unknown command."""
    value=re.sub(r'(?m)(?<!\\)%[^\n]*','',value)
    out=[];pos=0
    while pos<len(value):
        if value[pos]!='\\':out.append(value[pos]);pos+=1;continue
        match=re.match(r'\\([A-Za-z]+\*?|[^A-Za-z])',value[pos:])
        if not match:raise ValueError('Invalid TeX escape')
        name=match[1];pos+=len(match[0])
        if name in ['textbf','textit','emph','section*','subsection*','subsubsection*','readingtext','textsuperscript','continuation']:
            inner,pos=group(value,pos);out.append(texplain(inner))
        elif name=='itempara':
            number,pos=group(value,pos);inner,pos=group(value,pos);out.append(number+'. '+texplain(inner))
        elif name=='booktitle':
            first,pos=group(value,pos);second,pos=group(value,pos);out.append(texplain(first)+' '+texplain(second))
        elif name in ['begin','end']:
            environment,pos=group(value,pos)
            if environment not in ['minipage','quote','itemize','enumerate','samepage']:raise ValueError('Unknown environment '+environment)
            if name=='begin' and environment=='minipage':_,pos=group(value,pos)
            out.append(' ')
        elif name=='fontsize':
            _,pos=group(value,pos);_,pos=group(value,pos)
        elif name=='allowbreak':
            if value[pos:pos+2]=='{}':pos+=2
        elif name in ['par','raggedright','noindent','item','begingroup','endgroup','selectfont','clearpage','newpage','nobreak','newline']:
            out.append(' ')
        elif name in ['&','%','$','#','_','{','}']:out.append(name)
        elif name in ['textbackslash','textasciitilde','textasciicircum']:
            out.append({'textbackslash':'\\','textasciitilde':'~','textasciicircum':'^'}[name])
            if value[pos:pos+2]=='{}':pos+=2
        else:raise ValueError('Unknown TeX command '+name)
    return norm(''.join(out))


def master_events(raw,doc):
    labels=re.findall(r'^\[\^([^\]]+)\]:',raw,re.M)
    special=lambda label:bool(re.fullmatch(r'(?:[DPR]\d+|P\d+N\d+[a-z]?)',label))
    general=[label for label in labels if not special(label)]
    notes={label:label if special(label) else str(general.index(label)+1) for label in labels}
    def mdplain(value):
        value=re.sub(r'<!--.*?-->','',value)
        value=re.sub(r'\[\^([^\]]+)\]',lambda m:notes[m[1]],value)
        value=value.replace('**','').replace(r'\*','*')
        value=re.sub(r'(?<!\w)\*([^*\n]+?)\*(?!\w)',r'\1',value)
        return norm(value)
    # Whole table groups include newly generated lemma/person captions.
    parts=[];cursor=0
    for t in doc['tables']:
        at=raw.find(t['revised'],cursor)
        if at<0:raise ValueError('Accepted revised table block not found')
        parts.extend([raw[cursor:at],f"\n\n@@TABLE:{t['original_index_zero_based']+1}@@\n\n"])
        cursor=at+len(t['revised'])
    parts.append(raw[cursor:]);raw=''.join(parts)
    raw=re.sub(r'(?m)^(<!--.*-->)$',r'\n\1\n',raw)
    events=[];comments=[];title=None
    for chunk in re.split(r'\n\s*\n',raw.strip()):
        lines=chunk.splitlines()
        if lines[0].startswith('# '):title=mdplain(lines[0][2:]);continue
        if re.fullmatch(r'@@TABLE:\d+@@',chunk):
            events.append({'kind':'table','number':int(chunk[8:-2])});continue
        if all(line.startswith('<!--') for line in lines):
            comments.extend(re.fullmatch(r'<!--\s*(.*?)\s*-->',line)[1] for line in lines);continue
        if lines[0].startswith('##'):
            if len(lines)!=1:raise ValueError('Multiline heading')
            texts=[re.sub(r'^#+ ','',lines[0])]
        elif all(line.startswith('- ') for line in lines):texts=[line[2:] for line in lines]
        elif all(line.startswith('> ') for line in lines):texts=[' '.join(line[2:] for line in lines)]
        elif all(re.match(r'^\d+\.\s+',line) for line in lines):texts=lines
        else:texts=[' '.join(lines)]
        for text in texts:events.append({'kind':'prose','text':mdplain(text)})
    return title,events,comments


def clean_pdf(raw):
    cleaned=[]
    for page in raw.replace('\r\n','\n').replace('\r','\n').split('\f'):
        lines=[line for line in page.splitlines() if not ('Old English' in line and re.search(r'Unit\s+\d+',line))]
        while lines and not lines[-1].strip():lines.pop()
        if lines and re.fullmatch(r'\s*\d+\s*',lines[-1]):lines.pop()
        cleaned.append('\n'.join(lines))
    return '\n'.join(cleaned)


def check_table_cells(doc,groups,error):
    """Match actual physical TeX cells to the approved current Markdown matrices."""
    for i,(group_,table) in enumerate(zip(groups,doc['tables'])):
        physical=tables.decode_tex(group_[2]);render=doc['rendering']['tables'][i]
        if 'panels' in render:
            panels=render['panels'];covered=set()
            if len(physical)!=len(panels):error(f'T{i+1}: physical panel count')
            for actual,panel in zip(physical,panels):
                bidx=panel['output_table_index_zero_based'];cols=panel['source_columns_zero_based']
                matrix=tables.matrix(table['output_blocks'][bidx])
                expected=[[tables.plain(row[c]) for c in cols] for row in matrix]
                if actual!=expected:error(f'T{i+1}: actual TeX cells differ from master')
                covered.update((bidx,r,c) for r,row in enumerate(matrix) for c in cols)
            required={(bidx,r,c) for bidx,b in enumerate(table['output_blocks']) for r,row in enumerate(tables.matrix(b)) for c in range(len(row))}
            if covered!=required:error(f'T{i+1}: incomplete physical coverage')
        else:
            block=table['output_blocks'][0];matrix=tables.matrix(block)
            expected=[[[tables.plain(v) for v in row] for row in matrix]]
            if doc['path']=='chapters/ch01/student.md' and i==15:
                expected=[[['Noun; gender','Meaning','Diagnostic forms','Pattern; limit']]]
                for row in block['rows']:
                    v=list(map(tables.plain,row));expected[0].append([v[0]+' ('+v[1]+')',v[2],'G sg '+v[3]+' N pl '+v[4],v[5]])
            elif doc['path']=='chapters/ch13/student.md' and i==16:
                expected=[[[tables.plain(row[c]) for c in cols] for row in matrix] for cols in [[0,1,5],[0,2,3,4]]]
            if physical!=expected:error(f'T{i+1}: unchanged or existing reflow differs from master')
        wanted={bidx:tables.plain(b['caption']) for bidx,b in enumerate(table['output_blocks']) if b.get('caption')}
        actual={int(m[2]):texplain(m[3]) for m in re.finditer(r'(?ms)^% course-caption:(T\d+):(\d+):begin\n(.*?)^% course-caption:\1:\2:end',group_[2])}
        if actual!=wanted:error(f'T{i+1}: caption differs from master')
        for lt in re.finditer(r'\\begin\{longtable\}.*?\\end\{longtable\}',group_[2],re.S):
            first=lt[0].split(r'\endfirsthead')[0]
            repeated=lt[0].split(r'\endfirsthead')[1].split(r'\endhead')[0]
            first=re.search(r'\\toprule(.*?)\\midrule',first,re.S)[1]
            repeated=re.search(r'\\toprule(.*?)\\midrule',repeated,re.S)[1]
            if first!=repeated:error(f'T{i+1}: repeated longtable header differs')
    if tables.ERRORS:error({'type':'tex_cell_decoder','errors':list(tables.ERRORS)})
    tables.ERRORS.clear()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdftotext',default=shutil.which('pdftotext') or 'C:/Program Files/Git/mingw64/bin/pdftotext.exe')
    parser.add_argument('--report',type=Path,default=Path('build/course-export-check.json'))
    parser.add_argument('--chapter',type=int,help='Optional diagnostic restriction; omit for full acceptance.')
    args=parser.parse_args()
    manifest=json.loads((ROOT/'docs/revisions/table-layout/tables.json').read_text(encoding='utf8'))
    accepted=json.loads((ROOT/'docs/revisions/table-layout/table-review.json').read_text(encoding='utf8'))
    bound={doc['path']:doc for doc in accepted['documents']}
    reports=[]
    for doc in manifest['documents']:
        if args.chapter and doc['chapter']!=args.chapter:continue
        errors=[];typography=[];missing=[]
        source=(ROOT/doc['path']).read_text(encoding='utf8');texpath=ROOT/doc['tex_path'];tex=texpath.read_text(encoding='utf8')
        pdfpath=texpath.parent/'build'/(texpath.stem+'.pdf')
        def error(message):errors.append(message)
        if tables.sha(source)!=bound[doc['path']]['sha256_normalized_lf']:error('Master identity differs from acceptance')
        if tables.logical_mapping_digest(doc)!=bound[doc['path']]['logical_mapping_sha256']:error('Logical table identity differs from acceptance')
        try:title,events,comments=master_events(source,doc)
        except Exception as e:
            reports.append({'master':doc['path'],'errors':['Markdown inventory: '+str(e)]});continue
        prose=[e['text'] for e in events if e['kind']=='prose']
        marked=re.findall(r'(?m)^% mdparagraph:(P\d+):begin\n(.*?)^% mdparagraph:\1:end',tex,re.S)
        if marked:
            try:
                decoded=[texplain(body) for _,body in marked]
                if len(decoded)!=len(prose):error(f'Paragraph count: Markdown {len(prose)}, TeX {len(decoded)}')
                for i,(a,b) in enumerate(zip(prose,decoded)):
                    if chars(a)!=chars(b):error({'type':'tex_prose','index':i+1,'master':a,'tex':b})
            except Exception as e:error('TeX paragraph decoding: '+str(e))
        else:
            body=tex.split(r'\begin{document}',1)[1].split(r'\end{document}',1)[0]
            body=re.sub(r'(?ms)^% mdtable:(T\d+):begin\n.*?^% mdtable:\1:end','',body)
            try:
                hay=chars(texplain(body));cursor=0
                for i,p in enumerate(prose):
                    at=hay.find(chars(p),cursor)
                    if at<0:error({'type':'tex_prose','index':i+1,'master':p})
                    else:cursor=at+len(chars(p))
            except Exception as e:error('Unmarked TeX decoding: '+str(e))
        missing_comments=[comment for comment in comments if '% '+comment not in tex]
        if missing_comments:error({'type':'editorial_comments','missing':missing_comments})
        tablegroups=list(re.finditer(r'(?m)^% mdtable:(T\d+):begin\n(.*?)^% mdtable:\1:end',tex,re.S))
        if len(tablegroups)!=len(doc['tables']):error('Table group count')
        check_table_cells(doc,tablegroups,error)
        titlematch=re.search(r'\\booktitle(\{.*)',tex)
        titlefirst,pos=group(titlematch[1],0);titlesecond,pos=group(titlematch[1],pos)
        expected_subtitle=title.split('. ',1)[1]
        if texplain(titlesecond)!=expected_subtitle or texplain(titlefirst)!=f"UNIT {doc['chapter']}":error('Title differs from master')
        visible=[{'kind':'title','text':texplain(titlefirst)+' '+texplain(titlesecond)}];visible_cells=0;captions=0
        for event in events:
            if event['kind']=='prose':visible.append({'kind':'prose','text':event['text']});continue
            index=event['number']-1;body=tablegroups[index][2]
            # Captions and physical panels are inventoried in their actual order.
            for part in re.finditer(r'(?ms)^% course-caption:(T\d+):(\d+):begin\n(.*?)^% course-caption:\1:\2:end|\\begin\{(tabular|longtable)\}\{[^\n]*\}\n.*?\\end\{\4\}',body):
                if part[1]:
                    text=texplain(part[3]);visible.append({'kind':'caption','table':index+1,'text':text});captions+=1
                else:
                    decoded=tables.decode_tex(part[0])
                    for matrix in decoded:
                        for row in matrix:
                            visible.append({'kind':'table_row','table':index+1,'text':' '.join(row),'cells':row});visible_cells+=len(row)
        extraction=subprocess.run([args.pdftotext,'-enc','UTF-8','-raw',str(pdfpath),'-'],capture_output=True,check=True).stdout.decode('utf8')
        pdf=chars(clean_pdf(extraction));projected=quote_projection(pdf);cursor=0
        for i,event in enumerate(visible):
            wanted=chars(event['text']);at=pdf.find(wanted,cursor);alias=False
            if at<0:
                at=projected.find(quote_projection(wanted),cursor);alias=at>=0
                if alias and any(a!=b and (a,b) not in [("'",'’'),("'",'‘'),('"','“'),('"','”')] for a,b in zip(wanted,pdf[at:at+len(wanted)])):
                    at=-1;alias=False
            if at<0:missing.append({'event':i+1,**event})
            else:
                if alias:typography.append({'event':i+1,'kind':event['kind'],'expected':wanted,'actual':pdf[at:at+len(wanted)]})
                cursor=at+len(wanted)
        suspicious=Counter(c for c in extraction if c=='\ufffd' or unicodedata.category(c) in ['Co','Cn'] or (unicodedata.category(c)=='Cc' and not c.isspace()))
        if suspicious:error({'type':'suspicious_pdf_characters','characters':dict(suspicious)})
        logpath=pdfpath.with_suffix('.log')
        glyphs=re.findall(r'Missing character:[^\n]*',logpath.read_text(encoding='utf8',errors='replace')) if logpath.exists() else ['Build log not present']
        if glyphs:error({'type':'glyph_log','messages':glyphs})
        reports.append({'master':doc['path'],'master_sha256':hashlib.sha256((ROOT/doc['path']).read_bytes()).hexdigest(),'tex':doc['tex_path'],'tex_sha256':hashlib.sha256(texpath.read_bytes()).hexdigest(),'pdf':pdfpath.relative_to(ROOT).as_posix(),'pdf_sha256':hashlib.sha256(pdfpath.read_bytes()).hexdigest(),'pages':extraction.count('\f'),'prose_blocks':len(prose),'editorial_comments':len(comments),'visible_table_cells':visible_cells,'table_captions':captions,'pdf_events':len(visible),'errors':errors,'missing_pdf_events':missing,'typographic_quote_projections':typography})
    result={'status':'pass' if all(not d['errors'] and not d.get('missing_pdf_events') for d in reports) else 'fail','document_count':len(reports),'method':'Independent complete Markdown block inventory, TeX text decoder and direct Xpdf raw extraction. NFC, whitespace and Xpdf soft-hyphen normalization; quote projections reported separately. Every prose block, table row/cell and caption checked in document order.','documents':reports}
    dest=args.report if args.report.is_absolute() else ROOT/args.report;dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'status':result['status'],'documents':len(reports),'errors':sum(len(d['errors']) for d in reports),'missing_pdf_events':sum(len(d.get('missing_pdf_events',[])) for d in reports),'quote_projections':sum(len(d.get('typographic_quote_projections',[])) for d in reports)},indent=2))
    return 0 if result['status']=='pass' else 1


if __name__=='__main__':raise SystemExit(main())
