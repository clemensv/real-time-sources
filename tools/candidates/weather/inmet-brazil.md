# Brazil INMET Open Data

**Country/Region**: Brazil
**Publisher**: INMET (Instituto Nacional de Meteorologia)
**API Endpoint**: `https://apitempo.inmet.gov.br/` (REST API — intermittently available)
**Documentation**: https://portal.inmet.gov.br/manual/manual-de-uso-da-api-de-estações
**Protocol**: REST API
**Auth**: API Token (free registration at portal.inmet.gov.br)
**Data Format**: JSON
**Update Frequency**: Hourly (automatic stations), 3-hourly (conventional stations)
**License**: Brazilian Open Government Data

## What It Provides

INMET operates Brazil's national weather observation network — the largest in South America, covering a continent-sized country (8.5 million km²):

- **Automatic Station Data**: Real-time observations from ~600+ automatic weather stations (estações automáticas). Parameters include:
  - Temperature (instantaneous, max, min)
  - Relative humidity (instantaneous, max, min)
  - Atmospheric pressure
  - Wind speed and direction, gusts
  - Precipitation (accumulated)
  - Solar radiation
  - Dewpoint temperature

- **Conventional Station Data**: Observations from conventional (manually operated) stations at standard synoptic hours.

- **Weather Forecasts**: City-level forecasts for Brazilian state capitals and major cities.

- **Weather Warnings** (Avisos Meteorológicos): Severe weather alerts via alertas2.inmet.gov.br.

- **Agrometeorological Data**: Via SISDAGRO — agricultural weather monitoring including drought indices, frost risk, water balance.

- **Climate Monitoring**: Monthly climate summaries, sea surface temperature monitoring.

## API Details

The INMET API (`apitempo.inmet.gov.br`) provides station data:
```
GET https://apitempo.inmet.gov.br/estacao/dados/{freq}/{station_id}
```

Where `freq` is `T` (all data) or a specific parameter code, and `station_id` is the INMET station code (e.g., A801 for São Paulo).

Station list and metadata available through separate endpoints.

Authentication via token header. Registration at portal.inmet.gov.br.

**Important**: The API has shown intermittent availability during probing — some endpoints returned 404. INMET's API infrastructure appears to be in flux.

## Freshness Assessment

- Automatic stations report hourly.
- Conventional stations report at 3-hourly synoptic intervals (00, 03, 06, 09, 12, 15, 18, 21 UTC).
- The warning system (alertas2.inmet.gov.br) is separate and appears more reliable.
- API availability has been inconsistent — endpoints may be reorganized.

## Entity Model

- **Station**: INMET station code (e.g., A801) + name + state + lat/lon + type (automatic/conventional).
- **Observation**: Multi-parameter readings per station per hour.
- **Forecast**: City-level forecast text.
- **Warning**: Regional alert with severity and type.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Hourly automatic stations, but API availability inconsistent |
| Openness | 2 | Free registration, token auth |
| Stability | 1 | API showed 404 errors during probing; infrastructure appears in transition |
| Structure | 2 | JSON when working, but endpoint organization unclear |
| Identifiers | 2 | INMET station codes, but no clear documentation of the code system |
| Additive Value | 3 | Largest South American network, Amazon/tropical coverage |
| **Total** | **12/18** | |

## Notes

- Brazil's geographic scale is enormous — the station network covers everything from Amazon rainforest to semi-arid Nordeste to subtropical South.
- The API infrastructure appears unstable. INMET may be migrating APIs or reorganizing endpoints.
- The station network includes ~600 automatic stations — impressive for South America but still sparse for a country the size of Brazil.
- The SISDAGRO agricultural weather platform is a unique offering — agricultural meteorology is critical for Brazil's economy (world's largest agricultural exporter).
- Documentation is in Portuguese only.
- Alternative access: INMET data is also available through the BDMEP (Banco de Dados Meteorológicos para Ensino e Pesquisa) historical archive and through WMO GTS via OGIMET.
- Worth revisiting periodically — INMET has been improving its digital infrastructure, and a more stable API may emerge.
