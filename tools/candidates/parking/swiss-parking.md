# Swiss City Parking (Basel + Zürich via ParkenDD)

**Country/Region**: Switzerland — Basel, Zürich
**Publisher**: Kanton Basel-Stadt / Parkleitsystem Zürich, aggregated via ParkenDD
**API Endpoints**:
- Basel: `https://api.parkendd.de/Basel` and `https://data.bs.ch/api/explore/v2.1/catalog/datasets/100014/records`
- Zürich: `https://api.parkendd.de/Zuerich` (source: `http://www.pls-zh.ch/plsFeed/rss`)
**Documentation**: https://github.com/offenesdresden/ParkAPI
**Protocol**: REST
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Real-time (~5 minutes)
**License**: Open data (canton/city-level licenses)

## What It Provides

Real-time parking garage occupancy for two major Swiss cities. Basel publishes 14 parking garages with free/total space counts, and Zürich publishes 20+ garages. Both are accessible through the ParkenDD aggregator API (which normalizes data from many European cities) and through their native city data portals.

## API Details

**ParkenDD aggregated API (recommended):**
```
GET https://api.parkendd.de/Basel
GET https://api.parkendd.de/Zuerich
```

Returns normalized JSON:
```json
{
  "last_downloaded": "2026-04-06T12:00:00",
  "last_updated": "2026-04-06T12:00:00",
  "lots": [
    {
      "name": "City",
      "free": 872,
      "total": 1114,
      "state": "open",
      "address": "Schanzenstrasse 48",
      "coords": {"lat": 47.561101, "lng": 7.5824076},
      "lot_type": "Tiefgarage",
      "id": "city"
    }
  ]
}
```

**Basel native portal (Opendatasoft):**
```
GET https://data.bs.ch/api/explore/v2.1/catalog/datasets/100014/records?limit=100
```

Returns richer data including historical time series and additional metadata.

**Zürich native source:**
The Parkleitsystem Zürich feed at `http://www.pls-zh.ch/plsFeed/rss` provides the raw RSS/XML data that ParkenDD aggregates.

Key fields (ParkenDD):
- `name` — Garage name
- `free` — Available spaces
- `total` — Total capacity
- `state` — open/closed/nodata
- `coords` — Lat/lng coordinates
- `address` — Street address
- `lot_type` — Parking type (Tiefgarage = underground, Parkhaus = multi-story)

## Freshness Assessment

ParkenDD updates approximately every 5 minutes by scraping source feeds. Basel's native Opendatasoft portal provides more direct access with per-minute timestamps. Zürich's PLS feed updates as the parking guidance system detects changes. Both cities have well-functioning parking guidance systems that track entry/exit counts.

## Entity Model

- **Parking Garage**: Facility with name, address, coordinates, type
- **Availability**: Free spaces, total capacity, state (open/closed)
- **Metadata**: Lot type (underground, multi-story), operator

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time, ~5 minute updates |
| Openness | 3 | No auth, open data licenses |
| Stability | 3 | ParkenDD is well-maintained; city feeds are government-operated |
| Structure | 3 | Clean normalized JSON via ParkenDD; Opendatasoft for Basel |
| Identifiers | 2 | Name-based IDs in ParkenDD; more structured in native portals |
| Additive Value | 2 | Swiss coverage; demonstrates multi-source aggregation via ParkenDD |
| **Total** | **16/18** | |

## Notes

- Both Basel and Zürich are already covered by the ParkAPI/ParkenDD aggregator documented separately. This document details the Swiss-specific aspects.
- Basel's Opendatasoft portal (`data.bs.ch`) is the same platform as Ghent — confirming the Opendatasoft parking pattern applies across cities and countries.
- Zürich's PLS RSS feed is a raw data source. ParkenDD handles the XML-to-JSON normalization.
- Building a ParkAPI bridge (recommended approach #1 in the parking INDEX) automatically covers both Swiss cities plus 28+ others. No separate Swiss bridge needed.
