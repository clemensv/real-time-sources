# OpenAQ

**Country/Region**: Global
**Publisher**: OpenAQ (non-profit)
**API Endpoint**: `https://api.openaq.org/v3/`
**Documentation**: https://docs.openaq.org/
**Protocol**: REST
**Auth**: API Key (free registration at explore.openaq.org/register, passed via `X-API-Key` header)
**Data Format**: JSON
**Update Frequency**: Near real-time (varies by source; typically hourly)
**License**: CC BY 4.0 (data); varies by upstream source

## What It Provides

OpenAQ is the world's largest open air quality data aggregator, ingesting government-grade monitoring data and low-cost sensor data from 130+ countries. It normalizes heterogeneous sources into a single schema covering PM2.5, PM10, O₃, NO₂, SO₂, CO, and BC (black carbon). The platform aggregates from national EPAs (US AirNow, EEA, CPCB India, etc.) as well as community networks like PurpleAir and Sensor.Community.

## API Details

- **Base URL**: `https://api.openaq.org/v3/`
- **Key Endpoints**:
  - `GET /v3/locations` — list monitoring locations with metadata, coordinates, sensors
  - `GET /v3/locations/{id}` — single location detail
  - `GET /v3/locations/{id}/sensors` — sensors at a location
  - `GET /v3/locations/{id}/latest` — most recent measurement per sensor
  - `GET /v3/sensors/{id}/measurements` — time-series measurements
  - `GET /v3/countries` — list countries
  - `GET /v3/parameters` — list measured parameters
  - `GET /v3/providers` — list upstream data providers
- **Pagination**: Cursor-based with `limit` and `page` params (max 1000 per page)
- **Rate Limits**: Free tier limited; higher tiers available
- **Bulk**: Historical archive available on AWS S3 Open Data

## Freshness Assessment

Data freshness depends on the upstream source. Government monitors typically update hourly. Low-cost sensors (PurpleAir) can be near real-time (~2 min). The `datetimeLast` field on each location indicates last observation time.

## Entity Model

- **Country** → has many **Locations**
- **Location** → has coordinates, provider, owner, licenses, instruments
- **Location** → has many **Sensors**
- **Sensor** → has **Parameter** (pm25, pm10, o3, no2, so2, co, bc)
- **Sensor** → produces **Measurements** (value + timestamp)

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Hourly to near-real-time depending on source |
| Openness | 3 | CC BY 4.0, free API key |
| Stability | 3 | Well-funded non-profit, v3 API, AWS archival |
| Structure | 3 | Excellent normalized JSON, OpenAPI spec |
| Identifiers | 3 | Stable numeric IDs for locations, sensors, parameters |
| Additive Value | 3 | Global aggregator — one API for 130+ countries |
| **Total** | **18/18** | |

## Notes

- OpenAQ is the meta-source — it aggregates many of the other APIs in this list (AirNow, EEA, CPCB, etc.). Using OpenAQ alone could cover a vast portion of the air quality domain.
- The v3 API (current) requires an API key; the older v2 API is being deprecated.
- Historical data is available via AWS S3 in Parquet format for bulk analysis.
- OpenAQ also provides license metadata per location, which is unusual and valuable for downstream compliance.
