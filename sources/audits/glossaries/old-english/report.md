# Old English corpus glossary audit

Audit date: 29 October 2026. Coordinator issue: `oec-gloss-oe`. No chapter master, coverage contract, cumulative register, source index, Beads record, or Git state was changed by this worker.

## Scope and result

The corpus comprises the student and answer-key masters of Units 1–18 and the pronunciation guide: **38 files**. The audit includes paradigms, vocabulary, readings, original exercises, answer models, alternatives, prose explanations, help, source notes, and source quotations embedded in notes. All 18 active contracts remain the teaching authorities; a glossary lookup adds no learning milestone.

The corpus has **298,775 raw word occurrences** and **12,279 distinct NFC/casefolded token types**. After reconciliation, **5,580 token types have an explicit lexical lookup route**, and **6,699 have an explicit nonlexical or exceptional disposition**. There are **zero unclassified surface types** in this snapshot. These are audit counts, not claims about the number of Old English running words: English homographs and occurrences of a word as a morphological stem also appear in the concordance.

The 6,699 dispositions consist of 6,668 reviewed ordinary exclusions and 31 specifically documented exceptions. The ordinary exclusions contain 357 fragments, letters, endings, or mixed-language labels and 6,311 English words, other-language words, names, or metadata tokens. The 31 exceptions distinguish correction/rejected/reconstructed examples and conspicuous non-OE spellings. A new token introduced by a later edit will remain unresolved until reviewed; the whitelist is not regenerated automatically by the coverage check.

## Deliverables and rerun

- `inventory.json`: compact per-surface lookup inventory, file hashes, counts, and the first source location. Its column schema is embedded in the file.
- `resolutions.json`: **188 explicit lexical surface resolutions**, **23 supplemental lemma proposals**, **10 pronunciation lemma proposals** with exact IDs, the **12 pronunciation forms absent from the original register lookup**, and explicit error/correction/other-language decisions. Each proposed addition gives its exact corpus surface, concise meaning, part of speech, and reused source route. Unchecked extra gender or conjugation metadata is not invented.
- `reviewed-exclusions.json`: the fixed list resulting from manual review of the complete initially unmatched token vocabulary, including unformatted text. This is distinct from the list of rejected linguistic examples.
- `audit.py`: regenerates coverage from the current masters and registers. Run `python -X utf8 sources/audits/glossaries/old-english/audit.py` from the repository root. An unresolved count above zero requires inspection.
- `curate.py`: rebuilds the explicit resolution records from reviewed decisions and validates all existing lemma IDs. Run it before `audit.py` only when updating those decisions.

The complete location-and-context concordance, detailed evidence routes, and intermediate candidate lists are reproducible under `build/glossary-oe/`; they are deliberately not duplicated in the tracked inventory. The full concordance permits inspection of every occurrence, not only each first location.

## Extraction and reconciliation

The extractor reads every non-comment text line. It retains line numbers, item IDs where present, exact spelling, and context; table cells and unformatted source notes are included. It tokenizes letters with internal hyphens, preserves quantity and hooked letters, and matches only NFC plus case folding. It does not silently substitute thorn/eth, remove length marks, or normalize every dictionary hyphen.

The register has 1,265 lemma records. Headwords, source spellings, and milestone `forms` alone are insufficient. Explicit `variants`, `accepted_variants`, `valid_alternatives`, and `principal_parts` supply further supported lookups. Parenthesized optional letters, such as `(ge)hæfd`, require both documented expansions. Alternatives are indexed without converting them into independent-recall milestones.

All initially unmatched token types were reviewed in sorted order, including tokens outside bold text, italics, and tables. Candidate OE spellings were then inspected in their actual contexts. Ordinary English, Latin, Greek, modern-language quotations, phonetic symbols, inflectional fragments, and mixed English/OE labels were separated from words requiring lookup. English/OE homographs are not assigned a language by spelling alone: the index gives lexical lookup candidates, and the full concordance preserves the contexts.

## Material additions and distinctions

Source notes contribute real vocabulary. Cook p.129/PDF145 note2 supplies **cīepa, cīepmann, cēapmann**, “merchant”. Cook p.176/PDF192 note14 quotes *Beowulf* 653–655 and requires **werod, guma, hǣl, ābēad**. The p.129 and p.176 images were personally inspected for this audit; the compound division in cēap-mann is a printed line break. Other additions include **nafogār**, “auger”, **mægð**, “maiden”, named adjective models **grēne** and **wilde**, and reference-only indefinite/possessive words. The supplemental records identify source routes for coordinator reconciliation of entry metadata; they are not new teaching assignments.

The pronunciation discrepancy is resolved explicitly. The original register lookup lacks **āc, eorl, cyrice, cēlan, frosc, ecg, docga, sengan, cnīf, cnīfas, hǣlðu, forðām**. Their exact forms and meanings are supported by `guides/pronunciation/examples.json`. **Cyrice** can cross-reference existing **cirice** with the guide's spelling evidence; **cnīfas** belongs with **cnīf**. The guide's **forðām**, “therefore”, must not simply inherit the register conjunction **for-ðām**, “because”. **Hǣlðu**, “health”, likewise needs its supplied sense retained. Unused examples in the guide's evidence pool, such as **hliehhan**, do not create a corpus requirement.

Do not put **dægas, hwælas, wastmas, fōnende, unnað, wīsrra, swētrra**, or reconstructed **sǣwa** into an ordinary list of attested forms. The exact source strings remain searchable as rejected/reconstructed notices. **Wǣstm** is preserved in the register's source spellings but is explicitly erroneous under C01: route it to a correction notice for **wæstm**. **Wundas, mynsteru**, and **fiscnað** have specifically rejected or unselected roles in their present contexts; the audit does not assert their universal historical impossibility. **Āgyltan** is a real weak verb but is erroneous as Cook's hint for “reward”; preserve C06, distinguish its valid lexical sense, and cross-reference **āgyldan** for the intended reward meaning.

The glossary still requires ordinary editorial reconciliation of the supplemental entry metadata and its generated presentation. This audit certifies explicit corpus dispositions, not independent re-verification of every historical form already accepted in the eighteen source-checked contracts.
