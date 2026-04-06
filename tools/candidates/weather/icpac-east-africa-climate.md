# ICPAC East Africa Climate Monitoring

- **Country/Region**: East Africa (Kenya, Uganda, Tanzania, Rwanda, Burundi, Ethiopia, Eritrea, Djibouti, Somalia, South Sudan, Sudan)
- **Endpoint**: `https://icpac.net/api/`
- **Protocol**: REST
- **Auth**: Unknown (endpoint unreachable during probing)
- **Format**: JSON (expected)
- **Freshness**: Dekadal (10-day) to monthly
- **Docs**: https://icpac.net/
- **Score**: 8/18

## Overview

The IGAD Climate Prediction and Applications Centre (ICPAC) is the WMO-designated
Regional Climate Centre for East Africa. It provides climate monitoring, seasonal
forecasts, and early warning services for 11 countries in the Greater Horn of Africa.

ICPAC produces:
- **Climate Outlook Forums** (GHACOF): Seasonal rainfall forecasts
- **Dekadal rainfall monitoring**: 10-day rainfall accumulation vs normal
- **Drought monitoring**: SPI, NDVI anomalies
- **Food security linkages**: Climate-food security advisories
- **Extreme weather outlooks**: Sub-seasonal to seasonal forecasts

## Endpoint Analysis

**API endpoint unreachable** during probing (`https://icpac.net/api/` — connection
failed). The ICPAC website is a Django/Wagtail application that likely has REST
endpoints for map data and downloads.

Known ICPAC data products:
| Product | Update Frequency | Format |
|---------|-----------------|--------|
| Rainfall estimates | Dekadal (10-day) | GeoTIFF, maps |
| Temperature anomalies | Monthly | GeoTIFF |
| Drought indicators (SPI) | Monthly | Maps, tabular |
| Seasonal forecast | March, July, October | PDF, maps |
| ENSO outlook | Monthly | PDF |

ICPAC also contributes to:
- **GEOGloWS**: Streamflow forecasts for East African rivers
- **FEWS NET**: Food security early warning
- **IGAD**: Regional climate services

## Integration Notes

- **API exploration needed**: The ICPAC API was unreachable during this research.
  Try again at different times or contact ICPAC directly.
- **Map tile services**: ICPAC may serve climate data through WMS/WFS map services
  rather than REST APIs. Check for GeoServer or MapServer endpoints.
- **Copernicus linkage**: ICPAC uses Copernicus Climate Change Service (C3S) data.
  The C3S API might be more accessible for the same underlying data.
- **Collaboration potential**: ICPAC is interested in improving data access. They've
  participated in hackathons and data challenges.
- **High regional relevance**: For East Africa climate events (droughts, floods, El Niño
  impacts), ICPAC is the authoritative regional voice.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Dekadal to monthly |
| Openness | 1 | API status unclear |
| Stability | 2 | WMO-designated regional centre |
| Structure | 1 | API not verified |
| Identifiers | 1 | Unknown |
| Richness | 2 | Regional climate expertise |
