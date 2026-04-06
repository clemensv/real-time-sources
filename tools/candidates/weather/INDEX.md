# Weather & Atmospheric Data — Candidate Sources

Research conducted: April 2026

## Already Integrated in Repository

| Source | Directory | Country | Protocol |
|--------|-----------|---------|----------|
| DWD (Deutscher Wetterdienst) | `dwd/` | Germany | File-server polling |
| NOAA NWS | `noaa-nws/` | USA | GeoJSON REST |
| NOAA NDBC | `noaa-ndbc/` | USA | Buoy text data |
| NOAA GOES/SWPC | `noaa-goes/` | USA | Space weather JSON |

## New Candidates Researched

| # | Source | File | Country | Score | Protocol | Auth | Highlights |
|---|--------|------|---------|-------|----------|------|------------|
| 1 | [UK Met Office DataHub](uk-met-office.md) | `uk-met-office.md` | UK | 16/18 | REST (GeoJSON/GRIB2) | API Key (free) | UK 2km model, hourly spot data |
| 2 | [Météo-France](meteo-france.md) | `meteo-france.md` | France | 16/18 | REST API | API Key (free) | AROME 1.3km model, radar |
| 3 | [SMHI Weather](smhi-weather.md) | `smhi-weather.md` | Sweden | 17/18 | REST (JSON) | **None** | ~700 stations, no-auth, clean JSON |
| 4 | [KNMI Data Platform](knmi.md) | `knmi.md` | Netherlands | 15/18 | REST (file-based) | API Key (anon avail) | 10-min obs, NetCDF files, notifications |
| 5 | [JMA](jma.md) | `jma.md` | Japan | 17/18 | Atom+XML PULL | **None** | 1,300 AMeDAS stations, minute-level feed |
| 6 | [BOM Australia](bom-australia.md) | `bom-australia.md` | Australia | 17/18 | HTTP JSON polling | **None** | 30-min obs JSON, 5-min radar, 10-min satellite |
| 7 | [ECMWF Open Data](ecmwf-open-data.md) | `ecmwf-open-data.md` | International | 16/18 | HTTPS + Python client | **None** | World's best global NWP model (IFS), multi-cloud |
| 8 | [Environment Canada](environment-canada.md) | `environment-canada.md` | Canada | 18/18 | HTTP + AMQP push + OGC | **None** | AMQP push, HRDPS 2.5km, CAP warnings |
| 9 | [IPMA Portugal](ipma-portugal.md) | `ipma-portugal.md` | Portugal | 14/18 | Static JSON files | **None** | Dead-simple JSON, Azores/Madeira |
| 10 | [AEMET Spain](aemet-spain.md) | `aemet-spain.md` | Spain | 16/18 | REST (OpenAPI 3.0) | API Key (free) | Lightning, fire risk, CAP warnings |
| 11 | [DMI Denmark](dmi-denmark.md) | `dmi-denmark.md` | Denmark | 17/18 | OGC API — Features | API Key (free) | Greenland coverage, GeoJSON, standards |
| 12 | [GeoSphere Austria](geosphere-austria.md) | `geosphere-austria.md` | Austria | 17/18 | REST API + HTTP | **None** | INCA nowcasting, AROME 2.5km, 96 datasets |
| 13 | [FMI Finland](fmi-finland.md) | `fmi-finland.md` | Finland | 17/18 | OGC WFS 2.0 | **None** | Pioneer in met open data, multi-source |
| 14 | [Open-Meteo](open-meteo.md) | `open-meteo.md` | Global | 15/18 | REST JSON | **None** | Aggregator, multi-model, simplest API |
| 15 | [MeteoSwiss](meteoswiss.md) | `meteoswiss.md` | Switzerland | 14/18 | HTTP file download | **None** | New OGD mandate (2024), Alpine coverage |

## Ranking by Feasibility Score

1. **18/18** — Environment Canada (MSC Datamart + GeoMet) — AMQP push, OGC, no auth
2. **17/18** — SMHI Weather, JMA, BOM Australia, DMI Denmark, GeoSphere Austria, FMI Finland
3. **16/18** — UK Met Office, Météo-France, ECMWF Open Data, AEMET Spain
4. **15/18** — KNMI, Open-Meteo
5. **14/18** — IPMA Portugal, MeteoSwiss

## Top Recommendations for Integration

### Tier 1 — Highest Priority
- **Environment Canada**: Perfect score. AMQP push notifications, high-res model, OGC standards, no auth. Best-in-class open data infrastructure.
- **BOM Australia**: Clean JSON, no auth, Southern Hemisphere coverage. Easiest to integrate among high-scoring candidates.
- **SMHI Weather**: No auth, clean JSON REST, excellent developer experience. Natural extension of existing `smhi-hydro` integration.

### Tier 2 — High Value
- **JMA**: No auth, 1,300-station network, minute-level feed. Japan coverage with earthquake/volcano bonus. XML parsing required.
- **DMI Denmark**: OGC API standard, GeoJSON. Unique Greenland/Arctic coverage.
- **GeoSphere Austria**: No auth, 96 datasets, INCA nowcasting. Alpine specialization.
- **FMI Finland**: No auth, WFS 2.0, multi-source (road weather, radiation). Pioneer in met open data.

### Tier 3 — Valuable with API Key
- **UK Met Office**: High-res UK model (2km), GeoJSON spot data. API key required.
- **Météo-France**: AROME 1.3km model (highest-res freely available). API in migration.
- **ECMWF Open Data**: The world's best global NWP model. GRIB2 format adds complexity.
- **AEMET Spain**: OpenAPI 3.0 spec, lightning/fire data. Two-step retrieval pattern.

### Tier 4 — Worth Monitoring
- **KNMI**: Good data but file-based (NetCDF) pattern adds processing overhead.
- **Open-Meteo**: Aggregator — better for reference than as primary source.
- **IPMA Portugal**: Minimal but functional. Small coverage area.
- **MeteoSwiss**: New OGD mandate, infrastructure still maturing.

## Sources Considered but Not Researched in Detail

| Source | Country | Reason |
|--------|---------|--------|
| KMA (Korea Meteorological Administration) | South Korea | API portal in Korean, registration requires Korean phone number |
| IMD (India Meteorological Department) | India | Data primarily available through IITM data portal; complex access procedures |
| CMA (China Meteorological Administration) | China | Data access restricted; no clear open API for international users |
| MetService New Zealand | New Zealand | Limited open data API; mainly commercial |
| CHMI (Czech Hydrometeorological Institute) | Czechia | Weather side not as accessible as hydro (already in repo as `chmi-hydro`) |

## Geographic Coverage Map

```
Americas:      Environment Canada (18), [NOAA NWS, NDBC — already integrated]
Europe North:  SMHI (17), FMI (17), DMI (17)
Europe West:   UK Met Office (16), Météo-France (16), KNMI (15)
Europe Central: GeoSphere Austria (17), MeteoSwiss (14), [DWD — already integrated]
Europe South:  AEMET Spain (16), IPMA Portugal (14)
Asia:          JMA Japan (17)
Oceania:       BOM Australia (17)
Global:        ECMWF (16), Open-Meteo (15)
```
