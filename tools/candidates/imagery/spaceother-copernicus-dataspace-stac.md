# Copernicus Data Space Ecosystem STAC API

- **Country/Region**: Global (ESA Copernicus program)
- **Endpoint**: `https://catalogue.dataspace.copernicus.eu/stac/`
- **Protocol**: STAC 1.0.0 (SpatioTemporal Asset Catalog)
- **Auth**: Free registration for data access (STAC catalog open)
- **Format**: GeoTIFF, JPEG2000, NetCDF, SAFE (Sentinel native), HDF5
- **Freshness**: Hours to days (Sentinel-1 GRD ~3h, Sentinel-2 L1C ~1-2h, L2A ~3-6h, Sentinel-3 ~3h, Sentinel-5P ~3h)
- **Docs**: https://dataspace.copernicus.eu/, https://documentation.dataspace.copernicus.eu/
- **Score**: 17/18

## Overview

The Copernicus Data Space Ecosystem is the **new official ESA data distribution platform** (launched 2023, replacing SciHub/CREODIAS/Sobloo/Mundi). It provides **unified STAC-based access** to all Copernicus Sentinel missions (Sentinel-1/2/3/5P/6) plus Landsat Collection 2, Envisat, and derived products.

This is the **authoritative ESA source** for Sentinel data, with **faster NRT latency** than third-party STAC aggregators (Planetary Computer, Earth Search). Sentinel-2 L1C appears **1-2 hours** after acquisition, Sentinel-1 GRD **~3 hours**, and Sentinel-3 OLCI/SLSTR/SRAL **~3 hours**.

The STAC catalog is **fully open** (no auth for metadata queries), but **asset download requires free registration**. The platform replaces the legacy SciHub portal and provides **cloud-native access** (COG for optical, Zarr for some products, SAFE archives for full quality).

**Key collections**:
- **sentinel-2-l1c** — Top-of-atmosphere reflectance, 10-60m, ~1-2h latency
- **sentinel-2-l2a** — Atmospherically corrected surface reflectance, 10-60m, ~3-6h latency
- **sentinel-1-grd** — C-band SAR Ground Range Detected, 10m, ~3h latency
- **sentinel-3-olci** — Ocean color, 300m, ~3h latency
- **sentinel-3-slstr** — Sea/Land Surface Temperature, 500m-1km, ~3h latency
- **sentinel-3-sral** — Radar altimetry (sea level, wave height), along-track, ~3h latency
- **sentinel-5p-l2** — Atmospheric composition (NO2, CO, O3, CH4, aerosols), 7km, ~3h latency
- **sentinel-6-mf-l2** — Ocean altimetry (sea level, wave height), along-track, ~3h latency
- **landsat-c2-l2** — Landsat 8/9 Level-2 surface reflectance, 30m, ~12-24h latency

## Endpoint Analysis

**STAC API verified** — the root endpoint returns a STAC 1.0.0 catalog with 100+ collections.

Collections tested:
```
GET https://catalogue.dataspace.copernicus.eu/stac/collections
```

Returns extensive collection list including all Sentinel missions, Landsat, Envisat, and derived products (global mosaics, DEM, land cover, etc.).

**Example: Query recent Sentinel-2 L2A over the Mediterranean**
```bash
curl -X POST "https://catalogue.dataspace.copernicus.eu/stac/search" \
  -H "Content-Type: application/json" \
  -d '{
    "collections": ["sentinel-2-l2a"],
    "bbox": [10, 35, 20, 45],
    "datetime": "2024-01-01T00:00:00Z/..",
    "query": {
      "eo:cloud_cover": {"lt": 20}
    },
    "limit": 10
  }'
```

Returns STAC items with:
- `id`: Sentinel-2 product ID (e.g., `S2B_MSIL2A_20240115T092329_N0510_R093_T33SUB_20240115T112345`)
- `geometry`: Tile footprint (100×100km MGRS grid cell)
- `properties.datetime`: Acquisition timestamp
- `properties.eo:cloud_cover`: Cloud percentage
- `properties.s2:mgrs_tile`: MGRS tile ID (e.g., `33SUB`)
- `properties.s2:processing_baseline`: ESA processing version
- `assets`: Links to all bands (B01-B12, SCL, AOT, WVP, TCI), SAFE manifest, metadata

**Asset access**:
- **STAC catalog** — Open (no auth)
- **Asset download** — Requires **free registration** at https://dataspace.copernicus.eu/
- **OData API** — Alternative to STAC for searching (legacy SciHub compatibility)
- **S3 access** — Some products available via public S3 buckets (Sentinel-2 COG, experimental)

**Authentication**:
1. Register at https://dataspace.copernicus.eu/
2. Obtain OAuth2 token via `client_credentials` flow
3. Include token in asset download requests (`Authorization: Bearer <token>`)

**Example asset URL**:
```
https://zipper.dataspace.copernicus.eu/odata/v1/Products(12345678-1234-1234-1234-123456789012)/$value
```

**Data formats**:
- **SAFE** — ESA native format (directory structure with XML metadata + GeoTIFF/JPEG2000 bands)
- **COG** — Cloud-optimized GeoTIFF (experimental, Sentinel-2 only)
- **NetCDF** — Sentinel-3, Sentinel-5P
- **JPEG2000** — Sentinel-2 native bands (lossy compression)

## Schema/Sample

**STAC Item structure** (Sentinel-2 L2A example):
```json
{
  "type": "Feature",
  "stac_version": "1.0.0",
  "id": "S2B_MSIL2A_20240115T092329_N0510_R093_T33SUB_20240115T112345",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[10.5, 35.1], [11.6, 35.1], [11.6, 36.2], [10.5, 36.2], [10.5, 35.1]]]
  },
  "properties": {
    "datetime": "2024-01-15T09:23:29Z",
    "platform": "sentinel-2b",
    "constellation": "sentinel-2",
    "instruments": ["msi"],
    "eo:cloud_cover": 8.3,
    "s2:mgrs_tile": "33SUB",
    "s2:processing_baseline": "05.10",
    "s2:product_type": "S2MSI2A",
    "s2:datatake_id": "GS2B_20240115T092329_037123_N05.10",
    "proj:epsg": 32633,
    "view:sun_azimuth": 158.2,
    "view:sun_elevation": 28.5
  },
  "assets": {
    "B04": {
      "href": "https://zipper.dataspace.copernicus.eu/.../B04.jp2",
      "type": "image/jp2",
      "roles": ["data"],
      "gsd": 10,
      "eo:bands": [{"name": "B04", "common_name": "red", "center_wavelength": 0.665}]
    },
    "safe-manifest": {
      "href": "https://zipper.dataspace.copernicus.eu/.../manifest.safe",
      "type": "application/xml",
      "roles": ["metadata"]
    }
  }
}
```

**Stable identifiers**: Sentinel product IDs are globally unique and stable (e.g., `S2B_MSIL2A_20240115T092329_N0510_R093_T33SUB_20240115T112345`). Suitable for Kafka keys.

## Why Strong

1. **Official ESA source** — Authoritative for Sentinel data. Fastest NRT latency (1-2h for Sentinel-2 L1C, ~3h for Sentinel-1 GRD/Sentinel-3).
2. **Complete Sentinel coverage** — All missions (Sentinel-1/2/3/5P/6) in one STAC catalog. Single integration point.
3. **STAC 1.0.0 native** — Modern, standard-compliant API. Cloud-native tooling compatible (pystac-client, odc-stac).
4. **Free and open** — Registration is free. No usage limits or commercial restrictions.
5. **Cloud-native formats** — COG (experimental), Zarr, NetCDF. Optimized for partial reads and cloud processing.
6. **Global coverage** — All Sentinel data, all orbits, all regions. No geographic restrictions.

## Limitations

- **Registration required for downloads** — STAC catalog is open, but asset access requires OAuth2 token (free account).
- **COG availability unclear** — Sentinel-2 COG assets are experimental and may not be complete. SAFE archives are authoritative.
- **SAFE format overhead** — Native SAFE archives are directory structures (zip files), not single-file COGs. Requires unpacking.
- **No push notifications** — STAC is pull-only. Bridge must poll `/search` for new products.
- **OAuth2 token management** — Access tokens expire (typically 10 minutes). Bridge must refresh tokens automatically.

## Integration Notes

**Recommended bridge pattern**: **Multi-collection STAC poller with OAuth2**

1. **Authentication** — Bridge obtains OAuth2 token via `client_credentials` flow (`COPERNICUS_CLIENT_ID`, `COPERNICUS_CLIENT_SECRET`).
2. **Token refresh** — Automatically refresh token before expiry (use `refresh_token` grant).
3. **STAC polling** — Every 15-30 minutes, query `/search` for each collection with `datetime=lastPoll/..`.
4. **Delta detection** — Track `item.id` in SQLite or Kafka compacted topic. Emit only new products.
5. **Message groups** — One per collection family:
   - `sentinel2_l2a_tiles` — keyed by `{tile}/{date}` (e.g., `33SUB/2024-01-15`)
   - `sentinel1_grd_scenes` — keyed by `{mode}/{orbit}/{date}` (e.g., `IW/12345/2024-01-15`)
   - `sentinel3_olci_granules` — keyed by `{orbit}/{date}` (e.g., `12345/2024-01-15`)
6. **Reference data** — Emit Sentinel mission metadata (orbit parameters, sensor specs, coverage) at startup.

**Why use Copernicus Data Space instead of Element84 Earth Search?**
- **Faster NRT** — Copernicus is the ground segment. Data appears 1-2h faster than third-party aggregators.
- **Complete collections** — All Sentinel missions (including Sentinel-3, Sentinel-5P, Sentinel-6). Earth Search only has Sentinel-1/2.
- **Official source** — ESA-operated. Guaranteed availability and uptime.

**Why use Earth Search/Planetary Computer instead of Copernicus Data Space?**
- **No auth** — Earth Search has public S3 buckets (no token management). Simpler deployment.
- **COG-native** — Earth Search COG assets are production-ready. Copernicus COG is experimental.
- **Multi-vendor** — Planetary Computer includes Landsat, GOES, MODIS/VIIRS (not just Sentinel).

**Recommended strategy**: Use **Copernicus Data Space for Sentinel-3/5P/6** (not available on Earth Search) and **Earth Search for Sentinel-1/2** (simpler auth). Or use **Copernicus Data Space for all Sentinel missions** if NRT latency (1-2h) is critical.

## Verdict

**STRONG ACCEPT** — This is the **official ESA STAC endpoint** with **fastest NRT latency** for Sentinel data (1-2h for Sentinel-2 L1C, ~3h for Sentinel-1 GRD). The **STAC 1.0.0 interface** is excellent, and **free registration** is a minor barrier (OAuth2 token management is standard).

Recommended as the **primary source for Sentinel-3/5P/6** (atmospheric composition, ocean color, altimetry) which are **not available on Earth Search or Planetary Computer**. For **Sentinel-1/2**, this is the **fastest NRT option** (1-2h faster than cloud aggregators).

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3 | All Sentinel missions (1/2/3/5P/6) + Landsat in one STAC catalog |
| Freshness | 3 | Sentinel-2 L1C ~1-2h, Sentinel-1 GRD ~3h, Sentinel-3 ~3h (fastest NRT) |
| Openness | 3 | Free registration, no commercial restrictions, OAuth2 token required |
| Schema clarity | 3 | STAC 1.0.0, eo/projection/SAR/atmospheric extensions |
| Machine-readability | 3 | JSON, GeoJSON, COG (experimental), SAFE, NetCDF |
| Repo fit | 2 | OAuth2 token management required, but excellent NRT latency |
