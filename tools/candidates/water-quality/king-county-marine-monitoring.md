# King County Marine Buoy Water Quality

- **Country/Region**: US — Puget Sound, King County, WA
- **Publisher**: King County Department of Natural Resources and Parks (DNRP)
- **Endpoint**: `https://data.kingcounty.gov/resource/t5pc-wkwc.json`
- **Protocol**: REST (Socrata SODA API)
- **Auth**: None (app token optional)
- **Format**: JSON, CSV, XML
- **Freshness**: Near real-time (15-minute intervals from mooring stations)
- **Docs**: https://data.kingcounty.gov/Environment-Waste-Management/Puget-Sound-Marine-Monitoring/t5pc-wkwc
- **Score**: 14/18

## Overview

King County operates a marine monitoring network in Puget Sound with moored buoys and sampling stations that measure water temperature, salinity, dissolved oxygen, turbidity, chlorophyll, pH, and nutrients. The mooring stations report at 15-minute intervals, providing near real-time marine conditions. This complements the NANOOS candidate with a county-operated network focused on central Puget Sound and Elliott Bay.

## API Details

**Socrata Open Data API:**
```
GET https://data.kingcounty.gov/resource/t5pc-wkwc.json
```

**SODA Query Examples:**

| Query | URL |
|-------|-----|
| Latest records | `?$order=collect_date DESC&$limit=10` |
| Specific station | `?$where=locator='KSBP02'&$order=collect_date DESC` |
| Recent data | `?$where=collect_date > '2024-01-01'&$order=collect_date DESC` |

**Direct Mooring Data Download:**
```
https://green2.kingcounty.gov/marine-buoy/Data.aspx
```
Allows filtering by parameter, date range, and station — downloadable as CSV.

**Key Parameters Monitored:**
- Water temperature (°C)
- Salinity (PSU)
- Dissolved oxygen (mg/L)
- Turbidity (NTU)
- Chlorophyll fluorescence (µg/L)
- pH
- Wind speed/direction (some stations)
- Air temperature (some stations)

**Station Locations:**
- Central Puget Sound offshore stations
- Elliott Bay nearshore stations
- Duwamish River estuary
- East and west passage stations

## Freshness Assessment

Good. Mooring stations report every 15 minutes and data is available on the open data portal and download site with minimal delay. Cruise/sampling data (quarterly ship-based surveys) is less frequent. For real-time use, the mooring data is the primary source.

## Entity Model

- **Station** — Locator code, name, coordinates, type (mooring/cruise)
- **Parameter** — Water temperature, salinity, DO, turbidity, chlorophyll, pH
- **Observation** — Timestamp, station, parameter, value, quality flag
- **Cruise** — Quarterly ship-based sampling events (batch, not real-time)

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | 15-min mooring data is good; cruise data is quarterly |
| Openness | 3 | Socrata SODA API, no auth, county government data |
| Stability | 2 | County program, dependent on funding; data since 2009 |
| Structure | 2 | Socrata JSON; mixed mooring/cruise data in same dataset |
| Identifiers | 2 | Station locator codes; parameter names are descriptive |
| Additive Value | 3 | Unique central Puget Sound marine monitoring network |
| **Total** | **14/18** | |

## Notes

- Complements the NANOOS ERDDAP candidate — NANOOS covers UW/IOOS moorings while King County covers the county's own monitoring network.
- The direct buoy data download site (`green2.kingcounty.gov`) may have more real-time data than the Socrata dataset.
- Water temperature data is directly useful for swimming advisories and marine recreation planning.
- Dissolved oxygen levels can indicate marine health and affect fishing conditions.
- Data quality: provisional data is released first; final QA'd data follows.
- King County also maintains a separate swim beach bacteria monitoring program (see separate candidate).
