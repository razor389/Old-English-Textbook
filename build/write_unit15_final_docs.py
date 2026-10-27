"""Write the course handoff only from accepted Unit15 artifacts."""
import argparse
import json
import re
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--exports-checkpoint',default='this export checkpoint');a=p.parse_args()
def read(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def write(path,text):Path(path).write_text(text.strip()+'\n',encoding='utf-8',newline='\n')
c=read('chapters/ch15/coverage.json');pages=read('typesetting/ch15/page-review.json');reg=read('chapters/ch15/register-integration.json');parity=read('typesetting/ch15/content-parity.json')
assert c['textual_review']['status']==c['presentation_review']['status']=='accepted'
assert pages['status']=='PASS' and reg['status']=='accepted' and not pages['unresolved_findings']
lp,kp=pages['page_totals']['learner'],pages['page_totals']['key'];total=lp+kp
contract,draft,blind,accepted=(c[k] for k in ['contract_checkpoint','complete_drafts_checkpoint','independent_solutions_checkpoint','accepted_text_checkpoint'])
exports=a.exports_checkpoint;after=reg['metrics']['after'];scope=reg['metrics']['unit15_status_counts']
counts={k:sum(d[k] for d in parity['documents']) for k in ['paragraph_heading_list_blocks','original_tables','original_table_cells_including_headers','all_editorial_comments_preserved']}
rows=[line for line in Path('STATUS.md').read_text(encoding='utf-8').splitlines() if re.match(r'^\| \[(?:[1-9]|1[0-4])\]\(typesetting/ch',line)]
assert len(rows)==14
course_table='\n'.join(['| Unit | Grammar | Learner / key pages | Complete exports/registers |','| --- | --- | --- | --- |']+rows+[f'| [15](typesetting/ch15/README.md) | Negation, quantity and comparison in discourse | {lp} / {kp} | {exports} |'])
write('STATUS.md',f'''# Status

Updated 27 October 2026. The eighteen-unit outline and complete Cook mapping are settled. **Units 1–15 are complete and independently reviewed**, with complete learner/key PDFs, every-page inspection and integrated teaching registers. Complete Unit 15 exports and registers are saved at **`{exports}`**. Unit 16 has not been drafted.

## Completed Unit 15

The [brief](curriculum/UNIT_15_BRIEF.md) and [contract](chapters/ch15/coverage.json) teach negative concord and contractions, indefinite and distributive reference, quantity, equality, preference and proportion in connected discourse. All **50 Cook IX.28–30 and joint X, XI.31 prompts** remain, with 55 original tasks and eight translated examples. **69 defined systems / 691 logical positions** appear in literal tables: 675 form/expression cells and 16 explicitly unassigned number slots. Complete tables retain their sense, syntax and reference limits.

Three exact readings total **415 words**: the 103-word opening argument of *Duties of the Rich toward the Poor* (printed 159.1–12 / PDF 175), the complete 152-word *Alfred’s Preface to Boethius* (162.1–17 / PDF 178), and the complete 160-word *A Prayer of King Alfred* (163.1–18 / PDF 179). Individual line numbers are editorial counts anchored by printed marginal numbers. All **27 original notes / 33 anchors**, 114 reading helps and 36 Cook help groups remain. The Duties outer speech continues on pp. 160–161 outside the assignment. No additional narrative is newly composed.

A fresh non-author froze [all solutions](chapters/ch15/independent-solutions.md) at **`{blind}`** before key/current-contract/audit access. The [review](chapters/ch15/review.md) and [ledger](chapters/ch15/review-ledger.json) reconcile all **105 tasks / 322 requested outputs**, including 116 form outputs and 64 anchored reading responses. A separate [fresh paradigm review](chapters/ch15/reviews/paradigms.json) verifies all 691 positions, their actual displays and primary evidence. No material finding remains open. Sealed analysis packets and blind solutions remain unchanged; canonical amendments preserve corrections separately.

The [learner PDF](typesetting/ch15/chapter-15.pdf) has **{lp} pages**; the [key](typesetting/ch15/answer-key.pdf) **{kp}**. All **{total} final pages** passed non-author visual inspection. [Full parity](typesetting/ch15/content-parity.json) covers {counts['paragraph_heading_list_blocks']} prose/heading/list blocks, {counts['original_tables']} tables and {counts['original_table_cells_including_headers']:,} table cells including headers. [Presentation acceptance](typesetting/ch15/page-review.json) binds final PDF/image identities and clean logs. Checkpoints: contract **`{contract}`**, drafts **`{draft}`**, accepted text **`{accepted}`**.

## Completed course artifacts

{course_table}

Each unit retains its contract, evidence, editable learner and separate key, frozen solutions, independent review, complete TeX/PDFs and page ledgers.

## Cumulative records and boundaries

The [lexicon](lexicon/entries.json) contains **{after['lemmas']:,} lemmas, {after['forms']:,} forms and {after['senses']:,} senses**; [grammar](curriculum/grammar.json) contains **{after['features']:,} constructions**. Unit 15 establishes {scope['forms']['new_production']} productive form milestones, {scope['forms']['new_recognition_only']} recognition-only forms, {scope['senses']['new_production']} productive senses and {scope['features']['new_production']} productive constructions. Supplied exposure remains separate from independent recall.

The [integration audit](chapters/ch15/register-integration.json) preserves earlier milestones, per-chapter records, evidence, supplied histories, surfaces, analyses and metadata against **`9129cda`**. All **2,311 fixed prior active artifacts** and **134 archived files** remain unchanged; the immutable baseline also includes both actual registers. Existing analyses remain intact, with contextual refinements recorded separately.

Negative concord expresses one denial. The selected negative indicative tables do not establish every subjunctive use. Full strengu is a recognition reference; hǣlu/hǣtu and people names retain explicit number/sense limits. The attracted dative in Cook 31.12 is a supplied construction, not a general rule for free-choice subjects. The confirmed **blōstmian** spelling corrects an earlier audit transcription, not Cook’s text.

The canonical crosswalk is **456 assigned / 188 deferred / none excluded**, totaling all 644 numbered items. Exercises **1–31** have full item-level audits; **32–48** still require them. Active contracts govern assignment and later assignments resolve prior deferrals without rewriting earlier contracts.

Continue only a requested unit. Read all fifteen active contracts and actual registers first; use the sole-coordinator Beads workflow and checkpoint the contract before prose. No remote or publication is configured.
''')
old=Path('docs/HANDOFF.md').read_text(encoding='utf-8')
rows=[line for line in old.splitlines() if re.match(r'^\| (?:[1-9]|1[0-4]) \|',line)]
assert len(rows)==14
rows=[line.replace('This handoff checkpoint','9129cda') for line in rows]
table='\n'.join(['| Unit | Contract before prose | Accepted text | Complete exports/registers | Final handoff | Learner/key pages |','| --- | --- | --- | --- | --- | --- |']+rows+[f'| 15 | {contract} | {accepted} | {exports} | This handoff checkpoint | {lp} / {kp} |'])
write('docs/HANDOFF.md',f'''# Handoff to the next session

The requested Unit 15 is complete. **Units 1–15** have independently reviewed learner/key masters, complete LuaLaTeX exports, every-page inspection and integrated registers. Complete Unit 15 exports and registers are saved at **`{exports}`**. The main [README](../README.md), [course/source map](../curriculum/COOK_MAP.md) and [typesetting index](../typesetting/README.md) include Unit 15. Unit 16 has not been drafted.

## Unit 15 evidence and review

The [contract](../chapters/ch15/coverage.json) preceded prose at **`{contract}`**; complete drafts were saved at **`{draft}`**. A fresh non-author froze all [pre-key solutions](../chapters/ch15/independent-solutions.md) at **`{blind}`**, under the [strict protocol](../sources/audits/unit15-coordinator/review-independence.json), before current key/contract/audit/proposal access. The [freeze record](../chapters/ch15/blind-freeze.json) verifies every actual requested output was attempted. The [review](../chapters/ch15/review.md), [ledger](../chapters/ch15/review-ledger.json) and separate [fresh paradigm review](../chapters/ch15/reviews/paradigms.json) accept all 105 tasks / 322 outputs and 69 systems / 691 positions. Accepted text is saved at **`{accepted}`**. No material finding remains open.

All 50 Cook IX.28–30 and joint X, XI.31 prompts remain, alongside 55 original tasks and eight translated examples. Preserve joint-group IDs EX-X-XI-31-NN. The exact readings total 415 words: Duties opening argument (159.1–12 / PDF 175), complete Alfred preface (162.1–17 / PDF 178) and complete prayer (163.1–18 / PDF 179). Editorial line counts are anchored by the printed marginal numbers. All 27 original notes / 33 anchors, 114 reading helps and 36 Cook help groups remain. The Duties speech continues outside the selection on pp. 160–161. Transcription, original apparatus and modern help are separate.

The 600 dpi exercise image confirms **blōstmian** with m; the n reading was an audit error, preserved in withdrawn source notes. It is not a Cook erratum. Canonical amendments and review ledgers record later corrections without altering sealed packets or the blind witness. Reading **gehīersumnesse** means obedience. Keep the printed **Lædene** distinct from the supplied long-vowel glossary form **Lǣdene**. Existing **wītga** and **bisceop** suffice where Cook gives unqualified English prompts.

The [learner PDF](../typesetting/ch15/chapter-15.pdf) has **{lp} pages**, the [key](../typesetting/ch15/answer-key.pdf) **{kp}**. All {total} final pages have non-author visual records bound to final PDF/image identities. [Presentation acceptance](../typesetting/ch15/page-review.json) reconciles every page, full parity and clean logs. See the [export README](../typesetting/ch15/README.md) for reproduction and layout records.

## Registers and preservation

The [integration record](../chapters/ch15/register-integration.json) preserves all prior teaching milestones, per-chapter records, evidence references, supplied histories, surfaces, analyses and metadata. Totals: **{after['lemmas']:,} lemmas, {after['forms']:,} forms, {after['senses']:,} senses and {after['features']:,} constructions**. Unit 15 adds {scope['forms']['new_production']} productive form milestones, {scope['forms']['new_recognition_only']} recognition-only forms, {scope['senses']['new_production']} productive senses and {scope['features']['new_production']} productive constructions. Supplied exposure is separate.

The immutable ignored `build/unit15-prior-baseline.json` captures the actual fourteen-unit state at **`9129cda`**: 830 lemmas, 9,710 forms, 1,017 senses and 820 features. The retained [prior-state record](../sources/audits/unit15-coordinator/prior-state.json) covers 2,313 earlier files including both registers, and 134 archived files. Do not overwrite the baseline or rerun old merge helpers against integrated registers. All 2,311 fixed prior artifacts and 134 archive files remain unchanged.

Complete morphology retains its stated senses and syntax. The 16 unassigned number slots are explicit pedagogical limits. Strengu supplies the full abstract-u reference class; hǣlu/hǣtu do not gain productive count plurals. Negative be includes five multiword constructions. Cook 31.12’s attracted dative remains supplied; original C06 uses internal nominative plus an explicit main-clause dative. Citations and supplied expressions do not establish independent productive recall.

The canonical crosswalk is **456 assigned / 188 deferred / none excluded**, totaling 644. Exercises **1–31** have full item-level audits; **32–48** still need them. Active contracts govern assignment.

## Recoverable checkpoints

{table}

## Resuming and reproducing

Read AGENTS.md, STATUS.md, EDITORIAL_POLICY.md, docs/WORKFLOW.md, the plan/map, source registry, all fifteen active contracts and actual registers. Run `bd prime`, then `bd ready`, serially; root remains the sole embedded-Dolt writer. Begin another unit only when requested.

Use parallel agents with exclusive files for independent source/curriculum analysis. Reconcile and checkpoint the contract before prose. Give a fresh blind solver only the actual learner master, accepted earlier learner teaching/registers and original primary images. Current contracts, audits and token maps may expose answers. Freeze every actual solution in Git before explicit comparison access. Resolve independent review, export complete PDFs and inspect every page before integration. Export Beads before local checkpoints; no remote push is configured.

Run `python -X utf8 scripts/check_unit15.py --draft --tex` after rebuilding ignored PDF text/log products as described in the export record. Retained TeX preserves final layout; rerunning assembly can discard repairs. Raw and normalized-LF hashes distinguish checkout conversion from text changes. Substantive contract identities permit later completion metadata. Do not rerun pre-prose or older merge helpers against integrated state.
''')
write('typesetting/ch15/README.md',f'''# Unit 15 exports

The complete [learner PDF](chapter-15.pdf) has **{lp} pages**; the [separate key](answer-key.pdf) has **{kp}**. Editable masters: [student.md](../../chapters/ch15/student.md) and [answer-key.md](../../chapters/ch15/answer-key.md). All 105 tasks, vocabulary, complete defined paradigms, three connected readings, support and original notes are included.

All **{total} final pages** passed non-author visual inspection. [Individual ledgers](reviews/) retain page-specific observations and final PDF/image identities. [Final acceptance](page-review.json) reconciles every page, complete parity, unchanged accepted masters and clean logs. [Layout adjustments](layout-adjustments.json) record the actual repairs and reinspection history. Byte-identical page reuse identifies the specific previously inspected image.

## Content and review

[Complete parity](content-parity.json) covers **{counts['paragraph_heading_list_blocks']} prose/heading/list blocks, {counts['original_tables']} tables, {counts['original_table_cells_including_headers']:,} cells including headers, and {counts['all_editorial_comments_preserved']} editorial comments**. An independent Markdown inventory matches decoded TeX; full prose matches extracted PDF text after whitespace and soft-hyphen normalization. Original note references retain D/P/R-prefixed numbers, with general source notes numbered separately. Every definition remains. Visual review includes actual tables, endings and special characters.

The learner gives 69 defined systems / 691 positions, comprising 675 form/expression cells and 16 explicitly unassigned slots. All 50 Cook IX.28–30 and joint X, XI.31 prompts retain wording and IDs, alongside 55 original tasks and eight examples. The three exact source readings total 415 words and retain 27 notes / 33 anchors, 114 reading helps and 36 Cook help groups. The continuation of Duties on pp. 160–161 remains unassigned.

The fresh [reviewer](../../chapters/ch15/review.md) froze [all solutions](../../chapters/ch15/independent-solutions.md) before key/current-contract/audit access. A separate [fresh paradigm reviewer](../../chapters/ch15/reviews/paradigms.json) checked every position and rule against primary evidence. Neither authored a master or task. Canonical amendments preserve corrections separately from sealed packets and the unchanged blind witness. No material finding is open.

## Rebuilding

Retained TeX preserves the reviewed layout. Use LuaLaTeX with Cambria and [book-layout.tex](../book-layout.tex): 165 × 241 mm trim, body 11/14.3 pt, tables 10.5/13.2 pt, source notes 10/12.8 pt. Both documents use `Ligatures=TeXOff`. Earlier exports and shared layout remain unchanged.

From this directory:

```powershell
New-Item -ItemType Directory -Force build
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-15.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build chapter-15.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build answer-key.tex
& 'C:/Program Files/Git/mingw64/bin/pdftotext.exe' -enc UTF-8 -layout build/chapter-15.pdf build/chapter-15.txt
& 'C:/Program Files/Git/mingw64/bin/pdftotext.exe' -enc UTF-8 -layout build/answer-key.pdf build/answer-key.txt
```

The checked toolchain is TeX Live 2026 LuaHBTeX 1.24.0, Xpdf pdftotext 4.00 and Ghostscript. This Windows installation needs access to the owner's font caches. Final logs contain no missing characters, overfull/underfull boxes, font substitutions or unresolved rerun warnings.

From the repository root, `python -X utf8 scripts/check_unit15.py --draft --tex` checks task/key references, exact prompts/readings, literal tables, model/dependency bindings, evidence identities and logs. It supplements linguistic and visual review. Render every page with Ghostscript `png16m`, `-r150 -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -dBATCH -dNOPAUSE`, supplying TeX Live's `Resource/Init`, `lib` and `kanji` through `-I`.

Build products and rendered page images are ignored unless explicitly retained; ledgers preserve inspected identities. Source evidence images remain tracked. One-use helpers are not required generators; reassembly can discard layout repairs. Rebuilt PDF metadata can differ, so replace retained PDFs only after full parity and page review.

Checkpoints: contract **`{contract}`**, drafts **`{draft}`**, blind solutions **`{blind}`**, accepted text **`{accepted}`**. Complete exports/registers: **`{exports}`**. The [handoff](../../docs/HANDOFF.md) records final closure.
''')
print('Wrote final status, handoff and export README from accepted Unit15 records.')
