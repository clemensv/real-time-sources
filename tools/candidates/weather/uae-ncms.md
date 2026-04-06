# UAE NCMS — National Centre of Meteorology

**Country/Region**: United Arab Emirates
**Publisher**: National Centre of Meteorology (NCMS), UAE
**API Endpoint**: `https://www.ncms.ae/` (web portal — connection failed)
**Documentation**: https://www.ncms.ae/en
**Protocol**: Web portal; mobile app backend (undocumented)
**Auth**: N/A (no public API discovered)
**Data Format**: HTML, mobile app JSON (undocumented)
**Update Frequency**: Hourly observations; real-time for warnings
**License**: UAE government data

## What It Provides

NCMS is the UAE's national meteorological authority, monitoring weather across one of the world's most extreme arid climates. Summer temperatures routinely exceed 50°C, and the UAE has been investing heavily in weather modification (cloud seeding).

NCMS data includes:
- **Current conditions**: Temperature, humidity, wind, visibility from stations across all 7 emirates
- **Marine weather**: Critical for Persian Gulf shipping (Strait of Hormuz)
- **Aviation weather**: Dubai, Abu Dhabi, Sharjah — among the world's busiest airports
- **Fog advisories**: Dense fog is a major hazard on UAE highways
- **Sand/dust storms**: Shamal wind events
- **Cloud seeding operations**: UAE is a global leader in rain enhancement
- **UV index**: Extreme in summer months

### Probe Results

Connection to `ncms.ae` **failed** (connection timeout). The website may require specific TLS configuration, have geographic restrictions, or was experiencing downtime during testing.

### Known Alternative Access

- **NCMS mobile app**: Available on iOS/Android; has detailed station data
- **Abu Dhabi Open Data**: `data.abudhabi` portal may have weather datasets
- **Dubai Pulse**: `dubaidata.ae` — Dubai's open data platform
- **WMO GTS**: UAE synoptic data shared internationally

## Entity Model

- **Station**: Observing stations across 7 emirates (Abu Dhabi, Dubai, Sharjah, Ajman, Umm Al Quwain, Ras Al Khaimah, Fujairah)
- **Marine Zone**: Persian Gulf, Gulf of Oman sea areas
- **Warning Area**: Emirates-based warning zones
- **Aviation Station**: ICAO-coded airports (OMDB, OMAA, OMSJ, etc.)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Real-time data exists (mobile app confirms); web inaccessible |
| Openness | 0 | Connection failed; no public API documented |
| Stability | 2 | Well-funded national agency; modern infrastructure |
| Structure | 1 | Mobile app suggests API backend exists; undocumented |
| Identifiers | 2 | ICAO codes for airports; emirate-based geography |
| Additive Value | 2 | Gulf region coverage; extreme heat monitoring; aviation weather |
| **Total** | **9/18** | |

## Integration Notes

- **Not currently viable** — website inaccessible
- The UAE's smart city initiatives (Dubai, Abu Dhabi) suggest APIs may exist but are not publicly documented
- Abu Dhabi's open data platform and Dubai Pulse are worth investigating separately
- Aviation weather (METAR/TAF) for UAE airports is available through standard aviation data sources
- Strait of Hormuz marine weather is strategically critical (30% of global seaborne oil transits)
- Cloud seeding operation data would be unique and scientifically interesting if ever made public

## Verdict

Well-funded agency but no public API discovered. The UAE has the technological capability and resources to run a modern weather API — the mobile app demonstrates real-time data delivery. The lack of a documented public API is the barrier. Worth investigating Abu Dhabi and Dubai's separate open data platforms as alternative entry points for Gulf weather data.
