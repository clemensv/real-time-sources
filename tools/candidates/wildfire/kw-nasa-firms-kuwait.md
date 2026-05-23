# NASA FIRMS Wildfire Detection — Kuwait Region

- **Country/Region**: Global (includes Kuwait)
- **Endpoint**: `https://firms.modaps.eosdis.nasa.gov/api/area/csv/<MAP_KEY>/VIIRS_SNPP_NRT/world/1/2025-05-23`
- **Protocol**: REST / HTTP CSV (also JSON available)
- **Auth**: Free API key (MAP_KEY) required, obtain at https://firms.modaps.eosdis.nasa.gov/api/
- **Format**: CSV, JSON, KML, Shapefile
- **Freshness**: Near-real-time (3–6 hour latency from satellite overpass)
- **Docs**: https://firms.modaps.eosdis.nasa.gov/api/
- **Score**: 12/18

## Overview

The **Fire Information for Resource Management System (FIRMS)** is NASA's global wildfire detection service. It provides near-real-time active fire/thermal anomaly data from satellite sensors:

- **MODIS** (Terra/Aqua satellites) — 1km resolution, 4 overpasses/day per location
- **VIIRS** (Suomi NPP / NOAA-20 satellites) — 375m resolution, better sensitivity, 2 overpasses/day per location

FIRMS detects:
- Active fires (wildfires, agricultural burns, industrial flares)
- Thermal anomalies (lava flows, gas flares, industrial heat sources)
- Smoke plumes (via adjacent products)

**Kuwait fire context**:
- **Minimal wildfire risk** — Kuwait is mostly desert with sparse vegetation, no forests
- **Agricultural burns** — Seasonal crop residue burning in agricultural areas (Wafra, Abdally)
- **Oil/gas flares** — Persistent thermal hotspots at oil refineries and wellheads (Al-Ahmadi, Burgan field)
- **Industrial fires** — Occasional refinery/petrochemical incidents
- **Tire dump fires** — Al-Jahra tire graveyard (world's largest), occasional fires detected by VIIRS
- **Border smuggling fires** — Illegal burning along Kuwait-Iraq border

**Kuwait use cases**:
- **Flare monitoring** — Track oil/gas flaring emissions (environmental compliance)
- **Agricultural burn tracking** — Air quality impact from crop burning
- **Industrial incident detection** — Refinery fires, storage tank fires
- **Illegal burning** — Environmental enforcement (tire dumps, waste burning)

## Endpoint Analysis

**Endpoint verified** — FIRMS API active and stable:

```
GET https://firms.modaps.eosdis.nasa.gov/api/area/csv/<MAP_KEY>/VIIRS_SNPP_NRT/<lon_min>,<lat_min>,<lon_max>,<lat_max>/1/<date>
```

**Example for Kuwait bounding box** (29–30°N, 47–48.5°E, past 1 day):
```
GET https://firms.modaps.eosdis.nasa.gov/api/area/csv/MAP_KEY/VIIRS_SNPP_NRT/47,29,48.5,30/1/2025-05-23
```

**Parameters**:
- `MAP_KEY`: Free API key from FIRMS registration
- `VIIRS_SNPP_NRT` or `MODIS_NRT`: Sensor/product
- Bounding box: `lon_min,lat_min,lon_max,lat_max`
- `1`: Number of days to retrieve (1–10)
- Date: `YYYY-MM-DD` (optional, defaults to today)

**Rate limits** (free tier):
- 1,000 requests per day
- No per-minute throttling documented

**Response time**: ~500ms for small bounding box, ~2s for large area

**Expected Kuwait coverage**:
- **Few fire detections** — Kuwait has minimal natural fire activity
- **Persistent hotspots** — Oil refineries (Al-Ahmadi, Mina Abdullah) and wellhead flares show up as recurring thermal anomalies
- **Seasonal variability** — Agricultural burns in spring/summer (April–June)

## Schema / Sample Payload

**CSV format**:

```csv
latitude,longitude,brightness,scan,track,acq_date,acq_time,satellite,instrument,confidence,version,bright_t31,frp,daynight
29.0567,48.1234,320.5,0.41,0.39,2025-05-23,0730,NOAA-20,VIIRS,n,2.0NRT,290.2,5.3,D
29.3456,47.8765,335.2,0.42,0.40,2025-05-23,0732,NOAA-20,VIIRS,h,2.0NRT,295.8,12.7,D
```

**Field mapping**:
- `latitude`, `longitude`: Fire location (decimal degrees)
- `brightness`: Brightness temperature of fire pixel (Kelvin, channel I-4)
- `scan`, `track`: Pixel size (km) along scan and track directions
- `acq_date`, `acq_time`: Acquisition date (YYYY-MM-DD) and time (HHMM UTC)
- `satellite`: NOAA-20, Suomi NPP, Terra, Aqua
- `instrument`: VIIRS, MODIS
- `confidence`: Fire confidence (l=low, n=nominal, h=high) for VIIRS; 0–100 for MODIS
- `version`: Product version (2.0NRT)
- `bright_t31`: Brightness temperature channel I-5 (Kelvin)
- `frp`: Fire Radiative Power (MW) — intensity measure
- `daynight`: D=day, N=night

**JSON format** (also available via `json` parameter):

```json
[
  {
    "latitude": 29.0567,
    "longitude": 48.1234,
    "brightness": 320.5,
    "scan": 0.41,
    "track": 0.39,
    "acq_date": "2025-05-23",
    "acq_time": "0730",
    "satellite": "NOAA-20",
    "instrument": "VIIRS",
    "confidence": "n",
    "version": "2.0NRT",
    "bright_t31": 290.2,
    "frp": 5.3,
    "daynight": "D"
  }
]
```

## Why It's Strong

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Freshness | 2 | 3–6 hour latency (not real-time but near-real-time) |
| Openness | 3 | Free API key, generous limits (1,000 req/day) |
| Stability | 3 | NASA operational service, stable since 2002 |
| Structure | 3 | CSV/JSON, well-documented schema |
| Identifiers | 0 | **No stable fire ID** — each detection is independent, no fire perimeter tracking |
| Additive value | 1 | Global service, Kuwait is included but not unique |

**Score: 12/18** — Strong technical fit, but **identifiers are the major weakness**.

## Limitations

- **No fire IDs** — FIRMS detects individual thermal pixels, not coherent fire events. Same fire may generate dozens of detections over multiple days, but there's no linking ID.
- **Subject/key challenge** — Without stable fire IDs, difficult to key events for Kafka. Options:
  - Use `lat/lon + acq_date` as composite key (but fires move)
  - Use pixel grid cell ID (but fires span cells)
  - Treat each detection as independent event (no deduplication)
- **Latency** — 3–6 hours from satellite overpass to API availability (not true real-time)
- **False positives** — Industrial heat sources (oil flares, refineries) appear as persistent "fires"
- **Kuwait-specific low value** — Kuwait has minimal wildfire activity. Most detections are oil/gas flares (already known locations) or rare agricultural burns.
- **Global source** — A FIRMS bridge should cover **worldwide**, not just Kuwait. Kuwait coverage is a byproduct.

## Verdict

**Verdict**: ⏭️ **Reference** — FIRMS is a strong global wildfire detection service that includes Kuwait. However:

1. **Global scope** — If this repo adds FIRMS, it should be a **global bridge** covering all regions, not Kuwait-specific.
2. **Low Kuwait fire activity** — Kuwait has minimal wildfires. Most detections are industrial flares (false positives for wildfire monitoring).
3. **Identifier problem** — Lack of stable fire IDs makes Kafka keying difficult. Would require spatial clustering or accepting each pixel as independent event.
4. **Existing coverage?** — Check if repo already has a wildfire source (e.g., `australia-wildfires` might use FIRMS). If so, ensure it covers global data, not just Australia.

**Recommendation**:
- **Primary action**: Build a **global FIRMS bridge** that covers all countries including Kuwait (not a Kuwait-specific implementation).
- **Key design**: Use `lat + lon + acq_date` as composite key, or implement spatial clustering to group pixels into fire events.
- **Kuwait-specific filtering**: Allow users to filter by bounding box or country code in Kafka consumer (not at bridge level).

**Next steps** (if building FIRMS bridge):
1. Register for free FIRMS MAP_KEY
2. Design global bridge with configurable bounding boxes (not hardcoded)
3. Implement polling loop (recommended: every 6–12 hours to catch new satellite passes)
4. Handle deduplication (same fire pixel reported multiple times)
5. Consider filtering false positives (persistent industrial heat sources vs. actual fires)
6. Use FRP (Fire Radiative Power) to prioritize high-intensity events

**Cross-Gulf observation**:
FIRMS covers all GCC states. A global bridge would provide wildfire detection for Kuwait, Saudi Arabia, UAE, Oman, etc. without per-country implementations.
