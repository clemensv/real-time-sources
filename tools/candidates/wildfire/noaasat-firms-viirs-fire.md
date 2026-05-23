# NASA FIRMS VIIRS Active Fire (NOAA JPSS Satellites)

- **Country/Region**: Global
- **Endpoint**: `https://firms.modaps.eosdis.nasa.gov/api/area/csv/VIIRS_SNPP_NRT/{MAP_KEY}/{area}/{day_range}`
- **Protocol**: REST (CSV)
- **Auth**: Free MAP_KEY registration required
- **Format**: CSV
- **Freshness**: 3-hour latency (near-real-time)
- **Docs**: https://firms.modaps.eosdis.nasa.gov/api/
- **Score**: 13/18

## Overview

NASA's Fire Information for Resource Management System (FIRMS) provides near-real-time active fire detection data from the **VIIRS** (Visible Infrared Imaging Radiometer Suite) instrument aboard **NOAA's JPSS satellites**: Suomi-NPP (launched 2011), NOAA-20 (launched 2017), and NOAA-21 (launched 2022). VIIRS detects thermal anomalies at 375m resolution using IR channels optimized for fire detection.

VIIRS active fire products are used for:
- **Wildfire early warning**: Detection within 3 hours of satellite overpass
- **Agricultural burning monitoring**: Tracking slash-and-burn practices
- **Biomass burning emissions**: Input for air quality models
- **Firefighting resource allocation**: Real-time fire location updates
- **Illegal deforestation detection**: Forest clearance fires

FIRMS aggregates VIIRS fire detections globally and provides a REST API with CSV/JSON/GeoJSON/KML/Shapefile outputs. The service is **NASA-hosted** but monitors **NOAA operational satellites** (JPSS constellation).

## Endpoint Analysis

**API endpoint structure:**

```
GET https://firms.modaps.eosdis.nasa.gov/api/area/csv/VIIRS_SNPP_NRT/{MAP_KEY}/{area}/{day_range}
```

Parameters:
- `{MAP_KEY}`: Free API key (register at https://firms.modaps.eosdis.nasa.gov/api/)
- `{area}`: Geographic bounds (e.g., `world`, `-125,24,-66,50` for CONUS)
- `{day_range}`: Number of days back (1-10 for NRT, up to 60 for archive)

Example:
```
GET https://firms.modaps.eosdis.nasa.gov/api/area/csv/VIIRS_SNPP_NRT/YOUR_MAP_KEY/world/1
```

Response: CSV with columns:
```
latitude,longitude,bright_ti4,scan,track,acq_date,acq_time,satellite,confidence,version,bright_ti5,frp,daynight
38.5,-120.3,320.5,0.4,0.4,2026-05-23,0812,N,nominal,2.0NRT,295.2,12.3,D
```

**Fields:**
- `latitude`, `longitude`: Fire detection location (decimal degrees)
- `bright_ti4`, `bright_ti5`: Brightness temperature (K) for channels I4 and I5
- `scan`, `track`: Pixel size along/across track (km)
- `acq_date`, `acq_time`: Acquisition date (YYYY-MM-DD) and time (HHMM UTC)
- `satellite`: "N" (Suomi-NPP), "20" (NOAA-20), "21" (NOAA-21)
- `confidence`: "low", "nominal", "high"
- `frp`: Fire Radiative Power (MW)
- `daynight`: "D" (day) or "N" (night)
- `version`: Product version

**Key model**: `{satellite}/{acq_date}/{acq_time}/{latitude}/{longitude}` — composite key per fire pixel.

**Volume**: Varies widely (10-100,000 fires/day globally depending on season).

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3/3 | **Critical for wildfire management** and air quality forecasting |
| Freshness | 2/3 | 3-hour latency (NRT processing, not real-time) |
| Openness | 2/3 | Free API key required (generous limits: 1,000 requests/day) |
| Schema Clarity | 3/3 | Clean CSV, well-documented fields |
| Machine-Readability | 3/3 | CSV, straightforward parsing |
| Repo Fit | 0/3 | **NASA-hosted** (not NOAA direct); auth required |

**Total: 13/18**

- Global fire detection at 375m resolution
- NOAA operational satellites (JPSS constellation)
- CSV output is clean and well-structured
- FRP (Fire Radiative Power) provides intensity metric
- Confidence flag for filtering false alarms
- **However**: Requires API key (though free and generous)
- 3-hour latency is borderline for "near-real-time"
- NASA-hosted (not NOAA SWPC/NESDIS direct endpoint)

## Limitations

- **Requires MAP_KEY** (free registration, but not zero-auth)
- **3-hour latency** (satellite overpass + processing time)
- **NASA-hosted** (not a native NOAA endpoint)
- Rate limits: 1,000 requests/day per key (generous, but not unlimited)
- Cloud cover obscures fires (IR detection)
- Small/low-intensity fires may be missed (375m resolution)
- Duplicate detections across overlapping satellite passes require deduplication

## Verdict

**CONSIDER** — FIRMS VIIRS is a **high-value fire detection product** used operationally worldwide. However, it has two friction points: (1) **requires free API key** (not zero-auth), and (2) **NASA-hosted** (not a direct NOAA endpoint, though it monitors NOAA satellites). If the repo accepts "free API key" as "open enough," FIRMS is a strong candidate for wildfire monitoring. Otherwise, look for a **NOAA-native VIIRS fire API** (e.g., NESDIS/OSPO fire products). **Moderate priority** — strong operational value, but auth and NASA-hosting are minor barriers.
