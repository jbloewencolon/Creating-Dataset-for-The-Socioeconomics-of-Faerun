#!/usr/bin/env python3
"""Validate generated Faerûn dataset quality constraints."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def validate(rows: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []

    region_rollup: dict[str, tuple[int, int]] = {}
    for i, row in enumerate(rows, start=2):
        try:
            pop = int(float(row["settlement_population"]))
            econ = int(float(row["settlement_economy"]))
            region_pop = int(float(row["region_population"]))
            region_econ = int(float(row["region_economy"]))
            risk = float(row["risk_index"])
            conf = float(row["source_confidence"])
            lat = float(row["geo_lat"])
            lon = float(row["geo_lon"])
        except Exception as exc:
            errors.append(f"line {i}: numeric parse error: {exc}")
            continue

        if risk < 0 or risk > 100:
            errors.append(f"line {i}: risk_index out of bounds: {risk}")
        if conf < 0 or conf > 1:
            errors.append(f"line {i}: source_confidence out of bounds: {conf}")
        if lat < -90 or lat > 90 or lon < -180 or lon > 180:
            errors.append(f"line {i}: invalid geo coordinates: ({lat}, {lon})")

        try:
            dem = json.loads(row["demographic_breakdown"])
            if sum(int(v) for v in dem.values()) != pop:
                errors.append(f"line {i}: demographic sum mismatch")
        except Exception as exc:
            errors.append(f"line {i}: demographic JSON invalid: {exc}")

        try:
            cls = json.loads(row["class_density"])
            csum = round(sum(float(v) for v in cls.values()), 4)
            if csum != 1.0:
                errors.append(f"line {i}: class_density sum != 1.0 ({csum})")
        except Exception as exc:
            errors.append(f"line {i}: class_density JSON invalid: {exc}")

        region = row["region_kingdom"]
        if region not in region_rollup:
            region_rollup[region] = (region_pop, region_econ)
        else:
            p, e = region_rollup[region]
            if p != region_pop or e != region_econ:
                errors.append(f"line {i}: inconsistent region rollup for {region}")

    # Verify region rollups equal sums
    sums: dict[str, list[int]] = {}
    for row in rows:
        r = row["region_kingdom"]
        p = int(float(row["settlement_population"]))
        e = int(float(row["settlement_economy"]))
        if r not in sums:
            sums[r] = [0, 0]
        sums[r][0] += p
        sums[r][1] += e

    for region, (rp, re) in region_rollup.items():
        if region not in sums:
            continue
        if rp != sums[region][0] or re != sums[region][1]:
            errors.append(f"region {region}: rollup mismatch (row {rp}/{re} vs sum {sums[region][0]}/{sums[region][1]})")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="generated_data/faerun_dataset_generated.csv")
    args = parser.parse_args()

    rows = load_rows(Path(args.input))
    if not rows:
        raise SystemExit("No rows found")

    errors = validate(rows)
    if errors:
        for err in errors[:50]:
            print(f"ERROR: {err}")
        raise SystemExit(f"Validation failed with {len(errors)} issue(s)")

    print(f"Validation passed: {args.input} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
