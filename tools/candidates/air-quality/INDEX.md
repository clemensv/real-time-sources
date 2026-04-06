# Air Quality and Atmospheric Composition — Candidate Sources

Scouted: 2026-04-06

## Summary

| # | Source | Region | API? | Auth | Freshness | Total Score | Priority |
|---|--------|--------|------|------|-----------|-------------|----------|
| 1 | [OpenAQ](openaq.md) | Global | ✅ REST v3 | API Key (free) | Hourly–RT | 18/18 | 🟢 HIGH |
| 2 | [US EPA AirNow](us-epa-airnow.md) | US/CA/MX | ✅ REST | API Key (free) | Hourly | 15/18 | 🟢 HIGH |
| 3 | [Defra AURN](defra-aurn.md) | UK | ✅ SOS/REST | None | Hourly | 16/18 | 🟢 HIGH |
| 4 | [UBA Germany](uba-germany.md) | Germany | ✅ REST v3 | None | Hourly | 16/18 | 🟢 HIGH |
| 5 | [Sensor.Community](sensor-community.md) | Global | ✅ REST | None | ~2.5 min | 15/18 | 🟡 MEDIUM |
| 6 | [PurpleAir](purpleair.md) | Global (US-heavy) | ✅ REST v1 | API Key (free) | ~2 min | 14/18 | 🟡 MEDIUM |
| 7 | [AQICN / WAQI](aqicn-waqi.md) | Global | ✅ REST | API Key (free) | Hourly | 13/18 | 🟡 MEDIUM |
| 8 | [EEA Air Quality](eea-air-quality.md) | Europe | ⚠️ Bulk DL | None | Hourly | 13/18 | 🟡 MEDIUM |
| 9 | [South Korea AirKorea](south-korea-airkorea.md) | South Korea | ✅ REST | API Key (free) | Hourly | 13/18 | 🟡 MEDIUM |
| 10 | [NSW EPA Australia](nsw-epa-australia.md) | Australia (NSW) | ✅ REST (likely) | Unknown | Hourly | 13/18 | 🟡 MEDIUM |
| 11 | [Japan SORAMAME](japan-soramame.md) | Japan | ❌ Web only | N/A | Hourly | 7/18 | 🔴 LOW |
| 12 | [India CPCB](india-cpcb.md) | India | ❌ Web only | N/A | 15-min | 7/18 | 🔴 LOW |

## Recommended Implementation Order

1. **OpenAQ** — global aggregator; one API covers 130+ countries. Start here.
2. **UBA Germany** — clean REST API, no auth, well-structured. Good model for national connectors.
3. **Defra AURN** — standard SOS API, no auth. Immediate integration.
4. **US EPA AirNow** — authoritative US source with forecasts not in OpenAQ.
5. **Sensor.Community** — real-time citizen science; no auth; unique granularity.
6. **PurpleAir** — delta queries via `modified_since`; needs API key + non-commercial license.
7. **AQICN/WAQI** — pre-calculated AQI and forecasts; restrictive license.
8. **South Korea AirKorea** / **NSW EPA** / **EEA** — regional supplements as needed.

## Key Observations

- **OpenAQ is the meta-aggregator**: It already ingests data from AirNow, EEA, CPCB, several Australian EPAs, PurpleAir, and many others. Implementing OpenAQ first gives the broadest coverage with the least effort.
- **Citizen science fills gaps**: Sensor.Community and PurpleAir provide hyper-local, near-real-time data in areas where government monitors are sparse.
- **License matters**: OpenAQ (CC BY 4.0), Defra (OGL), UBA (dl-de), and AirNow (US Public Domain) are the most permissive. PurpleAir and AQICN restrict commercial use.
- **Japan and India lack APIs**: Despite being major air quality markets, SORAMAME and CPCB only offer web dashboards. Use OpenAQ or AQICN as intermediaries.
- **Forecasts are rare**: Only AirNow and AQICN provide air quality forecasts via API. This is a differentiating feature.
