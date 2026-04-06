# Hydrology and Water Monitoring — Candidate Sources

## Already Implemented

| Source | Country | Directory |
|--------|---------|-----------|
| PegelOnline | Germany | `pegelonline/` |
| RWS Waterwebservices | Netherlands | `rws-waterwebservices/` |
| Hub'Eau Hydrometrie | France | `hubeau-hydrometrie/` |
| BAFU Hydro via existenz.ch | Switzerland | `bafu-hydro/` |
| CHMI Hydro | Czech Republic | `chmi-hydro/` |
| IMGW Hydro | Poland | `imgw-hydro/` |
| NVE Hydro | Norway | `nve-hydro/` |
| SMHI Hydro | Sweden | `smhi-hydro/` |
| SYKE Hydro | Finland | `syke-hydro/` |
| EA Flood Monitoring | UK (England) | `uk-ea-flood-monitoring/` |
| USGS Instantaneous Values | USA | `usgs-iv/` |
| VMM Waterinfo | Belgium | `waterinfo-vmm/` |
| WSV (German Waters) | Germany | `german-waters/` |

## Considered but Dismissed

| Source | Country | Reason |
|--------|---------|--------|
| Austria eHYD | Austria | SPA-only portal; no public REST API. GeoSphere Austria has excellent met data API but no hydrology. See [austria-geosphere.md](austria-geosphere.md) |
| Spain SAIH (various confederaciones) | Spain | Re-investigated: 9 basin portals probed. Tajo has modern SPA, Duero shows reservoir data, but no public API on any. See [spain-saih.md](spain-saih.md) |
| Portugal SNIRH | Portugal | Returns 403 Forbidden; no public API access |
| India CWC / India-WRIS | India | CWC returns 401; India-WRIS times out. 5000+ stations locked behind auth. See [india-cwc-wris.md](india-cwc-wris.md) |
| South Africa DWS | South Africa | Returns 403 Forbidden; no public API access |
| Japan MLIT river.go.jp | Japan | Re-investigated: web-only interface; no structured API found. data.go.jp portal also HTML-only |
| South Korea WAMIS/K-water | South Korea | Re-investigated: Ajax endpoints found on water.or.kr but inconsistent. See [south-korea-kwater.md](south-korea-kwater.md) |
| Denmark DMI/SDFI | Denmark | DMI met obs API works (OGC API Features, GeoJSON) but no hydrology-specific parameters. See [denmark-dmi-metobs.md](denmark-dmi-metobs.md) |
| Latvia LVĢMC | Latvia | data.gov.lv returned 0 results for water level; SPA portal without public API |
| Croatia HVZ | Croatia | Static file server; no structured API; endpoints unreachable |
| Serbia Srbijavode | Serbia | Endpoints unreachable |
| Iceland IMO/Veðurstofa | Iceland | vedur.is has hydrology section (vatnamal) but no API; opendata.vedur.is unreachable; apis.is/hydro unreachable |
| Romania INHGA | Romania | Redirects to WordPress site (hidro.ro); WP REST API has CMS content only, no hydrology data. See [romania-inhga.md](romania-inhga.md) |
| Bulgaria NIMH | Bulgaria | hydro.bg and meteo.bg are web-only portals; no structured API found |
| Greece YPEKA | Greece | floods.ypeka.gr is WordPress portal; no real-time hydrology API found |
| Estonia Keskkonnaamet | Estonia | ilmateenistus.ee has weather observations but no hydrology API; keskkonnaportaal.ee returns 401 |
| Mexico CONAGUA | Mexico | All endpoints behind Cloudflare WAF challenge. See [mexico-conagua.md](mexico-conagua.md) |
| Chile DGA/SNIA | Chile | Returns 403 Forbidden on data endpoints. See [chile-dga.md](chile-dga.md) |
| Colombia IDEAM | Colombia | fews.ideam.gov.co times out; no public API found |
| Peru SENAMHI | Peru | Various endpoints return 404 or time out; no public API |
| Argentina INA | Argentina | File server with directory listings; hydro products but no REST API. See [argentina-ina.md](argentina-ina.md) |

## New Candidates — Round 1 (Previously Researched)

| Source | Country | Score | Status | File |
|--------|---------|-------|--------|------|
| ECCC Water Survey / MSC GeoMet | Canada | 18/18 | Research complete | [canada-eccc-wateroffice.md](canada-eccc-wateroffice.md) |
| BOM Water Data Online | Australia | 16/18 | Research complete | [australia-bom-waterdata.md](australia-bom-waterdata.md) |
| OPW waterlevel.ie | Ireland | 18/18 | Research complete | [ireland-opw-waterlevel.md](ireland-opw-waterlevel.md) |
| ARSO Hidro | Slovenia | 17/18 | Research complete | [slovenia-arso-hidro.md](slovenia-arso-hidro.md) |
| SEPA Water Levels | Scotland | 16/18 | Research complete | [scotland-sepa-waterlevels.md](scotland-sepa-waterlevels.md) |
| Hilltop (Regional Councils) | New Zealand | 15/18 | Research complete | [newzealand-hilltop.md](newzealand-hilltop.md) |
| ANA Telemetria | Brazil | 15/18 | Research complete | [brazil-ana-telemetria.md](brazil-ana-telemetria.md) |

## New Candidates — Round 2 (Deep Dive)

### Europe

| Source | Country | Score | Status | File |
|--------|---------|-------|--------|------|
| LHMT Hydro API | Lithuania | 15/18 | Research complete | [lithuania-lhmt-hydro.md](lithuania-lhmt-hydro.md) |
| OVF vizugy.hu | Hungary | 10/18 | Research complete | [hungary-ovf-vizugy.md](hungary-ovf-vizugy.md) |
| DMI Met Obs API | Denmark | 14/18 | Research complete | [denmark-dmi-metobs.md](denmark-dmi-metobs.md) |
| SAIH Confederaciones | Spain | 10/18 | Research complete | [spain-saih.md](spain-saih.md) |
| ARPA / ISPRA Hydro | Italy | 8/18 | Research complete | [italy-arpa-hydro.md](italy-arpa-hydro.md) |
| GeoSphere Austria | Austria | 15/18 | Research complete | [austria-geosphere.md](austria-geosphere.md) |
| SHMÚ Hydrology | Slovakia | 8/18 | Research complete | [slovakia-shmu.md](slovakia-shmu.md) |
| INHGA | Romania | 6/18 | Research complete | [romania-inhga.md](romania-inhga.md) |

### Asia-Pacific

| Source | Country | Score | Status | File |
|--------|---------|-------|--------|------|
| HAII Thaiwater | Thailand | 15/18 | Research complete | [thailand-thaiwater.md](thailand-thaiwater.md) |
| WRA Flood Hydrology | Taiwan | 14/18 | Research complete | [taiwan-wra.md](taiwan-wra.md) |
| K-water / WAMIS | South Korea | 11/18 | Research complete | [south-korea-kwater.md](south-korea-kwater.md) |
| CWC / India-WRIS | India | 9/18 | Research complete | [india-cwc-wris.md](india-cwc-wris.md) |

### Americas

| Source | Country | Score | Status | File |
|--------|---------|-------|--------|------|
| INA Alert System | Argentina | 10/18 | Research complete | [argentina-ina.md](argentina-ina.md) |
| CONAGUA | Mexico | 8/18 | Research complete | [mexico-conagua.md](mexico-conagua.md) |
| DGA / SNIA | Chile | 6/18 | Research complete | [chile-dga.md](chile-dga.md) |

### Global Aggregators

| Source | Scope | Score | Status | File |
|--------|-------|-------|--------|------|
| Copernicus GloFAS | Global | 15/18 | Research complete | [copernicus-glofas.md](copernicus-glofas.md) |
| Copernicus CDS / EFAS | Europe + Global | 15/18 | Research complete | [copernicus-cds-efas.md](copernicus-cds-efas.md) |
| WMO WHOS | Multi-basin | 10/18 | Research complete | [wmo-whos.md](wmo-whos.md) |
| GRDC | Global (historical) | 9/18 | Research complete | [grdc-global.md](grdc-global.md) |
| Mekong River Commission | Mekong basin | 9/18 | Research complete | [mekong-river-commission.md](mekong-river-commission.md) |
| Google Flood Hub | Global | 10/18 | Research complete | [google-flood-hub.md](google-flood-hub.md) |

### Africa

| Source | Country | Score | Status | File |
|--------|---------|-------|--------|------|
| South Africa DWS Rivers | South Africa | 9/18 | Research complete | [south-africa-dws-rivers.md](south-africa-dws-rivers.md) |
| GloFAS Africa Flood Forecast | Pan-African | 13/18 | Research complete | [glofas-africa-flood-forecast.md](glofas-africa-flood-forecast.md) |
| Nile Basin Water Monitoring | East/North Africa (11 countries) | 11/18 | Research complete | [nile-basin-water-monitoring.md](nile-basin-water-monitoring.md) |

## Summary

### Deep Dive Results

This deep dive investigated **40+ sources** across three rounds, producing **17 new research documents** on top of the 7 previously documented candidates. Confirmed working APIs with verified endpoints:

#### Tier 1 — Excellent APIs (15+/18, production-ready)

1. **Lithuania LHMT** (15/18) — Clean REST/JSON API at `api.meteo.lt/v1/hydro-stations`. No auth, hourly water level + temperature for ~70 stations. Same API pattern as the well-known meteo.lt weather API. Verified with live observations.

2. **Thailand HAII Thaiwater** (15/18) — Rich JSON API at `api-v3.thaiwater.net`. No auth. Water levels, discharge, dam storage, flood severity across 1000+ stations and 35+ dams. Bilingual (Thai/English). Best open hydro API in Southeast Asia.

3. **Taiwan WRA** (14/18) — OData-style REST API at `fhy.wra.gov.tw/WraApi/v1/`. No auth. Water level stations with warning thresholds, reservoir daily data, rain stations. Station metadata confirmed; real-time timeseries endpoint not yet located.

4. **Copernicus GloFAS** (15/18) — Global river discharge forecasts via CDS API. STAC catalogue browsable without auth; data download requires free CDS account. GRIB/NetCDF format. Model-derived, not in-situ gauges.

5. **Copernicus CDS/EFAS** (15/18) — European flood awareness forecasts. Higher resolution than GloFAS for Europe. Same CDS infrastructure.

#### Tier 2 — Partial Access or Auxiliary (10-14/18)

6. **Denmark DMI** (14/18) — Excellent OGC API for meteorological observations but lacks hydrology-specific parameters. Free API key required.

7. **GeoSphere Austria** (15/18) — Outstanding API architecture at `dataset.api.hub.geosphere.at` with 96 datasets. But meteorological only — Austria's actual hydrology data (eHYD) has no API.

8. **Hungary OVF** (10/18) — 500+ stations visible on vizugy.hu. Data rendered in HTML tables with 15-minute updates. Newer API at data.vizugy.hu requires auth tokens.

9. **South Korea K-water** (11/18) — Ajax endpoints exist but inconsistent from outside Korea. 1500+ stations nationwide.

10. **Spain SAIH** (10/18) — 3000+ stations across 9 basins. All behind web-only portals. Tajo has modern SPA; no public API on any basin.

11. **WMO WHOS** (10/18) — OpenSearch XML descriptor works; actual data queries unverified. Federated access to national services.

12. **Argentina INA** (10/18) — File server approach with directory listings. Hydro data products exist but not as REST API.

13. **Google Flood Hub** (10/18) — AI-powered forecasts for 80+ countries but completely closed for programmatic access.

#### Tier 3 — Dismissed with Documentation (< 10/18)

Sources investigated in depth but lacking public API: Italy (8), Slovakia (8), Mexico (8), India (9), GRDC (9), MRC Mekong (9), Romania (6), Chile (6).

### Integration Recommendations

**Immediate implementation candidates** (from this deep dive):
- **Lithuania LHMT** — minimal effort, clean API, fills Baltic gap
- **Thailand Thaiwater** — rich data, covers major ASEAN country
- **Taiwan WRA** — good station/reservoir data, OData patterns

**High-value but requires CDS account**:
- **Copernicus GloFAS/EFAS** — global/European coverage, model-derived forecasts

**Watch list** (may improve):
- Hungary (data.vizugy.hu API appears to be developing)
- Spain (EU INSPIRE mandate may force API publication)
- India (CWC's 401 response suggests API exists behind auth)

### Geographic Coverage After Deep Dive

| Region | Implemented | New Candidates | Dismissed |
|--------|------------|---------------|-----------|
| Northern Europe | NO, SE, FI, DK* | LT | EE, LV, IS |
| Western Europe | DE, NL, FR, BE, UK, CH | IE, AT* | PT |
| Central Europe | CZ, PL | SI, HU, SK | HR, RS |
| Southern Europe | — | — | ES, IT, GR, RO, BG |
| North America | US | CA | MX |
| South America | — | BR, AR* | CL, CO, PE |
| Asia-Pacific | — | AU, NZ, TH, TW | JP, KR*, IN, CN |
| Global | — | GloFAS, EFAS, WHOS, GRDC | Flood Hub, MRC |

\* = partial access or meteorological only

### Protocol Patterns

- **REST/JSON (no auth)**: Lithuania, Thailand, Taiwan, Ireland, Canada, Slovenia, Nepal (BIPAD)
- **Kisters WISKI**: Australia, Scotland (shared adapter possible)
- **OGC API Features**: Canada (gold standard), Denmark (met only)
- **STAC/CDS**: GloFAS, EFAS (batch processing, auth required)
- **OpenSearch XML**: WMO WHOS
- **SOAP/XML**: Brazil, New Zealand
- **HTML scraping only**: Hungary, Spain, Italy, most dismissed sources

### Deep Dive Round 3 — South Asia, SE Asia, Middle East

| Source | Country | Score | Status | File |
|--------|---------|-------|--------|------|
| Nepal BIPAD Hydrology | Nepal | 16/18 | ✅ CONFIRMED WORKING | [nepal-bipad-hydrology.md](nepal-bipad-hydrology.md) |
| Nepal DHM / BIPAD | Nepal | 16/18 | Research complete | [nepal-dhm-hydrology.md](nepal-dhm-hydrology.md) |
| MRC Mekong (re-probe) | Mekong Basin | 11/18 | SPA still blocks API | [mekong-river-commission-update.md](mekong-river-commission-update.md) |
| ICIMOD HKH Mountains | Hindu Kush-Himalaya | 10/18 | Research data, no real-time API | [icimod-hkh-mountains.md](icimod-hkh-mountains.md) |
| Turkey DSI Transboundary | Turkey | 9/18 | Euphrates-Tigris context | [turkey-dsi-transboundary.md](turkey-dsi-transboundary.md) |
| Cambodia/Laos Mekong Gap | Cambodia/Laos | 3/18 | Gap documentation | [cambodia-laos-mekong-gap.md](cambodia-laos-mekong-gap.md) |

**Key finding**: Nepal's BIPAD portal is a breakthrough — a working Django REST API with real-time river water levels in GeoJSON format, no auth required. This is the first confirmed public hydrology API in South Asia.


## Latin America Expansion  April 2026

| Source | Country | Score | File | Status |
|--------|---------|-------|------|--------|
| **Colombia IDEAM Hydro** | Colombia | **15/18** | [colombia-ideam-hydro.md](colombia-ideam-hydro.md) |  **Build**  Socrata API on datos.gov.co; near-real-time precipitation; 5 major basins |
| **Colombia IDEAM Inventory** | Colombia | 15/18 | [colombia-ideam-inventory.md](colombia-ideam-inventory.md) |  Multi-dataset survey (precip + pressure + temp) |
| **Brazil ANA SNIRH** | Brazil | **12/18** | [brazil-ana-snirh-expanded.md](brazil-ana-snirh-expanded.md) |  **Maybe**  REST endpoint pattern found but not returning data; complements existing ANA candidate |

### Key Finding: Colombia IDEAM via Socrata

The datos.gov.co Socrata API is the breakthrough for Colombia. Three IDEAM datasets (precipitation, atmospheric pressure, temperature) with near-real-time data confirmed (2026-04-05 23:59). Standard SoQL queries, no authentication, well-documented Socrata platform. A single Socrata adapter handles all three datasets with different resource IDs. Colombia's hydrographic zones span Amazon, Orinoco, Magdalena-Cauca, and the wettest place on Earth (Chocó/Pacific coast).