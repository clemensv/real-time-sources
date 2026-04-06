# Nationale Databank Laadinfrastructuur (NDL) Netherlands

**Country/Region**: Netherlands
**Publisher**: Rijkswaterstaat / NDW (Nationale Databank Wegverkeersgegevens)
**API Endpoint**: `https://opendata.ndw.nu/charging_point_locations.geojson.gz` and `https://opendata.ndw.nu/charging_point_locations_ocpi.json.gz`
**Documentation**: https://opendata.ndw.nu/
**Protocol**: File download (OCPI format, GeoJSON)
**Auth**: None
**Data Format**: GeoJSON (3.3 MB compressed) / OCPI JSON (20 MB compressed)
**Update Frequency**: Continuous — files updated every few minutes
**License**: Open data (Dutch government)

## What It Provides

The Netherlands' National Charging Infrastructure Database publishes real-time charging point data via the NDW open data portal. This is the Dutch national access point for EV charging data, containing all publicly accessible charging stations in the Netherlands. The OCPI (Open Charge Point Interface) formatted export includes detailed location, EVSE, connector, and real-time status information. A separate tariff file provides pricing data.

## API Details

Three files available on the NDW open data portal:

1. **GeoJSON locations** (3.3 MB compressed):
   ```
   https://opendata.ndw.nu/charging_point_locations.geojson.gz
   ```
   Standard GeoJSON with point features for each charging location.

2. **OCPI locations** (20 MB compressed):
   ```
   https://opendata.ndw.nu/charging_point_locations_ocpi.json.gz
   ```
   Full OCPI v2.2 format with nested Location → EVSE → Connector hierarchy, including real-time status per EVSE (AVAILABLE, CHARGING, BLOCKED, OUT_OF_ORDER, etc.).

3. **OCPI tariffs** (4.2 MB compressed):
   ```
   https://opendata.ndw.nu/charging_point_tariffs_ocpi.json.gz
   ```
   Tariff information per charging network in OCPI format.

Files are updated continuously — the NDW portal shows `Last modified` timestamps within the current hour.

OCPI structure per location:
```json
{
  "id": "...",
  "name": "...",
  "address": "...",
  "city": "...",
  "coordinates": {"latitude": "...", "longitude": "..."},
  "evses": [{
    "uid": "...",
    "status": "AVAILABLE",
    "connectors": [{
      "id": "...",
      "standard": "IEC_62196_T2",
      "power_type": "AC_3_PHASE",
      "max_voltage": 230,
      "max_amperage": 32
    }]
  }]
}
```

## Freshness Assessment

The OCPI file is updated every few minutes (last modified timestamps are within the current hour). The OCPI format includes per-EVSE status, which reflects real-time connector availability. The Netherlands has one of the densest charging networks in Europe (100,000+ public charge points), and this data is the authoritative source. Excellent freshness for a file-based distribution.

## Entity Model

- **Location**: A physical charging site with address, coordinates, operator
- **EVSE**: An Electric Vehicle Supply Equipment unit (a "charge point") with real-time status
- **Connector**: Physical connector with standard (Type 2, CCS, etc.), power specs
- **Tariff**: Pricing structure per network/operator
- **Status**: AVAILABLE, CHARGING, BLOCKED, INOPERATIVE, OUT_OF_ORDER, PLANNED, REMOVED

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Files updated every few minutes with real-time EVSE status |
| Openness | 3 | Fully open, no auth, no registration |
| Stability | 3 | Government-operated NDW platform; OCPI is an industry standard |
| Structure | 3 | OCPI v2.2 — well-defined, nested, industry-standard schema |
| Identifiers | 3 | OCPI UIDs for locations, EVSEs, connectors |
| Additive Value | 3 | Complete Dutch charging data with real-time status + tariffs in one package |
| **Total** | **18/18** | |

## Notes

- This is arguably the best open EV charging data source in Europe. Real-time EVSE status, comprehensive coverage, OCPI standard format, no auth required, updated continuously. A model for how governments should publish charging data.
- The OCPI format is the industry standard for charge point data exchange, used by roaming platforms (Hubject, Gireve) and CPOs worldwide. Building a bridge for this data means the same parser works with any OCPI-compliant source.
- The tariff file adds pricing transparency that's rare in EV charging data.
- File sizes are significant (20 MB compressed for OCPI) — a bridge should download, diff against previous state, and emit change events.
- NDW also publishes road traffic data (see road-traffic candidates).
