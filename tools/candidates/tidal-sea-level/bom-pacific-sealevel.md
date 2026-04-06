# BOM Pacific Sea Level and Geodetic Monitoring (PSLM)

**Country/Region**: Pacific Islands (14 Pacific Island countries)
**Publisher**: Bureau of Meteorology (BOM), Australian Government
**API Endpoint**: `https://www.bom.gov.au/pacific/projects/pslm/index.shtml` (project portal)
**Documentation**: https://www.bom.gov.au/pacific/projects/pslm/
**Protocol**: HTTP file download (CSV)
**Auth**: None
**Data Format**: CSV
**Update Frequency**: Monthly (similar to ABSLMP)
**License**: Crown Copyright, CC BY 3.0 AU

## What It Provides

The PSLM project (formerly the South Pacific Sea Level and Climate Monitoring Project) installs and maintains high-quality SEAFRAME tide gauges across 14 Pacific Island nations and territories. These are among the only precision sea level monitoring instruments in many of these locations.

Participating countries/territories:
- Cook Islands, Fiji, Kiribati, Marshall Islands, Federated States of Micronesia, Nauru, Papua New Guinea, Samoa, Solomon Islands, Tonga, Tuvalu, Vanuatu, Palau, and Niue

Data includes:
- Hourly sea level observations
- Co-located meteorological observations (pressure, temperature, wind)
- GNSS geodetic data for tracking land movement

The project is funded by the Australian Government as part of its Pacific aid program and is critical for monitoring sea level rise impacts on vulnerable low-lying Pacific island nations.

## API Details

Access is via file downloads from the BOM website, following a similar pattern to the ABSLMP:

- Station data organized by country and year in CSV format
- Metadata and station descriptions available
- GNSS data accessible separately

No REST API is provided. URLs follow predictable patterns for automated download.

## Freshness Assessment

Moderate. Like the ABSLMP, data files are updated monthly. Not real-time. For operational Pacific tide data, the IOC SLSMF provides faster access to many of the same stations (which report via GTS).

## Entity Model

- **Station**: SEAFRAME station code, country, island, latitude, longitude
- **Observation**: timestamp (hourly), sea level (mm), atmospheric pressure, wind speed/direction, temperature
- **Annual File**: station + year CSV

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Monthly updates; not real-time |
| Openness | 3 | Free, CC BY 3.0 AU |
| Stability | 3 | Government-funded, multi-decade commitment (started 1990s) |
| Structure | 1 | File-based, no API |
| Identifiers | 2 | SEAFRAME codes; some cross-referencing to GLOSS/IOC |
| Additive Value | 3 | Unique coverage of Pacific SIDS — often the only precision data available |
| **Total** | **13/18** | |

## Notes

- This is one of the most important climate monitoring programs for Pacific island nations. Many of these locations have no other high-quality sea level monitoring.
- The project has been running since the early 1990s, providing critical baseline data for measuring sea level rise impacts on low-lying atolls.
- For real-time data from these stations, the IOC SLSMF is the better access path. The PSLM data provides the QC'd archive.
- Co-located GNSS data enables separation of absolute sea level change from vertical land motion — crucial for understanding true sea level rise at island locations.
- The humanitarian significance of this dataset is high — it directly informs climate adaptation planning for some of the world's most vulnerable nations.
