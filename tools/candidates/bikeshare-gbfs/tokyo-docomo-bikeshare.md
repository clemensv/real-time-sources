# Tokyo Docomo Bikeshare

**Country/Region**: Japan — Tokyo (+ other Japanese cities via ODPT)
**Publisher**: Docomo Bike Share / Open Data Platform for Transportation (ODPT)
**API Endpoint**: `https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo/gbfs.json`
**Documentation**: https://developer-dc.odpt.org/
**Protocol**: GBFS 2.3
**Auth**: None
**Data Format**: JSON (GBFS)
**Update Frequency**: 60-second TTL
**License**: ODPT open data license

## What It Provides

Docomo Bikeshare operates Tokyo's largest bikeshare system with 1,794 stations across central Tokyo wards (Chiyoda, Minato, Shibuya, Shinjuku, etc.). The system publishes GBFS 2.3 feeds through Japan's Open Data Platform for Transportation (ODPT). A separate Japan-wide feed aggregates Docomo systems across multiple cities.

## API Details

**Tokyo-specific auto-discovery:**
```
GET https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo/gbfs.json
```

**Japan-wide auto-discovery:**
```
GET https://api-public.odpt.org/api/v4/gbfs/docomo-cycle/gbfs.json
```

Returns standard GBFS 2.3 manifest with feeds:
- `system_information.json` — System metadata
- `station_information.json` — 1,794 stations with coordinates and names
- `station_status.json` — Real-time bike availability per station

Station data includes Japanese and English names:
```json
{
  "station_id": "00010137",
  "name": "A4-01.東京駅八重洲口 / Tokyo Station Yaesu",
  "lat": 35.6804,
  "lon": 139.7704,
  "capacity": 40
}
```

## Freshness Assessment

TTL is 60 seconds. Station status updates as bikes are rented and returned. The ODPT platform is well-maintained and consistently available. Data reflects real-time dock occupancy.

## Entity Model

- **System**: City-level bikeshare system (Tokyo, plus other cities via Japan-wide feed)
- **Station**: Dock-based station with bilingual name, coordinates, capacity
- **Availability**: Number of bikes available, docks available per station

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 60s TTL, real-time |
| Openness | 3 | No auth, publicly accessible |
| Stability | 3 | ODPT government platform, GBFS 2.3 compliant |
| Structure | 3 | Standard GBFS schema |
| Identifiers | 3 | Station IDs, system IDs |
| Additive Value | 3 | Largest Japanese bikeshare; ODPT platform covers multiple Japanese transit datasets |
| **Total** | **18/18** | |

## Notes

- Tokyo Docomo is in the MobilityData GBFS catalog as `docomo-cycle-tokyo`. A generic GBFS bridge handles it.
- The Japan-wide feed (`docomo-cycle`) aggregates systems in Tokyo, Yokohama, Osaka, and other cities — one feed for all of Japan.
- ODPT also publishes transit data (trains, buses) — the platform is a gateway to broader Japanese open transit data.
- Station names are bilingual (Japanese/English), which is excellent for international users.
- This is the largest GBFS system in Asia by station count.
