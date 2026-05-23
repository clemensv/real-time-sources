# EUMETSAT ROM SAF Radio Occultation Atmospheric Profiles

- **Country/Region**: Global (GPS-RO limb sounding)
- **Endpoint**: `https://rom-saf.eumetsat.int`, EUMETSAT Data Store
- **Protocol**: BUFR, NetCDF download, FTP
- **Auth**: Free registration
- **Format**: BUFR, NetCDF-4
- **Freshness**: Near-real-time (~90 minutes), operational
- **Docs**: https://rom-saf.eumetsat.int
- **Score**: 11/18

## Overview

The Radio Occultation Meteorology SAF (ROM SAF) processes GPS radio occultation (GPS-RO) data from Metop satellites to derive **vertical atmospheric profiles** of:
- Temperature
- Pressure
- Humidity (water vapor)
- Refractivity

**How GPS-RO works**: GPS signals passing through Earth's atmosphere are refracted. By measuring the refraction (bending angle), ROM SAF retrieves atmospheric structure from surface to 40 km altitude.

**Why GPS-RO matters**:
- **Numerical weather prediction**: High-quality vertical profiles for data assimilation
- **Climate monitoring**: Independent temperature record (no calibration drift)
- **Tropical cyclones**: Warm-core structure detection
- **Stratosphere**: Temperature trends, polar vortex monitoring

ROM SAF provides ~600-800 vertical profiles per day globally (from Metop-A/B/C).

## Endpoint Analysis

**ROM SAF Data Portal**: https://rom-saf.eumetsat.int/data_access.php

**Distribution**:
- BUFR on WMO GTS (operational NWP centers)
- NetCDF files via FTP (registration required)
- EUMETSAT Data Store (subset of products)

**Update cadence**:
- NRT mode: Profiles available ~90 minutes after observation
- Each Metop satellite provides ~200-300 profiles/day
- Spatial coverage: Global, but sparse (profiles separated by ~300-500 km along track)

**File format**: NetCDF-4 or BUFR (one file per profile)

## Schema / Sample

**Atmospheric Profile (NetCDF)**:
```json
{
  "type": "eumetsat.rom-saf.atmospheric-profile",
  "source": "rom-saf/metopb",
  "id": "romsaf_metopb_20240615_120834_lat42p5_lon012p3",
  "time": "2024-06-15T12:08:34Z",
  "subject": "atmos-profile/{lat_bucket}/{lon_bucket}",
  "data": {
    "satellite": "metopb",
    "occultation_id": "metopb_occ_12345",
    "latitude": 42.52,
    "longitude": 12.34,
    "profile": [
      {"altitude_km": 0.5, "temperature_k": 288.5, "pressure_hpa": 985.2, "humidity_pct": 68.0},
      {"altitude_km": 1.0, "temperature_k": 285.1, "pressure_hpa": 901.3, "humidity_pct": 55.0},
      {"altitude_km": 2.0, "temperature_k": 278.4, "pressure_hpa": 795.5, "humidity_pct": 42.0}
      // ... up to 40 km
    ],
    "quality_flag": "good"
  }
}
```

**Keying**: Lat/lon bucket (profiles are point soundings but locations vary)

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Freshness** | 2 | 90-minute latency |
| **Openness** | 2 | Free registration, BUFR on GTS |
| **Stability** | 3 | Operational ROM SAF, Metop mission |
| **Structure** | 3 | NetCDF-4, BUFR, documented |
| **Identifiers** | 1 | Profile locations vary (no fixed stations) |
| **Additive value** | 0 | Vertical profiles, not surface obs |

## Limitations

1. **Sparse coverage**: ~800 profiles/day globally = one profile per ~640,000 km² (size of France). Not dense enough for local applications.

2. **Vertical profiles**: Each event has 50-100 altitude levels. Large payload per event.

3. **90-minute latency**: Acceptable for NWP but not for nowcasting.

4. **No fixed locations**: Profile locations vary with satellite orbit. Cannot key by station ID.

5. **Specialized use**: Primary consumers are NWP centers (ECMWF, NOAA, DWD). Limited direct public utility.

## Verdict

**SKIP** (11/18) — ROM SAF profiles are scientifically valuable for NWP but **too sparse** and **specialized** for event streaming. Profiles are already distributed via BUFR on WMO GTS to operational met centers.

**Better alternative**: Surface weather observations (already in repo: DWD, NOAA) or radiosondes (if repo adds upper-air).
