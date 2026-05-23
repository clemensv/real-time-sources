# DEWA Mohammed bin Rashid Al Maktoum Solar Park (Real-Time Solar Generation)

- **Country/Region**: United Arab Emirates / Dubai
- **Endpoint**: **UNKNOWN** — requires discovery
- **Protocol**: Unknown (likely REST API or SCADA export)
- **Auth**: Unknown
- **Format**: Likely JSON or CSV
- **Freshness**: Expected real-time (minute-level generation data typical for grid-connected solar)
- **Docs**: https://www.dewa.gov.ae/en/about-dewa/strategic-initiatives/mbr-solar-park
- **Score**: **TBD** (cannot score without endpoint)

## Overview

The **Mohammed bin Rashid Al Maktoum Solar Park** (MBR Solar Park) is one of the world's largest single-site solar power plants, located in Seih Al Dahal, 50 km south of Dubai.

**Current status** (as of 2025):
- **Phases 1–5 operational**: 2,427 MW total capacity
  - Phase 1: 13 MW (PV, 2013)
  - Phase 2: 200 MW (PV, 2017)
  - Phase 3: 800 MW (PV, 2020)
  - Phase 4: 950 MW (PV, 2022) — world's largest single-site PV project at completion
  - Phase 5: 464 MW (PV + CSP with storage, 2023–2024)
- **Phases 6–7 planned**: Additional 1,800 MW by 2030
- **Final target**: 5,000 MW by 2030 (powering ~1.3 million homes)

**Technology**:
- Photovoltaic (PV): Bifacial modules, single-axis tracking
- Concentrated Solar Power (CSP): Phase 5 includes molten salt thermal storage (15 hours)

**Why this is significant**:
- **Scale**: One of the top 5 solar parks globally by capacity
- **Grid impact**: Represents ~20% of Dubai's peak demand when fully operational
- **Duck curve dynamics**: MBR Solar Park creates pronounced solar generation peaks (10am–2pm) that stress grid flexibility
- **CSP storage**: Phase 5's thermal storage enables power generation after sunset, flattening the duck curve
- **Climate leadership**: UAE positions MBR as a flagship project for Gulf renewable energy transition

## Why Real-Time Solar Data Is Valuable

1. **Grid balancing**: Solar generation fluctuates with cloud cover, dust storms, and time of day. Real-time data reveals grid stress points.
2. **Weather correlation**: Solar irradiance drops during dust storms (common in UAE March–April). Cross-referencing solar output with NCM weather data would reveal dust event impacts.
3. **Performance monitoring**: Compare actual generation vs. installed capacity to detect soiling (dust on panels), outages, or degradation.
4. **Energy transition analytics**: Track how solar displaces gas-fired generation in Dubai's grid mix.
5. **Economic**: Solar generation correlates with DEWA's avoided fuel costs and carbon emissions savings.

## Endpoint Discovery Required

### 1. DEWA Open Data Initiative

**DEWA announced in 2023** that it would launch an open data platform, which may include MBR Solar Park generation data. Search for:

```
site:dewa.gov.ae open data
site:dewa.gov.ae solar park generation
site:dewa.gov.ae real-time solar
site:dewa.gov.ae api
site:dewa.gov.ae developer
```

### 2. DEWA Dashboard / Public Monitoring

DEWA may publish a public dashboard showing MBR Solar Park's live generation (similar to German TSOs publishing renewable generation on their websites). Check for:

```
site:dewa.gov.ae solar park dashboard
site:dewa.gov.ae renewable energy monitoring
```

If a dashboard exists, inspect network traffic (browser DevTools) to find the underlying API endpoint.

### 3. Smart Grid / SCADA

MBR Solar Park is connected to DEWA's smart grid. DEWA has announced smart grid initiatives (smart meters, demand response, distributed energy resources). The SCADA system that controls the park may export telemetry to a central data lake. Check for:

```
site:dewa.gov.ae smart grid
site:dewa.gov.ae energy management system
```

### 4. UAE Ministry of Energy & Infrastructure

The federal Ministry of Energy & Infrastructure may aggregate national renewable energy data (including MBR). Check:

```
site:moei.gov.ae solar generation
site:moei.gov.ae renewable energy data
```

### 5. IRENA / IEA / Ember Data

**International Energy Agency (IEA)**, **IRENA** (International Renewable Energy Agency), and **Ember** (energy think tank) publish country-level renewable energy data. They may source UAE solar generation from DEWA or federal authorities. Check if these organizations provide:

- IRENA Renewable Energy Statistics: https://www.irena.org/
- IEA Data Explorer: https://www.iea.org/
- Ember Climate: https://ember-climate.org/data/

If DEWA provides data to these bodies, the same data may be available directly from DEWA.

### 6. Direct Contact

Email DEWA's open data team (if contact info is discoverable) or use DEWA's customer service to request API access to MBR Solar Park generation data.

## If Endpoint Is Found

If DEWA publishes real-time MBR Solar Park generation data, this would be a **Build** candidate with a score of **16–17/18**:

| Criterion | Expected Score | Notes |
|-----------|----------------|-------|
| Freshness | 3 | Real-time generation (1–15 min intervals typical for grid-connected solar) |
| Openness | 2–3 | TBD (DEWA open data initiative suggests free access, but may require API key) |
| Stability | 3 | DEWA is a government utility; SCADA systems are mission-critical |
| Structure | 3 | JSON or CSV REST API (expected) |
| Identifiers | 3 | Site ID (MBR Solar Park) or sub-site IDs (Phase 1, Phase 2, etc.) |
| Additive value | 2–3 | New region (Gulf solar), unique dataset (mega-scale PV + CSP), energy domain already in repo |

**Key model**: Site-keyed (`site_id`) or phase-keyed (`phase_id`)

**Event families**:
- Reference: site metadata (phases, installed capacity, technology type, commissioning dates)
- Telemetry: generation output (MW, MWh cumulative, timestamp, capacity factor, status: online/offline/curtailed)
- Alerts: outage notifications, maintenance windows

**CloudEvents subject**: `ae/dubai/solar/mbr-park/phases/{phase_id}` or `ae/dubai/energy/solar-generation`

**Repo sibling**: The repo has `entsoe` (European grid) planned. MBR Solar Park would be a complementary dataset showing renewable penetration in a different grid context (GCCIA, not ENTSO-E).

## If Endpoint Cannot Be Found

If DEWA does not publish MBR Solar Park data:

- **Status**: Skip (no public API)
- **Gap type**: Major renewable energy asset data not publicly accessible
- **Alternative**:
  - Aggregate UAE solar from IEA/IRENA (monthly-to-annual, too slow)
  - Satellite-based solar irradiance estimates (NASA POWER, Solcast) — proxy but not actual generation
- **Recommendation**: 
  - Contact DEWA to request API access
  - Advocate for open data (renewable energy generation is published by TSOs worldwide: Germany RTE, California CAISO, Australia AEMO, etc.)

**Political context**: UAE hosts COP28 (2023) and positions itself as a climate leader. Publishing real-time renewable energy data would demonstrate transparency and align with global best practices.

**Verdict**: **Maybe** (medium-high priority, pending endpoint discovery). MBR Solar Park data is a **strategic target** because:
- World-class solar asset (top 5 globally)
- Reveals UAE's renewable energy transition in real-time
- Unique dataset (Gulf solar with dust storm impacts, CSP storage dynamics)
- High public interest (climate, energy security, smart grid)

Spend 1–2 hours searching DEWA website, dashboard hunting, and checking international aggregators. If no endpoint is found, reach out to DEWA directly before marking as Skip.
