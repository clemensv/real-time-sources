# EUMETSAT OSI SAF ASCAT Ocean Surface Winds

- **Country/Region**: Global oceans (ice-free waters, 50°N-50°S primary coverage)
- **Endpoint**: FTP: `ftp.osi-saf.org`, EUMETSAT Data Store: `https://api.eumetsat.int/data`
- **Protocol**: FTP, REST API (Data Store with registration), BUFR, NetCDF
- **Auth**: FTP anonymous, Data Store requires free EUMETSAT registration
- **Format**: NetCDF-4, BUFR, GRIB2
- **Freshness**: Near-real-time (~90 minutes from observation), 2x daily swath coverage per satellite
- **Docs**: https://osi-saf.eumetsat.int/products/osi-150-a
- **Score**: 14/18

## Overview

The Advanced Scatterometer (ASCAT) on Metop-A, Metop-B, and Metop-C measures ocean surface wind speed and direction using C-band radar backscatter. ASCAT provides:

- **Wind Vector Cells (WVC)**: 12.5 km or 25 km resolution grid cells along satellite swath
- **Coverage**: Global oceans between ~82°N and ~82°S, excluding ice-covered regions
- **Swath width**: 2×550 km (two swaths per satellite, separated by nadir gap)
- **Revisit**: Each Metop satellite provides 2 passes per day per location; with 3 satellites (Metop-A/B/C), total coverage is 6 passes/day

OSI SAF wind products:
- **OSI-150-a**: ASCAT 12.5 km coastal winds (NRT, 90-minute latency)
- **OSI-151-a**: ASCAT 25 km ocean winds (NRT, 90-minute latency)
- **OSI-154**: ASCAT 12.5 km stress-equivalent winds (optimized for air-sea interaction)

**Why ocean winds matter**:
- **Shipping**: Route optimization, storm avoidance
- **Renewable energy**: Offshore wind farm site assessment and power forecasting
- **Fisheries**: Upwelling detection (nutrient-rich water brought to surface by wind stress)
- **Hurricane tracking**: Scatterometer winds penetrate clouds, detect tropical cyclone wind structure
- **Wave forecasting**: Wind speed/direction drives ocean wave models (ECMWF WAM, NOAA WaveWatch III)

ASCAT is **the** reference for global ocean winds — higher spatial resolution and better coverage than numerical weather prediction (NWP) model outputs alone.

## Endpoint Analysis

**FTP Distribution** (primary NRT channel):
```
ftp://ftp.osi-saf.org/prod/wind/
  /ascat_coastal_12.5km/
  /ascat_ocean_25km/
```

Example filename:
```
ascat_20240615_120000_metopb_12345_eps_o_125_l2.nc
```

Filename structure:
- `ascat`: Product type
- `20240615_120000`: Orbit start time
- `metopb`: Satellite (Metop-A, B, or C)
- `12345`: Orbit number
- `eps_o_125`: EPS, ocean, 12.5 km
- `l2`: Level-2 (swath geometry, not gridded)

**Update pattern**:
- New files arrive every ~100 minutes (orbital period)
- Each file covers one half-orbit swath (~50 minutes of observation)
- File size: ~10-30 MB (NetCDF), ~1-5 MB (BUFR)
- Latency: ~90 minutes from observation to FTP availability

**EUMETSAT Data Store API**:
```
GET https://api.eumetsat.int/data/browse/collections?q=ASCAT
```

Requires free registration. Provides:
- Search interface (OData query parameters)
- Direct file download via HTTP
- Same products as FTP (potentially faster than FTP polling)

**BUFR stream** (WMO GTS distribution):
- ASCAT winds distributed on Global Telecommunication System as BUFR messages
- National met services receive via GTS and may republish via their own APIs
- Lower latency than file-based FTP (~30-60 minutes)

## Schema / Sample

**NetCDF Level-2 Wind Vector Cell**:
```
dimensions:
    wvc_index = 82 (wind vector cells across swath)
    scan_index = 1623 (along-track scans)

variables:
    float wind_speed(scan_index, wvc_index)
        units: "m/s"
        standard_name: "wind_speed"
        valid_range: 0.0, 50.0
        
    float wind_dir(scan_index, wvc_index)
        units: "degree"
        standard_name: "wind_to_direction"
        valid_range: 0.0, 360.0
        comment: "Meteorological convention (direction FROM which wind blows)"
        
    float lat(scan_index, wvc_index)
    float lon(scan_index, wvc_index)
    
    int wvc_quality_flag(scan_index, wvc_index)
        flag_meanings: "good medium poor unusable"
        flag_values: 0, 1, 2, 3
        
    double time(scan_index)
        units: "seconds since 1981-01-01 00:00:00"
```

**Event model** (CloudEvents bridge):
```json
{
  "specversion": "1.0",
  "type": "eumetsat.osi-saf.ascat.wind-vector-cell",
  "source": "metopb/orbit/12345",
  "id": "metopb_12345_scan0856_wvc42",
  "time": "2024-06-15T12:08:34Z",
  "subject": "ocean-wind/metopb/12345/856/42",
  "datacontenttype": "application/json",
  "data": {
    "satellite": "metopb",
    "orbit_number": 12345,
    "scan_index": 856,
    "wvc_index": 42,
    "latitude": 35.67,
    "longitude": -12.34,
    "wind_speed_ms": 12.5,
    "wind_direction_deg": 245.0,
    "wind_u_ms": -5.3,
    "wind_v_ms": -11.3,
    "quality_flag": "good",
    "ambiguity_removed": true
  }
}
```

**Key/Subject design**:
- Option A: `{satellite}/{orbit}/{scan}/{wvc}` (unique per observation)
- Option B: `{lat_bucket}/{lon_bucket}` (geographic cell, multiple passes per day)
- Option C: Emit entire swath as single event (bulk payload)

Recommend **Option A** for full fidelity, with consumers aggregating by geography.

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Freshness** | 2 | ~90-minute latency, new swaths every ~100 min |
| **Openness** | 3 | Anonymous FTP, free Data Store registration, CC-BY-4.0 |
| **Stability** | 3 | Operational since 2006 (Metop-A), proven record |
| **Structure** | 3 | NetCDF-4/BUFR, CF conventions, WMO standards |
| **Identifiers** | 2 | Orbit + scan + WVC indexing (stable within file) |
| **Additive value** | 1 | Repo has no ocean winds; complements weather stations |

**Total: 14/18**

**Strengths**:
- **Reference-quality winds**: ASCAT is the gold standard for global ocean winds
- **All-weather**: Radar sees through clouds (vs. optical/IR satellites)
- **Sub-daily revisit**: 6 passes/day with 3 satellites (Metop-A/B/C)
- **Long time series**: Metop-A operational since 2006, ensuring continuity
- **Operational backing**: EUMETSAT core mission, guaranteed long-term support
- **Multiple satellites**: Redundancy (if one Metop fails, others continue)

**Real-world use**:
- **2017 Hurricane Irma**: ASCAT detected 50 m/s winds, guiding evacuation timing
- **Offshore wind farms**: Developers use ASCAT for multi-year wind resource assessment
- **Shipping**: Maersk integrates ASCAT winds into route optimization (fuel savings)

## Limitations

1. **Swath geometry, not continuous**: Polar orbit provides 2 passes/day per location, not continuous monitoring. Geostationary satellites (GOES, Meteosat) monitor continuously but can't measure wind vectors directly (only infer from cloud motion).

2. **90-minute latency**: NRT products arrive ~90 minutes after observation. For real-time storm tracking, this is acceptable. For sub-hourly nowcasting, it's dated. BUFR stream on GTS has lower latency (~30-60 min) but requires GTS access.

3. **Ocean-only**: Land backscatter is too complex for wind retrieval. ASCAT provides no data over land (unlike weather station networks).

4. **Rain contamination**: Heavy rain attenuates C-band radar, degrading wind quality in tropical squalls. Quality flags mark affected cells.

5. **Event granularity**: Each swath has ~130,000 wind vector cells (82 WVC × 1,600 scans). Emitting one event per cell creates high message volume (~130k events per swath, ~200 swaths/day across 3 satellites = 26M events/day). Must decide: emit per-cell events, or aggregate into coarser spatial bins?

6. **No real-time stream API**: FTP polling or Data Store HTTP download. No WebSocket or SSE stream of observations as they arrive.

## Verdict

**STRONG CANDIDATE** (14/18) — ASCAT winds are reference-quality, operationally stable, and fill a gap (repo has no ocean parameter monitoring). The 90-minute latency is acceptable for marine applications (shipping, offshore wind, fisheries).

**Implementation path**:
1. **Poll FTP or Data Store**: Check for new NetCDF files every 10 minutes
2. **Parse swath**: Extract wind vector cells from NetCDF
3. **Emit events**: One CloudEvent per WVC (or per N×N grid of WVCs for lower volume)
4. **Key design**: Use `{satellite}/{orbit}/{scan}/{wvc}` for uniqueness
5. **Quality filter**: Emit only "good" and "medium" quality cells (drop "poor" and "unusable")

**Volume estimate**:
- 3 satellites × ~14 orbits/day × ~130,000 WVC/orbit = ~5.5M events/day
- After quality filtering (~70% pass): ~3.8M events/day
- Average event size: ~250 bytes JSON → ~950 MB/day

**Alternative: gridded aggregation**:
- Pre-bin WVCs into 0.5° × 0.5° lat/lon grid (~1M cells globally)
- Emit one event per grid cell per pass (with multiple satellites, some cells get 6 updates/day)
- Reduces volume to ~500k events/day

**Next steps**:
1. Prototype FTP polling (check `/prod/wind/ascat_coastal_12.5km/` for new files)
2. Parse NetCDF with `netCDF4-python` or `xarray`
3. Design keying scheme (per-WVC vs. gridded)
4. Implement quality filtering (flag_values 0 and 1 only)

**Recommended topic folder**: `oceans` (ocean surface parameter monitoring).
