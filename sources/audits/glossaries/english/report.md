# English lookup audit

The inventory covers **1,392 assigned chapter tasks: 644 Cook items and 748 original tasks**, plus all **25 pronunciation responses**. Every chapter task has a resolved current learner location, accepted key location and contract. All 1,681 referenced lexical senses resolve in the cumulative register. No Cook item or original task has been omitted from the crosswalk.

## Deliverables

- `exercise-inventory.json`: one record per task, with the exact contract prompt, task kind, required senses, output-position records where present, local support, source controls and source/learner/key references. The contract remains the authority for assignment; this inventory adds no teaching milestone.
- `sense-use-crosswalk.json`: one record per exercise-linked sense, retaining the original semantic label, headword, lexical identity, evidence references and all task uses. `old_english_output_task_ids` distinguishes the broad OE-producing task scope; it is not a claim that every linked word is independently tested. In particular, supplied and reading-analysis dependencies remain visible.
- `lookup-additions.json`: **225 curated access entries and 485 English lookup labels**, with sense-specific choices, case/usage notes and exact task provenance. These cover actual English prompt synonyms, multiword expressions and grammar routes that a bare reversal of register glosses misses. They supplement the complete lexical index; they are not a list of complete exercise answers.
- `inventory-summary.json`: counts, input file hashes and unresolved-reference checks.
- `build_inventory.py` and `build_lookup_additions.py`: reproduce these narrow repeated crosswalk checks. Working prompt/sense lists are written only under ignored `build/glossary-en/`; no register snapshot is written.

## Scope and interpretation

All 48 Cook sets were reviewed from their actual English prompts. Original English composition and output prompts were also checked, including the multi-answer groups in Units 16–18. Accepted key explanations were consulted for semantic and government contrasts, especially where the English surface fails to predict the Old English construction. Existing source evidence is reused; this audit does not claim a new inspection of all source page images.

English used only to give an instruction—such as *identify*, *parse*, *give the genitive*, *singular* and *preterite*—is not translation vocabulary. English prose explaining a key is likewise not an exercise translation target. The pronunciation guide asks sound questions with all Old English words/meanings supplied; its 25 responses establish no additional English-to-Old-English production requirement.

The crosswalk contains 1,681 senses from 1,263 lemmas because reading translation and reading-analysis tasks also belong to the exercise inventory. Of these senses, 1,176 occur in the broad OE-producing task classification. Do not use that smaller figure to discard reading-related lookup support: the requested complete exercise aid benefits from the full inventory, while preserving supplied scope. Nor should the presence of a sense ID be treated as proof that the learner can find it under the English word actually printed in a task.

## Findings that affect the glossary

Actual prompt wording needs explicit access under, among others, **increase → weaxan**, **subside → geswīcan**, **lad → cnapa**, **knowledge → andgiet**, **provender → fōdor**, **spices → wyrt**, **country → ēðel**, **years of age → winter**, **rule → rīce**, **woo → giernan**, and **hear/listen to → hlystan**. The additions give item IDs and frames, so these contextual routes do not become unrestricted new senses.

Some current register gloss fields are dependency prose rather than usable lexical definitions. In particular, `asmean-u17-source-sense`, `geriman-u17-source-sense`, `befeallan-u17-source-sense`, and `hearpian-u17-source-sense` cannot be reversed verbatim. The accepted learner/key supplies **āsmēan**, **gerīman**, the love-as-subject idiom, and the supplied harping construction. Their access entries retain these limits and identify the actual prompt.

The guide must distinguish **do** as a modern English auxiliary from lexical/substitute **dōn**; future **will/shall** from volitional **willan** and obligatory **sculan**; perfect/progressive English from a mechanically copied auxiliary; and wish **let/may** from permission. Bare noun phrases can translate **a/an**. Presentational **there** and impersonal **it** may be omitted, supplied or realized differently according to the exercise. These are grammar routes, not forced word equivalences.

Case frames are essential for such entries as **rule over**, **cease from**, **deny**, **grant**, **hear/listen to**, **help**, **obey**, **woo**, **fear**, **receive**, **have compassion on**, and **provide for oneself**. The two selected *receive* frames and the two *fear* frames must remain distinct. Likewise, English *of*, *to* and *for* often correspond to governed cases or whole constructions rather than the homonymous Old English preposition.

The source corrections remain active: **C01 wæstm** has short æ despite the retained Cook hint; **C06 āgyldan**, strong III, replaces Cook's erroneous weak `āgyltan` hint in `EX-XII-XIII-34-09`. The additions do not alter source prompts or their omission controls.

## Outstanding integration and review

There are **no unresolved task IDs, missing current learner/key anchors or missing required sense IDs** in this handoff. This establishes a complete audit crosswalk, not completed glossary publication. The coordinator still needs to reconcile these routes with the OE entry inventory, create the learner glossary and review the actual English index. The access entries deliberately retain some linked sense choices under one explanatory entry; a renderer must preserve that usage note rather than flattening all aliases into unqualified synonym equivalence.
