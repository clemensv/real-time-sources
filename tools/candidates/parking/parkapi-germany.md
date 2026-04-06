# ParkAPI (ParkenDD)

**Country/Region**: Germany + Europe (30+ cities)
**Publisher**: Open-source community (offenesdresden / jdemaeyer)
**API Endpoint**: `https://api.parkendd.de/`
**Documentation**: https://github.com/offenesdresden/ParkAPI
**Protocol**: REST
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Real-time (scrapes upstream sources continuously)
**License**: MIT (API software); individual city data licenses vary

## What It Provides

ParkAPI (formerly ParkenDD) is an open-source aggregator that provides real-time parking garage occupancy data for 30+ cities, primarily in Germany but also including cities like Zürich, Basel, and Aarhus. It scrapes and normalizes parking data from individual city parking guidance systems into a single, consistent API.

## API Details

**City index:**
```
GET https://api.parkendd.de/
```
Returns a JSON object with all supported cities, their coordinates, data sources, and attribution.

**City parking data:**
```
GET https://api.parkendd.de/{CityName}
```
Returns real-time lot data:
```json
{
  "lots": [
    {
      "id": "dresdenaltmarkt",
      "name": "Altmarkt",
      "coords": {"lat": 51.0495, "lng": 13.7379},
      "total": 400,
      "free": 156,
      "state": "open",
      "lot_type": "garage",
      "forecast": false
    }
  ],
  "last_downloaded": "2026-04-06T10:30:00",
  "last_updated": "2026-04-06T10:28:00"
}
```

Supported cities include:
- **Germany**: Aachen, Bonn, Dortmund, Dresden, Freiburg, Hamburg, Heidelberg, Ingolstadt, Kaiserslautern, Karlsruhe, Köln, Konstanz, Lübeck, Magdeburg, Mannheim, Münster, Nürnberg, Oldenburg, Regensburg, Rosenheim, Ulm, Wiesbaden
- **Switzerland**: Zürich, Basel
- **Denmark**: Aarhus

Each city entry includes `source` (upstream data URL), `attribution`, and `active_support` flag.

## Freshness Assessment

ParkAPI continuously scrapes upstream parking guidance systems. The `last_downloaded` and `last_updated` timestamps indicate when data was last fetched and when the upstream source last changed. Typical update intervals are 1–5 minutes, matching the upstream parking guidance systems. Real-time for practical purposes.

## Entity Model

- **City**: A supported city with coordinates, source, attribution
- **Lot**: A parking garage/lot with name, coordinates, type (garage, lot, underground)
- **Availability**: Total capacity, free spaces, occupancy state (open, closed, nodata, unknown)
- **Metadata**: Forecast availability flag, lot type, address

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time scraping, 1–5 minute updates |
| Openness | 3 | No auth, no registration, fully open API |
| Stability | 2 | Community-maintained; some city scrapers break when upstream changes |
| Structure | 3 | Clean, consistent JSON schema across all cities |
| Identifiers | 2 | City-specific lot IDs, not globally unique; no standard identifiers |
| Additive Value | 3 | 30+ cities from one API — massive value as an aggregator |
| **Total** | **16/18** | |

## Notes

- ParkAPI is the single best source for multi-city parking data in Germany. One API, 30+ cities, normalized schema. Exactly the kind of aggregator that's ideal for a bridge.
- Some city scrapers have `active_support: false`, meaning they may be unreliable or broken. Focus on actively supported cities.
- The upstream data sources vary widely: WFS services, HTML scraping, RSS feeds, proprietary APIs. ParkAPI abstracts all of this.
- Zürich data comes from the PLS Zürich AG parking guidance system (CC-0 license).
- A new version (ParkAPI v2/v3) exists at https://github.com/ParkenDD/parkapi-sources-v3 with a more modular architecture.
