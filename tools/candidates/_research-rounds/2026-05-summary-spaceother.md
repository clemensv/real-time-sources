# Space "Other" Sources Research Summary

## Executive Summary

Researched 20 near-real-time satellite Earth observation feeds from "other Western and open" space agencies and programs (non-NASA/ESA-Copernicus/NOAA/EUMETSAT/Asia). Focus on cloud-native STAC aggregators, national SAR programs, commercial open data, and specialty missions (ocean altimetry, deforestation, hyperspectral).

**Key findings**:
1. **STAC-on-AWS/Azure is the new substrate** — Cloud aggregators (Planetary Computer, Element84 Earth Search, Copernicus Data Space) provide superior access vs. legacy FTP/HTTP portals
2. **Open C-band SAR dominates** — Sentinel-1 (via STAC) is the clear leader; national programs (RCM, SAOCOM, COSMO-SkyMed) are either restricted or lack modern APIs
3. **Brazil (INPE) is a standout** — DETER deforestation + Queimadas fires are world-class operational systems with OGC WFS/WMS (no STAC but excellent data)
4. **Commercial "open data" is patchy** — Planet NICFI, Maxar, Umbra, Capella have license restrictions, sparse coverage, or static archives (not continuous feeds)
5. **NRT latency winners** — Copernicus Data Space (1-2h for Sentinel-2 L1C), AVISO+ (3-6h for ocean SSH), INPE Queimadas (3-6h for fire hotspots)

## Counts by Verdict

| Verdict | Count | Candidates |
|---------|-------|------------|
| **STRONG ACCEPT** | 7 | Planetary Computer STAC, Element84 Earth Search, Copernicus Data Space STAC, INPE DETER, INPE Queimadas, AVISO+ Altimetry, SWOT |
| **CONDITIONAL ACCEPT** | 6 | Digital Earth Australia, Planet NICFI, TanDEM-X DEM (static), CONAE SAOCOM, INPE Amazonia-1/CBERS, USGS LandsatLook STAC |
| **WEAK ACCEPT** | 4 | Maxar Open Data, Sentinel Hub STAC, Umbra SAR, Capella SAR |
| **REJECT** | 3 | CSA RCM (not open), EnMAP (not real-time), GEOSS Portal (metadata aggregator) |

## Topic-Grouped Table

### Imagery (Multi-Mission STAC Aggregators)

| Source | Score | Freshness | Openness | Verdict | Notes |
|--------|-------|-----------|----------|---------|-------|
| Microsoft Planetary Computer STAC | 16/18 | 2 | 3 | **STRONG** | 50+ collections (Landsat + Sentinel + GOES + MODIS), Azure-hosted, free SAS tokens |
| Element84 Earth Search STAC | 16/18 | 3 | 3 | **STRONG** | AWS-native, Landsat + Sentinel-1/2, public S3 buckets (no auth) |
| Copernicus Data Space STAC | 17/18 | 3 | 3 | **STRONG** | **Official ESA**, fastest NRT (1-2h for Sentinel-2 L1C), OAuth2 required |
| Digital Earth Australia STAC | 14/18 | 2 | 3 | **CONDITIONAL** | Australia-only, unique derived products (WOfS, fuel moisture, burned area) |
| Sentinel Hub STAC | 11/18 | 2 | 1 | **WEAK** | Commercial free tier (30k PU/month), on-demand rendering (not bulk download) |
| USGS LandsatLook STAC | 14/18 | 2 | 3 | **CONDITIONAL** | Metadata-only (no download links), use Element84 Earth Search instead |

### Imagery (SAR)

| Source | Score | Freshness | Openness | Verdict | Notes |
|--------|-------|-----------|----------|---------|-------|
| CONAE SAOCOM (Argentina L-band) | 10/18 | 1 | 2 | **CONDITIONAL** | **Only open L-band SAR globally**, FTP-only (no STAC), registration required |
| CSA RCM (Canada C-band) | 7/18 | 2 | 0 | **REJECT** | **Not open data** (government/academic only), 3m resolution but restricted |
| DLR TerraSAR-X / TanDEM-X | 9/18 | 0 | 1 | **CONDITIONAL** | TanDEM-X DEM (12m global, static) is open; raw SAR restricted (proposal/commercial) |
| Umbra SAR Open Data | 8/18 | 0 | 3 | **WEAK** | Ultra-high-res (25cm X-band), static archive (~10 sites), no API |
| Capella SAR Open Data | 9/18 | 0 | 2 | **WEAK** | 50cm X-band, static archive (~15 sites), multi-temporal (San Francisco) |

### Imagery (Optical - National)

| Source | Score | Freshness | Openness | Verdict | Notes |
|--------|-------|-----------|----------|---------|-------|
| INPE Amazonia-1 / CBERS-4A | 11/18 | 1 | 2 | **CONDITIONAL** | Brazil-operated, 64m resolution (lower than Sentinel-2), catalog scraping required |
| DLR EnMAP Hyperspectral | 10/18 | 0 | 2 | **REJECT** | 228-band hyperspectral (30m), tasking-based (weeks to months latency), **not NRT** |

### Wildfire / Deforestation

| Source | Score | Freshness | Openness | Verdict | Notes |
|--------|-------|-----------|----------|---------|-------|
| INPE DETER (Brazil deforestation) | 15/18 | 3 | 3 | **STRONG** | Daily NRT alerts (WFS), multi-sensor, **authoritative for Brazil** |
| INPE Queimadas (Brazil fire hotspots) | 16/18 | 3 | 3 | **STRONG** | NRT fire hotspots (WFS), multi-sensor (MODIS/VIIRS/GOES/Meteosat), FRP included |
| Planet NICFI (tropical forest monthly) | 12/18 | 1 | 1 | **CONDITIONAL** | 4.77m monthly mosaics (tropics ±30°), **non-commercial license**, eligibility required |

### Disaster Response

| Source | Score | Freshness | Openness | Verdict | Notes |
|--------|-------|-----------|----------|---------|-------|
| Maxar Open Data | 10/18 | 1 | 1 | **WEAK** | 0.3-0.5m (commercial-grade), event-driven (5-10/year), **CC BY-NC** (non-commercial) |

### Oceans

| Source | Score | Freshness | Openness | Verdict | Notes |
|--------|-------|-----------|----------|---------|-------|
| AVISO+ Altimetry (CNES) | 13/18 | 3 | 2 | **STRONG** | Multi-mission SSH/SLA/currents (Jason-3 + Sentinel-3/6 + Cryosat-2 + SARAL), NRT 3-6h |

### Hydrology

| Source | Score | Freshness | Openness | Verdict | Notes |
|--------|-------|-----------|----------|---------|-------|
| SWOT (NASA/CNES) | 15/18 | 3 | 3 | **STRONG** | **Unique inland water** (rivers, lakes, 15m resolution), ocean SSH (1km), NRT 6-12h |

### Cross-Cutting Aggregators

| Source | Score | Freshness | Openness | Verdict | Notes |
|--------|-------|-----------|----------|---------|-------|
| GEOSS Portal | 6/18 | 1 | 1 | **REJECT** | Metadata aggregator (not data source), federated search only, **no unified API** |

## Top 5 Picks (Across All "Other" Scope)

### 1. **Copernicus Data Space STAC API** (Score: 17/18)
**Rationale**: Official ESA STAC endpoint with **fastest NRT latency** (1-2h for Sentinel-2 L1C, ~3h for Sentinel-1 GRD). Covers **all Sentinel missions** (1/2/3/5P/6) in one catalog. Free registration (OAuth2) is a minor barrier. **Tier-1 source** for Sentinel-3 (ocean color, atmospheric composition) and Sentinel-5P (atmospheric chemistry) which are **not available** on Element84 or Planetary Computer.

**Why not #1 overall?** OAuth2 token management adds complexity vs. Element84's public S3 buckets. But for **Sentinel-3/5P/6**, this is the **only STAC option**.

### 2. **Element84 Earth Search STAC API** (Score: 16/18)
**Rationale**: **AWS-native Tier-1 STAC aggregator** for Landsat + Sentinel-1/2. Simpler auth than Copernicus Data Space (public S3 buckets, no tokens). Excellent NRT latency (1-3 days for Sentinel-2 L2A). **Best option for AWS-hosted bridges**. Narrower collection set than Planetary Computer (no GOES, MODIS/VIIRS), but focuses on the **core optical + SAR missions**.

**Pair with Planetary Computer** for GOES/MODIS/VIIRS, or pair with **Copernicus Data Space** for Sentinel-3/5P/6.

### 3. **Microsoft Planetary Computer STAC API** (Score: 16/18)
**Rationale**: **Broadest collection set** (50+ missions: Landsat + Sentinel-1/2/3 + GOES + MODIS/VIIRS + HLS + DEM + land cover). Azure-hosted, free SAS tokens (transparent via Python SDK). **Single integration** unlocks dozens of missions. **Best option for Azure-hosted bridges** or multi-mission coverage.

**Limitation**: Landsat NRT ~12h, Sentinel-2 L2A ~1-3d (slower than Copernicus Data Space by 1-2h). But **breadth** compensates.

### 4. **INPE DETER + Queimadas (Brazil)** (Scores: 15/18, 16/18)
**Rationale**: **World-class operational systems** for deforestation alerts (DETER, daily NRT) and fire hotspots (Queimadas, 3-6h NRT). **Authoritative for Brazil** (used by IBAMA, ICMBio, Federal Police). Rich attribution (municipality, biome, FRP, fire risk). **OGC WFS/WMS** (not STAC, but standard protocols).

**Why bundle?** Both are INPE-operated, same TerraBrasilis platform, complementary data (deforestation polygons + fire points). A single bridge can integrate both.

**Limitation**: Brazil-only geographic scope (but 60% of South American forests). For global fire monitoring, supplement with NASA FIRMS or Copernicus EFFIS.

### 5. **AVISO+ Altimetry (CNES)** (Score: 13/18)
**Rationale**: **Multi-mission ocean altimetry fusion** (Jason-3 + Sentinel-3A/B + Sentinel-6 + Cryosat-2 + SARAL). Single integration point for **global daily SSH/SLA/currents**. NRT products (3-6h latency) are **operational-grade** (used by Copernicus Marine, ECMWF, navies). Free registration (minor barrier).

**Why not higher?** NetCDF/OpenDAP (not STAC/JSON), FTP/THREDDS polling required (not REST). But **data quality** and **multi-mission fusion** are excellent.

**Pair with SWOT** for **inland water** (rivers, lakes) which AVISO+ does not cover.

## Notable Gaps

### 1. **No open high-resolution SAR** (continuous monitoring)
- **RCM (Canada)**: 3m C-band SAR, daily revisit, **government/academic only** (not public)
- **COSMO-SkyMed (Italy)**: 1m X-band SAR, **commercial** (Airbus/e-GEOS), no open NRT
- **SAOCOM (Argentina)**: 10m L-band SAR (unique soil moisture), **FTP-only**, catalog lag
- **TerraSAR-X (Germany)**: 1m X-band SAR, **proposal or commercial** (not open)

**Conclusion**: For **open SAR**, **Sentinel-1** (10m C-band, via Copernicus Data Space or Earth Search) is the **only continuous NRT option**. National programs are either restricted or lack modern APIs.

**Exception**: **SAOCOM** (L-band) is **unique** for soil moisture + biomass, but integration is difficult (FTP-only, registration, catalog lag).

### 2. **Commercial "open data" is not continuous**
- **Planet NICFI**: Monthly mosaics (not daily), **non-commercial license**, eligibility barrier
- **Maxar Open Data**: Disaster-activated (5-10 events/year), **CC BY-NC** (non-commercial)
- **Umbra / Capella SAR**: Sample scenes (static archives), not continuous monitoring

**Conclusion**: Commercial "open data" programs are **supplementary** (high-resolution samples for algorithm development, disaster response) but **not primary sources** for continuous monitoring.

### 3. **STAC coverage gaps**
- **No STAC**: AVISO+ (NetCDF/OpenDAP), SAOCOM (FTP), Amazonia-1/CBERS (HTTP), TerraSAR-X (WMS/WCS)
- **Experimental STAC**: Copernicus Data Space (COG assets incomplete), USGS LandsatLook (metadata-only, no download links)

**Conclusion**: **STAC is the future**, but legacy missions and national agencies lag behind. For **best STAC coverage**, use **Planetary Computer** (50+ collections) or **Copernicus Data Space** (all Sentinels).

### 4. **Hyperspectral is not NRT**
- **EnMAP (Germany)**: 228-band, 30m, tasking-based (weeks to months latency)
- **PRISMA (Italy)**: 240-band, 30m, tasking-based (not continuous)
- **DESIS (Germany)**: 235-band, 30m, ISS-mounted (limited coverage)

**Conclusion**: Hyperspectral missions are **tasking-based** or **experimental** (not continuous NRT monitoring). For **operational multispectral**, use **Sentinel-2** (13 bands, 10m, 5-day revisit, NRT).

### 5. **Regional focus limits global utility**
- **Digital Earth Australia**: Australia-only (excellent derived products, but narrow scope)
- **INPE DETER / Queimadas**: Brazil-centric (authoritative for South America, but not global)
- **SAOCOM**: South America priority coverage, global secondary

**Conclusion**: Regional sources are **excellent for their domains** (DEA for Australia, INPE for Brazil) but **not substitutes for global STAC aggregators** (Planetary Computer, Earth Search, Copernicus Data Space).

## Cross-Cutting Insights

### 1. **STAC-on-AWS/Azure is the new common substrate**
- **Planetary Computer** (Azure, 50+ collections), **Element84 Earth Search** (AWS, Landsat + Sentinel-1/2), **Copernicus Data Space** (ESA, all Sentinels) provide **unified STAC 1.0.0 access** to multi-mission EO data
- **COG-native assets** enable HTTP range requests, partial reads, cloud-optimized workflows
- **Python-first tooling** (pystac-client, odc-stac, stackstac) makes STAC the **de facto standard** for EO data access

**Impact on repo**: A **single STAC client bridge** (with OAuth2 token support for Copernicus) can integrate **100+ collections** across 3 endpoints (Planetary Computer, Earth Search, Copernicus Data Space). This is **far more efficient** than maintaining separate FTP/HTTP scrapers for each mission.

### 2. **Brazil (INPE) is a standout for operational monitoring**
- **DETER**: Daily deforestation alerts (multi-sensor fusion, WFS), **authoritative for Brazil**
- **Queimadas**: NRT fire hotspots (MODIS + VIIRS + GOES-16, WFS), includes FRP
- **TerraBrasilis**: Modern OGC WFS/WMS platform (not STAC, but well-designed)

**Why standout?** INPE integrates **satellite data** (Amazonia-1, CBERS, Sentinel-1/2, Landsat) with **operational workflows** (IBAMA enforcement, REDD+ reporting, fire risk modeling). The **open OGC APIs** (WFS/WMS) are excellent for integration.

**Comparison**: INPE's WFS/WMS is **better** than many national agencies that rely on FTP (CONAE, DLR) or restricted portals (CSA, ASI).

### 3. **NRT latency hierarchy**
| Latency | Sources | Use Cases |
|---------|---------|-----------|
| **1-2 hours** | Copernicus Data Space (Sentinel-2 L1C), INPE Queimadas (fire hotspots) | Disaster response, wildfire detection, flood monitoring |
| **3-6 hours** | Copernicus Data Space (Sentinel-1 GRD, Sentinel-3), AVISO+ (ocean SSH), SWOT (river/lake water level) | Ocean forecasting, maritime ops, flood forecasting |
| **12-24 hours** | Element84 Earth Search (Landsat), Planetary Computer (Landsat), INPE DETER (deforestation) | Agricultural monitoring, deforestation enforcement |
| **1-3 days** | Element84 Earth Search (Sentinel-2 L2A), Planetary Computer (Sentinel-2 L2A), Digital Earth Australia (ARD) | Land cover classification, vegetation indices |
| **Weeks to months** | SAOCOM (catalog lag), Amazonia-1/CBERS (catalog lag), EnMAP (tasking) | Historical analysis, algorithm development |

**Insight**: For **true NRT** (<6 hours), use **Copernicus Data Space** (Sentinel-1/2/3), **INPE Queimadas** (fires), or **AVISO+** (ocean). For **daily NRT** (12-24h), **Element84 Earth Search** (Landsat, Sentinel-2) is excellent. For **tasking-based or historical**, national agencies lag significantly.

### 4. **OAuth2 token management is the new auth barrier**
- **Copernicus Data Space**: OAuth2 `client_credentials` flow, tokens expire in 10 minutes (auto-refresh required)
- **Sentinel Hub**: OAuth2, free tier capped (30k PU/month), commercial above
- **AVISO+**: Free registration (username/password), FTP credentials

**Impact on repo**: Bridges must handle **OAuth2 token refresh** for Copernicus Data Space (most important NRT source). Use **refresh_token grant** to avoid re-authentication. Python libraries like `oauthlib` or `requests-oauthlib` simplify this.

**Alternative**: For **no-auth simplicity**, use **Element84 Earth Search** (public S3 buckets) or **Planetary Computer** (free SAS token signing via Python SDK).

### 5. **License confusion (commercial vs. non-commercial)**
- **Planet NICFI**: Free for **non-commercial** (REDD+, research), **prohibits commercial use**
- **Maxar Open Data**: **CC BY-NC 4.0** (non-commercial), disaster-activated
- **Umbra / Capella SAR**: Mostly **CC BY 4.0** (commercial allowed), but sample scenes only

**Impact on repo**: If the repo targets **commercial users**, **NICFI and Maxar are incompatible**. Document license restrictions in CONTAINER.md and README.

**Best practice**: For **fully open** data (no commercial restrictions), stick to:
- **Sentinel** (ESA open data policy, commercial use allowed)
- **Landsat** (US public domain, no restrictions)
- **AVISO+** (CNES open data policy, commercial use allowed with attribution)
- **SWOT** (NASA public domain, CNES open data policy)

### 6. **NICFI sunset risk (2025)**
- **NICFI funding expires in 2025** (Norway's International Climate & Forests Initiative)
- Program may not continue after 2025 (depends on Norwegian government budget renewal)

**Impact on repo**: If NICFI is added, **document sunset risk** and have a **fallback plan** (Sentinel-2 10m or Landsat 30m for tropical forest monitoring).

## Recommendations for Repo Integration

### **Tier-1 Sources** (must-have)
1. **Copernicus Data Space STAC** — All Sentinels (1/2/3/5P/6), fastest NRT (1-2h), official ESA
2. **Element84 Earth Search STAC** — Landsat + Sentinel-1/2, AWS-native, no auth
3. **Microsoft Planetary Computer STAC** — 50+ collections (GOES, MODIS/VIIRS, HLS, DEM), Azure-native
4. **INPE DETER + Queimadas** — Brazil deforestation + fire hotspots, operational authority, OGC WFS/WMS
5. **AVISO+ Altimetry** — Multi-mission ocean SSH/SLA/currents, NRT 3-6h, operational-grade
6. **SWOT** — Inland water (rivers, lakes), unique capability, NASA/CNES joint

### **Tier-2 Sources** (strong value, conditional acceptance)
7. **Digital Earth Australia** — Australia-specific derived products (WOfS, fuel moisture, burned area)
8. **SAOCOM** — Only open L-band SAR (soil moisture, biomass), FTP-only (integration challenge)
9. **Planet NICFI** — Tropical forest 4.77m monthly, non-commercial license (REDD+ focus)

### **Tier-3 Sources** (supplementary, static archives)
10. **TanDEM-X DEM** — Global 12m DEM (static baseline, one-time ingestion)
11. **Maxar Open Data** — Disaster response 0.3-0.5m imagery (event-driven, CC BY-NC)
12. **Umbra / Capella SAR** — Ultra-high-res SAR samples (static archives, algorithm development)

### **Skip**
- **CSA RCM** (not open data)
- **EnMAP** (not real-time)
- **GEOSS Portal** (metadata aggregator, not data source)
- **USGS LandsatLook STAC** (metadata-only, use Element84 Earth Search instead)
- **Sentinel Hub STAC** (commercial free tier, on-demand rendering, not bulk download)
- **Amazonia-1/CBERS** (lower resolution than Sentinel-2, catalog scraping required, DETER is better for Brazil)

## Final Verdict Summary

| Tier | Count | Sources |
|------|-------|---------|
| **Tier-1 (must-have)** | 6 | Copernicus Data Space, Element84 Earth Search, Planetary Computer, INPE DETER + Queimadas, AVISO+, SWOT |
| **Tier-2 (strong value)** | 3 | Digital Earth Australia, SAOCOM, Planet NICFI |
| **Tier-3 (supplementary)** | 4 | TanDEM-X DEM, Maxar Open Data, Umbra SAR, Capella SAR |
| **Skip** | 7 | CSA RCM, EnMAP, GEOSS, LandsatLook STAC, Sentinel Hub STAC, Amazonia-1/CBERS, (implied: ASI COSMO-SkyMed) |

**Total candidates evaluated**: 20  
**Strong Accept**: 7  
**Conditional Accept**: 6  
**Weak Accept**: 4  
**Reject**: 3
