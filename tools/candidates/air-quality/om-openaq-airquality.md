# OpenAQ - Oman Air Quality Monitoring

- **Country/Region**: Global (filter for Oman, country code `OM`)
- **Endpoint**: `https://api.openaq.org/v3/locations?countries=OM` (v3 API)
- **Protocol**: REST (HTTP JSON API)
- **Auth**: API key required (v3)
- **Format**: JSON
- **Freshness**: Hourly (typical for government air quality monitoring stations)
- **Docs**: https://docs.openaq.org/
- **Score**: 10/18 (if Oman stations exist)

## Overview

**OpenAQ** is a global open-source platform that aggregates real-time air quality data from government monitoring networks, research-grade sensors, and citizen science projects worldwide. OpenAQ ingests data from:
- Official government monitoring networks (environment ministries, EPA equivalents)
- Low-cost sensor networks (PurpleAir, Sensor.Community)
- Research institutions
- Open data portals

For Oman, OpenAQ **could** provide access to:
- **Environment Authority (EA) monitoring stations** (if EA publishes data to WMO or other aggregators)
- **Municipality air quality networks** (Muscat, Salalah) if they operate PM2.5/PM10/O₃ monitors
- **Industrial monitoring** (oil/gas facilities, ports, cement plants) if data is publicly shared
- **Research sensors** (Sultan Qaboos University or other institutions)

Oman's air quality challenges include:
- **Desert dust storms** (shamal winds from Iraq/Saudi Arabia, local dust devils)
- **Vehicle emissions** in Muscat and other urban areas
- **Industrial emissions** from oil refineries, LNG plants (Sohar, Sur, Duqm), cement factories
- **Seasonal haze** from agricultural burning in South Asia (transboundary pollution)

However, public air quality monitoring infrastructure in Oman is **less developed** than in Europe, North America, or East Asia. The Environment Authority (EA) may operate monitoring stations, but data publication is unclear.

## Endpoint Analysis

**API requires authentication (v3), no Oman stations found** — testing of the OpenAQ v3 API (2026-05-23) returned:
```
{"message": "Unauthorized. A valid API key must be provided in the X-API-Key header."}
```

The OpenAQ v2 API (now retired as of 2024) previously allowed unauthenticated queries but returned:
```
{"message": "Gone. Version 1 and Version 2 API endpoints are retired and no longer available."}
```

To verify whether Oman has air quality monitoring stations in the OpenAQ database, an **API key** is required. OpenAQ API keys are **free** but require registration at https://explore.openaq.org/.

### Expected Query (with API key):
```
GET https://api.openaq.org/v3/locations?countries=OM&limit=100
Headers:
  X-API-Key: <your_api_key>
```

If Oman stations exist, the response would include:
```json
{
  "results": [
    {
      "id": 12345,
      "name": "Muscat - Al Khuwair",
      "locality": "Muscat",
      "country": "OM",
      "coordinates": {"latitude": 23.XX, "longitude": 58.XX},
      "sensors": [
        {"parameter": "pm25", "units": "µg/m³"},
        {"parameter": "pm10", "units": "µg/m³"}
      ],
      "lastUpdated": "2026-05-23T07:00:00Z"
    }
  ]
}
```

### Reality Check: Oman Air Quality Data Availability

A manual search of the OpenAQ web interface (https://explore.openaq.org/) during discovery did **not reveal any active monitoring stations in Oman**. This suggests:
1. Oman's Environment Authority does not currently publish real-time air quality data to international aggregators (WMO, OpenAQ, etc.)
2. No citizen science sensor networks (PurpleAir, Sensor.Community) have deployed sensors in Oman, or if they have, the data is not shared publicly
3. Oman may operate internal monitoring (e.g., for oil/gas facilities or airports) but does not make data publicly available

By contrast, neighboring UAE has dozens of stations in OpenAQ (Abu Dhabi, Dubai, Sharjah environment departments publish real-time PM2.5/PM10/O₃/NO₂).

## Integration Notes

- **If Oman stations exist in OpenAQ**, the integration would be straightforward:
  - Poll the `/v3/locations` endpoint to get station list
  - Poll `/v3/measurements` for each station to get latest readings (hourly cadence typical)
  - Key events by station ID + parameter (e.g., `station_12345/pm25`)
  - Normalize to µg/m³ for PM2.5/PM10, ppb for O₃/NO₂
  
- **OpenAQ v3 API changes** (vs. v2):
  - API key required for all endpoints (v2 was public)
  - Rate limits enforced (free tier: 100 requests/minute, 10,000/day typical)
  - Better temporal queries (start/end timestamps)
  - Sensor-level metadata (measurement intervals, data quality flags)

- **Overlap with existing sources**: The repo does not currently have air quality coverage. If Oman stations exist in OpenAQ, this would be **additive**. However, if OpenAQ aggregates Oman Environment Authority data, it's better to bridge **EA's direct API** (if one exists) rather than OpenAQ, to avoid aggregation lag and ensure authoritative source attribution.

- **Alternative: Sensor.Community deployment**: If no government monitoring exists, **deploy low-cost PM2.5 sensors** in Oman (Sensor.Community kits) and publish the data to OpenAQ. This is a **citizen science** approach but requires physical presence in Oman to install sensors. Out of scope for pure data source discovery.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Hourly updates typical for government stations |
| Openness | 2 | Free API key required (v3), rate limits apply |
| Stability | 3 | OpenAQ is a well-established nonprofit with multi-year operational history |
| Structure | 3 | JSON API with formal schema, well-documented |
| Identifiers | 2 | Station IDs are stable, but parameter naming varies by source |
| Additive value | -2 | **No Oman stations found in OpenAQ during discovery** |

**Verdict**: ❌ Skip

**Rationale**: **No active air quality monitoring stations in Oman were found in the OpenAQ database** as of 2026-05-23. This suggests Oman's Environment Authority does not currently publish real-time air quality data to public aggregators. While the OpenAQ platform itself is excellent (well-documented API, global coverage, strong data quality practices), **there is no Oman data to bridge**.

**Alternative recommendations**:
1. **Contact Oman Environment Authority (ea.gov.om)** directly to inquire:
   - Does EA operate air quality monitoring stations (PM2.5, PM10, O₃, NO₂)?
   - Is the data published in real-time to a public portal or API?
   - If not currently public, would EA consider publishing data to OpenAQ or a national open data portal?
   
2. **Check neighboring UAE and Saudi Arabia** for transboundary air quality monitoring. Abu Dhabi and Dubai have extensive networks in OpenAQ. These stations may capture dust storms and industrial plumes that affect Oman.

3. **Monitor OpenAQ for future Oman station additions**. If EA begins publishing data or if citizen science sensors are deployed, Oman stations would appear in OpenAQ automatically.

**If Oman stations appear in OpenAQ in the future, upgrade to ✅ Build.** The platform is already a proven fit for this repo's bridge pattern (similar to existing hydrology and weather sources).
