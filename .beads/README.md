# Project Beads tracker

This repository uses Beads 1.0.2 with its local embedded Dolt database. The coordinator serializes tracker commands and assigns exclusive files to parallel editorial agents. Start with `bd prime` and `bd ready`; follow [the project workflow](../docs/WORKFLOW.md), not generic instructions for unrelated storage versions or remote setups.

The live `.beads/embeddeddolt/` directory is ignored by Git. `issues.jsonl` is a deliberately tracked issue-level export. Export explicitly before local Git checkpoints with `bd export -o .beads/issues.jsonl`; automatic export/staging is disabled. Local Dolt auto-commit is enabled. There is no configured remote or automatic push.

On a future clone without the database, preserve the export and use `bd bootstrap --yes`, then verify the issue list and ready queue. This export recovers issue state, not complete database history. Do not hand-edit it or destructively reinitialize an existing tracker. See the installed `bd backup` help when full-history backup is needed.

The first-unit epic is `oec-pilot`. Initial independent work is `oec-map`, `oec-sequence`, and `oec-source`. [Seed task index](../docs/SEED_TASKS.md).
