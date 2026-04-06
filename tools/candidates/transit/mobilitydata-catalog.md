# MobilityData GTFS-RT Feed Catalog & Quality

**Country/Region**: Global
**Publisher**: MobilityData (non-profit maintaining GTFS/GTFS-RT specifications)
**API Endpoint**: https://database.mobilitydata.org/ (Mobility Database Catalog)
**Documentation**: https://mobilitydata.org/ and https://gtfs.org/
**Protocol**: N/A — this is a meta-catalog of feeds, not a data source
**Auth**: Open access (catalog is publicly browsable; API access via GitHub)
**Data Format**: CSV catalog + individual feeds in various formats
**Update Frequency**: Catalog updated continuously via community contributions
**License**: Apache 2.0 (catalog); individual feeds carry their own licenses

## What It Provides

MobilityData maintains the official GTFS and GTFS-RT specifications and operates the Mobility Database — the world's most comprehensive catalog of transit data feeds:

- **2,200+ GTFS feeds** globally — schedule data
- **800+ GTFS-RT feeds** — real-time trip updates, vehicle positions, service alerts
- **Feed quality metrics**: which feeds pass validation, common errors, update frequency
- **Feed metadata**: operator name, country, bounding box, authentication requirements

The catalog is the canonical reference for which transit agencies worldwide publish GTFS-RT and how to access their feeds.

## Catalog Details

### Mobility Database

The catalog is available as:
- **Web interface**: https://database.mobilitydata.org/ — searchable, filterable
- **CSV download**: https://github.com/MobilityData/mobility-database-catalogs — full catalog as CSV files
- **API**: programmatic access via the database

Each feed entry includes:
- `provider` — agency name
- `feed_url` — direct URL to the GTFS/GTFS-RT feed
- `data_type` — gtfs, gtfs-rt
- `location.country_code` — ISO country code
- `location.bounding_box` — geographic bounds
- `authentication_type` — none, api_key, http_header
- `status` — active, deprecated, inactive

### Highest-Quality GTFS-RT Feeds (Assessment)

Based on the catalog and community knowledge, the highest-quality open GTFS-RT feeds include:

| Agency | Country | Auth | Modes | Notes |
|--------|---------|------|-------|-------|
| MBTA (Boston) | US | API key | All | Also has SSE streaming |
| TriMet (Portland) | US | API key | Bus/Rail | Long-running, well-maintained |
| BART (San Francisco) | US | None | Rail | Simple, reliable |
| TfNSW (Sydney) | AU | API key | All | Massive, comprehensive |
| BKK (Budapest) | HU | None | All | Open, no auth |
| Entur (Norway) | NO | None | All | National, also SIRI |
| HSL (Helsinki) | FI | API key | All | Excellent quality |
| King County Metro (Seattle) | US | None | Bus | Clean, simple |
| WMATA (DC) | US | API key | Bus/Rail | Major US city |
| LA Metro | US | API key | Bus/Rail | Large US system |

### GTFS-RT Validation

MobilityData maintains the official [GTFS-RT Validator](https://github.com/MobilityData/gtfs-realtime-validator) — an open-source tool that checks feed compliance. Common quality issues across feeds:
- Missing `trip_id` or `route_id` references
- Timestamps in the past
- Missing `vehicle.id`
- Stop sequence gaps

## Freshness Assessment

N/A — this is a meta-catalog. The catalog itself is well-maintained. Feed quality varies enormously — from agencies with 100% GTFS-RT compliance and 10-second update intervals to agencies publishing stale or broken feeds.

## Entity Model

- **Feed**: unique ID, provider, URL, data type, location, authentication, status
- **Operator**: name, associated feeds, website, location
- Each feed links to actual GTFS-RT endpoints that follow the standard GTFS-RT entity model (TripUpdate, VehiclePosition, Alert)

## Feasibility Rating

| Criterion       | Score | Notes                                                        |
|-----------------|-------|--------------------------------------------------------------|
| Freshness       | 1     | Meta-catalog, not a real-time source                          |
| Openness        | 3     | Fully open catalog; Apache 2.0 licensed                       |
| Stability       | 3     | Maintained by the GTFS spec organization                      |
| Structure       | 3     | Clean CSV/JSON catalog; well-defined schema                   |
| Identifiers     | 2     | MobilityData IDs; links to agency GTFS IDs                    |
| Additive Value  | 3     | Essential discovery tool for the GTFS-RT bridge               |
| **Total**       | **15/18** |                                                           |

## Notes

- MobilityData's catalog is the single most valuable resource for automating GTFS-RT bridge deployment — it tells you where every feed is, what auth it needs, and what geography it covers.
- The GitHub-based catalog (mobility-database-catalogs) can be consumed programmatically: clone the repo, parse the CSV, and auto-configure GTFS-RT bridge instances for hundreds of agencies.
- MobilityData also maintains the GTFS Canonical Validator, GTFS Schedule Best Practices, and the GTFS-RT Best Practices — quality guidance for feed producers.
- The organization is based in Montreal and funded by a consortium of transit agencies, tech companies, and governments — it's the neutral standard body for GTFS.
- For this project, the catalog's value is as a configuration source: "which feeds should the GTFS-RT bridge connect to?" The catalog answers that question for the entire world.
