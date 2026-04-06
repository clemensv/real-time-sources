# Taipei YouBike 2.0

**Country/Region**: Taiwan (island-wide — Taipei, New Taipei, Taoyuan, Hsinchu, Taichung, Kaohsiung, etc.)
**Publisher**: YouBike Co., Ltd.
**API Endpoint**: `https://apis.youbike.com.tw/json/station-yb2.json`
**Documentation**: https://data.taipei/dataset/detail?id=c6bc8aed-557d-41d5-bfb1-8da24f78f2fb
**Protocol**: REST (proprietary JSON — not GBFS)
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Real-time (~1 minute)
**License**: Open data (Taipei City Government)

## What It Provides

YouBike 2.0 is Taiwan's dominant public bikeshare system with approximately 9,070 stations island-wide — making it one of the largest station-based bikeshare systems in the world by station count. It covers Taipei, New Taipei City, Taoyuan, Hsinchu, Taichung, Chiayi, Tainan, Kaohsiung, and Pingtung. The system uses a proprietary JSON API rather than GBFS.

## API Details

```
GET https://apis.youbike.com.tw/json/station-yb2.json
```

Returns a flat JSON array of all YouBike 2.0 stations across Taiwan:
```json
{
  "sno": "500101001",
  "sna": "YouBike2.0_捷運科技大樓站",
  "tot": 28,
  "sbi": 6,
  "bemp": 22,
  "act": "1",
  "lat": 25.02605,
  "lng": 121.5436,
  "ar": "復興南路二段235號前",
  "sareaen": "Da'an Dist.",
  "aren": "No.235, Sec. 2, Fuxing S. Rd."
}
```

Key fields:
- `sno` — Station number (unique ID)
- `sna` — Station name (Chinese, prefixed with "YouBike2.0_")
- `tot` — Total docks
- `sbi` — Available bikes
- `bemp` — Empty docks
- `act` — Active flag (1 = operational)
- `lat`, `lng` — WGS84 coordinates
- `ar` — Address (Chinese)
- `sareaen`, `aren` — English district/address

## Freshness Assessment

Data updates approximately every minute. The `act` flag indicates station operational status. Real-time availability reflects bike rental/return activity. The single-file JSON dump is large (~9,000 records) but compresses well.

## Entity Model

- **Station**: Dock-based station with ID, name, coordinates, address
- **Availability**: Bikes available (`sbi`), empty docks (`bemp`), total capacity (`tot`)
- **Status**: Active/inactive flag
- **Geography**: District-level grouping via `sareaen`

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time, ~1 minute updates |
| Openness | 3 | No auth, publicly accessible |
| Stability | 3 | Government-backed, consistently available |
| Structure | 2 | Proprietary flat JSON — no GBFS, station names in Chinese |
| Identifiers | 3 | Unique station numbers, coordinates |
| Additive Value | 3 | Largest Asian bikeshare not in GBFS catalog; Taiwan has zero GBFS entries |
| **Total** | **17/18** | |

## Notes

- YouBike is NOT in the MobilityData GBFS catalog — Taiwan has zero entries. This requires a dedicated bridge.
- The Taipei Open Data portal dataset (`data.taipei`) may have shifted endpoints; the `apis.youbike.com.tw` JSON endpoint is the reliable source.
- Station names are in Chinese with English district names. A bridge should preserve both.
- The system is enormous — 9,070 stations dwarfs most European and American bikeshare systems.
- YouBike 2.0 replaced the original YouBike 1.0 system with lighter, dock-less docking stations.
