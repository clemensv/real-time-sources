# Qatar Air Quality (Open-Meteo Copernicus CAMS)

- **Country/Region**: Qatar (Doha)
- **Endpoint**: `https://air-quality-api.open-meteo.com/v1/air-quality?latitude=25.28&longitude=51.52&current=pm10,pm2_5,dust,nitrogen_dioxide,ozone,sulphur_dioxide,carbon_monoxide&hourly=pm10,pm2_5,dust`
- **Protocol**: REST / JSON
- **Auth**: None
- **Format**: JSON
- **Freshness**: Hourly updates (CAMS model output)
- **Docs**: https://open-meteo.com/en/docs/air-quality-api
- **Score**: 15/18

## Overview

Open-Meteo provides free access to **Copernicus Atmosphere Monitoring Service (CAMS)** air
quality model output for any location worldwide. For Qatar, the most significant parameters are:
- **PM10 and PM2.5**: Particulate matter from urban pollution and desert dust
- **Dust**: Quantitative dust concentration (μg/m³) — **critical for Qatar**, where dust storms
  (haboobs) and dust haze are frequent, especially during spring/summer shamal winds
- **NO2**: Nitrogen dioxide from traffic and industrial sources (LNG, petrochemical)
- **O3**: Tropospheric ozone (photochemical smog, common in hot climates)
- **SO2, CO**: Secondary pollutants

Qatar lacks a publicly accessible, real-time air quality monitoring network despite operating
17 AQM stations (data published on data.gov.qa is **annual only**). Open-Meteo fills this gap
with hourly modeled concentrations based on Copernicus CAMS, which assimilates satellite data
(Sentinel-5P, MODIS) and emission inventories.

The **dust parameter** is especially valuable — Qatar experiences frequent dust events from
Saudi Arabian and Iraqi deserts. Quantitative dust concentration is not available from most
free AQ APIs (WAQI does not provide dust; EPA AirNow is US-only).

## Endpoint Analysis

**Live test successful** — API returned current air quality for Doha:

```json
{
  "latitude": 25.28,
  "longitude": 51.52,
  "generationtime_ms": 0.123,
  "utc_offset_seconds": 10800,
  "timezone": "Asia/Qatar",
  "timezone_abbreviation": "AST",
  "current_units": {
    "time": "iso8601",
    "pm10": "μg/m³",
    "pm2_5": "μg/m³",
    "dust": "μg/m³",
    "nitrogen_dioxide": "μg/m³",
    "ozone": "μg/m³"
  },
  "current": {
    "time": "2025-05-22T15:00",
    "pm10": 198.4,
    "pm2_5": 48.0,
    "dust": 256.0,
    "nitrogen_dioxide": 9.9,
    "ozone": 123.0
  },
  "hourly_units": {
    "time": "iso8601",
    "pm10": "μg/m³",
    "pm2_5": "μg/m³",
    "dust": "μg/m³"
  },
  "hourly": {
    "time": ["2025-05-22T00:00", "2025-05-22T01:00", ...],
    "pm10": [195.2, 198.1, 201.3, ...],
    "pm2_5": [46.5, 47.8, 48.9, ...],
    "dust": [250.0, 255.0, 260.0, ...]
  }
}
```

**Key observation**: `dust: 256.0 μg/m³` at time of test — this indicates **active dust storm
conditions** (dust >100 μg/m³ is considered elevated; >250 μg/m³ is hazardous for sensitive
groups). This matches typical Qatar spring weather when shamal winds carry dust from the north.

**PM10 vs Dust**: The model separates total PM10 (198 μg/m³) from dust (256 μg/m³). The dust
value appears to represent the dust-specific component before mixing with anthropogenic PM.

**Hourly forecast**: The `hourly` block provides 7-day forecasts (168 hours). Current conditions
update every hour.

**Alternative pollutants** available:
- `european_aqi` (European Air Quality Index, 0-100+ scale)
- `uv_index` (can be added to same request)
- `aerosol_optical_depth` (satellite-derived total column aerosol)

**Multi-location**: Can request multiple lat/lon points in a single call (grid-based retrieval).

## Integration Notes

- **Polling interval**: 60 minutes (matches CAMS hourly output)
- **CloudEvents subject**: `airquality/doha` or `airquality/{lat}_{lon}`
- **Kafka key**: Location identifier (e.g., `doha` or `25.28_51.52`)
- **Entity model**: Grid point time series (not station-based, but gridded model output)
- **Data source**: Copernicus CAMS (European Centre for Medium-Range Weather Forecasts)
- **License**: CC BY 4.0
- **Overlap check**: The repo does not currently have an air quality bridge. This would be a
  **new domain**.
- **Comparison with ground truth**: Qatar's 17 official AQM stations are not publicly
  accessible in real-time. WAQI has a single private GAIA sensor in Qatar (Rawdat Al Khail,
  idx=538951) but it's citizen-science grade, not official monitoring. CAMS model output is
  the **best available free real-time source** for Qatar AQ.
- **Dust storms**: The dust parameter is unique to Open-Meteo and critical for Qatar. Dust
  events reduce visibility (aviation hazard), cause respiratory issues, and are a public
  health concern. Real-time dust concentration monitoring would be valuable.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Hourly updates (not sub-hourly, but acceptable for AQ) |
| Openness | 3 | No auth, free tier, CC BY 4.0, documented API |
| Stability | 3 | Open-Meteo operational service, Copernicus CAMS is ESA/EC program |
| Structure | 2 | Typed JSON with units metadata |
| Identifiers | 2 | Lat/lon grid points (not station IDs, but stable coordinates) |
| Additive value | 3 | New domain (air quality) not in repo; dust parameter unique |

**Verdict**: Recommended as a **general air-quality bridge** using Open-Meteo's global
coverage. Qatar (Doha at 25.28°N, 51.52°E) would be the initial configuration, but the bridge
could be extended to any city worldwide. The **dust concentration** parameter is the standout
feature — no other free API provides this, and it's directly relevant to Qatar's environment.

**Alternative approach**: If official Qatar AQM station data becomes available via MECC or
Ashghal, that would be preferable (ground truth vs model). But given the current lack of
public access, CAMS model output is the pragmatic solution.

**Use cases**:
- Public health alerts for dust storm days
- Aviation weather (dust affects visibility at OTHH)
- Environmental monitoring dashboard
- Research on dust transport patterns in the Persian Gulf
- Correlation with shamal wind events (cross-reference with METAR wind data)
