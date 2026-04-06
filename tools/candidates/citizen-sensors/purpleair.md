# PurpleAir

**Country/Region**: Global (strongest in North America)
**Publisher**: PurpleAir, Inc.
**API Endpoint**: `https://api.purpleair.com/v1/sensors`
**Documentation**: https://api.purpleair.com (Swagger UI), https://community.purpleair.com/t/about-the-purpleair-api/7145
**Protocol**: REST
**Auth**: API Key required (free, from https://develop.purpleair.com)
**Data Format**: JSON
**Update Frequency**: ~2 minutes (sensors report every 2 minutes)
**License**: Proprietary (free for non-commercial research use with API key)

## What It Provides

PurpleAir operates a global network of low-cost air quality sensors focusing on PM2.5 measurements using laser particle counters. With over 30,000 sensors worldwide, it provides one of the densest real-time air quality monitoring networks. The API exposes current and historical readings including PM1.0, PM2.5, PM10, temperature, humidity, pressure, and air quality index values.

## API Details

- **List sensors**: `GET /v1/sensors` — bulk query with field selection
- **Single sensor**: `GET /v1/sensors/{sensor_index}` — detailed current reading
- **Historical**: `GET /v1/sensors/{sensor_index}/history` — time-series data
- **Group sensors**: `GET /v1/groups/{group_id}/members` — organizational grouping
- **Authentication**: `X-API-Key` header (read key for public data, write key for owned sensors)
- **Key fields**: `sensor_index`, `name`, `latitude`, `longitude`, `altitude`, `pm2.5`, `pm2.5_10minute`, `pm2.5_30minute`, `pm2.5_60minute`, `temperature`, `humidity`, `pressure`, `last_seen`, `confidence`, `model`
- **Bounding box filter**: `nwlat`, `nwlng`, `selat`, `selng` parameters
- **Field selection**: `fields` parameter to reduce payload (e.g., `fields=name,latitude,longitude,pm2.5`)
- **Rate limiting**: 1 request/minute for sensor list; higher for individual sensors

## Freshness Assessment

Sensors report every 2 minutes. The API reflects the latest readings with minimal delay. Real-time averages (2-minute, 10-minute, 30-minute, 60-minute) are pre-computed. API rate limiting constrains polling frequency but 2-minute cycles align with sensor reporting.

## Entity Model

- **Sensor**: `sensor_index` (integer, globally unique), with name, location, model, firmware
- **Channel**: Each sensor has A/B channels (dual laser counters for confidence scoring)
- **Reading**: Current values at last report time, plus rolling averages
- **Group**: Organizational grouping of sensors by owner/project

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 2-minute sensor reporting cycle |
| Openness | 1 | API key required; proprietary license |
| Stability | 3 | Well-funded commercial product, stable API |
| Structure | 3 | Clean REST API with Swagger docs |
| Identifiers | 3 | Stable integer sensor indices |
| Additive Value | 2 | Overlaps with Sensor.Community but denser in North America |
| **Total** | **15/18** | |

## Notes

- API key is free but requires registration at develop.purpleair.com.
- The dual-channel design (A/B lasers) enables confidence scoring — sensors with divergent A/B readings may be flagged.
- EPA correction factors are commonly applied to PurpleAir PM2.5 readings to align with reference monitors.
- PurpleAir data is widely used by US government agencies (EPA AirNow Fire and Smoke Map).
- Historical data is available but may be rate-limited.
- Commercial use requires a separate licensing agreement.
