# WAQI / AQICN — African Air Quality Stations

- **Country/Region**: Pan-African (stations in South Africa, Kenya, Nigeria, Egypt, Morocco, Ghana, Uganda, Ethiopia, Rwanda, Senegal, Tunisia)
- **Endpoint**: `https://api.waqi.info/feed/{city}/?token={token}`
- **Protocol**: REST
- **Auth**: API token (free registration)
- **Format**: JSON
- **Freshness**: Real-time (hourly updates)
- **Docs**: https://aqicn.org/json-api/doc/
- **Score**: 13/18

## Overview

The World Air Quality Index (WAQI/AQICN) project aggregates air quality data from
government and institutional monitoring stations worldwide. It provides a unified AQI
scale and real-time data access for stations across Africa.

African stations are sourced from:
- US Embassy/Consulate air quality monitors (most reliable)
- National environmental agencies (South Africa SAAQIS, Egypt, Morocco)
- Research institutions and NGOs
- Low-cost sensor networks (PurpleAir, Clarity)

The demo token returns fallback data (Shanghai), but authenticated requests with a proper
token return actual station data.

## Endpoint Analysis

**Probed with demo token** — the demo token does not properly route to African cities
(returns Shanghai as fallback). This is a known limitation of the demo token.

Authenticated API endpoints:
```
# Single station by city name
GET /feed/nairobi/?token={TOKEN}

# Station by ID
GET /feed/@{station_id}/?token={TOKEN}

# Stations in bounding box (Africa)
GET /map/bounds/?latlng=-35,-20,37,55&token={TOKEN}

# Station search
GET /search/?keyword=nairobi&token={TOKEN}
```

Expected response structure:
```json
{
  "status": "ok",
  "data": {
    "aqi": 85,
    "city": {"name": "Nairobi US Embassy"},
    "iaqi": {
      "pm25": {"v": 85},
      "pm10": {"v": 42},
      "o3": {"v": 12},
      "no2": {"v": 8},
      "t": {"v": 22},
      "h": {"v": 65}
    },
    "time": {"iso": "2026-04-06T18:00:00+03:00"}
  }
}
```

Known African stations (from AQICN map):
- Nairobi US Embassy, Kenya
- Lagos US Consulate, Nigeria
- Kampala US Embassy, Uganda
- Addis Ababa US Embassy, Ethiopia
- Dar es Salaam US Embassy, Tanzania
- Johannesburg, South Africa (multiple stations)
- Cairo, Egypt (multiple stations)
- Casablanca, Morocco
- Tunis, Tunisia
- Dakar US Embassy, Senegal
- Accra US Embassy, Ghana
- Kigali US Embassy, Rwanda

## Integration Notes

- **Token required**: Register at https://aqicn.org/data-platform/token/ for a free
  API token. The demo token is unreliable for specific city queries.
- **Bounding box approach**: Use the `/map/bounds/` endpoint to discover all African
  stations, then poll individual stations for latest data.
- **US Embassy dominance**: In many African capitals, the US Embassy monitor is the only
  reliable reference-grade AQ station. These use BAM-1020 PM2.5 monitors.
- **Complement with OpenAQ**: OpenAQ provides the same underlying data but with a
  different API structure. Use both for redundancy.
- **AQI conversion**: WAQI provides pre-calculated AQI values. For raw concentrations,
  use the `iaqi` object.
- **Polling frequency**: Hourly is sufficient — most stations report hourly.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Hourly updates |
| Openness | 2 | Free token required |
| Stability | 2 | Community project, generally reliable |
| Structure | 2 | JSON API, demo token quirks |
| Identifiers | 2 | WAQI station IDs |
| Richness | 2 | AQI, PM2.5, PM10, gases, temperature |
