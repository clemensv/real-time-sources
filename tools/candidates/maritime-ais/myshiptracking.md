# MyShipTracking API

**Country/Region**: Global (terrestrial AIS coverage, Greece-based)
**Publisher**: MyShipTracking.com
**API Endpoint**: `https://api.myshiptracking.com/api/v1/...`
**Documentation**: https://api.myshiptracking.com/
**Protocol**: REST
**Auth**: API Key + Secret Key (free trial account, paid plans)
**Data Format**: JSON, XML
**Update Frequency**: Real-time (terrestrial AIS)
**License**: Commercial (credit-based pricing, free trial with 2000 credits / 10 days)

## What It Provides

MyShipTracking provides terrestrial AIS vessel tracking data through a comprehensive REST API.
The service aggregates AIS data from a network of shore-based receivers and offers a full suite
of endpoints for vessel tracking, historical data, port information, and fleet management.

Data includes:
- Real-time vessel position, speed, course, heading
- Vessel identity (MMSI, IMO, name, callsign, type)
- Voyage data (destination, ETA, draught)
- Historical tracks over defined time periods
- Port calls (arrival/departure records)
- Port details (location, timezone, UN/LOCODE)
- Vessels in zone / vessels nearby queries

## API Details

Comprehensive REST API with these endpoints:

| Endpoint | Description |
|---|---|
| Vessel Status | Latest position/voyage for a single vessel |
| Vessels Status (Bulk) | Multiple vessels in one request |
| Vessels In Zone | All vessels in a geographic bounding box |
| Vessels Nearby | Vessels within radius of a reference vessel |
| Vessel History Track | Historical track with time range and grouping |
| Vessel Search | Search by vessel name |
| Port Details | Port info by UN/LOCODE |
| Port Search | Search ports by name |
| Vessels In Port | Vessels currently in a port |
| Port Estimate | ETA estimates for a port |
| Port Calls | Historical port call records |
| Fleet Management | Create/edit/delete fleets, add/remove vessels |

Authentication: API Key in request headers. Key generated from account page after registration.

Rate limits:
- Full accounts: 2000 calls/minute
- Trial accounts: 90 calls/minute
- Maximum 500 credits per request (overuse protection)

Each endpoint has a credit cost. Trial provides 2000 credits total for 10 days.

Error handling follows a standardized envelope with specific error codes (MST_ERR_VALIDATOR,
ERR_INVALID_KEY, ERR_NO_CREDITS, ERR_RATE_LIMIT, etc.).

## Freshness Assessment

Good for coastal areas with station coverage. Terrestrial AIS only — no satellite data. The API
delivers real-time data from the contributing receiver network, but coverage is limited to areas
within VHF range of shore stations. The service is honest about this limitation in their docs.

Important caveat from their docs: "Due to the nature of terrestrial coverage, there may be
instances where vessels remain out of range for extended periods."

## Entity Model

Per-vessel records with standard AIS fields:
- `mmsi`, `imo`, `name`, `callsign`, `type`
- `lat`, `lon`, `speed`, `course`, `heading`
- `destination`, `eta`, `draught`
- `navstat` (navigational status)
- Timestamps

Port records: UN/LOCODE, name, country, timezone, coordinates.

Fleet management adds organizational layers on top.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 2 | Real-time terrestrial, but gaps in coverage |
| Openness | 1 | Credit-based commercial model, trial is very limited |
| Stability | 2 | Commercial service, active development, no public SLA |
| Structure | 3 | Well-documented REST API with standardized error handling |
| Identifiers | 3 | MMSI, IMO, callsign, UN/LOCODE for ports |
| Additive Value | 2 | Vessels-in-zone and fleet management are useful features |

**Total: 13/18**

## Notes

- The "Vessels In Zone" endpoint is particularly useful — it enables area monitoring without
  knowing specific vessel identifiers beforehand. This is a capability that aprs.fi lacks.
- The credit-based pricing model makes cost predictable but the trial is extremely limited
  (2000 credits / 10 days).
- Fleet management features (create fleets, assign vessels, track fleet positions) add value
  for operational use cases.
- Terrestrial-only limitation is clearly stated and should be respected in integration design.
- The standardized error envelope is a nice touch for robust integration.
- Coverage map is available on the website — Mediterranean and Northern Europe appear strongest.
