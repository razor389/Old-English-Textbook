# Opening revision: bounded glossary refresh

The JSON beside this note supplies four complete candidate OE entry records, two append-only sense changes, exact display paragraphs, seven diagnostic provenance records, five new pronunciation routes, six dictionary-reference routes, seven curated English reference routes, and all 25 pronunciation task records bound to the actual final learner text. These are integration candidates, not a claim that the revised Unit 1 or its key has been audited. No key was opened.

## Dictionary additions

| Entry | Proposed display | Evidence and limit |
| --- | --- | --- |
| cealf | **cealf** (n.). calf. Only this cited form is supplied. | Fulk §135b, p.103/PDF115, ċealf; remove the overpoint. Gender and inflection remain unspecified. |
| dīc | **dīc** (n. m.); gen. sg. dīces; nom. pl. dīcas. ditch; dike. | Cook vocabulary p.283/PDF299 assigns §43; the masculine model is p.28/PDF44. Genitive is a checked rule formation. Fulk §135b explicitly prints the plural. |
| scield | **scield** (n. m.); gen. sg. scieldes; nom. pl. scieldas. shield. | Cook vocabulary p.311/PDF327 assigns §43. Both diagnostics apply the checked masculine model, retaining scield-. |
| scūfan | **scūfan** (v. strong); pret. 1 sg. scēaf; pret. pl. scufon; past ptcp. scofen. thrust. | Cook vocabulary p.311/PDF327 assigns class II §103. His p.60/PDF76 ū–ēa–u–o series and brūcan/brēac/brucon/brocen authorize the three individually labelled rule formations. They are not claimed as exact printed scūfan principal parts. |

Keep **węndan** as the headword and append the bounded display “Supplied preterite węnde: went.” Cook §4, p.6/PDF22, gives the exact contrast. Keep its existing senses and bounded diagnostic status. Add **direct** to the existing adjective **riht**, preserving “right; just”; Cook vocabulary p.309/PDF325 distinguishes the adjective from the neighbouring noun. **Sēcan** is already covered. The final learner note no longer prints the prefixed Fulk witness, which remains in revision evidence; no extra prefixed headword or silent prefix removal is needed.

No routine inflection receives a separate printed entry. The reference-form records use the existing dictionary schema and distinguish one exact diagnostic from six checked formations. Do not add an unverified ge- participle or a newly invented present-third-singular pointer. Noun shield and adjective direct must remain distinct from the existing English verb routes.

## Apply the data and Markdown deliberately

1. Check the proposal’s input hashes and record preconditions. Add the four OE records; append only the two new senses/override to the existing records. Preserve all old homographs, sense IDs, principal parts and selective cross-references. Store the new reference evidence in the versioned supplement; leave the frozen `dictionary-presentation.json` and its acceptance unchanged.
2. Insert the four supplied paragraphs under their `<!-- entry: OE-… -->` markers in the normal alphabetic positions. Append the bounded sense text to the two existing paragraphs. The historical `build/glossary-coordinator/assemble.py` lines269–318 document the current paragraph and ordering rules, but importing/running that file executes old one-use assembly. Reuse only its small `oesort`, `ensort`, `letter` and paragraph conventions in a bounded integration helper; do not regenerate all accepted prose from present registers.
3. The seven explicit English operations are recommended reference access, especially if all six new senses enter the cumulative register, because the existing checker expects register-sense access. They create five headings and append routes under existing shield/direct. Preserve those existing verb routes. These additions do not turn supplied pronunciation vocabulary into required English-to-OE production. The JSON provides deterministic existing-style EN IDs and exact route objects rather than mechanically splitting gloss strings.
4. Refresh current `form-lookup.json` occurrences and entries’ actual-form coverage. Bind the five new learner routes to the current learner lines. When the six new reference formations are printed, give them explicit dictionary-reference access/provenance; populate their actual glossary locations after insertion. Distinguish those reference occurrences from instructional occurrences. Never print exhaustive inflection lists merely because the lookup data are complete.

## Preserve history and measure current coverage

Use one versioned bridge, `docs/revisions/opening/glossary-supplement.json`, with compact current surface and exercise inventories. The bridge names the frozen original inventory, 38-master manifest, 137-file boundary and presentation recipe by hash. It records explicit authorized old→new identities and retains the old files as history. Do not overwrite the original snapshots or relabel old reviews as acceptance of new content.

Rebuild the current 38-master inventory after the pronunciation and Unit 1 keys have been independently checked; include the minimally changed Unit 2 learner identity. Reuse `WORD`, `key()` and `clean_line()` from `sources/audits/glossaries/old-english/audit.py`, plus its line/item/section and compact-row conventions. Its `main()` has fixed corpus paths, reads keys, and writes the old inventory; do not execute it against the historical outputs. A narrow current wrapper should write concordances only beneath ignored build storage and a compact versioned inventory beside the bridge. Preserve exact NFC/casefold matching, unresolved-token inspection and existing error/reconstruction dispositions. Keep all legitimate ambiguous routes.

For the unchanged sound-history appendix, check its existing additive `glossary-access.json` against its retained master and the current headwords. For dictionary principal parts, validate the union of old reviewed reference evidence and the new supplement. A reference form is not evidence of an earlier instructional occurrence. Compute final counts from the actual current corpus; the new total is not necessarily old count plus eleven.

The JSON supplies the 25 current pronunciation records, with exact prompt and group-context hashes, current line numbers, supplied forms and explicit sound-only exclusions. Their empty lexical requirement arrays now have a current reason, not merely a preserved old ID. Bind their final key correspondence after independent solving. Rebuild all affected Unit 1 records from the actual revised contract, learner and reviewed key: required input/output senses, supplied senses, each output position, idioms, synonyms and grammar routes. Retain unchanged task records only after their source identities are checked. All 1,417 task identities should still reconcile, including 92 Unit 1 items and the 25 pronunciation responses; stable IDs alone do not prove stable requirements.

`english/build_inventory.py` offers the existing contract-field logic and `spans()` extractor, but runs writes at module import. Copy/extract only the needed function and field logic into the bounded current wrapper. Its spans extend to the next marker and can include intervening headings; bind the actual prompt and shared task context deliberately. Do not count instruction words as translation vocabulary. The proposal does not mark revised Unit 1 complete.

## Narrow checker bridge and exports

The current `scripts/check_glossary_exports.py` has no revision option. Add an optional `--revision` input while keeping its historical default unchanged. In revision mode, substitute the named current surface/task inventories, merge additive diagnostic provenance without conflicting IDs, and verify exact approved file deltas while still hashing every other protected file. Preserve all checks for old diagnostics, sense access, dangling targets, selective pointers, complete entry identities and ordered Markdown/TeX/PDF content. Do not disable preservation or count checks wholesale.

Then use the existing renderer and compilation process:

```powershell
python -X utf8 scripts/build_glossary_exports.py
Push-Location typesetting/glossaries
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build old-english.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build old-english.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build english.tex
lualatex -interaction=nonstopmode -halt-on-error -output-directory=build english.tex
Pop-Location
```

After implementing the explicit revision option, run:

```powershell
python -X utf8 scripts/check_glossary_exports.py --build --revision docs/revisions/opening/glossary-supplement.json --report typesetting/glossaries/opening-2026-11-02-content-check.json
```

The renderer remains unchanged: it converts the deliberately edited full Markdown masters to complete TeX and content maps. The checker’s `master_blocks()`, `tex_plain()`, `normalized()` and complete PDF extraction already verify ordered full content, not samples. Retain that work. Independently review the linguistic additions and every changed exported page, then promote reviewed PDFs and refresh the full-book component identities and page/index mappings. Record new export/page receipts with the new hashes; keep historical receipts intact. Update both glossary READMEs with actual current counts, pages, commands and receipt links, and add a current-revision pointer to the glossary contract while preserving its original completion record. No additional glossary framework is needed.
