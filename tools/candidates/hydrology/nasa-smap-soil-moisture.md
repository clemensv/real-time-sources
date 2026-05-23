# NASA SMAP (Soil Moisture Active Passive) NRT

- **Country/Region**: Global (land areas, 60°N–60°S for radar, global for radiometer)
- **Endpoint**: `https://n5eil01u.ecs.nsidc.org/SMAP/` (NSIDC DAAC)
- **Protocol**: HTTPS file download (HDF5, NetCDF, GeoTIFF)
- **Auth**: Earthdata Login (free registration)
- **Format**: HDF5, NetCDF-4, GeoTIFF
- **Freshness**: 24–48 hours from satellite overpass
- **Docs**: https://nsidc.org/data/smap, https://smap.jpl.nasa.gov/data/
- **Score**: 12/18

## Overview

NASA's Soil Moisture Active Passive (SMAP) mission measures soil moisture and freeze/thaw state from a polar-orbiting satellite using L-band microwave radiometry. Launched in 2015, SMAP provides global coverage every 2–3 days at 9km, 36km resolution (radiometer-only; the radar failed in 2015). Soil moisture is critical for drought monitoring, flood forecasting, agricultural yield prediction, and climate modeling.

SMAP Level 3 products provide gridded soil moisture estimates in units of volumetric water content (m³/m³) for the top 5 cm of soil. Near real-time (NRT) products are delivered within 24–48 hours of observation and use preliminary ancillary data; science-quality (Standard) products arrive weeks later with final calibration.

The mission is operated by NASA JPL; data is archived at the National Snow and Ice Data Center (NSIDC) Distributed Active Archive Center (DAAC).

## Endpoint Analysis

**NSIDC DAAC FTP/HTTPS directory:**
```
https://n5eil01u.ecs.nsidc.org/SMAP/SPL3SMP_E.006/
```

Data files follow orbit-date naming:
```
SMAP_L3_SM_P_E_20240115_R18290_001.h5
         ^   ^   ^       ^      ^
       L3  SM Enh  date   orbit  version
```

**Product variants:**
- `SPL3SMP_E` — Enhanced L3 Radiometer Soil Moisture, Passive, 9km EASE-Grid 2.0, daily composites
- `SPL3SMP` — L3 Radiometer Soil Moisture, Passive, 36km, daily
- `SPL3FTP` — L3 Freeze/Thaw, Passive, 36km, daily

**Sample HDF5 structure (SPL3SMP_E):**
- `Soil_Moisture_Retrieval_Data_AM/soil_moisture` — morning overpass, grid of volumetric soil moisture (0.0–1.0 m³/m³)
- `Soil_Moisture_Retrieval_Data_PM/soil_moisture` — evening overpass
- `Soil_Moisture_Retrieval_Data_AM/retrieval_qual_flag` — quality flag (0=good, >0=suspect/failed)
- Latitude/longitude grids embedded in HDF5

**Earthdata Login required:**
```bash
curl -n -c cookies.txt -b cookies.txt \
  "https://n5eil01u.ecs.nsidc.org/SMAP/SPL3SMP_E.006/2024.01.15/SMAP_L3_SM_P_E_20240115_R18290_001.h5"
```

**Grid:**
- EASE-Grid 2.0 projection (Equal-Area Scalable Earth Grid)
- 9km resolution: 1624×3856 global grid (Enhanced product)
- 36km resolution: 406×964 global grid (Standard product)

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 24–48 hour latency — daily to sub-daily but not real-time |
| Openness | 2 | Free Earthdata Login required, instant registration |
| Stability | 3 | NASA JPL operational mission since 2015 |
| Structure | 2 | HDF5 with documented grid structure, but not JSON/REST |
| Identifiers | 2 | Grid cells (EASE-Grid row/col) are stable; daily composites are the temporal unit |
| Richness | 1 | Soil moisture (single variable) + quality flags; limited context |

**SMAP is the only global satellite soil moisture mission with sub-50km resolution.** The 9km Enhanced product is unique in Earth observation. Soil moisture is a key variable for drought early warning (e.g., U.S. Drought Monitor, FAO GIEWS), agricultural modeling (crop stress, irrigation scheduling), and flood forecasting (antecedent soil saturation controls runoff).

**Complements existing hydrology bridges:** SMAP provides *antecedent condition* (how wet was the soil before the rain?); GPM IMERG provides *precipitation input*; USGS/European gauge networks provide *streamflow output*. Combining all three enables rainfall-runoff modeling.

**Grid-based daily composite structure.** Each file is a global snapshot for one day (AM and PM overpasses averaged or separate grids). A bridge could emit CloudEvents per grid cell, per region of interest (drought-watch zones, river basins), or as aggregated statistics (e.g., "mean soil moisture for California Central Valley on 2024-01-15").

## Limitations

- **24–48 hour latency** — too slow for flash flood warnings, but acceptable for drought monitoring and seasonal agricultural forecasts.
- **Earthdata Login required.** Free but adds auth complexity (same as GPM IMERG).
- **File-based delivery (HDF5).** Each daily composite is a ~200 MB file. Bridge must poll directory, download, parse HDF5, extract grid cells. Heavier infrastructure than JSON REST.
- **Coverage gaps.** Soil moisture retrievals fail over dense vegetation, frozen ground, standing water, and wet snow. Quality flags identify failed/suspect pixels. A significant fraction of each daily grid is missing or low-quality.
- **Single variable.** SMAP measures soil moisture (and freeze/thaw state in a separate product), not soil temperature, evapotranspiration, or vegetation health (those require other satellites or models).
- **Volume.** 9km global grid = ~6 million cells. Emitting all cells daily as Kafka events is impractical; must filter to regions of interest or aggregate.
- **Revisit time: 2–3 days** at any given location (polar orbit). Not continuous coverage. Some locations may have no observations for days due to orbit gaps or quality failures.

**Key tradeoff:** SMAP is scientifically valuable for drought/agriculture applications but has the same file-based HDF5 delivery and grid-volume challenges as GPM IMERG. Best suited for region-specific bridges (e.g., "Sahel soil moisture monitor" or "US Corn Belt drought tracker").

## Final Verdict

**Verdict**: ⚠️ **Maybe**

SMAP is NASA's flagship soil moisture product and the only global satellite mission with this capability. The data is operationally used by USDA, NOAA, FEWS NET, and drought monitoring agencies worldwide. However, the 24–48 hour latency, file-based HDF5 delivery, and grid-cell volume make it a heavier bridge than point-sensor APIs.

If the repo prioritizes **drought and agriculture** domains, SMAP is a strong candidate — especially for specific regions (Sub-Saharan Africa, South Asia, US Great Plains). If the repo focuses on sub-hourly hydrology (flash floods, urban runoff), SMAP is lower priority.

**Recommended if pursued:**
- Regional bridge (drought-watch zones, major agricultural regions)
- Keying by grid cell (EASE-Grid row/col or lat/lon at 9km)
- Poll daily for new NRT composites
- Emit only high-quality cells (retrieval_qual_flag == 0) OR aggregate to regional statistics

**Bridge type:** Poller (HTTPS file listing + HDF5 download/parse, daily interval)

**Keying:** Grid cell (EASE-Grid row/col or lat/lon)

**Reference data:** EASE-Grid metadata (row/col to lat/lon mapping) — static, embedded in HDF5 or available from NSIDC docs

**Pairs well with:** GPM IMERG (precipitation), USGS-IV / European hydro gauges (streamflow)
