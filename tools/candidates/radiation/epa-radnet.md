# EPA RadNet

**Country/Region**: United States (all 50 states + Puerto Rico)
**Publisher**: U.S. Environmental Protection Agency (EPA)
**API Endpoint**: `https://radnet.epa.gov/cdx-radnet-rest/api/rest/csv/{year}/fixed/{state}/{city}`
**Documentation**: https://www.epa.gov/radnet/radnet-csv-file-downloads
**Protocol**: REST (CSV download)
**Auth**: None
**Data Format**: CSV
**Update Frequency**: Hourly (near-real-time, updated several times daily from mirror server)
**License**: U.S. Government public domain

## What It Provides

RadNet is the EPA's nationwide radiation monitoring network, consisting of ~140 fixed air monitors across the United States. These stations continuously measure:

- **Gamma gross count rate** — across multiple energy channels (R02–R09)
- **Dose equivalent rate** — in nSv/h (nanoSieverts per hour)
- **Exposure rate** — where available

The network was established to detect unusual radiation levels in the ambient environment and is a key component of U.S. nuclear emergency preparedness. Data spans back to 2006–2007 for most stations.

## API Details

### Endpoint Pattern

```
GET https://radnet.epa.gov/cdx-radnet-rest/api/rest/csv/{year}/fixed/{state}/{city}
```

Parameters:
- `{year}` — Calendar year (e.g., 2026)
- `{state}` — State abbreviation (e.g., CA, NY, TX)
- `{city}` — City name, URL-encoded (e.g., LOS%20ANGELES)

### Example Request

```
GET https://radnet.epa.gov/cdx-radnet-rest/api/rest/csv/2026/fixed/CA/LOS%20ANGELES
```

### CSV Columns

| Column | Description |
|---|---|
| `LOCATION_NAME` | Station identifier (e.g., "CA: LOS ANGELES") |
| `SAMPLE COLLECTION TIME` | Timestamp (MM/DD/YYYY HH:MM:SS format) |
| `DOSE EQUIVALENT RATE (nSv/h)` | Dose equivalent rate in nanoSieverts/hour |
| `GAMMA COUNT RATE R02 (CPM)` | Gamma count rate, energy range 02 |
| `GAMMA COUNT RATE R03 (CPM)` | Gamma count rate, energy range 03 |
| `GAMMA COUNT RATE R04 (CPM)` | Gamma count rate, energy range 04 |
| `GAMMA COUNT RATE R05 (CPM)` | Gamma count rate, energy range 05 |
| `GAMMA COUNT RATE R06 (CPM)` | Gamma count rate, energy range 06 |
| `GAMMA COUNT RATE R07 (CPM)` | Gamma count rate, energy range 07 |
| `GAMMA COUNT RATE R08 (CPM)` | Gamma count rate, energy range 08 |
| `GAMMA COUNT RATE R09 (CPM)` | Gamma count rate, energy range 09 |
| `STATUS` | Data status (e.g., "APPROVED") |

### Sample Data

```csv
LOCATION_NAME,SAMPLE COLLECTION TIME,DOSE EQUIVALENT RATE (nSv/h),GAMMA COUNT RATE R02 (CPM),...,STATUS
CA: LOS ANGELES,01/01/2026 00:06:00,61.00,2958.00,1820.00,532.00,281.00,182.00,212.00,129.00,35.00,APPROVED
CA: LOS ANGELES,01/01/2026 01:06:00,62.00,2914.00,1793.00,519.00,267.00,181.00,207.00,125.00,33.00,APPROVED
```

### Historical Data

ZIP archives available per station, per year range:
```
https://www.epa.gov/system/files/other-files/2026-02/al_birmingham_2025-2007.zip
```

### Coverage

Stations in every state, major cities. Complete list available at the EPA documentation page. Each state has 1–10+ monitors.

## Freshness Assessment

Live data confirmed on 2026-04-06. The Los Angeles CSV returned hourly data from January 2026, with data marked "APPROVED." The EPA states data is updated "several times daily from a mirrored server." Timestamps are in UTC. The data is near-real-time but not instantaneous — there's a processing/approval pipeline.

## Entity Model

- **Station** — Identified by state + city name (e.g., "CA: LOS ANGELES"). Fixed location, with start date for each data stream.
- **Measurement** — Hourly reading with dose equivalent rate (nSv/h), gamma count rates across 8 energy channels (CPM), and approval status.
- **Data Stream** — Stations may have gamma gross count rate and/or exposure rate streams, with different start dates.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 2 | Near-real-time but "several times daily" mirror refresh, not instant |
| Openness | 3 | U.S. government public domain, no auth required |
| Stability | 3 | Federal EPA infrastructure, operational since 2006 |
| Structure | 2 | CSV only — no JSON API, requires parsing. Predictable URL pattern though. |
| Identifiers | 2 | State + city name as identifier, not a formal station code |
| Additive Value | 3 | ~140 stations, nationwide USA coverage, multi-channel spectral data |
| **Total** | **15/18** | |

## Notes

- The API is essentially a CSV-per-station-per-year download service — there's no single "get all stations" endpoint returning JSON. You need to know the state and city name to construct the URL.
- The multi-channel gamma spectral data (R02–R09) is unusually detailed — most other networks only report a single aggregated dose rate. This enables nuclide identification.
- Dose equivalent rate in nSv/h (not µSv/h like European networks) — divide by 1000 for comparison.
- No formal station list API — the station inventory is embedded in the EPA documentation HTML page.
- Historical ZIP archives provide bulk access to years of data per station.
- Timestamps in MM/DD/YYYY format (American convention) and UTC.
