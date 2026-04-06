# IOC Sea Level Monitoring — African Tide Gauges

- **Country/Region**: Pan-African coastal nations (South Africa, Mozambique, Kenya, Tanzania, Egypt, Morocco, Senegal, and more)
- **Endpoint**: `https://www.ioc-sealevelmonitoring.org/service.php?query=stationlist&format=json`
- **Protocol**: REST
- **Auth**: None
- **Format**: JSON
- **Freshness**: Real-time (1–15 minute intervals depending on station)
- **Docs**: https://www.ioc-sealevelmonitoring.org/service.php
- **Score**: 14/18

## Overview

The UNESCO Intergovernmental Oceanographic Commission (IOC) Sea Level Monitoring
Facility provides real-time tide gauge data from hundreds of stations worldwide,
including African coastal stations. This is the operational backbone for tsunami
early warning in the Indian Ocean and Mediterranean — both critical for African
coastal nations.

African coastal exposure is growing rapidly as urbanization concentrates populations
in coastal cities (Lagos, Dar es Salaam, Maputo, Mombasa, Dakar, Casablanca,
Alexandria). Sea level data is essential for storm surge warnings, port operations,
and climate monitoring.

## Endpoint Analysis

**Verified live** — the station list endpoint returns JSON with all global stations
including metadata, last observations, and update timestamps.

Station record structure:
```json
{
  "Code": "xxxx",
  "Location": "Station Name",
  "country": "XXX",
  "Lat": -34.0,
  "Lon": 25.6,
  "rate": 15,
  "units": "M",
  "lasttime": "2026-04-06T21:50:00.000",
  "lastvalue": 1.146,
  "sensor": "rad"
}
```

Key African countries with tide gauges (3-letter IOC country codes):
- `SOU` — South Africa
- `MOZ` — Mozambique
- `KEN` — Kenya
- `TNZ` — Tanzania
- `EGY` — Egypt
- `MOR` — Morocco
- `SEN` — Senegal
- `MAD` — Madagascar
- `CIV` — Côte d'Ivoire
- `NIG` — Nigeria
- `NAM` — Namibia

Data retrieval per station:
```
GET /service.php?query=data&code={station_code}&timestart=2026-04-06&timestop=2026-04-07&format=json
```

## Integration Notes

- **Station discovery**: Fetch the full station list and filter by African country
  codes or by lat/lon bounding box.
- **High-frequency data**: Some stations report every minute, others every 15 minutes.
  The `rate` field indicates the sampling interval.
- **Tsunami warning**: For Indian Ocean and Mediterranean stations, rapid sea level
  changes could be tsunami indicators. The IOC TOWS system uses this data.
- **Storm surge**: Combine with weather data to detect storm surge events affecting
  African coastal cities.
- **Data gaps**: Not all African coastal nations have operational tide gauges. Coverage
  is better on the east coast (Indian Ocean tsunami monitoring investment) than the
  west coast.
- **Sensor types**: `rad` (radar), `bub` (bubbler), `prs` (pressure). Radar sensors
  are generally more reliable.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 1–15 minute updates |
| Openness | 3 | No auth, UNESCO public data |
| Stability | 2 | UNESCO infrastructure, some stations intermittent |
| Structure | 2 | JSON but inconsistent field naming |
| Identifiers | 2 | IOC station codes (4-letter) |
| Richness | 2 | Sea level + basic station metadata |
