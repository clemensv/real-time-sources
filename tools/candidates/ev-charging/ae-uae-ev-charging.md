# UAE EV Charging Networks (DEWA Green Charger, Open Charge Map)

- **Country/Region**: United Arab Emirates (primarily Dubai and Abu Dhabi)
- **Endpoints**:
  - DEWA Green Charger: **UNKNOWN** (requires discovery)
  - Open Charge Map: `https://api.openchargemap.io/v3/poi/?output=json&countrycode=AE` (requires API key)
- **Protocol**: REST API (JSON)
- **Auth**: 
  - DEWA: Unknown
  - Open Charge Map: Free API key (rate limits apply)
- **Format**: JSON
- **Freshness**: Near-real-time (charger status updates when state changes: available → in use → faulted)
- **Docs**:
  - DEWA: https://www.dewa.gov.ae/en/consumer/innovation/green-charger
  - Open Charge Map: https://openchargemap.org/site/develop/api
- **Score**: **TBD** (Open Charge Map: 13–14/18 if UAE data is comprehensive; DEWA: TBD pending discovery)

## Overview

The UAE is rapidly expanding electric vehicle charging infrastructure as part of its clean energy strategy:

### Dubai (DEWA Green Charger)
- **Operator**: Dubai Electricity & Water Authority (DEWA)
- **Network**: "DEWA Green Charger" — Dubai's public EV charging network
- **Stations**: 300+ charging points across Dubai (as of 2024)
- **Locations**: Shopping malls (Dubai Mall, Mall of the Emirates), government buildings, DEWA offices, public parking, gas stations
- **Charger types**: AC Level 2 (3.7 kW, 7 kW, 22 kW), DC Fast (50 kW, 150 kW, 350 kW)
- **App**: "DEWA Smart App" — shows charger locations, availability, reservations

### Abu Dhabi
- **Operator**: Multiple (ADNOC, private operators)
- **Network**: Less centralized than Dubai; expanding rapidly
- **Stations**: 100+ public charging points

### Other Emirates
- **Sharjah**: SEWA (Sharjah Electricity & Water Authority) operates limited EV chargers
- **Northern emirates**: Sparse coverage (FEWA areas, private operators)

### Nationwide Initiatives
- **UAE EV Goal**: 50% of vehicles to be electric by 2050
- **Etihad Rail**: New electrified passenger rail network (launching 2025–2026) will spur EV infrastructure growth

**Why EV charging data is significant**:
- **UAE adoption rate**: High-income population, strong government incentives, luxury EV market (Tesla, Porsche Taycan, Mercedes EQS)
- **Real-time availability**: Charger status (available, in use, faulted) is essential for route planning
- **Grid integration**: EV charging patterns reveal load management and smart grid dynamics
- **Tourism / business**: Dubai is a major tourist and business hub; EV charging maps are practical utility

## Endpoint Discovery Required

### 1. DEWA Green Charger API

**DEWA announced an open data initiative in 2023**, which may include EV charger locations and status. Possible access routes:

**Search DEWA website**:
```
site:dewa.gov.ae green charger api
site:dewa.gov.ae open data
site:dewa.gov.ae developer
```

**Check DEWA Smart App**:
- Install "DEWA Smart App" (iOS/Android)
- Use mitmproxy or Charles Proxy to intercept API calls when viewing charger map
- This could reveal internal REST API endpoints

**Check Open Charge Point Interface (OCPI)** compliance:
- OCPI is the standard protocol for EV roaming (like OCPP for backend, but for inter-network data sharing)
- If DEWA supports OCPI, they may publish a public endpoint

**Check Dubai Pulse / Dubai Data**:
- If these portals ever become accessible, search for "green charger" or "EV charging"

### 2. Open Charge Map (Global Aggregator)

**Open Charge Map** is a crowdsourced global registry of EV charging stations (similar to OpenStreetMap for charging infrastructure). It includes UAE stations submitted by users, operators, and data imports.

**API endpoint verified** (requires free API key):
```
GET https://api.openchargemap.io/v3/poi/?output=json&countrycode=AE&maxresults=500
```

**Returns**:
- Station locations (lat/lon, address)
- Operator name (DEWA, ADNOC, private)
- Number of charging points per station
- Charger types (Type 2, CCS, CHAdeMO)
- Power output (kW)
- Status: operational, partially operational, planned, removed
- User comments and check-ins

**Limitations**:
- **Crowdsourced data quality**: Accuracy depends on user submissions; some entries may be outdated
- **No real-time status**: Open Charge Map shows **static registry data** (station exists, charger types, power levels) but not **real-time availability** (is the charger currently in use?)
- **API key required**: Free tier has rate limits (e.g., 100 requests/day); may need paid tier for continuous polling

**Why Open Charge Map is still valuable**:
- **Comprehensive UAE coverage**: Likely includes DEWA, ADNOC, and private operators
- **Standardized format**: JSON schema is well-documented
- **Stable identifiers**: Each station has a unique OCM ID
- **Good for reference data**: Even without real-time status, the station registry is useful for enrichment

### 3. Other Aggregators / Platforms

**ChargePoint, EVgo, Blink, etc.**:
- Check if major global EV networks operate in UAE (unlikely; UAE uses regional operators)

**PlugShare** (mobile app):
- Community-driven app similar to Open Charge Map; may have UAE data
- No official API, but web scraping is possible (not ideal for production bridge)

**A Better Routeplanner (ABRP)** / **Chargemap**:
- EV route planning apps; may aggregate UAE charger data
- APIs exist but may be commercial

## If DEWA API Is Found

If DEWA publishes a real-time charger status API, this would be a **Build** candidate with a score of **15–16/18**:

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time charger status (state changes propagate within seconds) |
| Openness | 2–3 | TBD (DEWA open data initiative suggests free access, but may require API key) |
| Stability | 3 | DEWA is a government utility; systems are stable |
| Structure | 3 | JSON REST API (expected) |
| Identifiers | 3 | Charger IDs (station ID + connector ID) |
| Additive value | 2 | New region (Gulf), but EV charging domain exists in repo taxonomy |

**Key model**: Charger-keyed (`station_id/connector_id`)

**Event families**:
- Reference: station metadata (location, operator, charger types, power levels)
- Telemetry: charger status (available, in-use, faulted, offline, timestamp)

**CloudEvents subject**: `ae/dubai/ev-charging/dewa/stations/{station_id}/connectors/{connector_id}`

## If Only Open Charge Map Is Available

If DEWA does not publish real-time data, but Open Charge Map has comprehensive UAE coverage:

**Score**: 13/18

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | **Static registry**, not real-time status (major limitation) |
| Openness | 2 | Free API key with rate limits |
| Stability | 3 | Open Charge Map is a mature platform |
| Structure | 3 | JSON REST API, well-documented |
| Identifiers | 3 | OCM IDs are stable |
| Additive value | 1 | Aggregator (not primary source), no real-time status |

**Use case**: 
- **Reference data only** — station locations, charger types, power levels
- **Not a real-time bridge** (no status updates)
- Could be modeled as **metadata enrichment** rather than a standalone bridge

## Verdict

**DEWA Green Charger (if real-time API found)**: **Build** (score 15–16/18)

**Open Charge Map**: **Maybe** (reference data only; useful for enrichment but not a real-time event stream)

**Priority**: Medium. EV charging is a growing domain, and Dubai is a high-profile EV market. However, this is **lower priority than weather, air quality, or radiation** (which have clearer scientific and public safety value).

**Recommended next steps**:
1. Search DEWA website and apps for API endpoints (1–2 hours)
2. If found, proceed to **Build**
3. If not found, poll Open Charge Map for static registry data and document as a **reference data source** (not a real-time bridge)
4. Contact DEWA to request API access or advocate for open data publication
