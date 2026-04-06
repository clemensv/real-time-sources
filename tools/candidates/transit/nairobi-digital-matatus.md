# Nairobi Digital Matatu GTFS

- **Country/Region**: Kenya (Nairobi)
- **Endpoint**: `https://gtfs.digitaltransport4africa.org/api/gtfs/feeds`
- **Protocol**: REST / GTFS Static
- **Auth**: None
- **Format**: GTFS (protobuf), CSV, JSON
- **Freshness**: Static (schedule data), potential GTFS-RT in future
- **Docs**: https://www.digitalmatatus.com/
- **Score**: 10/18

## Overview

The Digital Matatus project mapped Nairobi's entire informal transit network — over
130 matatu (minibus) routes serving millions of daily riders. This was a groundbreaking
effort to formalize Africa's most complex informal transit system into a machine-readable
GTFS format.

Nairobi's matatus are the backbone of mobility for 4+ million residents. The GTFS
data enables routing, analysis, and — if real-time tracking is added — live vehicle
positions.

The Digital Transport for Africa (DT4A) initiative has extended this model to other
African cities including Kampala, Dar es Salaam, Accra, Kigali, and Addis Ababa.

## Endpoint Analysis

**Digital Matatus GTFS static** data available at:
```
https://www.digitalmatatus.com/gtfs/matatu_gtfs.zip
```

The Digital Transport for Africa API:
```
GET https://gtfs.digitaltransport4africa.org/api/gtfs/feeds
```

This endpoint returned 404 during probing, suggesting the API structure may have changed.

GTFS static data contains:
- `routes.txt` — 130+ matatu routes
- `stops.txt` — Thousands of informal stops
- `trips.txt` — Trip definitions
- `stop_times.txt` — Arrival/departure times
- `shapes.txt` — Route geometries

Other African cities with GTFS data:
| City | Country | Status |
|------|---------|--------|
| Nairobi | Kenya | Complete |
| Kampala | Uganda | Complete |
| Dar es Salaam | Tanzania | Complete |
| Kigali | Rwanda | Complete |
| Addis Ababa | Ethiopia | In progress |
| Accra | Ghana | In progress |
| Lagos | Nigeria | BRT system mapped |

## Integration Notes

- **GTFS-RT potential**: The static GTFS data is the foundation. GPS tracking of
  matatus could enable GTFS-RT feeds, but this isn't yet widely implemented.
- **BRT systems**: Lagos BRT, Dar es Salaam DART, and planned BRT systems in Nairobi
  and Kampala are more likely to have GTFS-RT capabilities.
- **Existing bridge**: The repository already has a `gtfs` bridge. African GTFS feeds
  would be additional data sources for the same bridge.
- **Informal transit challenge**: Matatus don't run fixed schedules — they depart when
  full. This fundamentally differs from European/American transit. A GTFS bridge needs
  to account for this.
- **Mobile data**: Many matatu tracking efforts use rider smartphones or driver apps.
  This data is real-time but typically not publicly accessible.
- **DT4A collaboration**: The Digital Transport for Africa initiative actively promotes
  open transit data. They may provide API access to aggregated feeds.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Static schedules (GTFS-RT not yet available) |
| Openness | 3 | Open data, Creative Commons |
| Stability | 2 | Academic/NGO project, periodic updates |
| Structure | 2 | GTFS standard but static only |
| Identifiers | 1 | Route/stop IDs internal to the dataset |
| Richness | 1 | Routes and stops, no real-time positions |
