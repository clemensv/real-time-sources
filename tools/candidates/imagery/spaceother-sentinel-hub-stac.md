# Sentinel Hub STAC API (Commercial Free Tier)

- **Country/Region**: Global (Sinergise / Planet Labs)
- **Endpoint**: `https://services.sentinel-hub.com/api/v1/catalog/1.0.0/`
- **Protocol**: STAC 1.0.0
- **Auth**: OAuth2 (free tier: 30,000 processing units/month)
- **Format**: GeoTIFF (on-demand rendering), JPEG, PNG
- **Freshness**: Hours (Sentinel-2 L1C ~2-4h, L2A ~6-12h, Sentinel-1 GRD ~6-12h)
- **Docs**: https://docs.sentinel-hub.com/, https://www.sentinel-hub.com/
- **Score**: 11/18

## Overview

Sentinel Hub is a **commercial EO cloud platform** by Sinergise (acquired by Planet Labs 2023) offering **on-demand satellite imagery processing** via API. It provides a **STAC 1.0.0 catalog** for Sentinel-1/2, Landsat-8/9, MODIS, and commercial data (Planet, Airbus, Maxar).

The platform's strength is **on-demand rendering** — instead of downloading full scenes, users request pixel-perfect subsets (bbox + bands + resolution + time range) and receive **pre-processed GeoTIFF/PNG** output. This is ideal for web applications, dashboards, and analytics pipelines that need **small AOIs** rather than full scenes.

**Free tier**: 30,000 processing units per month (sufficient for ~3,000 km² at 10m resolution, or 100 full Sentinel-2 tiles). **Paid tiers** scale to enterprise volumes.

**Key collections (free tier)**:
- **sentinel-2-l1c** — Top-of-atmosphere reflectance, 10-60m
- **sentinel-2-l2a** — Atmospherically corrected, 10-60m
- **sentinel-1-grd** — C-band SAR, 10m
- **landsat-8-l1** / **landsat-9-l1** — Landsat Level-1 (not L2), 30m
- **modis** — MODIS Level-1B, 250-1000m

**Paid-tier collections**:
- **planet** — Planet SkySat, PlanetScope (3-5m)
- **airbus** — Pleiades, SPOT (1.5-6m)
- **maxar** — WorldView, GeoEye (0.3-0.5m)

## Endpoint Analysis

**STAC API verified** — `https://services.sentinel-hub.com/api/v1/catalog/1.0.0/` returns STAC 1.0.0 catalog.

Collections tested:
```
GET https://services.sentinel-hub.com/api/v1/catalog/1.0.0/collections
```

Returns:
- `sentinel-2-l1c`
- `sentinel-2-l2a`
- `sentinel-1-grd`
- `landsat-8-l1`
- `landsat-9-l1`
- `modis`

**Example: Query recent Sentinel-2 L2A over Spain**
```bash
curl -X POST "https://services.sentinel-hub.com/api/v1/catalog/1.0.0/search" \
  -H "Authorization: Bearer <SENTINEL_HUB_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "collections": ["sentinel-2-l2a"],
    "bbox": [-4, 40, -3, 41],
    "datetime": "2024-01-01T00:00:00Z/..",
    "limit": 10
  }'
```

Returns STAC items similar to Copernicus Data Space structure (Sentinel-2 product IDs, MGRS tiles, cloud cover, etc.).

**Authentication**:
1. Create account at https://www.sentinel-hub.com/ (free tier)
2. Create OAuth2 client in Configurator
3. Obtain access token via `client_credentials` flow
4. Include token in API requests (`Authorization: Bearer <token>`)

**On-demand rendering** (Process API, not STAC):
```bash
curl -X POST "https://services.sentinel-hub.com/api/v1/process" \
  -H "Authorization: Bearer <SENTINEL_HUB_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "bounds": {"bbox": [-4.5, 40.5, -4.4, 40.6]},
      "data": [{"type": "sentinel-2-l2a", "dataFilter": {"timeRange": {"from": "2024-01-01T00:00:00Z", "to": "2024-01-15T23:59:59Z"}}}]
    },
    "output": {
      "width": 512,
      "height": 512,
      "responses": [{"identifier": "default", "format": {"type": "image/tiff"}}]
    },
    "evalscript": "//VERSION=3\nfunction setup() { return { input: [\"B04\", \"B03\", \"B02\"], output: { bands: 3 } }; }\nfunction evaluatePixel(sample) { return [sample.B04, sample.B03, sample.B02]; }"
  }'
```

Returns GeoTIFF with RGB composite (Red, Green, Blue bands) clipped to bbox.

**Stable identifiers**: Same as Copernicus Data Space (Sentinel product IDs).

## Why Strong

1. **On-demand rendering** — No need to download full scenes. Request exact bbox + bands + resolution. Saves bandwidth and storage.
2. **Multi-source STAC** — Sentinel-1/2, Landsat, MODIS in one API. Paid tier adds Planet, Airbus, Maxar.
3. **Cloud-native tooling** — Excellent Python SDK (`sentinelhub-py`), QGIS plugin, OGC WMTS/WMS/WCS endpoints.
4. **Free tier** — 30,000 processing units/month is sufficient for research, prototyping, and small-scale monitoring.
5. **Evalscript flexibility** — Custom band math, cloud masking, NDVI, time-series composites via JavaScript-like scripting.

## Limitations

- **Commercial service** — Free tier is capped (30,000 PU/month). Enterprise use requires paid subscription.
- **On-demand overhead** — Process API adds latency (~5-15s per request). Not suitable for bulk downloads.
- **Not a data archive** — Sentinel Hub queries upstream sources (Copernicus Data Space, AWS Open Data). Adds dependency.
- **Processing units** — Complex to estimate. Full Sentinel-2 tile at 10m resolution costs ~300 PU. Small AOIs are cheap, full tiles are expensive.
- **Free tier Landsat is L1** — Only Level-1 (top-of-atmosphere). L2 (surface reflectance) requires paid tier or custom processing.
- **STAC vs. Process API** — STAC catalog is read-only (metadata only). Actual data access requires Process API (separate workflow).

## Integration Notes

**Recommended bridge pattern**: **AOI-based on-demand fetcher** (not polling)

1. **Authentication** — Bridge obtains OAuth2 token (`SENTINEL_HUB_CLIENT_ID`, `SENTINEL_HUB_CLIENT_SECRET`).
2. **Event-driven** — Downstream consumers request imagery for specific AOIs (e.g., wildfire perimeter, flood extent, agricultural field).
3. **Process API invocation** — Bridge calls Process API with bbox, time range, bands, evalscript.
4. **Caching** — Bridge caches rendered outputs in S3 or blob storage. Subsequent requests for same AOI+time return cached result.
5. **Message groups** — Not applicable (this is a **pull** service, not a **push** feed).

**Why not use Sentinel Hub for the repo?** The repo focuses on **push-based real-time feeds** (continuous monitoring, data streams). Sentinel Hub is **pull-based on-demand rendering** (request-response). Different use case.

**When to use Sentinel Hub**:
- **Web applications** — Dashboards, map viewers, mobile apps that need **dynamic imagery tiles** (WMTS).
- **Small AOIs** — Agricultural field monitoring, urban expansion tracking (100-1000 km²).
- **Custom processing** — NDVI time series, cloud-free composites, change detection via evalscripts.

**When NOT to use Sentinel Hub**:
- **Bulk downloads** — Full-scene archives are cheaper from Copernicus Data Space or Earth Search.
- **Continuous monitoring** — Real-time feeds should poll STAC catalogs (Copernicus, Earth Search), not render on-demand.
- **High-volume processing** — Free tier is capped. Enterprise pricing may be prohibitive.

## Verdict

**WEAK ACCEPT (niche utility)** — Sentinel Hub is an **excellent on-demand rendering platform** for web applications and small-AOI monitoring, but it's **not a real-time feed**. The STAC catalog is a **metadata index** (same data as Copernicus Data Space), not a unique data source.

**Recommended ONLY IF**:
- The repo wants to add an **on-demand imagery service** (not a continuous feed)
- Users need **web-friendly tile rendering** (WMTS, WMS) for dashboards
- Small-AOI monitoring (agricultural fields, urban areas) is a priority

**Skip IF**:
- The repo focuses on **continuous real-time feeds** (polling STAC is better served by Copernicus Data Space or Earth Search)
- Bulk scene downloads are the primary use case (free tier is too limited)
- Users want **fully open** data (Sentinel Hub is commercial with free tier caps)

Alternative: For **on-demand Sentinel imagery**, use **Copernicus Data Space** (free, no caps) or **Earth Search** (public S3 buckets, no rendering service but direct COG access).

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 2 | On-demand rendering + multi-source STAC (Sentinel-1/2, Landsat, MODIS) |
| Freshness | 2 | Sentinel-2 L1C ~2-4h, L2A ~6-12h (slower than Copernicus Data Space) |
| Openness | 1 | Free tier capped (30,000 PU/month), commercial service |
| Schema clarity | 3 | STAC 1.0.0, well-documented Process API |
| Machine-readability | 2 | GeoTIFF, JPEG, PNG (on-demand only, not bulk download) |
| Repo fit | 1 | On-demand rendering (pull), not continuous feed (push) |
