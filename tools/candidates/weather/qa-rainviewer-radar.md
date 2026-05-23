# RainViewer Global Radar (Qatar Coverage)

- **Country/Region**: Global (Qatar coverage via Middle East radar mosaic)
- **Endpoint**: `https://api.rainviewer.com/public/weather-maps.json`
- **Protocol**: REST / JSON (manifest) → tile CDN
- **Auth**: None
- **Format**: JSON manifest + PNG radar tiles
- **Freshness**: New radar frames every 10 minutes; 2-hour past archive available
- **Docs**: https://www.rainviewer.com/api.html
- **Score**: 11/18

## Overview

**RainViewer** is a global precipitation radar visualization service that aggregates radar
data from national meteorological services worldwide and publishes it as tiled map overlays.
The service provides:
- **Past radar** (last 2 hours, 10-minute intervals) — actual precipitation observed
- **Nowcast** (next 30 minutes, 5-minute intervals) — short-term precipitation forecast
- **Satellite IR** (infrared cloud imagery)
- **Coverage tiles** (which areas have radar coverage)

For **Qatar**, RainViewer provides:
- **Middle East radar mosaic** (aggregated from regional met services)
- **Precipitation detection** (rain, dust storms when combined with satellite)
- **10-minute update cadence** (recent frames)

**Qatar precipitation context**:
- **Annual rainfall**: <80 mm/year (one of the driest climates globally)
- **Rain season**: November-March (winter), with most days being rain-free
- **Dust visibility**: While RainViewer is designed for precipitation, radar can sometimes
  detect **heavy dust storms** (large dust particles reflect radar)
- **Flash flood risk**: Even 20-30mm rainfall can cause flash floods in Doha due to poor
  drainage infrastructure

**Use case**: RainViewer is **not a primary precipitation data source** for Qatar (rainfall
is rare), but it's useful for:
1. **Rare rain event tracking**: When rain does occur, 10-minute radar updates show storm
   movement and intensity
2. **Dust storm detection** (secondary): Heavy dust can appear on radar, especially haboobs
   with sand/dust lofted to high altitudes
3. **Regional context**: Rainfall in neighboring countries (Oman, UAE, Saudi Arabia) affects
   supply chains and regional logistics

## Endpoint Analysis

**Live test successful** — API returned manifest of available radar frames:

```json
{
  "version": "1.4",
  "generated": 1779522628,
  "host": "https://tilecache.rainviewer.com",
  "radar": {
    "past": [
      {"time": 1779521400, "path": "/v2/radar/1779521400/256/"},
      {"time": 1779521100, "path": "/v2/radar/1779521100/256/"},
      {"time": 1779520800, "path": "/v2/radar/1779520800/256/"},
      {"time": 1779520500, "path": "/v2/radar/1779520500/256/"},
      {"time": 1779520200, "path": "/v2/radar/1779520200/256/"},
      {"time": 1779519900, "path": "/v2/radar/1779519900/256/"},
      {"time": 1779519600, "path": "/v2/radar/1779519600/256/"},
      {"time": 1779519300, "path": "/v2/radar/1779519300/256/"},
      {"time": 1779519000, "path": "/v2/radar/1779519000/256/"},
      {"time": 1779518700, "path": "/v2/radar/1779518700/256/"},
      {"time": 1779518400, "path": "/v2/radar/1779518400/256/"},
      {"time": 1779518100, "path": "/v2/radar/1779518100/256/"},
      {"time": 1779517800, "path": "/v2/radar/1779517800/256/"}
    ],
    "nowcast": []
  },
  "satellite": {
    "infrared": [
      {"time": 1779522000, "path": "/v2/satellite/1779522000/"}
    ]
  }
}
```

**Key fields**:
- `generated`: Unix timestamp when manifest was generated
- `host`: Base URL for tile CDN
- `radar.past[]`: Array of past radar frames (13 frames = ~2 hours at 10-minute intervals)
- `radar.nowcast[]`: Short-term forecast frames (often empty if no active precipitation)
- `satellite.infrared[]`: Infrared satellite imagery (cloud tops)

**Tile URL construction**:
```
{host}{path}{z}/{x}/{y}/4/1_1.png
```

Example for Qatar (Doha):
- Lat/lon: 25.28°N, 51.52°E
- Zoom level 8, tile x=150, y=101 (approximately)
- Full URL: `https://tilecache.rainviewer.com/v2/radar/1779521400/256/8/150/101/4/1_1.png`

**Color scale** (PNG pixel values):
- 0: No precipitation
- 1-255: Precipitation intensity (light to heavy)
- Color map provided in docs (blue = light rain, yellow/red = heavy rain)

**Alternative**: Satellite IR tiles show cloud coverage (useful for dust storm tracking when
combined with MODIS dust imagery)

## Integration Notes

- **Polling interval**: 10 minutes (matches radar frame update cadence)
- **CloudEvents subject**: `radar/{region}/{time}` → `radar/middle-east/1779521400`
- **Kafka key**: `{time}` (Unix timestamp of radar frame)
- **Entity model**: Gridded radar imagery (not point data, but raster tiles)
- **Data format**: The bridge would need to:
  1. Poll manifest endpoint every 10 minutes
  2. Identify new radar frames (compare timestamps)
  3. Fetch relevant tiles for Qatar (bounding box 24-27°N, 50-52°E)
  4. Extract precipitation intensity from PNG pixels
  5. Emit events per grid cell or aggregated region
- **Overlap check**: The repo does not currently have a precipitation radar bridge. NOAA NWS
  provides text-based precipitation forecasts, but no radar imagery ingestion.
- **Challenges**:
  - Tile-based data (requires lat/lon → tile coordinate conversion)
  - PNG decoding (extract numerical values from image pixels)
  - Sparse data for Qatar (most frames will show zero precipitation)
  - Radar coverage in Middle East is patchy (not all countries publish open radar data)

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 10-minute updates (good but not sub-minute streaming) |
| Openness | 3 | No auth, free, documented API |
| Stability | 2 | Commercial service (RainViewer.com), no SLA, but operational for years |
| Structure | 1 | PNG tiles (requires decoding, not native JSON/Protobuf) |
| Identifiers | 2 | Timestamps are stable, but grid cells require lat/lon → tile math |
| Additive value | 1 | New domain (precipitation radar) but Qatar has minimal rainfall |

**Verdict**: **Marginal candidate** due to:
1. **Low precipitation frequency in Qatar** (most radar frames will be empty)
2. **Tile-based data format** (adds complexity to bridge implementation)
3. **Uncertain radar coverage** for Qatar (Middle East radar mosaic quality varies)

**Recommendation**: **Defer** unless the repo adds precipitation radar as a priority domain.
For Qatar specifically, **Open-Meteo precipitation forecast** (hourly rainfall mm) is simpler
and more useful than 10-minute radar tiles.

**Possible future use case**:
- If Qatar experiences a **rare heavy rain event** (e.g., 50+ mm in 24 hours, as occurred in
  2015), RainViewer radar tiles would provide high-resolution tracking of storm cells and
  movement. This could be valuable for:
  - Flash flood early warning
  - Drainage system overflow prediction
  - Airport operations (runway flooding)
  - Road closures (Doha's poor drainage causes widespread flooding even from moderate rain)

**Alternative approach**:
- Instead of a full radar tile bridge, implement a **precipitation detection alert** bridge:
  1. Poll RainViewer manifest every 10 minutes
  2. Fetch tiles covering Qatar bounding box
  3. Check if any pixels > threshold (e.g., >10 = light rain detected)
  4. Emit **binary alert event** (rain detected: yes/no) rather than full raster data
  5. This simplifies implementation and focuses on the rare, high-impact rain events

**Qatar rain event history**:
- **Oct 2015**: 80mm rainfall in 24 hours (Qatar's average annual total), caused widespread
  flooding in Doha
- **Nov 2018**: 40mm in 12 hours, flash floods, airport disruption
- **Jan 2020**: 30mm, flooding in low-lying areas
- **Most years**: <20mm total annual rainfall, with many months receiving 0mm

**Integration with other Qatar sources**:
- Combine RainViewer radar with:
  - Open-Meteo precipitation forecast (mm/hour) → cross-check forecast vs actual
  - METAR present weather (RA = rain, SHRA = showers) → ground truth at airport
  - Open-Meteo cloud cover (%) → pre-cursor to precipitation
  - GDACS flood alerts (if heavy rain triggers humanitarian impact threshold)
