# EUMETSAT Metop IASI Hyperspectral Sounder

- **Country/Region**: Global (polar orbit coverage)
- **Endpoint**: EUMETSAT Data Store, EARS-IASI (regional rapid), BUFR/GTS
- **Protocol**: NetCDF, HDF5, BUFR download
- **Auth**: Free EUMETSAT registration
- **Format**: NetCDF-4, HDF5, BUFR
- **Freshness**: Near-real-time (~3 hours global, ~30-90 min EARS regional)
- **Docs**: https://www.eumetsat.int/iasi
- **Score**: 11/18

## Overview

The Infrared Atmospheric Sounding Interferometer (IASI) on Metop-A/B/C provides **hyperspectral infrared soundings** (8,461 spectral channels from 3.62-15.5 µm). IASI measures:

- **Temperature profiles** (surface to 40 km)
- **Humidity profiles** (water vapor vertical distribution)
- **Trace gases**: O3, CO, CO2, CH4, N2O, SO2, NH3, HNO3
- **Surface properties**: Skin temperature, emissivity

**Why IASI matters**:
- **Numerical weather prediction**: High-quality atmospheric profiles for data assimilation
- **Volcanic ash**: SO2 plume detection for aviation safety
- **Air quality**: CO and NH3 for pollution monitoring
- **Climate**: Long-term trace gas records (Metop-A since 2006)

IASI is one of the **most important sounders for global NWP** (ECMWF, NOAA use extensively).

## Endpoint Analysis

**EUMETSAT Data Store**:
```
GET https://api.eumetsat.int/data/browse/collections?q=IASI
```

**Distribution channels**:
- **Global NRT**: ~3 hours from observation (via Data Store)
- **EARS-IASI**: ~30-90 minutes (Europe/North Atlantic, via EUMETCast/BUFR)
- **BUFR on WMO GTS**: Temperature/humidity profiles distributed to NWP centers

**Update cadence**:
- Each Metop satellite: ~14 orbits/day
- IASI footprint: 12 km circular (at nadir)
- Global coverage: 2x daily per location

**File size**: 50-200 MB per orbit (NetCDF Level-2 products)

## Schema / Sample

**IASI Temperature Profile**:
```json
{
  "type": "eumetsat.iasi.temperature-profile",
  "source": "metopb/iasi",
  "id": "iasi_metopb_20240615_120834_lat42p5_lon012p3",
  "time": "2024-06-15T12:08:34Z",
  "subject": "atmos-profile/{lat_bucket}/{lon_bucket}",
  "data": {
    "satellite": "metopb",
    "orbit_number": 12345,
    "latitude": 42.52,
    "longitude": 12.34,
    "temperature_profile": [
      {"pressure_hpa": 1000, "temperature_k": 288.5},
      {"pressure_hpa": 850, "temperature_k": 278.3},
      {"pressure_hpa": 500, "temperature_k": 252.1}
      // ... 100+ levels
    ],
    "ozone_column_du": 312.5,
    "co_column_molec_cm2": 1.8e18,
    "so2_detected": false
  }
}
```

**Keying**: Lat/lon bucket (footprint locations vary with orbit)

## Why Strong (for specific use cases)

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Freshness** | 2 | 3-hour latency (global), 30-90 min (EARS) |
| **Openness** | 2 | Free registration, BUFR on GTS |
| **Stability** | 3 | Operational Metop mission since 2006 |
| **Structure** | 3 | NetCDF-4, HDF5, BUFR, documented |
| **Identifiers** | 1 | Footprint locations vary (no fixed stations) |
| **Additive value** | 0 | Vertical profiles (specialized, NWP-focused) |

## Limitations

1. **3-hour latency (global)**: Too slow for nowcasting. EARS-IASI is faster but regional (Europe) and requires EUMETCast/Data Store verification.

2. **Vertical profiles**: Each sounding has 100+ pressure levels. Large payload per event.

3. **Swath coverage**: 2x daily per location (not continuous).

4. **Specialized use**: Primary consumers are NWP centers. Limited direct public utility.

5. **Overlap with ROM SAF**: ROM SAF GPS-RO also provides temperature/humidity profiles (independent technique, higher vertical resolution in stratosphere).

## Verdict

**MARGINAL** (11/18) — IASI is scientifically valuable for NWP and volcanic ash detection, but **3-hour latency**, **vertical profile complexity**, and **specialized use** limit event-streaming utility.

**Exception**: **IASI SO2 for volcanic eruptions** — if a volcano erupts, IASI detects SO2 plumes within hours. This could be event-streamed as "volcanic plume detected" alerts. However, this is a **rare event** (few eruptions per year affect aviation).

**Better alternatives**:
- **AC SAF** for trace gases (already covered)
- **Surface weather obs** for temperature/humidity (already in repo)
- **Volcanic Ash Advisory Centers (VAAC)** for aviation ash alerts

**Status**: Low priority. Consider only if volcanic SO2 alerts are needed (but this is a rare, high-consequence event better served by VAAC bulletins).
