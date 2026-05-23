# NASA FIRMS - Iraq Wildfire and Agricultural Fire Detection

- **Country/Region**: Global (includes Iraq)
- **Endpoint**: `https://firms.modaps.eosdis.nasa.gov/api/country/`
- **Protocol**: HTTP REST API (CSV, JSON, GeoJSON, KML, SHP)
- **Auth**: API key required (free, self-service)
- **Format**: CSV, JSON, GeoJSON, KML, Shapefile
- **Freshness**: Near-real-time (3-6 hour latency from satellite overpass)
- **Docs**: https://firms.modaps.eosdis.nasa.gov/api/
- **Score**: 13/18

## Overview

NASA's Fire Information for Resource Management System (FIRMS) distributes active fire detection data from MODIS and VIIRS satellites globally. For Iraq, fire detections include:
- **Agricultural stubble burning** (wheat/barley fields after harvest — major air quality issue)
- **Reed fires in southern marshlands** (seasonal, sometimes accidental, sometimes malicious)
- **Waste burning** (informal dump sites)
- **Oil field gas flares** (persistent thermal hotspots, though VIIRS Nightfire is better for this)
- **Wildfire** (rare in Iraq, but possible in northern Kurdistan mountain forests)

Iraq has **severe seasonal air quality crises** from agricultural burning, particularly in the wheat-growing regions of Nineveh, Salah ad-Din, and Diyala provinces. Stubble burning produces dense smoke plumes that blanket Baghdad and other cities in late spring/early summer.

FIRMS provides near-real-time fire detection that could track these burning events as they happen.

## Endpoint Analysis

**API requires registration** — NASA provides free API keys via self-service at https://firms.modaps.eosdis.nasa.gov/api/

Attempted request without key:
```
curl https://firms.modaps.eosdis.nasa.gov/api/country/csv/YOUR_MAP_KEY/VIIRS_SNPP_NRT/IRQ/1
# Result: "Invalid API call."
```

Endpoint pattern:
```
GET https://firms.modaps.eosdis.nasa.gov/api/country/{format}/{MAP_KEY}/{source}/{country_code}/{days}
```

Parameters:
- `format` — csv, json, geojson, kml, shp
- `MAP_KEY` — free API key (obtained via email registration)
- `source` — VIIRS_SNPP_NRT (highest resolution, 375m), VIIRS_NOAA20_NRT, MODIS_NRT
- `country_code` — IRQ (Iraq), three-letter ISO code
- `days` — number of days back (1-10)

Response (CSV format):
```
latitude,longitude,bright_ti4,scan,track,acq_date,acq_time,satellite,instrument,confidence,version,bright_ti5,frp,daynight
33.5,44.2,320.5,0.4,0.4,2026-05-23,0730,N,VIIRS,n,2.0NRT,290.3,5.2,D
```

Key fields:
- `latitude`, `longitude` — detection coordinates
- `acq_date`, `acq_time` — acquisition timestamp
- `bright_ti4`, `bright_ti5` — brightness temperature (K)
- `frp` — fire radiative power (MW)
- `confidence` — l/n/h (low/nominal/high)
- `satellite` — N (Suomi-NPP), J1 (NOAA-20)

## Integration Notes

- **Free API key required** — not ideal for "no auth" preference, but registration is self-service and limits are generous (no documented rate limit for CSV endpoint).
- **Country-level queries** — the `/country/` endpoint filters for Iraq automatically (lat/lon bounding box 29-38°N, 38-49°E).
- **Daily polling pattern** — query for `days=1` every few hours to get incremental detections.
- **Kafka keying challenge**: Fire detections are point events with no stable facility ID. Options:
  - Use `latitude,longitude,acq_date,acq_time` composite key (unique per detection)
  - Use grid cell ID (snap to 0.01° or 0.1° cells)
- **Seasonal patterns**: Iraq fire activity peaks in May-June (wheat harvest stubble burning) and in summer (reed fires in southern marshes).
- **Volume**: Iraq typically has 10-100 fire detections per day during burning season, 0-10 per day off-season.
- **Overlap with VIIRS Nightfire**: FIRMS detects all thermal anomalies (fires + flares). VIIRS Nightfire specializes in persistent combustion (flares). For Iraq, both are relevant but serve different use cases.

## Iraq-Specific Use Cases

1. **Agricultural burning tracking** — monitor stubble burning in wheat belt provinces (Nineveh, Salah ad-Din, Diyala) and correlate with air quality impacts in Baghdad.
2. **Marsh fire monitoring** — southern Iraq marshlands (Mesopotamian Marshes, UNESCO World Heritage Site) sometimes experience fires. Real-time detection aids conservation.
3. **Conflict/arson detection** — in areas with ISIS remnants or tribal disputes, agricultural fires can be malicious. Near-real-time detection helps humanitarian response.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 3-6 hour latency (near-real-time relative to satellite overpass) |
| Openness | 2 | Free API key required, generous limits |
| Stability | 3 | NASA operational system, documented API |
| Structure | 3 | CSV/JSON/GeoJSON, documented schema |
| Identifiers | 1 | No stable fire IDs, point events with coordinates |
| Richness | 2 | Coordinates, FRP, confidence, timestamp, satellite |

**Verdict**: ✅ **Acceptable candidate** — Iraq agricultural burning is a major air quality issue. FIRMS provides near-real-time fire detection. **API key requirement** is a friction point but free and self-service. The main limitation is **no stable identifiers** (fires are transient point events, not persistent facilities like weather stations). Kafka keying would need grid cells or composite keys. Worth adding if agricultural/marsh fire monitoring is a priority — this would be the first wildfire/agricultural fire bridge in the repo, and Iraq is a compelling use case.
