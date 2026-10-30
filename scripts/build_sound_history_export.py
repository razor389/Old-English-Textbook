"""Render the complete editable sound-history appendix in the shared course style."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
STAR = "LITERALRECONSTRUCTIONSTAR"


def escape(value):
    replacements = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
                    "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
                    "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    return "".join(replacements.get(c, c) for c in value.replace(STAR, "*"))


def inline(value):
    assert STAR not in value
    value = value.replace(r"\*", STAR)
    # Link labels remain readable in the standalone print appendix.
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
    parts = re.split(r"(\*\*[^*]+\*\*|(?<!\*)\*[^*\n]+\*(?!\*))", value)
    output = []
    for part in parts:
        if part.startswith("**") and part.endswith("**"):
            output.append(r"\textbf{" + escape(part[2:-2]) + "}")
        elif part.startswith("*") and part.endswith("*"):
            output.append(r"\emph{" + escape(part[1:-1]) + "}")
        else:
            output.append(escape(part))
    return "".join(output)


def blocks(raw):
    for chunk in re.split(r"\n\s*\n", raw.strip()):
        lines = chunk.splitlines()
        if all(line.startswith("<!--") and line.endswith("-->") for line in lines):
            yield "comment", chunk
        elif lines[0].startswith("# "):
            assert len(lines) == 1
            yield "title", lines[0][2:]
        elif re.match(r"^#{2,3} ", lines[0]):
            assert len(lines) == 1
            yield ("heading" if lines[0].startswith("## ") else "subheading"), re.sub(r"^#+ ", "", lines[0])
        elif lines[0].startswith("|"):
            assert len(lines) >= 2 and re.fullmatch(r"[| :\-]+", lines[1])
            rows = [[c.strip() for c in re.split(r"(?<!\\)\|", line.strip()[1:-1])] for line in lines]
            matrix = [rows[0], *rows[2:]]
            assert all(len(row) == len(matrix[0]) for row in matrix)
            yield "table", matrix
        elif all(line.startswith("- ") for line in lines):
            for line in lines:
                yield "bullet", line[2:]
        elif all(re.match(r"^\d+\.\s+", line) for line in lines):
            for line in lines:
                yield "paragraph", line
        else:
            yield "paragraph", " ".join(lines)


def table(matrix):
    columns = len(matrix[0])
    weights = {2: [0.34, 0.66], 3: [0.25, 0.35, 0.40], 4: [0.25]*4}.get(columns, [1/columns]*columns)
    if matrix[0][0] == "Nominative/accusative singular":
        weights = [0.35, 0.35, 0.30]
    # Allocate the actual intercolumn space; @{} removes the two outer pads.
    axes = "@{}" + "".join(r">{\raggedright\arraybackslash}p{\dimexpr" + f"{w:.4f}" + r"\linewidth-" + f"{2*w*(columns-1):.4f}" + r"\tabcolsep\relax}" for w in weights) + "@{}"
    header = " & ".join(r"\textbf{" + inline(cell) + "}" for cell in matrix[0]) + r" \\"
    lines = [r"\begingroup", r"\fontsize{10.5}{13.2}\selectfont", r"\setlength{\LTleft}{0pt}",
             r"\setlength{\LTright}{0pt plus 1fil}", r"\begin{longtable}{" + axes + "}",
             r"\toprule", header, r"\midrule", r"\endfirsthead", r"\toprule", header,
             r"\midrule", r"\endhead", r"\bottomrule", r"\endfoot", r"\bottomrule", r"\endlastfoot"]
    lines.extend(" & ".join(inline(cell) for cell in row) + r" \\" for row in matrix[1:])
    lines += [r"\end{longtable}", r"\endgroup"]
    return lines


def main():
    master = ROOT / "appendices/sound-history/student.md"
    events = list(blocks(master.read_text(encoding="utf-8-sig")))
    lines = ["% Complete editable master: appendices/sound-history/student.md",
             r"\newcommand{\runningtitle}{Sound history}", r"\input{../book-layout.tex}",
             r"\hyphenpenalty=10000\exhyphenpenalty=10000", r"\emergencystretch=3em",
             r"\newcommand{\reserve}[1]{\par\penalty-100\begingroup\dimen0=\pagegoal\advance\dimen0 by-\pagetotal\ifdim\dimen0<#1\newpage\fi\endgroup}",
             r"\begin{document}", r"\addfontfeatures{Ligatures=TeXOff}", r"\raggedright"]
    record = []
    for kind, value in events:
        if kind == "comment":
            lines.extend("% " + line[4:-3].strip() for line in value.splitlines())
            continue
        identifier = f"B{len(record)+1:03}"
        if kind in ["heading", "subheading"]:
            lines.append(r"\reserve{5\baselineskip}")
        lines.append(f"% appendix-block:{identifier}:{kind}:begin")
        if kind == "title":
            lines.append(r"\booktitle{APPENDIX}{" + inline(value) + "}")
        elif kind in ["heading", "subheading"]:
            command = "section" if kind == "heading" else "subsection"
            lines.append("\\" + command + "*{" + inline(value) + "}")
        elif kind == "table":
            lines.extend(table(value))
        elif kind == "bullet":
            lines.append(r"\begin{itemize}\item " + inline(value) + r"\end{itemize}")
        else:
            lines.append(inline(value) + r"\par")
        lines.append(f"% appendix-block:{identifier}:end")
        record.append({"id": identifier, "kind": kind})
    lines.append(r"\end{document}")
    target = ROOT / "typesetting/sound-history"
    target.mkdir(parents=True, exist_ok=True)
    (target / "sound-history.tex").write_text("\n".join(lines)+"\n", encoding="utf-8", newline="\n")
    (target / "content-map.json").write_text(json.dumps({"master": master.relative_to(ROOT).as_posix(),
        "master_sha256": hashlib.sha256(master.read_bytes()).hexdigest(), "blocks": record}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8", newline="\n")
    print(json.dumps({"blocks": len(record), "tables": sum(r['kind']=='table' for r in record)}))


if __name__ == "__main__":
    main()
