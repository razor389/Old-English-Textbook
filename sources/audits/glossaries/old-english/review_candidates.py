"""Print bounded contexts for the lexical candidates found during type review."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "build/glossary-oe"

# These are review candidates, not declarations that a string is a valid word.
CANDIDATES = """
andswerian beboden burge cumenne cyme cyn dorst felgan fisc-cynn fiscer
for-ceorfan for-wiernan forceorf forcierf forcorf forcurf forguld forgēaf fugolas
fuluhter ge-lýfan ge-manig-fieldan ge-neósian ge-weald gearo geatum gegierel
gelýfan geseon gewendan geworpen guma gán hlyst hwelc hwilcera hwilcere hwylc
hwǣt hyngrian lifie lifien magan mehte mild-heort mild-heortnes munan mynsteru
mótan nafogār nearo nieht nihte nōht nǣnig ofslagen ongiet ringe rēd rēdon rēn
rīcia rīciu sceamul scencan scolde scoldon scēaphierd secgan seofoð seol siext
sint slægene smire smylt smyltness sonne strengo styriend stán-weall sumode
sunas sunes swerian syn sīn til uncr ut wealh weorðscip werod wieton wilde
wile wioton wisse wissen wundas
be-bēodan brōðru bōce cēapmann cīepa cīepmann cȳdde cȳðst deorwurðan dęnia
dęniga fielþ filhþ fiscnað for-weorðan frēan frēondas fædere fæderes fēdeð
fēondas fēran fētt fōnende fōtas fōte ge-fēra ge-sēon gelǣdst gelǣran
genēalǣhte gescrȳdd grēne grēowon grōwan gōd-wębb gōdena hwæt-swā
hwæðere hwæðeres hæfd hālgra hęrgas hęrges hęrigas hęrigeas hęriges
hūlīc hȳd lēde lēdon lęcgan lǣden mægð nēosian rēd rēdon rēn rīcia rīciu
sciphęr scōd slægene swētrra swīgiende sāde sāden tō-berstan tō-twǣman
tōdǣlan tōðas tōðe unnað wætru wīsrra ðām ðēah-ðe ðęncean þing þonne þrēo
þurfan þyncan þūsend ā-gildan ābēad āfyld āgyltan āhebban āhwæðer āhwā āstāh
āwęg ēadges ēagna ęfned ęgesan īeced ōht ūpāhebban ǣghwæðer ǣghwā
""".split()


def main():
    data = json.loads((OUT / "all-token-concordance.json").read_text(encoding="utf-8"))
    rows = []
    for token in sorted(set(CANDIDATES)):
        for loc in data.get(token, [])[:2]:
            text = loc["context"]
            m = re.search(re.escape(token), text, re.I)
            start = max(0, m.start()-55) if m else 0
            end = m.end()+170 if m else 225
            rows.append(f"{token}\t{loc['path']}:{loc['line']}\t{text[start:end]}")
    (OUT / "review-candidate-contexts.tsv").write_text("\n".join(rows)+"\n", encoding="utf-8")
    print("\n".join(rows))


if __name__ == "__main__":
    main()
