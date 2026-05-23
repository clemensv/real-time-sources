# NASA MODAPS / LANCE NRT Data (MODIS & VIIRS Land Products)

- **Country/Region**: Global
- **Endpoint**: `https://nrt3.modaps.eosdis.nasa.gov/api/v2/` (REST), `https://nrt3.modaps.eosdis.nasa.gov/archive/allData/` (file archive)
- **Protocol**: REST (JSON), HTTPS file download (HDF5, GeoTIFF)
- **Auth**: None (REST API), Earthdata Login for file download
- **Format**: JSON (REST metadata), HDF5/GeoTIFF (data files)
- **Freshness**: 3 hours from satellite overpass
- **Docs**: https://lance.modaps.eosdis.nasa.gov/, https://nrt3.modaps.eosdis.nasa.gov/api/v2/docs
- **Score**: 12/18

## Overview

The MODIS Adaptive Processing System (MODAPS), part of NASA's Land, Atmosphere Near real-time Capability for EOS (LANCE), provides near real-time (NRT) data from MODIS (Terra/Aqua) and VIIRS (Suomi-NPP, NOAA-20, NOAA-21) instruments. Products are delivered within 3 hours of satellite overpass and include active fire, snow cover, land surface temperature, vegetation indices, and atmospheric corrections.

MODAPS/LANCE is the production system behind FIRMS (active fire), NASA Worldview imagery layers, and operational early-warning systems for wildfires, floods, drought, and agricultural monitoring. The REST API provides metadata (product availability, file listings, granule info), while actual data files (HDF5, GeoTIFF) are downloaded via HTTPS.

Products span Level 0 (raw satellite data) to Level 3 (gridded daily/8-day composites). NRT products use best-available ancillary data and preliminary calibration; Standard Processing (weeks to months later) uses final cal/val.

## Endpoint Analysis

**REST API base:**
```
https://nrt3.modaps.eosdis.nasa.gov/api/v2/
```

**List available products:**
```
GET https://nrt3.modaps.eosdis.nasa.gov/api/v2/products
```

Returns JSON array of ~50 NRT products, e.g.:
```json
[
  {
    "product": "MOD14",
    "platform": "Terra",
    "instrument": "MODIS",
    "level": "2",
    "description": "Thermal Anomalies/Fire"
  },
  {
    "product": "VNP14IMGTDL",
    "platform": "SNPP",
    "instrument": "VIIRS",
    "level": "2",
    "description": "Thermal Anomalies/Fire I-Band 375 m"
  }
]
```

**List files for a product/date:**
```
GET https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/details?products=MOD14&archiveSets=61&temporalRanges=2024-01-15
```

Returns JSON with file URLs, sizes, checksums.

**Download data file (Earthdata Login required):**
```
GET https://nrt3.modaps.eosdis.nasa.gov/archive/allData/61/MOD14/2024/015/MOD14.A2024015.0305.061.NRT.hdf
```

**Sample NRT products:**
- `MOD14` / `MYD14` — MODIS active fire (Terra/Aqua), Level 2 swath, 1 km
- `VNP14IMGTDL` / `VJ114IMGTDL` — VIIRS active fire I-band (Suomi-NPP/NOAA-20), 375 m
- `MOD10_L2` / `MYD10_L2` — MODIS snow cover, Level 2 swath, 500 m
- `VNP43` — VIIRS surface reflectance daily, 500 m / 1 km
- `MOD13A1` — MODIS vegetation indices (NDVI/EVI), 16-day composite, 500 m

**HDF5 structure (MOD14 example):**
- `fire mask` — pixel classification: 0=non-fire, 7/8/9=fire (nominal/high/very high confidence)
- `FP_latitude`, `FP_longitude` — fire pixel centroids
- `FP_T21`, `FP_power` — brightness temp (K), fire radiative power (MW)
- `Scan start time` — granule timestamp

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 3-hour NRT latency, global daily coverage from polar orbiters |
| Openness | 2 | REST API no-auth; file download needs Earthdata Login (free) |
| Stability | 3 | NASA operational system since 2002 (MODIS), 2012 (VIIRS) |
| Structure | 2 | REST API JSON metadata is clean; data files are HDF5 (binary) |
| Identifiers | 1 | Swath pixels have lat/lon but no persistent IDs; fire pixels from MOD14 are the same data as FIRMS |
| Richness | 1 | MODAPS is the data *source*, not a value-added product; FIRMS (fire), IMERG (precip), TEMPO (air quality) *use* MODAPS data and add processing |

**MODAPS is the upstream infrastructure for many NASA NRT products.** The REST API is useful for *discovering* what's available and *when*, but the actual scientific value comes from products built *on top of* MODAPS:
- **Fire pixels** → FIRMS provides the same MOD14/VNP14 data with a cleaner API
- **Snow cover** → NSIDC provides MODIS/VIIRS snow products with better domain context
- **Vegetation indices** → NASA AppEEARS or Land Processes DAAC provide NDVI/EVI time series with spatial aggregation
- **Imagery layers** → NASA GIBS/Worldview renders MODAPS products as map tiles

**MODAPS itself is a data *distribution* system,** not a value-added event stream. If you want active fire data, use FIRMS (which wraps MOD14). If you want snow cover, use NSIDC MODIS snow products. MODAPS is where you go when the downstream product doesn't exist yet or you need raw swath data for custom processing.

## Limitations

- **Swath data has variable geometry.** MOD14 fire pixels are in satellite-native swath coordinates (scan/track), not a fixed grid. Each granule covers a different ground track. This makes stable keying difficult unless you reproject to a fixed grid.
- **HDF5 files require parsing.** Unlike FIRMS CSV/JSON, you must download ~50 MB HDF5 files and extract pixels programmatically.
- **Earthdata Login for data downloads.** REST API is no-auth, but grabbing the actual granules needs auth.
- **Overlap with existing NASA products.** MOD14 = FIRMS fire data, MOD10 = NSIDC snow, etc. Unless you need raw swath data for custom algorithms, the downstream products are easier to work with.
- **No value-added processing.** MODAPS delivers L0–L3 products from the MODIS/VIIRS processing chain, but it doesn't aggregate, filter, or contextualize. Compare to EONET (which curates events) or FIRMS (which formats fire pixels for easy consumption).

**MODAPS is not a *bridge* target; it's the *source* other NASA products bridge.** The repo should bridge FIRMS, EONET, TEMPO, SMAP, etc., not raw MODAPS granules.

## Final Verdict

**Verdict**: ⏭️ **Reference**

MODAPS/LANCE is critical NASA infrastructure that powers many NRT products, but it is not itself a good target for event bridging. The REST API is useful for metadata queries ("when did the latest VIIRS fire granule arrive?"), but the actual data products are better accessed via domain-specific wrappers (FIRMS for fire, NSIDC for snow, GIBS for imagery).

**Use MODAPS when:**
- You need raw MODIS/VIIRS swath data for custom processing not available in downstream products
- You're building a new NRT product on top of MODIS/VIIRS and need granule-level delivery notifications
- You want metadata about data availability/latency for monitoring LANCE system performance

**Do not use MODAPS when:**
- A downstream NASA product exists (FIRMS, EONET, SMAP, TEMPO, etc.) that provides the same data with a cleaner API
- You need stable entity IDs or gridded data (swath geometry is variable)
- You want JSON/REST instead of HDF5 file download/parse

**Bridge type:** N/A (use downstream products like FIRMS instead)

**Related NASA products to bridge instead:**
- **FIRMS** (active fire from MOD14/VNP14) — already in repo, scored 15/18
- **EONET** (natural events including MODIS-detected fires/floods/snow) — already in repo, scored 16/18
- **NSIDC MODIS/VIIRS snow products** — candidate for snow-avalanche domain
