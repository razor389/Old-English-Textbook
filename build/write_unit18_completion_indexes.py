"""Write final course indexes only from actual reviewed Unit18 acceptance records."""
import argparse,json,re
from pathlib import Path

ap=argparse.ArgumentParser();ap.add_argument('--exports-checkpoint',required=True);a=ap.parse_args()
assert re.fullmatch(r'[0-9a-f]{7,40}',a.exports_checkpoint)
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def txt(p):return Path(p).read_text(encoding='utf-8-sig')
def once(s,before,after):
    assert s.count(before)==1,(before,s.count(before))
    return s.replace(before,after,1)
c=read('chapters/ch18/coverage.json');pages=read('typesetting/ch18/page-review.json');reg=read('chapters/ch18/register-integration.json')
assert c['completion']['complete'] and pages['status']=='PASS' and reg['status']=='accepted'
assert c['textual_review']['status']==c['presentation_review']['status']=='accepted'
assert not pages['unresolved_findings']
m=c['contract_metrics'];p=pages['page_totals'];after=reg['metrics']['after']
lp,kp,total=p['learner'],p['key'],p['total']
tasks,outputs,systems,cells=(m[k] for k in ['tasks','requested_output_positions','paradigms','logical_cells'])
assert tasks==60 and outputs==87 and c['source_assignment_policy']['cumulative_assigned_cook_items']==644
contract,drafts,solutions,accepted=(c[k] for k in ['contract_checkpoint','complete_drafts_checkpoint','independent_solutions_checkpoint','accepted_text_checkpoint'])
exports=a.exports_checkpoint
out={}
summary=f'**Unit 18 is complete:** [learner PDF](typesetting/ch18/chapter-18.pdf), {lp} pages, and [separate key PDF](typesetting/ch18/answer-key.pdf), {kp} pages. Independent prose consolidation brings together {systems} complete defined systems / {cells:,} literal cells and {tasks} tasks / {outputs} answers. All 47 Cook XII, XIII.44–48 compositions remain, with 13 original practice groups and the exact 226-word love, gifts and farewell episode from *Apollonius*, including all 22 original notes / 29 anchors. Fresh independent reviews and non-author inspection of all {total} pages are complete. See the [review and export record](typesetting/ch18/README.md).'
s=once(txt('README.md'),'**Units 1–17 are complete**','**All 18 planned units are complete**')
s=once(s,'The earlier two-chapter experiment is preserved',summary+'\n\nAll **644 numbered Cook items** are assigned across the completed course; none remain deferred or excluded. The course does not claim coverage of every reader selection or of supplementary poetry.\n\nThe earlier two-chapter experiment is preserved')
out['README.md']=s

s=txt('curriculum/COURSE_PLAN.md')
old=next(x for x in s.splitlines() if x.startswith('| 18.'))
s=once(s,old,'| 18. Independent prose consolidation | Extended reading, selective parsing, translation and controlled composition using cumulative grammar, with complete newly required systems and explicit local support. | All 47 joint XII, XIII, Exercises 44–48 prompts, plus 13 original groups requesting 40 answers. Joseph supplies English composition. | The exact 226-word Apollonius love, gifts and farewell episode, Cook 175.18–177.2 / PDF 191–193; all 22 original notes / 29 anchors. |')
s=s.replace('Exercises 1–43 now have full item-level audits; Exercises 44–48 still require them.','Exercises 1–48 now have full item-level audits.')
s=s.replace('The current crosswalk is **597 assigned and 47 deferred items**.','Through Unit 17 the crosswalk was **597 assigned and 47 deferred items**.')
s=s.replace('All 19 original notes / 20 anchors remain; later love and gifts are unassigned.','All 19 original notes / 20 anchors remain; later love and gifts were unassigned at that checkpoint.')
para=f'The completed [Unit 18 contract](../chapters/ch18/coverage.json), [source audit](../sources/audits/unit18-source/source-gate-report.json) and [grammar audit](../sources/audits/unit18-grammar/grammar-report.md) establish all 47 final Cook compositions and the complete gifts-and-farewell passage. There are {systems} defined systems / {cells:,} literal cells, two translated examples and {tasks} tasks / {outputs} answers. Every supplied dependency remains visible; independent production, recognition and supplied exposure remain separate. The current crosswalk is **644 assigned, zero deferred and none excluded**. All eighteen planned units are complete; additional readings, poetry or a sequel require a separate request and contract.'
s=once(s,'Active coverage contracts, not this plan or the archive,',para+'\n\nActive coverage contracts, not this plan or the archive,')
out['curriculum/COURSE_PLAN.md']=s
s=txt('curriculum/COOK_MAP.md')
s=s.replace('The current canonical crosswalk is **597 assigned, 47 deferred and none excluded**','Through Unit 17 the canonical crosswalk was **597 assigned, 47 deferred and none excluded**')
s=s.replace('The following love and gifts remain unassigned.','The following love and gifts were unassigned at the Unit 17 checkpoint.')
s=s.replace('Exercises **1–43** now have full item-level linguistic audits; Exercises **44–48** remain structurally audited only.','Exercises **1–48** now have full item-level linguistic audits.')
para='The [Unit 18 contract](../chapters/ch18/coverage.json) assigns all **47 exact joint XII, XIII.44–48 prompts**, in complete sets of 8/9/9/11/10. Original EX-XII-XIII-NN-NN identifiers and all 154 original hints/controls remain. The final canonical crosswalk is **644 assigned, zero deferred and none excluded**. Joseph is the English composition sequence. The separately assigned 226-word Apollonius reading spans **175.18–177.2 / PDF 191–193**, from **Sōðlice, mid-ðȳ-ðe ðæs cyninges dohtor geseah** through **ðæt wē mægen ūs geręstan.** All 26 physical lines, 22 notes and 29 anchors remain. Line counts are editorial, anchored by printed marginal numbers. The next episode, Apollonius as Teacher, is unassigned. Thirteen original practice groups request forty answers.'
s=once(s,'All exercise boundaries and terminal item numbers have been checked against images.',para+'\n\nAll exercise boundaries and terminal item numbers have been checked against images.')
out['curriculum/COOK_MAP.md']=s
s=txt('sources/README.md').replace('Exercises 1–43 now have separate item-level audits; Exercises 44–48 still require them.','Exercises 1–48 now have separate item-level audits.')
s=s.replace('The current crosswalk is 597 assigned / 47 deferred out of 644; Exercises 1–43 have full item-level audits.','At the Unit 17 checkpoint the crosswalk was 597 assigned / 47 deferred out of 644; Exercises 1–43 had full item-level audits.')
s+='\nUnit 18’s [source report](audits/unit18-source/source-gate-report.json), [grammar report](audits/unit18-grammar/grammar-report.md), [design](../curriculum/proposals/unit18/REPORT.md) and [coordinator reconciliation](audits/unit18-coordinator/reconciliation.json) establish all 47 final compositions and the exact 226-word Apollonius continuation. All 154 source controls and 22 reading notes / 29 anchors remain. [Query resolutions](audits/unit18-source/query-resolutions.json) distinguish our corrected transcription errors from source errors, preserve the source servant phrase with supplied analysis, and document exact form/name locators. Crawford1922 supplies corroboration only, not a new assigned reading. The original findan-error hypothesis was withdrawn after checking actual Unit4 teaching and primary evidence. [Final amendments](../chapters/ch18/authoring-amendments.json), [fresh review](../chapters/ch18/review.md) and [separate paradigm review](../chapters/ch18/reviews/paradigms.json) govern subsequent refinements while sealed packets remain intact. All644 Cook items are now assigned; none remain deferred or excluded. All48 exercises have full item-level audits.\n'
out['sources/README.md']=s

r=read('sources/registry.json')
uses={
 'cook_ex_1895':{'source_record':'sources/audits/unit18-source/exercises-prompts.json','scope':'All 47 joint XII, XIII Exercises 44–48 prompts, printed 29–33 / PDF 37–41; all 154 hints and controls retained.'},
 'cook_fb_1895_2':{'source_record':'sources/audits/unit18-source/reading-source.json','scope':'Exact 226-word Apollonius 175.18–177.2 / PDF 191–193, 26 physical lines, 22 notes and 29 anchors; selected grammar/glossary pages support explicit systems and local help.'},
 'wright_oe_1914':{'scope':'Selected primary-image rules corroborate explicitly bounded morphology and exceptions; §559(3), printed 295 / PDF 315, supports dative ætforan in the reviewed correction. Reused archived images supply evidence, never inherited teaching milestones.'},
 'bosworth_toller_1898_1921':{'scope':'Personally inspected dictionary facsimiles support selected senses, government, quantity and source phrases. Review additions include main pages 21, 576 and 697 and Supplement 330 for the bounded A05 support. Attested quotation, normalized transcription and rule-derived forms remain distinct.'},
 'crawford_heptateuch_1922':{'scope':'Corroboration only: printed 190–195 correspond to PDF 214–219; title PDF 9. Exact instrumental phrase, æcernu variant, names and substitution parallel; review also checks respectful leof, Hwilum ær, the material frame with unprefixed Fille, and On mergen with morgen in the apparatus. No assigned Joseph reading and no claim that this was Cook’s edition.'}}
seen=set()
for group in ['selected_sources','supporting_sources']:
    for entry in r[group]:
        sid=entry['source_id']
        if sid in uses:
            assert 'unit18_use' not in entry,sid
            entry['unit18_use']={**uses[sid],'source_evidence':'sources/audits/unit18-source/evidence-catalog.json','grammar_evidence':'sources/audits/unit18-grammar/evidence-catalog.json','review_support':'chapters/ch18/support-amendment-spec.json','author_support_report':'chapters/ch18/review-evidence/grammar-support.json','independent_review':'chapters/ch18/reviews/paradigms.json'};seen.add(sid)
        if sid=='cook_ex_1895':
            entry['verification']='All 48 exercise boundaries and terminal counts structurally checked; all Exercises 1–48 now have full item-level linguistic audits. Completed active contracts assign all 644 numbered items with zero remaining deferrals/exclusions. Historical audit records retain their original scope.'
assert seen==set(uses)
out['sources/registry.json']=json.dumps(r,ensure_ascii=False,indent=2)+'\n'
s=once(txt('typesetting/README.md'),'Use `chapter-template.tex` as a minimal document shell',f'The reviewed [Unit 18 exports](ch18/README.md) have **{lp} learner and {kp} key pages**. Every final page has a non-author visual record, complete text/table parity and final identities. All eighteen planned units now have complete exports.\n\nUse `chapter-template.tex` as a minimal document shell')
out['typesetting/README.md']=s
parity=pages['content_parity']['counts']
out['typesetting/ch18/README.md']=f'''# Unit 18 exports: independent prose consolidation

The complete [learner PDF](chapter-18.pdf) has **{lp} pages**; the separate [key](answer-key.pdf) has **{kp}**. Editable masters are [student.md](../../chapters/ch18/student.md) and [answer-key.md](../../chapters/ch18/answer-key.md). All {total} final pages passed actual non-author visual inspection; [page-review.json](page-review.json) binds both PDFs and every page image to individual inspection ledgers.

Both exports retain {tasks} tasks / {outputs} requested answers, all47 final Cook prompts, {systems} defined systems / {cells:,} literal cells, two translated examples, the full226-word passage and all22 original notes /29 anchors. The separate key gives models, targets, meanings, explanations, alternatives and diagnoses. [Full parity](content-parity.json) checks {parity['paragraph_heading_list_blocks']:,} prose/heading/list blocks, {parity['original_tables']} tables and {parity['original_table_cells_including_headers']:,} table cells. Final logs have no missing-character, font-substitution, box or rerun warnings. [Layout adjustments](layout-adjustments.json) preserve repairs. Cambria and the established165×241mm layout remain.

Checkpoints: contract `{contract}`, complete drafts `{drafts}`, frozen independent solutions `{solutions}`, accepted text `{accepted}`, complete exports/registers `{exports}`. [Fresh text review](../../chapters/ch18/review.md), [separate paradigm review](../../chapters/ch18/reviews/paradigms.json) and [amendments](../../chapters/ch18/authoring-amendments.json) retain evidence and resolutions.

## Reproduction

From `typesetting/ch18`, compile the retained TeX twice with LuaLaTeX and Cambria:

```powershell
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-18.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
```

Use `pdftotext -enc UTF-8 -layout` to extract the build PDFs to `build/chapter-18.txt` and `build/answer-key.txt`. The installed executable is `C:/Program Files/Git/mingw64/bin/pdftotext.exe`; PowerShell requires its call operator before a quoted executable path. From the repository root run:

```powershell
python -X utf8 typesetting/ch18/build/_check_content_parity.py
python -X utf8 scripts/check_unit18.py --draft --tex
```

Rerunning assembly can discard manual layout repairs. Rebuilding does not replace accepted PDFs or establish new visual acceptance. Preserve inspected images/ledgers and render changed exports into a fresh version. Do not regenerate sealed audits or rerun register mergers against completed state.
'''
out['chapters/ch18/README.md']=f'''# Unit 18: independent prose consolidation

Complete and independently reviewed. Read the [learner](student.md) with the [separate key](answer-key.md), or use the complete [PDF exports](../../typesetting/ch18/README.md).

The [contract](coverage.json) preceded prose. Its {tasks} tasks request {outputs} answers; all47 Cook44–48 items and the complete226-word Apollonius passage remain. [Frozen solutions](independent-solutions.md), [fresh review](review.md), [paradigm review](reviews/paradigms.json), [amendments](authoring-amendments.json) and [register integration](register-integration.json) document acceptance and preservation.

This finishes the planned eighteen-unit course and the assignment of all644 Cook items. Further readings or supplementary poetry require a separate request.
'''
oldstatus=txt('STATUS.md')
table=re.search(r'\| Unit \| Grammar \| Learner / key pages \| Complete exports/registers \|\n.*?(?=\n\n)',oldstatus,re.S)[0]
table+=f'\n| [18](typesetting/ch18/README.md) | Independent prose consolidation | {lp} / {kp} | {exports} |'
out['STATUS.md']=f'''# Status

Updated28 October2026. **All18 planned units are complete**, independently reviewed, exported in full and integrated into the teaching registers. Unit18 complete exports/registers are saved at **`{exports}`**. All644 numbered Cook items are assigned; zero remain deferred or excluded. No sequel or supplementary poetry is drafted.

## Completed Unit18

The [contract](chapters/ch18/coverage.json) covers all47 joint XII,XIII Exercises44–48 prompts,13 original practice groups, two translated examples and the exact226-word love, gifts and farewell passage at Cook175.18–177.2 / PDF191–193. All154 original controls and22 reading notes /29 anchors remain. There are **{tasks} tasks /{outputs} answers** and **{systems} defined systems /{cells:,} literal cells**, with explicit production, recognition and supplied boundaries.

Contract `{contract}` preceded prose; complete drafts are `{drafts}`. A fresh non-author froze every [solution](chapters/ch18/independent-solutions.md) at `{solutions}` before key/current-contract/audit access. [Fresh review](chapters/ch18/review.md) and [separate paradigm review](chapters/ch18/reviews/paradigms.json) resolve material findings; accepted text is `{accepted}`. [Amendments](chapters/ch18/authoring-amendments.json) retain changes without rewriting earlier witnesses.

The [learner PDF](typesetting/ch18/chapter-18.pdf) has **{lp} pages**, the [key](typesetting/ch18/answer-key.pdf) **{kp}**. All **{total} final pages** passed non-author inspection, [full parity](typesetting/ch18/content-parity.json) and [presentation acceptance](typesetting/ch18/page-review.json).

## Completed course artifacts

{table}

Each unit retains its contract, evidence, learner/key masters, frozen solutions, reviews, full TeX/PDFs and page ledgers.

## Registers and preservation

The lexicon contains **{after['lemmas']:,} lemmas, {after['forms']:,} forms and {after['senses']:,} senses**; grammar contains **{after['features']:,} features**. Supplied exposure remains distinct from independent recall. The [integration audit](chapters/ch18/register-integration.json) preserves all earlier records, analyses, surfaces, metadata, supplied histories and earliest milestones against `0eda277`. All **{reg['prior_active_files_preserved']:,} fixed earlier artifacts** and **{reg['archived_files_preserved']} archived files** remain unchanged. Do not recapture the seventeen-unit baseline or rerun older mergers.

All Exercises1–48 have full item-level audits. Active contracts govern assignment; completion does not imply mastery of every reader selection. Further work requires a new request. Beads uses one coordinator writer; no remote or publication is configured.
'''
oldhandoff=txt('docs/HANDOFF.md')
checks=re.search(r'\| Unit \| Contract before prose \| Accepted text \| Complete exports/registers \| Final handoff \| Learner/key pages \|\n.*?(?=\n\n)',oldhandoff,re.S)[0]
rows=checks.splitlines()
rows=[line.replace('This handoff checkpoint','0eda277') if line.startswith('| 17 |') else line for line in rows]
checks='\n'.join(rows)+f'\n| 18 | {contract} | {accepted} | {exports} | This handoff checkpoint | {lp} / {kp} |'
out['docs/HANDOFF.md']=f'''# Handoff

The requested **Unit18 and the planned eighteen-unit course are complete**. All units have independently reviewed learner/key masters, complete LuaLaTeX exports, every-page inspection and integrated registers. Unit18 exports/registers are saved at **`{exports}`**. The [main README](../README.md), plan/map, source registry and typesetting index include the final unit. No further unit or supplement is authorized by this completion.

## Final unit and evidence

The [contract](../chapters/ch18/coverage.json) preceded prose at `{contract}`. Complete drafts are `{drafts}`; the fresh non-author’s unchanged [solutions](../chapters/ch18/independent-solutions.md) were frozen at `{solutions}` before key/current-contract/audit access. [Review](../chapters/ch18/review.md), [output ledger](../chapters/ch18/review-ledger.json) and [separate paradigm review](../chapters/ch18/reviews/paradigms.json) accept all {tasks} tasks /{outputs} answers and {systems} systems /{cells:,} cells. Accepted text is `{accepted}`. No material finding remains open.

All47 joint XII,XIII.44–48 items retain complete8/9/9/11/10 sets and154 controls. Joseph is English composition. The separately assigned226-word Apollonius continuation is175.18–177.2 / PDF191–193, ending with the proposal to go and rest; it does not report completed arrival. All26 physical lines,22 original notes and29 anchors remain. Apollonius as Teacher is unassigned.

Consult final [amendments](../chapters/ch18/authoring-amendments.json) and review alongside sealed audits. Initial audit lęcgað/ðēowra readings were corrected to actual lęcgeað/ðēowa; these were transcription errors, not Cook errors. Servant-phrase historical classification stays bounded and supplied. Earlier findan3sgfunde is valid under Unit4; the contrary provisional finding was withdrawn. Reading225ūs uses the actual prior accusative record; selected ēowerre has dative feminine agreement. Crawford1922 is corroboration only. Earlier witnesses remain intact.

The [learner PDF](../typesetting/ch18/chapter-18.pdf) has {lp} pages and the [key](../typesetting/ch18/answer-key.pdf) {kp}. All {total} final pages have actual non-author visual records bound to final identities, complete parity and clean logs. [Reproduction instructions](../typesetting/ch18/README.md) preserve the final layout workflow.

## Registers and boundaries

Totals: **{after['lemmas']:,} lemmas, {after['forms']:,} forms, {after['senses']:,} senses and {after['features']:,} features**. [Integration](../chapters/ch18/register-integration.json) preserves every earlier per-chapter record, earliest milestone, supplied history, source surface, analysis and metadata history.

The retained immutable `build/unit18-prior-baseline.json` captures seventeen-unit state at `0eda27783a3830fbd10bebef3702e27c15ff837c`:1197lemmas,12557forms,1573senses and1143features. The [prior-state record](../sources/audits/unit18-coordinator/prior-state.json) identifies3290files including registers; all3288fixed nonregister artifacts and134archive files remain unchanged. Do not recapture the baseline or rerun earlier integration helpers.

The final canonical crosswalk is **644 assigned /0deferred /none excluded**. All48exercises have full item-level audits. Source completeness is not a claim that every reader passage or all Old English grammar has been taught.

## Recoverable checkpoints

{checks}

## Resuming

Read AGENTS.md, STATUS.md, EDITORIAL_POLICY.md, docs/WORKFLOW.md, the plan/map, source registry, all18active contracts and actual registers. Run `bd prime`, then `bd ready`, serially. Root remains the sole embedded-Dolt writer. Await a new request before additional course content.

For requested revisions, preserve originals and scope, make bounded amendments, repeat affected independent checks and actually inspect changed export pages. Use `python -X utf8 scripts/check_unit18.py --draft --tex` after reproducing ignored log/text products as documented. Retained TeX includes final layout repairs; assembly may discard them. Raw and normalized-LF identities distinguish checkout conversion from content changes. Export Beads and commit locally; no remote push is configured.
'''
spacing={
 'Unit18':'Unit 18','All18':'All 18','all18':'all 18','all47':'all 47','All47':'All 47',
 'all644':'all 644','All644':'All 644','All48':'All 48','all48':'all 48','all22':'all 22',
 'all154':'all 154','All154':'All 154','All26':'All 26','all3288':'all 3,288',
 'Updated28 October2026':'Updated 28 October 2026','18planned':'18 planned',
 '18active':'18 active','48exercises':'48 exercises','48 exercise':'48 exercise',
 'Cook175':'Cook 175','Cook44':'Cook 44','Exercises1':'Exercises 1',
 'PDF191':'PDF 191','PDF214':'PDF 214','PDF9':'PDF 9','Crawford1922':'Crawford 1922',
 'full226':'full 226','complete226':'complete 226','assigned226':'assigned 226','exact226':'exact 226',
 'all47':'all 47','all22':'all 22','complete8/9':'complete 8/9','sets and154':'sets and 154',
 '22notes':'22 notes','29anchors':'29 anchors','26physical':'26 physical',
 '26 physical':'26 physical','22 reading':'22 reading','Cook177':'Cook 177',
 'Exercises44':'Exercises 44','printed29':'printed 29','PDF37':'PDF 37',
 'printed190':'printed 190','PDF214':'PDF 214','165×241mm':'165 × 241 mm',
 'established165':'established 165','word and22':'word and 22','and22':'and 22',
 'and13':'and 13','prompts,13':'prompts, 13','all48':'all 48',
 '18planned':'18 planned','Unit4':'Unit 4','findan3sgfunde':'findan third-singular funde',
 'Reading225ūs':'Reading token 225 ūs','reading225ūs':'reading token 225 ūs',
 '1143features':'1,143 features','1573senses':'1,573 senses','12557forms':'12,557 forms',
 '1197lemmas':'1,197 lemmas','identifies3290files':'identifies 3,290 files',
 '3288fixed':'3,288 fixed','134archive':'134 archive','0deferred':'0 deferred',
 '1143features':'1,143 features','and1143':'and 1,143','all644':'all 644',
 'all154':'all 154','22 original notes /29':'22 original notes / 29',
 ' /0':' / 0',' /{outputs}':' / {outputs}'
}
for path,content in out.items():
    if path.endswith('.md'):
        for before,replacement in spacing.items():content=content.replace(before,replacement)
    Path(path).write_text(content.rstrip()+'\n',encoding='utf-8',newline='\n')
print('Updated',len(out),'indexes from actual final acceptance; all18planned units complete.')
