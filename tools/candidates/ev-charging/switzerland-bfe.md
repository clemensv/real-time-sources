# Switzerland BFE / ich-tanke-strom.ch

**Country/Region**: Switzerland
**Publisher**: Bundesamt für Energie BFE (Swiss Federal Office of Energy)
**API Endpoint**: `https://data.geo.admin.ch/ch.bfe.ladestellen-elektromobilitaet/data/oicp/ch.bfe.ladestellen-elektromobilitaet.json`
**Documentation**: https://opendata.swiss/en/dataset/ladestationen-fuer-elektroautos
**Protocol**: File download (OICP JSON format) + STAC metadata API
**Auth**: None
**Data Format**: JSON (OICP/Hubject format)
**Real-Time Status**: Yes — `DynamicInfoAvailable: true` on records; separate EVSEStatus resource
**Update Frequency**: Continuously updated (STAC metadata shows today's date)
**Station Count**: Several thousand EVSEs across Switzerland
**License**: Open use with mandatory source attribution; commercial use requires permission (opendata.swiss terms)

## What It Provides

The Swiss Federal Office of Energy (BFE) publishes all publicly accessible EV charging stations in Switzerland via the federal geodata infrastructure (data.geo.admin.ch). The public-facing portal is ich-tanke-strom.ch (which redirects to the federal map viewer). The data is published in OICP (Open InterCharge Protocol) format — the same protocol used by Hubject, Europe's largest EV roaming hub. This means the data is Hubject-compatible and follows the same EVSE data model used across European roaming networks.

Two resources are published:
1. **EVSEData** — static station information (location, connectors, power, operator)
2. **EVSEStatus** — real-time availability status per EVSE

## API Details

**Static EVSE Data (OICP format):**
```
GET https://data.geo.admin.ch/ch.bfe.ladestellen-elektromobilitaet/data/oicp/ch.bfe.ladestellen-elektromobilitaet.json
```

Returns an `EVSEData` array with records including:
- `EvseID` — Hubject-compatible EVSE ID (e.g., `CH*CCI*E22078`)
- `ChargingStationId` — station grouping ID
- `ChargingStationNames[]` — multilingual names (en/fr/de/it)
- `Address` — city, postal code, street, country
- `GeoCoordinates` — lat/lon (Google format: `"46.23432 6.055602"`)
- `Plugs[]` — connector types (Type 2 Outlet, CCS Combo 2, CHAdeMO, etc.)
- `ChargingFacilities[]` — power details (Amperage, Voltage, power in kW, powertype)
- `AuthenticationModes[]` — NFC RFID, Direct Payment, REMOTE
- `IsOpen24Hours` — 24/7 access flag
- `DynamicInfoAvailable` — whether real-time status is available for this EVSE
- `IsHubjectCompatible` — roaming compatibility flag
- `HotlinePhoneNumber` — operator contact

**Real-Time EVSE Status:**
A separate JSON resource provides current availability status per EVSE. Available via opendata.swiss resource links.

**STAC Metadata:**
```
GET https://data.geo.admin.ch/api/stac/v0.9/collections/ch.bfe.ladestellen-elektromobilitaet
```
Returns collection metadata including last update timestamp (confirms continuous updates).

## Freshness Assessment

The dataset is continuously updated — the STAC metadata shows `updated: "2026-04-06T11:03:23Z"` (today). The `DynamicInfoAvailable: true` flag on EVSE records indicates real-time status data is available. Switzerland's charging infrastructure is well-connected via roaming platforms (primarily Hubject), which provides the pipeline for real-time status data to flow into this national dataset.

The OICP format is a strong indicator of data quality — it's the same format used for B2B roaming between charging operators across Europe.

## Entity Model

- **EVSE**: Individual Electric Vehicle Supply Equipment, identified by Hubject-compatible EVSE ID (`CH*CCI*E22078`)
- **Charging Station**: Groups one or more EVSEs at a physical location
- **Operator**: Identified via EVSE ID prefix (e.g., `CCI` = Chargecloud)
- **Connector/Plug**: Type 2, CCS Combo 2, CHAdeMO, etc.
- **Charging Facility**: Power specification (kW, voltage, amperage, AC/DC)

The EVSE ID format follows eMI3/OICP standards: `{country}*{operator}*E{number}`.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Continuously updated; real-time EVSE status available |
| Openness | 2 | Open data but commercial use needs permission; no auth for access |
| Stability | 3 | Federal government infrastructure (data.geo.admin.ch); STAC API |
| Structure | 3 | OICP format — industry-standard, well-defined, Hubject-compatible |
| Identifiers | 3 | eMI3/OICP EVSE IDs — globally unique, roaming-compatible |
| Additive Value | 2 | Switzerland-specific; moderate network size; excellent format |
| **Total** | **16/18** | |

## Notes

- The OICP format is a major differentiator. Building an OICP parser for Switzerland means the same code works with any Hubject-connected data source.
- Switzerland is not an EU member, so EU AFIR doesn't apply directly — but Switzerland voluntarily publishes open charging data following the same principles.
- The multilingual station names (de/fr/it/en) reflect Switzerland's four-language reality.
- The `IsHubjectCompatible` flag indicates which EVSEs participate in cross-border roaming.
- Power levels in the dataset range from 22 kW AC (Type 2) to 224 kW DC (CCS Combo 2), reflecting Switzerland's modern fast-charging infrastructure.
- ich-tanke-strom.ch redirects to the Swiss federal map viewer (map.geo.admin.ch) with the charging station layer enabled.
