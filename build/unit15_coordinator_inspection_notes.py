"""Record actual coordinator views, not inferred image inspection."""
import hashlib,json
from pathlib import Path
p=Path('sources/audits/unit15-coordinator/primary-inspections.json')
d=json.loads(p.read_text(encoding='utf-8-sig'))
rows=[
 ('sources/audits/unit15-source/exercise-003.png','Cook Exercises17: exact 30.6/30.12 wording and printed blōstnian with n; larger source image resolved the small-image ambiguity.'),
 ('sources/audits/unit15-grammar/bt_b0682.jpg','BT682b micel begins, but substantive use IV is not on this page; negative locator finding.'),
 ('sources/audits/unit15-grammar/bt_b0683.jpg','BT683a micel IV: neuter substantive quantity, with and without genitive; correct positive locator.'),
 ('sources/audits/unit15-grammar/bt_b0750.jpg','BT750b on-fōn header allows genitive,dative,accusative; II(a) quotes receiving separate pennies. Supports the bounded accusative payment frame.'),
 ('sources/audits/unit15-grammar/bt_d0357.jpg','Supplement357a gelīc IV(1): Þū dydest hig gelīce ūs, agreeing object complement plus dative comparison standard.'),
 ('sources/audits/unit15-grammar/bt_d0718.jpg','Supplement718b swīðe IV: comparative preference, rather, with different objects.'),
 ('sources/audits/unit15-source/wright-p184.png','Wright184 full strengu singular/plural class model; §383 lists hǣlu,hǣtu and says few class nouns have plural. Does not supply ordinary productive plural meanings for these two nouns.'),
 ('sources/audits/unit15-grammar/fb-p39.png','Cook39 §57.3 permits syncopation of disyllabic adjectives before vowel-initial endings and notes selected hālig without feminine/neuter-plural -u. §58 long monosyllables drop -u.'),
 ('sources/audits/unit15-grammar/fb-p40.png','Cook40 §59 shows grēne, feminine grēnu and neuter plural grēnu; -e citation adjectives follow short-model endings while replacing citation -e before another ending. §58.2 governs double-consonant simplification before consonants.'),
 ('sources/audits/unit14-grammar/fb-p79.png','Cook79 prints negative past copulas næs/nǣre/nǣron and willan negatives ne(l)le,nelt,ne(l)le,nellað with y variants. The selected e-series is directly licensed; past nolde/noldon extends the known weak ending pattern.'),
]
d['additional_images']=[{'path':f,'sha256':hashlib.sha256(Path(f).read_bytes()).hexdigest(),'actually_viewed':True,'method':'Coordinator personally viewed actual image using view_image before contract reconciliation.','observation':n} for f,n in rows]
d['additional_images'][0]['superseded_observation_note']='The earlier n judgment was mistaken; see the600dpi reinspection below. The historical observation is preserved, not accepted as the final reading.'
f='sources/audits/unit15-coordinator/cook-ex17-600.png'
d['final_reinspection']={'path':f,'sha256':hashlib.sha256(Path(f).read_bytes()).hexdigest(),'actually_viewed':True,'method':'Direct600dpi rendering of Cook Exercises1895 printed17/PDF25; personally viewed with original detail.','observation':'The hint is blōstmian, with m (two arches). This corrects the coordinator and source/grammar editors’ earlier n judgment, not Cook. The source and grammar editors independently reinspected this same actual page.','source_cache':'sources/cache/cook_ex_1895.pdf','source_cache_sha256':hashlib.sha256(Path('sources/cache/cook_ex_1895.pdf').read_bytes()).hexdigest(),'corroboration_finding_aids':['https://bosworthtoller.com/4743','https://lrc.la.utexas.edu/books/asd/dict-B'],'corroboration_limit':'Primary dictionary electronic entries corroborate blóstmian; no newly downloaded dictionary page image is claimed. The actual Cook image determines its exact prompt.'}
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Recorded',len(rows),'additional actual primary views.')
