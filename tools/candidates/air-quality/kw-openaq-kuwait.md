# OpenAQ Kuwait Air Quality Stations

> ✅ **SHIPPED** · feeder: `openaq` · entry: `kuwait` · 2026-06-22


- **Country/Region**: Kuwait
- **Endpoint**: `https://api.openaq.org/v3/locations?countries_id=119` (v3 API)
- **Protocol**: REST / HTTP JSON
- **Auth**: API key required (free tier available)
- **Format**: JSON
- **Freshness**: Hourly to daily (varies by station)
- **Docs**: https://docs.openaq.org/
- **Score**: 7/18

## Overview

OpenAQ aggregates air quality data from government monitoring networks and low-cost sensor projects worldwide. Kuwait (country_id 119 in OpenAQ v3) historically had monitoring stations reporting PM2.5, PM10, O₃, NO₂, SO₂, and CO measurements to the OpenAQ platform.

The Kuwaiti data likely originates from:
- **Kuwait Environment Public Authority (EPA)** — government monitoring network
- **eMISK** (Environmental Monitoring Information System of Kuwait) — national air quality platform
- Possible embassy or research sensors

OpenAQ v2 API (which provided unauthenticated access) was **sunset in 2024**. The v3 API now requires a free API key obtained from the OpenAQ website. Historical data showed Kuwait had 5–10 active monitoring locations, primarily in Kuwait City and industrial zones.

## Endpoint Analysis

**v3 API requires authentication** — probing without an API key returns 401 Unauthorized.

```
GET https://api.openaq.org/v3/locations?countries_id=119&limit=100
Authorization: Bearer <api_key>
```

**Probe result** (2025-05-23):
- HTTP 401 Unauthorized without key
- API key registration is free at https://explore.openaq.org/
- Rate limits: 10 requests/second, 10,000/day on free tier

**Historical coverage** (from v2 era):
- ~5-10 stations across Kuwait
- Parameters: PM2.5, PM10, O₃, NO₂, SO₂, CO
- Update frequency: hourly to daily depending on station
- Notable stations: Kuwait City, Jahra, Ahmadi industrial area

The v3 API response format is JSON with pagination. Each location includes:
- `id`: OpenAQ location ID
- `name`: Station name
- `coordinates`: lat/lon
- `parameters`: Available pollutants
- `lastUpdated`: Most recent measurement timestamp
- Nested measurements endpoint for time-series data

## Schema / Sample Payload

**Expected v3 response** (format based on v3 docs, not probed live):

```json
{
  "meta": {
    "found": 8
  },
  "results": [
    {
      "id": 12345,
      "name": "Kuwait City Central",
      "locality": "Kuwait City",
      "timezone": "Asia/Kuwait",
      "coordinates": {
        "latitude": 29.3759,
        "longitude": 47.9774
      },
      "country": {
        "id": 119,
        "code": "KW",
        "name": "Kuwait"
      },
      "owner": {
        "id": 456,
        "name": "Kuwait EPA"
      },
      "provider": {
        "id": 789,
        "name": "eMISK"
      },
      "isMobile": false,
      "isMonitor": true,
      "parameters": [
        {"id": 2, "name": "pm25", "units": "µg/m³"},
        {"id": 1, "name": "pm10", "units": "µg/m³"},
        {"id": 5, "name": "o3", "units": "µg/m³"},
        {"id": 3, "name": "no2", "units": "µg/m³"}
      ],
      "datetime": {
        "first": "2018-01-01T00:00:00Z",
        "last": "2025-05-23T06:00:00Z"
      }
    }
  ]
}
```

## Why It's Marginal

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Freshness | 1 | Hourly to daily — not real-time |
| Openness | 2 | Free API key required, generous limits |
| Stability | 2 | Versioned API, but v2→v3 migration broke unauthenticated access |
| Structure | 3 | Well-documented JSON API |
| Identifiers | 2 | OpenAQ location IDs are stable |
| Additive value | 0 | OpenAQ is a **global aggregator** — building a Kuwait-specific bridge duplicates a future global OpenAQ bridge |

## Limitations

- **API key required** — OpenAQ v3 dropped unauthenticated access. Free tier is available but requires registration, which is a friction point for open-source deployment.
- **Aggregator, not primary source** — OpenAQ scrapes data from upstream sources (Kuwait EPA/eMISK). A bridge to the **primary source** (eMISK platform) would be preferred if accessible.
- **Update cadence varies** — Some stations report hourly, others daily. Not suitable for minute-level streaming.
- **Kuwait coverage uncertain** — Without live probing (API key required), we cannot verify current station count or data freshness. Historical coverage was modest (~8 stations).
- **Global bridge preferred** — If this repo builds an OpenAQ bridge, it should cover all countries, not just Kuwait.

## Alternative: Direct eMISK Access

The **Environmental Monitoring Information System of Kuwait (eMISK)** is the upstream source for Kuwait's air quality data. If eMISK exposes a public API or data portal, it would be a better candidate than OpenAQ because:
- No third-party aggregator dependency
- Potentially more stations and parameters
- Direct access to Kuwait EPA's operational network

**eMISK investigation** (2025-05-23):
- Website: https://www.emisk.org (connection failed during probe)
- May require VPN or be accessible only within Kuwait
- If accessible, this should be the primary candidate, not OpenAQ

## Verdict

**Verdict**: ❌ **Skip** — OpenAQ is a global aggregator. If this repo adds air quality bridges, prioritize:
1. **Direct national sources** (eMISK for Kuwait, if API exists)
2. **A global OpenAQ bridge** covering all countries (not Kuwait-specific)

Documented here as a fallback option but not recommended for Kuwait-specific implementation. The OpenAQ v3 API key requirement and hourly-to-daily cadence make it a poor fit for real-time streaming compared to government sources with sub-hourly updates.
