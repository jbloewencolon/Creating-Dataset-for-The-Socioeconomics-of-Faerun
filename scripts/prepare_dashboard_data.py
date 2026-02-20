#!/usr/bin/env python3
"""Prepare dashboard-ready CSV extracts from Faerûn source data (.xlsx or .csv).

No third-party dependencies required.
"""

from __future__ import annotations

import argparse
import ast
import csv
import json
import re
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET

NS = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def _col_to_idx(ref: str) -> int:
    m = re.match(r"([A-Z]+)(\d+)", ref)
    if not m:
        raise ValueError(f"Invalid cell ref: {ref}")
    letters = m.group(1)
    col = 0
    for ch in letters:
        col = col * 26 + (ord(ch) - 64)
    return col - 1


def parse_xlsx(path: Path) -> tuple[list[str], list[dict[str, Any]]]:
    with zipfile.ZipFile(path) as zf:
        shared_strings: list[str] = []
        if "xl/sharedStrings.xml" in zf.namelist():
            sroot = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            for si in sroot.findall("a:si", NS):
                text = "".join((t.text or "") for t in si.findall(".//a:t", NS))
                shared_strings.append(text)

        root = ET.fromstring(zf.read("xl/worksheets/sheet1.xml"))

    table: list[list[Any]] = []
    for row in root.findall(".//a:sheetData/a:row", NS):
        values: dict[int, Any] = {}
        for cell in row.findall("a:c", NS):
            idx = _col_to_idx(cell.attrib.get("r", "A1"))
            ctype = cell.attrib.get("t")
            if ctype == "inlineStr":
                is_node = cell.find("a:is", NS)
                value = (
                    "".join((t.text or "") for t in is_node.findall(".//a:t", NS))
                    if is_node is not None
                    else ""
                )
            else:
                v = cell.find("a:v", NS)
                if v is None or v.text is None:
                    value = ""
                elif ctype == "s":
                    value = shared_strings[int(v.text)]
                else:
                    raw = v.text
                    try:
                        value = float(raw) if "." in raw else int(raw)
                    except ValueError:
                        value = raw
            values[idx] = value

        if values:
            row_values = [""] * (max(values.keys()) + 1)
            for i, v in values.items():
                row_values[i] = v
            table.append(row_values)

    headers = [str(h).strip() for h in table[0]]
    records: list[dict[str, Any]] = []
    for row in table[1:]:
        record = {}
        for i, h in enumerate(headers):
            record[h] = row[i] if i < len(row) else ""
        records.append(record)
    return headers, records


def parse_csv(path: Path) -> tuple[list[str], list[dict[str, Any]]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        headers = [h.strip() for h in (reader.fieldnames or [])]
        records: list[dict[str, Any]] = []
        for row in reader:
            rec: dict[str, Any] = {}
            for h in headers:
                rec[h] = row.get(h, "")
            records.append(rec)
    return headers, records


def load_input(path: Path) -> tuple[list[str], list[dict[str, Any]]]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return parse_csv(path)
    if suffix == ".xlsx":
        return parse_xlsx(path)
    raise ValueError(f"Unsupported input format: {suffix}. Use .xlsx or .csv")


def parse_literal_list(value: Any) -> list[str]:
    if value in (None, ""):
        return []
    txt = str(value).strip()

    try:
        obj: Any = json.loads(txt)
    except (ValueError, json.JSONDecodeError):
        try:
            obj = ast.literal_eval(txt)
        except (ValueError, SyntaxError):
            return []

    def flatten(x: Any) -> list[str]:
        if isinstance(x, list):
            out: list[str] = []
            for item in x:
                out.extend(flatten(item))
            return out
        if isinstance(x, str):
            val = x.strip()
            if val and val != "[]":
                return [val]
            return []
        return []

    return flatten(obj)


def parse_literal_dict(value: Any) -> dict[str, float]:
    if value in (None, ""):
        return {}
    txt = str(value).strip()

    try:
        obj: Any = json.loads(txt)
    except (ValueError, json.JSONDecodeError):
        try:
            obj = ast.literal_eval(txt)
        except (ValueError, SyntaxError):
            return {}

    if not isinstance(obj, dict):
        return {}

    out: dict[str, float] = {}
    for k, v in obj.items():
        key = str(k).strip()
        try:
            out[key] = float(v)
        except (ValueError, TypeError):
            continue
    return out


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fieldnames})


def build_outputs(headers: list[str], records: list[dict[str, Any]], outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)

    settlements: list[dict[str, Any]] = []
    exports_long: list[dict[str, Any]] = []
    imports_long: list[dict[str, Any]] = []
    demographics_long: list[dict[str, Any]] = []
    class_density_long: list[dict[str, Any]] = []

    for row_id, rec in enumerate(records, start=1):
        settlement = str(rec.get("settlement", "")).strip()
        region = str(rec.get("region_kingdom", "")).strip()

        exports = parse_literal_list(rec.get("exports", ""))
        imports = parse_literal_list(rec.get("imports", ""))
        demographics = parse_literal_dict(rec.get("demographic_breakdown", ""))
        class_density = parse_literal_dict(rec.get("class_density", ""))

        for item in exports:
            exports_long.append(
                {
                    "row_id": row_id,
                    "settlement": settlement,
                    "region_kingdom": region,
                    "export_item": item,
                }
            )
        for item in imports:
            imports_long.append(
                {
                    "row_id": row_id,
                    "settlement": settlement,
                    "region_kingdom": region,
                    "import_item": item,
                }
            )

        for group, pop in demographics.items():
            demographics_long.append(
                {
                    "row_id": row_id,
                    "settlement": settlement,
                    "region_kingdom": region,
                    "demographic_group": group,
                    "population": int(pop),
                }
            )

        for social_class, share in class_density.items():
            class_density_long.append(
                {
                    "row_id": row_id,
                    "settlement": settlement,
                    "region_kingdom": region,
                    "social_class": social_class,
                    "share": share,
                }
            )

        normalized = dict(rec)
        normalized["exports_json"] = json.dumps(exports, ensure_ascii=False)
        normalized["imports_json"] = json.dumps(imports, ensure_ascii=False)
        normalized["demographic_breakdown_json"] = json.dumps(demographics, ensure_ascii=False)
        normalized["class_density_json"] = json.dumps(class_density, ensure_ascii=False)
        settlements.append(normalized)

    settlement_fields = headers + [
        "exports_json",
        "imports_json",
        "demographic_breakdown_json",
        "class_density_json",
    ]

    write_csv(outdir / "settlements_dashboard.csv", settlements, settlement_fields)
    write_csv(outdir / "exports_long.csv", exports_long, ["row_id", "settlement", "region_kingdom", "export_item"])
    write_csv(outdir / "imports_long.csv", imports_long, ["row_id", "settlement", "region_kingdom", "import_item"])
    write_csv(
        outdir / "demographics_long.csv",
        demographics_long,
        ["row_id", "settlement", "region_kingdom", "demographic_group", "population"],
    )
    write_csv(
        outdir / "class_density_long.csv",
        class_density_long,
        ["row_id", "settlement", "region_kingdom", "social_class", "share"],
    )

    missing = Counter()
    for rec in records:
        for h in headers:
            if rec.get(h, "") in ("", None):
                missing[h] += 1

    summary = outdir / "QA_SUMMARY.md"
    with summary.open("w", encoding="utf-8") as f:
        f.write("# Dashboard Data QA Summary\n\n")
        f.write(f"- Input rows: **{len(records)}**\n")
        f.write(f"- Input columns: **{len(headers)}**\n")
        f.write(f"- `exports_long` rows: **{len(exports_long)}**\n")
        f.write(f"- `imports_long` rows: **{len(imports_long)}**\n")
        f.write(f"- `demographics_long` rows: **{len(demographics_long)}**\n")
        f.write(f"- `class_density_long` rows: **{len(class_density_long)}**\n\n")
        f.write("## Missingness (top 10)\n")
        for col, cnt in missing.most_common(10):
            f.write(f"- `{col}`: {cnt}\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="Demographics_of_Faerun_Dataset.xlsx")
    parser.add_argument("--outdir", default="dashboard_data")
    args = parser.parse_args()

    headers, records = load_input(Path(args.input))
    build_outputs(headers, records, Path(args.outdir))
    print(f"Prepared dashboard data in {args.outdir} from {len(records)} records.")


if __name__ == "__main__":
    main()
