# KARI GEO-KOMPSAT-2A AMI Weather Imagery

- **Country/Region**: South Korea / East Asia (Full disk similar to Himawari)
- **Endpoint**: https://nmsc.kma.go.kr/enhome (KMA National Meteorological Satellite Center)
- **Protocol**: Web portal, proprietary broadcast (HRIT/LRIT), limited open data access
- **Auth**: Registration required for full data, limited samples public
- **Format**: NetCDF4, GRIB2, GeoTIFF (products), HDF5 (L1b)
- **Freshness**: 10 minutes (full disk), 2 minutes (regional)
- **Docs**: https://nmsc.kma.go.kr/enhome/html/base/cmm/selectPage.do?page=satellite.gk2a.intro
- **Score**: 6/18

## Overview

GEO-KOMPSAT-2A (GK-2A), launched in 2018 and stationed at 128.2°E, carries the Advanced Meteorological Imager (AMI) — a 16-channel multispectral imager similar to Himawari-8/9 AHI and GOES-16/17 ABI. AMI provides full-disk imagery every 10 minutes, regional scans every 2 minutes, and has 0.5–2 km spatial resolution depending on the channel.

GK-2A covers the Korean Peninsula, Japan, China, Southeast Asia, and the western Pacific — overlapping significantly with Himawari-9's coverage but from a different longitude (128.2°E vs 140.7°E).

**Critical limitation**: Unlike Himawari (which is mirrored to AWS by NOAA), **GK-2A data is not widely distributed through open cloud platforms**. The Korea Meteorological Administration (KMA) National Meteorological Satellite Center (NMSC) portal at https://nmsc.kma.go.kr is the primary distribution point, but **open data access is limited**.

## Endpoint Analysis

**NMSC portal verified** — https://nmsc.kma.go.kr/enhome/html/base/cmm/selectPage.do?page=satellite.gk2a.intro provides information about GK-2A and AMI.

**Data distribution channels**:
1. **Satellite broadcast (HRIT/LRIT)** — real-time data broadcast to ground stations (requires satellite receiver hardware, not Internet-accessible)
2. **NMSC web portal** — sample imagery and basic products (registration may be required for bulk access)
3. **Open API** — NMSC mentions "Open API" on the GK-2A page, but **no public API documentation was found** in English
4. **FTP server** — existence and accessibility unclear
5. **DCPC** (Data Collection and Production Center) — mentioned for user data access, but details sparse

**Attempts to locate Open API documentation**:
- https://nmsc.kma.go.kr/enhome/html/base/cmm/selectPage.do?page=static.edu.openApi → redirects to error page
- https://data.nmsc.kma.go.kr → connection refused (server may be internal-only or offline)

**No AWS/cloud mirror detected**: Unlike NOAA's mirroring of Himawari to `noaa-himawari9` S3 bucket, there is no known public cloud mirror of GK-2A data.

**Korean-language barrier**: Most detailed documentation and data access instructions are in Korean. English pages are limited to high-level overviews.

**Products available** (if accessible):
- **AMI Level 1b** — calibrated radiances, 16 channels, full disk every 10 min
- **AMI Level 2** — 52 meteorological products including cloud mask, SST, winds, fog, volcanic ash, typhoon tracking, etc.

**Freshness**: 10-minute full disk, 2-minute extended local area (Korea), similar to Himawari. If data were openly accessible, freshness would be excellent.

## Why Openness is a Problem

1. **No documented public API**: "Open API" is mentioned but not findable. English documentation is sparse.
2. **Registration process unclear**: Whether free registration provides programmatic access (FTP, API key) is undocumented in English.
3. **Korean-language primary documentation**: Data access guides are in Korean, creating a language barrier for international users.
4. **No cloud mirror**: Unlike Himawari (AWS), GOES (AWS), Meteosat (EUMETSAT), GK-2A data is not openly redistributed.
5. **Satellite broadcast focus**: KMA emphasizes the HRIT/LRIT broadcast (for national meteorological services with ground receivers), not Internet-based open data.

## Comparison to Himawari

| Feature | Himawari-9 (JMA) | GEO-KOMPSAT-2A (KMA) |
|---------|------------------|----------------------|
| Instrument | AHI (16 bands) | AMI (16 bands) |
| Full disk cadence | 10 minutes | 10 minutes |
| Regional cadence | 2.5 minutes | 2 minutes |
| Coverage | 140.7°E (Japan-centric) | 128.2°E (Korea-centric) |
| Open data access | ✅ AWS S3 (NOAA mirror) | ❌ No public cloud mirror |
| API/download | ✅ S3 HTTP/API, no auth | ❌ Portal/FTP, registration unclear |
| English docs | ✅ Extensive | ⚠️ Limited |

**Verdict on overlap**: GK-2A and Himawari cover overlapping geographic areas with similar sensors and cadences. **Himawari is already mirrored openly to AWS** with no authentication. GK-2A adds marginal value (slightly different viewing angle) but comes with much higher access barriers.

## Verdict

**❌ Skip** — GK-2A/AMI is technically strong (world-class geostationary sensor, 10-minute full disk, 16 bands) but **data access barriers disqualify it**:
- No public API or cloud mirror
- Registration process and data access pathways undocumented in English
- Korean-language barrier
- **Himawari-9 already provides similar coverage with open AWS access**

**Recommendation**: Pursue Himawari-9 AWS mirror instead. GK-2A would only add value if:
1. KMA publishes GK-2A data to AWS/Azure/GCP with open access (unlikely)
2. A specific use case requires the 128.2°E viewing angle (e.g., better coverage of western China or India)
3. KMA provides clear English API documentation and removes registration barriers

Until then, GK-2A is **not viable** for this repo's open data mission.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3 | World-class geostationary weather sensor, 16-band multispectral, 10-min full disk |
| Freshness | 3 | 10-minute full disk, 2-minute regional — excellent cadence |
| Openness | 0 | No public API or cloud mirror, registration unclear, Korean-language docs — **major barrier** |
| Schema Clarity | 1 | NetCDF4/HDF5 likely (similar to Himawari), but schema docs in Korean |
| Machine-Readability | 0 | No accessible machine-readable endpoint detected |
| Repo-Fit | -1 | Overlaps with Himawari (already openly available), access barriers make it non-viable |

**Score: 6/18** — Not viable. Himawari-9 provides equivalent open coverage. GK-2A is disqualified by access barriers.
