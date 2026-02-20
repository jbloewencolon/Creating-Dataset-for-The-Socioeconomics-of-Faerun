# Live Dashboard Map Plan (Faerûn Socioeconomics)

## Goal
Build a live, explorable map dashboard that turns the dataset into a decision/learning product for analysts, educators, and D&D worldbuilders.

## Product Outcomes
1. **Exploration**: Users can filter settlements by region, population band, economy band, government type, magic academy presence, and dragon activity.
2. **Comparative analysis**: Users can compare regions on population, economy, tax profile, and trade mix.
3. **Narrative utility**: GMs can quickly discover “high opportunity” or “high risk” locations for campaigns.

## Delivery Paths

### Path A — Tableau Public (MVP, 1–2 weeks)
Recommended for speed and visibility.

### Core Views
- **Map view**: Settlement-level points with color for `region_kingdom`, size by `settlement_population`, and tooltip with economy/tax/dragon metrics.
- **Regional summary**: Bar charts for `region_economy`, `region_population`, and average `tax_rate`.
- **Risk panel**: Distribution of `dragon_sightings`, `magical_climate`, and cause-of-death frequency.
- **Trade panel**: Cleaned counts/tags from `exports` and `imports`.

### MVP Filters
- Region/kingdom
- Settlement population quantile band
- Settlement economy quantile band
- Government type
- Magic academy (yes/no/type)
- Dragon sightings band

### Tableau Publishing Checklist
1. Convert workbook source to analysis-ready `csv` (or `hyper`) extract.
2. Standardize schema for stringified columns (`demographic_breakdown`, `exports`, `imports`, `class_density`).
3. Add geospatial fields (lat/lon + optional region polygon mapping table).
4. Build dashboard layout with map + KPI strips + drilldown table.
5. Publish to Tableau Public and document refresh cadence.

### Path B — Proprietary Dashboard (Production, 3–6 weeks)
Recommended if you need private access, role-based features, or custom gameplay integrations.

### Suggested Architecture
- **Data layer**: Scheduled ETL to CSV/Parquet in object storage or relational DB.
- **API layer**: Lightweight FastAPI service exposing filtered settlement and region endpoints.
- **UI layer**: Streamlit/Dash (fast) or React + Mapbox/Leaflet (custom).
- **Observability**: Basic usage analytics, refresh health checks, and schema validation logs.

### Production Features
- Authentication and role controls.
- Saved views (for campaign planning or teaching modules).
- Scenario sliders (e.g., tax shocks, migration assumptions, dragon-risk multipliers).
- Versioned data snapshots for reproducible classroom exercises.

## Data Preparation Requirements (Both Paths)
1. **Create canonical data dictionary** with column types and valid ranges.
2. **Normalize list/dict text fields** to long-form relational tables where possible.
3. **Add provenance columns** (`canon_status`, `source_confidence`, `source_reference`).
4. **Define metric semantics** (currency units, annualization assumptions, tax interpretation).
5. **Add QA tests** for null thresholds, impossible values, and regional aggregation consistency.


## Implementation Update
The repository now includes a starter data-prep script:

```bash
python scripts/prepare_dashboard_data.py
```

This produces dashboard extracts in `dashboard_data/` including normalized long tables for exports, imports, demographics, and class density plus a `QA_SUMMARY.md` snapshot.

- Added `scripts/generate_faerun_dataset.py` for repeatable seed-based dataset refreshes (`--rows`, `--seed`, `--out`).
- `scripts/prepare_dashboard_data.py` now accepts both `.xlsx` and generated `.csv` inputs, enabling a full refresh cycle for new data versions.
- Added a generator quality gate (`scripts/validate_faerun_dataset.py`) before dashboard extraction to enforce data consistency and reproducibility standards.

## Proposed Milestones
- **Milestone 1 (Week 1):** Data cleaning + geospatial join + dashboard wireframe.
- **Milestone 2 (Week 2):** Tableau MVP published and documented.
- **Milestone 3 (Week 3–4):** Proprietary prototype with filtering API.
- **Milestone 4 (Week 5–6):** Auth, monitoring, and release hardening.

## Success Metrics
- Time-to-first-insight under 60 seconds for new users.
- >80% of settlements render with complete tooltip metrics.
- Dashboard refresh success rate >99% for scheduled updates.
- Positive qualitative feedback from both data learners and D&D GMs.
