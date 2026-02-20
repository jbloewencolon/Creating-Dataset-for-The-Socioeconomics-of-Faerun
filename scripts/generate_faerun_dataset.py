#!/usr/bin/env python3
"""Generate higher-quality synthetic Faerûn socioeconomic datasets.

Improvements over prior generator:
- Region-weighted settlement sampling
- Region-specific geo bounds and climate baselines
- Stronger internal consistency checks (demographics, class density, region rollups)
- Explicit provenance confidence tied to canon_status
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path
from typing import Any

REGIONS: dict[str, dict[str, Any]] = {
    "Amn": {
        "capital": "Athkatla",
        "base_temp": 67,
        "base_rain": 74,
        "weight": 1.2,
        "wealth_factor": 1.12,
        "lat": (8.0, 28.0),
        "lon": (-45.0, -8.0),
    },
    "Cormyr": {
        "capital": "Suzail",
        "base_temp": 61,
        "base_rain": 58,
        "weight": 1.1,
        "wealth_factor": 1.05,
        "lat": (18.0, 42.0),
        "lon": (-8.0, 28.0),
    },
    "Calimshan": {
        "capital": "Memnon",
        "base_temp": 79,
        "base_rain": 30,
        "weight": 0.9,
        "wealth_factor": 1.08,
        "lat": (-2.0, 24.0),
        "lon": (-66.0, -28.0),
    },
    "Tethyr": {
        "capital": "Darromar",
        "base_temp": 68,
        "base_rain": 61,
        "weight": 1.0,
        "wealth_factor": 1.0,
        "lat": (2.0, 26.0),
        "lon": (-58.0, -16.0),
    },
    "Sembia": {
        "capital": "Selgaunt",
        "base_temp": 55,
        "base_rain": 47,
        "weight": 1.0,
        "wealth_factor": 1.02,
        "lat": (24.0, 48.0),
        "lon": (18.0, 54.0),
    },
    "Waterdeep": {
        "capital": "Waterdeep",
        "base_temp": 52,
        "base_rain": 44,
        "weight": 0.85,
        "wealth_factor": 1.15,
        "lat": (28.0, 56.0),
        "lon": (-42.0, -4.0),
    },
    "Baldurs Gate": {
        "capital": "Baldur's Gate",
        "base_temp": 57,
        "base_rain": 51,
        "weight": 1.05,
        "wealth_factor": 1.07,
        "lat": (16.0, 42.0),
        "lon": (-36.0, -2.0),
    },
    "Neverwinter": {
        "capital": "Neverwinter",
        "base_temp": 48,
        "base_rain": 42,
        "weight": 0.9,
        "wealth_factor": 1.03,
        "lat": (34.0, 66.0),
        "lon": (-56.0, -18.0),
    },
}

GOVERNMENTS = [
    "Confederacy",
    "Democracy",
    "Dictatorship",
    "Magocracy",
    "Monarchy",
    "Merchant Council",
    "Satrapy",
    "Theocracy",
    "Patriarchy",
]

CAUSES_OF_DEATH = [
    "monster attack",
    "disease",
    "famine",
    "war",
    "crime",
    "arcane mishap",
    "old age",
]

EXPORT_POOL = [
    "timber",
    "fish",
    "grain",
    "wine",
    "cloth",
    "armor",
    "weapons",
    "gems",
    "books",
    "horses",
    "salt",
]
IMPORT_POOL = [
    "spices",
    "silk",
    "ore",
    "parchment",
    "glass",
    "magic items",
    "mercenaries",
    "coal",
    "jewelry",
]

LANG_POOL = ["Common", "Elvish", "Dwarvish", "Halfling", "Orc", "Draconic"]
RELIGION_POOL = ["Tyr", "Torm", "Mystra", "Lathander", "Chauntea", "Tempus", "Selune"]


def weighted_region_choice(rng: random.Random) -> str:
    regions = list(REGIONS.keys())
    weights = [float(REGIONS[r]["weight"]) for r in regions]
    return rng.choices(regions, weights=weights, k=1)[0]


def normalized_class_density(rng: random.Random) -> dict[str, float]:
    poor = rng.uniform(0.45, 0.7)
    middle = rng.uniform(0.2, 0.4)
    wealthy = rng.uniform(0.02, 0.1)
    aristocrat = max(0.005, 1 - (poor + middle + wealthy))
    total = poor + middle + wealthy + aristocrat
    parts = {
        "poor": poor / total,
        "middle": middle / total,
        "wealthy": wealthy / total,
        "aristocrat": aristocrat / total,
    }
    # Keep rounded values while forcing exact sum of 1.0
    rounded = {k: round(v, 4) for k, v in parts.items()}
    delta = round(1.0 - sum(rounded.values()), 4)
    rounded["poor"] = round(rounded["poor"] + delta, 4)
    return rounded


def demographic_breakdown(pop: int, rng: random.Random) -> dict[str, int]:
    ratios = {
        "humans": rng.uniform(0.65, 0.88),
        "elves": rng.uniform(0.02, 0.12),
        "dwarves": rng.uniform(0.03, 0.1),
        "halflings": rng.uniform(0.02, 0.1),
        "half-orcs": rng.uniform(0.01, 0.06),
    }
    total = sum(ratios.values())
    norm = {k: v / total for k, v in ratios.items()}
    allocated = {k: int(pop * v) for k, v in norm.items()}
    rem = pop - sum(allocated.values())
    allocated["misc."] = rem
    return allocated


def sample_trade(pool: list[str], rng: random.Random, kmin: int = 1, kmax: int = 5) -> list[str]:
    k = rng.randint(kmin, kmax)
    return sorted(rng.sample(pool, k=min(k, len(pool))))


def make_record(i: int, rng: random.Random, capital_every: int) -> dict[str, object]:
    region = weighted_region_choice(rng)
    region_cfg = REGIONS[region]
    capital = str(region_cfg["capital"])
    is_capital = i % capital_every == 0
    settlement = capital if is_capital else f"{region} Settlement {i:04d}"

    pop = int(max(80, rng.lognormvariate(7.25, 1.08)))
    class_dist = normalized_class_density(rng)
    dem = demographic_breakdown(pop, rng)
    exports = sample_trade(EXPORT_POOL, rng)
    imports = sample_trade(IMPORT_POOL, rng)

    lifestyle_gold_day = (
        class_dist["poor"] * 2.0
        + class_dist["middle"] * 8.0
        + class_dist["wealthy"] * 25.0
        + class_dist["aristocrat"] * 90.0
    )
    settlement_economy = int(pop * lifestyle_gold_day * 365 * float(region_cfg["wealth_factor"]))
    hidden_economy = int(settlement_economy * rng.uniform(0.78, 1.35))
    rumored_treasure_value = int(hidden_economy * rng.uniform(0.0007, 0.07))

    dragon = min(int(rng.paretovariate(2) - 1), 120)
    dragon = max(dragon if rng.random() < 0.17 else 0, 0)
    magical_climate = rng.randint(0, 10)
    tax_rate = rng.randint(0, 20) if rng.random() < 0.67 else 0

    risk_index = round(min(100.0, dragon * 0.9 + magical_climate * 3.5 + tax_rate * 0.8), 2)
    trade_balance = len(exports) - len(imports)

    canon_status = "canonical" if is_capital else rng.choices(["derived", "synthetic"], [0.45, 0.55], k=1)[0]
    if canon_status == "canonical":
        source_conf = round(rng.uniform(0.88, 0.99), 2)
    elif canon_status == "derived":
        source_conf = round(rng.uniform(0.6, 0.86), 2)
    else:
        source_conf = round(rng.uniform(0.35, 0.7), 2)

    lat_lo, lat_hi = region_cfg["lat"]
    lon_lo, lon_hi = region_cfg["lon"]

    return {
        "settlement": settlement,
        "region_kingdom": region,
        "capital": capital,
        "settlement_population": pop,
        "settlement_economy": settlement_economy,
        "rumored_treasure_value": rumored_treasure_value,
        "demographic_breakdown": json.dumps(dem, ensure_ascii=False),
        "average_age": rng.randint(24, 180),
        "most_likely_cause_of_death": rng.choice(CAUSES_OF_DEATH),
        "government_type": json.dumps([rng.choice(GOVERNMENTS)], ensure_ascii=False),
        "class_density": json.dumps(class_dist, ensure_ascii=False),
        "tax_rate": tax_rate,
        "exports": json.dumps([exports], ensure_ascii=False),
        "imports": json.dumps([imports], ensure_ascii=False),
        "ruler": f"Ruler {region[:3].upper()}-{rng.randint(1,999)}",
        "military": rng.choice(["small militia", "professional guard", "mercenary heavy", "naval patrol"]),
        "magic_academy": rng.choice(["None", "guilds", "local academy", "arcanum"]),
        "languages": ", ".join(sorted(rng.sample(LANG_POOL, k=rng.randint(1, 3)))),
        "religions": ", ".join(sorted(rng.sample(RELIGION_POOL, k=rng.randint(1, 3)))),
        "region_population": "",  # computed post-pass
        "region_economy": "",  # computed post-pass
        "area": round(rng.uniform(8.0, 550.0), 2),
        "average_temperature": round(float(region_cfg["base_temp"]) + rng.uniform(-8, 7), 1),
        "annual_rainfall": round(float(region_cfg["base_rain"]) + rng.uniform(-18, 20), 1),
        "magical_climate": magical_climate,
        "dragon_sightings": dragon,
        "sources": "synthetic generator v3",
        "canon_status": canon_status,
        "source_confidence": source_conf,
        "hidden_economy": hidden_economy,
        "trade_balance": trade_balance,
        "risk_index": risk_index,
        "geo_lat": round(rng.uniform(lat_lo, lat_hi), 5),
        "geo_lon": round(rng.uniform(lon_lo, lon_hi), 5),
    }


def fill_region_rollups(rows: list[dict[str, object]]) -> None:
    region_pop: dict[str, int] = {}
    region_econ: dict[str, int] = {}
    for row in rows:
        region = str(row["region_kingdom"])
        region_pop[region] = region_pop.get(region, 0) + int(row["settlement_population"])
        region_econ[region] = region_econ.get(region, 0) + int(row["settlement_economy"])

    for row in rows:
        region = str(row["region_kingdom"])
        row["region_population"] = region_pop[region]
        row["region_economy"] = region_econ[region]


def validate_rows(rows: list[dict[str, object]]) -> list[str]:
    errors: list[str] = []
    for i, row in enumerate(rows, start=1):
        pop = int(row["settlement_population"])
        dem = json.loads(str(row["demographic_breakdown"]))
        if sum(int(v) for v in dem.values()) != pop:
            errors.append(f"row {i}: demographic sum != population")

        cls = json.loads(str(row["class_density"]))
        cls_sum = round(sum(float(v) for v in cls.values()), 4)
        if cls_sum != 1.0:
            errors.append(f"row {i}: class density sum is {cls_sum}, expected 1.0")

        if float(row["risk_index"]) < 0 or float(row["risk_index"]) > 100:
            errors.append(f"row {i}: risk index out of [0,100]")

        if int(row["hidden_economy"]) < int(row["settlement_economy"]) * 0.6:
            errors.append(f"row {i}: hidden economy implausibly low")

    return errors


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(path: Path, rows: list[dict[str, object]], seed: int, capital_every: int) -> None:
    regions = sorted({str(r["region_kingdom"]) for r in rows})
    payload = {
        "seed": seed,
        "rows": len(rows),
        "columns": len(rows[0]) if rows else 0,
        "regions": regions,
        "capital_every": capital_every,
        "generator_version": "v3",
        "notes": "Generated by scripts/generate_faerun_dataset.py",
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=650)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--capital-every", type=int, default=80)
    ap.add_argument("--out", default="generated_data/faerun_dataset_generated.csv")
    ap.add_argument("--meta", default="generated_data/faerun_dataset_generated.meta.json")
    args = ap.parse_args()

    rng = random.Random(args.seed)
    rows = [make_record(i + 1, rng, args.capital_every) for i in range(args.rows)]
    fill_region_rollups(rows)

    errors = validate_rows(rows)
    if errors:
        for err in errors[:20]:
            print(f"validation_error: {err}")
        raise SystemExit(f"Generation failed with {len(errors)} validation errors")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    write_csv(out, rows)

    meta = Path(args.meta)
    meta.parent.mkdir(parents=True, exist_ok=True)
    write_metadata(meta, rows, args.seed, args.capital_every)

    print(f"Generated dataset: {out} ({len(rows)} rows, seed={args.seed}, version=v3)")


if __name__ == "__main__":
    main()
