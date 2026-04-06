# NOAA GLM (Geostationary Lightning Mapper) — GOES-19/18

**Country/Region**: Western Hemisphere (Americas, Atlantic, eastern Pacific)
**Publisher**: NOAA / NESDIS via AWS Open Data Program
**API Endpoint**: `https://noaa-goes19.s3.amazonaws.com/GLM-L2-LCFA/` (GOES-19 East), `https://noaa-goes18.s3.amazonaws.com/GLM-L2-LCFA/` (GOES-18 West)
**Documentation**: https://registry.opendata.aws/noaa-goes/
**Protocol**: AWS S3 (HTTPS REST), SNS push notifications
**Auth**: None — fully open, anonymous S3 access
**Data Format**: NetCDF-4 (CF-compliant)
**Update Frequency**: Every 20 seconds (180 files/hour per satellite)
**License**: Public Domain — NOAA Open Data

## What It Provides

The Geostationary Lightning Mapper (GLM) is an optical instrument on NOAA's GOES geostationary satellites that detects total lightning — both cloud-to-ground (CG) and intra-cloud (IC) — from geostationary orbit. It produces the Lightning Cluster-Filter Algorithm (LCFA) Level 2 product with three hierarchical detection levels:

- **Events** — individual optical pulses (most granular)
- **Groups** — spatially and temporally clustered events from a single flash
- **Flashes** — complete lightning discharge events (most useful for applications)

Each entity includes latitude, longitude, time, radiant energy, and area.

### Satellite Coverage

| Satellite | Position | Status | Data Range |
|---|---|---|---|
| GOES-19 | 75.2°W (East) | Operational since Apr 2025 | 2025–present |
| GOES-18 | 137.2°W (West) | Operational | 2022–present |
| GOES-16 | — (retired from East) | Archive only | 2018–2025 (day 010) |

Together, GOES-19 and GOES-18 provide continuous lightning monitoring across the entire Western Hemisphere.

## API Details

### S3 File Listing

```
GET https://noaa-goes19.s3.amazonaws.com/?list-type=2&prefix=GLM-L2-LCFA/{YYYY}/{DDD}/{HH}/&max-keys=100
```

File naming convention: `OR_GLM-L2-LCFA_G{sat}_s{start}_e{end}_c{created}.nc`

### File Characteristics

- **Cadence**: Every 20 seconds
- **Size**: ~150–370 KB per file
- **Latency**: Files appear on S3 within ~30–40 seconds of observation window end
- **Format**: NetCDF-4 (CF-compliant) containing events, groups, and flashes with coordinates, energy, area, quality flags

### SNS Push Notifications

```
arn:aws:sns:us-east-1:123901341784:NewGOES19Object
arn:aws:sns:us-east-1:123901341784:NewGOES18Object
```

Subscribe to these SNS topics for event-driven ingest — get notified the moment new files land on S3.

### Sample File Listing (GOES-19, 2026-04-06 09:00 UTC)

```
GLM-L2-LCFA/2026/096/09/OR_GLM-L2-LCFA_G19_s20260960900000_e20260960900200_c20260960900223.nc  372,540 bytes
GLM-L2-LCFA/2026/096/09/OR_GLM-L2-LCFA_G19_s20260960900200_e20260960900400_c20260960900419.nc  341,820 bytes
GLM-L2-LCFA/2026/096/09/OR_GLM-L2-LCFA_G19_s20260960900400_e20260960901000_c20260960901019.nc  345,916 bytes
```

## Freshness Assessment

Exceptional. New files every 20 seconds with ~30–40 seconds S3 ingestion latency. This means sub-minute end-to-end latency from lightning strike to data availability. SNS notifications enable push-based ingestion. Verified live on 2026-04-06 with current-hour files on both GOES-19 and GOES-18 S3 buckets.

## Entity Model

GLM LCFA products contain three hierarchical entity types per file:

- **Flash** — complete lightning discharge (lat, lon, time, energy, area, quality). This is the primary unit for most applications.
- **Group** — spatially/temporally clustered events within a flash (more granular).
- **Event** — individual optical pulse detected by the CCD array (most granular, highest volume).

Each entity type includes: latitude, longitude, time (nanosecond precision), radiant energy (Joules), area (km²), quality flags.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | 20-second file cadence, sub-minute S3 latency |
| Openness | 3 | No auth, fully public S3, public domain |
| Stability | 3 | NOAA production infrastructure, AWS Open Data Program |
| Structure | 3 | NetCDF-4 CF-compliant, well-documented schema |
| Identifiers | 2 | Flash/group/event IDs within files but no persistent cross-file IDs |
| Additive Value | 3 | Only open source of total lightning (IC + CG) for Western Hemisphere, satellite-based, continuous |
| **Total** | **17/18** | |

## Notes

- This is the single best open lightning data source discovered. No authentication, 20-second update cadence, production-grade AWS infrastructure, SNS push notifications — it checks every box.
- NetCDF-4 format requires a NetCDF library to parse (e.g., Python netCDF4, xarray) — not as simple as JSON, but standard in atmospheric science.
- The GLM detects total lightning (CG + IC), which is ~5x more lightning than CG-only networks detect. IC lightning is a strong predictor of severe weather intensification.
- Coverage is limited to the Western Hemisphere (GOES field of view). For Eastern Hemisphere coverage, combine with EUMETSAT MTG-LI.
- Historical archive available: GOES-16 from 2018, GOES-18 from 2022, GOES-19 from 2025.
- Consider using GOES-derived imagery products alongside GLM data — the same S3 buckets host ABI (Advanced Baseline Imager) data.
