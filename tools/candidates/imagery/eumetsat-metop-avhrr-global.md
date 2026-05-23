# EUMETSAT Metop AVHRR Global Imagery

- **Country/Region**: Global (polar orbit coverage)
- **Endpoint**: EUMETSAT Data Store, EARS-AVHRR (regional), EUMETCast
- **Protocol**: File download (NetCDF, HDF5), EUMETCast broadcast
- **Auth**: Free EUMETSAT registration
- **Format**: NetCDF-4, HDF5, AAPP native
- **Freshness**: Near-real-time (~3 hours global, ~30-90 min EARS regional)
- **Docs**: https://www.eumetsat.int/avhrr
- **Score**: 9/18

## Overview

The Advanced Very High Resolution Radiometer (AVHRR) on Metop-A/B/C provides moderate-resolution imagery in 6 channels (visible, near-IR, thermal IR). AVHRR has been flying since 1978 (NOAA satellites), making it the **longest continuous Earth observation record**.

**Channels**:
- VIS/NIR: 0.6 µm, 0.8 µm (reflected sunlight)
- SWIR: 1.6 µm, 3.7 µm (daytime cloud discrimination, nighttime fire)
- TIR: 10.8 µm, 12.0 µm (temperature, cloud top)

**Applications**:
- **Sea surface temperature (SST)**: Global ocean monitoring
- **Vegetation monitoring**: NDVI for agriculture
- **Cloud detection**: Day/night cloud masks
- **Fire detection**: 3.7 µm channel detects hot spots
- **Snow/ice mapping**: Polar monitoring

## Why Weak for Event Streaming

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Freshness** | 1 | 3-hour latency (global), 30-90 min (EARS) |
| **Openness** | 2 | Free registration |
| **Stability** | 3 | Operational since 1978 (NOAA), Metop since 2006 |
| **Structure** | 2 | Imagery (NetCDF/HDF5), not tabular |
| **Identifiers** | 0 | No entities (pixels, not events) |
| **Additive value** | 1 | Imagery is input; derived products are events |

## Verdict

**SKIP** (9/18) — Same issue as SEVIRI/FCI: **raw imagery is not event-based**. Derived products from AVHRR are already covered:

- **OSI SAF**: Uses AVHRR for SST, sea ice, ocean color
- **LSA SAF**: Uses AVHRR (polar) for LST, fire detection
- **NWC SAF**: Uses AVHRR for cloud nowcasting (PPS software)

AVHRR is the **input to SAF products**, not an event stream itself.

**Exception**: If "fire hot spot detected" alerts from AVHRR are needed (separate from LSA SAF FRP), this could work. But LSA SAF FRP (SEVIRI-based, 15-min) is already covered and provides higher temporal resolution for Europe/Africa.

**Recommendation**: Skip raw AVHRR. Stick with SAF-derived products.
