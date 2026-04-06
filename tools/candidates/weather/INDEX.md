# Weather & Atmospheric Data — Candidate Sources

Research conducted: April 2026 (Deep Dive Round 2: April 2026)

## Already Integrated in Repository

| Source | Directory | Country | Protocol |
|--------|-----------|---------|----------|
| DWD (Deutscher Wetterdienst) | `dwd/` | Germany | File-server polling |
| NOAA NWS | `noaa-nws/` | USA | GeoJSON REST |
| NOAA NDBC | `noaa-ndbc/` | USA | Buoy text data |
| NOAA GOES/SWPC | `noaa-goes/` | USA | Space weather JSON |

## New Candidates Researched

### Original Research (Round 1)

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

### Deep Dive Round 1 — European & Developed-World Met Services

| # | Source | File | Country | Score | Protocol | Auth | Highlights |
|---|--------|------|---------|-------|----------|------|------------|
| 16 | [Met Éireann](met-eireann.md) | `met-eireann.md` | Ireland | 14/18 | Static JSON files | **None** | No-auth JSON forecasts, per-county warnings, marine |
| 17 | [KMA API Hub](kma-south-korea.md) | `kma-south-korea.md` | South Korea | 14/18 | REST API | API Key (Korean portal) | 13 data categories, Chollian-2A satellite, typhoon |
| 18 | [IMGW-PIB Poland](imgw-poland.md) | `imgw-poland.md` | Poland | 14/18 | REST (JSON) | **None** | No-auth synoptic JSON, fills Central/Eastern Europe gap |
| 19 | [Veðurstofa Íslands](vedurstofa-iceland.md) | `vedurstofa-iceland.md` | Iceland | 11/18 | Legacy XML (broken) | Unknown | Volcanic monitoring, API in transition |
| 20 | [IMD India](imd-india.md) | `imd-india.md` | India | 11/18 | Web portal + files | Registration | 1.4B people served, monsoon, RSMC for Indian Ocean cyclones |

### Deep Dive Round 2 — Developing World & Tropics

| # | Source | File | Country | Score | Protocol | Auth | Highlights |
|---|--------|------|---------|-------|----------|------|------------|
| 21 | [HKO Hong Kong](hko-hong-kong.md) | `hko-hong-kong.md` | Hong Kong | 17/18 | REST (JSON) | **None** | Best Asian API, typhoon tracking, 10-min regional data |
| 22 | [Singapore NEA](singapore-nea.md) | `singapore-nea.md` | Singapore | 17/18 | REST (JSON) | **None** | 1-minute temperature updates, 50+ rain gauges, no auth |
| 23 | [CWA Taiwan](cwa-taiwan.md) | `cwa-taiwan.md` | Taiwan | 17/18 | REST (Swagger) | API Key (free) | 700+ stations, typhoon, earthquake, OpenAPI docs |
| 24 | [BMKG Indonesia](bmkg-indonesia.md) | `bmkg-indonesia.md` | Indonesia | 16/18 | REST (JSON) | **None** | Village-level forecasts, 17,000 islands, bilingual |
| 25 | [Argentina SMN](smn-argentina.md) | `smn-argentina.md` | Argentina | 15/18 | REST (JSON) | **None** | Antarctic bases, Patagonia, 53° latitude span |
| 26 | [Brazil INMET](inmet-brazil.md) | `inmet-brazil.md` | Brazil | 12/18 | REST (JSON) | API Token | 600+ stations, Amazon/tropical, API unstable |

### Deep Dive Round 3 — Specialized Weather Data Sources

| # | Source | File | Country | Score | Protocol | Auth | Highlights |
|---|--------|------|---------|-------|----------|------|------------|
| 27 | [Iowa Environmental Mesonet](iem-mesonet.md) | `iem-mesonet.md` | USA | 17/18 | REST (OpenAPI 3.1) | **None** | ASOS/METAR aggregator, storm reports, VTEC events, open source |
| 28 | [Synoptic Data](synoptic-data.md) | `synoptic-data.md` | Global | 16/18 | REST API | API Key (commercial) | 170,000+ stations, 320 networks, multi-level QC |
| 29 | [Copernicus CDS](copernicus-cds.md) | `copernicus-cds.md` | Global | 14/18 | REST + Python client | Token (free) | ERA5 reanalysis, climate monitoring, GRIB/NetCDF |
| 30 | [EUMETSAT](eumetsat.md) | `eumetsat.md` | Global | 14/18 | HTTPS + OGC | Registration (free) | Meteosat 5-min rapid scan, Metop, volcanic ash |
| 31 | [OGIMET](ogimet.md) | `ogimet.md` | Global | 13/18 | CGI (plain text) | **None** | Global SYNOP/METAR from WMO GTS, any station worldwide |
| 32 | [Netatmo Weather](netatmo.md) | `netatmo.md` | Global | 12/18 | REST API | OAuth 2.0 | Citizen stations, urban density, 5-min updates |

## Ranking by Feasibility Score

1. **18/18** — Environment Canada (MSC Datamart + GeoMet) — AMQP push, OGC, no auth
2. **17/18** — SMHI Weather, JMA, BOM Australia, DMI Denmark, GeoSphere Austria, FMI Finland, **HKO Hong Kong**, **Singapore NEA**, **CWA Taiwan**, **IEM Mesonet**
3. **16/18** — UK Met Office, Météo-France, ECMWF Open Data, AEMET Spain, **BMKG Indonesia**, **Synoptic Data**
4. **15/18** — KNMI, Open-Meteo, **Argentina SMN**
5. **14/18** — IPMA Portugal, MeteoSwiss, **Met Éireann**, **KMA South Korea**, **IMGW Poland**, **Copernicus CDS**, **EUMETSAT**
6. **13/18** — **OGIMET**
7. **12/18** — **Brazil INMET**, **Netatmo**
8. **11/18** — **Veðurstofa Íslands**, **IMD India**

## Top Recommendations for Integration

### Tier 1 — Highest Priority
- **Environment Canada**: Perfect score. AMQP push notifications, high-res model, OGC standards, no auth. Best-in-class open data infrastructure.
- **BOM Australia**: Clean JSON, no auth, Southern Hemisphere coverage. Easiest to integrate among high-scoring candidates.
- **SMHI Weather**: No auth, clean JSON REST, excellent developer experience. Natural extension of existing `smhi-hydro` integration.
- **HKO Hong Kong** *(new)*: Zero-auth JSON, 10-minute regional data, typhoon tracking. One of the easiest APIs to integrate in Asia.
- **Singapore NEA** *(new)*: 1-minute temperature updates from 50+ stations, no auth. Reference-quality tropical urban monitoring.

### Tier 2 — High Value
- **JMA**: No auth, 1,300-station network, minute-level feed. Japan coverage with earthquake/volcano bonus. XML parsing required.
- **DMI Denmark**: OGC API standard, GeoJSON. Unique Greenland/Arctic coverage.
- **GeoSphere Austria**: No auth, 96 datasets, INCA nowcasting. Alpine specialization.
- **FMI Finland**: No auth, WFS 2.0, multi-source (road weather, radiation). Pioneer in met open data.
- **CWA Taiwan** *(new)*: Swagger-documented, 700+ stations, typhoon/earthquake. Free API key.
- **IEM Mesonet** *(new)*: OpenAPI 3.1, no auth, ASOS/METAR aggregation, storm reports. Open source. Complements NOAA NWS.

### Tier 3 — Valuable with API Key
- **UK Met Office**: High-res UK model (2km), GeoJSON spot data. API key required.
- **Météo-France**: AROME 1.3km model (highest-res freely available). API in migration.
- **ECMWF Open Data**: The world's best global NWP model. GRIB2 format adds complexity.
- **AEMET Spain**: OpenAPI 3.0 spec, lightning/fire data. Two-step retrieval pattern.
- **BMKG Indonesia** *(new)*: Village-level forecasts for 17,000 islands, no auth. Enormous geographic coverage.
- **Synoptic Data** *(new)*: 170,000+ stations worldwide, push streaming. Commercial — free tier for evaluation.

### Tier 4 — Worth Monitoring
- **KNMI**: Good data but file-based (NetCDF) pattern adds processing overhead.
- **Open-Meteo**: Aggregator — better for reference than as primary source.
- **IPMA Portugal**: Minimal but functional. Small coverage area.
- **MeteoSwiss**: New OGD mandate, infrastructure still maturing.
- **Met Éireann** *(new)*: Simple JSON files, good for warning monitoring. Ireland/Atlantic coverage.
- **IMGW Poland** *(new)*: No-auth JSON synoptic data. Fills Central/Eastern European gap.
- **Argentina SMN** *(new)*: No-auth JSON, Antarctic bases. Unique Southern Hemisphere coverage.
- **Copernicus CDS** *(new)*: ERA5 reanalysis — gold standard for climate data. Not real-time but irreplaceable for historical analysis.
- **EUMETSAT** *(new)*: Meteosat imagery, volcanic ash tracking. Complex satellite data formats.

### Tier 5 — Specialized / Limited Access
- **OGIMET** *(new)*: Global SYNOP data from any WMO station. Fragile infrastructure but irreplaceable for some regions.
- **Netatmo** *(new)*: Unprecedented urban station density. OAuth 2.0 auth, consumer-grade data quality.
- **Brazil INMET** *(new)*: 600+ stations, Amazon coverage. API infrastructure unstable — revisit periodically.
- **KMA South Korea** *(new)*: 13 data categories, own satellite. Korean-language barrier, registration may require Korean phone.
- **IMD India** *(new)*: 1.4 billion people, monsoon monitoring, cyclone RSMC. No modern API — significant access barriers.
- **Veðurstofa Íslands** *(new)*: Volcanic monitoring. Legacy API deprecated — watch for reconstruction.

## Sources Considered but Not Researched in Detail

| Source | Country | Reason |
|--------|---------|--------|
| CMA (China Meteorological Administration) | China | Data access restricted; no clear open API for international users |
| MetService New Zealand | New Zealand | Limited open data API; mainly commercial |
| CHMI (Czech Hydrometeorological Institute) | Czechia | Weather side not as accessible as hydro (already in repo as `chmi-hydro`) |
| Roshydromet (Russia) | Russia | Data access restricted; limited international availability |
| DHMZ (Croatia) | Croatia | Web-only data; no public API identified |
| ARSO (Slovenia) | Slovenia | Some open data but limited English documentation |
| OMSZ (Hungary) | Hungary | Limited public API availability |
| SHMÚ (Slovakia) | Slovakia | Web portal only, no REST API |
| Meteo.cat (Catalonia) | Spain (regional) | Regional service, data may overlap with AEMET |
| ARPAV / MeteoAM (Italy regional) | Italy | Fragmented regional services, no unified API |
| PAGASA (Philippines) | Philippines | Limited digital infrastructure for data access |
| TMD (Thailand) | Thailand | Web-only forecasts, no public API |
| MetMalaysia | Malaysia | Limited open data API |
| Vietnam Met Service | Vietnam | No public API identified |
| Pakistan Met Department | Pakistan | Very limited digital data access |
| Saudi Arabia PME / UAE NCMS | Saudi Arabia / UAE | Restricted or commercial data access |
| Morocco / Tunisia / Egypt met services | North Africa | Limited open data infrastructure |
| SAWS (South Africa) | South Africa | Some open data but limited API access |
| NiMet (Nigeria) | Nigeria | Very limited digital infrastructure |
| Mexico SMN (CONAGUA) | Mexico | Web-based, no REST API confirmed |
| Chile DMC | Chile | Limited public API |
| Weather Underground API | Global | Deprecated / absorbed into IBM Weather |
| Weathercloud API | Global | Limited scope, citizen stations |
| Windy API | Global | Primarily visualization; limited data API |
| EUMETNET OPERA | Europe | Radar composites available through member NMHSs |

## Geographic Coverage Map

```
Americas:      Environment Canada (18), Argentina SMN (15), Brazil INMET (12),
               [NOAA NWS, NDBC — already integrated]
Europe North:  SMHI (17), FMI (17), DMI (17), Veðurstofa Iceland (11)
Europe West:   UK Met Office (16), Météo-France (16), KNMI (15), Met Éireann (14)
Europe Central: GeoSphere Austria (17), MeteoSwiss (14), IMGW Poland (14),
               [DWD — already integrated]
Europe South:  AEMET Spain (16), IPMA Portugal (14)
Asia East:     JMA Japan (17), HKO Hong Kong (17), CWA Taiwan (17), KMA S.Korea (14)
Asia Southeast: Singapore NEA (17), BMKG Indonesia (16)
Asia South:    IMD India (11)
Oceania:       BOM Australia (17)
Global:        ECMWF (16), Synoptic Data (16), Open-Meteo (15), Copernicus CDS (14),
               EUMETSAT (14), OGIMET (13), Netatmo (12),
               IEM Mesonet (17, US-focused)
```
