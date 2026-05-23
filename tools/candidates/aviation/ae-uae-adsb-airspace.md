# ADS-B Flight Tracking - UAE Airspace (Dubai, Abu Dhabi, Sharjah Airports)

- **Country/Region**: United Arab Emirates (Dubai DXB/DWC, Abu Dhabi AUH, Sharjah SHJ, Fujairah FUJ, Ras Al Khaimah RAK)
- **Endpoint**: **Global coverage via ADSBexchange, OpenSky Network, local receivers**
- **Protocol**: BEAST binary (Mode-S), SBS BaseStation, REST API
- **Auth**: Varies (ADSBexchange: API key; OpenSky: free with rate limits; local: no auth)
- **Format**: JSON (APIs), binary BEAST (raw)
- **Freshness**: Real-time (ADS-B positions broadcast every 1–2 seconds)
- **Docs**: 
  - ADSBexchange: https://www.adsbexchange.com/data/
  - OpenSky Network: https://opensky-network.org/apidoc/
  - Local receiver: dump1090 (open source)
- **Score**: **Overlap with global sources** (ADSBexchange, OpenSky cover UAE)

## Overview

The UAE is a **major aviation hub**:

### Airports
- **Dubai International (DXB)**: World's busiest airport for international passengers (88M/year)
- **Dubai World Central (DWC) / Al Maktoum International**: Cargo + expanding passenger terminal (future mega-hub)
- **Abu Dhabi International (AUH)**: 23M passengers/year, hub for Etihad Airways
- **Sharjah International (SHJ)**: 15M passengers/year, low-cost carrier hub (Air Arabia)
- **Fujairah (FUJ)**, **Ras Al Khaimah (RAK)**: Regional airports

### Airspace
- UAE Flight Information Region (FIR) managed by UAE General Civil Aviation Authority (GCAA)
- High-density airspace: Dubai/Abu Dhabi approach sectors handle 1,000+ movements/day
- Strategic location: Major Europe ↔ Asia route crossings

### ADS-B Coverage
- All UAE airports require ADS-B Out (ICAO mandate)
- Multiple ground receivers operated by:
  - GCAA (official)
  - Enthusiast networks (ADSBexchange, OpenSky contributors)
  - Commercial aggregators (Flightradar24, FlightAware)

## Why UAE ADS-B Is NOT a Unique Source

**The repo already has ADS-B patterns**:
- Local Mode-S receiver bridge (for self-hosted dump1090)
- SKILL.md lists OpenSky Network and ADSBexchange as known sources

**UAE airspace is already covered by global ADS-B aggregators**:
1. **ADSBexchange**: Global crowdsourced network, includes UAE ground stations
2. **OpenSky Network**: Academic ADS-B network, global coverage including UAE
3. **Flightradar24**, **FlightAware**: Commercial (skip)

**Geographic filtering**: UAE flights can be filtered from global feeds using bounding boxes or airport codes (DXB, AUH, SHJ).

## If Deployed as UAE-Specific

If someone wanted a UAE-focused ADS-B deployment, this would be a **configuration of existing sources**:

**Option 1: Local receiver in UAE**
- Deploy a Raspberry Pi + RTL-SDR dongle running dump1090 near Dubai or Abu Dhabi
- Use existing Mode-S bridge in the repo
- **Advantage**: Low latency, full control, no API limits
- **Disadvantage**: Requires physical deployment in UAE

**Option 2: OpenSky Network API** (filtered to UAE)
- Use OpenSky's REST API with bounding box filter:
  ```
  GET https://opensky-network.org/api/states/all
    ?lamin=22.0&lomin=51.0&lamax=27.0&lomax=57.0
  ```
- **Advantage**: No hardware, free (with rate limits)
- **Disadvantage**: Rate limits (10 sec polling, anonymous users)

**Option 3: ADSBexchange API** (filtered to UAE)
- Similar to OpenSky but requires API key
- Higher rate limits than OpenSky

## Scoring (if treated as a separate UAE source)

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time (1–2 second ADS-B broadcasts) |
| Openness | 2–3 | OpenSky is free with limits; ADSBexchange requires key |
| Stability | 3 | ADS-B is ICAO standard, mature technology |
| Structure | 3 | JSON (APIs) or binary BEAST (structured) |
| Identifiers | 3 | ICAO hex (24-bit aircraft address, globally unique) |
| Additive value | -3 | **Duplicates global ADS-B sources** — only adds geographic focus |

## Verdict

**Skip** (as a separate UAE-specific source). UAE airspace is already covered by:
- Global ADS-B aggregators (ADSBexchange, OpenSky Network)
- Existing Mode-S receiver bridge in the repo

**Recommendation**:
- **Document UAE as a deployment scenario** for the Mode-S bridge (if someone wants a local receiver)
- **Document UAE bounding box** for OpenSky API filtering
- **Do NOT create a separate "UAE ADS-B" source** — it duplicates existing patterns

**GCAA alternative**: If the UAE General Civil Aviation Authority (GCAA) publishes its **own** real-time flight tracking API (with additional metadata like flight plans, slots, gate assignments, customs clearance), **that** would be a **Build** candidate as a distinct source. But raw ADS-B from UAE airspace is not unique.

**Check GCAA**:
```
site:gcaa.gov.ae flight data
site:gcaa.gov.ae real-time
site:gcaa.gov.ae api
```

If GCAA publishes an API with value-added data (not just ADS-B relay), reconsider as a **Maybe** or **Build**.
