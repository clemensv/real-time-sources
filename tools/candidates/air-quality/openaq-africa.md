# OpenAQ Air Quality — African Stations

- **Country/Region**: Pan-African (South Africa, Nigeria, Kenya, Egypt, Ghana, Ethiopia, Uganda, Rwanda, Morocco, Tunisia, and more)
- **Endpoint**: `https://api.openaq.org/v3/locations?country=ZA&limit=100`
- **Protocol**: REST
- **Auth**: API key required (free registration)
- **Format**: JSON
- **Freshness**: Near real-time (hourly or better for most stations)
- **Docs**: https://docs.openaq.org/
- **Score**: 13/18

## Overview

OpenAQ is the world's largest open air quality data platform, aggregating data from
government monitoring networks, low-cost sensors, and research stations globally. Africa's
air quality monitoring network has grown dramatically in recent years, driven by:

- **Government stations**: South Africa (SAAQIS), Egypt, Morocco, Tunisia
- **US Embassy/Consulate monitors**: Nairobi, Lagos, Kampala, Addis Ababa, Dar es Salaam
- **Low-cost sensor networks**: PurpleAir and Clarity sensors in Kampala, Nairobi,
  Accra, Lagos
- **Research networks**: TAHMO stations with air quality sensors

African cities face severe air quality challenges from vehicular emissions, industrial
pollution, biomass burning, and Saharan dust events. The data gap in Africa makes every
station valuable.

## Endpoint Analysis

**API v2 deprecated** (410 Gone) — confirmed during probing. Must use v3 API.

**API v3 requires authentication** (401 Unauthorized) — free API key registration at
https://explore.openaq.org/register required.

The v3 API structure:
```
GET /v3/locations?country={ISO2}&limit=100
GET /v3/locations/{location_id}/measurements
GET /v3/locations/{location_id}/latest
GET /v3/countries — List countries with station counts
```

Known African station networks:
- **South Africa**: SAAQIS network — multiple cities, PM2.5/PM10/SO2/NO2/O3
- **Kenya (Nairobi)**: US Embassy + low-cost sensors
- **Nigeria (Lagos, Abuja)**: US Consulate + emerging government network
- **Uganda (Kampala)**: AirQo network — one of Africa's most impressive citizen
  science air quality networks
- **Ghana (Accra)**: EPA Ghana + research sensors
- **Egypt (Cairo)**: Government stations
- **Ethiopia (Addis Ababa)**: US Embassy
- **Rwanda (Kigali)**: Emerging network
- **Morocco**: National monitoring network

## Integration Notes

- **API key registration**: Required but free. Quick sign-up process.
- **Country iteration**: Poll `/v3/locations?country={ISO2}` for each African country
  to discover stations, then poll latest measurements.
- **Data quality varies**: Government reference stations produce high-quality data.
  Low-cost sensors are less accurate but provide spatial coverage.
- **AirQo Kampala**: The AirQo project in Uganda operates 100+ low-cost sensors and
  feeds into OpenAQ. This is a standout African air quality network.
- **Saharan dust events**: These cause dramatic spikes in PM10/PM2.5 across West and
  North Africa. Detecting and flagging these events adds value.
- **US Embassy stations**: Often the most reliable data source in African capitals,
  but only one station per city.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Hourly or better |
| Openness | 2 | Free API key required |
| Stability | 3 | Well-maintained platform |
| Structure | 2 | JSON API, v2→v3 migration shows instability |
| Identifiers | 2 | OpenAQ location IDs |
| Richness | 1 | Air quality parameters (PM2.5, PM10, gases) |
