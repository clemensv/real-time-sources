# Tidal / Sea Level — Candidate Data Sources

Research candidates for real-time tidal and sea level monitoring APIs.

**Already covered in repo**: USA NOAA CO-OPS Tides and Currents (`noaa/`)

## Candidates

| Slug | Source | Country/Region | Score | Key Strength |
|------|--------|---------------|-------|-------------|
| [ioc-slsmf](ioc-slsmf.md) | IOC Sea Level Station Monitoring Facility | Global (~1,000 stations) | **17/18** | Comprehensive global real-time aggregator; V2 API with QC |
| [pegelonline-germany](pegelonline-germany.md) | PegelOnline WSV | Germany (North Sea + Baltic + rivers) | **17/18** | Flawless REST/JSON API; UUID-based; no auth; North Sea + Baltic tidal |
| [puertos-del-estado](puertos-del-estado.md) | Puertos del Estado REDMAR | Spain (40+ stations) | **16/18** | Open THREDDS/OPeNDAP; Canary Islands + Gibraltar coverage |
| [kartverket-norway](kartverket-norway.md) | Kartverket Hydrographic Service | Norway (entire coastline) | **16/18** | REST API; CC BY 4.0; fjord coverage; 5-day forecasts |
| [dmi-denmark](dmi-denmark.md) | DMI Ocean Observations | Denmark + Greenland | **16/18** | OGC API Features; GeoJSON; Danish straits shipping bottleneck |
| [smhi-sweden](smhi-sweden.md) | SMHI Oceanographic Observations | Sweden (entire coastline) | **16/18** | Clean REST/JSON; no auth; minute-resolution; Baltic coverage |
| [emodnet-physics](emodnet-physics.md) | EMODnet Physics ERDDAP | Europe (pan-European) | **15/18** | Single ERDDAP access point for all European marine data |
| [uhslc](uhslc.md) | University of Hawaii Sea Level Center | Global (~500 stations) | **14/18** | Pacific/tropical focus; superior QC; OPeNDAP access |
| [shom-refmar](shom-refmar.md) | SHOM REFMAR | France (50+ stations) | **13/18** | French overseas territories (Pacific, Caribbean, Indian Ocean) |
| [jma-tidal](jma-tidal.md) | JMA Tidal Observations | Japan (~80 stations) | **13/18** | Real-time tsunami-grade data; no public API though |
| [bom-pacific-sealevel](bom-pacific-sealevel.md) | BOM Pacific Sea Level Monitoring | Pacific Islands (14 nations) | **13/18** | Unique SIDS coverage; only precision data for many atolls |
| [psmsl](psmsl.md) | Permanent Service for Mean Sea Level | Global (~1,500 stations) | **13/18** | 300+ year records; the global reference for sea level trends |
| [bodc-uk-tide-gauges](bodc-uk-tide-gauges.md) | BODC UK Tide Gauge Network | UK (43 gauges) | **12/18** | Century-long records; near-real-time raw + QC'd processed |
| [bom-sea-level](bom-sea-level.md) | BOM ABSLMP | Australia (14 stations) | **12/18** | Geodetic-quality; co-located met data; CC BY license |
| [ioc-africa-tide-gauges](ioc-africa-tide-gauges.md) | IOC Africa Tide Gauges | Pan-African coastal | **14/18** | African coast coverage; tsunami warning; 1-15 min updates |

## Recommendation

**Top pick**: IOC SLSMF (17/18) — the global aggregator that covers ~1,000 stations with a clean REST API. This single integration provides more coverage than all other candidates combined.

**Strong second**: PegelOnline Germany (17/18) — one of the best-designed water level REST APIs anywhere. Clean JSON, UUID identifiers, no auth, filterable by water body. Covers North Sea tidal, Baltic non-tidal, and major European rivers.

**Nordic trio**: Kartverket + DMI + SMHI (all 16/18) together provide complete Scandinavian coastal coverage from North Cape to the Øresund. All three are open, well-structured REST APIs with CC BY licensing. SMHI and Kartverket need no auth at all.

**Pan-European aggregator**: EMODnet Physics ERDDAP (15/18) provides a single access point for European marine observations — useful if you want one integration instead of 10+ national APIs.

**Reference dataset**: PSMSL (13/18) is not real-time but is the authoritative global archive for sea level change analysis. PSMSL station IDs are the de facto standard for identifying tide gauge locations worldwide.

**Worth noting**: Most of these stations also report through the IOC SLSMF. The direct national sources add value through datum-referenced data, better QC, station-specific metadata, and forecast data that the IOC aggregator doesn't carry.

### Asia — Deep Dive Round 5

| Slug | Source | Country/Region | Score | Key Strength |
|------|--------|---------------|-------|-------------|
| [incois-india-ocean](incois-india-ocean.md) | INCOIS India | Indian Ocean | **11/18** | Tsunami warning center; 404 on tested API endpoints; high-value gap |

**Key finding**: India's INCOIS operates the Indian Ocean tsunami early warning system — a critical function for 2.7 billion coastal residents. The documented API endpoints returned 404 during testing. The data exists behind government web portals but lacks a stable public REST API.
