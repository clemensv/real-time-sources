This documents the Finnish Meteorological Institute (FMI) air quality open data via WFS. Verified:

- Base URL: `https://opendata.fmi.fi/wfs`
- Protocol: OGC WFS 2.0 (Web Feature Service)
- Confirmed working: `request=getFeature&storedquery_id=urban::observations::airquality::hourly::multipointcoverage&place=Helsinki&maxlocations=1` returned WFS XML with 24h timeseries data for Helsinki
- Stored query IDs include air quality variants (simple, multipointcoverage, timevaluepair)
- Auth: None (registration recommended for high usage)
- Data Format: GML/XML
- Measurements available for Helsinki and other Finnish cities with municipal monitoring

```
# Finnish Meteorological Institute (FMI) Air Quality

**Country/Region**: Finland
**Publisher**: Ilmatieteen laitos (Finnish Meteorological Institute, FMI)
**API Endpoint**: `https://opendata.fmi.fi/wfs`
**Documentation**: https://en.ilmatieteenlaitos.fi/open-data
**Protocol**: OGC WFS 2.0 (Web Feature Service)
**Auth**: None (API key recommended for heavy use)
**Data Format**: GML/XML (OGC standard)
**Update Frequency**: Hourly
**License**: Creative Commons Attribution 4.0 (CC BY 4.0)

## What It Provides

FMI's open data service includes air quality observations from Finnish municipal monitoring networks alongside weather data. Air quality data covers major Finnish cities (Helsinki, Espoo, Tampere, Oulu, Turku, etc.) and includes PM10, PM2.5, NO₂, O₃, SO₂, CO, and the Finnish Air Quality Index (AQINDEX). The WFS interface follows OGC standards and supports stored queries for hourly air quality data. FMI also includes Fintraffic road weather and STUK radiation data.

## API Details

- **Base URL**: `https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0`
- **Key Stored Queries**:
  - `urban::observations::airquality::hourly::multipointcoverage` — hourly AQ as multi-point coverage grid
  - `urban::observations::airquality::hourly::simple` — hourly AQ as simple features (easier to parse)
  - `urban::observations::airquality::hourly::timevaluepair` — hourly AQ as time-value pairs
- **Query Parameters**: `place` (city name), `fmisid` (station ID), `maxlocations`, `starttime`, `endtime`, `parameters` (e.g., AQINDEX_PT1H_avg, PM10_PT1H_avg, NO2_PT1H_avg)
- **Response**: GML 3.2 FeatureCollection (XML) with observation data, coordinates, and time series
- **Available Parameters**: PM10_PT1H_avg, PM25_PT1H_avg, NO2_PT1H_avg, O3_PT1H_avg, SO2_PT1H_avg, CO_PT1H_avg, AQINDEX_PT1H_avg

## Freshness Assessment

Hourly observations are available with a delay of approximately 1-2 hours. The WFS returns a 24-hour window by default. The `starttime` and `endtime` parameters allow custom time ranges. Air quality data availability depends on municipal monitoring networks.

## Entity Model

- **StoredQuery** → predefined query template with parameters
- **Station/Location** → place name or fmisid, with coordinates in GML Point
- **Observation** → location × parameter × time → value (in GML coverage or simple feature)
- **Parameter** → pollutant measurement type with averaging period (e.g., PM10_PT1H_avg)

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Hourly observations |
| Openness | 3 | No auth for moderate use; CC BY 4.0 |
| Stability | 3 | FMI is a national met office; WFS is an OGC standard |
| Structure | 1 | GML/XML is complex to parse compared to JSON REST APIs |
| Identifiers | 2 | Place names and fmisid; OGC-standard feature IDs |
| Additive Value | 2 | Finland-only; includes AQINDEX not widely available |
| **Total** | **14/18** | |

## Notes

- The WFS/GML format is verbose and complex compared to JSON REST APIs. The `simple` stored query variant is the easiest to parse.
- FMI provides weather, radiation, and air quality through the same WFS — a one-stop-shop for Finnish environmental data.
- Air quality data availability depends on municipal networks — not all Finnish cities are covered.
- The `multipointcoverage` format returns gridded data; `timevaluepair` returns individual time-value pairs; `simple` returns the simplest flat structure.
- FMI's open data also includes Radiation and Nuclear Safety Authority (STUK) measurements — potential for multi-domain environmental monitoring.
- Rate limits are generous but registration is recommended for production use.
```
