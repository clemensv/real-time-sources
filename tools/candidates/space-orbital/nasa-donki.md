# NASA DONKI (Space Weather Database of Notifications, Knowledge, Information)

**Country/Region**: Global
**Publisher**: NASA / CCMC (Community Coordinated Modeling Center)
**API Endpoint**: `https://api.nasa.gov/DONKI/`
**Documentation**: https://ccmc.gsfc.nasa.gov/donki/, https://api.nasa.gov/
**Protocol**: REST
**Auth**: API Key (free, `DEMO_KEY` available for testing)
**Data Format**: JSON
**Update Frequency**: Event-driven (events added as they occur; data within hours of detection)
**License**: US Government public domain

## What It Provides

DONKI is NASA's space weather event database providing structured records of solar and geomagnetic events. It covers solar flares (FLR), coronal mass ejections (CME), geomagnetic storms (GST), interplanetary shocks (IPS), solar energetic particles (SEP), magnetopause crossings (MPC), radiation belt enhancement (RBE), and high-speed streams (HSS). Each event includes timing, classification, source location, instruments, linked events, and notification history.

Live probe confirmed working API: returned solar flare events for Jan 1-7, 2024, with detailed records including flare class (M2.3, M4.7, M1.1), source locations (N03E70), active region numbers (13536), instruments (GOES-P: EXIS), and linked events (CME associations).

## API Details

- **Base URL**: `https://api.nasa.gov/DONKI/{event_type}?startDate={date}&endDate={date}&api_key={key}`
- **Event types**: `FLR` (flares), `CME` (coronal mass ejections), `CMEAnalysis`, `GST` (geomagnetic storms), `IPS` (interplanetary shocks), `SEP` (solar energetic particles), `MPC` (magnetopause crossings), `RBE` (radiation belt enhancement), `HSS` (high-speed streams), `WSAEnlilSimulations`, `notifications`
- **Parameters**: `startDate`, `endDate` (YYYY-MM-DD), `api_key`
- **DEMO_KEY**: Rate limited to 30 req/hour, 50 req/day
- **Registered key**: 1000 req/hour (free at https://api.nasa.gov)
- **Event fields**: Event-type specific ID, catalog, instruments, begin/peak/end times, classification, source location, active region, notes, linked events, version history
- **Linked events**: Cross-references between event types (e.g., a flare linked to a CME)

## Freshness Assessment

Events are added to DONKI within hours of detection by space weather instruments. For major events (X-class flares, Earth-directed CMEs), entries appear rapidly. The database is actively maintained by the CCMC team with versioned records. Historical data goes back to the start of Solar Cycle 24 (~2010).

## Entity Model

- **Event**: Typed by category (FLR, CME, GST, etc.), with unique ID (e.g., `2024-01-01T08:33:00-FLR-001`)
- **Instrument**: Detecting instrument (e.g., GOES-P: EXIS, SOHO: LASCO C2)
- **Active Region**: NOAA active region number (e.g., 13536)
- **Linked Event**: Cross-reference by activity ID to related events
- **Notification**: Alert record with message body and send time

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Events added within hours; not real-time telemetry |
| Openness | 3 | DEMO_KEY available; free registered keys; US Gov public domain |
| Stability | 3 | NASA/CCMC operated; production infrastructure |
| Structure | 3 | Clean JSON; well-documented event types and relationships |
| Identifiers | 3 | Typed event IDs with timestamps; cross-linked events |
| Additive Value | 3 | Unique structured space weather event database |
| **Total** | **17/18** | |

## Notes

- DONKI is the authoritative database for space weather events. No other source provides this breadth of structured solar/geomagnetic event data.
- The `linkedEvents` field is powerful — it connects solar flares to CMEs to geomagnetic storms, forming event chains.
- DEMO_KEY is sufficient for testing but register a free key for production use.
- Event IDs encode the event time and type, making them self-describing.
- The `notifications` endpoint provides the actual alert messages sent to subscribers.
