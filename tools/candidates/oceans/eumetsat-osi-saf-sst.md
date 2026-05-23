# EUMETSAT OSI SAF Sea Surface Temperature (SST)

- **Country/Region**: Global oceans
- **Endpoint**: FTP: `ftp.osi-saf.org/prod/sst/`, EUMETSAT Data Store
- **Protocol**: FTP, REST API (Data Store), NetCDF/GRIB download
- **Auth**: FTP anonymous, Data Store requires free EUMETSAT registration
- **Format**: NetCDF-4, GRIB2
- **Freshness**: Hourly (gridded L3 composites), 6-hourly (foundation SST)
- **Docs**: https://osi-saf.eumetsat.int/products/osi-203-b
- **Score**: 13/18

## Overview

OSI SAF produces multi-sensor sea surface temperature (SST) products by blending observations from:
- **Infrared radiometers**: SLSTR (Sentinel-3), AVHRR (Metop, NOAA)
- **Microwave radiometers**: AMSR-2 (GCOM-W)

Key products:
- **OSI-203-b**: Global hourly SST (0.05° resolution, L3 composite)
- **OSI-204**: Global foundation SST (daily, 0.05°, optimal interpolation)
- **OSI-205**: SST anomaly (deviation from climatology)

SST is critical for:
- **Weather forecasting**: Ocean-atmosphere heat exchange drives hurricane intensification
- **Fisheries**: SST fronts (sharp gradients) attract fish aggregations
- **Climate monitoring**: Ocean heat content, El Niño/La Niña tracking
- **Coral bleaching**: Sustained high SST (>30°C) triggers mass bleaching events

## Endpoint Analysis

**FTP Distribution**:
```
ftp://ftp.osi-saf.org/prod/sst/
  /l3/
    /msg/
    /metop/
    /multi-sensor/
```

**File pattern** (multi-sensor hourly):
```
20240615-OSISAF-L3C_GHRSST-SSTsubskin-MULTI-REP-v02.0-fv01.0.nc
```

**Update cadence**:
- Hourly composites: New file every hour (~20 minutes after hour)
- Daily foundation SST: Once per day (~06:00 UTC for previous day)
- File size: ~100-200 MB (NetCDF), ~50 MB (GRIB)

**Grid specifications**:
- Resolution: 0.05° × 0.05° (global)
- Coverage: 90°S to 90°N, ice-free oceans
- Format: GHRSST Data Specification v2.0 (international SST standard)

## Schema / Sample

**NetCDF GHRSST Level-3 Collated (L3C)**:
```
dimensions:
    lat = 3600
    lon = 7200
    time = 1

variables:
    float sea_surface_temperature(time, lat, lon)
        units: "kelvin"
        valid_min: 270.0
        valid_max: 320.0
        long_name: "sea surface subskin temperature"
        
    float sst_dtime(time, lat, lon)
        units: "hours"
        comment: "time difference from product time to observation time"
        
    byte quality_level(time, lat, lon)
        flag_meanings: "no_data bad low acceptable excellent"
        flag_values: 0, 1, 2, 3, 5
        
    float sses_bias(time, lat, lon)
        long_name: "SSES bias estimate"
        units: "kelvin"
        comment: "Estimated SST bias"
        
    float sses_standard_deviation(time, lat, lon)
        long_name: "SSES standard deviation"
        units: "kelvin"
```

**Event model** (CloudEvents bridge):
```json
{
  "type": "eumetsat.osi-saf.sst.grid-cell",
  "source": "osi-saf/sst/multi-sensor",
  "id": "sst_20240615_12_n35p5_e012p5",
  "time": "2024-06-15T12:00:00Z",
  "subject": "sst/{lat_bucket}/{lon_bucket}",
  "data": {
    "latitude": 35.525,
    "longitude": 12.475,
    "sst_kelvin": 293.5,
    "sst_celsius": 20.35,
    "quality_level": "excellent",
    "sst_uncertainty_k": 0.3,
    "observation_time": "2024-06-15T11:47:00Z",
    "sensor_blend": ["slstr-3a", "slstr-3b", "avhrr-metopb"]
  }
}
```

**Keying challenge**: 
- Global grid = 3,600 × 7,200 = 25.9M cells
- Emitting all cells every hour = 620M events/day
- **Solution**: Emit only ocean cells with valid SST (~40% of grid = 10M cells) → 240M events/day
- **Better solution**: Emit 1° × 1° aggregates (360 × 180 = 64,800 cells) with mean/std SST → 1.5M events/day

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Freshness** | 2 | Hourly composites (~20-min latency) |
| **Openness** | 3 | Anonymous FTP, free registration, CC-BY-4.0 |
| **Stability** | 3 | Operational, GHRSST standard, EUMETSAT SAF |
| **Structure** | 3 | NetCDF-4, GHRSST spec, CF conventions |
| **Identifiers** | 1 | Gridded (must create lat/lon bucket keys) |
| **Additive value** | 1 | Repo has no SST; complements NOAA water temp |

**Strengths**:
- **Hourly updates**: Faster than daily climatology products
- **Multi-sensor fusion**: More complete coverage than single-satellite products
- **GHRSST standard**: Interoperability with other SST products (NOAA, NASA, JMA)
- **Global coverage**: All ice-free oceans
- **Climate record**: Continuous since 2008 (Metop-A)

**Use cases**:
- **Coral bleaching alerts**: Detect SST >30°C for 4+ weeks (Great Barrier Reef, Caribbean)
- **Hurricane rapid intensification**: SST >26.5°C required for tropical cyclones
- **El Niño monitoring**: Track equatorial Pacific SST anomalies
- **Fisheries**: Tuna favor SST fronts (sharp gradients between water masses)

## Limitations

1. **Gridded format**: 25.9M cells globally. Must aggregate or filter to avoid overwhelming event volume.

2. **Hourly cadence**: Better than daily, but still coarse compared to sub-minute streaming feeds (AIS, weather obs).

3. **Cloud gaps**: Infrared sensors cannot see through clouds. Hourly composite may have missing data in cloudy regions. Microwave sensors fill gaps but have lower resolution.

4. **No natural entity IDs**: SST is a field, not a set of stations. Must create artificial grid-cell keys.

5. **Overlap with NOAA**: NOAA produces similar global SST (GHRSST L4 Multi-scale Ultra-high Resolution). OSI SAF adds European provenance and SLSTR data (Sentinel-3).

6. **File size**: 100-200 MB per hourly file = 2.4-4.8 GB/day. Not prohibitive, but larger than point-observation feeds.

## Verdict

**PROMISING** (13/18) — Hourly global SST is valuable, but the gridded format and high cell count require careful event design. **Recommended approach**:

1. **Aggregate to 1° × 1° grid**: 64,800 cells × 24 hours = 1.5M events/day (manageable)
2. **Emit mean, min, max, stddev per cell**: Preserve statistical distribution
3. **Filter ocean-only**: Skip land cells (reduces to ~40k ocean cells)
4. **Include quality metadata**: Flag cells with poor coverage or high uncertainty

**Alternative**: Emit only **SST anomaly hotspots** (cells >2 standard deviations from climatology) — reduces volume to ~5,000 events/day, focuses on extreme events (marine heatwaves, cold pools).

**Next steps**:
1. Prototype FTP polling for hourly NetCDF files
2. Parse with `xarray` (handles GHRSST NetCDF natively)
3. Implement 1° aggregation or anomaly filtering
4. Test with Kafka producer (validate volume and latency)

**Status**: Good candidate if event granularity is solved. Pairs well with **OSI SAF winds** for comprehensive ocean surface monitoring.
