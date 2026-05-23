# National Center of Meteorology (NCM) - UAE Weather Network

- **Country/Region**: United Arab Emirates (Federal)
- **Endpoint**: **UNKNOWN** — requires discovery
- **Protocol**: Unknown (likely REST API)
- **Auth**: Unknown
- **Format**: Likely JSON or XML
- **Freshness**: Expected real-time (sub-hourly station observations)
- **Docs**: https://www.ncm.ae/
- **Score**: **TBD** (cannot score without endpoint)

## Overview

The National Center of Meteorology (NCM) is the UAE's federal meteorological authority, operating a comprehensive weather monitoring network across all seven emirates. NCM's infrastructure includes:

- **Automatic Weather Stations**: 86+ AWS across UAE (desert, coastal, mountain, urban locations)
- **Weather Radar**: 5 Doppler radars covering the entire country
- **Lightning Detection Network**: Real-time stroke detection
- **Upper Air Stations**: Radiosonde launches (twice daily)
- **Marine Buoys**: Offshore wave and wind monitoring
- **Air Quality Stations**: Particulate and gas monitoring (PM10, PM2.5, O3, NOx)

NCM provides services critical to aviation (Dubai, Abu Dhabi airports), offshore oil & gas operations, agriculture (cloud seeding), and public safety (fog warnings, dust storm tracking, extreme heat advisories).

**Cloud seeding operations**: NCM operates one of the world's most active cloud seeding programs (150+ missions annually) using aircraft-mounted flares to enhance rainfall. Real-time tracking of cloud seeding flights and rainfall outcomes would be a unique dataset.

## Why NCM Is a High-Priority Candidate

1. **National authority** — official source for UAE weather data
2. **Dense network** — 86 AWS, 5 radars, lightning, marine buoys, air quality
3. **Real-time operations** — NCM provides nowcasting and warnings; data must be real-time
4. **Strategic value** — UAE weather (extreme heat, fog, dust storms) has global interest
5. **Unique datasets** — cloud seeding missions, dust storm tracking, fog prediction (Dubai/Abu Dhabi airports)
6. **Multi-domain** — weather + air quality + lightning + marine in one source

## Known Challenges

**NCM website has strict WAF protection**: All attempts to access ncm.ae endpoints (including `/api/weather`, `/api/stations`, `/weather-forecast`) return HTTP 302 redirects or rejection messages. This indicates:
- The website uses aggressive bot detection (Cloudflare, Akamai, or custom WAF)
- API endpoints may require authentication or are not publicly documented
- Data may be restricted to internal systems or paid partners

**Possible data access routes**:

1. **UAE Federal Open Data Portal** (bayanat.ae): NCM may publish datasets to the federal catalog. However, bayanat.ae is slow/unreachable in testing, suggesting infrastructure issues.

2. **Dubai Pulse / Dubai Data** (data.dubai.ae, dubaipulse.gov.ae): Dubai municipality may have its own weather stations separate from NCM. These portals are also inaccessible in testing.

3. **WMO OSCAR/Surface**: The World Meteorological Organization's Observing Systems Capability Analysis and Review (OSCAR) database lists UAE weather stations with metadata. NCM may submit data to WMO's Global Telecommunication System (GTS), which feeds international weather services. However, GTS data is typically for national meteorological services, not public APIs.

4. **Third-party aggregators**: OpenWeather, Weather Underground, and other services may ingest NCM data indirectly. But these are commercial and not "open" sources.

5. **Direct contact**: Reach out to NCM's IT/data services department to request API documentation or developer access.

## Next Steps (Discovery Required)

1. **Probe bayanat.ae CKAN API** during UAE daytime hours (UTC+4):
   ```
   GET https://bayanat.ae/api/3/action/package_search?q=weather
   GET https://bayanat.ae/api/3/action/package_search?q=meteorology
   GET https://bayanat.ae/api/3/action/package_search?q=ncm
   ```

2. **Check WMO OSCAR/Surface** for NCM station identifiers:
   ```
   https://oscar.wmo.int/surface/
   ```
   Search for UAE stations, then check if NCM publishes SYNOP or BUFR bulletins.

3. **Inspect NCM mobile app** (iOS/Android): If NCM has a weather app, reverse-engineer the API endpoints it uses for live data.

4. **Search for NCM OpenAPI/Swagger docs**:
   ```
   site:ncm.ae swagger
   site:ncm.ae openapi
   site:ncm.ae api documentation
   ```

5. **Contact NCM directly**: Email open.data@ncm.ae (if it exists) or use the contact form on ncm.ae to request API access.

6. **Check for GRIB/NetCDF files**: NCM may publish model outputs (forecasts) as downloadable GRIB2 or NetCDF files on a file server (similar to NOAA, DWD). Look for patterns like:
   ```
   https://data.ncm.ae/forecasts/
   https://ftp.ncm.ae/
   ```

## If Endpoint Is Found

If NCM publishes a real-time REST API for AWS observations, this would be a **Build** candidate with a score of **16–17/18**:

| Criterion | Expected Score | Notes |
|-----------|----------------|-------|
| Freshness | 3 | Real-time station observations (sub-hourly) |
| Openness | 2–3 | TBD (may require free API key or be fully open) |
| Stability | 3 | National met service, operational system |
| Structure | 3 | JSON or XML with structured fields |
| Identifiers | 3 | Station IDs (WMO codes or NCM internal IDs) |
| Additive value | 2–3 | New region (Gulf), unique datasets (cloud seeding, UAE-specific fog/dust), but overlaps with existing weather domain |

**Key model**: Station-keyed (WMO station ID or NCM station code)

**Event families**:
- Reference: station metadata (location, elevation, sensors, commissioning date)
- Telemetry: observations (temperature, pressure, wind, humidity, precipitation, visibility, dust concentration)
- Alerts: fog warnings, dust storm warnings, extreme heat advisories

**CloudEvents subject**: `ae/weather/ncm/stations/{station_id}`

## If Endpoint Cannot Be Found

If NCM does not publish open data, document this as a **gap** in UAE coverage and note it in the final report as:

- **Status**: Skip (no public API found despite thorough search)
- **Gap type**: National meteorological service data unavailable
- **Alternative**: Rely on global sources (NOAA GFS model, satellite data) or third-party aggregators
- **Recommendation**: Advocate for NCM to publish an open data API (UAE government has strong smart city / open data initiatives; this is an obvious candidate)

**Verdict**: **Maybe** (pending endpoint discovery). NCM is a **high-priority target** for UAE discovery. Spend 2–3 hours on endpoint hunting (portal probes, mobile app reverse-engineering, WMO checks) before marking as Skip.
