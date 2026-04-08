# South Africa DWS Hydrological Data Network

- **Country/Region**: South Africa
- **Endpoint**: `https://www.dws.gov.za/Hydrology/Unverified` (near-real-time), `https://www.dws.gov.za/Hydrology/Verified/HyDataSets.aspx?Station={StationCode}` (audited)
- **Protocol**: HTTP (ASP.NET web forms)
- **Auth**: None
- **Format**: HTML (tabular data, parseable)
- **Freshness**: Hourly (unverified/preliminary), daily (verified)
- **Docs**: https://www.dws.gov.za/Hydrology/
- **Score**: 10/18

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

## Unverified (Near-Real-Time) Data — Confirmed Live April 2026

The unverified data endpoint at `https://www.dws.gov.za/Hydrology/Unverified` is
the most valuable discovery. It serves **hourly updated** HTML tables for 6 Water
Management Areas (WMAs):

| WMA | Example | Stations |
|-----|---------|:--------:|
| Limpopo-Olifants | WMA1 | ~50+ |
| Inkomati-Usuthu | WMA2 | ~30+ |
| Pongola-Mtamvuna | WMA3 | ~30+ |
| Vaal-Orange | WMA4 | ~80+ |
| Mzimvubu-Tsitsikama | WMA5 | ~40+ |
| Breede-Olifants | WMA6 | ~40+ |

### Sample Live Data (Vaal-Orange, 2026-04-08 05:00)

| Station | Place | Stage (m) | Flow/Cap |
|---------|-------|----------:|:--------:|
| C1R001 | Vaal Dam | 22.837 | 104.03% |
| C9R002 | Bloemhof Dam | 18.301 | 106.02% |
| D3R002 | Gariep Dam | 55.611 | 98.66% |
| D3R003 | Vanderkloof Dam | 61.508 | 103.54% |
| D8H015 | Orange at Sendelingsdrif | 2.448 | 943.55 m³/s |

Columns: Station code, Place name, Date/Time, Stage (m), Flow or Capacity (%),
Spill indicator, Comment. Blue-highlighted rows indicate dams (capacity shown as %).

### Station Code Convention

- First letter: Drainage region (A–X)
- Number: Sub-catchment
- H = flow gauging station, R = reservoir/dam, M = rainfall

### Additional Endpoints

- **Weekly dam state**: `https://www.dws.gov.za/Hydrology/Weekly/Province.aspx` —
  ~210 dams by province or WMA, updated weekly
- **Daily Orange/Vaal**: `https://www.dws.gov.za/Hydrology/Daily/Default.aspx` —
  daily dam/flow/rainfall chart for the Vaal-Orange system
- **Dam optimization**: `https://www.dws.gov.za/Hydrology/Unverified/Home/DamOpt?stanum={code}` —
  routing through specific dams (inflow, outflow, capacity)

### Scraping Approach

The unverified data pages render as simple HTML tables selectable by WMA via a
dropdown. The tables use a consistent `Station | Place | Date/Time | Stage | Flow/Cap | Spill | Comment`
structure. No AJAX, no ViewState tokens needed for the unverified pages — they're
straightforward GET requests with a query parameter for the WMA.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Hourly unverified, daily verified |
| Openness | 3 | No auth, government data |
| Stability | 1 | Ageing ASP.NET infrastructure |
| Structure | 1 | HTML scraping required, but tables are simple |
| Identifiers | 2 | Station codes (SA-specific convention) |
| Richness | 1 | Flow rates, levels, dam capacity, spill |
