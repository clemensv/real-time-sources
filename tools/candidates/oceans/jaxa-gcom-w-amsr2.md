# JAXA G-Portal GCOM-W/AMSR2 Ocean Products

- **Country/Region**: Japan / Global (polar-orbiting)
- **Endpoint**: `https://gportal.jaxa.jp/gpr/` (web portal + SFTP)
- **Protocol**: SFTP download (registration required), CSW catalog search
- **Auth**: Free registration required (Registered User or Specified User tiers)
- **Format**: HDF5, NetCDF (Level 2/3)
- **Freshness**: Near-real-time (NRT) products available within 3 hours of observation
- **Docs**: https://gportal.jaxa.jp/gpr/information?lang=en
- **Score**: 10/18

## Overview

JAXA's Global Change Observation Mission - Water (GCOM-W1), also known as "Shizuku", carries the Advanced Microwave Scanning Radiometer 2 (AMSR2), a passive microwave radiometer providing all-weather observations of sea surface temperature (SST), sea ice concentration, soil moisture, precipitation, and atmospheric water vapor.

G-Portal is JAXA's primary Earth observation data portal, distributing GCOM-W, Aqua/AMSR-E, ALOS, ALOS-2, and GCOM-C products. Near-real-time (NRT) AMSR2 data is available within 3 hours of observation, with both Level 2 (swath) and Level 3 (gridded daily) products.

**Key strength**: AMSR2 is the world's most capable passive microwave ocean sensor, providing SST through clouds (microwave penetration), critical for typhoon monitoring and polar sea ice analysis.

**Registration barrier**: G-Portal requires user registration (free, but email verification and approval process). Two tiers: Registered User (password auth) and Specified User (SSH key auth). This is a **moderate openness penalty** but not a disqualifier.

## Endpoint Analysis

**G-Portal web interface verified** — https://gportal.jaxa.jp/gpr/ provides search, visualization, and download. User manual available at https://gportal.jaxa.jp/gpr/assets/mng_upload/COMMON/upload/GPortalUserManual_en.pdf

**Data access methods**:
1. **Web download** — search by map/time, add to cart, download via browser (interactive, not suitable for automation)
2. **SFTP** — programmatic bulk download (requires registration, recommended for bridge)
3. **CSW catalog** — OGC Catalog Service for the Web (XML metadata search, can query for latest products)

**SFTP structure** (example from user manual):
```
gportal.jaxa.jp (port 22, SFTP only, FTP discontinued April 2025)
/data/GCOM-W/AMSR2/L2/
  SST/
    {YYYY}/{MM}/{DD}/
      GW1AM2_{YYYYMMDD}_{hhmm}_{orbit}_L2SGSSTLF3300300.h5
/data/GCOM-W/AMSR2/L3/
  SST_D/
    {YYYY}/{MM}/
      GW1AM2_{YYYYMMDD}_01D_EQOD_L3SGSSTLA3300300.h5
```

**Products of interest (NRT availability)**:
- **L2 SST** (Sea Surface Temperature, swath) — ~1400 km swath, 10 km resolution, NRT within 3 hours
- **L2 SIC** (Sea Ice Concentration) — polar regions, 10 km, NRT
- **L2 SWS** (Soil Moisture) — land, 10 km, NRT
- **L2 PRC** (Precipitation) — 10 km, NRT
- **L3 daily gridded** versions of above — 0.25° global grids, one file per day

**Freshness verification**: User manual states "NRT products are available within 3 hours of observation". GCOM-W1 is polar-orbiting (not geostationary), so any given location is observed 1-2 times per day. The "freshness" is high (3-hour latency) but coverage is **not continuous** like Himawari.

**CSW catalog query** (OGC standard):
```
GET https://gportal.jaxa.jp/csw/csw?
  service=CSW&version=2.0.2&request=GetRecords&
  constraint=datasetId='GW1AM2__L2SGSSTLF'&
  constraint_language_version=1.1.0
```

Returns XML with metadata for available granules. This is machine-queryable but verbose (XML parsing required).

## Schema / Sample Metadata

AMSR2 products are HDF5 or NetCDF with well-defined schemas. Example L2 SST metadata:

```json
{
  "satellite": "GCOM-W1",
  "sensor": "AMSR2",
  "processing_level": "L2",
  "product_name": "SST",
  "observation_start": "2026-01-15T03:45:00Z",
  "observation_end": "2026-01-15T05:20:00Z",
  "orbit_number": 54321,
  "swath_width_km": 1450,
  "resolution_km": 10,
  "variables": ["sst", "wind_speed", "water_vapor", "cloud_liquid_water"],
  "geolocation_included": true,
  "format": "HDF5"
}
```

**Stable identifiers**: Orbit number + product type is a stable key. File naming is deterministic: `GW1AM2_{YYYYMMDD}_{hhmm}_{orbit}_L2SGSSTLF3300300.h5`

**CloudEvents subject template**: `gcom-w/amsr2/l2/{product}/{orbit}`  
**Kafka key template**: `gcom-w-{product}-{orbit}`

Each orbit file contains a full swath (ascending or descending pass). One satellite pass takes ~100 minutes and covers a ~1400 km wide strip from pole to pole. A bridge would emit one event per orbit per product type.

**Volume estimate**: GCOM-W1 completes ~14 orbits per day. With 4 NRT L2 products (SST, SIC, soil moisture, precip), that's ~56 events/day at the L2 level, or 4 events/day at the L3 daily grid level. **Very manageable volume.**

## Why This is Valuable

1. **All-weather ocean observation**: AMSR2 microwave radiometry works through clouds, unlike infrared SST (Himawari). Critical for typhoons, polar regions, and persistent cloud cover areas.
2. **Sea ice monitoring**: AMSR2 is the operational data source for Arctic/Antarctic sea ice extent tracking (NSIDC uses AMSR2 for daily sea ice reports).
3. **Soil moisture**: L-band microwave soil moisture is a key climate variable, used for drought monitoring and agricultural forecasting.
4. **JAXA operational mission**: GCOM-W1 launched 2012, still operational, expected to continue through 2020s.
5. **Complementary to Himawari**: Polar-orbiting microwave (AMSR2) complements geostationary infrared/visible (Himawari). Together they cover full day/night, all-weather Earth observation.

## Limitations

1. **Registration required**: Free but not instant — email verification, approval process (typically 1-2 business days for Registered User tier). **Moderate openness penalty.**
2. **SFTP only for automation**: Web download is manual; CSW is queryable but XML-heavy. SFTP is the cleanest programmatic path but requires SSH client library.
3. **HDF5/NetCDF format**: Not JSON. Requires `h5py` or `netCDF4` libraries to parse. Metadata extraction is more complex than REST JSON.
4. **Polar-orbiting coverage**: Not continuous like geostationary — each location observed 1-2x per day. Bridge would emit events in bursts as new orbits are processed.
5. **File size**: L2 orbit files are ~200-500 MB each (HDF5 compressed). Cannot emit raw file as CloudEvents payload — must extract metadata + reference SFTP URL or download separately.
6. **CSW catalog may lag**: CSW metadata updates may not be as fast as SFTP file publication. Polling SFTP directory listings directly may be more reliable for NRT detection.

## Verdict

**✅ Recommend (with caveats)** — GCOM-W/AMSR2 is a strong scientific candidate for ocean (SST, sea ice) and land (soil moisture) monitoring. The registration barrier is a moderate openness penalty (score 2/3 instead of 3/3) but the data quality and freshness are excellent.

**Best scope**: Start with **L3 daily gridded SST and Sea Ice Concentration** (one file per day per product). This avoids the complexity of swath geometry (L2) and provides a global gridded view. Emit 2 events per day (SST + SIC). Volume is minimal, and L3 grids are easier to visualize/analyze than L2 swaths.

**Bridge pattern**: Poll SFTP directory `/data/GCOM-W/AMSR2/L3/SST_D/{YYYY}/{MM}/` daily, detect new files, SFTP download, extract HDF5 metadata (observation date, grid bounds, QA summary), emit CloudEvent with SFTP URL reference.

**Alternative if registration is blocking**: Check if any AMSR2 NRT products are mirrored to public servers (e.g., NOAA, EUMETSAT, NASA LANCE). However, G-Portal is the authoritative JAXA source.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3 | World-class microwave ocean/land sensor, critical for sea ice + all-weather SST |
| Freshness | 2 | NRT within 3 hours of observation, but polar-orbiting (1-2 passes/day per location) |
| Openness | 2 | Free registration required (email verify, 1-2 day approval), SFTP access thereafter |
| Schema Clarity | 2 | HDF5/NetCDF with documented schema, CF-compliant, but binary not JSON |
| Machine-Readability | 2 | SFTP + CSW catalog queryable, HDF5 parseable, but not REST JSON |
| Repo-Fit | -1 | New transport (SFTP polling), new format (HDF5), but polar-orbit cadence is manageable |

**Score: 10/18** — Solid candidate with scientific value. Registration barrier lowers openness score, but data quality justifies the effort. Recommend L3 daily grids (SST + sea ice) as initial scope.
