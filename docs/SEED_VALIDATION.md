# Seed validation

22 October 2026. The seed was independently reviewed for policy/template consistency, handoff completeness, meaningful links, archive boundaries, and accidental inherited teaching milestones. The coordinator reconciled the two navigation/wording findings before initialization.

- All 132 archived files match the previous repository's committed blobs at `7dd99f938d4969147fe3d996c42a344d9fc4cb90`. Provenance hashes are recorded, and Git attributes preserve their exact bytes. Archived AGENTS.md is renamed so it cannot apply as active instructions.
- Both active teaching registers are empty. All 33 inherited original source records are unassigned in the new course.
- All active Markdown links and UTF-8/NFC text pass checks. The archive wrapper supplies working PDF links where historical review links used omitted build directories.
- All three ignored PDF caches match the registry hashes. Selected page images and historical deliverables are retained in the snapshot.
- Beads 1.0.2 uses the new repository's own embedded `oec` database, with no redirect or worktree. The repository-local role is maintainer.
- The 12 seeded issues have the specified descriptions, acceptance criteria, owners' file scopes, parent links, and prerequisite links. The dependency graph is acyclic. The actionable task queue is source mapping, sequence design, and opening source audit; the parent epic is also shown by `bd ready`.
- `bd doctor` is unsupported in this release's embedded mode; it did not perform a check. The export and dependency graph were validated directly and compared with the actual ready queue.

No new learner chapter or PDF has been drafted or reviewed. The new layout carries forward an inspected baseline; each future unit requires fresh content and rendered-page review. The seed is a preparation and handoff, not a completed course.
