# BarentsWatch AIS Live API

**Country/Region**: Norway
**Publisher**: BarentsWatch (Norwegian Coastal Administration / Kystverket data)
**API Endpoint**: `https://live.ais.barentswatch.no/live/v1/latest/ais`
**Documentation**: https://live.ais.barentswatch.no/ (OpenAPI/Swagger), https://developer.barentswatch.no/docs/appreg
**Protocol**: REST (JSON streaming)
**Auth**: OAuth2 client_credentials (free registration at barentswatch.no)
**Data Format**: JSON, GeoJSON
**Update Frequency**: Real-time streaming (messages arrive as they come from shore stations)
**License**: NLOD (Norwegian Licence for Open Government Data)

## What It Provides

Real-time AIS data for Norwegian waters, sourced from Kystverket (Norwegian Coastal Administration)
shore-based AIS stations. This is the same underlying data as the kystverket-ais raw TCP feed, but
exposed through a modern, structured REST/JSON streaming API.

AIS message types supported:
- **Position reports** (AIS types 1, 2, 3, 9, 18, 19, 27): lat/lon, SOG, COG, heading, ROT, nav status
- **Static and voyage data** (AIS types 5, 24): vessel name, callsign, IMO, ship type, dimensions, destination, ETA, draught
- **Binary Broadcast MetHyd** (AIS type 8): meteorological/hydrological data
- **Aids-to-Navigation** (AIS type 21): AtoN reports

## API Details

OpenAPI spec at: `https://live.ais.barentswatch.no/live/openapi/ais/openapi.json`

Key endpoints:

| Endpoint | Method | Description |
|---|---|---|
| `/v1/latest/ais` | GET | Latest AIS messages per MMSI (within 24h) |
| `/v1/latest/ais` | POST | Same, with filter body (MMSI list, geometry, etc.) |
| `/v1/latest/combined` | GET | Combined position + static data per vessel |
| `/v1/sse/...` | GET | Server-Sent Events streams |

The `/latest/combined` endpoint supports multiple output formats via query params:
- `modelType`: Full or Simple
- `modelFormat`: JSON list, GeoJSON features, or FeatureCollection

Authentication flow:
1. Register at https://www.barentswatch.no/minside/
2. Create an AIS-API client (self-service)
3. POST to `https://id.barentswatch.no/connect/token` with `client_credentials` grant, scope `ais`
4. Use returned bearer token in Authorization header

Example token request:
```bash
curl -X POST --header "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=YOUR_ID&scope=ais&client_secret=YOUR_SECRET&grant_type=client_credentials" \
  https://id.barentswatch.no/connect/token
```

Downsampling is supported on some endpoints (max one message per minute per MMSI).

## Freshness Assessment

Excellent. This is a live streaming API backed by the Norwegian shore-based AIS network. Messages
arrive in near-real-time as they are received by Kystverket stations. The "latest" endpoints
return the most recent message per MMSI within the last 24 hours, so the data is always fresh.
The `since` query parameter allows polling for only new updates since a given timestamp.

## Entity Model

Position message fields:
- `mmsi`, `msgtime`, `latitude`, `longitude`, `sog` (speed over ground), `cog` (course over ground)
- `heading`, `rot` (rate of turn), `navstat` (navigational status)

Static data fields:
- `mmsi`, `name`, `callsign`, `imo`, `shipType`, `destination`, `eta`, `draught`
- `shipLength`, `shipWidth`, `dimensionA/B/C/D`

Combined endpoint merges both into a single object per vessel.

Identifiers: MMSI (primary), IMO, callsign.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | Real-time streaming from shore stations |
| Openness | 2 | Free registration required, NLOD license |
| Stability | 3 | Government-backed, operational since years, used by NAIS |
| Structure | 3 | OpenAPI spec, clean JSON/GeoJSON, well-documented |
| Identifiers | 3 | MMSI, IMO, callsign all present |
| Additive Value | 2 | Same data source as kystverket-ais, but vastly better API surface |

**Total: 16/18**

## Notes

- This wraps the SAME Norwegian AIS data already available via kystverket-ais raw TCP, but in a
  dramatically more developer-friendly form. The raw TCP feed requires NMEA parsing; this API
  delivers structured JSON.
- Could potentially replace the kystverket-ais integration entirely, or serve as a complementary
  structured access path.
- The SSE (Server-Sent Events) endpoints enable push-based real-time streaming without WebSocket complexity.
- Coverage is Norwegian waters only (shore-based terrestrial AIS range).
- The API is actively maintained — it powers the official NAIS (https://nais.kystverket.no) vessel
  traffic application.
