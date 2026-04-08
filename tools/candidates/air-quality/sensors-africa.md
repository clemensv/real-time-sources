# sensors.AFRICA — Pan-African Citizen Science Air Quality Network

- **Country/Region**: Pan-African (Nigeria, Kenya, Ghana, Tanzania, Zambia)
- **Endpoint**: `https://api.sensors.africa/v2/`
- **Protocol**: REST (Django REST framework)
- **Auth**: None for key endpoints (`/v2/cities/`, `/v2/nodes/list-nodes/`, `/v2/locations/`); auth required for `/v2/now/`, `/v2/data/`, `/v2/sensor-types/`
- **Format**: JSON
- **Freshness**: Real-time — sensors report every ~3 minutes; `/v2/nodes/list-nodes/` includes last-5-minute stats
- **Docs**: https://api.sensors.africa/docs/
- **Score**: 11/18
- **Verdict**: **VIABLE CANDIDATE** — genuine real-time sensor network, but small fleet and partial auth restrictions

## Overview

sensors.AFRICA is a pan-African citizen science initiative by Code for Africa that
deploys low-cost ESP8266/ESP32 particle sensors to monitor air quality in African
cities. It measures PM1.0 (P0), PM2.5 (P2), PM10 (P1), temperature, and humidity.
Funded by innovateAFRICA, incubated by Code for Africa.

GitHub: https://github.com/CodeForAfrica/sensors.AFRICA

## Live API Probing (April 2026)

### Cities (11 across 6 countries)

| City | Country | Active Nodes |
|------|---------|:------------:|
| Nairobi | Kenya | ~8 |
| Nakuru | Kenya | ~12 |
| Kisumu | Kenya | ~1 |
| Mombasa | Kenya | ~1 |
| Lagos | Nigeria | ~5 |
| Abuja | Nigeria | ~5 |
| Ado-Ekiti / Akure | Nigeria | ~3 |
| Awka | Nigeria | ~3 |
| Accra | Ghana | ~6 |
| Kumasi | Ghana | ~1 |
| Lusaka | Zambia | ~1 |
| Dar es Salaam | Tanzania | listed but no active nodes seen |

### Node Fleet

`GET /v2/nodes/list-nodes/` returned **~50 node entries** (some duplicates from
relocated nodes). Sensors report every ~3 minutes. Many nodes were active within
the hour of probing (timestamps like `2026-04-08T05:52:*`).

### Value Types

| Code | Meaning | Unit |
|------|---------|------|
| P0 | PM1.0 | µg/m³ |
| P1 | PM10 | µg/m³ |
| P2 | PM2.5 | µg/m³ |
| temperature | Air temperature | °C |
| humidity | Relative humidity | % |

### Endpoint Access Matrix

| Endpoint | Auth Required | Status |
|----------|:------------:|--------|
| `GET /v2/cities/` | No | 200 — returned 11 cities with coordinates |
| `GET /v2/nodes/list-nodes/` | No | 200 — full node list with recent stats |
| `GET /v2/locations/` | No | Likely 200 (paginated) |
| `GET /v2/data/` | **Yes** | 403 for unauthenticated |
| `GET /v2/now/` | **Yes** | 403 for unauthenticated |
| `GET /v2/sensor-types/` | **Yes** | 403 for unauthenticated |
| `GET /v2/data/stats/{type}/` | Unknown | Returns aggregated stats by city/interval |
| `GET /v2/sensors/` | Unknown | Sensor list |

### Key Observation

The `/v2/nodes/list-nodes/` endpoint is the most useful **unauthenticated** endpoint.
It returns every public node with:
- Node UID (e.g., `esp8266-935156`, `ESP32-6896B3F16E20`)
- Location name, lat/lon, city
- `last_data_received_at` timestamp
- Recent stats per value type: average, minimum, maximum, start/end datetime

This effectively serves as a "current readings" endpoint without needing auth.

## Integration Notes

- **Polling strategy**: Poll `/v2/nodes/list-nodes/` every 5 minutes. Each node
  includes its latest stats with timestamps — delta-detect on `last_data_received_at`.
- **Reference data**: `/v2/cities/` for city catalog, node locations from the
  nodes endpoint.
- **Key model**: `{node_uid}` or `{city_slug}/{sensor_id}` — node UIDs are stable
  hardware identifiers (ESP MAC-derived).
- **Small fleet**: ~50 nodes total is small compared to PurpleAir (~30,000) or
  Sensor.Community (~15,000). However, it fills a unique geographic niche — African
  cities with almost no other monitoring.
- **Overlap with OpenAQ**: Some sensors.AFRICA data may already flow into OpenAQ.
  Check for duplication before implementing both.
- **Hardware reliability**: Many nodes show intermittent reporting. Some haven't
  reported in months. The network has significant uptime issues.

## Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time, sensors report every ~3 min |
| Openness | 2 | Key endpoints are public; detailed data needs auth |
| Stability | 1 | Small NGO project, hardware reliability issues, many nodes go offline |
| Structure | 2 | Clean JSON, well-structured Django REST framework API |
| Identifiers | 2 | Node UIDs (hardware MAC-based), sensor IDs, city slugs |
| Richness | 1 | Only PM + temp + humidity; no gas-phase pollutants (NO₂, O₃, SO₂) |

## Comparison with Alternatives

- **OpenAQ** (score 13/18): Broader coverage, more pollutants, but requires API key.
  OpenAQ aggregates data from many sources including government reference stations.
- **Sensor.Community** (Luftdaten): ~15,000 nodes globally but very few in Africa.
- **PurpleAir**: Large network but negligible African presence.

sensors.AFRICA is the **only dedicated African citizen science air quality API** but
its small size and auth restrictions limit its standalone value. Best pursued after
OpenAQ, or as a complement if unique stations are confirmed.
