# FAA SWIM (System Wide Information Management)
**Country/Region**: United States (National Airspace System)
**Publisher**: Federal Aviation Administration (FAA)
**API Endpoint**: `https://swim.faa.gov/` (registration portal)
**Documentation**: https://www.faa.gov/air_traffic/technology/swim
**Protocol**: JMS / SOLACE / SFTP
**Auth**: Registration required (US-only, government vetting)
**Data Format**: FIXM (XML), AIXM (XML), WXXM (XML), proprietary
**Update Frequency**: Real-time (streaming)
**License**: US Government — restricted to approved consumers

## What It Provides
SWIM is the FAA's enterprise information management platform providing real-time National Airspace System (NAS) data:
- **STDDS (SWIM Terminal Data Distribution System)**: Airport surface movement, ASDE-X radar data
- **TFMS (Traffic Flow Management System)**: En-route flight positions, flight plans, flow constraints
- **ITWS (Integrated Terminal Weather System)**: Terminal area weather products
- **TBFM (Time Based Flow Management)**: Arrival/departure sequencing data
- **NOTAM**: Notices to Air Missions
- **METAR/TAF**: Aviation weather observations and forecasts
- **Aeronautical information**: Airspace, routes, procedures

## API Details
- **Access portal**: `https://swim.faa.gov/` — registration and subscription management
- **Protocol**: JMS (Java Message Service) over SOLACE messaging broker
- **Data formats**: FIXM (Flight Information Exchange Model), AIXM (Aeronautical Information Exchange Model), WXXM (Weather Information Exchange Model)
- **Registration process**: Organization must register, get approved, establish connectivity
- **Connectivity**: Dedicated VPN or internet connection to SWIM cloud
- **SFTP**: Some data products available via SFTP bulk download

## Freshness Assessment
Excellent for approved consumers. SWIM provides real-time streaming data with sub-second latency for many products. However, the access process is complex and restricted.

## Entity Model
- **Flight** (GUFI - Globally Unique Flight Identifier, callsign, aircraft type, departure, arrival)
- **Position** (latitude, longitude, altitude, timestamp, source)
- **Airport** (ICAO/IATA codes, surface data, weather)
- **Airspace** (sectors, flow constraints, special use airspace)
- **NOTAM** (location, effective time, description)
- **Weather** (METAR, TAF, SIGMET, terminal weather products)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Real-time streaming |
| Openness | 0 | Registration required, US government vetting |
| Stability | 3 | FAA official infrastructure |
| Structure | 3 | FIXM/AIXM international standards |
| Identifiers | 3 | GUFI, ICAO codes, standard identifiers |
| Additive Value | 3 | Authoritative US airspace data |
| **Total** | **15/18** | |

## Notes
- SWIM is the gold standard for US aviation data but access is highly restricted
- The registration process can take weeks/months and requires organizational approval
- JMS/SOLACE protocol is enterprise messaging, not simple HTTP/REST
- FIXM, AIXM, WXXM are international ICAO-endorsed XML standards
- For most external consumers, OpenSky or ADS-B Exchange are more practical alternatives
- SWIM data feeds some public-facing services (e.g., FAA's flight delay information)
