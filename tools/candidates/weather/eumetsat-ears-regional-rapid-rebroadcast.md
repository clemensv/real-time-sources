# EUMETSAT EARS (EUMETSAT Advanced Retransmission Service)

- **Country/Region**: Regional (Europe, North Atlantic, Arctic, Africa)
- **Endpoint**: EUMETCast, EUMETSAT Data Store (limited)
- **Protocol**: EUMETCast broadcast, file download (NetCDF, BUFR)
- **Auth**: Free registration (Data Store), EUMETCast requires hardware
- **Format**: NetCDF-4, BUFR, GRIB2
- **Freshness**: Near-real-time (~30-90 minutes from observation)
- **Docs**: https://www.eumetsat.int/ears
- **Score**: 12/18

## Overview

EUMETSAT Advanced Retransmission Service (EARS) provides **rapid regional rebroadcast** of polar-orbiter data for Europe/North Atlantic. EARS reduces latency by processing data at **regional HRPT stations** (High Rate Picture Transmission ground receivers) instead of waiting for global data dumps.

**EARS products**:
- **EARS-AVHRR**: Metop/NOAA AVHRR imagery (visible, thermal IR)
- **EARS-ATOVS**: AMSU-A, MHS sounding (temperature, humidity profiles)
- **EARS-ASCAT**: Ocean surface winds (same as OSI SAF, but lower latency)
- **EARS-IASI**: Hyperspectral IR sounder (temperature, trace gas profiles)
- **EARS-VIIRS**: NOAA-20/21 visible/IR imagery
- **EARS-NUCaps**: NOAA hyperspectral profiles

**Why EARS matters**:
- **Latency reduction**: 30-60 minutes vs. 3-6 hours for global products
- **Regional focus**: Europe/Arctic coverage (where EUMETSAT NMS need fast data)
- **Nowcasting**: ASCAT winds, AVHRR cloud, IASI temperature profiles for rapid-update NWP

## Endpoint Analysis

**Primary distribution**: EUMETCast (DVB-S broadcast). **Not suitable for HTTP bridge**.

**EUMETSAT Data Store**: Some EARS products available via Data Store, but catalog is unclear. Verification needed.

**BUFR on GTS**: EARS-ASCAT winds and ATOVS soundings distributed via WMO GTS.

**Update cadence**:
- EARS-ASCAT: New swaths every ~100 minutes (orbital period)
- EARS-AVHRR: Continuous (every pass over European HRPT stations)
- Latency: 30-90 minutes from observation

## Schema / Sample

EARS products are **same data** as global products, but with **lower latency and regional scope**. For example:

**EARS-ASCAT** = OSI SAF ASCAT winds (already covered), but ~30-60 minutes faster for Europe/North Atlantic.

**Event model**: Same as corresponding global products (ASCAT winds, AVHRR imagery, IASI profiles).

## Why Strong (if accessible)

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Freshness** | 2 | 30-90 minute latency (vs. 3-6 hours global) |
| **Openness** | 1 | EUMETCast primary (Data Store unclear) |
| **Stability** | 3 | Operational EUMETSAT service |
| **Structure** | 3 | NetCDF-4, BUFR, GRIB2 |
| **Identifiers** | 2 | Swath geometry (varies by product) |
| **Additive value** | 1 | Lower latency vs. global, but regional only |

## Limitations

1. **EUMETCast dependency**: Primary channel is broadcast (requires DVB-S ground station). HTTP access unclear.

2. **Regional scope**: Europe/North Atlantic only. Global coverage requires waiting for standard products.

3. **Overlap with global products**: EARS-ASCAT = OSI SAF ASCAT (same data, faster delivery). If OSI SAF ASCAT is bridged, EARS adds only latency improvement, not new phenomena.

4. **Data Store availability**: Unclear which EARS products are available via Data Store API. May require contacting EUMETSAT.

## Verdict

**SKIP** (12/18) — EARS **reduces latency** for existing products (ASCAT, AVHRR, IASI) but does not add new phenomena. If **OSI SAF ASCAT winds** are bridged (already covered as strong candidate), EARS-ASCAT provides the same data ~60 minutes faster.

**Recommendation**: 
- If latency is critical, investigate EARS-ASCAT via Data Store or BUFR/GTS
- Otherwise, stick with global OSI SAF products (clearer access path)

**Status**: Conditional — only pursue if Data Store access is confirmed and latency improvement is essential.
