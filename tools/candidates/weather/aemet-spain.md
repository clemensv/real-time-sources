# AEMET OpenData — Spain

**Country/Region**: Spain (including Canary Islands, Ceuta, Melilla)
**Publisher**: AEMET (Agencia Estatal de Meteorología)
**API Endpoint**: `https://opendata.aemet.es/opendata/api/`
**Documentation**: https://opendata.aemet.es/dist/index.html (Swagger UI), OpenAPI spec at https://opendata.aemet.es/AEMET_OpenData_specification.json
**Protocol**: REST API (OpenAPI 3.0)
**Auth**: API Key (free registration required)
**Data Format**: JSON (via two-step retrieval: metadata → data URL → actual data)
**Update Frequency**: Hourly (observations), daily (forecasts), real-time (warnings)
**License**: Reutilización de información del sector público (Spanish open data reuse law)

## What It Provides

AEMET OpenData is a well-documented REST API covering Spanish meteorological data:

- **Conventional observations** (`observacion-convencional`): Real-time and recent observations from AEMET's station network across Spain.

- **Specific forecasts** (`predicciones-especificas`): Location-specific weather forecasts.

- **Normalized text forecasts** (`predicciones-normalizadas-texto`): Standard format forecast texts.

- **Maritime forecasts** (`prediccion-maritima`): Coastal and open sea forecasts.

- **Weather warnings** (`avisos_cap`): Severe weather alerts in CAP format, by autonomous community (region). Latest warnings and historical archive (since June 2018).

- **Climatological values** (`valores-climatologicos`): Climate normals, historical data.

- **Radar network** (`red-radares`): Precipitation radar data.

- **Lightning network** (`red-rayos`): Lightning detection data.

- **Satellite information** (`informacion-satelite`): Satellite imagery metadata.

- **Fire risk indices** (`indices-incendios`): Forest fire meteorological risk maps.

- **Special networks** (`redes-especiales`): Additional monitoring networks.

- **Antarctic data** (`antartida`): Spanish Antarctic station observations.

## API Details

The API uses a **two-step retrieval pattern**:
1. Call an endpoint (e.g., `/api/avisos_cap/ultimoelaborado/area/esp`) with your API key.
2. Receive a JSON response containing a `datos` URL (temporary link to the actual data).
3. Fetch the `datos` URL to get the actual data payload.

This indirection allows AEMET to generate temporary download URLs for larger datasets.

OpenAPI 3.0 specification is published and can be loaded in Swagger UI.

Security: API key passed via header or query parameter.

Regional warning areas are identified by codes:
- `esp` = All Spain
- `61` = Andalucía, `62` = Aragón, ... `76` = La Rioja

## Freshness Assessment

- Conventional observations update hourly from AEMET's synoptic network.
- Weather warnings (CAP) are the latest elaborated product, updated in real-time.
- Forecast products update multiple times daily.
- The warning archive goes back to June 2018.

## Entity Model

- **Station**: AEMET station identifier
- **Observation**: Timestamped multi-parameter readings per station
- **Warning (CAP)**: Regional alerts by autonomous community code
- **Forecast**: Location-specific or area-based predictions
- **Fire risk map**: Regional fire weather risk assessment

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Hourly observations, real-time warnings |
| Openness | 2 | Free but requires API key registration |
| Stability | 3 | National meteorological agency with legal open data mandate |
| Structure | 2 | Two-step retrieval adds complexity; data format varies by endpoint |
| Identifiers | 3 | Station codes, regional autonomous community codes, CAP standard |
| Additive Value | 3 | Spain + Canaries + Antarctic; lightning and fire risk data unique |
| **Total** | **16/18** | |

## Notes

- The two-step retrieval pattern (request → get data URL → fetch data) is unusual and adds latency.
- Documentation and API interface are in Spanish.
- The OpenAPI specification is well-maintained and can be used to auto-generate client code.
- CAP (Common Alerting Protocol) warnings follow an international standard.
- Lightning data and fire risk indices are distinctive — not commonly available from other met services.
- Coverage extends to the Canary Islands and even Antarctic stations.
- Rate limits apply (HTTP 429 responses for excessive requests).
