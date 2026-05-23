# Bahrain Air Quality - OpenAQ Coverage

- **Country/Region**: Bahrain (BH)
- **Endpoint**: `https://api.openaq.org/v3/locations?countries=BH` (OpenAQ API v3)
- **Protocol**: REST / HTTP GET
- **Auth**: Free API key required (X-API-Key header)
- **Format**: JSON
- **Freshness**: Varies by station (hourly to real-time)
- **Docs**: https://docs.openaq.org/
- **Score**: 6/18 (conditional — depends on station availability)

## Overview

OpenAQ is a global air quality data aggregator that collects measurements from
government monitoring networks, research institutions, and citizen sensor projects
worldwide. The platform provides a unified API for accessing PM2.5, PM10, O3, NO2,
SO2, CO, and other pollutant measurements from over 100 countries.

Bahrain (country code: BH) is a Gulf island nation with significant air quality
challenges due to:
- **Desert dust**: Frequent sand and dust storms, especially in summer
- **Industrial emissions**: Oil refining, aluminum smelting, and petrochemical facilities
- **Urban pollution**: Traffic emissions in Manama and surrounding areas
- **Marine port activity**: Diesel emissions from ships at Khalifa Bin Salman Port
- **Transboundary pollution**: Dust and pollutants from the Arabian Peninsula and Iran

The Supreme Council for Environment (SCE) is responsible for environmental monitoring
in Bahrain, including air quality. However, **the SCE website (sce.gov.bh) was
inaccessible during discovery** (403 Forbidden), so direct access to Bahrain's national
air quality network could not be verified.

OpenAQ aggregates air quality data from national networks worldwide. If Bahrain's SCE
operates monitoring stations and shares data with international platforms (WMO, UNEP,
or regional networks), those stations may appear in OpenAQ.

## Endpoint Analysis

**OpenAQ v3 API tested:**
```
GET https://api.openaq.org/v3/locations?countries=BH
Headers: X-API-Key: <free_api_key>
```

**Result during discovery:**
- HTTP 401 Unauthorized — API key required (expected)
- Could not verify station presence without a valid API key

**OpenAQ v2 API tested (now retired):**
```
GET https://api.openaq.org/v2/locations?country=BH
```

**Result:**
- HTTP 410 Gone — "Version 1 and Version 2 API endpoints are retired and no longer
  available. Please migrate to Version 3 endpoints."

**OpenAQ v3 requires free API key:**
OpenAQ v3 (launched 2024) requires users to register for a free API key at
https://explore.openaq.org/. The key is passed in the `X-API-Key` HTTP header for all
requests. Free tier limits are generous (thousands of requests per day).

**To verify Bahrain station availability:**
1. Register for free OpenAQ v3 API key
2. Query `https://api.openaq.org/v3/locations?countries=BH` with `X-API-Key` header
3. Check response for Bahrain monitoring stations

**Potential outcomes:**
- **Bahrain stations found**: SCE or another Bahrain entity shares data with OpenAQ.
  Stations would have lat/lon, pollutant parameters, update frequency, and measurement
  units. Proceed to integration.
- **No stations found**: Bahrain does not share air quality data with OpenAQ. Either
  SCE operates a closed network, or data is published only on sce.gov.bh (which was
  inaccessible during discovery).

## Integration Notes

**Why Bahrain air quality would be valuable:**
- **Gulf region coverage**: No existing air quality bridges for Gulf states in the repo
- **Unique air quality profile**: Desert dust events, oil/gas industry emissions,
  marine pollution combine to create distinct pollution patterns
- **Small geographic area**: Bahrain is a compact island nation (~765 km²), so a small
  number of stations can provide good spatial coverage
- **OpenAQ domain fit**: Repo could add a generic OpenAQ bridge that works for any
  country, with Bahrain as an initial use case

**Current blockers:**
- OpenAQ v3 API key required to verify station presence (free but requires registration)
- SCE website (sce.gov.bh) was inaccessible during discovery, so national air quality
  network could not be assessed directly
- Unknown whether Bahrain shares air quality data with OpenAQ or other international
  aggregators

**Alternative approaches if OpenAQ has no Bahrain stations:**
1. **Contact SCE directly**: Inquire about public air quality data availability, API
   access, or data sharing with OpenAQ.
2. **Check regional networks**: Gulf Cooperation Council Environmental Information
   System (if it exists) or UNEP Regional Office for West Asia.
3. **Sensor.Community (citizen sensors)**: No Bahrain sensors found during discovery,
   but this could change (community-driven network).
4. **Wait for sce.gov.bh to become accessible**: The site may have been temporarily
   down or blocking non-Bahrain traffic. Retry from Bahrain IP or contact site admins.

**Generic OpenAQ bridge opportunity:**
If Bahrain (or other countries) have stations in OpenAQ, a generic `openaq` bridge
could be created that:
- Polls OpenAQ v3 API for specified countries or bounding boxes
- Fetches latest measurements for PM2.5, PM10, O3, NO2, SO2, CO
- Keys events by OpenAQ location ID (stable, globally unique)
- Works for any country/region with OpenAQ coverage

This would be analogous to the generic GTFS bridge, which works for any transit agency.
OpenAQ covers 100+ countries with 10,000+ stations, so a single bridge could unlock
air quality data for dozens of regions.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Typically hourly, some stations near-real-time |
| Openness | 2 | Free API key required, generous limits |
| Stability | 3 | OpenAQ is established platform, versioned API |
| Structure | 3 | JSON with typed fields, well-documented |
| Identifiers | 2 | OpenAQ location IDs are stable; geographic identifiers (lat/lon) available |
| Additive value | 2 | New domain (air quality) for Gulf region; generic bridge would cover many countries |

**Verdict**: **Conditional — requires verification**. OpenAQ v3 is a strong candidate
for a generic air quality bridge, but **Bahrain station availability must be confirmed**
before proceeding. The platform is well-documented, uses a modern REST API with JSON,
and covers 100+ countries. If Bahrain has stations in OpenAQ, this is a strong
candidate (score 14-15). If not, the verdict changes to "not viable for Bahrain"
but "still viable for other countries."

**Next steps:**
1. **Register for free OpenAQ v3 API key** at https://explore.openaq.org/
2. **Query for Bahrain stations**: `GET https://api.openaq.org/v3/locations?countries=BH`
   with `X-API-Key` header
3. **If stations found**: Proceed to design generic OpenAQ bridge (Bahrain as initial
   target, but extensible to other countries)
4. **If no stations found**: Investigate SCE direct contact, regional networks, or
   Sensor.Community as alternatives
5. **Monitor**: Check if sce.gov.bh becomes accessible and publishes air quality data
   or API documentation
