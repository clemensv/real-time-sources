# AviationWeather.gov Data API

**Country/Region**: Global (US-centric, but METAR/TAF/SIGMET coverage is worldwide)
**Publisher**: NOAA / National Weather Service / Aviation Weather Center
**API Endpoint**: `https://aviationweather.gov/api/data/metar`
**Documentation**: https://aviationweather.gov/data/api/
**Protocol**: REST
**Auth**: None (fully open, no registration required)
**Data Format**: JSON, GeoJSON, XML (IWXXM), CSV, raw text
**Update Frequency**: Real-time (METAR every 1 min cache, TAF every 10 min, SIGMET every 1 min)
**License**: US Government public domain

## What It Provides

The Aviation Weather Center's Data API is the authoritative source for aviation weather
products worldwide. This isn't just US data — METAR and TAF coverage is truly global,
covering every ICAO-reporting airport on the planet. SIGMETs are international. The API
was redeveloped in 2025 with a proper OpenAPI specification.

Products available:

- **METAR** — Terminal weather observations (worldwide, ~10,000+ stations)
- **TAF** — Terminal aerodrome forecasts (worldwide)
- **SIGMET** — Domestic US SIGMETs (convective, turbulence, icing, IFR)
- **International SIGMET** — Global aviation warnings
- **G-AIRMET** — Graphical AIRMETs (CONUS, replaced text AIRMETs in Jan 2025)
- **PIREP/AIREP** — Pilot reports and aircraft reports
- **CWA** — Center Weather Advisories
- **TFM Convective Forecast** — New in 2025
- **Station info** — Weather observation station metadata (worldwide)
- **Airport info** — Airport information (worldwide)
- **NAVAID/Fix/Feature/Obstacle** — Aviation navigation features (worldwide)

## API Details

OpenAPI spec: `https://aviationweather.gov/data/schema/openapi.yaml`

Key endpoints (all under `https://aviationweather.gov/api/data/`):

| Endpoint | Description | Output Formats | Verified |
|---|---|---|---|
| `/metar?ids=KJFK,EGLL&format=json` | METAR observations | raw, json, geojson, xml, csv, iwxxm | ✅ Live |
| `/taf?ids=KJFK&format=json` | TAF forecasts | raw, json, geojson, xml, iwxxm | ✅ Live |
| `/isigmet?format=json` | International SIGMETs | raw, json, geojson, xml, iwxxm | ✅ Live |
| `/airsigmet?format=json` | Domestic US SIGMETs | raw, json, geojson, xml, iwxxm | ✅ Live |
| `/gairmet?format=json` | Graphical AIRMETs | json, geojson, xml | ✅ |
| `/pirep?bbox=-90,30,-80,40&format=json` | Pilot reports | raw, json, geojson, xml | ✅ |
| `/stationinfo?ids=KJFK&format=json` | Station metadata | json, geojson, xml | ✅ |
| `/airport?ids=KJFK&format=json` | Airport information | json, geojson, xml | ✅ |

Query parameters:
- `ids` — Station/airport ICAO identifiers (comma-separated)
- `bbox` — Bounding box: `minLon,minLat,maxLon,maxLat`
- `format` — Output format (json, geojson, raw, xml, csv, iwxxm)
- `hours` — Hours back (METAR)
- `date` — Specific date/time
- `taf` — Include TAF with METAR (boolean)
- `hazard` — Filter SIGMETs by hazard type (conv, turb, ice, ifr)

Bulk cache files (gzipped, updated every 1-10 minutes):

| File | Content | Frequency |
|---|---|---|
| `/data/cache/metars.cache.csv.gz` | All current METARs | 1 min |
| `/data/cache/tafs.cache.xml.gz` | All current TAFs | 10 min |
| `/data/cache/airsigmets.cache.csv.gz` | All CONUS SIGMETs | 1 min |
| `/data/cache/gairmets.cache.xml.gz` | All G-AIRMETs | 1 min |
| `/data/cache/aircraftreports.cache.csv.gz` | All PIREPs/AIREPs | 1 min |

No authentication required for any endpoint.

## Sample Responses

METAR (JSON):
```json
{
  "icaoId": "KJFK",
  "obsTime": "2026-04-06T10:51:00Z",
  "temp": 5.0,
  "dewp": -5.0,
  "wdir": 320,
  "wspd": 13,
  "visib": 10,
  "altim": 30.01,
  "fltCat": "VFR",
  "clouds": [{"cover": "SCT", "base": 5000}, {"cover": "SCT", "base": 25000}],
  "rawOb": "KJFK 061051Z 32013KT 10SM SCT050 SCT250 05/M05 A3001 RMK AO2 SLP162 T00501050"
}
```

METAR (GeoJSON):
```json
{
  "type": "FeatureCollection",
  "features": [{
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [-73.76394, 40.63916]},
    "properties": {
      "id": "KJFK", "obsTime": "2026-04-06T10:51:00Z",
      "temp": 5.0, "dewp": -5.0, "wdir": 320, "wspd": 13,
      "visib": 10, "altim": 30.01, "fltcat": "VFR"
    }
  }]
}
```

International SIGMET (JSON):
```json
{
  "icaoId": "VOMM",
  "firId": "...",
  "firName": "...",
  "hazard": "TS",
  "qualifier": "EMBD",
  "validTimeFrom": "2026-04-06T07:15:00Z",
  "validTimeTo": "2026-04-06T11:15:00Z",
  "coords": [...],
  "rawSigmet": "..."
}
```

## Freshness Assessment

Outstanding. This is the authoritative aviation weather source — the same data that pilots
and dispatchers use for flight planning and in-flight decision making. METARs are cached
every minute, reflecting observations typically issued every 30-60 minutes per station (more
frequently with SPECIs). SIGMETs are updated within a minute of issuance.

The 2025 API redevelopment improved consistency and added GeoJSON output, making the data
significantly more useful for geospatial applications. The cache files provide efficient
bulk access to complete global datasets.

Verified live: 151 active international SIGMETs returned, 3 METAR stations queried
simultaneously, GeoJSON FeatureCollection output confirmed with point geometries.

## Entity Model

- **METAR**: icaoId, obsTime, temp, dewp, wdir, wspd, wgst, visib, altim, slp, fltCat,
  clouds[], cover, rawOb, receiptTime, reportTime, elev, lat, lon, name
- **TAF**: icaoId, issueTime, validTimeFrom, validTimeTo, rawTaf, forecast[]
- **SIGMET**: icaoId, firId, firName, hazard, qualifier, validTimeFrom, validTimeTo,
  coords[], base, top, dir, spd, rawSigmet
- **PIREP**: icaoId, obsTime, lat, lon, altitude, type, turbulence, icing, clouds
- **Station**: icaoId, iataId, name, state, country, lat, lon, elev

Identifiers: ICAO station codes (primary), IATA codes (airport lookup), WMO station numbers.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | Cache updates every 1 min, real-time observations |
| Openness | 3 | No auth, no registration, US government public domain |
| Stability | 3 | NOAA/NWS infrastructure, operational since decades, 2025 redevelopment |
| Structure | 3 | OpenAPI spec, GeoJSON/JSON/XML/CSV/IWXXM, well-documented |
| Identifiers | 3 | ICAO codes, IATA codes, WMO numbers |
| Additive Value | 2 | Aviation weather complements flight tracking — unique data type |

**Total: 17/18**

## Notes

- This is the single best open aviation data API available. No auth, global coverage,
  multiple output formats, proper OpenAPI spec, government-backed stability. The only reason
  it doesn't score 18/18 is that it's weather rather than novel — METAR/TAF are well-known.
- The GeoJSON output makes it trivial to overlay aviation weather on maps alongside flight
  tracking data from OpenSky or ADS-B Exchange.
- The cache files are the recommended approach for bulk access — they provide complete global
  datasets updated every minute without stressing the API.
- IWXXM (ICAO Meteorological Information Exchange Model) format is available for standards
  compliance use cases.
- Complements flight tracking sources: combine METAR/TAF with aircraft positions for
  weather-aware flight monitoring.
- The 2025 API redevelopment removed legacy `/cgi-bin/` paths — use `/api/data/` exclusively.
