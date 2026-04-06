# Transitland — Global Transit Data Aggregator

**Country/Region**: Global (coverage across 60+ countries)
**Publisher**: Interline Technologies (maintainer of Transitland)
**API Endpoint**: `https://transit.land/api/v2/rest/` (REST), `https://transit.land/api/v2/query` (GraphQL)
**Documentation**: https://www.transit.land/documentation
**Protocol**: REST/JSON + GraphQL
**Auth**: API key required (free tier available; paid plans for higher usage)
**Data Format**: JSON
**Update Frequency**: Varies — aggregates static GTFS data; some feeds have real-time metadata
**License**: Varies per feed (Transitland itself is open source; individual feeds carry their own licenses)

## What It Provides

Transitland is the largest open index of transit data feeds in the world. It doesn't produce transit data — it catalogues, validates, and serves data from thousands of transit agencies globally:

- **Feed Directory**: 2,500+ GTFS feeds from 60+ countries — searchable, validated, with metadata
- **Operator Index**: structured data about transit operators, their feeds, relationships, and coverage areas
- **Route and Stop Data**: aggregated static GTFS data queryable via REST or GraphQL
- **Feed Health Monitoring**: tracks feed freshness, validation errors, update frequency
- **Historical Data**: archived feed versions over time

The platform is built on the open-source [transitland-lib](https://github.com/interline-io/transitland-lib) and the community-maintained [Transitland Atlas](https://github.com/transitland/transitland-atlas) (a Git repository of feed URLs and operator metadata).

## API Details

### REST API

- `GET /feeds?limit=10` — list feeds
- `GET /feeds?spec=gtfs-rt` — filter to GTFS-RT feeds
- `GET /operators?search=Tokyo` — search operators
- `GET /routes?operator_onestop_id={id}` — routes for an operator
- `GET /stops?lon=-73.98&lat=40.76&radius=500` — stops near a point

API key goes in `apikey` query parameter or header.

### GraphQL API

- Full query flexibility: feeds, operators, routes, stops, trips, departures
- Supports complex joins and nested queries
- Paid tier only

### Transitland Atlas (Open Source)

The feed directory itself is an open-source Git repository:
- https://github.com/transitland/transitland-atlas
- DMFR (Distributed Mobility Feed Registry) format — JSON files describing feeds
- Community contributions welcome — anyone can add a feed via pull request

## Freshness Assessment

Mixed — depends on use case. As a feed directory, Transitland is excellent and continuously updated. It tracks which agencies publish GTFS-RT (real-time) feeds and provides their URLs. However, Transitland itself does not proxy or serve real-time GTFS-RT data — it points you to the source feeds. The static GTFS data served through the API is typically within one feed-version of current (updated when agencies publish new feeds).

## Entity Model

- **Feed**: onestop_id, spec (gtfs/gtfs-rt), url, authorization info, license, last_fetched, last_successful_fetch
- **Operator**: onestop_id, name, short_name, website, associated_feeds, places_served
- **Route**: onestop_id, route_short_name, route_long_name, route_type, operator, geometry
- **Stop**: onestop_id, stop_name, coordinates, served_by_routes
- **OnestopID**: Transitland's globally unique identifier system for stops, routes, operators, feeds

## Feasibility Rating

| Criterion       | Score | Notes                                                        |
|-----------------|-------|--------------------------------------------------------------|
| Freshness       | 1     | Directory of feeds, not a real-time data source itself        |
| Openness        | 2     | Free tier with rate limits; Atlas is fully open source        |
| Stability       | 3     | Long-running, well-maintained, community-backed               |
| Structure       | 3     | Clean REST/GraphQL; OnestopID system is well-designed         |
| Identifiers     | 3     | OnestopID provides global unique identifiers for transit entities|
| Additive Value  | 3     | Meta-source — indexes GTFS-RT feeds for the GTFS-RT bridge to consume|
| **Total**       | **15/18** |                                                           |

## Notes

- Transitland's primary value for this project is as a **feed discovery service** — it knows which agencies worldwide publish GTFS-RT and where their feed URLs are. This is enormously useful for the existing GTFS-RT bridge.
- The Transitland Atlas (open-source Git repo) could be used to auto-discover and configure GTFS-RT bridge instances for hundreds of agencies.
- OnestopID is an elegant global identifier system: `o-9q9-caltrain` (operator), `r-9q9-local` (route), `s-9q9-embarcadero` (stop) — using geohash-based prefixes.
- Transitland also tracks which feeds require API keys and what their license terms are — metadata that helps automate bridge deployment.
- The GraphQL API is the most powerful way to query the data but requires a paid plan.
- Interline Technologies (the company behind Transitland) also offers commercial products built on the same data.
