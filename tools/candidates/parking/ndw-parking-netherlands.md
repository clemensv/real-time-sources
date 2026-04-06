# NDW Netherlands Parking (Truck Parking)

**Country/Region**: Netherlands
**Publisher**: NDW (Nationale Databank Wegverkeersgegevens) / Rijkswaterstaat
**API Endpoint**: `https://opendata.ndw.nu/Truckparking_Parking_Status.xml` (status) and `https://opendata.ndw.nu/Truckparking_Parking_Table.xml` (static)
**Documentation**: https://opendata.ndw.nu/
**Protocol**: DATEX II v3
**Auth**: None
**Data Format**: XML (DATEX II ParkingStatusPublication)
**Update Frequency**: Every 1 minute
**License**: Dutch government open data

## What It Provides

Real-time truck parking occupancy data for parking facilities along Dutch motorways. Provides vacant spaces, occupied spaces, and occupancy percentages per facility, including breakdowns by parking space groups. Uses the DATEX II v3 parking extension — the European standard for parking data exchange.

## API Details

**Static data (Parking Table):**
```
GET https://opendata.ndw.nu/Truckparking_Parking_Table.xml
```
Contains parking facility definitions: locations, capacity, names, access conditions.

**Dynamic data (Parking Status):**
```
GET https://opendata.ndw.nu/Truckparking_Parking_Status.xml
```
Returns DATEX II v3 ParkingStatusPublication:
```xml
<ns2:parkingRecordStatus xsi:type="ns2:ParkingSiteStatus">
  <ns2:parkingRecordReference id="NL-12_411"/>
  <ns2:parkingStatusOriginTime>2026-04-06T10:24:52Z</ns2:parkingStatusOriginTime>
  <ns2:parkingOccupancy>
    <ns2:parkingNumberOfVacantSpaces>345</ns2:parkingNumberOfVacantSpaces>
    <ns2:parkingNumberOfOccupiedSpaces>4</ns2:parkingNumberOfOccupiedSpaces>
    <ns2:parkingOccupancy>19.6</ns2:parkingOccupancy>
  </ns2:parkingOccupancy>
  <ns2:parkingSiteStatus>spacesAvailable</ns2:parkingSiteStatus>
</ns2:parkingRecordStatus>
```

Status values: `spacesAvailable`, `almostFull`, `full`, `unknown`, `closed`

Group-level breakdowns show occupancy by parking space category (regular, oversized, hazardous goods, etc.).

## Freshness Assessment

The `parkingStatusOriginTime` shows per-facility timestamps within the last minute. Data is updated every ~1 minute from the parking guidance systems. The DATEX II publication timestamp confirms continuous updates. Excellent real-time freshness.

## Entity Model

- **Parking Site**: Motorway truck parking facility with reference ID (NL-12_xxx)
- **Occupancy**: Vacant spaces, occupied spaces, percentage
- **Space Groups**: Breakdown by category (regular truck, oversized, hazmat)
- **Status**: Site-level status enum (spacesAvailable, almostFull, full, closed)
- **Metadata**: Linked to Parking Table for static attributes (capacity, location, access)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Per-minute updates with per-facility timestamps |
| Openness | 3 | No auth, no registration, direct XML download |
| Stability | 3 | Government-operated NDW platform; DATEX II is EU standard |
| Structure | 3 | DATEX II v3 — strict XML schema, well-defined semantics |
| Identifiers | 3 | Standardized parking record IDs linked to parking table |
| Additive Value | 2 | Truck parking is niche but valuable; DATEX II pattern reusable for EU parking |
| **Total** | **17/18** | |

## Notes

- DATEX II v3 is the EU standard for traffic and parking data exchange. Building a parser for this format unlocks data from many European countries (Germany, UK, Sweden, etc.).
- NDW recently migrated to DATEX II v3 (v2.3 files discontinued as of April 2026). Ensure parser handles v3 schema.
- Truck parking is specifically valuable for logistics/freight applications — availability of truck parking is a significant operational concern in Europe.
- NDW also publishes road traffic data (see road-traffic candidates) on the same platform — complementary data streams.
- The static Parking Table file provides the reference data needed to resolve IDs to names and locations.
