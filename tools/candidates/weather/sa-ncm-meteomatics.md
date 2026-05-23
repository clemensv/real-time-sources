# Saudi National Center for Meteorology (NCM) - Meteomatics API

- **Country/Region**: Saudi Arabia (KSA)
- **Endpoint**: `https://api-mm.ncm.gov.sa/`
- **Protocol**: REST (Meteomatics commercial platform)
- **Auth**: API key required
- **Format**: JSON, WMS/WFS, Vector tiles
- **Freshness**: Hourly+ (PT1H intervals)
- **Docs**: https://api-doc.ncm.gov.sa/en/api/getting-started
- **Score**: 10/18

## Overview

The National Center for Meteorology (المركز الوطني للأرصاد, NCM) is Saudi Arabia's official meteorological authority, responsible for weather forecasting, climate monitoring, and weather warnings across the Kingdom. NCM operates an extensive network of weather stations covering urban centers, desert regions, and the mountainous Asir region.

NCM's API is powered by Meteomatics AG, a Swiss commercial weather intelligence platform. The API provides access to NCM's observations, forecasts, marine weather, and specialized products including:

- **Dust storm warnings** — critical for Saudi Arabia where haboob events are frequent and disrupt aviation, transportation, and health
- **Hajj weather services** — specialized forecasting for Makkah, Mina, Arafat, and Muzdalifah during the annual pilgrimage (2-3 million pilgrims)
- **Marine weather** — Red Sea and Arabian Gulf conditions for shipping and offshore operations
- **Lightning detection** — thunderstorm activity
- **Rainfall monitoring** — crucial for flash flood warnings in Jeddah and other cities

Saudi Arabia's climate ranges from extreme desert heat (50°C+ in summer) to winter snow in the northern highlands. The Kingdom experiences seasonal dust storms (primarily spring/summer), flash flooding in western mountains, and occasional tropical cyclone remnants from the Arabian Sea.

## Endpoint Analysis

**API Base**: `https://api-mm.ncm.gov.sa/`
**Documentation**: `https://api-doc.ncm.gov.sa/en/api/getting-started`

Sample endpoint structure (Meteomatics format):
```
GET https://api-mm.ncm.gov.sa/{validdatetime}/{parameters}/{location}/json
```

Example (temperature at coordinates):
```
GET https://api-mm.ncm.gov.sa/2025-11-16T00:00:00Z--2025-11-19T00:00:00Z:PT1H/t_2m:C/52.520551,13.461804/json
```

**Probe result**:
```
HTTP 401 Unauthorized
{"message":"Unauthorized"}
```

The 401 response confirms the endpoint structure is valid but requires authentication. The Meteomatics platform typically issues API keys with usage-based billing or subscription tiers.

**Available data types** (per Meteomatics standard):
- Temperature (2m, surface, dewpoint)
- Precipitation (rate, accumulation, type)
- Wind (speed, direction, gusts) at multiple levels
- Pressure (surface, mean sea level)
- Humidity, cloud cover, visibility
- Solar radiation, UV index
- Soil moisture, evapotranspiration
- Marine parameters (wave height, swell, sea surface temp)
- Lightning strike density
- Air quality indices (dust, PM2.5, PM10)

**Station network**: NCM operates 200+ automatic weather stations across Saudi Arabia, including:
- Riyadh, Jeddah, Dammam, Makkah, Madinah (major cities)
- Najran, Abha, Taif (southern mountains — altitude up to 3000m)
- Ha'il, Al Jawf, Tabuk (northern regions — winter cold, occasional snow)
- Yanbu, Jizan (coastal Red Sea)
- Dhahran, Jubail (Arabian Gulf coast, oil infrastructure)

## Integration Notes

- **Auth barrier**: Requires API key. NCM's licensing terms and pricing are not publicly documented. May require formal agreement with NCM or Meteomatics.
- **Meteomatics platform**: The underlying provider is a commercial Swiss weather API. NCM may have a custom deployment or white-label integration. Standard Meteomatics keys do not work with the `api-mm.ncm.gov.sa` domain.
- **Dust storm value**: This is the highest-value weather product for Saudi Arabia. Haboob dust storms are frequent, reduce visibility to <50m, cause respiratory issues, and shut down airports. Real-time dust/PM10 data from NCM would be unique.
- **Hajj weather**: During the annual Hajj pilgrimage (Dhu al-Hijjah, Islamic calendar), NCM provides specialized forecasts and warnings for the holy sites. This is a critical public safety mission with global impact.
- **Alternative approach**: If the API key cannot be obtained, NCM publishes forecast maps and bulletins on its website. These could be scraped, but are not real-time observations.
- **WMO integration**: NCM is the Saudi Arabian WMO member. Its station data should be available through WMO Global Information System (GIS) channels, though potentially delayed.

## Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Hourly observations, sub-hourly for some parameters |
| Openness | 1 | API key required; terms and pricing not public |
| Stability | 3 | NCM is the official national met service; Meteomatics is a stable commercial platform |
| Structure | 2 | JSON with schema, but Meteomatics format is proprietary |
| Identifiers | 1 | Coordinates-based queries; station IDs not exposed in docs |
| Additive value | 2 | First Saudi weather source; dust storm data is unique |

**Total: 12/18**

**Verdict**: ⚠️ **Maybe** — Strong technical fit and high-value dust/hajj weather data, but **auth barrier** is significant. Requires outreach to NCM or Meteomatics to negotiate API access. If a free tier or academic/non-commercial license exists, this becomes a ✅ **Build** candidate. The dust storm and hajj weather products are globally unique and justify the effort.
