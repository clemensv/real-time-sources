# Hydro-Québec Power Outages
**Country/Region**: Québec, Canada
**Publisher**: Hydro-Québec (provincial crown corporation)
**API Endpoint**: `https://pannes.hydroquebec.com/` (Angular SPA with internal API)
**Documentation**: None (web portal, no documented API)
**Protocol**: Angular SPA backend (XHR/Fetch endpoints)
**Auth**: None for public portal
**Data Format**: JSON (behind JavaScript, not directly accessible)
**Update Frequency**: Near real-time (minutes)
**License**: Québec government public data

## What It Provides
Hydro-Québec's outage portal provides real-time power outage information for Canada's largest province:
- **Active outages**: Location, affected customers, start time, estimated restoration
- **Outage causes**: Storm, equipment failure, vegetation, planned maintenance
- **Municipal summaries**: Outage counts and affected customers by municipality
- **Geographic display**: Interactive map of outage locations
- **Historical totals**: Running count of affected customers and outage events
- **Coverage**: 4.4 million customers across 1.7 million km²

## API Details
- **Portal**: `https://pannes.hydroquebec.com/` — Angular SPA (HTTP 200)
- **Expected data endpoints** (behind Angular, not directly accessible):
  - Municipal bilingual data: `/pannes/donnees/v3_0/bismunicaliteen.json`
  - Summary totals: `/pannes/donnees/v3_0/bilan.json`
  - Background interruptions: `/pannes/bilan-interruptions-background`
- **Direct probing results**: All data endpoints returned connection errors or state errors
- **Technique required**: Browser DevTools network inspection to discover actual XHR endpoints
- **Data structure**: Likely JSON with municipality codes, customer counts, and restoration estimates

## Probe Results
```
https://pannes.hydroquebec.com/: HTTP 200 OK (Angular SPA)
/pannes/donnees/v3_0/bismunicaliteen.json: Connection error
/pannes/donnees/v3_0/bilan.json: Connection error
Assessment: Portal functional, data endpoints not directly accessible
  — likely served through Angular service layer with session/CSRF tokens
```

## Freshness Assessment
Excellent when accessible. The outage portal updates in near real-time during active storms and outages. Hydro-Québec is frequently tested by severe winter weather (ice storms, heavy snow), and the portal handles high traffic during major events.

## Entity Model (Inferred)
- **Outage** (ID, start time, estimated restoration, cause, status)
- **Municipality** (code, name_fr, name_en, region)
- **Impact** (customers_affected, outage_count per municipality)
- **Summary** (total_outages, total_customers_affected, last_update)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Real-time during outage events |
| Openness | 1 | No documented API, Angular SPA only |
| Stability | 3 | Crown corporation, critical infrastructure |
| Structure | 2 | JSON behind SPA, structured data exists |
| Identifiers | 2 | Municipal codes, outage IDs (inferred) |
| Additive Value | 3 | Only source for Québec outage data (4.4M customers) |
| **Total** | **14/18** | |

## Notes
- Hydro-Québec is the fourth-largest hydroelectric utility in the world
- Quebec's extreme winter weather makes outage data particularly valuable
- The Angular SPA architecture means data endpoints exist but require discovery
- Browser DevTools network tab during an active outage would reveal the actual API
- Consider Playwright/Puppeteer automation as an integration path
- The v3_0 path structure suggests a versioned internal API — structured and intentional
- During the 1998 ice storm, 1.4 million customers lost power — this system was built for resilience
