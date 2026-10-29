"""One-use completion indexes, written only after actual export/register acceptance."""
import argparse,json,re
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument('--exports-checkpoint',required=True)
a=ap.parse_args()
assert re.fullmatch(r'[0-9a-f]{7,40}',a.exports_checkpoint)
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def text(p): return Path(p).read_text(encoding='utf-8')
def replace_once(s,before,after):
    assert s.count(before)==1,(before,s.count(before))
    return s.replace(before,after,1)
c=read('chapters/ch17/coverage.json')
pages=read('typesetting/ch17/page-review.json')
reg=read('chapters/ch17/register-integration.json')
assert c['completion']['complete'] and reg['status']=='accepted' and pages['status']=='PASS'
assert c['textual_review']['status']==c['presentation_review']['status']=='accepted'
assert not pages['unresolved_findings']
counts=c['contract_metrics']; totals=pages['page_totals']; metrics=reg['metrics']
lp,kp,total=totals['learner'],totals['key'],totals['total']
tasks,outputs,systems,cells=(counts[k] for k in ['tasks','requested_output_positions','paradigms','logical_cells'])
original_outputs=sum(len(t['output_positions']) for t in c['assigned_items'] if t['task_id'].startswith('NEW-'))
features=len(c['grammar_inventory']); teaching=len(c['teaching_records'])
assert original_outputs==64
assert features==c['explicit_scope_metrics']['features']==64
assert teaching==c['explicit_scope_metrics']['teaching_records']==420
contract,drafts,solutions,accepted=(c[k] for k in ['contract_checkpoint','complete_drafts_checkpoint','independent_solutions_checkpoint','accepted_text_checkpoint'])
exports=a.exports_checkpoint
after=metrics['after']; milestones=metrics['unit17_status_counts']
parity=pages['content_parity']['counts']
out={}

summary=f'**Unit 17 is complete:** [learner PDF](typesetting/ch17/chapter-17.pdf), {lp} pages, and [separate key PDF](typesetting/ch17/answer-key.pdf), {kp} pages. Connected exposition, praise and figurative language are taught through {systems} complete bounded systems / {cells:,} cells and {tasks} tasks, including all 82 Cook XII, XIII.37–43 prompts. The complete 252-word music-performance episode from *Apollonius* has local help and all 19 original notes / 20 anchors. Fresh independent reviews and non-author inspection of all {total} pages are complete. See the [review and export record](typesetting/ch17/README.md).'
s=replace_once(text('README.md'),'**Units 1–16 are complete**','**Units 1–17 are complete**')
s=replace_once(s,'<!-- course-unit-summaries -->',summary+'\n\n<!-- course-unit-summaries -->')
out['README.md']=s

s=text('curriculum/COURSE_PLAN.md')
oldrow=next(line for line in s.splitlines() if line.startswith('| 17.'))
newrow='| 17. Connected exposition, praise, and figurative language | Comparative, relative, conditional and participial constructions across report, praise and petition; personal adjectives and nominalized participles; literal structure and contextual meaning. Complete new systems retain explicit sense and syntax limits. | Joint Group XII, XIII, Exercises 37–43: all 82 items, plus 21 original tasks. | The complete 252-word music-performance episode, Cook 174.7–175.17 / PDF 190–191, with local help and all 19 original notes / 20 anchors. |'
s=replace_once(s,oldrow,newrow)
s=s.replace('Exercises 1–36 now have full item-level audits; Exercises 37–48 still require them.','Exercises 1–43 now have full item-level audits; Exercises 44–48 still require them.')
s=replace_once(s,'The current crosswalk is **515 assigned and 129 deferred items**.','Through Unit 16 the crosswalk was **515 assigned and 129 deferred items**.')
para=f'The [Unit 17 source audit](../sources/audits/unit17-source/source-report.md), [grammar audit](../sources/audits/unit17-grammar/REPORT.md) and [contract](../chapters/ch17/coverage.json) establish all 82 joint XII, XIII.37–43 prompts and the complete music-performance scene. The {systems} bounded systems / {cells:,} cells appear in literal tables. Four translated examples support the practice; the 21 original tasks request {original_outputs} responses, and all {tasks} tasks together request {outputs}. The amended contract identifies {features} grammar features and {teaching} teaching records. The complete Cook sets retain their original hints and Exercise 37’s global instruction. High quantities and source-specific expressions remain visibly supplied. All 19 original notes / 20 anchors remain; later love and gifts are unassigned. The current crosswalk is **597 assigned and 47 deferred items**.'
s = replace_once(s, 'Active coverage contracts, not this plan,', para + '\n\nActive coverage contracts, not this plan,')
out['curriculum/COURSE_PLAN.md']=s

s=text('curriculum/COOK_MAP.md')
s=replace_once(s,'The current canonical crosswalk is **515 assigned, 129 deferred and none excluded**','Through Unit 16 the canonical crosswalk was **515 assigned, 129 deferred and none excluded**')
s=s.replace('Exercises **1–36** now have full item-level linguistic audits; Exercises **37–48** remain structurally audited only.','Exercises **1–43** now have full item-level linguistic audits; Exercises **44–48** remain structurally audited only.')
para='The [Unit 17 contract](../chapters/ch17/coverage.json) assigns all **82 exact joint XII, XIII.37–43 prompts**: 14, 10, 7, 10, 12, 9 and 20 items respectively. Original IDs remain EX-XII-XIII-NN-NN; the Exercise 37 global instruction remains attached to all fourteen items. The current canonical crosswalk is **597 assigned, 47 deferred and none excluded**, totaling all 644 items. The exact 252-word music-performance episode spans printed 174.7–175.17 / one-based PDF 190–191, from **Ðā ēode hēo ūt** through **ðe hē forðtēah.** Individual lines are editorial counts anchored by printed marginal numbers. All 19 original notes and 20 anchors remain, including 174.12a and both note-17 attachments. The following love and gifts remain unassigned. Twenty-one original tasks accompany the source work.'
s=replace_once(s,'All exercise boundaries and terminal item numbers have been checked against images.',para+'\n\nAll exercise boundaries and terminal item numbers have been checked against images.')
out['curriculum/COOK_MAP.md']=s

s=text('sources/README.md')
s=s.replace('Exercises 1–36 now have separate item-level audits; Exercises 37–48 still require them.','Exercises 1–43 now have separate item-level audits; Exercises 44–48 still require them.')
s=replace_once(s,'The current crosswalk is 515 assigned / 129 deferred out of 644; Exercises 1–36 have full item-level audits.','At the Unit 16 checkpoint the crosswalk was 515 assigned / 129 deferred out of 644; Exercises 1–36 had full item-level audits.')
s+=f'\nUnit 17’s [source audit](audits/unit17-source/source-report.md), [grammar audit](audits/unit17-grammar/REPORT.md), [design](../curriculum/proposals/unit17/REPORT.md) and [coordinator reconciliation](audits/unit17-coordinator/reconciliation.json) establish all 82 Cook XII, XIII.37–43 prompts and the exact 252-word music-performance episode. The [contract](../chapters/ch17/coverage.json) retains {tasks} tasks / {outputs} outputs, {systems} bounded systems / {cells:,} literal cells, four translated examples and all 19 original notes / 20 anchors. [Preserved morphology corrections](audits/unit17-source/morphology-correction-01.json) distinguish evidenced full-stem mægen obliques from the withdrawn contraction proposal and limit andgiet to its assigned abstract singular. The [numeral record](audits/unit17-coordinator/numeral-42-02.json) supplies the whole 144,000 expression from the inspected Bosworth–Toller parallel, retaining collective ðæt and final -o without a general numeral-case claim. [Wright evidence](audits/unit17-coordinator/niwe-42-02.json) supports supplied nīwne sang by an explicit class rule. [Fresh text review](../chapters/ch17/review.md) and [separate paradigm review](../chapters/ch17/reviews/paradigms.json) resolve material findings; their final amendments govern any later refinements while the original audit packets remain unchanged. The current crosswalk is 597 assigned / 47 deferred out of 644; Exercises 1–43 have full item-level audits.\n'
out['sources/README.md']=s

registry=read('sources/registry.json')
uses={
 'cook_ex_1895':{'source_record':'sources/audits/unit17-source/exercises-prompts.json','inspection_record':'sources/audits/unit17-source/evidence-catalog.json','scope':'All 82 joint XII, XIII Exercises 37–43 items, printed 22–28 / one-based PDF 30–36, including every original hint and the complete Exercise 37 global instruction.'},
 'cook_fb_1895_2':{'source_record':'sources/audits/unit17-source/evidence-catalog.json','grammar_record':'sources/audits/unit17-grammar/evidence-catalog.json','review':'chapters/ch17/reviews/paradigms.json','scope':'Exact 252-word music-performance episode at printed 174.7–175.17 / one-based PDF 190–191, with 19 original notes and 20 anchors. Individual line counts are editorial. Selected grammar and vocabulary pages support the bounded current systems; no claim that every rule-derived cell is separately attested.'},
 'wright_oe_1914':{'coordinator_record':'sources/audits/unit17-coordinator/niwe-42-02.json','inspection_record':'sources/audits/unit17-coordinator/primary-inspections.json','review':'chapters/ch17/reviews/paradigms.json','scope':'Actually inspected printed 49 §90 / PDF69, 213 §433 / PDF233 and 214 §434 / PDF234 establish nīwe quantity, the wilde paradigm and explicit class membership. The supplied nīwne is rule-derived; no separate token-attestation claim.'},
 'bosworth_toller_1898_1921':{'source_record':'sources/audits/unit17-source/evidence-catalog.json','grammar_record':'sources/audits/unit17-grammar/evidence-catalog.json','coordinator_record':'sources/audits/unit17-coordinator/primary-inspections.json','numeral_record':'sources/audits/unit17-coordinator/numeral-42-02.json','review':'chapters/ch17/reviews/paradigms.json','scope':'Inspected primary facsimiles support the selected lexical senses, government and forms. Main1082 supplies the complete 144000 exclusion parallel with collective ðæt and final-o ðūsendo; declared acute-to-macron normalization is retained. Source transcriptions serve only as finding aids.'}}
seen=set()
for section in ['selected_sources','supporting_sources']:
    for entry in registry[section]:
        sid=entry['source_id']
        if sid in uses:
            assert 'unit17_use' not in entry,sid
            entry['unit17_use']=uses[sid];seen.add(sid)
assert seen==set(uses)
out['sources/registry.json']=json.dumps(registry,ensure_ascii=False,indent=2)+'\n'

s=text('typesetting/README.md')
para=f'The reviewed [Unit 17 exports](ch17/README.md) have **{lp} learner and {kp} key pages**. Every final page has a non-author visual record, complete text/table parity and final file identities.'
s=replace_once(s,'Use `chapter-template.tex` as a minimal document shell',para+'\n\nUse `chapter-template.tex` as a minimal document shell')
out['typesetting/README.md']=s

out['typesetting/ch17/README.md']=f'''# Unit 17 exports: connected exposition, praise and figurative language

The complete [learner PDF](chapter-17.pdf) has **{lp} pages** and the separate [answer key](answer-key.pdf) **{kp}**. Their editable masters are [student.md](../../chapters/ch17/student.md) and [answer-key.md](../../chapters/ch17/answer-key.md). All {total} final pages passed non-author inspection; [page-review.json](page-review.json) binds the final PDFs and page images to the individual inspection ledgers.

The exports include all {tasks} tasks / {outputs} answer positions, all 82 assigned Cook prompts, {systems} complete bounded systems / {cells:,} literal cells, four translated examples, the full 252-word music-performance episode and all 19 original notes / 20 anchors. Original source notes and modern help remain separate. The key gives the complete translation, models, targets, essential meanings, alternatives and diagnoses.

[Full content parity](content-parity.json) verifies {parity['paragraph_heading_list_blocks']:,} prose/heading/list blocks, {parity['original_tables']} tables and {parity['original_table_cells_including_headers']:,} table cells including headers. It checks complete Markdown/TeX content and PDF characters alongside visual inspection. The final logs have no missing-character, font-substitution, box or rerun warnings. [Layout adjustments](layout-adjustments.json) retain the repair history. Cambria and the inherited 165 × 241 mm layout remain in use.

The [contract](../../chapters/ch17/coverage.json) preceded prose at `{contract}`. Drafts are saved at `{drafts}`, frozen independent solutions at `{solutions}`, and accepted text at `{accepted}`. The [fresh text review](../../chapters/ch17/review.md) and [separate paradigm review](../../chapters/ch17/reviews/paradigms.json) resolve material findings. [Authoring amendments](../../chapters/ch17/authoring-amendments.json) preserve the original decisions and later repairs. Complete exports/registers are saved at `{exports}`.

## Reproduction

Build the retained TeX from `typesetting/ch17` using LuaLaTeX and Cambria. Repeat each command if the log requests stable references:

```powershell
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-17.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
```

Extract the build PDFs to `build/chapter-17.txt` and `build/answer-key.txt` with `pdftotext -enc UTF-8 -layout`. From the repository root run:

```powershell
python -X utf8 typesetting/ch17/build/_check_content_parity.py
python -X utf8 scripts/check_unit17.py --draft --tex
```

The installed Xpdf executable is `C:/Program Files/Git/mingw64/bin/pdftotext.exe`; use PowerShell’s call operator before the quoted path. The assembly helper records the initial conversion; rerunning it can discard manual layout repairs. Rebuilding does not replace the accepted PDFs or establish a new visual review. Render changed exports into a fresh version and preserve earlier inspected images and ledgers. Typesetting does not regenerate the active registers or sealed source packets.
'''

status=text('STATUS.md')
old_table=re.search(r'\| Unit \| Grammar \| Learner / key pages \| Complete exports/registers \|\n.*?(?=\n\n)',status,re.S)[0]
table=old_table+f'\n| [17](typesetting/ch17/README.md) | Connected exposition, praise and figurative language | {lp} / {kp} | {exports} |'
out['STATUS.md'] = f"# Status\n\nUpdated 28 October 2026. **Units 1–17 are complete and independently reviewed**, with complete learner/key PDFs, every-page inspection and integrated teaching registers. Complete Unit 17 exports and registers are saved at **`{exports}`**. The eighteen-unit outline and all 644 Cook item mappings remain settled. Unit 18 remains undrafted; begin only when requested.\n\n## Completed Unit 17\n\nThe [brief](curriculum/UNIT_17_BRIEF.md) and [contract](chapters/ch17/coverage.json) cover connected exposition, praise and figurative language. All **82 Cook joint XII, XIII.37–43 prompts** remain in complete sets, with the global Exercise 37 instruction, 21 original tasks and four translated examples. There are **{tasks} tasks / {outputs} answer positions** and **{systems} complete bounded systems / {cells:,} literal cells**. Form knowledge, lexical meaning and syntactic scope remain distinct.\n\nThe exact **252-word music-performance episode** is Cook 174.7–175.17 / one-based PDF 190–191. Individual line numbers are editorial counts anchored by printed marginal numbers. All **19 original notes / 20 anchors** remain, including the swīgende note 12a and both note-17 attachments. English context supplies the preceding banquet; subsequent love and gifts remain unassigned. No additional narrative was composed.\n\nA fresh non-author froze [all independent solutions](chapters/ch17/independent-solutions.md) at **`{solutions}`** before current key/contract/audit access. The [review](chapters/ch17/review.md), [output ledger](chapters/ch17/review-ledger.json) and separate [paradigm review](chapters/ch17/reviews/paradigms.json) resolve all material findings. Original witnesses and sealed packets remain unchanged; [amendments](chapters/ch17/authoring-amendments.json) record later repairs. Checkpoints: contract **`{contract}`**, drafts **`{drafts}`**, accepted text **`{accepted}`**.\n\nThe [learner PDF](typesetting/ch17/chapter-17.pdf) has **{lp} pages** and the [key](typesetting/ch17/answer-key.pdf) **{kp}**. All **{total} final pages** passed non-author visual inspection. [Full parity](typesetting/ch17/content-parity.json) and [presentation acceptance](typesetting/ch17/page-review.json) bind complete content, final PDF/image identities and clean logs.\n\n## Completed course artifacts\n\n{table}\n\nEach unit retains its contract, evidence, editable learner and separate key, frozen solutions, independent reviews, complete TeX/PDFs and page ledgers.\n\n## Registers and boundaries\n\nThe [lexicon](lexicon/entries.json) contains **{after['lemmas']:,} lemmas, {after['forms']:,} forms and {after['senses']:,} senses**; [grammar](curriculum/grammar.json) contains **{after['features']:,} constructions**. Unit 17 establishes {milestones['forms']['new_production']:,} productive form milestones, {milestones['forms']['new_recognition_only']} recognition-only forms, {milestones['senses']['new_production']} productive senses and {milestones['features']['new_production']} productive constructions. Supplied exposure remains separate from independent recall.\n\nThe [integration audit](chapters/ch17/register-integration.json) preserves earlier records, analyses, surfaces, metadata, evidence, supplied histories and earliest milestones against **`defa800`**. All **{reg['prior_active_files_preserved']:,} fixed earlier active artifacts** remain unchanged. Do not recapture the immutable sixteen-unit baseline or rerun older integration helpers.\n\nThe canonical crosswalk is **597 assigned / 47 deferred / none excluded**, totaling 644 numbered items. Exercises **1–43** have full item-level audits; **44–48** still require them. Active contracts govern assignments. Before another requested unit, read all seventeen active contracts and actual registers, and use the sole-coordinator Beads workflow. No remote or publication is configured.\n"

handoff=text('docs/HANDOFF.md')
checkpoints=re.search(r'\| Unit \| Contract before prose \| Accepted text \| Complete exports/registers \| Final handoff \| Learner/key pages \|\n.*?(?=\n\n)',handoff,re.S)[0]
checkpoints=checkpoints.replace('| 16 | 543e214 | bbf014e | edb1bbb | This handoff checkpoint | 67 / 32 |','| 16 | 543e214 | bbf014e | edb1bbb | defa800 | 67 / 32 |')
checkpoints+=f'\n| 17 | {contract} | {accepted} | {exports} | This handoff checkpoint | {lp} / {kp} |'
out['docs/HANDOFF.md'] = f"# Handoff to the next session\n\nThe requested **Unit 17 is complete**. Units 1–17 have independently reviewed learner/key masters, complete LuaLaTeX exports, every-page inspection and integrated registers. Complete Unit 17 exports/registers are saved at **`{exports}`**. The main [README](../README.md), [course/source map](../curriculum/COOK_MAP.md), [registry](../sources/registry.json) and [typesetting index](../typesetting/README.md) include Unit 17. **Unit 18 remains undrafted; begin only when requested.**\n\n## Unit 17 evidence and review\n\nThe [contract](../chapters/ch17/coverage.json) preceded prose at **`{contract}`**. Complete drafts were saved at **`{drafts}`**. A fresh non-author froze all [pre-key solutions](../chapters/ch17/independent-solutions.md) at **`{solutions}`** under the [strict protocol](../sources/audits/unit17-coordinator/review-independence.json) before current key/contract/audit access. The [freeze record](../chapters/ch17/blind-freeze.json) verifies every actual requested output was attempted. The [review](../chapters/ch17/review.md), [ledger](../chapters/ch17/review-ledger.json) and separate [paradigm review](../chapters/ch17/reviews/paradigms.json) accept all **{tasks} tasks / {outputs} outputs** and **{systems} systems / {cells:,} cells**. Accepted text is saved at **`{accepted}`**. No material finding remains open.\n\nAll 82 Cook joint XII, XIII.37–43 items remain, with counts 14/10/7/10/12/9/20 and original EX-XII-XIII-NN-NN IDs. Exercise 37’s article/second-person-pronoun omission remains a local instruction. The reading is the exact 252-word performance episode, **174.7–175.17 / PDF 190–191**, from Ðā ēode hēo ūt through ðe hē forðtēah. All 19 original notes / 20 anchors remain; individual line counts are editorial. The following love and gifts are unassigned.\n\nUse the final [amendments](../chapters/ch17/authoring-amendments.json) and independent review alongside the frozen audit packets. The selected mægen obliques retain the full stem; andgiet has four assigned abstract singular cases without a defectiveness claim. Gelīefst in the reading means permit, with a separate supplied homonym identity. The whole 144,000 expression retains collective ðæt and final-o ðūsendo; it does not establish a general numeral-case rule. Supplied nīwne sang is rule-derived from inspected Wright pages. Hālga, masculine horn, endingless accusative cwēn, descendants sǣd and husband wer retain their explicit senses and evidence. Original translation witnesses remain unchanged.\n\nThe [learner PDF](../typesetting/ch17/chapter-17.pdf) has **{lp} pages** and the [key](../typesetting/ch17/answer-key.pdf) **{kp}**. All **{total} final pages** have non-author visual records bound to final file identities. [Presentation acceptance](../typesetting/ch17/page-review.json) reconciles complete parity and clean logs. The [export README](../typesetting/ch17/README.md) provides reproduction and layout records.\n\n## Registers and preservation\n\nThe [integration record](../chapters/ch17/register-integration.json) preserves every prior record, earliest milestone, supplied history, source surface, analysis and metadata history. Totals are **{after['lemmas']:,} lemmas, {after['forms']:,} forms, {after['senses']:,} senses and {after['features']:,} features**. Current unit milestones remain distinct from supplied exposure.\n\nThe immutable ignored `build/unit17-prior-baseline.json` captures the actual sixteen-unit state at **`defa8008f6887a1f5f6afe9db27431d500a03f67`**: 1,067 lemmas, 11,188 forms, 1,376 senses and 1,080 features. The retained [prior-state record](../sources/audits/unit17-coordinator/prior-state.json) identifies 2,935 earlier files including both registers. All 2,933 fixed nonregister artifacts remain unchanged. Do not recapture the baseline or rerun older mergers against integrated registers. Reused supplied words have explicit local-help or original-hint routes without new production milestones.\n\nThe canonical crosswalk is **597 assigned / 47 deferred / none excluded**, totaling 644. Exercises **1–43** have full item-level audits; **44–48** still require them. Active chapter contracts govern assignments.\n\n## Recoverable checkpoints\n\n{checkpoints}\n\n## Resuming and reproducing\n\nRead AGENTS.md, STATUS.md, EDITORIAL_POLICY.md, docs/WORKFLOW.md, the plan/map, source registry, all seventeen active contracts and actual registers. Run `bd prime`, then `bd ready`, serially. Root remains the sole embedded-Dolt writer. Begin another unit only when requested.\n\nUse parallel agents with exclusive files for independent source/curriculum analysis; reconcile and checkpoint the contract before prose. A fresh blind solver may read the actual learner master, earlier accepted teaching/registers and original primary images, but current contracts/audits/token maps can expose answers. Freeze every actual response in Git before explicit comparison access. Resolve independent review, inspect every exported page, integrate preserved registers, update indexes, export Beads and save local checkpoints. No remote push is configured.\n\nRun `python -X utf8 scripts/check_unit17.py --draft --tex` after rebuilding ignored PDF text/log products as described in the export README. Retained TeX preserves final layout; rerunning assembly can discard repairs. Raw and normalized-LF identities distinguish checkout conversion from textual changes. Completion metadata does not alter the substantive accepted contract. Do not rerun pre-prose assembly or old merge helpers against completed state.\n"

for path,content in out.items():
    Path(path).write_text(content.rstrip()+'\n',encoding='utf-8',newline='\n')
print('Updated',len(out),'completion indexes from actual accepted records; Unit18 remains undrafted.')
