# BOM — Bureau of Meteorology (Australia)

**Country/Region**: Australia
**Publisher**: Bureau of Meteorology (BOM)
**API Endpoint**: `http://reg.bom.gov.au/fwo/` (observations), `ftp://ftp.bom.gov.au/anon/gen/` (FTP)
**Documentation**: https://www.bom.gov.au/catalogue/data-feeds.shtml
**Protocol**: HTTP file polling (JSON, XML) and Anonymous FTP
**Auth**: None (anonymous access for web and FTP)
**Data Format**: JSON, XML (BOM schema), plain text, GeoTIFF, JPG (satellite/radar images)
**Update Frequency**: Half-hourly observations (72-hour history), 5-minute radar, 10-minute satellite
**License**: Crown Copyright — free for non-commercial use; commercial use requires Registered User agreement

## What It Provides

The Bureau of Meteorology provides extensive real-time weather data through anonymous web and FTP services:

- **Station observations (JSON/XML)**: 72-hour historical observations for individual weather stations, updated every 30 minutes. Rich parameter set including:
  - Air temperature, apparent temperature, dew point
  - Relative humidity, delta-T
  - Wind speed/direction/gust (km/h and knots)
  - Pressure (QNH, MSL, station-level), pressure tendency
  - Rain trace, cloud cover/type/base height/oktas
  - Visibility, sea state, swell direction/height/period

- **State/territory observation summaries**: XML summaries for all stations in each state, updated every 10 minutes.

- **Forecasts**: State forecasts, city forecasts, precis forecasts, district forecasts, coastal waters forecasts — all via FTP in text and XML.

- **Warnings**: RSS feeds for state-based weather warnings, national warnings summary page.

- **Radar**: 5-minute radar images for individual radars with static overlays.

- **Satellite**: Himawari-9 imagery every 10 minutes in JPG and GeoTIFF.

- **UV Index**: UV forecasts and sun protection times.

## API Details

The observation JSON endpoint follows a predictable URL pattern:
```
http://reg.bom.gov.au/fwo/{product_id}/{product_id}.{wmo_station_id}.json
```

Example: `http://reg.bom.gov.au/fwo/IDN60901/IDN60901.94767.json` returns Sydney Airport observations.

The JSON response includes:
- `observations.header`: Product metadata, refresh time, station name/state
- `observations.data`: Array of observation records sorted by time (newest first), with ~48 entries (30-min intervals over 72 hours)

Each observation record contains ~30 fields including WMO station number, timestamps (local and UTC), and all meteorological parameters.

FTP access at `ftp://ftp.bom.gov.au/anon/gen/` provides forecasts, warnings, and other products organized by product type.

## Freshness Assessment

- Station observations: New data every 30 minutes, with half-hourly and hourly reporting.
- The probed endpoint (`IDN60901.94767.json`) returned fresh data timestamped within the last 30 minutes.
- Radar: Every 5 minutes per radar.
- Satellite: Every 10 minutes.
- State observation summaries: Every 10 minutes.

## Entity Model

- **Station**: WMO station number (e.g., 94767 = Sydney Airport), with name, state, lat/lon
- **Product**: Identified by product code (e.g., IDN60901 = NSW capital city observations)
- **Observation**: Timestamped record with ~30 parameters, `sort_order` for sequencing
- **Forecast area**: State/territory/district/city hierarchy

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 30-min observations, 5-min radar, 10-min satellite |
| Openness | 2 | Free anonymous access for non-commercial; commercial needs registration |
| Stability | 3 | National government agency, established data feeds |
| Structure | 3 | Clean JSON with consistent schema, well-organized product hierarchy |
| Identifiers | 3 | WMO station numbers, stable product codes |
| Additive Value | 3 | Sole authoritative source for Australian weather; Southern Hemisphere coverage |
| **Total** | **17/18** | |

## Notes

- The JSON observation format is exceptionally well-structured — one of the cleanest raw weather data feeds available.
- Each JSON record contains both metric and knot-based wind measurements, both local and UTC timestamps.
- The `reg.bom.gov.au` subdomain is the registered user gateway but works for anonymous JSON access too.
- BOM explicitly states they cannot track anonymous usage, so they can't notify of service changes.
- The product code system is well-documented: `ID{state}{product_type}` pattern.
- No CORS headers on JSON endpoints — server-side fetching required for web applications.
- Commercial use requires a Registered User Services agreement.
