# Montreal BIXI

**Country/Region**: Canada — Montreal
**Publisher**: BIXI Montréal
**API Endpoint**: `https://gbfs.velobixi.com/gbfs/gbfs.json`
**Documentation**: https://bixi.com/en/open-data/
**Protocol**: GBFS 1.0
**Auth**: None
**Data Format**: JSON (GBFS)
**Update Frequency**: Real-time
**License**: Open data

## What It Provides

BIXI is one of North America's oldest and largest bikeshare systems, launched in 2009 as a pioneer that helped inspire Citi Bike, Capital Bikeshare, and many others. With 873 stations across Montreal, it is the largest bikeshare in Canada. BIXI publishes GBFS 1.0 feeds and also offers extensive historical trip data for analytics.

## API Details

```
GET https://gbfs.velobixi.com/gbfs/gbfs.json
```

Returns GBFS 1.0 manifest with feeds:
- `system_information` — System metadata
- `station_information` — 873 stations with coordinates, capacity
- `station_status` — Real-time bike availability
- `system_alerts` — Service alerts

Available in English (`en`) and French (`fr`).

```json
{
  "station_id": "1",
  "name": "Métro Champ-de-Mars (Viger / Sanguinet)",
  "lat": 45.51025293,
  "lon": -73.55672752,
  "capacity": 33
}
```

## Freshness Assessment

Real-time station status. BIXI operates seasonally (typically April–November due to Montreal winters), so station availability may show zero during off-season. During operating season, data is continuously updated as bikes move through the system.

## Entity Model

- **Station**: Dock-based station with ID, bilingual name, coordinates, capacity
- **Availability**: Bikes available, docks available
- **Alerts**: Service notifications

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time during operating season |
| Openness | 3 | No auth, bilingual (EN/FR) |
| Stability | 3 | Established since 2009, reliable infrastructure |
| Structure | 2 | GBFS 1.0 — older version, but functional |
| Identifiers | 3 | Unique station IDs, coordinates |
| Additive Value | 2 | Covered by GBFS catalog; value is as Canada's largest system + historical data |
| **Total** | **16/18** | |

## Notes

- BIXI is in the MobilityData GBFS catalog as `Bixi_MTL`. A generic GBFS bridge handles it.
- GBFS 1.0 is the oldest supported version — a bridge should handle the differences from 2.x/3.0 (fewer feeds, simpler schema).
- BIXI publishes comprehensive historical trip data (origin/destination, duration) on its open data page — valuable for analytics but out of scope for real-time ingestion.
- Seasonal operation means the bridge should handle gracefully when stations report zero availability in winter.
- BIXI's pioneering role means its data patterns influenced many subsequent North American bikeshare systems.
