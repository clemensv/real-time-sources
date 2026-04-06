# Air Quality and Atmospheric Composition — Candidate Sources

Scouted: 2026-04-06

## Summary

### Tier 1 — Ground-Station APIs (Global & National)

| # | Source | Region | API? | Auth | Freshness | Total Score | Priority |
|---|--------|--------|------|------|-----------|-------------|----------|
| 1 | [OpenAQ](openaq.md) | Global | ✅ REST v3 | API Key (free) | Hourly–RT | 18/18 | 🟢 HIGH |
| 2 | [US EPA AirNow](us-epa-airnow.md) | US/CA/MX | ✅ REST | API Key (free) | Hourly | 15/18 | 🟢 HIGH |
| 3 | [Defra AURN](defra-aurn.md) | UK | ✅ SOS/REST | None | Hourly | 16/18 | 🟢 HIGH |
| 4 | [UBA Germany](uba-germany.md) | Germany | ✅ REST v3 | None | Hourly | 16/18 | 🟢 HIGH |
| 5 | [Luchtmeetnet (NL)](luchtmeetnet-nl.md) | Netherlands | ✅ REST | None | Hourly | 17/18 | 🟢 HIGH |
| 6 | [IRCELINE (Belgium)](irceline-belgium.md) | Belgium | ✅ SOS/REST | None | Hourly | 16/18 | 🟢 HIGH |
| 7 | [LAQN London](laqn-london.md) | UK (London) | ✅ REST | None | Hourly | 17/18 | 🟢 HIGH |
| 8 | [Singapore NEA](singapore-nea.md) | Singapore | ✅ REST | None | Hourly | 16/18 | 🟢 HIGH |
| 9 | [Taiwan MOENV](taiwan-moenv.md) | Taiwan | ✅ REST | API Key (free) | Hourly | 16/18 | 🟢 HIGH |
| 10 | [Sensor.Community](sensor-community.md) | Global | ✅ REST | None | ~2.5 min | 15/18 | 🟡 MEDIUM |
| 11 | [NILU Norway](nilu-norway.md) | Norway | ✅ REST | API Key (req'd) | Hourly | 15/18 | 🟡 MEDIUM |
| 12 | [Canada AQHI](canada-aqhi.md) | Canada | ⚠️ Files/WMS | None | Hourly | 15/18 | 🟡 MEDIUM |
| 13 | [GIOŚ Poland](gios-poland.md) | Poland | ✅ REST | None (rate-limited) | Hourly | 14/18 | 🟡 MEDIUM |
| 14 | [PurpleAir](purpleair.md) | Global (US-heavy) | ✅ REST v1 | API Key (free) | ~2 min | 14/18 | 🟡 MEDIUM |
| 15 | [FMI Finland](fmi-finland.md) | Finland | ✅ WFS 2.0 | None | Hourly | 14/18 | 🟡 MEDIUM |
| 16 | [AQICN / WAQI](aqicn-waqi.md) | Global | ✅ REST | API Key (free) | Hourly | 13/18 | 🟡 MEDIUM |
| 17 | [EEA Air Quality](eea-air-quality.md) | Europe | ⚠️ Bulk DL | None | Hourly | 13/18 | 🟡 MEDIUM |
| 18 | [Hong Kong EPD](hongkong-epd.md) | Hong Kong | ⚠️ XML feed | None | Hourly | 13/18 | 🟡 MEDIUM |
| 19 | [Atmo France](atmo-france.md) | France | ⚠️ ArcGIS | Varies | Hourly | 13/18 | 🟡 MEDIUM |
| 20 | [Swiss NABEL](swiss-nabel.md) | Switzerland | ⚠️ WMS/CSV | None | Hourly | 13/18 | 🟡 MEDIUM |
| 21 | [South Korea AirKorea](south-korea-airkorea.md) | South Korea | ✅ REST | API Key (free) | Hourly | 13/18 | 🟡 MEDIUM |
| 22 | [NSW EPA Australia](nsw-epa-australia.md) | Australia (NSW) | ✅ REST (likely) | Unknown | Hourly | 13/18 | 🟡 MEDIUM |
| 23 | [Mexico SINAICA](mexico-sinaica.md) | Mexico | ❌ Web/CSV | N/A | Hourly | 11/18 | 🔴 LOW |
| 24 | [Chile SINCA](chile-sinca.md) | Chile | ❌ Web/CSV | N/A | Hourly | 8/18 | 🔴 LOW |
| 25 | [Japan SORAMAME](japan-soramame.md) | Japan | ❌ Web only | N/A | Hourly | 7/18 | 🔴 LOW |
| 26 | [India CPCB](india-cpcb.md) | India | ❌ Web only | N/A | 15-min | 7/18 | 🔴 LOW |

### Africa-Focused Sources

| # | Source | Region | API? | Auth | Freshness | Total Score | Priority |
|---|--------|--------|------|------|-----------|-------------|----------|
| A1 | [OpenAQ Africa](openaq-africa.md) | Pan-African | ✅ REST v3 | API Key (free) | Hourly | 13/18 | 🟡 MEDIUM |
| A2 | [WAQI Africa](waqi-africa-stations.md) | Pan-African | ✅ REST | API Key (free) | Hourly | 13/18 | 🟡 MEDIUM |
| A3 | [AirQo Uganda](airqo-uganda.md) | Uganda (Kampala) | ✅ REST | API Key (free) | Hourly | 13/18 | 🟡 MEDIUM |

### Tier 2 — Satellite & Modelled Data

| # | Source | Region | API? | Auth | Freshness | Total Score | Priority |
|---|--------|--------|------|------|-----------|-------------|----------|
| 27 | [Copernicus CAMS](copernicus-cams.md) | Global/Europe | ✅ CDS API | Token (free) | Daily forecasts | 13/18 | 🟡 MEDIUM |
| 28 | [Sentinel-5P TROPOMI](sentinel-5p-tropomi.md) | Global | ✅ OData | Account (free) | Daily (NRTI <3h) | 13/18 | 🟡 MEDIUM |
| 29 | [NOAA GML Greenhouse](noaa-gml-greenhouse.md) | Global | ⚠️ File DL | None | Monthly | 14/18 | 🟡 MEDIUM |

### Tier 3 — Specialized (Pollen & Bioaerosols)

| # | Source | Region | API? | Auth | Freshness | Total Score | Priority |
|---|--------|--------|------|------|-----------|-------------|----------|
| 30 | [DWD Pollenflug](dwd-pollenflug.md) | Germany/Europe | ✅ JSON file | None | Daily | 16/18 | 🟢 HIGH |

## Recommended Implementation Order

1. **OpenAQ** — global aggregator; one API covers 130+ countries. Start here.
2. **Luchtmeetnet (NL)** — cleanest national API in Europe: REST, no auth, paginated JSON. Model connector.
3. **UBA Germany** — clean REST API, no auth, well-structured.
4. **IRCELINE (Belgium)** — same 52°North SOS platform as Defra AURN. Reuse client code.
5. **Defra AURN** — standard SOS API, no auth.
6. **LAQN London** — best urban-scale air quality API; DAQI with per-species breakdown.
7. **US EPA AirNow** — authoritative US source with forecasts not in OpenAQ.
8. **Singapore NEA** — trivially simple JSON API; no auth; haze monitoring.
9. **Taiwan MOENV** — clean JSON with coordinates embedded; API key required.
10. **Sensor.Community** — real-time citizen science; no auth; unique granularity.
11. **GIOŚ Poland** — JSON-LD with Polish field names; includes AQI sub-indices.
12. **Canada AQHI** — file-based but includes health-focused AQHI forecasts.
13. **DWD Pollenflug** — single JSON file; unique pollen data type.
14. **Copernicus CAMS** — global gridded forecasts; fills gaps where no stations exist.
15. **PurpleAir** — delta queries via `modified_since`; needs API key + non-commercial license.
16. **AQICN/WAQI** — pre-calculated AQI and forecasts; restrictive license.
17. **South Korea AirKorea** / **NSW EPA** / **EEA** / **Hong Kong EPD** / **NILU Norway** / **FMI Finland** — regional supplements as needed.

## Key Observations

- **OpenAQ is the meta-aggregator**: It already ingests data from AirNow, EEA, CPCB, several Australian EPAs, PurpleAir, and many others. Implementing OpenAQ first gives the broadest coverage with the least effort.
- **European APIs are excellent**: Luchtmeetnet, IRCELINE, UBA, Defra, GIOŚ, and FMI all provide well-structured open APIs. Europe leads in open air quality data.
- **The 52°North SOS pattern repeats**: IRCELINE (Belgium) and Defra AURN (UK) use the identical 52°North SOS Timeseries API — one client covers both.
- **Citizen science fills gaps**: Sensor.Community and PurpleAir provide hyper-local, near-real-time data in areas where government monitors are sparse.
- **License matters**: OpenAQ (CC BY 4.0), Defra (OGL), UBA (dl-de), Luchtmeetnet (CC0), and AirNow (US Public Domain) are the most permissive. PurpleAir and AQICN restrict commercial use.
- **Asia-Pacific has strong APIs**: Singapore, Taiwan, Hong Kong, and South Korea all provide structured data. Japan and India remain web-only.
- **Latin America lags in APIs**: Mexico (SINAICA) and Chile (SINCA) lack documented public APIs. Use OpenAQ as intermediary.
- **Forecasts are rare but growing**: AirNow, AQICN, CAMS, and Canada AQHI provide forecasts. DWD Pollenflug provides pollen forecasts.
- **Satellite data is complementary**: CAMS and Sentinel-5P provide global coverage but require scientific data formats (GRIB, NetCDF). Not simple JSON.
- **Pollen is a unique niche**: DWD Pollenflug is the only open JSON pollen forecast API found. CAMS also provides modelled pollen for Europe.
- **Greenhouse gas monitoring** (NOAA GML) is reference-grade but monthly — a different use case from urban air quality.
