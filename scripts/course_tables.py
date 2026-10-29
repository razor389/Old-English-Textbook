"""Lossless presentation transforms for the course's Markdown paradigm tables.

Canonical coverage matrices and linguistic registers are deliberately not edited.
Coordinates in the returned mappings are zero based: row 0 is the header, and
rows 1 onward are body rows. A document replacement always covers exactly one
original Markdown table; generated panels stay inside that replacement span.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


TABLE_RE = re.compile(r"(?:^\|[^\n]*(?:\n|$))+", re.MULTILINE)
SEPARATOR_RE = re.compile(r"^:?-+:?$")
PERSON_TOKEN = r"(?:[123](?:st|nd|rd)?|first|second|third)"
NUMBER_TOKEN = r"(?:sg\.?|singular|pl\.?|plural)"
PERSON_RE = re.compile(rf"^({PERSON_TOKEN})\s*,?\s*({NUMBER_TOKEN})(?::\s*(.*))?$", re.I)
PERSON_NUMBERS = {"first": "1", "second": "2", "third": "3", "1st": "1", "2nd": "2", "3rd": "3"}
PERSON_HEADERS = {"Person", "Person and number", "Person / number", "Person/number", "Indicative person and number"}
CASE_NAMES = {"n": "Nominative", "nom": "Nominative", "nominative": "Nominative",
              "g": "Genitive", "gen": "Genitive", "genitive": "Genitive",
              "d": "Dative", "dat": "Dative", "dative": "Dative",
              "a": "Accusative", "acc": "Accusative", "accusative": "Accusative"}
GENDERS = {"m": "Masculine", "masculine": "Masculine", "n": "Neuter",
           "neuter": "Neuter", "f": "Feminine", "feminine": "Feminine"}
GENDER_ORDER = {"Masculine": 0, "Neuter": 1, "Feminine": 2}
PLURAL = "1–3 pl."
SINGULAR = "1–3 sg."


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_tables(markdown: str) -> list[dict[str, Any]]:
    """Return actual pipe tables; prose and HTML comments are not consumed."""
    tables = []
    previous_end = 0
    for match in TABLE_RE.finditer(markdown):
        lines = match.group().splitlines()
        cells = [[c.strip() for c in line.strip().strip("|").split("|")] for line in lines]
        if len(cells) < 2 or not all(SEPARATOR_RE.fullmatch(c.replace(" ", "")) for c in cells[1]):
            continue
        if any(len(row) != len(cells[0]) for row in cells):
            raise ValueError(f"Nonrectangular table at line {markdown[:match.start()].count(chr(10)) + 1}")
        preceding = markdown[previous_end:match.start()]
        markers = re.findall(r"<!--\s*table:\s*(\S+)\s*-->", preceding)
        headings = re.findall(r"^#{1,6}\s+(.+)$", markdown[:match.start()], re.MULTILINE)
        tables.append({"original_index_zero_based": len(tables), "start": match.start(),
                       "end": match.end(), "line": markdown[:match.start()].count("\n") + 1,
                       "raw": match.group(), "headers": cells[0], "rows": cells[2:],
                       "marker": markers[-1] if markers else None,
                       "heading": headings[-1] if headings else None})
        previous_end = match.end()
    return tables


def render_markdown(headers: list[str], rows: list[list[str]]) -> str:
    matrix = [headers, ["---"] * len(headers), *rows]
    return "\n".join("| " + " | ".join(row) + " |" for row in matrix) + "\n"


def _cell(text: str, sources: list[tuple[int, int]], how: str = "label") -> dict[str, Any]:
    return {"text": text, "sources": [list(p) for p in sources], "how": how}


def _literal(original: list[list[str]], r: int, c: int) -> dict[str, Any]:
    return _cell(original[r][c], [(r, c)], "exact")


def _case(label: str) -> str:
    return CASE_NAMES.get(label.strip().rstrip(".").lower(), label)


def _person(label: str) -> str:
    shared = re.fullmatch(rf"({NUMBER_TOKEN}):\s*persons\s+(.+)", label, re.I)
    if shared and _all_persons(shared[2]):
        return SINGULAR if shared[1].lower().startswith("s") else PLURAL
    match = PERSON_RE.fullmatch(label)
    if match:
        person = PERSON_NUMBERS.get(match[1].lower(), match[1])
        text = person + (" sg." if match[2].lower().startswith("s") else " pl.")
        return text + (": " + match[3] if match[3] else "")
    shared = re.fullmatch(rf"(.+?)\s+({NUMBER_TOKEN})(?::\s*(.*))?", label, re.I)
    if shared and _all_persons(shared[1]):
        text = SINGULAR if shared[2].lower().startswith("s") else PLURAL
        return text + (": " + shared[3] if shared[3] else "")
    return label


def _all_persons(label: str) -> bool:
    """Recognize an explicit all-person list, without treating 1/3 as 1–3."""
    value = label.lower().strip()
    if value in {"all", "all persons", "all three persons"}:
        return True
    value = re.sub(rf"\b{PERSON_TOKEN}\b", lambda m: PERSON_NUMBERS.get(m[0], m[0]), value)
    return bool(re.fullmatch(r"1\s*[–-]\s*3", value)
                or re.fullmatch(r"1\s*[,/]\s*2\s*(?:,\s*(?:and\s+)?|/\s*|and\s+)3", value))


def _command_person(label: str) -> str | None:
    """Recognize complete second-person command labels; never infer other persons."""
    value = label.lower().strip()
    phrases = {"one person": "2 sg.", "one person addressed": "2 sg.",
               "two or more people": "2 pl.", "two or more people addressed": "2 pl.",
               "singular": "2 sg.", "plural": "2 pl.",
               "singular command": "2 sg.", "plural command": "2 pl."}
    if value in phrases:
        return phrases[value]
    value = re.sub(r"^imperative\s*,\s*", "", value)
    normalized = _person(value)
    if re.fullmatch(r"2 (?:sg|pl)\.(?::.*)?", normalized):
        return normalized
    return None


def _nominal_header(label: str) -> str:
    value = re.sub(r"\bsg\.?(?=\s|$)", "singular", label, flags=re.I)
    value = re.sub(r"\bpl\.?(?=\s|$)", "plural", value, flags=re.I)
    if re.match(r"^(?:masculine|neuter|feminine|common|singular|plural)\b", value, re.I):
        value = value[0].upper() + value[1:]
    return value


def _gender(label: str) -> tuple[str, str | None] | None:
    match = re.fullmatch(r"(Masculine|Neuter|Feminine|M|N|F)(?:\s+(singular|plural|sg\.?|pl\.?))?", label, re.I)
    if not match:
        return None
    number = match[2]
    if number:
        number = "singular" if number.lower().startswith("s") else "plural"
    return GENDERS[match[1].lower()], number


def _chunks(values: list[Any], size: int) -> list[list[Any]]:
    return [values[i:i + size] for i in range(0, len(values), size)]


def _block(cells: list[list[dict[str, Any]]], caption: str | None = None,
           caption_sources: list[tuple[int, int]] | None = None,
           caption_how: str = "exact") -> dict[str, Any]:
    return {"cells": cells, "caption": caption, "caption_sources": caption_sources or [],
            "caption_how": caption_how}


def _finish(original: list[list[str]], blocks: list[dict[str, Any]], kind: str,
            original_raw: str | None, context: dict[str, Any], literal_first_column: bool = False) -> dict[str, Any]:
    output = []
    mapping = {(r, c): {"source": [r, c], "original_value": value,
                        "role": "literal" if r > 0 and (c > 0 or literal_first_column)
                        and not (kind == "adjective_number_panels" and c == 1) else "label",
                        "targets": []}
               for r, row in enumerate(original) for c, value in enumerate(row)}
    for bi, block in enumerate(blocks):
        matrix = block["cells"]
        for ri, row in enumerate(matrix):
            for ci, cell in enumerate(row):
                for source in cell["sources"]:
                    target = {"block": bi, "row": ri, "column": ci, "how": cell["how"]}
                    old = original[source[0]][source[1]]
                    if cell["how"] == "exact" and cell["text"] != old:
                        # A transposed lemma is a literal component of its new header.
                        start = cell["text"].find(old)
                        if start < 0:
                            raise ValueError("Literal source absent from generated heading")
                        target["slice"] = [start, start + len(old)]
                    mapping[tuple(source)]["targets"].append(target)
        headers = [c["text"] for c in matrix[0]]
        rows = [[c["text"] for c in row] for row in matrix[1:]]
        caption = block.get("caption")
        for source in block.get("caption_sources", []):
            mapping[tuple(source)]["targets"].append({"block": bi, "caption": True,
                                                     "how": block.get("caption_how", "exact")})
        output.append({"headers": headers, "rows": rows, "caption": caption,
                       "caption_markdown": f"**{caption}**" if caption else None,
                       "raw": render_markdown(headers, rows),
                       "cell_origins": [[{"sources": c["sources"], "how": c["how"]} for c in row] for row in matrix]})
    # Labels of a transposed axis can become the layout itself (e.g. 'Verb').
    # Explicitly record that re-encoding; it is never allowed for a form cell.
    for item in mapping.values():
        if not item["targets"] and item["role"] == "label":
            item["targets"].append({"block": 0, "row": 0, "column": 0,
                                    "how": "axis_context", "reason": kind})
    original_raw = original_raw if original_raw is not None else render_markdown(original[0], original[1:])
    semantic_change = len(output) != 1 or output[0]["headers"] != original[0] or output[0]["rows"] != original[1:] or output[0]["caption"]
    revised = "\n".join((b["caption_markdown"] + "\n\n" if b["caption_markdown"] else "") + b["raw"] for b in output)
    if not semantic_change:
        revised = original_raw
        output[0]["raw"] = original_raw
    elif not original_raw.endswith("\n"):
        revised = revised.rstrip("\n")
    result = {**context, "coordinate_convention": "zero-based matrix coordinates; header row is 0",
              "kind": kind, "changed": revised != original_raw,
              "original": original_raw, "raw": original_raw, "revised": revised,
              "original_headers": original[0], "original_rows": original[1:],
              "output_blocks": output, "mapping": list(mapping.values()),
              "original_sha256": digest(original_raw), "revised_sha256": digest(revised)}
    errors = validate_transform(result)
    if errors:
        raise ValueError("; ".join(errors[:8]))
    return result


def transform_table(headers: list[str], rows: list[list[str]], *,
                    context: dict[str, Any] | None = None, original_raw: str | None = None) -> dict[str, Any]:
    """Transform one actual table without touching neighboring prose or comments."""
    context = context or {}
    original = [list(headers), *[list(r) for r in rows]]
    h = original[0]
    cells = [[_literal(original, r, c) for c in range(len(h))] for r in range(len(original))]
    kind = "unchanged"

    # Full pronoun and adjective declensions sometimes have cases as columns.
    case_columns = {_case(label): c for c, label in enumerate(h[1:], 1)}
    if len(h) == 5 and set(case_columns) == {"Nominative", "Genitive", "Dative", "Accusative"}:
        if h[0] == "Person and number":
            blocks = []
            for person, caption in [("1", "First person"), ("2", "Second person"), ("3", "Third person")]:
                group = [r for r in range(1, len(original)) if original[r][0].startswith(person + " ")]
                if not group:
                    continue
                new = [[_cell("Case", [(0, 0)])]]
                for r in group:
                    label = original[r][0][2:]
                    new[0].append(_cell(label[0].upper() + label[1:], [(r, 0)]))
                for case in ["Nominative", "Genitive", "Dative", "Accusative"]:
                    c = case_columns[case]
                    new.append([_cell(case, [(0, c)]), *[_literal(original, r, c) for r in group]])
                blocks.append(_block(new, caption))
            return _finish(original, blocks, "pronoun_case_rows", original_raw, context)
        if h[0] == "Gender and number":
            identities = {r: _gender(original[r][0]) for r in range(1, len(original))}
            if not all(identities.values()):
                raise ValueError("Unknown complete-declension gender/number label")
            blocks = []
            for number in ["singular", "plural"]:
                group = [r for r, value in identities.items() if value[1] == number]
                if not group:
                    continue
                group.sort(key=lambda r: GENDER_ORDER[identities[r][0]])
                new = [[_cell("Case", [(0, 0)]), *[_cell(identities[r][0] + " " + number, [(r, 0)]) for r in group]]]
                for case in ["Nominative", "Genitive", "Dative", "Accusative"]:
                    c = case_columns[case]
                    new.append([_cell(case, [(0, c)]), *[_literal(original, r, c) for r in group]])
                blocks.append(_block(new))
            return _finish(original, blocks, "complete_key_declension_case_rows", original_raw, context)

    # Already compact multi-lemma weak indicatives: two lemmas per narrow panel.
    paired = h == ["Verb", "Present 1 sg.", "2 sg.", "3 sg.", "All pl.", "Preterite 1/3 sg.", "2 sg.", "All pl."]
    subj = h == ["Lemma", "Present all singular", "Present all plural", "Preterite all singular", "Preterite all plural"]
    subj = subj or (h == ["Verb", "Present singular", "Present plural", "Preterite singular", "Preterite plural"]
                    and "subjunctive" in str(context.get("heading", "")).lower())
    if paired or subj:
        blocks = []
        labels = ["1 sg.", "2 sg.", "3 sg.", PLURAL] if paired else [SINGULAR, PLURAL]
        columns = [(1, 5), (2, 6), (3, 5), (4, 7)] if paired else [(1, 3), (2, 4)]
        for group in _chunks(list(range(1, len(original))), 2):
            new = [[_cell("Person and number", [(0, 0)])]]
            for r in group:
                for tense in ["Present", "Preterite"]:
                    if len(group) == 1:
                        col = 1 if tense == "Present" else (5 if paired else 3)
                        new[0].append(_cell(tense, [(0, col)]))
                    else:
                        new[0].append(_cell(original[r][0] + " · " + tense, [(r, 0)], "exact"))
            for label, pair in zip(labels, columns):
                outrow = [_cell(label, [(0, pair[0]), (0, pair[1])])]
                for r in group:
                    outrow.extend(_literal(original, r, c) for c in pair)
                new.append(outrow)
            blocks.append(_block(new, original[group[0]][0] if len(group) == 1 else None,
                                 [(group[0], 0)] if len(group) == 1 else None))
        return _finish(original, blocks, "paired_lemma_subjunctives" if subj else "paired_lemma_indicatives",
                       original_raw, context, literal_first_column=True)

    # Preserve separately taught tenses: transpose inside the existing block only.
    if h[0] in {"Verb", "Verb label"} and h[1:] == ["1 sg.", "2 sg.", "3 sg.", PLURAL]:
        blocks = []
        for group in _chunks(list(range(1, len(original))), 4):
            new = [[_cell("Person and number", [(0, 0)]), *[_literal(original, r, 0) for r in group]]]
            for c in range(1, 5):
                new.append([_cell(h[c], [(0, c)]), *[_literal(original, r, c) for r in group]])
            blocks.append(_block(new))
        return _finish(original, blocks, "single_tense_comparison_transpose", original_raw, context, True)

    # Complete imperative comparisons keep only the two assigned second persons.
    command_context = "command" in str(context.get("heading", "")).lower() or "imperative" in str(context.get("heading", "")).lower() or "IMP" in str(context.get("marker", ""))
    command_columns = h == ["Verb", "Singular command", "Plural command"] or (h == ["Verb", "Singular", "Plural"] and command_context)
    command_columns = command_columns or (len(h) == 3 and h[0] == "Verb"
                                           and [_command_person(v).split(":", 1)[0] if _command_person(v) else None
                                                for v in h[1:]] == ["2 sg.", "2 pl."]
                                           and any("addressee" in v.lower() for v in h[1:]))
    if command_columns:
        blocks = []
        for group in _chunks(list(range(1, len(original))), 4):
            new = [[_cell("Person and number", [(0, 0)]), *[_literal(original, r, 0) for r in group]]]
            for c, label in [(1, _command_person(h[1])), (2, _command_person(h[2]))]:
                new.append([_cell(label, [(0, c)]), *[_literal(original, r, c) for r in group]])
            blocks.append(_block(new))
        return _finish(original, blocks, "command_comparison_person_rows", original_raw, context, True)
    if h == ["Singular", "Plural"] and len(rows) == 1 and command_context:
        new = [[_cell("Person and number", [(0, 0), (0, 1)]), _cell("Command", [(0, 0), (0, 1)])],
               [_cell("2 sg.", [(0, 0)]), _literal(original, 1, 0)],
               [_cell("2 pl.", [(0, 1)]), _literal(original, 1, 1)]]
        return _finish(original, [_block(new)], "command_pair_person_rows", original_raw, context, True)
    if len(h) == 2 and (h[-1] in {"Command", "Imperative"} or command_context
                        or "command" in h[0].lower()
                        or all(re.search(r"\b(?:command|imperative)\b", row[0], re.I) for row in rows)):
        mapped = [_command_person(row[0]) for row in rows]
        if len(mapped) == 2 and set(mapped) == {"2 sg.", "2 pl."}:
            cells[0][0] = _cell("Person and number", [(0, 0)])
            for r, label in enumerate(mapped, 1):
                cells[r][0] = _cell(label, [(r, 0)])
            if h[1] not in {"Command", "Imperative"}:
                mood = "Imperative" if any("imperative" in row[0].lower() for row in rows) else "Command"
                cells[0][1] = _cell(mood, [(0, 1), (0, 0), *[(r, 0) for r in range(1, len(original))]])
            caption = h[0].split(":", 1)[0] if ":" in h[0] and "command" in h[0].lower() else None
            block = _block(cells, caption, [(0, 0)] if caption else None, "label")
            return _finish(original, [block], "command_person_labels", original_raw, context)

    # A compact subjunctive table with tenses as rows becomes number rows.
    if h == ["Tense", "All persons singular", "All persons plural"]:
        new = [[_cell("Person and number", [(0, 0)]),
                *[_cell(original[r][0].capitalize(), [(r, 0)]) for r in range(1, len(original))]]]
        for c, label in [(1, SINGULAR), (2, PLURAL)]:
            new.append([_cell(label, [(0, c)]), *[_literal(original, r, c) for r in range(1, len(original))]])
        return _finish(original, [_block(new)], "subjunctive_number_rows", original_raw, context)
    if h == ["Present all singular", "Present all plural"] and len(rows) == 1:
        new = [[_cell("Person and number", [(0, 0), (0, 1)]), _cell("Present", [(0, 0), (0, 1)])],
               [_cell(SINGULAR, [(0, 0)]), _literal(original, 1, 0)],
               [_cell(PLURAL, [(0, 1)]), _literal(original, 1, 1)]]
        return _finish(original, [_block(new)], "present_subjunctive_number_rows", original_raw, context, True)
    if len(h) == 3 and h[0] == "Series" and [_person(v) for v in h[1:]] == [SINGULAR, PLURAL]:
        new = [[_cell("Person and number", [(0, 0)]),
                *[_literal(original, r, 0) for r in range(1, len(original))]]]
        for c, label in [(1, SINGULAR), (2, PLURAL)]:
            new.append([_cell(label, [(0, c)]),
                        *[_literal(original, r, c) for r in range(1, len(original))]])
        return _finish(original, [_block(new)], "subjunctive_series_person_rows", original_raw, context, True)
    if h[0].lower().endswith("subjunctive number") and h[1:] == ["Present", "Preterite"]:
        labels = [_person(row[0]) for row in rows]
        if labels == [SINGULAR, PLURAL]:
            cells[0][0] = _cell("Person and number", [(0, 0)])
            for c in [1, 2]:
                cells[0][c] = _cell(h[c] + " subjunctive", [(0, c), (0, 0)])
            for r, label in enumerate(labels, 1):
                cells[r][0] = _cell(label, [(r, 0)])
            caption = h[0].split(":", 1)[0] if ":" in h[0] else None
            block = _block(cells, caption, [(0, 0)] if caption else None, "label")
            return _finish(original, [block], "subjunctive_key_person_labels", original_raw, context)

    # Early noun comparisons: four case rows, paired number columns per lemma.
    if h[0] == "Case and number":
        index = {}
        for r in range(1, len(original)):
            match = re.fullmatch(r"(N|G|D|A) (singular|plural)", original[r][0])
            if not match:
                raise ValueError("Unrecognized noun case/number row")
            index[(_case(match[1]), match[2])] = r
        if set(index) != {(case, number) for case in CASE_NAMES.values() for number in ["singular", "plural"]}:
            raise ValueError("Incomplete noun case/number grid")
        blocks = []
        for group in _chunks(list(range(1, len(h))), 2):
            new = [[_cell("Case", [(0, 0)])]]
            for c in group:
                for number in ["singular", "plural"]:
                    new[0].append(_cell((number.title() if len(group) == 1 else h[c] + " " + number), [(0, c)]))
            for case in ["Nominative", "Genitive", "Dative", "Accusative"]:
                newrow = [_cell(case, [(index[(case, number)], 0) for number in ["singular", "plural"]])]
                for c in group:
                    newrow.extend(_literal(original, index[(case, number)], c) for number in ["singular", "plural"])
                new.append(newrow)
            # A lone lemma's identity must remain explicit after its header moves.
            blocks.append(_block(new, h[group[0]] if len(group) == 1 else None,
                                 [(0, group[0])] if len(group) == 1 else None))
        return _finish(original, blocks, "noun_number_columns", original_raw, context)

    # Unit 3 Number/Case grids become the same two panels as later adjectives.
    if h[:2] == ["Number", "Case"] and set(h[2:]) == {"Masculine", "Neuter", "Feminine"}:
        blocks = []
        for number in ["Singular", "Plural"]:
            selected = [r for r in range(1, len(original)) if original[r][0].split(":", 1)[0] == number]
            if len(selected) != 4:
                raise ValueError("Unexpected adjective Number/Case rows")
            number_labels = {original[r][0] for r in selected}
            if len(number_labels) != 1:
                raise ValueError("Mixed adjective number scopes")
            number_label = next(iter(number_labels))
            order = sorted(range(2, len(h)), key=lambda c: GENDER_ORDER[h[c]])
            new = [[_cell("Case", [(0, 0), (0, 1)]), *[_cell(h[c] + " " + number_label.lower(), [(0, c), *[(r, 0) for r in selected]]) for c in order]]]
            for r in selected:
                new.append([_cell(_case(original[r][1]), [(r, 1)]), *[_literal(original, r, c) for c in order]])
            blocks.append(_block(new))
        result = _finish(original, blocks, "adjective_number_panels", original_raw, context)
        # The old Number column is an axis, not a lexical form column.
        return result

    for c, value in enumerate(h):
        if "all persons pl." in value:
            cells[0][c] = _cell(value.replace("all persons pl.", PLURAL), [(0, c)])
            kind = "shared_person_header_alias"

    # These subjects are part of Unit 2's explicitly requested complete paradigm.
    # Keep every original pronoun string as an exact literal inside its label.
    pronoun_labels = ["ic", "ðū", "hē / hēo / hit", "wē / gē / hīe"]
    if h == ["Person", "Present", "Preterite"] and [row[0] for row in rows] == pronoun_labels:
        cells[0][0] = _cell("Person and number", [(0, 0)])
        for r, label in enumerate(["1 sg.", "2 sg.", "3 sg.", PLURAL], 1):
            cells[r][0] = _cell(label + ": " + original[r][0], [(r, 0)], "exact")
        return _finish(original, [_block(cells)], "pronoun_subject_person_labels", original_raw, context, True)

    is_person = h[0] in PERSON_HEADERS and not any(x in h for x in ["Nominative", "Genitive", "Dative", "Accusative"])
    if is_person:
        cells[0][0] = _cell("Person and number", [(0, 0)])
        if h[0] == "Indicative person and number":
            for c in range(1, len(h)):
                cells[0][c] = _cell(h[c] + " indicative", [(0, c), (0, 0)])
        for r in range(1, len(cells)):
            cells[r][0] = _cell(_person(original[r][0]), [(r, 0)])
        plural = []
        for r in range(1, len(original)):
            match = PERSON_RE.fullmatch(_person(original[r][0]))
            if match and match[2].lower().startswith("pl"):
                plural.append((int(match[1]), r, match[3]))
        blank_grid = any(re.search(r"\(\d+\)\s*_", value) for row in rows for value in row)
        if len(plural) == 3 and [p[0] for p in plural] == [1, 2, 3] and not blank_grid:
            indices = [p[1] for p in plural]
            if all(original[r][1:] == original[indices[0]][1:] for r in indices):
                label = PLURAL
                if any(p[2] for p in plural):
                    label += ": " + ", ".join(p[2] for p in plural if p[2])
                merged = [_cell(label, [(r, 0) for r in indices])]
                merged.extend(_cell(original[indices[0]][c], [(r, c) for r in indices], "exact") for c in range(1, len(h)))
                cells = [row for ri, row in enumerate(cells) if ri not in indices[1:]]
                cells[indices[0]] = merged
                kind = "identical_plural_rows"
            else:
                kind = "protected_distinct_person_values"
        elif blank_grid:
            kind = "protected_numbered_response_grid"
        else:
            kind = "person_labels"

    # Compact already-bounded subjunctives retain their all-person scope.
    if h[0] == "Number (all three persons)":
        cells[0][0] = _cell("Person and number", [(0, 0)])
        for r in range(1, len(cells)):
            label = _person(original[r][0])
            if label in {"Singular", "Plural"}:
                label = SINGULAR if label == "Singular" else PLURAL
            if label in {SINGULAR, PLURAL}:
                cells[r][0] = _cell(label, [(r, 0)])
        kind = "subjunctive_person_labels"

    if h[0] in {"Case", "Series / case"}:
        for c, value in enumerate(h[1:], 1):
            normalized = _nominal_header(value)
            if normalized != value:
                cells[0][c] = _cell(normalized, [(0, c)])
                kind = "nominal_header_labels"
        for r in range(1, len(cells)):
            cells[r][0] = _cell(_case(original[r][0]), [(r, 0)])
        # Sort complete NGDA groups only; retain other bounded/reference rows.
        rank = {case: i for i, case in enumerate(["Nominative", "Genitive", "Dative", "Accusative"])}
        for prefix in ["", "Strong ", "Weak "]:
            group = [r for r in range(1, len(cells)) if cells[r][0]["text"].startswith(prefix)
                     and cells[r][0]["text"][len(prefix):].title() in rank]
            if len(group) == 4 and {cells[r][0]["text"][len(prefix):].title() for r in group} == set(rank):
                ordered = sorted((cells[r] for r in group), key=lambda row: rank[row[0]["text"][len(prefix):].title()])
                for r, row in zip(group, ordered):
                    cells[r] = row
        genders = [_gender(v) for v in h[1:]]
        if genders and all(genders):
            # Separate number panels for genuinely six-column gender/number grids.
            if len(genders) == 6 and {n for _, n in genders} == {"singular", "plural"}:
                blocks = []
                for number in ["singular", "plural"]:
                    cols = [c for c in range(1, len(h)) if genders[c - 1][1] == number]
                    if len(cols) != 3 or {genders[c - 1][0] for c in cols} != set(GENDER_ORDER):
                        raise ValueError("Incomplete gender/number panel")
                    cols.sort(key=lambda c: GENDER_ORDER[genders[c - 1][0]])
                    panel = [[cells[0][0], *[_cell(genders[c - 1][0] + " " + number, [(0, c)]) for c in cols]]]
                    panel.extend([[row[0], *[row[c] for c in cols]] for row in cells[1:]])
                    blocks.append(_block(panel))
                return _finish(original, blocks, "gender_number_panels", original_raw, context)
            order = sorted(range(1, len(h)), key=lambda c: (genders[c - 1][1] or "", GENDER_ORDER[genders[c - 1][0]]))
            for c, (gender, number) in enumerate(genders, 1):
                cells[0][c] = _cell(gender + (" " + number if number else ""), [(0, c)])
            cells = [[row[0], *[row[c] for c in order]] for row in cells]
            kind = "gender_order_and_case_labels"
        elif kind == "unchanged":
            kind = "case_labels"
    return _finish(original, [_block(cells)], kind, original_raw, context)


def _target_value(record: dict[str, Any], target: dict[str, Any]) -> str:
    block = record["output_blocks"][target["block"]]
    value = block["caption"] if target.get("caption") else ([block["headers"], *block["rows"]])[target["row"]][target["column"]]
    if "slice" in target:
        value = value[target["slice"][0]:target["slice"][1]]
    return value


def _label_axes(text: str, *, header: bool) -> dict[str, set[str]]:
    """Read grammatical labels independently of any transform's cell ordering."""
    value = text.lower().strip()
    axes = {}
    number = re.search(r"\b(singular|plural|dual|sg\.?|pl\.?)\b", value)
    if number:
        axes["number"] = {"du" if number[1] == "dual" else "sg" if number[1].startswith("s") else "pl"}
    person_value = _person(value)
    person_value = re.sub(rf"\b{PERSON_TOKEN}\b", lambda m: PERSON_NUMBERS.get(m[0], m[0]), person_value)
    persons = re.search(r"\b((?:[123]\s*[,/–-]\s*)*[123])\s*,?\s+(singular|plural|sg\.?|pl\.?)", person_value)
    if persons:
        digits = set(re.findall(r"[123]", persons[1]))
        if re.search(r"1\s*[–-]\s*3", persons[1]):
            digits.add("2")
        axes["persons"] = digits
    elif re.search(r"all (?:(?:three )?persons )?(?:singular|plural|sg|pl)", value):
        axes["persons"] = {"1", "2", "3"}
    else:
        named_person = re.search(r"\b([123])[- ]person\b", person_value)
        if named_person:
            axes["persons"] = {named_person[1]}
    if value in {"one person", "one person addressed", "two or more people", "two or more people addressed"}:
        axes["persons"] = {"2"}
        axes["number"] = {"sg" if value.startswith("one") else "pl"}
    gender = re.match(r"^(masculine|neuter|feminine)(?:\b|$)", value)
    if header and not gender:
        gender = re.match(r"^(m|n|f)(?:\b|$)", value)
    if gender:
        axes["gender"] = {GENDERS[gender[1]]}
    if not header or re.match(r"^(nominative|genitive|dative|accusative)(?:\b|$)", value):
        case = re.match(r"^(?:(strong|weak) )?(nominative|genitive|dative|accusative|nom\.?|gen\.?|dat\.?|acc\.?|n|g|d|a)(?:\s|$)", value)
        if case:
            axes["case"] = {_case(case[2])}
            if case[1]:
                axes["declension"] = {case[1]}
    if "present" in value:
        axes["tense"] = {"present"}
    elif "preterite" in value:
        axes["tense"] = {"preterite"}
    if "reference only" in value:
        axes["scope"] = {"reference_only"}
    if "subjunctive" in value:
        axes["mood"] = {"subjunctive"}
    elif "indicative" in value:
        axes["mood"] = {"indicative"}
    elif "imperative" in value or "command" in value:
        axes["mood"] = {"imperative"}
    return axes


def validate_transform(record: dict[str, Any]) -> list[str]:
    """Check coverage and literal equality against the actual generated cells."""
    errors = []
    original = [record["original_headers"], *record["original_rows"]]
    expected = {(r, c) for r, row in enumerate(original) for c in range(len(row))}
    actual = [tuple(m["source"]) for m in record["mapping"]]
    if set(actual) != expected or len(actual) != len(expected):
        errors.append("Source coordinate coverage is incomplete or repeated")
    for item in record["mapping"]:
        r, c = item["source"]
        if item["original_value"] != original[r][c]:
            errors.append(f"Source value differs at {r},{c}")
        exact = [t for t in item["targets"] if t["how"] == "exact"]
        if item["role"] == "literal" and not exact:
            errors.append(f"Unmapped literal cell {r},{c}")
        if not item["targets"]:
            errors.append(f"Unmapped source coordinate {r},{c}")
        for target in exact:
            if _target_value(record, target) != item["original_value"]:
                errors.append(f"Changed literal cell {r},{c}")
        if item["role"] == "label":
            source_axes = _label_axes(item["original_value"], header=r == 0)
            target_unions: dict[str, set[str]] = {}
            for target in item["targets"]:
                if target["how"] != "label" or target.get("caption"):
                    continue
                target_axes = _label_axes(_target_value(record, target), header=target["row"] == 0)
                for axis, values in target_axes.items():
                    target_unions.setdefault(axis, set()).update(values)
                for axis in set(source_axes) & set(target_axes):
                    if not source_axes[axis] & target_axes[axis]:
                        errors.append(f"Changed {axis} association at source {r},{c}")
            for axis in set(source_axes) & set(target_unions):
                if not source_axes[axis] <= target_unions[axis]:
                    errors.append(f"Narrowed {axis} scope at source {r},{c}")
    for bi, block in enumerate(record["output_blocks"]):
        matrix = [block["headers"], *block["rows"]]
        if any(len(row) != len(matrix[0]) for row in matrix):
            errors.append(f"Nonrectangular output panel {bi}")
        parsed = parse_tables(block["raw"])
        if len(parsed) != 1 or parsed[0]["headers"] != block["headers"] or parsed[0]["rows"] != block["rows"]:
            errors.append(f"Rendered output panel differs {bi}")
        if len(matrix) != len(block["cell_origins"]) or any(len(a) != len(b) for a, b in zip(matrix, block["cell_origins"])):
            errors.append(f"Output coordinate provenance is incomplete {bi}")
        for ri, row in enumerate(block["cell_origins"]):
            for ci, origin in enumerate(row):
                if not origin["sources"]:
                    errors.append(f"Unsourced output cell {bi},{ri},{ci}")
                for source in origin["sources"]:
                    owners = [m for m in record["mapping"] if m["source"] == source]
                    if len(owners) != 1 or not any(t.get("row") == ri and t.get("column") == ci
                                                 and t["block"] == bi and t["how"] == origin["how"]
                                                 for t in owners[0]["targets"]):
                        errors.append(f"Output provenance lacks reverse mapping {bi},{ri},{ci}")
    # Exact reversibility includes references carried by a number-axis label.
    for item in record["mapping"]:
        if "reference only" in item["original_value"].lower():
            if not any("reference only" in _target_value(record, target).lower() for target in item["targets"]):
                errors.append("Reference-only scope disappeared from the displayed labels")
    return errors


def reconstruct_original(record: dict[str, Any]) -> tuple[list[str], list[list[str]]]:
    """Recover original literal cells from the output; axis labels from the map."""
    errors = validate_transform(record)
    if errors:
        raise ValueError("; ".join(errors))
    matrix = [[None for _ in row] for row in [record["original_headers"], *record["original_rows"]]]
    for item in record["mapping"]:
        exact = next((t for t in item["targets"] if t["how"] == "exact"), None)
        value = _target_value(record, exact) if exact else item["original_value"]
        r, c = item["source"]
        matrix[r][c] = value
    return matrix[0], matrix[1:]


def transform_document(markdown: str, *, chapter: int | None = None,
                       kind: str = "student") -> tuple[str, dict[str, Any]]:
    """Return revised Markdown and a lossless audit; never write any master."""
    tables = parse_tables(markdown)
    parts, untouched, records = [], [], []
    cursor = 0
    revised_cursor = 0
    for table in tables:
        between = markdown[cursor:table["start"]]
        parts.append(between)
        untouched.append(between)
        revised_cursor += len(between)
        context = {k: table[k] for k in ["original_index_zero_based", "start", "end", "line", "marker", "heading"]}
        record = transform_table(table["headers"], table["rows"], original_raw=table["raw"], context=context)
        record["revised_start"] = revised_cursor
        revised_cursor += len(record["revised"])
        record["revised_end"] = revised_cursor
        parts.append(record["revised"])
        records.append(record)
        cursor = table["end"]
    parts.append(markdown[cursor:])
    untouched.append(markdown[cursor:])
    revised = "".join(parts)
    report = {"chapter": chapter, "document_kind": kind,
              "original_sha256_normalized_lf": digest(markdown), "revised_sha256_normalized_lf": digest(revised),
              "outside_tables_sha256": digest("".join(untouched)), "table_count": len(records),
              "changed_table_count": sum(r["changed"] for r in records),
              "output_table_count": sum(len(r["output_blocks"]) for r in records),
              "tables": records}
    return revised, report


def _negative_probes(documents: list[dict[str, Any]]) -> list[str]:
    """Show that validation rejects errors which the real revision must catch."""
    records = [t for d in documents for t in d["tables"]]
    finite = next(t for t in records if t["kind"] == "identical_plural_rows")
    negative = copy.deepcopy(finite)
    negative["output_blocks"][0]["rows"][0][1] += "x"
    block = negative["output_blocks"][0]
    block["raw"] = render_markdown(block["headers"], block["rows"])
    assert any("Changed literal cell" in e for e in validate_transform(negative))
    negative = copy.deepcopy(finite)
    negative["output_blocks"][0]["rows"][-1][0] = "1–3 sg."
    block = negative["output_blocks"][0]
    block["raw"] = render_markdown(block["headers"], block["rows"])
    assert any("Changed number association" in e for e in validate_transform(negative))
    gender = next(t for t in records if t["kind"] == "gender_number_panels")
    negative = copy.deepcopy(gender)
    block = negative["output_blocks"][0]
    block["headers"][1], block["headers"][2] = block["headers"][2], block["headers"][1]
    block["raw"] = render_markdown(block["headers"], block["rows"])
    assert any("Changed gender association" in e for e in validate_transform(negative))
    scoped = next(t for t in records if t["kind"] == "adjective_number_panels"
                  and any("reference only" in str(r) for r in t["original_rows"]))
    negative = copy.deepcopy(scoped)
    block = negative["output_blocks"][1]
    block["headers"] = [v.replace(": reference only", "") for v in block["headers"]]
    block["raw"] = render_markdown(block["headers"], block["rows"])
    assert any("Reference-only scope disappeared" in e for e in validate_transform(negative))
    negative = copy.deepcopy(finite)
    negative["mapping"].pop()
    assert any("Source coordinate coverage" in e for e in validate_transform(negative))
    return ["changed form rejected", "plural-to-singular mislabel rejected",
            "wrong gender heading rejected", "lost reference-only scope rejected", "missing coordinate rejected"]


def orientation_prose_suggestions(root: Path) -> list[dict[str, Any]]:
    """Bounded wording proposals for the coordinator; this module applies none."""
    replacements = [
        (2, "Every table gives the complete singular and plural present and preterite indicative. **1/3 sg.** means both first and third singular; **all pl.** means first, second and third plural. The plural column also supplies the form for dual subjects. Thus seven displayed forms account for all twelve person–number–tense cells.",
         "Every paradigm gives the complete singular and plural present and preterite indicative. **1–3 pl.** includes first, second and third plural; the shared plural row also supplies the form for dual subjects. In principal-part citations, **1/3 sg.** means both first and third singular. All twelve person–number–tense combinations remain explicit."),
        (2, "Our present row retains", "The selected present paradigm retains"),
        (2, "the selected row is not a rule", "the selected paradigm is not a rule"),
        (2, "learn each complete row.", "learn each complete paradigm."),
        (2, "Some complete rows here combine", "Some complete paradigms here combine"),
        (3, "Use the two gōd tables with this map.", "Use the strong and weak gōd panels with this map."),
        (4, "A column labelled **1–3 pl.**", "A row labelled **1–3 pl.**"),
        (6, "Each pair of rows supplies all twelve present/preterite cells.", "For each verb, the present and preterite tables give all twelve person–number–tense cells."),
        (6, "Keep the stem printed in each row.", "Keep each verb’s printed stem."),
        (6, "The compact tables expand combined plural rows into their explicitly stated person assignments and apply the given endings to the selected stems.", "The compact tables explicitly identify the three persons covered by each shared plural row and apply the given endings to the selected stems."),
        (7, "A column headed **all singular** or **all plural** includes all three persons.", "A row headed **1–3 sg.** or **1–3 pl.** includes all three persons."),
        (7, "Thus one four-cell row below gives all twelve person–number–tense combinations.", "Thus four displayed forms for each verb give all twelve person–number–tense combinations."),
        (7, "The named rows define this unit’s complete subjunctive assignment.", "The named verbs define this unit’s complete subjunctive assignment."),
        (7, "The first three rows are class II:", "The first three verbs are class II:"),
        (7, "Hāten is present plural subjunctive in its finite row;", "Hāten is present plural subjunctive in its finite paradigm;"),
        (7, "**Alternative present of “be”.** Each column again covers all three persons.", "**Alternative present of “be”.** Each row again covers all three persons."),
        (7, "Their presence in the first column does not supply", "Their presence in the table headings does not supply"),
        (7, "Wyrcean’s full subjunctive row appears with weak class I in §2. The remaining new verbs follow these rows. As before, every singular and plural column includes all three persons.",
         "Wyrcean’s full subjunctive paradigm appears with weak class I in §2. The remaining new verbs follow in these tables. As before, each shared singular or plural row includes all three persons."),
        (8, "A row labelled “persons 1, 2, 3” includes every person in that number.", "A row labelled **1–3 sg.** or **1–3 pl.** includes every person in that number."),
        (14, "A plural form is repeated for each person to make the complete system explicit.", "A shared **1–3 pl.** row gives the common form for all three plural persons."),
        (17, "The columns are masculine, neuter and feminine, first singular and then plural.", "Each panel has masculine, neuter and feminine columns; the singular panel precedes the plural panel."),
    ]
    suggestions = []
    for chapter, old, new in replacements:
        path = root / f"chapters/ch{chapter:02}/student.md"
        text = path.read_text(encoding="utf-8")
        suggestions.append({"path": path.relative_to(root).as_posix(), "old": old, "new": new,
                            "old_occurrences": text.count(old), "new_occurrences": text.count(new),
                            "action": "coordinator proposal only; do not alter exercise prompts"})
    return suggestions


def main() -> None:
    parser = argparse.ArgumentParser(description="Dry-run lossless paradigm presentation transforms; does not edit masters.")
    parser.add_argument("--audit", action="store_true", help="check all 36 active learner/key masters")
    args = parser.parse_args()
    if not args.audit:
        parser.error("Use --audit; the public Python API returns transformations without writing masters.")
    root = Path(__file__).resolve().parents[1]
    documents = []
    changes = Counter()
    for chapter in range(1, 19):
        for stem in ["student", "answer-key"]:
            path = root / f"chapters/ch{chapter:02}/{stem}.md"
            original = path.read_text(encoding="utf-8")
            revised, report = transform_document(original, chapter=chapter, kind=stem)
            second, second_report = transform_document(revised, chapter=chapter, kind=stem)
            if second != revised or second_report["changed_table_count"]:
                raise AssertionError(f"Not idempotent: {path}")
            for record in report["tables"]:
                if reconstruct_original(record) != (record["original_headers"], record["original_rows"]):
                    raise AssertionError(f"Failed inverse mapping: {path}")
                if record["changed"]:
                    changes[record["kind"]] += 1
            # All original characters outside table replacements must survive.
            parts = []
            cursor = 0
            for record in report["tables"]:
                assert revised[record["revised_start"]:record["revised_end"]] == record["revised"]
                parts.extend([revised[cursor:record["revised_start"]], record["original"]])
                cursor = record["revised_end"]
            parts.append(revised[cursor:])
            assert "".join(parts) == original
            documents.append({"path": path.relative_to(root).as_posix(), **report})
    result = {"status": "pass", "mode": "dry_run_only", "documents": documents,
              "counts": {"documents": len(documents), "original_tables": sum(d["table_count"] for d in documents),
                         "changed_tables": sum(d["changed_table_count"] for d in documents),
                         "output_tables": sum(d["output_table_count"] for d in documents)},
              "changed_kinds": dict(changes),
              "checks": ["exact literal coordinate coverage", "inverse cell reconstruction", "all-document idempotence", "outside-table preservation"],
              "negative_checks": _negative_probes(documents),
              "orientation_prose_suggestions": orientation_prose_suggestions(root)}
    folder = root / "build/style-audit"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "row-implementation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    summary = ["# Table transform dry run", "", "All 36 masters passed exact-cell mapping, inverse reconstruction and idempotence. No masters were written.", "",
               "```json", json.dumps({"counts": result["counts"], "changed_kinds": result["changed_kinds"]}, indent=2), "```", "",
               "The JSON contains every original/revised block, output panel and reversible coordinate map.", "",
               "## Bounded prose follow-up", "", "The JSON gives exact, unapplied wording proposals for Units 2–4, 6–8, 14 and 17. Preserve task instructions requesting all six logical positions: compact display does not change the requested answers.", "",
               "Unit 2's pronouns retain all ten distinct person/number/gender columns across three person panels, including both duals. Six Unit 3 full key declensions also use four case rows. Complete imperative pairs use only 2 sg./2 pl.; no first- or third-person commands are inferred.", "",
               "The six mixed command/infinitive reference tables in Unit 6 retain their mixed axes. Principal-part, nonfinite citation, lexical diagnostic and partial task tables retain their original scope and axes. Every inspected simple four-case row table already followed NGDA; complete case groups are normalized to that order without moving extra reference rows.", ""]
    (folder / "row-implementation.md").write_text("\n".join(summary), encoding="utf-8", newline="\n")
    print(json.dumps({"status": "pass", "counts": result["counts"], "changed_kinds": result["changed_kinds"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
