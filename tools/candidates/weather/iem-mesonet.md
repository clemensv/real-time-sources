# Iowa Environmental Mesonet (IEM)

**Country/Region**: United States (with some global data)
**Publisher**: Iowa State University — Department of Agronomy
**API Endpoint**: `https://mesonet.agron.iastate.edu/api/1/`
**Documentation**: https://mesonet.agron.iastate.edu/api/ (overview), https://mesonet.agron.iastate.edu/api/1/docs (Swagger)
**Protocol**: REST API (FastAPI/OpenAPI 3.1)
**Auth**: None (fully open, no API key required)
**Data Format**: JSON, GeoJSON, CSV
**Update Frequency**: Real-time (current observations), hourly (METAR), 1-minute (ASOS)
**License**: Free to use, including commercial — no formal license restriction

## What It Provides

The Iowa Environmental Mesonet is a legendary weather data aggregator. Run by daryl herzmann at Iowa State since the early 2000s, it archives and serves an extraordinary breadth of US meteorological data:

### API v1 (FastAPI/OpenAPI)

- **IEM Reanalysis (IEMRE)**: Gridded daily and hourly reanalysis data by lat/lon point.
- **Flash Flood Guidance** by point: NWS RFC flash flood guidance data.
- **ASOS Interval Summaries**: Computed summaries over arbitrary time intervals.
- **Station Metadata**: Network and station lookup.

### Ad-hoc GeoJSON/JSON Services (dozens of endpoints)

- **Current Observations** (`/json/current.py`): Live METAR/ASOS observations for any IEM network.
- **Network GeoJSON** (`/geojson/network.py`): Station metadata as GeoJSON for any network (e.g., IA_ASOS, ISUSM).
- **Local Storm Reports** (`/geojson/lsr.py`): NWS local storm reports as GeoJSON.
- **Storm Based Warnings** (`/geojson/sbw.py`): NWS polygon warnings.
- **VTEC Events**: Valid Time Event Codes — all NWS watches, warnings, advisories with searchable archive.
- **SPC Outlooks/Watches/MCDs**: Storm Prediction Center convective outlooks and mesoscale discussions.
- **NEXRAD Storm Attributes**: Radar-derived storm attributes.
- **Sounding/RAOB Data**: Upper-air sounding data.
- **Text Products**: Full NWS text product archive and search.
- **Snowfall Observations**: 6-hour snowfall over past 48 hours.

### Bulk Data Download (CGI services)

- **ASOS/METAR Data** (`/cgi-bin/request/asos.py`): Comprehensive METAR download for any station. Supports ~20 parameters including temperature, dewpoint, wind, visibility, sky cover, weather codes, ice accretion, peak wind gusts.
- **ASOS 1-Minute Data**: NCEI 1-minute ASOS data.
- **NWS COOP Observations**: Cooperative observer network data.
- **HADS/DCP/SHEF Data**: Hydrometeorological data.

### OGC Services

- WMS/WFS services for radar, satellite, and analysis products.

## API Details

The API v1 uses FastAPI with full OpenAPI 3.1 specification:
```
GET https://mesonet.agron.iastate.edu/api/1/openapi.json
```

GeoJSON services use simple query parameters:
```
GET https://mesonet.agron.iastate.edu/geojson/network.py?network=IA_ASOS
```

ASOS download service with extensive parameters:
```
GET https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=KDSM&data=tmpf,dwpf&sts=2026-04-01&ets=2026-04-06&tz=UTC
```

No authentication required. IP-based rate limiting on bulk download services. Open source — all code is on GitHub (akrherz/iem, akrherz/iem-web-services).

## Freshness Assessment

- Current observations: Real-time from ASOS/AWOS network.
- METAR data: Updated with each report (hourly + specials).
- 1-minute ASOS data available.
- NWS products: Archived within minutes of issuance.
- Storm reports and warnings: Near-real-time.
- Probed network GeoJSON — received immediate response with station metadata.

## Entity Model

- **Network**: Categorized by state and type (e.g., IA_ASOS, IA_COOP, ISUSM).
- **Station**: ICAO codes for airports, state-specific IDs for other networks. Rich metadata including elevation, WFO, time zone, county, UGC codes.
- **Observation**: Multi-parameter timestamped readings.
- **Warning/Event**: VTEC-coded with WFO, phenomenon, significance, event tracking number.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time METAR, 1-minute ASOS, near-real-time NWS products |
| Openness | 3 | No auth, no registration, open source, commercial use OK |
| Stability | 2 | One-person project at a university — brilliant but bus-factor risk |
| Structure | 3 | OpenAPI 3.1, GeoJSON, clean JSON, multiple output formats |
| Identifiers | 3 | ICAO codes, VTEC codes, WFO IDs — all standard meteorological identifiers |
| Additive Value | 3 | Unique aggregation of ASOS/AWOS, NWS products, storm data; decades of archive |
| **Total** | **17/18** | |

## Notes

- The IEM is one of the most valuable open weather data resources in existence. It aggregates data that would otherwise require navigating dozens of disparate NOAA/NWS systems.
- The archive depth is extraordinary — some stations have data going back to the 1920s.
- The "bus factor" risk is real — the site acknowledges its dependence on a single developer. But the code is open source on GitHub, which mitigates this.
- ASOS/METAR download service is the de facto standard way to get bulk US airport weather observations.
- Storm-based warnings as GeoJSON with polygon geometries are incredibly useful for geospatial applications.
- The VTEC event tracking system provides complete watch/warning/advisory lifecycle data.
- Rate limits are enforced to prevent abuse, but normal use is unrestricted.
- Complements the already-integrated NOAA NWS source by providing easier access to observation data, storm reports, and archived products.
