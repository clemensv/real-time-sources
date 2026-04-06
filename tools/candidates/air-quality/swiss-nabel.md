This documents the Swiss NABEL (National Air Pollution Monitoring Network) operated by BAFU/FOEN. Verified:

- 16 monitoring stations across Switzerland
- Data available on opendata.swiss: stations dataset with WMS/WMTS/REST resources
- RESTful API via geo.admin.ch for station metadata
- License: Open use, must provide the source
- BAFU data query page at bafu.admin.ch
- No easily accessible real-time JSON API found — mainly file downloads and geo services

```
# Swiss NABEL (National Air Pollution Monitoring Network)

**Country/Region**: Switzerland
**Publisher**: BAFU / FOEN (Bundesamt für Umwelt / Federal Office for the Environment)
**API Endpoint**: `https://api3.geo.admin.ch/rest/services/api/MapServer/ch.bafu.nabelstationen` (station metadata)
**Documentation**: https://www.bafu.admin.ch/bafu/en/home/topics/air/state/data/data-query-nabel.html
**Protocol**: REST (geo.admin.ch), WMS/WMTS (map services)
**Auth**: None
**Data Format**: JSON (station metadata), CSV (measurement data downloads)
**Update Frequency**: Hourly (measurements); station metadata is static
**License**: Open Government Data (opendata.swiss — Open Use, attribution required)

## What It Provides

The NABEL network monitors air quality at 16 locations across Switzerland, representing different environments: city centres, residential areas, motorway corridors, rural sites, and alpine/pre-alpine backgrounds. Measured pollutants include PM10, PM2.5, O₃, NO₂, SO₂, CO, and various VOCs. The 16 stations are strategically distributed to characterize Switzerland's diverse topography and emission patterns.

## API Details

- **Station Metadata**: `https://api3.geo.admin.ch/rest/services/api/MapServer/ch.bafu.nabelstationen/`
  - Returns station locations, names, and metadata via the Swiss Federal Geoportal
- **Map Services**:
  - WMS: `https://wms.geo.admin.ch/` — layer `ch.bafu.nabelstationen`
  - WMTS: `https://wmts.geo.admin.ch/` — same layer for tiled maps
- **Measurement Data**: Bulk download from BAFU data query page (CSV format)
  - No public REST JSON API for real-time measurements was found
  - Data can be downloaded from the NABEL data query tool at bafu.admin.ch
- **STAC Catalog**: Available via opendata.swiss for machine-readable metadata
- **Stations (16)**: Including Bern, Zürich, Basel, Lausanne, Lugano, Payerne, Davos, Jungfraujoch (high-alpine)

## Freshness Assessment

NABEL provides hourly measurements, but the real-time data access is limited to the BAFU website and bulk downloads. No live JSON API for measurement data has been identified. Station metadata is available via geo.admin.ch REST API. The high-alpine Jungfraujoch station provides globally significant background atmospheric data.

## Entity Model

- **Station** → id, name, location type (urban/suburban/rural/alpine), coordinates, elevation
- **Component** → pollutant (PM10, PM2.5, O₃, NO₂, SO₂, CO, VOCs)
- **Measurement** → station × component × datetime → value (µg/m³)

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Hourly data exists but no live JSON API for measurements |
| Openness | 3 | Open government data; no auth for metadata API |
| Stability | 3 | Swiss federal government; NABEL network since 1979 |
| Structure | 1 | Station metadata via REST; measurements only as CSV bulk download |
| Identifiers | 2 | Station names; geo.admin.ch feature IDs |
| Additive Value | 2 | Only 16 stations; includes unique high-alpine data (Jungfraujoch) |
| **Total** | **13/18** | |

## Notes

- The main limitation is the lack of a public real-time JSON API for measurements. Station metadata is accessible, but hourly readings require scraping or bulk file processing.
- Jungfraujoch (3,580 m elevation) is one of the world's highest-altitude atmospheric monitoring sites — its data is used in global atmospheric research.
- Only 16 stations for all of Switzerland means coarse spatial coverage, but the stations are well-maintained reference-grade instruments.
- Swiss cantonal networks (e.g., Zurich OSTLUFT, Bern INLUFT) provide additional stations but through separate portals.
- opendata.swiss lists the NABEL stations dataset with WMS, WMTS, STAC, and REST resources — all metadata-oriented.
- For real-time Swiss air quality, consider using OpenAQ or EEA as intermediaries that may already ingest NABEL data.
```
