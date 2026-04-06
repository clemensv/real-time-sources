This documents the Polish Chief Inspectorate of Environmental Protection (GIOŚ) air quality API. Verified API data:

- Base URL: `https://api.gios.gov.pl/pjp-api/v1/rest/`
- Confirmed working endpoints:
  - `GET /station/findAll` → returns all stations as JSON-LD: `{"Lista stacji pomiarowych":[{"Identyfikator stacji":11,"Kod stacji":"DsCzerStraza","Nazwa stacji":"Czerniawa","WGS84 φ N":"50.912475","WGS84 λ E":"15.312190","Identyfikator miasta":142,"Nazwa miasta":"Czerniawa","Gmina":"Świeradów-Zdrój","Powiat":"lubański","Województwo":"DOLNOŚLĄSKIE","Ulica":"ul. Strażacka 7"}, ...]}`
  - `GET /aqindex/getIndex/{stationId}` → returns AQ index: `{"AqIndex":{"Identyfikator stacji pomiarowej":52,"Wartość indeksu":1,"Nazwa kategorii indeksu":"Dobry","Wartość indeksu dla wskaźnika SO2":0,...,"Kod zanieczyszczenia krytycznego":"OZON"}}`
  - `GET /data/getData/{sensorId}` → returns hourly measurement data with timestamps and values
- Swagger docs at: `https://api.gios.gov.pl/pjp-api/swagger-ui/index.html`
- Auth: None required (rate-limited: 1500 req/min for real-time, 2 req/min for archival)
- Data Format: JSON-LD
- Update Frequency: Hourly

```
# GIOŚ (Polish Chief Inspectorate of Environmental Protection)

**Country/Region**: Poland
**Publisher**: Główny Inspektorat Ochrony Środowiska (GIOŚ)
**API Endpoint**: `https://api.gios.gov.pl/pjp-api/v1/rest/`
**Documentation**: https://api.gios.gov.pl/pjp-api/swagger-ui/index.html
**Protocol**: REST
**Auth**: None (rate-limited)
**Data Format**: JSON-LD
**Update Frequency**: Hourly
**License**: Public sector information reuse (Polish government)

## What It Provides

GIOŚ operates Poland's national air quality monitoring network (Państwowy Monitoring Środowiska). The API provides access to real-time and historical measurements from ~250+ stations across all 16 voivodeships (provinces). Pollutants include PM10, PM2.5, SO₂, NO₂, O₃, CO, and benzene. The API also serves the Polish Air Quality Index (Indeks Jakości Powietrza) per station. All measurements are in µg/m³.

## API Details

- **Base URL**: `https://api.gios.gov.pl/pjp-api/v1/rest/`
- **Key Endpoints**:
  - `GET /station/findAll` — all stations with metadata (id, code, name, lat/lon, city, commune, district, voivodeship, street)
  - `GET /station/sensors/{stationId}` — sensors (measurement points) at a given station
  - `GET /data/getData/{sensorId}` — hourly measurement data for a sensor (last 3 days from current hour)
  - `GET /aqindex/getIndex/{stationId}` — current Polish AQI + sub-indices per pollutant
- **Rate Limits**: Real-time data: 1500 req/min; archival/metadata: 2 req/min
- **Response Format**: JSON-LD with Polish-language field names and schema.org context
- **Sample AQI**: `{"Wartość indeksu":1,"Nazwa kategorii indeksu":"Dobry","Kod zanieczyszczenia krytycznego":"OZON"}`
- **AQI Categories**: Bardzo dobry (Very good, 0), Dobry (Good, 1), Umiarkowany (Moderate, 2), Dostateczny (Sufficient, 3), Zły (Bad, 4), Bardzo zły (Very bad, 5)

## Freshness Assessment

Hourly measurements are available from the current hour back to 3 days. The AQI index is recalculated every ~10 minutes. Data is preliminary (unverified) and may contain gaps due to equipment failures or transmission issues.

## Entity Model

- **Station** → id, code (e.g., `DsCzerStraza`), name, lat/lon, city, commune, district, voivodeship, street
- **Sensor** → id, station_id, parameter (pollutant name + code)
- **Measurement** → sensor × datetime → value (µg/m³)
- **AQI** → station → overall index + sub-indices per pollutant + critical pollutant code

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Hourly data, AQI recalculated every ~10 min |
| Openness | 3 | No auth required, generous rate limits |
| Stability | 2 | Government agency; Swagger docs; but v1 API replaced older REST (410'd) |
| Structure | 2 | JSON-LD but Polish-language field names; custom schema |
| Identifiers | 2 | Numeric station/sensor IDs + station codes; Polish city names |
| Additive Value | 2 | Poland-only; partially in EEA/OpenAQ |
| **Total** | **14/18** | |

## Notes

- Response fields are in Polish (e.g., `Wartość` = Value, `Nazwa stacji` = Station name, `Województwo` = Voivodeship). Client code needs a field-name mapping.
- The old REST API (without `/v1/`) returns HTTP 410 Gone — always use the v1 path.
- JSON-LD format includes `@context` references to schema.org — unusual for a government air quality API.
- Poland has significant PM2.5/PM10 issues (domestic coal heating), making this data particularly relevant for health applications.
- OpenAPI/Swagger documentation is available, which simplifies client generation.
- Archival data endpoints have a strict 2 req/min limit — plan for slow bulk fetches.
```
