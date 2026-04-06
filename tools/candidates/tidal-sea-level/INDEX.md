# Tidal / Sea Level — Candidate Data Sources

Research candidates for real-time tidal and sea level monitoring APIs.

**Already covered in repo**: USA NOAA CO-OPS Tides and Currents (`noaa/`)

## Candidates

| Slug | Source | Country/Region | Score | Key Strength |
|------|--------|---------------|-------|-------------|
| [ioc-slsmf](ioc-slsmf.md) | IOC Sea Level Station Monitoring Facility | Global (~1,000 stations) | **17/18** | Comprehensive global real-time aggregator; V2 API with QC |
| [puertos-del-estado](puertos-del-estado.md) | Puertos del Estado REDMAR | Spain (40+ stations) | **16/18** | Open THREDDS/OPeNDAP; Canary Islands + Gibraltar coverage |
| [uhslc](uhslc.md) | University of Hawaii Sea Level Center | Global (~500 stations) | **14/18** | Pacific/tropical focus; superior QC; OPeNDAP access |
| [shom-refmar](shom-refmar.md) | SHOM REFMAR | France (50+ stations) | **13/18** | French overseas territories (Pacific, Caribbean, Indian Ocean) |
| [jma-tidal](jma-tidal.md) | JMA Tidal Observations | Japan (~80 stations) | **13/18** | Real-time tsunami-grade data; no public API though |
| [bom-pacific-sealevel](bom-pacific-sealevel.md) | BOM Pacific Sea Level Monitoring | Pacific Islands (14 nations) | **13/18** | Unique SIDS coverage; only precision data for many atolls |
| [bodc-uk-tide-gauges](bodc-uk-tide-gauges.md) | BODC UK Tide Gauge Network | UK (43 gauges) | **12/18** | Century-long records; near-real-time raw + QC'd processed |
| [bom-sea-level](bom-sea-level.md) | BOM ABSLMP | Australia (14 stations) | **12/18** | Geodetic-quality; co-located met data; CC BY license |

## Recommendation

**Top pick**: IOC SLSMF (17/18) — the global aggregator that covers ~1,000 stations with a clean REST API. This single integration provides more coverage than all other candidates combined.

**Strong second**: Puertos del Estado (16/18) — open THREDDS access, no auth, unique Canary Islands and Strait of Gibraltar coverage.

**Worth noting**: Most of these stations also report through the IOC SLSMF. The direct national sources add value through datum-referenced data, better QC, and station-specific metadata that the IOC aggregator doesn't carry.
