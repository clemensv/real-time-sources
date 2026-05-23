# JAXA GCOM-C SGLI Ocean Color & Land Surface

- **Country/Region**: Japan / Global (polar-orbiting)
- **Endpoint**: https://gportal.jaxa.jp (G-Portal, registration required)
- **Protocol**: SFTP download, CSW catalog
- **Auth**: Free registration required
- **Format**: HDF5, NetCDF
- **Freshness**: Near-real-time (within 3 hours for NRT products)
- **Docs**: https://gportal.jaxa.jp
- **Score**: 9/18

## Overview

GCOM-C (Global Change Observation Mission - Climate), also known as "Shikisai", launched in 2017, carries the Second-generation Global Imager (SGLI) — a 19-channel multi-spectral radiometer covering visible, near-infrared, shortwave infrared, and thermal infrared. SGLI provides ocean color (chlorophyll-a, suspended sediment), land surface temperature, snow cover, and vegetation indices at 250 m to 1 km resolution.

**Key strength**: SGLI is one of the most advanced polar-orbiting ocean color sensors, with more spectral channels than MODIS or VIIRS. It provides high-quality chlorophyll-a, vegetation indices (NDVI, EVI), and land surface temperature (LST).

Like GCOM-W/AMSR2, GCOM-C products are distributed through JAXA's G-Portal (same registration and SFTP access model).

## Endpoint Analysis

**G-Portal** — same infrastructure as GCOM-W/AMSR2 (covered in separate candidate file). Registration, SFTP, and CSW catalog access are identical.

**SFTP structure** (example):
```
gportal.jaxa.jp/data/GCOM-C/SGLI/
  L2/
    NWLR/  # Normalized Water-Leaving Radiance (ocean color input)
    CHLA/  # Chlorophyll-a concentration
    SST/   # Sea Surface Temperature
    LST/   # Land Surface Temperature
    NDVI/  # Normalized Difference Vegetation Index
  L3/
    CHLA_D/  # Daily chlorophyll-a grid
    LST_D/   # Daily land surface temperature
```

**Products of interest (NRT availability)**:
- **L2 Ocean Color** — Chlorophyll-a, TSS (total suspended solids), CDOM (colored dissolved organic matter), Kd (diffuse attenuation coefficient)
- **L2 Land** — Land Surface Temperature (day/night), NDVI, snow cover, vegetation continuous field
- **L3 daily grids** — 0.05° or 0.25° global grids, one file per day per product

**Freshness**: NRT products within 3 hours of observation (same as GCOM-W). GCOM-C is polar-orbiting with ~1-2 day revisit at mid-latitudes, daily at high latitudes.

**Volume estimate**: ~14 orbits per day. With multiple products (CHLA, LST, NDVI), L2 volume is ~100-200 files/day. L3 daily grids are 5-10 files/day. **Manageable**.

## Schema / Sample Metadata

HDF5 with CF-compliant metadata. Example L2 chlorophyll-a:

```json
{
  "satellite": "GCOM-C",
  "sensor": "SGLI",
  "processing_level": "L2",
  "product_name": "CHLA",
  "observation_start": "2026-01-15T02:30:00Z",
  "observation_end": "2026-01-15T04:00:00Z",
  "orbit_number": 12345,
  "swath_width_km": 1150,
  "resolution_m": 250,
  "variables": ["chlorophyll_a", "quality_flag", "solar_zenith_angle"],
  "units": "chlorophyll_a: mg/m³",
  "format": "HDF5"
}
```

**Stable identifier**: `{orbit}/{product}` — same as GCOM-W.

**CloudEvents subject template**: `gcom-c/sgli/l2/{product}/{orbit}`  
**Kafka key template**: `gcom-c-{product}-{orbit}`

## Why This is Valuable

1. **Advanced ocean color**: 19-channel SGLI provides better spectral resolution than MODIS/VIIRS for coastal and Case-2 waters (turbid, sediment-laden)
2. **Vegetation monitoring**: NDVI and LST at 250 m resolution complement MODIS/VIIRS
3. **Complements GCOM-W**: GCOM-C (optical/thermal) and GCOM-W (microwave) together provide comprehensive Earth observation
4. **Operational since 2017**: Mature mission with stable data products
5. **Climate research**: GCOM-C is part of JAXA's long-term climate monitoring program

## Limitations

1. **Registration required**: Same as GCOM-W (free but email verification, 1-2 day approval)
2. **SFTP/HDF5**: Same transport and format challenges as GCOM-W
3. **Polar-orbiting gaps**: 1-2 day revisit (not continuous like geostationary)
4. **Cloud cover**: Ocean color requires clear skies; LST is also cloud-limited
5. **L2 swath complexity**: Swath geometry is more complex than gridded L3

## Verdict

**✅ Recommend (with caveats)** — GCOM-C/SGLI is a strong ocean color and land surface candidate. Same infrastructure as GCOM-W, so if GCOM-W registration is successful, GCOM-C is accessible via the same credentials.

**Best scope**: **L3 daily grids for Chlorophyll-a and Land Surface Temperature**. Two files per day, globally gridded, easier to ingest than L2 swaths.

**Bridge pattern**: Same SFTP polling as GCOM-W. Poll `/data/GCOM-C/SGLI/L3/CHLA_D/{YYYY}/{MM}/` daily, detect new files, download, extract HDF5 metadata, emit CloudEvent.

**Pair with GCOM-W**: If building a GCOM-W/AMSR2 bridge (ocean SST, sea ice), adding GCOM-C/SGLI (ocean chlorophyll, land LST) uses the same infrastructure. **Dual-mission bridge** could cover ocean + land + atmosphere.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3 | Advanced ocean color, vegetation, LST — complements MODIS/VIIRS |
| Freshness | 2 | NRT within 3 hours, but polar-orbiting (1-2 day revisit per location) |
| Openness | 2 | Free registration required (same as GCOM-W) |
| Schema Clarity | 2 | HDF5/CF-compliant, documented, but binary |
| Machine-Readability | 2 | SFTP + CSW catalog, HDF5 parseable |
| Repo-Fit | -2 | Same infrastructure as GCOM-W, but polar-orbit cadence and HDF5 format are friction |

**Score: 9/18** — Solid candidate if paired with GCOM-W. Recommend L3 daily chlorophyll-a + LST.
