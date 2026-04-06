# SADC Climate Services Centre

- **Country/Region**: Southern Africa (16 SADC member states: Angola, Botswana, Comoros, DRC, Eswatini, Lesotho, Madagascar, Malawi, Mauritius, Mozambique, Namibia, Seychelles, South Africa, Tanzania, Zambia, Zimbabwe)
- **Endpoint**: `https://www.sadc.int/pillars/climate-change-and-climate-services`
- **Protocol**: HTTP (web portal)
- **Auth**: None
- **Format**: HTML, PDF (reports)
- **Freshness**: Monthly to seasonal
- **Docs**: https://www.sadc.int/
- **Score**: 7/18

## Overview

The Southern African Development Community (SADC) Climate Services Centre (CSC)
provides regional climate monitoring and prediction for 16 member states. It produces:

- **Southern Africa Regional Climate Outlook Forum (SARCOF)**: Seasonal rainfall forecasts
  issued before each rainy season
- **Monthly climate bulletins**: Rainfall analysis, drought monitoring
- **Drought early warning**: Regional drought indicators
- **Cyclone advisories**: Indian Ocean cyclone monitoring for coastal states

Southern Africa faces extreme climate variability — from severe droughts (El Niño) to
devastating cyclones (Cyclone Idai 2019, Cyclone Freddy 2023). SADC CSC coordinates
the regional response.

## Endpoint Analysis

**Web portal** — no structured API discovered. SADC publishes reports and maps through
their website. The climate information is embedded in PDF documents rather than
machine-readable APIs.

SADC Climate Data Sources:
- SADC CSC receives data from national met services of all 16 member states
- Uses satellite data from EUMETSAT/Copernicus
- Ingests CPC/NOAA rainfall estimates
- Runs regional climate models

Potential alternative data pathways:
- **Copernicus Climate Data Store**: ECMWF reanalysis data for the SADC region
- **CHIRPS**: Climate Hazards Group InfraRed Precipitation (satellite rainfall estimates)
- **National met services**: Some SADC countries have their own data (SA SAWS, Mauritius MMS)

## Integration Notes

- **No direct API**: SADC CSC does not provide a programmable API. Climate products
  are published as PDF bulletins and map images.
- **PDF parsing approach**: Seasonal outlooks and drought bulletins could be parsed
  from PDFs, but this is fragile and labor-intensive.
- **Better alternatives**: For the underlying climate data, use Copernicus CDS,
  Open-Meteo, or CHIRPS — they cover the same region with API access.
- **SARCOF signal**: The seasonal outlook consensus (issued 3x/year) is a high-value
  signal for agricultural planning and food security. Even as a scraped PDF summary,
  it's worth capturing as a CloudEvent.
- **Future potential**: SADC is investing in digital climate services. API access
  may improve as regional capacity grows.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Seasonal to monthly |
| Openness | 2 | Public website |
| Stability | 2 | SADC regional institution |
| Structure | 0 | No API, PDF/HTML only |
| Identifiers | 0 | None |
| Richness | 2 | Regional climate expertise, 16-country coverage |
