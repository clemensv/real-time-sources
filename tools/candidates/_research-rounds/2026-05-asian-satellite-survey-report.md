# Asian Space Agency Satellite Feed Survey - Final Report

**Survey Scope**: Near-real-time satellite Earth observation feeds from Asian space agencies (JAXA, ISRO, KARI, CNSA, TASA)  
**Date**: January 2026  
**Investigator**: GitHub Copilot CLI (6-agent parallel research fleet)  
**Total Candidates Evaluated**: 11

---

## Executive Summary

This survey identified **11 candidate feeds** from Asian space agencies, with scores ranging from **3/18 to 14/18**. The findings reveal a **stark contrast** in open data maturity:

- **JAXA (Japan)**: World-class open data via AWS S3 mirrors (Himawari) and G-Portal SFTP (GCOM-W/C). **4 strong candidates**, including 2 flagship-quality sources.
- **KARI (South Korea)**: Advanced sensors (GEMS air quality, GOCI-II ocean color) but **severe access barriers** (registration, Korean-language portals, no cloud mirrors). **0 viable candidates** without registration success.
- **ISRO (India)**: Registration walls, proprietary formats, and domestic user preference. **0 viable candidates**. VEDAS API Centre is promising but not NRT.
- **CNSA (China)**: Fengyun-4 geostationary satellites exist but **Chinese-language portal and closed access model** disqualify them. **0 viable candidates**.
- **TASA (Taiwan)**: No NRT satellite imagery feeds identified (FORMOSAT-5 is tasked optical, FORMOSAT-7/COSMIC-2 is radio occultation distributed via UCAR).

**Top Recommendation**: **JAXA Himawari-9 L2 Sea Surface Temperature** (AWS S3, 13/18 score) — world-class 10-minute SST, open access, manageable volume, directly usable ocean parameter.

---

## Counts by Agency

| Agency | Candidates | ✅ Recommend | ⚠️ Conditional | ❌ Skip |
|--------|------------|-------------|---------------|---------|
| **JAXA (Japan)** | 5 | 4 | 0 | 1 |
| **KARI (Korea)** | 3 | 0 | 2 | 1 |
| **ISRO (India)** | 2 | 0 | 1 | 1 |
| **CNSA (China)** | 1 | 0 | 0 | 1 |
| **TASA (Taiwan)** | 0 | 0 | 0 | 0 |
| **Total** | **11** | **4** | **3** | **4** |

---

## Counts by Verdict

| Verdict | Count | Candidates |
|---------|-------|------------|
| **✅ Recommend** | 4 | Himawari L2 SST (13/18), Himawari L1b (14/18), GCOM-W AMSR2 (10/18), GCOM-C SGLI (9/18) |
| **⚠️ Conditional** | 3 | KARI GEMS (8/18), KARI GOCI-II (7/18), ISRO VEDAS (7/18) |
| **❌ Skip** | 4 | KARI GK-2A (6/18), JAXA P-Tree (5/18), ISRO INSAT-3D (4/18), CNSA FY-4 (3/18) |

---

## Topic-Grouped Table

| Topic | Candidate | Agency | Score | Verdict | Notes |
|-------|-----------|--------|-------|---------|-------|
| **Imagery** | Himawari-9 AHI L1b Full Disk | JAXA | 14/18 | ✅ Recommend | AWS S3, 16-band, 10-min, 160 files/scan |
| **Imagery** | VEDAS API Centre | ISRO | 7/18 | ⚠️ Conditional Skip | WMS tiles + NDVI API, not NRT |
| **Oceans** | Himawari-9 L2 SST | JAXA | 13/18 | ✅ **Top Pick** | AWS S3, 10-min SST, 1 file/scan |
| **Oceans** | GCOM-W AMSR2 SST/Sea Ice | JAXA | 10/18 | ✅ Recommend | G-Portal SFTP, microwave all-weather |
| **Oceans** | GCOM-C SGLI Ocean Color/LST | JAXA | 9/18 | ✅ Recommend | G-Portal SFTP, 19-band advanced OC |
| **Oceans** | GOCI-II Ocean Color | KARI | 7/18 | ⚠️ Conditional | Hourly geostationary OC, registration barrier |
| **Oceans** | P-Tree SST Web Viewer | JAXA | 5/18 | ❌ Skip | Web map tiles only, not data API |
| **Air Quality** | GEMS NO2/SO2/AOD | KARI | 8/18 | ⚠️ Conditional | World-first GEO AQ, registration barrier |
| **Weather** | GEO-KOMPSAT-2A AMI | KARI | 6/18 | ❌ Skip | No cloud mirror, overlaps with Himawari |
| **Weather** | INSAT-3D/3DR Imager | ISRO | 4/18 | ❌ Skip | Severe registration barrier, proprietary format |
| **Weather** | Fengyun-4A/4B AGRI | CNSA | 3/18 | ❌ Skip | Chinese-language, closed access |

---

## Top 5 Picks Across All Agencies

### 1. **JAXA Himawari-9 L2 Sea Surface Temperature** (13/18) — **Flagship**
- **Why**: AWS S3 (no auth), 10-minute global SST, 144 files/day, typhoon forecasting, fisheries, climate monitoring
- **Access**: `s3://noaa-himawari9/AHI-L2-FLDK-ISatSS/`
- **Volume**: 1 NetCDF4 file per 10-minute observation (~3 GB/day total)
- **Bridge Effort**: Moderate (S3 polling, NetCDF4 parsing, metadata extraction)
- **Impact**: World-class temporal resolution for geostationary SST, fills major gap in repo (no satellite ocean products)

### 2. **JAXA Himawari-9 L1b Full Disk Imagery** (14/18) — **Flagship**
- **Why**: AWS S3 (no auth), 16-band multispectral, 10-minute full disk, typhoon/wildfire/volcanic ash tracking
- **Access**: `s3://noaa-himawari9/AHI-L1b-FLDK/`
- **Volume**: 160 files per 10-minute scan (~2-3 TB/day raw) — **requires scoping** (recommend band-level events, not segment-level)
- **Bridge Effort**: High (S3 polling, NetCDF4, volume management)
- **Impact**: First geostationary satellite in repo, first Asian satellite source, global meteorological use

### 3. **JAXA GCOM-W AMSR2 SST + Sea Ice** (10/18) — **Strong**
- **Why**: All-weather microwave SST/sea ice, complements Himawari infrared, critical for polar regions
- **Access**: G-Portal SFTP (free registration, 1-2 day approval)
- **Volume**: ~14 orbits/day, L3 daily grids = 2 files/day (SST + SIC)
- **Bridge Effort**: Moderate (SFTP polling, HDF5 parsing, registration overhead)
- **Impact**: Fills polar/all-weather gap, pairs with Himawari for comprehensive ocean coverage

### 4. **JAXA GCOM-C SGLI Ocean Color + LST** (9/18) — **Strong**
- **Why**: 19-band advanced ocean color (chlorophyll-a), land surface temperature, complements MODIS/VIIRS
- **Access**: G-Portal SFTP (same credentials as GCOM-W)
- **Volume**: ~14 orbits/day, L3 daily grids = 5-10 files/day
- **Bridge Effort**: Moderate (same SFTP as GCOM-W, HDF5)
- **Impact**: Adds ocean color and land surface to GCOM suite, complements GCOM-W microwave

### 5. **KARI GEMS Air Quality (NO2/SO2/AOD)** (8/18) — **Conditional**
- **Why**: World-first geostationary air quality, hourly NO2/SO2/aerosols over East Asia, transboundary pollution tracking
- **Access**: NESC portal (registration required, Korean institutions preferred, approval timeline unknown)
- **Volume**: ~8 hours/day × 6 products × hourly = ~100 files/day
- **Bridge Effort**: High (registration barrier, FTP access uncertainty, NetCDF4)
- **Impact**: Unique domain (GEO air quality), scientifically significant, but **access risk is severe**

---

## Notable Gaps by Agency

### JAXA (Japan) — **Best-in-Class Open Data**
- ✅ **Strengths**: AWS S3 mirrors (Himawari), G-Portal SFTP (GCOM-W/C), documented APIs (CSW), English documentation
- ❌ **Gaps**: 
  - ALOS-2 SAR NRT data not openly available (G-Portal has archive, but NRT is restricted or limited)
  - GPM precipitation radar (joint with NASA) is primarily NASA-distributed, not separate JAXA NRT endpoint
  - ISS-based sensors (IMAP, SMILES) are archive-only or experimental

### KARI (South Korea) — **Advanced Sensors, Closed Access**
- ✅ **Strengths**: GEMS (world-first GEO air quality), GOCI-II (world-class GEO ocean color), GK-2A/AMI (16-band geostationary)
- ❌ **Gaps**:
  - **No open cloud mirrors** — unlike JAXA's Himawari (AWS), KARI data is portal-locked
  - **Korean-language barriers** — English documentation is sparse, registration forms in Korean
  - **Domestic user preference** — international users face approval delays or rejections
  - **No public APIs** — web portals and FTP only, no REST/OGC services
- **Potential fix**: If KARI partnered with NOAA/AWS (like JMA did for Himawari), GK-2A and GEMS data could become world-accessible overnight

### ISRO (India) — **Proprietary Formats, Registration Walls**
- ✅ **Strengths**: INSAT-3D/3DR cover unique geography (Indian Ocean), VEDAS API Centre is a positive step
- ❌ **Gaps**:
  - **MOSDAC registration barrier** — severe, Indian institutions strongly preferred
  - **Proprietary IMG format** — INSAT data historically in ISRO-specific format, HDF5 transition incomplete
  - **No NRT products via VEDAS** — VEDAS API has temporal composites (weeks lag), not live satellite data
  - **Oceansat-3 ocean color** — launched 2022, but MOSDAC distribution suffers same access issues
  - **RISAT SAR** — likely restricted for defense reasons
- **Potential fix**: ISRO could mirror select datasets (INSAT-3D L2 products, Oceansat-3 chlorophyll) to AWS/Azure with open access. VEDAS API Centre could add NRT feeds.

### CNSA (China) — **Closed Data Model**
- ✅ **Strengths**: Fengyun-4A/4B (14-band geostationary, 15-min full disk), FY-3 polar-orbiters, HY-1/2 ocean, Gaofen high-res
- ❌ **Gaps**:
  - **Chinese-language portal** — NSMC portal is primarily Chinese, minimal English
  - **No international open data program** — CMA does not mirror FY-4 to AWS/cloud (unlike NOAA for Himawari)
  - **Domestic user focus** — MICAPS/CIMISS systems are for Chinese institutions
  - **Data export restrictions** — China's data sovereignty policies may limit foreign redistribution
- **Potential fix**: WMO data sharing agreements or bilateral partnerships (e.g., EUMETSAT-CMA) could open select FY-4 products. CMACast satellite broadcast exists but requires ground receiver.

### TASA (Taiwan) — **No Imagery Satellites Identified**
- ✅ **Strengths**: FORMOSAT-7/COSMIC-2 radio occultation (joint with NOAA, distributed via UCAR CDAAC — excellent open access for atmospheric profiles)
- ❌ **Gaps**:
  - **FORMOSAT-5** optical imaging — tasked system (not continuous coverage), archive via NSPO portal (registration required)
  - **No geostationary satellites** — Taiwan does not operate GEO satellites
  - **No polar-orbiting wide-swath imagers** — FORMOSAT series are narrow-swath high-resolution (0.5-2 m), not suitable for NRT global products
- **Note**: FORMOSAT-7/COSMIC-2 GPS-RO data (atmospheric temperature/moisture profiles) is openly available via UCAR but is **not satellite imagery** — it's radio occultation soundings. Separate domain.

---

## Cross-Cutting Themes

### 1. **Open Data Maturity by Agency** (Ranked)

| Rank | Agency | Openness Score | Evidence |
|------|--------|----------------|----------|
| 1 | **JAXA** | ⭐⭐⭐⭐⭐ | AWS S3 mirrors (no auth), G-Portal SFTP (free registration), CSW catalog, English docs, redistribution allowed |
| 2 | **TASA** | ⭐⭐⭐⭐ | COSMIC-2 via UCAR (open), FORMOSAT-5 archive (registration but accessible) |
| 3 | **KARI** | ⭐⭐ | Registration required, Korean-language, domestic preference, no cloud mirrors |
| 4 | **ISRO** | ⭐ | Severe registration barriers, proprietary formats, Indian institutions preferred |
| 5 | **CNSA** | ⭐ | Chinese-language, no international open data, data export restrictions |

### 2. **Sentinel Asia & CEOS Coordination**

**Sentinel Asia** (disaster response imagery sharing, coordinated by JAXA) exists but is a **request-based system** for emergency observations, not a continuous NRT feed. Member agencies (JAXA, KARI, ISRO, etc.) contribute imagery during disasters, but the data is shared among Sentinel Asia partners, not publicly streamed.

**CEOS (Committee on Earth Observation Satellites)** promotes data sharing standards, but compliance varies. JAXA is highly compliant (CEOS-ARD for PALSAR-2 mosaics). KARI and ISRO participate in CEOS but have not adopted open cloud distribution.

### 3. **GEO-KOMPSAT vs Himawari Overlap**

**Coverage comparison**:
- **Himawari-9** at 140.7°E — optimal for Japan, western Pacific, Australia
- **GEO-KOMPSAT-2A** at 128.2°E — optimal for Korea, China, Southeast Asia
- **Overlap**: Both cover Korea, Japan, China, Philippines, Indonesia, western Pacific

**Why Himawari wins**:
- ✅ AWS S3 open access (vs KARI portal registration)
- ✅ 10-minute full disk (vs GK-2A 10 min, tied)
- ✅ 16 bands (vs GK-2A 16 bands, tied)
- ✅ English documentation (vs Korean-primary)

**When GK-2A would be better**:
- If you need the 128.2°E viewing angle specifically (better western China, India coverage)
- If KARI opened GK-2A data to AWS/cloud (would become competitive)

**GOCI-II unique value**: Hourly geostationary ocean color has no Himawari equivalent (Himawari L2 ocean color is static algorithms, not hourly monitoring). GOCI-II is worth pursuing **if accessible via NASA Ocean Color mirror**.

### 4. **Why Asian Agencies Lag Western Agencies in Open Data**

**Leading open data examples**:
- 🇺🇸 **NOAA/NASA**: GOES-16/17 on AWS, Landsat on AWS/GCP, Sentinel mirror on AWS
- 🇪🇺 **EUMETSAT/ESA**: Sentinel on AWS/GCP, Copernicus Open Access Hub, WEkEO

**Asian agency challenges**:
1. **Data sovereignty concerns** — China, India have policies restricting foreign data redistribution
2. **Domestic user focus** — KARI, ISRO prioritize national users over international community
3. **Language barriers** — Chinese/Korean-primary portals limit international adoption
4. **Cloud infrastructure partnerships** — NOAA/ESA have formal AWS/GCP partnerships; Asian agencies lack equivalent
5. **Export control** — Some sensors (SAR, high-resolution optical) may have defense/security restrictions

**Exception**: JAXA is **world-class** in open data (Himawari AWS mirror, G-Portal SFTP, CEOS-ARD compliance). This is partly due to:
- US-Japan cooperation (NOAA mirrors Himawari)
- WMO commitments (meteorological data sharing)
- Scientific community engagement (JAXA supports international research)

---

## Recommendations

### Immediate Actions (High Confidence)

1. **✅ Implement Himawari-9 L2 SST bridge** (AWS S3, 13/18 score)
   - Easiest entry point for Asian satellite data
   - 10-minute global SST grid, 144 files/day, open access
   - S3 polling pattern is new to repo but well-documented
   - **Deliverable**: 1 event per 10 minutes, ~4,300 events/month

2. **✅ Implement Himawari-9 L1b bridge (band-level events)** (AWS S3, 14/18 score)
   - Emit 1 event per band per 10-minute scan (16 events/10 min, 2,300 events/day)
   - Each event references 10 S3 URLs (segment files for that band)
   - Avoids overwhelming Kafka with 160 events per scan
   - **Deliverable**: Full 16-band multispectral coverage, typhoon/wildfire/ash tracking

### Moderate-Effort Actions (Registration Required)

3. **⚠️ Attempt G-Portal registration for GCOM-W/AMSR2 + GCOM-C/SGLI**
   - Free registration, 1-2 day approval expected
   - If approved, implement L3 daily grids:
     - GCOM-W: SST + Sea Ice (2 files/day, microwave all-weather)
     - GCOM-C: Chlorophyll-a + LST (5 files/day, ocean color + land surface)
   - **Deliverable**: Polar-orbiting complement to geostationary Himawari

4. **⚠️ Check NASA Ocean Color for GOCI-II**
   - If GOCI-II is mirrored to https://oceancolor.gsfc.nasa.gov, it becomes **highly viable** (score increases to 12/18)
   - Hourly geostationary ocean color is unique and valuable
   - If not on NASA Ocean Color, **skip KOSC registration** (Korean-language barrier, uncertain approval)

### Low-Priority / Monitor for Future

5. **📋 Monitor VEDAS API Centre for NRT products**
   - VEDAS is ISRO's first public API — a positive development
   - If they add daily Resourcesat AWIFS or hourly INSAT-3D products, re-evaluate
   - Current offering (temporal composites, WMS tiles) is not suitable for NRT bridge

6. **📋 Monitor KARI GEMS if registration pathway clarifies**
   - GEMS (world-first GEO air quality) is scientifically significant
   - But registration barrier is severe (Korean institutions preferred, approval opaque)
   - **Only pursue if**:
     - Clear English registration pathway documented
     - International users report successful approval
     - Or GEMS data mirrored to NASA/EUMETSAT

7. **❌ Skip GK-2A, INSAT-3D, Fengyun-4**
   - GK-2A overlaps with Himawari (which is openly accessible)
   - INSAT-3D registration barrier is prohibitive
   - Fengyun-4 Chinese-language and closed access disqualify it

---

## Deliverables

**Candidate files created**: 11  
**Path**: `c:\git\real-time-sources\tools\candidates\{topic}\{agency}-{slug}.md`

**Topics covered**:
- `imagery/` — 2 files (Himawari L1b, VEDAS API)
- `oceans/` — 5 files (Himawari SST, GCOM-W, GCOM-C, GOCI-II, P-Tree)
- `air-quality/` — 1 file (GEMS)
- `weather/` — 3 files (GK-2A, INSAT-3D, FY-4)

**Each file contains**:
- Bullet metadata (country, endpoint, protocol, auth, format, freshness, docs, score)
- Overview
- Endpoint analysis (live probing where possible)
- Schema / sample metadata
- Why strong / why valuable
- Limitations
- Verdict (✅ Recommend, ⚠️ Conditional, ❌ Skip)
- Scoring table (6 criteria × 3 points)

---

## Conclusion

**Asian space agencies operate world-class satellites** — JAXA's Himawari-9, KARI's GEMS, ISRO's INSAT-3D, and CNSA's Fengyun-4 are technically on par with Western geostationary missions. However, **open data accessibility varies dramatically**:

- **JAXA is exemplary** — Himawari AWS mirror and G-Portal SFTP make Japanese satellite data as accessible as NOAA/NASA data.
- **KARI has advanced sensors** (GEMS, GOCI-II) but **closed access models** limit international adoption.
- **ISRO and CNSA prioritize domestic users**, with registration barriers and language challenges that disqualify most feeds for this repo.

**Top recommendation**: Start with **JAXA Himawari-9 L2 SST** (AWS S3, no auth, 10-minute global ocean temperature) as the **flagship Asian satellite bridge**. If successful, expand to **Himawari L1b** (16-band imagery) and **GCOM-W/C** (polar-orbiting microwave + ocean color).

**Long-term opportunity**: Advocate for **KARI to mirror GK-2A and GEMS to AWS** (following JAXA's Himawari model). This single change would unlock world-class air quality and ocean color data for the global community.

---

**Report Date**: 2026-01-15  
**Next Review**: Monitor VEDAS API Centre and KARI/NASA partnerships quarterly.
