# EUMETSAT LSA SAF Fire Radiative Power (FRP)

- **Country/Region**: Europe, Africa, Middle East (MSG disk), Global (Metop swaths)
- **Endpoint**: FTP: `landsaf.ipma.pt/products`, WMS: `landsaf.ipma.pt/geoserver`
- **Protocol**: FTP (HDF5, NetCDF), WMS, REST (in development)
- **Auth**: Free registration for FTP, WMS open
- **Format**: HDF5, NetCDF-4, BUFR (WMO GTS distribution)
- **Freshness**: 15 minutes (MSG FRP-GRID), 3 hours (Metop swaths), daily (FRP accumulation)
- **Docs**: https://landsaf.ipma.pt/en/products/active-fire/
- **Score**: 15/18

## Overview

The Land Surface Analysis SAF (LSA SAF), operated by Portugal's IPMA, detects active fires and quantifies Fire Radiative Power (FRP) — the rate of thermal energy release from wildfires. LSA SAF products:

| Product | Description | Cadence | Resolution | Coverage |
|---------|-------------|---------|------------|----------|
| **FRP-PIXEL** | Individual fire pixels | 15 min | 3 km | MSG disk |
| **FRP-GRID** | Gridded FRP (0.05° cells) | 15 min | ~5 km | MSG disk |
| **FRP** (Metop) | Polar-orbiter FRP | ~100 min | 1 km | Global swaths |

**Why FRP matters**:
- **Fire emissions**: FRP correlates with smoke particulate (PM2.5) and CO2 release
- **Early wildfire detection**: Fires detected within minutes of ignition
- **Burn area estimation**: Cumulative FRP → total energy release → burned area
- **Air quality forecasting**: FRP feeds CAMS smoke plume models
- **Agricultural burning**: Track crop residue fires (illegal in many EU countries)

**FRP vs. traditional fire detection**:
- **Binary fire masks** (e.g., MODIS active fire) detect fire presence/absence
- **FRP** quantifies fire intensity — a small grassfire (10 MW) vs. a crown fire (10,000 MW)

LSA SAF FRP is a **key input to CAMS** (Copernicus Atmosphere Monitoring Service) for forecasting smoke transport. It's also used by EU civil protection (EFFIS — European Forest Fire Information System).

## Endpoint Analysis

**FTP Distribution**: `ftp://landsaf.ipma.pt/products/FRP/`

Directory structure:
```
/FRP-PIXEL/MSG/YYYY/MM/DD/
  HDF5_LSASAF_MSG_FRP-PIXEL-ListProduct_MSG-Disk_YYYYMMDDHHMM.h5
  
/FRP-GRID/MSG/YYYY/MM/DD/
  HDF5_LSASAF_MSG_FRP-GRID_MSG-Disk_YYYYMMDDHHMM.h5
```

**File naming**:
```
HDF5_LSASAF_MSG_FRP-PIXEL-ListProduct_MSG-Disk_202406151200.h5
```
- Observation time: 12:00 UTC on June 15, 2024
- `FRP-PIXEL-ListProduct`: List of fire detections (not gridded)

**Update cadence**:
- New files every 15 minutes (MSG SEVIRI repeat cycle)
- Latency: ~20 minutes from observation
- File size: 50 KB - 5 MB (depends on fire activity; small in winter, large in summer)

**WMS Service** (visualization):
```
https://landsaf.ipma.pt/geoserver/lsa/wms?
  service=WMS&
  request=GetMap&
  layers=lsa:FRP-PIXEL&
  time=2024-06-15T12:00:00Z
```

**BUFR on WMO GTS**: FRP detections distributed to national met services via Global Telecommunication System (BUFR messages). Lower latency (~10 min) but requires GTS access.

## Schema / Sample

**FRP-PIXEL HDF5** structure:
```
/FRP/
  /Line (dimension: n_fires)
  /Column
  /Latitude
  /Longitude
  /FRP (units: MW)
  /FRP_Uncertainty (MW)
  /Fire_Class (nominal, probable, possible)
  /Observation_Time (seconds since 2000-01-01)
```

**Decoded to JSON** (CloudEvents bridge):
```json
{
  "type": "eumetsat.lsa-saf.fire.detection",
  "source": "lsa-saf/frp-pixel/msg-seviri",
  "id": "frp_20240615_120000_n42p5_w008p2",
  "time": "2024-06-15T12:00:00Z",
  "subject": "fire/{lat_0.1deg}/{lon_0.1deg}",
  "data": {
    "latitude": 42.487,
    "longitude": -8.234,
    "frp_mw": 345.7,
    "frp_uncertainty_mw": 42.1,
    "fire_class": "nominal",
    "pixel_area_sqkm": 12.3,
    "brightness_temp_k": 367.5,
    "satellite": "MSG-4",
    "observation_time": "2024-06-15T11:58:23Z"
  }
}
```

**Key design**: `fire/{lat_0.1deg}/{lon_0.1deg}` (round to 0.1° for grouping nearby pixels)

**Event model**:
- One event per fire pixel detection
- Subject = geographic bucket (allows tracking fire growth within cell)
- FRP value enables time-series analysis (fire intensifying vs. decaying)

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Freshness** | 3 | 15-minute updates (MSG), 3-hourly (Metop) |
| **Openness** | 3 | Free registration, open WMS, BUFR on GTS |
| **Stability** | 3 | Operational LSA SAF since 2005, IPMA + EUMETSAT |
| **Structure** | 3 | HDF5/NetCDF, BUFR, documented schema |
| **Identifiers** | 2 | Pixel lat/lon (not persistent station IDs) |
| **Additive value** | 1 | Repo has no wildfire; high-value domain |

**Strengths**:
- **15-minute cadence**: Fast enough for early wildfire detection
- **Quantitative**: FRP (MW) is more informative than binary fire/no-fire
- **Operational critical**: Feeds EU civil protection (EFFIS) and CAMS smoke forecasts
- **Point detections**: Fire pixels are natural event entities (vs. gridded products)
- **Long time series**: LSA SAF FRP operational since 2005 (Meteosat-8)

**Real-world use**:
- **2017 Portugal fires**: LSA SAF detected Pedrógão Grande fire within 10 minutes of ignition; FRP peaked at 15,000 MW (crown fire)
- **2019 Amazon fires**: Global FRP product detected surge in August (later confirmed by MODIS/VIIRS)
- **2023 Greece wildfires**: LSA SAF FRP used for smoke forecast (Athens air quality warnings)

## Limitations

1. **Cloud obscuration**: Infrared sensors cannot see through clouds. Fires under thick smoke or storm clouds may be missed. Polar-orbiting VIIRS/MODIS provide backup during cloudy MSG scenes.

2. **Nighttime sensitivity**: SEVIRI mid-IR channel (3.9 µm) is less sensitive at night than VIIRS (smaller fires missed).

3. **Pixel size**: MSG at 3 km resolution misses small fires (<0.5 hectare). VIIRS at 375 m has better small-fire detection.

4. **Geographic scope**: MSG disk covers Europe/Africa/Middle East. Americas/Asia require different satellites (GOES-R/Himawari).

5. **FRP uncertainty**: FRP estimate has ~20-40% uncertainty (depends on fire temperature, atmospheric correction, viewing angle).

6. **Temporal continuity**: 15-minute sampling means rapidly evolving fires may show large FRP jumps between observations (vs. continuous geostationary monitoring of a single fire).

7. **No fire progression tracking**: Each pixel detection is independent. To track a fire's growth over time, consumer must spatially cluster pixels and maintain fire object state (polygon growth).

## Verdict

**STRONG CANDIDATE** (15/18) — LSA SAF FRP is one of the best EUMETSAT NRT products for this repo:

- **True event stream**: Each fire detection is a natural event entity
- **High freshness**: 15 minutes
- **Quantitative payload**: FRP (MW) enables intensity-based alerting
- **Operational importance**: Critical for EU wildfire response and smoke forecasting
- **Clean schema**: HDF5 list of detections, easy to parse

**Implementation path**:
1. **FTP polling**: Check `/products/FRP/FRP-PIXEL/MSG/` for new HDF5 files every 5 minutes
2. **Parse HDF5**: Use `h5py` to extract fire pixel list
3. **Emit events**: One CloudEvent per fire pixel
4. **Key design**: `fire/{lat_0.1deg}/{lon_0.1deg}` (allows aggregation by 0.1° cell)
5. **Quality filter**: Emit only "nominal" and "probable" fire classes (skip "possible" to reduce false alarms)

**Volume estimate**:
- Summer (peak fire season): ~500-2,000 fire pixels per 15-min observation over MSG disk
  - 96 observations/day × 1,000 avg pixels = 96,000 events/day
- Winter (low fire season): ~50-200 pixels per observation
  - 96 × 100 = 9,600 events/day
- **Annual average**: ~30,000 events/day

**Pair with**:
- **CAMS smoke forecasts** (Copernicus Atmosphere) for downwind air quality
- **Sentinel-2 burn scar** (post-fire burned area mapping)
- **Weather stations** (wind speed/direction for fire spread modeling)

**Next steps**:
1. Register for LSA SAF FTP access
2. Download sample FRP-PIXEL HDF5 file
3. Prototype `h5py` parsing
4. Test event emission for major fire event (e.g., Greece summer 2023)

**Status**: **Top recommendation** for EUMETSAT. Clean event model, high operational value, fills gap in repo.
