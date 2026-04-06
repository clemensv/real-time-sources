# Datalastic Maritime API

**Country/Region**: Global (HQ: Germany, servers in Munich)
**Publisher**: Datalastic (commercial AIS data provider)
**API Endpoint**: `https://api.datalastic.com/api/v0/...`
**Documentation**: https://www.datalastic.com/api-reference/
**Protocol**: REST
**Auth**: API Key (paid subscription, free tier available)
**Data Format**: JSON
**Update Frequency**: Real-time AIS
**License**: Commercial (tiered pricing)

## What It Provides

Datalastic is a commercial maritime API provider offering real-time and historical AIS vessel
tracking data. The platform aggregates data from a global network of AIS receivers and provides
it through a REST API designed for integration into third-party applications.

Products:
- **Live Ship Tracker**: Real-time vessel location, ETA, destination, status
- **Location Tracking (Zone)**: Monitor a defined area, list all vessels
- **Port Data**: Global maritime port information
- **Static Ship Data**: Vessel descriptive information (type, capacity, dimensions)
- **Historical Data**: Vessel location/status history

## API Details

REST API with multiple endpoint groups:

| Endpoint Group | Description |
|---|---|
| Live Ship Tracker | Current vessel position by MMSI/IMO |
| Location Tracking | Vessels within a geographic zone |
| Port Finder | Port information and search |
| Static Ship Data | Vessel metadata (type, tonnage, etc.) |
| Historical Vessel Data | Historical positions, status, destination |

Authentication: API key passed as query parameter or header.

Getting started:
1. Choose a subscription plan at https://www.datalastic.com/pricing/
2. Subscribe and receive API key by email
3. Include key in API requests

The API supports a comprehensive vessel type taxonomy — the documentation lists hundreds of
specific vessel types (from "Crude Oil Tanker" to "Inland, Pushtow, nine or more barges"),
far more granular than standard AIS type codes.

Data fields include standard AIS data plus enriched vessel characteristics like detailed
vessel type classification, year built, carrying capacity, etc.

Server uptime: 99.8% (2024 reported).

## Freshness Assessment

Good for real-time tracking in terrestrial-covered areas. Datalastic operates its own AIS
receiver stations ("AIS towers") and aggregates additional community feeds. The live tracking
endpoint provides current positions. Historical data is also available for retrospective analysis.

## Entity Model

Vessel records:
- MMSI, IMO, name, callsign
- Vessel type (detailed taxonomy with hundreds of specific types)
- Position (lat/lon, course, speed, heading)
- Navigational status
- Destination, ETA, draught
- Vessel dimensions and characteristics

Port records:
- Port name, location, timezone

CSV static data exports available for bulk vessel/port databases.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 2 | Real-time terrestrial AIS, coverage varies |
| Openness | 1 | Paid commercial service (free tier may exist) |
| Stability | 2 | 99.8% uptime claimed, commercial service |
| Structure | 2 | REST API, extensive type taxonomy, but limited public docs |
| Identifiers | 3 | MMSI, IMO, detailed vessel types |
| Additive Value | 2 | Detailed vessel type taxonomy is unique value-add |

**Total: 12/18**

## Notes

- The standout feature is the extraordinarily detailed vessel type taxonomy — hundreds of
  specific types that go far beyond the ~100 standard AIS type codes. This could be valuable
  for vessel classification use cases.
- Like most commercial AIS providers, the pricing is not transparent (must subscribe to see).
- The "AIS tower" infrastructure suggests they operate their own receiving stations rather than
  relying entirely on community feeds.
- CSV exports for static vessel data could be useful for building a reference database.
- Munich-based servers suggest GDPR compliance and European data residency.
- Worth evaluating if the free tier provides sufficient access for prototyping.
