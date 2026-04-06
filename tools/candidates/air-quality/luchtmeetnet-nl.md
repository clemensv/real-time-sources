# Luchtmeetnet (Netherlands National Air Quality Monitoring)

**Country/Region**: Netherlands
**Publisher**: RIVM (Rijksinstituut voor Volksgezondheid en Milieu) / Luchtmeetnet consortium
**API Endpoint**: `https://api.luchtmeetnet.nl/open_api/`
**Documentation**: https://api-docs.luchtmeetnet.nl/
**Protocol**: REST
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Hourly
**License**: Open data (Dutch government, CC0 / Public Domain)

## What It Provides

Luchtmeetnet is the Netherlands' national air quality monitoring network, operated by a consortium led by RIVM (the Dutch National Institute for Public Health and the Environment). It aggregates measurements from ~80 stations operated by RIVM, GGD Amsterdam, DCMR (Rotterdam-Rijnmond), and provincial authorities. Measured pollutants include PM10, PM2.5, NO₂, O₃, SO₂, CO, benzene, and others. The open API provides both real-time hourly data and historical measurements.

## API Details

- **Base URL**: `https://api.luchtmeetnet.nl/open_api/`
- **Key Endpoints**:
  - `GET /stations` — paginated list of all stations (number, location name)
  - `GET /stations/{number}` — station detail (type, components, geometry, municipality, organisation)
  - `GET /measurements` — measurement data filtered by station_number, formula (component), page
  - `GET /components` — list of measured components
  - `GET /lki` — Dutch Air Quality Index (Luchtkwaliteitsindex) values
- **Query Parameters**: `station_number`, `formula` (e.g., NO2, PM25, O3), `page`, `order_by`, `start`, `end`
- **Pagination**: Response includes `pagination` object with `current_page`, `last_page`, `next_page`
- **Response Structure**: `{"pagination":{...},"data":[...]}`
- **Sample Station**: `{"number":"NL49572","location":"Velsen-Staalstraat","type":"Industrial","components":["PM25","PM10"],"geometry":{"type":"point","coordinates":[4.6288,52.4744]}}`

## Freshness Assessment

Hourly measurements are available with a typical delay of 1-2 hours. The API serves validated preliminary data. Station metadata includes the start year, operational status, and responsible organisation.

## Entity Model

- **Station** → number (e.g., `NL49572`), location name, type, municipality, province, organisation, geometry, components
- **Component** → formula code (NO2, PM10, PM25, O3, etc.), description
- **Measurement** → station × component × datetime → value (µg/m³)
- **LKI** → Dutch Air Quality Index per station

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Hourly data, responsive API |
| Openness | 3 | No auth, open government data (CC0) |
| Stability | 3 | Dutch government backed, well-maintained |
| Structure | 3 | Clean JSON, standard REST with pagination |
| Identifiers | 3 | Stable station numbers (NL-prefixed codes), formula codes |
| Additive Value | 2 | Netherlands-only; partially in EEA/OpenAQ |
| **Total** | **17/18** | |

## Notes

- One of the cleanest national air quality APIs in Europe — simple REST, no auth, paginated JSON, stable identifiers.
- Station numbers use the `NLnnnnn` format, enabling cross-referencing with EEA reporting codes.
- The `type` field classifies stations (Traffic, Industrial, Background, Regional) — useful for filtering.
- The `components` array on each station shows which pollutants are measured there, avoiding wasted API calls.
- Luchtmeetnet also provides an LKI (Dutch Air Quality Index), which is a value-add over raw measurements.
- Already partially available through OpenAQ and EEA, but the direct API gives richer metadata and the LKI index.
