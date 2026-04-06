# US CBP Border Wait Times
**Country/Region**: United States (land border crossings with Mexico and Canada)
**Publisher**: US Customs and Border Protection (CBP)
**API Endpoint**: `https://bwt.cbp.gov/api/bwtnew`
**Documentation**: https://bwt.cbp.gov/ (no formal API documentation, but REST endpoint confirmed)
**Protocol**: REST/JSON
**Auth**: None (public)
**Data Format**: JSON
**Update Frequency**: Approximately every hour (timestamps per port)
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
- **All ports**: `GET https://bwt.cbp.gov/api/bwtnew` — returns JSON array of all 81 ports
- **Specific port**: `GET https://bwt.cbp.gov/api/bwtnew?port={port_number}` (e.g., `?port=250601` for San Ysidro)
- **Web application**: `https://bwt.cbp.gov/` — Angular SPA (uses the same backend API)
- **CORS**: Enabled (Access-Control-Allow-Origin: *)
- **Response fields per port**:
  - `port_number`, `port_name`, `border` (Canadian/Mexican), `crossing_name`, `hours`, `port_status`
  - `date`, `time` — last update timestamp
  - `commercial_vehicle_lanes` — maximum_lanes, standard_lanes (delay_minutes, lanes_open), FAST_lanes
  - `passenger_vehicle_lanes` — maximum_lanes, standard_lanes, NEXUS_SENTRI_lanes, ready_lanes
  - `pedestrian_lanes` — maximum_lanes, standard_lanes, ready_lanes
  - Each lane type includes: update_time, operational_status, delay_minutes, lanes_open
- **XML feed (legacy)**: `https://bwt.cbp.gov/xml/bwt.xml` — may still be available

Note: The REST API at `bwt.cbp.gov/api/bwtnew` was confirmed working during probing, returning a JSON array of 81 ports with detailed lane-level wait time data, CORS headers, and no authentication required.

## Freshness Assessment
Good. Wait times are updated approximately every hour at most ports. Some major ports update more frequently. The data is based on actual measured wait times or estimates from CBP officers at each port. Timestamps per port confirm independent update schedules.

## Entity Model
- **Port of Entry** (port number, name, state, border (Canada/Mexico), crossing name)
- **Wait Time** (passenger vehicles, pedestrians, commercial, by lane type)
- **Lane Type** (Standard, SENTRI, NEXUS, Ready Lane, FAST)
- **Status** (open, closed, time of last update)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Hourly updates, per-port timestamps |
| Openness | 3 | Public REST API confirmed, no auth, CORS enabled |
| Stability | 3 | US Government, CBP official service |
| Structure | 3 | Clean JSON with nested lane-level detail |
| Identifiers | 3 | Port numbers are stable federal identifiers |
| Additive Value | 3 | Only source for US border wait times |
| **Total** | **17/18** | |

## Notes
- The `bwt.cbp.gov/api/bwtnew` endpoint returns clean JSON with 81 ports — no scraping needed
- Both US-Canada and US-Mexico borders covered in one API call
- CORS enabled — direct browser integration possible
- Lane-level detail includes standard, FAST, NEXUS/SENTRI, and Ready Lane wait times
- CBP port numbers are standardized identifiers usable across government systems
- Wait time accuracy varies — they are estimates, not precise measurements
- Consider pairing with CBSA (Canadian) data for complete border picture
