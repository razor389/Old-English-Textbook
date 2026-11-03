# Opening glossary lookup integration

The coordinator-only helper is `build/opening/reconcile_glossary_lookups.py`, SHA-256 `0a3a3034ad1ae8e6bc7c1c9433e005634e51f00efa6a75d513c77cf49c2ea99f`. It imports only the guarded current inventory wrapper. Importing it or running either stage without `--apply` writes nothing. No historical builder is called.

The helper is pinned to the approved [surface proposal](current-glossary-dispositions.json), SHA-256 `1af28400f4cca5ad6ed2846f643232a740fdb0a65aa0b2c7efe538baa7d98484`. It does not invent authorizations, accept reviews, add senses or revise teaching milestones.

## Coordinator sequence

First finish the Unit 2 metadata/orientation update and the exact authorized deltas, register aliases and accepted task-review bindings in `docs/revisions/opening/glossary-supplement.json`. Preparation permits the explicitly planned Unit 2 learner change only when that exact new master hash is authorized; the other 37 master identities remain pinned to the proposal.

Run the preparation dry run, inspect its plan, then apply it:

```powershell
python -B -X utf8 build/opening/reconcile_glossary_lookups.py prepare
python -B -X utf8 build/opening/reconcile_glossary_lookups.py prepare --apply
python -B -X utf8 scripts/refresh_opening_glossary_inventory.py --revision docs/revisions/opening/glossary-supplement.json
```

Preparation appends only **dēore** to **OE-deor** and **græs** to **OE-gaers**, adds their two initial lookup rows, and merges the 57 approved surface dispositions into the bridge. It verifies the two compact entry preconditions and the inspected source-image identities. Existing dispositions must agree; no exclusion may hide a known lexical route. All other entry fields, English entries, cross-references, bridge baselines, authorizations and review records are preserved.

If the updated Unit 2 orientation introduces further unknown English wording, inspect and disposition those exact contexts centrally, then regenerate the current inventories. The helper preserves additional coordinator dispositions; it does not infer new exclusions.

Once the wrapper reports a fully passed current inventory, refresh both lookup tables:

```powershell
python -B -X utf8 build/opening/reconcile_glossary_lookups.py refresh
python -B -X utf8 build/opening/reconcile_glossary_lookups.py refresh --apply
python -B -X utf8 scripts/refresh_opening_glossary_inventory.py --revision docs/revisions/opening/glossary-supplement.json
python -B -X utf8 build/opening/reconcile_glossary_lookups.py verify
python -B -X utf8 scripts/check_glossary_exports.py --build --revision docs/revisions/opening/glossary-supplement.json --report typesetting/glossaries/opening-2026-11-02-content-check.json
```

Refresh calls `validate_retained()` first and refuses unresolved, stale or differently authorized inventories. It refreshes the exact surface set and first locations, preserves every existing homograph target, and requires the same **1,417 task IDs**. Exercise rows receive current sense/feature requirements, English routes, contract-record identities and actual learner/key block identities. Pronunciation remains sound-only. Old recovered-sense annotations and requirements remain recoverable from the immutable baseline copy instead of being presented as current requirements.

## Baseline history and repeatability

The first applied change saves each original lookup **byte for byte**, before replacing the active file, under:

- `docs/revisions/opening/lookup-history/form-lookup-1a1f1de42b3b260ee0ab6117f29afb82bc9e6eb12baae8aa1d144d49a0414ab8.json`
- `docs/revisions/opening/lookup-history/exercise-lookup-f06b35a599c8cde9ca57526346738f6dc88d31e7cc62097d0a4318ca32fd2ee8.json`

The original hashes are pinned. Existing archives must match exactly. Each active lookup records its archive and approved proposal identity. The frozen original corpus, surface/task inventories and earlier review receipts are never overwritten.

Lookup metadata binds the stable semantic projection and all other actual source hashes, excluding the lookup files themselves. This avoids a circular whole-file hash dependency because form-lookup is also an inventory input. The second inventory run recalculates its complete input identities; `verify` recomputes retained inventories and requires that another refresh would write nothing.

Every input is checked again immediately before an applied plan. Original lookup archives are written first, and replacement is atomic per file. Unrelated entry edits, conflicting dispositions, lost homograph routes, vanished prior surfaces, changed task IDs or missing review/boundary bindings stop execution. There is no force or waive-errors option.

## Checks performed

The real preparation dry run passed. Read-only in-memory checks confirmed that only the two approved entry-form arrays change, all bridge review/authorization/baseline fields remain intact, and repeated preparation is a no-op. An unrelated change to **OE-deor** was rejected.

An explicitly synthetic passed-state fixture exercised all **5,587 current surface rows** and **1,417 task rows**, preserved every old route, and reached a no-op after the simulated second inventory hash update. This fixture tests refresh shape and hash-cycle behavior; it does not accept the still-pending real inventories.

The actual refresh dry run correctly refused the pending authorizations. All four shared-file hashes remained unchanged throughout testing, and no lookup-history directory was created. The helper passes syntax and UTF-8/LF checks. Its `--apply` paths have not been run by this worker.
