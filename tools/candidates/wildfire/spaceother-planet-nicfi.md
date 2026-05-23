# Planet NICFI Tropical Forest Monitoring Program

- **Country/Region**: Global tropics (lat ±30°)
- **Endpoint**: `https://api.planet.com/basemaps/v1/mosaics` (requires NICFI agreement)
- **Protocol**: Planet Basemaps API (RESTful JSON)
- **Auth**: API key (free via NICFI program for eligible users)
- **Format**: GeoTIFF (COG), quad tiles
- **Freshness**: Monthly mosaics (published ~2-4 weeks after month-end)
- **Docs**: https://www.planet.com/nicfi/, https://developers.planet.com/docs/basemaps/
- **Score**: 12/18

## Overview

The Norway's International Climate & Forests Initiative (NICFI) program provides **free access** to Planet's high-resolution (4.77m) tropical forest satellite imagery via monthly mosaics. Coverage spans **±30° latitude** (all tropical and subtropical forests globally) from December 2015 to present. Mosaics are derived from Planet's SkySat (0.5m panchromatic sharpened to 0.5m color) and Dove (PlanetScope) constellation (3m multispectral).

The program is designed for **forest monitoring, carbon accounting, and land-use change detection**. Eligible users include governments, NGOs, researchers, and indigenous communities working on forest conservation, REDD+, sustainable development, or humanitarian response. Commercial use is **prohibited** unless licensed separately.

**Key features**:
- **4.77m resolution** — 10× higher than Sentinel-2, 6× higher than Landsat
- **Monthly cadence** — Cloud-free composites published every month
- **Tropics-only** — ±30° latitude band (Amazon, Congo Basin, Southeast Asia, Central America)
- **Free for qualified users** — Must sign NICFI data access agreement
- **Analysis-ready** — Atmospherically corrected surface reflectance mosaics

## Endpoint Analysis

**Planet Basemaps API verified** — the `/mosaics` endpoint requires authentication via API key.

Tested (with auth):
```
GET https://api.planet.com/basemaps/v1/mosaics
Authorization: api-key <NICFI_API_KEY>
```

Returns list of available mosaics:
```json
{
  "mosaics": [
    {
      "id": "planet_medres_normalized_analytic_2024-01_mosaic",
      "name": "2024-01 Mosaic",
      "datatype": "uint16",
      "grid": {
        "quad_size": 4096,
        "resolution": 4.77
      },
      "first_acquired": "2024-01-01",
      "last_acquired": "2024-01-31",
      "_links": {
        "tiles": "https://api.planet.com/basemaps/v1/mosaics/.../tiles",
        "quads": "https://api.planet.com/basemaps/v1/mosaics/.../quads"
      }
    }
  ]
}
```

**Mosaic structure**:
- **Monthly composites** — One mosaic per month (e.g., `2024-01_mosaic`, `2024-02_mosaic`)
- **Quad-based tiling** — Data is delivered as 4096×4096 pixel quads (tiles) in Web Mercator or UTM projection
- **Bands**: Blue, Green, Red, NIR (4-band multispectral)
- **Format**: GeoTIFF (COG-compatible)

**Example: Fetch quad list for a mosaic**
```
GET https://api.planet.com/basemaps/v1/mosaics/planet_medres_normalized_analytic_2024-01_mosaic/quads?bbox=-70,-10,-60,0
Authorization: api-key <NICFI_API_KEY>
```

Returns quads (tiles) intersecting the bbox, with download URLs for each quad.

**Authentication**:
1. **Sign up** for NICFI program at https://www.planet.com/nicfi/
2. **Verify eligibility** — Provide organization info, use case description
3. **Receive API key** — Valid for 1 year, renewable
4. **Rate limits** — 10 requests/second, 1000 quads/day (generous for research)

**Access restrictions**:
- **Tropics-only** — Coverage is limited to ±30° latitude
- **No commercial use** — NICFI license prohibits commercial applications (e.g., selling imagery, embedding in paid products)
- **Attribution required** — Must credit "Planet & NICFI"
- **Eligibility verification** — Planet reviews applications (typically approved within 2-3 business days)

## Schema/Sample

**Mosaic metadata**:
```json
{
  "id": "planet_medres_normalized_analytic_2024-01_mosaic",
  "name": "2024-01 Mosaic",
  "datatype": "uint16",
  "grid": {
    "quad_size": 4096,
    "resolution": 4.77
  },
  "first_acquired": "2024-01-01T00:00:00Z",
  "last_acquired": "2024-01-31T23:59:59Z",
  "interval": "1 month",
  "bbox_degrees": [-180, -30, 180, 30],
  "_links": {
    "self": "https://api.planet.com/basemaps/v1/mosaics/...",
    "tiles": "https://api.planet.com/basemaps/v1/mosaics/.../tiles/{z}/{x}/{y}.png",
    "quads": "https://api.planet.com/basemaps/v1/mosaics/.../quads"
  }
}
```

**Quad structure** (individual tile):
```json
{
  "id": "L15-1234E-5678N",
  "bbox": [-70.5, -5.1, -70.4, -5.0],
  "percent_covered": 100,
  "_links": {
    "download": "https://api.planet.com/basemaps/v1/.../L15-1234E-5678N.tif?api_key=..."
  }
}
```

**Stable identifiers**:
- Mosaic ID: `planet_medres_normalized_analytic_{YYYY-MM}_mosaic`
- Quad ID: Grid-based (e.g., `L15-1234E-5678N`)

Both are stable and suitable for Kafka keys.

## Why Strong

1. **Unique resolution** — 4.77m is **10× better than Sentinel-2** (10m) and **6× better than Landsat** (30m). Critical for detecting small-scale forest clearing, road building, and selective logging.
2. **Tropics-wide coverage** — Unified dataset for Amazon, Congo Basin, SE Asia, Central America. No need to stitch together regional sources.
3. **Monthly cadence** — More frequent than annual land cover products, sufficient for operational deforestation monitoring.
4. **Free for forest conservation** — The NICFI license is explicitly designed for REDD+, carbon accounting, and forest protection use cases.
5. **Analysis-ready** — Surface reflectance mosaics are cloud-free, gap-filled, and normalized. No preprocessing required.

## Limitations

- **Monthly latency** — Mosaics are published 2-4 weeks after month-end. Not suitable for real-time fire alerts or disaster response (use MODIS/VIIRS for that).
- **Eligibility required** — Not universally open. Applicants must justify their use case and agree to non-commercial terms.
- **Tropics-only** — No data outside ±30° latitude. Not useful for temperate/boreal forests or polar regions.
- **No L1 data** — Only composites (mosaics). Individual scene timestamps and per-pixel acquisition dates are lost.
- **Sunset risk** — NICFI funding is time-limited (currently committed through 2025). Program may not continue indefinitely.
- **No STAC** — Planet Basemaps API is proprietary. Not compatible with standard STAC tooling (pystac-client, odc-stac).
- **Commercial restrictions** — Cannot be used in paid products, commercial services, or revenue-generating applications without a separate license.

## Integration Notes

**Recommended bridge pattern**: **Monthly mosaic poller**

1. **API key config** — Bridge requires `PLANET_API_KEY` (from NICFI enrollment).
2. **Mosaic enumeration** — At startup, fetch `/mosaics` to discover available monthly composites.
3. **Polling loop** — Every day, check for new mosaics (detect when `last_acquired` month increments).
4. **Quad fetching** — For each new mosaic, query `/quads?bbox=...` for target AOIs (e.g., Amazon, Congo Basin, Borneo).
5. **Message groups** — One group for mosaic metadata events:
   - `nicfi_mosaics` — keyed by `{year}/{month}` (e.g., `2024/01`)
   - Subject: `planet-nicfi/mosaic/{year}/{month}`
   - Payload: Mosaic metadata + quad download URLs
6. **Reference data** — Emit list of all historical mosaics (2015-12 to present) at startup.

**Why not emit individual quads as events?** Quads are **tiles**, not **observations**. The mosaic is the atomic unit. Downstream consumers fetch quads on-demand based on their AOIs.

**Alternative**: For **on-demand access**, expose Planet Basemaps API directly via a proxy service. But Kafka adds:
- **Durable mosaic catalog** — New mosaics are persisted in topic, enabling historical replays
- **Change detection** — Compare consecutive months to detect deforestation events
- **Enrichment** — Bridge could pre-compute forest cover statistics, change masks, or alert polygons

**NICFI license compliance**: The bridge must:
- Include NICFI attribution in CloudEvent metadata (`source: "planet-nicfi"`, `attribution: "Planet & NICFI"`)
- Document non-commercial use restriction in CONTAINER.md and README
- Not redistribute raw imagery (only metadata + download URLs)

**Eligibility**: The repo maintainer must **enroll in NICFI** and obtain an API key. The bridge cannot be deployed by arbitrary users without their own API keys.

## Verdict

**CONDITIONAL ACCEPT (with reservations)** — This is a **high-value tropical forest monitoring source** with **unique resolution** (4.77m) and **monthly cadence**, but it has significant limitations:

1. **License restrictions** — Non-commercial only. If the repo targets commercial users or paid services, NICFI data is incompatible.
2. **Eligibility barrier** — Not universally open. Requires application + approval. Inconsistent with the repo's "open data feeds" focus.
3. **Sunset risk** — NICFI funding expires in 2025. The program may not continue.
4. **Monthly latency** — Not truly "real-time". Published 2-4 weeks after month-end.

**Recommended IF**:
- The repo wants to support **tropical forest monitoring** (deforestation, REDD+, carbon accounting)
- Users accept **non-commercial license** restrictions
- The repo maintainer is willing to **manage NICFI enrollment** and distribute API keys to authorized users

**Skip IF**:
- The repo prioritizes **universally open** data (no signup barriers)
- The repo targets **commercial users** (NICFI license prohibits this)
- The repo needs **true real-time** data (<1 day latency)

Alternative: For **open + real-time forest monitoring**, use:
- **Sentinel-2 L2A** (10m, 5-day revisit, fully open) via Planetary Computer or Earth Search
- **Landsat Collection 2** (30m, 16-day revisit, fully open) via Earth Search
- **MODIS/VIIRS fire products** (1km, daily, fully open) for fire alerts

NICFI's advantage is **resolution** (4.77m vs. 10-30m) and **monthly cloud-free composites** (vs. per-scene imagery with variable cloud cover). But the **license restrictions** and **eligibility barrier** make it a poor fit for a general-purpose open data repo.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3 | Unique 4.77m resolution, tropics-wide monthly composites |
| Freshness | 1 | Monthly cadence, 2-4 week lag (not real-time) |
| Openness | 1 | Requires eligibility approval, non-commercial license only |
| Schema clarity | 2 | Planet Basemaps API is well-documented but proprietary (not STAC) |
| Machine-readability | 3 | JSON API, GeoTIFF quads, COG-compatible |
| Repo fit | 2 | Tropics-only, license restrictions, eligibility barrier |
