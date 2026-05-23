# CNSA Fengyun-4A/4B Geostationary Imagery

- **Country/Region**: China / East Asia, Western Pacific
- **Endpoint**: https://satellite.nsmc.org.cn (National Satellite Meteorological Center)
- **Protocol**: Web portal (Chinese-language), data server details unclear
- **Auth**: Registration required (Chinese language, domestic users preferred)
- **Format**: HDF5, GRIB2 (likely)
- **Freshness**: 15 minutes (full disk), 5 minutes (regional)
- **Docs**: https://satellite.nsmc.org.cn (Chinese language)
- **Score**: 3/18

## Overview

Fengyun-4A (FY-4A, launched 2016) and Fengyun-4B (FY-4B, launched 2021) are Chinese geostationary meteorological satellites stationed at 104.7°E and 123°E respectively. They carry the Advanced Geostationary Radiation Imager (AGRI) — a 14-channel multispectral imager providing full-disk scans every 15 minutes and regional scans every 5 minutes.

FY-4 also carries the Geostationary Interferometric Infrared Sounder (GIIRS) for atmospheric profiling and a Lightning Mapping Imager (LMI) — one of the few operational geostationary lightning sensors.

The National Satellite Meteorological Center (NSMC) at http://satellite.nsmc.org.cn is China Meteorological Administration's satellite data portal.

**Critical barriers**:
1. **Chinese-language portal** — NSMC portal is primarily in Chinese with limited English content
2. **Registration required** — data access requires account registration (Chinese-language forms)
3. **Domestic user preference** — international users report difficulty accessing CMA data
4. **No public cloud mirror** — unlike Himawari (AWS), FY-4 data is not openly redistributed
5. **Export control concerns** — China has data sovereignty and export control policies that may restrict foreign access

## Endpoint Analysis

**NSMC portal verified** — https://satellite.nsmc.org.cn redirects to https://satellite.nsmc.org.cn/DataPortal/en/home/index.html (English version exists but is limited).

**Portal structure**:
- Language auto-detect redirects Chinese users to `/DataPortal/cn/`, English users to `/DataPortal/en/`
- English version shows a date/time range picker but minimal product information
- No obvious download links or API documentation in English

**Probing attempts**:
```bash
$ curl -s "https://satellite.nsmc.org.cn/DataPortal/en/home/index.html" | grep -i "api\|download\|ftp"
# No results — page is minimal HTML with no API links
```

**Registration**:
- Portal shows login/register buttons
- Registration form likely requires Chinese phone number, institutional affiliation within China
- No indication of international user access pathway

**Data distribution channels** (inferred from CMA documentation):
1. **MICAPS** (Meteorological Information Comprehensive Analysis and Process System) — CMA's internal data distribution system (requires Chinese government/research institution access)
2. **CIMISS** (China Meteorological Information Sharing System) — data sharing platform (registration required, domestic focus)
3. **Satellite broadcast (CMACast)** — DVB-S satellite broadcast to ground stations in Asia-Pacific (requires receiver hardware)
4. **FTP server** — may exist but not publicly documented

**No open data initiative detected**: Unlike NOAA (which mirrors Himawari to AWS), CMA does not appear to have an equivalent open data program for international users.

## Products (if accessible)

- **FY-4A/4B AGRI Level 1** — 14-channel calibrated radiances, 0.5–4 km resolution, 15-minute full disk
- **FY-4 GIIRS** — Hyperspectral infrared sounder, atmospheric temperature/moisture profiles
- **FY-4 LMI** — Lightning detection, ~7 km resolution, continuous monitoring
- **Level 2 products** — Cloud mask, SST, winds, fog, dust, snow, fire, aerosol optical depth, etc.

**Freshness**: 15-minute full disk is competitive with other GEO satellites. Regional scans every 5 minutes.

## Why This Scores Very Low

1. **Language barrier**: Chinese-language portal, limited English documentation, registration forms in Chinese
2. **Closed access model**: No evidence of open data for international users
3. **Domestic user focus**: CMA data systems prioritize Chinese government/research institutions
4. **No cloud mirror**: FY-4 data not available via AWS/Azure/GCP
5. **Data sovereignty concerns**: China's data export regulations may restrict foreign redistribution

## Comparison to Himawari

| Feature | Himawari-9 (JMA) | FY-4B (CMA) |
|---------|------------------|-------------|
| Coverage | 140.7°E | 123°E |
| Full disk cadence | 10 min | 15 min |
| Channels | 16 | 14 |
| Open access | ✅ AWS S3, no auth | ❌ No public access |
| English docs | ✅ Extensive | ❌ Minimal |
| International users | ✅ Welcome | ⚠️ Domestic focus |

FY-4 and Himawari cover overlapping regions. **Himawari is openly accessible; FY-4 is not.**

## Verdict

**❌ Skip** — Fengyun-4 data is **not viable** for this repo due to:
- Chinese-language barrier (registration, documentation, portal)
- No public cloud storage or open API
- Domestic user preference (international access unclear or restricted)
- Data export/sovereignty concerns

**Recommendation**: Do not pursue FY-4 unless:
1. CMA launches an international open data portal with English documentation and free access (unlikely in near term)
2. FY-4 data is mirrored to a third-party open platform (e.g., through WMO data sharing, EUMETSAT, or academic collaboration)
3. A Chinese research partner can provide proxy access

**Alternative**: For coverage of China and western Pacific, use **Himawari-9** (already openly accessible via AWS).

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 2 | Covers China/western Pacific (overlaps with Himawari), 14-band AGRI, unique LMI lightning |
| Freshness | 2 | 15-minute full disk, 5-minute regional — competitive cadence |
| Openness | 0 | Chinese-language portal, registration required, no international access pathway — **severe barrier** |
| Schema Clarity | 0 | Data formats unknown (likely HDF5/GRIB2), no English docs |
| Machine-Readability | 0 | No public API or FTP, portal structure unclear |
| Repo-Fit | -1 | Overlaps with Himawari (openly available), access barriers disqualify |

**Score: 3/18** — Not viable. Language and access barriers are prohibitive. Himawari covers same region with open access.
