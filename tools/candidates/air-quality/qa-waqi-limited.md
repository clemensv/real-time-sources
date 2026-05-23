# WAQI Qatar Air Quality (Limited Coverage)

- **Country/Region**: Qatar
- **Endpoint**: `https://api.waqi.info/feed/geo:25.28;51.52/?token={API_KEY}`
- **Protocol**: REST / JSON
- **Auth**: Free API key required (registration at aqicn.org)
- **Format**: JSON
- **Freshness**: Hourly updates (for official stations); varies for citizen sensors
- **Docs**: https://aqicn.org/api/
- **Score**: 6/18

## Overview

The **World Air Quality Index (WAQI)** project aggregates air quality data from over 130
countries, including official government monitoring stations and citizen-science sensors
(PurpleAir, Sensor.Community). The service provides a free API with a registration-required
key (generous limits: 1000 requests/minute).

**For Qatar**, WAQI coverage is **extremely limited**:
- **Zero official government stations** indexed (Qatar's 17 MECC AQM stations are not published to WAQI)
- **One citizen-science sensor** detected: GAIA private sensor at "Rawdat Al Khail" (idx=538951)
- **Feed quality**: The single sensor is not representative of Qatar-wide air quality

**Discovery method**:
```
GET https://api.waqi.info/feed/geo:25.28;51.52/?token={API_KEY}
```

Returns nearest station to Doha coordinates (25.28°N, 51.52°E).

**Alternative endpoint**:
```
GET https://api.waqi.info/search/?token={API_KEY}&keyword=qatar
```

Search for all stations containing "qatar" keyword.

## Endpoint Analysis

**Probe result**: API requires registration (free) and returns limited data for Qatar.

**Expected JSON structure** (based on WAQI docs, not live-tested without key):
```json
{
  "status": "ok",
  "data": {
    "aqi": 87,
    "idx": 538951,
    "attributions": [
      {
        "url": "https://gaia.org/",
        "name": "GAIA Air Quality Monitoring Stations"
      }
    ],
    "city": {
      "geo": [25.35, 51.48],
      "name": "Rawdat Al Khail, Qatar",
      "url": "https://aqicn.org/city/qatar/rawdat-al-khail"
    },
    "dominentpol": "pm25",
    "iaqi": {
      "pm25": {"v": 87},
      "pm10": {"v": 125},
      "t": {"v": 36.5},
      "h": {"v": 48}
    },
    "time": {
      "s": "2025-05-22 14:00:00",
      "tz": "+03:00",
      "v": 1779522000
    }
  }
}
```

**Key fields**:
- `aqi`: Air Quality Index (0-500 scale, US EPA standard)
- `idx`: Station identifier (unique)
- `dominentpol`: Dominant pollutant (pm25, pm10, o3, no2, etc.)
- `iaqi`: Individual pollutant measurements (PM2.5, PM10, temperature, humidity)
- `city.geo`: Station lat/lon
- `time.v`: Unix timestamp of measurement

**Polling**: Hourly updates for most stations.

## Integration Notes

- **Polling interval**: 60 minutes (hourly data for most stations)
- **CloudEvents subject**: `airquality/{station_id}` → `airquality/538951`
- **Kafka key**: `idx` (station ID)
- **Entity model**: Air quality station time series
- **Auth requirement**: Free API key (registration at aqicn.org, limits: 1000 req/min)
- **Overlap check**: The repo does not have a WAQI bridge. However, **Open-Meteo air quality**
  provides Qatar coverage via Copernicus CAMS model with **no auth required** and broader
  parameter coverage (includes dust concentration, which WAQI does not provide).
- **Qatar coverage problem**: **One citizen sensor** is not sufficient for Qatar-wide air
  quality monitoring. Qatar's 17 official MECC stations are not indexed in WAQI.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Hourly updates (acceptable for AQ) |
| Openness | 1 | Free but requires API key (1000 req/min limit is generous) |
| Stability | 2 | WAQI operational for years, but single-sensor coverage is fragile |
| Structure | 2 | Typed JSON with schema |
| Identifiers | 2 | Station IDs are stable |
| Additive value | -3 | One sensor only; Open-Meteo CAMS is superior (no auth, full coverage, includes dust) |

**Verdict**: **Not recommended** for Qatar due to:
1. **Insufficient coverage** (one citizen sensor vs 17 official stations)
2. **Auth requirement** (free but adds friction; Open-Meteo requires no auth)
3. **Missing dust parameter** (critical for Qatar; WAQI does not report dust concentration)
4. **Open-Meteo is superior** for Qatar (CAMS model covers entire country, includes dust,
   no auth required)

**Why this matters despite rejection**:
- **WAQI typically has good coverage** in countries with open data policies (US EPA AirNow,
  UK DEFRA, Germany UBA, etc.). For Qatar, the **absence of official stations in WAQI** is
  a **negative finding** — it confirms that Qatar's 17 MECC AQM stations do **not publish
  real-time data** to international aggregators.
- **data.gov.qa air quality datasets** (17 datasets from MECC) all have `update_frequency: ANNUAL`
  — this confirms that Qatar's AQM network data is **batch-only, not real-time**.

**Recommendation**: Document WAQI's limited Qatar coverage as a **negative finding**. Use
**Open-Meteo Copernicus CAMS** instead for Qatar air quality monitoring (already documented
in separate candidate file: `qa-doha-air-quality-openmeteo.md`).

**Comparison: WAQI vs Open-Meteo for Qatar**:
| Aspect | WAQI | Open-Meteo CAMS |
|--------|------|-----------------|
| Coverage | 1 citizen sensor | Full Qatar grid |
| PM2.5 | ✅ Yes | ✅ Yes |
| PM10 | ✅ Yes | ✅ Yes |
| Dust | ❌ No | ✅ Yes (critical for Qatar) |
| NO2, O3, SO2, CO | ✅ Yes | ✅ Yes |
| Auth | API key required | No auth |
| Freshness | Hourly | Hourly |
| Data source | Citizen sensor (GAIA) | Copernicus CAMS model |

**Qatar MECC AQM Network** (not publicly accessible in real-time):
- **17 monitoring stations** across Qatar (locations on data.gov.qa)
- **Parameters measured**: PM10, PM2.5, O3, NO2, SO2, CO, meteorology
- **Publication**: Annual reports on data.gov.qa; no real-time API
- **Equipment**: Continuous analyzers (Thermo Scientific, Teledyne, etc.)
- **Data gaps**: Real-time data is collected but **not published** publicly

**Future potential**: If Qatar MECC publishes real-time AQM data in the future (similar to
UK DEFRA, US EPA AirNow), it would be a **high-value addition** to the repo. The 17-station
network provides spatial coverage across Doha, industrial areas (Mesaieed, Ras Laffan), and
residential zones.
