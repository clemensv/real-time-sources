# EUMETSAT Sentinel-3 Marine Products (OLCI/SLSTR)

- **Country/Region**: Global (polar orbit coverage)
- **Endpoint**: EUMETSAT Data Store, Copernicus Marine Service
- **Protocol**: REST API, FTP, OData
- **Auth**: Free registration (EUMETSAT / Copernicus)
- **Format**: NetCDF-4, SAFE archive
- **Freshness**: Near-real-time (~3 hours), daily composites
- **Docs**: https://www.eumetsat.int/sentinel-3
- **Score**: 11/18

## Overview

EUMETSAT operates the **marine data distribution** for Sentinel-3 (Copernicus satellite) on behalf of ESA. Sentinel-3 carries two marine-focused instruments:

- **OLCI** (Ocean and Land Colour Instrument): 21-band spectrometer for ocean color, chlorophyll-a, water quality
- **SLSTR** (Sea and Land Surface Temperature Radiometer): SST, LST, fire detection

**Marine NRT products**:
- **OLCI Level-2 OC**: Ocean color, chlorophyll-a concentration
- **SLSTR Level-2 SST**: Sea surface temperature (swath)
- **Synergy L2**: Combined OLCI+SLSTR surface reflectance

**Why marine products matter**:
- **Harmful algal blooms (HABs)**: Chlorophyll-a hotspots indicate blooms (toxic for shellfish)
- **Fisheries**: Phytoplankton (ocean color) drives food chain (fish aggregation)
- **Water quality**: Turbidity, suspended sediment in coastal waters
- **Coral bleaching**: SST anomalies trigger bleaching events

## Endpoint Analysis

**EUMETSAT Data Store**:
```
GET https://api.eumetsat.int/data/browse/collections?q=Sentinel-3
```

**Copernicus Marine Service** (alternative):
```
https://data.marine.copernicus.eu/products
```

**Update cadence**:
- NRT products: ~3 hours from observation
- Each Sentinel-3 satellite (A, B, C) provides daily global coverage
- Swath width: 1,270 km (OLCI), 1,400 km (SLSTR)

**File size**: 50-200 MB per granule (NetCDF SAFE archive)

## Schema / Sample

**OLCI Ocean Color (chlorophyll-a)**:
```json
{
  "type": "eumetsat.sentinel3.olci.ocean-color",
  "source": "sentinel-3a/olci",
  "id": "s3a_olci_20240615_120000_lat42p5_lon012p3",
  "time": "2024-06-15T12:00:00Z",
  "subject": "ocean-color/{lat_bucket}/{lon_bucket}",
  "data": {
    "satellite": "sentinel-3a",
    "latitude": 42.52,
    "longitude": 12.34,
    "chl_a_mg_m3": 1.85,
    "turbidity_fnu": 2.1,
    "suspended_matter_g_m3": 0.45,
    "quality_flags": ["water", "good_quality"],
    "observation_time": "2024-06-15T11:58:23Z"
  }
}
```

**Keying**: Lat/lon bucket (swath geometry, no persistent stations)

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Freshness** | 2 | 3-hour latency for NRT |
| **Openness** | 3 | Free, Copernicus open data policy |
| **Stability** | 3 | Operational Copernicus mission |
| **Structure** | 3 | NetCDF-4, SAFE format, documented |
| **Identifiers** | 0 | Swath geometry (no natural entity IDs) |
| **Additive value** | 0 | Overlap with other ocean color sources |

## Limitations

1. **3-hour latency**: Not real-time (harmful algal blooms develop over hours-days)
2. **Swath geometry**: Polar orbit, not continuous coverage
3. **Cloud obscuration**: Optical sensors cannot see through clouds (frequent gaps)
4. **Gridded vs. point**: Swath pixels, not station observations
5. **Overlap**: NASA produces similar ocean color (MODIS Aqua, VIIRS) with comparable latency

## Verdict

**MARGINAL** (11/18) — Good stability and openness, but **3-hour latency** and **swath geometry** limit event-streaming utility. Daily ocean color composites may be more useful than NRT swaths.

**Status**: Low priority. Focus on OSI SAF SST (hourly) or other higher-frequency products.
