# JAXA Himawari-9 L2 Sea Surface Temperature (AWS Mirror)

- **Country/Region**: Japan / Asia-Pacific (Himawari full disk coverage)
- **Endpoint**: `s3://noaa-himawari9/AHI-L2-FLDK-ISatSS/` (AWS S3, NOAA mirror)
- **Protocol**: HTTP (S3 REST), no auth
- **Auth**: None
- **Format**: NetCDF4
- **Freshness**: 10 minutes
- **Docs**: https://www.data.jma.go.jp/mscweb/en/himawari89/space_segment/spsg_ahi.html
- **Score**: 13/18

## Overview

Himawari-9 Level-2 Sea Surface Temperature (SST) product is a derived ocean product from the Advanced Himawari Imager (AHI) infrared channels. SST is computed from brightness temperature observations in the thermal infrared window bands (10.4 µm and 12.4 µm), with corrections for atmospheric absorption and water vapor.

**Same infrastructure as L1b Himawari**: This product uses the same NOAA AWS mirror (`noaa-himawari9`) as the Level-1b radiance data, inheriting all the same openness and accessibility benefits.

**Key difference from L1b**: L1b provides raw calibrated radiances (160 files per scan, one per band/segment). L2 SST is a **single global grid per 10-minute observation** — much lower volume, easier to ingest.

## Endpoint Analysis

**AWS S3 bucket verified** — same `noaa-himawari9` bucket, different product directory:

```bash
$ curl -s "https://noaa-himawari9.s3.amazonaws.com/?list-type=2&prefix=AHI-L2-FLDK-ISatSS/&max-keys=5&delimiter=/"
AHI-L2-FLDK-ISatSS/2026/
AHI-L2-FLDK-ISatSS/2025/
...
```

**Directory structure**:
```
AHI-L2-FLDK-ISatSS/
  {YYYY}/{MM}/{DD}/{HH}/
    HS_H09_{YYYYMMDD}_{HHMM}_L2SSTISSDAHIREALxx.nc
```

**File naming**:
- `HS` = Himawari Standard (JMA product code prefix)
- `H09` = Himawari-9
- `L2SSTISS` = Level-2 Sea Surface Temperature, ISatSS algorithm
- `DAHIREAL` = full disk, AHI, real-time
- `xx` = version number

**One file per 10-minute observation** — much simpler than L1b (160 files). Each file contains a global SST grid covering the full disk.

**Freshness**: Same 10-15 minute latency as L1b. Files appear on S3 shortly after observation time.

**Volume**: 144 files per day (one every 10 minutes), each ~10-30 MB (NetCDF4 compressed). Total ~2-4 GB/day — **very manageable**.

## Schema / Sample Metadata

NetCDF4 file with CF-1.7 conventions. Key variables:

```json
{
  "satellite": "Himawari-9",
  "instrument": "AHI",
  "product": "SST",
  "algorithm": "ISatSS",
  "observation_time": "2026-01-15T12:00:00Z",
  "processing_time": "2026-01-15T12:10:00Z",
  "spatial_resolution_km": 2.0,
  "projection": "Geostationary",
  "sub_lon": 140.7,
  "variables": {
    "sst": "Sea Surface Temperature (K or °C)",
    "quality_flag": "0=good, 1=marginal, 2=bad, 3=not processed",
    "latitude": "2D array",
    "longitude": "2D array"
  }
}
```

**Stable identifier**: `{observation_time}` is the natural key. One SST grid per timestamp.

**CloudEvents subject template**: `himawari/h09/ahi/sst/{timestamp}`  
**Kafka key template**: `h09-sst-{timestamp}`

**Event frequency**: 144 events per day (one every 10 minutes) — **ideal volume** for Kafka.

## Why This is Stronger Than L1b

1. **Lower volume**: 1 file per 10 min (vs 160 for L1b) — much easier to poll and ingest
2. **Single global grid**: No multi-segment stitching required
3. **Derived product**: SST is a directly usable oceanographic parameter (no additional processing needed)
4. **Same openness**: Inherits all AWS/NOAA open access benefits (no auth, no registration, public HTTP)

## Why This is Valuable

1. **Ocean temperature monitoring**: SST is critical for typhoon intensity forecasting, El Niño/La Niña tracking, coral bleaching alerts, and fisheries management
2. **10-minute temporal resolution**: World-class for geostationary SST (most polar orbiters are 1-2x per day)
3. **Full disk coverage**: Continuous SST monitoring across western Pacific and Indian Ocean from 60°S to 60°N
4. **Complements polar-orbiting sensors**: GCOM-W/AMSR2 provides all-weather microwave SST; Himawari provides clear-sky infrared SST at higher temporal resolution
5. **Operationally used**: Japan Meteorological Agency uses Himawari SST for typhoon forecasting and marine weather bulletins

## Limitations

1. **Clear-sky only**: Infrared SST requires cloud-free pixels. Clouds cause data gaps (quality flags mark cloudy pixels as invalid).
2. **Daytime/nighttime algorithm differences**: Some SST algorithms perform better at night (no solar contamination). Quality varies by time of day.
3. **Coastal/shallow water challenges**: SST algorithms can struggle in shallow or turbid coastal waters.
4. **Calibration drift**: Satellite IR sensors can drift over time; SST products require ongoing validation against buoy measurements.

## Verdict

**✅ Strongly Recommend** — Himawari L2 SST is a **flagship candidate**:
- **Easier to implement than L1b** (lower volume, single file per observation)
- **Directly usable ocean parameter** (no post-processing required)
- **Same open access as L1b** (AWS S3, no auth)
- **10-minute cadence** (world-class temporal resolution)
- **Complements other ocean sources** (pairs well with GCOM-W/AMSR2 for all-weather coverage)

**Bridge pattern**: Poll S3 bucket `AHI-L2-FLDK-ISatSS/{YYYY}/{MM}/{DD}/{HH}/` every 5 minutes, detect new NetCDF files, download (or reference S3 URL), extract metadata (timestamp, grid bounds, QA summary), emit CloudEvent.

**Event structure**:
- **Type**: `himawari.ahi.sst.observation`
- **Subject**: `himawari/h09/ahi/sst/{timestamp}` (e.g., `himawari/h09/ahi/sst/20260115T1200Z`)
- **Key**: `h09-sst-{timestamp}`
- **Payload**: Metadata + S3 URL reference (not the full NetCDF grid — too large for Kafka)

**Scope**: Start with SST only. Other L2 products (clouds, winds) can be added later if successful.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3 | Critical ocean parameter, typhoon forecasting, fisheries, climate monitoring |
| Freshness | 3 | 10-minute observations, 10-15 min latency to S3 — near-real-time |
| Openness | 3 | Public AWS S3, no auth, no registration, free redistribution |
| Schema Clarity | 2 | NetCDF4/CF conventions, well-documented schema, but binary not JSON |
| Machine-Readability | 3 | S3 REST API, regular file structure, NetCDF4 parseable with standard libraries |
| Repo-Fit | -1 | New domain (satellite ocean products), S3 polling pattern, but much cleaner than L1b |

**Score: 13/18** — Excellent candidate. Strongly recommend over L1b (lower volume, more directly usable).
