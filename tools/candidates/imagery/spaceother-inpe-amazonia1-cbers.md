# INPE Amazonia-1 / CBERS-4A (Brazil-China Earth Resources Satellite)

- **Country/Region**: Global (Brazil-China partnership, South America priority)
- **Endpoint**: `http://www2.dgi.inpe.br/catalogo/explore` (INPE catalog)
- **Protocol**: HTTP download, WMS/WFS (TerraBrasilis integration)
- **Auth**: Free registration required
- **Format**: GeoTIFF, HDF5
- **Freshness**: Days to weeks (operational missions, catalog updates lag)
- **Docs**: http://www.inpe.br/amazonia1/, http://www.cbers.inpe.br/
- **Score**: 11/18

## Overview

**Amazonia-1** (launched 2021) is **Brazil's first 100% domestically-built EO satellite** providing **64m resolution** multispectral imagery with a **Wide Field Imager (WFI)** designed for **Amazon deforestation monitoring**. The satellite has a **5-day revisit** and is integrated with INPE's DETER and PRODES deforestation programs.

**CBERS-4A** (China-Brazil Earth Resources Satellite, launched 2019) is the latest in the CBERS series (partnership since 1988) providing **2m resolution panchromatic** (MUX camera) and **55m multispectral** (WFI camera) imagery. CBERS-4A complements Amazonia-1 for Brazilian environmental monitoring.

**Key sensors**:
- **Amazonia-1 WFI** — 64m resolution, 4 bands (blue, green, red, NIR), 850km swath, 5-day revisit
- **CBERS-4A MUX** — 16m multispectral (blue, green, red, NIR), 20m panchromatic (sharpened to 2m), 120km swath
- **CBERS-4A WFI** — 55m multispectral, 866km swath

**Data access**:
- **INPE catalog** — `http://www2.dgi.inpe.br/catalogo/` (free registration required)
- **TerraBrasilis integration** — WMS/WFS layers for recent acquisitions
- **AWS Open Data** — Some CBERS-4/4A scenes in AWS Registry of Open Data (experimental)

## Endpoint Analysis

**INPE catalog verified** — `http://www2.dgi.inpe.br/catalogo/explore` provides search interface.

However:
- **No STAC** — Custom HTML search form, not standards-based
- **Registration required** — Free account needed for download
- **HTTP download** — Scene-by-scene, no bulk API
- **Catalog lag** — New scenes appear days to weeks after acquisition (not NRT)

**TerraBrasilis WMS/WFS** — Some Amazonia-1/CBERS-4A scenes exposed via:
```
https://terrabrasilis.dpi.inpe.br/geoserver/wms?service=WMS&request=GetCapabilities&layers=amazonia1:recent_scenes
```

But coverage is sparse (only recent acquisitions for Brazil).

**Data format**:
- **GeoTIFF** — 16-bit multispectral, 8-bit panchromatic
- **HDF5** — Raw sensor data (L0/L1)
- **Metadata** — XML (scene-level)

**Stable identifiers**: Scene IDs (e.g., `AMAZONIA_1_WFI_20240115_042_016_L2_BAND4`). Keyed by `{satellite}/{sensor}/{date}/{path}/{row}`.

## Why Strong

1. **Brazil-operated** — Amazonia-1 is 100% Brazilian (not dependent on international partnerships for data access).
2. **5-day revisit** — Same as Sentinel-2 (but lower resolution: 64m vs. 10m).
3. **Amazon-optimized** — WFI designed for wide-swath tropical monitoring (850km swath).
4. **DETER integration** — Amazonia-1 is a primary data source for INPE DETER (deforestation alerts).
5. **Free and open** — INPE data policy allows scientific and commercial use.

## Limitations

- **Low resolution** — 64m (Amazonia-1 WFI) and 55m (CBERS-4A WFI) are coarser than Sentinel-2 (10m) or Landsat (30m).
- **No STAC/API** — Custom catalog, HTTP download only (not cloud-native).
- **Registration required** — Free but adds deployment friction.
- **Catalog lag** — Days to weeks (not NRT).
- **Brazil-centric** — Priority coverage over South America, global coverage secondary.
- **Limited ground segment** — INPE capacity constraints mean slower processing than ESA/USGS.

## Integration Notes

**Pattern**: **Catalog scraper** (HTTP polling, no API)

1. Authenticate to INPE catalog (`INPE_USERNAME`, `INPE_PASSWORD`)
2. Poll catalog search daily for new scenes
3. Parse HTML results for scene metadata (date, path/row, cloud cover, sensor)
4. Download GeoTIFF files via HTTP
5. Emit metadata to Kafka

**Message groups**:
- `amazonia1_scenes` — keyed by `{date}/{path}/{row}`
- `cbers4a_scenes` — keyed by `{date}/{path}/{row}`
- Payload: Scene metadata (bbox, cloud cover, sensor, download URL)

**Challenges**:
- No API (must scrape HTML catalog)
- Registration required
- Slow downloads (Brazil servers)

## Verdict

**CONDITIONAL ACCEPT** — Amazonia-1 and CBERS-4A provide **Brazil-operated multispectral monitoring** with **5-day revisit**, but **lower resolution** (64m vs. Sentinel-2 10m) and **no STAC/API** make integration challenging.

**Recommended IF**:
- Users need **Brazil-operated data** (not dependent on ESA/NASA)
- South America is the target region (priority coverage)
- Lower resolution is acceptable (64m vs. Sentinel-2 10m)
- Custom catalog scraper is feasible

**Skip IF**:
- Users need **cloud-native access** (STAC, COG) — use Sentinel-2 or Landsat instead
- Higher resolution is required (use Sentinel-2 10m or Landsat 30m)
- Repo wants **NRT latency** (Amazonia-1/CBERS catalog lags days to weeks)

Alternative: For **Amazon deforestation monitoring**, INPE **DETER** (already covered) is the **operational alert system** that **uses** Amazonia-1/CBERS data. Downstream consumers get **polygon alerts** (not raw scenes), which is more actionable.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 2 | Brazil-operated, 5-day revisit, Amazon-optimized, but lower resolution (64m) |
| Freshness | 1 | Catalog updates lag days to weeks (not NRT) |
| Openness | 2 | Free registration required, open data policy (scientific + commercial) |
| Schema clarity | 2 | Scene metadata in XML, but no STAC |
| Machine-readability | 2 | GeoTIFF, HDF5, but HTTP-only (no API, no COG) |
| Repo fit | 2 | Catalog scraping required, registration barrier, lower resolution |
