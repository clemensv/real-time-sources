# Trafiklab / Samtrafiken SIRI Regional

**Country/Region**: Sweden
**Publisher**: Samtrafiken / Trafiklab (Swedish public transport data platform)
**API Endpoint**: `https://opendata.samtrafiken.se/siri/{operator}/{datatype}?key={API_KEY}`
**Documentation**: https://www.trafiklab.se/api/netex-datasets/netex-regional/
**Protocol**: SIRI 2.0 (Norwegian/Nordic profile v1.1)
**Auth**: API Key (free registration at trafiklab.se)
**Data Format**: XML (SIRI 2.0)
**Update Frequency**: Real-time — updates per vehicle journey change; polling recommended every 15–60 s
**License**: CC0 1.0 Universal (Public Domain)

## What It Provides

Sweden's national public transport data platform publishes real-time data for most Swedish transit operators in both GTFS-RT and SIRI formats. The SIRI feed — the NeTEx/SIRI Regional dataset — provides:

- **SIRI-ET (Estimated Timetable)**: real-time delays, cancellations, extra departures, detours
- **SIRI-SX (Situation Exchange)**: disruption messages, textual descriptions of service changes
- **SIRI-VM (Vehicle Monitoring)**: vehicle positions and progress against timetable

Coverage includes major operators: SL (Stockholm), Skånetrafiken, Östgötatrafiken, UL (Uppsala), and many more — over 20 regional operators with real-time data.

## API Details

The SIRI feed follows the Norwegian SIRI Profile based on SIRI 2.0. Endpoints per operator and data type:

- `GET /siri/{operator}/et?key=...` — Estimated Timetable
- `GET /siri/{operator}/sx?key=...` — Situation Exchange
- `GET /siri/{operator}/vm?key=...` — Vehicle Monitoring

Rate limits vary by key tier:
- Bronze: 50 calls/min, 30K calls/month
- Silver: 250 calls/min, 2M calls/month
- Gold: 500 calls/min, 22.5M calls/month

Static NeTEx data provides the reference model — line definitions, stop places, timetables — against which the SIRI real-time data is resolved. Operators are identified by short codes (`sl`, `skane`, `otraf`, etc.).

The SIRI XML uses standard SIRI 2.0 elements: `EstimatedVehicleJourney`, `EstimatedCall`, `MonitoredVehicleJourney`, `PtSituationElement`.

## Freshness Assessment

Good to excellent. Real-time coverage varies by operator — Stockholm (SL), Skåne, and Östergötland have full ET+VM+SX; some smaller operators only provide static data. Updates are typically every 15–30 seconds for active vehicles.

## Entity Model

- **EstimatedVehicleJourney** (ET): trip with estimated arrival/departure at each call
- **MonitoredVehicleJourney** (VM): vehicle position, bearing, delay, route progress
- **PtSituationElement** (SX): disruption with affected stops/lines, validity period, text
- References NeTEx static data via `DatedVehicleJourneyRef`, `StopPointRef`, `LineRef`

## Feasibility Rating

| Criterion       | Score | Notes                                                       |
|-----------------|-------|-------------------------------------------------------------|
| Freshness       | 3     | Real-time ET/VM/SX for major operators                      |
| Openness        | 3     | CC0 license, free API key, generous rate limits              |
| Stability       | 3     | National platform backed by Samtrafiken; stable for years    |
| Structure       | 3     | SIRI 2.0 Nordic Profile — well-documented, schema-validated |
| Identifiers     | 3     | NeTEx/NaPTAN-style stop IDs, standardized line/operator refs |
| Additive Value  | 3     | Native SIRI — complements GTFS-RT bridge nicely              |
| **Total**       | **18/18** |                                                          |

## Notes

- The Oxyfi WebSocket API (`wss://api.oxyfi.com/trainpos/listen`) is a separate, complementary feed providing raw GPS positions of Swedish trains at 1 Hz — NMEA format over WebSocket. Could be a separate candidate.
- Trafiklab also offers GTFS-RT feeds (GTFS Regional), but the SIRI feeds carry richer data (occupancy, detailed stop-level estimates) and are the canonical format.
- The Nordic SIRI Profile is documented by Entur (Norway) and shared across Scandinavian countries.
- Perfect test case for a SIRI protocol bridge since it covers ET, VM, and SX — all three major SIRI services.
