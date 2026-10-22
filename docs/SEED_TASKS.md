# Seeded Beads tasks

This is a seed-time index, not a second live task tracker. Run `bd ready`, `bd show <id>`, and `bd list` for current state. The original task specification is preserved in `seed-tasks.json`.

| ID | Task | Role | Blocked by at seed time |
|---|---|---|---|
| oec-seed | Seed the fresh grammar-led course repository | coordinator | Closed during seeding |
| oec-pilot | Establish the new course and complete its first grammar unit | coordinator | None |
| oec-map | Inventory Cook exercises for a grammar-led course map | source-editor | None |
| oec-sequence | Refine the full-paradigm course sequence | curriculum-analyst | None |
| oec-source | Audit remaining opening-unit source and reading material | source-editor | None |
| oec-reconcile | Reconcile the course outline and Cook-to-unit mapping | coordinator | oec-map, oec-sequence |
| oec-analyze | Audit the first unit's full paradigms and learning dependencies | curriculum-linguistic-analyst | oec-reconcile, oec-source |
| oec-contract | Record the reconciled first-unit learning contract | coordinator | oec-analyze |
| oec-draft | Write the complete first unit and separate explanatory key | lesson-author | oec-contract |
| oec-review | Independently solve and review the first unit | independent-reviewer | oec-draft |
| oec-typeset | Typeset complete first-unit learner and key PDFs | typesetter | oec-review |
| oec-finish | Complete presentation review and merge first-unit records | coordinator | oec-typeset |

The first actionable work is `oec-map`, `oec-sequence`, and `oec-source`. Each has exclusive output paths in its issue. The coordinator serializes Beads mutations and integrates shared files. Drafting is blocked until source/curriculum reconciliation and the first learning contract.
