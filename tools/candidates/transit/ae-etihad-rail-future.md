# Etihad Rail - Future Passenger Rail GTFS (2025–2026 Launch)

- **Country/Region**: United Arab Emirates (Federal - Abu Dhabi, Dubai, Sharjah, RAK, Fujairah)
- **Endpoint**: **NOT YET OPERATIONAL** (service launches 2025–2026)
- **Protocol**: Expected GTFS + GTFS-RT (General Transit Feed Specification)
- **Auth**: Unknown (likely none for static GTFS, TBD for real-time)
- **Format**: GTFS static (ZIP with CSV files), GTFS-RT (Protobuf)
- **Freshness**: Expected real-time (train positions, delays, cancellations)
- **Docs**: https://www.etihadrail.ae/
- **Score**: **FUTURE SOURCE** (cannot score until operational)

## Overview

**Etihad Rail** is the UAE's national freight and passenger railway network, currently under construction:

### Network Status (as of 2025)
- **Stage 1** (2016): Freight-only, Habshan (gas fields) → Ruwais (industrial port), 264 km, operational
- **Stage 2** (2023–2024): Freight expansion, UAE-Saudi border → Dubai/Abu Dhabi → Fujairah, 605 km, operational
- **Stage 3** (under construction): Passenger rail, expected launch **2025–2026**

### Passenger Service (Stage 3)
- **Route**: Abu Dhabi → Dubai → Sharjah → RAK → Fujairah (eventually)
- **Stations**: 
  - Abu Dhabi Central (near Mussafah)
  - Dubai (likely near Dubai South / Al Maktoum Airport)
  - Sharjah
  - RAK
  - Fujairah (future extension)
- **Speed**: Up to 200 km/h (intercity high-speed)
- **Frequency**: Expected hourly Abu Dhabi ↔ Dubai (30-minute journey)
- **Technology**: Modern electrified rolling stock (manufacturer TBD)

**Why Etihad Rail is significant**:
- **First intercity passenger rail in the Gulf** (Qatar has Doha Metro, but this is intercity)
- **Connects all major UAE population centers** (Abu Dhabi, Dubai, Sharjah)
- **Alternative to congested E11 highway** (Abu Dhabi–Dubai road is heavily trafficked)
- **Tourism**: Connects Dubai tourists with Abu Dhabi attractions (Louvre, Sheikh Zayed Mosque)

## Why This Is a Future Build Candidate

1. **GTFS-RT expected**: Modern passenger rail systems worldwide publish GTFS-RT (Amtrak, Deutsche Bahn, SNCF, JR East). Etihad Rail is being built to international standards and will likely follow this pattern.
2. **Real-time train tracking**: Passengers will expect live train locations, delay predictions, platform assignments (standard in modern rail apps).
3. **App integration**: Etihad Rail will have a mobile app (likely multi-modal with RTA, Abu Dhabi DoT). The app will need backend APIs for real-time data.
4. **Strategic value**: First intercity rail in the Gulf; high-profile infrastructure project.

## Current Status

**Passenger service has NOT launched yet**. Expected timeline:
- **2025 Q3–Q4**: Soft launch (testing, limited service)
- **2026**: Full commercial service

**GTFS publication timeline**:
- **Static GTFS**: Expected 3–6 months before launch (for Google Maps, Apple Maps integration)
- **GTFS-RT**: Expected at launch or shortly after

## Endpoint Discovery (When Operational)

When Etihad Rail launches passenger service, check for:

### 1. Etihad Rail Website
```
site:etihadrail.ae gtfs
site:etihadrail.ae real-time
site:etihadrail.ae api
site:etihadrail.ae developer
```

### 2. MobilityData Catalog
Etihad Rail will likely register with MobilityData (global GTFS catalog):
```
https://database.mobilitydata.org/ (search "Etihad Rail" or "UAE")
```

### 3. Google Maps / Apple Maps
If Etihad Rail appears in Google/Apple journey planners, they have received GTFS static. GTFS-RT may follow.

### 4. Etihad Rail Mobile App
When the app launches:
- Install app (iOS/Android)
- Use mitmproxy to intercept API calls for train tracking
- Look for GTFS-RT endpoints or custom JSON APIs

### 5. Integration with RTA / Abu Dhabi DoT
Etihad Rail will integrate with urban transit (Metro, bus) for multi-modal journeys. Check if RTA or DoT publish combined feeds.

## Expected Scoring (When Operational)

If Etihad Rail publishes GTFS-RT at launch, this would be a **Build** candidate with a score of **16–17/18**:

| Criterion | Expected Score | Notes |
|-----------|----------------|-------|
| Freshness | 3 | Real-time train positions (expected 10–30 second updates) |
| Openness | 2–3 | TBD (modern rail agencies publish GTFS-RT openly or with free API keys) |
| Stability | 3 | National railway operator; mission-critical systems |
| Structure | 3 | GTFS-RT Protobuf (formal spec) |
| Identifiers | 3 | Train IDs, trip IDs, route IDs (stable) |
| Additive value | 3 | **First Gulf intercity rail**, new unique dataset |

**Total**: 17–18/18 (if fully open)

## Integration Notes

**Key model**: Train/trip-keyed (`vehicle_id` or `trip_id`)

**Event families**:
- Reference: GTFS static (routes, stops, trips, schedules, fare rules)
- Telemetry: train positions (lat/lon, speed, bearing, timestamp), trip updates (delays, platform assignments, cancellations), service alerts (line closures, engineering works)

**CloudEvents subject**: `ae/rail/etihad/trains/{vehicle_id}` or `ae/rail/etihad/trips/{trip_id}`

**Repo sibling**: The repo has `gtfs` (generic transit). Etihad Rail would use the same bridge pattern.

## Verdict

**FUTURE BUILD** (high priority once operational).

**Action required**:
1. **Monitor Etihad Rail announcements** for passenger service launch date
2. **Re-evaluate in Q3 2025** when service is closer to launch
3. **Check for GTFS publication** 3–6 months before launch
4. **Build bridge** at or shortly after launch

**Why this is high priority**:
- First intercity rail in the Gulf (unique dataset)
- GTFS-RT is a standard protocol (easy integration)
- High-profile infrastructure project (global interest)
- Fills a gap in UAE transit coverage (current GTFS discovery found no RTA or Abu Dhabi feeds)

**Temporary status**: **Skip** (for now, service not operational). **Add to watchlist** for 2025 re-evaluation.

Document as a **future high-value target** in the final report.
