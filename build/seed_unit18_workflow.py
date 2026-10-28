"""Coordinator-only serial Beads setup for the requested final planned unit."""
import subprocess

jobs = [
    ('source', 'Audit Unit 18 Cook prompts and connected readings',
     'Independently inspect all 47 joint XII, XIII Exercises 44-48 prompts on printed 29-33 / PDF37-41. Preserve exact English, hints, original IDs and instructions. Retain the sustained Joseph composition sequence and separately inspect candidate connected Old English prose from the selected Cook reader; do not infer an Old English Joseph source from the joint heading. Record exact boundaries, complete notes, actual images, words, forms, senses and constructions. Reconcile chosen spans with curriculum analysis before final source acceptance.',
     'Complete image-verified prompt and reading transcriptions, reversible normalization, notes and lexical/construction dependencies in sources/audits/unit18-source; no silent omissions or unverified spelling/length claims.', []),
    ('grammar', 'Audit Unit 18 complete forms and linguistic scope',
     'Independently inspect the assigned source prompts and all actual earlier contracts/registers. Establish every required lexical sense, form and construction; full bounded nominal/verbal systems, stems, exceptions and basic uses require primary evidence. Separate previously taught, new production, new recognition and supplied support. Own sources/audits/unit18-grammar and build/u18-grammar-* only.',
     'Evidence-bound paradigms, ordinary frames, complete cell routes and dependency proposals cover every assigned task and chosen reading without unresolved tested knowledge.', []),
    ('design', 'Design Unit 18 cumulative prose consolidation',
     'Read all seventeen active contracts and actual registers, inspect the final 47 Cook items and candidate connected prose, and design the final planned unit. Retain coherent complete Cook sets. Propose meaningful cumulative parsing, translation and controlled composition, explicit new teaching and local support; the capstone title confers no unrecorded mastery. Own curriculum/proposals/unit18 and build/u18-design-* only. Reconcile independent source and grammar evidence before final proposal.',
     'Complete proposal fixes pedagogical scope, reading boundaries, task/output plan, prior/new/supplied dependencies and full paradigm needs; every Cook item accounted for, without learner/key prose.', []),
    ('contract', 'Reconcile and checkpoint Unit 18 contract',
     'Coordinator reconciles independent source, grammar and curriculum audits into chapters/ch18/coverage.json. Resolve every assigned source item, form/sense/construction dependency, literal paradigm route and requested output before prose. Preserve all seventeen earlier contracts and register history.',
     'All 47 Cook prompts and chosen connected readings bound, no unresolved tested dependencies, complete bounded systems and tasks fixed; contract and exported Beads saved locally before learner/key prose.', ['source','grammar','design']),
    ('draft', 'Write Unit 18 learner text and separate key',
     'After the committed contract, assign exclusive learner and key files. Write concise rules, complete paradigms with stems and exceptions, ordinary uses, all exact Cook prompts, meaningful original tasks and connected supported readings with original notes. Prepare independent translations from actual Old English.',
     'Both complete masters match the committed contract and every actual output; key identifies target, essential meaning, defensible alternatives and diagnoses; supplied support remains visible without testing independent recall.', ['contract']),
    ('review', 'Independently solve and review Unit 18',
     'A fresh non-author solves every actual learner output before current key, contract, audits, proposals or answer-bearing witnesses. Freeze all unchanged attempts in Git before explicit comparison access. Review every task, answer and dependency; preserve original attempts and record repairs separately.',
     'All actual outputs independently attempted and frozen before comparison; complete key/source/dependency reconciliation; material findings resolved with final artifact identities.', ['draft']),
    ('paradigms', 'Independently verify Unit 18 forms and scope',
     'A separate fresh non-author verifies all full defined paradigms, literal displayed coordinates, stem rules, exceptions, senses and uses against primary images and actual prior teaching. Own review ledgers only.',
     'Every assigned logical cell and displayed route verified; evidence, valid variants and teaching limits explicit; all material findings resolved.', ['draft']),
    ('typeset', 'Export and inspect complete Unit 18 PDFs',
     'After independent linguistic acceptance, produce complete LuaLaTeX learner and separate-key exports. Check complete Markdown/TeX/PDF parity and clean logs. Give non-author visual reviewers exclusive page ledgers; inspect every actual page and recheck changed pages after repairs.',
     'Complete PDFs retain all tables, tasks, reading help and original notes; all final pages visually inspected with final identities, special characters and layout accepted; complete TeX/PDFs retained.', ['review','paradigms']),
    ('finish', 'Integrate Unit 18 and complete the planned course',
     'Integrate accepted teaching into the actual cumulative registers without changing earlier surfaces, analyses, metadata, evidence, histories or earliest milestones. Account for all 644 Cook items in active contracts. Update README, course/source indexes, registry, status/handoff and export documentation. Export Beads and save recoverable local Git revisions; no unrequested supplementary course work.',
     'Deep preservation audit passes against the immutable seventeen-unit baseline; all eighteen units indexed with complete exports and review records, final source crosswalk reconciled, Beads exported and local handoff saved.', ['typeset']),
]

def run(*args):
    result = subprocess.run([
        'C:/Program Files/PowerShell/7/pwsh.exe', '-NoLogo', '-NoProfile',
        '-File', 'C:/Users/Ross/AppData/Roaming/npm/bd.ps1', *args],
        text=True, encoding='utf-8', capture_output=True)
    print(result.stdout.strip(), flush=True)
    if result.returncode:
        print(result.stderr, flush=True)
        raise SystemExit(result.returncode)

for suffix, title, description, acceptance, dependencies in jobs:
    issue = 'oec-u18-' + suffix
    run('create', '--id', issue, '--type', 'task', '--priority', '2',
        '--title', title, '--description', description, '--acceptance', acceptance)
    run('dep', 'add', issue, 'oec-u18', '--type', 'parent-child')
    for dep in dependencies:
        run('dep', 'add', issue, 'oec-u18-' + dep)
print('Unit18 gates created serially. Only independent audit/design tasks are ready.', flush=True)
