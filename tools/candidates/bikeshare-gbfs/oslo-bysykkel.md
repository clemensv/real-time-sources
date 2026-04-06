# Oslo Bysykkel

**Country/Region**: Norway — Oslo
**Publisher**: Oslo Bysykkel / Urban Sharing AS
**API Endpoint**: `https://gbfs.urbansharing.com/oslobysykkel.no/gbfs.json`
**Documentation**: https://oslobysykkel.no/en/open-data
**Protocol**: GBFS 2.3
**Auth**: None
**Data Format**: JSON (GBFS)
**Update Frequency**: 10-second TTL
**License**: Norwegian Licence for Open Government Data (NLOD) 2.0

## What It Provides

Oslo Bysykkel is Oslo's municipal bikeshare with 247 stations, operated by Urban Sharing. The same Urban Sharing platform powers bikeshare systems in Bergen, Trondheim, Milan (BikeMi), and Edinburgh. The feed is notable for its 10-second TTL (extremely fresh), polygon station geometries, and deep-link URIs.

## API Details

```
GET https://gbfs.urbansharing.com/oslobysykkel.no/gbfs.json
```

Returns GBFS 2.3 manifest with feeds:
- `system_information` — System metadata
- `station_information` — 247 stations with coordinates, capacity, and polygon `station_area` geometries
- `station_status` — Real-time availability
- `vehicle_types` — Bike classifications
- `system_pricing_plans` — Pricing tiers

Station data includes deep links and rich geometry:
```json
{
  "station_id": "2350",
  "name": "Aker Brygge",
  "lat": 59.9118,
  "lon": 10.7303,
  "capacity": 33,
  "station_area": {
    "type": "MultiPolygon",
    "coordinates": [...]
  },
  "rental_uris": {
    "android": "oslobysykkel://stations/2350",
    "ios": "oslobysykkel://stations/2350"
  }
}
```

**Other Urban Sharing systems (same platform):**
- Bergen: `https://gbfs.urbansharing.com/bergenbysykkel.no/gbfs.json`
- Trondheim: `https://gbfs.urbansharing.com/trondheimbysykkel.no/gbfs.json`
- Milan BikeMi: `https://gbfs.urbansharing.com/bikemi.com/gbfs.json`
- Edinburgh: `https://gbfs.urbansharing.com/edinburghcyclehire.com/gbfs.json`

## Freshness Assessment

The 10-second TTL is among the freshest GBFS feeds available — most systems use 60-second TTLs. Station status updates reflect near-real-time bike movements. The Urban Sharing infrastructure is production-grade and highly reliable.

## Entity Model

- **Station**: Dock-based station with polygon geometry, deep links, capacity
- **Vehicle Type**: Bike classifications (mechanical, e-bike where available)
- **Availability**: Bikes available, docks available, station status
- **Pricing**: Subscription plans

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 10-second TTL — exceptionally fresh |
| Openness | 3 | No auth, NLOD license, publicly accessible |
| Stability | 3 | Urban Sharing platform, well-maintained |
| Structure | 3 | GBFS 2.3 with rich extras (polygon geometries, deep links) |
| Identifiers | 3 | Station IDs, vehicle type IDs |
| Additive Value | 2 | Covered by GBFS catalog; value is Urban Sharing platform pattern covering 5+ cities |
| **Total** | **17/18** | |

## Notes

- Oslo Bysykkel is in the MobilityData GBFS catalog. A generic GBFS bridge handles it.
- The Urban Sharing platform is the key insight here — one platform pattern covers Oslo, Bergen, Trondheim, Milan, and Edinburgh. All use `gbfs.urbansharing.com/{domain}/` as the URL pattern.
- The polygon `station_area` geometries are unusual for GBFS feeds and enable precise geofencing.
- The documented open data page at oslobysykkel.no/en/open-data is a model of how to present bikeshare open data — clear, well-structured, with explicit license terms.
