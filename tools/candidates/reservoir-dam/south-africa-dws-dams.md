# South Africa DWS Dam and River Levels

- **Country/Region**: South Africa (plus Lesotho, Eswatini)
- **Endpoint**: `https://www.dws.gov.za/Hydrology/Weekly/ProvinceWeek.aspx?province=Gauteng`
- **Protocol**: HTTP (ASP.NET web scraping required)
- **Auth**: None
- **Format**: HTML (requires parsing), some CSV available via data retrieval
- **Freshness**: Weekly dam level updates; daily/hourly river flow data available
- **Docs**: https://www.dws.gov.za/Hydrology/
- **Score**: 10/18

## Overview

South Africa's Department of Water and Sanitation (DWS) operates an extensive hydrological
monitoring network covering all major dams and river gauging stations. In a water-scarce
country where dam levels make front-page news (remember Cape Town's Day Zero crisis),
this data is critically important.

The system provides:
- **Weekly dam storage levels** by province, water management area, or drainage region
- **Real-time river flow data** from hundreds of gauging stations
- **Municipal water supply** system levels (Cape Town, Johannesburg, Durban, etc.)

The challenge: it's all served through an ageing ASP.NET application with no proper API.

## Endpoint Analysis

**Verified live** — the ProvinceWeek page returns structured HTML with navigation for:

Provincial views: Eastern Cape, Free State, Gauteng, KwaZulu-Natal, Limpopo, Mpumalanga,
Northern Cape, North West, Western Cape, plus Lesotho and Eswatini.

Water Management Areas: Limpopo-Olifants, Inkomati-Usuthu, Pongola-Mtamvuna,
Vaal-Orange, Mzimvubu-Tsitsikamma, Breede-Olifants.

Named supply systems: Algoa, Amathole, Bloemfontein, Cape Town, Crocodile East/West,
IVRS, Orange, Polokwane, Umgeni, uMlathuze.

Data retrieval endpoint for station data:
```
https://www.dws.gov.za/Hydrology/Verified/HyDataSets.aspx?Station=A2H049
```
This returns daily river flow data with 7,000-record limits per query.

**PDF reports** also available: `/Hydrology/Weekly/Weekly.pdf`

## Integration Notes

Building a bridge requires HTML scraping, which is fragile but feasible:

- **Dam levels**: Parse the weekly provincial tables. Each row contains dam name,
  river, capacity (millions of m³), current storage, percentage full, and previous
  year comparison.
- **River flows**: The verified data endpoint serves CSV-like tabular data per station.
  Station codes follow the South African drainage region naming convention (e.g., A2H049).
- **Municipal systems**: Critical supply system dashboards (Cape Town, Johannesburg)
  show aggregated supply vs demand.
- **Scraping strategy**: Use a headless browser or ASP.NET form submission to navigate
  the server-side rendered pages. The URLs are predictable.
- **Alternative**: Look for partners who may have already built APIs on top of this
  (civic tech organizations in SA have attempted this).

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Weekly dam levels, daily river flow |
| Openness | 3 | No auth, government public data |
| Stability | 2 | Ageing ASP.NET infrastructure, occasional 403s |
| Structure | 0 | HTML scraping required, no API |
| Identifiers | 2 | Station codes exist but are SA-specific |
| Richness | 1 | Comprehensive national coverage |
