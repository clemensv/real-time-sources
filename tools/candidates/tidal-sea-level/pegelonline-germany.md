# PegelOnline (WSV) — Germany Coastal and Inland Water Levels

**Country/Region**: Germany (North Sea, Baltic Sea, and inland waterways)
**Publisher**: WSV (Wasserstraßen- und Schifffahrtsverwaltung des Bundes — Federal Waterways and Shipping Administration)
**API Endpoint**: `https://www.pegelonline.wsv.de/webservices/rest-api/v2/`
**Documentation**: https://www.pegelonline.wsv.de/webservices/rest-api/v2/
**Protocol**: REST API (JSON)
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Real-time (15-minute intervals)
**License**: German government open data (DL-DE/BY-2.0)

## What It Provides

PegelOnline is Germany's federal water level monitoring service, providing real-time data from gauging stations on:

- **North Sea coast** — tidal stations (Helgoland, Cuxhaven, Borkum, List auf Sylt, etc.)
- **Baltic Sea coast** — non-tidal coastal stations (Warnemünde, Sassnitz, Kiel, etc.)
- **Major inland waterways** — Rhine, Elbe, Danube, Weser, etc.

Verified API probe returned 15+ North Sea stations and 20+ Baltic Sea stations, all with UUID identifiers, coordinates, and agency metadata.

This is distinct from BSH (Bundesamt für Seeschifffahrt und Hydrographie) — PegelOnline covers the operational gauging network, while BSH focuses on offshore/deep-sea conditions.

## API Details

Clean REST JSON API:

```
# List all stations
GET https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json

# Filter by water body
GET https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json?waters=NORDSEE
GET https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json?waters=OSTSEE
GET https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json?waters=RHEIN

# Station details with current measurement
GET https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/{uuid}/W.json?includeCurrentMeasurement=true

# Measurement time series
GET https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/{uuid}/W/measurements.json?start=P1D
```

Duration format follows ISO 8601 (P1D = past 1 day, P7D = past 7 days, P31D = past 31 days).

Station metadata includes: UUID, station number, short/long name, km marker, agency, lat/lon, water body.

## Freshness Assessment

Excellent. Real-time at 15-minute intervals. Measurements available for the past 31 days through the API. Historical data available through a separate archive service.

## Entity Model

- **Station**: uuid, number, shortname, longname, km (river kilometer), agency, lat/lon
- **Water**: shortname, longname (e.g., NORDSEE, OSTSEE, RHEIN, ELBE)
- **Timeseries**: station UUID, parameter code (W = water level), unit
- **Measurement**: timestamp, value (cm above gauge datum)
- **CurrentMeasurement**: latest value, timestamp, trend, stateMnwMhw

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time 15-min intervals |
| Openness | 3 | No auth, no registration, open data license |
| Stability | 3 | Federal government infrastructure, legally mandated |
| Structure | 3 | Clean REST JSON; UUID identifiers; ISO 8601 durations |
| Identifiers | 3 | UUIDs + station numbers; water body classification |
| Additive Value | 2 | North Sea + Baltic + major European waterways; tidal + non-tidal |
| **Total** | **17/18** | |

## Notes

- One of the best-designed water level REST APIs in Europe. Clean JSON, UUID-based, no auth, standardized time formats.
- The water body filter (`waters=NORDSEE`, `waters=OSTSEE`) makes it trivial to separate tidal from non-tidal stations.
- Germany's North Sea coast has some of the world's most extreme tidal ranges (Wadden Sea).
- The same API covers inland waterways, making it dual-purpose: coastal tide monitoring + river level monitoring.
- Historical Cuxhaven data (since 1843) is among the longest continuous tide gauge records in the world.
- Complements the Scandinavian trio (Norway/Denmark/Sweden) for complete North Sea and Baltic coverage.
