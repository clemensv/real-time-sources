# KARI GEO-KOMPSAT-2A GOCI-II Ocean Color

- **Country/Region**: South Korea / East Asia, Northwest Pacific
- **Endpoint**: http://kosc.kiost.ac.kr (Korea Ocean Satellite Center)
- **Protocol**: Web portal download (registration required)
- **Auth**: Registration required
- **Format**: NetCDF4 (likely)
- **Freshness**: Hourly during daytime
- **Docs**: http://kosc.kiost.ac.kr/index.nm
- **Score**: 7/18

## Overview

GEO-KOMPSAT-2A (GK-2A) carries the Geostationary Ocean Color Imager II (GOCI-II), the **world's second geostationary ocean color sensor** (after GOCI-1 on COMS). GOCI-II observes the Northwest Pacific and Yellow/East China Seas with **hourly observations during daylight** — a unique capability for tracking algal blooms, sediment plumes, and coastal water quality changes.

GOCI-II has 13 spectral bands (visible and near-infrared) at 250 m spatial resolution, covering a 2500 × 2500 km area centered on Korea.

**Why this matters**: Most ocean color sensors are polar-orbiting (1-2 passes per day). GOCI-II's hourly cadence enables **diurnal cycle studies** — tracking how phytoplankton, turbidity, and harmful algal blooms evolve hour-by-hour. Critical for coastal management in one of the world's most productive (and polluted) ocean regions.

**Data distribution**: Korea Ocean Satellite Center (KOSC) at Korea Institute of Ocean Science & Technology (KIOST) distributes GOCI-II data via web portal.

## Endpoint Analysis

**KOSC portal** — http://kosc.kiost.ac.kr/index.nm is the official GOCI-II data portal.

**Portal status**: The site loads but appears to be Korean-language primary with limited English content. Registration pathway for international users is unclear.

**Data access methods** (inferred from GOCI-1 experience):
1. **Web portal** — search by date/product, download after login
2. **FTP server** — may exist for bulk download (credentials after registration approval)
3. **NASA Ocean Color** — GOCI-1 data was mirrored to NASA OBPG (Ocean Biology Processing Group); unclear if GOCI-II is similarly distributed

**Products available**:
- **L1B** — Calibrated top-of-atmosphere radiances (13 bands)
- **L2** — Chlorophyll-a, TSS, CDOM, Kd, Rrs (remote sensing reflectance), fluorescence line height (FLH)
- **L3** — Hourly, daily, monthly composites

**Freshness**: Hourly observations during daylight (~8-10 hours per day depending on season). Latency from observation to product availability is unclear but likely 1-3 hours (standard for ocean color processing).

**Volume estimate**: ~8-10 observations per day × multiple products = ~80-100 files/day for L2 hourly. L3 daily composites reduce to ~5-10 files/day.

## Registration Barrier

**Same issue as GK-2A/AMI**: Korean government data portals often have:
- Registration forms in Korean
- Preference for domestic institutions
- Approval delays for international users
- Limited English documentation

**GOCI-1 precedent**: The original GOCI (on COMS satellite) data was eventually mirrored to **NASA Ocean Color** (https://oceancolor.gsfc.nasa.gov), providing open access. If GOCI-II follows the same path, it would become freely accessible. However, as of 2026, GOCI-II on NASA Ocean Color is **unclear**.

## Why This is Valuable (If Accessible)

1. **Hourly ocean color**: Unique geostationary capability for diurnal cycle studies
2. **Coastal water quality**: Yellow Sea and East China Sea are ecologically/economically critical but heavily impacted by pollution and eutrophication
3. **Harmful algal bloom tracking**: Hourly updates enable early detection and forecasting
4. **Complements polar-orbiting sensors**: GOCI-II fills temporal gaps between GCOM-C, Sentinel-3, and MODIS/VIIRS passes

## Limitations

1. **Registration required**: Korean portal, domestic user preference
2. **Limited spatial coverage**: 2500 × 2500 km centered on Korea (does not cover global oceans like polar-orbiting sensors)
3. **Daytime-only**: Optical sensor requires sunlight (~8-10 hours/day)
4. **Uncertain NASA mirror**: If GOCI-II is not mirrored to NASA Ocean Color, accessibility is limited to KOSC portal

## Verdict

**⚠️ Conditional Recommend** — GOCI-II is scientifically unique (only geostationary ocean color sensor actively operating) and valuable for coastal ocean monitoring. **However, data accessibility is uncertain**.

**Recommended action**:
1. **Check NASA Ocean Color** — verify if GOCI-II data is available at https://oceancolor.gsfc.nasa.gov (if yes, this becomes a strong candidate with open access)
2. **Attempt KOSC registration** — if NASA mirror is not available, try registering at KOSC portal (expect Korean-language forms and potential delays)
3. **Monitor EUMETSAT** — EU/Korea data sharing agreements may lead to GOCI-II distribution through EUMETSAT portals

**If accessible via NASA Ocean Color**: Score increases to **12/18** (openness improves from 1 to 3).

**If only via KOSC portal**: Score remains **7/18** due to registration barriers.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3 | Unique hourly geostationary ocean color, harmful algal bloom tracking, diurnal cycles |
| Freshness | 3 | Hourly daytime observations — world-class temporal resolution |
| Openness | 1 | Registration required at Korean portal, international access unclear (unless NASA mirror exists) |
| Schema Clarity | 2 | NetCDF4 likely (standard for ocean color), but KOSC docs limited |
| Machine-Readability | 1 | Portal download, FTP possible, no public REST API |
| Repo-Fit | -3 | Limited coverage (Korea-centric), access barriers — **conditional fit** |

**Score: 7/18** — High scientific value, but access barriers reduce viability. Strongly recommend checking **NASA Ocean Color mirror first** before attempting Korean portal registration.
