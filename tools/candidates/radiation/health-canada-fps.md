# Health Canada Fixed Point Surveillance (FPS) Network

**Country/Region**: Canada
**Publisher**: Health Canada / Santé Canada
**API Endpoint**: `https://open.canada.ca/data/api/3/action/package_show?id=f7d4c308-83e0-4e07-8f55-64a005c146cc`
**Data Download**: `https://open.canada.ca/data/dataset/f7d4c308-83e0-4e07-8f55-64a005c146cc/resource/6b2bd925-637c-4a63-bf6f-3bb4d4eceb83/download/2025jan-decdosedata_english.csv`
**Documentation**: https://open.canada.ca/data/en/dataset/f7d4c308-83e0-4e07-8f55-64a005c146cc
**Protocol**: CKAN REST API + CSV file download
**Auth**: None
**Data Format**: CSV
**Update Frequency**: Quarterly (P3M) — monthly dose values published per quarter
**License**: Open Government Licence — Canada

## What It Provides

The FPS network monitors public radiation dose from radioactive materials in the atmosphere around Canadian nuclear facilities and at regional sites nationwide. It measures external dose from three noble gases — Argon-41, Xenon-133, Xenon-135 — plus total Air KERMA (all external gamma sources including natural background). Units are nGy/month (nanoGray per month).

85 monitoring stations across 10 systems/regions:

| System | Description |
|---|---|
| Pickering | Ontario nuclear power complex |
| Darlington | Ontario nuclear power complex |
| Bruce | Ontario nuclear power complex |
| Gentilly | Quebec (decommissioned reactor) |
| Point Lepreau | New Brunswick nuclear station |
| Greater Toronto Area/Lake Ontario | Urban/regional |
| Ottawa Valley | Chalk River/Petawawa region |
| Regional | National sites (Yellowknife, Regina, Calgary, Winnipeg, etc.) |
| Vancouver Island | BC sites |
| Halifax | Nova Scotia sites |

Coverage spans from Resolute (Arctic) to Victoria (Pacific) to St. John's (Atlantic), including Iqaluit, Cambridge Bay, Haida Gwaii, and Whitehorse.

## API Details

### CKAN Metadata API

```
GET https://open.canada.ca/data/api/3/action/package_show?id=f7d4c308-83e0-4e07-8f55-64a005c146cc
```

Returns full dataset metadata with resource URLs, license info, update schedule.

### CSV Data (current year — 2025)

```
GET https://open.canada.ca/data/dataset/f7d4c308-83e0-4e07-8f55-64a005c146cc/resource/6b2bd925-637c-4a63-bf6f-3bb4d4eceb83/download/2025jan-decdosedata_english.csv
```

### Sample Data

```csv
System,Station,Month,Ar41 (nGy/month),Xe133 (nGy/month),Xe135 (nGy/month),Air KERMA (nGy/month)
Pickering,P2 Montgomery Rd,Jan,-,-,-,19334
Pickering,P2 Montgomery Rd,Feb,-,-,-,14414
Darlington,D1 Blue Circle Cement,Jan,-,-,-,21147
Bruce,Kincardine,Jan,-,-,-,24590
```

### Historical Data

Multiple yearly datasets available on Open Canada (2016–2025), all with same CSV structure. Discovery via:

```
GET https://open.canada.ca/data/api/3/action/package_search?q=fixed+point+surveillance+radiation
```

## Freshness Assessment

Not real-time — quarterly updates with monthly aggregated dose values. Data confirmed live on 2026-04-06 with 2025 data available (1,022 rows, ~42 KB). Well-suited for periodic batch ingestion.

## Entity Model

- **Station** — identified by system name + station name (e.g., "Pickering / P2 Montgomery Rd"). No formal station ID or coordinates in the CSV.
- **Measurement** — monthly aggregated dose for each noble gas isotope plus total Air KERMA, in nGy/month.
- **Data Dictionary** — available as separate text file download from the same dataset.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 1 | Quarterly updates, monthly aggregates — not real-time |
| Openness | 3 | No auth, Open Government Licence, CKAN API |
| Stability | 3 | Government of Canada open data infrastructure |
| Structure | 3 | Clean CSV with consistent schema, data dictionary provided |
| Identifiers | 1 | No station IDs, no coordinates — text names only |
| Additive Value | 2 | Unique Canadian nuclear perimeter monitoring, 85 stations |
| **Total** | **13/18** | |

## Notes

- Not a real-time source — quarterly batch data. Included because it provides unique Canadian nuclear facility perimeter monitoring data not available elsewhere.
- No geographic coordinates in the CSV — station locations would need to be geocoded or cross-referenced.
- The CKAN API enables programmatic discovery of new yearly datasets as they're published.
- Complements EPA RadNet (USA) for North American radiation coverage.
- EURDEP does not include Canadian data — this is the only open source for Canadian radiation monitoring.
