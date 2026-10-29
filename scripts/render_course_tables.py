"""Render revised course tables without reassembling surrounding lesson TeX.

This module has no import-time writes.  The renderer consumes the explicit
table records returned by ``course_tables.transform_document``.  Historical
one-use assemblers are deliberately not imported.

The returned audit contains physical-panel coordinates and actual decoded
cells.  Callers must still compile, check the complete PDFs, and inspect pages.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Any
import unicodedata


STYLE = {
    "font_size_pt": 10.5,
    "leading_pt": 13.2,
    "available_width_mm": 124.0,
    "column_gap_mm": 2.812,
    "max_comparison_columns": 4,
    "longtable_data_rows": 16,
}

MARKED_TABLE = re.compile(
    r"(?m)^% mdtable:(?P<id>T\d+(?:[A-Za-z]|-P\d+)?):begin\r?\n"
    r"(?P<body>.*?)^% mdtable:(?P=id):end(?=\r?$)", re.S | re.M
)
TEX_ENVIRONMENT = re.compile(
    r"\\begin\{(?P<env>tabular|longtable)\}\{(?P<spec>[^\n]+)\}\r?\n"
    r"(?P<body>.*?)\\end\{(?P=env)\}", re.S
)


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).split())


def markdown_plain(text: str) -> str:
    """Visible cell text, retaining escaped and unpaired reconstruction stars."""
    text = re.sub(r"<!--.*?-->", "", text)
    text = text.replace(r"\*", "\uE000")
    text = text.replace("**", "")
    text = re.sub(r"(?<!\w)\*([^*\n]+?)\*(?!\w)", r"\1", text)
    return normalized(text.replace("\uE000", "*"))


def inline_tex(text: str) -> str:
    """Escape one Markdown cell without changing its visible Unicode text."""
    text = re.sub(r"<!--.*?-->", "", text)
    text = text.replace(r"\*", "\uE000")
    pieces = re.split(r"(\*\*.*?\*\*|(?<!\w)\*[^*\n]+?\*(?!\w))", text)
    escapes = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%",
        "$": r"\$", "#": r"\#", "_": r"\_", "/": r"/\allowbreak{}",
        "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}", "\uE000": "*",
    }

    def escape(value: str) -> str:
        return "".join(escapes.get(char, char) for char in value)

    result = []
    for piece in pieces:
        if piece.startswith("**") and piece.endswith("**") and len(piece) >= 4:
            result.append(r"\textbf{" + escape(piece[2:-2]) + "}")
        elif piece.startswith("*") and piece.endswith("*") and len(piece) > 2:
            result.append(r"\emph{" + escape(piece[1:-1]) + "}")
        else:
            result.append(escape(piece))
    return "".join(result)


def _group(text: str, pos: int) -> tuple[str, int]:
    if pos >= len(text) or text[pos] != "{":
        raise ValueError(f"Expected TeX group at {text[pos:pos+50]!r}")
    depth, start = 1, pos + 1
    pos += 1
    while depth and pos < len(text):
        if text[pos] == "\\":
            pos += 2
            continue
        if text[pos] == "{":
            depth += 1
        elif text[pos] == "}":
            depth -= 1
        pos += 1
    if depth:
        raise ValueError("Unclosed TeX group")
    return text[start:pos-1], pos


def tex_plain(text: str) -> str:
    """Strict cell decoder, independent of the emitter's row/cell maps."""
    out, pos = [], 0
    while pos < len(text):
        if text[pos] != "\\":
            out.append(text[pos])
            pos += 1
            continue
        match = re.match(r"\\([A-Za-z]+\*?|[^A-Za-z])", text[pos:])
        if not match:
            raise ValueError(f"Undecodable TeX: {text[pos:]!r}")
        name = match[1]
        pos += len(match[0])
        if name in {"textbf", "emph", "textit", "textsuperscript"}:
            body, pos = _group(text, pos)
            out.append(tex_plain(body))
        elif name == "allowbreak":
            if text[pos:pos+2] == "{}":
                pos += 2
        elif name in {"newline", "par", "raggedright"}:
            out.append(" ")
        elif name in {"&", "%", "$", "#", "_", "{", "}", "*"}:
            out.append(name)
        elif name in {"textbackslash", "textasciitilde", "textasciicircum"}:
            out.append({"textbackslash": "\\", "textasciitilde": "~",
                        "textasciicircum": "^"}[name])
            if text[pos:pos+2] == "{}":
                pos += 2
        else:
            raise ValueError(f"Unsupported cell command: {name}")
    return normalized("".join(out))


def decode_tex_tables(tex: str) -> list[list[list[str]]]:
    """Decode each physical table; omit repeated longtable header furniture."""
    tables = []
    for match in TEX_ENVIRONMENT.finditer(tex):
        rows = []
        for line in match["body"].splitlines():
            line = line.strip()
            if not line.endswith(r"\\") or line.startswith(r"\multicolumn"):
                continue
            rows.append([tex_plain(cell.strip()) for cell in line[:-2].split(" & ")])
        if match["env"] == "longtable" and len(rows) > 1 and rows[1] == rows[0]:
            rows.pop(1)
        if not rows:
            raise ValueError("Empty or undecodable TeX table")
        if any(len(row) != len(rows[0]) for row in rows):
            raise ValueError("Inconsistent decoded TeX column count")
        tables.append(rows)
    return tables


def verify_prior_table(original_rows: list[list[str]], tex: str) -> str:
    """Verify the original logical matrix against its actual retained TeX.

    Only the already documented reflows are accepted.  This binds ordinal
    matching to content, including Unit 1 where stable markers were absent.
    """
    expected = [[markdown_plain(cell) for cell in row] for row in original_rows]
    actual = decode_tex_tables(tex)
    if actual == [expected]:
        return "same coordinates"
    if len(expected[0]) == 7 and len(actual) == 2:
        panels = [[[row[c] for c in columns] for row in expected]
                  for columns in ([0, 1, 2, 3], [0, 4, 5, 6])]
        if actual == panels:
            return "singular/plural panels"
    if expected[0] == ["Verb", "Present 1 sg.", "2 sg.", "3 sg.", "All pl.",
                       "Preterite 1/3 sg.", "2 sg.", "All pl."] and len(actual) == 2:
        panels = [[['Verb', '1 sg.', '2 sg.', '3 sg.', 'All pl.']] + [row[:5] for row in expected[1:]],
                  [['Verb', '1/3 sg.', '2 sg.', 'All pl.']] + [[row[0]] + row[5:] for row in expected[1:]]]
        if actual == panels:
            return "present/preterite panels"
    if expected[0] == ["Noun", "Stem", "G singular", "D singular", "N plural", "Model"]:
        panels = [[[row[c] for c in columns] for row in expected]
                  for columns in ([0, 1, 5], [0, 2, 3, 4])]
        if actual == panels:
            return "nominal diagnostic panels"
    if len(expected[0]) == 6 and expected[0][0] == "Noun":
        reflow = [["Noun; gender", "Meaning", "Diagnostic forms", "Pattern; limit"]]
        reflow += [[f"{row[0]} ({row[1]})", row[2], f"G sg {row[3]} N pl {row[4]}", row[5]]
                   for row in expected[1:]]
        if actual == [reflow]:
            return "six-field vocabulary in four columns"
    raise ValueError("Original Markdown matrix does not match actual retained TeX")


def table_spans(tex: str) -> list[dict[str, Any]]:
    """Find complete marked blocks, or Unit 1's unmarked outer table groups."""
    marked = list(MARKED_TABLE.finditer(tex))
    if marked:
        blocks = [{"id": m["id"], "start": m.start(), "end": m.end(),
                   "raw": m[0], "body": m["body"], "marked": True} for m in marked]
        total = len(list(TEX_ENVIRONMENT.finditer(tex)))
        contained = sum(len(list(TEX_ENVIRONMENT.finditer(b["body"]))) for b in blocks)
        if total != contained:
            raise ValueError("TeX contains table environments outside its marked blocks")
        return blocks
    environments = list(TEX_ENVIRONMENT.finditer(tex))
    blocks, previous_end = [], 0
    for number, match in enumerate(environments, 1):
        begin = list(re.finditer(r"(?m)^\\par\\begingroup\r?$", tex[:match.start()]))
        if not begin or begin[-1].start() < previous_end:
            raise ValueError("Cannot identify a unique outer table group")
        end = re.match(r"\r?\n\\par\\endgroup", tex[match.end():])
        if not end:
            raise ValueError("Unmarked table lacks its expected outer group end")
        start, stop = begin[-1].start(), match.end() + end.end()
        body = tex[start:stop]
        blocks.append({"id": f"T{number:02}", "start": start, "end": stop,
                       "raw": body, "body": body, "marked": False})
        previous_end = stop
    return blocks


def _panel_columns(rows: list[list[str]]) -> list[list[int]]:
    """Readable panels repeat only the descriptor column, never omit a cell."""
    n = len(rows[0])
    # Five-column panels include two complete lemma/tense pairs.  Splitting
    # these after a third form column would separate the second lemma's tenses.
    if n <= 5:
        return [list(range(n))]
    return [[0] + list(range(start, min(start + 3, n))) for start in range(1, n, 3)]


def _widths(rows: list[list[str]], columns: list[int]) -> list[float]:
    count = len(columns)
    available = STYLE["available_width_mm"] - STYLE["column_gap_mm"] * (count - 1)
    if count == 3 and markdown_plain(rows[0][0]).lower() in {"case", "person", "person and number"}:
        return [round(available / 3, 3)] * 3
    if count in {4, 5} and markdown_plain(rows[0][0]).lower() == "case":
        return [22.0] + [round((available - 22) / (count - 1), 3)] * (count - 1)
    weights = []
    for column in columns:
        text = [markdown_plain(row[column]) for row in rows]
        longest = max((max(map(len, value.split()), default=0) for value in text), default=1)
        length = max(map(len, text), default=1)
        weights.append(max(10, min(65, .45 * length + .55 * longest)))
    return [round(available * weight / sum(weights), 3) for weight in weights]


def _physical_table(rows: list[list[str]], widths: list[float], environment: str) -> str:
    spec = "@{}" + "".join(r">{\raggedright\arraybackslash}p{" + str(w) + "mm}" for w in widths) + "@{}"
    header = " & ".join(r"\textbf{" + inline_tex(cell) + "}" for cell in rows[0]) + r" \\"
    out = [r"\setlength{\LTleft}{0pt}\setlength{\LTright}{\fill}"]
    if environment == "tabular":
        out.append(r"\noindent")
    out.extend([r"\begin{" + environment + "}{" + spec + "}", r"\toprule", header, r"\midrule"])
    if environment == "longtable":
        out.extend([r"\endfirsthead", r"\toprule", header, r"\midrule", r"\endhead",
                    r"\midrule", r"\multicolumn{" + str(len(rows[0])) + r"}{r}{\footnotesize Continued on the following page.}\\",
                    r"\endfoot", r"\bottomrule", r"\endlastfoot"])
    out.extend(" & ".join(inline_tex(cell) for cell in row) + r" \\" for row in rows[1:])
    if environment == "tabular":
        out.append(r"\bottomrule")
    out.append(r"\end{" + environment + "}")
    return "\n".join(out)


def render_block(output_tables: list[dict[str, Any]], table_id: str, *,
                 outer_minipage_closures: int = 0,
                 comments: list[str] | None = None,
                 width_overrides: dict[str, list[float]] | None = None) -> tuple[str, dict[str, Any]]:
    """Emit one stable old table block containing one or more new matrices.

    Each output table supplies ``headers``, ``rows`` and optional ``caption``.
    Physical panels retain explicit output-matrix coordinates in the audit.
    """
    if outer_minipage_closures not in {0, 1}:
        raise ValueError("Unsupported outer-minipage structure")
    out = [f"% mdtable:{table_id}:begin", "% course-table-style: 2026-10"]
    for comment in comments or []:
        out.append("% " + comment)
    panels, first = [], True
    for matrix_index, matrix in enumerate(output_tables):
        rows = [matrix["headers"]] + matrix["rows"]
        if not rows or len(rows[0]) < 2 or any(len(row) != len(rows[0]) for row in rows):
            raise ValueError(f"Invalid matrix in {table_id}")
        caption = matrix.get("caption")
        if caption:
            out.extend([r"\par\addvspace{3pt}", f"% course-caption:{table_id}:{matrix_index}:begin",
                        r"\textbf{" + inline_tex(caption) + r"}\par\nobreak",
                        f"% course-caption:{table_id}:{matrix_index}:end"])
        for columns in _panel_columns(rows):
            panel_id = f"{table_id}-P{len(panels)+1:02}"
            actual = [[row[c] for c in columns] for row in rows]
            widths = (width_overrides or {}).get(panel_id, _widths(rows, columns))
            if len(widths) != len(columns) or any(w <= 0 for w in widths):
                raise ValueError(f"Invalid width override for {panel_id}")
            environment = "longtable" if len(rows) - 1 > STYLE["longtable_data_rows"] else "tabular"
            out.extend([f"% course-panel:{panel_id}:begin", r"\par\begingroup",
                        r"\fontsize{10.5}{13.2}\selectfont",
                        _physical_table(actual, widths, environment), r"\par\endgroup",
                        f"% course-panel:{panel_id}:end"])
            panels.append({"panel_id": panel_id, "output_table_index_zero_based": matrix_index,
                           "source_columns_zero_based": columns, "environment": environment,
                           "widths_mm": widths, "expected_cells": [[markdown_plain(c) for c in row] for row in actual]})
            if first and outer_minipage_closures:
                out.append(r"\end{minipage}\par")
            first = False
            out.append(r"\par\addvspace{5pt}")
    if out[-1] == r"\par\addvspace{5pt}":
        out.pop()
    out.append(f"% mdtable:{table_id}:end")
    rendered = "\n".join(out)
    actual_cells = decode_tex_tables(rendered)
    expected_cells = [p["expected_cells"] for p in panels]
    if actual_cells != expected_cells:
        raise ValueError(f"Actual decoded TeX differs from supplied matrices: {table_id}")
    captions = re.findall(r"% course-caption:[^\n]+:begin\n\\textbf\{(.*?)\}\\par\\nobreak\n% course-caption:[^\n]+:end", rendered)
    if [tex_plain(caption) for caption in captions] != [markdown_plain(t["caption"]) for t in output_tables if t.get("caption")]:
        raise ValueError(f"Actual decoded captions differ from supplied captions: {table_id}")
    return rendered, {"table_id": table_id, "panels": panels, "decoded_cell_parity": "pass",
                      "outer_minipage_closures": outer_minipage_closures,
                      "rendered_sha256": sha256(rendered)}


def _record_tables(record: dict[str, Any]) -> list[dict[str, Any]]:
    """Normalize the pure transform's output blocks without executing it."""
    blocks = record.get("output_blocks", [])
    tables = []
    for block in blocks:
        if isinstance(block, dict) and "headers" in block and "rows" in block:
            tables.append({"headers": block["headers"], "rows": block["rows"],
                           "caption": block.get("caption")})
        else:
            raise ValueError("Expected output_blocks with headers/rows/caption")
    if not tables:
        raise ValueError("Transform record contains no output matrices")
    return tables


def verify_revised_tables(tex: str, table_records: list[dict[str, Any]]) -> dict[str, Any]:
    """Recheck actual revised TeX independently of any stored render report.

    This remains valid after width or pagination repairs: it decodes the real
    table text and compares it with the pure transform's output coordinates.
    The old block IDs intentionally survive when one old matrix becomes
    several new Markdown matrices.
    """
    spans = table_spans(tex)
    if len(spans) != len(table_records):
        raise ValueError("Revised TeX block count differs from original table groups")
    cells, outputs, captions = 0, 0, 0
    for index, (span, record) in enumerate(zip(spans, table_records)):
        if record.get("original_index_zero_based", index) != index:
            raise ValueError("Revised verification records are out of order")
        matrices = _record_tables(record)
        outputs += len(matrices)
        if not record["changed"]:
            if len(matrices) != 1 or matrices[0].get("caption"):
                raise ValueError("Unexpected transformation of an unchanged matrix")
            verify_prior_table([matrices[0]["headers"]] + matrices[0]["rows"], span["body"])
            cells += sum(len(row) for row in [matrices[0]["headers"]] + matrices[0]["rows"])
            continue
        expected = []
        for matrix in matrices:
            rows = [matrix["headers"]] + matrix["rows"]
            columns = _panel_columns(rows)
            if set(c for panel in columns for c in panel) != set(range(len(rows[0]))):
                raise ValueError("Panel coordinates omit a source column")
            expected.extend([[[markdown_plain(row[c]) for c in panel] for row in rows] for panel in columns])
            cells += sum(len(row) for row in rows)
        actual = decode_tex_tables(span["body"])
        if actual != expected:
            raise ValueError(f"{span['id']}: actual revised TeX cells differ")
        actual_captions = re.findall(r"% course-caption:[^\n]+:begin\r?\n\\textbf\{(.*?)\}\\par\\nobreak\r?\n% course-caption:[^\n]+:end", span["body"])
        expected_captions = [markdown_plain(matrix["caption"]) for matrix in matrices if matrix.get("caption")]
        if [tex_plain(caption) for caption in actual_captions] != expected_captions:
            raise ValueError(f"{span['id']}: actual revised TeX captions differ")
        captions += len(expected_captions)
    return {"status": "pass", "original_table_groups": len(spans),
            "output_markdown_matrices": outputs, "logical_display_cells_checked": cells,
            "caption_count": captions}


def replace_table_blocks(tex: str, table_records: list[dict[str, Any]], *,
                         width_overrides: dict[str, list[float]] | None = None) -> tuple[str, dict[str, Any]]:
    """Surgically apply a complete ordered list of pure table transforms.

    Non-table segments are copied verbatim.  Unchanged marked tables remain
    byte-identical; unmarked Unit 1 tables acquire stable ordinal markers.
    """
    spans = table_spans(tex)
    if len(spans) != len(table_records):
        raise ValueError(f"Table count mismatch: {len(spans)} TeX / {len(table_records)} records")
    newline = "\r\n" if "\r\n" in tex else "\n"
    result, cursor, audits, untouched = [], 0, [], []
    for index, (span, record) in enumerate(zip(spans, table_records)):
        if record.get("original_index_zero_based", index) != index:
            raise ValueError("Transform records are not in original table order")
        prior_mode = None
        if "original_headers" in record and "original_rows" in record:
            try:
                prior_mode = verify_prior_table([record["original_headers"]] + record["original_rows"], span["body"])
            except ValueError as error:
                raise ValueError(f"{span['id']}: {error}") from error
        prefix = tex[cursor:span["start"]]
        result.append(prefix)
        untouched.append(prefix)
        changed = record.get("changed")
        if changed is None:
            changed = record.get("original_raw") != record.get("revised_raw")
        if changed:
            if prior_mode is None:
                raise ValueError("Changed tables require their original headers/rows")
            matrix_data = _record_tables(record)
            delta = span["body"].count(r"\begin{minipage}") - span["body"].count(r"\end{minipage}")
            if delta not in {0, -1}:
                raise ValueError(f"Unexpected minipage delta {delta} in {span['id']}")
            comments = []
            for line in span["body"].splitlines():
                if line.startswith("% ") and not line.startswith(("% mdtable:", "% table-reflow:", "% course-")):
                    comments.append(line[2:])
            replacement, audit = render_block(matrix_data, span["id"], outer_minipage_closures=-delta,
                                               comments=comments, width_overrides=width_overrides)
            replacement = replacement.replace("\n", newline)
        elif span["marked"]:
            replacement = span["raw"]
            audit = {"table_id": span["id"], "unchanged": True}
        else:
            replacement = f"% mdtable:{span['id']}:begin{newline}" + span["raw"] + f"{newline}% mdtable:{span['id']}:end"
            audit = {"table_id": span["id"], "unchanged": True, "ordinal_markers_added": True}
        result.append(replacement)
        cursor = span["end"]
        audit.update({"original_tex_sha256": sha256(span["raw"]),
                      "revised_tex_sha256": sha256(replacement), "changed": bool(changed),
                      "original_matrix_to_tex_parity": prior_mode})
        audits.append(audit)
    result.append(tex[cursor:])
    untouched.append(tex[cursor:])
    revised = "".join(result)
    final_spans = table_spans(revised)
    outside, cursor = [], 0
    for span in final_spans:
        outside.append(revised[cursor:span["start"]])
        cursor = span["end"]
    outside.append(revised[cursor:])
    if untouched != outside:
        raise ValueError("Non-table TeX changed")
    if tex.count(r"\begin{minipage}") - tex.count(r"\end{minipage}") != revised.count(r"\begin{minipage}") - revised.count(r"\end{minipage}"):
        raise ValueError("Document minipage balance changed")
    current_table_check = verify_revised_tables(revised, table_records) if all("output_blocks" in record for record in table_records) else None
    return revised, {"method": "Surgical table-block replacement; unchanged non-table segments compared byte for byte.",
                     "source_tex_sha256": sha256(tex), "revised_tex_sha256": sha256(revised),
                     "non_table_tex_unchanged": True, "non_table_segments_sha256": sha256("\0".join(untouched)),
                     "style": STYLE, "revised_table_verification": current_table_check, "tables": audits}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tex", required=True, type=Path)
    parser.add_argument("--transform-report", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path,
                        help="Explicit destination; the input TeX is never overwritten implicitly")
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--width-overrides", type=Path)
    args = parser.parse_args()
    records = json.loads(args.transform_report.read_text(encoding="utf-8"))["tables"]
    widths = json.loads(args.width_overrides.read_text(encoding="utf-8")) if args.width_overrides else None
    source = args.tex.read_bytes().decode("utf-8")
    revised, report = replace_table_blocks(source, records, width_overrides=widths)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(revised.encode("utf-8"))
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Rendered {sum(t['changed'] for t in report['tables'])} changed blocks; non-table TeX preserved.")


if __name__ == "__main__":
    main()
