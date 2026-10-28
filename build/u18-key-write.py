"""Write only the separate Unit18 key from the committed contract and author prose."""
import json,runpy,unicodedata,hashlib,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text(encoding='utf8'))
C=load('chapters/ch18/coverage.json');tasks={t['task_id']:t for t in C['assigned_items']}
A=runpy.run_path(str(R/'build/u18-key-original-answers.py'))['A'];N=runpy.run_path(str(R/'build/u18-key-cook-notes.py'))['N']
A={k:re.sub(r'(?<=[A-Za-z])(?=\d)',' ',v)for k,v in A.items()}
N={k:re.sub(r'(?<=[A-Za-z])(?=\d)',' ',v)for k,v in N.items()}
P={m['output_position_id']:m for m in load('curriculum/proposals/unit18/author-only-output-models.json')['models']}
cook={s['owner_id']:s['text']for s in load('curriculum/proposals/unit18/author-only-cook-sequence-bindings.json')['sequences']}
W=load('sources/audits/unit18-grammar/independent-reading-translation.json')['translation']
w1,w2=W[0].split(' King Arcestrates',1);w2='King Arcestrates'+w2
w3,w4=W[2].split(' Then the banquet',1);w4='Then the banquet'+w4
translations={'R01-O001':[w1],'R01-O002':[w2,W[1],w3],'R01-O003':[w4,W[3]]}
translation_notes={
'R01-O001':'The daughter is the perceiver and the person who falls in love; Apollonius is the person admired. “Accomplishments,” “skills” and “arts” can render the supplied cræft sense here. The permission belongs to an earlier occasion, recalled with “a little while ago”; it does not command a gift at that earlier moment. The free choice and royal treasure remain part of what she recalls.',
'R01-O002':'Retain the two separate amounts and their materials: two hundred pounds of gold, four hundred pounds by weight of silver. **Ðone mǣstan dǣl** is a superlative: “the greatest part/portion” or “most of the precious clothing,” not merely “a large amount.” The twenty male slaves are also a gift, then become the addressees of the carrying and placing commands. “Teacher” or “master” can render Lārēow; chamber is supplied with the original dining-room note. The princess’s commands are then reported as carried out. The final relative means that the men saw the gifts; original note13 expressly supplies męnn as its antecedent.',
'R01-O003':'The guests’ rising, leave-taking and going home are narrated as completed. “Bade them farewell” can render the wish that they be well; grētton is appropriate to taking leave here. Apollonius first addresses the king and princess, then turns to the slaves given him. His last words are commands and a proposal, followed by the purpose of rest. They do not narrate arrival or sleep. “Inn,” “guesthouse” and “lodging” can render giesthūs in this context. The printed cwēn is the princess, the established king’s daughter, rather than a newly introduced queen.'}
out=[]
def add(s=''):out.append(s)
add('# Unit 18. Answer key')
add('The composition models are new teaching material. They retain Cook’s complete Exercises 44–48 under his joint group **XII, XIII**. The connected reading is the separate Apollonius passage, and its translation was prepared independently from the actual Old English before comparison with other complete translations. Each model is one defensible answer; a different grammatical answer can still miss an explicit lexical, mood, number, omission or order target.[^key-sources]')
add('Preserve every participant, action, time relation and clause connection. Except where an order is specified, other grammatical orders are acceptable. English translations and analyses may use equivalent precise wording. Documented variants, such as **ðām** beside selected **ðǣm**, are not automatically errors; tasks that expressly require the selected forms still test those forms. The notes below identify the distinctions most likely to change the meaning.')
add('The original hints and complete local help remain available. A copied supplied form is not independent recall of an unassigned paradigm. In particular, source names, quantities, rare reading frames and the combined counterfactual in 44.7 are used with their help visible. A simple preterite may render English “did,” “has done” or “had done” where the context establishes the relation; a subjunctive in a report does not by itself make the report false.')
sections=[('A. Clauses and reference',['A01','A02','A03']),('C. Composition',['C01','C02']),('F. Forms and grammatical roles',['F01','F02','F03'])]
def original(short):
 t=tasks['NEW-U18-'+short];add('### '+short);add('<!-- key: '+t['key_id']+' -->');add('**Task:** '+t['prompt'])
 for seq in t.get('input_sequences',[]):add('**Input:** '+seq['text'])
 for p in t['output_positions']:
  oid=p['output_position_id'];suffix=oid.removeprefix('NEW-U18-');add('<!-- output: '+oid+' -->');add('**'+p['label']+'**')
  if suffix in translations:
   for paragraph in translations[suffix]:add(paragraph)
   add('**Target and explanation:** '+re.sub(r'(?<=[A-Za-z])(?=\d)',' ',translation_notes[suffix]))
  else:
   if p.get('response_language')=='Old English':add('**'+P[oid]['model']+'**')
   assert suffix in A,suffix
   add(A[suffix])
for heading,ids in sections:
 add('## '+heading)
 for short in ids:original(short)
for ex,nitems in [(44,8),(45,9),(46,9),(47,11),(48,10)]:
 add('## Cook '+str(ex))
 for item in range(1,nitems+1):
  tid=f'EX-XII-XIII-{ex}-{item:02}';t=tasks[tid];add(f'### Cook {ex}.{item}');add('<!-- key: '+t['key_id']+' -->');add(cook[tid]);assert len(t['output_positions'])==1
  add('<!-- output: '+t['output_positions'][0]['output_position_id']+' -->');add('**Cook’s prompt:** '+t['prompt']);add('**Target and explanation:** '+N[f'{ex}.{item}'])
add('## R. The princess’s gifts and the banquet’s end')
add('The assigned reading is Cook 175.18–177.2, ending with **geręstan** before *Apollonius as Teacher*. The divisions below cover every clause. Page and line references retain the edition’s pages and the stated physical-line convention. Use the source notes and complete local help throughout.')
for short in ['R01','R02','R03','R04','R05']:original(short)
add('### Cook’s original reading notes')
add('These twenty-two notes retain Cook’s wording and all twenty-nine anchor relationships. Their section numbers refer to his grammar; the visible modern help supplies the interpretations used above. His etymological questions and the Beowulf comparison are retained apparatus, not additional exercises or a poetry assignment.')
for note in C['source_spans'][0]['original_notes']:
 page=note['printed_page'];num=note['original_note_number'];anchors='; '.join(a['source_line_id'].replace('FB','').replace('-', '.')+' '+a['anchor_text']for a in note['anchors'])
 add('**'+str(page)+', note '+str(num)+'** ('+anchors+'). '+note['original_text'])
add('[^key-sources]: Cook, *Exercises in Old English* (1895), pp. 29–33, joint XII, XIII, Exercises 44–48; *A First Book in Old English*, second edition (1895), pp. 175–177 and the cited grammatical sections. The command-passive reference in 45.5 uses 177.10 as a grammatical parallel without assigning the following episode. Additional checked lexical evidence is Bosworth–Toller, main volume pp. 95 and 1056 and Supplement pp. 81, 240 and 646; proper-name and supplied nominal evidence is documented in the unit’s source apparatus. The earlier findan form funde is explicitly allowed by Cook’s strong-verb discussion; no correction to its earlier teaching is required.')
text=unicodedata.normalize('NFC','\n\n'.join(out)+'\n')
(R/'chapters/ch18/answer-key.md').write_text(text,encoding='utf8',newline='\n')
print('key written',len(text.split()),'whitespace words',len(tasks),'tasks',sum(len(t['output_positions'])for t in tasks.values()),'outputs')
