# Vélib' Métropole Paris

**Country/Region**: France — Paris / Île-de-France
**Publisher**: Smovengo (operator) / Paris Open Data
**API Endpoint**: `https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/gbfs.json` (GBFS) and `https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records` (Opendatasoft)
**Documentation**: https://www.velib-metropole.fr/donnees-open-data and https://opendata.paris.fr/explore/dataset/velib-disponibilite-en-temps-reel/
**Protocol**: GBFS 2.x + Opendatasoft REST API
**Auth**: None
**Data Format**: JSON
**Update Frequency**: ~1 minute (GBFS TTL: 3600 for catalog, but station_status updates more frequently)
**License**: Open Data Paris (ODbL)

## What It Provides

Real-time station availability for Paris's docked bikeshare system — the largest in Europe. Vélib' operates ~1,500 stations across Paris and 60+ surrounding municipalities with approximately 19,000 bikes (mechanical + electric).

## API Details

**GBFS endpoint (Smovengo):**
- `gbfs.json` — auto-discovery manifest
- `station_information.json` — station metadata
- `station_status.json` — real-time availability
- `system_information.json` — system info

**Paris Open Data endpoint (Opendatasoft):**
```
GET https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?limit=100
```

Returns records with:
```json
{
  "stationcode": "16107",
  "name": "Benjamin Godard - Victor Hugo",
  "is_installed": "OUI",
  "capacity": 35,
  "numdocksavailable": 25,
  "numbikesavailable": 9,
  "mechanical": 7,
  "ebike": 2,
  "is_renting": "OUI",
  "is_returning": "OUI",
  "duedate": "2026-04-06T09:49:10+00:00",
  "coordonnees_geo": {"lon": 2.275725, "lat": 48.865983}
}
```

The Opendatasoft API supports pagination, filtering, geo-distance queries, and export in JSON/CSV/GeoJSON.

## Freshness Assessment

The `duedate` field shows per-station update timestamps — typically within 2 minutes of current time. The GBFS `station_status` feed provides similar freshness. Real-time for practical purposes.

## Entity Model

- **Station**: ~1,500 stations with station codes, names, coordinates, capacity
- **Availability**: Mechanical bikes, e-bikes, empty docks
- **Status**: Installed, renting, returning flags
- **Geography**: Covers Paris proper + 60 surrounding municipalities

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Per-station timestamps within 2 minutes |
| Openness | 3 | Both GBFS and Opendatasoft endpoints are fully open |
| Stability | 3 | GBFS endpoint is stable; Paris Open Data has been running for years |
| Structure | 3 | Standard GBFS + well-structured Opendatasoft records |
| Identifiers | 3 | Stable station codes, commune codes |
| Additive Value | 2 | Available via GBFS catalog; Paris Open Data endpoint adds richer metadata (commune, arrondissement) |
| **Total** | **17/18** | |

## Notes

- Vélib' is listed in the MobilityData GBFS catalog, so a generic GBFS bridge would cover it. The Paris Open Data endpoint adds value through richer geographic metadata and the Opendatasoft query capabilities (geo-distance, filtering by arrondissement).
- The Opendatasoft API also provides historical data, which is not available via GBFS.
- Both mechanical and electric bike counts are broken out separately — useful for analytics.
