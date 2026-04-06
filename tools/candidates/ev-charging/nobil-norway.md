# NOBIL Norway

**Country/Region**: Norway (+ Sweden, Finland via Nordic integration)
**Publisher**: Enova SF (Norwegian government enterprise)
**API Endpoint**: `https://nobil.no/api/server/search.php` and `https://nobil.no/api/server/datadump.php`
**Documentation**: https://info.nobil.no/api (PDF: https://info.nobil.no/files/API_NOBIL_Documentation_v3_20250827.pdf)
**Protocol**: REST
**Auth**: API Key (free registration required)
**Data Format**: JSON / XML
**Update Frequency**: Near real-time (registry updates as operators report; real-time connector status available)
**License**: Creative Commons Attribution 4.0 International (CC BY 4.0)

## What It Provides

NOBIL is the official Norwegian government database of EV charging stations, maintained by Enova SF (a government enterprise under the Ministry of Climate and Environment). It contains all publicly accessible charging stations in Norway — the country with the world's highest EV penetration rate. NOBIL also covers Sweden and Finland through Nordic cooperation. Includes both station metadata and real-time connector availability.

## API Details

**Search API:**
```
POST https://nobil.no/api/server/search.php
Content-Type: application/x-www-form-urlencoded

apikey={key}&countrycode=NOR&action=search&type=near&lat=59.91&long=10.75&distance=5000&limit=10&format=json
```

Search parameters:
- `action=search` — search for stations
- `type=near` — geographic proximity search (lat/lon/distance)
- `type=municipality` — search by county/municipality code
- `type=id` — lookup by station ID (e.g., `NOR_00171`)

**Data Dump API:**
```
GET https://nobil.no/api/server/datadump.php?apikey={key}&countrycode=NOR&fromdate=2024-01-01&format=json
```

Returns full or delta dump of all stations. Supports `fromdate` for incremental updates.

**Real-time availability:**
Search API supports `realtime=TRUE` parameter to include current connector status (available, occupied, out of service).

Station data includes:
- Station ID (e.g., `NOR_00171`)
- Position (lat/lon), address, municipality, county
- Connector details: type (CCS, CHAdeMO, Type 2), power (kW), count
- Operator name
- Real-time status per connector (when `realtime=TRUE`)
- Parking fee, 24h access, roof/shelter info

## Freshness Assessment

The data dump supports delta updates via `fromdate`, enabling efficient incremental polling for new/changed stations. When `realtime=TRUE` is used in search queries, connector-level availability is included — this is genuine real-time data showing whether a connector is currently in use. Norway's high EV adoption means the data is actively maintained and up-to-date.

## Entity Model

- **Charging Station**: Identified by country-prefixed ID (e.g., `NOR_00171`)
- **Connector**: Individual charging point with type, power, real-time status
- **Operator**: Charging network or local operator
- **Location**: Address, municipality code, county, coordinates
- **Attributes**: Parking fee, 24h access, covered/shelter, public/restricted

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time connector status; delta dumps for registry changes |
| Openness | 3 | CC BY 4.0 license; free API key |
| Stability | 3 | Government-operated, v3 API (latest docs dated 2025-08-27) |
| Structure | 3 | Well-documented JSON/XML with nested connector details |
| Identifiers | 3 | Country-prefixed station IDs, municipality codes |
| Additive Value | 3 | Authoritative government source for EV-leading country; includes Nordic coverage |
| **Total** | **18/18** | |

## Notes

- Norway has the highest EV penetration in the world (80%+ of new car sales). NOBIL is the definitive source for Norwegian charging infrastructure.
- API key is free — register at https://info.nobil.no/api
- NOBIL covers Norway, Sweden, and Finland — three countries from one API.
- The `realtime=TRUE` parameter is particularly valuable — it provides connector-level occupancy data, which is rare among EV charging registries.
- Delta dump via `fromdate` parameter makes this very bridge-friendly: initial full dump, then poll for changes.
