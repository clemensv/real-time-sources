# Singapore NEA Air Quality (PSI & PM2.5)

**Country/Region**: Singapore
**Publisher**: National Environment Agency (NEA) via data.gov.sg
**API Endpoint**: `https://api.data.gov.sg/v1/environment/`
**Documentation**: https://data.gov.sg/collections/1395/view
**Protocol**: REST
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Hourly
**License**: Singapore Open Data Licence (permissive, attribution required)

## What It Provides

Singapore's National Environment Agency (NEA) publishes real-time air quality data via the data.gov.sg platform. The API provides the Pollutant Standards Index (PSI) and PM2.5 readings across five geographic regions of Singapore (North, South, East, West, Central). PSI sub-indices cover O₃, PM10, PM2.5, CO, SO₂, and NO₂. This is particularly relevant during Southeast Asian haze season (burning in Indonesia), when Singapore's air quality can deteriorate rapidly.

## API Details

- **Base URL**: `https://api.data.gov.sg/v1/environment/`
- **Key Endpoints**:
  - `GET /psi` — current PSI readings with all sub-indices by region
  - `GET /pm25` — current hourly PM2.5 readings by region
- **Query Parameters**: `date` (YYYY-MM-DD), `date_time` (ISO 8601) for historical queries
- **Regions**: west, east, central, south, north — each with label_location coordinates
- **Response Structure**: `{"region_metadata":[...],"items":[{"timestamp":...,"readings":{...}}],"api_info":{"status":"healthy"}}`
- **PSI Sub-indices**: o3_sub_index, pm10_sub_index, pm25_sub_index, co_sub_index, so2_sub_index, no2_one_hour_max, co_eight_hour_max, o3_eight_hour_max
- **Sample**: PSI 24h: `{"west":53,"east":49,"central":56,"south":44,"north":52}`

## Freshness Assessment

Data is updated hourly with the update timestamp included in the response (`update_timestamp`). The `api_info.status` field confirms API health. Historical queries by date are supported. Data latency is minimal (~1 minute after the hour).

## Entity Model

- **Region** → name (west/east/central/south/north), label_location (lat/lon)
- **PSI Reading** → timestamp, update_timestamp, readings (sub-indices per region)
- **PM2.5 Reading** → timestamp, pm25_one_hourly per region

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Hourly, ~1 min latency after the hour |
| Openness | 3 | No auth, open government data |
| Stability | 3 | Singapore government (data.gov.sg), well-maintained platform |
| Structure | 3 | Clean JSON, simple REST, self-documenting responses |
| Identifiers | 2 | Region-based only (5 regions, no individual station IDs) |
| Additive Value | 2 | Singapore-only; limited geographic granularity (5 zones) |
| **Total** | **16/18** | |

## Notes

- Extremely clean API — no auth, no pagination, instant responses, health status included.
- Only 5 geographic regions (not individual stations), so spatial resolution is coarse. Singapore is small (728 km²), so region-level data is still useful.
- Critical for haze monitoring: during trans-boundary haze events from Indonesian peat fires, PSI can exceed 300 (hazardous).
- The `date` parameter enables historical queries, useful for trend analysis.
- data.gov.sg also provides UV index and weather endpoints with the same pattern.
- Already partially covered by AQICN/WAQI, but the direct API provides sub-index granularity not available elsewhere.
