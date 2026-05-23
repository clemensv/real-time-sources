# NASA CYGNSS (Cyclone Global Navigation Satellite System)

- **Country/Region**: Tropical oceans (38°S to 38°N)
- **Endpoint**: `https://podaac-tools.jpl.nasa.gov/drive/files/allData/cygnss/` (PO.DAAC archive)
- **Protocol**: HTTPS file download (NetCDF-4)
- **Auth**: Earthdata Login (free registration)
- **Format**: NetCDF-4
- **Freshness**: 6–12 hours from observation (NRT Level 1)
- **Docs**: https://podaac.jpl.nasa.gov/CYGNSS, https://cygnss.engin.umich.edu/
- **Score**: 10/18

## Overview

NASA's Cyclone Global Navigation Satellite System (CYGNSS) is a constellation of eight small satellites that measure ocean surface wind speed in tropical cyclones using GPS signal reflections (GNSS-Reflectometry or GNSS-R). Launched in 2016, CYGNSS provides frequent sampling of tropical ocean regions (38°S to 38°N) with median revisit time of ~3 hours at any location — far more frequent than polar-orbiting satellites.

CYGNSS specializes in penetrating the heavy rain of tropical cyclones (hurricanes, typhoons), where traditional scatterometers (microwave radar) fail due to rain attenuation. The constellation measures ocean surface wind speed at 25 km spatial resolution, critical for hurricane intensity estimation, rapid intensification detection, and storm surge forecasting.

Data products include Level 1 (calibrated signal measurements), Level 2 (ocean wind speed and mean square slope), and Level 3 (gridded daily/3-day wind fields). Near real-time (NRT) Level 1 products are delivered within 6–12 hours; Science Data Record (SDR) products arrive weeks later with final calibration.

## Endpoint Analysis

**PO.DAAC data directory (CYGNSS L1 NRT):**
```
https://podaac-tools.jpl.nasa.gov/drive/files/allData/cygnss/L1/v3.1/
```

Files follow naming convention:
```
cyg01.ddmi.s20240115-000000-e20240115-235959.l1.power-brcs.a31.d32.nc
 ^              ^                                ^
sat ID         date range                      L1 product type
```

**Product types:**
- `L1 power-brcs` — Bistatic Radar Cross Section (BRCS), GPS signal power
- `L2 wind-speed` — Ocean surface wind speed (m/s), 25 km resolution
- `L3 gridded-wind` — Daily gridded wind fields, 0.2° × 0.2° resolution

**Sample NetCDF structure (L2 wind-speed):**
- `wind_speed` — ocean surface wind speed (m/s), 0–50 m/s range
- `lat`, `lon` — specular point (GPS signal reflection location)
- `sample_time` — observation timestamp (seconds since 2000-01-01)
- `wind_speed_uncertainty` — retrieval uncertainty (m/s)
- `quality_flags` — QA flags (0=good, >0=suspect/failed)

**Earthdata Login auth:**
```bash
curl -n -c cookies.txt -b cookies.txt \
  "https://podaac-tools.jpl.nasa.gov/drive/files/allData/cygnss/L1/v3.1/2024/015/cyg01.ddmi.s20240115-000000-e20240115-235959.l1.power-brcs.a31.d32.nc"
```

**Coverage:**
- Latitude: 38°S to 38°N (tropical/subtropical oceans)
- Median revisit time: ~3 hours at any tropical ocean location
- Constellation: 8 satellites, each in low-inclination orbit (35°)
- Spatial resolution: 25 km (wind speed), ~5 km (radar cross section)

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 6–12 hour latency for L1 NRT — faster than most satellite ocean products but not sub-hourly |
| Openness | 2 | Free Earthdata Login required, instant registration |
| Stability | 2 | NASA operational mission since 2016, but small-satellite constellation has had spacecraft failures (CyGNSS-2 degraded) |
| Structure | 2 | NetCDF-4 with CF conventions, well-documented variables |
| Identifiers | 1 | Specular point (lat/lon + timestamp) is unique, but no persistent ocean cell IDs |
| Richness | 1 | Ocean wind speed + uncertainty + QA flags; specialized for tropical cyclones |

**CYGNSS excels for tropical cyclone inner-core wind sampling.** The constellation's frequent revisit (~3 hours median) and rain-penetrating capability (GPS reflections are not attenuated by heavy rain like microwave radar) make it the best satellite source for hurricane intensity estimation. Operational forecasters (NOAA National Hurricane Center) use CYGNSS wind data to detect rapid intensification.

**Niche application: tropical cyclones.** CYGNSS is designed for hurricanes, typhoons, and tropical storms. Outside storm environments, the data adds value for ocean surface roughness monitoring, but it's not a general-purpose ocean wind product. For global ocean winds, use scatterometers (ASCAT, ScatSat) or SAR.

**6–12 hour latency is acceptable for cyclone forecasting** (hurricane track/intensity forecasts run every 6 hours), but it's not fast enough for real-time nowcasting (ship routing, offshore operations).

## Limitations

- **6–12 hour latency** for L1 NRT products. L2 wind-speed arrives 12–24 hours later. Too slow for sub-hourly event streaming.
- **Tropical oceans only** (38°S to 38°N). No mid-latitude or polar ocean coverage. No land observations.
- **Specialized for tropical cyclones.** Outside storm environments, CYGNSS wind retrievals have higher uncertainty (±2 m/s in calm conditions vs. ±1 m/s in strong winds). The system is optimized for 10–40 m/s winds (tropical storm to Category 2 hurricane).
- **File-based delivery (NetCDF).** Each satellite-day is a ~200 MB file. Bridge must poll directory, download, parse NetCDF, extract specular points. Heavier than JSON REST APIs.
- **Earthdata Login required.** Same auth complexity as other NASA EOSDIS products.
- **Constellation degradation.** One spacecraft (CyGNSS-2) has degraded performance; median revisit time has increased from original ~2.8 hours to ~3.2 hours. If more spacecraft fail, mission value degrades.

**CYGNSS is valuable but niche.** If the repo prioritizes tropical cyclone monitoring or ocean wind fields, CYGNSS is a strong candidate. For general-purpose NRT event bridging, it's lower priority than multi-domain sources (EONET, FIRMS).

## Final Verdict

**Verdict**: ⚠️ **Maybe**

CYGNSS provides unique tropical cyclone inner-core wind observations with ~3 hour revisit time and rain-penetrating capability. The 6–12 hour NRT latency is acceptable for operational hurricane forecasting. However, the tropical-only coverage (38°S to 38°N), specialized use case (cyclones), and file-based NetCDF delivery make it a niche bridge.

**Recommended if pursued:**
- Tropical cyclone monitoring bridge (trigger on active storms, emit wind-speed observations for storm-affected regions)
- Pair with NOAA NHC storm tracks (ATCF format) to filter CYGNSS data to active cyclone basins
- Use Level 2 wind-speed product (gridded to 25 km) for stable keying
- Poll every 6–12 hours for new granules

**If building ocean wind bridges, prioritize:**
1. **ASCAT** (MetOp-A/B/C, ESA/EUMETSAT, global ocean, 12.5 km, daily, NRT) — broader coverage, operational since 2006
2. **ScatSat-1** (ISRO, global ocean, 25 km, daily, NRT, ended 2021) — if historical bridge
3. **CYGNSS** (NASA, tropical oceans, 25 km, ~3 hour revisit, 6–12 hour latency, cyclone-optimized) — niche tropical cyclone application

**Bridge type:** Poller (HTTPS file listing + NetCDF download/parse, 6–12 hour interval)

**Keying:** Grid cell (lat/lon at 0.2° for L3 gridded, or specular point lat/lon for L2)

**Reference data:** None (specular points are self-contained; L3 gridding is fixed)

**Pairs well with:** NOAA NHC storm tracks (filter to active cyclones), GOES-16/17 tropical imagery (storm structure context), NOAA buoy observations (validation)

**Not suitable for:**
- General-purpose ocean wind monitoring (use scatterometers instead)
- Sub-hourly event streaming (6–12 hour latency)
- Mid-latitude or polar oceans (coverage limited to 38°S–38°N)
