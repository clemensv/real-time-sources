# Digitransit — Finland National Journey Planner

**Country/Region**: Finland (national, with focus on Helsinki HSL region)
**Publisher**: Fintraffic / HSL (Helsinki Region Transport) / Waltti
**API Endpoint**: `https://api.digitransit.fi/routing/v2/hsl/gtfs/v1` (HSL), `https://api.digitransit.fi/routing/v2/finland/gtfs/v1` (national)
**Documentation**: https://digitransit.fi/en/developers/
**Protocol**: OpenTripPlanner 2 GraphQL + GTFS-RT
**Auth**: API key required (free registration via Azure API Management portal)
**Data Format**: JSON (GraphQL), Protobuf (GTFS-RT)
**Update Frequency**: Real-time — GTFS-RT feeds updated every 15–30 s; GraphQL queries reflect real-time
**License**: Open data (various Finnish open data licenses; source code EUPL v1.2 / AGPLv3)

## What It Provides

Digitransit is Finland's open-source national journey planning platform, built on OpenTripPlanner 2. It covers:

- **HSL (Helsinki Region Transport)**: metro, tram, bus, commuter rail, ferry — real-time for all modes
- **Waltti regions**: bus networks in Tampere, Turku, Oulu, Jyväskylä, Lahti, Kuopio, Joensuu, and more
- **National long-distance**: VR (Finnish Railways) trains, Matkahuolto coaches
- **Åland**: ferry services

Real-time data includes trip updates (delays, cancellations), vehicle positions, and service alerts across all covered operators.

## API Details

### GraphQL (OTP2)

The primary API is an OpenTripPlanner 2 GraphQL endpoint. Multiple router instances exist:

- `/routing/v2/hsl/gtfs/v1` — HSL region (Helsinki, Espoo, Vantaa, etc.)
- `/routing/v2/waltti/gtfs/v1` — Waltti cities
- `/routing/v2/finland/gtfs/v1` — national (all operators)

GraphQL queries support:
- Departure boards at stops (`stop { stoptimesForPatterns { ... } }`)
- Journey planning with real-time (`plan { itineraries { ... } }`)
- Alerts and disruptions
- Stop/station search

### GTFS-RT

GTFS-RT protobuf feeds are published separately (previously on `cdn.digitransit.fi`, now behind API management):
- Trip Updates, Vehicle Positions, Service Alerts per region
- HSL GTFS-RT is the highest-quality feed — covers ~1,500 vehicles in real-time

### Authentication

Since ~2023, Digitransit moved behind Azure API Management. Registration is free but required. The subscription key goes in a `digitransit-subscription-key` header.

## Freshness Assessment

Good to excellent. HSL has one of the best real-time implementations in Europe — GPS positions for virtually every bus, tram, metro, and commuter train in the Helsinki region. VR trains have real-time tracking. Waltti city feeds vary in quality but are generally solid. The OTP2 GraphQL API merges real-time with scheduled data seamlessly.

## Entity Model

- **StopTime**: scheduled and real-time arrival/departure at a stop, delay, uncertainty
- **Trip**: route pattern instance with real-time status
- **Alert**: GTFS-RT alert mapped to routes, stops, or agencies
- **Pattern**: ordered sequence of stops for a route variant
- **Stop / Station**: with coordinates, zone, platform information
- **VehiclePosition**: lat/lon, bearing, speed, trip reference, occupancy status
- GTFS-compatible IDs throughout (HSL uses `HSL:` prefixed IDs)

## Feasibility Rating

| Criterion       | Score | Notes                                                        |
|-----------------|-------|--------------------------------------------------------------|
| Freshness       | 3     | Excellent real-time coverage, especially HSL Helsinki         |
| Openness        | 2     | Free API key required — registration adds slight friction     |
| Stability       | 3     | Backed by Fintraffic/HSL government agencies; long-running    |
| Structure       | 3     | OTP2 GraphQL + standard GTFS-RT — well-structured             |
| Identifiers     | 3     | GTFS-compatible, standardized Finnish stop/route IDs          |
| Additive Value  | 2     | GTFS-RT feeds coverable by existing bridge; GraphQL adds value|
| **Total**       | **16/18** |                                                           |

## Notes

- The Digitransit platform itself is fully open source (https://github.com/HSLdevcom/) — you can run your own instance.
- HSL also publishes a high-frequency MQTT stream of vehicle positions (mqtt.hsl.fi) — real-time GPS at ~1 s intervals for all Helsinki transit vehicles. This is architecturally interesting as a push-based source.
- The MQTT topic structure is `hsl/v2/{transport_mode}/{vehicle_id}` — clean, semantic, and high-volume.
- The GraphQL API is essentially OTP2's standard API — any OTP2-based system (Entur, Digitransit, others) shares the same query language.
- Finland's transit data quality is among the highest in Europe — consistent GTFS, excellent real-time, good accessibility data.
