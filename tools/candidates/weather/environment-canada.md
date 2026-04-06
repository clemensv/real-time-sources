# Environment Canada — MSC Datamart & GeoMet

**Country/Region**: Canada
**Publisher**: Meteorological Service of Canada (MSC), Environment and Climate Change Canada (ECCC)
**API Endpoint**: `https://dd.weather.gc.ca/` (Datamart), `https://geo.weather.gc.ca/geomet` (GeoMet)
**Documentation**: https://eccc-msc.github.io/open-data/
**Protocol**: HTTP file polling + AMQP push notifications (Datamart), OGC WMS/WCS/OGC API (GeoMet)
**Auth**: None (fully anonymous, no registration)
**Data Format**: GRIB2, GeoJSON, NetCDF, Shapefile, CSV, XML, PNG (map layers)
**Update Frequency**: Varies by product — hourly observations, model runs 2–4×/day, warnings in real-time
**License**: Environment and Climate Change Canada Data Server End-use Licence

## What It Provides

Canada's meteorological open data comes through two complementary platforms:

### MSC Datamart (`dd.weather.gc.ca`)
A raw data file server organized by date, providing:
- **Surface weather observations**: SWOB-ML (XML), CSV
- **NWP model output**: HRDPS (2.5 km Canada), RDPS (10 km), GDPS (25 km global) — GRIB2
- **Weather warnings**: CAP-CP (Common Alerting Protocol for Canada) XML
- **Radar**: Precipitation estimates, composites
- **Marine forecasts**: Including Great Lakes, coastal waters
- **Air quality**: AQHI (Air Quality Health Index) forecasts

Directory structure: `https://dd.weather.gc.ca/today/WXO-DD/` for current day's data with 30-day retention.

**AMQP push notifications**: Using the Sarracenia data pumping system, clients can subscribe to real-time file availability announcements via Advanced Message Queuing Protocol — eliminating the need to poll.

### MSC GeoMet
OGC-compliant web services providing:
- **WMS/WCS**: Map layers and data coverages for thousands of datasets
- **OGC API - Features**: GeoJSON access to point data
- **OGC API - Coverages**: Grid data access
- **STAC**: SpatioTemporal Asset Catalog for data discovery

GeoMet enables on-demand clipping, reprojection, format conversion, and custom visualization.

## API Details

**Datamart** is straightforward HTTP file access:
```
https://dd.weather.gc.ca/today/WXO-DD/observations/swob-ml/latest/
https://dd.weather.gc.ca/today/WXO-DD/model_gem_global/15km/grib2/
```

**AMQP (Sarracenia)** for real-time notifications:
- Subscribe to specific data categories
- Receive file availability announcements as they're published
- Download files based on announcements

**GeoMet OGC API**:
```
https://geo.weather.gc.ca/geomet/collections
```
Returns collections of meteorological data accessible via standard OGC endpoints.

Alternative high-bandwidth server: `http://hpfx.collab.science.gc.ca` with 10× bandwidth during peak hours.

## Freshness Assessment

- Surface observations: Published within minutes of collection via SWOB-ML.
- HRDPS 2.5 km model: Runs every 6 hours, data available ~2–3 hours after run.
- Weather warnings: Real-time via CAP-CP.
- AMQP push notifications enable near-instant awareness of new data.
- 30-day data retention on the file server.

## Entity Model

- **Station**: Identified by Climate ID and WMO ID
- **Observation (SWOB-ML)**: XML document per station per time step
- **Model grid**: GRIB2 files identified by model/resolution/run/step/level/parameter
- **Warning**: CAP-CP XML with area codes, severity, urgency
- **GeoMet collection**: OGC-standard collection with metadata

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time AMQP push, frequent model runs, immediate observation publishing |
| Openness | 3 | Fully anonymous, no registration, explicit open data mandate |
| Stability | 3 | Federal government service, operational 24/7 |
| Structure | 3 | Multiple formats (GRIB2, GeoJSON, XML), OGC standards via GeoMet |
| Identifiers | 3 | Climate IDs, WMO station IDs, CAP area codes |
| Additive Value | 3 | HRDPS 2.5km is excellent; AMQP push is unique; vast Canadian coverage |
| **Total** | **18/18** | |

## Notes

- The AMQP push notification system (Sarracenia) is a standout feature — very few met services offer real-time push.
- The combination of Datamart (raw files) + GeoMet (OGC services) covers both bulk processing and interactive access use cases.
- HRDPS at 2.5 km resolution is one of the highest-resolution operational models freely available.
- CAP-CP warnings follow an international standard (Common Alerting Protocol), making parsing straightforward.
- SWOB-ML (Surface Weather Observations Markup Language) is a well-documented XML standard.
- GeoMet supports on-the-fly format conversion — request data in GeoJSON, NetCDF, or CSV from the same endpoint.
- The `dd_info` mailing list provides advance notice of changes.
