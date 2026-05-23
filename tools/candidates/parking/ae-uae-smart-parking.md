# UAE Smart Parking Systems (Dubai RTA Mawaqif, Abu Dhabi Darb)

- **Country/Region**: United Arab Emirates / Dubai + Abu Dhabi
- **Endpoints**: 
  - Dubai RTA: `https://www.rta.ae/links/parking/parking.xml` (BLOCKED by WAF)
  - Abu Dhabi Darb: **UNKNOWN**
- **Protocol**: XML (Dubai), Unknown (Abu Dhabi)
- **Auth**: Unknown (Dubai endpoints are public but WAF-protected)
- **Format**: XML or JSON
- **Freshness**: Real-time (parking occupancy updated every 1–5 minutes)
- **Docs**:
  - Dubai: https://www.rta.ae/wps/portal/rta/ae/home/services/parking
  - Abu Dhabi: https://darb.itc.gov.ae/
- **Score**: **Blocked** (Dubai WAF) / **TBD** (Abu Dhabi)

## Overview

The UAE operates extensive smart parking systems in Dubai and Abu Dhabi:

### Dubai (RTA Mawaqif)
- **Operator**: Roads and Transport Authority (RTA)
- **System**: "Mawaqif" — integrated parking management
- **Coverage**: 
  - On-street parking: 50,000+ metered spaces across Dubai
  - Off-street parking: 100+ garages and lots (Dubai Mall, City Walk, etc.)
- **Technology**: SMS-based payment + parking meters + license plate recognition
- **App**: "RTA Dubai" app shows nearby parking availability

### Abu Dhabi (Mawaqif + Darb)
- **Operator**: Integrated Transport Centre (ITC) under Department of Transport (DoT)
- **System**: "Mawaqif" (on-street) + "Darb" (integrated mobility platform)
- **Coverage**:
  - On-street parking: 30,000+ metered spaces
  - Off-street parking: Major garages (Corniche, Yas Island, Saadiyat, ADNOC HQ, etc.)
- **Technology**: SMS + app-based payment + sensors
- **App**: "Darb" app (multi-modal: parking, buses, taxis, cycling)

### Other Emirates
- **Sharjah**: Smart parking in city center and near Sharjah University
- **Ajman, RAK**: Limited smart parking (primarily at malls and airports)

**Why parking data is valuable**:
- **Urban planning**: Parking occupancy reveals congestion patterns, demand hotspots
- **Real-time navigation**: Apps like Waze, Google Maps, Apple Maps use parking availability for routing
- **Economic indicators**: Parking demand correlates with retail activity, tourism, events
- **Behavioral analytics**: Parking duration, turnover rates, pricing elasticity

## Known Challenge: Dubai WAF (Same as Traffic)

**RTA's parking XML endpoint** is listed in older documentation and third-party integrations, but **all automated requests are blocked** by the same WAF that blocks traffic data:

```
https://www.rta.ae/links/parking/parking.xml
```

Returns:
```html
Request Rejected. Contact RTA call center (ask@rta.ae).
```

**This indicates**:
- The endpoint exists (URL is correct)
- The data is generated (RTA's system tracks parking in real-time)
- WAF blocks automation (same issue as RTA traffic)

**See earlier candidate**: `ae-rta-dubai-traffic.md` for full WAF analysis.

## Abu Dhabi Alternative

**Abu Dhabi's Darb platform** is more recent (launched ~2020) and may have better API access than Dubai's legacy RTA system.

**Search strategies**:
```
site:darb.itc.gov.ae api
site:darb.itc.gov.ae parking availability
site:dot.abudhabi.ae parking data
site:itc.gov.ae open data
```

**Check Darb mobile app**:
- Install "Darb" app (iOS/Android)
- Use mitmproxy to intercept API calls when viewing parking map
- This could reveal REST endpoints for parking availability

**Check ArcGIS**:
Abu Dhabi government uses Esri extensively. Search for:
```
https://maps.dot.abudhabi.ae/
https://services.arcgis.com/ (search for "ITC" or "Darb" or "Abu Dhabi parking")
```

## If Endpoint Is Found (Dubai or Abu Dhabi)

If RTA or ITC/DoT publish parking availability APIs (and bypass WAF), this would be a **Build** candidate with a score of **14–15/18**:

| Criterion | Expected Score | Notes |
|-----------|----------------|-------|
| Freshness | 3 | Real-time occupancy (1–5 min updates typical for smart parking) |
| Openness | 1–2 | Dubai: WAF blocks (fails openness); Abu Dhabi: TBD |
| Stability | 3 | Operational municipal systems |
| Structure | 3 | XML or JSON REST API |
| Identifiers | 3 | Parking facility IDs (garage codes, on-street zone IDs) |
| Additive value | 1 | Parking domain exists in repo taxonomy; UAE adds new region |

**Key model**: Parking facility-keyed (`facility_id` for garages, `zone_id` for on-street)

**Event families**:
- Reference: facility metadata (location, total capacity, pricing, hours)
- Telemetry: occupancy (available spaces, occupied spaces, percentage, timestamp, status: open/full/closed)

**CloudEvents subject**: `ae/dubai/parking/rta/facilities/{facility_id}` or `ae/abudhabi/parking/darb/zones/{zone_id}`

**Repo sibling**: The repo has a `parking` domain in the taxonomy but no existing parking source. This would be the **first parking bridge** in the repo.

## If No Endpoint Is Found / WAF Cannot Be Bypassed

If neither Dubai nor Abu Dhabi publish accessible parking data:

- **Status**: Skip (WAF blocks or no public API)
- **Gap type**: Smart parking systems not openly accessible
- **Alternative**: 
  - Manual app usage (not automatable)
  - Third-party parking aggregators (ParkWhiz, SpotHero — commercial, not UAE-focused)
- **Recommendation**: 
  - Contact RTA and ITC/DoT to request API access or IP whitelist
  - Advocate for open data (parking availability is a standard smart city dataset globally)

**Priority**: **Low-to-Medium**. Parking data is useful for urban analytics, but:
- **Volume**: Dozens to hundreds of facilities (not thousands)
- **Impact**: Less critical than weather, air quality, traffic incidents, or public safety data
- **Blockage**: Dubai's WAF makes this infeasible without direct RTA cooperation

**Verdict**:

**Dubai RTA Parking**: **Skip** (WAF blocks automated access; same issue as traffic)

**Abu Dhabi Darb Parking**: **Maybe** (pending endpoint discovery; lower priority than other UAE targets)

**Recommended action**: Check Abu Dhabi Darb app and ArcGIS. If found easily, add as a low-priority **Build**. If discovery takes >1 hour, **Skip** and focus on higher-value UAE sources (weather, air quality, radiation, marine).
