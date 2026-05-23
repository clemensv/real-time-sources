# CONAE SAOCOM (Argentina L-Band SAR Mission)

- **Country/Region**: Global (Argentina-operated)
- **Endpoint**: `https://catalogos.conae.gov.ar/` (catalog portal), FTP download
- **Protocol**: FTP, HTTP (catalog search)
- **Auth**: Free registration required
- **Format**: HDF5, GeoTIFF
- **Freshness**: Days to weeks (operational mission, but catalog updates lag)
- **Docs**: https://www.argentina.gob.ar/ciencia/conae/saocom, https://catalogos.conae.gov.ar/
- **Score**: 10/18

## Overview

SAOCOM-1A and SAOCOM-1B are Argentina's **L-band SAR satellites** (1.27 GHz, 23cm wavelength) providing **10m resolution** imagery. L-band penetrates vegetation canopy and dry soil better than C-band (Sentinel-1) or X-band (Umbra, Capella), making it ideal for:
- **Soil moisture mapping** (agriculture)
- **Forest biomass estimation** (canopy penetration)
- **Subsidence monitoring** (InSAR over vegetated areas)
- **Oil spill detection** (ocean)

CONAE (Comisión Nacional de Actividades Espaciales) operates the ground segment and distributes data via **catalogos.conae.gov.ar** portal.

**Data tiers**:
- **L1A** — Single Look Complex (SLC, phase-preserved for InSAR)
- **L1B** — Detected imagery (amplitude only)
- **L1C** — Geocoded, terrain-corrected
- **L2** — Derived products (soil moisture, biomass)

## Endpoint Analysis

**Catalog portal verified** — `https://catalogos.conae.gov.ar/` provides search interface.

However:
- **No STAC** — Custom HTML/JavaScript search form, not standards-based
- **No REST API** — Must use web UI or FTP directory listing
- **Registration required** — Free account needed for download access
- **FTP access** — `ftp://ftp.conae.gov.ar/` (requires credentials)

**Access workflow**:
1. Register at https://catalogos.conae.gov.ar/
2. Search catalog via web UI (filter by date, bbox, mode, polarization)
3. Download via HTTP or FTP (scene-by-scene, no bulk API)

**No public S3 or cloud access** — Data hosted on CONAE servers (Argentina).

## Schema/Sample

**SAOCOM scene metadata**:
- Scene ID: `SAOCOM1A_SM_20240115_DI_0001`
- Acquisition date: `2024-01-15`
- Mode: Stripmap (SM), TOPSAR (TS), or Scansar (SC)
- Polarization: HH, VV, HH+HV, VV+VH
- Resolution: 10m (Stripmap), 30m (Scansar)
- Swath: 40-320 km (mode-dependent)

**Stable identifiers**: Scene IDs are unique. Keyed by `{platform}/{mode}/{date}/{scene_id}`.

## Why Strong

1. **L-band** — Only **open L-band SAR** globally (JAXA ALOS-2 PALSAR-2 is commercial). Unique soil moisture + biomass capability.
2. **10m resolution** — Competitive with Sentinel-1 C-band (also 10m).
3. **Dual-satellite constellation** — SAOCOM-1A + 1B provide 8-day revisit.
4. **Free and open** — CONAE data policy allows scientific and commercial use (attribution required).
5. **Argentina-operated** — Non-ESA, non-NOAA alternative for SAR.

## Limitations

- **No STAC/REST API** — Web UI only, no programmatic search.
- **Registration required** — Free but adds deployment friction.
- **FTP download** — Not cloud-native (no S3, no COG).
- **Catalog lag** — New scenes appear days to weeks after acquisition (not NRT).
- **Argentina-hosted** — Slow download speeds outside South America.
- **Limited documentation** — English docs sparse, Spanish primary.

## Integration Notes

**Pattern**: **FTP directory poller** (non-standard, requires custom scraper)

1. Authenticate to FTP server (`CONAE_USERNAME`, `CONAE_PASSWORD`)
2. List `/saocom1a/` and `/saocom1b/` directories daily
3. Parse filenames for scene metadata (date, mode, polarization)
4. Download HDF5/GeoTIFF files
5. Emit metadata to Kafka

**Message groups**:
- `saocom_sar_scenes` — keyed by `{platform}/{mode}/{date}`
- Payload: Scene metadata + download URL

**Challenges**:
- No API (must scrape FTP or web UI)
- Slow downloads (Argentina servers)
- No push notifications (poll FTP daily)

## Verdict

**CONDITIONAL ACCEPT** — SAOCOM is the **only open L-band SAR mission** globally, making it **unique** for soil moisture and biomass monitoring. However, **no STAC/API**, **registration required**, and **FTP-only access** make integration **difficult**.

**Recommended IF**:
- Users need **L-band SAR** (soil moisture, forest biomass, subsidence over vegetation)
- South America is the target region (faster downloads, regional focus)
- Custom FTP scraper is acceptable (no standard API)

**Skip IF**:
- Users need **cloud-native access** (STAC, COG, S3) — use Sentinel-1 instead
- Global coverage is priority (SAOCOM has limited revisit outside South America)
- Repo wants **NRT latency** (SAOCOM catalog lags days to weeks)

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3 | Only open L-band SAR globally, unique soil moisture + biomass capability |
| Freshness | 1 | Catalog updates lag days to weeks (not NRT) |
| Openness | 2 | Free registration required, open data policy (scientific + commercial) |
| Schema clarity | 1 | Minimal metadata (filenames), no STAC |
| Machine-readability | 1 | HDF5, GeoTIFF, but FTP-only (no API, no COG) |
| Repo fit | 2 | FTP scraping required, registration barrier, slow downloads |
