# Editorial work and Beads

Beads tracks actionable work, owners, dependencies, and handoffs. Source records and chapter contracts remain the authorities for evidence and pedagogical coverage. The seed uses the locally installed `bd 1.0.2` with embedded Dolt. It needs no background server. The installed release's bundled documentation specifies one writer for this mode.

## Session start

Run these from the repository root, sequentially:

```powershell
bd prime
bd ready
bd show oec-map
```

The final example is the initial source-map task; use an actually ready issue when resuming later. Read `STATUS.md` as well. Use explicit issue IDs in commands; avoid implicit last-touched-issue behavior in a shared workspace.

The initial queue has independent source mapping, sequence design, and opening-source audit tasks. Their reconciliation blocks the first coverage contract and draft. See `SEED_TASKS.md` for the seed-time index; query Beads for current status.

## Coordination and file ownership

The coordinator is the sole tracker writer and serializes all `bd` commands. Claim a task before doing it or delegating it:

```powershell
bd --actor coordinator update oec-map --claim
bd update oec-map --assignee source-editor
```

The claim sets the task in progress. Record the worker identity, exclusive files, expected deliverable, and any coordination notes on the issue. Workers receive their bounded assignment and send results back without independently changing Beads, shared registers, or another agent's files. A worker may inspect the source and the assigned learner materials, subject to reviewer independence.

Parallel work is appropriate for source checking and curriculum analysis. Authorship waits for the reconciled contract. Independent review waits for the draft and should solve before consulting the key. Typesetting follows linguistic review; final presentation review and register integration belong to the coordinator. These dependencies are seeded in the issue graph.

This single-writer arrangement supports parallel editorial agents without requiring concurrent database writes. If genuinely independent sessions later need to write the tracker concurrently, plan a supported server-mode migration from the installed release's documentation. Do not start another writer against the embedded database, copy its live files, or initialize a separate tracker per worker.

## Dependencies and completion

```powershell
bd dep add oec-contract oec-analyze
bd update oec-map --append-notes 'Completed source map in the assigned audit files; unresolved source limits recorded.'
bd close oec-map --reason 'Acceptance criteria satisfied; source inventory and locators checked.'
```

`bd dep add A B` means A is blocked by B. Use it when discovering a real prerequisite. Do not mark a task complete because a draft exists if its acceptance criteria remain unmet. Create a follow-up issue for new concrete work; record evidence and affected item IDs. Reopen or block review work when repairs are still needed. Editorial reviews require evidence, not agent agreement alone.

## Saving work

The live database is under `.beads/embeddeddolt/` and is excluded from Git. Dolt auto-commit is enabled for local history. Automatic JSONL export and auto-staging are disabled deliberately; the coordinator exports explicitly at checkpoints:

```powershell
bd export -o .beads/issues.jsonl
git diff --check
git status --short
```

Stage the intended editorial changes and `.beads/issues.jsonl`, then create a local Git commit. The JSONL export includes issue-level data and dependencies; it is not a full backup of Dolt history. Do not hand-edit it. The seed includes no remote, auto-push, external service integration, or Git hooks; explicit export is part of the handoff procedure.

On a future clone lacking the local database, preserve the tracked export and use `bd bootstrap --yes`, then verify `bd list` and `bd ready`. Do not use destructive reinitialization to repair an existing tracker. For full database-history backup use the installed `bd backup` workflow when needed.

Installed commands and storage behavior were checked against `bd --help`, `bd init --help`, `bd update --help`, `bd dep add --help`, `bd export --help`, `bd bootstrap --help`, and the release's bundled README/CHANGELOG. [Upstream project](https://github.com/gastownhall/beads). Recheck local help after upgrading; older SQLite-era and newer server instructions may differ.

In this installed release, `bd doctor` reports that embedded mode is unsupported and performs no integrity check. Do not interpret its zero exit code as a pass or follow its destructive reinitialization suggestion. Validate the issue export, dependencies, and `bd ready` output instead; the seed checks are recorded in `SEED_VALIDATION.md`.
