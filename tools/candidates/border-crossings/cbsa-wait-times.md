# Canada CBSA Border Wait Times
**Country/Region**: Canada (29 busiest land border crossings)
**Publisher**: Canada Border Services Agency (CBSA)
**API Endpoint**: `https://www.cbsa-asfc.gc.ca/bwt-taf/menu-eng.html` (HTML page)
**Documentation**: https://www.cbsa-asfc.gc.ca/bwt-taf/menu-eng.html
**Protocol**: HTML (web page, updated hourly)
**Auth**: None
**Data Format**: HTML table
**Update Frequency**: At least hourly (per CBSA service standards)
**License**: Open Government Licence - Canada

## What It Provides
CBSA publishes current estimated wait times for the 29 busiest US-to-Canada land border crossings:
- **Commercial Flow** wait time (trucks)
- **Travellers Flow** wait time (passenger vehicles)
- **Last updated** timestamp per crossing
- **Office name and location** (Canadian and US side)

Crossings covered span from New Brunswick/Maine to British Columbia/Washington, including major crossings like Peace Bridge, Ambassador Bridge, Blue Water Bridge, Pacific Highway, and Rainbow Bridge.

## API Details
- **HTML page**: `https://www.cbsa-asfc.gc.ca/bwt-taf/menu-eng.html` — well-structured HTML table
- **French version**: `https://www.cbsa-asfc.gc.ca/bwt-taf/menu-fra.html`
- **CanBorder app**: CBSA's mobile app may use an internal API
- **Data fields**: CBSA Office name, Canadian/US city, commercial wait, traveller wait, update time with timezone
- **Wait time values**: "No Delay", specific minutes (e.g., "5 minutes", "2 minutes"), "Not Applicable", "Temporarily closed"

Confirmed live: Page returned current data with timestamps from today. Crossings like Pacific Highway showed "5 minutes" wait, most showed "No Delay".

## Freshness Assessment
Good. The page states wait times are "updated at least hourly" and timestamps confirm this. Major crossings like Niagara Falls and Pacific Highway appear to update every 15-30 minutes. Data is available 24/7 and reflects real-time conditions.

## Entity Model
- **Border Crossing** (CBSA office name, Canadian city/province, US city/state)
- **Wait Time** (commercial flow, traveller flow, as text: "No Delay" / "X minutes" / "Not Applicable" / "Temporarily closed")
- **Timestamp** (last updated, with timezone abbreviation)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Hourly updates, some crossings more frequent |
| Openness | 3 | Open Government Licence, fully public |
| Stability | 3 | Government of Canada, legally mandated |
| Structure | 1 | HTML table, requires parsing |
| Identifiers | 1 | Office names only, no formal IDs |
| Additive Value | 3 | Only source for Canada-side border waits |
| **Total** | **13/18** | |

## Notes
- Main limitation is HTML-only format — no REST API or structured data feed
- HTML table is well-structured and scrapable, but fragile to layout changes
- The CanBorder mobile app likely consumes a structured API that isn't publicly documented
- 29 crossings covers the major ones, but Canada has many more smaller crossings
- Pairing with US CBP data would give a complete picture of both directions
- Wait times are estimates and subject to sudden changes from enforcement actions
- The page explicitly links to CBP (US) data for the reverse direction
