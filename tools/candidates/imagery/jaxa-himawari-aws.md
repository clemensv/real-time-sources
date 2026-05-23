# JAXA Himawari-8/9 AHI Full Disk Imagery (AWS Mirror)

- **Country/Region**: Japan / Asia-Pacific (full disk coverage 60°S-60°N, 80°E-160°W)
- **Endpoint**: `s3://noaa-himawari9/` (AWS S3, NOAA mirror)
- **Protocol**: HTTP (S3 REST), no auth
- **Auth**: None
- **Format**: NetCDF4 (Level-1b), HDF5 (Level-2)
- **Freshness**: 10 minutes (full disk), 2.5 minutes (regional)
- **Docs**: https://www.data.jma.go.jp/mscweb/en/himawari89/space_segment/spsg_ahi.html
- **Score**: 14/18

## Overview

Himawari-8 and Himawari-9 are Japanese geostationary meteorological satellites operated by the Japan Meteorological Agency (JMA), stationed at 140.7°E. The Advanced Himawari Imager (AHI) provides 16-band multispectral imagery covering east Asia and the western/central Pacific from 35,800 km altitude, with full-disk scans every 10 minutes and regional scans as frequent as every 30 seconds.

NOAA mirrors Himawari data to AWS S3 (`noaa-himawari9`) with no authentication required, making it one of the most accessible near-real-time satellite imagery feeds from an Asian space agency. Data is available in near-real-time (typically 10-15 minutes from observation to S3 publication).

The AHI has dramatically better capabilities than its predecessor (MTSAT): 16 spectral bands (vs 5), 0.5-2 km resolution (vs 1-4 km), and 10-minute full disk scans (vs 30 minutes). True-color RGB composites are possible using visible bands B1 (blue 0.47µm), B2 (green 0.51µm), and B3 (red 0.64µm).

## Endpoint Analysis

**AWS S3 bucket verified** — the NOAA mirror is publicly accessible via HTTP and S3 API.

```bash
$ curl -s "https://noaa-himawari9.s3.amazonaws.com/?list-type=2&max-keys=10&delimiter=/" | grep -o "Prefix>.*<"
Prefix>AHI-L1b-FLDK/<
Prefix>AHI-L1b-Japan/<
Prefix>AHI-L1b-Target/<
Prefix>AHI-L2-FLDK-Clouds/<
Prefix>AHI-L2-FLDK-ISatSS/<
Prefix>AHI-L2-FLDK-Winds/<
```

**Directory structure**:
- `AHI-L1b-FLDK/` — Full Disk Level-1b calibrated radiances (all 16 bands)
- `AHI-L1b-Japan/` — Japan Area (Regions 1+2), 2.5-minute cadence
- `AHI-L1b-Target/` — Target Area (Region 3, movable), 2.5-minute cadence
- `AHI-L2-FLDK-Clouds/` — Cloud products (cloud mask, type, height, optical thickness)
- `AHI-L2-FLDK-ISatSS/` — Sea Surface Temperature
- `AHI-L2-FLDK-Winds/` — Atmospheric motion vectors

**Path pattern**: `AHI-L1b-FLDK/{YYYYMMDD}/{HH}/HS_H09_{YYYYMMDD}_{HHMM}_BNN_FLDK_R21_Sssss.DAT.bz2`
- `H09` = Himawari-9 (operational), `H08` = Himawari-8 (backup)
- `BNN` = Band number (B01-B16)
- `R21` = Resolution (full, half, quarter)
- `Sssss` = Segment number (01-10 for full disk)

Files are NetCDF4 (Level-1b) or HDF5 (Level-2), bzip2 compressed. Each band/segment is a separate file.

**Freshness probe** — data appears within 10-15 minutes of observation time. Archive extends back to July 2015.

**Volume estimate**: Full disk scan = 10 segments × 16 bands = 160 files every 10 minutes = ~23,000 files/day. Each file ~5-15 MB compressed. Total ~2-3 TB/day raw.

## Schema / Sample Metadata

Himawari AHI data follows JMA's standard NetCDF schema. Key metadata fields:

```json
{
  "satellite": "Himawari-9",
  "instrument": "AHI",
  "observation_time": "2026-01-15T12:00:00Z",
  "observation_area": "FLDK",
  "band_number": 13,
  "central_wavelength_um": 10.4073,
  "spatial_resolution_km": 2.0,
  "segment": 5,
  "projection": "Geostationary",
  "sub_lon": 140.7,
  "pixel_count_ns": 5500,
  "pixel_count_ew": 5500
}
```

**Stable identifiers**: Each file can be keyed by `{observation_time}/{band}/{segment}`. The temporal component provides natural partitioning.

**CloudEvents subject template**: `himawari/{satellite}/ahi/{area}/{band}/{segment}/{timestamp}`  
**Kafka key template**: `{satellite}-{area}-{band}-{timestamp}`

The high file volume (160 files every 10 minutes) suggests either:
1. Event per band (16 events/10min, each referencing 10 segment files)
2. Event per file (160 events/10min)
3. Event per full-disk scan (1 event/10min, referencing all 160 files)

Option 1 (event per band) is the sweet spot — manageable volume, preserves band-level granularity.

## Why This is Strong

1. **Freshness**: 10-minute full-disk cadence is world-class for geostationary satellites. Regional scans are 2.5 minutes (Japan Area) or 30 seconds (Landmark Areas).
2. **Openness**: NOAA AWS mirror has no authentication, no registration, no rate limits. Public bucket policy. JMA allows free redistribution with attribution.
3. **Stability**: JMA operational mission since 2015 (Himawari-8) and 2016 (Himawari-9). NOAA mirror has been reliable since 2015. Documented, versioned file format.
4. **Scientific value**: 16-band AHI is used globally for typhoon tracking, wildfire detection, volcanic ash monitoring, nowcasting, and ocean color. Critical for Asia-Pacific disaster response.
5. **Rich metadata**: NetCDF/HDF5 with CF-compliant metadata. Calibration coefficients, geolocation grids, quality flags all embedded.
6. **Repo fit**: This would be the first geostationary satellite bridge in the repo, the first Asian satellite source, and the first S3-native polling pattern.

## Limitations

1. **Volume**: 160 files every 10 minutes (full disk) is high. Bridge would need to selectively poll (e.g., only certain bands, or only full-disk summary events).
2. **File size**: Individual files are 5-15 MB compressed, 50-150 MB uncompressed. Bridge cannot emit the raw NetCDF as CloudEvents payload — must extract metadata and reference the S3 URL.
3. **Format complexity**: NetCDF4/HDF5 requires `netCDF4` or `h5py` Python libraries. Not simple JSON.
4. **No push notification**: S3 bucket does not publish SNS/SQS events. Bridge must poll the bucket (LIST operations can be slow).
5. **Derived products**: Level-2 products (clouds, SST, winds) have different schemas and update cadences. Bridge scope needs to be clearly defined (L1b only? Include L2?).
6. **Regional scans**: Japan/Target areas have faster cadence but different file naming and coverage. Complicates the bridge if included.

## Verdict

**✅ Recommend** — proceed with Himawari AHI Full Disk Level-1b (all 16 bands) as the initial scope. Emit one CloudEvents message per band per 10-minute scan (16 events every 10 minutes), each referencing the S3 URLs of the 10 segment files for that band. Subject/key on `{satellite}-{band}-{timestamp}`.

This is a flagship candidate: operated by a major space agency (JAXA/JMA), globally used for operational meteorology, openly accessible via AWS, and fills a major gap in the repo (no geostationary satellites, no Asian satellite sources). The polling pattern (S3 LIST + metadata extraction) is new to the repo but manageable.

**Next steps**:
1. Prototype S3 polling logic (boto3 or HTTP LIST, parse XML, detect new timestamps).
2. Install `netCDF4` or `h5py`, open one sample file, extract minimal metadata (timestamp, band, segment, calibration summary).
3. Design xreg manifest with one message group per band, subject = `himawari/h09/ahi/fldk/{band}/{timestamp}`, key = `h09-fldk-{band}-{timestamp}`.
4. Decide: emit segment-level granularity (160 events/scan) or band-level (16 events/scan, payload lists 10 segment URLs)? **Recommend band-level** to keep Kafka volume reasonable.
5. Test freshness: poll bucket every 5 minutes, measure lag from `observation_time` in filename to S3 `LastModified`.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3 | World-class geostationary coverage, 16-band multispectral, operational use for typhoons/fires/ash |
| Freshness | 3 | 10-minute full disk, 2.5-minute regional — near-real-time |
| Openness | 3 | Public AWS S3, no auth, no registration, free redistribution with attribution |
| Schema Clarity | 2 | NetCDF4/HDF5 with CF metadata — well documented but binary, not JSON |
| Machine-Readability | 2 | Requires NetCDF/HDF5 libraries, file structure is regular and parseable |
| Repo-Fit | 1 | New domain (satellite imagery), new protocol (S3 polling), high volume — requires scoping |

**Score: 14/18** — Strong candidate, flagship quality, requires careful scoping and S3 polling pattern development.
