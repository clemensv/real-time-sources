# Spire Maritime / Kpler AIS 2.0

**Country/Region**: Global (HQ: San Francisco / Paris)
**Publisher**: Spire Global / Kpler (commercial maritime intelligence)
**API Endpoint**: `https://api.sml.kpler.com/graphql`
**Documentation**: https://documentation.spire.com/maritime-2-0/
**Protocol**: GraphQL (single endpoint)
**Auth**: Bearer token (commercial subscription required)
**Data Format**: JSON (GraphQL responses)
**Update Frequency**: Real-time (satellite + terrestrial AIS)
**License**: Commercial (paid plans, trial available)

## What It Provides

Spire Maritime (now branded as Kpler AIS 2.0) provides global AIS vessel tracking via both
satellite-based AIS (S-AIS) and terrestrial AIS receivers. This is one of the premier commercial
AIS data services, offering global ocean coverage that terrestrial-only sources cannot match.

Data includes:
- Real-time vessel positions (lat/lon, speed, course, heading, ROT, navigational status)
- Vessel static data (name, MMSI, IMO, callsign, ship type, flag, dimensions)
- Current voyage data (draught, destination, ETA)
- Historical tracks and port calls
- Predicted routes and ETAs (enriched/derived data)
- Collection type indicators (satellite vs terrestrial)

## API Details

GraphQL-based API with a single endpoint. Queries are POST requests with GraphQL query bodies.

Example query — vessel positions:
```graphql
query {
  vessels(imo: [9538907, 9726413]) {
    nodes {
      staticData {
        name
        mmsi
        imo
        callsign
        shipType
      }
      lastPositionUpdate {
        accuracy
        collectionType
        course
        heading
        speed
        latitude
        longitude
        timestamp
        updateTimestamp
        navigationalStatus
      }
      currentVoyage {
        draught
        destination
        eta
      }
    }
  }
}
```

Features:
- Query by MMSI, IMO, ship type, geographic area, time range
- Pagination with cursors (`first`, `after`)
- Parallel root queries (e.g., tankers + cargo in one request)
- Field-level selection (only fetch what you need)
- GraphQL playground at `https://api.sml.kpler.com/graphql`

Authentication:
```
POST https://api.sml.kpler.com/graphql
Authorization: Bearer <your_token>
```

Trial tokens available via request at https://spire.com/maritime/get-started/

## Freshness Assessment

Excellent. Spire operates a constellation of satellites for S-AIS reception, combined with
terrestrial AIS stations. This gives truly global coverage including open ocean areas where
terrestrial AIS cannot reach. Satellite revisit times mean positions may be minutes to hours old
in mid-ocean, but near-coast the terrestrial data provides second-level latency.

The `collectionType` field in responses indicates whether a position came from satellite or
terrestrial reception, which is valuable for assessing data age.

## Entity Model

Nested GraphQL schema:
- `vessels` → `nodes[]` → `staticData`, `lastPositionUpdate`, `currentVoyage`
- Static: `name`, `mmsi`, `imo`, `callsign`, `shipType`, `flag`, `dimensions`
- Position: `latitude`, `longitude`, `speed`, `course`, `heading`, `rot`, `accuracy`, `navigationalStatus`, `collectionType`, `timestamp`
- Voyage: `draught`, `destination`, `eta`

Identifiers: MMSI, IMO (both queryable), callsign.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | Satellite + terrestrial = global real-time coverage |
| Openness | 0 | Commercial subscription required, trial available |
| Stability | 3 | Enterprise-grade service, SLA-backed |
| Structure | 3 | GraphQL with introspection, typed schema, playground |
| Identifiers | 3 | MMSI, IMO, callsign, ship type, flag |
| Additive Value | 3 | Global satellite AIS — covers open ocean, unique value |

**Total: 15/18**

## Notes

- This is the gold standard for global AIS data, but it comes at a cost. Pricing is not public
  but is enterprise-level (thousands per month for meaningful data volumes).
- The GraphQL API is extremely well-designed — arguably the best-structured AIS API available.
- Satellite AIS data fills the critical gap that all terrestrial-only sources have: no open
  ocean coverage.
- A free trial is available, which could be useful for prototyping and evaluation.
- Formerly branded as "Spire Maritime API" — now part of Kpler's maritime intelligence platform
  after Kpler's acquisition of Spire's maritime business.
- Not suitable for open-data projects due to commercial licensing, but worth documenting as the
  benchmark for what a well-structured AIS API looks like.
