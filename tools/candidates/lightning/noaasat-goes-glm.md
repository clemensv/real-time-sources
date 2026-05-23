# NOAA GOES Geostationary Lightning Mapper (GLM)

- **Country/Region**: USA / Americas (GOES-East and GOES-West coverage)
- **Endpoint**: S3 bucket `s3://noaa-goes16/GLM-L2-LCFA/` (also GOES-17, GOES-18, GOES-19)
- **Protocol**: S3 (AWS Open Data Program)
- **Auth**: None (public S3 bucket)
- **Format**: NetCDF4
- **Freshness**: 20-second cadence (per satellite)
- **Docs**: https://www.goes-r.gov/products/baseline-lightning-detection.html
- **Score**: 12/18

## Overview

The Geostationary Lightning Mapper (GLM) is an optical transient detector aboard GOES-R series satellites (GOES-16/17/18/19). GLM continuously monitors the Americas for lightning flashes, detecting both cloud-to-ground (CG) and intra-cloud (IC) lightning at 500 Hz. GLM products are published every 20 seconds via NOAA's Big Data Program on AWS S3.

GLM data is used for:
- **Severe weather nowcasting**: Rapid increases in lightning indicate storm intensification
- **Aviation safety**: Convective hazard detection for flight planning
- **Fire ignition detection**: Lightning-caused wildfires in dry regions
- **Tornado warning**: Lightning jump signatures precede tornadogenesis

GLM Level 2 Lightning Detection product (L2-LCFA) contains:
- **Events**: Individual pixel detections (~8 km resolution)
- **Groups**: Clusters of events within 16.5 km / 330 ms
- **Flashes**: Aggregated lightning flashes (final scientific product)

Each GOES satellite (East/West) produces ~4,320 files per day (1 file every 20 seconds).

## Endpoint Analysis

**S3 bucket structure verified:**

```
s3://noaa-goes16/GLM-L2-LCFA/{YYYY}/{DDD}/{HH}/
```

Where:
- `{YYYY}` = 4-digit year
- `{DDD}` = Day of year (001-366)
- `{HH}` = Hour (00-23)

Example file:
```
OR_GLM-L2-LCFA_G16_s20261420010000_e20261420011000_c20261420011019.nc
```

Filename breakdown:
- `OR` = Operational Real-time
- `GLM-L2-LCFA` = Product (Lightning Detection: Events, Groups, Flashes)
- `G16` = GOES-16
- `s20261420010000` = Start time (YYYYDDDHHMMSS)
- `e20261420011000` = End time
- `c20261420011019` = Creation time

**Data format**: NetCDF4 (HDF5-based), **not JSON**. Each file contains:
- `event_id`, `event_time_offset`, `event_lat`, `event_lon`, `event_energy`
- `group_id`, `group_time_offset`, `group_lat`, `group_lon`, `group_energy`, `group_area`
- `flash_id`, `flash_time_offset`, `flash_lat`, `flash_lon`, `flash_energy`, `flash_area`, `flash_quality_flag`

**Volume**: ~180 MB/hour per satellite (uncompressed), ~4.3 GB/day/satellite.

**Key model**: `{flash_id}` for flashes, `{group_id}` for groups, `{event_id}` for events. Each flash can contain multiple groups and events.

## Schema / Sample

NetCDF4 structure (simplified):
```
dimensions:
    event_id = UNLIMITED;
    group_id = UNLIMITED;
    flash_id = UNLIMITED;

variables:
    int event_id(event_id);
    double event_time_offset(event_id); // seconds since file start
    float event_lat(event_id);
    float event_lon(event_id);
    short event_energy(event_id); // picojoules

    int flash_id(flash_id);
    double flash_time_offset(flash_id);
    float flash_lat(flash_id);
    float flash_lon(flash_id);
    int flash_area(flash_id); // km²
    short flash_energy(flash_id);
    byte flash_quality_flag(flash_id);
```

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3/3 | Critical for severe weather nowcasting and aviation safety |
| Freshness | 3/3 | 20-second cadence, near-real-time lightning detection |
| Openness | 3/3 | No auth, AWS Open Data, free egress |
| Schema Clarity | 2/3 | NetCDF4 well-documented but requires domain knowledge |
| Machine-Readability | 1/3 | NetCDF4 (not JSON) — requires xarray/netCDF4 library |
| Repo Fit | 0/3 | **Large binary files** (not streaming JSON) — poor fit for HTTP poller |

**Total: 12/18**

- Geostationary lightning detection is **unique** and operationally significant
- 20-second cadence is excellent
- Flash/group/event hierarchy provides multi-scale analysis
- AWS S3 public access with no auth
- **However**: NetCDF4 files are 5-15 MB each, ~4.3 GB/day — not suited to this repo's polling model
- No JSON/REST API alternative (only S3 files)

## Limitations

- **Binary NetCDF4 format** — not JSON-parseable
- **Large file sizes** (5-15 MB per 20-second file)
- **High volume** (4,320 files/day/satellite, 17,280 files/day for 4 satellites)
- Requires NetCDF4 library (Python: xarray, netCDF4; not simple HTTP+JSON)
- No event-level REST API or WebSocket stream
- Coverage limited to Americas (GOES satellites view Western Hemisphere)
- Flash detection algorithm can miss low-energy IC flashes
- GOES-17 had ABI cooling issues (affected GLM availability 2018-2022)

## Verdict

**SKIP** — While GLM is scientifically and operationally significant, the **S3 NetCDF4 file delivery model** is incompatible with this repo's HTTP poller + JSON paradigm. A GLM bridge would need to:
1. Poll S3 listings every 20 seconds
2. Download 5-15 MB NetCDF4 files
3. Parse with xarray/netCDF4
4. Extract flash/group/event records
5. Emit ~100-10,000 events per file to Kafka

This is feasible but represents a **different integration pattern** (S3 file processor vs. REST poller). Consider GLM only if the repo adds support for S3-based satellite products. For now, **defer** due to format/volume mismatch. If a JSON-based GLM summary API emerges (e.g., SWPC lightning statistics), revisit.
