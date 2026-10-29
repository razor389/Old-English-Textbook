# Old English dictionary presentation: verb review

The printed dictionary should use the infinitive or an explicitly labelled citation headword, followed by class-appropriate principal parts. The complete surface-form index remains internal coverage evidence. Replacing the printed form lists does not authorize dropping any lemma, sense, source-error notice, or internal lookup route.

This reviewed handoff supplies machine-actionable `printed_diagnostics` for all **372 verb-labelled entries**. It includes **97 strong**, **107 weak**, **11 preterite-present**, **8 irregular**, and **3 impersonal** entries, plus **146 bounded source citations**. Every one of the **213 complete indicative systems expressed in structured register fields** has a classified core; the remaining systems with selected diagnostic cells were also checked. There are **zero unresolved core reference cells** and **zero unclassified complete systems**. Bounded source citations are explicitly reported rather than counted as complete paradigms.

| Verb type | Principal-part line |
| --- | --- |
| Strong | Infinitive; preterite 1 sg.; preterite plural; base past participle. |
| Weak | Infinitive; preterite 1 sg.; base past participle. Omit the predictable preterite plural. |
| Preterite-present | Citation headword; present 1/3 sg.; present plural; weak preterite; past participle only where evidenced. |
| Irregular | Useful present singulars and plural; preterite singular and plural; evidenced participle. Keep wesan and bēon present series identifiable. |
| Impersonal | Present 3 sg.; preterite 3 sg.; evidenced participle. Do not relabel these as personal first-singular cells. |

Ordinary present third-singular forms are provided separately as `present_3sg_candidate`, for the independent selective cross-reference policy. They are not all printed automatically. Keep useful vowel changes and contractions, while avoiding a new catalogue of predictable endings. `pret. 1 sg.` is deliberate: findan has the exceptional third-singular funde, so a blanket “1/3 sg.” label would be false.

The existing defective-citation caveats remain for durran, sculan, mugan and mōtan. Six preterite-present entries have no ordinary past participle in the checked paradigm; this is a source limit, not a universal nonattestation claim. Āgan instead carries the explicitly adjectival participle āgen “own”. Willan and wesan receive the same bounded statement about their source paradigms. Positive and negative forms retain separate labels.

**Recovered source evidence.** I actually opened and read 22 Cook grammar page images, covering printed pp. 59–80. The JSON binds every image hash and the printed-to-PDF convention (printed + 16 = one-based PDF page). It adds **80 past-participle reference forms** and **one adjectival participle**: **12 exact source citations** and **69 individually reviewed reference formations from the checked class rules**. The latter are declared new reference material, not claims that the source prints each resulting prefixed word as an independent token. The data gives the exact lexical-class evidence, rule and source pages for each. No open-ended conjugation rule is supplied.

The formations retain the selected course stems and spelling: for example āfēded/scrȳded use the source-permitted full dental participle, genēalǣced/nēalǣced follow the course’s class-113 system rather than importing the unrelated class-114 lǣht stem, and gearcod preserves the unprefixed gearcian lexeme. Optional (ge) is reproduced only where directly present in a selected source citation; it is not treated as a free lexical prefix.

Five existing-register display omissions are repaired explicitly: forgiefen (`forgiefan-pp-bare-source`) and gemētt (`gemetan-pp-bare-source`) require the contextual analysis; ongēaton (`ongietan-pret-3-pl-u12-source`) requires the source analysis/reference table; hǣlde and blōstmode are already supplied principal-part references in Unit 15. The previous Unit 16 principal-part repairs remain intact.

The six inflected participle exclusions remain frozen: bundene, gemanigfielde, gesceapene, gescrȳdde, tōgēiecte and worhte in their previously identified records. Their actual surface routes remain in the internal lookup. A number/case/gender guard must be combined with the explicit prose-evidence exclusions; metadata-key checks alone miss the latter.

**Integration.** Use `printed_diagnostics` as the core and add only independently selected ordinary present-third-singular diagnostics. New reference IDs are scoped to this review (`GLOSS-DICT-PP-*`, plus `GLOSS-DICT-ADJ-PART-agan`); they are not pretended to be existing cumulative-register records. Preserve the input form lookup unchanged. Individual source-only notes can be replaced by one front-matter explanation where `render_scope_note_individually` is false; retain the defective and non-infinitive headword notes. Apply approved data idempotently, regardless of later verification-status wording.

| Entry | Additional reference form | Cook printed page(s) | Evidence relation |
| --- | --- | --- | --- |
| ādrīfan | ādrifen | 59 | reviewed rule formation |
| āfēdan | āfēded | 68, 69 | reviewed rule formation |
| āgan | āgen | 77 | exact source |
| ālīehtan | ālīeht | 68, 69 | reviewed rule formation |
| ālūtan | āloten | 60, 61 | reviewed rule formation |
| andswarian | andswarod | 73, 74 | reviewed rule formation |
| āscian | āscod | 73, 74 | reviewed rule formation |
| āstīgan | āstigen | 59, 60 | reviewed rule formation |
| āstręccean | āstreaht | 69, 70 | reviewed rule formation |
| āweorpan | āworpen | 61, 62 | reviewed rule formation |
| āwrītan | āwriten | 59, 60 | reviewed rule formation |
| bēatan | bēaten | 66, 67 | reviewed rule formation |
| bebēodan | beboden | 60, 61 | reviewed rule formation |
| begān | begān | 80 | reviewed rule formation |
| behealdan | behealden | 66 | reviewed rule formation |
| bīegan | bīeged | 68, 69 | reviewed rule formation |
| blāwan | blāwen | 66, 67 | reviewed rule formation |
| bringan | (ge)brōht | 70 | exact source |
| bycgan | (ge)boht | 70 | exact source |
| cēapian | cēapod | 73, 74 | reviewed rule formation |
| cīepan | cīeped | 68, 69 | reviewed rule formation |
| cunnan | (ge)cunnen | 77 | exact source |
| cȳðan | cȳðed | 68, 69 | reviewed rule formation |
| dōn | (ge)dōn | 79 | exact source |
| ęfthweorfan | ęfthworfen | 61, 62 | reviewed rule formation |
| ēhtan | (ge)ēht | 68 | exact source |
| feohtan | fohten | 61, 62 | reviewed rule formation |
| flēon | flogen | 60 | reviewed rule formation |
| fordōn | fordōn | 79 | reviewed rule formation |
| foresęcgean | foresægd | 75 | reviewed rule formation |
| forstelan | forstolen | 63 | reviewed rule formation |
| forwiernan | forwierned | 68, 69 | reviewed rule formation |
| fręmman | (ge)fręmed | 71, 72 | exact source |
| gān | (ge)gān | 80 | exact source |
| gearcian | gearcod | 73, 74 | reviewed rule formation |
| gecweðan | gecweden | 63, 64 | reviewed rule formation |
| gegaderian | gegaderod | 73, 74 | reviewed rule formation |
| gemunan | gemunen | 78 | reviewed rule formation |
| genēalǣcan | genēalǣced | 68, 69 | reviewed rule formation |
| genēosian | genēosod | 73, 74 | reviewed rule formation |
| gesęttan | gesętt | 68, 69 | reviewed rule formation |
| gestillan | gestilled | 68, 69 | reviewed rule formation |
| gewilnian | gewilnod | 73, 74 | reviewed rule formation |
| gewunian | gewunod | 73, 74 | reviewed rule formation |
| gīeman | gīemed | 68, 69 | reviewed rule formation |
| giernan | gierned | 68, 69 | reviewed rule formation |
| grētan | grētt | 68, 69 | reviewed rule formation |
| hālsian | hālsod | 73, 74 | reviewed rule formation |
| hatian | hatod | 73, 74 | reviewed rule formation |
| hęrian | hęred | 71, 72 | reviewed rule formation |
| hyngran | (ge)hyngred | 71 | exact source |
| ingān | ingān | 80 | reviewed rule formation |
| lęcgean | (ge)lęgd | 71 | reviewed rule formation |
| leornian | leornod | 73, 74 | reviewed rule formation |
| nēalǣcan | nēalǣced | 68, 69 | reviewed rule formation |
| oferwinnan | oferwunnen | 61, 62 | reviewed rule formation |
| oferwyrcean | oferworht | 69, 70 | reviewed rule formation |
| ofðyncean | ofðūht | 70 | reviewed rule formation |
| oncnāwan | oncnāwen | 66 | reviewed rule formation |
| ondrǣdan | ondrǣden | 67 | reviewed rule formation |
| rīcsian | rīcsod | 73, 74 | reviewed rule formation |
| rōwan | rōwen | 66, 67 | reviewed rule formation |
| scēawian | scēawod | 73, 74 | reviewed rule formation |
| scęncan | scęnced | 68, 69 | reviewed rule formation |
| scęððan | scęðed | 71, 72 | reviewed rule formation |
| scrȳdan | scrȳded | 68, 69 | reviewed rule formation |
| sēcan | (ge)sōht | 70 | exact source |
| spǣtan | spǣtt | 68, 69 | reviewed rule formation |
| tǣlan | tǣled | 68, 69 | reviewed rule formation |
| tōgelǣdan | tōgelǣded | 68, 69 | reviewed rule formation |
| tōtwǣman | tōtwǣmed | 68, 69 | reviewed rule formation |
| ðęncan | (ge)ðōht | 70 | reviewed rule formation |
| ðolian | ðolod | 73, 74 | reviewed rule formation |
| ðurhwunian | ðurhwunod | 73, 74 | reviewed rule formation |
| undōn | undōn | 79 | reviewed rule formation |
| unnan | (ge)unnen | 77 | exact source |
| wician | wicod | 73, 74 | reviewed rule formation |
| windan | wunden | 61, 62 | reviewed rule formation |
| witan | (ge)witen | 76 | exact source |
| wiðstandan | wiðstanden | 65 | reviewed rule formation |
| wunian | wunod | 73, 74 | reviewed rule formation |

Validation confirms unique entry IDs, exact resolution of every printed diagnostic ID and spelling, absence of all six excluded inflected-participle IDs, and class-appropriate completeness for all full structured indicative systems. This review does not accept any PDF pagination: visual inspection remains paused pending the revised dictionary export.

Policy JSON SHA256: `dec0cc9c350788b156b7ec461eabab7677638217410b8c092a6cd75f0a898253`.
