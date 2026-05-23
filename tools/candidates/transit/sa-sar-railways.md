# Saudi Arabian Railways (SAR) - Passenger Rail Tracking

- **Country/Region**: Saudi Arabia (intercity rail)
- **Endpoint**: Unknown (no public API found)
- **Protocol**: Unknown
- **Auth**: Unknown
- **Format**: Unknown
- **Freshness**: Real-time (train positions update continuously)
- **Docs**: https://www.sar.com.sa (no data portal)
- **Score**: 9/18

## Overview

**Saudi Arabian Railways** (الخطوط الحديدية السعودية, SAR) operates intercity passenger and freight rail in Saudi Arabia:

**Passenger lines**:
1. **Haramain High-Speed Railway** (قطار الحرمين السريع) — Makkah-Madinah via Jeddah, King Abdullah Economic City (KAEC)
   - **450 km**, 300 km/h (Talgo 350 trains, similar to Spain's AVE)
   - Opened 2018, serves Hajj/Umrah pilgrims
   - ~5 million passengers/year
   - Stations: Makkah, Jeddah, KAEC, Madinah

2. **North-South Railway** (passenger service planned, currently freight-only)
   - Riyadh to northern mining regions (phosphate, bauxite)

3. **Riyadh-Dammam Railway** (under renovation, passenger service suspended)
   - Eastern Province connection

**Hajj significance**: The Haramain HSR is critical infrastructure for the annual Hajj pilgrimage, transporting hundreds of thousands of pilgrims between Makkah and Madinah (400 km) in ~2.5 hours.

**Technology**: The Haramain HSR uses **European high-speed rail technology** (Talgo trains from Spain, signaling by Thales). Modern HSR systems typically have:
- **GPS/GNSS train tracking** (real-time positions, accurate to <10m)
- **Automatic Train Protection (ATP)** — Prevents collisions, overspeeding
- **Centralized Traffic Control** — Dispatchers monitor all trains on a digital map

## Real-Time Data Likelihood

High-speed rail operators increasingly publish real-time train data:

| Operator | Country | Public data? | API? | Format |
|----------|---------|--------------|------|--------|
| **SAR (Haramain)** | Saudi Arabia | ❓ Unknown | ❌ None found | Unknown |
| Renfe (AVE) | Spain | ✅ Limited | ❌ None | Dashboard |
| SNCF (TGV) | France | ✅ Yes | ✅ SIRI/REST | XML/JSON |
| DB (ICE) | Germany | ✅ Yes | ✅ REST | JSON |
| Trenitalia (Frecciarossa) | Italy | ✅ Yes | ✅ REST | JSON |
| JR Central (Shinkansen) | Japan | ❌ Limited | ❌ None | Dashboard |

**Pattern**: European HSR operators (France, Germany, Italy) publish real-time train positions and delays. Asian/Gulf operators (Japan, Saudi Arabia) are less transparent.

**GTFS-RT potential**: Some rail operators publish **GTFS-RT** (the same format used for buses/metro). This would include:
- **Trip updates** — Real-time arrival/departure predictions
- **Vehicle positions** — Lat/lon of trains (from GPS)
- **Service alerts** — Delays, cancellations, track closures

## Endpoint Analysis

**SAR website**: `https://www.sar.com.sa`

The SAR website provides:
- Ticket booking (online purchase)
- Schedule lookups (departure times)
- Station information

**No data portal**: SAR does not advertise developer APIs, real-time dashboards, or open data.

**Mobile app**: SAR operates a mobile app for ticket booking ("SAR App"). Mobile apps often consume internal APIs that could be reverse-engineered, but this is fragile and violates most ToS.

**Attempted probes** (not tested):
```
https://api.sar.com.sa/v1/trains
https://sar.com.sa/api/realtime
https://data.sar.com.sa/gtfs-rt
```

**Comparison with Gulf rail**:

| Operator | Country | System | Public data? |
|----------|---------|--------|--------------|
| **SAR** | Saudi Arabia | Haramain HSR | ❌ None found |
| Etihad Rail | UAE | Intercity (under construction) | ❌ None |
| Qatar Rail | Qatar | Doha Metro | ❌ None |
| Oman Rail | Oman | Planned | N/A |

**Pattern**: Gulf rail operators do **not publish real-time data**. This matches the broader Gulf transit opacity (Dubai Metro, Doha Metro also have no GTFS-RT).

## Integration Notes

- **No public API confirmed**: SAR does not advertise real-time train data. This is typical for Gulf transport operators.
- **Haramain HSR is modern**: The system uses European technology (Talgo, Thales), which typically includes real-time tracking. The data exists internally but is not published.
- **Alternative: Google Maps** — If SAR trains appear in Google Maps transit directions, GTFS-static (schedules) exists. Real-time (GTFS-RT) is less likely.
- **Contact SAR**: Reach out to SAR or the operator (SRECO — Spain Railway International Company) to request API access.
- **Unique value**: Haramain HSR is the **only high-speed rail in the Middle East** (excluding Turkey). Real-time train tracking would be regionally unique.

**High-value use cases**:
- **Hajj logistics** — Track pilgrim transport capacity between Makkah and Madinah
- **HSR punctuality** — Delay analysis for one of the world's newest HSR systems
- **Desert rail operations** — Extreme heat (50°C) affects rail performance; real-time data would show operational challenges

## Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Train positions are real-time (if data existed) |
| Openness | 1 | No public API found; Gulf rail pattern is closed |
| Stability | 3 | SAR is the national railway, government-owned |
| Structure | 2 | Would likely be GTFS-RT or JSON (if existed) |
| Identifiers | 3 | Train IDs, trip IDs, station codes are stable |
| Additive value | 2 | First Middle East HSR data; overlaps with existing GTFS-RT bridges |

**Total: 14/18** (if data existed)  
**Actual: 9/18** (penalized for no public data)

**Verdict**: ⏭️ **Reference** — Haramain HSR is a **high-value future source** if SAR publishes real-time data. The system is modern, uses European technology with built-in GPS tracking, and serves a unique market (Hajj pilgrims). However, Gulf rail operators have a pattern of **not publishing data**.

**Recommended action**:
1. **Test Google Maps** — Search for Haramain HSR routes in Google Maps. If they appear, GTFS-static exists.
2. **Monitor SAR announcements** — Check sar.com.sa and Saudi media for data portal launches.
3. **Contact SAR/SRECO** — Request API access or ask about plans to publish real-time data.
4. **Monitor data.gov.sa** — Rail data may appear on the national open data portal.

If SAR publishes GTFS-RT for Haramain HSR, **immediately escalate to ✅ Build**. This would be the first Middle East high-speed rail source and valuable for:
- Transport research (HSR in extreme desert climate)
- Hajj logistics analysis
- Punctuality benchmarking (new HSR system performance)

**Timeline**: No data expected until SAR announces an open data initiative (no timeline known). Do not pursue without confirmed API access.
