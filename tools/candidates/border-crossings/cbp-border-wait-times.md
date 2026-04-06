# US CBP Border Wait Times
**Country/Region**: United States (land border crossings with Mexico and Canada)
**Publisher**: US Customs and Border Protection (CBP)
**API Endpoint**: `https://bwt.cbp.gov/` (Angular web application with backend API)
**Documentation**: https://bwt.cbp.gov/ (no formal API documentation)
**Protocol**: REST (Angular SPA backend)
**Auth**: None (public)
**Data Format**: JSON (internal API), HTML (web portal)
**Update Frequency**: Approximately every hour
**License**: US Government public domain

## What It Provides
CBP publishes estimated wait times at US land border ports of entry:
- Wait times for passenger vehicles
- Wait times for pedestrians
- Wait times for commercial vehicles (trucks)
- Wait times by lane type (standard, SENTRI, NEXUS, Ready Lane, FAST)
- Port of entry status (open/closed)
- Last updated timestamp per port
- Approximately 170 land border ports of entry

## API Details
- **Web application**: `https://bwt.cbp.gov/` — Angular SPA
- **Backend API**: The web application calls internal API endpoints for wait time data
- **Possible API patterns** (observed from the SPA):
  - Port-specific wait times
  - All-ports listing
  - Historical data (limited)
- **XML feed (legacy)**: `https://bwt.cbp.gov/xml/bwt.xml` — may still be available
- **Data fields**: Port name, port number, crossing type, lane type, delay/wait time, last updated, operating hours

Note: The web application at bwt.cbp.gov uses an Angular frontend. The internal API endpoints returned 404s during probing, suggesting the API routes may be protected or have changed. The legacy XML feed may still work as an alternative.

## Freshness Assessment
Good. Wait times are updated approximately every hour at most ports. Some major ports update more frequently. The data is based on actual measured wait times or estimates from CBP officers at each port.

## Entity Model
- **Port of Entry** (port number, name, state, border (Canada/Mexico), crossing name)
- **Wait Time** (passenger vehicles, pedestrians, commercial, by lane type)
- **Lane Type** (Standard, SENTRI, NEXUS, Ready Lane, FAST)
- **Status** (open, closed, time of last update)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Hourly updates |
| Openness | 1 | Public portal, but API not formally documented |
| Stability | 3 | US Government, CBP official service |
| Structure | 2 | JSON behind SPA, XML feed (legacy) |
| Identifiers | 3 | Port numbers are stable federal identifiers |
| Additive Value | 3 | Only source for US border wait times |
| **Total** | **14/18** | |

## Notes
- The Angular SPA makes direct API probing difficult — would need to reverse-engineer the API endpoints
- Legacy XML feed at `/xml/bwt.xml` is a simpler integration path if still available
- CBP port numbers are standardized identifiers usable across government systems
- Wait time accuracy varies — they are estimates, not precise measurements
- Consider pairing with CBSA (Canadian) data for complete border picture
