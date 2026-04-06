# MTA New York City (GTFS-RT High-Volume Feeds)

**Country/Region**: United States (New York City)
**Publisher**: Metropolitan Transportation Authority (MTA)
**API Endpoint**: `https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2F{feed_id}`
**Documentation**: https://new.mta.info/developers (registration required)
**Protocol**: GTFS-RT (Protobuf)
**Auth**: API Key (free registration)
**Data Format**: Protocol Buffers (GTFS-RT)
**Update Frequency**: Every 15–30 seconds per feed
**License**: MTA Developer License Agreement (free, attribution required)

## What It Provides

The MTA operates the largest transit system in North America. Its GTFS-RT feeds provide real-time data for:

- **NYC Subway** — 472 stations, 27 lines, ~5.5 million weekday riders
  - Multiple feeds by line group (1-7, A-G, J/Z, L, N/Q/R/W, S, SIR)
  - Trip updates (arrival/departure predictions)
  - Vehicle positions
  - Alerts
- **NYC Bus** — 300+ routes via MTA Bus Time (SIRI and GTFS-RT)
- **Long Island Rail Road (LIRR)** — GTFS-RT
- **Metro-North Railroad** — GTFS-RT

The NYC Subway feeds are among the highest-volume GTFS-RT streams in the world — hundreds of trains in motion at any time, each reporting multiple upcoming stop predictions.

## API Details

Subway GTFS-RT feeds (protobuf):
- Feed 1: Lines 1, 2, 3, 4, 5, 6, 7
- Feed 26: Lines A, C, E
- Feed 21: Lines B, D, F, M
- Feed 16: Lines N, Q, R, W
- Feed 36: Lines J, Z
- Feed 2: Line L
- Feed 11: Line SIR (Staten Island Railway)
- Feed 51: Combined alerts

Each feed returns standard GTFS-RT `FeedMessage` containing `TripUpdate` and `VehiclePosition` entities.

Bus (SIRI):
- `http://bustime.mta.info/api/siri/vehicle-monitoring.json?key={key}&LineRef={route}`
- `http://bustime.mta.info/api/siri/stop-monitoring.json?key={key}&MonitoringRef={stop}`

LIRR and Metro-North: separate GTFS-RT endpoints via the same API infrastructure.

## Freshness Assessment

Excellent. Subway feeds update every 15–30 seconds. Bus SIRI feeds are real-time. The sheer volume makes these feeds a stress test for any consumer — a single subway feed snapshot can contain thousands of TripUpdate entities.

## Entity Model

- Standard GTFS-RT entities: `TripUpdate`, `StopTimeUpdate`, `VehiclePosition`, `Alert`
- Trip IDs reference MTA's GTFS static data
- Stop IDs are MTA station complex codes (e.g., `127N` for Times Sq–42 St northbound)
- Route IDs: single-character subway line identifiers
- MTA uses GTFS-RT extensions for NYC-specific fields (direction, assigned flag)
- Bus SIRI uses standard SIRI-VM and SIRI-SM elements with MTA-specific operator refs

## Feasibility Rating

| Criterion       | Score | Notes                                                        |
|-----------------|-------|--------------------------------------------------------------|
| Freshness       | 3     | 15–30 s updates, massive throughput                          |
| Openness        | 2     | Free but requires registration and license agreement          |
| Stability       | 3     | Critical infrastructure, feeds running for 10+ years          |
| Structure       | 3     | Standard GTFS-RT (protobuf) + SIRI for buses                 |
| Identifiers     | 2     | MTA-specific stop/trip IDs; require MTA GTFS for resolution   |
| Additive Value  | 1     | GTFS-RT already covered by generic bridge; value is scale     |
| **Total**       | **14/18** |                                                           |

## Notes

- While the existing GTFS-RT bridge already handles this protocol, the MTA feeds are worth calling out because of their extraordinary volume — they're a natural "flagship deployment" of the bridge.
- The bus SIRI feeds (via BusTime) are an independent SIRI-VM/SM source — these would NOT be covered by the GTFS-RT bridge and are a separate integration.
- MTA has been modernizing their feeds — newer feeds include vehicle positions that older subway feeds lacked.
- The feed numbering scheme is MTA-specific and not documented in an obvious API catalog — you need to know the feed IDs.
- MTA also provides a "BusTime" SIRI API which is architecturally interesting — one of the few SIRI deployments in the US.
- Combined with MBTA, this gives excellent US coverage for a demo.
