# CSA RADARSAT Constellation Mission (RCM) - Canada

- **Country/Region**: Global (Canada-operated, priority Arctic + Canada)
- **Endpoint**: `https://www.eodms-sgdot.nrcan-rncan.gc.ca/` (Earth Observation Data Management System)
- **Protocol**: REST API, WMS, WCS
- **Auth**: Government/academic accounts only (restricted access)
- **Format**: GeoTIFF, HDF5, NITF
- **Freshness**: Hours to days (operational mission, but access is restricted)
- **Docs**: https://www.asc-csa.gc.ca/eng/satellites/radarsat/default.asp
- **Score**: 7/18

## Overview

RADARSAT Constellation Mission (RCM) is **Canada's C-band SAR constellation** (three satellites: RCM-1/2/3, launched 2019) providing **3m resolution** (spotlight mode) to **100m resolution** (ScanSAR wide swath). The constellation offers **daily revisit** globally and **4× daily revisit** over Canada/Arctic.

RCM is designed for:
- **Maritime surveillance** (ship detection, ice monitoring, oil spills)
- **Disaster response** (floods, wildfires, landslides)
- **Agriculture** (crop monitoring, soil moisture)
- **Arctic monitoring** (sea ice extent, ice roads, permafrost)

**Key modes**:
- **Spotlight** — 3m resolution, 20×20 km swath
- **High-Resolution** — 5m resolution, 30 km swath
- **Medium-Resolution** — 16m resolution, 30-50 km swath
- **ScanSAR** — 50-100m resolution, 350-500 km swath

## Endpoint Analysis

**EODMS portal verified** — `https://www.eodms-sgdot.nrcan-rncan.gc.ca/` provides search interface.

However:
- **Restricted access** — Only Canadian government, academic institutions, and approved research partners
- **No public API** — REST API exists but requires institutional credentials
- **No STAC** — Custom catalog format
- **No open data portal** — RCM data is **not freely available** (unlike Sentinel-1 or Landsat)

**Canadian Open Government Portal** hosts **derived products** (ice charts, flood maps) but **not raw RCM imagery**.

**Access tiers**:
- **Government users** — Full access (federal/provincial agencies)
- **Academic users** — Research licenses (Canadian universities, some international via agreements)
- **Commercial users** — Paid licenses (expensive, enterprise pricing)
- **Public** — **No access** (derived products only)

## Why Strong (if accessible)

1. **3m resolution** — Finest C-band SAR globally (better than Sentinel-1 10m).
2. **Daily global revisit** — 3-satellite constellation provides frequent coverage.
3. **Arctic focus** — Best SAR coverage of polar regions (4× daily over Arctic).
4. **Compact polarimetry** — RCM supports circular polarization (CP) for improved classification.

## Limitations

- **Restricted access** — **Not open data**. Government/academic only.
- **No public API** — EODMS requires institutional credentials.
- **No STAC/COG** — Custom formats, not cloud-native.
- **Canada-centric** — Priority coverage over Canada/Arctic, global coverage secondary.
- **Expensive for commercial use** — Enterprise licensing (no free tier).

## Integration Notes

**Not feasible for open-data repo** — RCM is **not freely available**. Derived products (ice charts, flood maps) from Canadian Open Government Portal could be integrated, but **raw RCM imagery is out of scope**.

**Alternative**: Use **Sentinel-1** (fully open, global, 10m resolution, C-band SAR) via Copernicus Data Space or Earth Search. For **Arctic monitoring**, Sentinel-1 provides comparable coverage (though 10m vs. RCM 3-5m).

## Verdict

**REJECT (not open data)** — RCM is a **high-quality C-band SAR constellation** (3m resolution, daily revisit), but it's **restricted to government/academic users**. Raw imagery is **not freely available** to the public.

**Recommended**: Skip RCM, use **Sentinel-1** for open C-band SAR instead.

**Possible exception**: If the repo wants to add **derived products** from Canadian Open Government Portal (ice charts, flood maps), those are open. But raw RCM imagery is out of scope for an open-data repo.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3 | 3m C-band SAR, daily global revisit, Arctic focus |
| Freshness | 2 | Operational mission (hours to days), but access restricted |
| Openness | 0 | **Government/academic only, not public** (no open data) |
| Schema clarity | 1 | EODMS metadata, but no public API documentation |
| Machine-readability | 1 | GeoTIFF, HDF5, NITF, but restricted access |
| Repo fit | 0 | **Not open data** — institutional credentials required |
