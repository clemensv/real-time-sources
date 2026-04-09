# PurpleAir Real-Time Air Quality Sensors

- **Country/Region**: Global (dense coverage in US Pacific Northwest / Puget Sound)
- **Publisher**: PurpleAir, Inc.
- **Endpoint**: `https://api.purpleair.com/v1/sensors`
- **Protocol**: REST
- **Auth**: API Key (free registration at develop.purpleair.com)
- **Format**: JSON
- **Freshness**: Real-time (2-minute sensor intervals)
- **Docs**: https://develop.purpleair.com/
- **Score**: 15/18

## Overview

PurpleAir operates a global network of low-cost PM2.5 air quality sensors, with exceptionally dense coverage in the Seattle/Puget Sound area (hundreds of sensors). Unlike EPA AirNow's ~dozen regulatory monitors in the region, PurpleAir provides hyper-local, real-time air quality readings every 2 minutes. This is invaluable for a free-time advisor: during wildfire smoke events, air quality can vary dramatically between neighborhoods, and PurpleAir captures this granularity.

## API Details

**Base URL:** `https://api.purpleair.com/v1/`

**Authentication:** `X-API-Key: {your_key}` header

**Key Endpoints:**

| Endpoint | Description |
|----------|-------------|
| `GET /sensors` | Query sensors with filters |
| `GET /sensors/{sensor_index}` | Single sensor data |
| `GET /sensors/{sensor_index}/history` | Historical data |

**Bounding Box Query for Puget Sound:**
```
GET /sensors?fields=sensor_index,name,latitude,longitude,pm2.5_cf_1,temperature,humidity,last_seen
  &location_type=0
  &max_age=3600
  &nwlat=48.0&nwlng=-122.8
  &selat=47.1&selng=-122.0
```

**Parameters:**
- `fields` — Comma-separated field list (controls response size and API point cost)
- `location_type` — 0=outdoor, 1=indoor
- `max_age` — Maximum seconds since last update (3600 = last hour)
- `nwlat/nwlng/selat/selng` — Bounding box coordinates

**Available Fields (subset):**
- `pm2.5_cf_1` — PM2.5 concentration (µg/m³)
- `pm10.0` — PM10 concentration
- `temperature` — Sensor temperature (°F)
- `humidity` — Relative humidity (%)
- `pressure` — Atmospheric pressure
- `voc` — Volatile organic compounds (some sensors)
- `ozone1` — Ozone (some sensors)
- `last_seen` — Unix timestamp of last reading

**Rate Limits:** Varies by plan; free tier allows reasonable developer use.

## Freshness Assessment

Excellent. Individual sensors report every 2 minutes. The API returns the latest reading with a `last_seen` timestamp. With `max_age=3600`, you get all sensors that have reported in the last hour. During smoke events, this near-real-time granularity is critical.

## Entity Model

- **Sensor** — sensor_index (numeric), name, location (lat/lon), type (indoor/outdoor)
- **Reading** — PM2.5, PM10, temperature, humidity, pressure, VOC, ozone, timestamp
- **Channel** — Sensors have A and B channels for quality validation
- **Group** — Optional sensor groupings

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | 2-minute intervals, truly real-time |
| Openness | 2 | Free API key required; point-based usage accounting |
| Stability | 2 | Private company; API has changed versions (v0→v1) |
| Structure | 3 | Well-designed REST API with field selection |
| Identifiers | 3 | Stable sensor_index IDs, structured fields |
| Additive Value | 2 | Hyper-local air quality; complements EPA AirNow candidate |
| **Total** | **15/18** | |

## Notes

- PurpleAir data is **not EPA-quality** — sensors are low-cost and can drift. The Puget Sound Clean Air Agency (PSCAA) applies calibration corrections. Raw data should be interpreted with correction factors.
- Dense Puget Sound coverage makes this uniquely valuable for neighborhood-level air quality.
- Existing `sensor-community` bridge in the repo covers a similar citizen-sensor pattern; PurpleAir integration could follow a similar architecture.
- API "points" system means careful field selection matters for cost management.
- Community libraries: `aiopurpleair` (Python async), R package available.
- PSCAA does NOT have its own public API — PurpleAir is the best programmatic path to hyper-local Puget Sound air quality.
