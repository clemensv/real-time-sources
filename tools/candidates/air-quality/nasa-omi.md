# NASA OMI (Ozone Monitoring Instrument) NRT Air Quality

- **Country/Region**: Global
- **Endpoint**: `https://aura.gesdisc.eosdis.nasa.gov/data/Aura_OMI_Level2/` (GES DISC archive)
- **Protocol**: HTTPS file download (HDF-EOS5)
- **Auth**: Earthdata Login (free registration)
- **Format**: HDF-EOS5
- **Freshness**: 24–48 hours from satellite overpass (NRT variant)
- **Docs**: https://disc.gsfc.nasa.gov/datasets?keywords=OMI&page=1, https://aura.gsfc.nasa.gov/omi.html
- **Score**: 11/18

## Overview

The Ozone Monitoring Instrument (OMI) aboard NASA's Aura satellite (launched 2004) measures atmospheric trace gases including ozone (O₃), nitrogen dioxide (NO₂), sulfur dioxide (SO₂), formaldehyde (HCHO), and aerosols. OMI is a nadir-viewing UV/visible spectrometer with 13×24 km spatial resolution at nadir (degraded at swath edges to ~28×150 km due to row anomaly).

Aura is a polar-orbiting satellite with daily global coverage (~14 orbits/day). OMI products include total column ozone (for UV index forecasts), tropospheric NO₂ (air pollution from traffic/industry), SO₂ (volcanic emissions, coal power plants), and aerosol optical depth. Near real-time (NRT) products are delivered within 24–48 hours; Standard Processing products arrive weeks later with final calibration.

OMI data is used operationally by NOAA Air Quality forecasts, EPA AirNow, volcanic ash advisory centers (SO₂ plume tracking), and international air quality monitoring agencies. After 20 years in orbit, OMI remains NASA's longest-running atmospheric chemistry mission.

## Endpoint Analysis

**GES DISC data directory (OMI NO₂ tropospheric column NRT):**
```
https://aura.gesdisc.eosdis.nasa.gov/data/Aura_OMI_Level2/OMNO2.003/
```

Files follow naming convention:
```
OMI-Aura_L2-OMNO2_2024m0115t0853-o00001_v003-2024m0116t1234.he5
         ^          ^           ^        ^
        L2        date       orbit   version/processing date
```

**Product codes (NRT variants):**
- `OMNO2` — Nitrogen Dioxide (tropospheric & stratospheric column), Level 2, swath
- `OMSO2` — Sulfur Dioxide (volcanic & anthropogenic), Level 2, swath
- `OMHCHO` — Formaldehyde, Level 2, swath
- `OMAERUV` — Aerosol Optical Depth and Single Scattering Albedo, Level 2, swath
- `OMTO3` — Total Column Ozone, Level 2, swath

**Sample HDF-EOS5 structure (OMNO2):**
- `HDFEOS/SWATHS/ColumnAmountNO2/Data Fields/ColumnAmountNO2Trop` — tropospheric NO₂ column (molecules/cm²)
- `HDFEOS/SWATHS/ColumnAmountNO2/Data Fields/ColumnAmountNO2TropStd` — retrieval uncertainty
- `HDFEOS/SWATHS/ColumnAmountNO2/Geolocation Fields/Latitude`, `Longitude` — pixel centers
- `HDFEOS/SWATHS/ColumnAmountNO2/Geolocation Fields/Time` — observation time (TAI93)
- Cloud fraction, solar zenith angle, terrain height, quality flags

**Earthdata Login auth:**
```bash
curl -n -c cookies.txt -b cookies.txt \
  "https://aura.gesdisc.eosdis.nasa.gov/data/Aura_OMI_Level2/OMNO2.003/2024/OMI-Aura_L2-OMNO2_2024m0115t0853-o00001_v003-2024m0116t1234.he5"
```

**Coverage:**
- Spatial resolution: 13×24 km at nadir (best case), 28×150 km at swath edge (after row anomaly)
- Swath width: 2600 km (global coverage in ~14 orbits/day)
- Temporal: Daily global coverage (one overpass per location per day, around 1:30 PM local time)

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 24–48 hour latency for NRT products — daily but not sub-daily |
| Openness | 2 | Free Earthdata Login required, instant registration |
| Stability | 3 | NASA operational mission since 2004, 20+ year data record |
| Structure | 2 | HDF-EOS5 with documented structure, but not JSON/REST |
| Identifiers | 1 | Swath pixels have lat/lon but no persistent IDs; daily global coverage but variable geometry |
| Richness | 1 | Trace gas columns + uncertainty + QA flags; single daily overpass per location |

**OMI is NASA's workhorse atmospheric chemistry mission.** The 20-year data record (2004–present) is unmatched for long-term air quality trend analysis and ozone layer monitoring. Daily global coverage makes it suitable for operational air quality forecasting (EPA AirNow uses OMI NO₂ for pollution transport modeling).

**Daily overpass cadence is too coarse for sub-daily event tracking.** Unlike TEMPO (hourly North America coverage), OMI passes over each location once per day at ~1:30 PM local time. You cannot capture diurnal cycles (rush-hour pollution peaks, evening industrial emissions) or rapid pollution events (wildfire smoke injections, volcanic plumes within hours). OMI is designed for daily-to-seasonal monitoring, not real-time alerting.

**Superseded by TEMPO (North America) and TROPOMI (global).** ESA's TROPOMI instrument (Sentinel-5P, launched 2017) provides similar trace gas measurements at finer resolution (7×7 km vs. OMI's 13×24 km) and with improved sensitivity. TEMPO (launched 2023) provides hourly North America coverage vs. OMI's single daily snapshot. For new NRT bridges, TEMPO and TROPOMI are higher priority than OMI.

**OMI remains valuable for:**
- Long-term trend analysis (20-year record vs. TEMPO's 1 year, TROPOMI's 7 years)
- Volcanic SO₂ tracking (OMI SO₂ algorithm is mature and operationally trusted)
- Regions outside TEMPO's North America field of regard

## Limitations

- **24–48 hour latency** for NRT products — acceptable for daily air quality forecasts but too slow for same-day alerts.
- **Single daily overpass** per location (~1:30 PM local time). Cannot capture diurnal cycles or sub-daily events.
- **Row anomaly degrades spatial resolution.** Since 2008, several OMI detector rows have failed, creating gaps in spatial coverage. Affected pixels have coarser resolution (28×150 km) and lower quality. Quality flags identify these pixels, but they reduce usable data coverage by ~30%.
- **Swath data has variable geometry.** Each orbit's pixels are at different lat/lon locations. Gridding to a fixed grid (e.g., 0.25° × 0.25°) is needed for stable keying.
- **File-based delivery (HDF-EOS5).** Each orbit is a ~100 MB file. Bridge must poll directory, download, parse HDF-EOS5, extract swath pixels. Heavier than JSON REST APIs.
- **Earthdata Login required.** Same as GPM IMERG, SMAP, TEMPO — free but adds auth complexity.

**OMI is solid but dated.** For new NRT air quality bridges, prioritize TEMPO (hourly, North America) or TROPOMI (daily, global, higher resolution).

## Final Verdict

**Verdict**: ⚠️ **Maybe**

OMI is a proven operational air quality product with 20 years of heritage, but it has been superseded by TEMPO (hourly North America) and TROPOMI (daily global, finer resolution). The 24–48 hour NRT latency and single daily overpass make it less attractive for real-time event streaming compared to TEMPO's ~2 hour latency and hourly cadence.

**Recommended if pursued:**
- Regional bridge for areas outside TEMPO coverage (Europe, Asia, South America, Africa)
- Focus on volcanic SO₂ tracking (OMI SO₂ algorithm is well-validated for ash aviation hazard)
- Long-term trend analysis (combine OMI's 20-year record with TEMPO/TROPOMI's recent data)
- Daily gridded products (regrid swath to 0.25° or 0.5° fixed grid for stable keying)

**If building a NASA air quality bridge:**
1. **TEMPO** (hourly North America, ~2 hour latency) — highest priority
2. **TROPOMI** (daily global, 7×7 km, ~3 hour latency, ESA but NASA partnership) — second priority
3. **OMI** (daily global, 13×24 km, 24-hour latency, 20-year record) — third priority, niche use cases

**Bridge type:** Poller (HTTPS file listing + HDF-EOS5 download/parse, daily interval)

**Keying:** Grid cell (regrid swath to fixed lat/lon grid at 0.25° or 0.5°)

**Reference data:** None (swath pixels are self-contained; gridding algorithm is deterministic)

**Pairs well with:** EPA AirNow ground stations (surface concentration), TEMPO (hourly for North America overlap), volcanic ash advisories (OMI SO₂ for plume tracking)
