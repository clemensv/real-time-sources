# NASA AppEEARS (Application for Extracting and Exploring Analysis Ready Samples)

- **Country/Region**: Global
- **Endpoint**: `https://appeears.earthdatacloud.nasa.gov/api/`
- **Protocol**: REST (JSON), asynchronous job submission
- **Auth**: Earthdata Login (free registration)
- **Format**: JSON (API), GeoTIFF, NetCDF, CSV (output)
- **Freshness**: Varies by source product (3 hours to weeks, depending on upstream MODIS/VIIRS/SMAP/GPM latency)
- **Docs**: https://appeears.earthdatacloud.nasa.gov/api/, https://appeears.earthdatacloud.nasa.gov/help
- **Score**: 9/18

## Overview

NASA's Application for Extracting and Exploring Analysis Ready Samples (AppEEARS) is a data extraction and aggregation service that provides time-series and spatial subsets from NASA Earth observation products. AppEEARS acts as a unified API across 50+ NASA land, atmosphere, and cryosphere datasets (MODIS, VIIRS, SMAP, GPM, ASTER, Landsat, etc.), enabling users to request data for specific points, regions, or administrative boundaries without downloading entire global tiles.

AppEEARS is designed for applications that need *samples* rather than *full coverage*: agricultural monitoring (extract NDVI time series for farm parcels), drought analysis (extract SMAP soil moisture for river basins), water quality (extract Landsat reflectance for lake polygons). The service handles coordinate transformations, temporal aggregation, quality filtering, and format conversion.

The REST API accepts job requests (point samples, area samples, or raster subsets), queues them for processing, and delivers results via download URLs. Job completion time ranges from minutes (small point sets) to hours (large regional subsets). This is an *on-demand data extraction service*, not a real-time event stream.

## Endpoint Analysis

**API base:**
```
https://appeears.earthdatacloud.nasa.gov/api/
```

**List available products:**
```
GET https://appeears.earthdatacloud.nasa.gov/api/product
```

Returns JSON array of ~50 products, e.g., MOD13Q1 (MODIS NDVI), VNP09H1 (VIIRS surface reflectance), SPL3SMP_E (SMAP soil moisture), GPM_3IMERGDL (IMERG precipitation).

**Submit point sample request:**
```
POST https://appeears.earthdatacloud.nasa.gov/api/task
{
  "task_type": "point",
  "task_name": "Farm_NDVI_2024",
  "params": {
    "dates": [{"startDate": "01-01-2024", "endDate": "01-31-2024"}],
    "layers": [{"product": "MOD13Q1.061", "layer": "250m_16_days_NDVI"}],
    "coordinates": [
      {"latitude": 45.5, "longitude": -120.3, "id": "Field_A"},
      {"latitude": 45.6, "longitude": -120.4, "id": "Field_B"}
    ]
  }
}
```

**Response:**
```json
{
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "pending"
}
```

**Check job status:**
```
GET https://appeears.earthdatacloud.nasa.gov/api/status/a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

When status changes to `done`, download results:
```
GET https://appeears.earthdatacloud.nasa.gov/api/bundle/a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

Returns CSV time-series with columns: `Date`, `MOD13Q1_061_250m_16_days_NDVI_Field_A`, `MOD13Q1_061_250m_16_days_NDVI_Field_B`, QA flags, etc.

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Depends on upstream product latency (3 hours for MODIS/VIIRS NRT, days for SMAP, weeks for Landsat); AppEEARS itself is on-demand (job queue), not streaming |
| Openness | 2 | Free Earthdata Login required; API is well-documented |
| Stability | 3 | NASA operational service since 2018, stable API |
| Structure | 2 | REST JSON API for job control; output is CSV/GeoTIFF/NetCDF |
| Identifiers | 1 | User-defined IDs for points/areas; no built-in entity tracking |
| Richness | 0 | AppEEARS is a *data extraction tool*, not a data product; it reformats upstream products |

**AppEEARS excels for spatial/temporal aggregation of NASA products,** but it is not a real-time event stream. It's a *batch processing service*: you submit a request, wait for processing (minutes to hours), download results. This is incompatible with Kafka event-streaming architecture, which requires sub-minute to sub-hour event delivery.

**Why it's here:** AppEEARS provides a convenient API for extracting NASA Earth observation data for specific locations/regions, but the asynchronous job model and dependence on upstream product latency place it outside the NRT event-streaming scope.

## Limitations

- **Asynchronous job model.** You submit a request, poll for status, wait for completion (minutes to hours), then download. This is batch processing, not streaming.
- **Latency depends on upstream products.** If you request MODIS NRT fire data, AppEEARS will deliver it with ~3 hour lag (LANCE latency) + job queue time. If you request SMAP soil moisture, latency is 24–48 hours (SMAP NRT) + queue time. AppEEARS adds no value for *speed*; it adds value for *spatial aggregation* and *format conversion*.
- **No change detection or incremental updates.** Each job is a one-time extraction. You cannot subscribe to "notify me when NDVI changes by >0.1 at these farm parcels." You must submit new jobs periodically and diff results yourself.
- **Not an event source.** AppEEARS repackages data from other NASA products (MODIS, VIIRS, SMAP, GPM, Landsat). If you want those products as event streams, bridge the upstream sources (FIRMS for fire, IMERG for precip, SMAP for soil moisture), not AppEEARS.

**AppEEARS is a convenience layer for spatial/temporal aggregation, not a real-time data source.**

## Final Verdict

**Verdict**: ⏭️ **Reference**

AppEEARS is an excellent NASA service for extracting time-series and regional subsets from Earth observation products, but it does not fit the repo's event-streaming model. The asynchronous job queue, batch processing design, and dependence on upstream product latency make it unsuitable for real-time Kafka bridges.

**Use AppEEARS for:**
- One-off data extractions (research, analysis, visualization)
- Spatial aggregation (extract regional statistics rather than downloading global grids)
- Format conversion (get CSV time-series from HDF5 products)

**Do not use AppEEARS for:**
- Real-time event streaming (use upstream products like FIRMS, IMERG, SMAP instead)
- Sub-hourly data delivery (job queue latency is unpredictable)
- Continuous monitoring (job model is pull-based, not push-based)

**For NASA event streams, bridge upstream products:**
- **FIRMS** (active fire) — 3-hour NRT, CSV/JSON API
- **GPM IMERG** (precipitation) — 4-hour NRT, HDF5 files
- **SMAP** (soil moisture) — 24-hour NRT, HDF5 files
- **TEMPO** (air quality) — 2-hour NRT, NetCDF files

**Bridge type:** N/A (batch job service, not event stream)
