# NASA POWER (Prediction Of Worldwide Energy Resources)

- **Country/Region**: Global
- **Endpoint**: `https://power.larc.nasa.gov/api/temporal/`
- **Protocol**: REST (JSON, CSV, GeoJSON, NetCDF)
- **Auth**: None
- **Format**: JSON, CSV, GeoJSON, NetCDF
- **Freshness**: Daily (1-day latency for meteorology, longer for solar/climatology)
- **Docs**: https://power.larc.nasa.gov/docs/
- **Score**: 11/18

## Overview

NASA's Prediction Of Worldwide Energy Resources (POWER) project provides solar and meteorological data derived from satellite observations and NASA models. Operated by NASA Langley Research Center, POWER was originally designed for renewable energy applications (solar panel siting, wind farm planning) but now serves agriculture, building energy efficiency, and water resource management.

POWER offers point-based time-series API access to over 200 parameters including solar irradiance (GHI, DNI, DHI), temperature (min/max/avg), precipitation, wind speed/direction, humidity, pressure, and derived agroclimatic indices (growing degree days, frost days, evapotranspiration). Data sources include MERRA-2 reanalysis (meteorology, 0.5°×0.625° resolution), CERES (solar, 1° resolution), and GPM IMERG (precipitation, 0.1° resolution).

Temporal resolution ranges from hourly to monthly climatologies. The API supports single-point queries, regional averages, and full-grid downloads. No auth required.

## Endpoint Analysis

**Single-point time-series query:**
```
GET https://power.larc.nasa.gov/api/temporal/daily/point?
  parameters=T2M,PRECTOTCORR
  &community=AG
  &longitude=-95.5
  &latitude=29.5
  &start=20240101
  &end=20240115
  &format=JSON
```

**Response (truncated):**
```json
{
  "header": {
    "title": "NASA/POWER CERES/MERRA2 Native Resolution Daily Data",
    "api_version": "2.5.8",
    "sources": ["merra2", "power_901"]
  },
  "messages": [],
  "parameters": {
    "T2M": {
      "20240101": 12.5,
      "20240102": 14.3,
      "20240103": 15.1
    },
    "PRECTOTCORR": {
      "20240101": 0.0,
      "20240102": 2.5,
      "20240103": 0.1
    }
  },
  "geometry": {
    "type": "Point",
    "coordinates": [-95.5, 29.5, 30.2]
  }
}
```

**Available temporal resolutions:**
- `hourly` — MERRA-2 hourly meteorology (UTC), 1980–present minus ~1 week lag
- `daily` — daily averages/sums, 1981–present minus 1 day
- `monthly` — monthly aggregates
- `climatology` — long-term monthly normals

**Parameter communities (thematic groupings):**
- `AG` — Agriculture (temp, precip, humidity, GDD, frost days, etc.)
- `SB` — Sustainable Buildings (irradiance, temp, wind)
- `RE` — Renewable Energy (solar, wind resource assessment)

**Regional queries:**
```
GET https://power.larc.nasa.gov/api/temporal/daily/regional?
  parameters=T2M
  &community=AG
  &bbox=-100,25,-90,35
  &start=20240115
  &end=20240115
  &format=GEOJSON
```

Returns GeoJSON FeatureCollection with one feature per grid cell in the bounding box.

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Daily data with 1-day lag for meteorology — not sub-daily or real-time |
| Openness | 3 | No auth, no registration, no rate limits |
| Stability | 3 | NASA LaRC operational system since 2003, current v2.5 API stable |
| Structure | 3 | REST JSON/CSV with clean schema, GeoJSON for spatial queries |
| Identifiers | 1 | Grid cells (lat/lon) are stable but no unique point IDs; queries specify coordinates |
| Richness | 0 | Derived/modeled data, not direct observations; 1-day lag makes it historical, not NRT |

**POWER excels for historical climate analysis and resource assessment, not real-time event streaming.** The 1-day lag for meteorology and longer lags for solar irradiance (CERES data has weeks to months latency) place it outside the "near real-time" scope. The daily resolution is too coarse for event-driven applications (hourly flash flood warnings, sub-daily agricultural alerts).

**Why it's here:** POWER provides *context data* for real-time event interpretation (e.g., "yesterday's solar irradiance at this wildfire location" or "7-day accumulated precipitation leading up to this flood event"), but it is not itself a real-time event stream. It's a background data layer, not a primary event source.

**API is excellent** — clean REST JSON, no auth, regional queries, multiple formats. If POWER had sub-hourly latency, it would score 14–15/18.

## Limitations

- **1-day minimum latency** for daily meteorology products. Hourly data has similar lag (MERRA-2 hourly is not real-time; it's reanalysis with ~1 week delay).
- **Derived/modeled data, not direct observations.** POWER uses MERRA-2 reanalysis (a blend of satellite obs + weather model), not raw sensor readings. Spatial resolution (0.5°×0.625° ~ 50km) is coarser than point weather stations.
- **Solar irradiance latency is weeks to months** (CERES data is research-quality, not operational). Only meteorology (temp, precip, wind) approaches daily latency.
- **No change detection or incremental API.** You query a date range and get all values; no "only new/updated data since last poll."
- **Grid-based, not station-based.** POWER returns model grid cell values, not actual station observations. For agriculture/energy applications this is acceptable; for hydrology, point-sensor gauges (USGS, European networks) are more accurate.

**POWER's strength is long-term climatology and global gap-filling** (stations are sparse in Africa, oceans, etc.). For real-time event bridging, it's too slow and too coarse.

## Final Verdict

**Verdict**: ⏭️ **Reference**

POWER is an excellent NASA service for historical climate data, renewable energy resource assessment, and agricultural planning, but it does not meet the repo's near-real-time threshold. The 1-day minimum latency and derived/modeled data (not direct observations) make it a context/background layer, not a primary event stream.

**Use POWER for:**
- Enriching real-time events with historical context (e.g., "7-day precip total before this flood," "solar irradiance at this wildfire ignition location")
- Filling spatial gaps where real-time station networks don't exist
- Agricultural models that run daily (not sub-hourly)

**Do not use POWER for:**
- Sub-daily event-driven applications (flash floods, severe weather)
- Real-time alerting (the 1-day lag is too slow)
- High-accuracy point observations (use station networks instead)

**If the repo adds "daily gridded climate context" as a domain,** POWER is the ideal source. But for the current focus on sub-hourly to daily event streams, it's out of scope.

**Bridge type:** N/A (1-day lag disqualifies from NRT event bridging)
