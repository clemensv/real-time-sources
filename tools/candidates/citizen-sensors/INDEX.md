# Citizen Sensor Network Candidates

Real-time data from citizen-operated environmental sensor networks.

| Source | Protocol | Auth | Freshness | Total Score |
|--------|----------|------|-----------|-------------|
| [iNaturalist](inaturalist.md) | REST | None | Seconds | 18/18 |
| [eBird](ebird.md) | REST | API Key (free) | Minutes | 17/18 |
| [Sensor.Community](sensor-community.md) | REST | None | ~5 min | 16/18 |
| [PurpleAir](purpleair.md) | REST | API Key | ~2 min | 15/18 |
| [Smart Citizen](smart-citizen.md) | REST | None | 1-5 min | 15/18 |
| [openSenseMap](opensensemap.md) | REST | None | 1-10 min | 14/18 |
| [Netatmo Weathermap](netatmo-weathermap.md) | REST | OAuth2 (free) | 5-10 min | 13/18 |
| [Safecast](safecast.md) | REST | None | Sporadic | 13/18 |
| [CWOP/MADIS](cwop-madis.md) | APRS-IS / HTTP | Mixed | Real-time / Hourly | 13/18 |

## Summary

iNaturalist is the new standout — a perfect 18/18 score for a planet-scale biodiversity observation platform with 335M+ observations, zero-auth API, and real-time availability. eBird complements it with the world's largest bird monitoring network (200M+ observations/year, free API key).

Sensor.Community remains the leader for open air quality monitoring. PurpleAir and Smart Citizen offer complementary sensor coverage — Smart Citizen's multi-sensor approach (air quality + noise + weather) from Barcelona's Fab Lab is particularly interesting. Netatmo adds unmatched urban weather station density, especially in European cities, though its OAuth2 requirement and anonymized stations are friction points.

openSenseMap, Safecast, and CWOP/MADIS round out the category with flexible platforms, radiation data, and legacy ham radio weather infrastructure respectively.
