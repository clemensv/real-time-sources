# South Africa DWS Hydrological Data Network

- **Country/Region**: South Africa
- **Endpoint**: `https://www.dws.gov.za/Hydrology/Verified/HyDataSets.aspx?Station={StationCode}`
- **Protocol**: HTTP (ASP.NET web forms)
- **Auth**: None
- **Format**: HTML (tabular data, parseable)
- **Freshness**: Daily flow data (verified), near-real-time (unverified/preliminary)
- **Docs**: https://www.dws.gov.za/Hydrology/
- **Score**: 9/18

## Overview

South Africa operates one of the most extensive hydrological monitoring networks in
Africa, with hundreds of river flow gauging stations managed by the Department of Water
and Sanitation (DWS). These stations monitor river flows, water levels, and water
quality across all major drainage regions.

The data is critical for:
- **Water resource management**: Allocation decisions for agriculture, mining, cities
- **Flood early warning**: Real-time flow monitoring for flood-prone catchments
- **Hydropower**: Flow data for hydro generation planning
- **Environmental flows**: Ecological reserve management

## Endpoint Analysis

**Verified live** — the HyDataSets endpoint accepts station codes and returns data
retrieval parameters:

```
Station: A2H049
Data limits: 7,000 records per query or 1 year per daily data request
              20 years for daily aggregated data
```

Station naming convention:
- First letter = Drainage region (A through X)
- Number = Sub-catchment identifier
- Letter suffix = Station type (H = flow, M = rain, R = reservoir)

Example stations:
| Code | Description | Type |
|------|-------------|------|
| A2H049 | Crocodile River | River flow |
| C5H003 | Vaal River at Vaal Dam | River flow |
| X2H016 | Limpopo River | River flow |

The system also provides:
- Station photos
- Data quality indicators
- Catchment area information
- Latitude/longitude coordinates

## Integration Notes

- **Scraping required**: No REST API exists. The ASP.NET web forms require POST
  requests with ViewState tokens and form parameters.
- **Station discovery**: The drainage region index pages list all stations per region.
  Scrape these to build a station inventory.
- **Data retrieval**: Submit form POST requests per station to retrieve CSV-format
  daily flow data. Parse the response HTML tables.
- **Preliminary vs verified**: DWS publishes both preliminary (near-real-time) and
  verified (quality-controlled) data. Preliminary is faster but less reliable.
- **High value target**: Despite the technical difficulty, this is the most comprehensive
  open river flow dataset in Africa. Worth the scraping investment.
- **Complement with satellite**: Use satellite altimetry data (Copernicus) for major
  rivers where ground stations are sparse.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Daily flow data, preliminary available faster |
| Openness | 3 | No auth, government data |
| Stability | 1 | Ageing ASP.NET infrastructure |
| Structure | 0 | HTML scraping required |
| Identifiers | 2 | Station codes (SA-specific convention) |
| Richness | 1 | Flow rates, levels, basic metadata |
