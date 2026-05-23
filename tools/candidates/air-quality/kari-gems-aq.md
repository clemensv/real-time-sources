# KARI GEO-KOMPSAT-2B GEMS Air Quality (NO2/SO2/Aerosol)

- **Country/Region**: South Korea / East Asia (5°S-45°N, 75°E-145°E)
- **Endpoint**: https://nesc.nier.go.kr (National Environmental Satellite Center, registration required)
- **Protocol**: Web portal download, FTP (restricted)
- **Auth**: Registration required (Korean institutions preferred)
- **Format**: NetCDF4 (Level 2/3)
- **Freshness**: Hourly (Level 3), 30-minute (Level 2 during daytime)
- **Docs**: https://nesc.nier.go.kr/en/html/satellite/doc/doc.do
- **Score**: 8/18

## Overview

GEO-KOMPSAT-2B (GK-2B), launched in 2020 and stationed at 128.2°E, carries the Geostationary Environment Monitoring Spectrometer (GEMS) — the world's **first geostationary air quality monitoring instrument**. GEMS observes nitrogen dioxide (NO2), sulfur dioxide (SO2), formaldehyde (HCHO), ozone (O3), and aerosol optical depth (AOD) over East Asia with hourly temporal resolution during daytime.

This is a **landmark mission**: GEMS provides continuous air quality monitoring from geostationary orbit, complementing ground-based networks. It tracks transboundary air pollution from China to Korea/Japan, monitors industrial emissions, and supports air quality forecasting.

GK-2B also carries GOCI-II (Geostationary Ocean Color Imager II), providing 10-channel ocean color imagery every hour (separate from GEMS).

**Critical barrier**: Data distribution is primarily through the Korean National Institute of Environmental Research (NIER) National Environmental Satellite Center (NESC) portal at https://nesc.nier.go.kr, which requires registration. The registration process **favors Korean institutions** and has been reported as difficult for international users.

## Endpoint Analysis

**NESC portal verified** — https://nesc.nier.go.kr/en/html/main/main.do is the official GEMS data portal (English version available).

**Data access**:
1. **Web portal download** — search by product/time, requires login
2. **FTP server** — `ftp.nesc.nier.go.kr` (login required, credentials provided after registration approval)
3. **No public REST API** — no documented HTTP API for programmatic access

**Registration process** (based on documentation):
- Submit registration form with institutional affiliation
- Wait for approval (timeline unclear, anecdotal reports suggest 1-2 weeks or longer)
- **Preference for Korean research institutions** — international users may face additional scrutiny or delays
- No indication of API key or automated access after registration

**Products available**:
- **GEMS Level 2** — NO2, SO2, HCHO, O3, AOD, UVAI (UV Aerosol Index) — 30-minute daytime observations, 7×7 km² nadir resolution
- **GEMS Level 3** — hourly gridded (0.05° or ~5 km), daily, monthly averages
- **GOCI-II Level 2** — Chlorophyll-a, TSS, CDOM, Kd, Rrs — hourly ocean color
- **GOCI-II Level 3** — daily/monthly ocean color composites

**File naming** (example from user guide):
```
gk2b_gems_l2_no2_fd_20260115_0300_le1c_v1.0.nc
  ^     ^    ^   ^   ^  ^           ^      ^
  sat  instr lv prod area YYYYMMDDhhmm proc version
```

**Freshness**: GEMS Level 2 products are typically available 3-6 hours after observation. Level 3 hourly grids may have similar latency. This is slower than meteorological satellites (Himawari publishes within 10-15 min).

**Volume estimate**: GEMS observes ~8 hours per day (daylight over East Asia). With 6 products (NO2, SO2, HCHO, O3, AOD, UVAI) × 16 half-hour slots × hourly L3 grids = ~100 files/day. Each file ~50-200 MB (NetCDF4). Manageable but requires SFTP/FTP access.

## Schema / Sample Metadata

GEMS products are NetCDF4 following CF-1.7 conventions. Example metadata (NO2):

```json
{
  "satellite": "GEO-KOMPSAT-2B",
  "instrument": "GEMS",
  "processing_level": "L2",
  "product": "NO2",
  "observation_area": "FD",
  "observation_time": "2026-01-15T03:00:00Z",
  "spatial_resolution_km": 7.0,
  "vertical_column_no2_trop": "tropospheric NO2 column density (molec/cm²)",
  "quality_flag": "0=good, 1=suspect, 2=bad",
  "format": "NetCDF4-classic"
}
```

**Stable identifiers**: `{product}/{observation_time}` is a natural key. File naming is deterministic.

**CloudEvents subject template**: `gk2b/gems/{product}/fd/{timestamp}`  
**Kafka key template**: `gk2b-gems-{product}-{timestamp}`

## Why This is Valuable

1. **World-first geostationary air quality**: GEMS is the pioneering mission for continuous air quality monitoring from GEO orbit. Scientifically and politically significant.
2. **Hourly daytime coverage**: Unlike polar-orbiting sensors (1-2 overpasses/day), GEMS observes every hour during daylight, enabling pollution event tracking (e.g., power plant plumes, traffic peaks, wildfire smoke).
3. **Transboundary pollution monitoring**: GEMS tracks air pollution transport from China to Korea/Japan, critical for policy and public health.
4. **Complements ground networks**: GEMS fills spatial gaps between ground-based air quality monitors, especially over oceans and remote areas.
5. **Operational use**: Korean Ministry of Environment uses GEMS data for air quality forecasting and public alerts.

## Limitations

1. **Registration required, opaque process**: Free but not open — registration approval timeline unclear, Korean institutions favored. **Major openness penalty.**
2. **No public API**: FTP/web portal only. No REST API, no OGC services (WMS/WCS), no OpenDAP.
3. **Daytime-only**: UV/visible spectrometer requires sunlight — no nighttime observations. ~8 hours/day coverage over East Asia.
4. **Latency**: 3-6 hours from observation to product availability is slower than meteorological satellites.
5. **NetCDF4 format**: Not JSON. Requires `netCDF4` library for parsing.
6. **FTP transport**: FTP (not SFTP) mentioned in docs — FTP is deprecated/insecure. May have switched to SFTP; needs verification.
7. **Limited geographic scope**: East Asia only (5°S-45°N, 75°E-145°E). Does not cover Europe, Americas, Africa.

## Verdict

**⚠️ Conditional Recommend** — GEMS is scientifically significant (world-first geostationary air quality) and fills a unique niche. However, the **registration barrier is substantial** (approval process, Korean institutional preference, no API). This lowers the openness score significantly (1/3).

**Feasibility depends on registration success**: If registration is approved and FTP/SFTP credentials are provided, the bridge is feasible. If registration is denied or indefinitely delayed, this source is inaccessible.

**Alternative path**: Check if any GEMS data is redistributed through:
1. NASA ARSET or LAADS DAAC (NASA sometimes mirrors international satellite data)
2. EUMETSAT (EU/Korea data sharing agreements)
3. Korean open data portal (data.go.kr) — unlikely for raw NetCDF, but worth checking

**Best scope if accessible**: GEMS Level 3 hourly NO2 and AOD (most policy-relevant for air quality). Emit one event per product per hour during daytime (~16 events/day total).

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3 | World-first geostationary air quality, hourly NO2/SO2/AOD, transboundary pollution tracking |
| Freshness | 2 | Hourly daytime observations, but 3-6 hour latency to product publication |
| Openness | 1 | Registration required, approval opaque, Korean institutions preferred — major barrier |
| Schema Clarity | 2 | NetCDF4/CF conventions, documented schema, but binary not JSON |
| Machine-Readability | 1 | FTP download only, no REST API, NetCDF4 parsing required |
| Repo-Fit | -1 | Unique domain (geostationary air quality), but access barriers and FTP transport complicate |

**Score: 8/18** — High scientific value, but registration barrier and lack of public API significantly reduce feasibility. Recommend attempting registration, but have a fallback if access is denied.
