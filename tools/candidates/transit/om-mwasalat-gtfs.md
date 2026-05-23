# Mwasalat Oman - Public Transit (GTFS / GTFS-RT)

- **Country/Region**: Oman (Muscat metropolitan area)
- **Endpoint**: Unknown (not found in MobilityData catalog)
- **Protocol**: GTFS static / GTFS-RT (if available)
- **Auth**: Unknown
- **Format**: Protobuf (GTFS-RT), ZIP (GTFS static)
- **Freshness**: Real-time (GTFS-RT updates vehicle positions every 30-60 seconds)
- **Docs**: https://www.mwasalat.om
- **Score**: 12/18 (if GTFS-RT were available)

## Overview

**Mwasalat** (Arabic: مواصلات, "Transport") is Oman's national public transport company, operating bus services in:
- **Muscat** (Greater Muscat urban area — Muttrah, Ruwi, Qurum, Al Khuwair, Seeb, Muscat International Airport)
- **Salalah** (Dhofar Governorate)
- **Sohar** (Al Batinah North)

Mwasalat operates:
- **Intracity bus routes** (fixed schedules, air-conditioned coaches)
- **Intercity coaches** (Muscat-Salalah, Muscat-Sohar, Muscat-Nizwa, Muscat-Sur)
- **Airport shuttle** (Muscat International Airport to city center)

As of 2023, Mwasalat's network includes ~50 routes and ~300 buses. The service is designed for commuters, students, airport travelers, and tourists.

For a real-time transit bridge, the relevant data formats are:
- **GTFS Static** (General Transit Feed Specification) — route definitions, stop locations, schedules (ZIP file of CSV tables)
- **GTFS-RT** (GTFS Realtime) — live vehicle positions, arrival predictions, service alerts (Protobuf over HTTP)

These formats are **standardized** (Google-developed, widely adopted globally) and already supported by the repo's GTFS bridge pattern.

## Endpoint Analysis

**Not found in MobilityData catalog** — a search of the MobilityData GTFS catalog (the authoritative global registry of transit feeds) for Oman/Mwasalat returned **no results** during discovery (2026-05-23).

Testing:
```
curl -s "https://api.mobilitydata.org/v1/feeds?country_code=om"
```
Returned empty or no Oman feeds.

Manual inspection of the Mwasalat website (mwasalat.om) during discovery:
- Corporate information (about us, services, routes)
- Route maps (static PDF or image maps)
- Schedules (HTML timetables, not machine-readable GTFS)
- **No "Developer API" or "Open Data" section**
- **No GTFS download link**

### Why Mwasalat May Not Publish GTFS

Possible reasons:
- **Small network**: With ~50 routes and ~300 buses, Mwasalat may not have invested in GTFS production (contrast with major systems like London TfL: 700+ routes, 9,000 buses, comprehensive GTFS)
- **Limited real-time tracking**: If buses do not have GPS/AVL (Automatic Vehicle Location) systems, GTFS-RT cannot be produced
- **No third-party integration demand**: GTFS is typically published to enable trip planning apps (Google Maps, Apple Maps, Moovit, Transit). If Mwasalat operates its own app and has not integrated with third-party platforms, there may be no business driver for GTFS publication
- **Regulatory environment**: Unlike EU (PSI Directive, open data requirements) or U.S. (FTA funding tied to GTFS), Oman has no mandate for transit agencies to publish open data

Some GCC transit systems **do** publish GTFS:
- **Dubai RTA** (Dubai Metro, Tram, Buses) — GTFS available
- **Doha Metro** (Qatar) — GTFS available
- **Riyadh Metro** (Saudi Arabia) — GTFS expected upon launch

But others (e.g., smaller regional bus operators) do not.

## Integration Notes

- **If Mwasalat published GTFS/GTFS-RT**, integration would be straightforward:
  - Fetch GTFS Static ZIP, parse CSV tables for routes, stops, schedules
  - Poll GTFS-RT feed (Protobuf over HTTP) every 30-60 seconds for:
    - **Vehicle positions** (bus lat/lon, speed, bearing, route ID)
    - **Trip updates** (arrival/departure predictions for each stop)
    - **Service alerts** (delays, detours, cancellations)
  - Key events by vehicle ID or trip ID (from GTFS)
  - Already a proven pattern in this repo (existing GTFS bridge)

- **Additive value**: The repo has a **generic GTFS bridge** but needs agency-specific feed URLs to ingest. If Mwasalat published GTFS, it would be a **configuration add** (new agency in the GTFS bridge config) rather than a new bridge implementation.

- **Real-time vs. static**: GTFS Static (schedules) is useful for trip planning but not real-time. **GTFS-RT** (vehicle positions, predictions) is required for live tracking, which is the focus of this repo.

- **Alternative: Scraping Mwasalat's app**: If Mwasalat operates a mobile app with real-time bus tracking, the app likely calls a backend API (JSON or XML). Reverse-engineering the app API is possible but:
  - **Fragile** (app updates break the scraper)
  - **Terms of Service risk** (app APIs are typically not public)
  - **Legal gray area** (scraping a private API without permission)
  
  Not recommended unless Mwasalat explicitly permits third-party access.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 0 | No data available to assess; GTFS-RT would be 30-60 second updates if it existed |
| Openness | 0 | No public GTFS feed found |
| Stability | 2 | GTFS/GTFS-RT is a stable global standard, but Mwasalat has not adopted it |
| Structure | 2 | GTFS-RT is Protobuf with formal schema (if Mwasalat published it) |
| Identifiers | 2 | GTFS uses stable IDs for routes, stops, trips, vehicles |
| Additive value | 0 | No data to bridge |

**Verdict**: ❌ Skip

**Rationale**: **No GTFS or GTFS-RT feed was found** for Mwasalat (Oman National Transport Company). The MobilityData catalog has no Oman entries, and Mwasalat's website does not advertise GTFS download or developer API access.

**Recommendations**:
1. **Contact Mwasalat directly** to inquire:
   - Does Mwasalat produce GTFS Static or GTFS-RT feeds?
   - Are they planning to publish transit data for third-party app integration?
   - Do buses have GPS/AVL systems that could support real-time tracking?

2. **Check Google Maps**: If Mwasalat routes appear in Google Maps with scheduled transit directions, Google has obtained GTFS Static from Mwasalat (possibly via private agreement). Inquire whether the same data is available publicly.

3. **Monitor MobilityData catalog**: If Mwasalat publishes GTFS in the future, it will appear in the global catalog automatically. Revisit this candidate if Oman entries appear.

**Low priority for immediate bridge work** — Oman's transit network is small (~50 routes) compared to major systems worldwide. Focus on higher-value sources (seismology, weather, cyclone warnings) before pursuing transit data that may not be publicly available.

**If Mwasalat publishes GTFS-RT in the future, upgrade to ✅ Build** — the existing repo GTFS bridge would support it with minimal configuration changes.
