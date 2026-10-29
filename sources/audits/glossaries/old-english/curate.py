"""Rebuild the explicitly reviewed supplement to the exact register index.

The decisions below follow a review of all 6,871 initially unmatched token
types, including unformatted source notes. They do not change teaching scope.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OWN = Path(__file__).resolve().parent
OUT = ROOT / "build/glossary-oe"

# Surface groups are deliberately explicit. No accent stripping or automatic
# replacement of thorn/eth is authorized for arbitrary future tokens.
ALIASES = {
    "andswarian": "and-swarian andswerian",
    "bebeodan": "be-bēodan beboden",
    "bindan": "bundne bundnum",
    "brothor": "brōðru",
    "burg": "burge",
    "boc": "bōce",
    "cuman": "cumenne cyme",
    "cynn": "cyn",
    "cythan": "cȳdde cȳðst",
    "deorwurth": "deorwurðan",
    "dene": "dęnia dęniga",
    "dohtor": "dohtru",
    "dryhten": "dryhtenes",
    "feolan": "felgan filhþ",
    "feallan": "fielþ",
    "fisccynn": "fisc-cynn",
    "forceorfan": "for-ceorfan",
    "forweorthan": "for-weorðan",
    "forwiernan": "for-wiernan",
    "freond": "frēondas",
    "fugol": "fugolas morgenas",
    "faeder": "fædere fæderes",
    "fedan": "fēdeð fētt fédan",
    "feond": "fēondas",
    "fot": "fōtas fōte",
    "gefera": "ge-fēra",
    "geliefan": "ge-lýfan gelýfan",
    "gemanigfieldan": "ge-manig-fieldan",
    "geneosian": "ge-neósian",
    "geseon": "ge-sēon geseon",
    "geweald": "ge-weald",
    "geat": "geatum",
    "genealaecan": "genēalǣhte",
    "gescrydan": "gescrȳdd",
    "gewendan": "gewendan",
    "weorpan": "geworpen",
    "gan": "gán",
    "don": "dón",
    "godwebb": "gōd-wębb",
    "god-adjective": "gōdena",
    "hwilc": "hwelc hwylc hwilcera hwilcere",
    "hwaether": "hwæðere hwæðeres",
    "hyngran": "hyngrian",
    "halig": "hālgra",
    "here": "hęrgas hęrges hęrigas hęrigeas hęriges",
    "hulic": "hūlīc",
    "ic": "iċ mec ūser ūsic",
    "thu": "ðec ēowic",
    "he": "heora hira hire hiene",
    "libban": "lifie lifien",
    "lecgean": "lēde lēdon lęcgan",
    "laeden": "lǣden",
    "magan": "magan mehte",
    "mildheort": "mild-heort",
    "mildheortnes": "mild-heortnes",
    "motan": "mótan",
    "niht": "nieht nihte",
    "nawiht": "nōht",
    "ofslean": "ofslagen",
    "ongietan": "ongiet",
    "raedan": "rēd rēdon",
    "regn": "rēn",
    "rice": "rīcia rīciu",
    "scencan": "scencan",
    "sculan": "scolde scoldon",
    "sceththan": "scōd",
    "secgan": "secgan sāde sāden",
    "seolh": "seol",
    "wesan": "sint",
    "slean": "slægene",
    "smierwan": "smire",
    "stanweall": "stán-weall",
    "strengu": "strengo",
    "sunu": "sunas sunes",
    "swerian": "swerian",
    "swigian": "swīgiende",
    "synn": "syn",
    "toberstan": "tō-berstan",
    "totwaeman": "tō-twǣman",
    "todaelan": "tōdǣlan",
    "toth": "tōðas tōðe",
    "weorod": "werod",
    "witan": "wieton wioton wisse wissen",
    "willan": "wile",
    "waeter": "wætru",
    "se": "ðām",
    "thencan": "ðęncean",
    "thing": "þing",
    "thonne": "þonne",
    "thrie": "þrēo",
    "thurfan": "þurfan",
    "thyncan": "þyncan",
    "thusend": "þūsend",
    "agyldan": "ā-gildan",
    "afyllan": "āfyld",
    "ahebban": "āhebban",
    "astigan": "āstāh",
    "onweg": "āwęg",
    "eadig": "ēadges",
    "eage": "ēagna",
    "awiht": "ōht",
    "up-ahebban": "ūpāhebban",
    "scrydan": "scrýdan",
    "cirice": "cyrice",
    "theah": "ðēah-ðe",
    "thaet-conjunction": "ðæt-ðe",
    "swa": "swā-hwā swā-hwilc",
}
# Correct the intentionally separate noun stem; the two unsyncopated plurals
# share one printed sentence but never share a lemma.
ALIASES["fugol"] = "fugolas"
ALIASES["morgen"] = "morgenas"

NEW = [
    ("cīepa", "cīepa", "merchant", "noun", "Cook FB p.129, PDF145, note2; exact source word and English meaning visually rechecked in this audit."),
    ("cīepmann", "cīepmann cēapmann", "merchant", "noun", "Cook FB p.129, PDF145, note2; cēapmann is explicitly a collateral form. Source divides cēap-mann only at the line ending."),
    ("frēa", "frēan", "lord", "noun", "Cook FB §153.d, p.89/PDF105, in Frēan ęgesan. C02 corrects the analysis, not these words. Corpus form is genitive singular Frēan."),
    ("ęgesa", "ęgesan", "fear; terror", "noun", "Cook FB §153.d, p.89/PDF105, in Frēan ęgesan, in fear of the Lord. Corpus form is dative singular."),
    ("fēran", "fēran", "go; travel; journey", "verb", "ch16 answer-key, EX-III-34-03 discussion; named alternative travel verb, without a new conjugational assignment."),
    ("gelǣdan", "gelǣdst", "bring; lead", "verb", "Cook FB p.130 following the Merchant opening: Hwilc ðing gelǣdst ðū ūs? Quoted in ch08/student.md:1163 as the following excluded passage. Second-singular present."),
    ("gelǣran", "gelǣran", "teach; instruct; train", "verb", "ch16 answer-key distinguishes the verb from the assigned participial adjective gelǣred; no finite paradigm is assigned."),
    ("grēne", "grēne", "green", "adjective", "Cook grēne adjective model cited in ch07 and ch17; this headword names the declensional model."),
    ("grōwan", "grōwan grēowon", "grow", "verb", "Cook FB §109 p.67/PDF83 assigns flōwan pattern; glossary p.297/PDF313 and Exercises p.50/PDF58. Grēowon is the expressly documented by-pattern plural past in ch05 answer-key."),
    ("guma", "guma", "man", "noun", "Cook FB p.176/PDF192 note14, quotation of Beowulf653–655. Source spelling visually rechecked; nominative singular in quotation."),
    ("hǣl", "hǣl", "health; welfare; greeting", "noun", "Cook FB p.176/PDF192 note14: him hǣl ābēad, bade him hail/gave him greeting. Distinguish this complete word from the hǣl- stem of hǣlu elsewhere."),
    ("ābēodan", "ābēad", "offer; announce; bid (a greeting)", "verb", "Cook FB p.176/PDF192 note14: him hǣl ābēad; third-singular preterite. Source token visually rechecked; quotation means bade him hail."),
    ("munan", "munan", "remember; have in mind", "verb", "Cook FB §134, cited in ch13 answer-key as the mistaken section reference attached to a different verb. Conventional citation, not new recall."),
    ("mægð", "mægð", "maiden; girl", "noun", "ch17/student.md:893 explicitly contrasts short mægð, maiden, with long mǣgð, tribe/nation; source glossary distinction is carried in the checked chapter record."),
    ("nafogār", "nafogār", "auger", "noun", "Cook FB p.139/PDF155, note4, reproduced in ch11/student.md:2051; exact source comparison with modern auger."),
    ("nēosian", "nēosian", "visit; seek out", "verb", "ch10 source note distinguishes its genitive construction from the selected accusative construction of genēosian."),
    ("nǣnig", "nǣnig", "no; not any; none", "indefinite pronoun/adjective", "Reference family citation in ch08 and ch15; consult Cook indefinite-pronoun section, no additional recall assignment."),
    ("sīn", "sīn", "his own; her own; its own", "possessive", "Reference-only possessive cited in ch08 and ch15; not an additional assigned system."),
    ("āhwæðer", "āhwæðer", "either (of two); any", "indefinite pronoun", "Reference family cited in ch15; Cook indefinite-pronoun inventory, no new recall."),
    ("ǣghwæðer", "ǣghwæðer", "each of two; both; either", "indefinite pronoun", "Reference family cited in ch15; Cook indefinite-pronoun inventory, no new recall."),
    ("āhwā", "āhwā", "anyone", "indefinite pronoun", "Reference family cited in ch15; Cook indefinite-pronoun inventory, no new recall."),
    ("ǣghwā", "ǣghwā", "everyone; each", "indefinite pronoun", "Reference family cited in ch15; Cook indefinite-pronoun inventory, no new recall."),
    ("wilde", "wilde", "wild", "adjective", "Named Wright adjective model in ch17 source note; no additional adjective paradigm assignment."),
]

ERRORS = {
    "wǣstm": "C01: preserved erroneous source quantity. The corrected course headword is wæstm, with short æ; do not display wǣstm as a valid alternative.",
    "dægas": "Deliberate learner error; requested plural is dagas.",
    "hwælas": "Deliberate learner error; requested plural is hwalas.",
    "wastmas": "Deliberate learner error; requested plural is wæstmas.",
    "sǣwa": "Explicitly starred reconstructed genitive plural; never an attested unqualified lookup form.",
    "fōnende": "Rejected mechanical present participle; selected form is fōnde.",
    "unnað": "Rejected manufactured indicative plural; selected present plural is unnon.",
    "wīsrra": "Rejected unsimplified comparative genitive plural; selected form is wīsra.",
    "swētrra": "Rejected unsimplified comparative genitive plural; selected form is swētra.",
    "wundas": "Rejected masculine-pattern plural of the feminine wund in this context; selected plural is wunda.",
    "mynsteru": "Rejected unselected unsyncopated model answer; do not declare all historical uses impossible without evidence.",
    "fiscnað": "Rejected silent respelling of the source fiscnoð; not evidence for a second assigned fishing word.",
    "āgyltan": "Actual weak verb distinct from strong āgyldan; Cook's hint is wrong for reward. Preserve C06 and supply a correction cross-reference; do not gloss this as reward.",
}


def main():
    data = json.loads((OUT / "all-token-concordance.json").read_text(encoding="utf-8"))
    lexicon = json.loads((ROOT / "lexicon/entries.json").read_text(encoding="utf-8"))
    lemmas = {e["lemma_id"]: e for e in lexicon["lemmas"]}
    rows = []
    def context(surface):
        values = data.get(surface.casefold(), [])
        # Include the complete word location when the first hit is merely a stem.
        whole = [v for v in values if not set(v.get("flags", [])) & {"prefix", "suffix"}]
        return (whole or values)[:2]
    for lid, surfaces in ALIASES.items():
        if lid not in lemmas:
            raise ValueError("Unknown lemma ID: " + lid)
        for surface in surfaces.split():
            if not context(surface):
                continue
            refs = sorted({r for sense in lemmas[lid].get("senses", []) for r in sense.get("evidence_refs", [])})
            row = {"surface": surface, "classification": "old_english", "lemma_ids": [lid], "route": "explicitly reviewed corpus alternative or source citation", "corpus_contexts": context(surface), "existing_lemma_evidence_refs": refs, "teaching_scope": "lookup only; no new milestone"}
            if surface in {"swā-hwā", "swā-hwilc"}:
                row["route"] = "free-choice expression label; see swā + interrogative + swā"
                row["note"] = "Not a single inflected form of swā; the printed hyphenated label refers to the whoever/whichever free-choice construction."
            elif surface == "ðæt-ðe":
                row["note"] = "Source etymological phrase used to explain conjunction ðætte; not a new article inflection."
            elif surface == "ðēah-ðe":
                row["note"] = "Source spelling of the although-expression, represented with a space as ðēah ðe in the course."
            rows.append(row)
    supplemental = []
    for number, (headword, surfaces, gloss, pos, evidence) in enumerate(NEW, 1):
        lid = "GLOSS-OE-" + str(number).zfill(2)
        supplemental.append({"lemma_id": lid, "headword": headword, "gloss": gloss, "part_of_speech": pos, "evidence_route": evidence, "status": "supplemental lexical proposal; source spelling/context reviewed; new headword metadata requires coordinator reconciliation"})
        for surface in surfaces.split():
            rows.append({"surface": surface, "classification": "old_english", "lemma_ids": [lid], "route": "supplemental lexical entry", "corpus_contexts": context(surface), "teaching_scope": "lookup only; no new milestone"})
    guide = json.loads((ROOT / "guides/pronunciation/examples.json").read_text(encoding="utf-8"))["examples"]
    guide_only = {"āc", "eorl", "cyrice", "cēlan", "frosc", "ecg", "docga", "sengan", "cnīf", "cnīfas", "hǣlðu", "forðām"}
    guide_additions = [e for e in guide if e["form"] in guide_only]
    pronunciation_lemmas = []
    for number, (headword, forms, gloss, pos) in enumerate([
        ("āc", ["āc"], "oak", "noun"),
        ("eorl", ["eorl"], "man", "noun"),
        ("cēlan", ["cēlan"], "cool", "verb"),
        ("frosc", ["frosc"], "frog", "noun"),
        ("ecg", ["ecg"], "edge", "noun"),
        ("docga", ["docga"], "dog", "noun"),
        ("sengan", ["sengan"], "singe", "verb"),
        ("cnīf", ["cnīf", "cnīfas"], "knife", "noun"),
        ("hǣlðu", ["hǣlðu"], "health", "noun"),
        ("forðām", ["forðām"], "therefore", "adverb"),
    ], 1):
        lid = "GLOSS-PRON-" + str(number).zfill(2)
        evidence = [e for e in guide_additions if e["form"] in forms]
        pronunciation_lemmas.append({"lemma_id": lid, "headword": headword, "gloss": gloss, "part_of_speech": pos, "source_forms": forms, "evidence_file": "guides/pronunciation/examples.json", "example_evidence": evidence, "status": "exact source-backed pronunciation examples; glossary lookup only; no added morphology or gender claim"})
        for surface in forms:
            rows.append({"surface": surface, "classification": "old_english", "lemma_ids": [lid], "route": "pronunciation_example", "evidence_refs": ["guides/pronunciation/examples.json#" + surface], "corpus_contexts": context(surface), "teaching_scope": "supplied pronunciation vocabulary only"})
    for surface, note in ERRORS.items():
        rows.append({"surface": surface, "classification": "reconstructed_or_rejected_or_correction", "note": note, "corpus_contexts": context(surface)})
    # These look language-like but their contexts establish other languages,
    # author names, phonetic symbols, or ordinary English metalanguage.
    other = "cædunt cælitus cæsar encyclopædia horæ lætantium lætitiæ pilæ volcæ œdipus ælfric æn æthelwald ἤρξατο ut sonne til ringe".split()
    for surface in other:
        rows.append({"surface": surface, "classification": "other_language_or_English_name", "note": "Context inspected: not an Old English lexical occurrence.", "corpus_contexts": context(surface)})
    (OWN / "resolutions.json").write_text(json.dumps({"schema_version": 1, "status": "explicit corpus dispositions; supplemental headwords for coordinator reconciliation", "resolutions": rows, "supplemental_lemma_proposals": supplemental, "pronunciation_lemma_proposals": pronunciation_lemmas, "pronunciation_only_examples": guide_additions}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"alias_resolutions": sum(r["classification"] == "old_english" for r in rows), "supplemental_lemmas": len(supplemental), "pronunciation_lemmas": len(pronunciation_lemmas), "pronunciation_only_forms": len(guide_additions), "excluded_error_and_other_language_types": sum(r["classification"] != "old_english" for r in rows)}, indent=2))


if __name__ == "__main__":
    main()
