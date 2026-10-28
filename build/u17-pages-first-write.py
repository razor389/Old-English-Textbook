from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
ROOT = Path(__file__).resolve().parents[1]
payload = json.loads(r'''{
  "observations": {
    "1": "The two-line chapter title and opening section fit inside the text block. Introductory paragraphs, the section-1 heading and its complete explanation are intact; header and folio are clear.",
    "2": "The four bold Old English examples, translations and explanatory paragraphs are legible. Macrons, æ and ð render distinctly; A01 and its three prompts remain together. A supplemental lossless detail view confirms a visible space between Does and wǣre in question 3.",
    "3": "A02, A03 and A04 each retain their complete prompt and three tasks. Old English æ/ð and macrons in the conditional examples are clear; section 2 starts with a full paragraph and stays above the footer.",
    "4": "The strong-masculine rule connects directly to hyll. Hyll, cēderbēam and horn each retain their descriptor plus all four singular/plural rows; headers align and macrons are intact.",
    "5": "The lof singular scope note remains with its table; olfend and ðegn retain complete singular/plural tables. All rows, horizontal rules and the lower ðegn cells fit without clipping; ð is clear.",
    "6": "Wīsdōm shows both macrons cleanly in text and cells, and its singular-only table is intact. Grundweall and cniht each have complete aligned four-case paradigms with attached explanatory prose.",
    "7": "Ymbhwyrft, gylt and gyltend descriptors remain immediately above complete tables. The longer agent-noun rule fits with gyltend; no orphan heading, clipped ending, or footer collision appears.",
    "8": "Finger's stem-change rule and full table, hearpere's complete paradigm, and weorðscipe's singular table fit on the page. Eth is clear. A supplemental lossless detail view confirms that every hearpere singular cell, including the accusative, aligns correctly.",
    "9": "Fox, ðorn and cynehelm each have four-case singular/plural tables with intact rules and aligned headings. The ðorn eth characters remain distinct, and the page has generous lower margin.",
    "10": "Gerīmcræft's æ and macrons are clear in its singular table. Stān retains all eight cells, with the dative singular stāne correctly aligned as confirmed in a lossless detail view. The strong-neuter heading stays with its complete introductory rule before the next page.",
    "11": "Mægen's exceptional plural and full-stem explanation stay with its complete table; æ is clear throughout. Andgiet's singular scope paragraph and table are intact, followed by the complete pund paradigm.",
    "12": "Edlēan, ðrymsetl and palmtwīg each retain their explanatory stems and complete four-case tables. Eth and the ē/ī length marks render cleanly; long forms do not touch the next column.",
    "13": "Cnēo's ē and the -w- stem are visible throughout its table and descriptor. Hol and nest each keep the light/heavy-stem explanation with all singular/plural cells; no clipping or detached heading appears.",
    "14": "Hrēod's complete table and long ē are clear. The strong-feminine overview is followed by hēanes with its reference-only singular explanation and both four-case columns on the same page.",
    "15": "Ȳst, cwēn and ðēnung tables are complete and their exceptional-form or suffix notes stay attached. ȳ, ē and ð render clearly, and long descriptive lines remain within the text block.",
    "16": "Getimbrung, ēaðmōdnes and ðīnen retain complete table/descriptor groups. The double-consonant notes and ē/ō/ī/ð characters remain legible; all column headings and footer are unobstructed.",
    "17": "Cnēoris and mǣgð full tables and blētsung's singular table are intact. The visible long-ǣ/short-æ distinction is maintained in the mǣgð explanation; no special-character collision or table overflow appears.",
    "18": "Beorhtnes and ðancung each retain their singular-scope explanation and full four-case table. The weak-noun heading stays with its complete overview; the page ends at a paragraph boundary above the folio.",
    "19": "Draca, nædre and dēma keep complete singular/plural paradigms with attached stem rules. The æ in nædre and ē in dēma are clear; the spelling-variant explanation wraps without clipping.",
    "20": "Hālga, hlīsa and ðēowa descriptors and full tables fit together. Macrons and eth are intact; the weak/strong servant distinction remains directly above ðēowa's table.",
    "21": "Ēare's contraction rule, tabele's retained-vowel rule and hearpe's stem rule each connect to a complete paradigm. All singular/plural column headings and bottom rules are clean; ē remains distinct.",
    "22": "Blōstma, biema and hlǣfdige each retain complete tables and stem notes, including the explicit biema spelling limit. Strong/weak adjective heading starts with a full introductory paragraph and stays above the page number.",
    "23": "The adjective-column and recognition-scope explanation is intact. Wæstmbǣre's descriptor and both strong singular/plural matrices stay together; ǣ and æ are distinguishable, all gender headings fit, and dashes are clear.",
    "24": "The wæstmbǣre continuation is explicitly labelled Weak and gives both complete matrices. Geong then starts with its own descriptor and both strong matrices. Multi-line headers, inapplicable dashes and table rules are aligned and unclipped.",
    "25": "Geong's labelled weak continuation has both complete matrices. Manigfeald begins with its descriptor and both strong matrices; long inflected forms fit their columns, with all instrumental dashes and table rules visible.",
    "26": "Manigfeald's weak matrices are complete at the top. Rīce's stem/ending explanation stays with both strong matrices, and the ī macrons and gender labels are legible; bottom rule clears the folio.",
    "27": "Rīce's weak continuation remains coherent above the new dæghwāmlīc entry. Both strong matrices for the latter fit without clipping, and æ, ā and ī remain distinct across the longer forms.",
    "28": "Dæghwāmlīc's weak tables retain readable long forms in all gender columns. Hlūd begins with its heavy-stem rule and both strong matrices; ū and instrumental dashes are clear.",
    "29": "Hlūd's complete weak continuation and æðele's descriptor plus both strong matrices fit within the page. The æ/ð characters remain intact in every visible form; the last table clears the footer.",
    "30": "Æðele's weak matrices finish cleanly. Æðelboren starts with its retained-stem instruction and both complete strong matrices; long forms remain separated by columns, and the lower instrumental row is unclipped.",
    "31": "Æðelboren's weak matrices finish intact. The adjectives-naming-people paragraph and new verb-system overview are readable, including ð, ǣ and the hooked e in dictionary references. The final verb-formation paragraph continues normally on page 32.",
    "32": "The continued overview leads into hęrian. Its descriptor, full indicative table, imperative pair and present-subjunctive table all remain on one page; hooked e, ð and every person/number label are legible.",
    "33": "Gecweðan's complete indicative display and ūpāhębban's indicative plus participle pair fit with their explanations. Æ/ǣ, ð, hooked e and ū/ā/ō render clearly, and every table row is inside its rules.",
    "34": "Oferwyrcean and gesęttan each retain the formation/government explanation and complete indicative table. Eth and hooked e are clear; tables have balanced spacing, aligned tense headings and complete bottom rows.",
    "35": "Giernan and mǣrsian indicative entries are complete and legible. Material layout finding: the separate mǣrsian participle heading and formation paragraph sit at the page bottom, while its scope paragraph and two-form table are on page 36.",
    "36": "The mǣrsian participle scope paragraph and table begin without the entry heading/formation rule, which are on page 35 (same material finding). Gewilnian and ðurhwunian have complete attached indicative entries; ǣ and ð are clear.",
    "37": "Wiðstandan and gearcian each have complete indicative tables directly below the governing/formation rules. Hooked e, ð and ō are clear, and the six person/number rows remain aligned.",
    "38": "Āfyllan's indicative and participle pair stay with its descriptor; āweorpan follows with its complete indicative display. Ā/ð and every singular/plural label are distinct; neither table is clipped.",
    "39": "Āwrītan and ālūtan each keep all six present/preterite rows with the stem-alternation rules. The ī, ā, ē, ū and ȳ marks remain readable and aligned; substantial lower margin is clean.",
    "40": "Windan, spǣtan and tǣlan retain complete indicative tables and attached rules. Ǣ and ð render distinctly; the final tǣlan table fits above the folio without clipped rows or rules.",
    "41": "Bīegan and gemunan each retain their full descriptive paragraph and six-row indicative table. Bīegan's length mark and ð are intact, with clear tense headings and uncrowded lower margin.",
    "42": "Ðęncean's indicative table is complete and hooked e/ð/ō remain legible. Blētsian and ofwundrian each keep heading, sense, formation/scope paragraphs and two-form participle table together; bottom rule clears the footer.",
    "43": "Wyrcean, gesweotolian and ācęnnan each retain all formation/scope prose and their two-form participle table. Ā and hooked e are clear; long gesweotolian forms fit without touching rules or margins.",
    "44": "Geopenian's participle pair, cnucian's command pair and āhębban's command pair remain with their rules. Ā, hooked e and ð render distinctly; each table has its own clear heading and full rows.",
    "45": "Plegian and cēosan command pairs and tōcuman's six-person present-subjunctive table stay attached to their descriptions. Ē/ō/ð and all singular/plural labels are legible; the lower table and folio are separated.",
    "46": "Geweorðan and leornian each retain a complete present-subjunctive table with the explanatory rule. Eth is clear, six rows per table align, and no orphan heading or clipped cell appears.",
    "47": "Āhyldan's full present-subjunctive table is clear. Material layout finding: the ondrǣdan present-participle heading and complete formation/scope paragraph are detached from all four matrices, which start on page 48.",
    "48": "All four ondrǣdan strong/weak agreement matrices are complete and legible, with clear ǣ and gender headings. Material layout finding: the page begins only with Strong while the entry heading and formation/scope paragraph are on page 47."
  },
  "findings": [
    {
      "id": "U17LF01",
      "status": "open",
      "severity": "material",
      "pages": [
        35,
        36
      ],
      "location": "mǣrsian: present and past participles entry across page 35 bottom and page 36 top",
      "description": "The entry heading and formation-rule paragraph are separated from the scope paragraph and two-form table by the page break, with substantial unused space at the bottom of page 35.",
      "requested_resolution": "Keep the short participle entry heading, both descriptive paragraphs and table together; inspect the affected final pages again."
    },
    {
      "id": "U17LF02",
      "status": "open",
      "severity": "material",
      "pages": [
        47,
        48
      ],
      "location": "ondrǣdan: present participle: strong and weak agreement entry across page 47 bottom and page 48 top",
      "description": "The entry heading and formation/scope paragraph are separated from all four agreement matrices. Page 48 starts only with Strong.",
      "requested_resolution": "Keep the descriptor with at least the first complete table, or move the entry introduction to page 48 if the whole group fits; inspect affected final pages again."
    },
    {
      "id": "U17LF-Q01",
      "status": "withdrawn",
      "severity": "query",
      "pages": [
        2
      ],
      "description": "Initial full-page view prompted a check of the visible space between Does and wǣre in A01 question 3.",
      "resolution": "A personally viewed lossless detail crop of the actual page-002.png shows a normal visible word space; generated TeX also contains that space. No repair required."
    },
    {
      "id": "U17LF-Q02",
      "status": "withdrawn",
      "severity": "query",
      "pages": [
        8,
        10
      ],
      "description": "Initial full-page views prompted a check of hearpere accusative and stān dative singular cell alignment.",
      "resolution": "Personally viewed lossless detail crops of the actual page-008.png and page-010.png show correctly aligned singular and plural columns. No repair required."
    }
  ]
}''')
def sha(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
manifest = json.loads((ROOT/'typesetting/ch17/build/render-manifest-v1.json').read_text(encoding='utf-8'))
current = json.loads((ROOT/'typesetting/ch17/build/render-manifest-final.json').read_text(encoding='utf-8'))
doc = manifest['documents']['learner']
current_pdf_sha = sha(doc['pdf'])
same_current = current_pdf_sha == doc['sha256'] == current['documents']['learner']['sha256']
pages = []
for n in range(1,49):
    entry = doc['images'][n-1]
    image_sha = sha(entry['path'])
    assert image_sha == entry['sha256']
    pages.append({
        'page': n,
        'status': 'needs_revision' if n in (35,36,47,48) else 'pass',
        'actually_viewed': True,
        'inspection_method': 'Personal full-page visual inspection of the actual 150-dpi PNG with view_image; no contact-sheet, OCR, or hash substitution.' + (' Supplementary lossless detail crop personally viewed to resolve a visual query.' if n in (2,8,10) else ''),
        'observations': payload['observations'][str(n)],
        'final_identity_verified': same_current,
        'image_path': entry['path'],
        'image_sha256': image_sha,
        'personally_viewed_image': {'path':entry['path'],'sha256':image_sha}
    })
review = {
    'schema_version':1,
    'document':'learner',
    'reviewer':'unit17_pages_first',
    'status':'needs_revision',
    'reviewed_at_utc':datetime.now(timezone.utc).isoformat(),
    'accepted_text_checkpoint':'a137171',
    'pdf_path':doc['pdf'],
    'pdf_sha256':doc['sha256'],
    'render_version':'v1',
    'render_dpi':150,
    'scope':'Personal page review of learner pages 1–48 only: 48 of the 96 learner pages, not all 141 learner-plus-key pages.',
    'findings':payload['findings'],
    'pages':pages
}
out = ROOT/'typesetting/ch17/reviews'
out.mkdir(exist_ok=True)
(out/'learner-first.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
lines = [
    '# Unit 17 learner pages 1–48 — independent visual review',
    '',
    '**Status: needs revision.** Personally inspected every full 150-dpi page image from learner v1, pages 1–48, with `view_image`. This is 48 of 96 learner pages; it is not a review of all 141 learner-plus-key pages.',
    '',
    'Reviewer: `unit17_pages_first`. Accepted text checkpoint: `a137171`.',
    '',
    'PDF SHA-256: `'+doc['sha256']+'`.',
    '',
    'The JSON ledger records the actual hash of every inspected image and concrete observations for every page. Full-page inspection covered special letters and length marks, table and header alignment, clipping, page breaks, introduction-to-table connection, readable type, headers and folios. Supplementary lossless details of pages 2, 8 and 10 resolved two visual queries without repairs.',
    '',
    '## Open findings',
    '',
    '- **U17LF01, pages 35–36:** the mǣrsian participle heading and formation rule are on page 35, while its scope paragraph and two-form table are on page 36. Keep the short entry together.',
    '- **U17LF02, pages 47–48:** the ondrǣdan agreement heading and formation/scope paragraph are on page 47, while all four matrices start on page 48. Keep the introduction with at least the first complete table.',
    '',
    'The page 2 word-space query and pages 8/10 column-alignment query were withdrawn after personal detail inspection; the history remains in the JSON findings.',
    '',
    '## Page observations',
    '',
    '| Page | Status | Personal observation |',
    '| --- | --- | --- |'
]
for page in pages:
    lines.append('| '+str(page['page'])+' | '+page['status']+' | '+page['observations'].replace('|','\\|')+' |')
(out/'learner-first.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'pages':len(pages),'status':review['status'],'current_v1_identity_verified':same_current,'actual_current_pdf_sha256':current_pdf_sha}))
