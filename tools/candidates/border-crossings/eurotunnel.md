# Eurotunnel / Channel Tunnel Live Travel Info
**Country/Region**: UK / France (Folkestone–Calais)
**Publisher**: Getlink / Eurotunnel
**API Endpoint**: `https://www.eurotunnel.com/uk/travelling-with-us/live-travel-information/` (web SPA)
**Documentation**: None (web portal only)
**Protocol**: Web SPA (JavaScript-rendered)
**Auth**: None for public portal
**Data Format**: HTML/JavaScript (data loaded dynamically)
**Update Frequency**: Near real-time (departure times, delays, wait times)
**License**: Proprietary (Getlink)

## What It Provides
The Eurotunnel/Le Shuttle service operates vehicle transport through the Channel Tunnel between England and France:
- **Next departure times**: Folkestone → Calais and Calais → Folkestone
- **Wait times**: Current delays at terminals
- **Service status**: Normal, delays, disrupted, suspended
- **Terminal information**: Check-in status, boarding gates
- **Travel advisories**: Border control delays, weather, special conditions
- **Capacity indicators**: Booking availability for upcoming departures

The Channel Tunnel is the only fixed link between the UK and continental Europe, carrying ~10 million passengers and ~1.6 million trucks per year.

## API Details
- **Live info page**: `https://www.eurotunnel.com/uk/travelling-with-us/live-travel-information/`
  - HTTP 200 OK, ~99 KB HTML
  - Modern JavaScript SPA — data loaded dynamically
  - No inline JSON or data elements in initial HTML
- **No REST API discovered**: All data is JavaScript-rendered
- **Possible integration paths**:
  - Browser automation (Playwright/Puppeteer) to extract rendered data
  - DevTools network inspection to find XHR/Fetch endpoints
  - Twitter/X feed monitoring (@LeShuttle) for service updates

## Probe Results
```
https://www.eurotunnel.com/uk/travelling-with-us/live-travel-information/
  Status: 200 OK
  Content-Type: text/html; charset=utf-8
  Size: ~99 KB
  Assessment: SPA, data not in initial HTML payload
```

## Freshness Assessment
Good for the data it serves. Departure times and service status update in near real-time. The page reflects current conditions at both terminals. However, access requires JavaScript execution.

## Entity Model (Inferred)
- **Departure** (direction, scheduled_time, actual_time, status)
- **Terminal** (location: Folkestone/Calais, status, wait_time)
- **ServiceStatus** (overall status, advisory messages)
- **Delay** (cause, estimated duration, affected departures)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Real-time departure and delay data |
| Openness | 1 | No API, SPA-only, proprietary |
| Stability | 3 | Major transport infrastructure operator |
| Structure | 1 | Data locked behind JavaScript SPA |
| Identifiers | 1 | Departure times as implicit IDs |
| Additive Value | 3 | Only data source for Channel Tunnel travel status |
| **Total** | **12/18** | |

## Notes
- Post-Brexit, the Channel Tunnel crossing involves both UK and French/EU border checks
- Border control delays are a significant real-time data signal since 2021
- The Eurotunnel is a complement to ferry services (P&O, DFDS, Irish Ferries)
- Browser automation would be required for any integration
- Consider monitoring @LeShuttle Twitter/X feed as a simpler real-time signal
- Pairs with CBP/CBSA (North America) for a cross-continental border wait picture
