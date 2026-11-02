"""Assemble and compile the complete two-volume course without editing components."""
from __future__ import annotations

import argparse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import unicodedata

from build_sound_history_export import escape, inline
from build_course_exports import diagnostics

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "typesetting/full-book"
LUALATEX = Path(os.environ.get("LOCALAPPDATA", "C:/Users/Ross/AppData/Local")) / "texlive/2026/bin/windows/lualatex.exe"


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def write_json(path, value):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def slug(value):
    return value.replace("/", "-")


def key(value):
    return unicodedata.normalize("NFKD", value).casefold()


def plain(value):
    value = re.sub(r"\\(?:textbf|emph)\{([^{}]*)\}", r"\1", value)
    return value.replace(r"\allowbreak{}", "").replace(r"\&", "&")


def boundary_check():
    boundary = read("book/preservation.json")
    changed = [r["path"] for r in boundary["files"] if sha(r["path"]) != r["sha256"]]
    if changed:
        raise ValueError("Protected files changed: " + ", ".join(changed))
    return len(boundary["files"])


def insert_point(line, command):
    """Attach a zero-width anchor after the first complete word/group, inside its paragraph."""
    depth = 0
    for i, char in enumerate(line):
        if char == "{" and (i == 0 or line[i - 1] != "\\"):
            depth += 1
        elif char == "}" and (i == 0 or line[i - 1] != "\\"):
            depth -= 1
        elif char == " " and depth == 0:
            return line[:i] + command + line[i:]
    if line.endswith(r"\par" + "\n"):
        return line[:-5] + command + line[-5:]
    return line.rstrip("\n") + command + ("\n" if line.endswith("\n") else "")


def front_text(volume):
    raw = (ROOT / "book/front-matter.md").read_text(encoding="utf-8")
    wanted = "Learner volume" if volume == "learner" else "Key volume"
    return re.split(r"\n## ", raw.split("## " + wanted + "\n", 1)[1], maxsplit=1)[0].strip().split("\n\n")


def component_title(component):
    return component["title"]


def assemble():
    boundary_check()
    manifest = read("book/contents.json")
    index = read("book/grammar-index.json")
    by_component = defaultdict(dict)
    for a in index["anchors"]:
        by_component[a["component_id"]][a["tex_anchor"]] = a
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "fragments").mkdir(exist_ok=True)
    (OUT / "build").mkdir(exist_ok=True)
    records = []
    for component in manifest["components"]:
        cid = component["component_id"]
        for source in component["sources"].values():
            assert sha(source["path"]) == source["sha256"], source["path"]
        raw = (ROOT / component["sources"]["tex"]["path"]).read_text(encoding="utf-8")
        assert raw.count(r"\begin{document}") == raw.count(r"\end{document}") == 1
        pre, remainder = raw.split(r"\begin{document}", 1)
        body, after = remainder.split(r"\end{document}", 1)
        assert not after.strip()
        setup = []
        for line in pre.splitlines():
            if line.startswith("%") or not line.strip() or line == r"\input{../book-layout.tex}" or line == r"\usepackage{multicol}":
                continue
            setup.append(line.replace(r"\newcommand{\runningtitle}", r"\renewcommand{\runningtitle}"))
        original_lines = body.splitlines(keepends=True)
        changes, navigation, generated = [], [], []
        hit = set()
        heading_number = 0
        pending_marker = None
        for number, line in enumerate(original_lines):
            value = line.rstrip("\n")
            revised = line
            if value.startswith(r"\pdfbookmark"):
                revised = "% book-navigation: standalone bookmark replaced by volume hierarchy\n"
            elif value.startswith(r"\booktitle{"):
                title = component_title(component)
                mark = r"\BookComponent{" + slug(cid) + "}{" + escape(title) + "}"
                revised = line.replace(r"\booktitle{", r"\booktitle{" + mark, 1)
            else:
                heading = re.fullmatch(r"\\(section|subsection)\*\{(.*)\}", value)
                if heading:
                    heading_number += 1
                    label = f"nav-{slug(cid)}-{heading_number:04}"
                    level = "subsection" if heading[1] == "section" else "subsubsection"
                    target = by_component[cid].get(value)
                    extras = r"\BookLabel{" + target["id"] + "}" if target else ""
                    if target:
                        hit.add(target["id"])
                    # Printed contents has major learner sections; all headings remain in PDF outlines.
                    printed = component["volume"] == "learner" and heading[1] == "section"
                    cmd = r"\BookHeading{" + label + "}{" + level + "}{" + escape(plain(heading[2])) + "}{" + ("1" if printed else "0") + "}" + extras
                    revised = value + cmd + ("\n" if line.endswith("\n") else "")
                    navigation.append({"label": label, "level": level, "title": plain(heading[2]), "printed_contents": printed, "source_body_line": number + 1})
                elif value in by_component[cid]:
                    target = by_component[cid][value]
                    if target["kind"] == "marker":
                        pending_marker = target
                    else:
                        revised = insert_point(line, r"\BookPoint{" + target["id"] + "}")
                        hit.add(target["id"])
                elif pending_marker and "&" in value and not value.startswith("%"):
                    # The first header cell is part of the actual first table page, even if the table moves.
                    first, rest = line.split("&", 1)
                    revised = insert_point(first, r"\BookPoint{" + pending_marker["id"] + "}") + "&" + rest
                    hit.add(pending_marker["id"])
                    pending_marker = None
            if revised != line:
                changes.append({"source_body_line": number + 1, "original": line, "generated": revised})
            generated.append(revised)
        expected = {a["id"] for a in by_component[cid].values()}
        assert hit == expected, (cid, expected - hit)
        fragment = "\n".join([r"\BookRecto", r"\begingroup", *setup, "% book-source-body:begin"]) + "\n"
        fragment += "".join(generated)
        fragment += "\n% book-source-body:end\n" + r"\par\label{end-" + slug(cid) + "}" + "\n" + r"\clearpage\endgroup" + "\n"
        relative = "typesetting/full-book/fragments/" + slug(cid) + ".tex"
        (ROOT / relative).write_text(fragment, encoding="utf-8", newline="\n")
        records.append({"component_id": cid, "volume": component["volume"], "fragment": relative, "fragment_sha256": sha(relative),
                        "source_tex": component["sources"]["tex"], "source_body_sha256": hashlib.sha256(body.encode()).hexdigest(),
                        "changes": changes, "navigation": navigation, "index_anchors": sorted(hit),
                        "start_label": "component-" + slug(cid), "end_label": "end-" + slug(cid)})
    content_map = {"schema_version": 1, "manifest_sha256": sha("book/contents.json"), "index_sha256": sha("book/grammar-index.json"),
                   "front_matter_sha256": sha("book/front-matter.md"), "components": records}
    write_json("typesetting/full-book/content-map.json", content_map)
    for volume, stem in [("learner", "book"), ("key", "answer-key")]:
        title = "Learner’s Book" if volume == "learner" else "Answer Key"
        lines = [r"\newcommand{\runningtitle}{Contents}", r"\input{../book-layout.tex}", r"\usepackage{multicol}",
                 r"\hypersetup{pdftitle={Old English: " + title + r"},pdfsubject={A grammar-led course},bookmarksopen=false,bookmarksnumbered=false}",
                 r"\hyphenpenalty=10000\exhyphenpenalty=10000\emergencystretch=3em",
                 r"\makeatletter",
                 r"\renewcommand{\@pnumwidth}{2.3em}\renewcommand{\@tocrmarg}{3em}",
                 r"\def\toclevel@section{0}\def\toclevel@subsection{1}\def\toclevel@subsubsection{2}",
                 r"\newcommand{\BookHiddenContents}[3]{\addtocontents{toc}{\protect\BookHiddenLine{#1}{#2}{#3}}\Hy@writebookmark{}{#2}{\@currentHref}{#1}{toc}}",
                 r"\makeatother",
                 r"\newcommand{\BookHiddenLine}[3]{}",
                 r"\newcommand{\BookRecto}{\clearpage\ifodd\value{page}\else\thispagestyle{empty}\null\clearpage\fi}",
                 r"\newskip\BookSavedSkip",
                 r"\newcommand{\BookMeta}[1]{\ifvmode\begingroup\BookSavedSkip=\lastskip\ifdim\BookSavedSkip=0pt #1\else\unskip #1\vskip\BookSavedSkip\fi\endgroup\else #1\fi}",
                 r"\newcommand{\BookLabel}[1]{\BookMeta{\label{#1}}}",
                 r"\newcommand{\BookPoint}[1]{\phantomsection\label{#1}}",
                 r"\newcommand{\BookComponent}[2]{\phantomsection\label{component-#1}\addcontentsline{toc}{section}{#2}}",
                 r"\newcommand{\BookHeading}[4]{\BookMeta{\label{#1}\ifnum#4=1\addcontentsline{toc}{#2}{#3}\else\BookHiddenContents{\csname toclevel@#2\endcsname}{#3}{\thepage}\fi}}",
                 r"\newcommand{\BookNeedspace}[1]{\par\begingroup\skip0=\lastskip\vskip-\skip0\dimen0=#1\relax\advance\dimen0 by\skip0\vskip0pt plus\dimen0\penalty-100\vskip0pt plus-\dimen0\vskip\dimen0\penalty9999\vskip-\dimen0\vskip\skip0\endgroup}",
                 r"\begin{document}\raggedright\pagenumbering{roman}",
                 r"\thispagestyle{empty}\vspace*{32mm}",
                 r"\booktitle{" + escape(title.upper()) + r"}{Old English}",
                 r"{\fontsize{16}{20}\selectfont A grammar-led course\par}",
                 r"\vfill Cook / Lambdin-style course\par November 2026\par\clearpage",
                 r"\renewcommand{\runningtitle}{About this volume}",
                 r"\section*{About this volume}"]
        lines.extend(inline(p) + r"\par" for p in front_text(volume))
        lines += [r"\clearpage\renewcommand{\runningtitle}{Contents}",
                  r"\setcounter{tocdepth}{2}", r"\tableofcontents",
                  r"\BookRecto\pagenumbering{arabic}"]
        lines += [r"\input{fragments/" + slug(cid) + ".tex}" for cid in manifest["volumes"][volume]]
        if volume == "learner":
            lines += [r"\BookRecto\begingroup\renewcommand{\runningtitle}{Grammatical index}",
                      r"\phantomsection\label{grammatical-index}\addcontentsline{toc}{section}{Grammatical index}",
                      r"\booktitle{REFERENCE}{Grammatical index}",
                      r"\fontsize{10.5}{13.2}\selectfont\setlength{\columnsep}{6mm}\raggedcolumns",
                      r"\input{grammar-index.tex}", r"\clearpage\endgroup"]
        lines += [r"\end{document}"]
        (OUT / (stem + ".tex")).write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    (OUT / "grammar-index.tex").write_text("% Index is populated from actual labels after the first compile.\n", encoding="utf-8", newline="\n")
    print(json.dumps({"assembled_components": len(records), "selected_index_targets": len(index["anchors"])}))


def labels(stem):
    raw = (OUT / "build" / (stem + ".aux")).read_text(encoding="utf-8")
    found = {}
    # Label names are generated ASCII; reference text may contain balanced braces.
    for line in raw.splitlines():
        m = re.match(r"\\newlabel\{([^}]+)\}\{", line)
        if not m:
            continue
        groups, depth, start = [], 0, None
        for i in range(m.end(), len(line)):
            if line[i] == "{" and (i == 0 or line[i-1] != "\\"):
                if depth == 0: start = i + 1
                depth += 1
            elif line[i] == "}" and (i == 0 or line[i-1] != "\\"):
                depth -= 1
                if depth == 0 and start is not None: groups.append(line[start:i])
                if depth < 0: break
        if len(groups) >= 4:
            found[m[1]] = {"page": groups[1], "destination": groups[3]}
    return found


def index_heading_id(heading):
    return "index-" + hashlib.sha256(heading.encode()).hexdigest()[:12]


def resolve_index():
    data = read("book/grammar-index.json")
    locations = labels("book")
    groups = defaultdict(list)
    resolved = []
    for item in data["entries"]:
        pages = {}
        for aid in item["anchors"]:
            assert aid in locations, "Index anchor missing: " + aid
            page = locations[aid]["page"]
            assert page.isdigit(), (aid, page)
            pages.setdefault(int(page), aid)
        row = dict(item, references=[{"page": p, "anchor": a, "destination": locations[a]["destination"]} for p, a in sorted(pages.items())])
        resolved.append(row)
        groups[item["heading"]].append(row)
    see = {r["heading"]: r["references"] for r in data["see"]}
    also = {r["heading"]: r["references"] for r in data["see_also"]}
    def crossrefs(refs):
        parts = []
        for ref in refs:
            text = ref["heading"] + (", " + ref["subheading"] if ref.get("subheading") else "")
            parts.append(r"\hyperlink{" + index_heading_id(ref["heading"]) + "}{" + escape(text) + "}")
        return "; ".join(parts)
    lines = [r"\begin{multicols}{2}"]
    letter = None
    for heading in sorted(set(groups) | set(see), key=key):
        initial = heading[0].upper()
        if initial != letter:
            lines += [r"\BookNeedspace{5\baselineskip}", r"\par\addvspace{6pt}{\large\bfseries " + escape(initial) + r"\par}"]
            letter = initial
        lines += [r"\BookNeedspace{3\baselineskip}", r"\par\addvspace{3pt}\noindent\hypertarget{" + index_heading_id(heading) + r"}{}\textbf{" + escape(heading) + "}"]
        if heading in see:
            lines[-1] += r". \emph{See} " + crossrefs(see[heading]) + r".\par"
            continue
        lines[-1] += r"\par\nopagebreak[4]"
        for row in groups[heading]:
            refs = ", ".join(r"\hyperref[" + r["anchor"] + "]{" + str(r["page"]) + "}" for r in row["references"])
            lead = escape(row["subheading"]) + ", " if row["subheading"] else ""
            lines.append(r"\par\noindent\hangindent=1em\hangafter=1\hspace*{1em}" + lead + refs + r"\par")
        if heading in also:
            lines.append(r"\par\noindent\hangindent=1em\hangafter=1\hspace*{1em}\emph{See also} " + crossrefs(also[heading]) + r".\par")
    lines.append(r"\end{multicols}")
    (OUT / "grammar-index.tex").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    write_json("typesetting/full-book/index-locations.json", {"schema_version": 1, "index_sha256": sha("book/grammar-index.json"), "entries": resolved,
                "anchors": {a["id"]: locations[a["id"]] for a in data["anchors"]}, "see": data["see"], "see_also": data["see_also"]})


def compile_pass(stem, number):
    result = subprocess.run([str(LUALATEX), "-interaction=nonstopmode", "-halt-on-error", "-output-directory=build", stem + ".tex"],
                            cwd=OUT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", errors="replace",
                            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    (OUT / "build" / f"{stem}-pass-{number}.txt").write_text(result.stdout, encoding="utf-8")
    if result.returncode:
        raise RuntimeError(f"{stem} pass {number} failed:\n" + result.stdout[-6000:])
    page_count = re.search(r"Output written on .*?\((\d+) pages?", result.stdout, re.S)
    print(stem, "pass", number, "pages", page_count[1] if page_count else "unknown", flush=True)


def compile_volume(volume):
    stem = "book" if volume == "learner" else "answer-key"
    compile_pass(stem, 1)
    if volume == "learner":
        resolve_index()
    previous = None
    for number in range(2, 6):
        compile_pass(stem, number)
        current = labels(stem)
        if volume == "learner":
            resolve_index()
        if current == previous:
            break
        previous = current
    else:
        raise RuntimeError("Page labels did not stabilize: " + stem)
    log = (OUT / "build" / (stem + ".log")).read_text(encoding="utf-8", errors="replace")
    findings = diagnostics(log)
    for marker in ["undefined references", "multiply defined", "destination with the same identifier", "Token not allowed"]:
        if marker in log:
            findings.append({"message": marker})
    write_json(f"build/full-book/{stem}-compile.json", {"status": "passed" if not findings else "needs_review", "volume": volume, "passes": number,
               "pdf": f"typesetting/full-book/build/{stem}.pdf", "pdf_sha256": sha(f"typesetting/full-book/build/{stem}.pdf"),
               "labels": current, "diagnostics": findings})
    print(stem, "diagnostics", len(findings), flush=True)
    return not findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=["assemble", "compile", "all"], default="all")
    parser.add_argument("--volume", choices=["learner", "key", "all"], default="all")
    args = parser.parse_args()
    if args.stage in ["assemble", "all"]:
        assemble()
    if args.stage in ["compile", "all"]:
        boundary_check()
        volumes = ["learner", "key"] if args.volume == "all" else [args.volume]
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(compile_volume, volumes))
        return 0 if all(results) else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
