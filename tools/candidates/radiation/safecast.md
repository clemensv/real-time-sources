# Safecast

**Country/Region**: Global (strongest coverage in Japan, USA, Europe)
**Publisher**: Safecast (Momoko Ito Foundation, 501(c)3 non-profit)
**API Endpoint**: `https://api.safecast.org`
**Documentation**: https://api.safecast.org/en-US (interactive API docs)
**Protocol**: REST (Ruby on Rails)
**Auth**: None for read access; API key for writes
**Data Format**: JSON
**Update Frequency**: Continuous (citizen-contributed, varies by device and user activity)
**License**: CC0 (Public Domain) for all data

## What It Provides

Safecast is the world's largest open citizen radiation monitoring network. Born from the 2011 Fukushima disaster, it has grown into a global platform with over 200 million measurements. Volunteers carry bGeigie Nano devices (mobile Geiger counters) and upload GPS-tagged radiation readings. Fixed "Pointcast" sensors provide continuous monitoring at specific locations.

Measurements are in CPM (counts per minute) from Geiger-Müller tubes, with location, timestamp, device metadata. The dataset covers Japan extensively (post-Fukushima mapping) and has growing coverage in North America, Europe, and elsewhere.

## API Details

### Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/measurements.json` | List measurements |
| GET | `/measurements/{id}.json` | Single measurement |
| GET | `/devices.json` | List devices |
| GET | `/bgeigie_imports.json` | bGeigie drive imports |
| GET | `/users.json` | User list |

### Query Parameters (Measurements)

- `latitude`, `longitude`, `distance` — Spatial filter (measurements near a point)
- `captured_after`, `captured_before` — Time range filter (capture time)
- `since`, `until` — Time range filter (database insertion time)
- `order` — Sort order (e.g., `captured_at+desc`)

### Example Request

```
GET https://api.safecast.org/measurements.json?distance=100&latitude=35.6&longitude=139.7
```

### Sample Response

```json
[
  {
    "id": 13313804,
    "user_id": 1,
    "value": 41.0,
    "unit": "cpm",
    "location_name": null,
    "device_id": null,
    "measurement_import_id": 29,
    "captured_at": "2011-06-07T23:47:37.000Z",
    "height": null,
    "latitude": 35.607703333333,
    "longitude": 139.7045
  }
]
```

### Bulk Data Download

Full dataset available as CSV:
```
GET https://api.safecast.org/system/measurements.csv
```

### Additional Services

- **Ingest API**: `https://ingest.safecast.org/v1/devices` — Real-time device data ingestion
- **Tilemap**: `https://safecast.org/tilemap/` — Interactive map visualization
- **GitHub**: `https://github.com/Safecast/safecastapi` — Open source (MIT licensed)

## Freshness Assessment

The API is live and returning data as of 2026-04-06. However, the measurement data returned for a Tokyo query showed measurements from 2011 — the API defaults to oldest-first ordering unless explicitly sorted. For real-time monitoring, one would need to query recent `captured_after` timestamps or use the ingest API for live sensor feeds.

The ingest API (`ingest.safecast.org/v1/devices`) returned an empty array, suggesting real-time fixed-sensor data may require specific device IDs.

## Entity Model

- **User** — Contributor account with ID.
- **Device** — Radiation detector (bGeigie Nano, Pointcast, etc.) with type and sensor info.
- **Measurement** — Core unit: value (CPM), unit, timestamp (`captured_at`), location (lat/lon), height, device reference.
- **bGeigie Import** — Bulk upload from a drive session, containing many measurements.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 2 | Continuous uploads but citizen-driven, not guaranteed real-time. Historical bias in default queries. |
| Openness | 3 | CC0 license, no auth for reads, open source codebase |
| Stability | 2 | Non-profit infrastructure, has been running since 2011 but no SLA |
| Structure | 2 | Clean JSON API but sparse metadata — device_id often null, no station concept |
| Identifiers | 1 | No stable station IDs — measurements are individual points, not station-based |
| Additive Value | 3 | 200M+ measurements, global citizen science network, unique coverage in Japan |
| **Total** | **13/18** | |

## Notes

- Safecast's strength is its massive, open dataset and grassroots coverage. Its weakness for real-time integration is the citizen-science model — data arrives when volunteers upload it.
- The CPM unit requires conversion to µSv/h using device-specific calibration factors, which aren't always available in the API response.
- For real-time fixed-station data, the Pointcast/Solarcast devices publish continuously, but accessing their live feeds may require the ingest API or Grafana dashboards.
- The full measurement CSV download is enormous (200M+ records) and not suitable for real-time use.
- Best used as a supplementary data source alongside official government monitoring networks.
