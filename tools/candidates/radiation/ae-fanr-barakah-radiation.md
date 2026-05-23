# FANR - Federal Authority for Nuclear Regulation (Barakah NPP Radiation Monitoring)

- **Country/Region**: United Arab Emirates / Abu Dhabi (Al Dhafra Region)
- **Endpoint**: **UNKNOWN** — requires discovery
- **Protocol**: Unknown (likely REST API or data portal)
- **Auth**: Unknown
- **Format**: Likely JSON, XML, or CSV
- **Freshness**: Expected real-time (continuous gamma dose rate monitoring)
- **Docs**: https://www.fanr.gov.ae/
- **Score**: **TBD** (cannot score without endpoint)

## Overview

The **Federal Authority for Nuclear Regulation (FANR)** is the UAE's nuclear safety regulator, responsible for oversight of the **Barakah Nuclear Power Plant** — the first commercial nuclear power plant in the Arab world.

**Barakah NPP** (operated by Emirates Nuclear Energy Corporation, ENEC):
- Location: Al Dhafra, Western Region, Abu Dhabi (53 km west of Ruwais, 250 km from Dubai)
- Units: 4 × APR1400 reactors (Korean design), 1,400 MW each
- Status: Units 1–3 operational (2020–2023), Unit 4 under commissioning (2024)
- Total capacity: 5,600 MW (25% of UAE electricity demand)

**Radiation monitoring network**: FANR operates (or mandates ENEC to operate) an **Environmental Radiation Monitoring Network** around Barakah NPP. This typically includes:
- **Gamma dose rate stations**: 10–20 stations within 30 km of the plant, measuring ambient gamma radiation (nSv/h or µSv/h)
- **Air samplers**: Particulate and iodine monitoring
- **Water sampling**: Seawater intake and discharge (Barakah uses seawater cooling)
- **Soil and vegetation**: Periodic sampling for radioisotopes
- **Meteorological data**: Wind speed, direction, temperature (for dispersion modeling)

**Regulatory requirement**: Nuclear power plants worldwide are required to publish real-time environmental monitoring data for public transparency. Examples:
- **Germany**: BfS ODL network (1,800 stations, open API)
- **France**: IRSN's Téléray network (open data)
- **Japan**: NRA post-Fukushima monitoring (JSON feeds)
- **USA**: EPA RadNet (near all US NPPs)

**UAE is likely to follow this international norm** given:
- IAEA oversight and safety standards
- UAE's commitment to transparency (Barakah was designed to meet IAEA safety standards)
- Public concern / media attention (Barakah is 200 km from major population centers)

## Endpoint Discovery Required

**FANR website** (https://www.fanr.gov.ae/) exists but does not prominently advertise environmental monitoring data. Possible access routes:

1. **Check FANR publications section** for monitoring reports:
   ```
   site:fanr.gov.ae environmental monitoring
   site:fanr.gov.ae radiation
   site:fanr.gov.ae barakah
   ```

   FANR publishes annual reports; these may cite a monitoring dashboard or data portal.

2. **Check ENEC (Emirates Nuclear Energy Corporation)** website:
   ```
   https://www.enec.gov.ae/
   site:enec.gov.ae monitoring
   site:enec.gov.ae environmental data
   ```

   ENEC may host the public-facing monitoring portal.

3. **Search for UAE open data portals** (bayanat.ae) for radiation monitoring datasets.

4. **Check international registries**:
   - **EURDEP** (European Radiological Data Exchange Platform): Only covers Europe + some neighboring regions; UAE would not be included.
   - **IAEA IRMIS** (Integrated Regulatory Management Information System): IAEA may have UAE data but likely not public-facing.
   - **Safecast** (citizen radiation network): Check if any Safecast users have deployed sensors near Barakah.

5. **Mobile app**: FANR or ENEC may have a mobile app for public information that includes live monitoring data. Check iOS/Android app stores:
   ```
   Search: "FANR UAE" or "Barakah monitoring" or "ENEC"
   ```

6. **Media / Press releases**: Search UAE news outlets for mentions of a radiation monitoring portal launch.

7. **Direct contact**: Email FANR's public affairs or technical support to request access to environmental monitoring data.

## If Endpoint Is Found and Public

If FANR/ENEC publish real-time gamma dose rate data, this would be a **Build** candidate with a score of **15–17/18**:

| Criterion | Expected Score | Notes |
|-----------|----------------|-------|
| Freshness | 3 | Real-time gamma dose rate (continuous, 1-minute or 10-minute averages typical) |
| Openness | 2–3 | TBD (nuclear data is often open for transparency, but may require registration) |
| Stability | 3 | Nuclear regulatory agency; data systems are mission-critical |
| Structure | 3 | Likely JSON, XML, or CSV (structured time series) |
| Identifiers | 3 | Station IDs (FANR/ENEC internal codes or GPS coordinates) |
| Additive value | 3 | **New domain** for repo (radiation monitoring), **new region** (Gulf), unique dataset (first Arab NPP) |

**Key model**: Station-keyed (radiation monitoring station ID)

**Event families**:
- Reference: station metadata (location, sensor type, measurement range, commissioning date)
- Telemetry: gamma dose rate (nSv/h, timestamp, status flags)
- Alerts: radiation anomaly alarms (if any — extremely rare for NPPs in normal operation)

**CloudEvents subject**: `ae/radiation/fanr/stations/{station_id}` or `ae/radiation/barakah/{station_id}`

**Repo sibling**: The repo does not currently have a radiation monitoring source. This would establish the **radiation monitoring domain** in the repo, with Barakah as the reference implementation. Could later expand to other nuclear facilities worldwide (France, Germany, Japan, USA).

## If Endpoint Cannot Be Found

If FANR/ENEC do not publish open data:

- **Status**: Skip (no public API found, or data is restricted)
- **Gap type**: Nuclear facility environmental monitoring not publicly accessible
- **Alternative**: 
  - Safecast (citizen network — likely sparse coverage near Barakah)
  - IAEA reports (aggregated, not real-time)
- **Recommendation**: 
  - Reach out to FANR/ENEC to request developer access
  - Advocate for open data publication (citing German BfS, French IRSN, Japanese NRA as models)
  - Note that UAE's commitments to IAEA transparency should include environmental monitoring

**Political / safety context**: Barakah NPP has faced scrutiny from neighboring countries (Qatar, Iran) and environmental groups. Publishing real-time radiation data would be a confidence-building measure and demonstrate compliance with international safety standards.

**Verdict**: **Maybe** (pending endpoint discovery). Barakah radiation monitoring is a **strategic candidate** because:
- Unique dataset (first Arab nuclear plant, Gulf region)
- Establishes new domain (radiation monitoring) in the repo
- High public interest (nuclear safety is globally newsworthy)
- Technically straightforward (station-keyed numeric time series, same pattern as hydrology/weather)

Spend time searching FANR, ENEC, and UAE data portals. If no endpoint is found, reach out directly to FANR before marking as Skip. If they publish data but gate it behind registration, assess whether the registration process is simple enough to qualify as "open" (many nuclear agencies allow free registration for research/educational use).
