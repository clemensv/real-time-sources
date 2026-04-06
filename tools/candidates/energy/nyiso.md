# NYISO (New York ISO)

**Country/Region**: New York State, United States
**Publisher**: New York Independent System Operator (NYISO)
**API Endpoint**: `http://mis.nyiso.com/public/csv/{category}/` (file-based)
**Documentation**: https://www.nyiso.com/public/markets_operations/market_data/custom_report/index.htm
**Protocol**: HTTP file download (CSV/XML)
**Auth**: None (public data)
**Data Format**: CSV, XML
**Update Frequency**: 5 minutes (real-time prices), hourly (load)
**License**: Public data

## What It Provides

NYISO operates the electricity grid for New York State — one of the most complex and congested grids in the US, serving 19 million people including New York City.

Key data categories:

- **Real-time LMPs** — 5-minute Locational Marginal Prices at zonal and nodal level
- **Day-ahead LMPs** — Hourly day-ahead market prices
- **Real-time load** — Actual system load by zone
- **Fuel mix** — Real-time generation by fuel type
- **Interface flows** — Flows on key transmission interfaces
- **Operating reserves** — Reserve market clearing prices
- **Ancillary services** — Regulation and reserve data
- **Demand response** — Demand-side participation data

## API Details

NYISO publishes data through its Market Information System (MIS) as downloadable CSV and XML files:

```
http://mis.nyiso.com/public/csv/realtime/
http://mis.nyiso.com/public/csv/damlbmp/
http://mis.nyiso.com/public/csv/rtfuelmix/
http://mis.nyiso.com/public/csv/pal/
```

Files are date-stamped (e.g., `20260406rtfuelmix.csv`). The CSV files have standard headers and are straightforward to parse.

NYISO also provides a Custom Report tool for ad-hoc queries and a Real-Time Dashboard for visualization.

Load zones: CAPITL, CENTRL, DUNWOD, GENESE, HUD VL, LONGIL, MHK VL, MILLWD, N.Y.C., NORTH, WEST.

## Freshness Assessment

Real-time fuel mix and LMP data update every 5 minutes. Load data updates hourly. Day-ahead data is published the afternoon before. The file-based system is reliable and well-established.

## Entity Model

- **Zone**: 11 NYISO load zones (N.Y.C., Long Island, Hudson Valley, etc.)
- **Node**: Hundreds of pricing nodes for nodal LMPs
- **Fuel Type**: Dual Fuel, Natural Gas, Nuclear, Hydro, Wind, Other Renewables, Other Fossil
- **Interface**: Key transmission constraints (Central-East, UPNY-SENY, etc.)
- **Time**: 5-minute intervals (real-time), hourly (day-ahead)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 5-minute real-time data |
| Openness | 3 | Fully public, no auth |
| Stability | 3 | Regulatory-mandated market operator |
| Structure | 2 | CSV files, no JSON API |
| Identifiers | 2 | NYISO-specific zone names (not standardized across ISOs) |
| Additive Value | 2 | EIA covers NYISO at BA level; NYISO adds zonal/nodal granularity |
| **Total** | **15/18** | |

## Notes

- NYISO's 11 load zones and constrained transmission interfaces make it one of the most interesting ISOs for congestion and locational pricing analysis.
- The EIA Grid Monitor (`respondent=NYIS`) provides hourly demand and generation for NYISO in clean JSON — use NYISO MIS only when zonal/nodal granularity is needed.
- New York City's zone is particularly interesting: heavily import-dependent, with major undersea cable interconnections.
- NYISO is leading on offshore wind interconnection data as NY builds its offshore wind fleet.
- The file-based CSV approach is less convenient than REST APIs but reliable and well-established.
