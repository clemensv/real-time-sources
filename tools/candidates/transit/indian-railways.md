# Indian Railways — Train Running Status

**Country/Region**: India
**Publisher**: Centre for Railway Information Systems (CRIS), Indian Railways
**API Endpoint**: Various — `indianrail.gov.in`, `enquiry.indianrail.gov.in` (official); `erail.in` (third-party)
**Documentation**: https://www.indianrail.gov.in/
**Protocol**: Web portal; mobile app backends; third-party APIs
**Auth**: Various (official API requires approval; third-party APIs require keys)
**Data Format**: HTML (official); JSON (third-party)
**Update Frequency**: Real-time (train positions update at each station stop)
**License**: Indian Railways data; third-party terms vary

## What It Provides

Indian Railways is the **world's 4th largest railway network** by size and **largest by daily ridership** — carrying 23 million passengers daily across 68,000+ km of track, with 13,000+ trains operating daily. The scale is staggering.

Real-time data available:
- **Train running status**: Current station, delay minutes, expected arrival times for all trains
- **PNR status**: Reservation status for booked tickets
- **Seat availability**: Real-time berth/seat availability across classes
- **Train schedules**: Timetable data for all 13,000+ trains
- **Coach position**: Physical coach order in train consist
- **Platform assignment**: Assigned platform at major stations

### Official API (CRIS)

Indian Railways' official API gateway was at `api.indianrailways.gov.in` — but this endpoint **failed to connect** during testing. The official API requires a formal application process through India's Open Government Data (OGD) platform.

### Third-Party APIs

Multiple third-party services provide real-time Indian Railways data:
- **RailwayAPI.com** (formerly IRCTC API) — Commercial API with running status, PNR, availability
- **eRail.in** — Popular Indian Railways information service with web data (returns HTML, not JSON API)
- **ConfirmTKT**, **RailYatri**, **ixigo** — Mobile apps with their own data layers

### Probe Results

- `api.indianrailways.gov.in` → Connection failed
- `realtime.indianrail.gov.in` → Connection failed
- `erail.in/data/get-train-route/12301` → Returns HTML (not a REST API)
- `indianrail.gov.in` → Website accessible (basic HTML, CRIS copyright)

## Entity Model

- **Train**: Identified by 5-digit train number (e.g., 12301 = Rajdhani Express)
- **Station**: 4-character station code (e.g., NDLS = New Delhi, HWH = Howrah)
- **PNR**: 10-digit booking reference
- **Coach**: Class code (1A, 2A, 3A, SL, CC, etc.) + coach number
- **Route**: Ordered list of stations with scheduled and actual times

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Train positions update at each stop; real-time delays tracked |
| Openness | 1 | Official API requires approval; third-party APIs are commercial |
| Stability | 2 | CRIS infrastructure is massive; API gateway appears unstable |
| Structure | 2 | Official API reportedly returns JSON; third-party APIs vary |
| Identifiers | 3 | 5-digit train numbers, 4-char station codes — well-established |
| Additive Value | 3 | World's largest rail network by ridership; 23M daily passengers |
| **Total** | **14/18** | |

## Integration Notes

- The official CRIS API requires formal approval through data.gov.in or railway board
- Third-party APIs (RailwayAPI.com) offer REST/JSON but are commercial ($50-200/month)
- Train numbers and station codes are stable, standardized identifiers
- Running status data maps well to GTFS-RT format (delay, position, arrival/departure)
- CloudEvents: one event per train-station arrival/departure with delay information
- The scale of 13,000+ daily trains generates enormous event volume
- Consider GTFS static schedule as baseline with real-time delay events as updates

## Verdict

Massive potential, difficult access. Indian Railways generates one of the world's largest streams of transit real-time data — 13,000+ trains, 23 million passengers daily. But the official API is unreliable and requires formal approval, while third-party APIs are commercial. The well-established identifier system (train numbers, station codes) and GTFS-compatible data structure make this technically feasible once API access is secured. Worth pursuing through official channels.
