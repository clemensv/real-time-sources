# Netatmo Weather API — Citizen Weather Station Network

**Country/Region**: Global (strongest coverage in Western Europe)
**Publisher**: Netatmo (Legrand Group)
**API Endpoint**: `https://api.netatmo.com/api/getpublicdata`
**Documentation**: https://dev.netatmo.com/apidocumentation/weather
**Protocol**: REST API (OAuth 2.0)
**Auth**: OAuth 2.0 (requires app registration + user consent flow)
**Data Format**: JSON
**Update Frequency**: 5–10 minutes (station reports)
**License**: Proprietary / Netatmo Terms of Service

## What It Provides

Netatmo operates one of the world's largest citizen weather station networks. Their personal weather stations report to the Netatmo cloud, and a subset of this data is available through their public API:

- **Public Weather Data** (`getpublicdata`): Real-time observations from Netatmo personal weather stations within a geographic area. Parameters include:
  - Temperature (indoor and outdoor)
  - Humidity
  - Atmospheric pressure
  - Rain gauge readings (accumulated and hourly)
  - Wind speed and gust (from wind gauge add-on)
  - Noise level (indoor)

- **Geographic Coverage**: Wherever Netatmo stations are deployed — densest in:
  - Western Europe (France, Germany, UK, Netherlands, Belgium)
  - North America (urban areas)
  - Increasingly worldwide

- **Station Density**: In dense European cities, station spacing can be as close as every few hundred meters — far denser than any official met service network.

## API Details

The public data endpoint queries stations within a bounding box:
```
GET https://api.netatmo.com/api/getpublicdata?lat_ne=49.0&lon_ne=2.5&lat_sw=48.7&lon_sw=2.2&filter=true
```

Authentication requires OAuth 2.0:
1. Register an application at dev.netatmo.com.
2. Implement OAuth 2.0 authorization flow (or use client credentials for personal access).
3. Include bearer token in requests.

The API returns station locations and latest readings. Data quality varies as these are consumer-grade instruments installed by non-professionals.

Rate limits apply (not clearly documented — estimated at ~500 requests/hour for the public data endpoint).

## Freshness Assessment

- Stations report every 5–10 minutes.
- Data availability depends on individual station uptime (personal devices may go offline).
- No guaranteed SLA — stations may appear and disappear.
- In practice, dense urban areas have sufficient redundancy that coverage is reliable.

## Entity Model

- **Station**: MAC-address-based unique identifier (anonymized in public data).
- **Module**: Sensor modules (outdoor, rain gauge, wind gauge, indoor).
- **Measurement**: Value + timestamp per module per parameter.
- **Location**: Approximate lat/lon (randomized slightly for privacy).

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 5–10 minute updates from all active stations |
| Openness | 1 | OAuth 2.0 required, proprietary terms, rate-limited |
| Stability | 2 | Commercial company (Legrand Group), but API terms could change |
| Structure | 2 | JSON API, but OAuth complexity and varying data availability |
| Identifiers | 1 | Anonymized station IDs, no standard meteorological identifiers |
| Additive Value | 3 | Unprecedented station density in urban areas; citizen science network |
| **Total** | **12/18** | |

## Notes

- The station density is Netatmo's killer feature — in Paris or London, you can get neighborhood-level weather readings every 5 minutes from hundreds of stations.
- Data quality is a concern. Consumer instruments are not calibrated to WMO standards, station siting varies wildly (rooftops, balconies, gardens, sheltered locations), and there's no quality control.
- The Netatmo Weathermap (weathermap.netatmo.com) provides a visual interface to the same data.
- OAuth 2.0 is a heavier auth requirement than API-key approaches. The client credentials flow simplifies this for server-to-server use.
- Privacy: Station locations are slightly randomized, and station owners can opt out of public sharing.
- Useful as a supplementary data source alongside official met service data, not as a primary source.
- Competing citizen weather platforms: Weather Underground, Weathercloud — Netatmo's advantage is the unified hardware platform and API.
